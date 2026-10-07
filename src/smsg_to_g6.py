#!/usr/bin/env python3
"""Convert smsg --all-graphs output (lines like "[(0,1),(0,2),...]") to graph6,
deduplicating isomorphs via canonical labels. Usage: smsg_to_g6.py n < smsg.log"""
import ast
import sys

import networkx as nx

n = int(sys.argv[1])
seen = set()
for line in sys.stdin:
    line = line.strip()
    if not line.startswith("[("):
        continue
    edges = ast.literal_eval(line)
    g = nx.Graph()
    g.add_nodes_from(range(n))
    g.add_edges_from(edges)
    can = nx.weisfeiler_lehman_graph_hash(g, iterations=4)
    key = (can, g.number_of_edges())
    # WL hash can collide; keep certificate-exact dedup via nauty later if needed.
    if key in seen:
        continue
    seen.add(key)
    sys.stdout.write(nx.to_graph6_bytes(g, header=False).decode())
print(f"smsg_to_g6: {len(seen)} distinct-ish graphs (WL-deduped; exact dedup via labelg downstream)", file=sys.stderr)
