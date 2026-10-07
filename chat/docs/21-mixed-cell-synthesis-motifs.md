# Mixed-cell synthesis: 47,647 rejected assemblies

**Scope/status:** Retained rejection witnesses and complete specified motifs; labelled counts need not be nonisomorphic.

**Retained source:** [eg_interface_filters_note.md](../provenance/eg_interface_filters_note.md).

**Executable evidence:** [experiments/04-interface-filters](../experiments/04-interface-filters/). Internal code/data paths in the extracted research text below are relative to that experiment directory. The section text is preserved from the source note; later corrections and superseding claims are indexed in [CORRECTIONS.md](../CORRECTIONS.md).

---

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
