# Findings index

This is the cross-stage result register. Scope and evidence labels are part of every claim. The original proofs, experiment details and files are linked from the topic notes. No counterexample or literature-priority claim is made.

| ID | Finding | Evidence and limit | Note |
|---|---|---|---|
| B01 | Prior campaign lower bounds: general >=36, cubic >=50, bipartite >=57 | `historical_upstream`. Background from the user repository, not a new continuation result. | [Read](docs/01-prior-campaign-context.md) |
| G01 | 61-vertex one-deficiency seed: C4=C8=0, C16=8, C32=176980 | `retained_graph_fresh_count`. Not an alpha-block or counterexample. | [Read](docs/02-alpha-block-and-voltage-lifts.md) |
| G02 | 184-vertex cubic Z3 hub lift: no C4/C8/C16; C32=492309 | `retained_graph_fresh_count`. Corrected projection split matters; nonsimple base projections cannot be ignored. | [Read](docs/02-alpha-block-and-voltage-lifts.md) |
| G03 | Noncubic 183- and 181-vertex lift completions: C32=819153 and 831828 | `retained_graph_fresh_count`. Degree-four/six examples, still contain C32. | [Read](docs/02-alpha-block-and-voltage-lifts.md) |
| G04 | Triangle cap: n186 C32=476415; symmetry-broken n186 C32=279630 | `retained_graph_fresh_count`. No C4/C8/C16; count reduction only. | [Read](docs/03-cap-and-local-search-history.md) |
| H01 | Reported n190 C32=224547 local basin | `historical_missing_artifact`. Exact graph and complete neighborhood ledger lost; report only. | [Read](docs/03-cap-and-local-search-history.md) |
| G05 | Recovered n190 checkpoints C32=220225 and 219531 | `reconstructed_fresh_count`. Reconstructed from explicit serialization/table and directly recounted. | [Read](docs/03-cap-and-local-search-history.md) |
| G06 | Targeted surgery: 219531 ->216687 ->216367 ->216246 | `reconstructed_fresh_count`. Successful edge operations retained; aggregate historical exhaustive ledgers not retained. | [Read](docs/04-targeted-multiedge-search.md) |
| H02 | 10,672,609 reported reconnection tasks; 104,797 survivors | `historical_workload_only`. Arithmetic checked; workload includes overlapping scopes, not unique graphs. | [Read](docs/04-targeted-multiedge-search.md) |
| T01 | Exact compression through three-edge interfaces | `written_proof_and_finite_checks`. Simple cycle crosses zero/two boundary edges; applies to this decomposition, not arbitrary covers. | [Read](docs/05-exact-gadget-compression.md) |
| G07 | n190 no C4/C8/C16, C32=178077 | `retained_graph_fresh_count`. Best retained fixed-order count in this chat, not a global record. | [Read](docs/05-exact-gadget-compression.md) |
| M01 | Approximately 1,832-fold specialized counting speedup | `retained_benchmark`. Historical measured runtime includes process startup; not universal performance. | [Read](docs/05-exact-gadget-compression.md) |
| G08 | n370 cubic: no C4/C8/C16/C32; gap16-32; C33=43 | `retained_construction_certificate`. Explicit C64; fixed-core solver optimality is not global order minimality. | [Read](docs/06-order370-cycle-gap.md) |
| T02 | 13- and 15-cycle parity contradictions on two cores | `written_proof_and_finite_certificates`. All T3/T7/T15 assignments on those two cores excluded as full counterexamples. | [Read](docs/07-fixed-core-parity-obstructions.md) |
| G09 | n26550 cubic: no powers through64; gap16-64; C65=630 | `retained_construction_certificate`. Explicit C128; construction optimality not proved. | [Read](docs/08-order26550-cycle-gap.md) |
| T03 | 3*n3 - n7 -17*n15 >=9 on bridgeless cubic cores | `written_proof_with_external_theorem`. Necessary condition for these specific interval templates; mixed family not fully excluded. | [Read](docs/09-turn-charge-inequality.md) |
| T04 | Safe triangular recursion closes at T3,T7,T15 | `written_proof_and_finite_certificates`. 540 local combinations plus induction; not all arbitrary cells. | [Read](docs/10-triangle-grammar-closure.md) |
| T05 | Theta(2,3,3) uniform fourfold dilation | `written_proof_and_regression`. Includes scoped quotient extensions; not an arbitrary mixed-cell exclusion. | [Read](docs/11-theta233-dilation.md) |
| G10 | 294-vertex theta assembly: C4=C8=0, C16=122 | `retained_graph_fresh_count`. Retained unsuccessful experiment; no optimum established. | [Read](docs/11-theta233-dilation.md) |
| C01 | 181-cell exhaustive small-interface domain | `scoped_census_and_verifier`. 3-7 terminals, <=6 cubic vertices, biconnected and simple; precise domain only. | [Read](docs/12-exhaustive181-cell-census.md) |
| T06 | Four-turn block certificate proves uniform dyadic inheritance at all scales | `written_proof_and_finite_certificates`. 152/181 certified in the first domain; labels do not carry automatically to mixed libraries. | [Read](docs/12-exhaustive181-cell-census.md) |
| T07 | Theta(2,3,4) cycle family is power-free iff exactly one A turn | `written_proof_and_finite_checks`. For dyadic quotient cycles using specified A/B passages, not all routes in a complete graph. | [Read](docs/13-theta234-phase-hole.md) |
| G11 | Power-free phase boundary graphs at n32,n40,n64 | `retained_boundary_graphs`. Degree-two terminals remain; total cycle counts 204,258,49176. | [Read](docs/13-theta234-phase-hole.md) |
| E01 | Three-cell strip exclusion | `finite_closure_certificate`. 46 specified cells, 4668 actions,553 states,2581404 transitions checked; only this architecture. | [Read](docs/14-strips-and-four-link-gluings.md) |
| G12 | 18-vertex six-terminal cell from four-link gluing | `retained_cell_and_generator`. Eight labelled survivors, one isomorphism class; not a degree-complete graph. | [Read](docs/14-strips-and-four-link-gluings.md) |
| E02 | Phase-ring edge/hub/cap repair exclusions | `finite_path_and_constraint_certificates`. Frozen seeds; all184 caps tested on n32 and n40 only; arbitrary networks not excluded. | [Read](docs/15-phase-boundary-repair.md) |
| C02 | Constructed catalogue of554 cells | `explicit_catalogue_and_verifier`. Specified families/restricted enumerations, not exhaustive by graph order. | [Read](docs/16-constructed554-cell-catalogue.md) |
| T08 | Pentagon variable-factor transmission | `written_proof_and_regression`. Can require factor2 or4; no single common factor needed. | [Read](docs/17-block-and-pentagon-transmission.md) |
| T09 | Hexagon parity, heptagon odd-divisor and G11 narrow-band escapes | `written_proofs_and_finite_checks`. Selected simple quotient cycle families; unused terminals remain. | [Read](docs/18-composition-escape-examples.md) |
| E03 | H56, X60, G88 fixed completion limits: <=2,19,8 edges | `finite_impossibility_certificates`. Each needs20; bounds from witnesses/conflict certificates; fixed vertex set and matching scope. | [Read](docs/19-frozen-backbone-completions.md) |
| M02 | Exact repeated-visit interface oracle | `implementation_and_independent_regression`. Multi-path disjointness, parity equations and one-circuit constraint;24 full-spectrum controls. | [Read](docs/20-exact-interface-oracle.md) |
| E04 | 47,647 mixed triangle-motif candidates rejected | `retained_rejection_ledgers`. 47501 C8 witnesses,146 C16; complete explicit motif/library scopes, labelled counts. | [Read](docs/21-mixed-cell-synthesis-motifs.md) |
| T10 | Exact heptagon safe profiles at every dyadic scale | `written_proof_and_finite_regression`. Three allowed profiles depending on exponent parity;11304 regression profiles. | [Read](docs/22-heptagon-phase-classification.md) |
| T11 | U11 variable-factor transmission | `written_proof_and_finite_certificates`. 330 block types,329 repair identities; U11 differs from G11. | [Read](docs/23-u11-variable-transmission.md) |
| C03 | Final554-cell classification:468 transmitters,86 local escapes | `explicit_catalogue_classification`. No remaining unclassified supplied object; no all-cell classification or mixed exclusion. | [Read](docs/23-u11-variable-transmission.md) |
| M03 | Joint cell-choice and wiring model | `verified_learning_unknown_search`. 2337 assignments;13486 schemas;1095 topology-only records; all runs unresolved. | [Read](docs/24-joint-cell-and-wiring-search.md) |
| E05 | Universal bad three-link pattern across11 cell choices | `finite_quantified_certificate`. All1331 choices have a checked C8 orC16 witness; specific port topology only. | [Read](docs/24-joint-cell-and-wiring-search.md) |
| M04 | Collision-guarded identification learning | `verified_learning_unknown_search`. 6087 complete quotient candidates;67272 checked clauses; identification is nonmonotone. | [Read](docs/25-guarded-terminal-identification.md) |
| T12 | All-T7/T15 impossible on every connected simple cubic core | `written_proof_with_external_theorem`. Bridge extension closes earlier exception; specific templates, not all noncubic or mixed constructions. | [Read](docs/26-bridge-extension.md) |
| T13 | Local mixed-cell charge condition in every leaf bridge component | `written_proof_with_external_theorem`. Sum of ordinary vertex charges plus2*c_w >=9; necessary, not sufficient. | [Read](docs/26-bridge-extension.md) |

## Discrete documentation files

The numerical filenames follow topic order. The five experiment bundles retain their research notes in addition to these topic-specific extracts; [PROVENANCE.md](PROVENANCE.md) records the archival prose edits.

- [Scope, notation, and evidence conventions](docs/00-scope-and-conventions.md)
- [Prior campaign: starting point and constraints](docs/01-prior-campaign-context.md)
- [The 61-vertex near-miss and three-sheeted lift experiments](docs/02-alpha-block-and-voltage-lifts.md)
- [Cap design, symmetry breaking, and local-basin history](docs/03-cap-and-local-search-history.md)
- [Targeted multi-edge surgery: 219,531 to 216,246](docs/04-targeted-multiedge-search.md)
- [Exact three-terminal compression and cycle polynomials](docs/05-exact-gadget-compression.md)
- [The 370-vertex graph: no C4, C8, C16, or C32](docs/06-order370-cycle-gap.md)
- [Parity certificates for the two 34-vertex cores](docs/07-fixed-core-parity-obstructions.md)
- [The 26,550-vertex graph: no C4, C8, C16, C32, or C64](docs/08-order26550-cycle-gap.md)
- [Turn-charge inequality on bridgeless cubic cores](docs/09-turn-charge-inequality.md)
- [Closure of the safe triangle-composition grammar](docs/10-triangle-grammar-closure.md)
- [Theta(2,3,3): joint routing and fourfold dilation](docs/11-theta233-dilation.md)
- [The exhaustive 181-cell interface census](docs/12-exhaustive181-cell-census.md)
- [Theta(2,3,4): an exact-one phase hole at every dyadic scale](docs/13-theta234-phase-hole.md)
- [Disjoint-routing strip closure and four-link gluing](docs/14-strips-and-four-link-gluings.md)
- [Edge, hub and cap exclusions for the phase boundary graphs](docs/15-phase-boundary-repair.md)
- [The constructed 554-cell catalogue](docs/16-constructed554-cell-catalogue.md)
- [Four-turn transmission certificates and the pentagon exception](docs/17-block-and-pentagon-transmission.md)
- [Parity, odd-divisor and narrow-band composition escapes](docs/18-composition-escape-examples.md)
- [Certified limits on three frozen-backbone completions](docs/19-frozen-backbone-completions.md)
- [An exact repeated-visit interface oracle](docs/20-exact-interface-oracle.md)
- [Mixed-cell synthesis: 47,647 rejected assemblies](docs/21-mixed-cell-synthesis-motifs.md)
- [Heptagon turn-count profiles at every dyadic scale](docs/22-heptagon-phase-classification.md)
- [U11 variable-factor transmission and final catalogue classification](docs/23-u11-variable-transmission.md)
- [Joint cell-choice and wiring synthesis](docs/24-joint-cell-and-wiring-search.md)
- [Noncubic candidates and collision-guarded identification](docs/25-guarded-terminal-identification.md)
- [All-T7/T15 obstruction for cubic cores with bridges](docs/26-bridge-extension.md)
- [Scope limits and obstructions](docs/27-scope-limits-and-obstructions.md)
- [Verification methodology and what was rerun](docs/28-verification-methodology.md)

Machine-readable equivalent: [data/findings.json](data/findings.json). For current file availability and exact freshly checked graph counts, see [data/graphs/README.md](data/graphs/README.md). Historical gaps and superseded claims are documented in [CORRECTIONS.md](CORRECTIONS.md).
