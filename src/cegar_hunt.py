#!/usr/bin/env python3
"""CEGAR *existence* hunt at a fixed order n: ask CaDiCaL for a min-degree-3,
C4-free graph, then block each discovered power-of-2 cycle (8/16/32) until
either a genuine counterexample survives (exit 42, prints graph6 loudly) or
the budget runs out. Deliberately NO minimality structure (a counterexample
at n need not be a *minimal* one) and no symmetry breaking that could slow
model-finding. This is a lottery ticket, not a decision procedure.

Usage: cegar_hunt.py n [max_rounds] [seed]
"""
import random
import sys
from collections import deque

import networkx as nx
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool
from pysat.solvers import Solver


def find_p2_cycle(adj, n):
    """Return (L, cycle-vertex-list) for the smallest power-of-2 cycle, else None."""
    adj_set = [set(a) for a in adj]
    L = 4
    while L <= n:
        for s in range(n):
            dist = [1 << 30] * n
            dist[s] = 0
            dq = deque([s])
            while dq:
                u = dq.popleft()
                for w in adj[u]:
                    if w >= s and dist[w] > dist[u] + 1:
                        dist[w] = dist[u] + 1
                        dq.append(w)
            on = [False] * n
            on[s] = True
            path = [s]

            def dfs(u, depth):
                if depth == L - 1:
                    return s in adj_set[u]
                for w in adj[u]:
                    if w >= s and not on[w] and dist[w] <= L - depth - 1:
                        on[w] = True
                        path.append(w)
                        if dfs(w, depth + 1):
                            return True
                        path.pop()
                        on[w] = False
                return False

            for w in adj[s]:
                if w > s and dist[w] <= L - 1:
                    on[w] = True
                    path.append(w)
                    if dfs(w, 1):
                        return L, list(path)
                    path.pop()
                    on[w] = False
        L *= 2
    return None


def main():
    n = int(sys.argv[1])
    max_rounds = int(sys.argv[2]) if len(sys.argv) > 2 else 200000
    seed = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    random.seed(seed)
    pool = IDPool()

    def ev(i, j):
        i, j = min(i, j), max(i, j)
        return pool.id(("e", i, j))

    cnf = []
    # min degree >= 3
    for v in range(n):
        inc = [ev(v, u) for u in range(n) if u != v]
        cnf.extend(CardEnc.atleast(lits=inc, bound=3, vpool=pool,
                                   encoding=EncType.seqcounter).clauses)
    # C4-free, eager
    for a in range(n):
        for b in range(a + 1, n):
            others = [x for x in range(n) if x != a and x != b]
            for ci in range(len(others)):
                for di in range(ci + 1, len(others)):
                    c, d = others[ci], others[di]
                    cnf.append([-ev(a, c), -ev(c, b), -ev(b, d), -ev(d, a)])
    # max degree cap (C4-free + mindeg-3 theorem)
    cap = (n - 1) // 2
    for v in range(n):
        inc = [ev(v, u) for u in range(n) if u != v]
        cnf.extend(CardEnc.atmost(lits=inc, bound=cap, vpool=pool,
                                  encoding=EncType.seqcounter).clauses)

    s = Solver(name="cadical195", bootstrap_with=cnf)
    # random polarity nudging for diversity across seeds
    rounds = 0
    while rounds < max_rounds:
        if not s.solve():
            print(f"[n={n}] UNSAT after {rounds} refinements "
                  f"(space exhausted — would be a *proof* at this order)", flush=True)
            return 20
        model = set(l for l in s.get_model() if l > 0)
        adj = [[] for _ in range(n)]
        edges = []
        for i in range(n):
            for j in range(i + 1, n):
                if ev(i, j) in model:
                    adj[i].append(j)
                    adj[j].append(i)
                    edges.append((i, j))
        hit = find_p2_cycle(adj, n)
        if hit is None:
            g = nx.Graph()
            g.add_nodes_from(range(n))
            g.add_edges_from(edges)
            g6 = nx.to_graph6_bytes(g, header=False).decode().strip()
            print(f"*** SURVIVOR at n={n} after {rounds} refinements: {g6}", flush=True)
            print(g6)
            return 42
        L, cyc = hit
        s.add_clause([-ev(cyc[i], cyc[(i + 1) % L]) for i in range(L)])
        rounds += 1
        if rounds % 500 == 0:
            print(f"[n={n} seed={seed}] {rounds} refinements (last blocked C{L})",
                  flush=True)
    print(f"[n={n}] budget exhausted after {rounds} refinements", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
