"""Bounded post-run mechanism test using saved exact witnesses, no new probes."""
from fractions import Fraction as F
from pathlib import Path
import json,time
import numpy as np
from exact_residual import jf,fj,AD,rss_bytes,require
from run_experiment import step_data,at_step

ROOT=Path(__file__).resolve().parents[1]

def main():
    t,c=time.perf_counter(),time.process_time()
    results=ROOT/'results'
    certs=json.loads((results/'krylov_certificates.json').read_text())
    cdf=json.loads((results/'cdf_results.json').read_text())
    dense=json.loads((results/'dense_certificate.json').read_text())
    dd=np.load(ROOT/'witnesses/dense.npz',allow_pickle=False)['diagonal']
    de=jf(dense['operator_error'])
    out={'operation':'Analyse the same saved J and complete dense certificate; no new Krylov run or probe draw',
         'cases':[]}
    for case in cdf['cases']:
        k=case['k'];cc=certs[str(k)];weights=[jf(q) for q in case['weights']]
        row=next(r for r in case['threshold_rows'] if r['percentile_display']==50)
        x=jf(row['threshold_scaled'])
        lo=at_step(step_data(cc,weights,'lower'),x)
        hi=at_step(step_data(cc,weights,'upper'),x)
        # Exact root enclosures show the threshold lies between the first two
        # nodes of EVERY Jacobi matrix. Then lower CMS(t-eta) is zero for every
        # eta>0, while upper CMS(t+eta)>=w1+w2. Even setting all nonnegative
        # numerical/statistical allowances to zero leaves this family floor.
        first_weights=[];second_weights=[]
        for j in cc:
            nodes=j['jacobi']['nodes']
            require(jf(nodes[0]['upper'])<x<jf(nodes[1]['lower']),
                    'median not in every first-node gap')
            first_weights.append(F(nodes[0]['weight_lower']))
            second_weights.append(F(nodes[1]['weight_lower']))
        floor=sum(w*(a+b) for w,a,b in zip(weights,first_weights,second_weights))
        current_width=jf(row['candidate']['width'])
        sampled_width=jf(row['deterministic_probe']['width'])
        out['cases'].append(dict(k=k,threshold=fj(x),
            zero_error_cms_lower=fj(lo),zero_error_cms_upper=fj(hi),
            fixed_envelope_width_floor=fj(floor),
            floor_float=float(floor),current_width=float(current_width),
            deterministic_stored_probe_width=float(sampled_width),
            numerical_transfer_increment=float(sampled_width-(hi-lo)),
            statistical_increment=float(current_width-sampled_width),
            smallest_weight_min=float(min(first_weights)),
            smallest_weight_max=float(max(first_weights)),
            scope='For these saved J, their CMS lag/lead envelopes and any positive transfer margins. Not an optimal truncated-moment lower bound or a universal SLQ impossibility.'))
    cluster=[]
    for threshold in (F(1,100000),F(1,20000),F(1,10000),F(1,1000)):
        lower=sum(F(int(d),AD)+de<=threshold for d in dd)
        upper=sum(F(int(d),AD)-de<=threshold for d in dd)
        cluster.append(dict(threshold_scaled=fj(threshold),lower_count=lower,upper_count=upper,
                            n=len(dd),fraction_lower=lower/len(dd),fraction_upper=upper/len(dd)))
    out['verified_dense_cluster_counts']=cluster
    out['resources']=dict(wall_seconds=time.perf_counter()-t,cpu_seconds=time.process_time()-c,
                          peak_rss_bytes=rss_bytes(),new_matvecs=0,new_probes=0,new_eigensolves=0)
    (results/'error_mechanism.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
