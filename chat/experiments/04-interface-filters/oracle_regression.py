from interface_oracle import NecklaceOracle
import networkx as nx,random,itertools as it,json,time
from pathlib import Path
P=Path(__file__).parent;rng=random.Random(20260905);records=[];start=time.time()
for m in [6,7,11]:
 o=NecklaceOracle(m,3)
 for j in range(8):
  k=1+j%2
  while True:
   ends=rng.sample(o.free,2*k);new=[tuple(sorted(ends[2*i:2*i+2])) for i in range(k)]
   if all(not o.base.has_edge(*e) for e in new):break
  H=o.base.copy();H.add_edges_from(new);edge_set=set(new);actual=0;cycle_count=0
  for cy in nx.simple_cycles(H):
   ec={tuple(sorted(e)) for e in zip(cy,cy[1:]+cy[:1])}
   if edge_set<=ec:actual|=1<<len(cy);cycle_count+=1
  predicted=o.spectrum(new)
  assert predicted==actual,(m,new,[i for i in range(len(H)+1) if (predicted^actual)>>i&1])
  records.append({'cell_size':m,'cells':3,'new_edges':new,'simple_cycles_using_all_new_edges':cycle_count,'spectrum':[i for i in range(len(H)+1) if actual>>i&1]})
print('PASS',len(records),'full-graph comparisons','seconds',time.time()-start)
(P/'oracle_regression.json').write_text(json.dumps(records,indent=2))
