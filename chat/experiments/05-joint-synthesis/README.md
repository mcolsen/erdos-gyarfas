# Erdős–Gyárfás joint-interface research bundle

**No counterexample or new complete near-miss was found. All included search runs are unresolved.**

Read `RESEARCH.md` for the new proofs, precise scopes, run results, and audit notes.

Certificate verification needs Python and NetworkX only:

```sh
python -m pip install -r requirements.txt
python verify.py
python verify_learning.py
```

`verification.log` and `learning_verification.log` record completed independent checks. The `src/` directory contains optional joint synthesis and collision-guarded identification solvers. Those additionally use a native Z3 shared library and a compiled C++ witness finder. They are not needed to verify the certificates.

`data/catalog.json` is the explicit preceding 554-cell catalogue, not an exhaustive graph classification. Original run summaries are retained unchanged. In them, `best_c16_upper_cap` is a historical misnomer for a capped witness count, NOT a numerical upper bound or an extremal result. See the research note.

The manifest lists SHA-256 hashes of all bundle payload files. `check_manifest.py` verifies them.
