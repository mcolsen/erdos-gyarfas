# The 370-vertex graph: no C4, C8, C16, or C32

**Scope/status:** Retained complete cubic graph; not a counterexample because it contains C64.

**Retained source:** [eg_gadget_research_note.md](../provenance/eg_gadget_research_note.md).

**Executable evidence:** [experiments/01-gadget-compression](../experiments/01-gadget-compression/). Internal code/data paths in the extracted research text below are relative to that experiment directory. The section text is preserved from the source note; later corrections and superseding claims are indexed in [CORRECTIONS.md](../CORRECTIONS.md).

---

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
