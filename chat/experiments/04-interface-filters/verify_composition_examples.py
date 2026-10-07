"""Regression checks for the elementary composition lemmas in RESEARCH_NOTE.md.
The accompanying proofs, not this finite regression, establish all cycle lengths.
"""
from pathlib import Path
import json
import networkx as nx

P = Path(__file__).resolve().parent

def sumset(supports):
    bits = 1
    for support in supports:
        new = 0
        for v in support:
            new |= bits << v
        bits = new
    return {i for i in range(bits.bit_length()) if (bits >> i) & 1}

def power_free(support):
    return not any(n >= 4 and n & (n - 1) == 0 for n in support)

def pentagon_witness(r, b):
    if r < 4 or r & (r-1) or not 0 <= b <= r:
        raise ValueError('Require dyadic r >= 4 and 0 <= b <= r.')
    if b == 0:
        return [2] * r
    a = r-b
    for x in range(a+1):
        y = 2*r-b-3*x
        if 0 <= y <= b:
            return [5]*x + [2]*(a-x) + [4]*y + [3]*(b-y)
    raise AssertionError('The constructive lemma failed.')

def main():
    lib={d['id']:d for d in json.loads((P/'catalog.json').read_text())}
    assert lib['cell0093']['pairs']['3,8'] == [4,5,6]
    graph=nx.Graph(lib['cell0093']['edges'])
    assert sorted(map(len,nx.simple_cycles(graph))) == [3,3,9,10,10,11]
    for r in [4,8,16,32,64,128]:
        for b in range(r+1):
            selected=pentagon_witness(r,b)
            assert len(selected)==r
            assert sum(selected)==(2*r if b==0 else 4*r)
            assert sum(selected) in sumset([{2,5}]*(r-b)+[{3,4}]*b)
        band=sumset([{5,6,7}]*r)
        assert band==set(range(5*r,7*r+1)) and power_free(band)
    for r in range(3,65):
        hexagon=sumset([{3,5}]+[{4}]*(r-1))
        assert hexagon=={4*r-1,4*r+1} and power_free(hexagon)
        heptagon=sumset([{3,6}]*r)
        assert heptagon==set(range(3*r,6*r+1,3)) and power_free(heptagon)
    print('PASS: constructive pentagon reduction and three composition-escape examples')

if __name__=='__main__':
    main()
