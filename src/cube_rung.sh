#!/bin/bash
# Cube-and-conquer SMS rung: count cubic (3-regular) graphs on n vertices
# avoiding the given cycle lengths, parallelized via smsg cube splitting.
# Productionized from the gate-validated 2026-07-31 pipeline (see
# notes/cube-and-conquer.md for the validation record and semantics traps).
#
# Usage: cube_rung.sh <venv> <outdir> <n> [lengths] [cutstart]
#   venv     python venv with pysms (sms_graph_builder)
#   outdir   working+output directory (created; safe to re-run: resumes)
#   n        vertex count
#   lengths  forbidden cycle lengths, default "4 8 16"
#   cutstart initial --simple-assignment-cutoff for cube gen, default 36
#
# Output: $outdir/RESULT.txt (machine-readable aggregate) and a verdict line
#   "n=<n> rc=OK|INCOMPLETE|GENFAIL count=<total> mode=cube ..." appended to
#   $outdir/summary.txt. Zero-count shards hide nothing: shard logs keep any
#   witness graphs (workers run without --hide-graphs).
#
# SOUNDNESS (validated count-exactly, 251=Markström at n=28 {4,8}, two
# granularities + unit-clause cross-path):
#   * worker i consumes cube i via --cube-line $((i+1)) (1-INDEXED; never use
#     --cubes-range for singletons: ranges are 1-indexed AND INCLUSIVE, and
#     "0 1" is a silent no-op with no count line);
#   * worker i's CNF carries blocking clauses of cubes 0..i-1, making cube
#     regions a partition of the solution space by construction;
#   * total = solutions found during cube generation + sum of shard counts;
#   * healthy cube-consumption exit code is 0 (monolith smsg exits 20);
#     a missing count line surfaces as PARSE_FAIL and fails the rung.
set -uo pipefail
export PATH="$HOME/.local/bin:$PATH"
export LD_LIBRARY_PATH="$HOME/.local/lib:${LD_LIBRARY_PATH:-}"
VENV=$1; OUT=$2; N=$3
LENGTHS=${4:-"4 8 16"}
CUTSTART=${5:-36}
mkdir -p "$OUT/shards"
T0=$SECONDS
P=$(( $(nproc) - $(pgrep -cx smsg || echo 0) - 4 ))
[ "$P" -lt 8 ] && P=8
[ "$P" -gt 40 ] && P=40

# --- encoding (idempotent) ---
if [ ! -s "$OUT/enc.cnf" ]; then
    "$VENV/bin/python" - "$N" "$OUT/enc.cnf" <<'PYEOF'
import sys
from pysms.graph_builder import GraphEncodingBuilder
n, cnf = int(sys.argv[1]), sys.argv[2]
b = GraphEncodingBuilder(n, directed=False)
b.minDegree(3)
b.maxDegree(3)
with open(cnf, "w") as f:
    b.print_dimacs(f)
PYEOF
fi
if [ ! -s "$OUT/cyc.txt" ]; then
    : > "$OUT/cyc.txt"
    for L in $LENGTHS; do
        [ "$L" -le "$N" ] || continue
        { printf '%d' "$L"
          for i in $(seq 0 $((L-1))); do printf ' %d %d' "$i" $(( (i+1) % L )); done
          printf '\n'
        } >> "$OUT/cyc.txt"
    done
fi

mkblocked() {  # $1=base cnf  $2=cubes file  $3=#leading cubes to block  $4=out cnf
    python3 - "$1" "$2" "$3" "$4" <<'PYEOF'
import sys
base, cubes, k, out = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
with open(base) as f:
    lines = f.readlines()
hdr = next(j for j, ln in enumerate(lines) if ln.startswith("p cnf"))
parts = lines[hdr].split()
nv, ncl = int(parts[2]), int(parts[3])
block = []
with open(cubes) as f:
    for i, ln in enumerate(f):
        if i >= k:
            break
        lits = ln.split()[1:-1]
        block.append(" ".join(str(-int(x)) for x in lits) + " 0\n")
lines[hdr] = f"p cnf {nv} {ncl + len(block)}\n"
with open(out, "w") as f:
    f.writelines(lines)
    f.writelines(block)
PYEOF
}
export -f mkblocked

# --- cube generation, auto-tuned cutoff (idempotent) ---
if [ ! -s "$OUT/cubes.txt" ]; then
    CUT=$CUTSTART
    for try in 1 2 3 4; do
        echo "[gen] try $try cutoff=$CUT $(date -Is)" >> "$OUT/driver.log"
        smsg --vertices "$N" --all-graphs --hide-graphs \
            --forbidden-subgraph-file "$OUT/cyc.txt" \
            --dimacs "$OUT/enc.cnf" --simple-assignment-cutoff $CUT \
            > "$OUT/gen_cut$CUT.log" 2>&1
        grep -aoP '^a( -?\d+)+ 0$' "$OUT/gen_cut$CUT.log" > "$OUT/cubes_cut$CUT.txt"
        NC=$(wc -l < "$OUT/cubes_cut$CUT.txt")
        echo "[gen] cutoff=$CUT -> $NC cubes" >> "$OUT/driver.log"
        if [ "$NC" -ge 500 ] && [ "$NC" -le 30000 ]; then
            cp "$OUT/cubes_cut$CUT.txt" "$OUT/cubes.txt"
            echo "$CUT" > "$OUT/CUTOFF.txt"
            break
        elif [ "$NC" -lt 500 ]; then
            CUT=$((CUT + 12))
        else
            CUT=$((CUT - 12))
        fi
    done
fi
[ -s "$OUT/cubes.txt" ] || { echo "n=$N rc=GENFAIL count=NA mode=cube elapsed=$((SECONDS-T0))s" >> "$OUT/summary.txt"; exit 1; }
CUT=$(cat "$OUT/CUTOFF.txt")
NC=$(wc -l < "$OUT/cubes.txt")
GENC=$(grep -oP 'Number of graphs:\s*\K\d+' "$OUT/gen_cut$CUT.log" | tail -1)
GENC=${GENC:-0}

# --- per-cube worker queue (idempotent: .res files persist) ---
export OUT N
seq 0 $((NC-1)) | xargs -P $P -I{} bash -c '
    i={}
    [ -s "$OUT/shards/c$i.res" ] && exit 0
    T=$OUT/shards/c$i.cnf
    mkblocked "$OUT/enc.cnf" "$OUT/cubes.txt" "$i" "$T"
    nice -n 10 smsg --vertices $N --all-graphs \
        --forbidden-subgraph-file "$OUT/cyc.txt" --dimacs "$T" \
        --cube-file "$OUT/cubes.txt" --cube-line $((i+1)) \
        > "$OUT/shards/c$i.log" 2>&1
    rc=$?
    rm -f "$T"
    c=$(grep -oP "Number of graphs:\s*\K\d+" "$OUT/shards/c$i.log" | tail -1)
    echo "$i rc=$rc count=${c:-PARSE_FAIL}" > "$OUT/shards/c$i.res"
'

# --- aggregate ---
NRES=$(ls "$OUT"/shards/*.res 2>/dev/null | wc -l)
BAD=$(cat "$OUT"/shards/*.res | grep -cv 'rc=0 count=[0-9]' || true)
SUM=$(cat "$OUT"/shards/*.res | grep -oP 'count=\K\d+' | paste -sd+ | bc)
TOT=$((SUM + GENC))
T=$((SECONDS - T0))
{
    echo "n=$N lengths='$LENGTHS' cubes=$NC cutoff=$CUT res=$NRES bad=$BAD gen_count=$GENC shard_sum=$SUM TOTAL=$TOT elapsed=${T}s"
    echo "DONE $(date -Is)"
} >> "$OUT/RESULT.txt"
if [ "$NRES" -eq "$NC" ] && [ "$BAD" -eq 0 ]; then
    echo "n=$N rc=OK count=$TOT mode=cube cubes=$NC elapsed=${T}s" >> "$OUT/summary.txt"
else
    echo "n=$N rc=INCOMPLETE count=$TOT mode=cube res=$NRES/$NC bad=$BAD elapsed=${T}s" >> "$OUT/summary.txt"
fi
