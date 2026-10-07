#!/bin/bash
# B0-block ladder: one smsg per n over the "min-deg >= 2, at most one deg-2
# vertex" space (encode_b0.py), forbidding all power-of-2 cycles <= n.
# Usage: b0_frontier.sh <venv> <outdir> <n1> [n2 ...]   (one thread per n)
# Optional: CAP=31 additionally forbids every cycle length in [CAP+1 .. n]
# (circumference-capped variant: any SAT hit is an alpha-block outright,
# since all powers of 2 above CAP are vacuously absent).
set -uo pipefail
VENV=$1; OUT=$2; shift 2
SRC=$(cd "$(dirname "$0")" && pwd)
export PATH="$HOME/.local/bin:$PATH"
export LD_LIBRARY_PATH="$HOME/.local/lib:${LD_LIBRARY_PATH:-}"
mkdir -p "$OUT"

run_one() {
    local n=$1
    local cnf="$OUT/enc_$n.cnf" cyc="$OUT/cyc_$n.txt" log="$OUT/n$n.log"
    "$VENV/bin/python" "$SRC/encode_b0.py" "$n" > "$cnf" || { echo "n=$n ENCODE_FAIL" >> "$OUT/summary.txt"; return; }
    : > "$cyc"
    emit_cycle() {
        printf '%d' "$1"
        for i in $(seq 0 $(($1-1))); do printf ' %d %d' "$i" $(( (i+1) % $1 )); done
        printf '\n'
    }
    local L=4
    while [ "$L" -le "$n" ] && { [ -z "${CAP:-}" ] || [ "$L" -le "$CAP" ]; } \
          && { [ -z "${PMAX:-}" ] || [ "$L" -le "$PMAX" ]; }; do
        emit_cycle "$L" >> "$cyc"
        L=$((L*2))
    done
    # PMAX caps the forbidden-pattern lengths (e.g. PMAX=16 skips the C32
    # pattern, whose propagator is Hamiltonian-sized at n=32). Sound for
    # UNSAT (larger space); a count>0 result needs post-filtering for the
    # skipped lengths (p2check).
    if [ -n "${CAP:-}" ]; then
        for (( L=CAP+1; L<=n; L++ )); do emit_cycle "$L" >> "$cyc"; done
    fi
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
echo "=== B0 ladder sweep complete ==="
sort -t= -k2 -n "$OUT/summary.txt"
