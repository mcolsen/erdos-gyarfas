#!/usr/bin/env python3
"""CNF for the *minimal-counterexample* structural search at order n.

Encodes (all proved in verification/carr-2605.22844-verification.md):
  - min degree >= 3
  - vertices of degree >= 4 form an independent set        [Markström 2004]
  - every vertex has a neighbor of degree exactly 3        [Carr 2026, Cor 0.1(1)]
  - #{v : deg(v) >= 4} <= floor(n/3)                       [my 2/3 strengthening]
  - max degree <= floor((n-1)/2)                           [C4-free + δ≥3 theorem;
      sound because every solution is C4-free via the forbidden-subgraph file]

high_v is one-directionally reified (deg >= 4 ⟹ high_v) by the sequential
counter, which is the sound direction for all uses here (high_v occurs only
negatively in the added clauses, and positively only under the cardinality
upper bound, so spurious-true assignments never admit extra solutions and
forced-true assignments enforce exactly the intended constraints).

UNSAT at order n, given assumption-free UNSAT at every order < n, extends the
frontier to n (a minimum-order counterexample would satisfy the structure).

Usage: encode_structural.py n > enc.cnf
"""
import sys

from pysms.graph_builder import GraphEncodingBuilder

n = int(sys.argv[1])
b = GraphEncodingBuilder(n, directed=False)
b.minDegree(3)
b.maxDegree((n - 1) // 2)

high = {}
for v in b.V:
    inc = [b.var_edge(v, u) for u in b.V if u != v]
    cv = b.counterFunction(inc, 4)
    high[v] = cv[3]                      # true whenever deg(v) >= 4

for u in b.V:
    for v in b.V:
        if u < v:
            b.append([-high[u], -high[v], -b.var_edge(u, v)])

for v in b.V:
    auxs = []
    for u in b.V:
        if u == v:
            continue
        a = b.id()
        b.append([-a, b.var_edge(u, v)])
        b.append([-a, -high[u]])
        auxs.append(a)
    b.append(auxs)                       # some neighbor of v is cubic

b.counterFunction([high[v] for v in b.V], n // 3, atMost=n // 3)

b.print_dimacs(sys.stdout)
