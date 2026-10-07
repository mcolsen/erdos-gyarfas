# Turn-charge inequality on bridgeless cubic cores

**Scope/status:** The initial bridgeless theorem. The bridge exception is closed for all-T7/T15 in note 26; mixed cells are not generally excluded.

**Retained source:** [eg_gap64_research_note.md](../provenance/eg_gap64_research_note.md).

**Executable evidence:** [experiments/02-gap64](../experiments/02-gap64/). Internal code/data paths in the extracted research text below are relative to that experiment directory. The section text is preserved from the source note; later corrections and superseding claims are indexed in [CORRECTIONS.md](../CORRECTIONS.md).

---

## 1. The three-terminal templates

T3 is a triangle. T7 has vertices0–6, terminals(0,1,4), and edges

```
0-2  0-5  1-2  2-3  3-1  4-5  5-6  6-4  3-6
```

The first terminal is distinguished. T15 is formed from two copies of T7,
offset by1 and8, and a new vertex0, with edges0-2,0-9,5-12. Its terminals are
(0,1,8), with0 distinguished. Every terminal is degree2; every other vertex
is degree3. Joining the terminals according to a cubic core restores cubicity.

A cell has only three boundary edges. A simple cycle crosses its boundary
zero or two times. Thus a noninternal cycle uses one terminal-to-terminal
path in every visited cell and projects to a simple core cycle. Independently
choosing those paths gives all cycles above that core cycle, without overlap.

The possible contributions of a visited cell, including one intercell edge,
are the following **complete integer intervals**:

|Cell|Turn uses distinguished terminal|Turn avoids distinguished terminal|
|---|---|---|
|T3|[2,3]|[2,3]|
|T7|[3,7]|[4,7]|
|T15|[4,15]|[6,15]|

Each shortest terminal path is unique. The internal cycle polynomials are

```
T3:  x^3
T7:  2x^3 + x^5 + 2x^6 + x^7
T15: 2(2x^3 + x^5 + 2x^6 + x^7) + x^9(1+x)^6.
```

Consequently all internal cycles avoid4 and8, and all have length at most15.
The verifiers enumerate these small graphs and their paths directly.

## 3. A global turn-charge obstruction

Consider an arbitrary connected, simple, bridgeless cubic core assembled
from T3,T7,T15. This section concerns avoiding **all** powers, not merely a
finite initial list.

For each core cycle, its expanded lengths fill an interval [L,U]. If that
interval avoids all powers of two, it must fit in a dyadic gap

```
[2^k+1, 2^(k+1)-1].
```

Hence a necessary condition is

```
2L-U >= 3.
```

Assign each vertex turn the additive charge w=2*l-u, where l and u are its
minimum and maximum contributions. The three possible turn charges are

```
T3:  +1,+1,+1
T7:  -1,-1,+1
T15: -7,-7,-3.
```

Their sum around a cycle is exactly2L-U. They can equivalently be represented
by sums of incident half-edge charges:

```
T3:  (1/2, 1/2, 1/2)
T7:  (-3/2, 1/2, 1/2)
T15: (-11/2, -3/2, -3/2),
```

with the first half-edge distinguished.

For a three-edge-colourable core, take its three two-factors obtained by
omitting each colour in turn. Every possible turn occurs once at each vertex.
A two-factor is a disjoint collection of cycles covering every vertex. If
all expanded cycles were power-free, each cycle would have charge>=3, so each
two-factor would have total charge>=3. Adding the three inequalities gives

```
3*n3 - n7 - 17*n15 >= 9.                         (1)
```

The same inequality holds for every bridgeless cubic core. Here the only
external theorem needed is Edmonds's perfect-matching-polytope theorem:
nonnegative edge vectors with vertex sums1 and all odd-cut sums>=1 form the
convex hull of perfect matchings. The constant vector1/3 satisfies those
conditions, because every odd cut in a bridgeless cubic graph has at least
three edges. Therefore there is a distribution over perfect matchings with
each edge marginal1/3. Their complementary two-factors give each possible
turn probability1/3. Averaging charges gives (1).

Reference for that standard theorem: Jack Edmonds, *Maximum matching and a
polyhedron with 0,1-vertices* (1965). The local turn-charge identities and the
remaining inequality proof are elementary. The constructed core is bipartite,
and its three disjoint perfect matchings are explicitly found by the verifier,
so its exclusion already follows from the elementary colourable case.

Allowing unexpanded single-vertex cells T1 changes the left side to
`3*(n1+n3)-n7-17*n15`; the same proof applies.

**Consequences.** With n3=0, inequality(1) is impossible. Thus no all-T7/T15
assembly on a bridgeless cubic core can be an Erdős–Gyárfás counterexample,
regardless of the core's order, girth, voltages or terminal orientations.
The wider T3/T7/T15 family is not excluded: it must obey the density bound.
Cores with bridges and cells with different path spectra are outside this
statement. An interval condition is necessary here because actual gaps can
invalidate the inference from endpoint bounds to a forbidden power.
