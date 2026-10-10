#!/usr/bin/env python3
"""Exact, computable global budgets and transport contracts for the homogeneous sampler.

No floating point enters a proof inequality. This does not silently promote the
fixed-precision local-draw program into a complete epsilon-W1 sampler.
"""
from __future__ import annotations
import argparse, hashlib, json, math, time, sys
sys.set_int_max_str_digits(0)
from fractions import Fraction as Q
from pathlib import Path

HERE=Path(__file__).resolve().parent

def asq(x):
    if isinstance(x,dict): return Q(int(x['num']),int(x['den']))
    return Q(x)

def enc(x):
    if isinstance(x,Q): return {'num':str(x.numerator),'den':str(x.denominator)}
    if isinstance(x,dict): return {k:enc(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)): return [enc(v) for v in x]
    return x

def dyadic_below(x):
    x=Q(x)
    assert x>0
    q=max(0,x.denominator.bit_length()-x.numerator.bit_length())
    while Q(1,1<<q)>x:q+=1
    return q,Q(1,1<<q)

def determinant(a):
    a=[[Q(x) for x in row] for row in a]; n=len(a); d=Q(1)
    for i in range(n):
        j=next((j for j in range(i,n) if a[j][i]),None)
        if j is None:return Q(0)
        if j!=i:a[i],a[j]=a[j],a[i];d=-d
        z=a[i][i];d*=z
        for j in range(i+1,n):
            t=a[j][i]/z
            for k in range(i+1,n):a[j][k]-=t*a[i][k]
    return d

def is_psd(a):
    """Exact rational symmetric Schur-complement test, including zero pivots."""
    a=[[Q(x) for x in row] for row in a];n=len(a)
    if any(a[i][j]!=a[j][i] for i in range(n) for j in range(n)):return False
    for i in range(n):
        if a[i][i]<0:return False
        if not a[i][i]:
            if any(a[i][j] for j in range(i+1,n)):return False
            continue
        for j in range(i+1,n):
            for k in range(j,n):
                a[j][k]-=a[i][j]*a[i][k]/a[i][i];a[k][j]=a[j][k]
    return True

def build_budget(h,p,n,r,epsilon):
    h=[[asq(x) for x in row] for row in h];m=len(h);d=p+n;eps=Q(epsilon)
    assert 0<eps<1 and p>=1 and n>=1 and m>=1
    assert all(len(row)==m for row in h) and is_psd(h) and determinant(h)>0
    assert 4*(m+1)**2<=r<=min(p,n), 'Outside finite-output theorem scope'
    alpha=math.prod((1-Q(2*j,r)) for j in range(1,(m+1)//2+1))
    c2=math.prod(1/(1-Q(2*j,r)) for j in range(1,m+1))
    assert alpha>=Q(1,2) and c2<2
    hmax=max(sum(abs(x) for x in row) for row in h)
    hmin=determinant(h)/hmax**(m-1)
    B=max(Q(1),sum(h[i][i] for i in range(m))) # >= Frobenius coefficient norm
    W=max(Q(1),1/hmin) # >= ||H^{-1/2}||, deliberately loose
    # Five bad-event buckets, all charged against an actual ideal coupling.
    for k in range(1,100000):
        eta=Q(1,1<<k);T=k
        normal_count=T*(m+r+p+n)
        L0=2
        while 2*normal_count*Q(1,1<<(L0*L0//2))>eta:L0+=1
        R=2*d*L0+1
        if 5*d*eta<=eps*eps/16 and 5*R*eta<=eps/4:break
    else:raise RuntimeError('Budget loop failed')
    _,v0=dyadic_below(eta*eta/(4*T*T))
    L=p*L0 # >= sqrt(p)*L0, the analyzed ideal X norm cutoff
    tq=0;t=Q(1)
    while (4*t>Q(4,9) or 4*t>Q(L*L,r) or
           (5*L)**(2*m)*8**r*(4*t)**(r-m)>eta**4/(4*T**4)):
        tq+=1;t/=2
    # Polar-coupling transport constants. Every primitive error below <=rho.
    Lambda=Q(r)*W*m*L0/v0
    Klambda=(Q(r)/v0*(2*W*m+2*W*W*m*L0)
             +4*W*m*L0*(2*r*r*(2*L0+1)/v0**2+1)+1)
    Ek=1+B*B*(2*Lambda+1)*Klambda
    Kx=2*p+2*p*L0*Ek+1
    Ky=n+1+2*n*L0*Kx/t
    Kout=Kx+Ky
    Kaccept=2*B*B*(Lambda+1)*Klambda
    delta_out=min(Q(1),eps/2,eps/(B*(2*R+1)))
    thresholds={
        'normal_perturbation_at_most_one':Q(1),
        'H_factor_positive':hmin/2,
        'V_margin':v0/(2*r*(2*L0+1)),
        'lambda_margin':1/Klambda,
        'K_factor_positive':1/(2*Ek),
        'X_conditioning_margin':min(Q(1),Q(r)*t/(2*L+1))/Kx,
        'pair_error_and_residual':delta_out/Kout,
        'acceptance_disagreement':eta/(4*T*(Kaccept+2)),
        'normal_seed_output_ball_margin':1/Kout,
    }
    rho_bits,rho=dyadic_below(min(thresholds.values()))
    # On |Z|<=L0, the entire quantile cell lies in [-L0-1,L0+1].
    # phi(z)>=2^{-((L0+1)^2+2)} there; cell quantile width <=rho/64.
    uniform_bits=rho_bits+(L0+1)**2+8
    round_bits=rho_bits+(max(p,n,m)+1).bit_length()+2
    result={
      'scope':'Homogeneous rational c=g=0; native Mp certificate must be separately verified',
      'epsilon':eps,'dimensions':{'m':m,'p':p,'n':n},'r':r,
      'ideal_acceptance_lower_bound':alpha,'tilted_L2_squared_upper':c2,
      'H_eigenvalue_lower':hmin,'H_eigenvalue_upper':hmax,'coefficient_norm_upper':B,
      'eta':eta,'bad_probability_upper':5*eta,'trial_cap':T,
      'normal_count_upper':normal_count,'normal_cutoff_L0':L0,
      'normal_tail_union_upper':2*normal_count*Q(1,1<<(L0*L0//2)),
      'V_analysis_min':v0,'V_implementation_min':v0/2,
      'X_analysis_norm_upper':L,'conditioning_t':t,'conditioning_t_exponent':tq,
      'conditioning_ideal_S_ge':4*t,'conditioning_implementation_S_ge':2*t,
      'conditioning_raw_bound_squared_upper':Q((5*L)**(2*m)*8**r)*(4*t)**(r-m),
      'output_norm_cap':R,'pair_error_max':delta_out,
      'bad_distance_sqrt_term_squared_upper':5*d*eta,
      'bad_distance_bounded_output_term_upper':5*R*eta,
      'primitive_error_rho':rho,'primitive_error_bits':rho_bits,
      'normal_uniform_bits':uniform_bits,'suggested_coordinate_fraction_bits':round_bits,
      'per_acceptance_uniform_bits':rho_bits,
      'transport_constants':{'Lambda':Lambda,'K_lambda':Klambda,'K_K_residual':Ek,
        'K_x':Kx,'K_y':Ky,'K_pair':Kout,'K_acceptance':Kaccept},
      'primitive_error_upper_constraints':thresholds,
      'required_per_call_error_contracts':[
        'Each finite normal coordinate is within rho of its coupled exact standard normal on |Z|<=L0.',
        'H Cholesky proposal factor P_H has ||P_H-H||op<=rho; its solves are exact or separately charged.',
        'sqrt(r/Vhat) interval midpoint has absolute error<=rho; lambda vector final rounding norm<=rho.',
        'K(lambda_hat) Cholesky factor P has ||P-K(lambda_hat)||op<=rho.',
        'X distance from P^{-1/2}O times finite seed, including solve/round, is <=rho.',
        'Y distance from exact projection at Xhat of finite seed, including solve/round, is <=rho.',
        'Acceptance probability enclosure at lambda_hat has width<=rho; exact cell comparison or zero fallback on overlap.',
        'Acceptance uniform cells have width<=rho; all primitive tapes are independent uniform bits.',
        'Exact separated V, whitened Gram, output norm and final residual checks are enforced.',
        'No unbudgeted implementation abort, certificate failure, or adaptive precision limit on the good event.'
      ],
      'claim_status':'Budget and transport inequalities implemented; full sampler requires all listed contracts',
    }
    assert_budget(result)
    return result

def assert_budget(b):
    eps=b['epsilon'];eta=b['eta'];T=b['trial_cap'];rho=b['primitive_error_rho']
    assert b['ideal_acceptance_lower_bound']>=Q(1,2)
    assert Q(1,1<<T)<=eta
    assert b['normal_tail_union_upper']<=eta
    assert b['V_analysis_min']<=eta*eta/(4*T*T)
    assert b['conditioning_raw_bound_squared_upper']<=eta**4/(4*T**4)
    assert all(rho<=x for x in b['primitive_error_upper_constraints'].values())
    assert b['bad_distance_sqrt_term_squared_upper']<=eps*eps/16
    assert b['bad_distance_bounded_output_term_upper']<=eps/4
    assert b['pair_error_max']<=eps/2
    assert Q(1,1<<b['normal_uniform_bits'])*2**((b['normal_cutoff_L0']+1)**2+2)<=rho/64
    return True

def inspect_local_draw(report,budget):
    """Fail-closed integration: compare evidence to contracts, never infer missing ones."""
    q=lambda x:asq(x)
    rho=budget['primitive_error_rho'];draw=report['draw']
    seeds=draw['seed_generation']['seeds'];out=draw['output'];prop=draw['proposal'];acc=draw['acceptance']
    checks={
      'observed_normal_coordinate_errors_meet_rho':all(q(s['coordinate_error_bound'])<=rho for s in seeds),
      'H_factor_residual_meets_rho':q(prop['H_factor_residual_bound'])<=rho,
      'K_factor_residual_meets_rho':q(draw['precision_factor']['residual_norm_bound_delta'])<=rho,
      'X_solve_error_meets_rho':q(out['squared_distance_to_L_inverse_transpose_rounded_seed_upper'])<=rho*rho,
      'Y_projection_rounding_meets_rho':q(out['fiber_rounding_error_squared'])<=rho*rho,
      'acceptance_squared_interval_width_meets_rho_squared':q(acc['squared_acceptance_upper'])-q(acc['squared_acceptance_lower'])<=rho*rho,
      'uniform_cell_width_meets_rho':Q(1,1<<acc['uniform_bits'])<=rho,
      'residual_within_requested_epsilon':q(out['final_residual_squared'])<=budget['epsilon']**2,
      'output_norm_within_cap':q(out['x_norm_squared'])+q(out['y_norm_squared'])<=budget['output_norm_cap']**2,
    }
    unresolved=[
      'Current entry point is a single fixed pseudorandom replay, not independent random bits and capped trials.',
      'No runtime enforcement of the global V, conditioning, output-ball and fallback contract.',
      'No guarantee all numerical certificates succeed on every analyzed good tape.',
      'Observed successful seed-cell certificates do not alone bound every possible generator abort.',
    ]
    return {'full_epsilon_W1_sampler_certified':False,'checks':checks,'unresolved':unresolved,
            'observed_local_draw_is_not_distributional_evidence':True}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--epsilon',default='1/16777216')
    ap.add_argument('--report',type=Path,default=HERE/'CERTIFIED_DRAW.json')
    ap.add_argument('--output',type=Path,default=HERE/'PROBABILITY_BUDGET.json');args=ap.parse_args()
    started=time.perf_counter()
    if args.report.exists():
        report=json.loads(args.report.read_text());cert=report['native_certificate'];ds=report['dimensions']
        b=build_budget(cert['H'],ds['p'],ds['n'],cert['r'],Q(args.epsilon))
        integration=inspect_local_draw(report,b)
        provenance={'core_report_sha256':hashlib.sha256(args.report.read_bytes()).hexdigest()}
    else:
        from certified_draw import make_raw_input,acquire_certificate,N
        h,r,_=acquire_certificate(make_raw_input());b=build_budget(h,N,N,r,Q(args.epsilon))
        integration={'full_epsilon_W1_sampler_certified':False,'unresolved':['No core report present.']};provenance={}
    payload={'budget':enc(b),'integration':integration,'provenance':provenance,'runtime_seconds':time.perf_counter()-started}
    args.output.write_text(json.dumps(payload,indent=2)+'\n')
    print(json.dumps({'epsilon':str(b['epsilon']),'r':b['r'],'trial_cap':b['trial_cap'],
      'normal_cutoff':b['normal_cutoff_L0'],'conditioning_t_bits':b['conditioning_t_exponent'],
      'primitive_error_bits':b['primitive_error_bits'],'normal_uniform_bits':b['normal_uniform_bits'],
      'fraction_bits':b['suggested_coordinate_fraction_bits'],'integration':integration,'runtime_seconds':payload['runtime_seconds']},indent=2))

if __name__=='__main__':main()
