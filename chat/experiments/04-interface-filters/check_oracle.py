from interface_oracle import NecklaceOracle
from pathlib import Path
import json,itertools as it,time,networkx as nx
P=Path(__file__).parent;D=P/'completions'
start=time.time()
for m,r,name in [(7,8,'hep56'),(6,10,'hex60'),(11,8,'gap88')]:
 o=NecklaceOracle(m,r)
 assert not any(o.spectrum([])>>p&1 for p in [4,8,16,32,64,128])
 E=[];excluded=[]
 for a,b in it.combinations(o.free,2):
  if o.base.has_edge(a,b):continue
  w=o.spectrum([(a,b)],True)
  if w is None:E.append((a,b))
  else:excluded.append({'edge':[a,b],'cycle':w})
 if name!='gap88':
  old={tuple(map(int,l.split())) for l in (D/f'{name}_compatible.txt').read_text().splitlines()};assert set(E)==old
 print(name,'compatible',len(E),'excluded',len(excluded),'routecache',o.routes.cache_info(),'elapsed',time.time()-start,flush=True)
 if name!='gap88':
  oldC={tuple(map(int,l.split())) for l in (D/f'{name}_conflicts.txt').read_text().splitlines()}
 C=[]
 for i,j in it.combinations(range(len(E)),2):
  if len(set(E[i]+E[j]))<4:C.append({'indices':[i,j],'reason':'shared_endpoint'});continue
  w=o.spectrum([E[i],E[j]],True)
  if name!='gap88':assert (w is not None)==((i,j) in oldC),(name,i,j)
  if w is not None:C.append({'indices':[i,j],'cycle':w})
 H=nx.Graph();H.add_nodes_from(range(len(E)));H.add_edges_from(d['indices'] for d in C)
 colors=nx.coloring.greedy_color(nx.complement(H),strategy='saturation_largest_first') if E else {}
 groups=[[i for i in H if colors[i]==c] for c in range(max(colors.values())+1)] if E else []
 cert={'n':len(o.base),'backbone_edges':list(o.base.edges()),'terminals':o.free,'candidate_edges':E,'excluded_edges':excluded,'conflicts':C,'clique_cover':groups,'claimed_upper_bound':len(groups),'required_for_cubic_completion':len(o.free)//2}
 (D/f'{name}_oracle_certificate.json').write_text(json.dumps(cert,indent=2))
 print(name,'pairs',len(E)*(len(E)-1)//2,'conflicts',len(C),'cliquecoverbound',len(groups),'required',len(o.free)//2,'elapsed',time.time()-start,flush=True)
