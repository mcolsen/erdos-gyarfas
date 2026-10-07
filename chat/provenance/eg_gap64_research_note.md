# A five-power-free cubic graph, turn-charge obstructions, and a gapped-cell test

## Results and their scope

The retained graph `data/eg26550.edge` has 26,550 vertices and 39,825 edges. It
is simple, connected and cubic. It contains no C4, C8, C16, C32 or C64. In fact,
it has no cycle at any length16–64, inclusive. It has exactly630 C65s, and an
explicit C128 is supplied. It is **not a counterexample** to Erdős–Gyárfás.

The accompanying mathematical results are:

* A joint cyclic-cover / terminal-path design certificate that eliminates
  entire families of cycles rather than deleting their members individually.
* A necessary inequality for counterexamples assembled from the existing
  3-,7-,15-vertex cells on a bridgeless cubic core. In particular, an all-T7/T15
  assembly on such a core can never be a counterexample.
* Closure of the safe triangle-composition grammar: starting with a single
  cubic vertex, this operation produces only T3,T7,T15 as internally
  power-free nontrivial cells, up to terminal isomorphism.
* A genuinely gapped five-terminal theta cell, an odd-necklace obstruction,
  and a constructive fourfold cycle-dilation theorem explaining why uniform
  use of that cell does not bypass the conjecture on the quotient graph.

No assertion of smallest possible order, new publication priority, or a proof
of the full conjecture is made. The larger order introduces further forbidden
powers that a genuine counterexample would also have to avoid. Passing a
longer initial list is a construction milestone, not evidence that the final
counterexample is now one local modification away.

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

## 2. Constructing the 26,550-vertex graph

### The fixed base and the cyclic cover

Define the126-vertex base B explicitly by the LCF specification

```
[17,27,-13,-59,-35,35,-11,13,-53,53,-27,21,57,11,-21,-57,59,-17]^7.
```

The saved edge list is authoritative and is independently checked to be
simple, connected, bipartite and cubic. Its girth is12. The complete cycle
counts through length20 are

|Length|Base cycles|
|---|---:|
|12|1,008|
|14|864|
|16|3,780|
|18|14,112|
|20|51,408|

There are no shorter or odd cycles in this range.

Fix the saved spanning tree. The other64 edges carry voltages in the cyclic
group Z/15Z; tree edges have voltage0. This is a cyclic **group**, not a field:
15 need not be prime for the construction or verifier. Direct an edge from
its lower-numbered endpoint a to b and write its voltage as z(a,b), with
z(b,a)=-z(a,b). The cover has vertices(a,t), t mod15, and edges

```
(a,t) -- (b,t+z(a,b)).
```

It is a connected cubic bipartite graph H on1,890 vertices. The voltage
assignment is included in `data/design.json`. Connectivity is checked both
by actual graph traversal and by the gcd of the cotree voltages with15.

Of the base cycles above, the voltage-zero cycles are

|Length|Voltage-zero base cycles|Lifted core cycles|
|---|---:|---:|
|12|0|0|
|14|94|1,410|
|16|303|4,545|
|18|971|14,565|
|20|3,465|51,975|

An independent BFS computation gives girth(H)=14.

### Why this finite cycle list suffices

The projection of a simple cycle in a graph cover is a cyclically
nonbacktracking closed walk. In a graph of girth g, any such walk of length
less than2g is simple: split at a repeated vertex; each of the resulting
closed nonbacktracking portions contains a cycle and has length at least g.
Thus both portions together would have length at least2g.

Here 2g=24. Every relevant core cycle of length at most21 therefore projects
to a simple base cycle. Since the base is bipartite, only lengths through20
need enumeration. A base cycle yields core cycles of the same length exactly
when its voltage is0; it then yields15 such cycles.

This avoids the usual mistake of ignoring nonsimple projections in a cover.
They are excluded **in this particular range by a proved girth bound**, not
assumed away in general.

### Choosing the cell interfaces

At each base vertex the design chooses T7 or T15 and one of its three
neighbours to receive the distinguished terminal. The same choice is used
at all15 vertices of that fibre.

For a core cycle, let q_v=1 when it avoids the distinguished port at v, and0
otherwise. The minimum expanded length is

```
L(C) = sum_{T7 vertices}(3+q_v) + sum_{T15 vertices}(4+2q_v).
```

The integer program requires L(C)>=65 for all4,833 voltage-zero base cycles
through length20. It minimizes total base-cell order. Its retained feasible
assignment has111 T15 and15 T7 choices per fibre orbit. Hence the full graph
uses1,665 T15 cells and225 T7 cells, giving

```
15*(111*15 + 15*7) = 26,550 vertices.
```

The timed solver found a feasible objective1770 with a bound1707. It did not
prove optimality. No conclusion relies on its bound, tolerance, or status:
the returned discrete assignment is checked directly with integer arithmetic.

### Proof of the forbidden-length gap

An internal cycle has length at most15 and is not4 or8. A noninternal cycle
projects to a simple cycle of H. If it visits at most21 cells, its projection
is one of the finite base cycles just checked, so its minimum length is at
least65. If it visits22 or more cells, each contributes at least3 edges, so
its length is at least66.

Therefore no cycle has length16–64, and no internal or external cycle has
length4 or8.

Exactly42 of the voltage-zero base cycles attain minimum65. Each has15
lifts, and each shortest path inside each cell is unique. Consequently the
number of C65s is exactly42*15=630. Any longer core cycle is too long to
contribute another C65.

The C++ weighted-core verifier independently explores8,763,709 DFS states on
H, without consulting the voltage equations, and finds no core cycle of
minimum expansion weight below65 and exactly630 of weight65. This provides
a separate check of the finite-projection calculation.

### Why the C128 is unsurprising, and why trace-zero is the wrong certificate

Explicit C65 and C128 vertex lists are supplied and checked against the
26,550-vertex edge list. This is not a claim to have counted all C128s.

Indeed, any14-cycle of this core must contain at least five T15 cells to
achieve minimum length>=65: with s T15s its minimum is at most56+2s. But its
maximum is98+8s>=138, while its minimum is at most84. Its interval therefore
contains128. Reorienting the cells cannot remove all C128s on this particular
core while retaining the C64 hole.

The graph deliberately admits nonsimple nonbacktracking closed walks of
forbidden lengths. Within T7, the cyclic walk

```
2,1,3,2,0,5,6,3
```

has length8 and no immediate backtracking, including at closure. Repeating
it eight times gives a cyclically nonbacktracking64-walk, despite the absence
of a simple C64. A certificate based on vanishing nonbacktracking trace would
therefore reject this useful construction. The distinction between simple
cycles and closed walks is essential.

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

## 4. Safe triangle recursion closes after15 vertices

Start with a singleton T1 having three external half-edges. An operation
takes three three-terminal cells, joins them around a triangle, using two
ports in each child, and leaves its third port exposed. Retain only results
whose internal cycles avoid every power of two.

If the children are power-free, the only additional cycles traverse the
three children. Their lengths are3 plus the sum of one terminal-path length
from each child. For children drawn from T1,T3,T7,T15, their supports are
intervals. Exhausting the20 unordered child multisets and27 exposed-port
choices gives540 finite cases. The only safe results are

```
(1,1,1) -> T3
(1,3,3) -> T7
(1,7,7) -> T15, with both T7 exposed ports distinguished.
```

The retained finite table includes a particular forbidden cycle length for
every rejected case. Swapping the two joined ports does not change the
path-length sum. In the surviving cases those swaps are also absorbed by
child automorphisms, so they introduce no new terminal-isomorphism type.
Induction proves closure of this entire grammar. A nominal31-vertex next
cell, for example, would contain a forbidden16-cycle.

This is not a classification of arbitrary power-free three-terminal graphs.
It rules out obtaining new cells solely by this specific recursive operation.

## 5. Genuine gaps: a five-terminal theta cell

Let Q consist of three internally disjoint branch-to-branch paths of lengths
2,3,3. Label its branch vertices5,6 and its terminals0–4, with edges

```
5-0  0-1  1-6  5-2  2-3  3-6  5-4  4-6.
```

Its only internal cycles are two C5s and one C6. Its ten terminal pairs have
four support types:

```
A = {1,4,5}        pairs01,23
B = {2,4,5}        pairs02,13
C = {2,3,5,6}      pairs04,14,24,34
D = {3,4,6}        pairs03,12.
```

These are genuine gaps, not just increased distance. For example an A-pair
has paths of lengths1,4,5 but no paths of length2 or3.

A five-edge interface permits a simple global cycle to cross a cell four
times. Correct evaluation must retain two mutually vertex-disjoint internal
paths, including their pairing of the four used terminals. The supplied
routing certificate enumerates all15 four-terminal pairing states, not just
the ten single-path polynomials. One state, `(0,3),(1,2)`, is impossible.
This is why a three-terminal simple-quotient formula cannot be used unchanged.

### An odd-necklace obstruction

If two Q cells are connected by two edges, all cycles crossing those two
edges have lengths2+S+T for their chosen terminal-pair supports. The only
support-type pairings avoiding both4 and8 are A-D and D-A.

Within one Q, partitioning four terminals into two disjoint pairs of types
A or D can only give A-A or D-D, never A-D. Therefore cells in a double-edge
necklace must alternate these two states. An odd necklace is impossible.
This elementary parity certificate covers every odd length, not just a
bounded search. Independently, all120^3=1,728,000 labelled port assignments
on the three-cell double-edge triangle were checked, with zero C4/C8-free
survivors.

### A stronger surprise: the gaps permit universal fourfold cycle dilation

For every r>=3 and every sequence of r turn types chosen from A,B,C,D,
there are path lengths summing to **3r**. Adding the r intercell edges gives
a simple cycle of length **4r** above any simple r-cycle in a loopless quotient.

Here is a constructive proof. Types C,D contain3. Every pair of A/B turns
can be assigned lengths summing6; every triple can be assigned lengths
summing9:

```
AA: 1+5     AB: 1+5     BB: 2+4
AAA: 1+4+4  AAB: 1+4+4  ABB: 1+4+4  BBB: 2+2+5.
```

Thus two or more A/B turns can be grouped into pairs and, when necessary,
one triple. If there is only one A, balance it with a C using4+2, or with
two Ds using1+4+4. If there is only one B, use a D with2+4, or two Cs with
5+2+2. The remaining turns use3. Those cases exhaust all r>=3.

The balancing verifier checks the construction on all87,360 ordered A/B/C/D
sequences of lengths3–8 as a regression test. The finite case argument above,
not that bounded test, proves all lengths.

**Consequently a uniform Q assembly on a simple5-regular quotient cannot
produce a counterexample unless its smaller quotient is already a
counterexample.** Any dyadic quotient cycle becomes another dyadic cycle,
scaled by4. Individual path gaps are not enough: they can disappear under
sums around a whole cycle.

The conclusion extends to full assemblies allowing port connections within
a cell or parallel links, provided the final graph is simple and C4/C8-free.
An internal port edge can only be of type B; it changes Q to a three-terminal
seven-vertex cell E with all terminal paths2–6. No second internal edge is
safe. E participates in the balancing proof because it contains both the C
and D supports. A double link incident to E always produces C8. Three
parallel links between Q cells always produce C4 or C8, since their three
terminal pairs cannot all be A/D pairs (A union D forms a4-cycle). Thus each
E cell has three distinct neighbours and each remaining five-terminal Q
cell has at least three distinct neighbours. The simple underlying quotient
has minimum degree>=3, and its dyadic cycles again lift to dyadic cycles.
This is a reduction, not a proof that the conjecture holds for every possible
quotient.

### A separately checked unsuccessful experiment

I assembled Q cells on the42-vertex incidence graph of the projective plane
over F4, obtaining294-vertex cubic graphs. The core has1,120 C6s and7,560 C8s.
The30 distinct local terminal configurations were searched using exact
projected C16 counts. Projections relevant to C16 are simple because the
quotient has girth6 and the projected walk length is at most8<12.

A bounded10-second search evaluated1,043,146 proposals and improved C16 from
291 to122, but did not reach0. A full-graph, gadget-independent cycle counter
verified the saved graph has C4=C8=0 and exactly122 C16s. This is not an
optimality or impossibility result. The stronger dilation theorem, discovered
while analysing this experiment, explains why its quotient's C8s make this
uniform family unsuitable as a shortcut to a full counterexample.

## 6. Interpretation and limitations

The construction proves that structural certificates can eliminate a long
band of simple-cycle lengths at moderate order while permitting abundant
non-simple walks. The two obstruction arguments establish that an all-T7/T15
bridgeless assembly cannot be a counterexample, and a uniform theta-cell
assembly transmits dyadic quotient cycles.

They do not exclude mixed T3/T7/T15 cores satisfying the charge bound and the
previous cycle-incidence tests, cores with bridges, arbitrary other cells,
or mixed-arity assemblies not covered by a common dyadic-dilation rule.
The experiments show why individual path gaps do not suffice: composition
can fill them, and four-terminal routing states are required when a simple
cycle can revisit a cell. These are limits of the tested representations,
not evidence that any untested family yields a counterexample.
