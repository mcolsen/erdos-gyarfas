"""Independent checks of finite certificates and explicit boundary graphs.

No optimisation solver is required. The catalogue is independently checked for
validity and small-order completeness; full catalogue completeness additionally
uses the elementary suppression argument and the exhaustive generator supplied
in src/. All graphs use ordinary undirected simple-cycle semantics.
"""
from __future__ import annotations
from pathlib import Path
from itertools import combinations, combinations_with_replacement, permutations
from collections import Counter, defaultdict
import json, hashlib, time
import networkx as nx

P=Path(__file__).resolve().parent

def load(rel):return json.loads((P/rel).read_text())
def mask(vals):
    z=0
    for v in vals:z|=1<<v
    return z

def values(bits):
    while bits:
        t=bits&-bits;yield t.bit_length()-1;bits-=t

def add(a,b):
    z=0
    for v in values(b):z|=a<<v
    return z

def read_graph(path):
    g=nx.Graph();n=m=None
    for l in path.read_text().splitlines():
        z=l.split()
        if not z:continue
        if z[0]=='p':n,m=map(int,z[-2:]);g.add_nodes_from(range(1,n+1))
        elif z[0]=='e':
            u,v=map(int,z[1:]);assert u!=v and not g.has_edge(u,v);g.add_edge(u,v)
    assert len(g)==n and g.number_of_edges()==m
    return g

def graph(d):
    g=nx.Graph();g.add_nodes_from(range(d['n']));g.add_edges_from(d['edges']);return g

def support(g,u,v):
    if u==v:return 1
    return mask(len(q)-1 for q in nx.all_simple_paths(g,u,v))

def signature(g,ports):return tuple(support(g,*[ports[j] for j in range(3) if j!=i]) for i in range(3))
def has_power(lengths):return any(x>=4 and x&(x-1)==0 for x in lengths)
def edgekey(g):return frozenset(tuple(sorted(e)) for e in g.edges())


def verify_catalogue():
    cat=load('data/catalogue.json');byid={g['id']:g for g in cat};assert len(byid)==181
    bybucket=defaultdict(list);profiles={}
    for d in cat:
        g=graph(d);assert nx.is_biconnected(g)
        assert set(dict(g.degree()).values())<={2,3}
        assert sorted(d['terminals'])==sorted(v for v,t in g.degree if t==2)
        assert len(d['terminals'])==d['k'] and len(g)-d['k']<=6
        assert not has_power(map(len,nx.simple_cycles(g)))
        sp={tuple(x['pair']):mask(x['lengths']) for x in d['paths']}
        for u,v in combinations(sorted(d['terminals']),2):assert sp[u,v]==support(g,u,v)
        profiles[d['id']]=sp
        bucket=bybucket[len(g),d['k']]
        assert not any(nx.is_isomorphic(g,h) for h in bucket)
        bucket.append(g)
    # Disjoint enumeration control, supplied by NetworkX's graph atlas.
    atlas=[]
    for g in nx.graph_atlas_g():
        if len(g)<3 or not nx.is_biconnected(g):continue
        deg=list(dict(g.degree()).values());k=deg.count(2)
        if not set(deg)<={2,3} or not 3<=k<=7:continue
        if has_power(map(len,nx.simple_cycles(g))):continue
        atlas.append(g)
        assert any(nx.is_isomorphic(g,h) for h in bybucket[len(g),k])
    assert len(atlas)==sum(d['n']<=7 for d in cat)
    print('Catalogue:',len(cat),'valid distinct cells; atlas control:',len(atlas),flush=True)
    return cat,byid,profiles


def verify_inheritance(cat,profiles):
    cert=load('certificates/inheritance.json');counts=Counter();four_cases=0
    for row in cert:
        d=next(g for g in cat if g['id']==row['id'])
        full={v<<1 for v in profiles[d['id']].values()}
        minimal={s for s in full if not any(t!=s and t&s==t for t in full)}
        assert minimal=={mask(x) for x in d['minimal_supports']}
        counts[row['status']]+=1
        if row['status']=='direct_inheritance':
            assert row['factor'] in (1,2,4,8,16) and all(s>>row['factor']&1 for s in full)
        elif row['status']=='four_block_inheritance':
            assert row['factor'] in (1,2,4,8,16)
            for seq in combinations_with_replacement(sorted(minimal),4):
                z=1
                for s in seq:z=add(z,s)
                assert z>>(4*row['factor'])&1;four_cases+=1
        elif row['status']=='breaks_dyadic_C4':
            seq=row['escape']['contributions'];assert all(mask(s) in full for s in seq)
            z=1
            for s in seq:z=add(z,mask(s))
            assert list(values(z))==row['escape']['cycle_support'] and not has_power(values(z))
        else:assert row['status']=='unresolved_C4_pass'
    assert counts==Counter({'four_block_inheritance':149,'direct_inheritance':3,'breaks_dyadic_C4':22,'unresolved_C4_pass':7})
    print('Inheritance:',dict(counts),'; four-turn cases:',four_cases,flush=True)


def routing(d):
    g=graph(d);ts=sorted(d['terminals']);paths={}
    for uv in combinations(ts,2):paths[uv]=[(len(q)-1,frozenset(q)) for q in nx.all_simple_paths(g,*uv)]
    S={k:mask(length for length,_ in ps) for k,ps in paths.items()};T={}
    for left in combinations(ts,2):
        for right in combinations([v for v in ts if v not in left],2):
            lengths=set()
            for pairing in [right,right[::-1]]:
                for a,ua in paths[tuple(sorted([left[0],pairing[0]]))]:
                    for b,ub in paths[tuple(sorted([left[1],pairing[1]]))]:
                        if ua.isdisjoint(ub):lengths.add(a+b)
            T[left,right]=mask(lengths)
    return S,T


def action_profile(d,left,right,S,T):
    lp=[tuple(sorted(left[j] for j in range(3) if j!=i)) for i in range(3)]
    rp=[tuple(sorted(right[j] for j in range(3) if j!=i)) for i in range(3)]
    L=tuple(S[p] for p in lp);R=tuple(S[p] for p in rp);M=tuple(tuple(T[p,q] for q in rp) for p in lp)
    return L,R,M


def verify_transfer(cat,byid):
    acts=load('data/transfers.json');assert len(acts)==4668
    routes={d['id']:routing(d) for d in cat if d['k']==6};assert len(routes)==46
    actual=set()
    for a in acts:
        d=byid[a['cell']];S,T=routes[d['id']]
        assert set(a['left']).isdisjoint(a['right']) and sorted(a['left']+a['right'])==sorted(d['terminals'])
        L,R,M=action_profile(d,a['left'],a['right'],S,T)
        assert (L,R,M)==(tuple(a['L']),tuple(a['R']),tuple(map(tuple,a['T'])))
        actual.add((d['id'],L,R,M))
    expected=set()
    for name,(S,T) in routes.items():
        d=byid[name];ts=sorted(d['terminals'])
        for ls in combinations(ts,3):
            right=[v for v in ts if v not in ls]
            for left in permutations(ls):expected.add((name,*action_profile(d,left,right,S,T)))
    assert actual==expected and len(actual)==len(acts)
    data=load('certificates/strip_states.json');states=data['states'];assert len(states)==553 and data['seeds']==524 and not data['queue_remaining']
    bysig={tuple(s['A']):s['id'] for s in states};assert len(bysig)==553
    assert {tuple(sorted(a['R'])) for a in acts}=={tuple(s['A']) for s in states[:524]}
    models={};seen_graphs=set()
    for s in states:
        if 'seed_action' in s:
            a=acts[s['seed_action']];g=graph(byid[a['cell']]);ports=[a['right'][j] for j in s['permutation']]
        else:
            old,op=models[s['parent']];a=acts[s['action']];d=byid[a['cell']];off=len(old);g=old.copy()
            g.add_nodes_from(range(off,off+d['n']));g.add_edges_from((off+u,off+v) for u,v in d['edges'])
            g.add_edges_from((op[i],off+a['left'][i]) for i in range(3));ports=[off+a['right'][j] for j in s['permutation']]
        assert len(g)==s['n'] and signature(g,ports)==tuple(s['A'])
        ek=edgekey(g)
        if ek not in seen_graphs:assert not has_power(map(len,nx.simple_cycles(g)));seen_graphs.add(ek)
        models[s['id']]=(g,ports)
    print('Routing: all 4,668 actions checked independently; 553 representative graphs checked.',flush=True)
    rejection_path=P/'certificates/strip_rejections.bin'
    generate=not rejection_path.exists();codes=bytearray() if generate else rejection_path.read_bytes()
    if not generate:assert len(codes)==len(states)*len(acts)
    accepted=[];edge_set=set();pm=mask([4,8,16])
    for si,s in enumerate(states):
        A=s['A']
        for ai,a in enumerate(acts):
            ix=si*len(acts)+ai
            if generate:
                code=255
                for i in range(3):
                    bad=(add(A[i],a['L'][i])<<2)&pm
                    if bad:
                        power=next(values(bad));pi=[4,8,16].index(power)
                        oldlen=next(t for t in values(A[i]) if 0<=power-2-t and a['L'][i]>>(power-2-t)&1)
                        assert oldlen<16;code=(pi*3+i)*16+oldlen;break
                codes.append(code)
            else:code=codes[ix]
            if code!=255:
                block,oldlen=divmod(code,16);pi,i=divmod(block,3);assert pi<3
                other=[4,8,16][pi]-2-oldlen
                assert other>=0 and A[i]>>oldlen&1 and a['L'][i]>>other&1
            else:
                assert all(not (add(A[i],a['L'][i])<<2)&pm for i in range(3))
                R=a['R'][:]
                for j in range(3):
                    for i in range(3):R[j]|=add(A[i],a['T'][i][j])<<2
                target=bysig[tuple(sorted(R))];accepted.append([si,ai]);edge_set.add((si,target))
    if generate:rejection_path.write_bytes(codes)
    assert accepted==data['edges'] and len(accepted)==142 and len(edge_set)==37
    assert {u for u,v in edge_set}.isdisjoint({v for u,v in edge_set})
    print('Strip closure:',len(codes),'certified state/action checks;',len(accepted),'valid labelled transitions; no two-step transition.',flush=True)


def verify_extra_cell():
    extra=load('data/super6.json');assert len(extra)==1
    d=extra[0];g=graph(d)
    assert len(g)==18 and g.number_of_edges()==24 and nx.is_biconnected(g)
    assert set(dict(g.degree()).values())=={2,3}
    assert sorted(v for v,k in g.degree if k==2)==sorted(d['terminals'])
    assert not has_power(map(len,nx.simple_cycles(g)))
    z=iter((P/'certificates/glue77_survivors.txt').read_text().split());count=0
    while True:
        try:a=next(z)
        except StopIteration:break
        b=next(z);n,m=int(next(z)),int(next(z));es=[(int(next(z)),int(next(z))) for _ in range(m)]
        h=nx.Graph();h.add_nodes_from(range(n));h.add_edges_from(es)
        assert a==b=='b2_0_k7_0' and n==18 and m==24 and nx.is_isomorphic(g,h)
        assert not has_power(map(len,nx.simple_cycles(h)))
        count+=1
    assert count==8
    print('Four-link gluing: all 8 stored survivors checked; one 18-vertex six-port isomorphism class.',flush=True)


def polynomial_mul(a,b):
    c=Counter()
    for i,x in a.items():
        for j,y in b.items():c[i+j]+=x*y
    return c


def verify_rings(byid):
    d=byid['b2_0_k6_0'];g=graph(d)
    assert Counter(map(len,nx.simple_cycles(g)))=={5:1,6:1,7:1}
    polyA=Counter(len(p) for p in nx.all_simple_paths(g,5,7));polyB=Counter(len(p) for p in nx.all_simple_paths(g,2,6))
    assert polyA=={3:1,5:1,6:1} and polyB=={4:2,7:2}
    # Regression check of the all-scale theorem: among A/B assignments on a
    # dyadic ring, absence of the unique possible power is equivalent to one A.
    # The arbitrary-order proof uses the missing increment 1 in <2,3>.
    for r in (4,8,16,32):
        for a in range(r+1):
            z=Counter({0:1})
            for j in range(r):z=polynomial_mul(z,polyA if j<a else polyB)
            assert (not has_power(z))==(a==1)
    print('Phase rule: one A is the unique power-free A/B count on tested dyadic rings; all-order proof in note.',flush=True)
    out={}
    for r in (4,5,8):
        turns=[(5,7)]*r if r==5 else [(5,7)]+[(2,6)]*(r-1)
        h=nx.Graph();h.add_nodes_from(range(1,8*r+1))
        for j in range(r):h.add_edges_from((u+8*j+1,v+8*j+1) for u,v in d['edges'])
        for j in range(r):h.add_edge(turns[j][1]+8*j+1,turns[(j+1)%r][0]+8*((j+1)%r)+1)
        stored=read_graph(P/f'data/phase_ring_{r}.edge');assert edgekey(h)==edgekey(stored)
        assert Counter(dict(h.degree()).values())=={2:4*r,3:4*r} and nx.is_biconnected(h)
        predicted=Counter({0:1})
        for t in turns:predicted=polynomial_mul(predicted,polyA if t==(5,7) else polyB)
        predicted.update({5:r,6:r,7:r})
        direct=Counter(map(len,nx.simple_cycles(h)));assert direct==predicted and not has_power(direct)
        out[r]=h
        print(f'Ring {r}: n={len(h)}, {sum(direct.values())} cycles enumerated independently, circumference={max(direct)}, power-free; degree-two ports={4*r}.',flush=True)
    return out


def verify_repair_witnesses(rings):
    for r,g in rings.items():
        ports={v for v,d in g.degree if d==2};frozen_counts=[]
        for mode in (0,1):
            fn=P/f'certificates/gate_all_{r}_{mode}.txt';seen=set();legal=[]
            for l in fn.read_text().splitlines():
                z=l.split();a,b=map(int,z[1:3]);assert a<b and not g.has_edge(a,b)
                if mode==1:assert not set(g[a])&set(g[b])
                seen.add((a,b))
                if z[0]=='LEGAL':legal.append((a,b));continue
                L=int(z[3]);w=list(map(int,z[4:]));assert len(w)==len(set(w)) and w[0]==a and w[-1]==b
                assert len(w)-1==L-(mode==0) and L>=4 and L&(L-1)==0
                assert all(g.has_edge(x,y) for x,y in zip(w,w[1:]))
            eligible={(a,b) for a,b in combinations(sorted(g),2) if not g.has_edge(a,b) and (mode==0 or not set(g[a])&set(g[b]))}
            assert seen==eligible
            touched={v for e in legal for v in e if v in ports}
            if mode==0:
                # At least these many ports provably cannot receive any added edge.
                frozen_counts.append(len(ports-touched))
        # For a new vertex attached solely to old deficient ports, every pair
        # must be unblocked. A triangle-free over-approximation is enough.
        H=nx.Graph();H.add_nodes_from(ports);seen=set()
        for l in (P/f'certificates/gate_{r}_hub.txt').read_text().splitlines():
            z=l.split();a,b=map(int,z[1:3]);assert a in ports and b in ports and a<b;seen.add((a,b))
            if z[0]=='LEGAL':H.add_edge(a,b);continue
            L=int(z[3]);w=list(map(int,z[4:]));assert len(w)==len(set(w)) and w[0]==a and w[-1]==b
            assert len(w)-1==L-2 and L>=4 and L&(L-1)==0
            assert all(g.has_edge(x,y) for x,y in zip(w,w[1:]))
        assert seen==set(combinations(sorted(ports),2)) and sum(nx.triangles(H).values())==0
        # Stronger hub test: the neighbours may include already cubic vertices.
        H=nx.Graph();H.add_nodes_from(g);seen=set()
        for l in (P/f'certificates/gate_all_{r}_hub.txt').read_text().splitlines():
            z=l.split();a,b=map(int,z[1:3]);assert a in g and b in g and a<b;seen.add((a,b))
            if z[0]=='LEGAL':H.add_edge(a,b);continue
            L=int(z[3]);w=list(map(int,z[4:]));assert len(w)==len(set(w)) and w[0]==a and w[-1]==b
            assert len(w)-1==L-2 and L>=4 and L&(L-1)==0
            assert all(g.has_edge(x,y) for x,y in zip(w,w[1:]))
        assert seen==set(combinations(sorted(g),2))
        # Unblocked pairs form an over-approximation; this suffices for exclusion.
        cliques=[c for c in nx.find_cliques(H) if len(c)>=3]
        touched={v for c in cliques for v in c if v in ports}
        if r in (4,5):assert not cliques
        else:assert len(cliques)==4 and touched=={3,4,5}
        print(f'Repair witnesses, ring {r}: at least {frozen_counts[0]} edge-frozen ports; '
              f'at least {len(ports-touched)} ports cannot be touched by a new degree-three-or-higher hub '
              'even with cubic old neighbours.',flush=True)


def read_caps():
    z=iter((P/'data/caps_all.txt').read_text().split());n=int(next(z));rs=[]
    for _ in range(n):
        name=next(z);v,k,m=[int(next(z)) for _ in range(3)];ts=[int(next(z)) for _ in range(k)];es=[(int(next(z)),int(next(z))) for _ in range(m)]
        g=nx.Graph();g.add_nodes_from(range(v));g.add_edges_from(es)
        assert not has_power(map(len,nx.simple_cycles(g)))
        assert all(g.degree(x)+ts.count(x)==3 for x in g)
        rs.append((name,g,ts,{(i,j):support(g,ts[i],ts[j]) for i,j in combinations(range(k),2)}))
    assert len(rs)==184;return rs


def verify_cap_exclusions(rings):
    caps=read_caps();pm=mask([4,8,16,32,64])
    for r in (4,5):
        g=rings[r];ports=sorted(v for v,d in g.degree if d==2);d=len(ports);sp={}
        for u,v in combinations(ports,2):sp[u,v]=support(g,u,v)
        saved={tuple(map(int,z.split()[:2])):int(z.split()[2]) for z in (P/f'certificates/path_supports_{r}.txt').read_text().splitlines()}
        assert sp==saved
        compatibility={};records=[]
        for name,c,ts,cp in caps:
            for S in cp.values():
                if S in compatibility:continue
                adj=[0]*d
                for i,j in combinations(range(d),2):
                    if not (add(sp[ports[i],ports[j]],S)<<2)&pm:adj[i]|=1<<j;adj[j]|=1<<i
                compatibility[S]=adj
            assign=[];visited=0
            def search(used):
                nonlocal visited
                visited+=1;i=len(assign)
                if i==len(ts):return True
                avail=((1<<d)-1)&~used
                for j,v in enumerate(assign):avail&=compatibility[cp[j,i]][v]
                for v in values(avail):
                    assign.append(v)
                    if search(used|1<<v):return True
                    assign.pop()
                return False
            assert not search(0);records.append((name,visited))
        saved=load(f'certificates/cap_pair_screen_{r}.json')
        assert [(x['cap'],x['states']) for x in saved]==records and not any(x['feasible_pair_screen'] for x in saved)
        print('Cap exclusions, ring',r,': all 184 caps; independently verified path sets and',sum(v for _,v in records),'CSP prefix states.',flush=True)


def main():
    t=time.monotonic();cat,byid,profiles=verify_catalogue();verify_inheritance(cat,profiles);verify_transfer(cat,byid);verify_extra_cell()
    rings=verify_rings(byid);verify_repair_witnesses(rings);verify_cap_exclusions(rings)
    print('PASS; elapsed seconds:',round(time.monotonic()-t,3),flush=True)
if __name__=='__main__':main()
