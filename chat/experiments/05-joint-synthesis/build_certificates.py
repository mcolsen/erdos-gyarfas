"""Reconstruct finite witnesses for the new all-orders filter theorems."""
from pathlib import Path
from itertools import combinations, combinations_with_replacement, product
from collections import Counter
import json
import networkx as nx
P=Path(__file__).resolve().parent

def addsets(sets):
    d={0:[]}
    for S in sets:
        nd={}
        for a,w in d.items():
            for b in sorted(S):nd.setdefault(a+b,w+[b])
        d=nd
    return d

def main():
    catalog=json.loads((P/'data/catalog.json').read_text())
    U=next(d for d in catalog if d['id']=='cell0095');G=nx.Graph(U['edges'])
    supports={tuple(sorted({len(p) for p in nx.all_simple_paths(G,a,b)}))
              for a,b in combinations(U['terminals'],2)}
    minimal=sorted(S for S in supports if not any(set(T)<set(S) for T in supports))
    assert minimal==[(2,6,10,11),(3,5,9,10),(3,7,8,9,10),(4,5,8),(4,6,7,10,11),(4,8,9),(5,7,8,9,10),(6,7,8,9)]
    quads=list(combinations_with_replacement(range(len(minimal)),4))
    good={};bad=[]
    for q in quads:
        w=addsets([minimal[t] for t in q])
        if 32 in w:good[q]=w[32]
        else:bad.append(q)
    assert bad==[(1,3,3,3)]
    repairs=[]
    for q in quads:
        if q==(3,3,3,3):continue
        pool=sorted(list(q)+list(bad[0]));found=None
        for ix in combinations(range(8),4):
            A=tuple(pool[i]for i in ix);B=tuple(pool[i]for i in range(8)if i not in ix)
            if A in good and B in good:found=(A,B);break
        assert found is not None,(q,pool)
        repairs.append({'partner':q,'replacement':found})
    cert={'cell':U,'minimal_contribution_supports':minimal,'good_four_blocks':[{'turns':q,'contributions':w}for q,w in good.items()],
          'sole_bad_four_block':bad[0],'repairs':repairs,'unrepairable_partner':[3]*4,
          'exceptional_pattern':'one B and r-1 D; choose B=3, one D=5, other D=4: total 4r'}
    (P/'certificates/u11_variable_dilation.json').write_text(json.dumps(cert,indent=2))
    rows=[]
    for k in range(2,8):
        r=2**k;safe=[];checked=0
        # Precompute polynomial support in bitsets, independent of the case proof.
        aa=[1];bb=[1];cc=[1]
        for j in range(r):
            aa.append((aa[-1]<<2)|(aa[-1]<<7))
            bb.append((bb[-1]<<3)|(bb[-1]<<6))
            cc.append((cc[-1]<<4)|(cc[-1]<<5))
        for a in range(r+1):
            for b in range(r-a+1):
                c=r-a-b;bits=0;work=bb[b]
                while work:
                    z=work&-work;bits|=aa[a]<<(z.bit_length()-1);work-=z
                out=0;work=cc[c]
                while work:
                    z=work&-work;out|=bits<<(z.bit_length()-1);work-=z
                ok=not((out>>(2*r))&1)and not((out>>(4*r))&1)
                if ok:safe.append([a,b,c])
                checked+=1
        expect=sorted([[0,r,0],[r-1,1,0],[r-2,0,2]] if k%2==0 else [[0,r,0],[r-2,2,0],[r-1,0,1]])
        assert sorted(safe)==expect,(r,safe,expect)
        rows.append({'k':k,'r':r,'profiles_checked':checked,'safe_profiles':safe})
    (P/'certificates/heptagon_profiles.json').write_text(json.dumps({'rows':rows,'total_profiles':sum(x['profiles_checked']for x in rows)},indent=2))
    print('U11: 330 four-blocks, 329 exact witnesses, 329 repair identities; heptagon profiles:',sum(x['profiles_checked']for x in rows),flush=True)
    # A learned three-link topology impossible for all 11^3 independent cell choices.
    motif=json.loads((P/'data/universal_three_cell.json').read_text());opts=motif['model']['options'][0]
    lookup={d['id']:d for d in catalog};pairs=[(5,6),(1,4),(2,3)]
    paths={}
    for slot,pair in enumerate(pairs):
        for ident in opts:
            d=lookup[ident];H=nx.Graph(d['edges']);a,b=(d['terminals'][i]for i in pair)
            per={}
            for pp in nx.all_simple_paths(H,a,b):per.setdefault(len(pp)-1,pp)
            paths[slot,ident]=per
    witnesses=[]
    for chosen in product(opts,repeat=3):
        vals=addsets([paths[i,d]for i,d in enumerate(chosen)])
        target=next((p for p in(4,8,16,32)if p-3 in vals),None)
        assert target is not None,chosen
        lens=vals[target-3];pp=[paths[i,d][lens[i]]for i,d in enumerate(chosen)]
        # Connect 0.second--2.first, 2.second--1.second, 1.first--0.first.
        offsets=[0,lookup[chosen[0]]['n'],lookup[chosen[0]]['n']+lookup[chosen[1]]['n']]
        cyc=[v+offsets[0]for v in pp[0]]+[v+offsets[2]for v in pp[2]]+[v+offsets[1]for v in reversed(pp[1])]
        assert len(cyc)==target and len(set(cyc))==target
        witnesses.append({'cells':chosen,'paths':pp,'cycle':cyc,'length':target})
    (P/'certificates/universal_three_cell_witnesses.json').write_text(json.dumps({'options':opts,'pairs':pairs,'witnesses':witnesses},separators=(',',':')))
    print('Universal wiring motif independently reconstructed for',len(witnesses),'assignments;',dict(Counter(w['length']for w in witnesses)),flush=True)

if __name__=='__main__':main()
