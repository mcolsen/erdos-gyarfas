#!/usr/bin/env python3
"""CNF for the B0-block search at order n: min degree >= 2 and AT MOST ONE
vertex of degree exactly 2 (all others >= 3).

Rationale (notes/block-program.md): every counterexample to Erdős–Gyárfás has
a leaf block; a leaf block is 2-connected, has at most one vertex of
block-degree 2 (the cut vertex), and itself avoids every power-of-2 cycle
length up to its own order. Conversely, gluing two copies of such a block at
their degree-2 vertices (or one copy onto a power-free subdivision skeleton)
gives a full min-degree-3 counterexample. So this relaxed space is exactly
equivalent to the conjecture, and it is NOT covered by any published or
campaign ladder (those all required min degree >= 3 everywhere).

Degree cap encoding: per-vertex sequential counter, cv[2] <-> deg(v) >= 3
(pysms seqCounter is two-sided; validated count-exactly against a geng stack
before any frontier claim — see results/b0_validation.txt). Pairwise clauses
(deg3_u v deg3_v) forbid two low-degree vertices. Connectivity and
2-connectivity are deliberately NOT encoded: dropping them only enlarges the
space, so UNSAT conclusions remain sound for the block frontier.

Usage: encode_b0.py n > enc.cnf
"""
import os
import sys

from pysms.graph_builder import GraphEncodingBuilder

n = int(sys.argv[1])
b = GraphEncodingBuilder(n, directed=False)
b.minDegree(2)

# Degree cap, SOUND ONLY when C4 is forbidden alongside this encoding (true
# for every ladder rung; validated count-exactly on the C4-only space).
# Proof: v of degree d, N(v) = {u_i}. Sum of (deg(u_i)-1) >= 2d-1 (at most
# one u_i has degree 2). Edges inside N(v) form a matching (a 2-edge path
# u_i-u_j-u_k closes a C4 through v), so they absorb <= 2*floor(d/2) of that
# sum; every remaining edge-endpoint lies outside {v} u N(v) and no outside
# vertex serves two u_i (C4 through v). Hence n-1-d >= 2d-1-2*floor(d/2)
# >= d-1, i.e. d <= n/2.
if os.environ.get("B0_NOCAP") != "1":
    b.maxDegree(n // 2)

deg3 = {}
for v in b.V:
    inc = [b.var_edge(v, u) for u in b.V if u != v]
    cv = b.counterFunction(inc, 3)
    deg3[v] = cv[2]                      # deg(v) >= 3

for u in b.V:
    for v in b.V:
        if u < v:
            b.append([deg3[u], deg3[v]])  # no two vertices of degree <= 2

b.print_dimacs(sys.stdout)
