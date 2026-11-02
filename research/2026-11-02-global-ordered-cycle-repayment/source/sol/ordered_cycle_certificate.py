#!/usr/bin/env python3
"""Acquire a global return/reward certificate for the proved ordered-cycle grammar.

All admission and parameter decisions use exact integers/Fractions. Unsupported
raw lists return UNKNOWN. Huge final powers are explicit exact factored values,
not materialized rationals or practical numerical performance claims.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import permutations
from math import isqrt
import json

P=Path(__file__).resolve().parent

def ceilq(x):
    x=F(x);return -(-x.numerator//x.denominator)

def ceilsqrt(x):
    x=F(x);n=isqrt(x.numerator//x.denominator)
    return n if n*n*x.denominator>=x.numerator else n+1

def complexes(k):return [(0,0,0),(1,1,0)]+[(j,j-1,j-1) for j in range(2,k+1)]

def raw_cycle(k,rates=None):
    C=complexes(k);rates=[F(1)]*(k+1) if rates is None else list(map(F,rates))
    assert len(rates)==k+1 and min(rates)>0
    return [(C[j],C[(j+1)%(k+1)],rates[j]) for j in range(k+1)]

def recognize(raw):
    table={};discarded=0
    for y,z,c in raw:
        if len(y)!=3 or len(z)!=3 or any(type(n) is not int or n<0 for n in tuple(y)+tuple(z)):
            return None,'malformed three-species integer endpoint'
        c=F(c)
        if c<=0:return None,'nonpositive rate'
        if tuple(y)==tuple(z):discarded+=1;continue
        key=(tuple(y),tuple(z));table[key]=table.get(key,F(0))+c
    if len(table)<4:return None,'not the proved k>=3 grammar'
    k=len(table)-1;C=complexes(k)
    for order in permutations(range(3)):
        actual=[tuple(v[order[j]] for j in range(3)) for v in C]
        keys=[(actual[j],actual[(j+1)%(k+1)]) for j in range(k+1)]
        if set(keys)==set(table):
            return {'k':k,'coordinate_permutation':order,'rates':[table[e] for e in keys],
                    'discarded_physically_null_channels':discarded},None
    return None,'raw channels do not match the proved ordered-cycle grammar'

def acquire(raw,u=F(21,20),t=F(11,10)):
    recognized,reason=recognize(raw)
    if recognized is None:return {'status':'UNKNOWN','reason':reason}
    u,t=F(u),F(t)
    if not 1<u<t:return {'status':'UNKNOWN','reason':'require exact 1<u<t'}
    k=recognized['k'];kap=recognized['rates'];total=sum(kap);delta=1-1/t;zeta=1-u/t;rho=1-delta/2
    partial=[sum(kap[:j+1]) for j in range(k+1)]
    R=max(sum(kap[:j])/kap[j] for j in range(1,k+1));S=sum(kap[:k])/kap[k]
    Ahi=ceilq(max(2*k,4*k*R*t**(3*k)/delta))
    Bhi=ceilq(max(2*k,2*k*(kap[0]/kap[1]+2*S)*t**(3*k)/delta))
    Chi=ceilq(max(2*k,2*k*(kap[0]/(2*kap[2])+kap[1]/kap[2]+2*S)*t**(3*k)/delta))
    d=kap[1]/(kap[0]+kap[1])*kap[1]/(kap[0]/2+kap[1]+kap[2])
    for j in range(3,k+1):d*=kap[j]/partial[j]
    J0=k*(k+1);L0=2*t**3;CT=F(2)**(J0+2)*L0**J0;Cout=t**(3*(k+1))*CT;U=4*S
    rho_target=F(1)/(F(2)**(k+2)*L0**(k+1))
    K=max(2*k,k-2+ceilsqrt(S/rho_target),ceilq(16*U*Cout/(d*delta)))
    assert S/F(K-k+2)**2<=rho_target
    assert K>=16*U*Cout/(d*delta)
    Bstar=K+k;DC=2*(k-1)*R;E=t**(3*(k+1));G=4*(DC*E+1);rB=kap[1]/kap[0]
    fmax=G*(Bstar+rB*F(Bstar*(Bstar+1),2));epsilon=delta/(8*rho)
    dC=F(1,2)*kap[1]/(kap[0]+kap[1])*kap[1]/(kap[0]/2+kap[1]+kap[2]*Bstar)
    DB=2*kap[0]/kap[1]+2*(k-2)*R
    bmin=ceilq(max(2*k,Bstar+1,4*(k-2)*R,2*DB*E/(delta*dC)))
    cmin=ceilq(max(2*k,2*DC,Bstar+1))
    J=3*k+3;Cbad=4*k*R+4*k*J*R*R;dA=kap[k-1]/(8*kap[k])
    amin=ceilq(max(2*k*(J+1),2*R,4*(k+J)*R,2*Cbad*t**(3*J)/(delta*dA)))
    Cnorm=k*(1+1/kap[0])*u**(3*k)
    Cbody=(k+1)*(1+1/kap[0])*u**(3*(k+1))
    Caxis=J*(1+1/kap[0])*u**(3*J)
    Cint=(1+1/kap[0])*(k+2)*t**(3*(k+1))*(1+CT)
    # Exact sufficient domination: C*s^M<=h and C*M*s^M<=h.
    def geometric(C,h):return ceilq(max(1,C/(zeta*h)))
    def linear_geometric(C,h):return ceilq(max(1,4/(zeta*zeta),2/(zeta*min(h/C,F(1)))))
    requirements={
        'global_complement_box':Ahi+Bhi+Chi,
        'section_profile_feedback':ceilq(fmax/epsilon),
        'normalizer_full_occupation':geometric(Cnorm,delta/8),
        'low_B_validity':Bstar+cmin,
        'low_C_validity':Bstar+bmin,
        'axis_all_landing_and_error_bounds':amin,
        'low_B_full_occupation':linear_geometric(Cbody,F(1,2)),
        'low_C_full_occupation':geometric(Cbody,delta*dC/4),
        'interior_full_occupation':linear_geometric(Cint,d*delta/16),
        'axis_full_occupation':linear_geometric(Caxis,delta*dA/4),
        'low_B_unit_residual_margin':ceilq(4/delta**2),
        'low_C_unit_residual_margin':ceilq(4/(dC*delta**2)),
        'interior_unit_residual_margin':ceilq(32/(d*delta**3)),
        'axis_unit_residual_margin':ceilq(8/(dA*delta**3)),
    }
    head=max(requirements.values())+1
    assert fmax/F(head+1)<=epsilon and epsilon<=(t-1)/2
    assert head>=Ahi+Bhi+Chi and head>=Bstar+cmin and head>=Bstar+bmin and head>=amin
    cb=all(kap[j]*kap[2]**(j-3)==kap[3]**(j-2) for j in range(4,k+1))
    Jdel=6*k-5;path=(2*k+1)*head;Qcol=total*F(head+Jdel)**(3*k-2);pmin=min(kap)/Qcol
    assert 0<pmin<=1
    params={name:str(value) for name,value in {
        'u':u,'t':t,'delta':delta,'zeta':zeta,'rho':rho,'R':R,'S':S,
        'A_hi':Ahi,'B_hi':Bhi,'C_hi':Chi,'interior_K':K,'section_B_cutoff':Bstar,
        'C_T':CT,'C_out':Cout,'negative_interior_word_d':d,'D_C':DC,
        'profile_G':G,'profile_ratio_kappa1_over_kappa0':rB,'f_max':fmax,
        'profile_feedback_epsilon':epsilon,'negative_low_C_d':dC,'D_B':DB,
        'axis_J':J,'axis_bad_constant':Cbad,'axis_negative_d':dA,
        'normalizer_cost':Cnorm,'bounded_plane_cost':Cbody,'axis_cost':Caxis,
        'interior_cost':Cint,'head_radius_M':head}.items()}
    return {'status':'PROVED_GRAMMAR_CERTIFICATE_ACQUIRED','scope':'Author-derived global theorem; not independently audited, not general weak-reversibility admission.',
            'raw_family':{'k':k,'rates':[str(v) for v in kap],'coordinate_permutation':recognized['coordinate_permutation'],
                          'genuine_channels':k+1,'discarded_null_channels':recognized['discarded_physically_null_channels'],
                          'stoichiometric_rank':3,'deficiency':k-3,'complex_balanced_rate_locus':cb},
            'consequence':'Nonexplosion, positive recurrence, and finite physical stationary (1+q)*u^M reward, with a common actual return/output contract.',
            'parameters_exact':params,'head_requirements_exact':{n:str(v) for n,v in requirements.items()},
            'section_profile_exact':'f_b=G*((Bstar-b)+(kappa1/kappa0)*(Bstar-b)*(Bstar+b+1)/2) for b<Bstar; zero otherwise.',
            'normalizer':'First degradation or k genuine jumps, repeated until Z={A=0} union {B=C=0} or M<=head; its actual F reward and boundary value define V_off<=t^M.',
            'head_trace_probability_exact_factored':{'base':str(pmin),'exponent':str(path)},
            'stationary_reward_bound_exact_factored':'kappa0*((1+1/kappa0)*u^head+2*t^(head+3))*(1+Npath*pmin^(-Npath))',
            'bound_parameters_exact':{'kappa0':str(kap[0]),'head':str(head),'u':str(u),'t':str(t),
                                      'Npath':str(path),'pmin':str(pmin),'collar_overshoot':Jdel,'Qcollar':str(Qcol)},
            'materialization_cost_boundary':{'expanded_probability_denominator_bits_upper':str(path*pmin.denominator.bit_length()),
                                             'expanded_probability_numerator_bits_upper':str(path*pmin.numerator.bit_length()),
                                             'factored_powers_materialized':False},
            'not_claimed':['general weak-reversibility decision','independent audit','historical novelty','practical mixing or tail computation','exponential global physical return-time moment']}

if __name__=='__main__':
    rows=[]
    for k in [3,4,5,8]:
        rates=[F(1)]*(k+1);rates[-1]=F(2)
        cert=acquire(raw_cycle(k,rates));assert cert['status']=='PROVED_GRAMMAR_CERTIFICATE_ACQUIRED'
        assert cert['raw_family']['complex_balanced_rate_locus']==(k==3)
        name='global_certificate_k'+str(k)+'.json';(P/'results'/name).write_text(json.dumps(cert,indent=2)+'\n')
        rows.append({'k':k,'deficiency':k-3,'complex_balanced':cert['raw_family']['complex_balanced_rate_locus'],
                     'head':cert['parameters_exact']['head_radius_M'],'file':name})
    rejected=raw_cycle(4);rejected[2]=((2,1,1),(3,3,2),F(1))
    no=acquire(rejected);assert no['status']=='UNKNOWN'
    (P/'results/compiler_summary.json').write_text(json.dumps({'scope':'Exact grammar recognition and acquired global proof data; sampled checks are separate.',
        'accepted':rows,'unsupported_control':no},indent=2)+'\n')
    print(json.dumps({'accepted':rows,'unsupported_control':no},indent=2))
