"""Exhaustive finite checks for the cell-grammar and routing obstructions."""
from pathlib import Path
import sys,itertools,json,collections
import networkx as nx

from gadgets import cell,bounded_cycles
P=Path(__file__).parent/'certificates';spec={};edges={};terms={}
for size in (1,3,7,15):
 if size==1:
  edges[size]=nx.empty_graph(1);terms[size]=[0,0,0]
  for i,j in itertools.combinations(range(3),2):spec[size,i,j]={0}
 else:
  G,t=cell(size);edges[size]=G;terms[size]=t
  for i,j in itertools.combinations(range(3),2):
   spec[size,i,j]={len(p)-1 for p in nx.all_simple_paths(G,t[i],t[j])}
   assert spec[size,i,j]==set(range(min(spec[size,i,j]),max(spec[size,i,j])+1))
  assert not set(map(len,bounded_cycles(G,size)))&{4,8,16,32}
records=[];safe=collections.Counter();cases=0
for sizes in itertools.combinations_with_replacement((1,3,7,15),3):
 for exposed in itertools.product(range(3),repeat=3):
  cases+=1; polys=[]
  for s,e in zip(sizes,exposed):
   i,j=[v for v in range(3) if v!=e];polys.append(spec[s,i,j])
  new={3+a+b+c for a in polys[0] for b in polys[1] for c in polys[2]}
  forbidden=sorted(new&{4,8,16,32,64})
  if forbidden:
   records.append({'sizes':sizes,'exposed':exposed,'obstruction':forbidden[0]});continue
  G=nx.Graph();off=0;ends=[];out=[]
  for s,e in zip(sizes,exposed):
   G.add_nodes_from(range(off,off+s));G.add_edges_from((a+off,b+off) for a,b in edges[s].edges())
   jj=[v for v in range(3) if v!=e];ends.append([terms[s][v]+off for v in jj]);out.append(terms[s][e]+off);off+=s
  for i in range(3):G.add_edge(ends[i][1],ends[(i+1)%3][0])
  assert sum(sizes) in (3,7,15) and nx.is_isomorphic(G,edges[sum(sizes)])
  assert set(out)=={v for v,d in G.degree() if d==2}
  safe[sizes]+=1;records.append({'sizes':sizes,'exposed':exposed,'safe_type':sum(sizes)})
assert set(safe)=={(1,1,1),(1,3,3),(1,7,7)}
(P/'grammar_recheck.json').write_text(json.dumps({'cases':cases,'safe_counts':{str(k):v for k,v in safe.items()},'records':records},indent=2))
print('Triangle grammar closure:',cases,'cases;',dict(safe))
# Local turn charges, doubled half-edge weights to keep integer arithmetic.
for s,h in [(1,[1,1,1]),(3,[1,1,1]),(7,[-3,1,1]),(15,[-11,-3,-3])]:
 for i,j in itertools.combinations(range(3),2):
  S=spec[s,i,j];l=min(S)+1;u=max(S)+1
  assert h[i]+h[j]==2*(2*l-u)
print('All 12 turn-charge identities verified.')
# A concrete, genuinely gapped five-terminal cell.
G=nx.Graph([(5,0),(0,1),(1,6),(5,2),(2,3),(3,6),(5,4),(4,6)])
ps={pair:[list(p) for p in nx.all_simple_paths(G,*pair)] for pair in itertools.combinations(range(5),2)}
support={pair:set(len(p)-1 for p in paths) for pair,paths in ps.items()}
classify={(1,4,5):'A',(2,4,5):'B',(2,3,5,6):'C',(3,4,6):'D'}
types={pair:classify[tuple(sorted(S))] for pair,S in support.items()}
bytype={name:set(vals) for vals,name in classify.items()};compatible=[]
for a,b in itertools.product(sorted(bytype),repeat=2):
 S={2+i+j for i in bytype[a] for j in bytype[b]}
 if not S&{4,8}:compatible.append((a,b))
assert set(compatible)=={('A','D'),('D','A')}
splits=[]
for a,b in itertools.combinations(support,2):
 if set(a)&set(b):continue
 if types[a] in ('A','D') and types[b] in ('A','D'):
  assert types[a]==types[b];assert (set(range(5))-set(a)-set(b))=={4}
  splits.append([a,b,types[a],types[b]])
matchings=[]
for a,b,c,d in itertools.combinations(range(5),4):
 for ab,cd in [((a,b),(c,d)),((a,c),(b,d)),((a,d),(b,c))]:
  ct=collections.Counter(len(p)+len(q)-2 for p in ps[ab] for q in ps[cd] if not set(p)&set(q))
  matchings.append({'pairs':[ab,cd],'polynomial':dict(sorted(ct.items()))})
cert={'edges':sorted(tuple(sorted(e)) for e in G.edges()),'terminals':list(range(5)),
 'internal_cycles':dict(collections.Counter(map(len,bounded_cycles(G,7)))),
 'path_polynomials':{str(k):dict(sorted(collections.Counter(len(p)-1 for p in v).items())) for k,v in ps.items()},
 'pair_types':{str(k):v for k,v in types.items()},'two_cell_compatibility':compatible,'disjoint_safe_splits':splits,'two_path_states':matchings}
(P/'theta_routing_recheck.json').write_text(json.dumps(cert,indent=2))
print('Theta routing certificate: only A-D joins; no disjoint A-D split; all odd double-edge necklaces excluded.')
print('PASS')
