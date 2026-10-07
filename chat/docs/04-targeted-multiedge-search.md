# Targeted multi-edge surgery: 219,531 to 216,246

**Evidence status:** the three successful surgeries are exactly reconstructible from retained edge data, and all four graph counts were checked again during packaging. The large enumeration totals below were recorded in the chat, but the complete task ledgers/search implementation for every scope were not retained. Do not treat their sum as a newly reproduced exhaustive certificate or a count of unique graphs.

## The successful move

From the 219,531-C32 graph, remove

`29–32, 44–141, 48–101, 126–174`

and add

`29–44, 32–126, 48–174, 101–141`.

This produces **216,687 C32s**. Then:

| Step | Removed | Added | Resulting C32 |
|---|---|---|---:|
| Two-switch 1 | 65–143, 170–183 | 65–170, 143–183 | 216,367 |
| Two-switch 2 | 19–85, 34–182 | 19–34, 85–182 | **216,246** |

All four graphs have 190 vertices, 285 edges, are cubic, and have no C4, C8 or C16. The reconstructed final file agrees **byte-for-byte** with the input retained in the later gadget-compression bundle. The surgery specification is [reconstructed_surgeries.json](../provenance/reconstructed_surgeries.json).

The final graph's reported short spectrum is C3=56, C5=22, C6=44, C7=22, no cycles of lengths 8 through 16, and C17=12. A full two-switch scan was reported to find no further improvement. The new packaging logs independently record graph structure and counts at 4,8,16,32; they do not reconstruct the historical neighborhood scan.

## Initial targeted search from 219,531

| Removed-edge scope | Reconnection tasks | C4/C8/C16-free survivors | Outcome |
|---|---:|---:|---|
| Three disjoint edges, top 30 incidence ranks | 29,304 | 873 | No improvement reported |
| Three disjoint edges, top 60 | 257,144 | 4,925 | No improvement reported |
| Four disjoint edges, top 20 | 234,060 | 3,213 | No improvement reported |
| Four disjoint edges, top 30 | 1,343,820 | 16,198 | Reached 216,687 |

The successful removed edges had approximate old incidence ranks 6,10,17,27. These rankings are not a theorem about which edges a successful move must use.

## Reported negative scopes from the polished 216,246 graph

| Scope | Tasks | Short-hole survivors |
|---|---:|---:|
| Adjacent three-edge moves, top 60 | 34,590 | 940 |
| Disjoint four-edge moves, top 30 | 1,515,240 | 26,055 |
| Adjacent four-edge moves, top 30 | 225,855 | 5,582 |
| Disjoint five-edge moves, top 12 | 430,848 | 2,905 |
| Disjoint five-edge moves, top 15 | 1,633,632 | 15,297 |
| Disjoint six-edge moves, top 10 | 1,268,400 | 5,181 |
| Seven of the top eight edges | 632,064 | 1,238 |
| All top eight edges | 1,190,672 | 2,037 |
| Coverage-ranked four-edge sets outside top 30 | 600,000 | 5,617 |
| Four-edge incidence shell, ranks 31–35 | 1,276,980 | 14,736 |

The reported total across both tables is **10,672,609 tasks** and **104,797 survivors**. Packaging checked that the arithmetic sums agree; it did not re-execute those searches. Nested top-K scopes overlap, so the total is workload, not a disjoint enumeration or number of isomorphism classes.

## Coverage versus replacement-cycle creation

The chat reported that the best joint-coverage cut intercepted 174,172 of the 216,246 existing C32s. Ten thousand leading complementary four-edge cuts were each tested with 60 deranged reconnections, giving the 600,000-task row. No improvement was reported.

This motivated a more precise objective:

`old C32s destroyed - new C32s created`.

For a new edge uv in a cut graph, a new C32 using only that new edge corresponds to a simple length-31 path from u to v. Such path counts account for single-new-edge cycles, but cycles containing several new edges require joint routing. The retained results contain no complete path-aware branch-and-bound implementation. The subsequent successful advance came from exact cell compression.
