# Closure of the safe triangle-composition grammar

**Scope/status:** Complete finite grammar calculation plus induction; not a classification of arbitrary cells.

**Retained source:** [eg_gap64_research_note.md](../provenance/eg_gap64_research_note.md).

**Executable evidence:** [experiments/02-gap64](../experiments/02-gap64/). Internal code/data paths in the extracted research text below are relative to that experiment directory. The section text is preserved from the source note; later corrections and superseding claims are indexed in [CORRECTIONS.md](../CORRECTIONS.md).

---

## 4. Safe triangle recursion closes after15 vertices

Start with a singleton T1 having three external half-edges. An operation
takes three three-terminal cells, joins them around a triangle, using two
ports in each child, and leaves its third port exposed. Retain only results
whose internal cycles avoid every power of two.

If the children are power-free, the only additional cycles traverse the
three children. Their lengths are3 plus the sum of one terminal-path length
from each child. For children drawn from T1,T3,T7,T15, their supports are
intervals. Exhausting the20 unordered child multisets and27 exposed-port
choices gives540 finite cases. The only safe results are

```
(1,1,1) -> T3
(1,3,3) -> T7
(1,7,7) -> T15, with both T7 exposed ports distinguished.
```

The retained finite table includes a particular forbidden cycle length for
every rejected case. Swapping the two joined ports does not change the
path-length sum. In the surviving cases those swaps are also absorbed by
child automorphisms, so they introduce no new terminal-isomorphism type.
Induction proves closure of this entire grammar. A nominal31-vertex next
cell, for example, would contain a forbidden16-cycle.

This is not a classification of arbitrary power-free three-terminal graphs.
It rules out obtaining new cells solely by this specific recursive operation.
