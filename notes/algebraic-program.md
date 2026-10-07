# The algebraic program: engineering spectral holes at powers of two

*Archived design notes for the algebraic campaign. Original conjectural
claims and unverified citations are identified below; the validation report
records their adjudication.*

**Historical proposal, superseded.** The program was validated, re-scoped,
and executed; see `algebraic-program-validation.md`. In particular, the
five-length walk-certification sweep is blocked by the trace-Moore bound,
C2030.1's C16 hole is cycle-only rather than trace-certified, Ramanujan
equidistribution points in the wrong direction, and the completed scoped
searches were negative. The original design is retained below as the record
of what was proposed and tested.

## 1. Why algebra is the only door left

The campaign's §4 analysis: a counterexample must avoid C_L for every power of
two L ≤ n, in a regime where a generic cubic graph carries ~2^L/(2L) cycles of
length L. Girth cannot do it (girth > 32 needs ≥ 131,070 vertices by the Moore
bound, and by then C64, C128, ... are in play — the girth route never
terminates). Local search cannot do it (measured floors, §2d/§2f). What CAN
suppress exponentially many cycles at an exact length is a *global algebraic
constraint* — the way bipartiteness suppresses every odd cycle at once, not by
fighting them individually but by making them structurally impossible.

The campaign already met three graphs that do this at short lengths: C2030.1
(girth 7, no C8/C16), C1458.10/11 (girth 12, no C16). Their symmetry groups
enforce holes in the cycle spectrum at lengths where generic graphs would have
16 and ~2,000 cycles respectively. The original hypothesis was that the same
mechanism could scale to 32 and 64.

## 2. The machinery: voltage lifts and twisted non-backtracking spectra

Take a small cubic base multigraph B, a finite group Γ, and a voltage
assignment α: E(B) → Γ (reversed edges get inverse voltages). The derived
graph (lift) B^α has vertex set V(B) × Γ, order n = |V(B)|·|Γ|, and is cubic.

**Key fact.** Every simple cycle of length L in the lift projects to a
*non-backtracking* closed walk of length L in B whose net voltage is the
identity. Hence:

> If B has NO identity-voltage non-backtracking closed walk of length L,
> then B^α has NO cycle of length L.   (Sufficient, not necessary.)

This converts "suppress ten million 32-cycles in a 100-vertex graph" into a
finite condition on a tiny object. And the condition is *computable by linear
algebra*: identity-voltage non-backtracking walk counts decompose over the
irreducible representations ρ of Γ as

    #NBW_triv(L) = (1/|Γ|) Σ_ρ dim(ρ) · tr(H_ρ^L)

where H_ρ is the ρ-twisted Hashimoto (directed-edge transfer) matrix of B — a
(2|E(B)|·dim ρ)-dimensional matrix. For abelian Γ all irreps are 1-dimensional:
checking all five conditions L ∈ {4,8,16,32,64} over all characters costs
|Γ| small-matrix power computations. Groups of order ~10³–10⁴ are trivially
searchable per (B, α).

The search target, stated spectrally: the trivial representation contributes a
*positive* walk count at L; the twisted traces must *exactly cancel* it. This
is Ramanujan-flavored eigenvalue placement — power sums of the twisted spectra
vanishing at five exact indices. By Newton's identities these are algebraic
conditions on the characteristic polynomials of the H_ρ: a finite variety to
land on, not a miracle to pray for.

## 3. The obstruction map (why cheap tricks fail — worth knowing precisely)

- **"Voltage = length" is impossible.** In an undirected lift, voltages are
  inverse-symmetric, so no assignment makes net voltage ≡ walk length (mod m);
  traversal direction flips signs. The one exception is m = 2 (signs don't
  matter mod 2): the bipartite double cover, which forces all cycle lengths
  even. That is the wrong direction — every forbidden length is already even.
  *The conjecture is protected by the parity of its targets: the only free
  length-modulus in graph theory is mod 2, and 2^k is even.*
- **"All lengths ≡ 0 mod 3" is a theorem away from impossible.** Bondy–Vince
  [cited from memory: min degree 3 forces two cycles with lengths differing by ≤ 2]
  prohibits cycle spectra contained in 3ℤ. So no single congruence class can
  carry the whole spectrum; holes must be *surgical*, not residue-classes.
- **"All lengths in one window between powers" dies by circumference.** Cubic
  graphs have circumference ≥ poly(n) [original citation, unverified here:
  ~n^0.69, Bilinski et al.; connectivity caveat in the validation report], so a
  spectrum confined to [2^k+1, 2^{k+1}−1] caps n far below the Moore bound
  that the required girth already demands. Dead both ways.

What survives all three obstructions: a spectrum that is *dense enough* to
satisfy gap theorems, spans many octaves, and has engineered point-holes
exactly at {4, 8, 16, 32, 64}. Nothing above forbids that; nothing known
constructs it. That is the precise frontier.

## 4. Original design and its adjudication

1. **C2030.1 mechanism.** |Aut| = 12180 = 2²·3·5·7·29. The design sought a
   quotient + voltage presentation exhibiting cancellation of the 8- and
   16-walk counts. Validation refuted the 16-walk premise: that hole is
   cycle-only. C1458.10/11 (1458 = 2·3⁶) do have trace-certified 16-holes.
2. **Twisted-Hashimoto checker.** Input (B, Γ, α), output the trivial-voltage
   NBW counts at the five lengths. The validation design compared explicit
   small lifts with independent `checker.py`/`p2check` cycle tests, accounting
   for the difference between walk and cycle counts.
3. **Original sweep scope.** Cubic multigraph bases on ≤ 10 vertices ×
   abelian Γ up to order ~10³, plus dihedral, Z_m⋊Z_k, and small SL(2,p)
   groups, with spanning-tree-normalized voltages and ascending-length
   filters. This five-length walk-certified scope was infeasible by the
   trace-Moore bound; the executed exact-cycle scope is in the validation
   report. The distinction matters: a lift can pass a cycle test even when
   its walk test fails, because closed walk witnesses need not be simple.
4. **Census cross-section.** The full Potočnik–Spiga–Verret cubic
   vertex-transitive census (~111k graphs ≤ 1280 vertices) was checked in the
   executed program. The original motivation used an undercounted Conder
   subset; `census-erratum.md` records the correction.
5. **Mechanism analysis.** The validation report records which lengths
   resisted cancellation and the distinction between walk-certified and
   cycle-only holes.

## 5. Limits of the original intuition

The first-moment heuristic suggested that counterexamples should not exist,
with algebraic rigidity as a possible exception. The expectation of near-misses
at {4,8,16} plus one of {32,64} was conjectural. The executed scoped searches
were negative; neither that outcome nor the heuristic settles the conjecture.
