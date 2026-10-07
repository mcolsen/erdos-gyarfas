# Dyadic-inheritance filters and phase-hole interfaces

**No counterexample is claimed.** The retained phase-ring graphs have degree-two terminals. They are explicit internally power-free boundary constructions, not minimum-degree-three graphs.

Start with `research_note.md` for the formulas, proofs, completed search scopes and limitations.

## Independent verification

With Python 3.10+ and NetworkX 3.1+:

```sh
python -m pip install -r requirements.txt
python verify.py
```

The final line should begin `PASS`. Network access is not used by the verifier. No SAT or integer-programming solver is required. Do not run Python with `-O`, which disables the verifier's assertions.

Important expected outputs:

```text
181 valid distinct cells; atlas control: 9
149 four-block certificates, 3 direct certificates, 22 explicit failures, 7 unresolved
83,161 four-turn cases
4,668 exact routing actions; 553 representative states
2,581,404 state/action checks; 142 valid labelled transitions; no two-step transition
32-vertex ring: 204 simple cycles, 16 degree-two terminals
40-vertex ring: 258 simple cycles, 20 degree-two terminals
64-vertex ring: 49,176 simple cycles, 32 degree-two terminals
184 cap exclusions on each of the 32- and 40-vertex rings
```

`logs/independent_verification.log` contains the retained execution result. Timing is incidental and depends on the machine.

## Construct the phase rings without search

```sh
python src/construct_phase_ring.py 8 /tmp/phase64.edge
python src/construct_phase_ring.py 4 /tmp/phase32.edge
python src/construct_phase_ring.py 5 /tmp/phase40.edge --all-a
```

The default requires a power-of-two number of cells at least four. It uses exactly one A passage. `--all-a` is the separately certified five-cell example. Output is a one-based DIMACS edge list. Graphs use `p edge N M` followed by `e u v` records.

## Regenerate the small catalogue and transfer closure

Work in a scratch copy because these exploratory generators write beside their own source files:

```sh
mkdir -p /tmp/eg-interface-rebuild
cp src/enumerate_skeletons.py src/enumerate_interfaces.py \
   src/screen_interfaces.py src/build_transfer.py src/strip_search.py \
   /tmp/eg-interface-rebuild/
python /tmp/eg-interface-rebuild/enumerate_skeletons.py
python /tmp/eg-interface-rebuild/enumerate_interfaces.py
python /tmp/eg-interface-rebuild/screen_interfaces.py small
python /tmp/eg-interface-rebuild/build_transfer.py
python /tmp/eg-interface-rebuild/strip_search.py
```

The census should end at 181. The transfer generator should produce 4,668 actions. The closure should have 553 states and an empty remaining queue. The final closure script has no time cutoff; with a different cell library, finite termination is not promised. The supplied independent verifier checks the retained closure entry by entry.

## Repeat selected C++ searches

These are small research probes, intended for the supplied simple, at-most-63/64-vertex inputs; they are not general graph-file parsers.

```sh
g++ -O3 -std=c++17 src/glue4_search.cpp -o /tmp/eg-glue4
/tmp/eg-glue4 data/cells7.txt data/cells7.txt /tmp/glue77.txt
```

Expected: 13,689 ordered cell pairs, 4,005,948 prefix nodes, eight labelled retained gluings. The verifier checks that the eight saved gluings are one isomorphism class and internally power-free.

```sh
g++ -O3 -std=c++17 src/attach_cell.cpp -o /tmp/eg-attach
/tmp/eg-attach data/phase_ring_4.edge data/caps_all.txt /tmp/caps32.txt 60
/tmp/eg-attach data/phase_ring_5.edge data/caps_all.txt /tmp/caps40.txt 60
```

Expected: `hits 0`, `exhaustive 1`; prefix states 3,162 and 3,864. The last argument is a runtime budget. A stopped run is not a negative certificate. The retained independent Python verifier instead proves these exclusions by reconstructing path supports and exhausting the cap injection constraint problems.

## Data layout

- `data/catalogue.json`: all 181 cells, terminal lists, complete path supports and screening status.
- `data/phase_cell.json`: the explicit theta(2,3,4) cell and all its terminal paths.
- `data/phase_ring_*.edge`: the three fully specified boundary graphs.
- `data/transfers.json`: exact single-path and two-disjoint-path actions.
- `data/super6.json`: the additional 18-vertex six-terminal cell.
- `certificates/inheritance.json`: finite inheritance and noninheritance witnesses.
- `certificates/strip_states.json`: the closed state set, transition list and actual graph reconstruction records.
- `certificates/strip_rejections.bin`: one witness byte per state/action pair; interpreted in `verify.py`.
- `certificates/gate*.txt`: explicit paths blocking edge additions, fusions or hubs.
- `certificates/cap_pair_screen_*.json`: per-template cap constraint results.
- `src/`: original generation/search probes and a standalone phase-ring constructor.
- `logs/`: completed run records and independent checks.
- `SHA256SUMS`: hashes of the retained files, excluding the manifest itself.

All mathematical scope restrictions are in the note. In particular, an inheritance certificate is a reduction to a smaller quotient, not a proof of the conjecture on arbitrary quotients. No repair exclusion in this bundle classifies all possible new junctions or arbitrary rewiring of a seed graph.
