#!/bin/bash
# n=34 per-cube pool over ranges of shards without "All cubes processed".
# Resumable per cube; writes the rung summary line when every cube is done.
SP=/tmp/claude-1000/-home-maria-projects-erdos-gyarfas/c144a1df-3cfa-4083-9296-c8d234dd9732/scratchpad
D=$SP/b0_p16cube/n34; nc=1985; per=125
t0=$SECONDS
mkdir -p "$D/percube"
: > "$D/percube/jobs.txt"
for i in $(seq 0 15); do
  grep -q "All cubes processed" "$D/shard$i.log" 2>/dev/null && continue
  lo=$((i*per)); hi=$(( (i+1)*per )); [ $hi -gt $nc ] && hi=$nc
  seq "$lo" $((hi-1)) >> "$D/percube/jobs.txt"
done
xargs -a "$D/percube/jobs.txt" -n1 -P 6 sh -c '
  SP=/tmp/claude-1000/-home-maria-projects-erdos-gyarfas/c144a1df-3cfa-4083-9296-c8d234dd9732/scratchpad
  D=$SP/b0_p16cube/n34; i=$0; log="$D/percube/cube_$i.log"
  [ -s "$log" ] && grep -q "All cubes processed" "$log" && exit 0
  nice -n 10 smsg --vertices 34 --all-graphs --forbidden-subgraph-file "$D/cyc.txt" \
    --dimacs "$D/enc.cnf" --cube-file "$D/cubes.txt" --cubes-range "$i" "$((i+1))" > "$log" 2>&1
'
total=0; bad=0
for i in $(seq 0 15); do
  if grep -q "All cubes processed" "$D/shard$i.log" 2>/dev/null; then
    c=$(grep -oP 'Number of graphs:\s*\K\d+' "$D/shard$i.log" | tail -1); total=$((total + ${c:-0}))
  fi
done
while read -r i; do
  log="$D/percube/cube_$i.log"
  grep -q "All cubes processed" "$log" 2>/dev/null || { bad=$((bad+1)); continue; }
  c=$(grep -oP 'Number of graphs:\s*\K\d+' "$log" | tail -1); total=$((total + ${c:-0}))
done < "$D/percube/jobs.txt"
el=$((SECONDS-t0))
if [ "$bad" -gt 0 ]; then
  echo "n=34 PERCUBE-INCOMPLETE badcubes=$bad elapsed=${el}s" | tee -a "$SP/b0_p16cube/summary.txt"
else
  echo "n=34 rc=cube count=$total elapsed=${el}s(percube) shards=5+percube cubes=1985" | tee -a "$SP/b0_p16cube/summary.txt"
  if [ "$total" -gt 0 ]; then
    echo "!!! n=34 SAT: $total graph(s) - see $D !!!" | tee -a "$SP/b0_p16cube/summary.txt"
  fi
fi
