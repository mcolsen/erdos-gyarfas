# Erdős–Gyárfás counterexample campaign — 2026-07-24

**Conjecture** (Erdős–Gyárfás 1995): every graph with minimum degree ≥ 3 contains a
simple cycle whose length is a power of two. ($100 for a proof, $50 for a counterexample;
Erdős reportedly doubted the conjecture.)

**Campaign outcome (final; all recorded jobs landed by 2026-08-04):**
No counterexample found. Both non-peer-reviewed inputs verified sound (one
strengthened). Frontier scoreboard ("any counterexample needs ≥ N vertices"):

| class | before this campaign | now | method |
|---|---|---|---|
| general min-degree-3 | ≥ 17 published / ≥ 32 unrefereed | **≥ 36** | assumption-free ≤ 32 + minimal-structure chain 33–35 |
| cubic | ≥ 30 | **≥ 50** | SMS ladder n = 32..48, nine even-order rungs, all zero |
| bipartite | — | **≥ 57** | 2-coloring SMS ladder n = 33..56 |

Plus: smallest cubic graph avoiding {C4,C8,C16} bracketed in **[50, 82]**.
Plus: the historical pure-enumeration frontier (Royle ~2004: n ≤ 15/16)
re-derived and extended with no SAT in the loop: **0 graphs avoiding
{C4,C8,C16} at every order n = 4 … 21** (geng + prune, settled 2026-07-29).

## 1. Adjudication of the two non-peer-reviewed inputs

### 1a. Carr, arXiv:2605.22844 ("predominantly cubic") — VERIFIED CORRECT, and strengthened
All four statements re-proved independently (see
`verification/carr-2605.22844-verification.md`). Bonus: the paper's own two corollaries
imply that **≥ 2/3** (not just 4/7) of the vertices of a minimal counterexample are
cubic. The independence of the degree-≥4 set is due to Markström (2004), as Carr says
(Markström's own statement of it has an obvious typo: "d ≥ 3" should be "d ≥ 4").

### 1b. Balaji, `erdos-gyarfas-min-degree-3` (SMS frontier n ≤ 31) — VERIFIED SOUND
- Design audit (all ~1.8k lines read): CEGAR blocking clauses sound; lex-leader
  symmetry breaking never removes an isomorphism class; DFS cycle detector exact;
  UNSAT over each relaxed space implies UNSAT over the true space. Their §7 honestly
  concedes LRAT certificates could not be checked (Glasgow propagator clauses are not
  RUP-derivable), so the n ≤ 31 claim rested on the SMS+Glasgow stack — the gap my
  validation closes:
- **Independent count-exact validation of every encoding ingredient** (my nauty/geng
  stack vs the SMS stack, disjoint codebases):
  | check | geng (mine) | SMS | verdict |
  |---|---|---|---|
  | n=8, min-deg-3, nothing forbidden | 2590 | 2590 | ✔ |
  | n=10, forbid C4 | 5 | 5 | ✔ |
  | n=10, forbid C8 only | 1315 | 1315 | ✔ |
  | n=12, forbid {C4,C8} | 0 | 0 | ✔ |
  | n=16, forbid {C4,C16} | 88 | 88 | ✔ |
- Their pytest gates: 55/55 pass locally.
- **Frontier replication on this machine: COMPLETE — n = 17–31, all 15 sizes UNSAT**
  (2.9 s at n=17 → 6539 s at n=31), matching their published table. Verdict: the
  n ≥ 32 bound is real and now independently replicated.

## 2. New frontier results (this campaign)

### 2a. Cubic case: frontier moves 30 → **50**
- Markström 2004 reproduced by exhaustive isomorph-free generation (geng -f + my C8
  prune plugin; no SAT): #cubic graphs with no C4/C8 = **4 at n=24** and **23 at
  n=26** — exactly his published Table 3 — and each contains a C16 (spectra checked).
- **NEW: SMS proves ZERO cubic graphs avoid {C4,C8,C16} at n=32 (5m52s), n=34
  (17m03s), n=36 (38m40s), n=38 (81m34s), n=40 (3h53m), and n=42 (8h17m).**
  A fortiori none avoid all power-of-2 lengths. With parity (no odd-order cubic
  graphs) and n ≤ 31 from §1b.
- **n = 44: ZERO (18h24m rerun, after an external stop killed the first attempt
  at ~9h).** (n = 46 projected to ~2 days — outside the phase-1 stopping rule;
  picked up by phase 2.)
- **n = 46: ZERO (2026-07-31; 88.1h wall / 73.6 CPU-h, 1.7× the ladder
  projection). Any cubic counterexample needs ≥ 48 vertices.** Same-day
  positive controls on the unchanged toolchain: {C4,C8}-free counts 4 (n=24)
  and 23 (n=26), both = Markström; rc=20 confirmed as smsg's normal
  enumeration-complete exit code (it ends UNSAT after blocking every found
  model, so rc=20 + parsed count = clean completion).
- **n = 48: ZERO (final paths landed 2026-08-03/04). Any cubic
  counterexample needs ≥ 50 vertices.** Two validated paths agree: the
  monolith returned `rc=20 count=0` (581,004 s wrapper elapsed; 525,663 s
  solver time), while cube-and-conquer resolved 1,195 top-level cubes as
  zero and recursively partitioned the remaining region into 1,137 cells,
  all zero. The hard corner was independently split into 914 and 2,618
  cells, again all zero. The pipeline reproduced Markström's positive
  n=28/{4,8} count 251 exactly at three granularities before production.
  The monolith log, aggregate records, compact ledgers, drivers, and checksum
  are archived in
  `results/n48_final_20260804.tar.gz`; see `notes/cube-and-conquer.md` and
  `notes/n48-interim-status.md` for the full execution history.

### 2b. General minimum-degree-3 case
- **Independent exhaustive verification (geng + prune plugin — no SAT involved):
  0 graphs avoiding {C4,C8,C16} at EVERY order n = 4 … 21 — COMPLETE.**
  n = 21 settled 2026-07-29 by a complete pure mod-256 partition: 256/256
  classes finished, 0 survivors, 509 CPU-h (mean 2.0 h/class, worst 18.9 h);
  verified: every class log carries geng's `>Z` completion line with count 0,
  all 256 `>A` headers identical (`-fX0x12800d3D10 n=21 e=32-50`), all output
  files empty. METHOD
  CORRECTION (2026-07-27): an earlier cross-mod "refinement race" (16→64→256)
  assumed class i (mod m) = ∪ classes i+km (mod 4m). This is FALSE in general:
  geng's dynamic splitlevel decrement threshold is multiplicity = 50·mod
  (geng.c:2694), so different mods can shift splitting levels at different
  traversal points, and cross-mod unions need not partition the work. Caught
  via a timing anomaly before any claim rested on it (all counts were zero
  either way). Single-mod partitions are exact regardless of decrement
  dynamics, since all classes of one run configuration share identical
  traversal state; the certifying mod-256 run above is pure single-mod
  throughout. CROSS-CERTIFIED 2026-07-30: the original pure mod-16 partition
  also completed — 16/16 classes, 0 graphs, 389 CPU-h (final stragglers:
  7/16 at 39.9 CPU-h, 6/16 at 42.4 CPU-h). Two complete independent
  partitions of the n = 21 space — different slicings, different machine
  loads, different dates — agree on zero survivors.
  This re-derives the entire historical frontier (Royle ~2004: n ≤ 15/16) and
  independently confirms Balaji's range low end by pure enumeration.
  Uses my degree-cap theorem (C4-free + δ≥3 ⟹ Δ ≤ ⌊(n−1)/2⌋ — proof in the Carr
  note) to shrink the geng space; n=5,7 are empty outright by the cap + parity.
- SMS replication n = 17–31: complete, all UNSAT (see §1b).
- **NEW: n = 32, the first order where C32 fits: ZERO {4,8,16}-free min-deg-3
  graphs exist (SMS, 5h27m, count=0, assumption-free).** No C32 analysis was even
  needed — there are no candidates. **The general frontier is now ≥ 33.**
- **Bipartite ladder** (`src/encode_bipartite.py`: 2-coloring CNF + forbid
  {4,8,16}; assumption-free within the class): **ZERO bipartite min-deg-3 graphs
  avoiding {C4,C8,C16} at every n = 33..56 (ladder COMPLETE; ≤ 32 covered by the
  general result) ⟹ **any bipartite counterexample needs ≥ 57 vertices.**
- **Structural rungs** (`src/encode_structural.py`: minimal-counterexample
  constraints — V₄₊ independent [Markström], cubic-neighbor [Carr], |V₄₊| ≤ n/3
  [my 2/3 bound], Δ-cap; sound for frontier extension by minimum-order chaining on
  top of the assumption-free base n ≤ 32; validated 0=0 at n=20, 24):
  **n=33: ZERO (≈5h), n=34: ZERO (≈10.5h), n=35: ZERO (≈22h) ⟹ general
  frontier ≥ 36.** (Ladder complete — n=36 structural was projected ≥ 30h and
  fell outside the campaign's stopping rule.)

### 2c. Structured-family hunt (completed scoped searches)
| family | graphs tested | survivors of {4,8,16} | outcome |
|---|---|---|---|
| Generalized Petersen GP(n,k), 2n ≤ 64 | 240 | 0 | dead |
| I-graphs I(n,j,k), 2n ≤ 64 | 1,148 | 0 | dead |
| Circulants C_n(S), n ≤ 64, deg 4–6 | 80,780 | 0 | dead |
| Cyclic lifts (Z_m) of θ, K4, K3,3, Q3, Petersen; n ≤ 64 | 176,348 | 0 | dead |
| Conder cubic arc-transitive census ≤ 10,000 (corrected) | 3,815 | **689** | all 689 contain C32 ∧ C64 ∧ C128 |
| PSV cubic vertex-transitive census ≤ 1280 (phase 2) | 111,360 | **100** | all 100 contain C32 ∧ C64 |

ERRATUM (found 2026-07-27, folded into main 2026-07-30): this section
originally claimed "Conder census ≤ 2048: 796 graphs, 3 survivors". 796 is
the size of the 768-vertex (extended Foster) file — the coverage label was
wrong; the tooling was not (checker.py exonerated by independent Glasgow
re-verification). Corrected sweep (the other-approaches lane, census
to 10,000 rebuilt from Conder's presentations and validated against his
packaged lists on ≤ 2048): 689 {4,8,16}-free graphs — 23 with n ≤ 2048,
incl. C1050.1 (girth 12, n = 1050, new smallest arc-transitive graph with
no C16) — and every one of the 689 contains C32, C64 AND C128 (2,067
verified witness cycles, zero timeouts). The phase-2 PSV sweep (algebra
phase) extends this to all 111,360 cubic
vertex-transitive graphs ≤ 1280: 100 survivors, smallest n = 180 (girth
3!), all contain C32 ∧ C64. Both censuses are clean: no arc-transitive
counterexample occurs through 10,000 vertices and no vertex-transitive
counterexample occurs through 1,280. Details: `notes/census-erratum.md` and
`notes/algebraic-program-validation.md`.

Three survivors remain the campaign's mechanism exemplars:
- **C2030.1** (2030 vertices, girth 7 (!), non-bipartite): contains 7-cycles yet no
  C4/C8/C16 — power-of-2-free up to 16 without high girth.
- **C1458.10, C1458.11** (1458 vertices, girth 12, bipartite): even-cycle spectra
  skipping 16.
All three contain C32 and C64 (Glasgow subgraph solver, witness found in ~20–50 ms),
so each satisfies the conjecture.

### 2d. Simulated annealing over cubic graphs — concluded negative
Energy = 10·#C4 + 5·#C8 + #C16 (exact counts each move); exact C32 gate on any E=0
state. Round 1 (20M moves): best energies 25/22/17/19 at n=34/36/38/40. Round 2
(60–80M moves, n = 44–62) plus a 3-strategy fleet at n = 48/56/62: best energies
floor at 13–20, minimum ever observed E = 13 (n = 60), invariant to move
strategy — no chain ever approached 0. Full floor analysis in §4.

### 2e. CEGAR existence lottery — concluded negative
`src/cegar_hunt.py` — CaDiCaL + eager C4 + cycle-blocking loop at fixed orders
(no minimality assumptions). Budgets exhausted at n=36 (100k refinements), n=40
(1M), n=48 (60k), n=56 (600k) without ever cornering a model into a survivor.

### 2f. The [65,127] window (five forbidden lengths) — night run
128-bit two-phase annealer (`src/sa_hunt128.c`):
- **Phase 1 succeeded instantly everywhere tried: {C4,C8,C16}-free cubic graphs
  EXIST and are easy to find at n = 96, 112, 120, 126** (8/8 chains, minutes each).
  All eight independently re-verified ({4,8,16}-free by `checker.py`, a disjoint
  implementation) and all eight contain C32 (Glasgow witness) — so they satisfy
  the conjecture; archived in `results/sa128_c4c8c16free_cubic_n96-126_have_c32.g6`.
- **Phase 2 (minimize #C32 within the {4,8,16}-free space) hit a structural wall:
  these graphs carry ≥ 10⁵ thirty-two-cycles** (node-budget-capped counts). With the
  Moore bound putting girth > 32 out of reach below ≈ 1.3·10⁵ vertices, a [65,127]
  counterexample would need a non-girth "spectral hole" at 32 AND 64 against ~10⁵⁺
  expected cycles of each length — beyond the local searches used here.
  (Assessed, not exhausted.)
- **New extremal bracket: the smallest cubic graph with no C4/C8/C16 has between
  50 and 82 vertices** (lower: SMS ladder through 48 all zero; upper: probes found
  verified specimens at n = 82, 90, 94 — all containing C32). Ten annealing
  probes at n = 66..80 (30-40M moves each) all failed, versus instant success
  at 82+: a sharp SA-findability transition near 80, hinting (not proving) the
  true threshold sits near the bracket's upper end.

### 2g. Block reduction and α-block ladder
- **Block equivalence:** EG is false if and only if there is a 2-connected
  graph with at most one degree-2 vertex (all others degree at least 3) whose
  cycle spectrum avoids every power of two up to its order. Such an
  **α-block** is itself a counterexample or yields one by gluing two copies at
  their degree-2 vertices. See `notes/block-program.md` for the proof.
- The independently validated SMS encoding searched a strict superset of these
  blocks and returned **zero at every n = 10..32**. Thus every leaf block of a
  counterexample has more than 32 vertices, a statement stronger than the
  same-order general frontier.
- The n=33, n=34, and circumference-capped n=46 continuations were interrupted
  without a verdict. Their final 2026-08-03 progress and exact scope are
  recorded in `STATUS.md`; `REPORT-other-approaches.md` contains the complete
  lane narrative and its census, lift, and arithmetic results.

## 3. Toolchain (all in `src/`, binaries via `build.sh`)

- `p2check.c` — exact power-of-2 cycle spectra/filter for graph6, n ≤ 64. DFS with
  BFS-distance pruning (L ≤ 16); exact meet-in-the-middle path-join (L ≥ 32).
  Validated: vs an algorithmically independent brute force on ALL 13,591 graphs with
  n ≤ 8 (zero mismatches); named-graph spectra (Petersen, Heawood, McGee,
  Tutte–Coxeter, dodecahedron, hypercube…); DFS↔MITM cross-agreement; count
  agreement with nauty's geng -f.
- `p2prune.c` — geng PRUNE plugin: kills any partial graph containing a forbidden
  C_L through the newest vertex (inductively exact). Reproduced Markström's 4/23.
- `checker.py` — arbitrary-n checker (census-scale graphs).
- `gen_families.py`, `gen_lifts.py` — family generators. `sa_hunt.c` — annealer.
- `encode_structural.py` — minimal-counterexample CNF. `cegar_hunt.py` — SAT lottery.
- `sms_frontier.sh`, `run_shards.sh`, `smsg_to_g6.py` — drivers.
- SMS + Glasgow built from source at Balaji's pinned commits; smsg on PATH.

## 4. Assessment: true with margin, or false only through algebra

The conjecture holds everywhere this campaign could decide it, and — more
informatively — it holds with *margin* everywhere we could measure it. The
decisive quantity is the expected number of cycles of length L in a cubic-like
graph, ≈ 2^L/(2L): **doubly exponential in the index of the power of two.**
Avoiding C8 means dodging ~16 expected cycles; C16, ~2·10³; C32, ~7·10⁷;
C64, ~10¹⁷. The forbidden lengths thin out as n grows (Erdős's reason for
doubting the conjecture), but each forbidden length gets exponentially fatter —
and the second effect wins. Concretely observed:

- {C4,C8}-free cubic graphs *explode* (4 → 23 → 251 at n=24/26/28), yet adding
  the C16 exclusion flattens the count to exactly zero for every order through 48.
- Annealing kills C4s and C8s easily and then floors at ~13–25 residual C16s at
  every n ∈ [34,62], invariant to move strategy (23 chains, 3 strategies, ~1.5
  billion moves — never once reaching a {4,8,16}-free state).
- In [65,127] the picture inverts exactly as the formula predicts: {4,8,16}-free
  cubic graphs are *easy* (8/8 chains, minutes each, n=82..126) and the wall
  moves to C32 (≥10⁵ thirty-two-cycles in every specimen; girth > 32 impossible
  below ~1.3·10⁵ vertices by Moore).

**Spectral holes exist only where the counts are small.** The campaign's most
instructive object, census graph C2030.1 (2030 vertices, girth 7, non-bipartite),
has holes at 8 and 16 — lengths where the expected counts (~16 and ~2·10³) are
small enough for algebraic symmetry to suppress; C1458.10/11 likewise skip 16.
All three contain C32 and C64 within milliseconds of Glasgow search: their
symmetry, which engineered the short holes, *spreads* the long cycles. No object
in the corrected censuses (689 arc-transitive survivors to 10,000 vertices, 100
vertex-transitive survivors to 1280), ~260k structured graphs, or any stochastic
search ever dodged a power ≥ 32.

A first-moment heuristic therefore says counterexamples should not exist at any
order — and the only known escape from such heuristics is the algebraic needle
(the loophole through which Moore graphs and cages exist). So the campaign's
final characterization: **if a counterexample exists, it is a highly structured
algebraic object with engineered spectral holes at two or more consecutive large
powers of two, at a scale where those holes suppress millions of cycles — a kind
of object for which this campaign found no construction principle.** This is
a heuristic assessment of the methods' limits, not an exclusion theorem.

What the campaign produced beyond the frontier table: a validated methodology
for adjudicating unrefereed computational claims (count-exact cross-validation
of disjoint stacks); eleven verified {4,8,16}-free cubic specimens; a new
well-posed extremal question (smallest such graph, bracketed in [50,82]); and
this heuristic characterization of the unresolved cases.

## 4b. The algebraic program — validated, re-scoped, executed (2026-07-27)

The successor campaign proposed in `notes/algebraic-program.md` was validated
and run (full detail: `notes/algebraic-program-validation.md`). Headlines:

- **Core machinery of the proposal verified** (lift criterion, twisted-trace
  formula), but its 5-length sweep design is **provably infeasible**: a new
  theorem (`notes/trace-moore-bound.md`, independently verified) shows a
  cubic graph with NO cyclically-non-backtracking closed L-walk (the
  proposal's certification condition) needs ≥ (2^{L/2}+1)²/(2^{L/2+1}−1)
  vertices — L=32 needs ≥ 32,770, L=64 needs ≥ 2.15×10⁹. Point-holes in the
  walk spectrum cost nearly as much as full girth (~8× discount). The
  literature scan suggests the single-length bound is novel; nothing prior
  applies NBW spectra or voltage lifts to Erdős–Gyárfás.
- **Full Potočnik–Spiga–Verret census swept** (111,360 cubic VT graphs
  ≤ 1280; two orders of magnitude beyond the Conder subset): exactly **100
  graphs avoid {C4,C8,C16}** — and **every one contains C32 ∧ C64**. The VT
  landscape is clean. Smallest survivor: n=180 (girth 3, spectrum
  {3,12,14,…}) — smallest known VT {4,8,16}-free cubic graph (was 1458).
- **Exact voltage-lift sweep of the [46,126] window**: all cubic multigraph
  bases on ≤ 6 vertices (with loops and semi-edges) across a 363-group
  library (all abelian ≤ 63 + dihedral/dicyclic/metacyclic/specials), plus
  71 loopless 8-vertex bases across groups of order 6–15: more than 2.3×10¹⁰
  voltage configurations, with exact per-config cycle semantics (engine
  matches independent Python ground truth on 209
  exhaustive spaces). **Three isomorphism classes survive {4,8,16}** — F21
  lift at n=126 (girth 6; F21 = Z7⋊Z3 the smallest odd-order nonabelian
  group), Z12 lift at n=96, Z15 lift at n=120 (girth 3) — and each contains
  C32. No lift counterexample exists below 128 vertices over this base/group
  space.
- **Mechanism split discovered** (the campaign's treasures reinterpreted):
  C1458.10/11 are trace-certified at 16 (tr(H¹⁶) = 0); C2030.1 is NOT — it
  carries 194,880 identity NBW 16-walks, none simple. Cycle-holes ≠
  walk-holes; only the latter are reachable by the proposed spectral
  machinery, and they obey the Moore-type bound above.
- **New extremal ladder** (smallest cubic graph with tr(H^L) = 0):
  L=8 = **28 exactly** (21 minimum witnesses,
  `results/tr8zero_n28_all21.g6`; smallest VT realization remains 30), L=16 ∈ **[130, 630]** (n=630
  census graph; 2-vertex-base abelian lifts proven empty in [130,630]),
  L=32 ∈ [32,770, ?] (winding-lattice hunt over the parameterized 2-vertex
  bases was empty throughout 32,770 ≤ n ≤ 100,000), L=64: floor 2.15×10⁹ —
  beyond all search.

## 5. Closure and remaining scope

1. **Archive**: the repository record and draft mathematical note preserve
   the campaign's results and evidence.
2. **Extremal bracket**: n=46 and n=48 are closed at zero, leaving [50,82].
   No n=50 rung was attempted. The validated cube-and-conquer machinery is
   retained for reproduction.
3. **The algebra program** — EXECUTED 2026-07-27, see §4b: census swept
   (clean), lift window [46,126] decided (three classes, conjecture holds),
   walk-certification provably fenced by the trace-Moore bound, Ramanujan
   route inverted. Unresolved cases include anti-Ramanujan spectral-concentration
   constructions at n ≥ 32,770 (trace-32), or exact-cycle-hole (C2030-style)
   constructions at any scale — both currently lack a construction principle;
   the winding-lattice machinery (`src/windhunt.c`, `src/lift/hunter32.py`)
   records the tests used for the parameterized families.
4. **The block program** — MERGED AND ARCHIVED: the α-block equivalence and
   ladder through n=32 are complete. Higher-rung and circumference-capped
   searches stopped incomplete and provide no further mathematical verdict;
   their stopping state is in `STATUS.md`.
5. **Stand down**: chosen 2026-08-08. The conjecture won on points; this repo
   is the record. After the final archive was verified, the redundant direct
   cube-0 process (which had no bearing on the two-path n=48 verdict) was
   stopped. No solver from either computational lane remains active.

Transcript-to-artifact reconciliation and explicit scope boundaries are in
`notes/claude-session-closure.md`.
