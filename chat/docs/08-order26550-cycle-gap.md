# The 26,550-vertex graph: no C4, C8, C16, C32, or C64

**Scope/status:** Retained complete cubic graph; exact structural certificate and explicit C128 witness.

**Retained source:** [eg_gap64_research_note.md](../provenance/eg_gap64_research_note.md).

**Executable evidence:** [experiments/02-gap64](../experiments/02-gap64/). Internal code/data paths in the extracted research text below are relative to that experiment directory. The section text is preserved from the source note; later corrections and superseding claims are indexed in [CORRECTIONS.md](../CORRECTIONS.md).

---

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
