# Cube-and-conquer for the SMS cubic ladder

Execution and validation record. Written 2026-07-31 ~17:50 PDT while the
n=48 rung was running; closed below after the final paths landed on
2026-08-03/04. Validation record complete in §4.

## 0. Executive summary

The SMS cubic ladder rungs ({C4,C8,C16}-free cubic graph counts) began as
single-threaded smsg monoliths: n=46 took 73.6 CPU-h. We built and validated
a cube-and-conquer pipeline on top of smsg's native cube support that solves
the identical CNF in parallel shards. On n=48, 1195 of 1196 top-level cubes
resolved quickly; recursive splitting closed the hard region. The final
verdict is **count=0**, separately matched by the monolith, so the cubic
frontier is ≥ 50 and the extremal bracket is [50,82]. No n=50 run was made.

Three smsg semantics traps were found the hard way (each caught by a
count-exact gate before touching production; §3), and the pipeline was
validated at four independent layers (§4). Final evidence is archived in
`results/n48_final_20260804.tar.gz`; the historical runbook remains in §6.

## 1. Motivation

After the n=46 rung closed (zero graphs; cubic frontier ≥ 48, bracket
[48,82] — REPORT §2a), the n=48 monolith had ~90 CPU-h invested with days
remaining, while ~44 threads sat idle. smsg ships cube-generation
(`--simple-assignment-cutoff`) and cube-consumption (`--cube-file`,
`--cubes-range`, `--cube-line`) flags, and the sibling lane had used them —
but their validation record was incomplete, and (as §3 shows) the obvious
consumption pattern silently miscounts. Rule applied throughout: no cubed
result is trusted until the pipeline reproduces a known positive count
exactly (Markström's 251 {C4,C8}-free cubic graphs at n=28).

## 2. Architecture

- Cube generation: `smsg --simple-assignment-cutoff K` emits cubes as
  `a <signed literals> 0` lines mixed into stdout; extract with
  `grep -aoP '^a( -?\d+)+ 0$'`. Cutoff auto-tuned to land 500–30000 cubes.
  Solutions can be found DURING generation; the gen log's own
  "Number of graphs" count is part of the total.
- Consumption: worker i solves cube i alone via `--cube-line $((i+1))`
  (1-indexed) on a CNF extended with blocking clauses of cubes 0..i-1
  (§3.3 — this is what makes the shard counts a partition).
- Scheduling: per-cube dynamic queue (`xargs -P`), NOT static ranges — cube
  costs are wildly skewed (§5), and static ranges strand a worker on a
  monster while its siblings idle. Pool size = free threads at launch,
  clamped [8,40]. Workers run without `--hide-graphs` so any witness graph
  is captured in its shard log.
- Idempotence: per-cube `.res` files; re-running the driver resumes.
- Total = gen-phase count + Σ shard counts. A shard is healthy iff rc=0 AND
  a count line parsed; anything else fails the rung (no silent gaps).

## 3. smsg cube semantics — measured, not assumed

Each of these was discovered by a failed gate, then confirmed by a decoded
numeric fingerprint. Reference truth: n=28, {C4,C8}, true count 251, first
cube's true count 211.

### 3.1 `--cubes-range a b` is 1-indexed AND inclusive
`--cubes-range 0 1` is a silent no-op: "All cubes processed", NO count line,
rc=0. `--cubes-range 1 2` solves cubes 1 and 2 (two cubes), printing
CUMULATIVE per-cube count lines (so `grep | tail -1` sees the invocation
total). Fingerprint that nailed it: per-cube "ranges" `i i+1` over all i
summed to 2·251 − 211 = 291 (cut=20, first cube counted once, all others
twice) and 2·251 − 0 = 502 (cut=28, first cube empty). Never use ranges for
singletons; `--cube-line N` (1-indexed) selects exactly one cube.

### 3.2 Bare consumption double-counts across invocations
Even with correct indexing, consuming cube i in its own smsg invocation
without the generation-time blocking context lets cube regions overlap: gate
A summed 291 (cut=20) and 950 (cut=28) against the true 251. Overlap can
only INFLATE counts, so cubed ZERO verdicts (e.g., the sibling lane's
p16cube rungs) remain sound via coverage; any cubed POSITIVE count obtained
by naive range-summing is suspect.

### 3.3 Fix: explicit blocking clauses
Worker i's CNF = base + clauses ¬cube_j for all j < i (each cube is a
conjunction of literals; its blocking clause is the disjunction of their
negations). Cube i then counts exactly the solutions in region_i minus
∪_{j<i} region_j — a partition of the solution space by construction,
independent of smsg's internal cube handling. Cost: ≤ NC extra clauses per
shard; negligible.

### 3.4 Misc
- Healthy cube-consumption exit code is 0. (Monolith enumeration exits 20 —
  UNSAT after blocking all found models — see REPORT §2a note.)
- The {4,8,16} set at small n is a USELESS gate (true count 0 for all
  n ≤ 46). Positive controls use {4,8} vs Markström: 4 @ n=24, 23 @ n=26,
  251 @ n=28. A "validation" that expects 0 validates nothing.

## 4. Validation record (all runs 2026-07-31, unchanged Jul-24 toolchain)

| gate | design | cut=20 (444 cubes) | cut=28 (1002 cubes) | verdict |
|---|---|---|---|---|
| A | naive per-cube ranges | 291 | 950 | FAIL → found §3.1+§3.2 |
| B | + blocking clauses | 291 | 502 | FAIL → decoded §3.1 exactly |
| smoke | `--cube-line 1` vs range `1 1` | 211 = 211 | — | both exact singletons |
| C | blocking + `--cube-line` | **251** | **251** | **PASS** |
| unit probe | cube literals as UNIT clauses, no `--cube-file` | 211/12/15 = 211/12/15 | 8 n=48 samples 0=0 | PASS (mechanism equivalence on positive data) |
| repo gate | `src/cube_gate.sh` (productionized scripts) | **251** (877 cubes, 155s) | — | **PASS** — third distinct granularity, same exact total |
| D (abandoned) | lookahead gen `--assignment-cutoff` | degenerate: 1 cube at every cutoff 150–800, ± `--lookahead-only-edge-vars --prerun` | — | this smsg build's lookahead cubing failed the splitting gate |

Structural caveat found in production (n=48): with `--simple-assignment-cutoff`,
cube/cell 0 is always the lex-extreme corner where SMS's canonical
(lex-minimal) representatives concentrate — prefix-order cubing peels the
easy bulk fast but recursing into cell 0 is a treadmill (each level
re-creates the corner). Recursion parallelized the bulk but left a hard
corner for the remaining workers; every non-corner cell at every
level has finished in seconds-to-hours. Lookahead cubing (the textbook fix)
is not available in this build (gate D above).

Independent-confirmation layer: the n=48 monolith (same CNF, no cubes)
ultimately completed with count zero, agreeing with the cubed total.

## 5. Production: the n=48 rung (historical in-flight record)

Final closure: the monolith returned `n=48 rc=20 count=0` on 2026-08-03.
The 2,618-cell deepest split, 914-cell parent split, and complete 1,137-cell
region-0 partition all aggregated to zero by 2026-08-04. The exact verdict
lines and final archive are reproduced in `notes/n48-interim-status.md`.
The bullets below preserve what was known when this report was first written.

- Top level: cutoff 36 → 1196 cubes, generated in seconds. 1195/1196 cubes
  resolved with count=0, the bulk within ~1 minute on 26 workers; cost skew
  is extreme — a consecutive cluster (#1060–1068) took minutes-to-hours, and
  cube #0 (the lexicographically-first region, all tracked edge vars false)
  ran 7.8+ CPU-h solo. At n=28/cut20 the analogous first cube held 211/251
  = 84% of all solutions; "cube 0 is most of the space" appears to be the
  pattern.
- Escalation (then running): region 0 re-encoded with cube-0 literals as unit
  clauses, sub-cubed at cutoff 72 → 1137 sub-cubes; 1121/1137 done, ALL
  ZERO, 16 stragglers including sub-cube #0 (the pattern is fractal). The
  original cube-0 worker raced the split as a redundant path. The recursive
  splitting method is recorded in §6.4.
- Verdict lines land in the run's summary.txt
  (`runs/sms4648/summary.txt`: monolith `n=48 rc=20 ...`, accelerator
  `n=48cube rc=OK|INCOMPLETE ...`, split `n=48cube0split ...`); region-0
  total + 1195 zeros = the rung count.
- CPU comparison so far: monolith 96+ CPU-h (unfinished); cubed pipeline
  ~10 CPU-h total including the monster region's progress. The gains are
  real but come entirely from splitting the easy 99.9% off the hard core;
  the hard core itself still costs what it costs — the win is that it
  parallelizes.

## 6. Archived execution paths and reproduction commands

The commands below document the pipeline used on this machine.
`$VENV` = the pysms venv (phase-1 scratchpad `venv`, has sms_graph_builder;
any venv with pysms works). Scripts live in `src/` (this repo).

### 6.0 Historical n=48 paths (state as of 2026-07-31 evening)

This subsection records the original paths. The run is complete; see §5 and
`notes/n48-interim-status.md`.

The phase-2 scratchpad runs directory was:
```
RUNS=/tmp/claude-1000/-home-maria-projects-erdos-gyarfas--claude-worktrees-algebra/e397a738-ce4d-43e7-a8c4-3397853029a5/scratchpad/runs
```
Verdicts were appended to `$RUNS/sms4648/summary.txt`. Three paths were
running at that snapshot:

1. **Region-0 split** (`$RUNS/cube0split/`): 1,137 expected `.res` ledgers,
   1,121 present at writing; aggregate format `n=48cube0split rc=... count=R`.
2. **Original cube-0 worker** (`$RUNS/cube48/`): its completion marker was
   `$RUNS/cube48/shards/c0.res`, with `n=48cube rc=... count=C` aggregating
   all 1,196 top-level cubes. This redundant worker never completed.
3. **Monolith** (PID 1188800 at writing; same CNF, no cubes): aggregate
   format `n=48 rc=20 count=M`, providing confirmation without cubing.

The 1,195 other top-level cubes all counted zero, so the rung count was R
(region-0 split), independently matched by M (monolith). Both completed at
zero: cubic frontier ≥ 50 by parity, extremal bracket [50,82]. Successful
completion required `rc=OK` for the cubed result or `rc=20` for the monolith;
`INCOMPLETE`, `GENFAIL`, and `PARSE_FAIL` were not verdicts.

### 6.1 Validation gate
```
src/cube_gate.sh $VENV /tmp/gate_out && echo SAFE
```
Re-runs the n=28/{4,8} rung through the full pipeline; PASS iff count=251
exactly. ~5–10 min on a moderately free box. This nonzero reference was
the validity gate for the smsg, pysms, and cube_rung.sh toolchain (§3.4).

### 6.2 Reproducing the n=48 rung
```
nohup src/cube_rung.sh $VENV /path/to/out 48 &     # {4,8,16}-free at n=48
tail -f /path/to/out/driver.log                    # gen progress
watch 'ls /path/to/out/shards/*.res | wc -l'       # shard progress
cat /path/to/out/summary.txt                       # verdict line when done
```
Interpretation: `rc=OK count=0` ⟹ zero {4,8,16}-free cubic graphs at that
n. For positive counts, witness graphs are in the shard logs of nonzero
cubes (`.res` files with `count=[1-9]`). Such witnesses require independent
regularity and cycle checks (`p2check -F 4,8,16` or `src/cycscan.c`), including
C32 at n=48. `rc=INCOMPLETE` or `GENFAIL` provides no verdict.
The script skips finished cubes on rerun and self-sizes its worker pool at launch.

### 6.3 Completion indicators
`ls shards/*.res | wc -l` vs `wc -l cubes.txt`. Missing indices =
unfinished cubes. A cube running for
hours is not an error — it is a hard region (expect cube 0 specifically).

### 6.4 Recursive splitting method
Hard cubes were isolated in `region.cnf` = enc.cnf + that cube's literals
as unit clauses (+ blocking clauses of earlier cubes for nonzero cube
indices). The same pipeline operated inside that region with a deeper
cutoff (roughly +36). The original construction was in scratchpad
`work/cube0split.sh` (2026-07-31 session), a 30-line specialization of
cube_rung.sh. Parent workers provided cross-checks against recursive splits;
the final recursive drivers are in `results/n48_final_20260804.tar.gz`.

### 6.5 Process persistence
Drivers used setsid/nohup to survive session close. Results were files,
with aggregate verdicts recorded in summary.txt.

## 7. Provenance

Session artifacts (scratchpad `runs/`): `cubeval28/RESULT.txt` (gates A/B/C
lines + cube sets), `cubeval28/cut20/SMOKE.txt`, `unitprobe/PROBE.txt`,
`cube48/` (production top level), `cube0split/` (region-0 split),
`gate_repo/` (repo-script gate). Repo: `src/cube_rung.sh`,
`src/cube_gate.sh`, this note. The monolith rung driver remains
`src/sms_cubic.sh` (unchanged; still the independent-confirmation path).
