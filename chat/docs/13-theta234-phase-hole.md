# Theta(2,3,4): an exact-one phase hole at every dyadic scale

**Scope/status:** Exact selected-cycle theorem and power-free boundary graphs. Those graphs still have degree-two vertices.

**Retained source:** [eg_interface_phase_research_note.md](../provenance/eg_interface_phase_research_note.md).

**Executable evidence:** [experiments/03-phase-interfaces](../experiments/03-phase-interfaces/). Internal code/data paths in the extracted research text below are relative to that experiment directory. The section text is preserved from the source note; later corrections and superseding claims are indexed in [CORRECTIONS.md](../CORRECTIONS.md).

---

## 3. An explicit all-scale phase hole

### 3.1 Cell definition

Let H be the theta graph whose branch-to-branch paths have lengths 2, 3, and 4. Its vertices are 0 through 7 and its edges are

    0-2  0-3  0-5  1-2  1-4  1-7  3-4  5-6  6-7.

Vertices 0 and 1 have degree three. The six terminals are 2,3,4,5,6,7. Its three internal cycles have lengths 5,6,7, one of each.

Use these two terminal-pair passages:

* A: from terminal 5 to terminal 7;
* B: from terminal 2 to terminal 6.

Their internal path polynomials are

    P_A(x) = x^2 + x^4 + x^5,
    P_B(x) = 2x^3 + 2x^6.

Including one external edge, the contribution polynomials are

    Q_A(x) = x^3(1+x^2+x^3),
    Q_B(x) = 2x^4(1+x^3).

All of these multiplicities were independently checked by direct simple-path enumeration.

### 3.2 Exactly one exceptional turn is necessary and sufficient

Let a quotient cycle have dyadic length r >= 4. Suppose a of its cells use passage A and the other r-a use B. Its expanded-cycle polynomial is

    F_(r,a)(x) = 2^(r-a) x^(4r-a)
                 (1+x^2+x^3)^a (1+x^3)^(r-a).

Its support lies between 4r-a and 7r-a. Since 0 <= a <= r,

    2r < 4r-a <= 4r <= 7r-a < 8r.

Thus the only possible power of two in that support interval is 4r. Its coefficient is positive exactly when the residual polynomial contains exponent a.

If a=0, that is the positive constant coefficient. If a=1, it is absent: the residual factors have no way to contribute an increment of one. If a>=2, write a=2p+3q with p,q nonnegative; every integer at least two has such a representation, and p+q<=a. Choosing p factors contributing x^2 and q factors contributing x^3 from the a copies of (1+x^2+x^3) makes the coefficient positive.

Therefore

    the expanded family is power-free  <=>  a = 1.

In particular, with exactly one A passage,

    F_r(x) = 2^(r-1) x^(4r-1)
             (1+x^2+x^3)(1+x^3)^(r-1),

and the coefficient at x^(4r) is zero for every dyadic r >= 4.

This is a genuine internal hole, not a lower bound pushing all cycles beyond a forbidden length. There are cycles on both sides of the missing power. It is also more informative than a congruence restriction on one terminal pair: a single exceptional passage and the other passages must compose in exactly the right way.

The all-orders proof is the elementary argument above. The verifier additionally tests every possible A-count for r=4,8,16,32 as a regression control; those finite tests are not presented as the proof for arbitrary r.

### 3.3 Explicit boundary graphs

Take r copies of H. In each cell designate the two selected terminals as incoming and outgoing and join the outgoing terminal of cell j to the incoming terminal of cell j+1 cyclically. For dyadic r, use one A cell and r-1 B cells. Each cell still has four unused terminals of degree two.

There are only two types of simple cycle: one internal to a cell, or one traversing every cell of the ring. A cycle cannot cross a two-edge cell boundary more than twice. Thus the complete cycle polynomial is

    r(x^5+x^6+x^7) + F_r(x).

The retained examples are:

| r | Vertices | Edges | Degree-two vertices | Degree-three vertices | Total simple cycles | Circumference |
|---|---:|---:|---:|---:|---:|---:|
| 4 | 32 | 40 | 16 | 16 | 204 | 27 |
| 8 | 64 | 80 | 32 | 32 | 49,176 | 55 |

Both graphs contain no power-of-two simple cycle. For r=8, there are 128 cycles of length 31 and 128 of length 33, but zero of length 32. This illustrates the phase hole directly.

A separate five-cell ring using A at every cell has polynomial

    5(x^5+x^6+x^7) + x^15(1+x^2+x^3)^5.

Its external lengths lie in [15,30], whose only candidate power is 16; the increment-one hole excludes it. This 40-vertex boundary graph has 20 vertices of each degree, 258 simple cycles, and circumference 30.

The verifier reconstructs all three edge lists and independently enumerates **every simple cycle** using NetworkX. It agrees with every coefficient of these polynomials. The graphs are biconnected but not cubic and do not satisfy minimum degree three. No comparison with lower bounds for minimum-degree-three counterexamples is claimed.
