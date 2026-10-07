from pathlib import Path
import sys,json,time,collections
import numpy as np
from scipy.optimize import milp,LinearConstraint,Bounds
from scipy.sparse import coo_matrix
P=Path(__file__).resolve().parent;d=json.loads((P/'data/base126.json').read_text()); seconds=float(sys.argv[1]) if len(sys.argv)>1 else 25
import networkx as nx
g=nx.Graph(d['edges']);d['cycles']=list(nx.simple_cycles(g,length_bound=20));ix={tuple(e):i for i,e in enumerate(d['cotree'])};d['forms']=[[(ix[tuple(sorted((a,b)))],1 if a<b else -1) for a,b in zip(c,c[1:]+c[:1]) if tuple(sorted((a,b))) in ix] for c in d['cycles']]
fixed=json.loads((P/'data/design.json').read_text());p=fixed['modulus'];x=fixed['voltages'];ns=[[] for _ in range(126)]
for a,b in d['edges']:ns[a].append(b);ns[b].append(a)
for a in ns:a.sort()
cycles=[c for c,f in zip(d['cycles'],d['forms']) if sum(s*x[v] for v,s in f)%p==0];print('zero cycles',dict(collections.Counter(map(len,cycles))),flush=True)
I=[];J=[];V=[];lo=[];hi=[]
def row(terms,a,b):
 i=len(lo);lo.append(a);hi.append(b)
 for j,z in terms:I.append(i);J.append(j);V.append(z)
for v in range(126):row([(6*v+j,1) for j in range(6)],1,1)
for c in cycles:
 terms=[]
 for i,v in enumerate(c):
  for k in range(6):
   q=int(ns[v][k%3] not in [c[i-1],c[(i+1)%len(c)]])
   terms.append((6*v+k,3+q if k<3 else 4+2*q))
 row(terms,65,np.inf)
A=coo_matrix((np.array(V,float),(I,J)),shape=(len(lo),756)).tocsc();t=time.monotonic()
res=milp(np.tile([7.,7.,7.,15.,15.,15.],126),integrality=np.ones(756),bounds=Bounds(0,1),constraints=LinearConstraint(A,lo,hi),options={'time_limit':seconds,'mip_rel_gap':0.01})
print('status',res.status,res.message,'sec',time.monotonic()-t,'obj',res.fun,'bound',getattr(res,'mip_dual_bound',None),flush=True)
if res.x is not None:
 ch={v:(7 if np.argmax(res.x[v*6:v*6+6])<3 else 15, ns[v][int(np.argmax(res.x[v*6:v*6+6]))%3]) for v in range(126)}
 vals=[]
 for c in cycles:
  L=0
  for i,v in enumerate(c):
   size,special=ch[v];q=int(special not in (c[i-1],c[(i+1)%len(c)]));L+=3+q if size==7 else 4+2*q
  assert L>=65
  vals.append(L)
 nfinal=p*sum(s for s,a in ch.values());print('FEASIBLE',nfinal,'counts',collections.Counter(s for s,a in ch.values()),'minimum',min(vals),flush=True)
 (P/'candidate_design.json').write_text(json.dumps({'modulus':p,'voltages':x,'choices':ch,'expanded_order':nfinal,'short_cycle_minimum':min(vals),'solver_status':int(res.status),'solver_objective':res.fun,'solver_dual_bound':getattr(res,'mip_dual_bound',None)},indent=2))
