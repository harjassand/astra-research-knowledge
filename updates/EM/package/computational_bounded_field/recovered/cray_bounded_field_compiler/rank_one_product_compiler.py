#!/usr/bin/env python3
"""Non-exhaustive rank-one product-base bounded-field mixture prototype.

The target is exp(K (a.x)^2/2 + h.x), x in {-1,+1}^n.  This program
compiles the field arrangement incrementally and never enumerates spin
states (except the separate n<=10 partition check in the demo).

It uses hybrid Gaussian interval weights (SciPy for moderate standardized
endpoints, mpmath for extreme tails), not certified interval arithmetic. Thus the mathematical error theorem is NOT an end-to-end
numerical certificate for this implementation.
"""
from __future__ import annotations
import argparse
import bisect
import itertools
import json
import math
import random
import time
from dataclasses import dataclass
from fractions import Fraction as F
from pathlib import Path

import mpmath as mp
from scipy.special import log_ndtr
from verify_compiler import to_mp, mp_logsum, log_normal_interval
from verify_discrete_mixture import ceil_log2_rational


def hybrid_log_interval(a: mp.mpf, b: mp.mpf) -> mp.mpf:
    """Uncertified accelerated log mass, with high-precision fallback.

    This is intentionally not asserted to satisfy a uniform input-bit error
    contract. It is a diagnostic implementation, not the theorem's engine.
    """
    fa,fb=float(a),float(b)
    if ((not math.isfinite(fa) or abs(fa)<100) and
        (not math.isfinite(fb) or abs(fb)<100) and fb-fa>1e-6):
        if fa>=0:
            top=float(log_ndtr(-fa)); bottom=float(log_ndtr(-fb))
        elif fb<=0:
            top=float(log_ndtr(fb)); bottom=float(log_ndtr(fa))
        else:
            mass=(math.erf(fb/math.sqrt(2))-math.erf(fa/math.sqrt(2)))/2
            if mass>0: return mp.mpf(math.log(mass))
            return log_normal_interval(a,b)
        correction=-math.expm1(bottom-top)
        if correction>0: return mp.mpf(top+math.log(correction))
    return log_normal_interval(a,b)


@dataclass
class Component:
    left: F | None
    right: F | None
    log_weight: mp.mpf
    log_base_partition: mp.mpf
    phase_field: F


class ProductCompiler:
    def __init__(self, a: list[F], h: list[F], variance: F, epsilon: F, seed: int = 12):
        if not a or len(a)!=len(h) or any(ai==0 for ai in a):
            raise ValueError('Equal nonempty input lengths and nonzero pattern coordinates required')
        if variance<=0 or not 0<epsilon<F(1,2):
            raise ValueError('Require variance>0 and 0<epsilon<1/2')
        self.a=a; self.h=h; self.n=len(a); self.variance=variance; self.eps=epsilon
        self.rng=random.Random(seed)
        # rho <= epsilon/4, b <= epsilon/8, so ideal TV <= epsilon/2.
        self.L=math.ceil(ceil_log2_rational(F(4*self.n)/epsilon)/2)
        self.N=math.ceil(F(8*self.n*self.L)/epsilon)
        self.step=F(2*self.L,self.N)
        self.signs=[1 if ai>0 else -1 for ai in a]
        self.components: list[Component]=[]
        self._compile()

    def _compile(self):
        n,L,N,step=self.n,self.L,self.N,self.step
        events=sorted(((F(-L)+j*step-hi)/ai,i,j) for i,(ai,hi) in enumerate(zip(self.a,self.h)) for j in range(N+1))
        values=[F(-L)+(F(j)+F(1,2))*step for j in range(N)]
        logs=[mp.log(2*mp.cosh(to_mp(c))) for c in values]
        sat_log=mp.log(2*mp.cosh(L))
        c=[F(-s*L) for s in self.signs]
        base_log=n*sat_log
        phase=sum(ci*si for ci,si in zip(c,self.signs))
        d=-sum(abs(ai) for ai in self.a)
        e=sum(-si*hi-L for si,hi in zip(self.signs,self.h))
        k=to_mp(self.variance); sqrtk=mp.sqrt(k); log_norm=mp.log(2*mp.pi*k)/2
        left=None

        def append_cell(right):
            dm=to_mp(d); mean=k*dm
            lo=-mp.inf if left is None else (to_mp(left)-mean)/sqrtk
            hi=mp.inf if right is None else (to_mp(right)-mean)/sqrtk
            lg=to_mp(e)+k*dm*dm/2+log_norm+hybrid_log_interval(lo,hi)
            self.components.append(Component(left,right,base_log+lg,base_log,phase))

        for right, group in itertools.groupby(events,key=lambda event:event[0]):
            append_cell(right)
            for _,i,j in group:
                ai,hi,sg=self.a[i],self.h[i],self.signs[i]
                old=c[i]
                oldlog=sat_log if abs(old)==L else logs[int((old+L)/step-F(1,2))]
                if sg>0:
                    if j==0:
                        new=values[0]; d+=ai; e+=hi+L
                    elif j==N:
                        new=F(L); d+=ai; e+=hi-L
                    else:
                        new=values[j]
                else:
                    if j==N:
                        new=values[N-1]; d-=ai; e+=-hi+L
                    elif j==0:
                        new=F(-L); d-=ai; e+=-hi-L
                    else:
                        new=values[j-1]
                newlog=sat_log if abs(new)==L else logs[int((new+L)/step-F(1,2))]
                base_log+=newlog-oldlog
                phase+=(new-old)*sg
                c[i]=new
            left=right
        append_cell(None)
        self.log_q=mp_logsum([c.log_weight for c in self.components])
        self.log_z_estimate=self.log_q-log_norm
        self.cumulative=[]; total=mp.mpf(0)
        for comp in self.components:
            total+=mp.exp(comp.log_weight-self.log_q)
            self.cumulative.append(total)
        if abs(total-1)>mp.mpf('1e-40'):
            raise ArithmeticError('Categorical normalization precision check failed')
        self.cumulative[-1]=mp.mpf(1)
        self._audit_components()

    def _audit_components(self):
        # Independent reconstruction of selected fields checks incremental updates.
        chosen={0,len(self.components)-1}
        chosen.update(self.rng.randrange(len(self.components)) for _ in range(32))
        for i in chosen:
            cs=self.fields(i)
            direct=mp.fsum(mp.log(2*mp.cosh(to_mp(ci))) for ci in cs)
            if abs(direct-self.components[i].log_base_partition)>mp.mpf('1e-40'):
                raise ArithmeticError('Incremental partition update failed')
            assert sum(ci*si for ci,si in zip(cs,self.signs))==self.components[i].phase_field

    def fields(self,index: int)->list[F]:
        comp=self.components[index]
        y=comp.right-1 if comp.left is None else (comp.left+1 if comp.right is None else (comp.left+comp.right)/2)
        out=[]
        for ai,hi in zip(self.a,self.h):
            ell=hi+ai*y
            if ell>=self.L: out.append(F(self.L))
            elif ell<=-self.L: out.append(F(-self.L))
            else:
                j=(ell+self.L)//self.step
                out.append(F(-self.L)+(F(j)+F(1,2))*self.step)
        return out

    def _uniform(self)->mp.mpf:
        return mp.mpf(self.rng.getrandbits(256))/mp.mpf(2)**256

    def draw(self)->list[int]:
        i=bisect.bisect_right(self.cumulative,self._uniform())
        return [1 if self._uniform()<1/(1+mp.exp(-2*to_mp(ci))) else -1 for ci in self.fields(i)]

    def ideal_error_bound(self)->mp.mpf:
        b=to_mp(F(self.n)*self.step/2)
        rho=self.n*mp.exp(-2*self.L)
        return 1-(1-rho)*mp.exp(-2*b)

    def check_small_partition(self)->mp.mpf:
        if self.n>10: raise ValueError('Small-system check limited to 10 spins')
        terms=[]
        for x in itertools.product((-1,1),repeat=self.n):
            projection=sum(ai*xi for ai,xi in zip(self.a,x))
            terms.append(to_mp(self.variance*projection*projection/2+sum(hi*xi for hi,xi in zip(self.h,x))))
        exact=mp_logsum(terms)
        error=self.log_z_estimate-exact
        b=to_mp(F(self.n)*self.step/2); rho=self.n*mp.exp(-2*self.L)
        assert abs(error)<=b-mp.log(1-rho)+mp.mpf('1e-35')
        return error

    def two_phase_diagnostic(self)->dict:
        plus=mp.exp(mp_logsum([c.log_weight+to_mp(c.phase_field)-c.log_base_partition for c in self.components])-self.log_q)
        minus=mp.exp(mp_logsum([c.log_weight-to_mp(c.phase_field)-c.log_base_partition for c in self.components])-self.log_q)
        field=to_mp(sum(hi*si for hi,si in zip(self.h,self.signs)))
        target_plus=1/(1+mp.exp(-2*field)); target_minus=1-target_plus
        tv=(abs(plus-target_plus)+abs(minus-target_minus)+1-plus-minus)/2
        amin=min(abs(ai) for ai in self.a); total=sum(abs(ai) for ai in self.a)
        tail_log=to_mp(-2*self.variance*amin*(total-amin)+2*sum(abs(hi) for hi in self.h))+self.n*mp.log(2)
        return {'mixture_TV_to_two_ground_phases':mp.nstr(tv,24),
                'target_non_ground_mass_log_upper_bound':mp.nstr(tail_log,24),
                'note':'Useful only when the displayed log upper bound is negative; floating values are not interval-certified.'}


def demo(output:Path):
    mp.mp.dps=90
    rows=[]
    for n,k in [(8,F(1,8)),(20,F(1,20)),(20,F(2**60))]:
        a=[F(((-1)**i)*(i+3),i+2) for i in range(n)]
        h=[F(((7*i+3)%13)-6,17) for i in range(n)]
        t=time.perf_counter(); compiler=ProductCompiler(a,h,k,F(1,4),seed=20261012)
        prep=time.perf_counter()-t
        t=time.perf_counter(); samples=[compiler.draw() for _ in range(256)]; draw_time=time.perf_counter()-t
        row={'n':n,'variance_rational':str(k),'cells':len(compiler.components),
             'epsilon_rational':'1/4','L':compiler.L,'outer_arithmetic_decimal_digits':90,'gaussian_interval_engine':'SciPy double for moderate endpoints; mpmath for extreme tails',
             'ideal_TV_bound_not_numerically_certified':mp.nstr(compiler.ideal_error_bound(),20),
             'estimated_log_Z':mp.nstr(compiler.log_z_estimate,30),
             'preprocessing_seconds':prep,'draws':256,'drawing_seconds':draw_time,
             'first_five_samples':samples[:5]}
        if n<=10: row['exact_small_partition_signed_log_error']=mp.nstr(compiler.check_small_partition(),24)
        if k>100: row['two_phase_check']=compiler.two_phase_diagnostic()
        rows.append(row)
    result={'status':'non_exhaustive_rank_one_product_base_prototype_not_certified_general_compiler',
            'cases':rows,
            'limitations':['No spin enumeration during compilation or sampling; only the separate 8-spin check enumerates.',
                           'This executable supports rank one and J0=0, not a correlated residual or general rank.',
                           'Hybrid double/mpmath interval masses have no certified uniform error bound.',
                           'Timings are single-run descriptive measurements, not matched competitive benchmarks.']}
    output.write_text(json.dumps(result,indent=2)+'\n'); print(json.dumps(result,indent=2))

if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('--output',type=Path,default=Path('product_prototype_results.json'))
    demo(parser.parse_args().output)
