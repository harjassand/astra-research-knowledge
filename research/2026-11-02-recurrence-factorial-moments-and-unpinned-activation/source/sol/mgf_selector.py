#!/usr/bin/env python3
"""A concrete raw-list receiver for the new multiplicative episode operation.

Admission here uses the ACCEPTED N1567 common-linkage-span binary corollary.
Other stable inputs return UNKNOWN. No finite exceptional radius, numerical
stationary moment value or practical mixing bound is emitted.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict,deque
import json
import sympy as sp
from mgf_envelope_certificate import acquire
from episode_diagnostics import rate,ordered,ack

P=Path(__file__).resolve().parent

def admitted_example():
    cycles=[[(0,0,0),(1,1,0),(1,0,1),(0,1,1)],
            [(1,0,0),(0,1,0),(0,0,1),(2,0,0)]]
    raw=[]
    for cycle in cycles:
        for j,y in enumerate(cycle):
            z=cycle[(j+1)%len(cycle)]
            raw.append((y,z,F(2 if y==(2,0,0) else 1)))
    return raw

def compile_receiver(raw,maxK=2**22):
    assert raw
    d=len(raw[0][0]);clean=[]
    for y,z,k in raw:
        assert len(y)==len(z)==d and all(type(a) is int and a>=0 for a in y+z) and k>0
        if y!=z:clean.append((y,z,F(k)))
    if not clean:return {'status':'FINITE_ABSORBING_ONLY'},None
    C=sorted({v for y,z,k in clean for v in [y,z]});adj=defaultdict(list);a=defaultdict(F)
    for i,(y,z,k) in enumerate(clean):adj[y].append((z,i));a[y]+=k
    paths={};reach={}
    for y in C:
        queue=deque([y]);back={y:None}
        while queue:
            v=queue.popleft()
            for w,i in adj[v]:
                if w not in back:back[w]=(v,i);queue.append(w)
        reach[y]=set(back)
        for z in back:
            word=[];v=z
            while back[v] is not None:u,i=back[v];word.append(i);v=u
            paths[y,z]=list(reversed(word))
    if any(y not in reach[z] for y,z,k in clean):return {'status':'UNKNOWN','reason':'not weakly reversible'},None
    linkages=[];unseen=set(C)
    while unseen:y=min(unseen);L=reach[y];linkages.append(sorted(L));unseen-=L
    if any(sum(y)>2 for y in C):return {'status':'UNKNOWN','reason':'this acquired admission uses the accepted binary common-span corollary'},None
    rank=lambda rows:sp.Matrix(rows).rank() if rows else 0
    fullrank=rank([tuple(b-a for a,b in zip(y,z)) for y,z,k in clean])
    lrank=[]
    for L in linkages:
        rr=rank([tuple(b-a for a,b in zip(y,z)) for y,z,k in clean if y in L]);lrank.append(rr)
    if any(r!=fullrank for r in lrank):return {'status':'UNKNOWN','reason':'some linkage does not span the full stoichiometric space','full_rank':fullrank,'linkage_ranks':lrank},None
    maxdepth=max(len(w) for w in paths.values());q=min(k/a[y] for y,z,k in clean);R=max(a.values())/min(a.values())
    cert=acquire(len(C),R,q,maxK=maxK,max_path_edges=maxdepth)
    if 'alpha_power_two_exponent' not in cert:return {'status':'UNKNOWN','reason':'scalar tilt not acquired within supplied finite budget','search':cert},None
    report={'status':'ADMITTED_AT_STATED_SCOPE','admission':'Accepted N1567 binary common-linkage-span corollary; new MGF envelope transfer is author-derived.',
            'dimension':d,'genuine_channels':len(clean),'complexes':C,'linkages':linkages,
            'full_stoichiometric_rank':fullrank,'linkage_ranks':lrank,'all_path_words':[
                {'from':y,'to':z,'word':w} for (y,z),w in sorted(paths.items())],
            'scalar_certificate':cert,
            'consequence':'Classwise fractional-factorial stationary moment beta=alpha/2 and a finite exponential moment of positive physical return time.',
            'not_acquired':['finite exceptional radius','numerical moment value','useful mixing rate','general weak-reversibility admission']}
    state={'raw':clean,'C':C,'a':a,'paths':paths,'reach':reach}
    return report,state

def select(state,x,t):
    assert all(a>=b for a,b in zip(x,t)) and t in state['C']
    z=tuple(a-b for a,b in zip(x,t));options=[]
    for c in sorted(state['reach'][t]):
        physical=tuple(a+b for a,b in zip(z,c))
        q=sum(rate(physical,y,k) for y,u,k in state['raw'])
        p=state['a'][c]*rate(physical,c,F(1))/q
        assert p>0
        options.append((p,c,physical))
    p,c,physical=min(options)
    # No exceptional-set test or huge probability threshold is needed to run this rule.
    return {'initial_population':x,'actual_carried_target':t,'residual':z,'selected_terminal':c,
            'acquired_word':state['paths'][t,c],'terminal_actual_population':physical,
            'terminal_source_probability_exact':str(p),
            'selection':'Exact minimum of actual terminal-source probabilities in the carried linkage.',
            'all_terminal_probabilities':[{'terminal':c0,'probability':str(p0)} for p0,c0,xx in options]}

if __name__=='__main__':
    raw=admitted_example();report,state=compile_receiver(raw);assert report['status']=='ADMITTED_AT_STATED_SCOPE'
    selections=[]
    for x,t in [((0,0,0),(0,0,0)),((10,0,0),(0,0,0)),((0,10,0),(0,0,0)),
                ((0,0,10),(0,0,0)),((10**100,10**100,10**100),(0,0,0)),
                ((10**6+2,10**6,10**6),(2,0,0))]:
        selections.append(select(state,x,t))
    stable_rejected=[((0,0),(1,0),F(1)),((1,0),(0,0),F(1)),((2,0),(1,1),F(1)),((1,1),(2,0),F(1))]
    neg,_=compile_receiver(stable_rejected);assert neg['status']=='UNKNOWN'
    high,_=compile_receiver(ordered());assert high['status']=='UNKNOWN'
    result={'scope':'An acquired raw-list sufficient receiver at exactly the accepted admission grammar; no global head enumeration.',
            'receiver':report,'actual_statewise_selections':selections,
            'negative_controls':[{'network':'stable detailed-balanced 0<->A,2A<->A+B','result':neg},
                                 {'network':'coupled ordered degree-seven obstruction','result':high}]}
    (P/'results/mgf_selector.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':report['status'],'alpha':report['scalar_certificate']['alpha_exact'],
                      'actual_statewise_selections':len(selections),'negative_control_statuses':[neg['status'],high['status']]},indent=2))
