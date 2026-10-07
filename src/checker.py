#!/usr/bin/env python3
"""Arbitrary-size exact power-of-2 cycle checker (for graphs with n > 64 where
p2check.c's bitmask limit applies; cross-checked against p2check on n <= 64).

Reads graph6/sparse6 lines on stdin (or a file); for each graph reports the
smallest power-of-2 cycle length found, or SURVIVOR if none exists and
min degree >= 3. DFS with BFS-distance pruning, canonical root (min vertex).

Usage: checker.py [--limit L] [file]
  --limit L : only test power-of-2 lengths <= L (default: all <= n; use to
              defer very expensive large-L tests on big graphs)
"""
import sys
from collections import deque

import networkx as nx


def has_cycle_exact(adj, n, L, root_filter=None):
    for s in range(n):
        if root_filter and not root_filter(s):
            continue
        allowed = [v >= s for v in range(n)]
        dist = [1 << 30] * n
        dist[s] = 0
        dq = deque([s])
        while dq:
            u = dq.popleft()
            for w in adj[u]:
                if allowed[w] and dist[w] > dist[u] + 1:
                    dist[w] = dist[u] + 1
                    dq.append(w)
        on = [False] * n
        on[s] = True
        path = [s]

        def dfs(u, depth):
            if depth == L - 1:
                return s in adj_set[u]
            for w in adj[u]:
                if allowed[w] and not on[w] and dist[w] <= L - depth - 1:
                    on[w] = True
                    path.append(w)
                    if dfs(w, depth + 1):
                        return True
                    path.pop()
                    on[w] = False
            return False

        adj_set = adj_set_g
        for w in adj[s]:
            if w > s and dist[w] <= L - 1:
                on[w] = True
                path.append(w)
                if dfs(w, 1):
                    return True
                path.pop()
                on[w] = False
        on[s] = False
    return False


def analyze(g, limit=None):
    global adj_set_g
    n = g.number_of_nodes()
    g = nx.convert_node_labels_to_integers(g)
    adj = [sorted(g[v]) for v in range(n)]
    adj_set_g = [set(a) for a in adj]
    mind = min((len(a) for a in adj), default=0)
    L = 4
    lengths = []
    while L <= n and (limit is None or L <= limit):
        lengths.append(L)
        L *= 2
    for L in lengths:
        if has_cycle_exact(adj, n, L):
            return mind, L, lengths
    return mind, None, lengths


def main():
    args = sys.argv[1:]
    limit = None
    if args and args[0] == "--limit":
        limit = int(args[1])
        args = args[2:]
    src = open(args[0]) if args else sys.stdin
    total = surv = 0
    for line in src:
        line = line.strip()
        if not line:
            continue
        if line.startswith(":"):
            g = nx.from_sparse6_bytes(line.encode())
        else:
            g = nx.from_graph6_bytes(line.encode())
        total += 1
        mind, first, lengths = analyze(g, limit)
        if first is None:
            surv += 1
            tag = "SURVIVOR" if mind >= 3 else f"free-but-mindeg={mind}"
            print(f"{tag} n={g.number_of_nodes()} tested={lengths} g6={line}",
                  flush=True)
            if mind >= 3:
                print(f"*** POTENTIAL COUNTEREXAMPLE (verify C_L for L>{max(lengths, default=0)} if any fit) ***",
                      file=sys.stderr, flush=True)
    print(f"checker.py: {total} graphs, {surv} with no tested power-of-2 cycle",
          file=sys.stderr)


if __name__ == "__main__":
    main()
