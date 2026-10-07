# Runbook — B0 / capped-cell execution archive

Historical execution record for the runs archived in `STATUS.md`. No job is
currently active. The commands and original scratch paths below are retained
for forensic reference; the source and lane
history are now on `main`.

## Where state lives

| place | contents | durability |
|---|---|---|
| repo `results/`, `REPORT-other-approaches.md`, `STATUS.md`, `notes/` | verdicts, records, method notes | permanent (pushed) |
| repo `src/` | encoders + drivers (`encode_b0.py`, `b0_frontier.sh`, `b0_cube_rung.sh`) | permanent |
| repo `src/ops/` | archived pool scripts (race, per-cube, shepherd) | permanent |
| scratchpad `SP=/tmp/claude-1000/-home-maria-projects-erdos-gyarfas/c144a1df-3cfa-4083-9296-c8d234dd9732/scratchpad` | original runs: encodings, cube files, per-cube logs, `*/summary.txt` | **/tmp — wiped on reboot** |
| original `runstate/` (gitignored) | hourly summaries + done-cube lists written by the shepherd; final counts are distilled in `STATUS.md` | local host state only |

## Historical health check

```bash
SP=/tmp/claude-1000/-home-maria-projects-erdos-gyarfas/c144a1df-3cfa-4083-9296-c8d234dd9732/scratchpad
# what's running
pgrep -af 'smsg --[v]ertices' | grep -oP '(b0_\w+|sms4648)/(n\d+/)?\S*?cyc[_.]\w+' | sort | uniq -c
# progress of the per-cube pools
grep -l "All cubes processed" $SP/b0_n33race/cube_*.log | wc -l          # /522
grep -l "All cubes processed" $SP/b0_p16cube/n34/percube/cube_*.log | wc -l  # /1360
# any verdicts?
tail -2 $SP/b0_{ladder,race,capped,capped_cube,p16,p16cube}/summary.txt
# memory headroom (the binding constraint - keep available > 20G)
free -g
```

A verdict was a new line in a `summary.txt`. The shepherd
(`src/ops/oom_shepherd.sh`, PID formerly in `$SP/SHEPHERD_PID`) monitored
the active pools.

## Interpreting verdict lines

- `n=N rc=20 count=0` or `n=N rc=cube count=0` → **rung N is ZERO** (no
  α-block). For PMAX=16 runs this is sound as-is (superset space).
- `count>0` on a PMAX=16 run → survivors avoid {4,8,16} but may contain
  C32+: a full-spectrum `p2check` post-filter is necessary for interpretation.
  A graph passing that filter is a counterexample candidate; the campaign's
  verification standard required two independent tools (`p2check` +
  `checker.py`/Glasgow).
- `count>0` on a CAP=31 run needs **no** post-filter — a hit is an α-block
  outright (all powers ≥32 vacuous below the cap).
- `FAILED` / `INCOMPLETE` / `PARSE_FAIL` lines → a kill or crash artifact,
  not a mathematical result.

## Historical restart mechanics

All pools skipped finished work automatically (a cube/shard log containing
`All cubes processed` was not re-run). Restarts used the original launchers:

```bash
# n=33 race pool (width 8 was memory-safe)
nohup setsid $SP/b0_n33race/launch.sh > $SP/b0_n33race/driver_new.log 2>&1 &
# n=34 per-cube pool
nohup setsid $SP/b0_p16cube/n34_percube.sh > $SP/b0_p16cube/n34_percube_driver_new.log 2>&1 &
# shepherd restart
nohup setsid $SP/oom_shepherd.sh > /dev/null 2>&1 &
```

The scratchpad was volatile. The recovery design depended on a local
`runstate/` snapshot and deterministic regeneration by `src/b0_cube_rung.sh`
of `enc.cnf`/`cyc.txt`/`cubes.txt` (same cutoff ⟹ same cubes; n33 used
cutoff 28, n34 cutoff 28, capped46 cutoff 30). Completed cubes were represented
by pre-seeded logs, using this pattern:

```bash
RS=<repo>/runstate
for i in $(cat $RS/n33race_done_cubes.txt); do
  printf 'All cubes processed\n' > $SP/b0_n33race/cube_$i.log; done
# same pattern for n34_done_cubes.txt -> b0_p16cube/n34/percube/cube_$i.log
```

(Pre-seeding avoided re-solving finished cubes; the snapshot cadence was
one hour.)

Per-cube pools (`src/ops/n34_percube.sh`) isolated the hard cubes and
preserved completed work across process kills.

## Operational lessons

1. **Memory was the budget**: the post-OOM limit was ~20 solvers with > 20G
   available in `free -g`. Solver RSS grew 0.3G → 6G+ over days.
2. **Kill discipline**: process inspection (`ps -eo pid,ppid,args`) identified
   drivers, wrappers, and gate-waiters for outermost-first termination by PID.
   Literal `pkill -f` patterns could match the invoking command itself;
   bracketed patterns such as `n3[4]` avoided that self-match.
3. **Silence is not failure**: smsg prints nothing until a cube/shard
   finishes. A quiet log is normal; a *finished* log without
   `All cubes processed` is a crash.
4. **SAT evidence**: a candidate required a preserved witness log and
   independent verification (see verdict section).

## Final scope

- The n=33 race stopped with cubes 1813 and 1814 incomplete, so it has no
  rung verdict. Their literals were recorded in the original `cubes.txt`.
- The sibling algebra lane later closed both n=46 and n=48; its final evidence
  is archived under `results/` and summarized in `REPORT.md` §2a.
