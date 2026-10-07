# Disjoint-routing strip closure and four-link gluing

**Scope/status:** Finite complete exclusions in explicit libraries and architectures; includes one 18-vertex six-terminal cell.

**Retained source:** [eg_interface_phase_research_note.md](../provenance/eg_interface_phase_research_note.md).

**Executable evidence:** [experiments/03-phase-interfaces](../experiments/03-phase-interfaces/). Internal code/data paths in the extracted research text below are relative to that experiment directory. The section text is preserved from the source note; later corrections and superseding claims are indexed in [CORRECTIONS.md](../CORRECTIONS.md).

---

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
