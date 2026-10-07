"""Explicit labelled boundary examples used by the guarded-identification tests."""
import itertools as it
import networkx as nx

def graph(m,r):
 if m==8:
  cell=nx.Graph([(0,2),(2,1),(0,3),(3,4),(4,1),(0,5),(5,6),(6,7),(7,1)])
  # Choose actual port pairs from the independently computed support types.
  terms=[v for v,d in cell.degree()if d==2]
  pairs={tuple(sorted((a,b))):sorted({len(p)-1 for p in nx.all_simple_paths(cell,a,b)})for a,b in it.combinations(terms,2)}
  A=next(p for p,s in pairs.items()if s==[2,4,5]);B=next(p for p,s in pairs.items()if s==[3,6])
  entry=[A[0]]+[B[0]]*(r-1);exit=[A[1]]+[B[1]]*(r-1)
 else:
  cell=nx.cycle_graph(m)
  if m==11:cell.add_edges_from([(0,2),(5,7)])
  entry=[3 if m==11 else 0]*r;exit=[8 if m==11 else (2 if m==7 or i==0 else 3)for i in range(r)]
 G=nx.Graph();G.add_nodes_from(range(m*r));G.add_edges_from((m*i+a,m*i+b)for i in range(r)for a,b in cell.edges());G.add_edges_from((m*i+exit[i],m*((i+1)%r)+entry[(i+1)%r])for i in range(r));return G
