# Interfaces that break dyadic cycle inheritance

## Outcome and scope

This investigation follows the exact gadget-compression and turn-charge work in `eg_gap64_research_note.md`. The goal was to reject interfaces that automatically transmit power-of-two cycles, then test interfaces escaping that rejection **together with their degree-completion requirements**.

The main positive result is an explicit eight-vertex, six-terminal cell with an **all-scale phase-hole rule**. A dyadic quotient cycle can be expanded into an entire cycle family containing no power-of-two length. The rule is exact: among two specified passage types, the quotient cycle must use exactly one exceptional passage.

There is **no counterexample and no new minimum-degree-three construction in this bundle**. The explicit 32-, 40-, and 64-vertex boundary graphs have degree-two terminals. Their cycle spectra have been independently enumerated, but their deficient degrees are essential unresolved defects. Completing these degrees is not a cosmetic last step.

Other retained results are:

* An exhaustive census of 181 small interfaces in a precisely specified domain. Finite, all-orders inheritance certificates eliminate 152 as uniform replacement shortcuts. Twenty-two have explicit four-cycle inheritance failures. Seven are unresolved by the filters used here.
* An exact disjoint-routing transfer system for three-edge strip interfaces. A finite closure certificate proves that no strip of three cells from the 46-cell six-terminal census library is power-free, irrespective of port permutations.
* One additional 18-vertex six-terminal cell obtained by four-edge gluing of seven-terminal cells. All eight retained labelled gluings give one isomorphism class.
* Explicit forbidden-path witnesses and constraint certificates excluding several natural repairs of the phase-hole boundary graphs. In particular, none of 184 cap templates can attach all of its terminals to distinct deficient vertices of either the 32- or 40-vertex seed while preserving power-freeness.

No publication-priority or novelty claim is made. The original generators are supplied, and a separate verifier checks graph data, path spectra, route spectra, closure certificates, and repair exclusions. These are independently executable finite checks, not proof-assistant formalizations.

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

## 3. An explicit all-scale phase hole

### 3.1 Cell definition

Let H be the theta graph whose branch-to-branch paths have lengths 2, 3, and 4. Its vertices are 0 through 7 and its edges are

    0-2  0-3  0-5  1-2  1-4  1-7  3-4  5-6  6-7.

Vertices 0 and 1 have degree three. The six terminals are 2,3,4,5,6,7. Its three internal cycles have lengths 5,6,7, one of each.

Use these two terminal-pair passages:

* A: from terminal 5 to terminal 7;
* B: from terminal 2 to terminal 6.

Their internal path polynomials are

    P_A(x) = x^2 + x^4 + x^5,
    P_B(x) = 2x^3 + 2x^6.

Including one external edge, the contribution polynomials are

    Q_A(x) = x^3(1+x^2+x^3),
    Q_B(x) = 2x^4(1+x^3).

All of these multiplicities were independently checked by direct simple-path enumeration.

### 3.2 Exactly one exceptional turn is necessary and sufficient

Let a quotient cycle have dyadic length r >= 4. Suppose a of its cells use passage A and the other r-a use B. Its expanded-cycle polynomial is

    F_(r,a)(x) = 2^(r-a) x^(4r-a)
                 (1+x^2+x^3)^a (1+x^3)^(r-a).

Its support lies between 4r-a and 7r-a. Since 0 <= a <= r,

    2r < 4r-a <= 4r <= 7r-a < 8r.

Thus the only possible power of two in that support interval is 4r. Its coefficient is positive exactly when the residual polynomial contains exponent a.

If a=0, that is the positive constant coefficient. If a=1, it is absent: the residual factors have no way to contribute an increment of one. If a>=2, write a=2p+3q with p,q nonnegative; every integer at least two has such a representation, and p+q<=a. Choosing p factors contributing x^2 and q factors contributing x^3 from the a copies of (1+x^2+x^3) makes the coefficient positive.

Therefore

    the expanded family is power-free  <=>  a = 1.

In particular, with exactly one A passage,

    F_r(x) = 2^(r-1) x^(4r-1)
             (1+x^2+x^3)(1+x^3)^(r-1),

and the coefficient at x^(4r) is zero for every dyadic r >= 4.

This is a genuine internal hole, not a lower bound pushing all cycles beyond a forbidden length. There are cycles on both sides of the missing power. It is also more informative than a congruence restriction on one terminal pair: a single exceptional passage and the other passages must compose in exactly the right way.

The all-orders proof is the elementary argument above. The verifier additionally tests every possible A-count for r=4,8,16,32 as a regression control; those finite tests are not presented as the proof for arbitrary r.

### 3.3 Explicit boundary graphs

Take r copies of H. In each cell designate the two selected terminals as incoming and outgoing and join the outgoing terminal of cell j to the incoming terminal of cell j+1 cyclically. For dyadic r, use one A cell and r-1 B cells. Each cell still has four unused terminals of degree two.

There are only two types of simple cycle: one internal to a cell, or one traversing every cell of the ring. A cycle cannot cross a two-edge cell boundary more than twice. Thus the complete cycle polynomial is

    r(x^5+x^6+x^7) + F_r(x).

The retained examples are:

| r | Vertices | Edges | Degree-two vertices | Degree-three vertices | Total simple cycles | Circumference |
|---|---:|---:|---:|---:|---:|---:|
| 4 | 32 | 40 | 16 | 16 | 204 | 27 |
| 8 | 64 | 80 | 32 | 32 | 49,176 | 55 |

Both graphs contain no power-of-two simple cycle. For r=8, there are 128 cycles of length 31 and 128 of length 33, but zero of length 32. This illustrates the phase hole directly.

A separate five-cell ring using A at every cell has polynomial

    5(x^5+x^6+x^7) + x^15(1+x^2+x^3)^5.

Its external lengths lie in [15,30], whose only candidate power is 16; the increment-one hole excludes it. This 40-vertex boundary graph has 20 vertices of each degree, 258 simple cycles, and circumference 30.

The verifier reconstructs all three edge lists and independently enumerates **every simple cycle** using NetworkX. It agrees with every coefficient of these polynomials. The graphs are biconnected but not cubic and do not satisfy minimum degree three. No comparison with lower bounds for minimum-degree-three counterexamples is claimed.

## 4. Exact routing through strips

### 4.1 Why single-path polynomials are not enough

For six-terminal cells, divide the terminals into three on the left and three on the right. Joining consecutive cells by a matching of three edges makes a strip. A simple cycle crosses each such separating cut zero or two times. But a path running between two exposed right terminals may enter the old strip and return, using **two vertex-disjoint paths** inside the new cell. Omitting that state would make the computation unsound.

Let A_i be the support of simple paths in the existing strip between the two exposed right terminals other than i. For a new cell, let:

* L_i be its left-pair path support omitting left terminal i;
* R_j be its right-pair path support omitting right terminal j;
* T_ij be the support of the **sum of lengths of two vertex-disjoint paths**, joining the left pair omitting i to the right pair omitting j, in either bijection.

For supports, '+' below denotes Minkowski addition and union is literal union. The new crossing-cycle supports are

    2 + A_i + L_i.

The updated right-boundary supports are exactly

    A'_j = R_j union union_i (2 + A_i + T_ij).

The extra two counts the joining edges. A simple path between the right endpoints can cross the separating cut only zero or two times, so these cases exhaust it. In the two-crossing case, the old segment is one simple path and the new cell contributes two disjoint segments. This proves the state update; it is not an approximation based on shortest paths.

The three boundary supports can be canonicalized under terminal permutation because all future left-port matchings are included. Once a prefix is internally power-free, its exact boundary signature is sufficient for all future right extensions. Multiplicities are unnecessary for existence tests.

### 4.2 Complete closure for the 46-cell six-terminal library

Using all 46 six-terminal cells in the census, all 3+3 port splits and all joining permutations yields 4,668 distinct cell actions. There are 524 seed boundary signatures. Exact closure finds 553 reachable signatures in total.

Every one of the 553 x 4,668 = 2,581,404 state/action pairs is checked. Only 142 labelled transitions are valid; they collapse to 37 directed signature edges. **No target of one of those edges is the source of another.** Hence there is no two-transition path from any initial cell.

It follows that every three-cell strip from this library contains C4, C8, or C16. A longer strip contains a three-cell segment, so it is also excluded. Joining the end boundaries cannot remove an already internal forbidden cycle. Thus cyclic necklaces of at least three of these cells, connected by three-link interfaces, are also excluded.

This is an exclusion of the specified finite cell library and connection architecture, not of arbitrary six-terminal interfaces. It does not apply after rewiring the seed cells, changing the number of joining edges, or choosing larger cell types outside the library.

The binary certificate has one byte per state/action pair. A rejected pair supplies an omitted-port index, a forbidden power, and a path-length split. The verifier checks that the two registered path supports really sum to that power minus two. Accepted pairs have their full disjoint-routing updates recomputed. The verifier separately reconstructs all 553 representative prefix graphs and checks their actual boundary path spectra and internal power-freeness. All 4,668 actions are also independently rebuilt from NetworkX simple paths and vertex-set disjointness tests.

The retained closure is complete: its queue is empty. Its maximum prefix depth is two and maximum retained order is eighteen. The final reproduction generator has no time cutoff. The independent verifier checks the finite transition system directly without relying on the search's stopping behavior.

## 5. Moving beyond three-link interfaces

As a separate test, pair cells from the full 117-member seven-terminal library and join them across four terminal edges. The six remaining terminals form a larger interface. This permits crossing patterns unavailable in the three-link strip and therefore was not excluded by the previous transfer proof.

The search covers 13,689 ordered cell pairs and all four-port selections and matchings. It visits 4,005,948 backtracking prefix nodes after early forbidden-cycle pruning. These are **prefix nodes**, not a claim that every unpruned complete assignment was individually materialized.

Exactly eight labelled safe gluings survive. All eight are isomorphic and arise from two theta(1,4,5) cells, yielding one 18-vertex, 24-edge six-terminal cell. Its complete edge list is `data/super6.json`. The verifier checks all eight retained gluings, their internal cycle safety, and their common isomorphism class. Completeness of the gluing search is reproducible with the supplied C++ generator and its full completion log.

This extra cell was included in the cap-repair tests below. Its mere existence is not a claim that it breaks every inheritance rule or can repair the phase ring.

## 6. Degree repair is the second essential filter

The phase construction leaves four deficient terminals per cell. A local spectrum with a missing power is useful only if those terminals can be given adequate degree without creating other forbidden cycles. The following exclusions concern the **retained fixed boundary graphs**, not all possible assemblies of H.

### 6.1 Edge additions among existing vertices

Adding a new edge uv creates a forbidden P-cycle whenever the old graph has a simple u-to-v path of length P-1. Every blocked pair has an explicit path witness in the certificate.

All nonedges were tested, including edges from a deficient terminal to an already cubic vertex. Consequently these checks do not impose an unnecessary maximum-degree-three requirement.

| Ring order | Deficient terminals | Terminals blocked from every existing-vertex edge addition |
|---|---:|---:|
| 32 | 16 | at least 13 |
| 40 | 20 | at least 10 |
| 64 | 32 | at least 29 |

Some other additions are safe, so the graphs are **not** wholly edge-saturated. However, one frozen terminal suffices to rule out a completion using only edge additions on the same vertex set. Adding edges cannot destroy the existing forbidden-path witnesses.

The bundle also records admissible pairwise vertex-fusion tests for nonadjacent vertices with disjoint neighbourhoods, but it does not claim to have exhausted arbitrary multi-step fusion and rewiring sequences. Fusion is not monotone in the same way as edge addition.

### 6.2 New hubs, even with already cubic old neighbours

For a new vertex attached to old vertices u and v, an old path of length P-2 creates a forbidden P-cycle. Build the pair-compatibility graph on **all** old vertices. A safe hub with degree at least three requires a clique of size at least three in this compatibility graph.

For the 32- and 40-vertex rings, the graph is triangle-free: no new degree-three-or-higher vertex can be attached solely to old vertices anywhere in those graphs, whether deficient or already cubic.

For the 64-vertex ring, the over-approximate compatibility graph has four triangles. The only deficient vertices they touch are the labelled vertices 3,4,5. Thus at least 29 of its 32 deficient vertices cannot be repaired by one new hub, even allowing the hub's other neighbours to be already cubic vertices. The earlier, more restrictive compatibility check on deficient vertices alone is triangle-free for all three rings.

These statements do not exclude networks of new vertices with edges between them, or altered internal cell connections. Explicit witnesses prove each blocked compatibility edge. The verifier only uses the unblocked edges as an over-approximation, which is sufficient for these exclusions without requiring a proof of every reported legal pair's safety.

### 6.3 A complete cap-attachment constraint test

The cap library contains 184 templates:

    181 census cells + the singleton three-stub cap + T15 + the new 18-vertex six-port cell.

For the 32- and 40-vertex rings, try attaching every cap terminal to a distinct deficient ring vertex. All injections are allowed; no other changes are made. For any two cap terminals i,j attached to f(i),f(j), let S be their internal cap path support and R the old ring path support between f(i),f(j).

A necessary safety condition is

    (2 + R + S) contains no power of two.

Those cycles use exactly two joining edges. If even this pairwise condition is impossible, more complicated four- or six-crossing cycles do not need examination to prove rejection. Conversely, passing it would not by itself certify a safe cap.

An exact injection constraint solver finds **no solution for any of the 184 caps on either seed**. The combined prefix-state counts are 3,162 for the 32-vertex ring and 3,864 for the 40-vertex ring. An independent C++ full-graph incremental cycle gate returns the same negative results. The Python verifier independently reconstructs every old path support and every cap path support, then reruns the pairwise constraint problem and reproduces those state counts.

The 64-vertex seed was not included in this full cap test. The C++ cap probe uses at most 63 vertices, while the independent proof-level scope here is just the two explicitly verified seeds. The exclusions do not cover partial cap attachment, caps outside the listed library, simultaneous interlinked caps, attachment to already cubic vertices for non-singleton caps, or surgeries that replace existing seed edges.

## 7. Interpretation and limitations

Three conclusions follow from the completed experiments.

First, gap screening must use composed support sets, not just a cell's minimum and maximum path lengths. The four-turn lemma supplies small certificates that rule out uniform inheritance shortcuts at every dyadic scale. The phase cell supplies an equally explicit escape that those certificates correctly do not reject.

Second, the escape is fragile in an informative way. On a dyadic A/B cycle, **exactly one A passage** is necessary and sufficient. Zero A passages and every count of at least two restore the forbidden length. This gives an exact-one predicate for a constraint solver tracking those passage types on a selected quotient cycle. It is not a solution of simultaneously satisfying all quotient cycles: other terminal-pair types and multi-visit routing states still have to be included in a complete global model.

Third, inheritance escape alone does not establish boundary repairability. The phase ring has the desired cycle polynomial but extremely restrictive leftover ports. The tested cap library cannot repair the 32- or 40-vertex seed under the attachment conditions in Section 6.3. The exact disjoint-route transition system rules out the 46-cell three-link strip architecture. Larger or differently connected junctions are not excluded by that theorem.

The bundle contains no fully attached graph of minimum degree at least three avoiding all power-of-two cycle lengths through its order. Its local phase-hole result and scoped repair exclusions do not establish such a graph; **all** simple-cycle routing states matter for that claim.

## 8. Verification and retained evidence

Run `python verify.py` with Python 3.10 or later and NetworkX 3.1 or later. No optimization solver, graph census server, network access, or prior research bundle is required. The verifier checks the supplied graphs and certificates rather than rerunning long searches. The sources and commands for regenerating the census and selected search results are in `README.md`.

The verification includes:

* graph validity, nonisomorphism, internal cycles, and terminal paths for all 181 cells;
* a disjoint small-order graph-atlas control;
* all 83,161 block-certificate cases and all 22 explicit inheritance-failure records;
* independent disjoint-route spectra for all 4,668 actions;
* all 2,581,404 strip state/action certificate entries;
* all 553 representative strip graphs;
* all eight retained four-link gluings;
* every simple cycle in the three boundary rings;
* every blocked-pair path witness used in edge and hub exclusions;
* independent full path sets and all 184 cap-attachment constraint problems on both tested rings.

The seven unresolved inheritance cases are intentionally left unresolved. Full census and gluing completeness use their supplied exhaustive generators and domain arguments; finite witnesses are not misrepresented as universal classifications outside those domains.

The predecessor notes and graphs motivated the search but are not needed to verify its results. This bundle replaces no prior graph artifact and makes no new claim about the minimum order of an Erdős–Gyárfás counterexample.
