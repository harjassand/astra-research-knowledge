#!/usr/bin/env python3
"""Full-generator parity witness on an exactly localized exported basis."""
import argparse
from decimal import Decimal,localcontext
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import resource
import time
import numpy as np
import verify_slab as v

def run(a):
    start=time.monotonic()
    resource.setrlimit(resource.RLIMIT_AS,(512*1024**2,512*1024**2))
    resource.setrlimit(resource.RLIMIT_CPU,(120,121))
    s=v.Slab(a.manifest)
    # Needed only for the simplified full-generator identity below. This is a
    # literal support check of every core, not an approximation or truncation.
    for cores in s.basis:
        for core in cores:
            nz=np.flatnonzero(np.any(core!=0,axis=(0,2)))
            assert len(nz) and min(nz)>16 and max(nz)<162
    signs=[Decimal((-1)**n) for n in range(163)]
    reaction=[]
    with localcontext() as ctx:
        ctx.prec=80
        for n in range(163):
            exact=-2*(v.birth(n)+v.death(n))*(-1)**n
            x=Decimal(exact.numerator)/Decimal(exact.denominator)
            assert F(x)==exact
            reaction.append(x)
    qphi=[v.ZERO];gphi=[v.ZERO]
    for j,cores in enumerate(s.basis):
        base=s.contractor.functional(cores,[signs]*8)
        gen=v.ZERO
        for site in range(8):
            w=[signs]*8;w[site]=reaction
            gen=gen+s.contractor.functional(cores,w)
        qphi=v.p_add(qphi,v.p_scale(s.time_power[j],base))
        gphi=v.p_add(gphi,v.p_scale(s.time_power[j],gen))
    r=v.p_add(v.p_scale(v.p_derivative(qphi),1/s.h),v.p_scale(gphi,-1))
    lb=v.integrated_abs_lower(r,s.h,a.bins)
    report={'status':'REJECT_FULL_FORWARD_L1_BUDGET' if lb>F('1e-9') else 'INCONCLUSIVE_LOWER_BOUND_ONLY','candidate':str(s.npz_path),'candidate_sha256':hashlib.sha256(s.npz_path.read_bytes()).hexdigest(),'witness':'(-1)^(sum of all eight physical counts), zero on overflow; infinity norm one','full_generator_identity':'On the verified support every reaction flips parity and no reaction overflows. Every hop preserves total parity exactly, so all twenty directed diffusion terms cancel algebraically. Target columns have no support. Thus G^T phi=-2*sum_i(b(n_i)+d(n_i))*phi on every supported column.','integrated_l1_residual_lower':v.fraction_json(lb),'temporal_signed_cross_terms':'Complete signed polynomial combined before exact dyadic-bin integration','arithmetic':'Directed 80-digit Decimal weighted TT contractions with exact rational rates; exact rational interval polynomial algebra','endpoint_parity_interval':v.interval_json(v.p_eval(qphi,F(1))),'no_probability_error_lower_bound_claimed':True,'memory_limit_mib':512,'cpu_limit_seconds':120,'elapsed_seconds':time.monotonic()-start,'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    Path(a.output).write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('manifest');p.add_argument('--output',required=True);p.add_argument('--bins',type=int,default=256);run(p.parse_args())
