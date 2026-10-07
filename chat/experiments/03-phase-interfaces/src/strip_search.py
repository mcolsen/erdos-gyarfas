# Exact closure for the supplied finite action library. The retained run closes
# after 553 states. With a different library, finite termination is NOT promised.
from pathlib import Path
import json,itertools,time,collections
P=Path(__file__).parent
acts=json.loads((P/'transfers.json').read_text());pm=sum(1<<x for x in [4,8,16,32,64,128,256])
def ss(a,b):
 z=0
 while b:
  p=b&-b;z|=a<<(p.bit_length()-1);b-=p
 return z
def canon(A):
 p=sorted(range(3),key=lambda i:A[i]);return tuple(A[i] for i in p),p
states=[];known={};q=collections.deque();edges=[];start=time.time();ntested=nvalid=0
# Seed every split/orientation of every catalogue six-pole.
for ai,a in enumerate(acts):
 key,p=canon(a['R'])
 if key in known:continue
 s={'id':len(states),'A':key,'n':a['n'],'seed_action':ai,'permutation':p,'depth':1};known[key]=s['id'];states.append(s);q.append(s['id'])
seeds=len(states)
while q:
 si=q.popleft();s=states[si];A=s['A'];vc=0
 for ai,a in enumerate(acts):
  ntested+=1
  if any((ss(A[i],a['L'][i])<<2)&pm for i in range(3)):continue
  nvalid+=1;vc+=1;R=a['R'][:]
  for j in range(3):
   for i in range(3):R[j]|=ss(A[i],a['T'][i][j])<<2
  key,p=canon(R);edges.append([si,ai])
  if key in known:continue
  s2={'id':len(states),'A':key,'n':s['n']+a['n'],'parent':si,'action':ai,'permutation':p,'depth':s['depth']+1};known[key]=s2['id'];states.append(s2);q.append(s2['id'])
 if si%50==0:print(si,'seeds',seeds,'depth',s['depth'],'n',s['n'],'valid',vc,'total',len(states),'queue',len(q),'sec',round(time.time()-start,2),flush=True)
(P/'strip_states.json').write_text(json.dumps({'states':states,'edges':edges,'queue_remaining':list(q),'seeds':seeds,'ntested':ntested,'nvalid':nvalid},indent=2))
print('FINAL','seeds',seeds,'states',len(states),'tested',ntested,'valid',nvalid,'maxdepth',max(s['depth'] for s in states),'maxn',max(s['n'] for s in states),'queue',len(q),'sec',time.time()-start)
