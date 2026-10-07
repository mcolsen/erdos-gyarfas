#!/usr/bin/env python3
"""CNF for the bipartite min-degree-3 search at order n: minDegree(3) plus a
2-coloring (color var per vertex; every edge joins different colors). Sound and
complete for bipartite graphs: any bipartite graph admits a coloring assignment,
and any model's edge set is bipartite by construction.

Usage: encode_bipartite.py n > enc.cnf"""
import sys

from pysms.graph_builder import GraphEncodingBuilder

n = int(sys.argv[1])
b = GraphEncodingBuilder(n, directed=False)
b.minDegree(3)
color = {v: b.id() for v in b.V}
for u in b.V:
    for v in b.V:
        if u < v:
            e = b.var_edge(u, v)
            b.append([-e, color[u], color[v]])
            b.append([-e, -color[u], -color[v]])
b.print_dimacs(sys.stdout)
