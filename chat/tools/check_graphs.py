#!/usr/bin/env python3
"""Repeat selected direct counts and structural checks; writes only ignored fresh output.
Requires NetworkX and a C++17 compiler. Does not rerun discovery searches.
"""
import sys
if not __debug__:
    raise RuntimeError("Do not use python -O: input checks use assertions")
from pathlib import Path
from collections import Counter
import json,hashlib,subprocess,time,re,networkx as nx
R=Path(__file__).resolve().parents[1];W=R/'.verification-output'
W.mkdir(parents=True,exist_ok=True)
exe=W/'direct_cycle_counter'
subprocess.run(['c++','-O3','-std=c++17',str(R/'experiments/01-gadget-compression/direct_cycle_counter.cpp'),'-o',str(exe)],check=True)
records=[]
for p in sorted((R/'data/graphs').glob('*.edge')):
 lines=p.read_text().splitlines(); hdr=lines[0].split();n,m=map(int,hdr[2:]);G=nx.Graph();G.add_nodes_from(range(1,n+1))
 edges=[]
 for line in lines[1:]:
  if not line.strip() or line.startswith('c '):continue
  typ,a,b=line.split();assert typ=='e';a=int(a);b=int(b);assert 1<=a<=n and 1<=b<=n and a!=b;edges.append(tuple(sorted((a,b))))
 assert len(edges)==m and len(set(edges))==m;G.add_edges_from(edges)
 rec={'path':str(p.relative_to(R)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'vertices':n,'edges':m,'degree_histogram':dict(sorted(Counter(dict(G.degree()).values()).items())),'connected':nx.is_connected(G),'fresh_exact_cycle_counts':{},'fresh_count_status':{}}
 if n<1000:rec['vertex_connectivity']=nx.node_connectivity(G);rec['edge_connectivity']=nx.edge_connectivity(G)
 lengths=[4,8,16,32] if n<1000 else []
 if n==294:lengths=[4,8,16]
 if n==370:lengths=[4,8,16,32,33]
 if n in (32,40,64):lengths=[4,8,16,32]+([64]if n>=64 else [])
 if n==61:lengths=[4,8,16,32]
 for L in lengths:
  t=time.monotonic()
  try:
   cp=subprocess.run([str(exe),str(p),str(L)],capture_output=True,text=True,timeout=35)
   if cp.returncode:status='ERROR';v=None
   else:
    match=re.fullmatch(r'n=\d+ L=\d+ count=(\d+)\s*',cp.stdout)
    if match:v=int(match[1]);status='EXACT';rec['fresh_exact_cycle_counts'][str(L)]=v
    else:status='UNPARSED';v=None
   rec['fresh_count_status'][str(L)]={'status':status,'stdout':cp.stdout.strip(),'stderr':cp.stderr.strip(),'seconds':round(time.monotonic()-t,3)}
  except subprocess.TimeoutExpired:rec['fresh_count_status'][str(L)]={'status':'TIMEOUT_UNKNOWN','seconds':round(time.monotonic()-t,3)}
 if n==26550:rec['note']='Direct enumerator is capped at n<=10000; absence through 64 is checked by the separate exact structural verifier, not this direct count run.'
 records.append(rec)
 (W/'graph_checks.json').write_text(json.dumps(records,indent=2)+'\n')
 print(p.name,n,rec['degree_histogram'],rec['fresh_exact_cycle_counts'],flush=True)
