# Checks executed during packaging

Date: 2026-10-06. These are newly executed packaging checks, separate from the original discovery and verification logs. All five original bundle manifests also matched before and after running these programs.

| Program | Status | Observed seconds | Log |
|---|---|---:|---|
| `01-gadget-compression/verify.py` | PASS | 1.481 | [Log](01-gadget-compression--verify.log) |
| `02-gap64/verify.py` | PASS | 5.031 | [Log](02-gap64--verify.log) |
| `02-gap64/verify_structural.py` | PASS | 0.718 | [Log](02-gap64--verify_structural.log) |
| `02-gap64/verify_theta_dilation.py` | PASS | 1.169 | [Log](02-gap64--verify_theta_dilation.log) |
| `03-phase-interfaces/verify.py` | PASS | 10.099 | [Log](03-phase-interfaces--verify.log) |
| `04-interface-filters/verify_results.py` | PASS | 9.006 | [Log](04-interface-filters--verify_results.log) |
| `04-interface-filters/oracle_regression.py` | PASS | 1.074 | [Log](04-interface-filters--oracle_regression.log) |
| `05-joint-synthesis/verify.py` | PASS | 14.455 | [Log](05-joint-synthesis--verify.log) |
| `05-joint-synthesis/verify_learning.py` | PASS | 12.952 | [Log](05-joint-synthesis--verify_learning.log) |

Twenty-one central graph files received structural inspection and the selected exact direct counts in [graph_checks.json](graph_checks.json). The n26,550 graph was checked by the gap64 structural verifier rather than the order-limited direct enumerator.

[input_manifest_audit.json](input_manifest_audit.json) records the five original content-manifest checks. [environment.json](environment.json) records the observed runtime. [verifier_runs.json](verifier_runs.json) contains machine-readable commands and verdicts.

Passing a certificate checker does not establish literature priority, proof-assistant formalization, completeness of an unrerun generator, or nonexistence in an UNKNOWN search domain. No expensive discovery solver was run during packaging.
