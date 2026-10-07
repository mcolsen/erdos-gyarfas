# Parity certificates for the two 34-vertex cores

**Scope/status:** Excludes specified cores only, with the T3/T7/T15 templates and arbitrary orientations.

**Retained source:** [eg_gadget_research_note.md](../provenance/eg_gadget_research_note.md).

**Executable evidence:** [experiments/01-gadget-compression](../experiments/01-gadget-compression/). Internal code/data paths in the extracted research text below are relative to that experiment directory. The section text is preserved from the source note; later corrections and superseding claims are indexed in [CORRECTIONS.md](../CORRECTIONS.md).

---

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
