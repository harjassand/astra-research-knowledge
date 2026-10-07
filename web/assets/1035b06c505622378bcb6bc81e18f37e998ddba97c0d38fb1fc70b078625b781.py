"""Bounded additional diagnostics for revision03; no external dependencies.

Exact/rational table checks and floating noncommuting matrix fixtures remain
separate. Neither certifies the full analytic theorems or their priority.
"""
from fractions import Fraction as F
from pathlib import Path
from decimal import Decimal, localcontext
import json
import math
import time

import entropy_table_certificate as cert
import matrix_contrast_checks as mat


def xlog_trace(a):
    return sum(x*math.log(x) if x>0 else 0. for x in mat.eigen(a))


def rootm_psd(a):
    # This admits PSD fixtures (including rank one), unlike a matrix-log oracle.
    d = math.sqrt(max(0.,mat.det(a)))
    denominator = math.sqrt(mat.tr(a)+2*d)
    if denominator == 0:
        return [[0.,0.],[0.,0.]]
    return mat.add(a,mat.I,1/denominator,d/denominator)


def main():
    start = time.perf_counter()
    examples = [
        ([[1.,0.],[0.,4.]],[[2.5,1.5],[1.5,2.5]]),
        ([[0.,0.],[0.,2.]],[[1.,1.],[1.,1.]]),
        ([[.2,.1],[.1,2.]],[[1.5,-.4],[-.4,.8]]),
    ]
    matrix_results = []
    for a0,a1 in examples:
        r0,r1 = rootm_psd(a0),rootm_psd(a1)
        s = mat.add(r0,r1,.5,.5)
        mean_a = mat.add(a0,a1,.5,.5)
        entropy = (xlog_trace(a0)+xlog_trace(a1))/2-xlog_trace(mean_a)
        variance = (mat.norm2(mat.add(r0,s,1,-1))+mat.norm2(mat.add(r1,s,1,-1)))/2
        r = math.sqrt(max(mat.eigen(a0)[1],mat.eigen(a1)[1]))
        lo = mat.eigen(s)[0]
        assert lo > 0
        ratio = r/lo
        b = (2*ratio*ratio*math.log(ratio)-ratio*ratio+1)/(ratio-1)**2
        reference = mat.mul(s,s)
        log_reference = mat.logm(reference)
        avg_divergence = sum(xlog_trace(a)-mat.tr(mat.mul(a,log_reference))-mat.tr(a)+mat.tr(reference)
                             for a in (a0,a1))/2
        assert entropy>=-1e-12 and entropy <= avg_divergence+1e-12
        assert avg_divergence <= b*variance+1e-12
        assert b <= 2+2*math.log(ratio)+1e-12
        matrix_results.append({'A0':a0,'A1':a1,'matrix_entropy':entropy,
                               'root_variance':variance,'mean_lower':lo,'range_root':r,
                               'ratio':ratio,'coefficient':b,'S_squared_reference_divergence':avg_divergence,
                               'entropy_upper':b*variance,
                               'commutator_norm':math.sqrt(mat.norm2(mat.add(mat.mul(a0,a1),mat.mul(a1,a0),1,-1)))})
    caps = []
    table = {'probabilities':['3/4','1/4'], 'diagonal_fields':[['0','1'],['4','0']]}
    with localcontext() as ctx:
        ctx.prec = 100
        for cap in [F(1,1024),F(1,16),F(1),F(64),F(1<<20)]:
            report = cert.certify(table,cap,bits=70)
            enclosure = report['root_certificate']['peer_H_L_interval']
            x = Decimal(cap.numerator)/Decimal(cap.denominator)
            actual = (1+x)**2/(x*x)*(1+x).ln()-(1+x)/x-Decimal('0.5')
            actual_g = ((1+x)/x*(1+x).ln()-1)/2
            def dec(t):
                q=F(t)
                return Decimal(q.numerator)/Decimal(q.denominator)
            assert dec(enclosure['lower_rational']) <= actual <= dec(enclosure['upper_rational'])
            assert actual>0 and actual <= (1+x).ln()
            g_enclosure=report['root_certificate']['peer_G_L_interval']
            assert dec(g_enclosure['lower_rational'])<=actual_g<=dec(g_enclosure['upper_rational'])
            assert 0<actual_g<=x/4
            caps.append({'cap':str(cap),'H_L_interval':enclosure,'Decimal_H_L_diagnostic':str(actual),
                         'G_L_interval':g_enclosure,'Decimal_G_L_diagnostic':str(actual_g),
                         'combined_information_upper_rational':report['integrated_information_upper_rational']})
    # Exact profile-at-zero omission witness; no numerical information estimate.
    witness = {'Y_probabilities':['1/2','1/2'],'A_values':['0','1'],
               'profile_f0':'1','profile_positive_u':'0','J_profile':'0',
               'conditional_Gaussian_variances':['2','1'],
               'consequence':'Conditional laws distinct for every T, so MI is a positive constant; integral with dT/T^2 diverges. Measurable profiles need explicit f(0)=0.'}
    result = {'status':'PASS_BOUNDED_ACQUISITION_ALGEBRA_CHECKS',
              'noncommuting_matrix_floating_diagnostics':matrix_results,
              'exact_interval_cap_certificates':caps,'profile_zero_counterexample':witness,
              'elapsed_seconds':time.perf_counter()-start,
              'scope':'Noncommuting square-root entropy inequality checked at three small floating examples, including rank-one fields. Cap output is rationally enclosed and compared with finite Decimal diagnostics. General proofs and novelty not certified.'}
    out = Path(__file__).with_name('acquisition_algebra_checks.json')
    out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'matrix_examples':len(matrix_results),
                      'cap_certificates':len(caps),'elapsed_seconds':result['elapsed_seconds'],
                      'output':str(out)},indent=2))


if __name__ == '__main__':
    main()
