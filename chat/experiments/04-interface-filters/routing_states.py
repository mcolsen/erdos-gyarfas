from pathlib import Path
import networkx as nx,itertools as it,json,collections
P=Path(__file__).parent

def pairings(xs):
 if not xs:yield [];return
 x=xs[0]
 for j in range(1,len(xs)):
  y=xs[j]
  for rem in pairings(xs[1:j]+xs[j+1:]):yield [(x,y)]+rem
out={}
for n in [6,7]:
 G=nx.cycle_graph(n);routes={p:list(nx.all_simple_paths(G,*p)) for p in it.combinations(range(n),2)};states=[];summary={}
 for k in [1,2,3]:
  num=possible=0
  for subset in it.combinations(range(n),2*k):
   for pairs in pairings(list(subset)):
    num+=1;assignments=[];counts=collections.Counter()
    for ps in it.product(*(routes[p] for p in pairs)):
     flat=[v for p in ps for v in p]
     if len(flat)!=len(set(flat)):continue
     length=sum(len(p)-1 for p in ps);counts[length]+=1;assignments.append([list(p) for p in ps])
    possible+=bool(assignments)
    states.append({'pairs':[list(p) for p in pairs],'path_sets':assignments,'length_counts':dict(sorted(counts.items()))})
  summary[k]={'states':num,'realizable':possible}
 out[str(n)]={'edges':[list(e) for e in G.edges()],'terminals':list(G),'summary':summary,'states':states}
 print(n,summary)
(P/'routing_states.json').write_text(json.dumps(out,indent=2))
