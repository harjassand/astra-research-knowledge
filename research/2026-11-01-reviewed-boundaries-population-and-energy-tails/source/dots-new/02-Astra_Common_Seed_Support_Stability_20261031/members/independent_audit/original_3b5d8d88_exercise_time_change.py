#!/usr/bin/env python3
"""Executed exact receiver/cost controls; asymptotic proof is not a simulation."""
from fractions import Fraction as F
from itertools import permutations,product
import copy,json
import seeded_time_change as s


def hard_raw():
    return [((0,0,0),(1,0,0),F(1)),((1,0,0),(0,0,0),F(1)),
        ((2,1,0),(1,1,1),F(1)),((1,1,1),(2,1,0),F(1)),
        ((2,0,1),(1,2,0),F(1)),((1,2,0),(2,0,1),F(1)),
        ((1,1,1),(1,0,2),F(2)),((1,0,2),(1,1,1),F(1))]


def test(label,raw,t=F(2),cap=100000):
    z=s.numerical(raw,t,cap)
    assert z['status']=='CERTIFIED_SAMPLED_CORE_AND_STATIONARY_MOMENT_BOUND'
    assert s.receive_qualitative(raw,s.encode(z['qualitative']))
    assert s.receive_numerical(raw,t,cap,s.encode(z))
    c=z['constants'];rec=s.recognize(raw);C,T,delta=c['C'],c['T'],c['delta']
    assert C*T==F(1,4) and 0<delta<=F(3,4*rec['n'])
    assert c['K0']==64*rec['n']*C*T/delta**2 and c['K']==c['K0']+2/delta
    assert c['minimum_mass_for_activation']>=rec['p']
    assert C*T/c['minimum_mass_for_activation']<=delta/8
    tests=[]
    for M in [c['M_cut'],c['M_cut']+1,2*c['M_cut'],10**50*c['M_cut']]:
        upper=1/t+(t-1/t)*c['combined_bad_event_constant']/M
        assert upper<=c['rho']<1
        tests.append(dict(mass=M,sampled_ratio_upper=upper))
    assert c['sampled_stationary_moment_bound']['prefactor']==2*t+1
    assert c['stationary_mean_cycle_time_interval']==dict(lower=1/(2*rec['lam']),upper=1/rec['lam'])
    assert c['continuous_stationary_flow_bound']==dict(prefactor=2*rec['lam']*(1/rec['mu']+1/rec['lam'])*(2*t+1),base=t,exponent=c['M_cut'])
    assert not c['head_states_enumerated'] and not c['stationary_power_expanded']
    return dict(label=label,receipt=z,threshold_algebra_checks=tests)


raw=s.opposing_raw()
rows=[test('opposing_pure_rays_non_complex_balanced',raw),test('mediated_no_F_A_N_fixture',hard_raw()),
      test('opposing_stripped_cubic_lift',s.catalytic_lift(raw)),test('near_one_base',raw,F(65,64)),
      test('large_base',raw,F(100))]
hetero=[(u,v,k*F(i+1,i+2)) for i,(u,v,k) in enumerate(raw)]
rows.append(test('heterogeneous_rates',hetero))

n=5;A=4;zero=(0,)*n;e=tuple(int(i==A) for i in range(n));chain=[(zero,e,F(2,3)),(e,zero,F(7,5))]
for j in range(n-1):
    u=tuple(2*int(i==j)+int(i==A) for i in range(n))
    v=tuple(int(i==j)+int(i==j+1)+int(i==A) for i in range(n))
    chain.extend([(u,v,F(j+1)),(v,u,F(1,j+1))])
rows.append(test('five_species_support_chain_open_role_last',chain))

metamorphic=[]
for p in permutations(range(3)):
    rr=[(tuple(u[i] for i in p),tuple(v[i] for i in p),k) for u,v,k in reversed(raw)]
    u,v,k=rr.pop();rr.extend([(u,v,k/3),(u,v,2*k/3),((0,0,0),(0,0,0),F(1))])
    z=s.numerical(rr,F(2))
    assert z['status']=='CERTIFIED_SAMPLED_CORE_AND_STATIONARY_MOMENT_BOUND'
    assert z['constants']==rows[0]['receipt']['constants']
    assert s.receive_qualitative(rr,s.encode(z['qualitative']))
    metamorphic.append(dict(permutation=p,qualitative=z['qualitative']))

# New support principle succeeds where every inverse-linear profile must fail.
# The pure-B and pure-C effective increments have opposite signs for all weights.
profile_obstruction=[]
for b,c in product([F(0),F(1,4),F(1,2),F(1)],repeat=2):
    d=c-b
    assert not(d>0 and -d>0)
    profile_obstruction.append(dict(weights=[b,c],pure_B_increment=d,pure_C_increment=-d))

# Stable condition-negative: lower-order restoration, neutral top order.
negative=[((0,0,0),(1,0,0),F(1)),((1,0,0),(0,0,0),F(1))]
for u,v in [((2,0,0),(1,1,0)),((2,0,0),(1,0,1)),((1,2,0),(1,0,2))]:
    negative.extend([(u,v,F(1)),(v,u,F(1))])
neg=s.qualitative(negative)
assert neg['status']=='SUPPORT_CONDITION_FAILED_STABILITY_UNKNOWN'
face=set(neg['support']['closed_face_support']);assert 0 not in face
for u,v,k in s.recognize(negative)['stripped']:
    if sum(u)==2 and all(not z or j in face for j,z in enumerate(u)):
        assert all(not z or j in face for j,z in enumerate(v))
# At all-one concentration, every forward/reverse pair individually balances.
assert all(any(v==uu and u==vv and k==kk for uu,vv,kk in negative) for u,v,k in negative)

# Compactly encoded huge degree: qualitative accepted, scalar-power acquisition declined.
p=10**50
huge=[((0,0),(1,0),F(1)),((1,0),(0,0),F(1)),((1,p),(2,p-1),F(1)),((2,p-1),(1,p),F(1))]
oldpow=F.__pow__
def forbidden(*args,**kwargs):raise AssertionError('qualitative path called Fraction power')
F.__pow__=forbidden
try:huge_q=s.qualitative(huge);assert s.receive_qualitative(huge,s.encode(huge_q))
finally:F.__pow__=oldpow
huge_n=s.numerical(huge,F(2),1000)
assert huge_q['status']=='CERTIFIED_ALL_FINITE_EXPONENTIAL_MOMENTS'
assert huge_n['status']=='NUMERICAL_UNKNOWN' and huge_n['work']['support_powers_executed']==0
assert huge_n['qualitative']==huge_q
capped=s.numerical(raw,F(2),1)
assert capped['status']=='NUMERICAL_UNKNOWN' and capped['qualitative']['status']=='CERTIFIED_ALL_FINITE_EXPONENTIAL_MOMENTS'

# Exactly n power evaluations are made, all with exponent p, never the Foster exponent.
calls=[]
def audited_power(self,exponent,*args,**kwargs):
    calls.append(exponent)
    return oldpow(self,exponent,*args,**kwargs)
F.__pow__=audited_power
try:pp=s.numerical(raw,F(2))
finally:F.__pow__=oldpow
assert calls==[2,2,2]

base=s.encode(rows[0]['receipt']);qual=base['qualitative'];tampered=[]
q_mutations={
 'family':lambda z:z.update(family='all weakly reversible'),
 'raw_hash':lambda z:z.update(raw_sha256='0'*64),
 'open_coordinate':lambda z:z['role'].update(open_coordinate=1),
 'stripped_top_order':lambda z:z['role'].update(stripped_top_order=3),
 'immigration':lambda z:z['role'].update(immigration='2'),
 'missing_seed':lambda z:z['support']['traces'].pop(),
 'missing_activation':lambda z:z['support']['traces'][1]['steps'].clear(),
 'bad_source':lambda z:z['support']['traces'][1]['steps'][0].update(stripped_channel=0),
 'reaction_work':lambda z:z['support'].update(reaction_tests=0),
 'source_work':lambda z:z['support'].update(source_coordinate_tests=0),
 'product_work':lambda z:z['support'].update(product_coordinate_tests=0),
 'graph_work':lambda z:z['work'].update(graph_edge_visits=0),
 'numerical_work':lambda z:z['work'].update(numerical_support_powers=1),
 'stationary_oracle':lambda z:z['work'].update(stationary_fiber_laws=1),
 'conclusions':lambda z:z.update(conclusions=['all weakly reversible networks solved']),
}
for label,mut in q_mutations.items():
    z=copy.deepcopy(qual);mut(z)
    # A deterministic bad source mutation might accidentally leave the original index.
    if z==qual:
        z['support']['traces'][1]['steps'][0]['stripped_channel']=999
    assert not s.receive_qualitative(raw,z);tampered.append('qual_'+label)
n_mutations={
 'C':lambda z:z['constants'].update(C='1'),
 'delta':lambda z:z['constants'].update(delta='1'),
 'level':lambda z:z['constants']['levels'].__setitem__(1,'1'),
 'K0':lambda z:z['constants'].update(K0='0'),
 'K':lambda z:z['constants'].update(K='0'),
 'M0':lambda z:z['constants'].update(minimum_mass_for_activation=1),
 'bad_event':lambda z:z['constants'].update(combined_bad_event_constant='0'),
 'Mcut':lambda z:z['constants'].update(M_cut=1),
 'rho':lambda z:z['constants'].update(rho='1/2'),
 'cycle_time':lambda z:z['constants'].update(maximum_mean_physical_cycle='0'),
 'Foster_power':lambda z:z['constants']['sampled_Foster_constant'].update(exponent=1),
 'moment_power':lambda z:z['constants']['sampled_stationary_moment_bound'].update(exponent=1),
 'occupation_bound':lambda z:z['constants']['continuous_stationary_positive_upper_sum'][0].update(prefactor='0'),
 'flow_interval':lambda z:z['constants']['stationary_mean_cycle_time_interval'].update(lower='1'),
 'flow_identity':lambda z:z['constants'].update(stationary_mean_cycle_time_identity='unknown normalization oracle'),
 'flow_bound':lambda z:z['constants']['continuous_stationary_flow_bound'].update(prefactor='0'),
 'head_count':lambda z:z['constants']['finite_head_size_symbolic'].update(lower=1),
 'one_step_claim':lambda z:z['constants'].update(interpretation='physical one-step F(A,N)'),
 'power_work':lambda z:z['work'].update(support_powers_executed=0),
 'bit_work':lambda z:z['work'].update(retained_rational_peak_bits=0),
 'preflight':lambda z:z['work']['power_preflights'][0].update(power_product_bits_upper=0),
 'solver_work':lambda z:z['work'].update(finite_fiber_linear_systems_solved=1),
}
for label,mut in n_mutations.items():
    z=copy.deepcopy(base);mut(z);assert not s.receive_numerical(raw,F(2),100000,z);tampered.append('numeric_'+label)

bad=[]
cases=[('float_rate',[(raw[0][0],raw[0][1],1.0)]+raw[1:]),
       ('bool_rate',[(raw[0][0],raw[0][1],True)]+raw[1:]),
       ('nonpositive_rate',[(raw[0][0],raw[0][1],0)]+raw[1:]),
       ('float_stoichiometry',[((0.0,0,0),(1,0,0),1)]+raw[1:]),
       ('nonWR',raw[:-1]),
       ('no_common_seed',raw+[((0,2,0),(1,1,0),1),((1,1,0),(0,2,0),1)]),
       ('extra_open',raw+[((0,0,0),(0,1,0),1),((0,1,0),(0,0,0),1)]),
       ('one_species',[((0,),(1,),1),((1,),(0,),1)])]
for label,rr in cases:
    try:s.qualitative(rr)
    except (ValueError,TypeError):bad.append(label)
    else:raise AssertionError(label)
for label,action in [('t_one',lambda:s.numerical(raw,F(1))),('t_float',lambda:s.numerical(raw,2.0)),
                     ('cap_bool',lambda:s.numerical(raw,F(2),True)),('cap_zero',lambda:s.numerical(raw,F(2),0))]:
    try:action()
    except (ValueError,TypeError):bad.append(label)
    else:raise AssertionError(label)
linear=[((0,0),(1,0),1),((1,0),(0,0),1),((2,0),(1,1),1),((1,1),(2,0),1)]
assert s.qualitative(linear)['status']=='UNKNOWN'

print(json.dumps(s.encode(dict(cases=rows,coordinate_permutations=metamorphic,
    inverse_linear_profile_sign_obstruction=profile_obstruction,stable_condition_negative=neg,
    huge_encoded_degree_qualitative=huge_q,huge_encoded_degree_numerical=huge_n,
    capped_numerical=capped,actual_fraction_power_exponents=calls,
    semantic_tamper_rejections=tampered,raw_domain_rejections=bad,
    stripped_linear_case='UNKNOWN under this theorem, not instability',
    asymptotic_fibers_or_heads_enumerated=False,Foster_powers_expanded=False,
    trajectories_simulated=False,tests_do_not_replace_proof=True)),indent=2,sort_keys=True))
