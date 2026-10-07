from pathlib import Path
import json,itertools,networkx as nx,time
P=Path(__file__).parent

def ss(a,b):
 z=0
 while b:
  t=b&-b;z|=a<<(t.bit_length()-1);b-=t
 return z

def readcaps():
 z=iter((P/'caps_all.txt').read_text().split());num=int(next(z));rs=[]
 for _ in range(num):
  name=next(z);n,k,m=[int(next(z)) for _ in range(3)];ts=[int(next(z)) for _ in range(k)];es=[(int(next(z)),int(next(z))) for _ in range(m)];G=nx.Graph(es);G.add_nodes_from(range(n));sp={}
  for i,j in itertools.combinations(range(k),2):
   lengths={0} if ts[i]==ts[j] else {len(p)-1 for p in nx.all_simple_paths(G,ts[i],ts[j])}
   sp[i,j]=sum(1<<v for v in lengths)
  rs.append({'id':name,'n':n,'k':k,'ports':ts,'edges':es,'sp':sp})
 return rs
caps=readcaps()
for r in (4,5):
 paths={tuple(map(int,l.split()[:2])):int(l.split()[2]) for l in (P/f'rings/path_supports_{r}.txt').read_text().splitlines()}
 ts=sorted(set(v for e in paths for v in e));d=len(ts);compat={};pm=sum(1<<p for p in (4,8,16,32,64))
 for c in caps:
  for m in c['sp'].values():
   if m in compat:continue
   adj=[0]*d
   for i,j in itertools.combinations(range(d),2):
    if not (ss(paths[ts[i],ts[j]],m)<<2)&pm:adj[i]|=1<<j;adj[j]|=1<<i
   compat[m]=adj
 records=[]
 for c in caps:
  k=c['k'];assign=[];nodes=[0];solutions=[]
  def rec(used):
   nodes[0]+=1;i=len(assign)
   if i==k:solutions.append([ts[j] for j in assign]);return True
   avail=((1<<d)-1)&~used
   for j,v in enumerate(assign):avail&=compat[c['sp'][j,i]][v]
   while avail:
    bit=avail&-avail;v=bit.bit_length()-1;avail-=bit;assign.append(v)
    if rec(used|bit):return True
    assign.pop()
   return False
  feasible=rec(0);records.append({'cap':c['id'],'feasible_pair_screen':feasible,'states':nodes[0],'witness':solutions[:1]})
 print('ring',r,'caps',len(records),'pair-screen positive',sum(x['feasible_pair_screen'] for x in records),'prefix states',sum(x['states'] for x in records),flush=True)
 print([x for x in records if x['feasible_pair_screen']],flush=True)
 (P/f'rings/cap_pair_screen_{r}.json').write_text(json.dumps(records,indent=2))
