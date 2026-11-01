#!/usr/bin/env python3
from fractions import Fraction as F
from itertools import permutations
from math import comb
from pathlib import Path
import copy,hashlib,importlib.util,json
import independent_time_change_receiver as v

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('candidate',HERE/'frozen_seeded_time_change.py');s=importlib.util.module_from_spec(spec);spec.loader.exec_module(s)
def opposing():
    return [((0,0,0),(1,0,0),F(1)),((1,0,0),(0,0,0),F(1)),
            ((1,2,0),(1,1,1),F(1)),((1,1,1),(1,2,0),F(1)),
            ((1,1,1),(1,0,2),F(2)),((1,0,2),(1,1,1),F(1)),
            ((1,1,1),(2,1,0),F(1)),((2,1,0),(1,1,1),F(1))]
def hard():
    return opposing()[:2]+[((2,1,0),(1,1,1),F(1)),((1,1,1),(2,1,0),F(1)),
                          ((2,0,1),(1,2,0),F(1)),((1,2,0),(2,0,1),F(1)),
                          ((1,1,1),(1,0,2),F(2)),((1,0,2),(1,1,1),F(1))]
def catalytic(raw):
    ans=raw[:2]
    for u,z,k in raw[2:]:
        for j in range(len(u)):
            ans.append((tuple(a+int(i==j)for i,a in enumerate(u)),tuple(a+int(i==j)for i,a in enumerate(z)),k))
    return ans
def chain():
    n=5;a=4;zero=(0,)*n;e=(0,0,0,0,1);raw=[(zero,e,F(2,3)),(e,zero,F(7,5))]
    for j in range(4):
        u=tuple(2*int(i==j)+int(i==a)for i in range(n));z=tuple(int(i==j)+int(i==j+1)+int(i==a)for i in range(n))
        raw.extend([(u,z,F(j+1)),(z,u,F(1,j+1))])
    return raw
def negative():
    raw=opposing()[:2]
    for u,z in [((2,0,0),(1,1,0)),((2,0,0),(1,0,1)),((1,2,0),(1,0,2))]:raw.extend([(u,z,F(1)),(z,u,F(1))])
    return raw
def leaves(z,path=()):
    if isinstance(z,dict):
        for k,x in z.items():yield from leaves(x,path+(k,))
    elif isinstance(z,list):
        for k,x in enumerate(z):yield from leaves(x,path+(k,))
    else:yield path,z
def mutate(z,path,value):
    q=copy.deepcopy(z);d=q
    for p in path[:-1]:d=d[p]
    d[path[-1]]=value;return q
def rejected(action):
    try:action()
    except (AssertionError,ValueError,TypeError):return True
    return False

def main():
    original=json.loads((HERE/'frozen_opposing_demo.json').read_text());exercise=json.loads((HERE/'frozen_exercise_results.json').read_text())
    raw=opposing();heter=[(u,z,k*F(i+1,i+2))for i,(u,z,k)in enumerate(raw)]
    raws=[raw,hard(),catalytic(raw),raw,raw,heter,chain()];rows=[]
    assert v.receive_numerical(raw,F(2),100000,original)
    for rr,row in zip(raws,exercise['cases']):
        cert=row['receipt'];t=F(cert['t']);assert v.receive_qualitative(rr,cert['qualitative']) and v.receive_numerical(rr,t,100000,cert)
        checks=v.check_scalar_proof(cert)
        assert v.canon([dict(mass=x['M'],sampled_ratio_upper=x['ratio'])for x in checks])==v.canon(row['threshold_algebra_checks'])
        rows.append(dict(label=row['label'],support_reaction_tests=cert['qualitative']['support']['reaction_tests'],
                         M_cut_decimal_digits=len(str(cert['constants']['M_cut'])),threshold_checks=checks))
    # Order five with a genuinely lower-order conservative pair.
    higher=[((0,0),(1,0),F(2,3)),((1,0),(0,0),F(7,5)),
            ((1,5),(2,4),F(3,2)),((2,4),(1,5),F(5,3)),((2,0),(1,1),F(17)),((1,1),(2,0),F(19))]
    higher_receipt=v.wire(s.numerical(higher,F(3,2),100000));assert v.receive_numerical(higher,F(3,2),100000,higher_receipt)
    rows.append(dict(label='order_five_plus_lower_order',support_reaction_tests=higher_receipt['qualitative']['support']['reaction_tests'],
                     M_cut_decimal_digits=len(str(higher_receipt['constants']['M_cut'])),threshold_checks=v.check_scalar_proof(higher_receipt)))
    metamorphic=[]
    for perm,row in zip(permutations(range(3)),exercise['coordinate_permutations']):
        rr=[(tuple(u[i]for i in perm),tuple(z[i]for i in perm),k)for u,z,k in reversed(raw)]
        u,z,k=rr.pop();rr.extend([(u,z,k/3),(u,z,2*k/3),((0,0,0),(0,0,0),F(1))])
        assert v.receive_qualitative(rr,row['qualitative']);proposal=v.wire(s.numerical(rr,F(2)))
        assert v.receive_numerical(rr,F(2),100000,proposal) and proposal['constants']==original['constants']
        metamorphic.append(dict(permutation=perm,graph_edge_visits=proposal['qualitative']['work']['graph_edge_visits']))
    # Exact condition-negative receipt is checked, but not accepted as a positive theorem.
    neg=negative();nz=v.qualitative(neg);assert v.canon(nz)==v.canon(exercise['stable_condition_negative'])
    assert not v.receive_qualitative(neg,nz)
    assert all(any(z==uu and u==zz and k==kk for uu,zz,kk in neg)for u,z,k in neg) # detailed balance at unit means
    assert v.canon(v.numerical(neg,F(2),1000))==v.canon(s.numerical(neg,F(2),1000))
    linear=[((0,0),(1,0),1),((1,0),(0,0),1),((2,0),(1,1),1),((1,1),(2,0),1)]
    assert v.qualitative(linear)['status']=='UNKNOWN'
    assert v.canon(v.qualitative(linear))==v.canon(s.qualitative(linear))
    # Every scalar/string/Boolean leaf is tampered independently, including all work fields.
    qbad=[]
    for path,old in leaves(original['qualitative']):
        new=not old if type(old)is bool else old+1 if type(old)is int else str(old)+'_tampered'
        q=mutate(original['qualitative'],path,new)
        assert not v.receive_qualitative(raw,q) and not s.receive_qualitative(raw,q);qbad.append(list(path))
    nbad=[]
    for path,old in leaves(original):
        new=not old if type(old)is bool else old+1 if type(old)is int else str(old)+'_tampered'
        q=mutate(original,path,new)
        assert not v.receive_numerical(raw,F(2),100000,q) and not s.receive_numerical(raw,F(2),100000,q);nbad.append(list(path))
    # Non-leaf omissions and invented oracle-bearing fields.
    structures=[]
    for key in original:
        q=copy.deepcopy(original);q.pop(key);assert not v.receive_numerical(raw,F(2),100000,q);structures.append('missing_'+key)
    q=copy.deepcopy(original);q['trusted_stationary_law']='oracle';assert not v.receive_numerical(raw,F(2),100000,q);structures.append('extra_oracle')
    # Exercise caps at each boundary; counters record completed powers, not attempted ones.
    caps=[1]+[x['power_product_bits_upper']-1 for x in original['work']['power_preflights']]+[original['work']['power_preflights'][-1]['power_product_bits_upper']]
    caprows=[]
    for cap in caps:
        expected=v.numerical(raw,F(2),cap);actual=s.numerical(raw,F(2),cap);assert v.canon(expected)==v.canon(actual)
        assert expected['qualitative']['status']=='CERTIFIED_ALL_FINITE_EXPONENTIAL_MOMENTS'
        caprows.append(dict(cap=cap,status=expected['status'],powers=expected['work']['support_powers_executed']))
    assert v.canon(v.numerical(raw,F(2),1))==v.canon(exercise['capped_numerical'])
    p=10**50;huge=[((0,0),(1,0),F(1)),((1,0),(0,0),F(1)),((1,p),(2,p-1),F(1)),((2,p-1),(1,p),F(1))]
    oldpow=F.__pow__
    def deny(*a,**k):raise AssertionError('power unexpectedly evaluated')
    F.__pow__=deny
    try:
        assert v.receive_qualitative(huge,exercise['huge_encoded_degree_qualitative'])
        assert v.canon(v.numerical(huge,F(2),1000))==v.canon(exercise['huge_encoded_degree_numerical'])
        assert v.canon(s.numerical(huge,F(2),1000))==v.canon(exercise['huge_encoded_degree_numerical'])
    finally:F.__pow__=oldpow
    powercalls=[]
    def record(self,exponent,*a,**kw):powercalls.append(exponent);return oldpow(self,exponent,*a,**kw)
    F.__pow__=record
    try:v.numerical(raw,F(2),100000)
    finally:F.__pow__=oldpow
    assert powercalls==[2,2,2]
    # Exact domain and architecture controls in both independent and candidate APIs.
    malformed=[('empty',[]),('bad_row',[(raw[0][0],raw[0][1])]),('one_species',[((0,),(1,),1),((1,),(0,),1)]),
               ('dimension',[((),(),1)]+raw),('float_rate',[(raw[0][0],raw[0][1],1.0)]+raw[1:]),
               ('bool_rate',[(raw[0][0],raw[0][1],True)]+raw[1:]),('zero_rate',[(raw[0][0],raw[0][1],0)]+raw[1:]),
               ('negative_rate',[(raw[0][0],raw[0][1],-1)]+raw[1:]),('string_rate',[(raw[0][0],raw[0][1],'1')]+raw[1:]),
               ('float_complex',[((0.0,0,0),(1,0,0),1)]+raw[1:]),('bool_complex',[((False,0,0),(1,0,0),1)]+raw[1:]),
               ('negative_complex',[((-1,0,0),(1,0,0),1)]+raw[1:]),('bad_null_rate',raw+[((0,0,0),(0,0,0),False)]),
               ('no_WR',raw[:-1]),('no_seed',raw+[((0,2,0),(1,1,0),1),((1,1,0),(0,2,0),1)]),
               ('extra_open',raw+[((0,0,0),(0,1,0),1),((0,1,0),(0,0,0),1)])]
    rejected_raw=[]
    for label,rr in malformed:
        assert rejected(lambda:v.qualitative(rr)) and rejected(lambda:s.qualitative(rr));rejected_raw.append(label)
    bad_scalar=[]
    for t,cap in [(F(1),1000),(F(0),1000),(F(-1),1000),(2.0,1000),(True,1000),(F(2),True),(F(2),0),(F(2),-1),(F(2),1.0)]:
        assert rejected(lambda:v.numerical(raw,t,cap)) and rejected(lambda:s.numerical(raw,t,cap));bad_scalar.append([repr(t),repr(cap)])
    head_checks=0
    for n in range(2,7):
        for cut in range(1,9):
            assert sum(comb(N+n-2,n-1)for N in range(1,cut+1))==comb(cut+n-1,n);head_checks+=1
    print(json.dumps(v.wire(dict(candidate_sha256=hashlib.sha256((HERE/'frozen_seeded_time_change.py').read_bytes()).hexdigest(),
        independent_raw_support_work_and_scalar_receiving=True,cases=rows,coordinate_permutations=metamorphic,
        qualitative_leaf_tampers_rejected=qbad,numerical_leaf_tampers_rejected=nbad,structural_receipt_tampers_rejected=structures,
        cap_boundary_checks=caprows,huge_degree_preflight_guarded_against_fraction_powers=True,
        independent_fraction_power_calls=powercalls,stable_failed_support_not_misclassified=True,
        raw_domain_rejections=rejected_raw,scalar_domain_rejections=bad_scalar,
        finite_head_binomial_identity_checks=head_checks,
        factored_continuous_bound_polynomial_identity_verified=True,finite_tests_supplement_proof=True)),indent=2,sort_keys=True))

if __name__=='__main__':main()
