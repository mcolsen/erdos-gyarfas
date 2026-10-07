# Validation and execution of the algebraic program — 2026-07-27

Verdict-first summary of validating `algebraic-program.md` (the proposed
successor campaign) and of the executed, re-scoped program. Toolchain and raw
outputs in the session scratchpad; validated tools promoted to `src/`.

## 1. Verdicts on the proposal's claims

| claim | verdict |
|---|---|
| Lift criterion (no identity-voltage NBW closed L-walk in base ⟹ no C_L in lift) | **CORRECT** — proved (cycle projections are cyclically-NBW; seam case included) and machine-verified on 124 random lifts over cyclic/dihedral/quaternion/symmetric groups: `tr(H_lift^L) = |Γ|·NBW_id(L)` exactly, criterion never violated, over-forbidding real (45/124 instances) |
| Twisted-trace formula `#NBW_triv(L) = (1/|Γ|)Σ_ρ dim ρ·tr(H_ρ^L)` | **CORRECT** — equivalent to block-diagonalizing the lift's Hashimoto matrix; verified numerically via the identity `tr(H_lift^L) = |Γ|·NBW_id(L)` |
| Feasibility of the 5-length sweep (kill at L = 4,8,…,64) | **REFUTED** — new theorem (§2): walk-certification at length L is impossible below ≈ 2^{L/2−1} vertices. The L=64 rung needs n > 2.1×10⁹ (the note's lifts: ≤ 10⁵); the L=32 rung needs n ≥ 32,770. The sweep as designed terminates empty with certainty. |
| Step-1 premise (the census treasures embody the twisted-cancellation mechanism) | **HALF-TRUE** — C1458.10/11: yes (tr(H¹⁶) = 0, walk-certified). C2030.1: **no** — tr(H¹⁶) = 194,880 with zero 16-cycles; its hole is a cycle-only phenomenon *invisible in principle* to the proposed machinery. Two distinct mechanisms exist in the wild (§3). |
| Obstruction map §3 of the note | Mostly right; one correction: "cubic circumference ≥ n^0.69" requires ≥ 2-connectivity (bridged cubic graphs have bounded circumference), so the window-obstruction argument needs the standard reduction to 2-connected minimal counterexamples. Bondy–Vince as cited is fine. |
| Census cross-section (step 4) | **CORRECT and productive** — executed in full (§4): 100 new treasures incl. an n=180 record and 22 walk-certified graphs (record trace-16 hole at n=630). |

## 2. The trace-hole Moore bound (new obstruction, reshapes everything)

See `trace-moore-bound.md` for statement, proof, and empirics. Core: for
connected cubic G, even L, s = 2^{L/2}: tr(H^L) = 0 forces
**n ≥ (s+1)²/(2s−1) ≈ 2^{L/2−1}** (bipartite: ≈ 2^{L/2}). Since
tr(H^L) ≥ 2L·#C_L ≥ 0, and tr(H^L) = 0 ⟹ no C_d for all d | L, the walk/
trace route certifies powers of two only at exponential vertex cost:

| certify at L | minimum n (cubic) | realized in the wild |
|---|---|---|
| 8 | 10 | **28 exactly** (§6; complete census: 21 witnesses at 28) |
| 16 | 130 | **630** (new record, census graph; was 1458) |
| 32 | 32,770 | none known; census max n=1280 — provably impossible there |
| 64 | 2,147,483,650 | out of reach for any conceivable search |

Literature scan (subagent, 2026-07-27): the single-length statement appears
**novel**; ingredients standard (Ihara–Bass; Kotani–Sunada eigenvalue
classification). Closest strands: spectral-Moore/LP bounds (Nozaki; Cioabă
et al. — opposite direction: they cap n given spectral gap), Sudakov–
Verstraëte cycle-spectrum richness Ω(2^{g/2}) (hypothesis girth, not a
single hole), zeta-function trace folklore. No prior application of NBW
spectra or voltage lifts to Erdős–Gyárfás found at all. For L < 2·girth the
bound literally reads: *a cubic graph with girth ≥ 9, n ≤ 128 contains a
16-cycle* — e.g. every (3,9)–(3,12) cage contains C16.

Empirical anchors: all 556,471 connected cubic graphs n ≤ 20 have
tr(H⁸), tr(H¹⁶) > 0 (sweep); across the full 111k-graph PSV census the
minimum observed tr(H³²) values sit at ≈ 2³² (non-bipartite survivors) and
≈ 2·2³² (bipartite) — graphs on the spectral floor exactly as the proof's
equality analysis predicts, none anywhere near 0.

## 3. Rosetta analysis (step 1 of the note, executed)

| graph | girth | tr(H⁴) | tr(H⁸) | tr(H¹⁶) | mechanism |
|---|---|---|---|---|---|
| C2030.1 | 7 | 0 | 0 | 194,880 | holes at 4,8 walk-certified; hole at 16 **cycle-only** (all 194,880 identity 16-walks are degenerate) |
| C1458.10/11 | 12 | 0 | 0 | 0 | fully walk-certified (girth-12 ⟹ tr(H¹⁶) = 32·#C16) |

Consequence for search design: walk-vanishing machinery can only find
C1458-type objects; C2030-type holes require exact cycle checks (walks
present, none simple). The executed sweep (§5) therefore uses *exact*
per-config tests — identity-voltage words plus a degeneracy check (a walk
lifts to a simple cycle iff no proper cyclic sub-segment is voltage-balanced
at an equal base vertex) — which captures both mechanisms.

## 4. Full PSV census sweep (step 4, executed; ~30 min wall)

All **111,360** cubic vertex-transitive graphs on ≤ 1280 vertices (download
verified against the published count), exact {C4,C8,C16} scan (`cycscan.c`,
new: canonical-rooted DFS, arbitrary n, VT root-0 mode; cross-validated
against `p2check` on all 509 cubic n=14 graphs and against the campaign's
treasure facts):

- **100 survivors** with no C4/C8/C16. (Novelty caveat post-erratum: the
  sibling lane found phase-1's Conder sweep undercounted — the corrected
  Conder AT census has survivors ≤ 1280 too, e.g. C1050.1, which duly
  reappears among these 100 at n=1050 as an independent cross-check; the
  VT census subsumes the AT one, so this list is the complete VT picture.)
  Smallest: **n = 180** (girth 3! sixty triangles, then no cycle length in
  {4,…,11}: spectrum {3, 12, 14, …}) — smallest known vertex-transitive
  {4,8,16}-free cubic graph (old record 1458), and a girth-3 counterpoint to
  the girth-first intuition. Not a truncation (a truncated girth-6 base
  would carry mixed 16-cycles; it has none).
- **All 100 contain C32 ∧ C64** (exact): the census is *clean* — the
  conjecture holds across the entire cubic VT landscape ≤ 1280.
- 47/100 have tr(H⁸) = 0; **22/100 have tr(H¹⁶) = 0** — walk-certified
  treasures; smallest at **n = 630**, halving the extremal record for a
  cubic trace-16 hole (bracket now [130, 630]).
- Files: survivors + traces archived to `results/` (see §7).

## 5. Exact lift sweep, window n ∈ [46,126] (steps 2–3, re-scoped, executed)

Machinery (all cross-validated; engine survivor sets match an independent
Python lift-build + explicit cycle count on **209 exhaustive (base,group)
spaces — zero mismatches**):

- Base enumerator: all connected cubic multigraphs with loops *and
  semi-edges* on k ≤ 6 vertices (5/22/141 at k=2/4/6; validated against
  hand-enumeration at k=2 and nauty `multig -l3` on no-semi subsets:
  5=5, 17=17 at k=4,6); k=8 loopless via `multig` (71 bases). Scope
  boundary: k=8 bases WITH semi-edges were not swept (enumeration cost out
  of proportion to the thin margin — semi slots are involution-rigid and
  every window discovery came from loopless multi-edge bases); k ≤ 6 is
  complete including semi-edges.
- Group library: 363 validated groups ≤ order 63 (all abelian; dihedral,
  dicyclic, all metacyclic actions, A4/S4/A5/SL(2,3)/Heisenberg-27, direct
  products; known gap: some exotic 2-groups of order 32/48 — accepted, since
  every *Cayley* lift (1-vertex base) of every group ≤ 426 is subsumed by
  the census sweep).
- Engine (`liftsweep.c`): per voltage config — maximal-subgroup generation
  masks (skips subgroup-lifts, provably lossless here since any cubic graph
  < 46 vertices contains a C4/C8/C16 by the SMS ladder), exact kills at
  L ∈ {1,2} (simplicity), L = 4 (identity word ⟺ C4), L ∈ {8,16}
  (identity word + non-degenerate ⟺ genuine cycle), abelian Aut-orbit
  slot-0 dedupe. Sound and complete for simple connected lifts in-window.

**Result: 2.298 × 10¹⁰ voltage configurations over 169 bases (k ≤ 6) ×
window groups → 336 raw survivors → exactly ONE isomorphism class.**
A single {C4,C8,C16}-free cubic lift exists in the entire window:
n = 126 = 6·21, deck group **F21 = Z7⋊Z3** (the smallest nonabelian group
of odd order), base = a 6-vertex multigraph with one doubled edge; girth 6,
cycle spectrum {6,7,9,10,…} — and it **contains C32 and C64** (conjecture
holds). It is not vertex-transitive (census-checked) — a genuinely new
extremal object, "the F21 graph". Every survivor independently re-verified
(rebuild + `cycscan` + `p2check` cross-checks; 0 discrepancies).

k=8 loopless (71 `multig -l3` bases × orders 6–15): two further classes —
n = 96 (Z12 lift) and n = 120 (Z15 lift), both girth 3, both containing
C32 ∧ C64. **Final tally for the window: three isomorphism classes of
{4,8,16}-free cubic lifts in [46,126] (F21@126 girth 6, Z12@96 and Z15@120
girth 3), every one satisfying the conjecture via C32.**

Reading: exact spectral holes (both mechanisms) at {4,8,16} are three
needles in ~23 billion configurations, all in the top quarter of the
window, and the conjecture eats each via C32 within milliseconds.

## 6. The L=8 certification rung (calibration data point)

tr(H⁸) = 0 ⟺ C4-free ∧ C8-free ∧ no two triangles joined by an edge
(dumbbell walks; figure-eights are impossible in cubic graphs — the shared
vertex would need degree 4); Markström's {C4,C8}-free cubic graphs at n = 24 (4
graphs) and 26 (23 graphs) all have girth 3 and tr(H⁸) ∈ {32,…,352} > 0.
So the smallest cubic tr(H⁸) = 0 graph has n ≥ 28. Notably the prior
campaign's 11 SA specimens (n = 82–126, {4,8,16}-free) are ALL girth 3 with
tr(H⁸) ∈ [576, 1152] — local search finds cycle-holes, never walk-holes;
every specimen also confirms the L=16 bound (n < 130 ⟹ tr(H¹⁶) > 0, and
indeed tr(H¹⁶) ≈ 10⁵ for each). Scanning the whole census at n ≤ 130 for
tr(H⁸) = 0 gives 38 hits, the smallest at **n = 30** (girth 5, twelve C5s,
no C7/C8/C9 — a vertex-transitive girth-5 C8-free graph). With Markström's
exhaustion of n ≤ 26 ({C4,C8}-free graphs exist only from 24, all girth 3,
all tr(H⁸) > 0 — verified here), the smallest cubic
tr(H⁸) = 0 graph has **exactly 28 vertices**, and the census at 28 is
complete: the full {C4,C8}-free enumeration returned 251 graphs (= Markström's
published count, revalidating the stack) of which **exactly 21 are trace-8
holes** — 17 of girth 3 (isolated triangles) and 4 of girth 5, the latter
independently reproduced by a disjoint girth-restricted enumeration (4 = 4,
canonical forms identical). All 21 verified by nbwtrace + p2check (both
modes) + cycscan; `results/tr8zero_n28_all21.g6`. The n<28 side was already
exhausted via Markström. Companion girth-5 census: the girth≥5 C8-free
cubic graphs (all automatic trace-8 holes) number **4 at n=28 and 48 at
n=30** (`results/g5_c8free_n30_all48.g6`; 48/48 verified, all distinct, and
the n=30 vertex-transitive census graph reappears among them — independent
stacks agreeing again). Floor-vs-realization ratios: L=8: floor 10, realized
28 (ratio 2.8); L=16: floor 130, realized 630 (ratio 4.8) — calibrating that L=32
realizations (floor 32,770) plausibly live at ~10⁵, informing §8.

## 6b. The Ramanujan inversion (SL(2,p) probes, and a corrected intuition)

The note proposed SL(2,p) and friends as "the classical sources of Ramanujan
behavior". Sampled probes of theta/dumbbell lifts over SL(2,29) (n = 48,720)
and SL(2,31) (n = 59,520) at L = 32 — sizes chosen as the smallest clearing
the 32,770 floor — show identity-walk counts ≈ 2³²/|Γ| per basepoint, i.e.
lift traces ≈ 2³² = the bare Perron term, with twisted contributions
fluctuating near zero (|Σ| ~ 10⁷–10⁸ ≪ 2³²). This is Ramanujan
*equidistribution*: twisted spectra spread on the |μ| = √2 circle, their
power sums nearly vanish. **But a trace-hole needs the twisted sum to be
−(2³² + n + 1) — maximally negative, not small**: every tempered eigenvalue
parked at cos(Lθ) = −1. Expander-quality groups are therefore precisely the
wrong tool; hole-engineering requires extreme spectral *concentration*
(what girth-forced structures like C1458's do). This inverts the note's §2
intuition and explains §5's negative results: the algebraic needle, if it
exists, is anti-Ramanujan.

## 7. Artifacts

- `src/nbwtrace.c` — exact u128 NBW traces, arbitrary degree, n ≤ 4096
  (validated against bigint matrix powers + Ihara–Bass on 89 graphs × 5 L's,
  0 mismatches; three-way vs brute enumeration on multigraphs with loops).
- `src/cycscan.c` — exact C_L presence/absence, n ≤ 4096, VT mode.
- `src/liftsweep.c` + `src/lift/{bases,groups,liftprep,liftjob,liftpost}.py`
  — the exact-lift pipeline (validation harnesses included).
- `results/census_psv_survivors_100.g6`,
  `results/census_psv_survivor_traces.txt`, `results/lift_f21_n126.g6`, and
  `results/lift_z12_n96_z15_n120.g6`.
- `notes/trace-moore-bound.md` — the theorem.

## 8. Final scope and limitations

1. **The walk/trace route is now quantitatively fenced**: nothing below
   32,770 vertices can be trace-certified at 32; nothing below ~2.1 billion
   at 64. Any counterexample below those scales must dodge long powers the
   C2030-way (walks present, none simple) — exact-check territory, where
   per-graph certification cost explodes with n.
2. **Every natural algebraic reservoir ≤ 1280 covered by the stated scope is
   exhausted**: full VT census clean; exact lift window [46,126] clean for
   all k ≤ 6 bases (including semi-edges) and loopless k=8 bases. Bases on
   eight vertices with semi-edges were not swept. The cubic SMS ladder is
   zero through n=48; structured families and [65,127] SA probes were also
   negative.
3. The winding-lattice hunt was executed for the feasible slice: the three
   zero-winding-free 2-vertex bases (loopsemi, semis4, dubsemi — theta and
   dumbbell are dead for all abelian Γ, mult₀(32) > 0) over Z_m, Z2×Z_k,
   Z2²×Z_k, Z4×Z_k across the whole window n ∈ [32770, 100000]:
   **zero hits** (likewise empty at L=16 over [130, 630] — the census's 630
   record is not approachable from 2-vertex bases). The SL(2,29)/SL(2,31)
   probes (6,000 samples) show the nonabelian "Ramanujan" route inverts
   (§6b). So the L=32 certification rung remains unrealized by every family
   parameterized in this campaign. Larger bases (winding lattices ⊂ Z^{r},
   r ≥ 4) and anti-Ramanujan constructions were outside the tested scope.
4. Honest posterior after this campaign: the conjecture looks *true with
   margin* in every family algebra can currently reach; the remaining
   uncertainty lives at scales where neither certification mechanism is
   computationally viable, and the trace-Moore bound now proves a large part
   of that inaccessibility rather than merely observing it.
