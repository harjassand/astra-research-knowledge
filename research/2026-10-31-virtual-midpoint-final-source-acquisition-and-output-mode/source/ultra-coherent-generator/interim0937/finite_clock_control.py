#!/usr/bin/env python3
"""Finite rotating-reset witnesses for the order-only bandwidth obstruction.

Exact kernels and analytic physical-correlation bounds, with no acquired
trajectories. Large countermodel resources are reported without allocation.
"""
from fractions import Fraction as Q
from pathlib import Path
import json
import time

from aliasfree import ceil_sqrt,log_bounds

HERE=Path(__file__).resolve().parent


def compact_upper(x,bits=96):
    scale=2**bits;z=x*scale
    return Q(-((-z.numerator)//z.denominator),scale)


def inspection_row(M,a,nu=Q(1),gamma=Q(1)):
    ratio=a/(nu+gamma+a);mass=nu/(nu+gamma+a)/(1-ratio**M)
    row=[];power=Q(1)
    for j in range(M):
        row.append(gamma/(nu+gamma)/M+mass*power);power*=ratio
    assert sum(row)==1 and min(row)>0
    # Check the entire resolvent equation using circular orientation.
    for j in range(M):
        assert (nu+gamma+a)*row[j]-a*row[(j-1)%M]-gamma/M==nu*Q(j==0)
    return row


def finite_case(n,M,t=Q(1),nu=Q(1),gamma=Q(1)):
    assert M%2==0 and M>=256*(n+Q(1,2))
    out=[]
    for offset in (Q(0),Q(1,2)):
        a=(n+offset)*M/t;row=inspection_row(M,a,nu,gamma)
        tv=sum(abs(x-Q(1,M)) for x in row)/2;bound=nu*M/(4*a)
        assert tv<=bound
        rotation_error=4*ceil_sqrt(Q(n+offset,M),96)
        assert rotation_error<=Q(1,4)
        # e^-gamma t is enclosed through the existing exact exponential
        # helper; it is not estimated from any synthetic labels.
        from entropy_cone import exponential_bounds
        exp_lo,exp_hi=exponential_bounds(-gamma*t,100)
        magnitude_lower=exp_lo*(1-rotation_error)
        entropylo=a*log_bounds(1+a*M/gamma,120)[0]
        out.append({'offset_half_cycles':str(offset),'hidden_states':M,'rotation_rate':str(a),
                    'escape_rate':str(a+gamma*(1-Q(1,M))),
                    'physical_correlation_sign':1 if offset==0 else -1,
                    'physical_correlation_magnitude_lower':float(magnitude_lower),
                    'ordered_inspection_row_TV_to_uniform':float(tv),
                    'proved_uniform_row_TV_bound':str(bound),
                    'entropy_rate_lower_preview':float(entropylo),
                    'exact_resolvent_equations_checked':M})
    return out


def large_budget_countermodel(N=1000,eta=Q(1,100),nu=Q(1),t=Q(1)):
    needed=Q(N)*nu*t/(2*eta);n=-((-needed.numerator)//needed.denominator)
    lower=128*(n+Q(1,2));M=2*(-((-lower.numerator)//lower.denominator))
    assert M>=256*(n+Q(1,2))
    a=Q(n*M)/t
    return {'total_inspection_intervals':N,'desired_pair_record_TV_upper':str(eta),
            'n':n,'hidden_states_each':M,'smallest_rotation_rate':str(a),
            'pair_record_TV_upper':str(Q(N)*nu*t/(2*n)),
            'physical_target_time':str(t),'reset_rate':'1',
            'physical_correlation_gap_lower':'(3/2)exp(-1)',
            'models_instantiated_or_sampled':False,
            'scope':'explicit finite parameter witness; no memory or hidden states were allocated at this large size'}


def main():
    start=time.perf_counter();out={'scope':__doc__,'finite_controls':finite_case(1,384)+finite_case(2,640),
        'resource_charged_countermodel_for_1000_intervals':large_budget_countermodel(),
        'new_record_acquisitions':0,'status':'FINITE_CLOCK_BANDWIDTH_CONTROLS_PASSED',
        'seconds':time.perf_counter()-start,
        'scope_limit':'ordered labels and known Poisson rate only; no claim against timestamped or controlled-delay observations'}
    (HERE/'clock_receipt.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__=='__main__':main()
