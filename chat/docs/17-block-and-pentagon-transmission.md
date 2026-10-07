# Four-turn transmission certificates and the pentagon exception

**Scope/status:** Historical count: 467 transmitters, 86 escapes, one unknown. Note 23 resolves that unknown, giving 468/86/0.

**Retained source:** [eg_interface_filters_note.md](../provenance/eg_interface_filters_note.md).

**Executable evidence:** [experiments/04-interface-filters](../experiments/04-interface-filters/). Internal code/data paths in the extracted research text below are relative to that experiment directory. The section text is preserved from the source note; later corrections and superseding claims are indexed in [CORRECTIONS.md](../CORRECTIONS.md).

---

## 2. An unbounded reduction from a finite four-turn check

### Four-turn lemma

Let a cell have contribution supports T_1,...,T_s. Suppose there is a dyadic integer d>=2 such that, for every four choices of turn supports,

    4d belongs to T_i + T_j + T_k + T_l.

Then every simple quotient cycle of dyadic length r>=4 in a uniform assembly yields a full-graph cycle of dyadic length dr.

**Proof.** Partition the r visits into consecutive groups of four. In each group, choose internal paths with total contribution 4d. Different visits use different cells, so these choices do not interfere. Their concatenation is a simple cycle of length (r/4)4d=dr. ∎

This is a finite certificate for *all* dyadic r; it is not extrapolation from testing short cycles. Sumset addition is commutative, so four-turn multisets suffice. Inclusion-minimal supports suffice too: any larger support contains the choices guaranteed by a smaller one.

The screen tests d=2,4,8,16,32. **466 of 554 cells have a certificate.** For **86**, it also finds a four-turn sumset containing *no* power of two at all. Those cells demonstrably escape automatic single-traversal inheritance on an appropriately oriented quotient C4.

Two cells have neither result: the pentagon `cell0001` and the eleven-vertex cell `cell0095`. The next lemma resolves the pentagon. The other remains unclassified, not certified promising.

### Why “no common dilation factor” is too weak: the pentagon

A pentagon has contribution supports

    A={2,5}, B={3,4}.

Let a dyadic r>=4 cycle use b B-turns and a=r-b A-turns.

If b=0, choose contribution 2 everywhere, yielding a cycle of length 2r.

If b>=1, choose x A-turns at value 5 instead of 2, and y B-turns at value 4 instead of 3. The length is

    2r + b + 3x + y.

It suffices to solve

    3x+y=2r-b, 0<=x<=r-b, 0<=y<=b.

For b>=2, the integer intervals [3x,3x+b], as x ranges from 0 to r-b, cover every integer from 0 to 3r-2b. The target 2r-b lies in this range. For b=1, dyadic r is nonzero modulo three, so 2r-1 is 0 or 1 modulo three. Choose y to be that residue and x=(2r-1-y)/3; the bounds hold for r>=4. Thus the desired cycle of length 4r exists.

**Every dyadic quotient cycle therefore survives, but the factor can depend on its turns.** All-A turns cannot realize 4r because 3x=2r has no solution; all-B turns cannot realize 2r because their minimum is 3r. This explains why searching only for a single common factor misses a real obstruction.

Together, the four-turn certificates and pentagon lemma give uniform-simple-quotient reductions for **467 catalogue cells**. They do not justify discarding those cells from arbitrary mixed-cell searches. The mixed experiments below deliberately keep them.
