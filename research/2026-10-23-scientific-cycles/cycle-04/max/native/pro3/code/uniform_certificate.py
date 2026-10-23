#!/usr/bin/env python3
"""Vanishing-screen finite bounds; deterministic calculations, not sampler runs.

Uses only Python's standard-library Decimal. No data files, network, target
normalizer or random seed.
Uses log horizon x and n=ceil(exp(x)); all formula relaxations are documented
in NUMERICS.md. Decimal outputs are rounded, not outward interval arithmetic.
"""
import argparse
import hashlib
import json
import platform
import time
from datetime import datetime, timezone
from pathlib import Path
from decimal import Decimal, getcontext, MAX_EMAX, MIN_EMIN


class DecimalMath:
    """Tiny named adapter so every transcendental uses the same Decimal context."""
    mpf=Decimal
    __version__='stdlib Decimal'
    @staticmethod
    def log(x): return Decimal(x).ln()
    @staticmethod
    def log1p(x): return (Decimal(1)+Decimal(x)).ln()
    @staticmethod
    def exp(x): return Decimal(x).exp()
    @staticmethod
    def sqrt(x): return Decimal(x).sqrt()
    @staticmethod
    def nstr(x,n): return format(x,f'.{n}g')
    @property
    def dps(self): return getcontext().prec
    @dps.setter
    def dps(self,value):
        getcontext().prec=value
        getcontext().Emax=MAX_EMAX
        getcontext().Emin=MIN_EMIN
    @property
    def mp(self): return self


mp=DecimalMath()


def constants(K, alpha, h, endpoint_fraction):
    beta = 1-alpha
    H = -h*mp.log(h)-(1-h)*mp.log1p(-h)
    delta = mp.exp(-(K+H)/(1-h))
    rho_h = 1-alpha*delta/2
    kappa = -mp.log(rho_h)
    rho_g = 1+beta/2
    a_star = kappa/(kappa+mp.log(rho_g))
    a = endpoint_fraction*a_star
    series_ratio = rho_g**a*rho_h**(1-a)
    assert 0 < series_ratio < 1
    S = 1+beta**(-a)*rho_g**a/(1-series_ratio)
    kappa0 = -mp.log1p(-alpha*mp.exp(-K)/2)
    Lstar = 1+mp.log(rho_g)/kappa0
    return dict(K=K, alpha=alpha, beta=beta, h=h,
                delta_h=delta, rho_h=rho_h, kappa_h=kappa,
                rho_g=rho_g, a_star=a_star, a=a, S=S,
                series_ratio=series_ratio, Lambda_star=Lstar,
                M=mp.exp(2*K+1))


def hybrid(c, x, eta):
    """Valid theorem bound at ceil(exp(x)), with safe survival relaxation."""
    x, eta = mp.mpf(x), mp.mpf(eta)
    assert x >= 16 and 0 < eta <= 1
    logR = x-4*mp.log(x)
    if logR <= 1:
        return None
    tail = min(mp.mpf(1), c['K']/(logR-1))
    theta = c['a']*min(eta, mp.mpf('0.5'))
    # N=floor(n/2) >= (exp(x)-2)/2 >= (x^2-2)/2 for x>=16.
    survival = mp.exp(-c['kappa_h']*(x*x-2)/2)
    high = c['S']*mp.exp(theta*(mp.log(tail)-logR))
    core = c['S']*mp.exp(theta*(mp.log(c['M']/c['h']+1)
                                      +mp.log(2/c['alpha'])-x))
    pi_core = mp.sqrt(2/c['alpha']*(c['M']*mp.exp(-x)+x**(-4)))
    parts = dict(high_target_tail=tail, late_first_hit=survival,
                 initial_high_transport=high, initial_core_transport=core,
                 stationary_core=pi_core)
    total = sum(parts.values())
    return dict(log_horizon=x, eta=eta, theta=theta, log_R=logR,
                parts=parts, raw_bound=total, bound=min(mp.mpf(1),total),
                log_scaled_raw_bound=x*total)


def pure(K, x):
    """q-start ordinary nonlazy IMH; see the coupling proof in NUMERICS.md."""
    x = mp.mpf(x)
    logR = x-2*mp.log(x)
    if logR <= 1:
        return None
    tail = min(mp.mpf(1),K/(logR-1))
    if tail >= 1:
        return None
    pi_tail = tail
    q_tail = tail*mp.exp(-logR)
    coupling = mp.exp(-(1-tail)*x*x)
    total = pi_tail+q_tail+coupling
    return dict(log_horizon=x, log_R=logR,
                parts=dict(pi_tail=pi_tail,q_tail=q_tail,coupling=coupling),
                raw_bound=total,bound=min(mp.mpf(1),total))


def certificate_search(fun, eps, counters):
    """Integer x search on a monotone sufficient bound, 5 percent margin."""
    def accepted(x):
        counters['certificate_evaluations'] += 1
        result=fun(x)
        return result, result is not None and result['raw_bound'] <= mp.mpf('.95')*eps
    lo,hi=15,16
    record,ok=accepted(hi)
    while not ok:
        lo,hi=hi,2*hi
        if hi > 2**32:
            return dict(status='no_bracket_below_2^32',last_log_horizon=hi)
        record,ok=accepted(hi)
    while hi-lo>1:
        mid=(hi+lo)//2
        record,ok=accepted(mid)
        if ok: hi=mid
        else: lo=mid
    record,ok=accepted(hi)
    previous,previous_ok=accepted(hi-1)
    assert ok and not previous_ok
    return dict(status='certificate_found', integer_log_horizon=hi,
                epsilon_log_horizon=eps*hi, result=record,
                previous_integer_passes=previous_ok,
                actual_step_count='ceil(exp(integer_log_horizon))')


def path_constant(K,alpha):
    beta=1-alpha
    d=2*alpha*mp.exp(-K)/beta
    if d>=1:
        return dict(d_limit=d,r_star=mp.mpf(1),necessary_multiplier=mp.mpf(1),
                    optimizer='v tends to infinity; single trap suffices')
    # Solve log(d)=log(r)+(1-r)/r log(1-r), monotonically in r.
    lo,hi=mp.mpf(0),mp.mpf(1)
    for _ in range(4*mp.mp.dps):
        r=(lo+hi)/2
        residual=mp.log(r)+(1-r)/r*mp.log1p(-r)-mp.log(d)
        if residual>0: hi=r
        else: lo=r
    r=(lo+hi)/2
    v=-mp.log1p(-r)/r
    phi=mp.log1p(d*mp.exp(v))/v
    return dict(d_limit=d,r_star=r,necessary_multiplier=1/r,
                optimizer_v=v,phi_at_optimizer=phi,
                identity_absolute_error=abs(phi-r))


def serial(value):
    if isinstance(value,mp.mpf): return mp.nstr(value,50)
    if isinstance(value,dict): return {k:serial(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)): return [serial(v) for v in value]
    return value


def run(dps):
    started=datetime.now(timezone.utc).isoformat()
    tick=time.perf_counter()
    mp.mp.dps=dps
    c=constants(mp.mpf(1),mp.mpf('.5'),mp.mpf('.01'),mp.mpf('.95'))
    counters={'certificate_evaluations':0,'horizon_rows':0,'policy_rows':0}
    horizon=[]
    for x in (100,1000,10000,100000,1000000):
        horizon.append(dict(schedule='fixed_eta_0.5',result=hybrid(c,x,mp.mpf('.5'))))
        counters['horizon_rows']+=1
        for lam in ('.5','1','2','4','8'):
            eta=min(mp.mpf(1),mp.mpf(lam)*mp.log(x)/x)
            horizon.append(dict(schedule='lambda_loglogn_over_logn',lambda_value=mp.mpf(lam),
                                result=hybrid(c,x,eta)))
            counters['horizon_rows']+=1
    policies=[]
    for eps_s in ('.05','.02','.01','.005','.002','.001'):
        eps=mp.mpf(eps_s)
        pure_result=certificate_search(lambda x:pure(c['K'],x),eps,counters)
        for d_s in ('.25','1','4','16'):
            d=mp.mpf(d_s)
            eta=min(mp.mpf(1),d*eps*mp.log(1/eps))
            hybrid_result=certificate_search(lambda x:hybrid(c,x,eta),eps,counters)
            policies.append(dict(epsilon=eps,d=d,eta=eta,hybrid=hybrid_result,
                                 ordinary_pure_imh=pure_result))
            counters['policy_rows']+=1
    path_result=path_constant(c['K'],c['alpha'])
    return serial(dict(started_utc=started,finished_utc=datetime.now(timezone.utc).isoformat(),
        wall_seconds=time.perf_counter()-tick,dps=dps,python=platform.python_version(),
        arithmetic_backend=mp.__version__, source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        numerical_contract='Rounded high precision; theorem is exact, numeric outputs are not interval proofs.',
        constants=c,path_constant=path_result,
        horizon_grid=horizon,accuracy_policies=policies,observed_counts=counters))


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--dps',type=int,default=80)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    result=run(args.dps)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('wall_seconds','dps','observed_counts','path_constant')},indent=2))
