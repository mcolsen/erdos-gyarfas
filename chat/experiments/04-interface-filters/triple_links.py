from pathlib import Path
import itertools as it,json,collections,functools,time,networkx as nx
P=Path(__file__).parent
lib=[d for d in json.loads((P/'catalog.json').read_text()) if len(d['terminals'])==7 and d['n']<=11]
SP=sorted(set(tuple(s) for d in lib for s in d['pairs'].values()));ix={s:i for i,s in enumerate(SP)}
def sig(d,ts):return tuple(ix[tuple(d['pairs'][f'{a},{b}'])] for a,b in it.combinations(ts,2))
allowed=set()
for a,s in enumerate(SP):
 for b,t in enumerate(SP):
  if not any((2+x+y)&(1+x+y)==0 for x in s for y in t):allowed.add((a,b))
perms=list(it.permutations(range(3)));pairs=list(it.combinations(range(3),2));index={p:i for i,p in enumerate(pairs)}
@functools.lru_cache(None)
def links(a,b):
 good=[]
 for perm in perms:
  if all((a[k],b[index[tuple(sorted((perm[u],perm[v])))]]) in allowed for k,(u,v) in enumerate(pairs)):good.append(perm)
 return tuple(good)
S=[]
for d in lib:
 for free in d['terminals']:
  rem=[v for v in d['terminals'] if v!=free]
  for left in it.combinations(rem,3):
   right=tuple(v for v in rem if v not in left);S.append((d['id'],free,left,right,sig(d,left),sig(d,right)))
cl=collections.defaultdict(list)
for i,s in enumerate(S):cl[(s[-2],s[-1])].append(i)
C=list(cl);G=nx.DiGraph();G.add_nodes_from(range(len(C)))
for i,(_,a) in enumerate(C):
 for j,(b,_) in enumerate(C):
  if links(a,b):G.add_edge(i,j)
T=[];tasks=0
for a in G:
 for b in G[a]:
  if b<a:continue
  for c in set(G[b])&set(G.predecessors(a)):
   if c<a:continue
   T.append((a,b,c));tasks+=len(cl[C[a]])*len(cl[C[b]])*len(cl[C[c]])*len(links(C[a][1],C[b][0]))*len(links(C[b][1],C[c][0]))*len(links(C[c][1],C[a][0]))
print('cells',len(lib),'states',len(S),'supportstates',len(C),'arcs',G.number_of_edges(),'triangles',len(T),'assemblies',tasks,flush=True)
(P/'triple_links_screen.json').write_text(json.dumps({'cell_ids':[d['id'] for d in lib],'supports':SP,'states':S,'state_classes':[[list(a),list(b)] for a,b in C],'arcs':list(G.edges()),'triangles':T,'tasks':tasks},indent=2))
