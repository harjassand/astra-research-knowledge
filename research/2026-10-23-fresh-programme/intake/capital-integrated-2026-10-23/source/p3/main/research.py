#!/usr/bin/env python3
"""Private Astra P3: acquired conditional-odds importance certificates.

The exact-model proof is in ../verification/MINIMAX_AND_CUBIC_COMPILER.md.
Integer outward adjoints and Decimal interval certificate arithmetic are
distinct from binary64 simulation. The latter has a conservative documented
uniform log-weight error allowance, not a claim of formal kernel verification.
"""
from __future__ import annotations
import argparse
from dataclasses import dataclass, asdict
from decimal import Decimal, localcontext, ROUND_FLOOR, ROUND_CEILING, ROUND_HALF_EVEN
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import platform
import time
import numpy as np
from scipy.special import expit, logsumexp

ROOT = Path(__file__).resolve().parent
PREC = 100
GRID_BITS = 80
Q_BITS = 32
SCALE = 1 << GRID_BITS
QSCALE = 1 << Q_BITS


def dec(x):
    if isinstance(x, Decimal):
        return x
    if isinstance(x, Fraction):
        with localcontext() as c:
            c.prec = PREC
            return Decimal(x.numerator) / Decimal(x.denominator)
    return Decimal(str(x))


def directed(op, direction):
    with localcontext() as c:
        c.prec = PREC
        c.rounding = direction
        return +op()


class Interval:
    """Positive Decimal intervals, with outward elementary operations."""
    def __init__(self, lo, hi=None):
        self.lo = dec(lo)
        self.hi = self.lo if hi is None else dec(hi)
        if self.lo > self.hi:
            raise ValueError('reversed interval')

    def __add__(self, rhs):
        rhs = rhs if isinstance(rhs, Interval) else Interval(rhs)
        return Interval(directed(lambda: self.lo + rhs.lo, ROUND_FLOOR),
                        directed(lambda: self.hi + rhs.hi, ROUND_CEILING))

    def __mul__(self, rhs):
        rhs = rhs if isinstance(rhs, Interval) else Interval(rhs)
        if self.lo < 0 or rhs.lo < 0:
            raise ValueError('positive multiplication only')
        return Interval(directed(lambda: self.lo * rhs.lo, ROUND_FLOOR),
                        directed(lambda: self.hi * rhs.hi, ROUND_CEILING))

    def __truediv__(self, rhs):
        rhs = rhs if isinstance(rhs, Interval) else Interval(rhs)
        if self.lo < 0 or rhs.lo <= 0:
            raise ValueError('positive division only')
        return Interval(directed(lambda: self.lo / rhs.hi, ROUND_FLOOR),
                        directed(lambda: self.hi / rhs.lo, ROUND_CEILING))

    def complement(self):
        return Interval(directed(lambda: Decimal(1) - self.hi, ROUND_FLOOR),
                        directed(lambda: Decimal(1) - self.lo, ROUND_CEILING))


def exp_interval(x):
    """Decimal.exp is correctly rounded; widen by a full last-place unit."""
    with localcontext() as c:
        c.prec = PREC
        z = dec(x).exp()
        ulp = Decimal(1).scaleb(z.adjusted() - PREC + 1)
    return Interval(directed(lambda: z - ulp, ROUND_FLOOR),
                    directed(lambda: z + ulp, ROUND_CEILING))


def log_upper(x):
    with localcontext() as c:
        c.prec = PREC
        z = dec(x).ln()
        ulp = Decimal(1).scaleb(z.adjusted() - PREC + 1) if z else Decimal('1e-100')
        c.rounding = ROUND_CEILING
        return +(z + ulp)


def odds_probability(p: Fraction, log_ratio: Decimal):
    odds = Interval(p) / Interval(1-p)
    odds = odds * exp_interval(log_ratio)
    return odds / (Interval(1) + odds)


def risk_upper(a: Decimal, q: Fraction):
    ai = Interval(a)
    bi = ai.complement()
    return (ai*ai/Interval(q) + bi*bi/Interval(1-q)).hi


def q_grid(q):
    with localcontext() as c:
        c.prec = PREC
        k = int((dec(q)*QSCALE).to_integral_value(rounding=ROUND_HALF_EVEN))
    return min(QSCALE-1, max(1,k))


@dataclass(frozen=True)
class Config:
    name: str
    d: int
    T: int
    b_denominator: int = 128
    rho: str = '1/2'
    kappa: str = '1/16'
    sigma: str = '7/16'

    def b_fraction(self):
        return [Fraction(4+(j%3),self.b_denominator) for j in range(self.d)]

    def p_fraction(self):
        return [Fraction(3+(j%3),8) for j in range(self.d)]

    @property
    def b(self):
        return np.array([float(v) for v in self.b_fraction()])

    @property
    def p(self):
        return np.array([float(v) for v in self.p_fraction()])

    @property
    def offset_per_step(self):
        return float(sum(self.b_fraction())+Fraction(1,8))

    def validate(self):
        r,k,s=map(Fraction,(self.rho,self.kappa,self.sigma))
        assert r>=0 and k>=0 and s>=0 and r+k+s<=1
        assert r+3*k<1


def neighbor(x):
    return 0.5*x + 0.25*(np.roll(x,1,axis=-1)+np.roll(x,-1,axis=-1))


def ceil_div(n,d):
    return -((-n)//d)


def acquire_intervals(cfg: Config):
    """Fixed dyadic precision; every lower/upper recurrence rounds outwards."""
    start=time.perf_counter()
    cfg.validate()
    r,k,s=map(Fraction,(cfg.rho,cfg.kappa,cfg.sigma))
    coeffs=[r+3*k/2, 3*k/4, 3*k/4]
    denom=math.lcm(*(v.denominator for v in coeffs))
    nums=[v.numerator*(denom//v.denominator) for v in coeffs]
    bint=[int(v*SCALE) for v in cfg.b_fraction()]
    assert all(Fraction(v,SCALE)==b for v,b in zip(bint,cfg.b_fraction()))
    lower=[[0]*cfg.d for _ in range(cfg.T)]
    upper=[[0]*cfg.d for _ in range(cfg.T)]
    vlo=bint[:]; vhi=bint[:]
    two_s=2*s
    for t in range(cfg.T-1,-1,-1):
        lower[t]=[(two_s.numerator*v)//two_s.denominator for v in vlo]
        upper[t]=[ceil_div(two_s.numerator*v,two_s.denominator) for v in vhi]
        vlo=[bint[j]+(r.numerator*vlo[j])//r.denominator for j in range(cfg.d)]
        vhi=[bint[j]+ceil_div(nums[0]*vhi[j]+nums[1]*vhi[(j-1)%cfg.d]+nums[2]*vhi[(j+1)%cfg.d],denom) for j in range(cfg.d)]
    elapsed=time.perf_counter()-start
    return lower,upper,elapsed


def certified_proposals(cfg,lower,upper):
    start=time.perf_counter()
    pfrac=cfg.p_fraction()
    names=['conditional_mc','linear_tilt','log_midpoint_tilt','probability_midpoint_minimax']
    qnums={name:np.empty((cfg.T,cfg.d),dtype=np.uint64) for name in names}
    endpoints=[]
    width_budget=Fraction(0)
    for t in range(cfg.T):
        row=[]
        for j in range(cfg.d):
            ell=dec(Fraction(lower[t][j],SCALE)); upp=dec(Fraction(upper[t][j],SCALE))
            ai=odds_probability(pfrac[j],ell); bi=odds_probability(pfrac[j],upp)
            a,b=ai.lo,bi.hi
            with localcontext() as c:
                c.prec=PREC
                qmid=(a+b)/2
                midlog=(ell+upp)/2
            qnums['conditional_mc'][t,j]=q_grid(dec(pfrac[j]))
            qnums['linear_tilt'][t,j]=q_grid((ai.lo+ai.hi)/2)
            qi=odds_probability(pfrac[j],midlog)
            qnums['log_midpoint_tilt'][t,j]=q_grid((qi.lo+qi.hi)/2)
            qnums['probability_midpoint_minimax'][t,j]=q_grid(qmid)
            row.append((a,b))
            width_budget+=Fraction((upper[t][j]-lower[t][j])**2,16*SCALE*SCALE)
        endpoints.append(row)
    logs={name:certificate_for_q(cfg,endpoints,qs) for name,qs in qnums.items()}
    return qnums,endpoints,logs,float(width_budget),time.perf_counter()-start


def certificate_for_q(cfg,endpoints,qnums):
    total=Decimal(0)
    for t in range(cfg.T):
        for j in range(cfg.d):
            q=Fraction(int(qnums[t,j]),QSCALE)
            a,b=endpoints[t][j]
            ki=max(Decimal(1),risk_upper(a,q),risk_upper(b,q))
            total=directed(lambda:total+log_upper(ki),ROUND_CEILING)
    return str(total)


def mean_path_adjoint(cfg,iterations=8):
    """Equally informed target-specific deterministic exponential-tilt baseline."""
    start=time.perf_counter()
    r,k,s=map(lambda v:float(Fraction(v)),(cfg.rho,cfg.kappa,cfg.sigma))
    base=np.log(cfg.p/(1-cfg.p))
    q=np.broadcast_to(cfg.p,(cfg.T,cfg.d)).copy()
    for _ in range(iterations):
        states=np.zeros((cfg.T+1,cfg.d))
        for t in range(cfg.T):
            z=neighbor(states[t])
            states[t+1]=r*states[t]+k*z*z*z+s*(2*q[t]-1)
        v=cfg.b.copy()
        theta=np.empty_like(q)
        for t in range(cfg.T-1,-1,-1):
            theta[t]=2*s*v
            z=neighbor(states[t])
            v=cfg.b+r*v+3*k*neighbor(z*z*v)
        qnew=expit(base+theta)
        q=0.5*q+0.5*qnew
    qnums=np.rint(q*QSCALE).clip(1,QSCALE-1).astype(np.uint64)
    return qnums,time.perf_counter()-start


def exact_log_coefficients(cfg,qnums):
    """Decimal correctly-rounded logarithms, then recorded binary64 rounding."""
    start=time.perf_counter()
    yes=np.empty_like(qnums,dtype=float); no=np.empty_like(yes)
    total_error=Decimal(0)
    pfrac=cfg.p_fraction()
    with localcontext() as c:
        c.prec=PREC
        for t in range(cfg.T):
            for j in range(cfg.d):
                q=Fraction(int(qnums[t,j]),QSCALE)
                a=(dec(pfrac[j])/dec(q)).ln()
                b=(dec(1-pfrac[j])/dec(1-q)).ln()
                yes[t,j]=float(a); no[t,j]=float(b)
                e=max(abs(Decimal.from_float(float(a))-a),abs(Decimal.from_float(float(b))-b))+Decimal('1e-90')
                total_error+=e
    return yes,no,float(total_error),time.perf_counter()-start


def roundoff_allowance(cfg,yes,no,coefficient_error):
    """Conservative standard binary64 model, documented in NUMERICS.md."""
    u=2.0**-53
    r=float(Fraction(cfg.rho)+3*Fraction(cfg.kappa))
    state=64*u/(1-r)
    bsum=float(np.sum(cfg.b)); maxlr=float(np.max(np.maximum(np.abs(yes),np.abs(no))))
    state_score=cfg.T*bsum*state
    dots=cfg.T*(8*cfg.d*u/(1-8*cfg.d*u))*(bsum+cfg.d*maxlr)
    sums=(8*cfg.T*u/(1-8*cfg.T*u))*cfg.T*(bsum+cfg.d*maxlr)
    return state_score+dots+sums+coefficient_error+1e-12


def sample_paths(cfg,qnums,n,seed,batch=1024):
    setup=time.perf_counter()
    yes,no,coeff_err,coeff_seconds=exact_log_coefficients(cfg,qnums)
    tau=roundoff_allowance(cfg,yes,no,coeff_err)
    setup_seconds=time.perf_counter()-setup
    start=time.perf_counter()
    rng=np.random.Generator(np.random.PCG64(seed))
    r,k,s=map(lambda v:float(Fraction(v)),(cfg.rho,cfg.kappa,cfg.sigma))
    scores=np.empty(n)
    max_abs_state=0.0
    for first in range(0,n,batch):
        m=min(batch,n-first)
        x=np.zeros((m,cfg.d)); score=np.zeros(m)
        for t in range(cfg.T):
            bits=rng.integers(0,QSCALE,size=(m,cfg.d),dtype=np.uint64)<qnums[t]
            z=neighbor(x)
            x=r*x+k*z*z*z+s*(2*bits.astype(float)-1)
            np.clip(x,-1,1,out=x)
            score+=np.sum(x*cfg.b+np.where(bits,yes[t],no[t]),axis=1)
        max_abs_state=max(max_abs_state,float(np.max(np.abs(x))))
        scores[first:first+m]=score
    sampling_seconds=time.perf_counter()-start
    return scores,{'setup_seconds':setup_seconds,'log_coefficient_seconds':coeff_seconds,
                   'sampling_seconds':sampling_seconds,'uniform_log_weight_error_allowance':tau,
                   'max_abs_final_state_observed':max_abs_state,'paths':n,
                   'state_coordinate_updates':n*cfg.T*cfg.d,'seed':seed,'rng':'numpy.PCG64',
                   'bit_distribution':'recorded dyadic q, uint64 uniform draw below 2**32'}


def certified_log_mean(scores):
    """Positive Decimal exp/sum; rounding allowance < 1e-35 for these sizes."""
    start=time.perf_counter()
    with localcontext() as c:
        c.prec=60
        pivot=Decimal.from_float(float(np.max(scores)))
        total=Decimal(0)
        for v in scores:
            total+=(Decimal.from_float(float(v))-pivot).exp()
        result=pivot+(total/len(scores)).ln()
    return float(result),time.perf_counter()-start


def statistics(scores,cfg,logK,tau):
    lm,elapsed=certified_log_mean(scores)
    scaled=np.exp(scores-lm)
    rv=float(np.var(scaled,ddof=1))
    n=len(scores)
    eps=math.sqrt(max(0,math.expm1(float(logK)))/(n*0.05)) if float(logK)<700 else float('inf')
    logz=lm-cfg.T*cfg.offset_per_step
    ci=None
    if eps<1:
        ci=[logz-tau-math.log1p(eps),logz+tau-math.log1p(-eps)]
    return {'log_probability_estimate':logz,'log10_probability_estimate':logz/math.log(10),
            'empirical_relative_variance':rv,'empirical_ess':float(n/(1+rv)),
            'empirical_standard_error_relative':math.sqrt(rv/n),
            'certified_relative_sampling_error_at_95pct':eps,
            'log_probability_95pct_interval':ci,'certificate_log_second_moment_upper':float(logK),
            'aggregation_seconds':elapsed,'aggregation_arithmetic_allowance_log':1e-35,
            'inference_label':'exact-model random-sampling bound plus binary64/Decimal arithmetic-model allowance; PRNG and platform are not formal verified'}


def smc(cfg,qnums,particles,replicates,seed):
    start=time.perf_counter()
    yes,no,_,setup=exact_log_coefficients(cfg,qnums)
    rng=np.random.Generator(np.random.PCG64(seed))
    r,k,s=map(lambda v:float(Fraction(v)),(cfg.rho,cfg.kappa,cfg.sigma))
    scores=np.zeros(replicates)
    for rep in range(replicates):
        x=np.zeros((particles,cfg.d)); out=0.
        for t in range(cfg.T):
            bits=rng.integers(0,QSCALE,size=(particles,cfg.d),dtype=np.uint64)<qnums[t]
            z=neighbor(x)
            x=r*x+k*z*z*z+s*(2*bits.astype(float)-1)
            np.clip(x,-1,1,out=x)
            inc=np.sum(x*cfg.b+np.where(bits,yes[t],no[t]),axis=1)
            norm=logsumexp(inc)
            out+=norm-math.log(particles)
            weights=np.exp(inc-norm)
            cumul=np.cumsum(weights); cumul[-1]=1.
            positions=(rng.random()+np.arange(particles))/particles
            x=x[np.searchsorted(cumul,positions,side='right')]
        scores[rep]=out
    elapsed=time.perf_counter()-start
    lm=float(logsumexp(scores)-math.log(replicates))
    rv=float(np.var(np.exp(scores-lm),ddof=1))
    return scores,{'log_probability_estimate':lm-cfg.T*cfg.offset_per_step,
                   'empirical_replicate_relative_variance':rv,
                   'equivalent_one_path_variance':rv*particles,
                   'empirical_standard_error_relative':math.sqrt(rv/replicates),
                   'total_seconds':elapsed,'log_coefficient_seconds':setup,
                   'particles':particles,'replicates':replicates,'seed':seed,
                   'state_coordinate_updates':particles*replicates*cfg.T*cfg.d,
                   'inference_label':'empirical particle baseline, no iid product certificate assigned'}


def anchored_envelope(cfg,lower,upper):
    """f(0)*prod(1-p+p exp ell/u); reports full accumulated log widths."""
    x=np.zeros(cfg.d); s0=0.
    r,k,s=map(lambda v:float(Fraction(v)),(cfg.rho,cfg.kappa,cfg.sigma))
    for _ in range(cfg.T):
        z=neighbor(x); x=r*x+k*z*z*z-s; s0+=float(x@cfg.b)
    lo=s0; hi=s0
    for t in range(cfg.T):
        for j,p in enumerate(cfg.p):
            ell=float(Fraction(lower[t][j],SCALE)); up=float(Fraction(upper[t][j],SCALE))
            lo+=math.log1p(p*math.expm1(ell)); hi+=math.log1p(p*math.expm1(up))
    offset=cfg.T*cfg.offset_per_step
    return {'log_lower_diagnostic':lo-offset,'log_upper_diagnostic':hi-offset,
            'log_width':hi-lo,'log10_width':(hi-lo)/math.log(10),
            'label':'analytically valid interval formula; these printed endpoints binary64 diagnostics'}


def exact_small_check():
    cfg=Config('root_small_exhaustive',2,8)
    m=cfg.d*cfg.T
    ids=np.arange(1<<m,dtype=np.uint64)
    bits=((ids[:,None]>>np.arange(m,dtype=np.uint64))&1).astype(bool).reshape(-1,cfg.T,cfg.d)
    x=np.zeros((len(ids),cfg.d)); score=np.zeros(len(ids)); lp=np.zeros(len(ids))
    r,k,s=map(lambda v:float(Fraction(v)),(cfg.rho,cfg.kappa,cfg.sigma))
    for t in range(cfg.T):
        z=neighbor(x); x=r*x+k*z*z*z+s*(2*bits[:,t].astype(float)-1)
        score+=np.sum(x*cfg.b,axis=1)
        lp+=np.sum(np.where(bits[:,t],np.log(cfg.p),np.log1p(-cfg.p)),axis=1)
    lower,upper,_=acquire_intervals(cfg)
    qs,endpoints,logs,width,_=certified_proposals(cfg,lower,upper)
    logz=float(logsumexp(score+lp))
    results={}
    for name,qnum in qs.items():
        q=qnum/QSCALE
        lq=np.sum(np.where(bits,np.log(q),np.log1p(-q)),axis=(1,2))
        R=float(np.exp(logsumexp(2*(score+lp)-lq)-2*logz))
        results[name]={'exact_enumeration_R_float':R,'bound_R':math.exp(float(logs[name]))}
        assert R<=math.exp(float(logs[name]))+1e-10
    violations=0
    for i in range(m):
        zero=(ids&(1<<i))==0
        dif=score[ids[zero]|np.uint64(1<<i)]-score[zero]
        t,j=divmod(i,cfg.d)
        ell=float(Fraction(lower[t][j],SCALE)); up=float(Fraction(upper[t][j],SCALE))
        violations+=int(np.sum((dif<ell-1e-12)|(dif>up+1e-12)))
    assert violations==0
    return {'paths_enumerated':len(ids),'bit_flip_checks':m*(len(ids)//2),
            'violations':violations,'log_probability':logz-cfg.T*cfg.offset_per_step,
            'risk_checks':results,'kind':'binary64 exhaustive supplemental check; exact Fraction check is separate'}


def run_case(cfg,index,skip_smc=False):
    out=ROOT/'results'/cfg.name
    out.mkdir(parents=True,exist_ok=True)
    print('starting '+cfg.name,flush=True)
    lower,upper,adj_seconds=acquire_intervals(cfg)
    qnums,endpoints,logs,width,cert_seconds=certified_proposals(cfg,lower,upper)
    qmean,mean_setup=mean_path_adjoint(cfg)
    qnums['mean_path_adjoint_8_iterations']=qmean
    logs['mean_path_adjoint_8_iterations']=certificate_for_q(cfg,endpoints,qmean)
    logK=float(logs['probability_midpoint_minimax'])
    required=max(1024,math.ceil(math.expm1(logK)/(.05*.05*.05)))
    n=((required+255)//256)*256
    cap_pass=n<=32768
    n=min(n,32768)
    result={'config':asdict(cfg),'dimension_of_independent_innovations':cfg.d*cfg.T,
            'possible_binary_paths_power_of_two':cfg.d*cfg.T,
            'adjoint_seconds':adj_seconds,'certificate_seconds':cert_seconds,
            'mean_path_setup_seconds':mean_setup,'width_only_log_bound':width,
            'required_paths_before_cap':required,'paths_per_method':n,'path_cap_pass':cap_pass,
            'anchored_probability_envelope':anchored_envelope(cfg,lower,upper),
            'logK_decimal':logs,'methods':{}}
    (out/'intervals.json').write_text(json.dumps({'scale_bits':GRID_BITS,'lower_numerators':lower,'upper_numerators':upper}))
    np.savez_compressed(out/'proposals.npz',**qnums)
    (out/'setup.json').write_text(json.dumps(result,indent=2))
    for k,(name,qnum) in enumerate(qnums.items()):
        seed=202610230731+index*100+k
        print(f'  {name}: n={n}, logK={float(logs[name]):.6g}',flush=True)
        score,receipt=sample_paths(cfg,qnum,n,seed)
        np.save(out/(name+'_logweights.npy'),score)
        stats=statistics(score,cfg,logs[name],receipt['uniform_log_weight_error_allowance'])
        stats.update(receipt)
        stats['end_to_end_seconds']=adj_seconds+cert_seconds+receipt['setup_seconds']+receipt['sampling_seconds']+stats['aggregation_seconds']+(mean_setup if name.startswith('mean_path') else 0)
        stats['variance_times_sampling_cost_per_path']=stats['empirical_relative_variance']*receipt['sampling_seconds']/n
        result['methods'][name]=stats
        (out/'results.json').write_text(json.dumps(result,indent=2))
    if not skip_smc:
        print('  linear_tilt_particle_filter',flush=True)
        score,stats=smc(cfg,qnums['linear_tilt'],256,64,202610239999+index)
        np.save(out/'linear_tilt_particle_filter_logweights.npy',score)
        stats['variance_times_sampling_cost_per_path']=stats['empirical_replicate_relative_variance']*stats['total_seconds']/64
        result['methods']['linear_tilt_particle_filter']=stats
    result['criteria']={'K_at_most_5':math.exp(logK)<=5,'five_percent_95pct_within_cap':cap_pass,
                         'anchored_envelope_width_over_1000':result['anchored_probability_envelope']['log_width']>math.log(1000)}
    (out/'results.json').write_text(json.dumps(result,indent=2))
    print('finished '+cfg.name+' '+json.dumps(result['criteria']),flush=True)
    return result


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--check',action='store_true')
    parser.add_argument('--case',choices=['small_confirmation','main_confirmation','scale_confirmation','all'])
    parser.add_argument('--skip-smc',action='store_true')
    args=parser.parse_args()
    (ROOT/'results').mkdir(exist_ok=True)
    freeze=json.loads((ROOT/'CONFIRMATION.json').read_text())
    if args.check:
        r=exact_small_check(); (ROOT/'results'/'root_small_check.json').write_text(json.dumps(r,indent=2)); print(json.dumps(r,indent=2))
    if args.case:
        start=time.perf_counter()
        done=[]
        for i,item in enumerate(freeze['cases']):
            if args.case in ['all',item['name']]:
                done.append(run_case(Config(**item),i,args.skip_smc))
        receipt={'python':platform.python_version(),'numpy':np.__version__,'platform':platform.platform(),
                 'elapsed_seconds':time.perf_counter()-start,'cases':[d['config']['name'] for d in done],
                 'confirmation_sha256':hashlib.sha256((ROOT/'CONFIRMATION.json').read_bytes()).hexdigest(),
                 'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                 'workers':'root process only; NumPy internal execution details unmetered',
                 'branch':'P3, no Ultra allocation'}
        (ROOT/'results'/('run_receipt_'+args.case+'.json')).write_text(json.dumps(receipt,indent=2))


if __name__=='__main__':
    main()
