#!/usr/bin/env python3
"""Reference (slow, exact) implementation of non-backtracking (Hashimoto) walk
machinery, for validating the algebraic program's claims.

Multigraph model: edges is a list of (u, v) pairs (parallel edges = repeated
pairs, loops = (u, u)).  Darts: edge i gives darts 2i (u->v) and 2i+1 (v->u);
rev(d) = d ^ 1.  Hashimoto transition d1 -> d2 iff head(d1) == tail(d2) and
d2 != rev(d1).  tr(H^L) counts cyclically-non-backtracking closed L-walks.

Three independent computations of tr(H^L):
  1. bigint matrix power of the explicit 2m x 2m Hashimoto matrix
  2. Ihara-Bass: tr(H^L) = (m-n)(1+(-1)^L) + tr(Q_L),
     Q_0=2I, Q_1=A, Q_L = A Q_{L-1} - (d-1) Q_{L-2}   [regular graphs only]
  3. brute-force enumeration of closed dart sequences (tiny L only)

Voltage lifts over an arbitrary finite group (elements = hashable objects with
a supplied mul/inv/id):  lift vertices (v, g); dart 2i with voltage a maps
(u, g) -> (v, g*a), dart 2i+1 carries a^{-1}.

Identity-voltage NBW count on the base: DP over (dart, group element).
Claim under test: |Gamma| * NBW_id(L) == tr(H_lift^L), and
NBW_id(L) == 0  =>  lift has no simple L-cycle.
"""
import sys
from itertools import product


# ---------- darts / Hashimoto ----------

def darts(edges):
    """Return (tail, head, rev) arrays for the 2|E| darts."""
    tail, head = [], []
    for (u, v) in edges:
        tail += [u, v]
        head += [v, u]
    return tail, head


def hashimoto_matrix(edges):
    tail, head = darts(edges)
    D = len(tail)
    H = [[0] * D for _ in range(D)]
    for d1 in range(D):
        for d2 in range(D):
            if head[d1] == tail[d2] and d2 != (d1 ^ 1):
                H[d1][d2] = 1
    return H


def mat_mul(A, B):
    n, k, m2 = len(A), len(B), len(B[0])
    Bt = list(zip(*B))
    return [[sum(a * b for a, b in zip(row, col)) for col in Bt] for row in A]


def mat_pow_trace(H, L):
    """tr(H^L) by exact bigint repeated squaring."""
    n = len(H)
    result = None
    base = [row[:] for row in H]
    e = L
    while e:
        if e & 1:
            result = base if result is None else mat_mul(result, base)
        e >>= 1
        if e:
            base = mat_mul(base, base)
    return sum(result[i][i] for i in range(n))


def trace_H_ihara(edges, n, L):
    """Ihara-Bass route, valid for d-regular multigraphs."""
    m = len(edges)
    deg = [0] * n
    for (u, v) in edges:
        deg[u] += 1
        deg[v] += 1
        if u == v:
            pass  # loop counts 2 to its endpoint; handled by the += lines
    d = deg[0]
    assert all(x == d for x in deg), "regular only"
    A = [[0] * n for _ in range(n)]
    for (u, v) in edges:
        if u == v:
            A[u][u] += 2          # loop: contributes 2 to adjacency diagonal
        else:
            A[u][v] += 1
            A[v][u] += 1
    I = [[2 if i == j else 0 for j in range(n)] for i in range(n)]
    Q_prev = I                       # Q_0 = 2I
    Q_cur = A                        # Q_1 = A
    if L == 0:
        return 2 * m
    for _ in range(L - 1):
        AQ = mat_mul(A, Q_cur)
        Q_next = [[AQ[i][j] - (d - 1) * Q_prev[i][j] for j in range(n)]
                  for i in range(n)]
        Q_prev, Q_cur = Q_cur, Q_next
    trQ = sum(Q_cur[i][i] for i in range(n))
    return (m - n) * (1 + (-1) ** L) + trQ


def trace_H_brute(edges, L):
    """Enumerate closed cyclically-NBW dart sequences (exponential; tiny only)."""
    tail, head = darts(edges)
    D = len(tail)
    succ = [[d2 for d2 in range(D) if head[d1] == tail[d2] and d2 != (d1 ^ 1)]
            for d1 in range(D)]
    count = 0
    def go(first, cur, steps):
        nonlocal count
        if steps == L:
            count += 1 if cur == first else 0
            return
        for nxt in succ[cur]:
            # prune: last step must be able to return; cheap full enumeration
            go(first, nxt, steps + 1)
    for e in range(D):
        for nxt in succ[e]:
            if L == 1:
                count += 1 if nxt == e else 0
            else:
                go(e, nxt, 1)
    # count counts walks e_1..e_L with transitions e_1->e_2..e_L->e_1:
    # loop above walks L transitions starting from e; adjust: we want closed
    # sequences of L darts.  Walk of L transitions from e returning to e ==
    # closed dart sequence of length L rooted at e.  OK.
    return count


# ---------- groups ----------

class Group:
    def __init__(self, elements, mul, inv, ident, name):
        self.elements = list(elements)
        self.mul = mul
        self.inv = inv
        self.id = ident
        self.name = name
        self.order = len(self.elements)


def cyclic(m):
    return Group(range(m), lambda a, b: (a + b) % m, lambda a: (-a) % m, 0,
                 f"Z{m}")


def direct(G1, G2):
    els = [(a, b) for a in G1.elements for b in G2.elements]
    return Group(els,
                 lambda x, y: (G1.mul(x[0], y[0]), G2.mul(x[1], y[1])),
                 lambda x: (G1.inv(x[0]), G2.inv(x[1])),
                 (G1.id, G2.id), f"{G1.name}x{G2.name}")


def dihedral(m):
    # elements (r, s): rotation r in Z_m, s in {0,1}; (r1,s1)(r2,s2) =
    # (r1 + (-1)^{s1} r2, s1+s2)
    els = [(r, s) for r in range(m) for s in range(2)]
    def mul(x, y):
        return ((x[0] + (y[0] if x[1] == 0 else -y[0])) % m, (x[1] + y[1]) % 2)
    def inv(x):
        return ((-x[0]) % m, 0) if x[1] == 0 else x
    return Group(els, mul, inv, (0, 0), f"D{m}")


def sym(k):
    from itertools import permutations
    els = list(permutations(range(k)))
    def mul(p, q):        # apply q then p?  fix: (p*q)(i) = p(q(i))
        return tuple(p[q[i]] for i in range(k))
    def inv(p):
        r = [0] * k
        for i, x in enumerate(p):
            r[x] = i
        return tuple(r)
    return Group(els, mul, inv, tuple(range(k)), f"S{k}")


def quaternion8():
    # {±1, ±i, ±j, ±k} as (sign, unit): encode 0..7 = e,i,j,k,-e,-i,-j,-k
    tbl_units = {  # unit multiplication: (a,b) -> (sign, unit)
        (0, 0): (1, 0), (0, 1): (1, 1), (0, 2): (1, 2), (0, 3): (1, 3),
        (1, 0): (1, 1), (1, 1): (-1, 0), (1, 2): (1, 3), (1, 3): (-1, 2),
        (2, 0): (1, 2), (2, 1): (-1, 3), (2, 2): (-1, 0), (2, 3): (1, 1),
        (3, 0): (1, 3), (3, 1): (1, 2), (3, 2): (-1, 1), (3, 3): (-1, 0),
    }
    def mul(x, y):
        sx, ux = (1 if x < 4 else -1), x % 4
        sy, uy = (1 if y < 4 else -1), y % 4
        s, u = tbl_units[(ux, uy)]
        s *= sx * sy
        return u if s == 1 else u + 4
    def inv(x):
        for y in range(8):
            if mul(x, y) == 0:
                return y
    return Group(range(8), mul, inv, 0, "Q8")


# ---------- lifts ----------

def lift_edges(base_edges, volts, G):
    """Voltage lift as an edge list on vertices (v, g) -> index v*|G| + gi.
    volts[i] = group element on dart 2i (u->v); dart 2i+1 gets inverse.
    Returns None if the lift is not simple (loop or parallel edge)."""
    gi = {g: i for i, g in enumerate(G.elements)}
    seen = set()
    out = []
    for (u, v), a in zip(base_edges, volts):
        for g in G.elements:
            x = u * G.order + gi[g]
            y = v * G.order + gi[G.mul(g, a)]
            if x == y:
                return None
            key = (min(x, y), max(x, y))
            if key in seen:
                return None
            seen.add(key)
            out.append((x, y))
    return out


def nbw_id_count(base_edges, volts, G, L):
    """# closed cyclically-NBW L-walks in base with identity net voltage,
    counted per starting dart (i.e., = tr(H_lift^L) / |G| if claim holds).
    DP over (dart, group element)."""
    tail, head = darts(base_edges)
    D = len(tail)
    dvolt = []
    for a in volts:
        dvolt += [a, G.inv(a)]
    succ = [[d2 for d2 in range(D) if head[d1] == tail[d2] and d2 != (d1 ^ 1)]
            for d1 in range(D)]
    total = 0
    for e in range(D):
        # start at dart e with accumulated voltage = volt(e) after traversing e
        vec = {(e, dvolt[e]): 1}
        for _ in range(L - 1):
            new = {}
            for (d, g), c in vec.items():
                for d2 in succ[d]:
                    key = (d2, G.mul(g, dvolt[d2]))
                    new[key] = new.get(key, 0) + c
            vec = new
        # close: walk of L darts e=e_1,...,e_L needs transition e_L -> e_1
        for (d, g), c in vec.items():
            if g == G.id and e in succ[d]:
                total += c
    return total


# ---------- simple-cycle spectrum of an edge list (small graphs) ----------

def cycle_count_exact(edges, n, L):
    """# simple cycles of length L (each counted once).  Small graphs only."""
    adj = [set() for _ in range(n)]
    for (u, v) in edges:
        adj[u].add(v)
        adj[v].add(u)
    count = 0
    def dfs(s, u, depth, visited):
        nonlocal count
        if depth == L - 1:
            if s in adj[u]:
                count += 1
            return
        for w in adj[u]:
            if w > s and w not in visited:
                visited.add(w)
                dfs(s, w, depth + 1, visited)
                visited.remove(w)
    for s in range(n):
        for w in adj[s]:
            if w > s:
                dfs(s, w, 1, {w})
    return count // 2   # each cycle found twice (two directions)


if __name__ == "__main__":
    print("nbw_ref: library module; run validate_nbw.py")
