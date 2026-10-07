from itertools import product, combinations, permutations
from collections import Counter
from pathlib import Path
import networkx as nx, json,time
OUT=Path(__file__).parent

def cubic_multigraphs(n):
    deg=[3]*n;edges=[]
    def row(i):
        if i==n:
            yield list(edges);return
        if deg[i]==0:
            yield from row(i+1);return
        js=list(range(i+1,n))
        def dist(j,left):
            if j==len(js):
                if left==0:yield from row(i+1)
                return
            v=js[j]
            for t in range(min(left,deg[v])+1):
                deg[v]-=t;edges.extend([(i,v)]*t)
                yield from dist(j+1,left-t)
                if t:del edges[-t:]
                deg[v]+=t
        yield from dist(0,deg[i])
    yield from row(0)

def cycles(n,edges):
    adj=[[] for _ in range(n)]
    for j,(a,b) in enumerate(edges):adj[a].append((b,j));adj[b].append((a,j))
    out=set()
    def dfs(s,v,seen,es):
        for w,e in adj[v]:
            if e in es:continue
            if w==s and len(es)>=1:
                out.add(tuple(sorted(es+[e])))
            elif w>s and w not in seen:
                dfs(s,w,seen|{w},es+[e])
    for s in range(n):dfs(s,s,{s},[])
    return sorted(out)

records=[]
for n in (2,4,6):
    reps=[];generated=0
    for edges in cubic_multigraphs(n):
        generated+=1;g=nx.MultiGraph();g.add_nodes_from(range(n));g.add_edges_from(edges)
        if not nx.is_connected(g) or list(nx.articulation_points(g)):continue
        if any(nx.is_isomorphic(g,h) for h in reps):continue
        reps.append(g)
    print('n',n,'labeled',generated,'biconnected classes',len(reps),flush=True)
    for i,g in enumerate(reps):
        es=sorted(tuple(sorted(e)) for e in g.edges());cs=cycles(n,es)
        counts=Counter(es);auts=[]
        for p in permutations(range(n)):
            if Counter(tuple(sorted((p[a],p[b]))) for a,b in es)==counts:auts.append(p)
        records.append({'name':f'b{n}_{i}','b':n,'edges':es,'cycles':cs,'automorphisms':auts})
(OUT/'skeletons.json').write_text(json.dumps(records,indent=2))
