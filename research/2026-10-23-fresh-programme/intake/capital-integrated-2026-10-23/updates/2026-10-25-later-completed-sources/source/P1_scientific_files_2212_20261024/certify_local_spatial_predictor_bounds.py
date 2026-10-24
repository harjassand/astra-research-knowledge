#!/usr/bin/env python3
"""New spatial theorem parameter evaluation, NOT a spatial trajectory run.
Requires the preserved sibling certify_positive_jump_predictor_v2.py.
The code certifies constants for a supplied positive local algorithm whose
endpoint enclosures meet the declared target; it does not execute that algorithm.
"""
from fractions import Fraction as F
from math import factorial
from pathlib import Path
import hashlib,json
from certify_positive_jump_predictor_v2 import ap,sqrt_upper as su,pack_upper as pack,ceildiv

def main():
    side=10; m=side*side
    edges=set()
    for i in range(side):
        for j in range(side):
            v=i*side+j
            for w in [((i+1)%side)*side+j,i*side+(j+1)%side]:
                edges.add(tuple(sorted((v,w))))
    assert len(edges)==2*m and all(sum(i in e for e in edges)==4 for i in range(m))
    H=F(1,8); theta=F(1,128); B=F(128,5); P=32
    step=F(1,1<<32); rho=1-step/2; gap=1-2*H
    assert step<=gap/(2*P-1) and 2*P*H*step<=1 and step<=gap/(16*P*H*H)
    U=[F(m)]; alpha=[F(0)]
    for p in range(1,P+1):
        beta=F(0) if p==1 else 2*p*H+4*p*p*H*H*step
        aa=(1-rho**(2*p))/step-beta
        assert aa>=p*gap/2
        alpha.append(aa)
        U.append((p*p*U[p-1]+sum(F(ap(p,r))*step**(r-1)*U[p-r]
                                      for r in range(2,p+1)))/aa)
        assert U[p]>=m*factorial(p)
    ell=2+su(F(1,2)); C2=2+2*su(3)
    clip,pbest=min((ell*F((p-1)**(p-1),p**p)*U[p]/B**(p-1),p)
                   for p in range(2,P+1))
    phase_unit=step/4*(C2*U[3]/theta+2*su(U[2]*U[3])*su(1/theta))
    pieces={'quantum_clipping_under_jump_law':clip,
       'noise_jumps':F(70)*step*m/(48*theta*theta),
       'hopping_jumps':step*H*H/4*(C2*U[1]/theta+2*su(m*U[1])*su(1/theta)),
       'cross_phase_jumps':4*phase_unit,'onsite_phase_jumps':phase_unit,
       'rational_damping':C2*step*U[1]/(16*theta)}
    columns=4*len(edges)+4*m  # zero remainder columns still paid
    rate=F(columns+2*len(edges)+2*m)/step
    pieces['endpoint_rounding_target']=rate*2*(F(1,1<<80)+F(1,1<<100))*su(1/theta)
    pieces['finite_thermal_initialization']=2*m*F(3,8)**64+(16*m*F(1,1<<128)+2*su(2*m)*F(1,1<<60))*su(1/theta)
    coeff=[F(0),F(P*P)]+[F(ap(P,r))*step**(r-1) for r in range(2,P+1)]
    base=coeff[1]/alpha[P]
    sstar=F(ceildiv(base.numerator,base.denominator)+1)
    while sum(coeff[r]/sstar**r for r in range(1,P+1))>alpha[P]:sstar+=1
    cp=sum(coeff[r]*sstar**(P-r) for r in range(1,P+1))
    pieces['local_radius_exit']=(m*factorial(P)+m*cp)/F(12)**(2*P)
    totalrate=rate+144*m; mean=int(totalrate/2)
    assert totalrate/2==mean
    cap=2*mean+128; J=2*columns+2*len(edges)+3*m+1
    small=F(2,factorial(64))+F(3,factorial(66))+F(64,1<<128)
    pieces['finite_probability_rows']=2*mean*small+F(2,1<<128)+2*cap*F(J,1<<128)
    src=Path(__file__)
    out={'status':'Exact parameter-bound evaluation for the local spatial theorem; no spatial trajectory/ensemble executed.',
       'code_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),
       'helper_sha256':hashlib.sha256(src.with_name('certify_positive_jump_predictor_v2.py').read_bytes()).hexdigest(),
       'graph':{'periodic_square_shape':[side,side],'modes':m,'degree':4,'edges':sorted(edges)},
       'parameters':{'kappa':1,'nu':1,'theta':'1/128','thermal_mean_photons':128,'eta':1,
          'onsite_and_cross_envelopes':1,'each_local_bath_allocation':'1/5','hopping_edge_envelope':'1/32',
          'H':'1/8','Omega':0,'c':1,'T':1,'bins':['1/2','1/2'],'P':P,'chosen_tail_moment':pbest,
          'all_flow_steps_and_epsilon_squared':str(step),'local_radius':12,'s_star':str(sstar),
          'state_grid_bits':80,'required_endpoint_width_bits':100,
          'preparation':'Supplied product thermal coherent mixture; finite initialization is charged.',
          'readout':'Supplied m-port orthonormal disjoint-pair +/- or local menu, total intensity<=S; common finite-latch feedback.'},
       'U1_upper':pack(U[1]),'U2_upper':pack(U[2]),'U3_upper':pack(U[3]),
       'allowances':{k:pack(v) for k,v in pieces.items()},'total_systematic_TV_upper':pack(sum(pieces.values())),
       'cost':{'real_current_field_coordinates':2*m,'charged_noise_columns':columns,
          'ideal_expected_internal_actions':int(rate),'small_Poisson_draws':2*mean,
          'categorical_proposals_cap':2*cap,'categories_per_proposal':J,
          'random_bits_bound_before_initialization':128*(2*mean+2*cap),'initial_random_bits':2*m*129,
          'row_evaluation':'Naive scan is O(categories) per proposal; local cached tree is possible but not benchmarked.',
          'statistical_forecast':'Requires additional independent paths; no statistical estimate is reported.'},
       'precision_scope':'The theorem supplies local algebraic/trig enclosure algorithms. This run evaluates their error target and other constants, not all spatial endpoint operations.',
       'claims_excluded':['practical speedup','executed spatial simulation','acquired measurement','economical rare-record conditioning']}
    dest=src.with_name('LOCAL_SPATIAL_PREDICTOR_PARAMETER_CERTIFICATE.json')
    dest.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ['total_systematic_TV_upper','cost']},indent=2))
    print('clipping',float(clip),'moment',pbest,'exit',float(pieces['local_radius_exit']))
    print(dest)

if __name__=='__main__':main()
