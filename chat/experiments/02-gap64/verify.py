"""Verify the 26,550-vertex construction without an optimization solver.

Independent base-cycle enumeration: NetworkX.simple_cycles, rather than the
canonical DFS used to formulate the original design. An additional C++ verifier
can check all low-cost cycles directly on the 1,890-vertex lifted core.
"""
from pathlib import Path
import collections,hashlib,itertools,json,math
import networkx as nx
from gadgets import cell,read_dimacs
P=Path(__file__).resolve().parent
base_data=json.loads((P/'data/base126.json').read_text())
design=json.loads((P/'data/design.json').read_text())
B=nx.Graph(base_data['edges']);m=design['modulus'];x=design['voltages']
choices={int(v):tuple(z) for v,z in design['choices'].items()}
assert set(B)==set(range(126)) and B.number_of_edges()==189 and all(d==3 for _,d in B.degree())
assert nx.is_connected(B) and nx.is_bipartite(B)
assert m==15 and len(x)==64 and all(0<=v<m for v in x)
ix={tuple(e):i for i,e in enumerate(base_data['cotree'])}
assert len(ix)==64 and all(B.has_edge(*e) for e in ix)
T=B.copy();T.remove_edges_from(ix);assert nx.is_tree(T)
def z(a,b):
 e=tuple(sorted((a,b)));v=x[ix[e]] if e in ix else 0
 return v if a<b else -v
ns={v:sorted(B[v]) for v in B}
for a,(size,special) in choices.items():assert size in (7,15) and special in ns[a]
polys={};internal={};templates={s:cell(s) for s in (7,15)}
for s,(small,terms) in templates.items():
 internal[s]=collections.Counter(map(len,nx.simple_cycles(small)))
 assert not any(internal[s][L] for L in (4,8,16,32,64))
 for i,j in itertools.combinations(range(3),2):
  p=collections.Counter(len(path) for path in nx.all_simple_paths(small,terms[i],terms[j]))
  assert set(p)==set(range(min(p),max(p)+1))
  assert p[min(p)]==1
  polys[s,i,j]=p
# Count and recheck ALL base cycles that a potentially forbidden external cycle
# could project to. 3 per visited cell implies at most 21 core vertices for L<=65.
# The base is bipartite, so enumerating through20 includes every cycle through21.
counts=collections.Counter();zero_counts=collections.Counter();minimum=999;count65=0;num65=0
for c in nx.simple_cycles(B,length_bound=20):
 counts[len(c)]+=1
 if sum(z(a,b) for a,b in zip(c,c[1:]+c[:1]))%m:continue
 zero_counts[len(c)]+=1;L=0;mult=1
 for i,v in enumerate(c):
  size,special=choices[v];order=[special]+[b for b in ns[v] if b!=special]
  a,b=sorted([order.index(c[i-1]),order.index(c[(i+1)%len(c)])]);p=polys[size,a,b]
  L+=min(p);mult*=p[min(p)]
 assert L>=65,(c,L)
 minimum=min(minimum,L)
 if L==65:count65+=m*mult;num65+=1
assert counts=={12:1008,14:864,16:3780,18:14112,20:51408}
assert zero_counts=={14:94,16:303,18:971,20:3465}
assert minimum==65 and count65==630 and num65==42
print('Independent base enumeration:',dict(sorted(counts.items())))
print('Zero-voltage cycles:',dict(sorted(zero_counts.items())))
# Rebuild both levels directly, using explicit labelled cell templates.
H=nx.Graph();H.add_nodes_from(range(126*m))
for a,b in B.edges():
 for t in range(m):H.add_edge(a*m+t,b*m+(t+z(a,b))%m)
assert len(H)==1890 and H.number_of_edges()==2835 and nx.is_connected(H) and nx.is_bipartite(H)
assert all(d==3 for _,d in H.degree()) and not list(nx.bridges(H))
recorded_core=read_dimacs(P/'data/core1890.edge')
assert {tuple(sorted((u+1,v+1))) for u,v in H.edges()}=={tuple(sorted(e)) for e in recorded_core.edges()}
G=nx.Graph();ports={};offset={};current=1
for a in range(126):
 size,special=choices[a];small,terms=templates[size];order=[special]+[b for b in ns[a] if b!=special]
 for t in range(m):
  u=a*m+t;offset[u]=current
  G.add_nodes_from(range(current,current+size));G.add_edges_from((current+b,current+c) for b,c in small.edges())
  for b,q in zip(order,terms):ports[u,b*m+(t+z(a,b))%m]=current+q
  current+=size
for u,v in H.edges():G.add_edge(ports[u,v],ports[v,u])
recorded=read_dimacs(P/'data/eg26550.edge')
assert set(G)==set(recorded) and {tuple(sorted(e)) for e in G.edges()}=={tuple(sorted(e)) for e in recorded.edges()}
assert len(G)==26550 and G.number_of_edges()==39825
assert all(d==3 for _,d in G.degree()) and nx.is_connected(G)
for L in (65,128):
 cert=json.loads((P/f'certificates/C{L}_witness.json').read_text());w=cert['vertices']
 assert len(w)==len(set(w))==L and all(G.has_edge(w[i-1],w[i]) for i in range(L))
# A cyclically nonbacktracking closed walk of length64 despite no simple C64.
a=next(a for a,(s,_) in choices.items() if s==7);off=offset[a*m]
walk=[off+v for v in [2,1,3,2,0,5,6,3]]*8
assert len(walk)==64 and all(G.has_edge(walk[i-1],walk[i]) for i in range(64))
assert all(walk[i-1]!=walk[(i+1)%64] for i in range(64))
assert len(set(walk))<64
# An explicit 3-edge-colouring certifies the core is in the elementary domain
# of the turn-charge obstruction (no polytope theorem needed for this graph).
left=nx.bipartite.sets(H)[0];work=H.copy();colourings=[]
for colour in range(3):
 match=nx.bipartite.maximum_matching(work,top_nodes=left)
 assert len(match)==len(H)
 matching=[tuple(sorted((u,match[u]))) for u in sorted(left)]
 assert len(matching)==len(H)//2
 colourings.append(matching);work.remove_edges_from(matching)
assert work.number_of_edges()==0
print('Exact edge-for-edge assembly, connected cubic graph; gap16..64; exact C65=630; explicit C128.')
print('Explicit non-simple cyclically nonbacktracking 64-walk verified.')
print('Lifted core independently has three disjoint perfect matchings.')
print('SHA256',hashlib.sha256((P/'data/eg26550.edge').read_bytes()).hexdigest())
print('PASS')
