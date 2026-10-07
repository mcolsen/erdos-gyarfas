#!/usr/bin/env python3
"""Emit liftsweep job files (one per base: words + all groups in the order
window), and helpers shared with validation.

Usage: liftjob.py <basesfile> <omin> <omax> <outdir> [--levels 1,2,4,8,16]
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from groups import build_library2
from liftprep import Base, parse_bases


def subgroups(g):
    """All subgroups as frozensets of element ids (order <= 63: closure BFS)."""
    def closure(seed):
        s = set(seed) | {g.id}
        frontier = list(s)
        while frontier:
            new = []
            for a in list(s):
                for b in frontier:
                    for x in (int(g.mul[a, b]), int(g.mul[b, a])):
                        if x not in s:
                            s.add(x)
                            new.append(x)
            frontier = new
        return frozenset(s)
    subs = {closure([e]) for e in range(g.order)}
    changed = True
    while changed:
        changed = False
        cur = list(subs)
        for i in range(len(cur)):
            for j in range(i + 1, len(cur)):
                u = closure(cur[i] | cur[j])
                if u not in subs and len(u) < g.order:
                    subs.add(u)
                    changed = True
    subs = {s for s in subs if len(s) < g.order}
    return subs


def maximal_subgroups(g):
    subs = subgroups(g)
    return [s for s in subs
            if not any(s < t for t in subs if t != s)]


def abelian_orbit_reps(g):
    """Aut-orbit representatives of elements of an abelian group:
    invariant = (element order, divisibility profile)."""
    assert g.abelian
    o = g.order
    # d*A images for d = 1..exponent
    expo = int(max(g.eord))
    img = {}
    for d in range(1, expo + 1):
        im = set()
        for x in range(o):
            y, p = g.id, x
            for _ in range(d):
                y = int(g.mul[y, x])
            im.add(y)
        img[d] = im
    keys = {}
    for x in range(o):
        key = (int(g.eord[x]), tuple(x in img[d] for d in range(1, expo + 1)))
        keys.setdefault(key, x)
    return sorted(keys.values())


def emit_group(f, g):
    f.write(f"group {g.name} {g.order}\n")
    f.write("mul " + " ".join(str(int(x)) for x in g.mul.flatten()) + "\n")
    f.write("inv " + " ".join(str(int(x)) for x in g.inv) + "\n")
    maxs = maximal_subgroups(g)
    maxs = maxs[:32]
    masks = [0] * g.order
    for mi, s in enumerate(maxs):
        for e in s:
            masks[e] |= (1 << mi)
    f.write(f"gensets {len(maxs)} " + " ".join(map(str, masks)) + "\n")
    if g.abelian:
        reps = abelian_orbit_reps(g)
        f.write(f"reps0 {len(reps)} " + " ".join(map(str, reps)) + "\n")
    else:
        f.write("reps0 0\n")
    f.write("run\n")


def emit_base(f, bid, b, levels):
    f.write(f"base {bid} {b.nslot} " +
            "".join({'cot': 'c', 'loop': 'l', 'semi': 's'}[k] for k in b.slots) + "\n")
    for L in levels:
        words = b.closed_nbw_words(L)
        f.write(f"words {L} {len(words)}\n")
        for (tokens, vpairs) in words:
            f.write("w " + " ".join(map(str, tokens)) + f" {len(vpairs)} " +
                    " ".join(f"{i} {j}" for (i, j) in vpairs) + "\n")


def main():
    mode = sys.argv[1]
    if mode == "groups":
        omin, omax, outpath = int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
        lib = [g for g in build_library2(63) if omin <= g.order <= omax]
        with open(outpath, "w") as f:
            for g in lib:
                emit_group(f, g)
        print(f"groups {omin}..{omax}: {len(lib)} -> {outpath}")
    elif mode == "bases":
        basesfile, outdir = sys.argv[2], sys.argv[3]
        levels = [1, 2, 4, 8, 16]
        os.makedirs(outdir, exist_ok=True)
        bases = parse_bases(basesfile)
        for bid, b in enumerate(bases):
            with open(os.path.join(outdir, f"base_{bid:04d}.txt"), "w") as f:
                emit_base(f, bid, b, levels)
            print(f"base {bid} done ({b.nslot} slots)", flush=True)
        print(f"emitted {len(bases)} base files to {outdir}")


if __name__ == "__main__":
    main()
