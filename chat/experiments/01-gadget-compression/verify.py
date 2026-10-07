"""Verify retained constructions and finite parity certificates; no solver needed."""
from pathlib import Path
from collections import Counter
import hashlib, json, itertools
import networkx as nx
from gadgets import (cell, expand, load_core, load_model, read_dimacs,
                     bounded_cycles)
P = Path(__file__).resolve().parent

# Exhaustive template checks, independent canonical DFS.
polys = {}
for size in (3, 7, 15):
    template, ports = cell(size)
    internal = Counter(map(len, bounded_cycles(template, size)))
    assert not any(internal[L] for L in (4, 8, 16, 32))
    for i, j in itertools.combinations(range(3), 2):
        counts = Counter(len(p)-1 for p in nx.all_simple_paths(template, ports[i], ports[j]))
        assert set(counts) == set(range(min(counts), max(counts)+1))
        polys[size, i, j] = counts
    print('cell', size, 'internal spectrum', dict(sorted(internal.items())))

# Rebuild the 370-vertex object and prove the entire [16,32] gap.
core, choices = load_model(P/'data/model370.json')
graph = read_dimacs(P/'data/eg370_no_C32.edge')
assert set(map(frozenset, expand(core, choices).edges())) == set(map(frozenset, graph.edges()))
cycles = list(bounded_cycles(core, 10))
assert Counter(map(len, cycles)) == {8: 90, 10: 72}
minimum = 1000
for c in cycles:
    value = 0
    for i, v in enumerate(c):
        size, special = choices[v]
        bypass = special not in (c[i-1], c[(i+1) % len(c)])
        value += (3+int(bypass)) if size == 7 else (4+2*int(bypass))
    assert value >= 33
    minimum = min(minimum, value)
# Any unenumerated core cycle has >=11 vertices, each contributing >=3 edges.
assert minimum == 33
assert Counter(size for size, _ in choices.values()) == {7: 10, 15: 20}
assert len(graph) == 370 and graph.number_of_edges() == 555
assert all(d == 3 for _, d in graph.degree()) and nx.is_connected(graph)
w = json.loads((P/'certificates/C64_witness.json').read_text())['vertices']
assert len(w) == len(set(w)) == 64
assert all(graph.has_edge(w[i-1], w[i]) for i in range(len(w)))
print('370-vertex graph: exact reconstruction, no cycles 16..32, valid C64 witness')

# Old-core obstruction: odd number of short core cycles, each vertex used evenly.
for corefile, certfile in [('input.core', 'old_core_parity.json'),
                           ('best190.core', 'best190_core_parity.json')]:
    h, _ = load_core(P/'data'/corefile)
    cert = json.loads((P/'certificates'/certfile).read_text())
    cs = cert['cycles']
    assert len(cs) % 2 == 1
    for c in cs:
        assert len(c) in (6, 7, 8) and len(c) == len(set(c))
        assert all(h.has_edge(c[i-1], c[i]) for i in range(len(c)))
    multiplicities = Counter(v for c in cs for v in c)
    assert all(k % 2 == 0 for k in multiplicities.values())
    print(corefile, 'parity contradiction certified with', len(cs), 'cycles')

# Independent coefficient calculation for the 190-vertex specimen.
h, ch = load_core(P/'data/best190.core')
best = read_dimacs(P/'data/eg190_178077.edge')
# expand() chooses a canonical order for the two nondistinguished ports;
# .core expansion can swap them. Check isomorphism rather than edge equality.
assert nx.is_isomorphic(best, expand(h, ch))
counts = Counter()
for c in bounded_cycles(h, 16):
    r = len(c)
    s = sum(ch[v][0] == 7 for v in c)
    q = sum(ch[v][0] == 7 and ch[v][1] not in (c[i-1], c[(i+1)%r])
            for i, v in enumerate(c))
    shift = 2*r+s+q
    p = [1]
    for factor in ([0,1],)*(r+2*q) + ([0,2,3],)*(s-q):
        z = [0] * min(33, len(p)+max(factor))
        for i, a in enumerate(p):
            for k in factor:
                if i+k < len(z): z[i+k] += a
        p = z
    for L in (4, 8, 16, 32):
        if 0 <= L-shift < len(p): counts[L] += p[L-shift]
assert [counts[L] for L in (4,8,16,32)] == [0,0,0,178077], counts
print('190-vertex graph: C4=C8=C16=0, C32=178077 (core polynomial)')
for path in sorted((P/'data').glob('*.edge')):
    print(path.name, hashlib.sha256(path.read_bytes()).hexdigest())
print('PASS')
