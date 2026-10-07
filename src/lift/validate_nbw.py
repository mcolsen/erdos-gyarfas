#!/usr/bin/env python3
"""Validation battery for nbw_ref.py — the algebraic program's foundations.

V1: three independent tr(H^L) computations agree (matrix / Ihara-Bass / brute)
V2: tr(H^L) vs simple-cycle counts: tr >= 2L*#C_L, equality when 2*girth > L
V3: group axioms for the group library
V4: lift claims: |G| * NBW_id(L) == tr(H_lift^L)  (trace formula), and
    NBW_id(L) == 0  ==>  lift C_L-free  (the lift criterion), plus
    over-forbid witnesses (NBW_id > 0 but no C_L) are recorded, expected >0.
"""
import random
import sys

from nbw_ref import (Group, cyclic, dihedral, direct, sym, quaternion8,
                     hashimoto_matrix, mat_pow_trace, trace_H_ihara,
                     trace_H_brute, lift_edges, nbw_id_count,
                     cycle_count_exact, darts)

random.seed(20260727)
fails = 0


def check(label, cond, detail=""):
    global fails
    if not cond:
        fails += 1
        print(f"FAIL {label}: {detail}")
    return cond


GRAPHS = {
    "K4": (4, [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]),
    "K33": (6, [(0, 3), (0, 4), (0, 5), (1, 3), (1, 4), (1, 5),
                (2, 3), (2, 4), (2, 5)]),
    "cube": (8, [(0, 1), (0, 2), (0, 4), (1, 3), (1, 5), (2, 3), (2, 6),
                 (3, 7), (4, 5), (4, 6), (5, 7), (6, 7)]),
    "petersen": (10, [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0), (0, 5), (1, 6),
                      (2, 7), (3, 8), (4, 9), (5, 7), (7, 9), (9, 6), (6, 8),
                      (8, 5)]),
    "theta": (2, [(0, 1), (0, 1), (0, 1)]),
    "dumbbell": (2, [(0, 0), (0, 1), (1, 1)]),
    "K4loop": (4, [(0, 0), (0, 1), (1, 2), (1, 3), (2, 3), (2, 3)]),
}

# ---- V1: three-way trace agreement ----
print("== V1: tr(H^L) three ways ==")
for name, (n, edges) in GRAPHS.items():
    H = hashimoto_matrix(edges)
    for L in (1, 2, 3, 4, 5, 6, 7, 8):
        t_mat = mat_pow_trace(H, L)
        ok = True
        try:
            t_ihara = trace_H_ihara(edges, n, L)
            ok &= check(f"V1-ihara {name} L={L}", t_mat == t_ihara,
                        f"mat={t_mat} ihara={t_ihara}")
        except AssertionError:
            pass  # irregular: Ihara route skipped
        if L <= 6 and len(edges) <= 12:
            t_brute = trace_H_brute(edges, L)
            ok &= check(f"V1-brute {name} L={L}", t_mat == t_brute,
                        f"mat={t_mat} brute={t_brute}")
    print(f"  {name}: ok  (tr(H^4)={mat_pow_trace(H,4)}, tr(H^8)={mat_pow_trace(H,8)})")

# ---- V2: trace vs cycle counts ----
print("== V2: tr(H^L) vs 2L*#C_L ==")
for name, (n, edges) in GRAPHS.items():
    if any(u == v for (u, v) in edges):
        continue
    simple = len({(min(u, v), max(u, v)) for (u, v) in edges}) == len(edges)
    if not simple:
        continue
    H = hashimoto_matrix(edges)
    girth = next(L for L in range(3, 20) if cycle_count_exact(edges, n, L) > 0)
    for L in range(3, 11):
        t = mat_pow_trace(H, L)
        c = cycle_count_exact(edges, n, L)
        check(f"V2-lb {name} L={L}", t >= 2 * L * c, f"tr={t} < 2L#C={2*L*c}")
        if L < 2 * girth:
            check(f"V2-eq {name} L={L} (L<2g={2*girth})", t == 2 * L * c,
                  f"tr={t} != 2L#C={2*L*c}")
    print(f"  {name}: girth={girth} ok; e.g. tr(H^8)={mat_pow_trace(H,8)}"
          f" #C8={cycle_count_exact(edges, n, 8)}")

# ---- V3: group axioms ----
print("== V3: group library axioms ==")
for G in (cyclic(5), cyclic(12), dihedral(4), dihedral(6), quaternion8(),
          sym(3), sym(4), direct(cyclic(3), cyclic(9))):
    els = G.elements
    ok = all(G.mul(G.id, a) == a and G.mul(a, G.id) == a for a in els)
    ok &= all(G.mul(a, G.inv(a)) == G.id for a in els)
    sample = els if len(els) <= 12 else random.sample(els, 12)
    ok &= all(G.mul(G.mul(a, b), c) == G.mul(a, G.mul(b, c))
              for a in sample for b in sample for c in sample)
    # closure
    ok &= all(G.mul(a, b) in set(els) for a in sample for b in sample)
    check(f"V3 {G.name}", ok, "group axiom failure")
    print(f"  {G.name}: order {G.order} ok")

# ---- V4: lift trace formula + lift criterion ----
print("== V4: lifts ==")
BASES = {
    "theta": (2, [(0, 1), (0, 1), (0, 1)]),
    "dumbbell": (2, [(0, 0), (0, 1), (1, 1)]),
    "K4": (4, [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]),
    "K4loop": (4, [(0, 0), (0, 1), (1, 2), (1, 3), (2, 3), (2, 3)]),
}
GROUPS = [cyclic(3), cyclic(5), cyclic(6), cyclic(8), dihedral(3),
          dihedral(4), quaternion8(), sym(3), direct(cyclic(2), cyclic(4))]
overforbid = 0
tested = 0
for bname, (nb, bedges) in BASES.items():
    for G in GROUPS:
        nl = nb * G.order
        if nl > 40:
            continue
        for trial in range(6):
            volts = [random.choice(G.elements) for _ in bedges]
            le = lift_edges(bedges, volts, G)
            if le is None:
                continue
            tested += 1
            Hl = hashimoto_matrix(le)
            for L in (3, 4, 5, 6, 7, 8):
                t_lift = mat_pow_trace(Hl, L)
                cnt = nbw_id_count(bedges, volts, G, L)
                check(f"V4-tr {bname}/{G.name} L={L}", t_lift == G.order * cnt,
                      f"tr_lift={t_lift} |G|*nbw={G.order * cnt} volts={volts}")
                cl = cycle_count_exact(le, nl, L)
                if cnt == 0:
                    check(f"V4-crit {bname}/{G.name} L={L}", cl == 0,
                          f"NBW_id=0 but #C_{L}={cl} volts={volts}")
                if cnt > 0 and cl == 0:
                    overforbid += 1
print(f"  lifts tested: {tested}; over-forbid instances (NBW>0, no C_L): {overforbid}")
check("V4-overforbid-exists", overforbid > 0,
      "expected some over-forbidding — suspicious if none")

print(f"\n{'ALL CHECKS PASSED' if fails == 0 else f'{fails} FAILURES'}")
sys.exit(1 if fails else 0)
