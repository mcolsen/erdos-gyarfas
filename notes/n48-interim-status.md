# n=48 rung — interim snapshot and final closure

Snapshot: 2026-08-01 09:35 PDT. This recorded the state while the scratchpad
was on volatile tmpfs. Companion documents: `notes/cube-and-conquer.md`
(pipeline, validation record, historical paths in §6.0) and
`results/n48_state_*.tar.gz` (bookkeeping snapshots produced by
`src/snapshot_n48.sh`).

## Final closure — 2026-08-04 results, archived 2026-08-08

The one unknown recorded in the snapshot below resolved to zero. The complete
n=48 result is **ZERO cubic graphs avoiding {C4,C8,C16}**, established by two
validated paths:

```
n=48c0s697s0 rc=OK count=0 elapsed=76043s subcubes=2618
n=48 rc=20 count=0 elapsed=581004s
n=48c0s697 rc=OK count=0 elapsed=256437s subcubes=914
n=48cube0split rc=OK count=0 elapsed=286291s subcubes=1137
```

- The full monolith completed 2026-08-03 with `Number of graphs: 0`, normal
  enumeration-complete result 20, and 525,663.028571 s solver time.
- The recursive path completed 2026-08-04: all 1,137 region-0 cells were zero;
  the last corner also independently aggregated to zero through both its
  914-cell parent split and its 2,618-cell deeper split.
- Therefore any cubic Erdős–Gyárfás counterexample has at least 50 vertices,
  and the smallest cubic {C4,C8,C16}-free graph lies in **[50,82]**.
- `results/n48_final_20260804.tar.gz` preserves the final monolith log,
  encoding, forbidden-cycle specification, summaries, cube sets, all `.res`
  ledgers, aggregate results, validation records, and recursive drivers. Its
  sidecar `.sha256` file verifies the archive.
- The original direct top-level cube-0 worker never finished. It was a third,
  redundant path, not needed by the two-path verdict, and was stopped after
  archival on 2026-08-08 after more than eight days of CPU time.

Sections 1–5 below preserve the historical progress snapshot and storage
limitations. `RUNNING` and `PENDING` describe the snapshot time only.

## 1. Results settled at snapshot time

- **n=46: ZERO** {C4,C8,C16}-free cubic graphs (73.6 CPU-h monolith +
  same-day controls). Cubic EG frontier ≥ 48; bracket [48,82]. REPORT §2a.
- **Pipeline validity**: cube-and-conquer validated count-exactly (251 =
  Markström at n=28/{4,8}) at three granularities + unit-clause cross-path
  + repo-script gate. Traps documented (1-indexed inclusive ranges;
  cross-invocation double-counting; lex-corner treadmill; lookahead
  generator degenerate in this build).

## 2. n=48 verification tree — state at snapshot time

Every resolved cell at every level is ZERO. Target identity: rung count
= 1195·0 (top-level cubes 1..1195) + region-0 count.

```
L0  monolith (same CNF, no cubes)      RUNNING  100.7 CPU-h   [confirmation]
L1  1196 cubes (cut 36)                1195 = 0 DONE; cube 0 = region 0:
L2    region 0: 1137 cells (cut 72)    1132 = 0 DONE; five monsters:
        cell 673                       = 0  VERIFIED TWICE (parent + L3 rec)
        cell 827                       = 0  VERIFIED TWICE (parent + L3 rec)
        cell 0                         = 0  VERIFIED TWICE (parent + L3 rec 648 cells)
        cell 801                       = 0  VERIFIED TWICE (parent + L3 rec 1496 cells)
        cell 697                       PENDING: L3 rec 913/914 (corner cell
                                       ~14h single-thread, parent worker ~16h,
                                       L4 split of the corner launched
                                       2026-08-01 09:33: 2618 cells, 8 workers)
L1  original cube-0 worker             RUNNING ~24 CPU-h      [redundant path]
```

Verdict lines were recorded in `$RUNS/sms4648/summary.txt` (see §4 for $RUNS).
Present at snapshot: `n=46`, `n=48c0s673`, `n=48c0s827`, `n=48c0s0`,
`n=48c0s801` (all count=0). Awaited: `n=48c0s697` (and/or `n=48c0s697s0`),
then `n=48cube0split` (its driver aggregates when parents 697 finish),
`n=48cube` (aggregates when original cube-0 finishes), `n=48` (monolith).

**The single number still unknown at snapshot time: region 697's
corner cell.** Every other region was settled at zero.

## 3. How the verdict assembled

- Region 697's corner resolved to zero through both the L3 and L4 splits,
  making region 0 zero and hence **n=48 count = 0 ⟹ cubic frontier ≥ 50,
  bracket [50,82]**.
- The monolith independently matched the full cubed result at zero.
- Workers ran without `--hide-graphs`, so any witness would have been
  preserved in its shard log. No positive witness was found.

## 4. Historical storage and recovery design

`$RUNS = /tmp/claude-1000/-home-maria-projects-erdos-gyarfas--claude-worktrees-algebra/e397a738-ce4d-43e7-a8c4-3397853029a5/scratchpad/runs`

- **Session persistence:** setsid/nohup drivers survived terminal or agent
  session loss, with verdicts stored in summary.txt.
- **Driver idempotence:** completed `.res` cells were skipped on restart.
  Original command lines were recorded in `$RUNS/<dir>/driver.log`;
  the pipeline and splitting method are in `cube-and-conquer.md` §6.2/§6.4.
- **Volatile storage:** a machine reboot erased tmpfs solvers and ledgers.
  The `results/n48_state_*.tar.gz` snapshots preserved completed-cell
  ledgers (~350K per snapshot), but no monolith solver checkpoint. The final
  archive in the final-closure section above supersedes those interim snapshots.

## 5. Separate other-approaches lane

Session c144a1df operated a separate smsg fleet (n=33/34 B0 work and capped
46/48/50 attempts with a different encoding). Those processes were outside
the n=48 verification tree. Their final interrupted states are in `STATUS.md`;
the capped n=46 attempt did not provide a cross-encoding verdict.
