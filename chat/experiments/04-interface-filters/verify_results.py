"""Verify cell spectra, uniform reductions, routing signatures, and completion exclusions.
Needs Python 3.10+ and NetworkX; no solver, compiler, or network access.
"""
from pathlib import Path
import json,itertools as it,collections,networkx as nx,sys,runpy,contextlib,io
P=Path(__file__).parent

def ispow(n):return n>=4 and n&(n-1)==0

def convolve(bits,support):
 out=0
 for v in support:out|=bits<<v
 return out

def verify_catalog():
 L=json.loads((P/'catalog.json').read_text());R={d['id']:d for d in json.loads((P/'screen.json').read_text())}
 uniform=escapes=0
 for d in L:
  G=nx.Graph();G.add_nodes_from(range(d['n']));G.add_edges_from(d['edges']);assert nx.is_connected(G)
  assert sorted(v for v,k in G.degree() if k==2)==d['terminals']
  assert all(k in [2,3] for v,k in G.degree())
  assert not any(ispow(len(c)) for c in nx.simple_cycles(G))
  for pair,s in d['pairs'].items():
   a,b=map(int,pair.split(','));assert sorted({len(p)-1 for p in nx.all_simple_paths(G,a,b)})==s
  rr=R[d['id']];minimal=rr['minimal_supports']
  assert all(any(set(s)<=set(x+1 for x in actual) for s in minimal) for actual in d['pairs'].values())
  for s in minimal:assert any(s==[x+1 for x in actual] for actual in d['pairs'].values())
  if rr['universal_four_block_factors']:
   c=rr['universal_four_block_factors'][0]
   assert c>=2 and c&(c-1)==0
   for ids in it.combinations_with_replacement(range(len(minimal)),4):
    b=1
    for i in ids:b=convolve(b,minimal[i])
    assert b>>(4*c)&1
   uniform+=1
  if rr['safe_four_turn_indices'] is not None:
   bits=1
   for i in rr['safe_four_turn_indices']:bits=convolve(bits,minimal[i])
   assert not any(bits>>q&1 for q in range(4,4*d['n']+1) if ispow(q));escapes+=1
 assert len(L)==554 and uniform==466 and escapes==86
 print('PASS: 554 cell spectra; 466 four-block reduction certificates; 86 genuine four-turn escapes')

def check_cycle(n,edges,cycle):
 assert len(cycle)==len(set(cycle)) and ispow(len(cycle))
 assert all(0<=x<n for x in cycle)
 assert all(tuple(sorted(e)) in edges for e in zip(cycle,cycle[1:]+cycle[:1]))

def verify_completion(path,special=False):
 d=json.loads(path.read_text());G=nx.Graph();G.add_nodes_from(range(d['n']));G.add_edges_from(d['backbone_edges']);B={tuple(sorted(e)) for e in G.edges()}
 assert sorted(d['terminals'])==sorted(v for v,k in G.degree() if k==2)
 assert all(k in [2,3] for v,k in G.degree())
 assert nx.number_of_selfloops(G)==0 and nx.is_connected(G)
 assert len(d['terminals'])%2==0 and len(d['terminals'])//2==d['required_for_cubic_completion']
 E=[tuple(e) for e in d['candidate_edges']];ES=set(E);discarded=set()
 for x in d['excluded_edges']:
  e=tuple(x['edge']);discarded.add(e);assert e not in ES and e not in B
  check_cycle(d['n'],B|{e},x['cycle'])
 all_possible={tuple(sorted(e)) for e in it.combinations(d['terminals'],2) if tuple(sorted(e)) not in B}
 assert ES.isdisjoint(discarded) and ES|discarded==all_possible
 C=set()
 for x in d['conflicts']:
  i,j=x['indices'];C.add(tuple(sorted((i,j))))
  if x.get('reason')=='shared_endpoint':assert len(set(E[i]+E[j]))<4
  else:check_cycle(d['n'],B|{E[i],E[j]},x['cycle'])
 if special:
  assert all(any(tuple(sorted(p)) in C for p in it.combinations(t,2)) for t in it.combinations(range(len(E)),3));bound=2
 else:
  groups=d['clique_cover'];assert set(it.chain.from_iterable(groups))==set(range(len(E)))
  for group in groups:assert all(tuple(sorted(p)) in C for p in it.combinations(group,2))
  bound=len(groups)
 assert bound==d['claimed_upper_bound'] and bound<d['required_for_cubic_completion']
 print('PASS:',path.name,'completion edges at most',bound,'but',d['required_for_cubic_completion'],'needed')

def verify_routes():
 old=json.loads((P/'routing_states.json').read_text())
 with contextlib.redirect_stdout(io.StringIO()):runpy.run_path(str(P/'routing_states.py'))
 assert json.loads((P/'routing_states.json').read_text())==old
 print('PASS: all 306 hexagon/heptagon single-, double-, and triple-path routing states')

def verify_ledgers():
 for mode,count in [('double',4064),('triple',43583)]:
  with contextlib.redirect_stdout(io.StringIO()):z=runpy.run_path(str(P/('double_necklaces.py' if mode=='double' else 'triple_links.py')))
  lib={d['id']:d for d in json.loads((P/'catalog.json').read_text())};S=z['S']
  rows=json.loads((P/f'{mode}_triangle_ledger.json').read_text());assert len(rows)==count
  observed=collections.Counter()
  for row in rows:
   states=[S[k] for k in row['state_ids']];offs=[0]
   for st in states:offs.append(offs[-1]+lib[st[0]]['n'])
   E={tuple(sorted((a+offs[i],b+offs[i]))) for i,st in enumerate(states) for a,b in lib[st[0]]['edges']}
   for i in range(3):
    k=2 if mode=='double' else 3
    perm=[a^row['swaps'][i] for a in range(k)] if mode=='double' else row['permutations'][i]
    for j in range(k):E.add(tuple(sorted((offs[i]+states[i][3][j],offs[(i+1)%3]+states[(i+1)%3][2][perm[j]]))))
   assert len(row['witness'])==row['forbidden_length'];check_cycle(offs[-1],E,row['witness']);observed[row['forbidden_length']]+=1
  expected={8:4040,16:24} if mode=='double' else {8:43461,16:122}
  assert dict(observed)==expected
  print('PASS:',mode,count,'explicit assembly-rejection witnesses')

if __name__=='__main__':
 verify_catalog();verify_routes()
 verify_completion(P/'completions/hep56_certificate.json',True)
 verify_completion(P/'completions/hex60_certificate.json')
 verify_completion(P/'completions/gap88_oracle_certificate.json')
 verify_ledgers()
 runpy.run_path(str(P/'verify_composition_examples.py'),run_name='__main__')
 print('ALL CHECKS PASSED')
