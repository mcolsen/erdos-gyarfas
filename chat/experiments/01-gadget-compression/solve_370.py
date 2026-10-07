"""Solve the fixed 30-vertex-core, two-cell C32-avoidance design problem.

Example: python solve_370.py --seconds 30 --output candidate.edge
The saved model370.json already contains a verified solution; solving is optional.
"""
from pathlib import Path
import argparse,json
import numpy as np
import networkx as nx
from scipy.optimize import milp,Bounds,LinearConstraint
from scipy.sparse import lil_matrix
from gadgets import expand,write_dimacs,bounded_cycles


def main() -> None:
    parser=argparse.ArgumentParser()
    parser.add_argument('--seconds',type=float,default=30)
    parser.add_argument('--output',type=Path,default=Path('candidate.edge'))
    args=parser.parse_args()
    graph=nx.LCF_graph(30,[-13,-9,7,-7,9,13],5)
    cycles=list(bounded_cycles(graph,10));n=len(graph)
    assert min(map(len,cycles))==8
    A=lil_matrix((n+len(cycles),6*n))
    lower=np.full(n+len(cycles),33.0);upper=np.full(n+len(cycles),np.inf)
    for v in range(n):
        A[v,6*v:6*v+6]=1;lower[v]=upper[v]=1
    for row,c in enumerate(cycles,n):
        for i,v in enumerate(c):
            for slot,w in enumerate(sorted(graph[v])):
                q=int(w not in (c[i-1],c[(i+1)%len(c)]))
                A[row,6*v+slot]=3+q
                A[row,6*v+3+slot]=4+2*q
    result=milp(np.tile([0,0,0,1,1,1],n),integrality=np.ones(6*n),
                bounds=Bounds(0,1),constraints=LinearConstraint(A.tocsc(),lower,upper),
                options={'time_limit':args.seconds,'mip_rel_gap':0.0})
    print(result.message)
    if result.x is None:
        raise SystemExit('No feasible construction returned within this run.')
    choices={}
    for v in range(n):
        slot=int(np.argmax(result.x[6*v:6*v+6]))
        choices[v]=(7 if slot<3 else 15,sorted(graph[v])[slot%3])
    # Integer recheck before emitting any candidate.
    for c in cycles:
        value=0
        for i,v in enumerate(c):
            size,special=choices[v]
            q=int(special not in (c[i-1],c[(i+1)%len(c)]))
            value+=(3+q) if size==7 else (4+2*q)
        if value<33:raise RuntimeError('Rounded solver assignment failed exact validation')
    expanded=expand(graph,choices)
    write_dimacs(expanded,args.output)
    args.output.with_suffix('.model.json').write_text(json.dumps(
        {'core_edges':list(graph.edges()),'choices':choices},indent=2))
    print(f'Verified C4,C8,C16,C32-free construction: {len(expanded)} vertices')

if __name__=='__main__':main()
