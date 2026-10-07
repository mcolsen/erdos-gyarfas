# Joint interface synthesis, exact heptagon phases, and guarded identification

## Outcome and scope

This continuation found **no Erdős–Gyárfás counterexample and no improved complete near-miss**. Every retained synthesis run is **UNKNOWN** or **UNKNOWN_SOLVER**, not an impossibility certificate. What it produced is a working joint-choice/joint-wiring search with independently verified learned constraints, two sharper interface theorems, a complete resolution of the previous catalogue's remaining unclassified entry, and a proof that removes the bridge exception from one earlier negative result.

The new mathematical results are:

1. An exact classification of the safe turn-count profiles on every dyadic quotient cycle expanded by heptagon cells.
2. A variable-factor transmission proof for the eleven-vertex catalogue cell `cell0095`. The specified 554-cell catalogue now has 468 certified uniform transmitters and 86 explicit local escape witnesses, with no unclassified entry under this dichotomy.
3. A collision-guarded cycle-learning rule for vertex identification, where ordinary monotone cycle-blocking would be unsound.
4. An extension of the all-T7/T15 obstruction to **every connected simple cubic core**, including cores with bridges.

The search results are deliberately kept separate from those theorems. We checked 13,486 learned joint-routing schemas, and 67,272 guarded rejection witnesses from 6,087 degree-complete identification candidates. These validate the specified rules and rejected assignments, not the exhaustion of any synthesis domain. Counts across different runs need not represent distinct isomorphism classes, or even different labelled graphs.

## 1. Definitions and source record

The input is the explicit catalogue in `data/catalog.json`, from the preceding research bundle. It contains 554 connected simple graphs with degrees two or three; degree-two vertices are terminals, and every internal simple cycle avoids powers of two. It is a constructed catalogue, **not all cells up to an order bound**. `data/screen.json` retains the preceding finite classification evidence. This run independently re-enumerated each graph's internal cycles and every terminal pair's simple-path length set.

A terminal-to-terminal path with L internal edges contributes L+1 when used on a cycle of the quotient: one external linking edge is assigned to each visited cell. Write T for a contribution support. For a simple quotient cycle passing through distinct cells, its possible expanded lengths are the sumset of its turn supports. These paths always produce actual simple cycles because the cells are disjoint. When a full cycle revisits a cell, one must instead retain several mutually vertex-disjoint paths in that cell. The joint learner below does so.

Uniform transmission is a **reduction**: a simple quotient's dyadic cycle yields a dyadic cycle in its uniform expansion. It does not prove the conjecture for arbitrary quotients; it does not automatically exclude mixed-cell assemblies, loops, or parallel quotient links.

## 2. Exact heptagon turn profiles at every dyadic scale

For a C7 cell, terminal separations one, two, and three give contribution supports

    A = {2,7},   B = {3,6},   C = {4,5}.

Let r=2^k, k>=2, be a simple quotient-cycle length, and let a,b,c count its A,B,C turns. Thus a+b+c=r. Its complete expanded spectrum is

    2a+3b+4c + {5x+3y+z : 0<=x<=a, 0<=y<=b, 0<=z<=c}.

All lengths lie between 2r and 7r, so the only possible dyadic lengths are 2r and 4r. The former occurs exactly for the all-A pattern. The latter occurs exactly when

    5x+3y+z = 2a+b                                      (H)

has a solution in the stated bounds.

### Theorem

The expanded family is power-free exactly for the following three profiles:

| Exponent k | Safe (a,b,c) profiles |
|---|---|
| k even | (0,r,0), (r-1,1,0), (r-2,0,2) |
| k odd | (0,r,0), (r-2,2,0), (r-1,0,1) |

The order of the turns is irrelevant for this one-cycle calculation. It is a necessary-and-sufficient statement for these selected simple-quotient-cycle families, not a sufficient condition for a complete assembly to be a counterexample. Additional cycles, including repeated cell visits, still matter.

For example, at r=8 the safe profiles are (0,8,0), (6,2,0), and (7,0,1). At r=16 they are (0,16,0), (15,1,0), and (14,0,2).

### Proof of completeness

Set D=2a+b and M=5a+3b+c. We solve (H) by cases. An interval of at least five consecutive integers remains an interval after adding the choices {0,5}; an interval of at least three remains an interval after adding {0,3}. This supplies the simple induction steps below.

* If c>=4, start with [0,c], add all a choices {0,5}, then all b choices {0,3}. The entire interval [0,M] is present, so D is present.
* If c=3 and b>=1, the choices for y,z first fill [0,3b+3], after which the five-steps fill [0,M]. If b=0, the attained residues modulo five are 0,1,2,3. The target 2r-6 has excluded residue four only when r is divisible by five, impossible for a power of two. The selected quotient and remainder respect the bounds.
* If c=2 and b>=1, the choices for y,z fill [0,3b+2], of width at least six; adding five-steps fills [0,M]. If b=0, the attained residues are 0,1,2 modulo five. The target 2r-4 fails precisely for r congruent to plus or minus one modulo five, equivalently even k. This is (r-2,0,2).
* Suppose c=1. If a=0, D=b=r-1 is zero or one modulo three; choose z that residue and y=(b-z)/3. If b=0, the allowed residues are zero and one modulo five, so D=2r-2 fails exactly for odd k. If a>=1,b=1, the allowed residues are 0,1,3,4 modulo five; D=2r-3 misses only when r is divisible by five. If a>=1,b>=2, the sumset contains [3,M-3]. The base (a,b)=(1,2) contains every integer 3 through 9; additional three- or five-steps preserve the claimed interval. D lies inside it.
* Finally suppose c=0. If a=0, the all-B contributions are multiples of three and neither 2r nor 4r is available. If b=0, all-A has the forbidden 2r. If a=1, choose x=0 when r is two modulo three, or x=1 when r is one modulo three; the resulting y is in [0,b]. For a>=2,b=1, the available residues modulo five are 0,3; D=2r-1 fails exactly for even k. For a>=2,b=2, the available residues are 0,3,1; D=2r-2 fails exactly for odd k. For a>=2,b=3, the residues are 0,3,1,4; D=2r-3 would fail only if five divided r. Finally, for a>=2,b>=4 the sumset contains [8,M-8]. The base (2,4) contains all integers 8 through 14, and adding three- or five-steps proves the interval by induction. D lies inside it.

For the residue arguments, r=2^k is plus or minus one modulo five exactly when k is even, and plus or minus two exactly when k is odd. Nonnegative bounded solutions in the listed small cases follow directly from the quotient/remainder choices; the r=4 cases are included. These cases exhaust all nonnegative a,b,c. QED.

`certificates/heptagon_profiles.json` records all 11,304 turn-count profiles for r=4,8,16,32,64,128. Discovery uses polynomial-support bitsets; verification uses an independent bounded-Diophantine test. The finite check is a regression of the proof, **not its extension to untested r**.

## 3. Resolution of the remaining catalogue cell: U11

This cell differs from the earlier G11 having chords 0-2 and 5-7. Here

    U11 = C11 + {0-2, 4-9},

with vertices 0,...,10 and terminals (1,3,5,6,7,8,10). It is catalogue `cell0095`.

Its inclusion-minimal contribution supports, in the certificate's index order, are

    0: {2,6,10,11}
    1: {3,5,9,10}       = B
    2: {3,7,8,9,10}
    3: {4,5,8}          = D
    4: {4,6,7,10,11}
    5: {4,8,9}
    6: {5,7,8,9,10}
    7: {6,7,8,9}.

Every actual turn support contains at least one of these minimal supports. There are 330 multisets of four minimal supports. Exactly one fails to realize a total of 32:

    B,D,D,D.

For every other multiset, an explicit choice summing to 32 is retained.

### Variable-factor transmission theorem

For every r divisible by four, and every sequence of r turns in U11, the expanded spectrum contains either 4r or 8r. Consequently every dyadic quotient cycle transmits a dyadic cycle.

**Proof.** Partition the selected minimal supports into blocks of four. Call a block bad only if it is BDDD. Two bad blocks can be repartitioned into BBDD and DDDD, both good. A bad block together with any partner block other than DDDD can also be repartitioned into two good blocks. `u11_variable_dilation.json` supplies and verifies all 329 such finite repartition identities.

Repeated repairs therefore remove every bad block unless the entire sequence has one B and r-1 Ds. In the nonexceptional case, choose contribution 32 from each good block, totaling 8r. In the exceptional case, choose 3 from B, 5 from one D, and 4 from each other D, totaling

    3 + 5 + 4(r-2) = 4r.

Enlarging a chosen minimal support to the original actual support cannot remove these paths. QED.

The exception is real, not merely a gap in the method: BDDD...D cannot make 8r. The low B choices are too small, whereas B=9 or 10 requires deficits one or two from the maximum-eight D choices. D permits only deficits zero, three, or four.

Together with the previous pentagon theorem, this leaves **468 uniformly transmitting catalogue cells and 86 with explicit power-free four-turn witnesses**. All prior cell graphs/path sets and four-turn certificates were rechecked in this investigation. This classification concerns the supplied 554 objects only; it is not a classification of all possible interfaces.

## 4. Joint cell-choice and wiring search

`src/joint_search.py` selects an internally safe cell for each slot, and a matching on all its terminals except the specified exposed terminals. There is **no frozen ring or fixed quotient**. Links within one cell are permitted when they preserve simplicity and internal power-freeness; parallel links between different cells are permitted. Cell options and connections are chosen in one constraint system.

The retained strong-learning trials used the 11 catalogue cells with seven terminals and at most 11 vertices. All 11 remain eligible, including uniformly transmitting cells: a uniform reduction is not a justified reason to discard a cell from mixed assemblies.

The targets were three or five seven-port slots with one exposed terminal (potential one-deficiency counterexample seeds), and three slots with three exposed terminals (new-cell synthesis). A power-free graph with just one degree-two vertex and all others cubic would suffice for a counterexample after identifying that vertex with its copy in a second graph. No such graph was found.

### Exact learning from a forbidden cycle

A full-graph witness is decomposed into the external links it uses and a set of internal terminal-pair routes for each cell. Multiple visits produce two or three paths; their vertices must be mutually disjoint. The learner enumerates those exact disjoint-routing supports for **every alternative cell type**, not only the type that produced the witness.

If E is the set of required external matching variables and Safe_Q is the condition that the whole routing circuit avoids every power of two, the learned rule is

    (OR over e in E of NOT e) OR Safe_Q(cell choices).

Safe_Q is compiled as a reduced multi-valued decision diagram. Its state is the set of possible cumulative lengths, so it retains the complete composed support rather than a single path-length choice. A diagram may collapse to false: then no allowed cell choices repair the offending wiring, and the learned rule is a topology-only nogood. Slot injections transfer a rule to every placement in identical-option slots.

These rules are sound because independently chosen disjoint routes, joined by the required external links into one circuit, yield an actual simple cycle. Adding other matching links cannot remove it. The independent verifier reconstructs each routing truth table from explicit cell graphs, checks that the pairing structure is one connected circuit, and checks the original full-graph witness.

### A concrete universally bad topology

Number ports by position in each cell's sorted terminal list, from zero. On three seven-port cells, the links

    (0,6)--(2,2),  (2,3)--(1,4),  (1,1)--(0,5)

are forbidden regardless of which of the 11 allowed cell types is used in each slot. The required internal turns are (5,6), (1,4), and (2,3).

All 11^3 = 1,331 expanded three-cell subgraphs were independently reconstructed. The retained certificates provide a C8 for 270 assignments and a C16 for 1,061 assignments. These are witness selections, not counts of all cycles. This is a checkable quantified rule over cell choices, not a claim that every triangle of cells is impossible.

### Retained run outcomes

| Run | Slots / exposed terminals | New model assignments | Learned schemas | Topology-only schemas | Verdict |
|---|---|---:|---:|---:|---|
| strong_test | 3 / 3 | 1,194 | 5,971 | 457 | UNKNOWN |
| sym33alpha | 3 / 1 | 251 | 1,474 | 127 | UNKNOWN_SOLVER |
| sym33cell | 3 / 3 | 395 | 2,425 | 149 | UNKNOWN_SOLVER |
| sym55alpha | 5 / 1 | 299 | 1,663 | 256 | UNKNOWN |
| clean33alpha | continuation of sym33alpha | 103 | 885 | 56 | UNKNOWN |
| clean33cell | continuation of sym33cell | 95 | 1,068 | 50 | UNKNOWN |

Across these retained trials: 2,337 model assignments, 13,486 schema records, and 1,095 topology-only schema records. After slot injections, 124,941 instances were asserted. Records can repeat across trials; none of these counts denotes nonisomorphic graphs or a globally deduplicated catalogue of rules.

Every learned schema's complete cell-choice truth table was independently reconstructed. All runs were stopped by an overall budget or an individual solver-call timeout. **None proved the target impossible.**

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

## 6. Extension of the T7/T15 obstruction to cores with bridges

### Theorem

An assembly using only T7 and T15 on **any connected simple cubic core**, with any terminal orientations, contains a power-of-two simple cycle. The core is not required to be bridgeless.

This is a theorem about these explicit templates, not arbitrary seven- or fifteen-vertex graphs, and not arbitrary interfaces or noncubic cores.

### Charges and the bridgeless case

Each turn has a complete interval of contributions [l,u]. A core cycle therefore expands to every length in [L,U]. If this interval avoids all powers of two, it fits in [2^k+1,2^(k+1)-1], hence 2L-U>=3.

Assign each turn charge w=2l-u. For T7 the three charges are (-1,-1,+1), whose sum s is -1. For T15 they are (-7,-7,-3), whose sum is -17.

The following standard consequence of Edmonds's matching-polytope theorem is used: a bridgeless loopless cubic multigraph has a probability distribution on perfect matchings with every edge marginal 1/3. Indeed, x_e=1/3 has vertex sums one, and every odd cut has at least three edges, so it lies in the perfect-matching polytope. Complementary two-factors therefore use each turn with probability 1/3.

In a bridgeless core, the expected charge of a complementary two-factor is (sum_v s_v)/3<0. But if all expanded cycles were power-free, each component cycle would have charge at least three, so every two-factor would have total charge at least three. Contradiction.

### Leaf bridge-component argument

Suppose the core has bridges. Delete them, and choose a leaf component B of the resulting component tree. It cannot be a singleton: a singleton in a cubic core would meet three bridges, not one. Within B exactly one vertex w has degree two; every other vertex has degree three. B is bridgeless.

Suppress w, replacing its two-edge path by one distinguished edge e. The result H is a bridgeless loopless cubic multigraph; parallel edges are allowed. Use the perfect-matching distribution above and lift its complementary two-factors back to B. For every v other than w, each turn is used with probability 1/3. Vertex w is used precisely when e belongs to the two-factor, with probability 2/3. Its one available turn has charge c_w<=1.

If the complete expanded graph were power-free, every cycle of every such lifted two-factor would have charge at least three. Its total charge would therefore be at least three. Taking expectations instead gives

    (sum_{v in B, v!=w} s_v + 2 c_w)/3
       <= (-(|B|-1)+2)/3
        = (3-|B|)/3
        < 3,

a contradiction. QED.

For mixed T3/T7/T15 cores the same argument gives the useful **local necessary condition**

    sum_{v in B, v!=w} s_v + 2 c_w >= 9

for every leaf bridge component, with s=3 for T3. It does not exclude every mixed construction.

### External theorem reference

Jack Edmonds, *Maximum matching and a polyhedron with 0,1-vertices*, Journal of Research of the National Bureau of Standards, Section B 69(1–2), 125–130 (1965), DOI: 10.6028/jres.069b.013. A primary-source restatement of the matching-polytope inequalities is given in the abstract of Guoli Ding, Lei Tan, Wenan Zang, *When Is the Matching Polytope Box-Totally Dual Integral?*, Mathematics of Operations Research 43(1), 64–99, online 2017, DOI: 10.1287/moor.2017.0852. The charge identities and bridge extension above are derived here; no literature novelty claim is made.

## 7. Verification, reproducibility, and audit

Run, with Python and NetworkX:

```sh
python verify.py
python verify_learning.py
```

The first command independently rechecks every catalogue graph and path support, the finite all-orders witnesses, all 11,304 heptagon profiles in the regression, all 1,331 universal-motif full graphs, and all 67,272 guarded identification clauses. The second reconstructs all 13,486 routing-rule truth tables without Z3. These are certificate-verification programs, not search solvers.

The optional C++ full-graph cycle oracle was cross-checked on all 1,252 nonempty graphs in NetworkX's graph atlas, for lengths 3 through 8: 7,512 complete count comparisons. Every returned witness was checked; count-cap and node-timeout semantics were separately exercised. Optional searches require the native Z3 library and compilation of this oracle; see `src/README.md`. The installed library was used through a small ctypes adapter, not an unavailable Python binding.

The bundle does not claim proof-assistant formalization. The unbounded theorems are mathematical arguments, with finite certificates and independent computations checking their concrete ingredients. The search verdicts remain unresolved.

### Discarded attempts and safeguards

Two exploratory resumes were discarded after the solver's diagnostic serialization was found to include internal model-converter commands. Those attempts are **not** included in the run table, witness totals, or bundle. The retained continuations used assertion-only exports; an export/reload regression is supplied. Every retained routing rule was independently validated regardless of solver state.

An earlier exploratory theta-backbone labeling check was corrected before the retained identification trials. The bundle's authoritative seed graphs are explicitly stored in each retained model, and every quotient witness is checked against those exact graphs. Overrestrictive single-pair diagnostics are not included as global exclusions.

Historical run summaries used the poorly named field `best_c16_upper_cap`. It records a capped count of witnesses, not a proven upper bound. The new source renames it; no result stated here relies on those numbers. All absent-cycle claims in code require a completed uncapped negative check, and a timeout is always UNKNOWN.

## 8. What changed

The implemented search chooses pieces and connections in one model, learns constraints valid across many replacement cells, and has a sound noncubic identification option. The heptagon theorem provides exact phase conditions instead of loose local preferences; the U11 theorem resolves a misleading apparent escape; the bridge argument closes the formerly unresolved all-T7/T15 case with bridges.

The remaining 86 local escapes are not degree-complete constructions. No statement here upgrades them to counterexamples or asserts that an unresolved synthesis model is satisfiable. The concrete advance is an implemented global realization problem, with exact routing semantics and independently checked learned rules, rather than an unspecified terminal-completion step.
