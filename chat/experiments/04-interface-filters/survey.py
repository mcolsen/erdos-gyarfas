from pathlib import Path
import itertools as it,json,networkx as nx,collections,time
P=Path(__file__).parent
start=time.time()
lib=[]; buckets=collections.defaultdict(list)
def add(G,source):
 if not nx.is_connected(G):return
 if any(d not in (2,3) for v,d in G.degree()):return
 terms=sorted(v for v,d in G.degree() if d==2)
 if not 3<=len(terms)<=15:return
 if any(len(c)&(len(c)-1)==0 for c in nx.simple_cycles(G)):return
 h=nx.weisfeiler_lehman_graph_hash(G)
 for i in buckets[h]:
  if nx.is_isomorphic(G,lib[i]['G']):lib[i]['sources'].append(source);return
 pairs={f'{a},{b}':sorted({len(p)-1 for p in nx.all_simple_paths(G,a,b)}) for a,b in it.combinations(terms,2)}
 shared=set.intersection(*(set(v) for v in pairs.values()))
 fixed=[x+1 for x in shared if x+1>=2 and (x+1)&x==0]
 d={'G':G,'n':len(G),'terminals':terms,'edges':sorted(tuple(sorted(e)) for e in G.edges()),'sources':[source],'pairs':pairs,'common_fixed_dilations':fixed}
 buckets[h].append(len(lib));lib.append(d)
for n in [3,5,6,7,9,10,11,12,13,14,15]:add(nx.cycle_graph(n),f'cycle{n}')
for a in range(1,12):
 for b in range(a,12):
  for c in range(b,12):
   if a==b==1 or a+b+c>18:continue
   G=nx.Graph();label=2
   for L in [a,b,c]:
    chain=[0]+list(range(label,label+L-1))+[1];label+=L-1
    G.add_edges_from(zip(chain,chain[1:]))
   add(G,f'theta({a},{b},{c})')
for path in sorted((P/'cells').glob('*.txt')):
 for row,line in enumerate(path.read_text().splitlines()):
  nums=list(map(int,line.split()));n,t=nums[:2];G=nx.cycle_graph(n);G.add_edges_from(zip(nums[2::2],nums[3::2]));add(G,f'{path.name}:{row+1}')
G=nx.Graph([(5,0),(0,1),(1,6),(5,2),(2,3),(3,6),(5,4),(4,6),(0,2)]);add(G,'previous_E')
for i,d in enumerate(lib):
 d['id']=f'cell{i:04d}';del d['G']
(P/'catalog.json').write_text(json.dumps(lib,indent=2))
print('unique',len(lib),'seconds',time.time()-start)
print('arity',collections.Counter(len(d['terminals']) for d in lib))
print('fixed dilation survivors',collections.Counter(len(d['terminals']) for d in lib if not d['common_fixed_dilations']))
for d in lib:
 if len(d['terminals'])<=5 and not d['common_fixed_dilations']:
  print(d['id'],d['n'],len(d['terminals']),d['sources'][0], sorted(set(tuple(v) for v in d['pairs'].values())))
print('threepole all')
for d in lib:
 if len(d['terminals'])==3:print(d['id'],d['n'],d['sources'][0],d['common_fixed_dilations'],d['pairs'])
