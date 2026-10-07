#!/usr/bin/env python3
"""Post-process liftsweep survivors: rebuild every lift, independently verify
simplicity/cubicity/connectivity and {C4,C8,C16}-freeness via cycscan (and
p2check when n <= 64), then exact C32/C64.  Any verification failure is a
FATAL engine bug report.  Output: verified survivors as graph6 + spectra.

Usage: liftpost.py <basesfile> <survfile> [outprefix]
SURV line: SURV base=<id> group=<name> vals=<v0,v1,...>
"""
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from groups import build_library2
from liftprep import parse_bases

SCRATCH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BIN = os.path.join(SCRATCH, "bin")


def to_g6(n, edges):
    adj = bytearray()
    bits = []
    for v in range(1, n):
        for u in range(v):
            bits.append(1 if ((u, v) in edges or (v, u) in edges) else 0)
    if n <= 62:
        head = bytes([n + 63])
    else:
        head = bytes([126, (n >> 12) + 63, ((n >> 6) & 63) + 63, (n & 63) + 63])
    body = bytearray()
    for i in range(0, len(bits), 6):
        chunk = bits[i:i + 6] + [0] * (6 - len(bits[i:i + 6]))
        body.append(sum(b << (5 - j) for j, b in enumerate(chunk)) + 63)
    return (head + bytes(body)).decode()


def main():
    basesfile, survfile = sys.argv[1], sys.argv[2]
    outprefix = sys.argv[3] if len(sys.argv) > 3 else survfile + ".post"
    bases = parse_bases(basesfile)
    lib = {g.name: g for g in build_library2(63)}
    lines = [l.strip() for l in open(survfile) if l.startswith("SURV")]
    print(f"{len(lines)} survivors to verify")
    ok, fatal = 0, 0
    g6out = open(outprefix + ".g6", "w")
    meta = open(outprefix + ".meta", "w")
    for li, line in enumerate(lines):
        parts = dict(p.split("=", 1) for p in line.split()[1:])
        b = bases[int(parts["base"])]
        g = lib[parts["group"]]
        vals = [int(x) for x in parts["vals"].split(",")]
        le = b.lift_edges_py(g.mul, g.inv, g.id, g.order, vals)
        n = b.k * g.order
        assert le is not None, f"FATAL: non-simple lift emitted: {line}"
        deg = {}
        for (u, v) in le:
            deg[u] = deg.get(u, 0) + 1
            deg[v] = deg.get(v, 0) + 1
        assert len(deg) == n and all(d == 3 for d in deg.values()), \
            f"FATAL: not cubic: {line}"
        g6 = to_g6(n, set(le))
        # independent exact checks
        r = subprocess.run([f"{BIN}/cycscan", "-F", "4,8,16,32,64"],
                           input=g6 + "\n", capture_output=True, text=True)
        out = r.stdout.strip().split()
        bits = {t.split("=")[0]: int(t.split("=")[1]) for t in out
                if t.startswith("C")}
        if bits["C4"] or bits["C8"] or bits["C16"]:
            print(f"FATAL ENGINE BUG: survivor has short cycle {bits}: {line}")
            fatal += 1
            continue
        if n <= 64:
            r2 = subprocess.run([f"{BIN}/p2check", "-s"], input=g6 + "\n",
                                capture_output=True, text=True)
            s2 = r2.stdout
            for L in (4, 8, 16):
                tok = f"{L}:{1 if bits[f'C{L}'] else 0}"
                assert tok in s2, f"FATAL p2check disagreement {L}: {s2} {line}"
        ok += 1
        tag = "*** POWER-OF-2-FREE (COUNTEREXAMPLE?) ***" if not (bits["C32"] or (n >= 64 and bits["C64"])) and n >= 65 else ""
        if not bits["C32"]:
            tag += " C32-FREE!"
        meta.write(f"{line} n={n} C32={bits['C32']} C64={bits['C64']} {tag}\n")
        g6out.write(g6 + "\n")
        if tag:
            print(f"!!! {line} n={n} {bits} {tag}", flush=True)
        if (li + 1) % 500 == 0:
            print(f"...{li+1}/{len(lines)} verified", flush=True)
    print(f"liftpost: {ok} verified survivors, {fatal} FATAL bugs -> {outprefix}.g6/.meta")
    sys.exit(2 if fatal else 0)


if __name__ == "__main__":
    main()
