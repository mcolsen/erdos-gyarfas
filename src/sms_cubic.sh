#!/bin/bash
# Cubic {C4,C8,C16}-free SMS ladder rung(s): count cubic graphs on n vertices
# with no cycle of length 4, 8, or 16 (extends the phase-1 ladder n<=44).
# Usage: sms_cubic.sh <venv> <outdir> <n1> [n2 ...]
set -uo pipefail
VENV=$1; OUT=$2; shift 2
export PATH="$HOME/.local/bin:$PATH"
export LD_LIBRARY_PATH="$HOME/.local/lib:${LD_LIBRARY_PATH:-}"
mkdir -p "$OUT"

run_one() {
    local n=$1
    local cnf="$OUT/enc_$n.cnf" cyc="$OUT/cyc_$n.txt" log="$OUT/n$n.log"
    "$VENV/bin/python" - "$n" "$cnf" <<'PYEOF'
import sys
from pysms.graph_builder import GraphEncodingBuilder
n, cnf = int(sys.argv[1]), sys.argv[2]
b = GraphEncodingBuilder(n, directed=False)
b.minDegree(3)
b.maxDegree(3)
with open(cnf, "w") as f:
    b.print_dimacs(f)
PYEOF
    : > "$cyc"
    for L in 4 8 16; do
        [ "$L" -le "$n" ] || continue
        {
            printf '%d' "$L"
            for i in $(seq 0 $((L-1))); do printf ' %d %d' "$i" $(( (i+1) % L )); done
            printf '\n'
        } >> "$cyc"
    done
    local t0=$SECONDS
    nice -n 10 smsg --vertices "$n" --all-graphs --hide-graphs \
        --forbidden-subgraph-file "$cyc" --dimacs "$cnf" > "$log" 2>&1
    local rc=$? t=$((SECONDS - t0))
    local count
    count=$(grep -oP 'Number of graphs:\s*\K\d+' "$log" | tail -1)
    echo "n=$n rc=$rc count=${count:-PARSE_FAIL} elapsed=${t}s" >> "$OUT/summary.txt"
    echo "n=$n done: count=${count:-PARSE_FAIL} (${t}s)"
}

for n in "$@"; do
    run_one "$n" &
done
wait
echo "=== cubic SMS rungs complete ==="
sort "$OUT/summary.txt"
