"""Independent integer/graph checks. No SAT or optimization solver required.

Finite certificates underpin the all-orders proofs in RESEARCH.md. Bounded
search logs verify rejected assignments and learning rules, not UNSAT claims.
"""
from pathlib import Path
from itertools import combinations,combinations_with_replacement,product
from functools import lru_cache
from collections import Counter
import argparse,gzip,hashlib,json,time
import networkx as nx
P=Path(__file__).resolve().parent

def pow2(n):return n>=4 and n&(n-1)==0

def sumset(sets):
    acc={0}
    for ss in sets:acc={a+b for a in acc for b in ss}
    return acc

def check_cycle(G,cycle):
    assert pow2(len(cycle)) and len(set(cycle))==len(cycle)
    assert all(G.has_edge(a,b)for a,b in zip(cycle,cycle[1:]+cycle[:1]))

def verify_catalogue():
    catalog=json.loads((P/'data/catalog.json').read_text())
    screen={d['id']:d for d in json.loads((P/'data/screen.json').read_text())}
    counts=Counter()
    for d in catalog:
        G=nx.Graph();G.add_nodes_from(range(d['n']));G.add_edges_from(d['edges'])
        assert nx.is_connected(G) and all(v in(2,3)for _,v in G.degree())
        assert sorted(v for v,k in G.degree()if k==2)==d['terminals']
        assert not any(pow2(len(c))for c in nx.simple_cycles(G))
        supports=set()
        for a,b in combinations(d['terminals'],2):
            pathset={len(p)-1 for p in nx.all_simple_paths(G,a,b)}
            assert pathset==set(d['pairs'][f'{a},{b}'])
            supports.add(tuple(sorted(x+1 for x in pathset)))
        minimal=sorted((s for s in supports if not any(set(t)<set(s)for t in supports)),key=lambda x:(len(x),x))
        item=screen[d['id']]
        assert {tuple(s)for s in item['minimal_supports']}==set(minimal)
        if item['universal_four_block_factors']:
            for factor in item['universal_four_block_factors']:
                assert pow2(4*factor)
                for turns in combinations_with_replacement(item['minimal_supports'],4):
                    assert 4*factor in sumset(turns)
            counts['four_block']+=1
        elif item['safe_four_turn_indices'] is not None:
            turns=[item['minimal_supports'][i]for i in item['safe_four_turn_indices']]
            assert not any(pow2(n)for n in sumset(turns))
            counts['explicit_escape']+=1
        else:
            assert d['id']in('cell0001','cell0095');counts['variable_factor']+=1
    assert dict(counts)=={'four_block':466,'variable_factor':2,'explicit_escape':86},counts
    print('Catalogue:',len(catalog),'graphs, ALL internal cycles and terminal-path supports checked;',dict(counts),flush=True)
    return {d['id']:d for d in catalog}

def verify_u11():
    cert=json.loads((P/'certificates/u11_variable_dilation.json').read_text())
    supports=cert['minimal_contribution_supports'];bad=tuple(cert['sole_bad_four_block'])
    good={tuple(w['turns']):w['contributions']for w in cert['good_four_blocks']}
    quads=list(combinations_with_replacement(range(8),4))
    assert len(quads)==330 and len(good)==329 and bad==(1,3,3,3)
    for q in quads:
        available=sumset(supports[i]for i in q)
        assert (32 in available)==(q in good)
        if q in good:assert sum(good[q])==32 and all(v in supports[i]for i,v in zip(q,good[q]))
    partners=[]
    for rec in cert['repairs']:
        q=tuple(rec['partner']);a,b=map(tuple,rec['replacement'])
        assert a in good and b in good and Counter(q+bad)==Counter(a+b)
        partners.append(q)
    assert sorted(partners)==[q for q in quads if q!=(3,3,3,3)]
    # All finite exceptional-form tests are supplementary, not the unbounded proof.
    for r in range(4,257,4):
        assert 3+5+4*(r-2)==4*r
        assert 3 in supports[1] and all(x in supports[3]for x in(4,5))
    print('U11: 330 four-block supports; 329 good witnesses; 329 partition repairs checked.',flush=True)

def verify_heptagon():
    cert=json.loads((P/'certificates/heptagon_profiles.json').read_text());total=0
    for row in cert['rows']:
        k=row['k'];r=row['r'];assert r==2**k
        safe=[];checked=0
        for a in range(r+1):
            for b in range(r-a+1):
                c=r-a-b;target=2*a+b
                # Independent bounded-Diophantine checker, NOT the polynomial builder.
                realize4=any(max(0,-((-(target-5*x-c))//3))<=min(b,(target-5*x)//3) for x in range(a+1))
                realize2=(a==r)
                if not realize4 and not realize2:safe.append([a,b,c])
                checked+=1
        expected=sorted([[0,r,0],[r-1,1,0],[r-2,0,2]]if k%2==0 else [[0,r,0],[r-2,2,0],[r-1,0,1]])
        assert sorted(safe)==expected==sorted(row['safe_profiles']),(r,safe,expected)
        assert checked==row['profiles_checked'];total+=checked
    assert total==11304==cert['total_profiles']
    # Base cases of the interval-fill induction used in the proof.
    assert set(range(3,10))<=sumset([{0,5},{0,3,6},{0,1}])
    assert set(range(8,15))<=sumset([{0,5,10},{0,3,6,9,12}])
    print('Heptagon: all',total,'profiles at r=4,8,16,32,64,128 agree with the all-orders case proof.',flush=True)

def verify_pentagon():
    for k in range(2,11):
        r=2**k
        for b in range(r+1):
            if b==0:assert 2*r==2*(r-b);continue
            # Independently solve the equation of the preceding variable-factor proof.
            assert any(0<=2*r-b-3*x<=b for x in range(r-b+1))
    print('Pentagon variable-factor arithmetic: regression through r=1024 checked.',flush=True)

def verify_motif(catalog):
    c=json.loads((P/'certificates/universal_three_cell_witnesses.json').read_text());seen=set();counts=Counter()
    for w in c['witnesses']:
        chosen=w['cells'];offsets=[0];G=nx.Graph()
        for i,did in enumerate(chosen):
            d=catalog[did];offset=offsets[-1]
            G.add_nodes_from(range(offset,offset+d['n']));G.add_edges_from((a+offset,b+offset)for a,b in d['edges']);offsets.append(offset+d['n'])
        def port(i,p):return offsets[i]+catalog[chosen[i]]['terminals'][p]
        G.add_edges_from([(port(0,6),port(2,2)),(port(2,3),port(1,4)),(port(1,1),port(0,5))])
        check_cycle(G,w['cycle']);assert len(w['cycle'])==w['length']
        seen.add(tuple(chosen));counts[w['length']]+=1
    assert seen==set(product(c['options'],repeat=3)) and len(c['witnesses'])==1331
    print('Universal three-link motif:',len(seen),'full graph assignments reconstructed; witnesses',dict(counts),flush=True)

def verify_contraction_run(directory):
    model=json.loads((directory/'model.json').read_text());B=nx.Graph();B.add_nodes_from(range(model['base_n']));B.add_edges_from(model['base_edges'])
    terminals=set(model['terminals']);X={(a,b):v for a,b,v in model['variables']};index={v:(a,b)for (a,b),v in X.items()}
    assert terminals=={v for v,d in B.degree()if d==2}
    assert set(X)=={(a,b)for a,b in combinations(sorted(terminals),2)if not B.has_edge(a,b)}
    @lru_cache(None)
    def quotient(matching):
        mate={u:v for a,b in matching for u,v in((a,b),(b,a))}
        assert set(mate)==terminals and len(matching)*2==len(mate)
        for e in matching:assert e in X
        reps=[min(v,mate.get(v,v))for v in B];ids={v:i for i,v in enumerate(sorted(set(reps)))};mp=[ids[v]for v in reps]
        G=nx.Graph();G.add_nodes_from(range(len(ids)));G.add_edges_from((mp[a],mp[b])for a,b in B.edges())
        assert nx.number_of_selfloops(G)==0 and len(G)==model['final_n'] and nx.is_connected(G)
        assert min(dict(G.degree()).values())>=3
        positive={X[e]for e in matching}
        assert all(any((lit>0)==(abs(lit)in positive)for lit in clause)for clause in model['degree_clauses'])
        return mp,G,positive
    path=directory/'witnesses.jsonl.gz';count=0;lengths=Counter();maxguards=0;totalguards=0
    with gzip.open(path,'rt')as f:
        for line in f:
            w=json.loads(line);matching=tuple(map(tuple,w['matching']));mp,G,pos=quotient(matching)
            cyc=w['cycle'];check_cycle(G,cyc);lengths[len(cyc)]+=1
            oriented=w['oriented_base_edges'];assert len(oriented)==len(cyc)
            for i,(u,v)in enumerate(oriented):assert B.has_edge(u,v)and(mp[u],mp[v])==(cyc[i],cyc[(i+1)%len(cyc)])
            groups=[sorted(set([oriented[i-1][1],e[0]]))for i,e in enumerate(oriented)]
            assert groups==w['groups'] and len(set(v for g in groups for v in g))==sum(map(len,groups))
            required={X[tuple(g)]for g in groups if len(g)==2}
            collisions={X[tuple(sorted((u,v)))]for i,j in combinations(range(len(groups)),2)for u in groups[i]for v in groups[j]if tuple(sorted((u,v)))in X}
            assert required==set(w['required']) and collisions==set(w['collisions'])
            assert set(w['clause'])=={-x for x in required}|collisions
            assert required<=pos and not collisions&pos
            count+=1;maxguards=max(maxguards,len(collisions));totalguards+=len(collisions)
    result=json.loads((directory/'result.json').read_text())
    assert count==result['clauses'] and {str(k):v for k,v in lengths.items()}==result['cycle_clauses_by_length']
    assert quotient.cache_info().misses==result['rounds']
    assert maxguards==result['max_collision_literals']and totalguards==result['total_collision_literals']
    assert result['status'].startswith('UNKNOWN')
    print(directory.name+':',result['rounds'],'degree-complete candidate graphs,',count,'collision-guarded rejection witnesses checked; status',result['status'],flush=True)
    return count

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--skip-search-logs',action='store_true');args=parser.parse_args()
    start=time.time();catalog=verify_catalogue();verify_u11();verify_heptagon();verify_pentagon();verify_motif(catalog)
    if not args.skip_search_logs:
        total=sum(verify_contraction_run(P/'runs'/name)for name in('contract_H56','contract_X60','contract_R64'))
        assert total==67272
    print('VERIFIED. Elapsed seconds:',round(time.time()-start,3),flush=True)
if __name__=='__main__':main()
