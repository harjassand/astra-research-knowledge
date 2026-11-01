#!/usr/bin/env python3
"""Independent raw instances, receiving, ties, rate extremes and exact tampering."""
from fractions import Fraction as F
from itertools import product,permutations
from pathlib import Path
import importlib.util,json,sys
import independent_multipartite_receiver as I
import multipartite_mechanism_checks as M
HERE=Path(__file__).resolve().parent
BASE=HERE.parent if (HERE.parent/'multipartite_seed.py').exists() else HERE.parent/'stochastic_multipartite_seed_pending_20261031'
sp=importlib.util.spec_from_file_location('candidate_multipartite',BASE/'multipartite_seed.py');C=importlib.util.module_from_spec(sp);sp.loader.exec_module(C)

def paths(x,p=()):
    if isinstance(x,dict):
        for k,v in x.items():yield from paths(v,p+(k,))
    elif isinstance(x,(tuple,list)):
        for k,v in enumerate(x):yield from paths(v,p+(k,))
    else:yield p,x

def change(x,p,v):
    if not p:return v
    k=p[0]
    if isinstance(x,dict):z=dict(x);z[k]=change(z[k],p[1:],v);return z
    z=list(x);z[k]=change(z[k],p[1:],v);return tuple(z) if isinstance(x,tuple) else z

def mutation(v):
    if type(v) in (int,F):return v+1
    if type(v) is str:return v+'!'
    if v is None:return 'changed'
    raise AssertionError(type(v))

def build_graph(n,edges):
    def z(*ids):return tuple(ids.count(i) for i in range(n))
    hubs=[z(i,j) for i,j in edges];raw=[(z(),z(0),F(1)),(z(0),z(),F(1))]
    for h in hubs:
        raw.extend([(z(0,0),h,F(1)),(h,z(0,0),F(1))])
        for x in range(1,n):raw.extend([(z(0,x),h,F(1)),(h,z(0,x),F(1))])
    return raw

def main():
    triangle=M.fixture([(1,),(2,),(3,)],sparse=True)
    triangle['raw']=[(u,v,F(2) if u==(0,1,1,0) and v==(1,1,0,0) else k) for u,v,k in triangle['raw']]
    cases=[('sparse_nonCB_triangle',triangle,4),
      ('K211_sparse',M.fixture([(1,2),(3,),(4,)],varied=True,sparse=True),3),
      ('K4_sparse',M.fixture([(1,),(2,),(3,),(4,)],t=F(101,100),sparse=True),3),
      ('K22',M.fixture([(1,2),(3,4)],t=F(5),varied=True),3),
      ('K11',M.fixture([(1,),(2,)],varied=True,t=F(3,2)),4)]
    out=[];ordinary=targeted=jumps=ties=0
    for name,f,cap in cases:
        raw=f['raw'];t=f['t'];r=I.parse(raw);q=C.qualitative(raw);cert=C.numerical(raw,t)
        assert I.canon(r)==C.canonical(C.recognize(raw))
        assert I.receive_qualitative(raw,q) and I.receive_numerical(raw,t,cert)
        assert cert['status']=='CERTIFIED_NUMERICAL'
        localj=localt=0
        for x in product(range(cap),repeat=r['n']):
            drift,j,ti=I.verify_master(r,cert,x);localj+=j;localt+=ti;ordinary+=1
        targets=set();a=r['a'];p0=r['parts'][0][0];p1=r['parts'][1][0];co=cert['constants']
        for mass in [2*co['Nstar']+10,10**50]:
            for aa in [0,1,2,5]:
                for small in [0,1,2,10]:
                    x=[0]*r['n'];x[a]=aa;x[p0]=mass;x[p1]=small;targets.add(tuple(x))
            cut=(co['delta']*mass/(1-co['delta'])).numerator//(co['delta']*mass/(1-co['delta'])).denominator
            for rr in [max(1,cut-1),max(1,cut),cut+1]:
                for aa in [0,1]:
                    x=[0]*r['n'];x[a]=aa;x[p0]=mass;x[p1]=rr-aa;targets.add(tuple(x))
            for aa in [0,1,mass]:
                x=[0]*r['n'];x[a]=aa
                for part in r['parts']:x[part[0]]=mass
                targets.add(tuple(x))
        for x in targets:drift,j,ti=I.verify_master(r,cert,x);localj+=j;localt+=ti
        jumps+=localj;ties+=localt;targeted+=len(targets)
        out.append({'name':name,'dimension':r['n'],'parts':r['parts'],'Nstar':co['Nstar'],
          'ordinary_states':cap**r['n'],'targeted_states':len(targets),'enabled_internal_jumps':localj,'destination_ties':localt})
    raw=triangle['raw'];t=F(2);q=C.qualitative(raw);cert=C.numerical(raw,t)
    qmut=nmut=0
    for p,v in paths(q):assert not I.receive_qualitative(raw,change(q,p,mutation(v)));qmut+=1
    for p,v in paths(cert):assert not I.receive_numerical(raw,t,change(cert,p,mutation(v)));nmut+=1
    permutations_checked=0
    for perm in permutations(range(4)):
        rr=[(tuple(u[i] for i in perm),tuple(v[i] for i in perm),k) for u,v,k in raw]
        cc=C.numerical(rr,t);assert I.receive_numerical(rr,t,cc);permutations_checked+=1
    tcontrols=[]
    for tt in [F(1)+F(1,10**200),F(3,2),F(1000),F(10**100)]:
        cc=C.numerical(raw,tt);assert I.receive_numerical(raw,tt,cc)
        assert cc['status']=='CERTIFIED_NUMERICAL' and cc['work']['rate_dependent_iterations']==0
        r=I.parse(raw);mass=cc['constants']['Nstar']
        for x in [(0,mass,0,0),(1,mass,0,0),(0,mass,1,0),(0,mass,mass,mass)]:I.verify_master(r,cc,x)
        tcontrols.append({'t':tt,'Nstar_bits':cc['constants']['Nstar'].bit_length(),'retained_scalar_bits':cc['work']['retained_scalar_bits']})
    # Edge deletion can validly acquire a DIFFERENT multipartite partition.
    repartition=build_graph(4,[(1,3),(2,3)])
    re=C.qualitative(repartition);assert I.receive_qualitative(repartition,re)
    assert re['status']=='CERTIFIED_QUALITATIVE' and re['inventory']['parts']==((1,2),(3,))
    # Known stable unit-rate networks outside this recognizer.
    negative=[('free_passenger',build_graph(4,[(2,3)])),
      ('P4',build_graph(5,[(1,2),(2,3),(3,4)])),('disconnected_edges',build_graph(5,[(1,2),(3,4)])),
      ('inconsistent_nonadjacency',build_graph(6,[(1,2),(2,3),(3,4),(1,5),(2,5),(3,5),(4,5)]))]
    aa=(2,0,0,0);hub=(0,1,1,0);ab=(1,1,0,0)
    negative.extend([('no_amplification',[row for row in raw if (row[0],row[1]) not in [(aa,hub),(hub,aa)]]),
      ('uncovered_arm',[row for row in raw if row[0]!=ab and row[1]!=ab]),
      ('nonreversible',[row for row in raw if (row[0],row[1])!=(hub,ab)]),
      ('active_active',raw+[(aa,ab,F(1)),(ab,aa,F(1))])])
    neg=[]
    for name,rr in negative:
        qq=C.qualitative(rr);assert I.receive_qualitative(rr,qq) and qq['status']=='UNKNOWN'
        neg.append({'name':name,'reason':qq['reason']})
    # Normalization is mathematical, while raw input-work is charged separately.
    rr=list(raw);u,v,k=rr.pop();rr.extend([(u,v,k/3),(u,v,2*k/3),((0,)*4,(0,)*4,F(7))])
    cc=C.numerical(rr,t);assert I.receive_numerical(rr,t,cc)
    assert cc['raw_sha256']==cert['raw_sha256'] and cc['qualitative']['work']['input_rows']==len(raw)+2
    malformed=[]
    for val in [0,-1,True,1.0,'1']:
        rr=list(raw);u,v,k=rr[0];rr[0]=(u,v,val);malformed.append(rr)
    for val in [-1,True,F(1),1.0]:
        rr=list(raw);u,v,k=rr[0];u=list(u);u[0]=val;rr[0]=(u,v,k);malformed.append(rr)
    malformed.extend([[],[((),(),1)],[(raw[0][0],raw[0][1])]])
    domain=0
    for rr in malformed:
        for fn in [I.qualitative,C.qualitative]:
            try:fn(rr)
            except (ValueError,TypeError):pass
            else:raise AssertionError('malformed raw accepted')
        domain+=1
    for tt in [F(1),0,-1,True,1.1,'2']:
        for fn in [I.numerical,C.numerical]:
            try:fn(raw,tt)
            except (ValueError,TypeError):pass
            else:raise AssertionError('invalid t accepted')
        domain+=1
    return {'status':'all independent multipartite controls passed','cases':out,'ordinary_states':ordinary,
      'targeted_states':targeted,'enabled_internal_jumps':jumps,'boundary_destination_ties':ties,
      'qualitative_leaf_mutations_rejected':qmut,'numerical_leaf_mutations_rejected':nmut,
      'permutations':permutations_checked,'exact_domain_controls':domain,'t_extremes':tcontrols,
      'structural_unknowns':neg,'repartition_after_edge_deletion':'accepted with newly acquired parts(1,2)|(3)',
      'duplicate_split_null_control':'same normalized math; changed input work correctly received',
      'scope':'No external retrieval. No Foster power expansion or head enumeration. No all-method instability claim.'}
if __name__=='__main__':print(json.dumps(I.wire(main()),sort_keys=True,indent=2))
