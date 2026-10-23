#!/usr/bin/env python3
"""Closed-form evaluations of proved floors, not capacity measurements."""
from decimal import Decimal, localcontext
from math import comb
from pathlib import Path
import hashlib, json, resource, time


def collision_v(k):
    n = (k-2)//2
    p = Decimal(comb(2*n,n))/Decimal(4**n)
    c = (2*n+1)*p*(Decimal(k-1)-Decimal(2*n)/3)
    return Decimal(k*(k-1))/8-c/8


def run():
    start = time.perf_counter()
    out = []
    with localcontext() as ctx:
        ctx.prec = 100
        D = Decimal
        ell = D(2).ln()
        for den in (16,32,64,256,512,2048,4096):
            beta=D(1)/den; b=beta*beta
            k8=int(1/(4*beta)); v8=collision_v(k8)
            k9=int(1/(16*b*(1-b.ln()))); v9=collision_v(k9)
            e8=ell*v8*b*b/(32*k8)
            e9=ell*v9*b*b/(64*k9)
            # Retain the actual pair and nonscalar four-call operation.
            delta=b*b/512; q=D('0.5')-delta; c=-b/128
            x=q*q; y=q*(1-q)/2; z=(1-q)**2/4
            def entropy(ps):
                return -sum(p*p.ln()/ell for p in ps if p)
            pair=entropy([x]+[z]*4+[y+c]*2+[y-c]*2)/2-D('1.5')
            p=(1+c/y)/2
            four=pair+x*y*(1-entropy([p,1-p]))/2
            row={'beta_denominator':den,'beta':str(beta),'b':str(b),
                 'cycle8_k':k8,'cycle8_exact_floor':str(e8),
                 'cycle9_k':k9,'cycle9_exact_floor':str(e9),
                 'pair_actual_entropy_excess':str(pair),
                 'nonscalar_four_call_actual_entropy_excess':str(four)}
            candidates={'cycle8':e8,'cycle9':e9,'pair':pair,'four_call':four}
            if den>=32:
                k=int(1/(256*b)); r=b*k; v=collision_v(k)
                budget=ell*v*b*b; excess=budget/(64*k)
                gamma=ell/4; kappa=(1-b)*budget/128
                lyap=kappa/(2*k*k); gap=kappa*kappa/(4*k*k)
                normalizer=1+3*gamma*gamma*r*r/4
                eta=3*ell*v*b*b/16
                assert k>=4 and r<=D(1)/256 and b<=D(1)/1024
                assert (1-b)*(D(7)/128-2*r)>16*ell*r
                assert excess>=ell*b/(2**20)
                row.update({'cycle10_k':k,'cycle10_v':str(v),'cycle10_exact_floor':str(excess),
                     'cycle10_uniform_floor':str(ell*b/(2**20)),
                     'cycle10_over_cycle9':str(excess/e9),
                     'cycle10_over_cycle8':str(excess/e8),
                     'cycle10_bk':str(r),
                     'normalizer_condition_number_upper':str(normalizer),
                     'tilt_deviation_upper':str(eta),
                     'rank':'rank(I-gamma*b*H/2), at most 3^k; not evaluated',
                     'log10_input_dimension':str(D(k)*D(3).ln()/D(10).ln()),
                     'kappa':str(kappa),'lyapunov_t':str(lyap),'one_minus_lambda':str(gap),
                     'log10_type_cutoff_coefficient_upper':str(((D(3)**k+D(16)).ln()-lyap.ln())/D(10).ln()),
                     'all_analytic_scalar_margins_pass':True})
                candidates['cycle10']=excess
            else:
                row['cycle10_status']='Outside proved beta range; no new floor asserted.'
            winner=max(candidates,key=candidates.get)
            row.update({'best_retained_certificate':winner,'best_retained_excess':str(candidates[winner])})
            out.append(row)
    return {'precision_decimal_digits':100,'observations':out,
            'wall_seconds':time.perf_counter()-start,
            'peak_rss_kib_linux':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            'scope':'Closed-form certificate comparisons under identical operation; not actual capacities, compiled codes, or discovery cost.',
            'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}


if __name__=='__main__':
    result=run()
    Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
    keys=['beta_denominator','cycle10_k','cycle10_exact_floor','cycle10_over_cycle9','best_retained_certificate']
    print(json.dumps({'rows':[{k:r[k] for k in keys if k in r} for r in result['observations']],
                      'wall_seconds':result['wall_seconds'],'peak_rss_kib_linux':result['peak_rss_kib_linux']},indent=2))
