from pathlib import Path
import itertools as it,json,collections,networkx as nx,time,runpy,contextlib,io
P=Path(__file__).parent
with contextlib.redirect_stdout(io.StringIO()):z=runpy.run_path(str(P/'triple_links.py'))
# Import the independent cycle-finder definition without executing its experiment.
src=(P/'test_double_triangles.py').read_text();ns={};exec(src[src.index('def find_cycle'):src.index('found=[];')],ns);find_cycle=ns['find_cycle']
S,C,cl,links=z['S'],z['C'],z['cl'],z['links'];lib={d['id']:d for d in z['lib']}
counts=collections.Counter();survivors=[];ledger=[];start=time.time()
for tr in z['T']:
 for ids in it.product(*(cl[C[k]] for k in tr)):
  states=[S[i] for i in ids];offs=[0]
  for s in states:offs.append(offs[-1]+lib[s[0]]['n'])
  edgebase=[(a+offs[i],b+offs[i]) for i,s in enumerate(states) for a,b in lib[s[0]]['edges']]
  choices=[links(states[i][-1],states[(i+1)%3][-2]) for i in range(3)]
  for perms in it.product(*choices):
   G=nx.Graph();G.add_nodes_from(range(offs[-1]));G.add_edges_from(edgebase)
   for i in range(3):
    for j in range(3):G.add_edge(offs[i]+states[i][3][j],offs[(i+1)%3]+states[(i+1)%3][2][perms[i][j]])
   terms=[s[1]+offs[i] for i,s in enumerate(states)]
   assert all(d==2 if v in terms else d==3 for v,d in G.degree())
   bad=None;w=None
   for L in [4,8,16,32]:
    if L>len(G):break
    w=find_cycle(G,L)
    if w is not None:bad=L;break
   counts[bad]+=1
   ledger.append({'state_ids':ids,'permutations':perms,'forbidden_length':bad,'witness':w})
   if bad is None:
    if not any(nx.is_isomorphic(H,G) for H,d in survivors):
     d={'n':len(G),'terminals':terms,'edges':list(G.edges()),'states':states,'permutations':perms}
     d['pairs']={f'{a},{b}':sorted({len(p)-1 for p in nx.all_simple_paths(G,a,b)}) for a,b in it.combinations(terms,2)}
     survivors.append((G,d));print('NEW',len(G),d['pairs'],flush=True)
print('tested',sum(counts.values()),'counts',dict(counts),'distinct_survivors',len(survivors),'seconds',time.time()-start)
(P/'triple_triangle_ledger.json').write_text(json.dumps(ledger))
(P/'triple_triangle_survivors.json').write_text(json.dumps([d for H,d in survivors],indent=2))
