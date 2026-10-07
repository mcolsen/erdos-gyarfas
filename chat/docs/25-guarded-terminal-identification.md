# Noncubic candidates and collision-guarded identification

**Scope/status:** 6,087 degree-complete rejected candidates; 67,272 guarded witness clauses; no exhausted synthesis domain.

**Retained source:** [eg_joint_research_note.md](../provenance/eg_joint_research_note.md).

**Executable evidence:** [experiments/05-joint-synthesis](../experiments/05-joint-synthesis/). Internal code/data paths in the extracted research text below are relative to that experiment directory. The section text is preserved from the source note; later corrections and superseding claims are indexed in [CORRECTIONS.md](../CORRECTIONS.md).

---

## 5. Noncubic search by vertex identification

Degree-two terminals need not be repaired by adding edges. Pairing terminals and identifying each pair can produce vertices of degree four, opening constructions outside the cubic matching search. Duplicate edges are collapsed in the resulting simple quotient, so exact minimum-degree constraints are necessary.

We tested this on three previously protected boundary graphs:

| Seed | Original order | Identified pairs | Resulting order | Models checked | Rejection witnesses | Verdict |
|---|---:|---:|---:|---:|---:|---|
| Eight heptagons H56 | 56 | 20 | 36 | 2,986 | 26,378 | UNKNOWN |
| Ten hexagons X60 | 60 | 20 | 40 | 2,366 | 29,276 | UNKNOWN |
| Eight theta(2,3,4) cells R64 | 64 | 16 | 48 | 735 | 11,618 | UNKNOWN_SOLVER |

Every proposed quotient is checked to be simple, connected, and of minimum degree at least three. The candidate class is thus degree-complete, not a collection of unresolved terminals. Every retained model had a C4 or C8. There were no successful constructions and no exhaustive nonexistence results.

### Why ordinary cycle blocking is wrong here

Additional identifications may merge two different vertices of a forbidden cycle and destroy its simplicity. Therefore a clause forbidding every later completion containing the currently required identifications is generally unsound.

Lift each edge of a quotient-cycle witness back to a chosen original seed edge. At a cycle vertex, the preceding edge's end and the following edge's start must either already be the same seed vertex, or require an identification. Let R be the set of required identification variables.

Let D contain every permitted identification that would merge an original vertex used at one cycle occurrence with an original vertex used at a different occurrence. The sound clause is

    (OR over e in R of NOT e) OR (OR over f in D of f).       (G)

If all required identifications persist and no cross-occurrence collision occurs, the same cycle stays simple. Therefore any counterexample satisfying those required identifications must activate at least one collision. This proves (G). Matching classes have size at most two; there are no indirect identification chains hidden from D.

The verifier independently reconstructs all 6,087 quotient candidates and checks every one of the 67,272 witness cycles, required sets, collision sets, and clauses. The largest witness clause contains 104 collision literals. An unguarded version would be shorter but would not be sound.

### Minimum-degree encoding

No adjacent terminal pair is identified: its merged vertex would have at most two distinct neighbours. Each original degree-three vertex forbids pairing any two of its neighbours. For a candidate merged pair (u,v), let K=N(u) union N(v). If |K|<3, disallow the pair. If |K|=3, conditionally forbid every further pairing inside K. If |K|=4, conditionally forbid each two-pair partition of K. These conditions precisely prevent reduction below three distinct neighbour classes under a perfect matching of terminals. They allow shared original neighbours whenever the final quotient still has sufficient degree; no overly strong individual-identification test is substituted.
