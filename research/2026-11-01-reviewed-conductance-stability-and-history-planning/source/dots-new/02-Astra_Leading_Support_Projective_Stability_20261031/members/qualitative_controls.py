"""Finite structural-interface controls; no quantitative construction calls."""
from fractions import Fraction as F
import copy,json
import structural_receiver as r
import projective_mass as p

sp,raw=p.demo_network();receipt=r.acquire(sp,raw);assert receipt['status']=='QUALITATIVE_CERTIFIED'
mutations=[]
for name in ['proof_hash','raw_hash','pivot','leading_order','missing_seed','source_row','zero_work','Euler_claim','conclusion']:
    c=copy.deepcopy(receipt)
    if name=='proof_hash':c['theorem_sha256']='0'*64
    elif name=='raw_hash':c['raw_sha256']='0'*64
    elif name=='pivot':c['role']['pivot']=1
    elif name=='leading_order':c['role']['leading_order']=3
    elif name=='missing_seed':c['support_witness']['trials'].pop()
    elif name=='source_row':c['support_witness']['trials'][1]['steps'][0]['internal_row']=1
    elif name=='zero_work':
        c['support_witness']['support_reaction_tests']=0;c['work']['support_reaction_tests']=0;c['work']['support_coordinate_tests_upper']=0
    elif name=='Euler_claim':c['work']['Euler_steps_executed']=1
    else:c['conclusions']=['all weakly reversible networks are positive recurrent']
    try:r.verify(sp,raw,c)
    except ValueError:mutations.append(name)
    else:raise AssertionError('tamper accepted: '+name)
# Tiny encoded input with huge molecularity still uses only the finite structural path.
p_huge=10**50
huge_raw=[((0,0),(1,0),1),((1,0),(0,0),1),((0,p_huge),(1,p_huge-1),1),((1,p_huge-1),(0,p_huge),1)]
huge=r.acquire(['A','B'],huge_raw);hv=r.verify(['A','B'],huge_raw,huge)
assert huge['status']=='QUALITATIVE_CERTIFIED' and 'Euler_steps_M' not in huge['support_witness']
assert huge['work']['Euler_steps_executed']==huge['work']['polynomial_degrees_searched']==0
# Multi-stage activation in five dimensions, with the open role permuted last.
n=5;A=n-1;zero=(0,)*n;unit=tuple(int(i==A) for i in range(n));chain=[(zero,unit,F(1)),(unit,zero,F(1))]
for j in range(n-1):
    u=tuple(2*int(i==j) for i in range(n));v=tuple(int(i==j)+int(i==j+1) for i in range(n))
    chain.extend([(u,v,F(j+1)),(v,u,F(1,j+1))])
cs=[f'B{i+1}' for i in range(n-1)]+['A'];five=r.acquire(cs,chain);fv=r.verify(cs,chain,five)
assert five['status']=='QUALITATIVE_CERTIFIED' and five['role']['pivot']==4
# A negative top face and the absence of an instability conclusion.
z=(0,0,0);A0=(1,0,0);B=(0,1,0);C=(0,0,1);BB=(0,2,0);CC=(0,0,2)
stable=[(z,A0,1),(A0,z,1),(A0,B,1),(B,A0,1),(A0,C,1),(C,A0,1),(BB,CC,1),(CC,BB,1)]
negative=r.acquire(sp,stable);nv=r.verify(sp,stable,negative)
assert negative['status']=='STRICT_TOP_CONE_OBSTRUCTED' and negative['network_stability']=='UNKNOWN'
falseface=copy.deepcopy(negative);falseface['support_witness']['closed_face_support']=[1]
try:r.verify(sp,stable,falseface)
except ValueError:mutations.append('noninvariant_face')
else:raise AssertionError('false face accepted')
# Unsupported raw architectures and exact numeric-domain checks.
nonwr=[((0,0),(1,0),1),((1,0),(0,0),1),((0,2),(1,1),1)]
assert r.acquire(['A','B'],nonwr)['status']=='UNSUPPORTED_RAW_ARCHITECTURE'
raw_rejections=[]
for label,ss,rr in [('scalar',['A'],[((0,),(1,),1),((1,),(0,),1)]),('float_rate',sp,[(raw[0][0],raw[0][1],1.0)]+raw[1:]),('float_stoichiometry',sp,[((0.0,0,0),(1,0,0),1)]+raw[1:])]:
    try:r.acquire(ss,rr)
    except ValueError:raw_rejections.append(label)
    else:raise AssertionError(label)
print(json.dumps({'tampered_receipts_rejected':mutations,'huge_encoded_order_qualitative':huge,'huge_receiving_pass':hv,
 'five_species_chain':five,'five_species_receiving_pass':fv,'stable_negative_face':negative,'negative_receiving_pass':nv,
 'raw_domain_rejections':raw_rejections,'nonWR_architecture_declined':True,
 'quantitative_functions_executed':False,'tests_supplement_the_theorem':True},indent=2,sort_keys=True))
