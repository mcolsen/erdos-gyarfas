# Joint cell-choice and wiring synthesis

**Scope/status:** Working search and verified learned rules; every retained search verdict is UNKNOWN or UNKNOWN_SOLVER.

**Retained source:** [eg_joint_research_note.md](../provenance/eg_joint_research_note.md).

**Executable evidence:** [experiments/05-joint-synthesis](../experiments/05-joint-synthesis/). Internal code/data paths in the extracted research text below are relative to that experiment directory. The section text is preserved from the source note; later corrections and superseding claims are indexed in [CORRECTIONS.md](../CORRECTIONS.md).

---

## 4. Joint cell-choice and wiring search

`src/joint_search.py` selects an internally safe cell for each slot, and a matching on all its terminals except the specified exposed terminals. There is **no frozen ring or fixed quotient**. Links within one cell are permitted when they preserve simplicity and internal power-freeness; parallel links between different cells are permitted. Cell options and connections are chosen in one constraint system.

The retained strong-learning trials used the 11 catalogue cells with seven terminals and at most 11 vertices. All 11 remain eligible, including uniformly transmitting cells: a uniform reduction is not a justified reason to discard a cell from mixed assemblies.

The targets were three or five seven-port slots with one exposed terminal (potential one-deficiency counterexample seeds), and three slots with three exposed terminals (new-cell synthesis). A power-free graph with just one degree-two vertex and all others cubic would suffice for a counterexample after identifying that vertex with its copy in a second graph. No such graph was found.

### Exact learning from a forbidden cycle

A full-graph witness is decomposed into the external links it uses and a set of internal terminal-pair routes for each cell. Multiple visits produce two or three paths; their vertices must be mutually disjoint. The learner enumerates those exact disjoint-routing supports for **every alternative cell type**, not only the type that produced the witness.

If E is the set of required external matching variables and Safe_Q is the condition that the whole routing circuit avoids every power of two, the learned rule is

    (OR over e in E of NOT e) OR Safe_Q(cell choices).

Safe_Q is compiled as a reduced multi-valued decision diagram. Its state is the set of possible cumulative lengths, so it retains the complete composed support rather than a single path-length choice. A diagram may collapse to false: then no allowed cell choices repair the offending wiring, and the learned rule is a topology-only nogood. Slot injections transfer a rule to every placement in identical-option slots.

These rules are sound because independently chosen disjoint routes, joined by the required external links into one circuit, yield an actual simple cycle. Adding other matching links cannot remove it. The independent verifier reconstructs each routing truth table from explicit cell graphs, checks that the pairing structure is one connected circuit, and checks the original full-graph witness.

### A concrete universally bad topology

Number ports by position in each cell's sorted terminal list, from zero. On three seven-port cells, the links

    (0,6)--(2,2),  (2,3)--(1,4),  (1,1)--(0,5)

are forbidden regardless of which of the 11 allowed cell types is used in each slot. The required internal turns are (5,6), (1,4), and (2,3).

All 11^3 = 1,331 expanded three-cell subgraphs were independently reconstructed. The retained certificates provide a C8 for 270 assignments and a C16 for 1,061 assignments. These are witness selections, not counts of all cycles. This is a checkable quantified rule over cell choices, not a claim that every triangle of cells is impossible.

### Retained run outcomes

| Run | Slots / exposed terminals | New model assignments | Learned schemas | Topology-only schemas | Verdict |
|---|---|---:|---:|---:|---|
| strong_test | 3 / 3 | 1,194 | 5,971 | 457 | UNKNOWN |
| sym33alpha | 3 / 1 | 251 | 1,474 | 127 | UNKNOWN_SOLVER |
| sym33cell | 3 / 3 | 395 | 2,425 | 149 | UNKNOWN_SOLVER |
| sym55alpha | 5 / 1 | 299 | 1,663 | 256 | UNKNOWN |
| clean33alpha | continuation of sym33alpha | 103 | 885 | 56 | UNKNOWN |
| clean33cell | continuation of sym33cell | 95 | 1,068 | 50 | UNKNOWN |

Across these retained trials: 2,337 model assignments, 13,486 schema records, and 1,095 topology-only schema records. After slot injections, 124,941 instances were asserted. Records can repeat across trials; none of these counts denotes nonisomorphic graphs or a globally deduplicated catalogue of rules.

Every learned schema's complete cell-choice truth table was independently reconstructed. All runs were stopped by an overall budget or an individual solver-call timeout. **None proved the target impossible.**
