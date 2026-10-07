# Scope, notation, and evidence conventions

## What this archive is

This is a consolidation of the substantive research reported in Maria Olsen's visible GPT Pro / ChatGPT conversation, together with the graph, code, certificate, and log files that remained available at packaging. It was assembled on **2026-10-06**. Stage identifiers express conversation order, not independently established experiment dates.

The starting point was Maria's earlier campaign, documented in the [parent repository](../../README.md). Those results are background, not discoveries of this continuation. The five later experiment bundles are preserved as independently runnable directories. Earlier experiments have more uneven evidence; the historical reports are not silently promoted to new exhaustive certificates.

**No Erdős–Gyárfás counterexample was produced in this conversation.** The 370- and 26,550-vertex graphs avoid successively longer initial lists of powers, but have explicit C64 and C128 witnesses, respectively. Power-free boundary graphs have degree-two vertices and are not counterexamples.

## Mathematical conventions

All claimed final graphs are finite, simple, undirected graphs. A cycle is a **simple cycle**, not necessarily induced. For these graphs the forbidden powers start at 4, since a simple cycle cannot have length 1 or 2. `C_L` denotes a cycle of length L; `#C_L` counts distinct undirected simple cycles, not rotations or orientations.

A complete candidate requires minimum degree at least three. A cubic graph has degree exactly three everywhere. A cell has designated degree-two vertices called terminals; other vertices usually have degree three. The singleton three-stub template is a separately stated convention. Attaching one external edge at each terminal restores cubicity.

A terminal path may pass through another terminal whose external edge is not used. Path length is the number of **edges**. A contribution support adds one intercell edge per visit. Distinguish internal path polynomials from contribution polynomials: confusing them shifts every cycle length.

With three boundary edges, a noninternal simple cycle uses exactly two and visits the cell once. With larger boundaries, a simple cycle can visit a cell multiple times. Correct interface states must retain mutually vertex-disjoint internal paths and their terminal pairing, and the selected pieces must form **one** circuit.

A graph-cover projection is different from contraction of three-edge cells. A lifted simple cycle can project to a nonsimple closed walk. Such projections may be excluded only by an explicitly proved bound, such as the `<2*girth` argument used in the 26,550-vertex construction.

## Reading the evidence labels

| Label | Meaning |
|---|---|
| Retained artifact | An explicit graph, model, certificate, source, or log is included. |
| Freshly checked at packaging | The indicated program or direct count was actually rerun; see `verification/packaging`. |
| Mathematical argument with finite checks | An unbounded claim is supported by a written proof; tests check ingredients or examples, not every possible graph. No proof-assistant formalization is claimed. |
| Scoped exhaustive result | A stated finite domain was exhausted according to its retained generator/closure argument. Scope and symmetry conventions are part of the claim. |
| Historical report only | A claim appeared in the chat, but sufficient raw output to establish it independently is not retained here. |
| UNKNOWN / UNKNOWN_SOLVER | The run stopped without deciding its domain. Never read this as UNSAT or a nonexistence proof. |
| Superseded / withdrawn | A later correction or stronger scoped result replaces an earlier statement. |

A hash establishes file identity, not mathematical correctness. Checking a witness proves that candidate fails; it does not prove that every candidate in a domain was generated. Checking a finite catalogue proves statements about its listed objects; catalogue completeness needs a separate construction argument. Counts of proposals, labelled graphs, records, and isomorphism classes are not interchangeable.

## Counterexample acceptance checklist

Before claiming a counterexample, independently verify the actual graph's simplicity, connectedness (or select a connected component), minimum degree, and absence of **every** power-of-two cycle not exceeding its order. An exact smaller circumference bound can shorten that list. Neither low counts, an empty bounded search, a capped counter, a solver timeout, nor a local interface escape is sufficient.

The two large-gap constructions are a useful stress test: both have many nonsimple nonbacktracking closed walks of forbidden lengths. The conjecture concerns simple cycles, so vanishing walk traces is stronger than necessary and can exclude useful constructions.

## Attribution and external knowledge

This archive records AI-assisted exploratory mathematics. Maria's prior campaign is attributed separately. Existing external theorems are identified in [REFERENCES.md](../REFERENCES.md). No publication priority, smallest-order record, peer review, or general novelty claim is established by the packaging exercise.
