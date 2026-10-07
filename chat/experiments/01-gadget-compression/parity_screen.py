"""Necessary-condition screen for EG counterexamples built from cells 3/7/15.

This is NOT a screen for merely C32-free graphs. It addresses simultaneous
avoidance of ALL powers of two. A PASS is necessary, never sufficient.
"""
from pathlib import Path
import argparse,json
from collections import Counter
from gadgets import load_core,bounded_cycles


def screen(core):
    cycles=[c for c in bounded_cycles(core,8) if len(c)<=8]
    for c in cycles:
        if len(c)<=4:
            return {'status':'ruled_out','reason':'core cycle of length 3 or 4',
                    'cycles':[list(c)]}
    cycles=[c for c in cycles if len(c)>=5]
    nodes=sorted(core);index={v:i for i,v in enumerate(nodes)};basis={}
    for i,c in enumerate(cycles):
        coefficients=sum(1<<index[v] for v in c)
        rhs=1;combination=1<<i
        while coefficients:
            pivot=coefficients.bit_length()-1
            if pivot not in basis:
                basis[pivot]=(coefficients,rhs,combination)
                break
            mask,b,comb=basis[pivot]
            coefficients^=mask;rhs^=b;combination^=comb
        else:
            if rhs:
                selected=[list(cycles[j]) for j in range(len(cycles))
                          if (combination>>j)&1]
                counts=Counter(v for c0 in selected for v in c0)
                assert len(selected)%2 and all(k%2==0 for k in counts.values())
                return {'status':'ruled_out','reason':'inconsistent binary parity equations',
                        'number_of_cycles':len(selected),'cycles':selected}
    return {'status':'passes_necessary_parity_test','constraints':len(cycles),
            'rank':len(basis),'warning':'Passing does not imply a counterexample exists.'}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('core',type=Path)
    parser.add_argument('--certificate',type=Path)
    args=parser.parse_args();core,_=load_core(args.core);result=screen(core)
    print(json.dumps(result,indent=2))
    if args.certificate:args.certificate.write_text(json.dumps(result,indent=2))
