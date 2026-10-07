# Corrections, supersession, and evidence gaps

This file takes precedence over historical prose where an early interpretation conflicts with a later corrected result. Research notes are retained in `provenance/` and their experiment directories, with the archival prose edits described in [PROVENANCE.md](PROVENANCE.md). Git history preserves the imported versions.

## C01 — Withdrawn 64-vertex / seven-C16 claim

An early response claimed a cubic 64-vertex graph with seven C16s. A later response identified stale state/mislabeling; the purported modified edges were not edges of the saved source. The clean reconstruction's best count in that surgery family was reported as 117. The seven-cycle result is withdrawn and must not be used in a frontier or specimen table.

## C02 — Incorrect C32 projection decomposition

For the 184-vertex hub lift, the original values 163,821 voltage-zero base C32s, 491,463 corresponding lifted cycles and only 846 other cycles are withdrawn. The corrected historical split is 49,360 voltage-zero base cycles -> 148,080 lifted simple-projection cycles; 148,338 lifted cycles with nonsimple base projections; and 195,891 additional hub cycles. The sum is 492,309.

Packaging recounted the base, uncapped lift and hub totals but did not redo the full projection classification. The original conclusion that 99.8% of C32s were controlled by simple-base-cycle linear forms is invalid. A voltage solver must include repeated projections and cap routes.

## C03 — Lost 224,547 checkpoint and overconfident local certificates

The n190/224,547 graph's scratch edge list was reported lost after a container restart. Its claimed neighborhood scans and bounded saddle results have no complete retained ledger in this archive. They remain historical reports only. Better later graphs do not recover that exact graph or prove those local claims.

Other early scores such as n186/264,624, n198/248,305, and several intermediate descent states lack retained graph artifacts. The 220,225 and 219,531 states are exceptions: packaging recovered them from serialized chat data and the complete incidence table, respectively, and directly checked their counts. See `data/missing_artifacts.json`.

## C04 — A filename or hash printed in a response is not verification

Some earlier tool calls failed when a source scratch path no longer existed. Several files were then reconstructed from saved serialization or edge data. This package uses only existing bytes, explicit reconstructions, and actual check outputs. The outer manifest supersedes handwritten hashes for package file identity. Integrity hashes do not establish graph properties.

## C05 — Workload totals are not distinct graphs

The multi-edge workload totals sum correctly to 10,672,609 tasks and 104,797 short-hole survivors, but nested top-K scopes overlap and isomorphism deduplication is not implied. Complete underlying task ledgers are unavailable. The successful 219,531 -> 216,687 -> 216,367 -> 216,246 surgeries are retained and rechecked separately.

The same rule applies to candidate assignments, learned schema records, transition actions, prefix nodes, labelled attachments, and witness counts throughout the archive. Do not add them and call the sum a number of nonisomorphic graphs.

## C06 — Incomplete work is UNKNOWN

The order-16 cap census was not completed here. The 196-probe saddle grid completed only 98 probes. Several targeted multi-edge tests were initially launched but not completed; later reports should be read by their stated scope, not as a blanket neighborhood proof. Every retained joint-synthesis and identification run remains UNKNOWN or UNKNOWN_SOLVER. A witness rejecting a candidate is not a proof that the search domain is exhausted.

## C07 — A capped count is not an upper bound

The joint research notes correct a historical field called `best_c16_upper_cap`: it stored a capped count of found witnesses, not a proven upper bound. Updated search sources rename it. Hitting a count cap supplies a lower bound; a timed-out absence query supplies no absence proof.

## C08 — Three-edge contraction is not a cover projection

A simple cycle crosses a three-edge cell boundary zero or twice, so the cell quotient is simple along that cycle. In a graph cover, simple lifted cycles can project to nonsimple closed walks. The `<2*girth` lemma justifies simple projections only in the explicit length window of the gap64 construction.

## C09 — Short-hole milestones are not counterexamples

The n370 graph contains C64 and the n26,550 graph contains C128. Their complete minimum-degree-three property does not compensate for those forbidden cycles. Boundary phase graphs avoid every power but have degree-two vertices. Larger graph order introduces additional powers that must be checked. No graph produced here satisfies both requirements for a counterexample.

## C10 — Individual path gaps are neither sufficient nor necessary

Theta(2,3,3) has gapped terminal paths but universally transmits a fourfold cycle. Conversely, the G11 turn contributes every length in [5,7], yet repeated on a dyadic quotient cycle stays in the gap [5r,7r]. Evaluate composed supports and unused-terminal compatibility, not a scalar measure of individual gappiness.

## C11 — No single common multiplier does not imply escape

The pentagon and U11 transmit dyadic cycles using factors that depend on the turn sequence. The four-turn common-factor test is sufficient but not necessary. The final 554-cell classification is 468 certified uniform transmitters and 86 explicit local escapes. The earlier 467/86/1 outcome is superseded by the U11 theorem.

## C12 — Two different catalogues

The 181-cell census is exhaustive only for biconnected simple degree-two/three cells with 3–7 terminals and at most six degree-three vertices. The 554-cell catalogue combines specified families and restricted enumerations; it is not every graph below an order bound. Their filters and unresolved counts refer to different domains, not successive exhaustive order frontiers.

## C13 — Uniform reductions do not eliminate mixed ingredients

A transmitting cell uniformly replacing a simple quotient cannot turn a quotient dyadic cycle into a fully power-free expansion. This is a reduction, not a proof that every quotient satisfies the conjecture. Different cell mixtures, loops, parallel connections, and identification need separate arguments. The joint/mixed searches correctly retain individually transmitting cell options.

## C14 — Larger interfaces require disjoint multi-path states

With five or more terminals, a simple cycle can visit the same cell more than once. Correct oracles enumerate simultaneous mutually vertex-disjoint routes and require one connected circuit. Merely multiplying one terminal-path polynomial per cell can miss cycles or count nonsimple configurations.

## C15 — Frozen-backbone exclusions are local to their domains

The ring-completion bounds and cap incompatibilities prohibit specified additions on fixed graphs. They do not prohibit replacing old edges, attaching a network of new cells, using all larger caps, or all noncubic completions. The phase-cap library was tested fully only on the 32- and 40-vertex seeds, not the 64-vertex seed.

## C16 — Identification is nonmonotone

Adding edges cannot destroy a forbidden cycle; identifying vertices can destroy its simplicity. Therefore naive monotone cycle-blocking clauses are unsound for fusion. The retained identification program uses collision-guarded clauses, checked independently. Its exact degree constraints also avoid incorrectly rejecting all pairs with shared neighbors.

## C17 — Discarded checkpoint resumes

Two exploratory joint-search resumes were discarded because diagnostic solver serialization included internal model-converter commands. Retained continuations use assertion-only exports. Excluded resumes are not part of the reported run totals or archive. An earlier theta-backbone labeling diagnostic was corrected before the retained identification trials.

## C18 — Bridge exception superseded in one family

The bridgeless turn-charge theorem originally left cores with bridges outside scope. The final leaf-component argument rules out **all-T7/T15** assemblies on every connected simple cubic core, including bridges. It does not rule out arbitrary mixed templates or noncubic quotients. The wider mixed family instead has global and leaf-component necessary inequalities.

## C19 — Solver optimality and novelty

The order-370 integer program reported optimality only for its fixed core and two cell types; the graph certificate establishes feasibility, not global minimum order. The order-26,550 solver produced a feasible assignment without proving its restricted objective optimal. No packaging check establishes literature priority, peer review, or a new general bound on the minimum counterexample order.

## C20 — Earlier “only algebra can work” assessments

The upstream report's first-moment and counting heuristics were motivations, not all-family impossibility theorems. Their extrapolations must not be used as exact early filters. The continuation's actual filters have stated finite domains or written mathematical proofs.

## C21 — Packaging verification is not a rerun of discovery

The nine certificate verification programs passed again, and the selected retained graph counts were recounted. The expensive discovery searches, full early neighborhood enumerations, upstream frontier computations, and all generator scopes were not rerun. The included fresh logs state exactly what executed. Infinite theorems remain written mathematical arguments with finite ingredient checks, not formal proofs produced by the software.

## C22 — “Retained” in old prose versus bytes actually available

The gadget note calls both intermediate improvements retained, but its delivered bundle contains the 178,077 graph and not a separate 180,300 edge list. Similarly, several early final messages linked scratch files that were not among the mounted artifacts at packaging. The graph inventory, original-member manifests and explicit reconstruction map—not the adjective “retained” in an old response—define what is available now. The available 303,008 checkpoint has been recounted; it is not the missing 224,547 graph.
