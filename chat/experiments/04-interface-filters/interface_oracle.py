"""Exact simple-cycle supports for the three documented necklace templates.
Nonempty `new` must be a matching of new edges between free degree-2 ports.
The result covers cycles using ALL specified new edges. With `new=[]`, it
covers the ring-traversing cycles only (not cycles internal to a base cell).
No truncation, randomization, path budget, or full-graph cycle DFS is used.
"""
from functools import lru_cache
from itertools import combinations,product
from collections import defaultdict
import networkx as nx


def pairings(xs):
    if not xs:
        yield ();return
    a=xs[0]
    for j in range(1,len(xs)):
        b=xs[j]
        for rest in pairings(xs[1:j]+xs[j+1:]):
            yield ((a,b),)+rest

class NecklaceOracle:
    def __init__(self,m,r):
        if m not in (6,7,11) or not isinstance(r,int) or r < 3:
            raise ValueError('Supported cell orders are 6, 7, 11; require r >= 3.')
        self.m,self.r=m,r
        self.cell=nx.cycle_graph(m)
        if m==11:self.cell.add_edges_from([(0,2),(5,7)])
        self.terminals=[v for v in self.cell if self.cell.degree(v)==2]
        self.entry=[3 if m==11 else 0]*r
        self.exit=[8 if m==11 else (2 if m==7 or i==0 else 3) for i in range(r)]
        self.ring=[((i,self.exit[i]),((i+1)%r,self.entry[(i+1)%r])) for i in range(r)]
        self.base=nx.Graph()
        for i in range(r):self.base.add_edges_from((m*i+a,m*i+b) for a,b in self.cell.edges())
        self.base.add_edges_from((m*i+a,m*j+b) for (i,a),(j,b) in self.ring)
        self.free=sorted(v for v,d in self.base.degree() if d==2)
        self.paths={}
        for a,b in combinations(self.terminals,2):
            self.paths[(a,b)]=[(tuple(p),sum(1<<v for v in p)) for p in nx.all_simple_paths(self.cell,a,b)]
        self.routes=lru_cache(None)(self._routes)

    def _routes(self,pairs):
        out={}
        def visit(i,seen,ps,total):
            if i==len(pairs):out.setdefault(total,tuple(ps));return
            for p,mask in self.paths[pairs[i]]:
                if mask&seen==0:visit(i+1,seen|mask,ps+[p],total+len(p)-1)
        visit(0,0,[],0)
        return out

    def configurations(self,new):
        links=self.ring+[(divmod(a,self.m),divmod(b,self.m)) for a,b in new]
        parity=[0]*self.r
        for (i,_),(j,_) in links[self.r:]:parity[i]^=1;parity[j]^=1
        # The cycle-space equations for the ring have exactly two solutions.
        for last in [0,1]:
            ringbits=[];prev=last
            for i in range(self.r):prev^=parity[i];ringbits.append(prev)
            assert ringbits[-1]==last
            active=[i for i,v in enumerate(ringbits) if v]+list(range(self.r,len(links)))
            if not active:continue
            ends=defaultdict(list);external=[]
            for e in active:
                a,b=links[e];ends[a[0]].append(a[1]);ends[b[0]].append(b[1]);external.append((a,b))
            if any(len(set(v))!=len(v) for v in ends.values()):raise ValueError('Repeated port')
            cells=sorted(ends);options=[]
            for i in cells:
                o=[]
                for pp in pairings(sorted(ends[i])):
                    rr=self.routes(pp)
                    if rr:o.append((pp,rr))
                options.append(o)
            for choice in product(*options):
                # Pairings plus external links must form ONE circuit, not several.
                step=defaultdict(list)
                for a,b in external:step[a].append(b);step[b].append(a)
                for i,(pp,_) in zip(cells,choice):
                    for a,b in pp:step[(i,a)].append((i,b));step[(i,b)].append((i,a))
                assert all(len(v)==2 for v in step.values())
                seen=set();stack=[next(iter(step))]
                while stack:
                    v=stack.pop()
                    if v in seen:continue
                    seen.add(v);stack.extend(step[v])
                if len(seen)!=len(step):continue
                yield external,cells,choice

    def spectrum(self,new,find_power=False):
        new=[tuple(e) for e in new]
        flat=[v for e in new for v in e]
        if (any(len(e)!=2 for e in new) or len(set(flat))!=len(flat)
                or any(v not in self.free for v in flat)
                or any(self.base.has_edge(*e) for e in new)):
            raise ValueError('New edges must form a nonedge matching on free ports.')
        spectrum=0
        for external,cells,choice in self.configurations(new):
            bits=1<<len(external)
            for _,rr in choice:
                nb=0
                for length in rr:nb|=bits<<length
                bits=nb
            spectrum|=bits
            if find_power:
                p=4
                while p <= len(self.base):
                    if bits>>p&1:return self._witness(external,cells,choice,p)
                    p*=2
        return None if find_power else spectrum

    def _witness(self,external,cells,choice,length):
        dp={len(external):[]}
        for _,rr in choice:
            nd={}
            for total,selected in dp.items():
                for q in rr:
                    if total+q<=length:nd.setdefault(total+q,selected+[q])
            dp=nd
        chosen=dp[length];G=nx.Graph()
        G.add_edges_from((self.m*i+a,self.m*j+b) for (i,a),(j,b) in external)
        for i,(_,rr),q in zip(cells,choice,chosen):
            for path in rr[q]:G.add_edges_from((self.m*i+a,self.m*i+b) for a,b in zip(path,path[1:]))
        assert nx.is_connected(G) and all(d==2 for v,d in G.degree()) and len(G)==length
        start=next(iter(G));cyc=[start];prev=-1;u=start
        while True:
            v=next(v for v in G[u] if v!=prev)
            if v==start:break
            cyc.append(v);prev,u=u,v
        assert len(cyc)==length
        return cyc
