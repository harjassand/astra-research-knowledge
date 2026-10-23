"""Bounded actual-input experiment and independent replay for Astra PRO2.

Run from any cwd: python3 /absolute/path/to/src/run_experiment.py --run
Replay saved exact witnesses without a numerical eigensolver: --replay
"""
from __future__ import annotations
import argparse
from bisect import bisect_right
from decimal import Decimal, localcontext, ROUND_CEILING
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import platform
import sys
import time

import numpy as np
import scipy
from scipy.linalg import eigh
from threadpoolctl import threadpool_limits, threadpool_info

from exact_residual import (AD,VD,certify_krylov,certify_dense,load_exact_generalized,
    fj,jf,sqrt_hi,sqrt_interval,up,rss_bytes,digest,require)
from certified_jacobi import certify_jacobi, verify_certificate

ROOT=Path(__file__).resolve().parents[1]
RESULTS=ROOT/'results'
WIT=ROOT/'witnesses'
DELTA=F(1,100)
S=8
KS=(32,64)
ETA_GRID=tuple(F(1,1<<j) for j in range(8,23))


def write_json(path,obj):
    Path(path).write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')


def timed(fn,*args,**kwargs):
    t,c=time.perf_counter(),time.process_time()
    out=fn(*args,**kwargs)
    return out,dict(wall_seconds=time.perf_counter()-t,
                    cpu_seconds=time.process_time()-c,peak_rss_bytes=rss_bytes())


def scipy_proposals(ai,gi,gd):
    """Proposal only; every floating operation is outside the proof boundary."""
    a=ai.astype(float)/AD
    n=ai.shape[0]
    vs=[]; ds=[]; bs=[]
    for ell in range(S):
        g=gi[:,ell].astype(float)/gd
        q=g/np.linalg.norm(g)
        v=np.zeros((n,max(KS)))
        diag=np.zeros(max(KS)); off=np.zeros(max(KS)-1)
        previous=np.zeros(n); beta=0.
        for j in range(max(KS)):
            v[:,j]=q
            w=a@q-beta*previous
            alpha=float(q@w)
            diag[j]=alpha
            w-=alpha*q
            # Two complete orthogonalisation passes. Their true cost is charged.
            for _ in range(2):
                w-=v[:,:j+1]@(v[:,:j+1].T@w)
            if j+1<max(KS):
                beta=float(np.linalg.norm(w))
                require(beta>0,'early exact/numerical breakdown: stop and report')
                off[j]=beta
                previous,q=q,w/beta
        vs.append(np.rint(v*VD).astype(np.int64))
        ds.append(np.rint(diag*AD).astype(np.int64))
        bs.append(np.rint(off*AD).astype(np.int64))
    return np.stack(vs),np.stack(ds),np.stack(bs)


def dense_proposal(ai):
    vals,vecs=eigh(ai.toarray().astype(float)/AD,check_finite=True,driver='evd')
    return np.rint(vecs*VD).astype(np.int64),np.rint(vals*AD).astype(np.int64),vals


def concentration_radius(n,s,delta,kind):
    # Decimal.ln is correctly rounded to ROUND_HALF_EVEN regardless of context.
    # Add one full last-place unit before taking an exact rational sqrt upper.
    q=2/delta if kind=='weighted' else 2*n/delta
    with localcontext() as ctx:
        ctx.prec=90
        x=Decimal(q.numerator)/Decimal(q.denominator)
        logx=x.ln()
        # q is integer in this experiment; require exact argument conversion.
        require(q.denominator==1,'concentration logarithm requires exact integer argument')
        eps=Decimal(1).scaleb(logx.adjusted()-89)
        logarithm=F(logx+eps)
    den=n*s-2 if kind=='weighted' else s*(n+2)
    return up(sqrt_hi(logarithm/den))


def fraction_from_any(x):
    if isinstance(x,dict):
        return jf(x)
    return F(x)


def step_data(certs,weights,which):
    events={}
    initial=F(0)
    for item,w in zip(certs,weights):
        nodes=item['jacobi']['nodes']
        if which=='upper':
            initial+=w*F(nodes[0]['weight_upper'])
            for j in range(1,len(nodes)):
                x=jf(nodes[j-1]['lower'])
                events[x]=events.get(x,F(0))+w*F(nodes[j]['weight_upper'])
        else:
            for j in range(len(nodes)-1):
                x=jf(nodes[j+1]['upper'])
                events[x]=events.get(x,F(0))+w*F(nodes[j]['weight_lower'])
    xx=sorted(events)
    yy=[]
    for x in xx:
        initial+=events[x]
        yy.append(initial)
    return xx,yy,(sum(w*F(item['jacobi']['nodes'][0]['weight_upper'])
                     for item,w in zip(certs,weights)) if which=='upper' else F(0))


def at_step(data,x):
    xx,yy,initial=data
    j=bisect_right(xx,x)-1
    return yy[j] if j>=0 else initial


class Envelope:
    def __init__(self,certs,weights,sampling,rounding,support_radius):
        self.lower=step_data(certs,weights,'lower')
        self.upper=step_data(certs,weights,'upper')
        self.error=sum(w*jf(c['residual']['operator_error']) for w,c in zip(weights,certs))
        self.start=sum(w*jf(c['residual']['start_error']) for w,c in zip(weights,certs))
        self.sampling=sampling
        self.rounding=rounding
        self.support_radius=support_radius

    def band(self,x,eta_grid=ETA_GRID):
        if x < -self.support_radius:
            return F(0),F(0)
        if x >= self.support_radius:
            return F(1),F(1)
        lo,hi=F(0),F(1)
        sl=self.start+self.sampling+self.rounding
        for eta in eta_grid:
            allowance=sl+self.error/eta
            lo=max(lo,at_step(self.lower,x-eta)-allowance)
            hi=min(hi,at_step(self.upper,x+eta)+allowance)
        require(lo<=hi,'inconsistent verified probability interval')
        return lo,hi

    def breakpoints(self):
        return sorted(set([x+eta for x in self.lower[0] for eta in ETA_GRID]+
                          [x-eta for x in self.upper[0] for eta in ETA_GRID]+
                          [-self.support_radius,self.support_radius]))

    def maximum_width(self):
        points=self.breakpoints()
        # Right-continuous step functions attain their values on [x_i,x_{i+1}).
        candidates=[points[0]-1]+points if points else [F(0)]
        width=F(-1); loc=F(0)
        for x in candidates:
            lo,hi=self.band(x)
            if hi-lo>width:
                width,loc=hi-lo,x
        return width,loc,len(candidates)


def band_json(lo,hi):
    return dict(lower=fj(lo),upper=fj(hi),width=fj(hi-lo),
                lower_float=float(lo),upper_float=float(hi),width_float=float(hi-lo))


def find_gaussian_slacks(cert):
    # The Gaussian module provides named rational fields; be strict, not silent.
    return (fraction_from_any(cert['global_normalized_cdf_slack']),
            [fraction_from_any(x) for x in cert['per_column_normalized_cdf_slack']])


def analyse(meta,allcerts,gcert,dense,diagonal,dense_vals):
    n=meta['n']
    require(gcert['n']==n and gcert['s']==S,'Gaussian block dimensions must match the experiment')
    rho,perprobe=find_gaussian_slacks(gcert)
    require(len(perprobe)==S,'exactly S per-probe rounding bounds required')
    rad=concentration_radius(n,S,DELTA,'weighted')
    oldrad=concentration_radius(n,S,DELTA,'spherical')
    dense_e=jf(dense['operator_error'])
    # Quantile midpoints chosen for display only. The all-threshold theorem
    # permits this choice after inspecting the data.
    sorted_d=sorted(F(int(z),AD) for z in diagonal)
    thresholds=[]
    for numerator in (1,5,10,25,50,75,90,95,99):
        rank=max(1,min(n-1,n*numerator//100))
        thresholds.append((numerator, (sorted_d[rank-1]+sorted_d[rank])/2))
    result=dict(n=n,s=S,delta=fj(DELTA),weighted_sampling_radius=fj(rad),
                classical_sampling_radius=fj(oldrad),gaussian_rounding_slack=fj(rho),
                dense_operator_error=fj(dense_e),
                dense_maximum_possible_width_bound=fj(F(1)),
                probe_rounding_failure_probability=gcert.get('excluded_cell_failure_bound'),
                cases=[])
    # Exact global largest ambiguity of dense eigenvalue intervals (closed at
    # the lower event, open at upper event, matching inclusive CDF convention).
    dense_events={}
    for d in sorted_d:
        dense_events[d-dense_e]=dense_events.get(d-dense_e,0)+1
        dense_events[d+dense_e]=dense_events.get(d+dense_e,0)-1
    active=best=0
    for x in sorted(dense_events):
        active+=dense_events[x]; best=max(best,active)
    result['dense_global_maximum_width']=fj(F(best,n))
    result['dense_global_maximum_ambiguous_eigenvalues']=best
    for k in KS:
        certs=allcerts[str(k)]
        require(len(certs)==S,'exactly S Krylov certificates required')
        norm2=[jf(c['residual']['probe_norm2']) for c in certs]
        weights=[z/sum(norm2) for z in norm2]
        support=jf(meta['M'])+jf(meta['tau'])
        candidate=Envelope(certs,weights,rad,rho,support)
        baseline=Envelope(certs,[F(1,S)]*S,oldrad,sum(perprobe)/S,support)
        numerical_only=Envelope(certs,weights,F(0),F(0),support)
        case={'k':k,'weighted_mean_backward_error':fj(candidate.error),
              'weighted_mean_start_error':fj(candidate.start),
              'weights':[fj(w) for w in weights],
              'threshold_rows':[]}
        for label,env in [('candidate',candidate),('classical',baseline),('deterministic_probe',numerical_only)]:
            (width,loc,count),cost=timed(env.maximum_width)
            case[label+'_maximum_width']=fj(width)
            case[label+'_maximum_width_float']=float(width)
            case[label+'_worst_threshold']=fj(loc)
            case[label+'_band_optimization_cost']=cost
            case[label+'_breakpoint_count']=count
        for percentile,x in thresholds:
            row={'percentile_display':percentile,'threshold_scaled':fj(x),
                 'threshold_generalized':fj(x*int(meta['scale']))}
            lo=F(sum(d+dense_e<=x for d in sorted_d),n)
            hi=F(sum(d-dense_e<=x for d in sorted_d),n)
            row['dense']=band_json(lo,hi)
            for label,env in [('candidate',candidate),('classical',baseline),('deterministic_probe',numerical_only)]:
                a,b=env.band(x)
                row[label]=band_json(a,b)
            row['dense_floating_fraction_diagnostic']=float(np.count_nonzero(dense_vals<=float(x))/n)
            case['threshold_rows'].append(row)
        result['cases'].append(case)
    return result


def run():
    from gaussian_bits import generate_probe_block
    RESULTS.mkdir(exist_ok=True);WIT.mkdir(exist_ok=True)
    t,c=time.perf_counter(),time.process_time()
    ai,meta=load_exact_generalized(ROOT/'sources')
    write_json(RESULTS/'input_construction.json',meta)
    print('INPUT',meta['n'],'tau',float(jf(meta['tau'])),flush=True)
    (gi,gd,gcert),gcost=timed(generate_probe_block,meta['n'],S,WIT)
    print('GAUSSIAN',gcost,flush=True)
    with threadpool_limits(limits=1):
        (vi,di,bi),pcost=timed(scipy_proposals,ai,gi,gd)
        np.savez_compressed(WIT/'lanczos.npz',basis=vi,diagonal=di,offdiagonal=bi)
        print('LANCZOS',pcost,flush=True)
        (dv,dd,dvals),dcost=timed(dense_proposal,ai)
        np.savez_compressed(WIT/'dense.npz',basis=dv,diagonal=dd,diagnostic_values=dvals)
        print('DENSE PROPOSAL',dcost,flush=True)
        dense,dcheck=timed(certify_dense,ai,dv,dd,jf(meta['tau']))
        print('DENSE CHECK',dcheck,'error',float(jf(dense['operator_error'])),flush=True)
        write_json(RESULTS/'dense_certificate.json',dense)
        allcerts={};jacobi_costs=[];residual_costs=[]
        for k in KS:
            out=[]
            for ell in range(S):
                residual,rc=timed(certify_krylov,ai,vi[ell,:,:k],di[ell,:k],
                                  bi[ell,:k-1],gi[:,ell],gd,jf(meta['tau']))
                jacobi,jc=timed(certify_jacobi,di[ell,:k].tolist(),bi[ell,:k-1].tolist(),AD)
                residual_costs.append(dict(k=k,probe=ell,**rc))
                jacobi_costs.append(dict(k=k,probe=ell,**jc))
                out.append(dict(residual=residual,jacobi=jacobi))
                print('CERT',k,ell,'e',float(jf(residual['operator_error'])),
                      'jacobi_s',jc['wall_seconds'],flush=True)
            allcerts[str(k)]=out
            write_json(RESULTS/'krylov_certificates.json',allcerts)
        analysis,acost=timed(analyse,meta,allcerts,gcert,dense,dd,dvals)
        write_json(RESULTS/'cdf_results.json',analysis)
    costs=dict(gaussian_generation=gcost,lanczos_proposal=pcost,dense_proposal=dcost,
        dense_verification=dcheck,krylov_residuals=residual_costs,jacobi_construction=jacobi_costs,
        envelope_analysis=acost,total_wall_seconds=time.perf_counter()-t,
        total_cpu_seconds=time.process_time()-c,peak_rss_bytes=rss_bytes(),
        environment=dict(python=sys.version,numpy=np.__version__,scipy=scipy.__version__,
                         platform=platform.platform(),threadpools=threadpool_info()),
        operations=dict(lanczos_matrix_vector_products=S*max(KS),
          full_reorthogonalization_passes=2*S*max(KS),
          residual_matrix_block_products=len(KS)*S,
          full_dense_eigendecompositions=1),
        scope='Process costs only. Failed attempts, literature, child diagnostics and replay are separate.')
    write_json(RESULTS/'experiment_resources.json',costs)
    print('COMPLETE',json.dumps(costs)[:1500],flush=True)


def replay():
    from gaussian_bits import verify_probe_block
    t,c=time.perf_counter(),time.process_time()
    ai,meta=load_exact_generalized(ROOT/'sources')
    oldmeta=json.loads((RESULTS/'input_construction.json').read_text())
    for key in ('n','scale','tau','M','input_sha256'):
        require(meta[key]==oldmeta[key],'input construction mismatch: '+key)
    vr=verify_probe_block(WIT,expected_n=meta['n'],expected_s=S)
    print('GAUSSIAN REPLAY',str(vr)[:300],flush=True)
    gi=np.load(WIT/'gaussian_probe_ints.npy',allow_pickle=False)
    gcert=json.loads((WIT/'gaussian_probe_certificate.json').read_text())
    require(gi.shape==(meta['n'],S),'saved probe matrix shape mismatch')
    require(gcert['probe_denominator']==str(1<<40),'saved probe denominator mismatch')
    gd=1<<40
    lanczos=np.load(WIT/'lanczos.npz',allow_pickle=False)
    allcerts=json.loads((RESULTS/'krylov_certificates.json').read_text())
    with threadpool_limits(limits=1):
        for k in KS:
            for ell in range(S):
                got=certify_krylov(ai,lanczos['basis'][ell,:,:k],lanczos['diagonal'][ell,:k],
                    lanczos['offdiagonal'][ell,:k-1],gi[:,ell],gd,jf(meta['tau']))
                old=allcerts[str(k)][ell]['residual']
                for key,value in got.items():
                    if key not in ('wall_seconds','cpu_seconds','peak_rss_bytes'):
                        require(value==old[key],'residual mismatch '+key)
                verify_certificate(allcerts[str(k)][ell]['jacobi'],
                    lanczos['diagonal'][ell,:k].tolist(),lanczos['offdiagonal'][ell,:k-1].tolist(),AD)
                print('REPLAY',k,ell,flush=True)
        dense_np=np.load(WIT/'dense.npz',allow_pickle=False)
        dense=certify_dense(ai,dense_np['basis'],dense_np['diagonal'],jf(meta['tau']))
        olddense=json.loads((RESULTS/'dense_certificate.json').read_text())
        for key,value in dense.items():
            if key not in ('wall_seconds','cpu_seconds','peak_rss_bytes'):
                require(value==olddense[key],'dense certificate mismatch '+key)
        rebuilt=analyse(meta,allcerts,gcert,dense,dense_np['diagonal'],dense_np['diagnostic_values'])
        saved=json.loads((RESULTS/'cdf_results.json').read_text())
        def strip_costs(o):
            if isinstance(o,dict):
                return {k:strip_costs(v) for k,v in o.items() if not k.endswith('_cost')}
            if isinstance(o,list):return [strip_costs(v) for v in o]
            return o
        require(strip_costs(rebuilt)==strip_costs(saved),'CDF envelope replay mismatch')
    receipt=dict(all_checks_passed=True,wall_seconds=time.perf_counter()-t,
                 cpu_seconds=time.process_time()-c,peak_rss_bytes=rss_bytes(),
                 eigensolver_calls=0,random_draws=0,
                 guarantee='Deterministic witnesses exact; stochastic coverage conditional on independent uniform input bits.')
    write_json(RESULTS/'independent_replay.json',receipt)
    print(json.dumps(receipt,indent=2),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--run',action='store_true')
    parser.add_argument('--replay',action='store_true')
    args=parser.parse_args()
    require(args.run != args.replay,'choose exactly one of --run or --replay')
    run() if args.run else replay()
