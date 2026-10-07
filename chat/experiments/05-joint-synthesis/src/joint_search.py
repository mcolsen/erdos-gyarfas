"""Joint cell-choice and terminal-matching synthesis with exact cycle witnesses.

No fixed quotient/backbone. Select one internally safe cell per slot. Match every
port, except an explicitly chosen number of exposed ports. Witness clauses are
lifted to all cell types admitting the same vertex-disjoint routing state.
A budget exhaustion is always UNKNOWN, never UNSAT or a verified construction.
"""
import argparse,ctypes as C,itertools as it,json,time,sys
from pathlib import Path
from functools import lru_cache
import networkx as nx
from z3tiny import Solver
P=Path(__file__).parent
lib=C.CDLL(str(P/'cycle_oracle.so'))
lib.cycles.argtypes=[C.c_int,C.c_int,C.POINTER(C.c_int),C.c_int,C.c_int,C.c_longlong,C.POINTER(C.c_int),C.POINTER(C.c_longlong)]
lib.cycles.restype=C.c_int

def find_cycles(G,L,cap=64,budget=10000000):
 edges=list(G.edges());ee=(C.c_int*(2*len(edges)))(*(v for e in edges for v in e));out=(C.c_int*(L*cap))();nodes=C.c_longlong()
 k=lib.cycles(len(G),len(edges),ee,L,cap,budget,out,C.byref(nodes))
 complete=k>=0
 count=k if complete else -k-1
 return [list(out[i*L:(i+1)*L]) for i in range(count)],complete,count<cap and complete,nodes.value

class Catalogue:
 def __init__(self,path):
  self.cells=json.loads(Path(path).read_text());self.byid={d['id']:d for d in self.cells};self.paths={}
 @lru_cache(None)
 def routes(self,ident,pairs):
  d=self.byid[ident];G=nx.Graph(d['edges']);t=d['terminals']
  pp=[]
  for a,b in pairs:
   key=(ident,a,b)
   if key not in self.paths:self.paths[key]=[(len(p)-1,sum(1<<v for v in p)) for p in nx.all_simple_paths(G,t[a],t[b])]
   pp.append(self.paths[key])
  ans=set()
  def rec(i,used,total):
   if i==len(pp):ans.add(total);return
   for l,mask in pp[i]:
    if not (mask&used):rec(i+1,mask|used,total+l)
  rec(0,0,0);return frozenset(ans)

def run(args):
 out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
 cat=Catalogue(args.catalog)
 opts=[[d for d in cat.cells if len(d['terminals'])==p and d['n']<=args.maxcell] for p in args.ports]
 if not all(opts):raise ValueError("No catalogue option for at least one requested arity/order")
 if args.exposed<0 or args.exposed>sum(args.ports):raise ValueError("Invalid exposed-port count")
 # A slot's port numbers, not original internal vertex labels, are SAT entities.
 ports=[(i,p) for i,n in enumerate(args.ports) for p in range(n)]
 if (len(ports)-args.exposed)%2:raise ValueError('Odd number of ports to match')
 s=Solver(seed=args.seed,timeout_ms=args.solve_ms)
 types=[[s.var(f't_{i}_{k}') for k in range(len(o))] for i,o in enumerate(opts)]
 for vs in types:s.exactly(vs)
 xs={e:s.var(f'e_{e[0]}_{e[1]}') for e in it.combinations(range(len(ports)),2)}
 inc=[[] for p in ports]
 for (a,b),v in xs.items():inc[a].append(v);inc[b].append(v)
 exposure=[s.var(f'free_{a}') for a in range(len(ports))] if args.exposed else []
 if exposure:s.exactly(exposure,args.exposed)
 for a,vs in enumerate(inc):s.exactly(vs+([exposure[a]] if exposure else []))
 # Ban loops that would duplicate an internal edge, or create a forbidden cycle.
 for (a,b),v in xs.items():
  i,p=ports[a];j,q=ports[b]
  if i!=j:continue
  for k,d in enumerate(opts[i]):
   supports=cat.routes(d['id'],((p,q),))
   if 1 in supports or any(l+1>=4 and ((l+1)&l)==0 for l in supports):s.clause([-v,-types[i][k]])
 if args.resume:s.load(Path(args.resume).read_text())
 metadata={'resume':args.resume,'ports':args.ports,'exposed':args.exposed,'max_cell_order':args.maxcell,'options':[[d['id'] for d in o]for o in opts], 'seed':args.seed,'solve_timeout_ms':args.solve_ms,'ports_named':ports}
 (out/'model.json').write_text(json.dumps(metadata,indent=2))
 start=time.time();rounds=0;learned=0;best=10**9;status='UNKNOWN';totalnodes=0;rejected_lengths={}
 log=open(out/'witnesses.jsonl','w');hist=open(out/'progress.jsonl','w')
 skeletons=set();universal=0;decision_nodes=0;orbit_instances=0
 def diagram(external,routes):
  """Compile the FULL length support of one routing circuit into a type MDD.
  -1 is false (circuit is forbidden); -2 is true (this circuit is safe).
  This handles repeated cell visits via the exact disjoint-routing catalogue.
  """
  nonlocal universal,decision_nodes,orbit_instances
  ids=tuple(sorted(routes));groups=[]
  for i in ids:
   g={}
   for k,d in enumerate(opts[i]):
    rs=tuple(sorted(cat.routes(d['id'],tuple(sorted(routes[i][0])))))
    g.setdefault(rs,[]).append(k)
   groups.append(list(g.items()))
  max_order=sum(max(d['n'] for d in o)for o in opts)
  power_mask=sum(1<<v for v in (2**k for k in range(2,max_order.bit_length()))if v<=max_order)
  nodes=[];cache={}
  @lru_cache(None)
  def rec(j,bits):
   if bits==0:return -2
   if j==len(ids):return -1 if bits&power_mask else -2
   branches=[]
   for support,which in groups[j]:
    nb=0
    for v in support:nb |= bits<<v
    child=rec(j+1,nb);branches.append((which,child))
   if len({child for _,child in branches})==1:return branches[0][1]
   key=(ids[j],tuple((tuple(ks),ch)for ks,ch in branches))
   if key not in cache:cache[key]=len(nodes);nodes.append({'slot':ids[j],'branches':branches})
   return cache[key]
  root=rec(0,1<<len(external));decision_nodes+=len(nodes)
  if root==-1:universal+=1
  asts={-1:s.FALSE(),-2:s.TRUE()}
  for j,node in enumerate(nodes):
   cases=[]
   for ks,child in node['branches']:
    if child==-1:continue
    selected=s.OR([s.v[types[node['slot']][k]]for k in ks])
    cases.append(selected if child==-2 else s.AND([selected,asts[child]]))
   asts[j]=s.OR(cases)
  s.assert_ast(s.OR([s.nv[v]for v in external]+[asts[root]]));orbit_instances+=1
  if args.symmetry:
   assert all([d['id']for d in o]==[d['id']for d in opts[0]] for o in opts)
   reverse={v:e for e,v in xs.items()}
   port_index={p:i for i,p in enumerate(ports)}
   for dst in it.permutations(range(len(opts)),len(ids)):
    mapping=dict(zip(ids,dst))
    if all(i==j for i,j in mapping.items()):continue
    ex=[]
    for v in external:
     a,b=reverse[v];i,p=ports[a];j,q=ports[b]
     key=tuple(sorted((port_index[(mapping[i],p)],port_index[(mapping[j],q)])))
     ex.append(xs[key])
    newasts={-1:s.FALSE(),-2:s.TRUE()}
    for h,node in enumerate(nodes):
     cases=[]
     for ks,child in node['branches']:
      if child==-1:continue
      selected=s.OR([s.v[types[mapping[node['slot']]][k]]for k in ks])
      cases.append(selected if child==-2 else s.AND([selected,newasts[child]]))
     newasts[h]=s.OR(cases)
    s.assert_ast(s.OR([s.nv[v]for v in ex]+[newasts[root]]));orbit_instances+=1
  return {'root':root,'nodes':nodes,'states':rec.cache_info().currsize,'all_slot_injections':args.symmetry}
 def learn(G,cyc,choices,owners,localport,edgevar):
  nonlocal learned
  external=[];idx=[]
  for h,(a,b) in enumerate(zip(cyc,cyc[1:]+cyc[:1])):
   key=tuple(sorted((a,b)))
   if key in edgevar:external.append(edgevar[key]);idx.append(h)
  assert idx,'Unsafe internal cell slipped through catalogue'
  routes={}
  for pos,h in enumerate(idx):
   nex=idx[(pos+1)%len(idx)];a=cyc[(h+1)%len(cyc)];b=cyc[nex];i=owners[a];assert i==owners[b]
   p,q=sorted((localport[a],localport[b]));length=(nex-h-1)%len(cyc)
   rr=routes.setdefault(i,[[],0]);rr[0].append((p,q));rr[1]+=length
  literals=[-v for v in external];conditions=[]
  for i,(pairs,length) in sorted(routes.items()):
   pairs=tuple(sorted(pairs));compatible=[k for k,d in enumerate(opts[i]) if length in cat.routes(d['id'],pairs)]
   assert choices[i] in compatible
   literals += [v for k,v in enumerate(types[i]) if k not in compatible]
   conditions.append({'slot':i,'pairs':pairs,'length':length,'compatible':compatible})
  key=(tuple(sorted(external)),tuple((i,tuple(sorted(pairs))) for i,(pairs,_) in sorted(routes.items())))
  if args.strong and key in skeletons:return
  skeletons.add(key)
  dd=diagram(external,routes) if args.strong else None
  if not args.strong:s.clause(literals)
  learned+=1
  log.write(json.dumps({'cycle':cyc,'choices':choices,'external_vars':external,'routing':conditions,'clause':literals,'diagram':dd})+'\n')
 while time.time()-start<args.seconds and rounds<args.rounds:
  answer=s.check()
  if answer==-1:status='SOLVER_UNSAT';break
  if answer==0:status='UNKNOWN_SOLVER';break
  rounds+=1;choices=[next(k for k,v in enumerate(vs) if s.val(v)) for vs in types]
  G=nx.Graph();owners=[];localport={};offsets=[]
  for i,k in enumerate(choices):
   d=opts[i][k];off=len(G);offsets.append(off);G.add_nodes_from(range(off,off+d['n']));G.add_edges_from((off+a,off+b)for a,b in d['edges']);owners.extend([i]*d['n'])
   for p,v in enumerate(d['terminals']):localport[off+v]=p
  edgevar={};chosen_edges=[]
  for (a,b),v in xs.items():
   if s.val(v):
    i,p=ports[a];j,q=ports[b];u=offsets[i]+opts[i][choices[i]]['terminals'][p];w=offsets[j]+opts[j][choices[j]]['terminals'][q]
    assert u!=w and not G.has_edge(u,w);G.add_edge(u,w);edgevar[tuple(sorted((u,w)))]=v;chosen_edges.append([a,b])
  assert sum(d==2 for _,d in G.degree())==args.exposed and all(d in(2,3)for _,d in G.degree())
  found=False;unknown=False;stage_counts={}
  p=4
  while p<=len(G):
   cyc,completed,count_exact,nodes=find_cycles(G,p,args.batch,args.nodes);totalnodes+=nodes
   stage_counts[p]={'count':len(cyc),'exact':count_exact}
   if cyc:
    for c in cyc:learn(G,c,choices,owners,localport,edgevar)
    rejected_lengths[p]=rejected_lengths.get(p,0)+len(cyc);found=True
   if not completed:unknown=True
   if found or unknown:break
   p*=2
  if p>=16 and not unknown:
   score=stage_counts.get(16,{'count':0})['count']
   if score<best:
    best=score;record={'round':rounds,'choices':choices,'cell_ids':[opts[i][k]['id']for i,k in enumerate(choices)],'matching':chosen_edges,'n':len(G),'stage_counts':stage_counts,'seconds':time.time()-start}
    (out/'best.json').write_text(json.dumps(record,indent=2));(out/'best.edge').write_text(f'p edge {len(G)} {G.number_of_edges()}\n'+''.join(f'e {a+1} {b+1}\n'for a,b in sorted(G.edges())))
    print('BEST',record,flush=True)
  if not found:
   if unknown:status='UNKNOWN_ORACLE';break
   status='POWER_FREE_CANDIDATE';break
  if rounds%25==0:
   line={'round':rounds,'learned':learned,'seconds':round(time.time()-start,3),'minimum_observed_capped_C16_witness_count':best,'last':stage_counts};print(line,flush=True);hist.write(json.dumps(line)+'\n');hist.flush();log.flush()
 log.close();hist.close()
 result={'status':status,'rounds':rounds,'clauses':learned,'seconds':time.time()-start,'minimum_observed_capped_C16_witness_count':best,'cycle_clauses_by_length':rejected_lengths,'oracle_nodes':totalnodes,'universal_topology_clauses':universal,'decision_diagram_nodes':decision_nodes,'orbit_instances':orbit_instances}
 (out/'result.json').write_text(json.dumps(result,indent=2));(out/'constraints.smt2').write_text(s.dump());s.close();print('RESULT',result,flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--catalog',default=str(P.parent/'data/catalog.json'));p.add_argument('--ports',type=int,nargs='+',default=[7]*5);p.add_argument('--exposed',type=int,default=1);p.add_argument('--maxcell',type=int,default=11);p.add_argument('--seconds',type=float,default=30);p.add_argument('--rounds',type=int,default=10000);p.add_argument('--solve-ms',type=int,default=2000);p.add_argument('--batch',type=int,default=64);p.add_argument('--nodes',type=int,default=2000000);p.add_argument('--seed',type=int,default=1);p.add_argument('--resume');p.add_argument('--strong',action='store_true');p.add_argument('--symmetry',action='store_true');p.add_argument('--out',default=str(P/'run1'));run(p.parse_args())
