# Interface filters beyond fixed dyadic dilation

## Outcome and scope

This continuation did **not** find an Erdős–Gyárfás counterexample or a new complete cubic near-miss. It built and independently verified a collection of interface-level reduction certificates, identified cells that escape those reductions, and gave finite impossibility certificates for three proposed ways of completing protected loops to cubic graphs.

The central results are:

1. A catalogue of **554 connected, internally power-free cells**, with every vertex of degree two or three and every degree-two vertex designated as a terminal. This is a specified construction catalogue, **not** all cells up to an order bound.
2. **466 cells** pass a finite four-turn certificate that implies dyadic-cycle transmission at *every* dyadic quotient length, for uniform assemblies on a simple quotient.
3. A separate constructive theorem proves the same reduction for the pentagon, despite its lacking one fixed dyadic dilation factor. Hence **467** catalogue cells have uniform-assembly reductions.
4. **86 cells** admit an explicit four-turn sequence whose entire expanded cycle-length support is power-free. One other cell remains unclassified by these screens. These are local escape witnesses, not degree-complete counterexamples.
5. Explicit parity, odd-divisor, and narrow-band escape mechanisms occur in a hexagon, a heptagon, and an eleven-vertex seven-terminal cell.
6. Three frozen-backbone cubic-completion attempts fail with checkable upper bounds of **2, 19, and 8** added edges, respectively, versus **20** needed in each.
7. Two mixed-cell synthesis motifs produce **47,647** pairwise-compatible candidate assemblies. Every candidate has a saved and independently checked C8 or C16 witness.
8. An exact interface oracle checks cycles using added links by combining boundary parity, vertex-disjoint internal routing states, and a one-circuit test. It does not assume that a simple full-graph cycle visits a cell only once.

A uniform-assembly reduction means that any counterexample produced in that scope would already contain a smaller counterexample as its simple quotient. It is **not** an unconditional proof that no counterexample exists in every such assembly. The reduction is also not automatically valid for arbitrary mixtures, loops, or parallel quotient links.

No publication-priority or general extremal-order claim is made.

## Reproduction

The bundle needs Python and NetworkX for verification. The executed environment used Python 3.13.5 and NetworkX 3.6.1; `environment.json` records the runtime. No optimizer, compiler, network access, or solver-status interpretation is needed to verify the main certificates.

```sh
python verify_results.py
python oracle_regression.py
```

The first command recomputes every cell's internal-cycle and terminal-path supports, checks the finite reduction certificates, regenerates all 306 hexagon/heptagon routing signatures, validates three completion impossibility certificates, and reconstructs and checks all 47,647 mixed-assembly rejection witnesses. The second compares the interface oracle with full expanded-graph cycle enumeration on 24 small instances.

Optional reconstruction of the catalogue and mixed-motif tests:

```sh
python survey.py
python dilation_screen.py
python test_double_triangles.py
python test_triple_triangles.py
```

`survey.py` reads the retained `cells/*.txt` enumeration outputs. Their completion logs are included. Rebuilding each restricted chord-enumeration scope from scratch is optional:

```sh
c++ -O3 -std=c++17 generate_cells.cpp -o generate_cells
./generate_cells 17 7 60 > candidate_cells.txt 2> candidate_cells.log
```

The third argument is a runtime budget; only a log with `complete=1` establishes a completed scope. The retained completed scopes are listed below. Verification treats the supplied explicit catalogue as authoritative; a witness remains valid without rerunning discovery.

## 1. Cell semantics and catalogue construction

A cell is a connected simple graph with degrees in {2,3}. Its degree-two vertices are terminals, each accepting at most one external edge in a cubic assembly. All internal simple cycles must avoid lengths 4,8,16,32,... . The catalogue contains cells with 3 through 15 terminals.

For terminals a,b, define the exact internal path-length support

    S(a,b) = { |E(P)| : P is a simple a–b path inside the cell }.

Define its contribution support T(a,b)=S(a,b)+1, assigning one external edge to each visit. Above a simple r-cycle in a quotient, with one visit to each cell, the expanded cycle-length support is the sumset

    T_1 + T_2 + ... + T_r.

Independent simple paths in distinct cells give a simple full-graph cycle. This remains a valid *subset* of full-graph cycles even when the interfaces have more than three terminals; other cycles may revisit cells and require joint-routing states.

The explicit catalogue combines:

* cycles of lengths 3,5,6,7,9,10,11,12,13,14,15;
* theta graphs with branch-path lengths 1<=a<=b<=c<=11 and a+b+c<=18, excluding the duplicate-edge case a=b=1;
* a Hamiltonian cycle plus a matching of noncycle chords, at odd orders 3 through 21, with exactly 3,5, or 7 terminals where admissible;
* the previously constructed seven-vertex three-terminal E cell.

Candidates are tested for internal power-freeness and deduplicated by graph isomorphism. The chord enumerator is complete within each retained `(order,terminal_count)` scope; these are restricted Hamiltonian scopes, not general enumeration of cells. Earlier partial order-23 probes contributed no entries and are not included in the certified catalogue scope.

`catalog.json` stores every edge list, terminal list, provenance tag, and exact path support. All 554 graphs have been independently re-enumerated using NetworkX to confirm the data.

## 2. An unbounded reduction from a finite four-turn check

### Four-turn lemma

Let a cell have contribution supports T_1,...,T_s. Suppose there is a dyadic integer d>=2 such that, for every four choices of turn supports,

    4d belongs to T_i + T_j + T_k + T_l.

Then every simple quotient cycle of dyadic length r>=4 in a uniform assembly yields a full-graph cycle of dyadic length dr.

**Proof.** Partition the r visits into consecutive groups of four. In each group, choose internal paths with total contribution 4d. Different visits use different cells, so these choices do not interfere. Their concatenation is a simple cycle of length (r/4)4d=dr. ∎

This is a finite certificate for *all* dyadic r; it is not extrapolation from testing short cycles. Sumset addition is commutative, so four-turn multisets suffice. Inclusion-minimal supports suffice too: any larger support contains the choices guaranteed by a smaller one.

The screen tests d=2,4,8,16,32. **466 of 554 cells have a certificate.** For **86**, it also finds a four-turn sumset containing *no* power of two at all. Those cells demonstrably escape automatic single-traversal inheritance on an appropriately oriented quotient C4.

Two cells have neither result: the pentagon `cell0001` and the eleven-vertex cell `cell0095`. The next lemma resolves the pentagon. The other remains unclassified, not certified promising.

### Why “no common dilation factor” is too weak: the pentagon

A pentagon has contribution supports

    A={2,5}, B={3,4}.

Let a dyadic r>=4 cycle use b B-turns and a=r-b A-turns.

If b=0, choose contribution 2 everywhere, yielding a cycle of length 2r.

If b>=1, choose x A-turns at value 5 instead of 2, and y B-turns at value 4 instead of 3. The length is

    2r + b + 3x + y.

It suffices to solve

    3x+y=2r-b, 0<=x<=r-b, 0<=y<=b.

For b>=2, the integer intervals [3x,3x+b], as x ranges from 0 to r-b, cover every integer from 0 to 3r-2b. The target 2r-b lies in this range. For b=1, dyadic r is nonzero modulo three, so 2r-1 is 0 or 1 modulo three. Choose y to be that residue and x=(2r-1-y)/3; the bounds hold for r>=4. Thus the desired cycle of length 4r exists.

**Every dyadic quotient cycle therefore survives, but the factor can depend on its turns.** All-A turns cannot realize 4r because 3x=2r has no solution; all-B turns cannot realize 2r because their minimum is 3r. This explains why searching only for a single common factor misses a real obstruction.

Together, the four-turn certificates and pentagon lemma give uniform-simple-quotient reductions for **467 catalogue cells**. They do not justify discarding those cells from arbitrary mixed-cell searches. The mixed experiments below deliberately keep them.

## 3. Three explicit interfaces that escape the common mechanism

### 3.1 Hexagon: a parity-twisted cycle family

A C6 has contribution supports, according to terminal distance 1,2,3,

    {2,6}, {3,5}, {4}.

On any simple r-cycle, take opposite terminals at r-1 visits and a distance-two turn at one visit. The *entire* expanded cycle family is

    {4r-1,4r+1}.

Both lengths are odd. Therefore neither is a power of two. This is an all-r statement about the selected turn pattern, not a claim that all cycles in a larger assembly receive that pattern.

### 3.2 Heptagon: an odd-divisor cycle family

For C7, terminal distance two gives internal paths of lengths 2 and 5, hence contributions

    {3,6}.

Using this turn at every visit yields exactly

    {3r,3r+3,...,6r}.

Every length is divisible by three, so every power of two is absent, for any r. The cell itself only contains its internal 7-cycle and is safe. It still has five unused terminals per visited cell.

### 3.3 A narrow interval, not a gapped spectrum

Define G11 as C11 on vertices 0,...,10 plus chords 0–2 and 5–7. Its seven terminals are

    {1,3,4,6,8,9,10}.

Its internal cycle polynomial is

    2x^3 + x^9 + 2x^10 + x^11,

so it is internally power-free. The terminal pair (3,8) has exact internal path support {4,5,6}, or contributions {5,6,7}.

Repeating that turn on a dyadic r-cycle produces the complete interval

    [5r,7r],

which lies strictly between the consecutive powers 4r and 8r.

This corrects an overly narrow design intuition: an interface need not have holes in its individual path support. A sufficiently narrow, appropriately positioned interval can escape inheritance too. What matters is the composed support around a cycle, together with the feasibility of completing all other terminals.

## 4. Frozen-necklace completion: explicit impossibility certificates

For each escape mechanism, a protected ring was assembled. All internal and ring-traversing cycles are power-free before adding any completion edges:

* **H56:** eight C7 cells, ring entering local terminal 0 and leaving terminal 2.
* **X60:** ten C6 cells, entering terminal 0 and leaving 3, except cell 0 leaves 2.
* **G88:** eight G11 cells, entering terminal 3 and leaving 8.

Each has 40 residual degree-two terminals. To obtain a cubic graph solely by adding edges among these terminals, **20 new edges forming a perfect matching are required**. Existing edges and vertices remain fixed. These conclusions do not exclude rewiring the backbone, using new cells or vertices, or pursuing a noncubic higher-degree completion.

| Backbone | Vertices | Individually admissible new edges | Certified maximum coexisting edges | Required |
|---|---:|---:|---:|---:|
| H56 | 56 | 40 | at most 2 | 20 |
| X60 | 60 | 289 | at most 19 | 20 |
| G88 | 88 | 56 | at most 8 | 20 |

### Certificate format and proof

First list every possible new edge between residual terminals. Every discarded edge is accompanied by an explicit simple forbidden cycle in the backbone plus that edge.

The remaining candidates form vertices of a conflict graph. Two candidate edges conflict if they share a terminal, or if adding them together creates a forbidden cycle. Cycle-based conflicts again carry explicit witnesses.

A valid cubic completion must be an independent set of the conflict graph. For H56, the certificate checks that **every triple of candidates contains a conflicting pair**, proving the bound two. For X60 and G88, explicit covers by **19 and 8 conflict cliques**, respectively, bound every independent set by those numbers.

The verifier checks the actual distinct-vertex cycle witnesses and graph adjacency, not an optimizer's feasibility or optimality status. It also checks that excluded and retained candidates cover the entire possible-edge set. Even if the retained set were an overapproximation of individually admissible edges, these upper-bound proofs would remain sound.

The certificates are:

* `completions/hep56_certificate.json`
* `completions/hex60_certificate.json`
* `completions/gap88_oracle_certificate.json`

A solver separately reported a stronger bound for one experiment, but that report is not used here. The stated numbers are the directly checkable certificate bounds.

## 5. An exact joint-routing oracle

For five-, six-, and seven-terminal cells, a simple full-graph cycle can visit a cell more than once. Counting only one terminal-to-terminal path per cell is therefore unsound.

`interface_oracle.py` handles the three necklace templates above without enumerating long paths in the full expanded graph:

1. Fix one or more proposed added links which the cycle must use.
2. Enforce even boundary degree at every cell. On a ring, these binary equations have exactly two solutions for which original ring edges are used.
3. At each cell, enumerate pairings of the active terminals. Four used terminals require two internally vertex-disjoint paths; six require three.
4. Cache the exact feasible internal routing states and total lengths, computed from the explicit cell graph.
5. Combine external links and internal pairings and require **one connected circuit**, not a disconnected collection of cycles.
6. Convolve the internal length supports and construct an actual expanded witness when a forbidden power is present.

Because all selected internal paths are mutually vertex-disjoint within their cells, and the pairing graph is one circuit, the resulting witness is a simple full-graph cycle. Conversely every full-graph cycle using the specified links induces one of the enumerated states.

With no added links, the oracle returns only ring-traversing cycles; cell-internal cycles are checked separately. With a nonempty added-link set, it returns cycles using **all** those links. For a two-link compatibility test, a cycle using only one link has already been covered by the individual-link tests.

The retained routing catalogue includes all **306** pairing states for C6 and C7:

| Cell | One-path states (feasible) | Two-path states (feasible) | Three-path states (feasible) |
|---|---:|---:|---:|
| C6 | 15 (15) | 45 (30) | 15 (2) |
| C7 | 21 (21) | 105 (70) | 105 (14) |

The G11 oracle computes the analogous states as needed directly from that graph.

### Cross-checks

The exact oracle agrees with an independent full-graph C++ checker on the retained H56 and X60 individual-link and pairwise-compatibility data. Their pairwise scopes contain 780 and 41,616 candidate pairs, respectively, with shared-terminal pairs handled immediately as cubic-degree conflicts. It then completes all G88 individual and pairwise tests without a path-search budget.

A further **24 full-spectrum checks** compare the oracle against `networkx.simple_cycles` on expanded three-cell necklaces with one or two new links. All agree. These are regression checks of the implementation; the decomposition argument above establishes its intended exact semantics.

A preliminary capped full-graph DFS had left 64 G88 single-link queries unresolved. Those timeouts were not treated as impossibility results. The exact oracle resolved the space and found 56 admissible links before proving the eight-edge compatibility bound.

## 6. Mixed-cell synthesis beyond the old odd-necklace rule

The prior uniform theta-cell argument prohibited an odd double-link necklace through a local alternating-state requirement. Mixed cells do not satisfy that premise automatically. To avoid applying a uniform reduction outside its scope, both experiments below retain individually transmitting cells as well.

### Double-link triangle

Use all **71 five-terminal cells** in the explicit catalogue. At each of three cells, expose one terminal, send two terminals to each neighbour, and consider both matchings across each double link.

First exclude any local pair of linked cells that already contains a forbidden cycle. This yields 2,130 labelled local states, 875 spectral state classes, and 54 compatible spectral triangle types (with cyclic-order symmetry reduced as in the enumeration source). The mixed compatibility structure is not bipartite: the old uniform alternating-state obstruction no longer applies.

Every resulting full candidate is then constructed and tested. All **4,064** candidates fail:

    4,040 have a supplied C8 witness;
       24 have a supplied C16 witness.

### Triple-link triangle

Use the **11 catalogue seven-terminal cells with at most 11 vertices**. This is not asserted to be the complete set of all seven-terminal graphs of those orders. Expose one terminal at each of three cells, use three links to each neighbour, and test all locally compatible terminal permutations.

All **43,583** full candidates fail:

    43,461 have a supplied C8 witness;
       122 have a supplied C16 witness.

The total is **47,647** full assemblies: 47,501 with C8 witnesses and 146 with C16 witnesses. These counts can include graph-isomorphic labelled outcomes. They refer to the explicit catalogues and gluing motifs, not to all graphs at the resulting orders.

Both motifs were attempts to synthesize new safe *three-terminal* cells from richer interfaces. Every vertex except the three exposed terminals would have degree three. No new internally power-free cell survived.

`double_triangle_ledger.json` and `triple_triangle_ledger.json` retain the cell states, port matchings, and actual forbidden-cycle witnesses. `verify_results.py` rebuilds each graph and checks its witness. The enumerators are also included so the stated enumeration scopes, rather than only the rejected witnesses, can be reproduced.

## 7. What has and has not been established

Established:

* finite certificates for unbounded uniform dyadic transmission in 466 cells;
* a separate, variable-factor transmission proof for the pentagon;
* 86 concrete failures of automatic four-cycle inheritance;
* three explicit local escape mechanisms with algebraic proofs;
* solver-independent exclusions of three frozen-backbone cubic completions;
* an exact repeated-visit interface oracle with independent cross-checks;
* rejection witnesses for all candidates in two precisely specified mixed-cell synthesis motifs.

Not established:

* an Erdős–Gyárfás counterexample;
* impossibility of all assemblies using any of the 86 locally escaping cells;
* a complete classification of power-free interfaces;
* a universal exclusion of arbitrary cell mixtures or arbitrary quotients;
* impossibility of changing the frozen backbones or using larger joint-routing architectures.

These experiments did not jointly optimize **cell types, terminal assignments, and quotient wiring** over unrestricted assemblies. The oracle supplies exact cycle-conflict witnesses, and the certificates show why pairwise path spectra alone are insufficient: repeated cell visits require multi-path routing states, and a local escape is not a degree-complete graph.

The resulting interface representation and rejection certificates establish the scoped results above, not the existence of a counterexample in an untested family.
