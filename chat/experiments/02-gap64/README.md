# Five-power-free construction and structural obstructions

This bundle contains a **26,550-vertex simple connected cubic graph** with no
cycles of lengths 4, 8, 16, 32 or 64. It has no cycle of any length from 16
through 64, exactly 630 cycles of length 65, and an explicit cycle of length128.
**It is not an Erdős–Gyárfás counterexample.** No order-minimality or publication
priority is claimed.

The graph is `data/eg26550.edge`, a one-based DIMACS edge list. Its SHA-256 is
`9279d54bb246b2368f895fc5e144342c3da336955745bb802023ff7424538064`.

## Verify without an optimization solver

The installed versions used here were Python3.13.5, NetworkX3.6.1, NumPy2.3.5,
and SciPy1.17.0. Only NetworkX is required for the certificate verifiers.

```sh
python -m pip install -r requirements.txt
python verify.py
python verify_structural.py
python verify_theta_dilation.py
c++ -O3 -std=c++17 src/weighted_core_verify.cpp -o weighted_core_verify
./weighted_core_verify data/core1890.edge data/core1890_types.txt
```

The Python construction verifier independently enumerates all base cycles up
to length20 using NetworkX, checks the modular voltages and minimum path
constraints, reconstructs the graph edge-for-edge, and checks actual C65 and
C128 witnesses. The C++ verifier uses neither the voltage equations nor the
base-cycle enumeration: it exhaustively checks low-cost simple cycles in the
1,890-vertex lifted core. Its expected output includes
`minimum_weight 65 core_cycles 630` and `PASS`.

`verify_structural.py` checks the closed triangle-composition grammar,
turn-charge identities and the five-terminal cell's routing certificate.
`verify_theta_dilation.py` checks a constructive balancing rule used in the
universal cycle-dilation proof. These two scripts write *_recheck.json files
in the certificates directory.

See `research_note.md` for the mathematical proofs and limitations. The
statements involving all bridgeless cubic cores use the classical
perfect-matching-polytope theorem; the three-edge-colourable specialization
has an elementary proof and suffices for the constructed core, whose three
perfect matchings are found and verified by `verify.py`.

## Optional design experiment

```sh
python -m pip install -r requirements-search.txt
python solve_design.py 25
```

This fixes the retained modulo15 voltage assignment and reruns the mixed
T7/T15 integer program. A timed rerun need not reproduce the same incumbent.
The saved graph and design are complete witnesses independent of solver
optimality. The original25-second run found an objective of1770 base-cell
vertices, or26550 after lifting; its bound was1707. It did **not** prove
optimality. A rerun writes `candidate_design.json` only if a feasible solution
is found, and never replaces the retained design.

## Gapped-cell experiment

`experiments/` contains a separate, unsuccessful experiment using genuine
gapped five-terminal theta cells on the incidence graph of the plane of
order4. The retained294-vertex graph has C4=C8=0 but C16=122, verified by the
independent full-graph counter. The cycle-dilation theorem in the note is the
reason this uniform-cell strategy is not a way to obtain a counterexample
without one already existing in its smaller quotient. The bounded local run
is not an impossibility proof or an optimum claim.

The initial modulo15 voltage search is also reproducible independently of the
cell-size integer program:

```sh
c++ -O3 -std=c++17 src/voltage_search.cpp -o voltage_search
./voltage_search data/voltage_constraints_C12.txt 15 3 11192030 voltage_candidate.txt
```

These1,008 constraints ban voltage-zero base C12s. The remaining base cycles
are handled by cell orientations and sizes, rather than requiring their
voltages to be nonzero as well.
