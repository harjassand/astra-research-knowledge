"""Actual uniform-chain purity bracket from acquired warmZ and a block GT trace.

It is much wider than the bootstrap rung tolerance and must not be marked
as acquiring that rung. No ansatz residual is needed for this separate bound.
"""
import sys
sys.dont_write_bytecode=True
import json,math,time
from fractions import Fraction as Q
import mpmath as mp
from block_purity_readout import (BASE,local_positive_exponential,transfers,
                                 trace_power_interval,upward,gamma)


def iv_fraction(q):
    return mp.iv.mpf(q.numerator)/q.denominator


def run():
    start=time.monotonic();mp.iv.dps=100;iv=mp.iv
    warm=json.loads((BASE/'sources/ACCEPTED_WARM_LOGZ.json').read_text())
    beta=1.5;G,tg,rg=local_positive_exponential(4,beta);F,tf,rf=local_positive_exponential(2,beta)
    T1,_=transfers(G,F);theta=upward((1+tg)*(1+tf)*(1+gamma(4000))-1)
    Ghalf,tghalf,rghalf=local_positive_exponential(4,.75)
    Fhalf,tfhalf,rfhalf=local_positive_exponential(2,.75)
    _,T2half=transfers(Ghalf,Fhalf)
    theta2=upward((1+tghalf)**2*(1+tfhalf)**2*(1+gamma(4000))-1)
    rows=[]
    for n in (256,512):
        m=n//4;lo,hi=trace_power_interval(T1,m,theta)
        scale=m*(rg['normalizing_binary_exponent']+rf['normalizing_binary_exponent'])
        gt_lower=iv.log(iv_fraction(lo))+scale*iv.log(2)-4*n*iv.mpf(3)/2
        gt_upper=iv.log(iv_fraction(hi))+scale*iv.log(2)-4*n*iv.mpf(3)/2
        alo,ahi=trace_power_interval(T2half,m,theta2)
        ascale=2*m*(rghalf['normalizing_binary_exponent']+rfhalf['normalizing_binary_exponent'])
        alt_upper=iv.log(iv_fraction(ahi))+ascale*iv.log(2)-8*n*iv.mpf(3)/4
        r05=next(x for x in warm['rows']if x['n']==n and x['beta']=='0.5')
        r075=next(x for x in warm['rows']if x['n']==n and x['beta']=='0.75')
        # Source endpoints are outward binary64 endpoints. Preserve their
        # exact binary values before interval operations.
        g05_upper=iv_fraction(Q.from_float(r05['log_normalized_Z_upper']))+n*iv.log(5)
        g075_lower=iv_fraction(Q.from_float(r075['log_normalized_Z_lower']))+n*iv.log(5)
        lower=2*g075_lower-3*g05_upper
        numerator_upper=alt_upper if alt_upper.b<gt_upper.b else gt_upper
        upper=numerator_upper-2*g075_lower
        loglo=math.nextafter(float(lower.a),-math.inf)
        loghi=math.nextafter(float(upper.b),math.inf)
        assert loglo<loghi<0
        row=dict(n=n,beta=.75,true_uniform_log_purity_lower=loglo,
            true_uniform_log_purity_upper=loghi,
            actual_beta1_5_logZ_GT_upper=math.nextafter(float(gt_upper.b),math.inf),
            actual_beta1_5_logZ_ALT2_upper=math.nextafter(float(alt_upper.b),math.inf),
            log_bracket_width=math.nextafter(loghi-loglo,math.inf),
            required_log_error=7.440476190476189e-7,
            rung_precision_acquired=False,
            numerator_upper_uses_only='Araki-Lieb-Thirring/Trotter2 with actual entangled4site blocks and actual seam bonds; GT1 is retained as the weaker comparison',
            lower_uses_only='ConvexitylogZ: logZ(1.5)>=4logZ(.75)-3logZ(.5)')
        rows.append(row);print(json.dumps(row,indent=2),flush=True)
    result=dict(status='ACTUAL_COLD_RUNG_BROAD_PURITY_BRACKET_NOT_REQUIRED_PRECISION',
        rows=rows,elapsed_seconds=time.monotonic()-start,
        conditions='Accepted warm source enclosures plus the explicitly bounded positive-arithmetic block trace. No small collar residual, gap, physical PSD product frame, or local-purity oracle is assumed.',
        scope='True uniform spin2 finite rings, all sectors and all periodic transfer modes. These wide intervals do not acquire either first-pair input for the dyadic lift.')
    (BASE/'results/COARSE_TRUE_PURITY.json').write_text(json.dumps(result,indent=2)+'\n')
    return result


if __name__=='__main__':run()
