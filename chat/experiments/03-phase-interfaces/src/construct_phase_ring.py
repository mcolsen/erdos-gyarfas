"""Construct explicit power-free boundary graphs; these are NOT cubic graphs.

Default: one A turn and r-1 B turns, with r a power of two at least four.
--all-a: the separate five-cell, all-A example.
Output is a one-based DIMACS edge list. No search is performed.
"""
from __future__ import annotations
import argparse
from pathlib import Path

EDGES = ((0,2),(0,3),(0,5),(1,2),(1,4),(1,7),(3,4),(5,6),(6,7))
A, B = (5,7), (2,6)

def construct(r: int, all_a: bool = False) -> list[tuple[int,int]]:
    if all_a:
        if r != 5:
            raise ValueError('The certified all-A example has r=5.')
    elif r < 4 or r & (r-1):
        raise ValueError('The one-A construction requires r=2^k >= 4.')
    turns = [A]*r if all_a else [A]+[B]*(r-1)
    edges = {(u+8*j+1,v+8*j+1) for j in range(r) for u,v in EDGES}
    for j in range(r):
        u = turns[j][1]+8*j+1
        v = turns[(j+1)%r][0]+8*((j+1)%r)+1
        edges.add(tuple(sorted((u,v))))
    degree = [0]*(8*r+1)
    for u,v in edges:
        if u == v: raise AssertionError('Unexpected loop.')
        degree[u] += 1; degree[v] += 1
    assert len(edges)==10*r and degree.count(2)==degree.count(3)==4*r
    return sorted(edges)

def main() -> None:
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('r',type=int);ap.add_argument('output',type=Path)
    ap.add_argument('--all-a',action='store_true');args=ap.parse_args()
    try: edges=construct(args.r,args.all_a)
    except ValueError as e: ap.error(str(e))
    args.output.write_text(f'p edge {8*args.r} {len(edges)}\n'+''.join(f'e {u} {v}\n' for u,v in edges))
    print(f'Wrote {args.output}: {8*args.r} vertices; {4*args.r} degree-two terminals remain.')
if __name__=='__main__': main()
