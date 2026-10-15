#!/usr/bin/env python3
"""Synthetic finite checks for dynamic decision closure; no laboratory data.

Run with the research wave's Python environment. Does not execute or edit
source audits. Writes only beside this script.
"""
from __future__ import annotations
import itertools
import json
from pathlib import Path
import numpy as np
import sympy as sp
from scipy.optimize import linprog, minimize_scalar

HERE=Path(__file__).resolve().parent
RNG=np.random.default_rng(202610152)


def response(a,b):
    return a*b/(a+b)


def segment(a,b,duration,x):
    k=a+b
    equilibrium=a/k
    decay=np.exp(-k*duration)
    end=equilibrium+(x-equilibrium)*decay
    total=b*(equilibrium*duration+(x-equilibrium)*(-np.expm1(-k*duration))/k)
    return float(end),float(total)


def periodic(a,b0,b1,period,fraction):
    t0=(1-fraction)*period
    t1=fraction*period
    k0,k1=a+b0,a+b1
    p0,p1=a/k0,a/k1
    e0,e1=np.exp(-k0*t0),np.exp(-k1*t1)
    x0=(p1*(1-e1)+p0*e1*(1-e0))/(1-e0*e1)
    xmid,y0=segment(a,b0,t0,x0)
    xend,y1=segment(a,b1,t1,xmid)
    assert abs(xend-x0)<1e-10
    return float((y0+y1)/period),float(x0),float(xmid)


def capacity(theta,f):
    a,b0,b1=theta
    return response(a,b0+(b1-b0)*f)


def price_support(theta,beta):
    a,b0,b1=theta
    D=b1-b0
    if beta<=0:
        f=1.
    else:
        f=float(np.clip((a*np.sqrt(D/beta)-a-b0)/D,0.,1.))
    return capacity(theta,f)-beta*f,f


def pulse_moment(theta,history):
    a,b0,b1=theta
    x=0.
    total=0.
    for mode,duration in history:
        x,y=segment(a,b1 if mode else b0,duration,x)
        total+=y
    return total


def moment_closure(types,features,moments,budget):
    """Standard column generation: continuous duty support solved analytically.

    Latent type class is the supplied finite library, not a certified
    continuous physical parameter domain. Mixtures preserve whole-type
    correlations. Floats exercise the proof, not interval-certified arithmetic.
    """
    m=features.shape[0]
    columns=[(i,f) for i in range(len(types)) for f in [0.,1.]]
    for iteration in range(250):
        C=np.array([capacity(types[i],f) for i,f in columns])
        F=np.array([f for _,f in columns])
        A=np.vstack([np.ones(len(columns)),np.stack([features[:,i] for i,_ in columns],axis=1)])
        result=linprog(-C,A_ub=F[None,:],b_ub=[budget],A_eq=A,
            b_eq=np.r_[1.,moments],bounds=(0,None),method='highs',
            options={'dual_feasibility_tolerance':1e-9,'primal_feasibility_tolerance':1e-9})
        assert result.success,result.message
        beta=max(0.,-float(result.ineqlin.marginals[0]))
        lam=-result.eqlin.marginals
        violations=[]
        for i,theta in enumerate(types):
            h,f=price_support(theta,beta)
            gap=h-lam[0]-lam[1:]@features[:,i]
            violations.append(float(gap))
            if gap>1e-8:
                columns.append((i,f))
        worst=max(violations)
        if worst<=1e-8:
            primal=-float(result.fun)
            dual=float(beta*budget+lam[0]+lam[1:]@moments+max(0.,worst))
            assert dual+1e-9>=primal and dual-primal<5e-8
            nonzero=int(np.count_nonzero(result.x>1e-8))
            assert nonzero<=m+2
            return {'upper_bound':dual,'primal_value':primal,'numerical_gap':dual-primal,
                'price':beta,'lambda':lam.tolist(),'calibration_count':m,
                'latent_types':len(types),'active_type_duty_atoms':nonzero,
                'column_generation_iterations':iteration+1,
                'largest_analytic_support_violation':max(0.,worst)}
    raise RuntimeError(f'Column generation did not converge: moments={m}, worst_violation={worst}')


def main():
    a,b,x,beta=sp.symbols('a b x beta',positive=True)
    V=x-beta*sp.log(x)
    residual=sp.factor(b*x-beta*b+sp.diff(V,x)*(a*(1-x)-b*x))
    assert sp.simplify(residual-a*(1-x)*(1-beta/x))==0
    t=sp.symbols('t',positive=True)
    # Substitution beta=t^2 makes the nonnegative square certificate explicit.
    gap=sp.factor(a*(1-t)**2-residual.subs(beta,t*t))
    assert sp.simplify(gap-a*(x-t)**2/x)==0
    results={'scope':'Internal analytic and synthetic finite checks only; no lab data',
        'seed':202610152,
        'symbolic_storage_identity':str(residual),
        'symbolic_nonnegative_gap':str(gap)}

    a0,b0,b1,f=1.,.1,10.,.5
    bbar=b0+(b1-b0)*f
    static=(1-f)*response(a0,b0)+f*response(a0,b1)
    ideal=response(a0,bbar)
    cycles=[]
    for h in [2.,1.,.5,.1,.02,.002]:
        rate,xlo,xhi=periodic(a0,b0,b1,h,f)
        assert rate<=ideal+1e-10
        cycles.append({'period':h,'duty':f,'average_rate':rate,'start_inventory':xlo,
                       'post_cold_inventory':xhi})
    assert abs(cycles[-1]['average_rate']-ideal)<1e-5
    # A finite executable ideal-mode schedule, with a separately charged
    # dimensionless per-transition cost. Not a measured thermal waveform.
    switch_cost=.001
    period=.1
    adjusted_duty=f-2*switch_cost/period
    finite_rate,xlo,xhi=periodic(a0,b0,b1,period,adjusted_duty)
    actual_cost=adjusted_duty+2*switch_cost/period
    assert actual_cost<=f+1e-12 and finite_rate>static
    results['binary_dynamic_counterexample']={
        'a':a0,'b0':b0,'b1':b1,'budget_hot_duty':f,
        'steady_time_share_bound':static,'ideal_dynamic_capacity':ideal,
        'ratio':ideal/static,'periodic_sequences':cycles,
        'finite_costed_synthetic_sequence':{'period':period,'duty':adjusted_duty,
            'per_transition_cost':switch_cost,'total_rate_cost':actual_cost,
            'average_product_rate':finite_rate,
            'warning':'Known ideal binary mode dynamics; thermal settling, waveform realization and laboratory costs unacquired.'}}

    # Arbitrary finite schedules: check the exact priced endpoint inequality.
    worst=-float('inf')
    for _ in range(256):
        aa=float(RNG.uniform(.2,3.))
        bb0=float(RNG.uniform(.02,.4))
        bb1=float(RNG.uniform(2.,12.))
        xstart=float(RNG.uniform(.05,.95))
        xnow=xstart
        Y=B=T=0.
        for _ in range(12):
            mode=int(RNG.integers(0,2))
            duration=float(RNG.uniform(.01,.6))
            bb=bb1 if mode else bb0
            xnow,y=segment(aa,bb,duration,xnow)
            Y+=y; B+=bb*duration; T+=duration
        meanb=B/T
        pp=(aa/(aa+meanb))**2
        potential=lambda z:z-pp*np.log(z)
        upper=T*response(aa,meanb)+potential(xstart)-potential(xnow)
        worst=max(worst,Y-upper)
    assert worst<1e-9
    results['finite_history_storage_checks']={'schedules':256,'largest_upper_bound_violation':worst}

    # Exact common-detector two-transient identification (no separate gain
    # calibration needed, conditional on the single-inventory model).
    aa=sp.Rational(7,5); bb0=sp.Rational(1,4); bb1=sp.Rational(31,5)
    gain=sp.Rational(9,7); offset=sp.Rational(2,11)
    k0,k1=aa+bb0,aa+bb1
    A0,A1=gain*aa*bb0/k0,gain*aa*bb1/k1
    P=sp.factor((k1*A1-k0*A0)/(k1-k0))
    recovered_a=sp.factor(k0-k0*A0/P)
    recovered_gain=sp.factor(P/recovered_a)
    assert recovered_a==aa and recovered_gain==gain
    assert k0-recovered_a==bb0 and k1-recovered_a==bb1
    results['common_detector_identification']={'a':str(recovered_a),
        'b0':str(k0-recovered_a),'b1':str(k1-recovered_a),
        'effective_gain':str(recovered_gain),'offset_from_empty_state':str(offset),
        'exact_rational_recovery':True,'degenerate_case':'k0=k1 does not identify gain and adsorption separately.'}

    # Unknown common detector filter cancels from the two Laplace responses.
    arguments=[sp.Rational(1,3),sp.Rational(2,3),sp.Rational(4,3)]
    tau=sp.Rational(17,13)
    ratios=[]
    for s in arguments:
        H=gain/(1+tau*s)
        Y0=H*aa*bb0/(s*(s+k0))
        Y1=H*aa*bb1/(s*(s+k1))
        ratios.append(sp.factor(Y1/Y0))
    mat=sp.Matrix([[r,-s,-1] for s,r in zip(arguments,ratios)])
    rhs=sp.Matrix([-r*s for s,r in zip(arguments,ratios)])
    out_k1,out_ratio,out_z=map(sp.factor,mat.inv()*rhs)
    out_k0=sp.factor(out_z/out_ratio)
    out_a=sp.factor((out_ratio*out_k0-out_k1)/(out_ratio-1))
    assert out_k0==k0 and out_k1==k1 and out_a==aa
    results['unknown_common_filter_cancellation']={
        'Laplace_arguments':[str(s) for s in arguments],
        'recovered_a':str(out_a),'recovered_b0':str(out_k0-out_a),
        'recovered_b1':str(out_k1-out_a),'exact_rational_recovery':True,
        'scope':'Common linear filter, zero detector memory, known empty catalyst; no DC/tail acquisition inferred.'}

    # A 12-type supplied model class, calibrated by pooled actual histories.
    # The same weights define every response: joint kinetic correlations stay
    # coupled rather than extremized separately for each mode/history.
    types=np.array(list(itertools.product([.5,1.,2.],[.05,.2],[2.,8.])),dtype=float)
    types[:,2]+=types[:,1]  # third coordinate is b1, not D
    weights=RNG.dirichlet(np.ones(len(types)))
    protocols=[[(0,.25)],[(1,.25)],[(0,.3),(1,.15)],
        [(1,.12),(0,.45)],[(0,.15),(1,.08),(0,.2),(1,.1)]]
    features=np.array([[pulse_moment(th,hist) for th in types] for hist in protocols])
    moments=features@weights
    budget=.4
    bounds=[]
    for count in [2,3,5]:
        bounds.append(moment_closure(types,features[:count],moments[:count],budget))
    assert bounds[0]['upper_bound']+1e-8>=bounds[1]['upper_bound']
    assert bounds[1]['upper_bound']+1e-8>=bounds[2]['upper_bound']
    priced=lambda bb:bb*budget+sum(w*price_support(th,bb)[0] for th,w in zip(types,weights))
    true=minimize_scalar(priced,bounds=(0.,10.),method='bounded',options={'xatol':1e-12})
    assert true.success
    assert bounds[-1]['upper_bound']+1e-8>=true.fun
    results['joint_heterogeneity_moment_closure']={
        'type_class':types.tolist(),'hidden_weights_for_synthetic_check':weights.tolist(),
        'calibration_histories':protocols,'pooled_calibration_moments':moments.tolist(),
        'budget':budget,'sharp_relaxed_bounds':bounds,
        'known_true_mixture_capacity':float(true.fun),
        'scope':'Supplied finite kinetic type class; oracle type-dependent duty allocation is an OUTER class, not an acquired device control.'}

    # Noise geometry of the returned deterministic dual witnesses. The target
    # .64 is an illustrative decision threshold, not an illuminated measurement.
    target=.64
    geometry=[]
    for bound in bounds:
        norm=float(np.abs(bound['lambda'][1:]).sum())
        margin=target-bound['upper_bound']
        geometry.append({'moments':bound['calibration_count'],
            'coefficient_l1_norm':norm,'noise_free_margin_to_synthetic_threshold':margin,
            'relative_fixed_witness_cost_factor':None if margin<=0 else (norm/margin)**2})
    assert geometry[0]['relative_fixed_witness_cost_factor'] is None
    assert geometry[2]['relative_fixed_witness_cost_factor']>geometry[1]['relative_fixed_witness_cost_factor']
    results['decision_precision_frontier']={'synthetic_threshold':target,
        'witnesses':geometry,'scope':'Equal unit exposure costs and equal sub-Gaussian noise proxies only; no measured costs/noise. A larger calibration library can reuse the cheaper earlier witness.'}

    # Geometry of common-mode uncertainty, independent of a chemistry model.
    covariance=np.array([[1.,.99],[.99,1.]])
    contrast=np.array([1.,-1.])
    joint_radius=float(np.sqrt(contrast@covariance@contrast))
    separate_radius=float(np.abs(contrast)@np.sqrt(np.diag(covariance)))
    assert abs(joint_radius-np.sqrt(.02))<1e-12
    results['correlated_calibration_geometry']={'joint_ellipsoid_contrast_radius':joint_radius,
        'independent_interval_radius':separate_radius,'ratio':separate_radius/joint_radius,
        'warning':'Illustrative acquired-covariance geometry only; no empirical covariance estimated.'}
    results['all_assertions_passed']=True
    (HERE/'calculation_results.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps({k:v for k,v in results.items() if k!='joint_heterogeneity_moment_closure'},indent=2))
    print(json.dumps({'moment_bounds':bounds,'known_true_capacity':float(true.fun)},indent=2))


if __name__=='__main__':
    main()
