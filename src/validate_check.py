#!/usr/bin/env python3
"""Validation battery for p2check + geng_p2.

Phase 1: ALL graphs on 4..8 vertices (via plain geng): compare p2check -s
         against an independent brute force (enumerate L-subsets and circular
         orderings; algorithmically unrelated to the DFS in p2check).
Phase 2: named graphs with known structure; also runs p2check -M so the DFS
         and meet-in-the-middle detectors must agree at L in {16,32}.
Phase 3: cross-tool agreement on C4 detection: nauty's geng -f count vs
         p2check filtering of the unrestricted stream.

Usage: validate_check.py NAUTYDIR BINDIR
"""
import itertools
import subprocess
import sys
import tempfile

import networkx as nx

NAUTY, BIN = sys.argv[1], sys.argv[2]


def g6(g):
    return nx.to_graph6_bytes(g, header=False).decode().strip()


def brute_has_cycle(g, L):
    """Independent logic: choose L vertices, try circular orders."""
    nodes = list(g.nodes())
    if L > len(nodes):
        return False
    adj = {v: set(g[v]) for v in nodes}
    for sub in itertools.combinations(nodes, L):
        first = sub[0]
        rest = sub[1:]
        for perm in itertools.permutations(rest):
            if perm[0] > perm[-1]:      # halve: fix direction
                continue
            cyc = (first,) + perm
            if all(cyc[(i + 1) % L] in adj[cyc[i]] for i in range(L)):
                return True
    return False


def run_p2check(lines, args):
    p = subprocess.run([f"{BIN}/p2check"] + args, input="\n".join(lines) + "\n",
                       capture_output=True, text=True)
    if p.returncode != 0:
        print(p.stderr)
        raise SystemExit(f"p2check failed rc={p.returncode}")
    return p


def parse_spectrum(out):
    res = []
    for ln in out.splitlines():
        head, _, tail = ln.partition(":")
        d = {}
        for tok in tail.split():
            L, v = tok.split(":")
            d[int(L)] = int(v)
        res.append(d)
    return res


fails = 0

# ---------- Phase 1 ----------
print("== Phase 1: all graphs n=4..8 vs independent brute force ==")
for n in range(4, 9):
    p = subprocess.run([f"{NAUTY}/geng", "-q", str(n)], capture_output=True, text=True)
    lines = [l for l in p.stdout.splitlines() if l.strip()]
    spec = parse_spectrum(run_p2check(lines, ["-s"]).stdout)
    assert len(spec) == len(lines)
    bad = 0
    for line, sp in zip(lines, spec):
        g = nx.from_graph6_bytes(line.encode())
        for L in [4, 8]:
            if L <= n:
                truth = brute_has_cycle(g, L)
                if truth != bool(sp.get(L)):
                    bad += 1
                    print(f"  MISMATCH n={n} L={L} {line}: brute={truth} p2check={sp.get(L)}")
    print(f"  n={n}: {len(lines)} graphs checked, {bad} mismatches")
    fails += bad

# ---------- Phase 2 ----------
print("== Phase 2: named graphs (with -M internal DFS/MITM cross-check) ==")
named = []
named.append(("Petersen", nx.petersen_graph(), {4: 0, 8: 1}))
named.append(("Heawood", nx.heawood_graph(), {4: 0, 8: 1}))       # girth 6; C8 known present
named.append(("McGee[LCF]", nx.LCF_graph(24, [12, 7, -7], 8), {4: 0}))
named.append(("Pappus", nx.pappus_graph(), {4: 0}))
named.append(("Desargues", nx.desargues_graph(), {4: 0}))
named.append(("MoebiusKantor", nx.moebius_kantor_graph(), {4: 0}))
named.append(("TutteCoxeter[LCF]", nx.LCF_graph(30, [-13, -9, 7, -7, 9, 13], 5), {4: 0, 8: 1}))  # girth 8
named.append(("Dodecahedron", nx.dodecahedral_graph(), {4: 0, 8: 1}))  # girth 5; two adjacent faces bound a C8
named.append(("C16", nx.cycle_graph(16), {4: 0, 8: 0, 16: 1}))
named.append(("C16+chord(0-8)", nx.cycle_graph(16), None))
named[-1][1].add_edge(0, 8)
named.append(("Q4 hypercube", nx.hypercube_graph(4), {4: 1, 8: 1, 16: 1}))
named.append(("K9", nx.complete_graph(9), {4: 1, 8: 1}))
named.append(("K4,4", nx.complete_bipartite_graph(4, 4), {4: 1, 8: 1}))

lines = [g6(nx.convert_node_labels_to_integers(g)) for _, g, _ in named]
spec = parse_spectrum(run_p2check(lines, ["-s", "-M"]).stdout)
for (name, g, expect), sp in zip(named, spec):
    show = " ".join(f"C{L}={v}" for L, v in sorted(sp.items()))
    ok = True
    if expect:
        for L, v in expect.items():
            if sp.get(L) != v:
                ok = False
    print(f"  {name:22s} {show}  {'OK' if ok else '*** UNEXPECTED ***'}")
    if not ok:
        fails += 1

# ---------- Phase 3 ----------
print("== Phase 3: C4 agreement with nauty's geng -f at n=10 (min degree 3) ==")


def geng_count(flags):
    p = subprocess.run([f"{NAUTY}/geng", "-u"] + flags, capture_output=True, text=True)
    return int([l for l in p.stderr.splitlines() if "graphs generated" in l][0].split()[1])


nauty_count = geng_count(["-d3", "-f", "10"])
p = subprocess.run(f"{NAUTY}/geng -q -d3 10 | {BIN}/p2check -F 4",
                   shell=True, capture_output=True, text=True)
mine = int([l for l in p.stderr.splitlines() if "passed=" in l][0].split("passed=")[1])
print(f"  geng -f count = {nauty_count}; p2check C4-filter of full stream = {mine}"
      f"  {'OK' if nauty_count == mine else '*** MISMATCH ***'}")
if nauty_count != mine:
    fails += 1
print(f"  [anchor] C4-free min-deg-3 graphs on 10 vertices: all={nauty_count}, "
      f"connected={geng_count(['-c', '-d3', '-f', '10'])} (Balaji's SMS anchor claims 5)")

print(f"\n{'ALL VALIDATIONS PASSED' if fails == 0 else f'{fails} FAILURES'}")
sys.exit(0 if fails == 0 else 1)
