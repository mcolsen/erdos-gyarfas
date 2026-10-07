from pathlib import Path
import itertools,json,collections,time
P=Path(__file__).parent;gs=[g for g in json.loads((P/'screened_small.json').read_text()) if g['k']==6]

def path_lists(g):
    n=g['n'];a=[[] for _ in range(n)]
    for u,v in g['edges']:a[u].append(v);a[v].append(u)
    ps={}
    for s,t in itertools.combinations(g['terminals'],2):
        out=[]
        def dfs(u,seen,d):
            if u==t:out.append((d,seen));return
            for v in a[u]:
                if not seen>>v&1:dfs(v,seen|1<<v,d+1)
        dfs(s,1<<s,0);ps[s,t]=out
    return ps

acts=[]
for g in gs:
    ps=path_lists(g);supports={k:sum(1<<v for v in {p[0] for p in z}) for k,z in ps.items()}
    TT={}
    for left in itertools.combinations(g['terminals'],2):
        for right in itertools.combinations([t for t in g['terminals'] if t not in left],2):
            mask=0
            for rp in (right,right[::-1]):
                for d,x in ps[tuple(sorted((left[0],rp[0])))]:
                    for e,y in ps[tuple(sorted((left[1],rp[1])))]:
                        if not x&y:mask|=1<<(d+e)
            TT[left,right]=mask
    seen=set()
    for leftset in itertools.combinations(g['terminals'],3):
        right=tuple(t for t in g['terminals'] if t not in leftset)
        for left in itertools.permutations(leftset):
            L=[supports[tuple(sorted(left[j] for j in range(3) if j!=i))] for i in range(3)]
            R=[supports[tuple(sorted(right[j] for j in range(3) if j!=i))] for i in range(3)]
            T=[[TT[tuple(sorted(left[p] for p in range(3) if p!=i)),tuple(sorted(right[p] for p in range(3) if p!=j))] for j in range(3)] for i in range(3)]
            key=(tuple(L),tuple(R),tuple(map(tuple,T)))
            if key in seen:continue
            seen.add(key)
            acts.append({'cell':g['id'],'n':g['n'],'left':left,'right':right,'L':L,'R':R,'T':T})
    print(g['id'],len(seen),flush=True)
(P/'transfers.json').write_text(json.dumps(acts,indent=2))
print('TOTAL',len(acts))
