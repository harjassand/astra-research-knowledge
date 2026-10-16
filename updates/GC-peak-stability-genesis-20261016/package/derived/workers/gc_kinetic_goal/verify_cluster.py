#!/usr/bin/env python3
"""Read-only exact replay of every immutable cluster resolvent vector.

No candidate construction imports, SciPy, pickle, simulation, or eight-site
state enumeration. Generator rows independently reconstructed from the
actual incoming manifest and the specified deletion of horizontal imports.
"""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
import argparse
from fractions import Fraction as F
from math import factorial
from pathlib import Path
import hashlib
import json
import resource
import sys
import time
import numpy as np
sys.set_int_max_str_digits(100000)

def downward(x, scale=10**12): return F((x*scale).numerator//(x*scale).denominator,scale)
def upward(x, scale=10**15): return -downward(-x,scale)

def main(args):
    start=time.monotonic()
    resource.setrlimit(resource.RLIMIT_CPU,(120,121))
    d=json.loads(Path(args.certificate).read_text())
    model_path=Path(args.model_manifest)
    model=json.loads(model_path.read_text())
    actual_edges={tuple(sorted(e)) for e in model['physical_edges']}
    expected={(0,1),(1,2),(2,3),(4,5),(5,6),(6,7),(0,4),(1,5),(2,6),(3,7)}
    assert actual_edges==expected and model['initial']==[50]*8 and model['cap']==162 and model['target_max']==15
    assert model['semantics']=='frozen_target_grid_plus_overflow'
    rates={key:F(v) for key,v in model['rates'].items()}
    cap_path=Path(args.cap_certificate)
    cap_receipt=json.loads(cap_path.read_text())['certificate']
    rho=F(161,100)
    def qb(n):
        bn=rates['birth_quadratic']*n*(n-1)+rates['birth_constant']
        an=rates['death_cubic']*n*(n-1)*(n-2)+rates['death_linear']*n
        return bn*(rho-1)+an*(1/rho-1)+3*rates['diffusion']*n*(rho+1/rho-2)
    q111,q112,q113,q114=[qb(n) for n in [111,112,113,114]]
    c3=(q114-3*q113+3*q112-q111)/6
    c2=(q113-2*q112+q111)/2-3*c3
    c1=q112-q111-c2-c3
    assert all(x<0 for x in [q111,c1,c2,c3])
    table=[rho**n*qb(n) for n in range(111)]
    K=max(table);assert [n for n,v in enumerate(table) if v==K]==[103]
    epsilon=(8*rho**50+8*K)/rho**163
    assert epsilon==F(cap_receipt['epsilon']['rational'])<F('1e-9')
    assert K==F(cap_receipt['K']['rational'])
    den=10000; one=1<<60; cap=d['cap']; k=d['erlang_shape']; rate=d['erlang_rate']
    assert cap==162 and k==64 and rate==64
    assert one==int(d['dyadic_denominator']) and den==d['denominator_rate']
    birth=[int(den*(rates['birth_quadratic']*n*(n-1)+rates['birth_constant'])) for n in range(cap+1)]
    death=[int(den*(rates['death_cubic']*n*(n-1)*(n-2)+rates['death_linear']*n)) for n in range(cap+1)]
    diffusion=int(den*rates['diffusion'])
    # The four retained vertical edges. Each deleted edge contributes an
    # emigration channel to both endpoints, and its immigration is discarded.
    retained={(0,4),(1,5),(2,6),(3,7)}
    removed=actual_edges-retained
    external=[sum(site in edge for edge in removed) for site in range(8)]
    assert external==[1,2,2,1,1,2,2,1]
    zpath=Path(args.certificate).parent/d['stored_vectors_npz']
    assert hashlib.sha256(zpath.read_bytes()).hexdigest()==d['stored_vectors_sha256']
    en=sum((F(1,factorial(j)) for j in range(33)),F(0))
    eup=en+F(34,33*factorial(33))
    poisson=sum((F(rate**j,factorial(j)) for j in range(k)),F(0))
    clocklo,clockhi=poisson/eup**rate,poisson/en**rate
    assert F(d['erlang_survival_at1_interval'][0]['exact'])==clocklo
    assert F(d['erlang_survival_at1_interval'][1]['exact'])==clockhi
    product_lower=F(1); uncapped_product_lower=F(1); product_upper=F(1); results=[]
    with np.load(zpath,allow_pickle=False) as z:
        assert set(z.files)=={'external_1','external_2'}
        for ext in [1,2]:
            stage=z['external_'+str(ext)]
            assert stage.dtype==np.uint64 and stage.shape==(k+1,cap+1,cap+1)
            initial=np.zeros((cap+1,cap+1),dtype=np.uint64);initial[:16,:16]=one
            assert np.array_equal(stage[0],initial)
            assert np.all(stage[:,:16,:16]==one)
            previous=stage[0].tolist(); sum_defect=0
            rec=d['pair_estimates'][str(ext)]
            for j in range(1,k+1):
                current=stage[j].tolist(); worst=0; where=None
                for n in range(cap+1):
                    for m in range(cap+1):
                        v=current[n][m]
                        residual=rate*den*(v-previous[n][m])
                        if n>15 or m>15:
                            successors=[(n+1,m,birth[n]),(n,m+1,birth[m])]
                            if n:
                                successors.extend([(n-1,m,death[n]+ext*diffusion*n),(n-1,m+1,diffusion*n)])
                            if m:
                                successors.extend([(n,m-1,death[m]+ext*diffusion*m),(n+1,m-1,diffusion*m)])
                            for nn,mm,hazard in successors:
                                other=one if nn>cap or mm>cap else current[nn][mm]
                                residual+=hazard*(v-other)
                        if abs(residual)>worst: worst=abs(residual); where=[n,m]
                expected=rec['phases'][j-1]
                assert expected['phase']==j and worst==int(expected['exact_residual_max_integer_numerator']) and where==expected['maximizer']
                sum_defect+=worst; previous=current
            radius=F(sum_defect,rate*den*one)
            estimate=F(previous[50][50],one)
            low=max(F(0),estimate-radius);high=min(F(1),estimate+radius)
            assert radius==F(rec['uniform_error_radius']['exact'])
            assert estimate==F(rec['random_horizon_estimate_exact'])
            assert low==F(rec['random_horizon_probability_interval'][0]['exact'])
            assert high==F(rec['random_horizon_probability_interval'][1]['exact'])
            pair_low=max(F(0),(low-clockhi)/(1-clockhi))
            pair_high=min(F(1),high/clocklo)
            assert pair_low==F(rec['deadline1_probability_lower']['exact'])
            assert pair_high==F(rec['deadline1_probability_upper']['exact'])
            product_lower*=pair_low**2;product_upper*=pair_high**2
            uncapped_pair_lower=max(F(0),pair_low-epsilon)
            uncapped_product_lower*=uncapped_pair_lower**2
            results.append({'external_degree':ext,'residual_radius_upward':str(upward(radius)),
                            'random_horizon_interval_descriptive':[float(low),float(high)],
                            'deadline1_pair_hit_lower_downward':str(downward(pair_low)),
                            'deadline1_uncapped_pair_hit_lower_downward':str(downward(uncapped_pair_lower)),
                            'deadline1_pair_hit_upper':str(pair_high)})
    assert product_upper==F(d['actual_eight_site_deadline_probability_upper']['exact'])==1
    assert product_lower>F('0.9262203971')
    assert uncapped_product_lower>F('0.926220394')
    report={'status':'PASS_EXACT_IMMUTABLE_CLUSTER_REPLAY',
            'all_saved_resolvent_vectors_checked':2*k,'states_per_vector':(cap+1)**2,
            'all_rational_model_and_dyadic_vector_arithmetic':'Exact Python integers and Fraction',
            'model_manifest_sha256':hashlib.sha256(model_path.read_bytes()).hexdigest(),
            'model_manifest':str(model_path), 'stored_vectors_sha256':d['stored_vectors_sha256'],
            'cap_certificate':str(cap_path),'cap_certificate_sha256':hashlib.sha256(cap_path.read_bytes()).hexdigest(),
            'original_T1_overflow_budget_upward':str(upward(epsilon,10**24)),
            'cap_arithmetic_reconstructed':'111 exact evaluations plus cubic negative shifted tail; maximum103; exact source epsilon matches',
            'npz_load_pickle':False,'results':results,
            'comparison_product_probability_T1_lower_downward':str(downward(product_lower)),
            'uncapped_comparison_product_probability_T1_lower_downward':str(downward(uncapped_product_lower)),
            'actual_eight_site_upper':str(product_upper),
            'interpretation':'The finite hit-or-overflow product exceeds0.9262203971. Subtracting the original T1 overflow allowance per pair shows the uncapped independent vertical-pair hit product exceeds0.926220394. This is not a lower bound on the actual eight-site probability.',
            'elapsed_seconds':time.monotonic()-start,
            'peak_rss_native_units':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            'platform':sys.platform,'cpu_limit_seconds':120}
    Path(args.output).write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('certificate');ap.add_argument('--model-manifest',required=True)
    ap.add_argument('--cap-certificate',required=True)
    ap.add_argument('--output',required=True);main(ap.parse_args())
