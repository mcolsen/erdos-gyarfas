#!/usr/bin/env python3
"""Cross-validate nbwtrace (C) against nbw_ref (Python bigint matrix power)."""
import subprocess
import sys

import networkx as nx

from nbw_ref import hashimoto_matrix, mat_pow_trace

BIN = sys.argv[1]
LS = [4, 6, 8, 10, 16]
fails = total = 0
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    g = nx.from_graph6_bytes(line.encode())
    g = nx.convert_node_labels_to_integers(g)
    edges = list(g.edges())
    H = hashimoto_matrix(edges)
    ref = {L: mat_pow_trace(H, L) for L in LS}
    out = subprocess.run([BIN, "-L", ",".join(map(str, LS))],
                         input=line + "\n", capture_output=True, text=True)
    got = {}
    for tok in out.stdout.split():
        if tok.startswith("tr"):
            k, v = tok[2:].split("=")
            got[int(k)] = int(v)
    total += 1
    for L in LS:
        if ref[L] != got.get(L):
            fails += 1
            print(f"MISMATCH {line} L={L} ref={ref[L]} c={got.get(L)}")
print(f"xval_trace: {total} graphs x {len(LS)} lengths, {fails} mismatches")
sys.exit(1 if fails else 0)
