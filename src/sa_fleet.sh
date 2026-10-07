#!/bin/bash
# Self-healing SA fleet: keeps one sa_hunt chain alive per spec until each has
# printed a 'done:' line (or found a counterexample, exit 42 -> 'FOUND' marker).
# Usage: sa_fleet.sh BIN OUTDIR MOVES n:seed [n:seed ...]
BIN=$1; OUT=$2; MOVES=$3; shift 3
mkdir -p "$OUT"
while :; do
    alldone=1
    for spec in "$@"; do
        n=${spec%%:*}; s=${spec##*:}
        log="$OUT/n${n}_s${s}.log" g6="$OUT/n${n}_s${s}.g6"
        grep -q 'done:\|COUNTEREXAMPLE' "$log" 2>/dev/null && continue
        alldone=0
        if ! pgrep -f "$(basename "$BIN") $n $s " > /dev/null; then
            echo "[fleet $(date +%H:%M:%S)] (re)launching n=$n seed=$s" >> "$OUT/fleet.log"
            nice -n 12 "$BIN" "$n" "$s" "$MOVES" >> "$g6" 2>> "$log" &
        fi
    done
    [ "$alldone" = 1 ] && { echo "[fleet] all chains done" >> "$OUT/fleet.log"; exit 0; }
    sleep 60
done
