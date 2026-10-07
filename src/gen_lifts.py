#!/usr/bin/env python3
"""Cyclic (Z_m) voltage-graph lifts of small cubic base multigraphs, n <= 64.

Base graphs (with spanning-tree edges fixed to voltage 0; only cotree edges
sweep voltages — WLOG up to lift isomorphism):
  theta  : 2 vertices, 3 parallel edges           (lift order 2m)
  k4     : K4                                     (lift order 4m)
  k33    : K3,3                                   (lift order 6m)
  cube   : Q3                                     (lift order 8m)
  petersen : Petersen                             (lift order 10m)

Every simple lift is emitted as graph6 (min degree 3 = cubic by construction;
multigraph lifts that collapse to multi-edges/loops are skipped).
Usage: gen_lifts.py <base> [mmax]
"""
import itertools
import sys

import networkx as nx

BASES = {
    "theta": (2, [(0, 1), (0, 1), (0, 1)]),
    "k4": (4, [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]),
    "k33": (6, [(0, 3), (0, 4), (0, 5), (1, 3), (1, 4), (1, 5), (2, 3), (2, 4), (2, 5)]),
    "cube": (8, [(0, 1), (0, 2), (0, 4), (1, 3), (1, 5), (2, 3), (2, 6), (3, 7),
                 (4, 5), (4, 6), (5, 7), (6, 7)]),
    "petersen": (10, [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0), (0, 5), (1, 6),
                      (2, 7), (3, 8), (4, 9), (5, 7), (7, 9), (9, 6), (6, 8), (8, 5)]),
}


def lift(nb, edges, volts, m):
    g = nx.Graph()
    for (u, v), a in zip(edges, volts):
        for i in range(m):
            x, y = u * m + i, v * m + (i + a) % m
            if x == y or g.has_edge(x, y):
                return None                     # loop or multi-edge: not simple
            g.add_edge(x, y)
    return g


def main():
    base = sys.argv[1]
    nb, edges = BASES[base]
    mmax = int(sys.argv[2]) if len(sys.argv) > 2 else 64 // nb
    mmax = min(mmax, 64 // nb)
    # spanning tree of the base: fix those voltages to 0
    tree = set()
    seen = {edges[0][0]}
    changed = True
    tree_idx = set()
    while changed:
        changed = False
        for i, (u, v) in enumerate(edges):
            if i in tree_idx:
                continue
            if (u in seen) != (v in seen):
                tree_idx.add(i)
                seen |= {u, v}
                changed = True
    cotree = [i for i in range(len(edges)) if i not in tree_idx]
    count = 0
    for m in range(3, mmax + 1):
        for volts_cot in itertools.product(range(m), repeat=len(cotree)):
            volts = [0] * len(edges)
            for i, a in zip(cotree, volts_cot):
                volts[i] = a
            g = lift(nb, edges, volts, m)
            if g is not None and nx.is_connected(g):
                sys.stdout.write(nx.to_graph6_bytes(g, header=False).decode())
                count += 1
    print(f"gen_lifts {base}: {count} simple connected lifts (m<= {mmax})", file=sys.stderr)


if __name__ == "__main__":
    main()
