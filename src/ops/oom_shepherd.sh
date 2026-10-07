#!/bin/bash
# Shepherd v2: (a) every 60s tag all solvers as preferred OOM victims
# (resumable; sessions/apps are not); (b) hourly, snapshot irreplaceable
# resume-state (summaries + done-cube lists) from the /tmp scratchpad to
# disk-backed runstate/ so a reboot costs hours, not days.
SP=/tmp/claude-1000/-home-maria-projects-erdos-gyarfas/c144a1df-3cfa-4083-9296-c8d234dd9732/scratchpad
RS=/home/maria/projects/erdos-gyarfas/.claude/worktrees/other-approaches/runstate
mkdir -p "$RS"
c=0
while true; do
  for p in $(pgrep -f 'smsg --[v]ertices'); do choom -p "$p" -n 900 >/dev/null 2>&1; done
  if [ $((c % 60)) -eq 0 ]; then
    for d in b0_ladder b0_race b0_capped b0_capped_cube b0_p16 b0_p16cube; do
      [ -f "$SP/$d/summary.txt" ] && cp "$SP/$d/summary.txt" "$RS/${d}_summary.txt"
    done
    grep -l "All cubes processed" "$SP"/b0_n33race/cube_*.log 2>/dev/null \
      | grep -oP 'cube_\K\d+' | sort -n > "$RS/n33race_done_cubes.txt"
    grep -l "All cubes processed" "$SP"/b0_p16cube/n34/percube/cube_*.log 2>/dev/null \
      | grep -oP 'cube_\K\d+' | sort -n > "$RS/n34_done_cubes.txt"
    grep -l "All cubes processed" "$SP"/b0_p16cube/n34/shard*.log 2>/dev/null \
      | grep -oP 'shard\K\d+' | sort -n > "$RS/n34_done_shards.txt"
    grep -l "All cubes processed" "$SP"/b0_capped_cube/n46/shard*.log 2>/dev/null \
      | grep -oP 'shard\K\d+' | sort -n > "$RS/capped46_done_shards.txt"
    date -u +"%FT%TZ" > "$RS/LAST_SNAPSHOT"
  fi
  c=$((c+1))
  sleep 60
done
