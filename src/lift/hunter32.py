#!/usr/bin/env python3
"""Trace-32-hole hunter at scale: abelian A = P x Z_k with small 2-group
prefix P (trivial, Z2, Z2^2, Z4) and big cyclic part Z_k.

Slots: FREE slots (cot edges / loops) take any (p, x) in P x Z_k; SEMI slots
take involutions.  For fixed base, winding list C, prefix P, semi values, and
free-slot prefix parts, the surviving windings (those whose P-component sum
is 0) impose congruences  sum_i c_i x_i != -b_c (mod k)  on the free Z_k
parts x_i.  With ONE free slot (all our bases) each surviving winding c
forbids an arithmetic progression of x values: c0*x = -b_c (mod k) has
solutions iff g = gcd(c0,k) | b_c, forbidden x = x0 + (k/g)*Z, g values.
Hit iff the union of forbidden sets != Z_k.  Cost per k: O(sum g) marks.

Usage: hunter32.py <dump> <baseid> <L> <nmin> <nmax>
Base slot orders (windhunt): 2 loopsemi (loop,s,s) | 3 semis4 (s,s,s,s)
| 4 dubsemi (e,s,s).  Free slot = slot 0 for bases 2,4; none for base 3.
Semi Z_k-parts are 0 or k/2 (k even); handled as extra b-contributions.
"""
import sys
from itertools import product as iproduct

import numpy as np


def involutions_prefix(P):
    """involutions (incl 0) of prefix group P (tuple of factor sizes)."""
    els = list(iproduct(*[range(m) for m in P]))
    return [e for e in els if all((2 * x) % m == 0 for x, m in zip(e, P))]


def main():
    dump, baseid, L, nmin, nmax = (sys.argv[1], int(sys.argv[2]),
                                   int(sys.argv[3]), int(sys.argv[4]),
                                   int(sys.argv[5]))
    C = []
    for line in open(dump):
        if line.startswith("c "):
            p = line.split()
            C.append(tuple(int(x) for x in p[1:p.index("mult")]))
    C = np.array(C, dtype=np.int64)
    nslots = C.shape[1]
    if baseid in (2, 4):
        free_slots = [0]
        semi_slots = list(range(1, nslots))
    else:
        free_slots = []
        semi_slots = list(range(nslots))
    print(f"base {baseid}: {len(C)} windings, slots={nslots} "
          f"free={free_slots} semi={semi_slots}")
    PREFIXES = [(), (2,), (2, 2), (4,)]
    hits = []
    for half in range(nmin // 2, nmax // 2 + 1):
        for P in PREFIXES:
            psize = 1
            for m in P:
                psize *= m
            if half % psize:
                continue
            k = half // psize
            if k < 3:
                continue
            # semi values: (prefix-involution, kpart in {0, k/2 if k even})
            pinv = involutions_prefix(P)
            kparts = [0] + ([k // 2] if k % 2 == 0 else [])
            semivals = [(pi, kp) for pi in pinv for kp in kparts
                        if any(pi) or kp]
            if len(semivals) < 1:
                continue
            for svals in iproduct(semivals, repeat=len(semi_slots)):
                # free slot prefix part
                pels = list(iproduct(*[range(m) for m in P])) or [()]
                for fp in (pels if free_slots else [()]):
                    # compute per winding: prefix component sum and k-part b
                    # prefix sum: c_free*fp + sum c_semi*sv_prefix  (mod P)
                    # k-part b: sum c_semi*sv_kpart  (mod k)
                    ok_prefix = np.zeros(len(C), dtype=bool)
                    for j, m in enumerate(P):
                        acc = np.zeros(len(C), dtype=np.int64)
                        if free_slots:
                            acc += C[:, free_slots[0]] * fp[j]
                        for s, sv in zip(semi_slots, svals):
                            acc += C[:, s] * sv[0][j]
                        ok_prefix |= (acc % m) != 0
                    b = np.zeros(len(C), dtype=np.int64)
                    for s, sv in zip(semi_slots, svals):
                        b += C[:, s] * sv[1]
                    b %= k
                    # windings with nonzero prefix component: satisfied.
                    # rest: need c_free * x + b != 0 mod k  (x = free k-part)
                    live = ~ok_prefix
                    if not free_slots:
                        if np.any(live & (b == 0)):
                            break  # some winding identically zero: dead
                        hits.append((2 * half, P, k, svals, None))
                        continue
                    cf = C[live][:, free_slots[0]] % k
                    bl = b[live]
                    # cf*x == -bl (mod k) forbidden
                    forb = np.zeros(k, dtype=bool)
                    dead = False
                    for cfi, bi in zip(cf.tolist(), bl.tolist()):
                        g = int(np.gcd(cfi, k))
                        rhs = (-bi) % k
                        if cfi == 0:
                            if rhs == 0:
                                dead = True
                                break
                            continue
                        if rhs % g:
                            continue
                        step = k // g
                        x0 = (pow(int(cfi) // g, -1, step) * (rhs // g)) % step
                        forb[x0::step] = True
                    if dead:
                        continue
                    freex = np.flatnonzero(~forb)
                    if len(freex):
                        hits.append((2 * half, P, k, svals, int(freex[0])))
        if hits:
            for h in hits:
                print("HIT", h, flush=True)
            print(f"first hits at n={hits[0][0]}; stopping scan")
            return
        if (half * 2) % 5000 < 2:
            print(f"...scanned to n={2*half}", flush=True)
    print("hunter32: no hits in range")


if __name__ == "__main__":
    main()
