# The 61-vertex near-miss and three-sheeted lift experiments

**Evidence:** explicit early graphs and sources are in [legacy](../legacy/); central copies are in [data/graphs](../data/graphs/). The small graph and total cycle counts were checked again during packaging. Some projection diagnostics and search coverage survive only as chat reports; those are labelled below.

## The retained one-deficiency graph

The graph `n061_one_deficiency_c16_8.edge` has 61 vertices, 91 edges, one degree-two vertex and 60 degree-three vertices. Its exact retained counts are

`C4=0, C8=0, C16=8, C32=176980`.

It is not an alpha-block, since it contains C16, and not a counterexample, since it also lacks minimum degree three. It provided the base for odd lifts. The original graph6 bytes are preserved at `legacy/b0_runs/continue12/s403.g6`.

The chat reported that the eight C16s had minimum edge hitting number three, with some edges covering five. Repair searches were described as exhausting 3,148 simple reconnections of disjoint three-edge hitting sets, 2,654,803 reconnections of four-edge hitting matchings, and 1,173,318 five-edge hit matchings under incremental pruning, with no C4/C8/C16-free result. Those complete search ledgers are **not retained** here. They should be cited as historical reports, not newly reproducible exhaustive certificates. The same qualification applies to the claimed 123,000-plus sampled coordinated moves and bounded depth-two escape tests.

Adjacent removed edges were explicitly not covered by those matching-based scopes. The graph-level difficulty was not merely hitting old C16s: repairing the resulting deficits introduced new forbidden cycles.

## Three-fold cyclic lift

Give oriented base edges voltages in Z/3Z. A base cycle of nonzero voltage becomes a cycle three times as long, so a C16 can become a safe C48. This alone does not certify the lift: a simple lifted cycle can project to a nonsimple base closed walk.

The regular lift has 183 vertices and three degree-two root fibres. Three completions were retained:

| Completion | Order | Degree structure | C4/C8/C16 | Exact C32 |
|---|---:|---|---|---:|
| One hub joined to all root fibres | 184 | Cubic | Absent | 492,309 |
| Triangle added among the root fibres | 183 | 180 degree-three, three degree-four vertices | Absent | 819,153 |
| All root fibres identified | 181 | 180 degree-three, one degree-six vertex | Absent | 831,828 |

The uncapped 183-vertex lift has C32 count 296,418 and three remaining degree-two vertices. These graphs and all counts in the table were directly rechecked during packaging.

## Corrected decomposition of the original C32 count

The first response's projection analysis was wrong. The later corrected report is:

| Component | C32 |
|---|---:|
| Base simple C32s with zero voltage | 49,360 base cycles |
| Their three lifted copies | 148,080 |
| Lifted C32s with nonsimple base projections | 148,338 |
| Additional C32s using the hub | 195,891 |
| Total in the hub graph | 492,309 |

Thus `148080+148338=296418` and adding the hub contribution gives 492,309. The old values 163,821 zero-voltage cycles, 491,463 inherited cycles and 846 other cycles are **withdrawn**. The claim that about 99.8% of the obstruction was described by simple-base-cycle linear forms is also withdrawn; the corrected simple-projection component is about 30.1%.

Packaging rechecked total C32 counts on the base, uncapped lift and hub graph. It did not rerun a complete projection-by-projection classification, so the detailed 49,360/148,338 split remains the corrected historical diagnostic, not a new packaging verification.

## Voltage-space formulations and their limits

A spanning tree fixes the gauge; cycle rank `91-61+1=31` leaves 31 independent ternary variables. A simple base cycle gives a linear voltage form over F3. Optimizing nonzero values of these forms is meaningful, but **does not capture nonsimple projections or cap-crossing cycles**.

The missing constraints concern the monodromy of full projected walks, not only simple base cycles. An S3 permutation lift permits more than cyclic translations. For a dyadic base cycle, identity monodromy preserves its length, a transposition leaves a fixed sheet and a two-sheet orbit, while a 3-cycle produces a safe threefold length. This observation is not sufficient for all lifted cycles.

Historical probes reported 455 one-coordinate and 102,375 two-coordinate S3 mutations, with 282 short-hole-preserving two-coordinate assignments in 32 graph-isomorphism classes; none improved the chosen seed's raw C32 count. A Z3^2 probe at 552 vertices reportedly reached nine residual C16s. The raw exhaustive mutation ledger and 552-vertex checkpoint are not retained, and neither report excludes larger changes or other bases.

## Audit caution

The initial claim of a 64-vertex cubic graph with seven C16s was explicitly withdrawn as stale-state/mislabeling; a clean reconstruction of that surgery family had a best count of 117. It must not appear in an extremal-results table.

The lift results demonstrate a useful initial short-hole mechanism, not a theorem that odd lifts solve all subsequent powers. Later exact cell contraction provided a representation with stronger simplicity guarantees; see [note 05](05-exact-gadget-compression.md).
