#!/usr/bin/env python3
"""Exact bounded admissions, not a simulation of asymptotic quantum coding."""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import math
import time


def coarse_checks():
    count = 0
    for d in range(2, 9):
        for n in range(51):
            p = {0: F(1, d ** n)}
            p.update({j: F((d-1)*d**(j-1), d**n) for j in range(1,n+1)})
            assert sum(p.values()) == 1
            loss = sum(pr*(n-max(0,j-1)) for j,pr in p.items())
            assert loss == F(d,d-1)*(1-F(1,d**n))
            assert loss <= F(d,d-1)
            count += 1
    return count


def periodic_law(d,l,b,k):
    """Joint law of stop indicator and retained true/noisy pair counts."""
    m,t = divmod(l,b)
    q,s = divmod(k,b)
    true = k-q
    result = []
    # All sentinel sites <=K match with certainty.
    for j in range(q+1,m+1):
        g = j-q-1
        p = F(d-1,d**(g+1))
        kept = j*(b-1)
        assert kept>=true
        result.append((str(j),p,true,kept-true,g,s))
    g = m-q
    result.append(('none',F(1,d**g),true,l-m-true,g,s))
    assert sum(x[1] for x in result)==1
    return result


def periodic_checks():
    cases=0
    branch_count=0
    samples=[]
    for d in range(2,7):
        for l in range(2,31):
            for b in range(1,l+1):
                m,t=divmod(l,b)
                true_mean=noise_mean=floor_mean=F(0)
                for k in range(1,l+1):
                    law=periodic_law(d,l,b,k)
                    for stop,p,true,noise,g,s in law:
                        assert noise>=0
                        assert noise<=(g+1)*(b-1)-s
                        if stop=='none':
                            recovered_q=m-g
                        else:
                            recovered_q=int(stop)-1-g
                        assert k==b*recovered_q+s
                        noise_mean+=p*noise/l
                        branch_count+=1
                    true_mean+=F(k-k//b,l)
                    floor_mean+=F(k//b,l)
                assert floor_mean==F(b*m*(m-1)//2+m*(t+1),l)
                assert noise_mean<=F(d*(b-1),d-1)
                assert true_mean==F(l+1,2)-floor_mean
                cases+=1
                if d==2 and l in (8,16,30) and b==round(math.sqrt(l)):
                    hg=F(d,d-1)*math.log(d)-math.log(d-1)
                    bound=float(true_mean-noise_mean)*math.log(d)-math.log(b)-hg
                    samples.append({'D':d,'L':l,'b':b,'true_mean':str(true_mean),
                                    'noise_mean':str(noise_mean),
                                    'entropy_mixture_lower_rate_nats':bound})
    return cases,branch_count,samples


def frac_log(x):
    return math.log(x.numerator)-math.log(x.denominator)


def exact_output_spectrum(d,l,b):
    """Finite actual receiver's coherent information from exact spectral classes."""
    joint={}
    for k in range(1,l+1):
        for stop,p,true,noise,g,s in periodic_law(d,l,b,k):
            item=joint.setdefault(stop,{'q':true+noise,'weights':{}})
            assert item['q']==true+noise
            item['weights'][k]=p/l
    coherent=0.0
    spectral_classes=0
    for stop,item in joint.items():
        prob=sum(item['weights'].values())
        q=item['q']
        posterior={k:w/prob for k,w in item['weights'].items()}
        trace=F(0)
        entropy=0.0
        for j in range(q+1):
            eig=sum((p*F(1,d**(2*(q-(k-k//b)))))
                    for k,p in posterior.items() if k-k//b<=j)
            multiplicity=1 if j==q else (d*d-1)*d**(2*(q-j-1))
            trace+=multiplicity*eig
            if eig:
                entropy-=float(multiplicity*eig)*frac_log(eig)
            spectral_classes+=1
        assert trace==1
        coherent+=float(prob)*(q*math.log(d)-entropy)
    m,t=divmod(l,b)
    floor_mean=F(b*m*(m-1)//2+m*(t+1),l)
    hgeom=d/(d-1)*math.log(d)-math.log(d-1)
    bound=(float(F(l+1,2)-floor_mean)-d*(b-1)/(d-1))*math.log(d)-math.log(b)-hgeom
    assert coherent+1e-10>=bound
    return {'D':d,'L':l,'b':b,'spectral_classes':spectral_classes,
            'actual_coherent_information_nats':coherent,
            'analytic_lower_bound_nats':bound,
            'arithmetic':'Rational eigenvalues and traces; floating natural logarithms'}


def main():
    started=time.perf_counter()
    coarse=coarse_checks()
    cases,branches,samples=periodic_checks()
    spectra=[exact_output_spectrum(d,l,b) for d,l,b in
             [(2,8,3),(2,16,4),(2,30,5),(2,100,7),(3,30,5),(4,30,5),(6,30,5)]]
    source=Path('outputs/Astra_Amplification_Cycle9_ULTRA_20261022/PROOF.txt')
    source_hash='a91d763e1526ffb934e5cfeb996c9bcb04bbdc624e2e4a93d175a51dfcad8bf2'
    if source.is_file():
        assert hashlib.sha256(source.read_bytes()).hexdigest()==source_hash
    result={'status':'PASS','coarse_exact_cases':coarse,
            'periodic_exact_parameter_cases':cases,'periodic_exact_branches':branches,
            'samples':samples,'finite_actual_output_spectra':spectra,
            'governing_C9_proof_sha256':source_hash,
            'limitations':['No quantum coding code constructed or simulated',
                          'No final root Cycle10 actual-source audit yet'],
            'wall_seconds':time.perf_counter()-started}
    out=Path(__file__).with_name('REPLAY_RESULT.json')
    out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
