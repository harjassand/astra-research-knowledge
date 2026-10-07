#!/usr/bin/env python3
"""Acquire public rational weight/Euler/scientific bounds; no empirical variance."""
from fractions import Fraction as F
from pathlib import Path
import argparse, importlib.util, json, time
spec=importlib.util.spec_from_file_location('owned_pipeline',Path(__file__).with_name('cutoff_euler_sampler.py'))
s=importlib.util.module_from_spec(spec); spec.loader.exec_module(s)

def acquire(N,T,R,quadrature=128):
    start=time.perf_counter(); c=s.Compiler(N,T,R,F(1,1000),701); c.precision()
    p=2; theta=F(1,10); young=F(1,10); k=c.k
    eLc=s.exp_bounds(c.Lc/(k*k),96)[1]
    Ap=F(p,4)*(c.Lc+young)*eLc
    d=Ap*(1+theta)/4
    noiseK=2*Ap*(1+1/theta)
    denom=F(N,3*c.Lc)-noiseK; assert denom>0
    noise_factor=1+6*noiseK/denom
    exponent=F(p*c.Tc,4*k*k)+F(p*c.B*c.B,4*young)+Ap*(1+1/theta)*c.B*c.B/(2*N)
    pref=s.exp_bounds(exponent,96)[1]*noise_factor
    # Denominator lower rectangles: sinch>=1,f(y)<=y4/12,d0>=1/2.
    h=F(1,quadrature); low=F(0)
    for j in range(8*quadrature):
        a=j*h; b=a+h
        lo,_=s.exp_bounds(-c.Lambda*b*b/8-b**4/192,80)
        low+=h*a*a*lo
    assert low>0
    # Numerator: retained seed tilt, cancel the negative scalar shift first.
    D=d-c.Lambda/(16*c.d0)+F(1,24*k*k); a=F(1,256)
    U=16; high=F(0)
    for j in range(U*quadrature):
        lo=j*h; hi=lo+h; tlo=lo*lo; thi=hi*hi
        vertex=D/(2*a)
        x=vertex if tlo<=vertex<=thi else (tlo if vertex<tlo else thi)
        _,e=s.exp_bounds(-a*x*x+D*x,80)
        high+=h*thi*e
    assert U*U>=2*max(D,F(0))/a
    # Quartic tail: Gamma(3/4)<2, pi cancels, deliberately loose factor4096.
    quartic_tail=F(4096,1<<(int(a*U**4/4)))
    outer=c.k*c.k/F(64)+c.Lambda/(16*c.d0)-F(1,24*k*k)-d
    assert outer>0
    gaussian_tail=F(max(1,s.ceilq(1/outer)**2),2)
    # This whole Gaussian integral bound is conservative but finite/public.
    K2=pref*(high+quartic_tail+gaussian_tail)/low
    mean_inverse=s.exp_bounds(c.B*c.B/2,96)[1]
    c.precision(); stat=s.ar.sqrt_iv(K2/R).hi*mean_inverse
    # Improved integrated lag: integral_t E|Euler_t-X_floor|² <= A²h²/3+S²h/2.
    # Explicit global constants from the owned cutoff, projection and PSD margin.
    rupper=F(1,5); assert c.r02<=rupper*rupper
    A=c.Lc*rupper/(2*k*k)+c.B/(2*c.s)
    S2=F(c.Tc,2*c.s*c.s)
    Lstar=4*c.La*c.La+16*c.Lsig*c.Lsig
    lag=A*A/(3*T*T)+S2/(2*T)
    CE=Lstar*s.exp_bounds(Lstar,96)[1]*lag
    LV=(c.Lc*rupper+c.B)*k*k/2
    logerr2=LV*LV*2*(CE+lag)
    c.precision(); rootK=s.ar.sqrt_iv(K2).hi
    branch=s.ar.sqrt_iv(CE).hi*k*k/F(4,5)  # 1/sqrt(1-r0)<=1/(1-rupper)<=5/4
    euler=mean_inverse*rootK*(2*s.ar.sqrt_iv(logerr2).hi+branch)
    # Scientific cone bound for the OWN squared-cutoff/contracted heat seed.
    # Seed map unchanged for |m|<=r0/4, output radius<r0/3.
    # a0=2atanh(r0/4)>=r0/2; kappa0>=r0^4/12288 (delta>=1/16).
    hN=c.Lc*k*k/4+c.Lc/(2*k*k)+c.B*k/2
    kappa0=c.r02*c.r02/12288
    kappa_cut=c.r02/(1728*c.Lc) # hit r0/2 from <=r0/3, drift<=r0/8.
    seed_log2=F(8)+c.Lambda+F(1,6)+F(3*N.bit_length(),4)+hN-kappa0*N
    exit_log2=F(8)+2*hN-kappa_cut*c.s*c.s
    drift=A; rlower=F(1,8)
    admitted=N>=c.Lambda*c.Lambda and drift<=rlower/8
    cone_tiny=admitted and seed_log2<=-100 and exit_log2<=-100
    cone=F(1,1<<99) if cone_tiny else F(1)
    systematic=cone+euler
    total=cone+euler+stat+F(1,1000)
    def compact(x):
        # Exact rational bound rounded UP to 32 dyadic bits for compact reporting.
        return F(s.ceilq(x*(1<<32)),1<<32)
    return {'scope':'Public analytic bounds acquired by exact rational rectangles, Taylor and root intervals; not empirical Monte Carlo accuracy',
        'N':N,'T':T,'R':R,'quadrature_grid_per_unit':quadrature,
        'moment':{'seed_radial_normalizer_lower':low,'tilted_radial_numerator_upper':high+quartic_tail+gaussian_tail,
            'seed_tilt_d':d,'net_quartic_tilt_D':D,'conditional_martingale_factor_upper':noise_factor,
            'K2_upper_compact':compact(K2),'mean_weight_inverse_upper':mean_inverse,
            'importance_trace_error_upper_compact':compact(stat)},
        'Euler':{'uniform_drift_magnitude_upper':A,'uniform_noise_Frobenius_squared_upper':S2,
            'drift_Lipschitz_upper':c.La,'noise_Lipschitz_upper':c.Lsig,
            'integrated_Euler_lag_squared_upper':lag,'path_strong_L2_squared_upper':CE,
            'potential_Lipschitz_upper':LV,'trace_error_upper_compact':compact(euler)},
        'cone':{'seed_error_log2_upper':seed_log2,'cutoff_residual_log2_upper':exit_log2,
            'thresholds_pass':admitted,'certifies_cone_error_at_most_2_to_minus99':cone_tiny,'trace_error_upper':cone},
        'combined_averaged_Gibbs_trace_error_upper_compact':compact(total),
        'nontrivial_full_scientific_bound':total<1,
        'physical_emissions_required':N,'native_gate_requirement':'Only reset and ideal single-qubit H,S,X; independent local selectors',
        'wall_seconds':time.perf_counter()-start,
        'attribution':'S02 exact/stopped source and owned pipeline; S01/S03 conditional moment/cutoff bridge; L08 scalar-envelope refinement; root/S08/S03 integrated-lag scaling.',
        'status':'INTERNAL_CONSTRUCTION_AND_RATIONAL_ACQUISITION, external theorem validation and priority UNKNOWN'}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--N',type=int,default=1<<48)
    ap.add_argument('--steps',type=int,default=1); ap.add_argument('--proposals',type=int,default=64)
    ap.add_argument('--quadrature',type=int,default=64); ap.add_argument('--out',required=True)
    args=ap.parse_args(); data=acquire(args.N,args.steps,args.proposals,args.quadrature)
    Path(args.out).write_text(json.dumps(s.stringize(data),indent=2)+'\n')
    print(json.dumps({'output':args.out,'K2':str(data['moment']['K2_upper_compact']),
        'statistical_upper':str(data['moment']['importance_trace_error_upper_compact']),
        'Euler_upper':str(data['Euler']['trace_error_upper_compact']),
        'cone_tiny':data['cone']['certifies_cone_error_at_most_2_to_minus99'],
        'combined':str(data['combined_averaged_Gibbs_trace_error_upper_compact']),
        'wall_seconds':data['wall_seconds']}))
if __name__=='__main__': main()
