#!/usr/bin/env python3
"""Exact executed controls. Finite checks supplement, never replace, the proof."""
from fractions import Fraction as F
from itertools import permutations, product
import copy
import json
import seeded_inverse_mass as s


def comps(N,n):
    if n == 1:
        yield (N,)
    else:
        for a in range(N+1):
            for z in comps(N-a,n-1):
                yield (a,)+z


def exercise(label,raw,bundle,limit=18):
    assert bundle['status'] == 'CERTIFIED'
    c = bundle['certificate']
    assert s.receive(raw,c['t'],c['weights'],s.encode(c))
    n,a,js = c['dimension'],c['open_coordinate'],c['satellite_coordinates']
    ordinary = 0
    for N in range(limit+1):
        for x in comps(N,n):
            s.check_state(raw,c,x)
            ordinary += 1
    points = []
    for A in [0,1,2,c['A_cut']-1,c['A_cut'],c['A_cut']+1]:
        for j,cut in zip(js,c['B_cuts']):
            for B in [0,cut-1,cut,cut+1,10**6,10**50]:
                x = [0]*n
                x[a],x[j] = A,B
                points.append(tuple(x))
    for M in [10**6,10**50]:
        points.append((M,)*n)
    for x in points:
        s.check_state(raw,c,x)
    return dict(label=label,ordinary_checks=ordinary,boundary_and_huge_checks=len(points),
                certificate=c,acquisition=bundle.get('acquisition','candidate-profile test only'))


raw = s.hard_raw()
demo = s.hard_search(raw,F(2),100)
rows = [exercise('non_complex_balanced_hard_lift_t2',raw,demo)]
for t in [F(65,64),F(100)]:
    rows.append(exercise('same_hard_lift_t'+str(t),raw,s.hard_search(raw,t,100),14))
heterogeneous = s.hard_raw((F(2,3),F(7,5),F(1,2),F(3,4),F(5,7),F(2,9),F(11,3),F(13,5)))
rows.append(exercise('heterogeneous_positive_rates',heterogeneous,s.hard_search(heterogeneous,F(2),100),14))

# The generic zero-weight route is acquired immediately, including an ell=3 jump.
zero = [((0,0),(1,0),1),((1,0),(0,0),1),((3,0),(1,2),2),((1,2),(3,0),3)]
zero_bundle = s.generic_search(zero,F(2),1)
assert zero_bundle['certificate']['S'] == 0 and zero_bundle['certificate']['ell'] == 3
rows.append(exercise('S_zero_ell_three',zero,zero_bundle,30))

# More-than-two-satellite raw baseline, with zero weights found not supplied.
star = [((0,0,0,0),(1,0,0,0),1),((1,0,0,0),(0,0,0,0),1)]
for j in range(1,4):
    u=tuple(2*int(i==0)+int(i==j) for i in range(4))
    v=tuple(int(i==0)+2*int(i==j) for i in range(4))
    star.extend([(u,v,F(j,2)),(v,u,F(j+1,3))])
rows.append(exercise('four_species_zero_profile_acquired',star,s.generic_search(star,F(2),1),12))

# A generic K1>0 case is a semantic profile test, NOT a proved all-rate accelerator.
unary = raw+[((2,0,0),(1,1,0),F(3,5)),((1,1,0),(2,0,0),F(7,4))]
eta = F(1,8)
manual_profile_trials = 0
while True:
    cc = s.derive(s.recognize(unary),F(2),(eta,F(0)))
    manual_profile_trials += 1
    if cc['status'] == 'CERTIFIED_REQUESTED_T_MOMENT':
        break
    eta /= 2
    assert manual_profile_trials <= 100
assert cc['K1'] > 0
rows.append(exercise('K1_positive_candidate_profile_semantic_check',unary,
    dict(status='CERTIFIED',certificate=cc,acquisition=dict(route='test-only eta halving, no all-rate termination claim',profiles=manual_profile_trials)),14))

# Permutations, duplicate splitting, input order, and validated null channels.
metamorphic = []
for p in permutations(range(3)):
    rr = [(tuple(u[i] for i in p),tuple(v[i] for i in p),k) for u,v,k in reversed(raw)]
    u,v,k = rr.pop()
    rr.extend([(u,v,k/3),(u,v,2*k/3),((0,0,0),(0,0,0),F(1))])
    b = s.hard_search(rr,F(2),100)
    assert b['status'] == 'CERTIFIED'
    assert b['certificate']['weights'] == tuple(F(1,2048) if p[j] == 1 else F(0) for j in b['certificate']['satellite_coordinates'])
    assert s.receive_structural(rr,s.encode(b['qualitative']))
    metamorphic.append(dict(permutation=p,open_coordinate=b['certificate']['open_coordinate'],profiles=b['acquisition']['profiles']))

# All-linear-profile obstruction: opposing pure rays require contradictory orders.
opposing = [((0,0,0),(1,0,0),1),((1,0,0),(0,0,0),1)]
for u,v in [((1,2,0),(1,1,1)),((1,1,1),(1,0,2)),((1,1,1),(2,1,0))]:
    opposing.extend([(u,v,F(1)),(v,u,F(1))])
opp = s.generic_search(opposing,F(2),100)
assert opp['status'] == 'UNKNOWN'
assert s.hard_structural(opposing)['status'] == 'UNKNOWN'
pure_sign_checks = 0
for w in product([F(0),F(1,4),F(1,2),F(1)],repeat=2):
    pp = s.derive(s.recognize(opposing),F(2),w)
    assert pp['status'] == 'PROFILE_REJECTED' and not all(u>0 for u in pp['pure'])
    pure_sign_checks += 1

# A quantitative cap does not erase an available qualitative theorem.
capped = s.hard_search(raw,F(2),1)
assert capped['status'] == 'UNKNOWN'
assert capped['qualitative']['status'] == 'CERTIFIED_ALL_FINITE_EXPONENTIAL_MOMENTS'
assert s.receive_structural(raw,s.encode(capped['qualitative']))
generic_capped = s.generic_search(raw,F(2),25)
assert generic_capped['status'] == 'UNKNOWN'

# Structural admission never invokes any numerical profile or halving code.
saved_derive = s.derive
def forbidden(*args,**kwargs):
    raise AssertionError('qualitative interface invoked numerical profile')
s.derive = forbidden
structural = s.hard_structural(raw)
huge_rates = s.hard_raw((10**100, F(1,10**100),1,1,1,1,2,1))
structural_huge_rates = s.hard_structural(huge_rates)
assert s.receive_structural(huge_rates,s.encode(structural_huge_rates))
s.derive = saved_derive
assert structural['profile_evaluations'] == 0

# Raw top support truly fails: every leading source contains A, so singleton C
# is an A-free invariant face. No previous theorem's instability claim is invented.
assert all(u[0] >= 1 and v[0] >= 1 for u,v,k in raw if sum(u) == 3)

# Re-derivation rejects material corruption, including factored-constant fields.
cert = s.encode(demo['certificate'])
tamper_rejected = []
mutations = {
    'raw_hash':lambda q:q.update(raw_sha256='0'*64),
    'open_coordinate':lambda q:q.update(open_coordinate=1),
    'pure_coefficient':lambda q:q['pure'].__setitem__(1,'1'),
    'ell':lambda q:q.update(ell='1'),
    'c':lambda q:q.update(c='1'),
    'zeta':lambda q:q.update(zeta='100'),
    'tail_cut':lambda q:q['B_cuts'].__setitem__(1,1),
    'implicit_box_size':lambda q:q.update(exception_states_not_enumerated=0),
    'foster_exponent':lambda q:q['foster_constant_factored'].update(exponent=0),
    'foster_bit_bound':lambda q:q['foster_constant_factored'].update(expanded_numerator_bits_upper=1),
    'unearned_all_t_scope':lambda q:q.update(guarantee='all t certified by every profile'),
    'extra_field':lambda q:q.update(oracle='accepted'),
}
for label,mutate in mutations.items():
    c = copy.deepcopy(cert)
    mutate(c)
    assert not s.receive(raw,F(2),demo['certificate']['weights'],c)
    tamper_rejected.append(label)
for key,value in [('profile_evaluations',1),('mediator_coordinate',2),('numerical_foster_constants_provided',True)]:
    q=s.encode(structural);q[key]=value
    assert not s.receive_structural(raw,q)
    tamper_rejected.append('structural_'+key)

bad_inputs = []
variants = [
    ('float_rate',[(raw[0][0],raw[0][1],1.0)]+raw[1:]),
    ('bool_rate',[(raw[0][0],raw[0][1],True)]+raw[1:]),
    ('zero_rate',[(raw[0][0],raw[0][1],0)]+raw[1:]),
    ('float_complex',[((0.0,0,0),(1,0,0),1)]+raw[1:]),
    ('negative_complex',[((-1,0,0),(1,0,0),1)]+raw[1:]),
    ('scalar',[((0,),(1,),1),((1,),(0,),1)]),
    ('not_WR',raw[:-1]),
    ('unseeded_channel',raw+[((0,2,0),(1,1,0),1),((1,1,0),(0,2,0),1)]),
    ('higher_stripped_order',raw+[((1,3,0),(1,0,3),1),((1,0,3),(1,3,0),1)]),
    ('extra_open_species',raw+[((0,0,0),(0,1,0),1),((0,1,0),(0,0,0),1)]),
]
for label,rr in variants:
    try:s.recognize(rr)
    except (ValueError,TypeError):bad_inputs.append(label)
    else:raise AssertionError(label)
for label,action in [
    ('float_t',lambda:s.hard_search(raw,2.0,10)),
    ('float_weight',lambda:s.derive(s.recognize(raw),F(2),(0.5,0))),
    ('bool_budget',lambda:s.hard_search(raw,F(2),True)),
    ('zero_budget',lambda:s.generic_search(raw,F(2),0)),
    ('t_one',lambda:s.generic_search(raw,F(1),1)),
]:
    try:action()
    except (ValueError,TypeError):bad_inputs.append(label)
    else:raise AssertionError(label)

print(json.dumps(s.encode(dict(cases=rows,metamorphic=metamorphic,
    capped_quantitative_preserves_qualitative=capped,generic_capped=generic_capped,
    opposing_profile_class_obstruction=dict(budgeted_result=opp,exact_sign_controls=pure_sign_checks,
        logical_scope='no inverse-linear profile can have both pure coefficients positive; stability remains UNKNOWN'),
    structural=structural,structural_huge_rates=structural_huge_rates,
    prior_top_face_obstruction='every cubic source requires A, so singleton satellite support cannot activate A',
    tampered_fields_rejected=tamper_rejected,raw_domain_rejections=bad_inputs,
    finite_exception_boxes_enumerated=False,foster_powers_expanded=False,
    simulations_used=False,tests_supplement_ordinary_proof=True)),indent=2,sort_keys=True))
