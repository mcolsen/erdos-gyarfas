#!/usr/bin/env python3
"""Per-base preprocessing for the lift sweep.

Dart model: proper edge {u,v} -> two darts d (u->v), rev d (v->u), one shared
slot (voltage t on the u->v dart; inverse on reverse).  Loop at v -> two darts
both v->v, rev-paired, slot t on the "forward" dart (t on one dart, t^-1 on
its partner).  Semi-edge at v -> ONE dart v->v with rev(d) = d, slot value
must be an involution != id.

Slots: spanning tree (proper edges) fixed to identity (gauge); free slots =
cotree proper edges + loops + semis.  Static domains:
  proper cotree: all of Gamma;  loop: t != id, t^2 != id;  semi: t^2=id, t!=id.

Words: all cyclically-non-backtracking closed L-walks of the base, one per
cyclic/reversal class, encoded as per-step tokens: 2*slot+0 (forward),
2*slot+1 (inverse), or 255 (tree dart, identity).  Per word also the list of
index pairs (i, j), 0 <= i < j < L, with equal base vertices v_i == v_j
(for the degeneracy = simple-cycle test in the lift).

Emits a text job file per base consumed by liftsweep.c, plus a Python-side
mirror used for validation.
"""
import sys
from itertools import product as iproduct

sys.setrecursionlimit(100000)


class Base:
    def __init__(self, k, edges, loops, semis):
        self.k, self.edges, self.loops, self.semis = k, list(edges), list(loops), list(semis)
        # build darts
        self.dtail, self.dhead, self.drev = [], [], []
        self.dslot, self.dsign = [], []   # slot id, +1/-1 (semi: +1)
        self.slot_kind = []               # per slot: 'tree','cot','loop','semi'
        # spanning tree over proper edges (first-found BFS forest)
        adj = {}
        for i, (u, v) in enumerate(self.edges):
            adj.setdefault(u, []).append((v, i))
            adj.setdefault(v, []).append((u, i))
        tree_idx = set()
        seen = {0}
        frontier = [0]
        while frontier:
            u = frontier.pop()
            for (w, i) in adj.get(u, []):
                if w not in seen and i not in tree_idx:
                    tree_idx.add(i)
                    seen.add(w)
                    frontier.append(w)
        assert seen == set(range(self.k)), "base not connected via proper edges+loops?"
        nslot = 0
        self.slots = []
        for i, (u, v) in enumerate(self.edges):
            if i in tree_idx:
                s, kind = None, 'tree'
            else:
                s, kind = nslot, 'cot'
                nslot += 1
                self.slots.append(kind)
            d = len(self.dtail)
            self.dtail += [u, v]
            self.dhead += [v, u]
            self.drev += [d + 1, d]
            self.dslot += [s, s]
            self.dsign += [+1, -1]
        for v in self.loops:
            s = nslot
            nslot += 1
            self.slots.append('loop')
            d = len(self.dtail)
            self.dtail += [v, v]
            self.dhead += [v, v]
            self.drev += [d + 1, d]
            self.dslot += [s, s]
            self.dsign += [+1, -1]
        for v in self.semis:
            s = nslot
            nslot += 1
            self.slots.append('semi')
            d = len(self.dtail)
            self.dtail += [v]
            self.dhead += [v]
            self.drev += [d]
            self.dslot += [s]
            self.dsign += [+1]
        self.nd = len(self.dtail)
        self.nslot = nslot
        self.succ = [[e for e in range(self.nd)
                      if self.dtail[e] == self.dhead[d] and e != self.drev[d]]
                     for d in range(self.nd)]

    def closed_nbw_words(self, L):
        """One representative per cyclic/reversal class of closed cyclic-NBW
        L-walks.  Returns list of (tokens, vpairs)."""
        classes = {}
        def canon(seq):
            best = None
            for rev in (False, True):
                s = seq if not rev else tuple(self.drev[d] for d in reversed(seq))
                for r in range(L):
                    rot = s[r:] + s[:r]
                    if best is None or rot < best:
                        best = rot
            return best
        path = []
        def dfs(d):
            path.append(d)
            if len(path) == L:
                # closure: transition path[-1] -> path[0] must be legal
                if path[0] in self.succ[path[-1]]:
                    key = canon(tuple(path))
                    if key not in classes:
                        classes[key] = tuple(path)
                path.pop()
                return
            for e in self.succ[d]:
                dfs(e)
            path.pop()
        for d0 in range(self.nd):
            dfs(d0)
        out = []
        for seq in classes.values():
            tokens = []
            for d in seq:
                s = self.dslot[d]
                if s is None:
                    tokens.append(255)
                else:
                    tokens.append(2 * s + (0 if self.dsign[d] > 0 else 1))
            verts = [self.dtail[seq[0]]]
            for d in seq:
                verts.append(self.dhead[d])
            vpairs = [(i, j) for i in range(L) for j in range(i + 1, L)
                      if verts[i] == verts[j]]
            out.append((tokens, vpairs))
        return out

    def lift_edges_py(self, table, inv, ident, order, vals):
        """Build lift edge list; None if not simple.  vals: per-slot element."""
        def slotval(d):
            s = self.dslot[d]
            if s is None:
                return ident
            v = vals[s]
            return v if self.dsign[d] > 0 else int(inv[v])
        seen = set()
        out = []
        for d in range(self.nd):
            if self.drev[d] < d:
                continue          # one per edge (semi: drev==d included once)
            a = slotval(d)
            u, v = self.dtail[d], self.dhead[d]
            for g in range(order):
                x, y = u * order + g, v * order + int(table[g][a])
                if x == y:
                    return None
                key = (min(x, y), max(x, y))
                if key in seen:
                    return None
                seen.add(key)
                out.append((x, y))
        return out


def parse_bases(path):
    out = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line.startswith("("):
                k, edges, loops, semis = eval(line)
                out.append(Base(k, edges, loops, semis))
    return out


if __name__ == "__main__":
    bases = parse_bases(sys.argv[1])
    Ls = [1, 2, 4, 8]
    for bi, b in enumerate(bases):
        counts = {L: len(b.closed_nbw_words(L)) for L in Ls}
        print(f"base {bi}: k={b.k} slots={b.nslot} ({b.slots}) words={counts}")
