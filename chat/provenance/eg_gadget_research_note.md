# Exact gadget compression, a C32-free graph, and a parity obstruction

## Outcome and limits

This investigation produced:

1. A retained **190-vertex cubic graph** with `C4=C8=C16=0` and exactly **178,077 C32s**, improving the supplied 216,246-cycle specimen at the same order.
2. A retained **370-vertex cubic graph** with **no C4, C8, C16, or C32**. More strongly, it has no cycle of any length from **16 through 32**. It has exactly **43 C33s** and contains a verified C64.
3. An exact cycle-polynomial representation of the original 190-vertex graph as a 34-vertex cubic core with small three-terminal cells.
4. A finite **13-cycle parity certificate** proving that the original core cannot yield an Erdős–Gyárfás counterexample under *any* reassignment or terminal orientation of the three cell types studied here. The new 190-vertex core has a separate 15-cycle certificate.

**No graph here is a counterexample.** The 190-vertex graph contains C32; the 370-vertex graph contains C64. No global order-minimality, publication-priority, or novelty claim is made. The negative certificates concern specified cores and a specified cell family, not arbitrary cubic graphs.

## Files and reproduction

- `data/input_216246.edge`: reconstructed starting graph, matching the prior SHA-256 exactly.
- `data/input.core`: its 34-vertex, port-labelled core.
- `data/eg190_178077.edge`, `data/best190.core`: improved fixed-order specimen and its core.
- `data/eg370_no_C32.edge`, `data/model370.json`: the four-power-free graph and complete assembly model.
- `certificates/no_C32.json`: finite core-cycle bounds for the 370-vertex graph.
- `certificates/C64_witness.json`: 64 distinct vertices in cyclic order, plus their core projection and cell paths.
- `certificates/old_core_parity.json`: the 13-cycle contradiction for the old core.
- `certificates/best190_core_parity.json`: the 15-cycle contradiction for the new core.
- `verify.py`: rebuilds and verifies constructions and certificates without an optimization solver.
- `direct_cycle_counter.cpp`: an independent full-graph canonical DFS counter, with no cell assumptions.
- `core_search.c`: exact compressed search over 3- and 7-vertex cells.
- `expand_core.py`: expands a `.core` state into a DIMACS graph, preserving its terminal-slot convention.
- `solve_370.py`: optional integer-program reconstruction of the 30-vertex-core design experiment.
- `parity_screen.py`: a necessary-condition filter for full counterexamples in the 3/7/15-cell family.

Install the Python dependencies, then run:

```sh
python -m pip install -r requirements.txt
python verify.py
c++ -O3 -std=c++17 direct_cycle_counter.cpp -o direct_cycle_counter
./direct_cycle_counter data/eg190_178077.edge 32
./direct_cycle_counter data/eg370_no_C32.edge 32
./direct_cycle_counter data/eg370_no_C32.edge 33
```

Expected final counts: **178077**, **0**, and **43**.

The verifier checks that the C64 witness really is a simple cycle. It also independently enumerates each small cell's internal cycles and terminal paths, reconstructs the 370-vertex graph edge-for-edge, enumerates its short core cycles by canonical DFS, and checks the parity certificates.

The 370-vertex graph and both 190-vertex graphs were separately checked to be simple, cubic, connected, 3-vertex-connected, and 3-edge-connected. Direct full-graph enumeration confirmed the four power-length counts for all three graphs; results are in `logs/independent_direct_counts.log`.

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

## 4. Constructing the 370-vertex graph

The core is explicitly constructed by

`LCF(30, [-13,-9,7,-7,9,13], 5)`.

Its cubicity and girth 8 were checked directly. It has 90 cycles of length 8 and 72 of length 10, and no other cycles of length at most 10.

At each core vertex, choose one of six options: T7 or T15, and one of three distinguished-terminal attachments. For a given core cycle:

- a T7 cell contributes minimum length `3+q_v`, including one inter-cell edge;
- a T15 cell contributes minimum length `4+2q_v`;
- `q_v` is 1 when the cycle avoids the distinguished terminal and 0 otherwise.

An integer program chooses one option per vertex and requires every core cycle of length at most 10 to have minimum expanded length at least 33. It minimizes the number of T15 cells.

The returned solution uses **twenty T15 cells and ten T7 cells**:

`20*15 + 10*7 = 370` vertices.

The solver reported optimality for this fixed-core, two-cell formulation. The independently checked feasibility certificate, not that optimality status, establishes the construction. This is not a claim that 370 is the smallest possible order for a C4/C8/C16/C32-free cubic graph.

### Proof of the full gap 16 through 32

Every cycle is internal to a cell or projects to a simple core cycle.

Internal cycles have lengths in `{3,5,6,7,9,10,11,12,13,14,15}`. Every core cycle of length at most 10 has minimum expansion length at least 33, as checked in the finite certificate. Every longer core cycle has at least 11 cells, each contributing at least three edges, and therefore also has length at least 33.

So no cycle has length 16 through 32. There are also no internal or external C4 or C8.

The graph has exactly 43 C33s, independently checked by direct enumeration. An explicit C64 is saved and verified, so the graph is **not** an Erdős–Gyárfás counterexample.

### Why C64 returns in this particular construction

On an 8-cycle of a T7/T15 core, an all-T7 assignment always allows C32: its minimum is at most 32 and its maximum is 56. Eliminating C32 on such a cycle therefore requires at least one T15. But that raises its maximum to at least 64, while its minimum is at most 48. Since path supports are intervals, it then allows C64.

Thus the C64 in this construction is structural, not an accidental defect that terminal reorientation can remove while retaining this core and these two cell types.

## 5. A coding-theoretic obstruction to the old search family

Consider an arbitrary core cycle with:

- `r` vertices;
- `s` T7 cells and `u` T15 cells;
- `q` nondistinguished-to-nondistinguished traversals of T7 cells;
- `p` such traversals of T15 cells.

Its expanded cycle lengths fill

`[2r+s+2u+q+2p, 3r+4s+12u]`.

For lengths 5 through 8, avoiding *all* powers of two inside that interval forces:

| Core cycle length | Permitted cell counts | Additional requirement |
|---|---|---|
| 5 | five T3, or one T3 plus four T7 | in the second case q>=3 |
| 6 | three T3 plus three T7 | q>=2 |
| 7 | five T3 plus two T7 | q>=1 |
| 8 | seven T3 plus one T7 | none |

No T15 may occur on these cycles in a full counterexample. A core cycle of length 3 or 4 is already impossible in this family.

In every permitted row, the number of T3 cells is **odd**. Write `y_v=1` if core vertex v receives T3 and 0 otherwise. Every short core cycle gives a binary equation

`sum_{v in C} y_v = 1 mod 2`.

This is a parity-check system. The original core has **13 explicit short cycles such that every vertex occurs in an even number of them**. Adding the 13 required equations yields

`0 = 13 = 1 mod 2`,

a contradiction.

The certificate is entirely finite: check the 13 cycles are actual simple cycles of lengths 6–8, count each vertex's appearances, and check every count is even. No optimization solver, external theorem, or numerical tolerance is needed.

Therefore the original 34-vertex core cannot produce a counterexample by **any** reassignment or terminal permutation of T3, T7, and T15. The 178,077-cycle core has an independent 15-cycle certificate proving the same restriction for it.

This does not forbid finding better C32 near-misses on these cores, and does not apply to arbitrary three-terminal gadgets with different path spectra. It is specifically an obstruction to eliminating every power of two within this cell family.

Run the general necessary-condition screen with:

```sh
python parity_screen.py data/input.core --certificate contradiction.json
```

A failure rules out that core for this family. A pass is only a necessary condition and is not evidence of a counterexample.

## 6. Other scoped probes and interpretation

The exploratory all-T7 searches also tried cores on 34, 50, 58, 64, 80, and 100 vertices, using both multiplicity and offending-core-cycle objectives. They improved their respective objectives but did not reach C32=0 during those bounded runs.

An orientation-only formulation on a 70-vertex girth-10 core was reported infeasible by the integer solver. The mixed T7/T15 formulation on the 24-vertex LCF core `[12,7,-7]^8` was likewise reported infeasible. A girth-preserving two-vertex insertion probe from that 24-vertex core produced two labelled insertions in one isomorphism class at order 26; that fixed-core mixed-cell formulation was also reported infeasible. These are narrow solver results, not exclusions of all graphs of those orders.

The experiments showed that huge expanded cycle families can be forbidden at their interfaces. At the same time, interval-valued path spectra make later forbidden powers unavoidable in some constructions. The parity filter certifies that the two tested cores are impossible full-counterexample cores within this cell family, independently of their C32 counts.

The certificates do not exclude different cores passing the necessary cycle-incidence conditions, different cells with genuinely gapped terminal-path spectra, or decompositions with richer interface states. Optimizing the same certified-impossible cores cannot yield a counterexample within this cell family.

## Checksums

```
input_216246.edge
60a04c2d2ccfdc652545f978cdb29e5e15bd085d64e49d97182a3eb68ac6769b

eg190_178077.edge
1083e61a82aa17f96ff1288ffebb5ce691f613c422b88cb14781eeb995978997

eg370_no_C32.edge
75ff07f380e9c5e2f410228254c10d4446a1159aced1612230daee5c572d3859
```
