"""Reproducible checks. Run `python validate.py` or select --part.

Monte Carlo checks are diagnostics, not proofs and not estimates of full TV
error. Exact identities, finite interval enclosures, and large-count stress
cases are recorded separately.
"""
from __future__ import annotations
import argparse, json, math, os, platform, random, statistics, sys, time
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from pathlib import Path
import numpy as np
import mpmath as mp
from prototype import PositiveGBS
from rational_gaussian import (RationalGaussian,pure_kernel,trace_modes,mean_counts,
                               log_herald_probability)
from matching_gadgets import edge_gadget,exact_count,weighted_to_unweighted
from bigint_sampler import DyadicUnimodal,_as_iv

OUT=Path(__file__).resolve().parent/'results'; OUT.mkdir(exist_ok=True)


def evaluate_pgf(model,z):
    a,b,c=model.pgf_parts(z)
    with mp.workdps(60):
        return float(mp.sqrt(mp.mpf(a.numerator)/a.denominator)
                     *mp.exp(mp.mpf(b.numerator)/b.denominator)
                     *mp.mpf(c.numerator)/c.denominator)


def scalar_checks():
    checks=0
    for n in [1,2,7,20,31]:
        for p in [F(1,7),F(1,2),F(6,7)]:
            mode=min(n,((n+1)*p.numerator)//p.denominator)
            def lr(k,m):
                return (mp.iv.loggamma(m+1)+mp.iv.loggamma(n-m+1)
                        -mp.iv.loggamma(k+1)-mp.iv.loggamma(n-k+1)
                        +(k-m)*(mp.iv.log(_as_iv(p))-mp.iv.log(_as_iv(1-p))))
            law=DyadicUnimodal(n,mode,lr,F(1,10**8),16)
            def mass(k): return F(math.comb(n,k))*p**k*(1-p)**(n-k)
            fm=mass(mode)
            for k in range(n+1):
                lo,hi=law.bounds(k); exact=mass(k)/fm
                assert F(lo,law.scale)<=exact<=F(hi,law.scale)
                checks+=1
    for shape in [F(1,2),F(3,2),F(21,2)]:
        for p in [F(1,10),F(1,2),F(9,10)]:
            x=(shape-1)*(1-p)/p; mode=max(0,x.numerator//x.denominator)
            maximum=max(40,mode+5)
            def lr(k,m):
                return (mp.iv.loggamma(k+_as_iv(shape))-mp.iv.loggamma(k+1)
                        -mp.iv.loggamma(m+_as_iv(shape))+mp.iv.loggamma(m+1)
                        +(k-m)*mp.iv.log(_as_iv(1-p)))
            law=DyadicUnimodal(maximum,mode,lr,F(1,10**8),24)
            weights=[F(1)]
            for k in range(1,maximum+1): weights.append(weights[-1]*(shape+k-1)*(1-p)/k)
            for k in range(maximum+1):
                lo,hi=law.bounds(k); exact=weights[k]/weights[mode]
                assert F(lo,law.scale)<=exact<=F(hi,law.scale)
                checks+=1
    for rate in [F(1,10),F(2),F(10)]:
        maximum=40; mode=rate.numerator//rate.denominator
        def lr(k,m):
            return (mp.iv.loggamma(m+1)-mp.iv.loggamma(k+1)
                    +(k-m)*mp.iv.log(_as_iv(rate)))
        law=DyadicUnimodal(maximum,mode,lr,F(1,10**8),16)
        for k in range(maximum+1):
            exact=rate**(k-mode)*F(math.factorial(mode),math.factorial(k))
            lo,hi=law.bounds(k)
            assert F(lo,law.scale)<=exact<=F(hi,law.scale)
            checks+=1
    return {'exact_interval_enclosure_checks':checks,'status':'passed'}


def gadget_checks():
    checks=0
    for w in range(1,128):
        n,es=edge_gadget(w)
        assert exact_count(n,es)==w; checks+=1
        assert exact_count(n,es,(0,1))==1; checks+=1
        assert exact_count(n,es,(0,))==0; checks+=1
    # Whole weighted graph versus independently computed 4-vertex hafnian.
    r=random.Random(931)
    for _ in range(20):
        A=[[F(0)]*4 for _ in range(4)]
        for i in range(4):
            for j in range(i): A[i][j]=A[j][i]=F(r.randrange(0,5),r.randrange(1,5))
        n,es,D=weighted_to_unweighted(A)
        expected=A[0][1]*A[2][3]+A[0][2]*A[1][3]+A[0][3]*A[1][2]
        assert F(exact_count(n,es),D**2)==expected; checks+=1
    return {'exact_matching_gadget_checks':checks,'status':'passed'}


def pure_reference(B,g,H,h,z,cutoff=18):
    """Independent Fock expansion of the original pure-state amplitude.

    This does not call the Schur sampler or its reduced matching recurrence.
    The returned missing mass is a numerical diagnostic of the chosen cutoff.
    """
    B=np.asarray(B,float); g=np.asarray(g,float); m=len(B)
    U=[i for i in range(m) if i not in H]
    @lru_cache(None)
    def amplitude(state):
        if not any(state): return 1.0
        a=next(i for i,n in enumerate(state) if n)
        rest=list(state); rest[a]-=1
        val=g[a]*amplitude(tuple(rest)) if g[a] else 0.0
        for b in range(m):
            if rest[b] and B[a,b]:
                nxt=rest.copy(); nxt[b]-=1
                val+=rest[b]*B[a,b]*amplitude(tuple(nxt))
        return val
    ld=np.linalg.slogdet(np.eye(m)-B@B)[1]
    lognorm=-.5*ld+float(g@np.linalg.solve(np.eye(m)-B,g))
    mass=0.0; marked=0.0
    for counts in product(range(cutoff+1),repeat=len(U)):
        state=[0]*m
        for i,k in zip(H,h): state[i]=k
        for i,k in zip(U,counts): state[i]=k
        a=amplitude(tuple(state))
        p=math.exp(-lognorm-sum(math.lgamma(k+1) for k in state))*a*a
        mass+=p; marked+=p*math.prod(float(x)**k for x,k in zip(z,counts))
    return mass,marked


def fast_statistics():
    fixtures=[
      ('dense_unconditioned',[[.13,.21,.08],[.21,.19,.12],[.08,.12,.1]],[],[]),
      ('one_photon_herald',[[.13,.21,.08],[.21,.19,.12],[.08,.12,.1]],[0],[1]),
      ('two_photon_herald',[[.13,.21,.08],[.21,.19,.12],[.08,.12,.1]],[0],[2]),
      ('two_mode_herald',[[.13,.21,.08],[.21,.19,.12],[.08,.12,.1]],[0,1],[1,1]),
      ('vacuum_herald',[[.13,.21,.08],[.21,.19,.12],[.08,.12,.1]],[0],[0]),
      ('sparse_bipartite',[[0,.6],[.6,0]],[],[])]
    rows=[]
    for number,(name,B,H,h) in enumerate(fixtures):
        B=np.array(B); model=PositiveGBS(B,H,h)
        n=16000; z=np.linspace(.61,.86,len(model.U))
        t=time.perf_counter(); samples=model.sample_many(n,6171+number); seconds=time.perf_counter()-t
        vals=np.prod(z**samples,axis=1); estimate=float(vals.mean()); se=float(vals.std(ddof=1)/math.sqrt(n))
        analytic=model.conditional_pgf(z)
        mass,marked=pure_reference(B,np.zeros(len(B)),H,h,z,cutoff=16)
        ph=math.exp(model.log_herald_probability)
        reference=marked/ph; tail=max(0.0,1-mass/ph)
        assert abs(reference-analytic)<2e-10+tail
        assert np.all((samples.sum(axis=1)+sum(h))%2==0)
        if name=='sparse_bipartite': assert np.all(samples[:,0]==samples[:,1])
        rows.append(dict(name=name,samples=n,seconds=seconds,empirical_pgf=estimate,
                         analytic_pgf=analytic,independent_fock_pgf=reference,
                         fock_omitted_mass=tail,standard_errors=(estimate-analytic)/se if se else 0,
                         herald_probability=ph))
    return rows


def rational_statistics():
    cases=[]
    cases.append(('displaced_pure',RationalGaussian.from_pure([[F(1,10),F(1,5)],[F(1,5),F(1,8)]],[F(1,3),F(1,4)])))
    cases.append(('displaced_herald',RationalGaussian.from_pure([[F(1,10),F(1,5)],[F(1,5),F(1,8)]],[F(1,3),F(1,4)],[0],[2])))
    B=[[F(1,10),F(1,8),F(1,9)],[F(1,8),F(1,7),F(1,10)],[F(1,9),F(1,10),F(1,9)]]
    K,l=pure_kernel(B,[F(1,4),F(1,5),F(1,6)])
    KM,lM=trace_modes(K,l,[0,1])
    assert any(KM[i][j+2] for i in range(2) for j in range(2))
    cases.append(('mixed_displaced_herald',RationalGaussian(KM,lM,[0],[1])))
    cases.append(('thermal',RationalGaussian([[0,F(1,2)],[F(1,2),0]],[0,0])))
    rows=[]
    for i,(name,model) in enumerate(cases):
        rng=random.Random(72931+i); n=700; z=[F(7,10)]*len(model.U)
        t=time.perf_counter(); samples=[model.sample(rng,F(1,10**10)) for _ in range(n)]; seconds=time.perf_counter()-t
        vals=np.array([math.prod(float(v)**k for v,k in zip(z,s)) for s in samples])
        exact=evaluate_pgf(model,z); se=float(vals.std(ddof=1)/math.sqrt(n))
        rows.append(dict(name=name,samples=n,seconds=seconds,total_variation_budget_per_draw='1e-10',
                         empirical_pgf=float(vals.mean()),analytic_pgf=exact,
                         standard_errors=(float(vals.mean())-exact)/se if se else 0,
                         exact_mean_counts=[str(x) for x in mean_counts(model)],
                         measured_mean_counts=np.mean(np.array(samples),axis=0).tolist()))
    return rows


def stress_cases():
    delta=F(1,10**40); lam=F(1,10**60)
    B=[[F(0),lam/2,lam/3],
       [lam/2,(1-delta)*F(3,5),(1-delta)*F(2,5)],
       [lam/3,(1-delta)*F(2,5),(1-delta)*F(3,5)]]
    t=time.perf_counter(); model=RationalGaussian.from_pure(B,None,[0],[4]); setup=time.perf_counter()-t
    rng=random.Random(76219); t=time.perf_counter(); sample=model.sample(rng,F(1,10**12)); elapsed=time.perf_counter()-t
    with mp.workdps(60):
        logp=log_herald_probability(model,digits=70)/mp.log(10)
        probability_text=mp.nstr(mp.power(10,logp),20)
    assert (sum(sample)+4)%2==0
    # Exact cancellation of a rare coupling, for a genuinely heralded output.
    pgfs=[]; logs=[]
    for l in [F(1,100),F(1,10**100)]:
        BB=[[0,l/2,l/3],[l/2,F(1,5),F(1,8)],[l/3,F(1,8),F(1,7)]]
        q=RationalGaussian.from_pure(BB,None,[0],[4])
        pgfs.append(q.pgf_parts([F(2,3),F(3,4)]))
        logs.append(str(log_herald_probability(q,digits=50)/mp.log(10)))
    assert pgfs[0]==pgfs[1]
    return dict(combined_bright_rare=dict(delta=str(delta),coupling=str(lam),herald_modes=[0],herald_counts=[4],
       setup_seconds=setup,sampling_seconds=elapsed,sample_counts=list(map(str,sample)),
       exact_conditional_mean_counts=[str(x) for x in mean_counts(model)],
       mean_counts_scientific=[float(x) for x in mean_counts(model)],
       herald_probability=probability_text,log10_herald_probability=str(logp),
       matching_states=model.matching.Z.cache_info().currsize,
       scalar_call_bound=model.engine.max_scalar_calls+1,tolerance='1e-12'),
       exact_rare_coupling_cancellation={'status':'passed','log10_herald_probabilities':logs})


def brightness_scaling():
    m=8; C=.5*np.eye(m)+.5*np.ones((m,m))/m; rows=[]
    for j,delta in enumerate([1e-3,1e-6,1e-9,1e-12]):
        B=(1-delta)*C
        t=time.perf_counter(); model=PositiveGBS(B); setup=time.perf_counter()-t
        rng=np.random.default_rng(881+j); n=400; times=[]; totals=[]
        for _ in range(n):
            t=time.perf_counter(); out=model.sample(rng); times.append(time.perf_counter()-t); totals.append(int(out.sum()))
        eig=np.linalg.eigvalsh(B); E=float(np.sum(eig**2/(1-eig**2)))
        rows.append(dict(modes=m,delta=delta,mean_photon_number=E,setup_seconds=setup,samples=n,
                         median_seconds=statistics.median(times),mean_seconds=statistics.mean(times),
                         empirical_mean_photons=statistics.mean(totals),max_generated_count=max(totals)))
    return rows


def independent_extensions():
    records=[]
    B=[[F(1,10),F(1,5)],[F(1,5),F(1,8)]]; g=[F(1,3),F(1,4)]
    for name,H,h in [('displaced_pure',[],[]),('displaced_herald',[0],[2])]:
        q=RationalGaussian.from_pure(B,g,H,h)
        z=[F(7,10)]*len(q.U)
        exact=evaluate_pgf(q,z)
        mass,marked=pure_reference(B,g,H,h,z,cutoff=24)
        ph=float(mp.exp(log_herald_probability(q)))
        reference=marked/ph; tail=max(0.,1-mass/ph)
        assert abs(exact-reference)<tail+2e-12
        records.append(dict(name=name,pgf=exact,independent_fock_pgf=reference,omitted_mass=tail))
    B3=[[F(1,10),F(1,8),F(1,9)],[F(1,8),F(1,7),F(1,10)],[F(1,9),F(1,10),F(1,9)]]
    g3=[F(1,4),F(1,5),F(1,6)]
    K,l=pure_kernel(B3,g3); KM,lM=trace_modes(K,l,[0,1])
    reduced=RationalGaussian(KM,lM,[0],[1]); unreduced=RationalGaussian(K,l,[0],[1])
    assert reduced.pgf_parts([F(7,10)])==unreduced.pgf_parts([F(7,10),F(1)])
    exact=evaluate_pgf(reduced,[F(7,10)])
    mass,marked=pure_reference(B3,g3,[0],[1],[F(7,10),F(1)],cutoff=24)
    ph=float(mp.exp(log_herald_probability(unreduced)))
    reference=marked/ph; tail=max(0.,1-mass/ph)
    assert abs(exact-reference)<tail+2e-12
    records.append(dict(name='mixed_displaced_herald',pgf=exact,independent_fock_pgf=reference,omitted_mass=tail,
                        exact_partial_trace_identity='passed'))
    for maker in [lambda:PositiveGBS(np.diag([.2,.3]),[0],[1]),
                  lambda:RationalGaussian.from_pure([[F(1,5),0],[0,F(3,10)]],None,[0],[1])]:
        try: maker()
        except ValueError as ex: assert 'zero probability' in str(ex)
        else: raise AssertionError('Impossible herald was accepted')
    assert RationalGaussian.from_pure([[0]],None,[0],[0]).sample(random.Random(3))==[]
    assert RationalGaussian.from_pure([[0]]).sample(random.Random(3))==[0]
    q=RationalGaussian.from_pure([[0,F(1,2)],[F(1,2),0]],None,[0],[1])
    assert q.pgf_parts([0])[2]==0
    records.append(dict(edge_cases='zero herald, full observation, vacuum, zero PGF: passed'))
    return records


def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--part',choices=['algebra','fast','rational','stress','scaling','independent','all'],default='all')
    args=parser.parse_args()
    functions={'algebra':lambda:dict(scalar=scalar_checks(),gadgets=gadget_checks()),
               'fast':fast_statistics,'rational':rational_statistics,'stress':stress_cases,'scaling':brightness_scaling,'independent':independent_extensions}
    parts=list(functions) if args.part=='all' else [args.part]
    for part in parts:
        t=time.perf_counter(); result=functions[part]()
        envelope={'part':part,'seconds':time.perf_counter()-t,'result':result,
                  'python':sys.version,'numpy':np.__version__,'mpmath':mp.__version__,'platform':platform.platform()}
        (OUT/f'{part}.json').write_text(json.dumps(envelope,indent=2))
        print(json.dumps(envelope,indent=2),flush=True)
if __name__=='__main__': main()
