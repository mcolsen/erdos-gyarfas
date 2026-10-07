# Campaign status — other-approaches lane

*Archived 2026-08-08 from the last shepherd snapshot at
2026-08-03T05:33:26Z. This is the final operational state, not a live-job
dashboard. The intellectual record lives in `REPORT-other-approaches.md`,
method notes in `notes/`, and artifacts in `results/`.*

## Headline

**B0 ladder clean n = 10–32.** No α-block (2-connected, ≤1 degree-2 vertex,
cycle spectrum avoiding all powers of 2 ≤ order) exists on ≤32 vertices — by
the block-equivalence theorem, no counterexample to Erdős–Gyárfás can be built
from blocks that small. Every rung independently verified (n=31 single
cross-checked by 9 cube shards; n=32 settled UNSAT-sound on the {4,8,16}
superset encoding, 997 cubes across 16 shards, all zero).

| rung | verdict | cost |
|---|---|---|
| 10–29 | 0 | seconds–3h each |
| 30 | 0 | 15.6h |
| 31 | 0 | 46.8h (single) |
| 32 | 0 | 58.9h (cube-and-conquer, 997 cubes, 16 shards) |

Full per-rung table: `results/b0_ladder_summary.txt`.

## Interrupted work (no verdict)

| front | final preserved state | mathematical status |
|---|---|---|
| **n=33** | 520/522 race cubes complete across ranges 1044–1304 and 1566–1826; cubes 1813 and 1814 incomplete | no rung verdict |
| **n=34** | shards 0,1,2,3,5 complete; 411/1,360 per-cube jobs complete in the remaining pool | no rung verdict |
| **capped cell n=46, c≤31** | shard 0 of 4 complete | no cell verdict |
| **capped 48/50** | cube-form runs remained queued after earlier singles were lost to OOM | not attempted after recovery |
| **algebra lane** | subsequently closed n=46 and n=48 at zero and archived its evidence | complete; see `REPORT.md` §2a |

The final snapshots contained no n=33, n=34, or capped-cell verdict line.
Partial cube completion is not evidence of UNSAT for a rung. No associated
solver or shepherd process was running when the repository was audited on
2026-08-08.

## OOM incident (2026-07-30 23:53) and defenses

Kernel OOM + systemd-oomd swept the ~40-solver fleet (smsg RSS grows to
3–6G+ over days; the fleet outgrew the 125G box). Casualties: capped
46/48/50 singles (3 days, unresumable), n=33 single + both cube tails,
11/16 n=34 shards, one sibling run. All verdicts and completed logs
survived. Defenses adopted during the campaign, in failure order:

1. **Sizing**: ≤~20 solvers / ~60G budget, actual RSS re-measured at every
   rebalance (memory, not cores, is the binding constraint).
2. **Early warning**: monitor fires LOW-MEM below 15G available (hours of
   runway at observed growth rates); OOM-ALERT on any kernel kill.
3. **Chosen victims**: all solvers tagged `oom_score_adj=900` (shepherd loop
   re-tags every 60s) — the kernel kills resumable shards, never sessions.
4. **Cheap deaths**: every pool is per-cube resumable (skip-done logs); a
   kill costs minutes, not shard-hours.

## Ops doctrine (hard-won)

- **Per-cube granularity everywhere**: shard-level runs hide monsters and
  lose hours on restart; per-cube pools drain trivial mass instantly,
  isolate monsters, and resume perfectly.
- **Kill discipline**: enumerate drivers AND gate-waiters before any kill;
  kill outermost wrappers first, by PID; `pkill` patterns bracket-tricked
  and never in the same Bash call as text containing the target string
  (scripts with hot strings are written via the file-write tool, not
  heredocs).
- PMAX=16 encoding is UNSAT-sound (superset space); any count>0 needs
  p2check post-filter before interpretation — and would be a full
  counterexample candidate requiring independent verification.

## Limits of the interrupted results

- Unfinished cubes 1813 and 1814 prevent a verdict for n=33.
- The n=34 evidence covers five complete shards and 411/1,360 per-cube jobs
  in the remaining pool, not the full deterministic partition.
- The capped n=46 evidence covers only one of four shards.
