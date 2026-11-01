#!/usr/bin/env python3
"""Independent raw constructions/receiving/algebra and negative controls.
The candidate is imported only to supply receipts for a separate receiver;
all graph/rational verification lives in independent_receiver.py.
"""
from fractions import Fraction as F
from itertools import product,permutations
from pathlib import Path
from copy import deepcopy
import importlib.util,json,sys
import independent_receiver as I
HERE=Path(__file__).resolve().parent
BASE=HERE.parent if (HERE.parent/'compound_seed.py').exists() else HERE.parent/'stochastic_compound_seed_pending_20261031'
spec=importlib.util.spec_from_file_location('candidate_compound',BASE/'compound_seed.py')
C=importlib.util.module_from_spec(spec);spec.loader.exec_module(C)

def fixture(n,parts,*,sparse=False,varied=False,port=(1,1),a=0):
    def v(*indices):return tuple(indices.count(i) for i in range(n))
    raw=[(v(),v(a),F(port[0])),(v(a),v(),F(port[1]))]
    hubs=[v(i,j) for left,right in parts for i in left for j in right]
    for h,H in enumerate(hubs):
        raw += [(v(a,a),H,F(h+2,3) if varied else F(1)),(H,v(a,a),F(h+3,2) if varied else F(1))]
    sat=[i for i in range(n) if i!=a]
    for k,x in enumerate(sat):
        for h,H in enumerate(hubs):
            if sparse and h!=k%len(hubs):continue
            raw += [(v(a,x),H,F(k+h+2,4) if varied else F(1)),
                    (H,v(a,x),F(k+2*h+3,5) if varied else F(2) if n==4 and x==2 else F(1))]
    return raw

def leafpaths(x,path=()):
    if isinstance(x,dict):
        for k,v in x.items():yield from leafpaths(v,path+(k,))
    elif isinstance(x,(list,tuple)):
        for j,v in enumerate(x):yield from leafpaths(v,path+(j,))
    else:yield path,x

def tamper(x,path,new):
    if not path:return new
    k=path[0]
    if isinstance(x,dict):
        z=dict(x);z[k]=tamper(z[k],path[1:],new);return z
    z=list(x);z[k]=tamper(z[k],path[1:],new)
    return tuple(z) if isinstance(x,tuple) else z

def mutated(v):
    if type(v) in (int,F):return v+1
    if v is None:return 'changed-none'
    if type(v) is str:return v+'!'
    raise AssertionError(type(v))

def profile_checks(r,c):
    co=c['constants'];K,J=co['K'],co['J'];count=0
    for z in list(range(1,K+2))+[J,J+1,10**20]:
        g=I.gvalue(c,z);d=g-I.gvalue(c,z+1)
        assert r['lam']*(c['t']*I.gvalue(c,z+1)-g)-co['beta']*z*z*d<=-co['epsilon']*g
        assert (z+1)**2*d>=co['dstar'];count+=2
    for z in [J,J+1,10**20]:
        g=I.gvalue(c,z);dm=I.gvalue(c,z-1)-g;dp=g-I.gvalue(c,z+1)
        E=r['mu']*(I.gvalue(c,z-1)/c['t']-g)+r['Kf']*z*dm+2*co['beta']*z*dp
        assert E<=-co['D']/2;count+=1
    return count

def main():
    fixtures=[('base',fixture(4,[([2],[3])]),F(2),4),
      ('K22_sparse',fixture(6,[([2,3],[4,5])],sparse=True,varied=True),F(3,2),3),
      ('two_components',fixture(6,[([2],[3]),([4],[5])],sparse=True),F(2),3),
      ('star_no_free',fixture(5,[([1],[2,3,4])],sparse=True,varied=True),F(5,4),3),
      ('minimal_three',fixture(3,[([1],[2])],varied=True,port=(F(2,3),F(5,4))),F(5),4)]
    cases=[];total_states=total_target=profile_count=0
    for name,raw,t,cap in fixtures:
        r=I.parse(raw);q=C.qualitative(raw);c=C.numerical(raw,t)
        assert I.canon(r)==C.canonical(C.recognize(raw))
        assert I.receive_qualitative(raw,q) and I.receive_numerical(raw,t,c)
        assert c['status']=='CERTIFIED_NUMERICAL';profile_count+=profile_checks(r,c)
        states=0
        for x in product(range(cap),repeat=r['n']):I.verify_master(r,c,x);states+=1
        targets=set();a=r['a'];left,right=r['components'][0];i,j=left[0],right[0]
        bulk=r['free'][0] if r['free'] else i
        for mass in [c['constants']['Nstar'],10**20,10**50]:
            for R in [0,1,2,c['constants']['K'],c['constants']['J']-1,c['constants']['J']]:
                for aa in sorted({0,min(1,R),min(2,R),R}):
                    x=[0]*r['n'];x[a]=aa;x[i]+=R-aa;x[j]+=R-aa;x[bulk]+=mass
                    targets.add(tuple(x))
        for x in sorted(targets):I.verify_master(r,c,x)
        total_states+=states;total_target+=len(targets)
        cases.append({'name':name,'species':r['n'],'states':states,'targeted_states':len(targets),
                      'K':c['constants']['K'],'J':c['constants']['J'],'Nstar':c['constants']['Nstar'],
                      'raw_sha256':r['raw_sha256']})
    raw=fixtures[0][1];t=F(2);q=C.qualitative(raw);c=C.numerical(raw,t)
    qmut=nmut=0
    for path,v in leafpaths(q):assert not I.receive_qualitative(raw,tamper(q,path,mutated(v)));qmut+=1
    for path,v in leafpaths(c):assert not I.receive_numerical(raw,t,tamper(c,path,mutated(v)));nmut+=1
    # A zero iteration cap must preserve qualitative conclusions and do no recurrence/head scans.
    capcert=C.numerical(raw,t,0);assert capcert['status']=='NUMERICAL_UNKNOWN'
    assert I.receive_numerical(raw,t,capcert,0)
    assert capcert['qualitative']==q and capcert['work']=={'profile_recurrence_steps':0,'finite_head_checks':0}
    unknownmut=0
    for path,v in leafpaths(capcert):assert not I.receive_numerical(raw,t,tamper(capcert,path,mutated(v)),0);unknownmut+=1
    # Independent parameter/permutation controls.
    pcount=0
    for p in permutations(range(4)):
        rr=[(tuple(u[i] for i in p),tuple(v[i] for i in p),k) for u,v,k in raw]
        cert=C.numerical(rr,t);assert I.receive_numerical(rr,t,cert);pcount+=1
    tchecks=[]
    for tt in [F(101,100),F(3,2),F(5),F(1000)]:
        cert=C.numerical(raw,tt,20000);assert I.receive_numerical(raw,tt,cert,20000)
        tchecks.append({'t':tt,'status':cert['status']})
    # Duplicate splitting and inert null rows: normalized math unchanged, charged raw work changes.
    rr=list(raw);u,v,k=rr.pop();rr.extend([(u,v,k/3),(u,v,2*k/3),((0,)*4,(0,)*4,F(7))])
    cert=C.numerical(rr,t);assert I.receive_numerical(rr,t,cert)
    assert cert['raw_sha256']==c['raw_sha256'] and cert['qualitative']['work']['input_rows']==len(raw)+2
    # Structural unknowns independently recognized; no stability counterclaim.
    def vv(n,*ids):return tuple(ids.count(i) for i in range(n))
    triangle=fixture(4,[([1],[2,3])]);h=vv(4,2,3);aa=vv(4,0,0)
    triangle.extend([(aa,h,F(1)),(h,aa,F(1))])
    path=fixture(5,[([1,3],[2,4])],sparse=True)
    missing=vv(5,1,4);path=[row for row in path if row[0]!=missing and row[1]!=missing]
    # Missing hub removes some sparse coverage too, but biclique check precedes arm coverage.
    h=vv(4,2,3);aa=vv(4,0,0);ab=vv(4,0,1)
    negatives=[triangle,path,[row for row in raw if (row[0],row[1])!=(aa,h)],
      [row for row in raw if row[0]!=ab and row[1]!=ab],raw+[(vv(4,1),vv(4,2),F(1)),(vv(4,2),vv(4,1),F(1))],
      raw+[(aa,ab,F(1)),(ab,aa,F(1))],raw+[(vv(4),vv(4,1),F(1)),(vv(4,1),vv(4),F(1))]]
    neg=[]
    for rr in negatives:
        cq=C.qualitative(rr);iq=I.qualitative(rr);assert I.canon(cq)==I.canon(iq)
        assert cq['status']=='UNKNOWN';neg.append(cq['reason'])
    # Exact-domain controls, separately in candidate and receiver.
    badraw=[]
    for value in [0,-1,True,1.0,'1']:
        rr=list(raw);u,v,k=rr[0];rr[0]=(u,v,value);badraw.append(rr)
    for value in [-1,True,F(1),1.0]:
        rr=list(raw);u,v,k=rr[0];u=list(u);u[0]=value;rr[0]=(u,v,k);badraw.append(rr)
    badraw.extend([[],[((),(),1)],[(raw[0][0],raw[0][1])]])
    domains=0
    for rr in badraw:
        for fn in [I.qualitative,C.qualitative]:
            try:fn(rr)
            except (ValueError,TypeError):pass
            else:raise AssertionError('malformed raw accepted')
        domains+=1
    for badt in [F(1),0,-1,True,1.1,'2']:
        for fn in [I.numerical,C.numerical]:
            try:fn(raw,badt)
            except (ValueError,TypeError):pass
            else:raise AssertionError('bad t accepted')
        domains+=1
    for budget in [-1,True,F(2),2.0]:
        for fn in [I.numerical,C.numerical]:
            try:fn(raw,t,budget)
            except (ValueError,TypeError):pass
            else:raise AssertionError('bad budget accepted')
        domains+=1
    return {'status':'all independent exact controls passed','cases':cases,'ordinary_states':total_states,
      'targeted_states':total_target,'profile_tail_algebra_checks':profile_count,
      'qualitative_leaf_tampers_rejected':qmut,'numerical_leaf_tampers_rejected':nmut,
      'budget_unknown_leaf_tampers_rejected':unknownmut,'permutations':pcount,'t_variations':tchecks,
      'structural_unknown_controls':neg,'exact_domain_controls':domains,
      'normalization_control':'duplicate split plus null row accepted with changed raw work',
      'scope':'receiver reconstructs from raw; no full head enumeration, no Foster power expansion, no fiber law'}
if __name__=='__main__':print(json.dumps(I.wire(main()),sort_keys=True,indent=2))
