#!/usr/bin/env python3
"""Engine validation: exhaustive small-group comparison.

For every base (k=2 and a few k=4) and every group of order 3..10, enumerate
ALL voltage configs in Python independently: build the lift explicitly,
require simple + connected (non-generating configs are skipped, mirroring
the engine's GEN rule), count C4/C8/C16 by explicit DFS on the lift.
Survivor set must EXACTLY equal the engine's SURV output.
"""
import os
import subprocess
import sys
from itertools import product as iproduct

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from groups import build_library2
from liftprep import parse_bases
from liftjob import emit_base, emit_group
from nbw_ref import cycle_count_exact

SCRATCH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENGINE = os.path.join(SCRATCH, "bin", "liftsweep")


def connected_edges(n, edges):
    parent = list(range(n))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for (u, v) in edges:
        parent[find(u)] = find(v)
    return len({find(v) for v in range(n)}) == 1


def python_survivors(b, g):
    doms = []
    for kind in b.slots:
        if kind == 'cot':
            doms.append(list(range(g.order)))
        elif kind == 'loop':
            doms.append([x for x in range(g.order)
                         if x != g.id and int(g.mul[x, x]) != g.id])
        else:
            doms.append([x for x in range(g.order)
                         if x != g.id and int(g.mul[x, x]) == g.id])
    surv = set()
    for vals in iproduct(*doms):
        le = b.lift_edges_py(g.mul, g.inv, g.id, g.order, list(vals))
        if le is None:
            continue
        nl = b.k * g.order
        if not connected_edges(nl, le):
            continue
        if cycle_count_exact(le, nl, 4):
            continue
        if cycle_count_exact(le, nl, 8):
            continue
        if cycle_count_exact(le, nl, 16):
            continue
        surv.add(tuple(vals))
    return surv


def main():
    bases = parse_bases("bases_k2.txt") + parse_bases("bases_k4.txt")[:6]
    lib = [g for g in build_library2(10) if 3 <= g.order <= 10]
    total_cfg = mismatches = 0
    for bi, b in enumerate(bases):
        for g in lib:
            # engine run (single base + single group; disable reps0 for
            # exact set comparison — orbit dedupe intentionally drops configs)
            job = f"/tmp/valjob_{os.getpid()}.txt"
            with open(job, "w") as f:
                emit_base(f, 0, b, [1, 2, 4, 8, 16])
                gsave = g.abelian
                g.abelian = False       # suppress reps0 emission
                emit_group(f, g)
                g.abelian = gsave
            out = subprocess.run([ENGINE, job], capture_output=True, text=True)
            eng = set()
            for line in out.stdout.splitlines():
                if line.startswith("SURV"):
                    vals = line.split("vals=")[1]
                    eng.add(tuple(int(x) for x in vals.split(",")))
            py = python_survivors(b, g)
            total_cfg += 1
            if eng != py:
                mismatches += 1
                print(f"MISMATCH base{bi} {g.name}: engine={len(eng)} py={len(py)}"
                      f" eng-py={sorted(eng - py)[:4]} py-eng={sorted(py - eng)[:4]}")
            os.unlink(job)
        print(f"base {bi} ({b.k}v, slots {b.slots}) done")
    print(f"validate_engine: {total_cfg} (base,group) spaces, {mismatches} mismatches")
    sys.exit(1 if mismatches else 0)


if __name__ == "__main__":
    main()
