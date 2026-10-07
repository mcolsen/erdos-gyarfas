# Regime analysis: where a counterexample can still live

*Companion to REPORT.md §4 and the algebra worktree's trace-moore-bound.md;
sharpens both with a thin/fat decomposition and an orbit-counting estimate.
Historical rationale for the lanes tested in this worktree.*

## 1. Thin vs fat lengths

Fix a graph of girth g. Call a length L **thin** if L < 2g and **fat** if
L ≥ 2g. The point of the split:

- **Thin lengths:** every closed cyclically-non-backtracking (CNB) L-walk is a
  simple L-cycle (a non-simple CNB closed walk decomposes over ≥ 2 cycles,
  total length ≥ 2g). Hence C_L-freeness ⟺ tr(H^L) = 0, and the trace-Moore
  bound applies: **a thin hole at L needs n ≥ ~2^{L/2−1}.**
- **Fat lengths:** walk counts are provably positive below that bound, but
  C_L-freeness is still possible as a *cycle-only hole* (all L-walks
  non-simple). C2030.1's hole at 16 (girth 7, tr(H^16) = 194,880) is exactly
  this. Fat holes are invisible to all trace/spectral machinery.

Consequences assembled with the campaign data:

| window | forbidden powers | status |
|---|---|---|
| n ≤ 45 (cubic), ≤ 35 (δ≥3) | 4..32 | closed by ladders |
| [46, 63] | 4,8,16,32 | open; girth ≤ 8 forced (trace-Moore: thin 16-hole needs n ≥ 130, so girth ≥ 9 ⟹ C16 present); so 16 and 32 must BOTH be fat/cycle-only holes |
| [65, 127] | + 64 | as REPORT §2f, plus: 32-hole and 64-hole both cycle-only against ~10^5 and ~10^13 walks |
| [130, ~32k], girth 9–16 | 16 thin-holeable | tr(H^16)=0 possible (C1458.10 realizes at 1458); but 32, 64 fat |
| ≥ 32770, girth ≥ 17 | 16 auto, 32 thin-holeable | tr(H^32)=0 becomes possible; 64 still needs n ≥ 2^31 |

Every window has at least one power that must be a **fat, cycle-only hole**.
The girth/trace route never closes the top octave; this is a structural
invariant of the problem, not a shortage of compute.

## 2. Orbit counting: what symmetry can and cannot suppress

The only known mechanism for fat holes is symmetry: in an arc-transitive
graph, C_L's come in Aut-orbits, and "no C_L" is #orbits-many coincidences,
not #cycles-many. But Tutte's theorem caps cubic arc-transitive vertex
stabilizers at 48, so |Aut| ≤ 48n, and generically

    #orbits of C_L ≈ (2^L / 2L) / (48n).

For a fat hole this must be a *small* number of coincidences. At the top
power L* ≈ n this ratio is ~2^n/n², astronomically ≥ 1 — **unless the
circumference stays below L***, in which case the top powers are absent for
free. That is the one loophole left in the assessment of REPORT §4:

> **Circumference control replaces hole-engineering for all powers above it.**

A counterexample does not need holes at every power ≤ n; it needs holes at
every power ≤ its circumference c(G). For 3-connected cubic graphs
circumference grows as n^{0.75+} (Bilinski et al.), so this loophole demands
low connectivity — and with cut vertices, cycles confine to blocks, which is
exactly the block program (notes/block-program.md): the real object is one
2-connected block, and within a 2-connected graph the circumference is again
polynomially large in the cited cubic setting (Bondy–Simonovits-type bounds
do not apply; this note did not establish an explicit bound for the full
B0 class). The block reduction and the circumference loophole
are the same observation seen from two sides, and they both terminate at:

**A counterexample = a 2-connected graph (≤1 degree-2 vertex) whose
circumference c sits just below a power of 2, with engineered fat holes at
the O(log c) powers below c.** Small c is the friend: every unit of
circumference above 2^k−1 buys another octave of required holes.

So the interesting extremal quantity is not order but **circumference vs
spectrum**: how large can a 2-connected, min-degree-3-except-one graph be
while keeping c(G) ≤ 63 (say)? If δ≥3 2-connected forces c(G) ≥ f(n) with
f unbounded (almost certainly true — long-cycle theorems), the block is
bounded in ORDER by circumference constraints, and a search is complete
once n exceeds that bound. Such an f would give a *finite* question per
circumference cap; this note leaves the applicable bound unresolved.

(Known start: Erdős–Gallai-type / Bondy: 2-connected + δ ≥ 3 gives
c ≥ min(n, 2δ) = 6 only — weak; for cubic graphs stronger long-cycle
results exist.)

## 3. Relation to the completed campaign

1. **Block/B0 ladder** (completed through n=32): searches the correct object;
   every rung transfers to a statement about all counterexamples of any order.
2. **Census 2048–10000** (completed): the only known fat-hole factory is
   arc-transitivity; the sweep found 689 {4,8,16}-free graphs, all containing
   C32, C64, and C128, and supplied Rosetta objects for mechanism study.
3. **Algebra worktree**: mechanism theory of C2030.1's fat hole; re-scoped by
   trace-Moore to cycle-only holes; the orbit-count heuristic favors |Aut|
   as large as possible relative to the walk count at
   the target power — i.e., L ≲ lg(96n²) + lg L ≈ 2 lg n + const: **fat
   holes at 32 are orbit-plausible only for n ≳ 2^{13}-ish** unless the walk
   structure is highly degenerate.
4. **[46,63] direct window**: needs girth ≤ 8 AND fat holes at 16 and 32
   with |Aut| ≤ 48·63 ≈ 3000 against ~2·10^3 and ~7·10^7 generic counts —
   requires either massive spectral degeneracy or circumference < 32 (is a
   2-connected δ≥3 graph on 46–63 vertices with circumference < 32
   possible? — concrete sub-question, checkable by SAT with a longest-cycle
   bound... note c < 32 kills the C32 requirement entirely and leaves
   {4,8,16} only!). **Capped search class: 2-connected, ≤1 deg-2, n ∈
   [46,63], no C4/C8/C16, circumference ≤ 31.** If such exists it IS an
   α-block (nothing longer than 31 exists, so 32+ vacuous). The capped
   attempts stopped without a verdict; see `STATUS.md`.

## 4. Honest odds update

The first-moment argument killed generic search; trace-Moore kills spectral
certification at 64 below 2^31; orbit counting now bounds symmetry's reach
too. The surviving corners are narrow and specific: (a) an α-block with
small circumference (§3.4), (b) an arc-transitive/near-AT object at
n ∈ [2^13, 10^4] with degenerate walk structure, (c) something outside these
frameworks. At closure, (a) had no completed capped-cell verdict; the full
arc-transitive census through 10,000 tested the AT portion of (b) and found
no counterexample. These are scoped results, not a resolution of the conjecture.
