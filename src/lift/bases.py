#!/usr/bin/env python3
"""Enumerate connected cubic multigraphs (loops + semi-edges allowed) on k
vertices, up to isomorphism.  Base = (k, edges, loops, semis) where
edges = sorted list of (u,v) u<v proper edges (with multiplicity),
loops = sorted list of vertices (loop each, contributes degree 2, max 1/vertex),
semis = sorted list of vertices (semi-edge each, degree 1, up to 3/vertex).

Isomorphism: brute-force canonical form over all k! permutations (k <= 8).
Validated: k=2 must give exactly 5 bases (theta; dumbbell; loop-bridge-2semi;
2semi-bridge-2semi; double-edge+semi at each).
"""
from itertools import permutations, combinations_with_replacement
import sys


def canonical(k, edges, loops, semis):
    best = None
    for p in permutations(range(k)):
        e2 = tuple(sorted(tuple(sorted((p[u], p[v]))) for (u, v) in edges))
        l2 = tuple(sorted(p[v] for v in loops))
        s2 = tuple(sorted(p[v] for v in semis))
        key = (e2, l2, s2)
        if best is None or key < best:
            best = key
    return best


def connected(k, edges, loops):
    if k == 1:
        return True
    parent = list(range(k))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for (u, v) in edges:
        ru, rv = find(u), find(v)
        if ru != rv:
            parent[ru] = rv
    return len({find(v) for v in range(k)}) == 1


def enumerate_bases(k, allow_semis=True):
    """All connected cubic (deg=3) multigraphs on k vertices up to iso."""
    seen = set()
    out = []
    # choose loops l_v in {0,1}, semis s_v in {0..3}; residual r_v = 3-2l-s
    # filled by proper edges; enumerate symmetric multiplicity matrices.
    def gen_matrices(res, pairs, idx, cur):
        if idx == len(pairs):
            if all(r == 0 for r in res):
                yield tuple(cur)
            return
        (u, v) = pairs[idx]
        maxm = min(res[u], res[v], 3)
        # prune: remaining pairs must be able to absorb residuals
        for mult in range(maxm + 1):
            res[u] -= mult
            res[v] -= mult
            # feasibility: each residual must be fillable by later pairs
            later = [p for p in pairs[idx + 1:]]
            feas = True
            for w in range(len(res)):
                if res[w] > 0 and not any(w in p for p in later):
                    feas = False
                    break
            if feas:
                yield from gen_matrices(res, pairs, idx + 1, cur + [mult] * 0 + [( (u, v), mult )])
            res[u] += mult
            res[v] += mult

    pairs = list(combinations_with_replacement(range(k), 2))
    pairs = [(u, v) for (u, v) in pairs if u < v]
    smax = 3 if allow_semis else 0
    from itertools import product as iproduct
    for lo in iproduct((0, 1), repeat=k):
        for se in iproduct(range(smax + 1), repeat=k):
            res = [3 - 2 * lo[v] - se[v] for v in range(k)]
            if any(r < 0 for r in res):
                continue
            if sum(res) % 2:
                continue
            for mat in gen_matrices(res, pairs, 0, []):
                edges = []
                for ((u, v), mult) in mat:
                    edges += [(u, v)] * mult
                loops = [v for v in range(k) if lo[v]]
                semis = []
                for v in range(k):
                    semis += [v] * se[v]
                if not connected(k, edges + [(v, v) for v in loops], loops):
                    continue
                key = canonical(k, edges, loops, semis)
                if key in seen:
                    continue
                seen.add(key)
                out.append((k, tuple(edges), tuple(loops), tuple(semis)))
    return out


if __name__ == "__main__":
    k = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    allow = "--nosemi" not in sys.argv
    bases = enumerate_bases(k, allow)
    for b in bases:
        print(b)
    print(f"k={k} semis={allow}: {len(bases)} bases", file=sys.stderr)
