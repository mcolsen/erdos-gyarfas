#!/bin/bash
# Snapshot the n=48 cube-tree bookkeeping and final evidence out of tmpfs.
# /tmp is tmpfs on this machine: a reboot/power outage destroys all running
# solvers AND their ledgers. This captures everything needed to resume
# (verdict lines, per-cell .res ledgers, cube sets, encodings) — a few MB —
# while skipping bulk shard logs and per-shard CNFs (regenerable).
# Usage: snapshot_n48.sh [scratchpad_runs_dir] [output.tar.gz]
set -euo pipefail
RUNS=${1:-/tmp/claude-1000/-home-maria-projects-erdos-gyarfas--claude-worktrees-algebra/e397a738-ce4d-43e7-a8c4-3397853029a5/scratchpad/runs}
WORK=$(dirname "$RUNS")/work
REPO="$(cd "$(dirname "$0")/.." && pwd)"
TS=$(date +%Y%m%d_%H%M)
OUT=${2:-$REPO/results/n48_state_$TS.tar.gz}
cd "$RUNS"
FILES=$(ls -1 \
    sms4648/summary.txt sms4648/enc_48.cnf sms4648/cyc_48.txt sms4648/n46.log sms4648/n48.log \
    2>/dev/null; \
    find cube48 cube0split $(ls -d c0s* 2>/dev/null | tr '\n' ' ') cubeval28 gate_repo gateD unitprobe \
        -maxdepth 2 \( -name 'summary.txt' -o -name 'RESULT.txt' -o -name 'PROBE.txt' \
        -o -name 'SMOKE.txt' -o -name 'cubes.txt' -o -name 'CUTOFF.txt' \
        -o -name 'driver.log' -o -name '*.res' \) 2>/dev/null)
DRIVERS=()
for driver in cube48_driver.sh cube0split.sh subsplit.sh unitprobe.sh; do
    [ -f "$WORK/$driver" ] && DRIVERS+=("$driver")
done
if [ ${#DRIVERS[@]} -gt 0 ]; then
    echo "$FILES" | tar czf "$OUT" -T - -C "$WORK" "${DRIVERS[@]}"
else
    echo "$FILES" | tar czf "$OUT" -T -
fi
(cd "$(dirname "$OUT")" && sha256sum "$(basename "$OUT")" > "$(basename "$OUT").sha256")
echo "snapshot: $OUT ($(du -h "$OUT" | cut -f1)) - $(echo "$FILES" | wc -l) result files + ${#DRIVERS[@]} drivers"
