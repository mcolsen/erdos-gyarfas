"""Degree-complete noncubic search by pairing and identifying deficient ports.
Cycles do NOT survive arbitrary contractions. Every learned cycle constraint
therefore includes positive collision literals, as well as required merges.
"""
from pathlib import Path
import itertools as it,json,time,argparse
import networkx as nx
from z3tiny import Solver
from joint_search import find_cycles
from boundary_graphs import graph
P=Path(__file__).parent

def run(args):
 out=Path(args.out);out.mkdir(exist_ok=True,parents=True)
 B=graph(args.cell,args.ring);terms=sorted(v for v,d in B.degree()if d==2);nfinal=len(B)-len(terms)//2
 assert len(terms)%2==0 and all(d in(2,3)for v,d in B.degree())
 s=Solver(args.seed,args.solve_ms);X={p:s.var(f'm_{p[0]}_{p[1]}')for p in it.combinations(terms,2)if not B.has_edge(*p)}
 inc={t:[] for t in terms}
 for (a,b),v in X.items():inc[a].append(v);inc[b].append(v)
 for vv in inc.values():s.exactly(vv)
 deg_clauses=[]
 def clause(c):s.clause(c);deg_clauses.append(c)
 # Unmerged vertices must retain three distinct neighbours.
 for w in B:
  if w in inc:continue
  for a,b in it.combinations(sorted(B[w]),2):
   if (a,b)in X:clause([-X[a,b]])
 # At a merged vertex, 3 or 4 original neighbours must retain >=3 classes.
 for (u,v),x in X.items():
  ns=sorted(set(B[u])|set(B[v]))
  if len(ns)<3:clause([-x])
  elif len(ns)==3:
   for a,b in it.combinations(ns,2):
    if (a,b)in X:clause([-x,-X[a,b]])
  else:
   assert len(ns)==4
   a,b,c,d=ns
   for pp,qq in [((a,b),(c,d)),((a,c),(b,d)),((a,d),(b,c))]:
    if pp in X and qq in X:clause([-x,-X[pp],-X[qq]])
 model={'base_n':len(B),'base_edges':list(B.edges()),'terminals':terms,'final_n':nfinal,'variables':[[*e,v]for e,v in X.items()],'degree_clauses':deg_clauses,'seed':args.seed}
 (out/'model.json').write_text(json.dumps(model,indent=2))
 log=open(out/'witnesses.jsonl','w');start=time.time();rounds=0;learned=0;status='UNKNOWN';best=10**9;bestcounts=None;lengths={};maxguard=0;guardsum=0
 while time.time()-start<args.seconds and rounds<args.rounds:
  ans=s.check()
  if ans==-1:status='SOLVER_UNSAT';break
  if ans==0:status='UNKNOWN_SOLVER';break
  rounds+=1;selected=[p for p,v in X.items()if s.val(v)]
  mate={u:v for a,b in selected for u,v in [(a,b),(b,a)]}
  reps=[min(v,mate.get(v,v))for v in B];ids={v:i for i,v in enumerate(sorted(set(reps)))};mp=[ids[x]for x in reps]
  G=nx.Graph();G.add_nodes_from(range(nfinal));origin={}
  for u,v in B.edges():
   a,b=mp[u],mp[v];assert a!=b
   G.add_edge(a,b);origin.setdefault(tuple(sorted((a,b))),(u,v))
  assert len(G)==nfinal and min(dict(G.degree()).values())>=3 and nx.is_connected(G)
  found=False;unknown=False;counts={};power=4
  while power<=len(G):
   cy,done,exact,nodes=find_cycles(G,power,args.batch,args.nodes)
   counts[power]={'count':len(cy),'exact':exact}
   for cyc in cy:
    lengths[power]=lengths.get(power,0)+1;oriented=[]
    for a,b in zip(cyc,cyc[1:]+cyc[:1]):
     u,v=origin[tuple(sorted((a,b)))];oriented.append((u,v)if mp[u]==a else (v,u))
    groups=[];required=set()
    for h,(u,v)in enumerate(oriented):
     prev=oriented[h-1][1];assert mp[prev]==mp[u]
     groups.append(sorted({prev,u}))
     if prev!=u:required.add(X[tuple(sorted((prev,u)))])
    collisions=set()
    for i,j in it.combinations(range(len(groups)),2):
     for u in groups[i]:
      for v in groups[j]:
       key=tuple(sorted((u,v)))
       if key in X:collisions.add(X[key])
    assert required and all(s.val(v)for v in required) and not any(s.val(v)for v in collisions)
    lits=sorted(-v for v in required)+sorted(collisions);s.clause(lits);learned+=1
    maxguard=max(maxguard,len(collisions));guardsum+=len(collisions)
    log.write(json.dumps({'matching':selected,'cycle':cyc,'oriented_base_edges':oriented,'groups':groups,'required':sorted(required),'collisions':sorted(collisions),'clause':lits})+'\n')
   if cy:found=True
   if not done:unknown=True
   if found or unknown:break
   power*=2
  if power>=16 and not unknown:
   count=counts.get(16,{'count':0})['count']
   if count<best:
    best=count;bestcounts=counts
    rec={'matching':selected,'counts':counts,'n':len(G),'edges':list(G.edges()),'degree_counts':{str(k):sum(d==k for v,d in G.degree())for k in(3,4)},'round':rounds}
    (out/'best.json').write_text(json.dumps(rec,indent=2));(out/'best.edge').write_text(f'p edge {len(G)} {G.number_of_edges()}\n'+''.join(f'e {u+1} {v+1}\n'for u,v in sorted(G.edges())))
    print('BEST',{'round':rounds,'n':len(G),'counts':counts,'degree_counts':rec['degree_counts']},flush=True)
  if not found:status='UNKNOWN_ORACLE'if unknown else 'POWER_FREE_CANDIDATE';break
  if rounds%100==0:print({'round':rounds,'clauses':learned,'seconds':time.time()-start,'last':counts},flush=True);log.flush()
 result={'status':status,'rounds':rounds,'clauses':learned,'seconds':time.time()-start,'best_counts':bestcounts,'cycle_clauses_by_length':lengths,'max_collision_literals':maxguard,'total_collision_literals':guardsum,'nfinal':nfinal}
 log.close();(out/'result.json').write_text(json.dumps(result,indent=2));(out/'constraints.smt2').write_text(s.dump());s.close();print('RESULT',result,flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--cell',type=int,default=7);p.add_argument('--ring',type=int,default=8);p.add_argument('--seconds',type=float,default=40);p.add_argument('--rounds',type=int,default=100000);p.add_argument('--solve-ms',type=int,default=2000);p.add_argument('--batch',type=int,default=32);p.add_argument('--nodes',type=int,default=2000000);p.add_argument('--seed',type=int,default=1);p.add_argument('--out',default=str(P/'contraction1'));run(p.parse_args())
