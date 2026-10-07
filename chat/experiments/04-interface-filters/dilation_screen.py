import json,itertools as it,collections,time,functools
from pathlib import Path
P=Path(__file__).parent
lib=json.loads((P/'catalog.json').read_text())
def mask(xs):return sum(1<<x for x in xs)
def conv(m,xs):
 out=0
 for x in xs:out|=m<<x
 return out

def supports(d):
 ss=sorted(set(tuple(x+1 for x in s) for s in d['pairs'].values()),key=lambda a:(len(a),a))
 keep=[]
 for s in ss:
  if not any(set(q)<=set(s) for q in keep):keep.append(s)
 return keep
@functools.lru_cache(maxsize=200000)
def four(a,b,c,d):return conv(conv(conv(mask(a),b),c),d)
res=[];start=time.time()
for d in lib:
 ss=supports(d);r4=list(it.combinations_with_replacement(range(len(ss)),4))
 common=None;escape=None
 for ids in r4:
  val=four(*(ss[i] for i in ids));common=val if common is None else common&val
  if escape is None:
   powers=[1<<k for k in range(2,(4*d['n']).bit_length())]
   if not any(val>>q&1 for q in powers):escape=list(ids)
 # common sum at r4 -> block dilation c=common/4
 fixed4=[c for c in [2,4,8,16,32] if common>>(4*c)&1]
 # Some modular anti-dilation homogeneous turn
 modular=[]
 for i,s in enumerate(ss):
  import math
  g=math.gcd(*s);odd=g
  while odd and odd%2==0:odd//=2
  if odd>1:modular.append({'support':s,'odd_divisor':odd})
 res.append({'id':d['id'],'n':d['n'],'arity':len(d['terminals']),'minimal_supports':ss,'universal_four_block_factors':fixed4,'safe_four_turn_indices':escape,'modular_escape_turns':modular})
(P/'screen.json').write_text(json.dumps(res,indent=2))
print('seconds',time.time()-start,'catalog',len(res),'cache',four.cache_info())
print('certified fourblock',sum(bool(d['universal_four_block_factors']) for d in res))
print('r4 escape',sum(d['safe_four_turn_indices'] is not None for d in res),'modular',sum(bool(d['modular_escape_turns']) for d in res))
print('survivors <=7ports')
for d in res:
 if not d['universal_four_block_factors'] and d['arity']<=7:
  print(d['id'],d['n'],d['arity'],'r4escape',d['safe_four_turn_indices'],'modular',d['modular_escape_turns'])
