# A Moore-type bound for point-holes in the non-backtracking walk spectrum

*Found while validating `algebraic-program.md`; this obstruction re-scopes that
program. Status: proof below; independently verified (see §5); empirics match.*

## Statement

Let G be a connected cubic (multi)graph on n vertices and H its Hashimoto
(non-backtracking, dart-transfer) matrix, of size 3n. Write s = 2^{L/2}.

**Theorem (trace-hole Moore bound).** If L ≥ 2 is even and tr(H^L) = 0, then

    n ≥ (s+1)² / (2s−1),   i.e.   n ≥ 2^{L/2−1} + O(1).

With n even (cubic) this gives concretely:

| L | bound on n |
|---|---|
| 8 | ≥ 10 |
| 16 | ≥ 130 |
| 32 | ≥ 32,770 |
| 64 | ≥ 2,147,483,650 (> 2^31) |

If G is bipartite the bound doubles (both ±3 are eigenvalues):
**n ≥ 2(s+1)²/(2s−1)** ≈ 2^{L/2}; even-rounded: L=8: 20, L=16: 260,
L=32: 65,540, L=64: 4,294,967,300.

**Why it matters here.** tr(H^L) counts cyclically-non-backtracking closed
L-walks, so tr(H^L) = 0 implies G has no cycle of length d for ANY d | L
(traverse a C_d L/d times: a cyclically-NBW closed L-walk). The
voltage-lift program of `algebraic-program.md` certifies C_L-freeness of a
lift exactly through tr(H_lift^L) = 0 (identity-voltage NBW count on the base
= tr(H_lift^L)/|Γ|). Hence:

- walk-certification at L = 64 is impossible below n ≈ 2.1×10⁹ — the proposed
  sweep (lifts of order ≤ 10⁵) can never pass its last rung;
- walk-certification at L = 32 requires n ≥ 32,770 — above the entire
  Potočnik–Spiga–Verret census (≤ 1280) and at the very top of the proposed
  group-order range;
- the walk route is only ~8× cheaper in vertices than brute girth: girth > L
  costs n ≥ ~4·2^{L/2} (even-girth Moore bound 2(2^{g/2}−1) at g = L+2), a
  single-length walk-hole costs n ≥ ~2^{L/2}/2. Point-holes in the WALK
  spectrum are nearly as expensive as killing all short cycles at once.
  (Point-holes in the CYCLE spectrum can be far cheaper — C2030.1 has a
  C16-hole at girth 7 with tr(H^16) = 194,880 > 0 — but those are exactly the
  holes the walk criterion cannot certify.)

## Proof

Ihara–Bass (cubic case): det(I − uH) = (1−u²)^{m−n} · det(I − uA + 2u²I),
m = 3n/2. Hence the 3n eigenvalues of H are: +1 and −1, each with
multiplicity m − n = n/2, together with the two roots μ±(λ) of

    x² − λx + 2 = 0,   one pair for each eigenvalue λ of A.

So for even L:

    tr(H^L) = n + Σ_{λ ∈ spec A} p_L(λ),     p_L(λ) := μ+(λ)^L + μ−(λ)^L.

Classify contributions (even L throughout; note μ+μ− = 2):

1. λ = 3 (Perron; present once, G connected): μ = 2, 1 ⟹ p_L(3) = 2^L + 1.
2. λ = −3 (iff bipartite): p_L(−3) = (−2)^L + (−1)^L = 2^L + 1.
3. 8 < λ² < 9: both roots real, same sign, product 2 ⟹ both nonzero; at even
   L both powers positive, and by AM–GM p_L ≥ 2·(μ+μ−)^{L/2} = 2·2^{L/2} > 0.
4. λ² = 8: double root ±√2: p_L = 2·2^{L/2} > 0.
5. λ² < 8 (tempered): μ± = √2·e^{±iθ} with 2√2·cosθ = λ ⟹
   p_L(λ) = 2·2^{L/2}·cos(Lθ) ≥ −2·2^{L/2}.

Thus, with at most n−1 eigenvalues contributing the worst case −2·2^{L/2} = −2s
(s = 2^{L/2}; 2·2^{L/2} = 2s):

    0 = tr(H^L) ≥ n + (2^L + 1) − (n−1)·2s = n + s² + 1 − (n−1)·2s.

Rearranged: n(2s − 1) ≥ s² + 2s + 1, i.e. n ≥ (s+1)²/(2s−1). ∎

(Disconnected G: tr is additive and each component is bounded separately, so
connectivity is no loss. d-regular: identical argument with q = d−1 replacing
2 gives n ≥ (q^{L/2}+1)²/((q−1)·… — cubic is the case we need; the general
statement is n·(d−2)/… omitted here.)

Equality pressure: to approach the bound EVERY non-Perron eigenvalue must be
tempered with cos(Lθ) = −1, i.e. λ = 2√2·cos(kπ/L) with k odd — a rigid
algebraic spectrum. Real graphs will sit above the bound; the empirical
question is how far (the current L=16 record is n=630, a factor 4.8 above
the even-rounded lower bound 130).

## Consequences

1. **The L=64 rung of the proposed sweep is unreachable.** No object of order
   < 2^31 passes; "kill early on L=4,8,…,64" terminates empty with certainty.
2. **A girth sandwich.** For girth ≥ 9, every cyclically-NBW closed 16-walk is
   a C16 traversal (a non-cycle cyclically-NBW closed walk has length ≥ 2g
   exactly — split at a repeated vertex into two internally-NB closed walks,
   each ≥ g; realized by the doubled girth cycle; figure-eights need degree 4):
   tr(H^16) = 32·#C16 (2L rootings per cycle). So a cubic graph with girth ≥ 9 and n ≤ 128 CONTAINS a
   C16 — e.g. all (3,9)-cages (n=58), (3,10)-cages (70), (3,11)-cages (112),
   and the (3,12)-cage (126) necessarily contain 16-cycles. More relevantly:
   **any C16-free cubic graph has girth ≤ 8 or ≥ 130 vertices.**
3. **The certification ladder is an extremal question per L.** Smallest cubic
   graph with tr(H^L) = 0: L=8 = 28 exactly (21 minimum witnesses);
   L=16 ∈ [130, 630] (a census graph realizes 630); L=32 ∈ [32770, ?] (no
   example known); L=64: ≥ 2^31, out of reach.
4. **What the walk criterion cannot see.** C2030.1-style holes (girth ≤ 8,
   cycle-freeness at L with walk count > 0) are invisible to trace conditions
   and require exact cycle checks — for these, only small lifts (n ≤ ~126,
   exhaustively checkable) or census objects are searchable.

## Empirics (this campaign's data)

- A full {C4,C8}-free cubic census through n=28 establishes the L=8 minimum
  as 28 exactly, with 21 witnesses. The PSV census supplies an n=630
  trace-16 hole, improving the realization previously supplied by C1458.10/11.
- C1458.10/11 (girth 12): tr(H^16) = 0 — realize the L=16 hole at n = 1458,
  11.2× the bound. tr(H^32) = 8,590,955,904 / 8,596,274,688 ≈ 2·(2^32+1):
  exactly the doubled-Perron floor of the bipartite bound — the graphs sit
  essentially ON the spectral floor at L=32, and still cannot reach 0 below
  n ≈ 65k (bipartite) — vivid confirmation.
- C2030.1 (girth 7, non-bipartite): tr(H^4) = tr(H^8) = 0 (walk-certified
  holes at 4 and 8 at n = 2030), tr(H^16) = 194,880 = 96n > 0 — a cycle-only
  hole at 16.
- geng sweep n ≤ 20 (all connected cubic graphs): no tr(H^16) = 0 (bound
  says impossible below 130) — see `results/` log.
