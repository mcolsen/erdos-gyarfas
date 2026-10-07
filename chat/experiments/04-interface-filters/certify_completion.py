from pathlib import Path
import json,networkx as nx,itertools as it,subprocess
P=Path(__file__).parent;D=P/'completions'
for name in ['hep56','hex60']:
 G=nx.Graph();lines=(D/f'{name}_backbone.edge').read_text().splitlines();n=int(lines[0].split()[2]);G.add_nodes_from(range(n));G.add_edges_from((int(w[1])-1,int(w[2])-1) for l in lines[1:] if (w:=l.split())[0]=='e')
 terms=[v for v in G if G.degree(v)==2]
 E=[tuple(map(int,l.split())) for l in (D/f'{name}_compatible.txt').read_text().splitlines()]
 C=set(tuple(map(int,l.split())) for l in (D/f'{name}_conflicts.txt').read_text().splitlines())
 H=nx.Graph();H.add_nodes_from(range(len(E)));H.add_edges_from(C)
 colors=nx.coloring.greedy_color(nx.complement(H),strategy='saturation_largest_first')
 groups=[[i for i in H if colors[i]==c] for c in range(max(colors.values())+1)]
 if name=='hep56':needed=sorted(C)
 else:needed=sorted({tuple(sorted((a,b))) for gp in groups for a,b in it.combinations(gp,2)})
 requests=[];excluded=[];checkedconf=[];Eset=set(E)
 for a,b in it.combinations(terms,2):
  if G.has_edge(a,b) or (a,b) in Eset:continue
  excluded.append({'edge':[a,b],'request':len(requests)});requests.append([(a,b)])
 for i,j in needed:
  if len(set(E[i]+E[j]))<4:checkedconf.append({'indices':[i,j],'reason':'shared_endpoint'})
  else:checkedconf.append({'indices':[i,j],'request':len(requests)});requests.append([E[i],E[j]])
 qpath=D/f'{name}_witness_requests.txt';qpath.write_text(''.join(str(i)+' '+str(len(e))+' '+' '.join(str(x) for ab in e for x in ab)+'\n' for i,e in enumerate(requests)))
 run=subprocess.run([str(P/'path_witness'),str(D/f'{name}_backbone.edge'),str(qpath)],capture_output=True,text=True,check=True,timeout=15)
 W={}
 for row in run.stdout.splitlines():
  vals=list(map(int,row.split()));idx,L=vals[:2];assert L>0
  cyc=vals[2:];assert len(cyc)==L and len(set(cyc))==L and (L&(L-1))==0
  edges=set(tuple(sorted(e)) for e in G.edges())|set(tuple(sorted(e)) for e in requests[idx])
  assert all(tuple(sorted(e)) in edges for e in zip(cyc,cyc[1:]+cyc[:1]));W[idx]=cyc
 assert len(W)==len(requests)
 for e in excluded:e['cycle']=W[e.pop('request')]
 for e in checkedconf:
  if 'request' in e:e['cycle']=W[e.pop('request')]
 cert={'n':n,'backbone_edges':list(G.edges()),'terminals':terms,'candidate_edges':E,'excluded_edges':excluded,'conflicts':checkedconf,'clique_cover':groups,'claimed_upper_bound':2 if name=='hep56' else len(groups),'required_for_cubic_completion':len(terms)//2}
 (D/f'{name}_certificate.json').write_text(json.dumps(cert,indent=2))
 if name=='hep56':assert all(any(tuple(sorted(e)) in C for e in it.combinations(t,2)) for t in it.combinations(range(len(E)),3))
 print(name,'cycle_witnesses',len(W),'upperbound',cert['claimed_upper_bound'],'required',len(terms)//2)
