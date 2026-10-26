#!/usr/local/bin/python3
"""Q54 stage2: sequential comparator, interior stress, exact task certificate.

All generated measurements are simulations. No stage1 files are imported or written.
"""
from pathlib import Path
import csv, json, math
import numpy as np
from scipy.special import expit, ndtr, ndtri
from scipy.optimize import linprog

OUT=Path(__file__).resolve().parent
M,L,A,SAFE,TARGET,SIGMA=1.,5.,4.,.5,1.,.001


def save_csv(name,rows):
    with (OUT/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)


def h(x,delta,c=.65,amplitude=A):
    x=np.asarray(x,dtype=float)
    return amplitude*delta*(np.logaddexp(0.,(x-c)/delta)-np.logaddexp(0.,-c/delta))


def sequential_comparison():
    rng=np.random.default_rng(540054)
    p=.05; threshold=math.log((1-p)/p); reps=40000
    rows=[]; arrays={}
    for delta in [.03,.025]:
        eps=float(h(SAFE,delta)); mu=eps**2/(2*SIGMA**2); sd=eps/SIGMA
        kl_goal=(1-2*p)*math.log((1-p)/p)
        fixed=math.ceil(4*SIGMA**2*float(ndtri(1-p))**2/eps**2)
        for label in [0,1]:
            llr=np.zeros(reps); counts=np.zeros(reps,dtype=np.int64); active=np.ones(reps,dtype=bool)
            while active.any():
                ids=np.flatnonzero(active)
                llr[ids]+=(2*label-1)*mu+sd*rng.standard_normal(len(ids))
                counts[ids]+=1
                active[ids[np.abs(llr[ids])>=threshold]]=False
                if counts.max()>100000:
                    raise RuntimeError('SPRT diagnostic safety cap hit; no censored success allowed')
            empirical=float(np.mean((llr>=0)!=bool(label)))
            rows.append(dict(delta=delta,hypothesis=label,replicates=reps,error=empirical,
                error_mc_se=math.sqrt(empirical*(1-empirical)/reps),
                mean_readings=float(counts.mean()),median_readings=float(np.median(counts)),
                p95_readings=float(np.quantile(counts,.95)),p99_readings=float(np.quantile(counts,.99)),
                maximum_realized_readings=int(counts.max()),fixed_n_for_5pct=fixed,
                expected_count_lower_bound=kl_goal/mu,
                fixed_n_error_at_rounded_mean=float(ndtr(-math.sqrt(round(counts.mean()))*eps/(2*SIGMA))),
                theoretical_error_upper=p))
            arrays[f'delta_{delta}_H{label}_counts']=counts
            arrays[f'delta_{delta}_H{label}_final_llr']=llr
    np.savez_compressed(OUT/'sprt_raw.npz',**arrays)
    save_csv('sequential_comparison.csv',rows)
    return rows


def interior_and_scope_stress():
    # f_+- = k*x +- h_eff/2; all derivatives lie inside [m+eta,L-eta].
    k,eta=3.,.5; eff=A-2*eta; rows=[]
    for delta in [.05,.025,.01,.005]:
        eps=float(h(SAFE,delta,amplitude=eff)); gap=float(h(TARGET,delta,amplitude=eff))
        rows.append(dict(delta=delta,margin=eta,effective_amplitude=eff,
                        safe_pair_gap=eps,target_pair_gap=gap,
                        error_after_1e6=float(ndtr(-1000*eps/(2*SIGMA))),
                        fixed_n_for_5pct_real=4*SIGMA**2*float(ndtri(.95))**2/eps**2,
                        derivative_lower=k-eff/2,derivative_upper=k+eff/2))
    save_csv('interior_pair.csv',rows)
    # A different known pair: endpoint equality kills endpoint information.
    def gap(x): return .5*np.tanh(x)*np.tanh(x-SAFE)
    scope=dict(endpoint_pair_gap=float(gap(SAFE)),interior_pair_gap=float(gap(SAFE/2)),
               target_pair_gap=float(gap(TARGET)),global_derivative_lower=2.,global_derivative_upper=4.,
               endpoint_error_any_n=.5,
               interior_one_read_error=float(ndtr(-abs(gap(SAFE/2))/(2*SIGMA))))
    (OUT/'endpoint_scope_counterexample.json').write_text(json.dumps(scope,indent=2)+'\n')
    return rows,scope


def envelopes(x,lower,upper,query):
    """For g=f-m*x, use monotone A-Lipschitz asymmetric cones."""
    query=np.atleast_1d(query)
    low=np.max(lower[:,None]-A*np.maximum(x[:,None]-query[None,:],0),axis=0)
    high=np.min(upper[:,None]+A*np.maximum(query[None,:]-x[:,None],0),axis=0)
    return low,high


def independent_lp(nodes,lower,upper,objective,center=False):
    # nodes contain anchor, safe data, target. Only safe data have observed intervals.
    d=len(nodes); n=len(lower); extra=int(center)
    c=np.zeros(d+extra)
    if center: c[-1]=-1
    else: c[-1]=objective
    aub=[]; bub=[]
    for j,dx in enumerate(np.diff(nodes)):
        row=np.zeros(d+extra); row[j+1]=1;row[j]=-1
        aub.append(row);bub.append(A*dx)
        aub.append(-row);bub.append(0.)
    for i in range(1,n):
        row=np.zeros(d+extra);row[i]=1
        if center: row[-1]=1
        aub.append(row);bub.append(upper[i])
        row=np.zeros(d+extra);row[i]=-1
        if center: row[-1]=1
        aub.append(row);bub.append(-lower[i])
    bounds=[(0.,0.)]+[(None,None)]*(d-1)
    if center: bounds.append((0,None))
    sol=linprog(c,A_ub=np.asarray(aub),b_ub=np.asarray(bub),bounds=bounds,method='highs')
    return sol


def smoothed_piecewise(nodes,values,width,query,derivative=False):
    """Exact Gaussian convolution of a finite hinge expansion, re-anchored at 0.

    The original function has slope 0 to the left/right of the listed knots,
    and adjacent slopes in [0,A]. Convolution therefore preserves those bounds
    over the entire real line (proved independently of numerical checking).
    """
    slopes=np.diff(values)/np.diff(nodes)
    jumps=np.diff(np.r_[0.,slopes,0.])
    def evaluate(q,deriv):
        q=np.atleast_1d(q)
        dist=q[:,None]-nodes[None,:]
        z=dist/width
        if deriv: basis=ndtr(z)
        else: basis=dist*ndtr(z)+width*np.exp(-z*z/2)/math.sqrt(2*math.pi)
        return np.einsum('ij,j->i',basis,jumps,optimize=False)
    if derivative: return evaluate(query,True)
    return evaluate(query,False)-evaluate(np.array([0.]),False)[0]


def generate_case(rng,kind):
    if kind=='single_softplus':
        base=float(rng.uniform(1.2,2.0)); amp=float(rng.uniform(.5,5-base))
        delta=float(np.exp(rng.uniform(np.log(.001),np.log(.2)))); c=float(rng.uniform(.1,1.1))
        pars=dict(base=base,amplitude=amp,delta=delta,center=c)
        return pars,lambda x:base*np.asarray(x)+h(x,delta,c,amp)
    if kind=='multiple_softplus':
        count=int(rng.integers(2,6));base=1.2
        amps=rng.dirichlet(np.ones(count))*float(rng.uniform(.5,3.6))
        widths=np.exp(rng.uniform(np.log(.005),np.log(.3),count));cs=rng.uniform(0,1.2,count)
        pars=dict(base=base,amplitudes=amps.tolist(),widths=widths.tolist(),centers=cs.tolist())
        def f(x):
            result=base*np.asarray(x,dtype=float)
            for amp,w,c in zip(amps,widths,cs): result=result+h(x,w,c,amp)
            return result
        return pars,f
    if kind=='single_frequency':
        k=3.; amp=float(rng.uniform(.2,1.8));omega=float(rng.uniform(1,30));phi=float(rng.uniform(0,2*math.pi))
        pars=dict(base=k,amplitude=amp,frequency=omega,phase=phi)
        return pars,lambda x:k*np.asarray(x)+amp/omega*(math.cos(phi)-np.cos(omega*np.asarray(x)+phi))
    if kind=='localized_arctangent':
        base=1.2; amp=float(rng.uniform(.5,3.6));w=float(np.exp(rng.uniform(np.log(.002),np.log(.2))));c=float(rng.uniform(0,1.2))
        pars=dict(base=base,amplitude=amp,width=w,center=c)
        return pars,lambda x:base*np.asarray(x)+amp*w*(np.arctan((np.asarray(x)-c)/w)-math.atan(-c/w))
    if kind=='two_frequency':
        k=3.; amps=rng.dirichlet(np.ones(2))*float(rng.uniform(.2,1.8));omega=rng.uniform(1,40,2);phi=rng.uniform(0,2*math.pi,2)
        pars=dict(base=k,amplitudes=amps.tolist(),frequencies=omega.tolist(),phases=phi.tolist())
        def f(x):
            result=k*np.asarray(x,dtype=float)
            for amp,w,p in zip(amps,omega,phi):result=result+amp/w*(math.cos(p)-np.cos(w*np.asarray(x)+p))
            return result
        return pars,f
    raise ValueError(kind)


def withheld_certificates():
    rng=np.random.default_rng(5402026)
    kinds=['single_softplus','multiple_softplus','single_frequency','localized_arctangent','two_frequency']
    n=17;alpha=.01;radius=SIGMA*float(ndtri(1-alpha/(2*n)))
    rows=[]; data=[]; tasks=[]; parameters=[]; witness_rows=[]; witness_functions=[]
    exemplar=None
    for kind in kinds:
        for replicate in range(40):
            cid=len(rows);pars,f=generate_case(rng,kind)
            # 16 independent strictly interior points plus the safe endpoint.
            x=np.r_[0.,np.sort(rng.uniform(.005,SAFE-.005,n-1)),SAFE]
            truth=np.asarray(f(x));obs=truth.copy();obs[1:]+=SIGMA*rng.standard_normal(n)
            radii=np.r_[0.,np.full(n,radius)]
            lower=obs-radii-M*x;upper=obs+radii-M*x
            nodes=np.r_[x,TARGET]
            lowvals,highvals=envelopes(x,lower,upper,nodes)
            feasible=bool(np.all(lowvals[:len(x)]<=upper+1e-10))
            covered=bool(np.all(np.abs(obs[1:]-truth[1:])<=radius))
            ftarget=float(f(TARGET))
            if not feasible:
                raise RuntimeError('Infeasible withheld record; preserve and investigate, do not drop it')
            lp_lo=independent_lp(nodes,lower,upper,1)
            lp_hi=independent_lp(nodes,lower,upper,-1)
            assert lp_lo.success and lp_hi.success
            lo=M*TARGET+lowvals[-1];hi=M*TARGET+highvals[-1]
            discrepancy=max(abs(lp_lo.x[-1]-(lo-M*TARGET)),abs(lp_hi.x[-1]-(hi-M*TARGET)))
            assert discrepancy<2e-8
            assert hi-lo>=A*(TARGET-SAFE)-1e-10
            center=independent_lp(nodes,lower,upper,0,center=True)
            if not center.success or center.x[-1]<=1e-10:
                raise RuntimeError('No strict interior data witness in withheld record')
            tau=float(center.x[-1]);mix=1e-4
            width=mix*tau/(8*A*math.sqrt(2/math.pi))
            assert width>0
            for side,values,optimum in [('lower',lowvals,lo),('upper',highvals,hi)]:
                blended=(1-mix)*values+mix*center.x[:-1]
                smooth=M*nodes+smoothed_piecewise(nodes,blended,width,nodes)
                # Independent analytic near-extremizer: all data inequalities checked.
                assert np.all(smooth[:len(x)]>=obs-radii-1e-9)
                assert np.all(smooth[:len(x)]<=obs+radii+1e-9)
                assert abs(smooth[0])<1e-12
                dense=np.linspace(-1,2,2001)
                deriv=M+smoothed_piecewise(nodes,blended,width,dense,True)
                assert deriv.min()>=M-1e-8 and deriv.max()<=L+1e-8
                target_deviation=abs(float(smooth[-1])-optimum)
                assert target_deviation<=mix*A*TARGET+2*A*width*math.sqrt(2/math.pi)+1e-8
                witness_rows.append(dict(case=cid,side=side,strict_slack=tau,mix=mix,
                                         gaussian_width=width,target_value=float(smooth[-1]),
                                         closed_class_optimum=optimum,approximation_gap=target_deviation))
                witness_functions.append(dict(case=cid,side=side,knots=nodes.tolist(),
                    unsmoothed_values=blended.tolist(),gaussian_width=width,
                    force_formula='m*x + GaussianConvolution(piecewise_linear_g)(x) - GaussianConvolution(piecewise_linear_g)(0)',
                    m=M,L=L,outer_g_slopes=[0,0]))
            rows.append(dict(case=cid,family=kind,replicate=replicate,true_target=ftarget,
                             target_lower=lo,target_upper=hi,interval_width=hi-lo,
                             simultaneous_calibration_covered=covered,
                             target_covered=bool(lo-1e-12<=ftarget<=hi+1e-12),
                             max_lp_discrepancy=discrepancy,strict_slack=tau))
            for xx,tt,yy,rr in zip(x,truth,obs,radii):
                data.append(dict(case=cid,family=kind,x=float(xx),true_force=float(tt),measurement=float(yy),radius=float(rr)))
            for cap in [1.5,2.5,3.5,4.5]:
                verdict='SAFE' if hi<=cap else 'UNSAFE' if lo>cap else 'UNKNOWN'
                wrong=(verdict=='SAFE' and ftarget>cap) or (verdict=='UNSAFE' and ftarget<=cap)
                tasks.append(dict(case=cid,family=kind,force_ceiling=cap,verdict=verdict,
                                  true_target=ftarget,incorrect_certificate=bool(wrong)))
            parameters.append(dict(case=cid,family=kind,parameters=pars))
            if cid==0:exemplar=dict(x=x,obs=obs,radii=radii,nodes=nodes,lower=lowvals,upper=highvals,truth=f(nodes))
    save_csv('withheld_cases.csv',rows);save_csv('withheld_measurements.csv',data)
    save_csv('withheld_tasks.csv',tasks);save_csv('analytic_near_extremizers.csv',witness_rows)
    (OUT/'withheld_parameters.json').write_text(json.dumps(parameters,indent=2)+'\n')
    (OUT/'analytic_witness_functions.json').write_text(json.dumps(witness_functions,indent=2)+'\n')
    np.savez(OUT/'certificate_example.npz',**exemplar)
    summary=dict(cases=len(rows),readings_per_case=n,total_scalar_readings=len(rows)*n,
                 simultaneous_calibration_target=1-alpha,
                 observed_calibration_coverage=sum(r['simultaneous_calibration_covered'] for r in rows),
                 observed_target_coverage=sum(r['target_covered'] for r in rows),
                 tasks=len(tasks),safe=sum(r['verdict']=='SAFE' for r in tasks),
                 unsafe=sum(r['verdict']=='UNSAFE' for r in tasks),unknown=sum(r['verdict']=='UNKNOWN' for r in tasks),
                 incorrect_certificates=sum(r['incorrect_certificate'] for r in tasks),
                 min_interval_width=min(r['interval_width'] for r in rows),
                 max_lp_discrepancy=max(r['max_lp_discrepancy'] for r in rows),
                 analytic_near_extremizers=len(witness_rows),
                 maximum_extremizer_target_gap=max(r['approximation_gap'] for r in witness_rows))
    return summary


def main():
    sequential=sequential_comparison()
    interior,scope=interior_and_scope_stress()
    certificates=withheld_certificates()
    summary=dict(sequential=sequential,endpoint_scope=scope,certificates=certificates,
                 interpretation='Simulations and governing proofs, no physical measurements; classical incumbents retained.')
    (OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
