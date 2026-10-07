# The constructed 554-cell catalogue

**Scope/status:** Specified construction catalogue, not every cell through an order bound.

**Retained source:** [eg_interface_filters_note.md](../provenance/eg_interface_filters_note.md).

**Executable evidence:** [experiments/04-interface-filters](../experiments/04-interface-filters/). Internal code/data paths in the extracted research text below are relative to that experiment directory. The section text is preserved from the source note; later corrections and superseding claims are indexed in [CORRECTIONS.md](../CORRECTIONS.md).

---

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
