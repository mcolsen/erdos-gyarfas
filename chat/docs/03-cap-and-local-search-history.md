# Cap design, symmetry breaking, and local-basin history

**Evidence status:** this is a curated historical record of the early chat. Explicit retained or reconstructible graphs are distinguished from lost checkpoints. Neighborhood-exhaustion, saddle-classification, and random-sampling numbers without retained ledgers remain historical reports. The later packaged construction records are stronger evidence.

## Cap geometry and breaking lift symmetry

Replacing the three-fibre hub by a triangle of **three new vertices**, each linked to one deficient fibre, yields a cubic graph on 186 vertices. This differs from adding triangle edges directly among the fibres, which makes a noncubic 183-vertex graph.

The retained cubic triangle-cap graph has 476,415 C32s, versus 492,309 for the hub. Degree-preserving two-switches `ab,cd -> ac,bd`, with exact C4/C8/C16 rejection gates, reached a retained 186-vertex graph with 279,630 C32s. Both counts were checked again during packaging.

The historical intermediate trajectory was

`476415 -> 431149 -> 369956 -> 304358 -> 287836 -> 279630`.

The 279,630 graph's reported short spectrum is C3=55, C5=21, C6=42, C7=21, no cycle of lengths 8–16, and C17=4. Its reported C64 witness is not retained as a standalone witness here. Direct short-power and C32 counts, cubicity and connectivity are newly recorded in the packaging checks.

## Order-eight caps and the lost 224,547 checkpoint

Cap cells obtained by deleting a vertex of an eight-vertex cubic graph give seven new vertices, hence an order-190 assembly. The cap's source order must not be confused with the number of added vertices.

| Cap source / assembly | Final order | Reported raw C32 | Best reported descent | Artifact status |
|---|---:|---:|---:|---|
| Three-new-vertex triangle cap | 186 | 476,415 | 264,624 | Raw and earlier 279,630 graph retained; 264,624 checkpoint absent |
| First order-eight cap class | 190 | 436,211 | Approximately 282,000 | Raw value in retained cap summary; graph for this class absent |
| Second order-eight cap class | 190 | 446,643 | 224,547 | Raw graph retained; 224,547 edge list lost |
| Order-sixteen cap experiment | 198 | 370,616 | 248,305 | Chat report only for the graphs |

The 446,643 raw graph is retained at `data/graphs/n190_c32_446643.edge`. Its continued descent checkpoint at 303,008 is also retained and has been directly recounted.

The lost 224,547 graph was reported cubic, 3-vertex-connected, with C3=56, C5=22, C6=44, C7=22, no cycles 8–16 and C17=12. The chat described a full 78,828-proposal two-switch scan with 1,389 short-hole survivors, 234 neutral but isomorphic proposals, and no improving move. It also described 37 nonisomorphic escape classes below a +15,000 barrier, approximately 1,600 legal three-edge rewires, 100,000 four-edge proposals with 11 survivors, and 100,000 five-edge proposals with none. **The missing graph and those local-neighborhood ledgers prevent treating this as an independently retained certificate.**

A container restart was reported to have erased the scratch checkpoint. Later better retained graphs do not retroactively reconstruct its exact edges or certify those historical neighborhood claims.

## What is retained from the cap census

`legacy/work2/caps8_summary.tsv` gives 24 labelled successful attachments: 12 with score 436,211 and 12 with 446,643. One 446,643 representative is retained. Other absolute paths inside that TSV are historical paths, not promises that those files exist in this package.

The chat also reported no acceptable attachment among 6,120 order-12-cap attachments or 42,756 order-14-cap attachments; random order-16 trials produced 14 survivors with score 370,616, while one million samples at each of cap-source orders 18, 20 and 22 found none. Those later census ledgers are absent. The full order-16 domain of `4060*16*6=389760` attachments was **not exhausted** in this chat.

The raw score did not reliably predict the final basin. This motivated testing multiple cap classes and permitting bounded uphill moves rather than retaining only the smallest initial count.

## Recovery to retained 219,531

A different randomized descent on the 446,643 seed reportedly followed

`446643 -> 260633 -> 255451 -> 245273 -> 243501 -> 242090 -> 239158 -> 237098 -> 237010 -> 234331 -> 231549`.

A +2,505 saddle move then led through

`234054 -> 229251 -> 223337 -> 220225 -> 219610 -> 219565 -> 219538 -> 219531`.

The 219,531 graph is recoverable exactly from the retained per-edge incidence TSV, which lists all 285 edges. The package includes that reconstruction and a new direct C32 count. Intermediate trajectory values are historical unless their explicit graphs are separately retained.

The chat reported a complete local scan at 219,531 with 78,828 proposals, 1,914 short-hole survivors and no improvement. Its positive saddle scores began `7,353,411,716,1762,2451,3248,3462`. The +353 and +411 cases returned to the same floor. A proposed 196-probe saddle grid completed 98 probes; **the other 98 are incomplete**, and no full saddle-radius conclusion follows.

## Edge concentration motivated coordinated moves

For the 219,531 graph the mean C32 incidence per edge is `32*219531/285`, approximately 24,649. The retained table identifies these heavy edges:

| Edge | C32 incidence |
|---|---:|
| 83–100 | 68,454 |
| 88–148 | 66,955 |
| 16–78 | 57,163 |
| 82–91 | 55,046 |
| 149–175 | 52,580 |
| 48–101 | 48,623 |
| 64–142 | 48,403 |
| 56–139 | 48,288 |

The next round exploited that concentration with joint multi-edge surgery; see [note 04](04-targeted-multiedge-search.md). Incidence is not additive cycle coverage: several busy edges may lie on largely the same cycles.

## Limits of this line of work

No local minimum is a global minimum. No count reduction proves proximity to zero. At order 190 a counterexample must avoid 4,8,16,32,64,128, so minimizing C32 alone is not a complete objective. The later contraction of the graph into small cells explained much of the apparent local rigidity and enabled broader, faster moves.
