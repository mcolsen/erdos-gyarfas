# Theta(2,3,3): joint routing and fourfold dilation

**Scope/status:** Uniform-assembly reduction and scoped unsuccessful experiment. Do not confuse with the theta(2,3,4) phase cell.

**Retained source:** [eg_gap64_research_note.md](../provenance/eg_gap64_research_note.md).

**Executable evidence:** [experiments/02-gap64](../experiments/02-gap64/). Internal code/data paths in the extracted research text below are relative to that experiment directory. The section text is preserved from the source note; later corrections and superseding claims are indexed in [CORRECTIONS.md](../CORRECTIONS.md).

---

## 5. Genuine gaps: a five-terminal theta cell

Let Q consist of three internally disjoint branch-to-branch paths of lengths
2,3,3. Label its branch vertices5,6 and its terminals0–4, with edges

```
5-0  0-1  1-6  5-2  2-3  3-6  5-4  4-6.
```

Its only internal cycles are two C5s and one C6. Its ten terminal pairs have
four support types:

```
A = {1,4,5}        pairs01,23
B = {2,4,5}        pairs02,13
C = {2,3,5,6}      pairs04,14,24,34
D = {3,4,6}        pairs03,12.
```

These are genuine gaps, not just increased distance. For example an A-pair
has paths of lengths1,4,5 but no paths of length2 or3.

A five-edge interface permits a simple global cycle to cross a cell four
times. Correct evaluation must retain two mutually vertex-disjoint internal
paths, including their pairing of the four used terminals. The supplied
routing certificate enumerates all15 four-terminal pairing states, not just
the ten single-path polynomials. One state, `(0,3),(1,2)`, is impossible.
This is why a three-terminal simple-quotient formula cannot be used unchanged.

### An odd-necklace obstruction

If two Q cells are connected by two edges, all cycles crossing those two
edges have lengths2+S+T for their chosen terminal-pair supports. The only
support-type pairings avoiding both4 and8 are A-D and D-A.

Within one Q, partitioning four terminals into two disjoint pairs of types
A or D can only give A-A or D-D, never A-D. Therefore cells in a double-edge
necklace must alternate these two states. An odd necklace is impossible.
This elementary parity certificate covers every odd length, not just a
bounded search. Independently, all120^3=1,728,000 labelled port assignments
on the three-cell double-edge triangle were checked, with zero C4/C8-free
survivors.

### A stronger surprise: the gaps permit universal fourfold cycle dilation

For every r>=3 and every sequence of r turn types chosen from A,B,C,D,
there are path lengths summing to **3r**. Adding the r intercell edges gives
a simple cycle of length **4r** above any simple r-cycle in a loopless quotient.

Here is a constructive proof. Types C,D contain3. Every pair of A/B turns
can be assigned lengths summing6; every triple can be assigned lengths
summing9:

```
AA: 1+5     AB: 1+5     BB: 2+4
AAA: 1+4+4  AAB: 1+4+4  ABB: 1+4+4  BBB: 2+2+5.
```

Thus two or more A/B turns can be grouped into pairs and, when necessary,
one triple. If there is only one A, balance it with a C using4+2, or with
two Ds using1+4+4. If there is only one B, use a D with2+4, or two Cs with
5+2+2. The remaining turns use3. Those cases exhaust all r>=3.

The balancing verifier checks the construction on all87,360 ordered A/B/C/D
sequences of lengths3–8 as a regression test. The finite case argument above,
not that bounded test, proves all lengths.

**Consequently a uniform Q assembly on a simple5-regular quotient cannot
produce a counterexample unless its smaller quotient is already a
counterexample.** Any dyadic quotient cycle becomes another dyadic cycle,
scaled by4. Individual path gaps are not enough: they can disappear under
sums around a whole cycle.

The conclusion extends to full assemblies allowing port connections within
a cell or parallel links, provided the final graph is simple and C4/C8-free.
An internal port edge can only be of type B; it changes Q to a three-terminal
seven-vertex cell E with all terminal paths2–6. No second internal edge is
safe. E participates in the balancing proof because it contains both the C
and D supports. A double link incident to E always produces C8. Three
parallel links between Q cells always produce C4 or C8, since their three
terminal pairs cannot all be A/D pairs (A union D forms a4-cycle). Thus each
E cell has three distinct neighbours and each remaining five-terminal Q
cell has at least three distinct neighbours. The simple underlying quotient
has minimum degree>=3, and its dyadic cycles again lift to dyadic cycles.
This is a reduction, not a proof that the conjecture holds for every possible
quotient.

### A separately checked unsuccessful experiment

I assembled Q cells on the42-vertex incidence graph of the projective plane
over F4, obtaining294-vertex cubic graphs. The core has1,120 C6s and7,560 C8s.
The30 distinct local terminal configurations were searched using exact
projected C16 counts. Projections relevant to C16 are simple because the
quotient has girth6 and the projected walk length is at most8<12.

A bounded10-second search evaluated1,043,146 proposals and improved C16 from
291 to122, but did not reach0. A full-graph, gadget-independent cycle counter
verified the saved graph has C4=C8=0 and exactly122 C16s. This is not an
optimality or impossibility result. The stronger dilation theorem, discovered
while analysing this experiment, explains why its quotient's C8s make this
uniform family unsuitable as a shortcut to a full counterexample.
