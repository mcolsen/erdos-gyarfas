# Optional search sources

The certificate verifiers in the parent directory need only Python and NetworkX.
To reproduce synthesis experiments, install an ordinary native Z3 shared library
(`libz3.so.4` on the tested Linux system) and compile the exact witness oracle:

```sh
c++ -O3 -std=c++17 -shared -fPIC cycle_oracle.cpp -o cycle_oracle.so
python oracle_regression.py
python z3_regression.py
python joint_search.py --ports 7 7 7 --exposed 1 --strong --symmetry \
  --seconds 60 --solve-ms 2000 --seed 11 --out ../../joint_trial
python contraction_search.py --cell 7 --ring 8 --seconds 60 --out ../../identification_trial
```

Time-limited runs are not deterministic checkpoints across machines. `UNKNOWN`
and `UNKNOWN_SOLVER` are unresolved searches, not nonexistence certificates.
The `count` field with `exact=false` is the number of witnesses returned before
a limit, never a cycle-count upper bound. Historical run summaries used the
misleading key `best_c16_upper_cap`; no reported theorem depends on that field.
The current source renames it to describe the observed capped witness count.

SMT exports contain original assertions only. Never reload diagnostic exports
containing Z3's internal `(model-add ...)` or model-converter commands. The
round-trip regression checks this. The separate C++ library uses process-global
scratch storage: use separate processes, not concurrent threads sharing it.
