#!/bin/bash
# Count-exact validation gate for the cube-and-conquer pipeline.
# Runs cube_rung.sh on the {C4,C8}-free cubic count at n=28, which must be
# EXACTLY 251 (Markström's published count, reproduced by the phase-1 geng
# stack). Run this after ANY change to smsg, pysms, or cube_rung.sh, and
# before trusting a new rung. Exit 0 = PASS, 1 = FAIL.
#
# CAUTION: do NOT "simplify" this gate to the {4,8,16} set — that count is
# genuinely 0 at small n (frontier), which validates nothing. A positive
# reference count is the point.
#
# Usage: cube_gate.sh <venv> <outdir>
set -uo pipefail
VENV=$1; OUT=$2
SRC="$(cd "$(dirname "$0")" && pwd)"
rm -rf "$OUT"
"$SRC/cube_rung.sh" "$VENV" "$OUT" 28 "4 8" 20
LINE=$(tail -1 "$OUT/summary.txt")
COUNT=$(grep -oP 'count=\K\d+' <<<"$LINE" || true)
if grep -q 'rc=OK' <<<"$LINE" && [ "$COUNT" = "251" ]; then
    echo "GATE PASS: $LINE (expect count=251)"
    exit 0
else
    echo "GATE FAIL: $LINE (expect rc=OK count=251)"
    exit 1
fi
