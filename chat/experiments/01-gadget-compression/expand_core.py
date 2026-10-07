"""Expand a port-labelled core model into a simple cubic DIMACS graph."""
import sys,hashlib,json
from pathlib import Path
import networkx as nx

def expand(path):
 rows=Path(path).read_text().splitlines();n=int(rows[0]);a=[list(map(int,r.split())) for r in rows[1:] if r.strip()];assert len(a)==n
 g=nx.Graph();ports={};off=1;cells=[]
 for u,(t,sp,*nb) in enumerate(a):
  assert t in (0,1) and sp in (0,1,2) and len(set(nb))==3 and u not in nb
  size=7 if t else 3;g.add_nodes_from(range(off,off+size));cells.append(list(range(off,off+size)))
  edges=[(0,2),(0,5),(1,2),(2,3),(3,1),(4,5),(5,6),(6,4),(3,6)] if t else [(0,1),(1,2),(2,0)]
  g.add_edges_from((off+x,off+y) for x,y in edges)
  ts=[None]*3
  if t:
   ts[sp]=off;other=[i for i in range(3) if i!=sp];ts[other[0]]=off+1;ts[other[1]]=off+4
  else:ts=[off,off+1,off+2]
  for k,v in enumerate(nb):ports[u,v]=ts[k]
  off+=size
 for u,(_,_,*nb) in enumerate(a):
  for v in nb:
   assert (v,u) in ports
   if u<v:g.add_edge(ports[u,v],ports[v,u])
 assert set(dict(g.degree()).values())=={3}
 return g,cells
if __name__=='__main__':
 g,cells=expand(sys.argv[1]);out=Path(sys.argv[2]);out.write_text(f'p edge {len(g)} {g.number_of_edges()}\n'+''.join(f'e {x} {y}\n' for x,y in sorted(tuple(sorted(e)) for e in g.edges())))
 print(json.dumps({'file':str(out),'n':len(g),'m':g.number_of_edges(),'connected':nx.is_connected(g),'sha256':hashlib.sha256(out.read_bytes()).hexdigest()},indent=2))
