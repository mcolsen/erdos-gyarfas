from pathlib import Path
import json,itertools,collections,time
P=Path(__file__).parent
rs=json.loads((P/'interfaces.json').read_text());summary=collections.Counter()

def sumset(a,b):
    out=0
    while b:
        bit=b&-b;out|=a<<(bit.bit_length()-1);b-=bit
    return out

def values(mask):return [i for i in range(mask.bit_length()) if mask>>i&1]

def spectra(g):
    n=g['n'];adj=[[] for _ in range(n)]
    for a,b in g['edges']:adj[a].append(b);adj[b].append(a)
    ts=g['terminals'];out=[]
    for s in ts:
        masks=[0]*n
        def dfs(v,seen,d):
            masks[v]|=1<<d
            for w in adj[v]:
                if not(seen>>w&1):dfs(w,seen|1<<w,d+1)
        dfs(s,1<<s,0)
        for t in ts:
            if t>s:out.append({'pair':[s,t],'lengths':values(masks[t]),'contributions':values(masks[t]<<1)})
    return out

import sys
part=sys.argv[1] if len(sys.argv)>1 else 'small'
if part=='small':rs=[g for g in rs if g['k']<=7]
else:
 a,b=map(int,part.split('-'));rs=rs[a:b]
start=time.time()
for ii,g in enumerate(rs):
    sp=spectra(g);g['paths']=sp
    masks=sorted(set(sum(1<<v for v in s['contributions']) for s in sp))
    minimal=[m for m in masks if not any(m!=q and m&q==q for q in masks)]
    common=(1<<(g['n']+1))-1
    for m in minimal:common&=m
    factors=[c for c in (1,2,4,8,16) if common>>c&1]
    g['minimal_supports']=[values(m) for m in minimal]
    g['fixed_direct_factors']=factors
    if factors:
        g['screen']='direct_inheritance';summary[g['screen']]+=1;continue
    common4=(1<<(4*g['n']+1))-1;bad=None
    for inds in itertools.combinations_with_replacement(range(len(minimal)),4):
        s=1
        for i in inds:s=sumset(s,minimal[i])
        common4&=s
        if not any(s>>p&1 for p in (4,8,16,32,64)):
            bad={'turn_indices':inds,'contributions':[values(minimal[i]) for i in inds],'cycle_support':values(s)}
            break
    if bad:
        g['screen']='breaks_dyadic_C4';g['escape4']=bad
    else:
        g['common_four_block_factors']=[c for c in (1,2,4,8,16) if common4>>(4*c)&1]
        g['screen']='four_block_inheritance' if g['common_four_block_factors'] else 'unresolved_C4_pass'
    summary[g['screen']]+=1
    if ii%100==0:print(ii,round(time.time()-start,2),dict(summary),flush=True)
(P/f'screened_{part}.json').write_text(json.dumps(rs,indent=2));(P/f'summary_{part}.json').write_text(json.dumps(dict(summary),indent=2))
print('FINAL',time.time()-start,dict(summary),flush=True)
for g in rs:
    if g['k']<=5:
        print(g['id'],'n',g['n'],'ports',g['k'],g['screen'],g.get('fixed_direct_factors'),g['minimal_supports'])
