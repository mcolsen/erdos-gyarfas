from pathlib import Path
import itertools,collections,json,time
import networkx as nx
P=Path(__file__).parent

def mul(a,b):
 c=0
 while b:
  if b&1:c^=a
  b>>=1;a<<=1
  if a&4:a^=7
 return c
V=[v for v in itertools.product(range(4),repeat=3) if v!=(0,0,0) and next(a for a in v if a)==1]
assert len(V)==21
G=nx.Graph();G.add_nodes_from(range(42))
for i,p in enumerate(V):
 for j,l in enumerate(V):
  if mul(p[0],l[0])^mul(p[1],l[1])^mul(p[2],l[2])==0:G.add_edge(i,j+21)
assert all(d==5 for v,d in G.degree()) and nx.is_connected(G)
ns={v:sorted(G[v]) for v in G}
T=nx.Graph([(5,0),(0,1),(1,6),(5,2),(2,3),(3,6),(5,4),(4,6)])
poly={tuple(sorted((a,b))):collections.Counter(len(p)-1 for p in nx.all_simple_paths(T,a,b)) for a,b in itertools.combinations(range(5),2)}
keys=[];kinds={}
for ab,q in poly.items():
 k=tuple(sorted(q.items()))
 if k not in keys:keys.append(k)
 kinds[ab]=keys.index(k)
assert len(keys)==4
states=[];perms=[]
for perm in itertools.permutations(range(5)):
 row=[-1 if i==j else kinds[tuple(sorted((perm[i],perm[j])))] for i in range(5) for j in range(5)]
 if row not in states:states.append(row);perms.append(perm)
assert len(states)==30
costs=[]
for types in itertools.product(range(4),repeat=6):
 d={0:1}
 for k in types:
  nd=collections.Counter()
  for x,a in d.items():
   for y,b in keys[k]:
    if x+y<=10:nd[x+y]+=a*b
  d=nd
 costs.append(d.get(10,0))
cycles=list(nx.simple_cycles(G,length_bound=8));count=collections.Counter(map(len,cycles));print('PG(2,4) core cycles',dict(count),flush=True)
assert set(count)=={6,8}
rows=[[(v,ns[v].index(c[i-1]),ns[v].index(c[(i+1)%len(c)])) for i,v in enumerate(c)] for c in cycles]
with (P/'theta_pg4_problem.txt').open('w') as f:
 f.write(f'42 30 {len(cycles)}\n')
 for row in states:f.write(' '.join(map(str,row))+'\n')
 f.write(' '.join(map(str,costs))+'\n')
 f.write(str(kinds[(0,1)])+'\n')
 for row in rows:f.write(str(len(row))+' '+' '.join(f'{v} {a} {b}' for v,a,b in row)+'\n')
(P/'theta_pg4_model.json').write_text(json.dumps({'edges':list(G.edges()),'neighbours':ns,'permutations':perms,'path_polynomials':keys,'core_cycle_counts':dict(count)}))
