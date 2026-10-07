# Other-approaches campaign report — 2026-07-27/28

Scope: alternative strategies to the algebra worktree's spectral program.
This historical lane is now merged into `main`, with artifacts in `results/`
and method notes in `notes/`. The original write-up was made while B0 rung 33
and circumference-capped cells were live; their final interrupted state is in
`STATUS.md`.

## Outcome table

| lane | result |
|---|---|
| **Block program** (new reduction) | EG ⟺ α-block existence (2-connected, ≤1 deg-2 vertex, power-free ≤ order). Novel per literature check. SMS ladder over this strictly-larger-than-δ≥3 space: **all zeros, n = 10–32** (n=31: 46.8h single, cross-checked by cube twin; n=32: 58.9h cube-and-conquer on the {4,8,16}-superset encoding — count=0 there settles the full rung); n=33 stopped incomplete at 520/522 race cubes, with no verdict |
| **Conder census 2048–10000** | complete, 3,815/3,815: **689 {4,8,16}-free, all contain C32∧C64∧C128** — census clean to 10,000 vertices; phase-1 erratum found & corrected (23 not 3 at ≤2048); new record: C1050.1 = smallest AT cubic with no C16 |
| **Lift closure [46,63]** | exhaustive, 138.7M lifts (bases ≤ 12 × all cyclic + all groups ≤ 15): **0 survivors** |
| **Lift gap [65,127]** | exhaustive, 30.5B lifts (bases 8–12 × cyclic): **0 survivors**; only 4 iso-classes of {4,8,16}-free lifts in the window (n = 96, 108, 110, 120), 2 matching the algebra worktree independently, 2 new |
| **Arithmetic lane** | closed with reasons: counting law (2^L·|H|/2L|G|) postdicts C2030.1's spectrum; AT-family hole at 32 needs n ≳ 7×10⁷, at 64 needs ≳ 10¹⁷; C2030.1 identified (non-orientable {7,3} map of PSL(2,29)); Biggs–Boshier three-squares theorem = the model "congruence-programmable hole", one hole at exponential cost |
| **Methodology survey** | program-search + exact staged evaluator is the transferable recipe; PatternBoost/RL documented to fail in exactly this regime; verifier non-exploitability is the recurring lesson |
| **Literature status at campaign close** | EG open, recorded as $1000-tier (erdosproblems #64); Erdős–Gyárfás themselves believed it false; block/deg-2 relaxation unpublished; the ≥2/3-cubic bound was independently posted by jul059 on the forum 07-26 (campaign derived 07-24) |

## Combined closure statement (with the algebra worktree)

No counterexample exists among: all graphs ≤ 35 (δ≥3), cubic ≤ 48,
B0 blocks ≤ 32 (this campaign, strictly stronger space), bipartite
≤ 56, all cyclic-group voltage lifts of multigraph bases ≤ 12 on [46,127],
all groups ≤ 15 on [46,63], the 363-group library over bases ≤ 6 (+ loopless
8) on [46,126], the full arc-transitive census ≤ 10,000, the full
vertex-transitive census ≤ 1,280, and — analytically — any arc-transitive
family at any order where a hole at 32 would need n ≳ 7×10⁷ with everything
above ~3·log₂|G| present. Trace-certified holes at 32 are additionally
empty to 100,000 vertices (algebra worktree). Every reachable "algebraic
needle" habitat that anyone has proposed is now either swept or bounded away.

## The two structural theorems of this lane

1. **α-block equivalence.** EG false ⟺ a single 2-connected graph with at
   most one degree-2 vertex avoiding all powers of 2 up to its order exists;
   two glued copies (or a power-free subdivision skeleton — verified
   {6,7,9,10} K4 example) then give counterexamples of every larger size.
   All published searches required δ≥3 everywhere, so the B0 ladder is new
   territory — and measurably so: rung n at cost c, the B0 spectrum-free
   space runs ~5–10× the δ≥3 analog (n=30: 15.6h vs ~1h), with the
   suppression view explaining why (the deg-2 vertex couples powers of 2 to
   Mersenne lengths 2^k−1 through one edge).
2. **Circumference loophole + decidability.** A counterexample needs holes
   only up to its circumference; c ≤ 31 makes every power ≥ 32 vacuous, and
   c ≥ 2·diam plus Birmelé's tw ≤ c make each capped cell finite and the
   whole capped corner MSO-decidable. Cells n = 46/48/50 with c ≤ 31 were
   attempted but not completed; bipartite instantiations were killed analytically
   (partial-Steiner incidence forces ≤ 15 points where bipartite-Moore
   forces C8).

## Where the conjecture now stands (this lane's assessment)

The campaign's phase-1 verdict ("true with margin, or false only through
algebra") sharpens to: **false only through a mechanism nobody has named.**
The algebraic families are closed by counting, not merely by search; the
walk/trace route is closed by theorem; the block reduction says the only
object worth hunting is a single α-block, and its ladder is clean through 32
with a cost curve steep enough that exhaustive progress beyond ~34 needs new
ideas rather than new cores. The genuinely untested corners that remain:

1. B0 ladder 33–36 (n=33 and n=34 were interrupted without verdicts).
2. Capped cells at larger n and caps (c ≤ 63 variants) — cheap, decidable,
   unexplored.
3. Non-cyclic groups over bases 8–12 (the one lift family not yet swept).
4. The mechanism theory of the 689-graph census survivor corpus (with the
   9-member girth-7 Macbeath family and the 4 lift near-miss classes) —
   the corpus is archived, but a general mechanism classification was not obtained.

## Speedup engineering (for the record)

SMS cube-and-conquer works but decomposes poorly on hard cores; recursive
sub-splitting has a floor; the single biggest lever found was **removing the
C32 forbidden-subgraph pattern** (Hamiltonian-sized propagator work at
n=32) and post-filtering instead — vindicated at n=32: 58.9h wall on shared
cores vs a ~6-day projection for the full encoding — plus a proven
Δ ≤ ⌊n/2⌋ degree cap for
the C4-free B0 space (validated count-exactly). Lift sweeping is embarrass-
ingly parallel and hit 1.45M assignments/s sustained on 24 workers with the
128-bit p2check extension (0 mismatches across 725k+ cross-checks).
