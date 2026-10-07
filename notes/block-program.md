# The block program: Erdős–Gyárfás is exactly a one-blemish block problem

*Status: theorem proved below (elementary); skeleton verified by exhaustive
cycle enumeration; SMS ladder complete with zero candidates through n=32.
Higher rungs stopped incomplete; see `STATUS.md`. This lane is independent
of, and complementary to, the algebraic program.*

## 1. The reduction

Call a graph a **B0-block** if it is 2-connected and has at most one vertex of
degree 2, all other vertices having degree ≥ 3. Call it an **α-block of order
b** if additionally its cycle spectrum avoids every power of 2 that is ≤ b
(equivalently: avoids {4, 8, 16, 32, 64, …} entirely, since no cycle exceeds b).

**Theorem (block equivalence).** The Erdős–Gyárfás conjecture is false if and
only if an α-block exists. Moreover, from any α-block of order b one
constructs, for infinitely many n, counterexamples of order n with min degree 3.

*Proof.* (⟹) Let G be a counterexample (δ(G) ≥ 3, no power-of-2 cycle,
finite). Consider its block–cut tree; let B be a leaf block. B cannot be a
bridge (K₂): a leaf block contains at most one cut vertex of G, and a bridge's
non-cut endpoint would have degree 1 in G. So B is 2-connected. Every
non-cut vertex of B has all its G-edges inside B, hence degree ≥ 3 in B; the
one cut vertex (if any) has B-degree ≥ 2 by 2-connectivity. Cycles of B are
cycles of G, so B avoids all powers of 2 up to |B|. B is an α-block. ∎(⟹)

(⟸) Let B be an α-block. If B has a degree-2 vertex w, take two disjoint
copies of B and identify their copies of w: the merged vertex has degree 4,
every other vertex keeps its B-degree ≥ 3, and the identified vertex is a cut
vertex, so every cycle of the union lies inside one copy — the spectrum is
unchanged. If B has no degree-2 vertex it is itself a δ≥3 counterexample.
For infinitely many orders, glue more copies in a star/tree pattern (cycles
never cross cut vertices). ∎

**Why this matters computationally.** Every published and campaign search
(Markström cubic; Royle/Balaji/campaign δ≥3; bipartite and structural
ladders) required minimum degree ≥ 3 at *every* vertex. The α-block target
allows **one vertex of degree 2**, and that relaxation is genuinely outside
all searched spaces: suppressing the degree-2 vertex of a candidate α-block
of order n gives a δ≥3 (multi)graph of order n−1 which need *not* be
power-of-2-free — it must only be power-free *off one edge* e, while carrying
no cycle of length 2^k−1 *through* e (subdividing e shifts those to 2^k).
The frontier ladders say nothing about such graphs. Concretely: the δ≥3
frontier (≥ 36) and cubic frontier (≥ 46) do NOT imply α-blocks of those
orders don't exist.

A B0-ladder UNSAT result at all orders ≤ N yields a statement *stronger* than
an order frontier: **every counterexample of any order has all its leaf
blocks larger than N vertices** (in particular none exists of order ≤ N, and
none of any order whose block structure has a small leaf).

## 2. The Mersenne twist

Via the suppression view, an α-block with a genuine degree-2 vertex at order
n ⟺ a δ≥3 graph H of order n−1 with a (possibly parallel) edge e such that:

- every cycle of length 4, 8, 16, … in H passes through e, and
- no cycle of length 3, 7, 15, 31, … (Mersenne, 2^k−1) passes through e.

So the one-blemish problem couples the powers of 2 with the Mersenne numbers
— the degree-2 vertex is "half an edge", and odd–even interplay appears that
none of the δ≥3 machinery sees. (Checked on the four n=24 {C4,C8}-free cubic
graphs: they have 138–330 sixteen-cycles and 138–245 fifteen-cycles, and no
edge covers all C16s while avoiding C3/C7/C15 — no cheap α-block from known
specimens; script `scratchpad/verify_block_idea.py`.)

## 3. Skeletons: one α-block already suffices in bulk

The two-copy gluing needs nothing else, but α-blocks also compose with
*power-free subdivision skeletons* into counterexamples of any size. Verified
example: subdivide the six edges of K4 into paths of lengths
(w₁₂,w₃₄,w₁₃,w₂₄,w₁₄,w₂₃) = (1,3,2,3,2,3). The resulting 12-vertex graph has
cycle spectrum exactly **{6, 7, 9, 10}** (counts 2/1/3/1; exhaustively
enumerated) — no power of 2 — with 8 degree-2 subdivision vertices. Gluing an
α-block copy onto each degree-2 vertex yields counterexamples with any
number of skeleton blocks. (Mod-4 view: all seven cycle sums ≢ 0 (mod 4),
and powers of 2 ≥ 4 are ≡ 0 (mod 4).) This is the "assembly line" — the
entire difficulty of Erdős–Gyárfás is compressed into the single finite
object of §1.

## 4. Search implementation and outcome

Space: min degree ≥ 2 with at most one degree-2 vertex ("≤1-deg-2"), all
powers of 2 ≤ n forbidden; connectivity NOT encoded (dropping it enlarges the
space, so UNSAT stays sound for the block frontier; any SAT hit gets its
2-connectivity and spectrum verified independently).

- `src/encode_b0.py` — pysms CNF: minDegree(2) + per-vertex sequential
  counter (two-sided, per pysms source) + pairwise (deg3_u ∨ deg3_v).
- Count-exact validation against a disjoint geng stack (geng -d2 + p2check -F
  + degree filter) at n = 8..11, full space and {4,8}-forbidden, before any
  frontier claim.
- The ladder returned zero throughout n=10..32. The n=31 single run was
  cross-checked by cube shards; n=32 was settled by a complete 997-cube
  partition of the {4,8,16}-free superset. Attempts at n=33 and n=34 stopped
  incomplete and yielded no verdict; see `STATUS.md`.

## 5. Honest assessment

The relaxation is one vertex, but the completed ladder only establishes the
block frontier through n=32; the interrupted higher rungs give no verdict.
The original hypothesis was that degree-driven constraints would make the
B0 ladder track the δ≥3 ladder a rung or two higher; this was not established.
The structural value is independent of further enumeration: (a) an α-block
at any order composes into counterexamples; (b) the Mersenne coupling of §2
relates this relaxation to the original search space; (c) a verified α-block
would refute the full conjecture.
