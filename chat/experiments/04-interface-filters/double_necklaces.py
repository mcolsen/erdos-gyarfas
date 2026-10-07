from pathlib import Path
import itertools as it, json, collections, networkx as nx, time
P=Path(__file__).parent
L=[d for d in json.loads((P/'catalog.json').read_text()) if len(d['terminals'])==5]
# State labels: exposed terminal, unordered left pair, unordered right pair.
S=[]
for d in L:
 for free in d['terminals']:
  rest=[v for v in d['terminals'] if v!=free]
  for left in it.combinations(rest,2):
   right=tuple(v for v in rest if v not in left)
   a=tuple(d['pairs'][','.join(map(str,left))]);b=tuple(d['pairs'][','.join(map(str,right))])
   S.append((d['id'],free,left,right,a,b))
spectra=sorted(set(s for x in S for s in x[-2:]));ix={s:i for i,s in enumerate(spectra)}
compat=set()
for i,a in enumerate(spectra):
 for j,b in enumerate(spectra):
  sums={2+x+y for x in a for y in b}
  if not any((x&(x-1))==0 for x in sums):compat.add((i,j))
print('cells',len(L),'states',len(S),'supports',len(spectra),'orderedcompatible_supports',len(compat),flush=True)
# Collapse local states by the pair of left/right spectra.
classes=collections.defaultdict(list)
for k,s in enumerate(S):classes[(ix[s[-2]],ix[s[-1]])].append(k)
C=list(classes);G=nx.DiGraph();G.add_nodes_from(range(len(C)))
for i,(_,a) in enumerate(C):
 for j,(b,_) in enumerate(C):
  if (a,b) in compat:G.add_edge(i,j)
print('spectral_states',len(C),'arcs',G.number_of_edges(),'scc_sizes',sorted([len(c) for c in nx.strongly_connected_components(G)],reverse=True)[:10],flush=True)
triples=[]
for a in G:
 for b in G[a]:
  if b<a:continue
  for c in set(G[b])&set(G.predecessors(a)):
   if c<a:continue
   triples.append((a,b,c))
print('triangle_state_types',len(triples),flush=True)
active=set(v for component in nx.strongly_connected_components(G) if len(component)>1 for v in component)
H=G.subgraph(active).to_undirected()
print('cyclicactive',len(active),'bipartite',nx.is_bipartite(H),flush=True)
(P/'double_necklace_screen.json').write_text(json.dumps({'cell_ids':[d['id'] for d in L],'spectra':spectra,'compatibility':sorted(compat),'states':[list(c) for c in C],'arcs':list(G.edges()),'triangles':triples,'cyclic_active_states':sorted(active),'bipartite':nx.is_bipartite(H)},indent=2))
if triples:
 for z in triples[:20]:
  print([[ (S[k][0],S[k][1],S[k][2],S[k][3]) for k in classes[C[t]][:3]] for t in z])
