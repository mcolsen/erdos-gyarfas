# The exhaustive 181-cell interface census

**Scope/status:** Exhaustive only in the stated degree, terminal-count and biconnectivity domain. Its seven unresolved entries are historical filter outcomes; the separate 554 catalogue is not the same domain.

**Retained source:** [eg_interface_phase_research_note.md](../provenance/eg_interface_phase_research_note.md).

**Executable evidence:** [experiments/03-phase-interfaces](../experiments/03-phase-interfaces/). Internal code/data paths in the extracted research text below are relative to that experiment directory. The section text is preserved from the source note; later corrections and superseding claims are indexed in [CORRECTIONS.md](../CORRECTIONS.md).

---

## 1. Conventions

All actual graphs are finite, undirected, and simple. A cycle is simple, not necessarily induced. Forbidden lengths are 4, 8, 16, and so on; length 2 is not a simple cycle in these graphs.

A cell has degree two at each terminal and degree three at every other vertex. One external edge incident to each terminal would restore cubicity. Except for the separately included singleton cap, terminals occupy distinct vertices. A cell with k terminals is sometimes called a k-pole; the data here specify ordinary graph edges and terminal lists explicitly, avoiding ambiguity about external half-edges.

For a terminal pair i,j, write P_ij(x) for the polynomial counting simple internal i-to-j paths by edge length. We also use the **contribution support** S_ij, containing each such length plus one. Counting one intercell edge per visited cell makes the sum of contributions equal to the length of an expanded cycle.

Products of ordinary polynomials count independent path choices. Boolean polynomial multiplication, equivalently Minkowski addition of supports, tests possible lengths without multiplicity. A path may pass through another terminal whose external edge is not selected. Disallowing that would incorrectly discard valid simple paths.

When a cycle visits each quotient vertex only once, its chosen internal paths lie in distinct cells and are automatically disjoint. For interfaces with more than three external edges, other global cycles may revisit a cell. Those need additional disjoint-path routing states; single-path polynomials alone do not enumerate all global cycles.

## 2. A finite inheritance screen with an all-orders consequence

### 2.1 The four-turn block lemma

Let S range over the contribution supports of one cell. Suppose a fixed dyadic integer c satisfies

    4c belongs to S1 + S2 + S3 + S4

for **every** choice of four terminal-pair supports, with repetitions allowed.

Then every quotient cycle of dyadic length r >= 4 has an expanded simple cycle of length cr. Partition its r visited cells into consecutive blocks of four. In each block choose paths with total contribution 4c. The choices in different cells are independent, giving total length cr. Because c and r are powers of two, cr is also a power of two.

The quotient is assumed simple for this reduction. In a uniform k-terminal replacement of a simple k-regular quotient, k >= 3, a counterexample upstairs would therefore require a smaller counterexample quotient. This does not prove the conjecture on arbitrary quotients. It also does not automatically exclude a mixed library whose cells have incompatible block multipliers.

A common dyadic contribution present in every turn support is an even simpler sufficient certificate. These direct certificates are counted separately below.

### 2.2 Removing redundant supports

If T and S are both actual turn supports and T is a subset of S, proving a universal sumset condition for T is enough when S occurs: the path lengths selected from T are available in S. Thus it suffices to check the inclusion-minimal supports. The verifier independently enumerates all terminal paths and verifies the minimal-support list before using it.

Four-turn support sums are commutative, so unordered multisets suffice. This is not an assumption about cyclic symmetry of the actual port assignment; it only reduces a local additive test.

### 2.3 Census domain and completeness argument

The census includes all biconnected simple cells with:

* degrees only two and three;
* 3 through 7 degree-two terminals;
* at most six degree-three vertices;
* no internal power-of-two cycle.

If there are no degree-three vertices, biconnectivity makes the cell a cycle. Otherwise suppress all degree-two vertices. The result is a loopless, biconnected cubic multigraph. A loop would correspond to a cycle attached to the rest through a single branch vertex, contradicting biconnectivity. The number of cubic vertices is even, so it is 2, 4, or 6 in this domain.

The supplied generator exhausts the cubic multigraphs of those orders, retaining 1, 2, and 5 skeleton isomorphism classes, respectively. It then exhausts edge subdivisions with the prescribed number of terminals. Parallel edge lengths are sorted, and subdivision assignments are canonicalized under all skeleton automorphisms. At most one member of a parallel class may have length one, so the expanded graph is simple. Every expanded cycle corresponds to a skeleton cycle with the corresponding sum of edge lengths, including two-edge skeleton cycles.

This produces the following nonisomorphic cells:

| Number of terminals | Cells |
|---|---:|
| 3 | 3 |
| 4 | 4 |
| 5 | 11 |
| 6 | 46 |
| 7 | 117 |
| **Total** | **181** |

A fresh rerun of the generators agreed edge-for-edge and terminal-list-for-terminal-list with the retained catalogue. Independently, the verifier checks every graph and every terminal path spectrum with NetworkX, checks pairwise nonisomorphism, and reproduces all nine qualifying graphs of order at most seven from NetworkX's graph atlas. Full completeness rests on the suppression argument and exhaustive generator, not merely on that small-order control.

### 2.4 Filter results

| Status | Cells | Meaning |
|---|---:|---|
| Direct dyadic contribution | 3 | All-order uniform inheritance certificate |
| Four-turn block certificate | 149 | All-order uniform inheritance certificate |
| Explicit dyadic C4 inheritance failure | 22 | One actual four-turn sumset contains no power at all |
| Unresolved by these filters | 7 | Neither a certificate nor the tested four-turn failure |

The verifier checks 83,161 four-turn cases for the 149 block certificates. A failure to find a common multiplier is **not** counted as an escape: the 22 escape records contain the actual turn supports and their complete sumset, checked to be power-free. The seven unresolved cells are not excluded, and their bounded-test status is not evidence that they work globally.
