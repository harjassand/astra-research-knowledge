"""Reproduce finite-state diagnostics and exact stopping-time counterexample.

No claim of superiority to high-dimensional state-of-the-art samplers.
The same bracket-acquisition step already bounds the target probability.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as F
import json
from pathlib import Path
import platform
import time
import numpy as np
import mpmath as mp
from certified_paths import (
    chemical_excursion, compile_chain, reference_values, proposal_array,
    second_moment_relative, reversed_drift, simulate,
    stopped_two_state_second_moment, verify_compiled,
)


def high_precision_probability(chain,horizon,digits=80):
    with mp.workdps(digits):
        n=chain.size
        p=[mp.mpf(x.numerator)/x.denominator for x in chain.p_up]
        row=[mp.mpf(0)]*n
        row[-1]=mp.mpf(1)
        for _ in range(horizon):
            nxt=[mp.mpf(0)]*n
            nxt[-1]=mp.mpf(1)
            for x in range(1,n-1):
                nxt[x]=p[x]*row[x+1]+(1-p[x])*row[x-1]
            row=nxt
        return mp.nstr(row[chain.start],digits)


def run(volumes,samples):
    rows=[]
    for volume in volumes:
        horizon=2*volume
        chain=chemical_excursion(volume)
        started=time.perf_counter()
        h=reference_values(chain,horizon)
        dp_seconds=time.perf_counter()-started
        precision_started=time.perf_counter()
        p80=high_precision_probability(chain,horizon)
        mp_seconds=time.perf_counter()-precision_started
        p=h[-1,chain.start]
        compiled=compile_chain(chain,horizon,bracket_bits=12)
        verify_start=time.perf_counter()
        verification=verify_compiled(compiled)
        verify_seconds=time.perf_counter()-verify_start
        q=proposal_array(compiled)
        drift=reversed_drift(chain,horizon)
        rv=second_moment_relative(chain,h,q)
        baseline_rv=second_moment_relative(chain,h,drift)
        cert=float(compiled.bound[-1][chain.start])-1
        lo=compiled.lower[-1][chain.start]
        hi=compiled.upper[-1][chain.start]
        midpoint=(lo+hi)/2
        relative_midpoint_bound=float((hi-lo)/(2*lo))
        diag=simulate(chain,horizon,q,samples,20261009+volume)
        drift_diag=simulate(chain,horizon,drift,samples,20262009+volume)
        row={
            'volume':volume,'states':chain.size,'reaction_event_horizon':horizon,
            'probability_float':float(p),'probability_80_digits':p80,
            'lower_rational':str(lo),'upper_rational':str(hi),
            'midpoint_relative_error_bound':relative_midpoint_bound,
            'crude_monte_carlo_relative_variance':float((1-p)/p),
            'reversed_drift_relative_variance':baseline_rv,
            'compiled_relative_variance':rv,
            'certified_relative_variance_upper':cert,
            'root_second_moment_bound_rational':str(compiled.bound[-1][chain.start]),
            'float_dynamic_program_seconds':dp_seconds,
            'mpmath_80_digit_dynamic_program_seconds':mp_seconds,
            'rational_bracket_acquisition_seconds':compiled.acquire_seconds,
            'rational_proposal_certification_seconds':compiled.compile_seconds,
            'compiled_nodes':compiled.processed_nodes,
            'independent_rational_verifier':verification,
            'independent_rational_verifier_seconds':verify_seconds,
            'compiled_monte_carlo':diag,'reversed_drift_monte_carlo':drift_diag,
        }
        rows.append(row)
        print(json.dumps({k:row[k] for k in [
            'volume','probability_float','midpoint_relative_error_bound',
            'crude_monte_carlo_relative_variance',
            'reversed_drift_relative_variance','compiled_relative_variance',
            'certified_relative_variance_upper',
            'rational_bracket_acquisition_seconds',
            'rational_proposal_certification_seconds']},indent=2),flush=True)
    s,d=F(1,100000),F(1,100)
    ratio=(1-s)/(1-d*d)
    return {
        'status':'Research prototype and diagnostic examples, not a transformative invention.',
        'date':'2026-10-09',
        'runtime':{'python':platform.python_version(),'numpy':np.__version__,
                   'mpmath':mp.__version__,'platform':platform.platform()},
        'configuration':{'bracket_bits':12,'certificate_bits':36,
                         'proposal_bits':30,'samples_per_proposal':samples},
        'chemical_diagnostics':rows,
        'counterexample':{
            'description':'Two transient states, approximate normalized Doob transform.',
            'hazard':str(s),'uniform_relative_committor_error':str(d),
            'expected_proposal_steps':str(1/s),
            'second_moment_continuation_ratio':str(ratio),
            'relative_variance':'infinite',
            'threshold':'finite if and only if hazard > relative_error**2',
            'finite_formula':'hazard*(1-relative_error**2)/(hazard-relative_error**2)',
        },
        'critical_resource_finding':(
            'Backward interval acquisition already gives a certified probability '
            'bracket. Its cost is O(horizon*states) arithmetic and remains '
            'exponential for an explicitly enumerated high-dimensional state space. '
            'The compiled sampler has not eliminated that acquisition bottleneck.'),
        'limitations':[
            'Finite reaction-event horizon, not physical-time rate estimation.',
            'Chemical example has a one-dimensional count coordinate.',
            'No neural committor, high-dimensional molecule, or learned-model training run.',
            'Timing measurements are single process runs, not controlled performance benchmarks.',
            'Certificate arithmetic is exact rational with outward rounding; diagnostic paths use floats.',
            'General theorem has a written proof and finite tests, not a proof-assistant formalization.',
        ],
    }


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--volumes',type=int,nargs='+',default=[40,80,160])
    parser.add_argument('--samples',type=int,default=20000)
    parser.add_argument('--output',type=Path,default=Path('results.json'))
    args=parser.parse_args()
    if args.samples<2:
        parser.error('--samples must be at least 2')
    results=run(args.volumes,args.samples)
    args.output.write_text(json.dumps(results,indent=2)+'\n')
