# Verdict on the arithmetic lane (research agent findings, digested)

Full agent report in session transcript; key holdings, all with citations
there. Status of each: literature-sourced unless marked [computed].

## Identifications

- **C2030.1** = 1-skeleton of the non-orientable regular map of type {7,3}
  with Aut = PSL(2,29) (Macbeath–Hurwitz family; NOT the sextet graph —
  S(p) needs p ≡ ±1 mod 8, and 29 ≡ 5). Its face-rotation relator (order 7)
  and (ah⁻¹)^15 relator explain the sporadic lengths. Exact spectrum
  [computed]: {7, 12, 15} ∪ [17, 40] on the tested range — holes at
  {8,9,10,11,13,14,16}.
- **C1458.10/11** = elementary-abelian 3-cover towers over Pappus/K₃,₃;
  their girth-12 relators are *cubes of 4-letter words* — the 12-cycles are
  K₃,₃'s 4-cycles wound three times through a Z₃ voltage. The C16-hole is a
  winding condition. This is precisely the "big-base × Z₃ twist" mechanism,
  realized in nature.

## The counting law (calibrated, heuristic)

For arc-transitive coset graphs Γ(G,H,a): expected number of length-L
cycle-forcing relations ≈ 2^L·|H|/(2L·|G|). Postdicts C2030.1's spectrum
exactly (sporadic algebraic lengths below threshold, coin-flip hole at 16,
everything ≥ 17 present). Consequences:

- **Hole at 32 in an AT family needs |G| ≳ 4×10⁸ (n ≳ 7×10⁷); hole at 64
  needs n ≳ 10¹⁷.** All lengths above ~3·log₂|G| up to circumference are
  present, and these graphs are (empirically) Hamiltonian.
- **Therefore no PSL(2,p)-type family (triplet, hexagon, sextet, Hurwitz
  maps, LPS, Chiu) can avoid all powers of 2.** The arithmetic route is
  closed as a counterexample source.
- The one congruence-programmable hole in the literature is Biggs–Boshier:
  in bipartite LPS X^{p,q}, the single bottom length 2⌈2log_p q⌉ vanishes
  iff p^⌈2log_p q⌉ − q² is of the form 4^a(8b+7) — the sums-of-three-squares
  2-adic obstruction. Exactly one hole, everything above present, order
  exponential in the hole position. Model theorem for hole mechanics; dead
  end for counterexamples.

## Abelian winding: scope and limitations

In an abelian lift of a base with cyclomatic number c, absence of simple
cycles of exact length L collapses from ~2^L word conditions to O(L^c)
winding-class congruences (Fossorier-type). These engineer *cycle-only*
holes — orthogonal to the trace-Moore obstruction, which binds walk-holes
only. Constraints per graph: Σ_{powers L ≤ circumference} O(L^c) — the open
question is satisfiability as the lift grows (kill-fraction arguments
suggest failure for c ≥ 2 at scale, consistent with every sweep to date).

Executed, fully: this worktree closed all cyclic lifts of bases ≤ 12
vertices in [46,63] (zero survivors), then the remaining [65,127] gap
(multigraph bases 8–12 × cyclic; 49.36e9 assignments, 30.5e9 lifts, 18/18
cells exhaustive, 0 survivors — results/lift_gap_65_127/); the algebra
worktree closed bases ≤ 6 (+ loopless 8) × 363 groups in [46,126].
**Combined: the cyclic voltage-lift route over bases ≤ 12 is exhaustively
closed on all of [46,127]. Nothing in this family below 128.** The window's
only {4,8,16}-free lifts form 4 isomorphism classes (n = 96, 108, 110, 120,
all girth 3, all containing C32∧C64; two match the algebra worktree's
independently-found classes, two are new — archived near-miss data).
Non-cyclic groups over bases 8–12 and larger-base pruning via Kim/Park
inevitable-cycle patterns were outside this sweep's scope.

## Also noted

Boben–Jajcay–Pisanski, "Generalized Cages" (EJC 2015): explicit graphs
whose cycle spectrum below a threshold N is an arbitrary prescribed set —
the only literature engineering interior spectrum holes; no control above
N. Its prescribed-spectrum result alone supplies no circumference control
of the kind required by the block program.
