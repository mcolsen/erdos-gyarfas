# Exact three-terminal compression and cycle polynomials

**Scope/status:** Finite templates, exact decomposition proof, and retained count reconstruction.

**Retained source:** [eg_gadget_research_note.md](../provenance/eg_gadget_research_note.md).

**Executable evidence:** [experiments/01-gadget-compression](../experiments/01-gadget-compression/). Internal code/data paths in the extracted research text below are relative to that experiment directory. The section text is preserved from the source note; later corrections and superseding claims are indexed in [CORRECTIONS.md](../CORRECTIONS.md).

---

## 1. What compression discovered

The supplied 190-vertex graph contains 56 vertex-disjoint triangles. Contracting all of them produces a 78-vertex cubic graph, which contains 22 further disjoint triangles. Contracting those produces a **34-vertex cubic core**.

The original graph is exactly an assembly of:

- twelve 3-vertex cells;
- twenty-two 7-vertex cells.

Each cell has exactly three degree-2 terminals; all other cell vertices have degree 3. Joining terminals along the core's edges restores cubicity.

This is exact coarse-graining, not an approximation. A simple cycle crosses any cut an even number of times. Since a cell boundary consists of only three edges, a simple cycle uses either zero or two of them. A cycle that leaves a cell therefore uses a single terminal-to-terminal path in that cell and projects to a simple core cycle. It cannot revisit the cell. Conversely, independently choosing a path through each cell of a simple core cycle gives a simple expanded cycle.

This avoids the repeated-projection issue encountered in regular voltage lifts: a quotient by three-edge cell boundaries has a stronger simplicity property than a covering projection.

## 2. The three cells

All cell definitions are explicit in `gadgets.py`; vertices and terminals are labelled.

### Cell T3

A triangle, with every vertex a terminal. Between any two terminals,

`P3(x) = x + x^2`.

Its internal cycle polynomial is `x^3`.

### Cell T7

The cell has vertices 0 through 6 and edges

```
0-2, 0-5, 1-2, 2-3, 3-1, 4-5, 5-6, 6-4, 3-6.
```

Its terminals are `(0,1,4)`, with terminal 0 distinguished.

Paths involving the distinguished terminal have polynomial

`A7(x) = x^2 + x^3 + x^4 + 2x^5 + x^6`

`       = x^2 (1+x)(1+x^2+x^3)`.

Paths between the other two terminals have polynomial

`B7(x) = x^3 + 3x^4 + 3x^5 + x^6 = x^3(1+x)^3`.

Its internal cycle polynomial is

`2x^3 + x^5 + 2x^6 + x^7`.

### Cell T15

Take two copies of T7, on vertices 1–7 and 8–14, and add vertex 0. Add edges `0-2`, `0-9`, and `5-12`. The terminals are `(0,1,8)`, again with terminal 0 distinguished.

Paths involving the distinguished terminal realize **every** length from 3 through 14. Paths between the other two terminals realize every length from 5 through 14.

The internal cycle polynomial is

`2(2x^3 + x^5 + 2x^6 + x^7) + x^9(1+x)^6`.

Thus no cell contains a cycle of power-of-two length. Full path multiplicities are independently enumerable from the templates; the interval-support property is checked by `verify.py`.

## 3. Exact cycle formula for T3/T7 assemblies

For a core cycle, let:

- `r` be its number of vertices;
- `s` be the number of T7 cells;
- `q` be the number of T7 cells traversed between their two nondistinguished terminals.

The polynomial counting all expanded simple cycles above that core cycle is exactly

`F_C(x) = x^(2r+s+q) (1+x)^(r+2q) (1+x^2+x^3)^(s-q)`.

The first exponent includes the inter-cell edges. Consequently the expanded cycle lengths fill the entire integer interval

`[2r+s+q, 3r+4s]`.

A C32 count is the sum of `[x^32] F_C(x)` over core cycles. Only core cycles of length at most 16 need to be considered, because every visited cell contributes at least two edges.

For the original graph, **209 core cycles** account for all **216,246** expanded C32s. The exact formula reproduces the independently enumerated full-graph count.

### Measured benefit

For this one graph and this runtime:

- ten standalone direct counts took 0.804960812 seconds total;
- ten thousand compressed counts took 0.439359 seconds total.

That is approximately **1,832 times faster per count** in this comparison. The direct timing includes process startup; this is not a universal graph-search speedup. Raw measurements are in `benchmark.json`.

A 10-second compressed run evaluated 1,168,145 proposed moves, with 159,810 exact short-hole survivors, and reached 180,300 C32s. A subsequent run reached 178,077. Both retained improvements were expanded and independently counted.

The search changes core connections, cell locations, and terminal orientations, rather than only rewiring individual edges of the expanded graph. Every accepted state is exactly C4/C8/C16-free. Connectivity was checked on retained outputs, not imposed on every intermediate state.

Build and run, for example:

```sh
cc -O3 -std=c11 -D_POSIX_C_SOURCE=200809L core_search.c -lm -o core_search
./core_search data/input.core candidate.core 10 20260904 4000 0
python expand_core.py candidate.core candidate.edge
./direct_cycle_counter candidate.edge 32
```

Arguments after the seed are temperature, objective mode, and optional maximum proposal count. Mode 0 counts actual expanded C32s; mode 1 counts offending core cycles; mode 2 weights their interval penetration. Timed runs do not guarantee identical stopping points on different computers. The retained `.core` files are complete reproducible witnesses regardless of search timing.
