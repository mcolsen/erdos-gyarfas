# Certified limits on three frozen-backbone completions

**Scope/status:** Fixed perfect-matching completion domains only; witness-derived independent-set upper bounds.

**Retained source:** [eg_interface_filters_note.md](../provenance/eg_interface_filters_note.md).

**Executable evidence:** [experiments/04-interface-filters](../experiments/04-interface-filters/). Internal code/data paths in the extracted research text below are relative to that experiment directory. The section text is preserved from the source note; later corrections and superseding claims are indexed in [CORRECTIONS.md](../CORRECTIONS.md).

---

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
