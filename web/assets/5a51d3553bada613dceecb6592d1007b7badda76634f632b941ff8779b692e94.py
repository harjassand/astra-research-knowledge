#!/usr/bin/env python3
"""Public fixed-bound diffusion weight moment by exact interval quadrature.

Every decision/enclosure uses rational arithmetic.  The envelope proof is
uniform for all N>=65536 at M=1/10,B=1/5; this is not empirical Monte Carlo.
"""
from fractions import Fraction as F
import importlib.util
import json
from pathlib import Path
import resource
import time

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('weight_iv',HERE/'certified_two_spin.py')
base=importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)
IV,iv=base.IV,base.iv


def exp_scalar(x):
    """Range-reduced exp with an explicit outward underflow enclosure."""
    base.ledger.add('extended_exp_scalar_calls')
    if x<=-IV.P:
        # e>2 gives exp(-P)<2^-P.  This never declares exact zero.
        return IV(F(0),F(1,1<<IV.P),raw=True)
    if x<0:
        return exp_scalar(-x).reciprocal()
    halves=0
    while x>1:
        x/=2
        halves+=1
    y=base.exp_scalar(x)
    for _ in range(halves):
        y=y*y
    return y


def exp_iv(x):
    x=iv(x)
    return IV(exp_scalar(x.lo).lo,exp_scalar(x.hi).hi,raw=True)


def integrate_envelope(c,d,e,L,panels,lower=False):
    """Darboux enclosures; all of each panel lies in its interval image."""
    step=L/panels
    total=F(0)
    rows=[]
    for j in range(panels):
        a,b=j*step,(j+1)*step
        r=IV(a,b)
        r2=r*r
        value=r2*exp_iv(-c*r2*r2+d*r2+e*r)
        contribution=step*(value.lo if lower else value.hi)
        total+=contribution
        rows.append({'a':str(a),'b':str(b),'integrand_interval':value.json(),
                     'charged_contribution':str(contribution)})
    return total,rows


def gaussian_tail(q,L):
    # Integration by parts and the elementary Gaussian tail bound give
    # int_L^infty r^2 exp(-q r^2)dr <= exp(-qL^2)(L/(2q)+1/(4q^2L)).
    return exp_scalar(-q*L*L).hi*(L/(2*q)+1/(4*q*q*L))


def acquire(p=2,panels=512):
    assert p>=1
    IV.precision(96)
    M,B=F(1,10),F(1,5)
    Lambda,Lc,Tc=M+1,2*M+1,3*(2*M+1)
    Nmin,sqrtN,fourthN=65536,F(256),F(16)
    dmin=1-Lambda/(2*sqrtN)
    theta,young=F(1,10),F(8)
    amplification=exp_scalar(Lc/(2*sqrtN)).hi
    beta=B/(2*sqrtN)
    d=F(p)*Lc*amplification**2*(1+theta)/16
    e=F(p)*B*amplification/4
    Kz=F(p)*Lc*amplification**2*(1+1/theta)/2
    ellz=F(p)*B*amplification/2
    K=Kz+young/2
    a=F(Nmin)/(3*Tc)
    assert a>K
    conditional_martingale_factor=1+6*K/(a-K)
    exponent_constant=(F(p)*Tc/(4*sqrtN)+Kz*beta**2+
                       ellz*beta+ellz**2/(2*young))
    prefactor=exp_scalar(exponent_constant).hi*conditional_martingale_factor
    c=F(11,2880)
    upper_d=d-Lambda/16+1/(24*sqrtN)
    L=F(16)
    assert upper_d/L**2+e/L**3<=c/2
    upper,upper_panels=integrate_envelope(c,upper_d,e,L,panels)
    tail_q=c*L**2/2
    upper_tail=gaussian_tail(tail_q,L)
    # For u>=1 the seed Gaussian outer tail, even after the tilt, is bounded
    # by R^2 exp(-R^2), uniformly over all N>=Nmin. delta>=3/50 is certified
    # by the scalar logcosh enclosure reproduced in the proof text.
    delta_lower=F(3,50)
    exp_044=exp_scalar(F(11,25))
    cosh_1=base.even_series_iv(iv(1),'cosh')
    assert exp_044.lo>cosh_1.hi
    outer_coefficient=delta_lower*sqrtN/4-d-1/(4*sqrtN)-e/(2*fourthN)
    assert outer_coefficient>=1
    outer_tail=gaussian_tail(F(1),2*fourthN)
    lower,lower_panels=integrate_envelope(F(1,192),-Lambda/(16*dmin),F(0),L,panels,lower=True)
    assert lower>0
    seed_moment_upper=(upper+upper_tail+outer_tail)/lower
    Kp=prefactor*seed_moment_upper
    # Separate the universal every-path denominator lower bound.
    inverse_mean_squared=exp_scalar(B*B).hi
    proposal_coeff=Kp*inverse_mean_squared if p==2 else None
    return {'status':'CERTIFIED_PUBLIC_UNIFORM_WEIGHT_MOMENT',
      'worker_id':'c07_s03','parameters':{'M':str(M),'B':str(B),'Lambda':str(Lambda),
         'Lc':str(Lc),'trace_C_upper':str(Tc),'p':p,'N_min':Nmin,
         'all_N_at_least_N_min':True,'theta':str(theta),'Young_parameter':str(young)},
      'constants':{'drift_amplification_upper':str(amplification),'seed_quadratic_tilt':str(d),
         'seed_linear_tilt':str(e),'martingale_K':str(K),'martingale_tail_a_lower':str(a),
         'conditional_martingale_factor_upper':str(conditional_martingale_factor),
         'prefactor_exponent_upper':str(exponent_constant),'prefactor_upper':str(prefactor),
         'seed_normalizer_lower':str(lower),'seed_tilt_integral_upper':str(upper+upper_tail+outer_tail),
         'seed_tilt_moment_upper':str(seed_moment_upper),'weight_p_moment_upper':str(Kp),
         'inverse_mean_squared_upper':str(inverse_mean_squared),
         'importance_proposal_coefficient_upper':str(proposal_coeff) if proposal_coeff else None},
      'quadrature':{'method':'Exact rational Darboux/interval sums, not point quadrature',
         'working_dyadic_bits':IV.P,'panels_per_integral':panels,'cap':str(L),
         'upper_quartic_coefficient':str(c),'upper_quadratic_coefficient':str(upper_d),
         'upper_tail_q':str(tail_q),'upper_envelope_tail':str(upper_tail),
         'exterior_seed_tail':str(outer_tail),'exterior_coefficient_lower':str(outer_coefficient),
         'delta_lower':str(delta_lower),'exp_044_interval':exp_044.json(),
         'cosh_1_interval':cosh_1.json(),'lower_panels':lower_panels,'upper_panels':upper_panels},
      'proof_contract':['Uniform fixed M,B, known-parameter stopped/cutoff/Euler law with contracted heat seed.',
         'Conditional martingale bound is used given m0; independence is not assumed.',
         'Only the exact seed moment is integrated; no empirical weight variance is substituted.',
         'At p=2, R>=coefficient/eta^2 controls averaged importance error eta.',
         'Acquisition cost is charged below; practical use is restricted to this admitted fixed-bound instance.']}


def main():
    base.ledger=base.Ledger()
    start,cpu=time.perf_counter(),time.process_time()
    result=acquire()
    result['costs']={**base.ledger.snapshot(),'wall_seconds':time.perf_counter()-start,
        'cpu_seconds':time.process_time()-cpu,
        'process_peak_rss_bytes_macos':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        'direct_Fraction_operations':'Some loop bookkeeping uses Fraction operators directly; counts are helper calls, not complete CPU bit counts.'}
    out=HERE/'evidence/certified_weight_constant.json'
    out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'output':str(out),'status':result['status'],
      'K2_upper_diagnostic':float(F(result['constants']['weight_p_moment_upper'])),
      'proposal_coefficient_diagnostic':float(F(result['constants']['importance_proposal_coefficient_upper'])),
      'normalizer_lower_diagnostic':float(F(result['constants']['seed_normalizer_lower'])),
      'wall_seconds':result['costs']['wall_seconds']}))


if __name__=='__main__': main()
