#!/bin/bash
# SMS frontier replication: one smsg per n, forbidding all power-of-2 cycles <= n,
# min-degree-3 CNF from pysms. Usage: sms_frontier.sh <venv> <outdir> <n1> [n2 ...]
# Runs sizes in parallel (one thread each), niced.
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
with open(cnf, "w") as f:
    b.print_dimacs(f)
PYEOF
    : > "$cyc"
    local L=4
    while [ "$L" -le "$n" ]; do
        {
            printf '%d' "$L"
            for i in $(seq 0 $((L-1))); do printf ' %d %d' "$i" $(( (i+1) % L )); done
            printf '\n'
        } >> "$cyc"
        L=$((L*2))
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
echo "=== SMS frontier sweep complete ==="
sort -t= -k2 -n "$OUT/summary.txt"
