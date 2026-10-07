# Reproduction and verification guide

## 1. Check content identity

From this archive's root directory:

```sh
python tools/check_archive.py
```

This is standard-library-only. It verifies the outer manifest, including the unmodified original sources and witness files. The five experiment directories additionally have nested manifests. All manifests describe the current tree, including the archival prose edits documented in [PROVENANCE.md](PROVENANCE.md). A hash check does not validate a graph property.

## 2. Run the independent certificate checks

The packaging run used Python 3.13.5 and NetworkX 3.6.1. The pinned verification dependency records that tested version, not a claim that other versions cannot work.

```sh
python -m pip install -r requirements-verify.txt
python tools/run_verifiers.py
```

Do **not** use `python -O`; the historical checkers use assertions. The wrapper removes inherited `PYTHONOPTIMIZE` for subprocesses. It writes fresh output below `.verification-output/`, leaving the original evidence logs unchanged. Set a different `--log-dir` to retain separate runs.

The per-program timeout is a guard against an unexpectedly slow environment. A timeout is reported as `TIMEOUT_UNKNOWN`, not a mathematical rejection. Increase `--timeout` as needed.

Individual suites are available:

```sh
python tools/run_verifiers.py --suite gadget
python tools/run_verifiers.py --suite gap64
python tools/run_verifiers.py --suite phase
python tools/run_verifiers.py --suite filters
python tools/run_verifiers.py --suite joint
```

The nine programs check graph reconstruction, template spectra, the finite ingredients of the written theorems, completion/strip certificates, rejection witnesses, and learned routing/identification rules. They do **not** rerun all catalogue generators or optimize new candidates.

## 3. Independent full-graph counts

Compile the separate canonical DFS implementation:

```sh
mkdir -p build
c++ -O3 -std=c++17 experiments/01-gadget-compression/direct_cycle_counter.cpp -o build/direct_cycle_counter
build/direct_cycle_counter data/graphs/n190_c32_178077.edge 32
build/direct_cycle_counter data/graphs/n370_c4c8c16c32free.edge 32
build/direct_cycle_counter data/graphs/n370_c4c8c16c32free.edge 33
```

Expected counts are `178077`, `0`, and `43`. The program normalizes rotations and orientations, checks simplicity of paths, and has a built-in graph-order cap of 10,000. Do not use it on the 26,550-vertex graph without treating a source change as a new implementation. The existing gap64 structural verifier is the appropriate exact certificate for that graph.

An optional third numeric argument is a count cap. Output `count>=K` is a lower bound, not an exact total. An exact zero requires normal completion. The legacy `cyclecap.c` is preserved but is not recommended as the main input-validation interface.

For the 26,550-vertex graph, a second independent weighted-core check is available:

```sh
cd experiments/02-gap64
c++ -O3 -std=c++17 src/weighted_core_verify.cpp -o ../../build/weighted_core_verify
../../build/weighted_core_verify data/core1890.edge data/core1890_types.txt
```

The expected output has no weight below 65 and reports 630 core cycles of minimum expansion weight 65. The Python verifier separately reconstructs the complete graph and checks the finite cycle constraints. Do not silently substitute walk-trace vanishing for simple-cycle absence.

## 4. Recover the early explicit checkpoints

```sh
python tools/reconstruct_legacy_graphs.py
```

This reconstructs 219,531 from a complete edge-incidence table, 220,225 from the literal saved serialization, and the three successful surgery checkpoints 216,687, 216,367, 216,246. It compares every resulting byte with the packaged graph and writes copies under `.verification-output/reconstructed/`.

It does not guess the missing 224,547 graph. The archive lists other missing intermediate objects separately.

## 5. Optional discovery runs

Each preserved experiment has its original discovery sources and dependency notes. Some searches need SciPy/integer programming, a C/C++ compiler, or native Z3. Those are not verification dependencies and are not bundled as executables. Old scratch paths in legacy sources/logs may need explicit adaptation; the archive does not pretend the entire historical runtime survived.

Timed stochastic searches do not guarantee the same checkpoint on a different computer. Explicit saved graphs and finite certificates are the reproducible objects. Seeds, complete configurations, solver verdicts, assertion-only state/constraint exports, witnesses, and graph files determine the recoverability of a search; diagnostic solver serialization was insufficient for the discarded checkpoints described in [CORRECTIONS.md](CORRECTIONS.md#c17--discarded-checkpoint-resumes).

## 6. What was checked while packaging

Read [verification/packaging/README.md](verification/packaging/README.md), `verifier_runs.json` and `graph_checks.json`. All nine chosen programs passed. The graph checks record actual direct-counter output, not inferred counts from file names. The large construction was verified structurally. Discovery runs and missing early ledgers were not recreated.
