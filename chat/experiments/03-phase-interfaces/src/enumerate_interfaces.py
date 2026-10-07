from pathlib import Path
import networkx as nx,json,itertools,collections,time
P=Path(__file__).parent
skeletons=json.loads((P/'skeletons.json').read_text())

def compositions(total,m):
    if m==1:
        yield (total,);return
    for t in range(total+1):
        for tail in compositions(total-t,m-1):yield (t,)+tail

def expand(sk,w):
    g=nx.Graph();g.add_nodes_from(range(sk['b']));v=sk['b']
    for (a,b),l in zip(sk['edges'],w):
        chain=[a]+list(range(v,v+l-1))+[b];v+=l-1
        g.add_edges_from(zip(chain,chain[1:]))
    return g

def signature(sk,w,p):
    dic=collections.defaultdict(list)
    for (a,b),l in zip(sk['edges'],w):dic[tuple(sorted((p[a],p[b])))].append(l)
    return tuple((a,b,tuple(sorted(vals))) for (a,b),vals in sorted(dic.items()))

records=[];summary=[]
for sk in skeletons:
    b=sk['b'];es=sk['edges'];m=len(es);group=collections.defaultdict(list)
    for i,e in enumerate(es):group[tuple(e)].append(i)
    seen=set();ntried=nsafe=0
    for k in range(3,8):
        if b+k>16:continue
        new=[]
        for extra in compositions(k,m):
            w=tuple(1+t for t in extra);ntried+=1
            if any(any(w[ids[j]]>w[ids[j+1]] for j in range(len(ids)-1)) or sum(w[i]==1 for i in ids)>1 for ids in group.values()):continue
            if any(sum(w[i] for i in c) in (4,8,16) for c in sk['cycles']):continue
            key=min(signature(sk,w,p) for p in sk['automorphisms'])
            if key in seen:continue
            seen.add(key);g=expand(sk,w);nsafe+=1
            ts=[v for v,d in g.degree if d==2]
            assert len(ts)==k and all(d in (2,3) for _,d in g.degree)
            data={'id':f'{sk["name"]}_k{k}_{len(new)}','skeleton':sk['name'],'b':b,'k':k,'n':len(g),'weights':w,'edges':sorted(map(list,g.edges())),'terminals':ts}
            new.append(data)
        records.extend(new);summary.append({'skeleton':sk['name'],'k':k,'safe_isoclasses':len(new)})
        print(sk['name'],'k',k,'safe',len(new),flush=True)
    print('TRIED',sk['name'],ntried,nsafe,flush=True)
for k in (3,5,6,7):
    g=nx.cycle_graph(k);records.append({'id':f'cycle{k}','skeleton':'cycle','b':0,'k':k,'n':k,'edges':sorted(map(list,g.edges())),'terminals':list(g)})
(P/'interfaces.json').write_text(json.dumps(records,indent=2));(P/'enumeration_summary.json').write_text(json.dumps(summary,indent=2))
print('TOTAL',len(records))
