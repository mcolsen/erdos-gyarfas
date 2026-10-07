#!/usr/bin/env python3
"""Generate structured cubic/min-deg-3 families as graph6 to stdout.

Families:
  gp      : generalized Petersen GP(n,k), 3<=n<=NMAX, 1<=k<n/2  (2n vertices)
  igraph  : I-graphs I(n,j,k), j,k < n/2 (generalizes GP)
  circ    : circulants C_n(S), |S| in {2,3}, degree 4 or 6 (min degree >= 3)
Usage: gen_families.py <family> <NMAX>
"""
import itertools
import sys

import networkx as nx


def emit(g):
    if not nx.is_connected(g):
        return
    sys.stdout.write(nx.to_graph6_bytes(g, header=False).decode())


def gp(n, k):
    g = nx.Graph()
    for i in range(n):
        g.add_edge(("u", i), ("u", (i + 1) % n))
        g.add_edge(("u", i), ("v", i))
        g.add_edge(("v", i), ("v", (i + k) % n))
    return nx.convert_node_labels_to_integers(g)


def igraph(n, j, k):
    g = nx.Graph()
    for i in range(n):
        g.add_edge(("u", i), ("u", (i + j) % n))
        g.add_edge(("u", i), ("v", i))
        g.add_edge(("v", i), ("v", (i + k) % n))
    return nx.convert_node_labels_to_integers(g)


def circulant(n, s):
    g = nx.Graph()
    for i in range(n):
        for d in s:
            g.add_edge(i, (i + d) % n)
    return g


def main():
    fam, nmax = sys.argv[1], int(sys.argv[2])
    if fam == "gp":
        for n in range(3, nmax + 1):
            for k in range(1, (n - 1) // 2 + 1):
                emit(gp(n, k))
    elif fam == "igraph":
        for n in range(3, nmax + 1):
            for j in range(1, (n - 1) // 2 + 1):
                for k in range(j, (n - 1) // 2 + 1):
                    g = igraph(n, j, k)
                    if min(d for _, d in g.degree()) >= 3:
                        emit(g)
    elif fam == "circ":
        for n in range(7, nmax + 1):
            half = n // 2
            for size in (2, 3):
                for s in itertools.combinations(range(1, half + 1), size):
                    g = circulant(n, s)
                    if min(d for _, d in g.degree()) >= 3:
                        emit(g)
    else:
        raise SystemExit(f"unknown family {fam}")


if __name__ == "__main__":
    main()
