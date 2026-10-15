#!/usr/bin/env python3
"""Conditional two-endpoint dislocation transport model.

All examples are dimensionless. There are NO measured ZnS endpoint mobilities
in this file. Numerical checks do not validate a material or establish novelty.
Run: python check_model.py
Requires only Python's standard library; writes model_results.json alongside it.
"""
from __future__ import annotations
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

@dataclass(frozen=True)
class Mobility:
    charged: float
    neutral: float

    def __post_init__(self) -> None:
        if not all(math.isfinite(v) and v >= 0 for v in (self.charged, self.neutral)):
            raise ValueError('Mobilities must be finite and nonnegative.')
        if self.charged + self.neutral <= 0:
            raise ValueError('At least one endpoint must be mobile.')

    @property
    def asymmetry(self) -> float:
        return (self.neutral-self.charged)/(2*(self.neutral+self.charged))


def drift(span_excursion: float, expansion: Mobility, contraction: Mobility) -> float:
    if not math.isfinite(span_excursion) or span_excursion <= 0:
        raise ValueError('Span excursion must be finite and positive.')
    return span_excursion*(expansion.asymmetry-contraction.asymmetry)


def integrate_endpoints(m: Mobility, x_c: float, x_n: float, delta_span: float,
                        steps: int=10000) -> tuple[float, float, float]:
    """Independent forward-Euler integration with constant signed force +/-1.

    Time is chosen to reach the prescribed span change in this constant-
    mobility model. Third output is positive glide dissipation, not full cost.
    """
    if steps < 1 or delta_span == 0:
        raise ValueError('Positive step count and nonzero span change required.')
    force = math.copysign(1.0, delta_span)
    duration = abs(delta_span)/(m.charged+m.neutral)
    dt = duration/steps
    dissipated = 0.0
    for _ in range(steps):
        x_c += -m.charged*force*dt
        x_n += m.neutral*force*dt
        dissipated += force**2*(m.charged+m.neutral)*dt
    return x_c, x_n, dissipated


def simpson(f: Callable[[float], float], lo: float, hi: float, n: int=20000) -> float:
    if n <= 0 or n % 2:
        raise ValueError('Simpson panel count must be positive and even.')
    dx=(hi-lo)/n
    return dx/3*(f(lo)+f(hi)+4*sum(f(lo+(2*i-1)*dx) for i in range(1,n//2+1))
                 +2*sum(f(lo+2*i*dx) for i in range(1,n//2)))


def main() -> None:
    d=Mobility(10,1)
    l=Mobility(0.1,1)
    expected=drift(1,d,l)
    c0,n0=0.,4.
    c1,n1,w1=integrate_endpoints(d,c0,n0,1)
    c2,n2,w2=integrate_endpoints(l,c1,n1,-1)
    simulated=(c2+n2-c0-n0)/2
    assert abs(expected+9/11)<1e-14
    assert abs(simulated-expected)<1e-10
    assert abs((n2-c2)-(n0-c0))<1e-10
    assert drift(1,d,d)==0
    assert abs(drift(1,d,Mobility(100,10)))<1e-14
    assert drift(1,Mobility(10,0),Mobility(.1,0))==0
    assert abs(drift(1,l,d)+expected)<1e-14
    assert w1+w2>0

    bounds=[]
    for r in (1,2,10,100,10000):
        c_low=1.
        c_high=float(r)
        best_n=math.sqrt(c_low*c_high)
        bound=(math.sqrt(r)-1)/(math.sqrt(r)+1)
        attained=abs(drift(1,Mobility(c_high,best_n),Mobility(c_low,best_n)))
        grid_n=[10**(-6+12*k/4000) for k in range(4001)]
        grid_max=max(abs(drift(1,Mobility(c_high,x),Mobility(c_low,x))) for x in grid_n)
        assert abs(bound-attained)<1e-12
        assert grid_max<=bound+1e-12
        bounds.append(dict(charged_mobility_ratio=r, optimal_neutral_mobility=best_n,
                           sharp_drift_per_span_bound=bound, grid_max=grid_max))

    # Span-dependent response example; geometric integral, not a physical fit.
    md=lambda x: Mobility(2+x,1+0.2*x)
    ml=lambda x: Mobility(.2+.1*x,1+.2*x)
    geometric=simpson(lambda x: md(x).asymmetry-ml(x).asymmetry,4,5)
    dc_d=simpson(lambda x: -md(x).charged/(md(x).charged+md(x).neutral),4,5)
    dn_d=simpson(lambda x: md(x).neutral/(md(x).charged+md(x).neutral),4,5)
    dc_l=simpson(lambda x: -ml(x).charged/(ml(x).charged+ml(x).neutral),5,4)
    dn_l=simpson(lambda x: ml(x).neutral/(ml(x).charged+ml(x).neutral),5,4)
    independent=(dc_d+dn_d+dc_l+dn_l)/2
    assert abs(independent-geometric)<1e-10
    assert abs((dn_d+dn_l)-(dc_d+dc_l))<1e-10

    result=dict(status='conditional_model_checks_passed_not_material_validation',
                units='dimensionless; no material-derived mobilities or force scale',
                evidence_not_acquired=['same-loop endpoint mobility ratio switching',
                   'safe reverse glide', 'charge-state reset', 'retained device benefit',
                   'full energy cost', 'historical novelty'],
                example=dict(expansion=dict(charged=10,neutral=1),
                             contraction=dict(charged=.1,neutral=1),
                             span_excursion=1, initial_span=4, analytic_drift=expected,
                             integrated_drift=simulated, final_span=n2-c2,
                             reduced_model_dissipation=w1+w2),
                null_checks=['fixed optical mode gives zero closed-span drift',
                             'common mobility rescaling gives zero drift',
                             'permanently pinned neutral endpoint gives zero drift',
                             'interchanging expansion and contraction modes reverses drift'],
                sharp_bound= bounds,
                span_dependent_example=dict(geometric_drift=geometric,
                                            endpoint_integral_drift=independent))
    out=Path(__file__).with_name('model_results.json')
    out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))

if __name__=='__main__':
    main()
