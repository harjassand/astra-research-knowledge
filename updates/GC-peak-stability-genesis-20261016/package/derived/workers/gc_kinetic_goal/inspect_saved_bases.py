#!/usr/bin/env python3
"""Exact support and two-point terminal-receiver tests of the three raw NPZs."""
from fractions import Fraction as F
from pathlib import Path
import argparse
import hashlib
import json
import resource
import numpy as np

def point_rank1(cores,physical,order):
    v=F(1)
    for i,g in enumerate(cores):
        assert g.shape==(1,163,1)
        v*=F.from_float(float(g[0,physical[order[i]],0]))
    return v

def main(a):
    resource.setrlimit(resource.RLIMIT_CPU,(120,121))
    packet=Path(a.packet)
    manifests=['experiments/candidate.json','experiments/weighted_repair/candidate.json','experiments/constrained_test/candidate.json']
    target=[15]*8;continuation=[16]+[15]*7;out=[]
    for manifest in manifests:
        mp=packet/manifest;m=json.loads(mp.read_text());p=mp.parent/m['npz']
        rec={'manifest':str(mp),'manifest_sha256':hashlib.sha256(mp.read_bytes()).hexdigest(),
             'npz':str(p),'npz_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
             'allow_pickle':False,'basis_count':m['basis_count'],'point_target':target,'point_continuation':continuation,'bases':[]}
        broad=None
        with np.load(p,allow_pickle=False) as z:
            assert np.all(z['time_coefficients'][:,0]==0)
            assert z['initial_overflow']==0
            for j in range(m['basis_count']):
                cores=[z[f'basis_{j}_core_{i}'] for i in range(8)]
                support=[]
                for g in cores:
                    assert g.dtype==np.float64 and np.all(np.isfinite(g))
                    ix=np.flatnonzero(np.any(g!=0,axis=(0,2)))
                    support.append([int(ix[0]),int(ix[-1])] if len(ix) else [])
                azero=any(not np.any(g[:,target[m['order'][i]],:]) for i,g in enumerate(cores))
                czero=any(not np.any(g[:,continuation[m['order'][i]],:]) for i,g in enumerate(cores))
                rec['bases'].append({'basis':j,'core_mode_support_ranges':support,'target_point_literal_zero':azero,'continuation_point_literal_zero':czero})
                if not azero or not czero:
                    assert broad is None
                    va=point_rank1(cores,target,m['order']);vc=point_rank1(cores,continuation,m['order'])
                    assert va>0 and vc>0;broad=(va,vc)
            if broad is None:
                lower=F(1)
                reason='Every saved basis is exactly zero at the target point; any unchanged-span backward terminal approximation has sup error>=1.'
            else:
                va,vc=broad
                lower=vc/(va+vc)
                rec['only_nonzero_basis_target_value_exact']=str(va)
                rec['only_nonzero_basis_continuation_value_exact']=str(vc)
                reason='All other bases vanish at both points. Minimizing max(|1-a*bA|,|a*bC|) over real a gives bC/(bA+bC).'
            rec['unchanged_forward_span_terminal_backward_sup_error_lower_exact']=str(lower)
            rec['unchanged_forward_span_terminal_backward_sup_error_lower_descriptive']=float(lower)
            rec['proof']=reason
        out.append(rec)
    report={'status':'PASS_EXACT_TWO_POINT_RECEIVER_BASIS_OBSTRUCTIONS',
            'scope':'Only reuse of these unchanged saved forward trial spaces for backward terminal1_target; no claim about enriched/new TT representations.',
            'target_indicator_frobenius_norm_exact':16**4,'candidates':out,
            'arithmetic':'Literal binary64 support tests; exact dyadic scalar products of rank-one cores and rational minimax formula.'}
    Path(a.output).write_text(json.dumps(report,indent=2))
    print(json.dumps({'status':report['status'],'terminal_sup_error_lowers':[x['unchanged_forward_span_terminal_backward_sup_error_lower_descriptive'] for x in out]},indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('packet');p.add_argument('--output',required=True);main(p.parse_args())
