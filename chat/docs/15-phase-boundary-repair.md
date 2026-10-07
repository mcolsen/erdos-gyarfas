# Edge, hub and cap exclusions for the phase boundary graphs

**Scope/status:** Fixed-seed completion exclusions with path witnesses. Not exclusions of arbitrary rewiring or networks of new vertices.

**Retained source:** [eg_interface_phase_research_note.md](../provenance/eg_interface_phase_research_note.md).

**Executable evidence:** [experiments/03-phase-interfaces](../experiments/03-phase-interfaces/). Internal code/data paths in the extracted research text below are relative to that experiment directory. The section text is preserved from the source note; later corrections and superseding claims are indexed in [CORRECTIONS.md](../CORRECTIONS.md).

---

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
