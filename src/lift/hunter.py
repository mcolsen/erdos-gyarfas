#!/usr/bin/env python3
"""Abelian trace-hole hunter over 2-vertex semi-bases.

Reads windhunt dump (winding vectors of ALL closed cyclically-NBW L-walks).
For abelian A = Z_{m1} x ... x Z_{mk} and slot values t_i in A (semi slots:
involutions), the lift has tr(H^L) = 0  iff  sum_i c_i * t_i != 0 in A for
every dumped winding c.  tr(H^L)=0 at L in {16,32} forces simplicity and
{4,8,16(,32)}-freeness automatically (d | L repetitions).

Every hit is verified end-to-end when n is small enough: build the lift,
nbwtrace must report tr(H^L) = 0, cycscan must report no C4/C8/C16.

Usage:
  hunter.py <dumpfile> <base-id> <L> <nmin> <nmax> [--verify-limit N]
Bases (slot order as in windhunt = liftprep):
  2 loopsemi: slots (loop, semi, semi@same vertex)  -> semis must differ
  3 semis4:   slots (semi,semi @u, semi,semi @v)
  4 dubsemi:  slots (cot-edge, semi@u, semi@v)
A-shapes tried: Z_m; Z2 x Z_m; Z2 x Z2 x Z_m; Z4 x Z_m  (|A| = n/2).
"""
import os
import subprocess
import sys
from itertools import product as iproduct

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

SCRATCH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASETUP = {
    2: (2, ((0, 1),), (1,), (0, 0)),
    3: (2, ((0, 1),), (), (0, 0, 1, 1)),
    4: (2, ((0, 1), (0, 1)), (), (0, 1)),
}


def involutions(shape):
    out = []
    for t in iproduct(*[range(m) for m in shape]):
        if any(t) and all((2 * x) % m == 0 for x, m in zip(t, shape)):
            out.append(t)
    return out


def elements(shape):
    return list(iproduct(*[range(m) for m in shape]))


def test(cs, ts, shape):
    """True iff every winding c has sum_i c_i t_i != 0 in A."""
    for c in cs:
        acc = [0] * len(shape)
        for ci, t in zip(c, ts):
            if ci:
                for j, (x, m) in enumerate(zip(t, shape)):
                    acc[j] = (acc[j] + ci * x) % m
        if not any(acc):
            return False
    return True


def verify_hit(baseid, shape, ts, L, do_build):
    if not do_build:
        return "unverified(n too big for direct trace)"
    from liftprep import Base
    from groups import abelian_group
    b = Base(*BASETUP[baseid])
    g = abelian_group(list(shape))
    ei = {e: i for i, e in enumerate(g_elements_order(g))}
    # abelian_group elements are tuples in iproduct order; map ts to ids
    idx = {tuple(e): i for i, e in enumerate(g.elements_list)} if hasattr(g, "elements_list") else None
    # groups.G stores mult table only; rebuild element list the same way
    els = elements(shape)
    eidx = {e: i for i, e in enumerate(els)}
    vals = [eidx[tuple(t)] for t in ts]
    le = b.lift_edges_py(g.mul, g.inv, g.id, g.order, vals)
    if le is None:
        return "FAIL: non-simple (should be impossible)"
    n = 2 * g.order
    # connectivity
    parent = list(range(n))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for (u, v) in le:
        parent[find(u)] = find(v)
    ncomp = len({find(v) for v in range(n)})
    from liftpost import to_g6
    g6 = to_g6(n, set(le))
    r = subprocess.run([f"{SCRATCH}/bin/nbwtrace", "-L", f"8,16,{L}"],
                       input=g6 + "\n", capture_output=True, text=True)
    tr = r.stdout.split("g6=")[0].strip()
    r2 = subprocess.run([f"{SCRATCH}/bin/cycscan", "-F", "4,8,16"],
                        input=g6 + "\n", capture_output=True, text=True)
    cyc = r2.stdout.split("g6=")[0].strip()
    return f"ncomp={ncomp} {tr} {cyc}", g6


def g_elements_order(g):
    return list(range(g.order))


def main():
    dumpfile, baseid, L, nmin, nmax = (sys.argv[1], int(sys.argv[2]),
                                       int(sys.argv[3]), int(sys.argv[4]),
                                       int(sys.argv[5]))
    vlimit = 2000
    if "--verify-limit" in sys.argv:
        vlimit = int(sys.argv[sys.argv.index("--verify-limit") + 1])
    cs = []
    for line in open(dumpfile):
        if line.startswith("c "):
            parts = line.split()
            r = parts.index("mult") - 1
            cs.append(tuple(int(x) for x in parts[1:1 + r]))
    print(f"{len(cs)} winding vectors loaded")
    b = BASETUP[baseid]
    nslots = (len(b[1]) - 1) + len(b[2]) + len(b[3])  # cotree + loops + semis
    kinds = (["cot"] * (len(b[1]) - 1) + ["loop"] * len(b[2])
             + ["semi"] * len(b[3]))
    hits = 0
    for half in range(nmin // 2, nmax // 2 + 1):
        shapes = [(half,)]
        if half % 2 == 0:
            shapes.append((2, half // 2))
            if (half // 2) % 2 == 0:
                shapes.append((2, 2, half // 4))
                shapes.append((4, half // 4))
        for shape in shapes:
            els = elements(shape)
            invs = involutions(shape)
            doms = []
            feasible = True
            for kind in kinds:
                if kind == "cot":
                    doms.append(els)
                elif kind == "loop":
                    doms.append(els)          # winding test filters bad loops
                else:
                    if not invs:
                        feasible = False
                        break
                    doms.append(invs)
            if not feasible:
                continue
            for ts in iproduct(*doms):
                if test(cs, ts, shape):
                    hits += 1
                    n = 2 * len(els)
                    msg = f"HIT base={baseid} L={L} A={'x'.join(f'Z{m}' for m in shape)} n={n} t={ts}"
                    if n <= vlimit:
                        v = verify_hit(baseid, shape, ts, L, True)
                        msg += f"  VERIFY: {v[0] if isinstance(v, tuple) else v}"
                        if isinstance(v, tuple):
                            with open(f"{SCRATCH}/runs/tracehole_hits.g6", "a") as f:
                                f.write(v[1] + "\n")
                    print(msg, flush=True)
                    if hits > 60:
                        print("(hit cap reached, stopping)")
                        return
    print(f"hunter: {hits} hits in n=[{nmin},{nmax}]")


if __name__ == "__main__":
    main()
