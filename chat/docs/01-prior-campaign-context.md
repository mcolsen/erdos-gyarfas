# Prior campaign: starting point and constraints

**Evidence status:** background transcribed from the repository README and reports retrieved earlier in the chat. These are Maria Olsen's existing campaign results, not new results of the continuation. The earlier repository's original files and complete computations were not re-fetched or rerun during packaging. The [parent README](../../README.md), [campaign report](../../REPORT.md), and [other-approaches report](../../REPORT-other-approaches.md) document those results and their artifacts.

## Reported starting bounds

| Class or claim | Reported outcome | Reported method/scope |
|---|---|---|
| General minimum degree three | Any counterexample has at least 36 vertices | Assumption-free SAT-modulo-symmetries through 32; sound minimum-order structural chaining at 33–35 |
| Cubic | At least 50 vertices | Even-order SAT ladder through 48, with monolith and cube-partition completion at 48 |
| Bipartite minimum degree three | At least 57 vertices | Two-colour SAT encoding through 56 |
| Independent pure enumeration | No counterexample through 21 | `geng` plus exact pruning; two complete single-modulus partitions at 21 |
| Predominantly cubic minimal counterexample | At least two thirds of vertices cubic | Strengthening of consequences reported in Carr's paper |
| C4-free degree cap | `Delta <= floor((n-1)/2)` for `delta>=3` | Elementary structural argument; no minimality assumption |
| Cubic graph avoiding C4/C8/C16 | Minimum order lies in [50,82] | SAT lower bound and explicit upper-bound specimens |
| Alpha-block ladder | No alpha-block of order at most 32 | A superset encoding allowing at most one degree-two vertex; higher interrupted runs undecided |

The reported prior independent enumeration replicated Markström's C4/C8-free cubic counts: 4 at order 24, 23 at order 26, and 251 at order 28. All relevant small survivors had C16. Cross-checks between disjoint `geng` and SAT stacks included counts 2590, 5, 1315, 0, and 88 on explicitly described controls in the upstream report. These are background validation reports, not new controls rerun here.

## Structured and stochastic lanes already explored

The report lists 240 generalized Petersen graphs, 1,148 I-graphs, 80,780 circulants, and 176,348 initial cyclic lifts through order 64 with no C4/C8/C16-free survivor. Later group-lift sweeps were substantially larger and had their own stated base/group/order restrictions; they must not be interpreted as all possible lifts.

The corrected arc-transitive sweep covered 3,815 cubic graphs through order 10,000. Its 689 C4/C8/C16-free survivors all had C32, C64, and C128. The vertex-transitive sweep covered 111,360 graphs through order 1,280, with 100 short-hole survivors, all containing C32 and C64. Useful examples were C2030.1, C1458.10, and C1458.11. The record distinguished simple-cycle holes from nonbacktracking-walk holes; C2030.1 had the former at 16 without the latter.

The annealing campaign repeatedly reached residual C16 counts around 13–25 at small cubic orders and did not reach zero there. At orders 82–126, C4/C8/C16-free examples became accessible, but carried very many C32s. These observations motivated changing representations rather than simply extending brute-force enumeration.

Later upstream regular-lift searches included small multigraph bases, abelian and selected nonabelian groups, and cyclic bases through order 12 in stated windows below 128. The reports describe tens of billions of voltage assignments but do not establish that every algebraic family at every order is excluded.

## Alpha-block reduction and the Mersenne viewpoint

An alpha-block is a 2-connected graph with at most one degree-two vertex, every other vertex of degree at least three, and no power-of-two cycle. A counterexample has an alpha-block as a leaf block. Conversely, an alpha-block with a degree-two vertex yields a counterexample by identifying that vertex in two copies; all cycles remain inside one copy and the identified vertex has degree four. An alpha-block with no degree-two vertex is already a counterexample.

Suppressing the exceptional degree-two vertex gives a minimum-degree-three multigraph with one distinguished edge. All power-of-two cycles must use that edge, while no cycle through it may have length `2^k-1`; subdivision shifts those Mersenne lengths to forbidden powers. This motivated the 61-vertex one-deficiency search in the continuation.

The upstream report also used low-circumference targets to make large forbidden lengths vacuous. Its interrupted capped and higher alpha-block runs supply no additional absence verdict. A weighted subdivision of K4 with weights `(1,3,2,3,2,3)` had cycle spectrum `{6,7,9,10}` but several deficient vertices; repairing those vertices remained the central difficulty.

## Nonbacktracking trace barrier

The reported cubic trace-hole bound is

`n >= (2^(L/2)+1)^2 / (2^(L/2+1)-1)`

when the length-L cyclically nonbacktracking trace vanishes. It places the L=32 threshold above 32,769 vertices and the L=64 threshold at roughly 2.15 billion. The original report described the single-length formulation as potentially novel, without establishing priority. The continuation later deliberately built simple-cycle holes with nonzero forbidden-length walk traces, outside this stronger condition.

## Corrections inherited from the upstream record

The report corrected an incorrect census-coverage label: the 796-graph file did not represent all arc-transitive cubic graphs through 2,048 vertices. It also corrected an unsafe assumption about refining `geng` residue/modulus work partitions: changing the modulus can change the splitting level, so cross-modulus unions do not automatically partition the work. The eventual order-21 claims rested on complete single-modulus runs.

Statements such as “only algebra can work” or “every reachable algebraic habitat is closed” were research assessments, not general impossibility theorems. The continuation itself found useful nonlinear/gadget constructions, so those assessments must not be used as early rejection rules.
