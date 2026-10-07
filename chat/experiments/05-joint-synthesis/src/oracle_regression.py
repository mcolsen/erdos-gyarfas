"""Full independent witness/count regression on the nonempty graph atlas."""
from pathlib import Path
from collections import Counter
import sys
import networkx as nx
from joint_search import find_cycles
n=0;cases=0
for G in nx.graph_atlas_g():
 if not len(G):continue
 counts=Counter(map(len,nx.simple_cycles(G)))
 for L in range(3,9):
  cs,done,exact,_=find_cycles(G,L,cap=100000,budget=10000000)
  assert done and exact and len(cs)==counts[L],(n,L,len(cs),counts[L])
  canon=set()
  for c in cs:
   assert len(c)==len(set(c))==L
   assert all(G.has_edge(a,b)for a,b in zip(c,c[1:]+c[:1]))
   canon.add(tuple(c))
  assert len(canon)==len(cs);cases+=1
 n+=1
assert n==1252 and cases==7512
cs,done,exact,_=find_cycles(nx.complete_graph(7),4,cap=1)
assert len(cs)==1 and done and not exact
cs,done,exact,_=find_cycles(nx.complete_graph(7),4,cap=10000,budget=1)
assert not done and not exact
print('Verified',n,'nonempty graph-atlas graphs;',cases,'full count comparisons; witness, cap, and timeout semantics.')
