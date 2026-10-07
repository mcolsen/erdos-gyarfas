#!/bin/bash
# Cube-and-conquer B0 ladder rung: generate SMS cubes, solve range-shards in
# parallel. Sound: cubes partition the space (validated count-exactly at n=10:
# shard-sum == plain count == geng count); a shard counts as done ONLY if its
# log contains "All cubes processed" (a zero-solution shard prints no count
# line); failed shards are retried once, else the rung is marked FAILED.
# Usage: b0_cube_rung.sh <venv> <outdir> <n> <cutoff> <nshards> [wait-pattern]
#   wait-pattern: optional pgrep -f pattern; shard phase waits until it clears.
set -uo pipefail
VENV=$1; OUT=$2; n=$3; CUTOFF=$4; NSH=$5; WAITPAT=${6:-}
SRC=$(cd "$(dirname "$0")" && pwd)
export PATH="$HOME/.local/bin:$PATH"
export LD_LIBRARY_PATH="$HOME/.local/lib:${LD_LIBRARY_PATH:-}"
mkdir -p "$OUT/n$n"
cnf="$OUT/n$n/enc.cnf" cyc="$OUT/n$n/cyc.txt"
"$VENV/bin/python" "$SRC/encode_b0.py" "$n" > "$cnf"
: > "$cyc"
emit_cycle() {
    printf '%d' "$1"
    for i in $(seq 0 $(($1-1))); do printf ' %d %d' "$i" $(( (i+1) % $1 )); done
    printf '\n'
}
L=4
while [ "$L" -le "$n" ] && { [ -z "${CAP:-}" ] || [ "$L" -le "$CAP" ]; } \
      && { [ -z "${PMAX:-}" ] || [ "$L" -le "$PMAX" ]; }; do
    emit_cycle "$L" >> "$cyc"
    L=$((L*2))
done
# PMAX caps pattern lengths (UNSAT-sound; count>0 needs post-filter p2check).
# CAP=31 additionally forbids every length in [CAP+1..n] (circumference-capped
# cell, same semantics as b0_frontier.sh: a SAT hit is an alpha-block outright).
if [ -n "${CAP:-}" ]; then
    for (( L=CAP+1; L<=n; L++ )); do emit_cycle "$L" >> "$cyc"; done
fi

t0=$SECONDS
# 1. cube generation (auto-tune cutoff upward if too few cubes)
co=$CUTOFF
while :; do
    nice -n 10 smsg --vertices "$n" --all-graphs --forbidden-subgraph-file "$cyc" \
        --dimacs "$cnf" --simple-assignment-cutoff "$co" > "$OUT/n$n/gen.log" 2>&1
    grep -aoP '^a .*0$' "$OUT/n$n/gen.log" > "$OUT/n$n/cubes.txt" || true
    nc=$(wc -l < "$OUT/n$n/cubes.txt")
    [ "$nc" -ge 200 ] || [ "$co" -ge $((CUTOFF+18)) ] && break
    co=$((co+6))
done
gencount=$(grep -oP 'Number of graphs:\s*\K\d+' "$OUT/n$n/gen.log" | tail -1)
echo "n=$n cubes=$nc (cutoff=$co) gen-solutions=${gencount:-0} gen-time=$((SECONDS-t0))s"

# 2. optional wait for machine capacity
if [ -n "$WAITPAT" ]; then
    while pgrep -f "$WAITPAT" >/dev/null; do sleep 120; done
fi

# 3. sharded solve with retry
run_shard() {
    local i=$1 lo=$2 hi=$3 log="$OUT/n$n/shard$1.log"
    nice -n 10 smsg --vertices "$n" --all-graphs --forbidden-subgraph-file "$cyc" \
        --dimacs "$cnf" --cube-file "$OUT/n$n/cubes.txt" --cubes-range "$lo" "$hi" > "$log" 2>&1
}
per=$(( (nc + NSH - 1) / NSH ))
for i in $(seq 0 $((NSH-1))); do
    lo=$((i*per)); hi=$(( (i+1)*per )); [ "$hi" -gt "$nc" ] && hi=$nc
    [ "$lo" -ge "$hi" ] && continue
    run_shard "$i" "$lo" "$hi" &
done
wait
total=${gencount:-0}; bad=""
for i in $(seq 0 $((NSH-1))); do
    log="$OUT/n$n/shard$i.log"; [ -f "$log" ] || continue
    if ! grep -q "All cubes processed" "$log"; then
        lo=$((i*per)); hi=$(( (i+1)*per )); [ "$hi" -gt "$nc" ] && hi=$nc
        echo "n=$n shard $i FAILED - retrying"
        run_shard "$i" "$lo" "$hi"
        grep -q "All cubes processed" "$log" || { bad="$bad $i"; continue; }
    fi
    c=$(grep -oP 'Number of graphs:\s*\K\d+' "$log" | tail -1)
    total=$((total + ${c:-0}))
done
el=$((SECONDS - t0))
if [ -n "$bad" ]; then
    echo "n=$n FAILED shards:$bad elapsed=${el}s" | tee -a "$OUT/summary.txt"
else
    echo "n=$n rc=cube count=$total elapsed=${el}s shards=$NSH cubes=$nc" | tee -a "$OUT/summary.txt"
    if [ "$total" -gt 0 ]; then
        echo "!!! n=$n SAT: $total graph(s) - inspect $OUT/n$n/*.log for witnesses !!!" | tee -a "$OUT/summary.txt"
    fi
fi
