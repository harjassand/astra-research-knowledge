#!/usr/bin/env python3
"""Exact rational constants + bounded IS on a coupled Gaussian Euler path.

No inherited simulation replay. All output is confined to this directory.
Rational normal-tail enclosures are deterministic certificates. The Monte Carlo
coverage theorem assumes ideal independent Gaussian/uniform primitives; the
NumPy/SciPy run is a floating implementation, not a formal random-bit or
floating-point verification. See PROOF.txt for the precise distinction.
"""
from __future__ import annotations
from fractions import Fraction as F
from math import isqrt
from pathlib import Path
import hashlib, json, math, sys, time
import numpy as np
from scipy.special import log_ndtr, ndtri_exp

HERE = Path(__file__).resolve().parent
SOURCE = Path('/Users/harjas/Documents/Codex/2026-10-13/astra-genesis-civilization-enabling-breakthrough-discovery')


def identity(n):
    return [[F(int(i == j)) for j in range(n)] for i in range(n)]


def transpose(a):
    return [list(x) for x in zip(*a)]


def multiply(a,b):
    bt=transpose(b)
    return [[sum((x*y for x,y in zip(row,col)),F(0)) for col in bt] for row in a]


def add(a,b):
    return [[x+y for x,y in zip(ra,rb)] for ra,rb in zip(a,b)]


def diag(values):
    return [[F(values[i]) if i==j else F(0) for j in range(len(values))] for i in range(len(values))]


def fmat(a):
    return np.asarray([[float(x) for x in row] for row in a])


def outward(q,digits=32):
    """Human-readable decimal strings enclosing an exact rational."""
    den=10**digits
    scaled=q.numerator*den//q.denominator
    def fmt(k):
        sign='-' if k<0 else ''
        k=abs(k)
        return sign+str(k//den)+'.'+str(k%den).zfill(digits)
    return [fmt(scaled),fmt(scaled+1)]


def frac_record(q):
    return {'numerator':str(q.numerator),'denominator':str(q.denominator),
            'outward_decimal':outward(q)}


def sqrt_interval(q,digits=55):
    scale=10**digits
    k=isqrt(q.numerator*scale*scale//q.denominator)
    lo,hi=F(k,scale),F(k+1,scale)
    assert lo*lo<=q<=hi*hi
    return lo,hi


def arctan_interval(q,terms=100):
    s=F(0)
    for k in range(terms):
        s+=(-1 if k%2 else 1)*q**(2*k+1)/(2*k+1)
    nxt=q**(2*terms+1)/(2*terms+1)
    return (s,s+nxt) if terms%2==0 else (s-nxt,s)


def pi_interval():
    a,b=arctan_interval(F(1,5))
    c,d=arctan_interval(F(1,239),terms=32)
    return 16*a-4*d,16*b-4*c


PI=pi_interval()


def floor_grid(x,digits=100):
    scale=10**digits
    return F(x.numerator*scale//x.denominator,scale)


def ceil_grid(x,digits=100):
    scale=10**digits
    return F(-((-x.numerator*scale)//x.denominator),scale)


def exp_negative_interval(x,terms=60):
    """e^-x by positive Taylor enclosure of e^(x/2^m), then reciprocal."""
    assert x>=0
    m=0
    while x/(2**m)>F(1,2):
        m+=1
    t=x/(2**m)
    term=F(1); total=term
    for k in range(1,terms+1):
        term=term*t/k
        total+=term
    nxt=term*t/(terms+1)
    # Every remaining successive term ratio is <= t/(terms+2).
    remainder=nxt/(1-t/(terms+2))
    lo,hi=floor_grid(total),ceil_grid(total+remainder)
    for _ in range(m):
        lo,hi=floor_grid(lo*lo),ceil_grid(hi*hi)
    return floor_grid(1/hi),ceil_grid(1/lo)


def normal_sf_interval(z2,terms=12):
    """Integral-by-parts bounds: Q(z)=phi(z)/z times Mills expansion.

    z2 is exact rational; all called z>=6.2. Truncation error is bracketed,
    not treated as a convergent infinite asymptotic series.
    """
    assert z2>36
    exp_lo,exp_hi=exp_negative_interval(z2/2)
    rlo,_=sqrt_interval(1/(2*PI[1]*z2))
    _,rhi=sqrt_interval(1/(2*PI[0]*z2))
    total=F(1); term=F(1)
    for k in range(1,terms+1):
        term*=F(2*k-1)/z2
        total+=(-1 if k%2 else 1)*term
    next_term=term*F(2*terms+1)/z2
    if terms%2==0:
        lower,upper=total-next_term,total
    else:
        lower,upper=total,total+next_term
    assert 0<lower<=upper
    return floor_grid(exp_lo*rlo*lower),ceil_grid(exp_hi*rhi*upper)


def inherited_force_recovery():
    """Only the query wrapper uses the hidden rotation; the learner does not."""
    sys.dont_write_bytecode=True
    sys.path.insert(0,str(SOURCE/'work/phase6/molecular_dynamics'))
    from gated_acquisition import Simulator
    sim=Simulator(20.,seed=4120)
    queries=0
    def observed_force(x,w):
        nonlocal queries
        queries+=1
        latent=np.asarray(w)@sim.rotation
        bx,by=sim.drift(np.asarray([x]),np.asarray([latent[0]]))
        return float(bx[0])
    cv=np.asarray([observed_force(0.,np.eye(9)[j]) for j in range(9)])
    coupling=float(np.linalg.norm(cv))
    direction=cv/coupling
    at_half=observed_force(.5,np.zeros(9))
    barrier=(at_half+.5*coupling)/1.5
    rng=np.random.default_rng(12036)
    w=rng.normal(size=(100,9)); x=rng.uniform(-1.4,1.4,100)
    true_y=(w@sim.rotation)[:,0]
    physical=sim.drift(x,true_y)[0]
    fitted=-4*barrier*x*(x*x-1)-coupling*(x-w@direction)
    residual=float(np.max(np.abs(physical-fitted)))
    # Validation queries are separately counted, not hidden in the ten queries.
    return {'acquisition_force_points':queries,'separate_heldout_force_points':100,
            'recovered_barrier':barrier,'recovered_coupling':coupling,
            'direction_alignment_scored_only':float(direction@sim.rotation[:,0]),
            'heldout_max_abs_drift_error_float':residual,
            'family_condition':'global supplied cubic x + linear hidden-coordinate family, positive coupling, exact noiseless physical force access',
            'no_global_family_validation_from_finite_queries':True}


def make_coupled_model():
    d=10; steps=16; dt=F(1,8)
    b=diag([-1,-1,F(-3,100)]+[-5]*7)
    b[0][2]=F(1);b[1][2]=F(-1)
    b[2][0]=F(1,100);b[2][1]=F(-1,100)
    r=identity(d)
    v=list(range(1,9)); norm=sum(x*x for x in v)
    for i in range(8):
        for j in range(8):
            r[i+2][j+2]=F(int(i==j))-F(2*v[i]*v[j],norm)
    assert multiply(r,transpose(r))==identity(d)
    observed=multiply(multiply(r,b),transpose(r))
    # Eleven force queries reconstruct an arbitrary supplied affine drift.
    count=0
    def force(z):
        nonlocal count
        count+=1
        return [sum((observed[i][j]*z[j] for j in range(d)),F(0)) for i in range(d)]
    offset=force([F(0)]*d)
    cols=[]
    for j in range(d):
        point=[F(0)]*d;point[j]=F(1)
        cols.append([x-y for x,y in zip(force(point),offset)])
    learnt=transpose(cols)
    assert learnt==observed
    a=add(identity(d),[[dt*x for x in row] for row in learnt])
    root0=multiply(r,diag([0,0]+[1]*8))
    root_noise=multiply(r,diag([F(1,2),F(1,2),F(1,20)]+[F(1,2)]*7))
    # Exact coefficient rows of x_c(k) as a function of 170 independent normals.
    powers=[identity(d)]
    for _ in range(steps):
        powers.append(multiply(powers[-1],a))
    blocks0=[multiply(powers[k],root0) for k in range(steps+1)]
    blocksn=[multiply(powers[k],root_noise) for k in range(steps)]
    m=[];labels=[]
    for k in range(1,steps+1):
        for channel in [0,1]:
            row=blocks0[k][channel].copy()
            for t in range(1,steps+1):
                row.extend(blocksn[k-t][channel] if t<=k else [F(0)]*d)
            m.append(row);labels.append([k,channel+1])
    variances=[sum((x*x for x in row),F(0)) for row in m]
    for k in range(steps):
        assert variances[2*k]==variances[2*k+1]
    return {'dimension':d,'steps':steps,'dt':dt,'drift':learnt,'matrix':m,
            'variance':variances,'labels':labels,'force_queries':count}


def run():
    started=time.perf_counter()
    recovered=inherited_force_recovery()
    model=make_coupled_model()
    b=F(17,2);j=len(model['matrix'])
    tail=[normal_sf_interval(b*b/v) for v in model['variance']]
    lower=[x[0] for x in tail]; upper=[x[1] for x in tail]
    # Rational masses u_j enclose the true marginal masses from above.
    total=sum(upper,F(0))
    # A channel-symmetry lower bound at the final time, with overlap bounded by
    # P(x1+x2>=2*b). Its variance is exact, and cross covariance is negative.
    m0,m1=model['matrix'][-2:]
    sumvar=sum(((x+y)**2 for x,y in zip(m0,m1)),F(0))
    overlap_lo,overlap_hi=normal_sf_interval((2*b)**2/sumvar)
    deterministic_lower=2*lower[-1]-overlap_hi
    assert deterministic_lower>0
    deterministic_upper=total
    # Distinct channels remain nearly disjoint over the complete time window.
    # Pair intersections imply x1(k)+x2(l)>=2*b. Use the largest exact
    # variance across all 16x16 such pairs, then a union bound.
    cross_sum_variances=[]
    cross_covariances=[]
    for r0 in model['matrix'][::2]:
        for r1 in model['matrix'][1::2]:
            cross_sum_variances.append(sum(((x+y)**2 for x,y in zip(r0,r1)),F(0)))
            cross_covariances.append(sum((x*y for x,y in zip(r0,r1)),F(0)))
    assert max(cross_covariances)<=0
    _,cross_pair_upper=normal_sf_interval((2*b)**2/max(cross_sum_variances))
    channel_intersection_upper=model['steps']**2*cross_pair_upper
    n=20000;epsilon=F(1,100)
    # Hoeffding: failure <= 2exp(-2*n*epsilon^2)=2exp(-4)<.05.
    fail_lo,fail_hi=exp_negative_interval(2*n*epsilon*epsilon)
    fail_hi*=2
    assert fail_hi<F(1,20)
    rng=np.random.default_rng(611308)
    mf=fmat(model['matrix']);sd=np.sqrt(np.asarray([float(v) for v in model['variance']]))
    h=mf/sd[:,None]
    z=float(b)/sd
    alpha=np.asarray([float(u/total) for u in upper]);alpha/=alpha.sum()
    # Every component is conditioned on a constituent event, not a mean shift.
    count_hist=np.zeros(j+1,dtype=np.int64)
    sum_lower=F(0);sum_upper=F(0)
    means=[];dominance=[];min_margin=math.inf
    multiplicity_records=[]
    # Floating diagnostics use exact rational mass endpoints and all full-path
    # event channels. Sample event masks are preserved for independent checking.
    for base in range(0,n,500):
        size=min(500,n-base)
        chosen=rng.choice(j,size=size,p=alpha)
        normal=rng.normal(size=(size,mf.shape[1]))
        u=rng.random(size)
        while np.any(u==0):
            u[u==0]=rng.random(np.sum(u==0))
        truncated=-ndtri_exp(log_ndtr(-z[chosen])+np.log(u))
        chosen_rows=h[chosen]
        proj=np.einsum('ij,ij->i',normal,chosen_rows)
        normal+=(truncated-proj)[:,None]*chosen_rows
        values=normal@mf.T
        event=values>=float(b)
        assert np.all(event[np.arange(size),chosen])
        mult=event.sum(axis=1)
        count_hist+=np.bincount(mult,minlength=j+1)
        min_margin=min(min_margin,float(np.min(np.abs(values-float(b)))))
        for row,k in zip(event,mult):
            # For q = sum_j (u_j/U) P(.|E_j),
            # Y=U / sum_{j:E_j} u_j/p_j.
            denom_upper=sum((upper[t]/lower[t] for t in np.flatnonzero(row)),F(0))
            sum_lower+=floor_grid(total/denom_upper,70)
            sum_upper+=total/int(k)
            multiplicity_records.append(int(sum((1<<int(t) for t in np.flatnonzero(row)),0)))
        dominance.extend(np.argmax(values.reshape(size,model['steps'],2).max(axis=1),axis=1).tolist())
    sample_lo=sum_lower/n;sample_hi=sum_upper/n
    ci_lo=max(deterministic_lower,sample_lo-epsilon*total)
    ci_hi=min(deterministic_upper,sample_hi+epsilon*total)
    receipt={
        'status':'RATIONAL_DETERMINISTIC_ENCLOSURE_AND_BOUNDED_IDEAL_SAMPLER_CONFIDENCE_THEOREM;FLOAT_SAMPLER_DEMONSTRATION',
        'inherited_force_recovery':recovered,
        'inherited_gaussian_global_control_energy_bound':6400,
        'inherited_log_second_moment_bound':6400,
        'inherited_acquisition_cost_kept':19400000,
        'inherited_reported_path_force_points':1438768,
        'inherited_matched_direct_force_oracle_cost_if_same_path_work':10+77360+1421804,
        'inherited_matched_polynomial_reconstruction_cost_if_same_path_work':10+1421804,
        'distinct_model':{
            'target':'P(any x1(k)>=8.5 or x2(k)>=8.5, k=1,...,16), exact full-state Euler dt=1/8; x1=x2=0 initially, eight nonreaction coordinates independent N(0,1)',
            'latent_drift':['-x1+y','-x2-y','.01*x1-.01*x2-.03*y']+['-5*z']*7,
            'noise_step_standard_deviations':['1/2','1/2','1/20']+['1/2']*7,
            'observation':'reaction outputs x1,x2; rational Householder rotation of y,z1,...,z7',
            'family':'globally affine drift supplied, noiseless full-vector force oracle, known exact Gaussian thermostat and preparation',
            'dimension':10,'steps':16,'events':j,'innovation_dimension':len(m0),
            'force_queries_acquisition':model['force_queries'],
            'exact_rational_acquisition_check_passed':True,
            'final_channel_correlation':float(sum((x*y for x,y in zip(m0,m1)),F(0))/model['variance'][-1]),
            'all_cross_channel_time_covariances_nonpositive_exact_check':True,
            'all_time_channel_intersection_upper':frac_record(channel_intersection_upper),
            'one_channel_only_sampling_minimum_relative_bias':float(F(1,2)-channel_intersection_upper/(2*deterministic_lower)),
        },
        'deterministic_certificate':{
            'lower':frac_record(deterministic_lower),
            'upper':frac_record(deterministic_upper),
            'upper_lower_ratio':float(deterministic_upper/deterministic_lower),
            'final_channel_overlap_upper':frac_record(overlap_hi),
            'scope':'unconditional mathematical enclosure; exact rational Taylor/Mills/Machin arithmetic; no random samples used'},
        'bounded_sampler':{
            'density':'q(w)=p(w)/U * sum_j [u_j/P(E_j)] 1_Ej(w), u_j exact rational upper marginal masses; U=sum u_j',
            'contribution':'Y=U / sum_j [u_j/P(E_j)] 1_Ej; 0<Y<=U',
            'samples':n,'seed':611308,'epsilon_relative_to_U':str(epsilon),
            'finite_sample_failure_upper':frac_record(fail_hi),
            'confidence_at_least':float(1-fail_hi),
            'sample_mean_enclosure_given_event_masks':[outward(sample_lo)[0],outward(sample_hi)[1]],
            'hoeffding_interval_if_ideal_sampler':[outward(ci_lo)[0],outward(ci_hi)[1]],
            'relative_halfwidth_if_ideal_sampler':float((ci_hi-ci_lo)/(ci_hi+ci_lo)),
            'contribution_multiplicity_histogram':count_hist.tolist(),
            'channel_dominance_counts':np.bincount(dominance,minlength=2).tolist(),
            'minimum_float_event_margin':min_margin,
            'not_formal_float_or_random_bit_validation':True,
            'operational_force_point_work_if_force_queried_each_step':n*model['steps'],
            'post_acquisition_gaussian_generation_requires_physical_force_queries':0,
            'linear_algebra_and_rng_charged_separately':True,
        },
        'matched_controls':{
            'data_free_exact_affine_force_reconstruction_plus_classical_ALOE':{
                'acquisition_force_points':model['force_queries'],
                'path_oracle_force_points_if_queried_per_step':n*model['steps'],
                'same_bounded_guarantee':True,
                'candidate_no_advantage_over_this_control':True},
            'deterministic_gaussian_tail_enclosure':{'acquisition_force_points':model['force_queries'],'samples':0},
            'exact_union_Doob':'zero-variance ideal comparator needs the union probability/conditional union law, not supplied here',
            'FFS_WE':'full-state classical splitting applicable; not executed because ALOE is already an identical same-input control with the proved finite-sample guarantee'},
        'scope_limitations':['global affine family is supplied, not inferred from finitely many force queries','new model is a solvable Gaussian benchmark, not an atomistic molecule','exact discrete Euler target only','ALOE/conditional Gaussian mixture is established prior art','weight-tail certificate for inherited nonlinear toy remains unresolved','no novelty or civilization-enabling advantage'],
        'execution_seconds':time.perf_counter()-started,
    }
    np.savez_compressed(HERE/'sample_masks.npz',event_masks=np.asarray(multiplicity_records,dtype=np.uint64))
    exact={'tail_bounds':[{'label':lab,'variance':frac_record(v),'lower':frac_record(l),'upper':frac_record(u)} for lab,v,l,u in zip(model['labels'],model['variance'],lower,upper)],
           'union_mass_upper':frac_record(total),'deterministic_lower':frac_record(deterministic_lower),
           'sample_mean_lower':frac_record(sample_lo),'sample_mean_upper':frac_record(sample_hi),
           'confidence_lower':frac_record(ci_lo),'confidence_upper':frac_record(ci_hi)}
    (HERE/'exact_certificate.json').write_text(json.dumps(exact,indent=2)+'\n')
    (HERE/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    pins=[]
    for rel in ['outputs/ASTRA_GENESIS_HANDOFF.txt','outputs/STRONGEST_VERIFIED_RESULT.txt','work/phase6/molecular_dynamics/HANDOFF.txt','work/phase6/molecular_dynamics/path_reweighting.py','work/phase6/molecular_dynamics/path_reweighting.json','work/phase6/molecular_dynamics/gated_acquisition.py']:
        data=(SOURCE/rel).read_bytes();pins.append({'path':str(SOURCE/rel),'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)})
    (HERE/'source_pins.json').write_text(json.dumps(pins,indent=2)+'\n')
    print(json.dumps({'force_recovery':recovered,'deterministic_interval':[outward(deterministic_lower)[0],outward(deterministic_upper)[1]],'ideal_sampler_interval':[outward(ci_lo)[0],outward(ci_hi)[1]],'relative_halfwidth':receipt['bounded_sampler']['relative_halfwidth_if_ideal_sampler'],'confidence':float(1-fail_hi),'execution_seconds':receipt['execution_seconds']},indent=2))


if __name__=='__main__':
    run()
