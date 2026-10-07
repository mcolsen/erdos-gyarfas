#!/bin/bash
# Per-cube race over n33 stuck shard ranges [1044,1305)+[1566,1827).
# Resumable: done cube logs are skipped. No kills anywhere in this script.
SP=/tmp/claude-1000/-home-maria-projects-erdos-gyarfas/c144a1df-3cfa-4083-9296-c8d234dd9732/scratchpad
D=$SP/b0_n33race; N33=$SP/b0_p16cube/n33
: > "$D/jobs.txt"
for i in $(seq 1044 1304) $(seq 1566 1826); do echo "$i" >> "$D/jobs.txt"; done
xargs -a "$D/jobs.txt" -n1 -P 8 sh -c '
  SP=/tmp/claude-1000/-home-maria-projects-erdos-gyarfas/c144a1df-3cfa-4083-9296-c8d234dd9732/scratchpad
  D=$SP/b0_n33race; N33=$SP/b0_p16cube/n33; i=$0; log="$D/cube_$i.log"
  [ -s "$log" ] && grep -q "All cubes processed" "$log" && exit 0
  nice -n 10 smsg --vertices 33 --all-graphs --forbidden-subgraph-file "$N33/cyc.txt" \
    --dimacs "$N33/enc.cnf" --cube-file "$N33/cubes.txt" --cubes-range "$i" "$((i+1))" > "$log" 2>&1
'
bad=0; total=0
for i in $(seq 1044 1304) $(seq 1566 1826); do
  log="$D/cube_$i.log"
  grep -q "All cubes processed" "$log" 2>/dev/null || { bad=$((bad+1)); continue; }
  c=$(grep -oP 'Number of graphs:\s*\K\d+' "$log" | tail -1); total=$((total + ${c:-0}))
done
if [ "$bad" -gt 0 ]; then
  echo "n33race INCOMPLETE badcubes=$bad total_so_far=$total" | tee -a "$SP/b0_race/summary.txt"
else
  echo "n33race rc=cube count=$total cubes=522 ranges=1044-1304,1566-1826" | tee -a "$SP/b0_race/summary.txt"
  [ "$total" -gt 0 ] && echo "!!! n33race SAT: $total graph(s) - see $D/cube_*.log !!!" | tee -a "$SP/b0_race/summary.txt"
fi
