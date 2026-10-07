#!/bin/bash
# Sharded geng_p2 run: run_shards.sh <binary> <outdir> <mod> <geng flags...>
# Env: P2_LENGTHS passes through to the plugin. Shards run niced at ~mod-way
# parallelism; per-shard graph6 goes to <outdir>/shard_<i>.g6, stderr (with the
# >Z count line) to <outdir>/shard_<i>.log. Prints total generated at the end.
set -euo pipefail
BINARY=$1; OUTDIR=$2; MOD=$3; shift 3
mkdir -p "$OUTDIR"
for i in $(seq 0 $((MOD-1))); do
    nice -n 10 "$BINARY" "$@" $i/$MOD "$OUTDIR/shard_$i.g6" \
        2> "$OUTDIR/shard_$i.log" &
done
wait
cat "$OUTDIR"/shard_*.g6 > "$OUTDIR/all.g6" || true
TOTAL=$(grep -h '>Z' "$OUTDIR"/shard_*.log | awk '{s+=$2} END {print s}')
echo "TOTAL_GENERATED=$TOTAL  (survivors in $OUTDIR/all.g6: $(wc -l < "$OUTDIR/all.g6"))"
