# Interface-filter research bundle

No Erdős–Gyárfás counterexample is claimed. See RESEARCH_NOTE.md for theorems, scope limits, and experiment details.

## Verify the retained results

```sh
python verify_results.py
python oracle_regression.py
```

Python and NetworkX are the only required dependencies. Verification does not run an optimizer or access the network.

`catalog.json` is the authoritative explicit cell catalogue. `screen.json` gives the finite four-turn certificates. The three certificate JSONs in `completions/` are graph-witness proofs of frozen-backbone cubic-completion impossibility. The two triangle ledgers contain every tested compatible assembly and its actual forbidden-cycle witness.

`interface_oracle.py` checks cycles with repeated cell visits via vertex-disjoint routing states and a one-circuit condition. Its `spectrum(new)` returns the support of cycles using ALL specified added edges; the empty input covers ring-traversing cycles only. Cell-internal cycles are checked separately.

Optional exhaustive motif reproduction:

```sh
python test_double_triangles.py
python test_triple_triangles.py
```

Do not interpret a successful uniform-cell reduction as a blanket exclusion of arbitrary mixed-cell assemblies. Do not interpret a protected loop with unfilled terminals as a minimum-degree-three graph.
