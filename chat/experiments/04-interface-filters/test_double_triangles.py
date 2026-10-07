from pathlib import Path
import itertools as it, json, collections, networkx as nx, time, runpy, contextlib,io
P=Path(__file__).parent
with contextlib.redirect_stdout(io.StringIO()):z=runpy.run_path(str(P/'double_necklaces.py'))
S,C,classes=z['S'],z['C'],z['classes'];lib={d['id']:d for d in json.loads((P/'catalog.json').read_text())}
def find_cycle(G,L):
 n=len(G);adj=[sum(1<<w for w in G[v]) for v in range(n)]
 def dfs(s,u,remain,seen,path):
  if remain==1:return path if adj[u]>>s&1 else None
  mask=adj[u]&~seen&~((1<<(s+1))-1)
  while mask:
   b=mask&-mask;mask^=b;w=b.bit_length()-1
   a=dfs(s,w,remain-1,seen|b,path+[w])
   if a is not None:return a
  return None
 for s in range(n):
  a=dfs(s,s,L,1<<s,[s])
  if a is not None:return a
 return None
found=[];counts=collections.Counter();ledger=[];beg=time.time()
for tr in z['triples']:
 for ids in it.product(*(classes[C[t]] for t in tr)):
  states=[S[i] for i in ids];offs=[0]
  for st in states:offs.append(offs[-1]+lib[st[0]]['n'])
  for swaps in it.product([0,1],repeat=3):
   G=nx.Graph();G.add_nodes_from(range(offs[-1]));terms=[]
   for i,s in enumerate(states):
    G.add_edges_from((a+offs[i],b+offs[i]) for a,b in lib[s[0]]['edges']);terms.append(s[1]+offs[i])
    right=s[3];left=states[(i+1)%3][2]
    for k in range(2):G.add_edge(offs[i]+right[k],offs[(i+1)%3]+left[k^swaps[i]])
   assert all(G.degree(v)==(2 if v in terms else 3) for v in G)
   bad=None
   for L in [4,8,16,32]:
    if L>len(G):break
    w=find_cycle(G,L)
    if w is not None:bad=L;break
   counts[bad]+=1
   ledger.append({'state_ids':list(ids),'swaps':list(swaps),'forbidden_length':bad,'witness':w if bad else None})
   if bad is None:
    if not any(nx.is_isomorphic(G,H) for H,d in found):
     d={'n':len(G),'terminals':terms,'edges':list(G.edges()),'states':[list(x) for x in states],'swaps':swaps}
     d['pairs']={f'{a},{b}':sorted({len(p)-1 for p in nx.all_simple_paths(G,a,b)}) for a,b in it.combinations(terms,2)}
     found.append((G,d));print('NEW',len(G),d['pairs'],flush=True)
print('tested',sum(counts.values()),'counts',dict(counts),'distinct_survivors',len(found),'seconds',time.time()-beg)
(P/'double_triangle_ledger.json').write_text(json.dumps(ledger))
(P/'double_triangle_survivors.json').write_text(json.dumps([d for H,d in found],indent=2))
