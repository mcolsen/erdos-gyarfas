"""Constructive proof-checks of universal fourfold cycle dilation."""
from pathlib import Path
import itertools,json,collections,sys
import networkx as nx
S={'A':{1,4,5},'B':{2,4,5},'C':{2,3,5,6},'D':{3,4,6},'E':{2,3,4,5,6}}
# E is the three-terminal cell formed by adding a permitted internal port edge.
def balanced(types):
 r=len(types);assert r>=3
 out=[3]*r;bad=[i for i,a in enumerate(types) if a in 'AB']
 if len(bad)==1:
  i=bad[0]
  if types[i]=='A':
   helpful=next((j for j,t in enumerate(types) if t in 'CE'),None)
   if helpful is not None:out[i],out[helpful]=4,2
   else:
    js=[j for j in range(r) if j!=i];out[i],out[js[0]],out[js[1]]=1,4,4
  else:
   helpful=next((j for j,t in enumerate(types) if t in 'DE'),None)
   if helpful is not None:out[i],out[helpful]=2,4
   else:
    js=[j for j in range(r) if j!=i];out[i],out[js[0]],out[js[1]]=5,2,2
 else:
  if len(bad)%2:
   js=bad[:3];bad=bad[3:]
   vals=next(z for z in itertools.product(*(S[types[j]] for j in js)) if sum(z)==9)
   for j,v in zip(js,vals):out[j]=v
  for i,j in zip(bad[::2],bad[1::2]):
   vals=next(z for z in itertools.product(S[types[i]],S[types[j]]) if sum(z)==6)
   out[i],out[j]=vals
 assert all(a in S[t] for t,a in zip(types,out)) and sum(out)==3*r
 return out
count=0
for r in range(3,9):
 for t in itertools.product('ABCD',repeat=r):balanced(t);count+=1
for r in range(3,8):
 for t in itertools.product('ABCDE',repeat=r):balanced(t)
G=nx.Graph([(5,0),(0,1),(1,6),(5,2),(2,3),(3,6),(5,4),(4,6)])
loops=[]
for a,b in itertools.combinations(range(5),2):
 if G.has_edge(a,b):continue
 H=G.copy();H.add_edge(a,b);cy=set(map(len,nx.simple_cycles(H)))
 if not cy&{4,8}:
  loops.append((a,b))
  terms=[v for v,d in H.degree() if d==2]
  for u,v in itertools.combinations(terms,2):assert {len(p)-1 for p in nx.all_simple_paths(H,u,v)}==S['E']
assert set(loops)=={(0,2),(1,3)}
P=Path(__file__).parent
(P/'certificates/theta_dilation_recheck.json').write_text(json.dumps({'supports':{k:sorted(v) for k,v in S.items()},'checked_ordered_sequences_r3_to_r8':count,'safe_internal_edges':loops,
 'proof':'For every r>=3 and every sequence of transit types, choose lengths summing to3r using pairs/triples of A/B and corrections with C/D/E. Add r intercell edges to obtain4r.'},indent=2))
print('PASS constructive balancing; tested',count,'ABCD sequences; E extension and safe internal edges checked.')
