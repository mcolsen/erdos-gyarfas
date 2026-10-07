# An exact repeated-visit interface oracle

**Scope/status:** Exact disjoint-routing and single-circuit semantics for the stated necklace templates.

**Retained source:** [eg_interface_filters_note.md](../provenance/eg_interface_filters_note.md).

**Executable evidence:** [experiments/04-interface-filters](../experiments/04-interface-filters/). Internal code/data paths in the extracted research text below are relative to that experiment directory. The section text is preserved from the source note; later corrections and superseding claims are indexed in [CORRECTIONS.md](../CORRECTIONS.md).

---

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
