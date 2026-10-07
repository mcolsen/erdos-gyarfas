"""Recheck learned joint-routing rules without Z3 or the search oracle."""
from pathlib import Path
from itertools import combinations
from functools import lru_cache
from collections import Counter
import argparse,gzip,json,time,math
import networkx as nx
P=Path(__file__).resolve().parent
CAT={d['id']:d for d in json.loads((P/'data/catalog.json').read_text())}
@lru_cache(None)
def routes(ident,pairs):
 d=CAT[ident];G=nx.Graph(d['edges']);ts=d['terminals'];paths=[]
 for a,b in pairs:paths.append([(len(p)-1,frozenset(p))for p in nx.all_simple_paths(G,ts[a],ts[b])])
 states={(frozenset(),0)}
 for possible in paths:states={(used|vertices,L+l)for used,L in states for l,vertices in possible if not used&vertices}
 return tuple(sorted({L for _,L in states}))
def check(name):
 D=P/'runs'/name;model=json.loads((D/'model.json').read_text());options=model['options'];ports=model['ports_named']
 ntypes=sum(map(len,options));evar={ntypes+1+i:pair for i,pair in enumerate(combinations(range(len(ports)),2))}
 count=universals=nodecount=instances=states=0
 with gzip.open(D/'witnesses.jsonl.gz','rt')as f:
  for line in f:
   w=json.loads(line);chosen=[options[i][k]for i,k in enumerate(w['choices'])];G=nx.Graph();offsets=[]
   for ident in chosen:
    d=CAT[ident];off=len(G);offsets.append(off);G.add_nodes_from(range(off,off+d['n']));G.add_edges_from((a+off,b+off)for a,b in d['edges'])
   active=[]
   for var in w['external_vars']:
    a,b=evar[var];active.extend([a,b]);i,p=ports[a];j,q=ports[b]
    G.add_edge(offsets[i]+CAT[chosen[i]]['terminals'][p],offsets[j]+CAT[chosen[j]]['terminals'][q])
   assert len(set(active))==len(active)
   cyc=w['cycle'];assert len(cyc)>=4 and len(cyc)&(len(cyc)-1)==0 and len(set(cyc))==len(cyc)
   assert all(G.has_edge(a,b)for a,b in zip(cyc,cyc[1:]+cyc[:1]))
   stateslots=[];groups=[];pairs_by_slot={}
   for rr in w['routing']:
    slot=rr['slot'];pairs=tuple(sorted(map(tuple,rr['pairs'])));pairs_by_slot[slot]=pairs
    assert len(set(x for pp in pairs for x in pp))==2*len(pairs)
    expected=[k for k,ident in enumerate(options[slot])if rr['length']in routes(ident,pairs)]
    assert rr['compatible']==expected and w['choices'][slot]in expected
    by_support={}
    for k,ident in enumerate(options[slot]):by_support.setdefault(routes(ident,pairs),[]).append(k)
    stateslots.append(slot);groups.append(list(by_support.items()))
   assert stateslots==sorted(stateslots)
   circuit=nx.MultiGraph();pi={tuple(p):i for i,p in enumerate(ports)}
   circuit.add_edges_from(evar[v]for v in w['external_vars'])
   for slot,pp in pairs_by_slot.items():
    for a,b in pp:circuit.add_edge(pi[slot,a],pi[slot,b])
   assert nx.is_connected(circuit)and all(deg==2 for _,deg in circuit.degree())
   assert sum(rr['length']for rr in w['routing'])+len(w['external_vars'])==len(cyc)
   dd=w['diagram'];assert dd is not None;nodes=dd['nodes']
   for h,node in enumerate(nodes):
    which=[k for ks,ch in node['branches']for k in ks]
    assert sorted(which)==list(range(len(options[node['slot']])))
    assert all(ch in(-1,-2)or 0<=ch<h for ks,ch in node['branches'])
   def nextnode(node,slot,k):
    if node<0:return node
    ns=nodes[node]['slot'];assert ns>=slot
    if ns>slot:return node
    return next(ch for ks,ch in nodes[node]['branches']if k in ks)
   @lru_cache(None)
   def equality(j,totals,node):
    if j==len(stateslots):
     expected=not any(t>=4 and t&(t-1)==0 for t in totals)
     assert node in(-1,-2)and(node==-2)==expected
     return
    slot=stateslots[j]
    for support,ks in groups[j]:
     changed=tuple(sorted({a+b for a in totals for b in support}))
     for next_id in {nextnode(node,slot,k)for k in ks}:equality(j+1,changed,next_id)
   equality(0,(len(w['external_vars']),),dd['root']);states+=equality.cache_info().currsize
   count+=1;universals+=dd['root']==-1;nodecount+=len(nodes)
   if dd.get('all_slot_injections',False):
    assert all(x==options[0]for x in options)
    instances+=math.factorial(len(options))//math.factorial(len(options)-len(stateslots))
   else:instances+=1
 result=json.loads((D/'result.json').read_text());assert result['status'].startswith('UNKNOWN')
 assert count==result['clauses']and universals==result['universal_topology_clauses']and nodecount==result['decision_diagram_nodes']
 if 'orbit_instances'in result:assert instances==result['orbit_instances'],(name,instances,result['orbit_instances'])
 print(name+':',count,'routing schemas; each truth table independently reconstructed;',universals,'type-independent rules;',instances,'slot-injection instances;',states,'verification states.',flush=True)
 return count
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('names',nargs='*',default=['strong_test','sym33alpha','sym33cell','sym55alpha','clean33alpha','clean33cell']);a=p.parse_args();start=time.time()
 total=sum(check(n)for n in a.names);print('VERIFIED',total,'learned joint-routing schemas. Seconds:',round(time.time()-start,3),flush=True)
