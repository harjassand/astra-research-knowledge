"""Exact finite isotope-code ambiguity and conditional source-fraction assay.

No actual isotope experiment. Standard mixing inversion is the matched decoder.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import math


def moments(measure):
    return [sum(w*t**k for t,w in measure) for k in range(3)]


def source_fraction_interval(f_interval, native_interval, hip_interval,
                             calibrated_effective_endmembers):
    if not calibrated_effective_endmembers:
        return {'verdict':'UNKNOWN: effective endmembers/fractionation/background not acquired'}
    if hip_interval[0] <= native_interval[1]:
        return {'verdict':'UNKNOWN: source intervals overlap'}
    values = [(f-a)/(b-a) for f,a,b in product(f_interval,native_interval,hip_interval)]
    lo,hi=max(0,min(values)),min(1,max(values))
    if lo>hi:
        return {'verdict':'REJECT_MODEL: no physical two-source mixture'}
    return {'verdict':'CONDITIONAL_RETAINED_SOURCE_FRACTION', 'lower':lo,'upper':hi}


def main():
    # Two nonnegative ingress histories; first two time moments + total agree.
    a=[(F(1,4),F(4,7)),(F(5,6),F(3,7))]
    b=[(F(0),F(1,6)),(F(1,2),F(2,3)),(F(1),F(1,6))]
    assert moments(a)==moments(b)==[F(1),F(1,2),F(1,3)]
    # Physical isotope codes f36=t/3, f38=t^2/3, f40=1-f36-f38.
    def counts(m):
        return [sum(w*t/3 for t,w in m),sum(w*t*t/3 for t,w in m),
                sum(w*(1-t/3-t*t/3) for t,w in m)]
    assert counts(a)==counts(b)
    # Constant-pressure bidirectional exchange: same cumulative exchange,
    # distinct closure cutoffs. N is fixed; marker x=1-exp(-integral lambda).
    exchange_a=1*(2-1)
    exchange_b=.5*(3-1)
    assert exchange_a==exchange_b
    # Favorable source assay demo: endmembers here are synthetic calibrated
    # values, not claimed natural abundance or actual purchased gas specs.
    f0, fh = .0034, .01
    true_fraction=.25
    f=(1-true_fraction)*f0+true_fraction*fh
    interval=source_fraction_interval((f-.00005,f+.00005),
        (f0-.00001,f0+.00001),(fh-.00001,fh+.00001),True)
    assert interval['lower']<=true_fraction<=interval['upper']
    unknown=source_fraction_interval((f,f),(f0,f0),(fh,fh),False)
    assert unknown['verdict'].startswith('UNKNOWN')
    n=100e6*(4*math.pi*(10e-6)**3/3)/(8.314462618*1200)
    result={
        'scope':'exact model witnesses and synthetic calibrated source mixing; no HIP assay',
        'moment_ambiguity':{'common_moments':[str(x) for x in moments(a)],
            'common_isotope_counts':[str(x) for x in counts(a)],
            'last_ingress_A':str(max(t for t,w in a)),
            'last_ingress_B':str(max(t for t,w in b))},
        'exchange_ambiguity':{'same_final_marker_fraction':1-math.exp(-1),
            'cutoff_A':2,'cutoff_B':3,'net_molar_uptake':0},
        'synthetic_source_assay':{'true_retained_HIP_source_fraction':true_fraction,
            'conditional_interval':interval,'uncalibrated_verdict':unknown,
            'strongest_same_data_decoder':'standard isotope mixture inversion; identical answer'},
        'illustrative_ideal_gas_quantity':{'radius_m':10e-6,'P_Pa':100e6,
            'T_K':1200,'total_moles':n,'marker_moles_at_1_percent':n*.01},
        'novelty':'generic isotope-tagged HIP plus MS disclosed in EP3243585A1',
        'physical_validation':False,
    }
    Path(__file__).with_name('isotope_query_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'passed':True,'scope':result['scope'],'interval':interval}))


if __name__=='__main__':
    main()
