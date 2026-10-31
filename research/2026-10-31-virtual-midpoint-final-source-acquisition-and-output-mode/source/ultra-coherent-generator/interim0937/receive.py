#!/usr/bin/env python3
"""Exact certificates, physical clock identities and honest finite-grid limits."""
from fractions import Fraction as Q
from pathlib import Path
from itertools import product
from collections import defaultdict
import ast
import json
import sys
import time

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'work'))
from flow import verify
from coherent_generator_control import source_model,inspection,predictions,simplex_round,word_probability
from aliasfree import log_bounds


def diagonal_outer_countermodel():
    P,pi,labels=source_model();B=inspection(P,Q(1),Q(1));back=[[B[j][i] for j in range(4)] for i in range(4)]
    pr=predictions(B,labels,1);mr=predictions(back,labels,1);mu=defaultdict(Q);k=3
    for x in range(4):
        rp=simplex_round([pr[b,][x] for b in (0,1)],k)
        rm=simplex_round([mr[b,][x] for b in (0,1)],k)
        for (p,wp),(m,wm) in product(rp.items(),rm.items()):mu[labels[x],p,m]+=pi[x]*wp*wm
    assert sum(mu.values())==1
    for (label,p,m),mass in mu.items():
        for vector in (p,m):
            for b in (0,1):assert abs(Q(label==b)-Q(vector[b],k))<=Q(2,k)
    target=[word_probability(B,pi,labels,w) for w in product((0,1),repeat=3)]
    for w,probability in zip(product((0,1),repeat=3),target):
        feature=sum(mass*Q(label==w[1])*Q(m[w[0]],k)*Q(p[w[2]],k) for (label,p,m),mass in mu.items())
        assert feature==probability
    assert any(word_probability(B,pi,labels,w)>0 for w in product((0,1),repeat=3) if len(set(w))>1)
    f=[1 if y==0 else -1 for y in labels]
    u=[sum(B[i][j]*f[j] for j in range(4)) for i in range(4)]
    v=[sum(B[j][i]*f[j] for j in range(4)) for i in range(4)]
    C1=sum(pi[i]*f[i]*u[i] for i in range(4));C2=sum(pi[i]*u[i]*v[i] for i in range(4))
    assert C1*C1-C2==Q(4,289)
    b=Q(2,17);ordinary=b*log_bounds((1+b)/(1-b),120)[0]
    return {'mesh':k,'support_nodes':len(mu),'exact_outer_entropy':'0',
            'true_model_positive_ordinary_rate_lower_preview':float(ordinary),
            'actual_zero_generator_fails_observed_word_law':True,
            'interpretation':'finite outer feasibility does not prove exact physical realization or zero true minimum'}


def main():
    start=time.perf_counter();checks=[]
    for path in list(HERE.glob('*.py'))+[ROOT/'work/coherent_generator_control.py']:
        ast.parse(path.read_text(),filename=str(path))
    for name in ('driven','reversible'):
        data=json.loads((HERE/(name+'_dual.json')).read_text());cert=verify(data)
        assert cert['lower']==Q(data['exact_lower_bound'])
        poison=dict(data);values=list(data['row_duals']);values[0]='1';poison['row_duals']=values
        try:verify(poison)
        except ValueError:pass
        else:raise AssertionError('positive row multiplier was accepted')
        maxdiag=max(cert['z']+cert['without_z'](i,i) for i in range(len(cert['nodes'])))
        poison=dict(data);poison['normalization_dual']=str(cert['z']+1-maxdiag)
        try:verify(poison)
        except ValueError:pass
        else:raise AssertionError('poisoned entropy normalization was accepted')
        # Changing physical time units scales ALL rates and entropy coefficients.
        scale=Q(7,3);scaled=dict(data)
        scaled['kinetic_cap']=str(scale*Q(data['kinetic_cap']));scaled['inspection_rate']=str(scale*Q(data['inspection_rate']))
        for key in ('word_coefficients','state_potential'):scaled[key]=[str(scale*Q(x)) for x in data[key]]
        scaled['normalization_dual']=str(scale*Q(data['normalization_dual']))
        assert verify(scaled)['lower']==scale*cert['lower']
        checks.append({'name':name,'exact_columns':cert['columns_checked'],
                        'certified_lower_preview':float(cert['lower']),
                        'positive_row_and_wrong_normalization_rejected':True,
                        'physical_time_unit_rescaling_checked':True,
                        'compiler_seconds':data['seconds']})
    output={'scope':__doc__,'certificates':checks,'exact_coarse_outer_countermodel':diagonal_outer_countermodel(),
            'new_record_acquisitions':0,'status':'COHERENT_GENERATOR_CERTIFICATE_CONTROLS_PASSED',
            'seconds':time.perf_counter()-start}
    (HERE/'verification.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps(output,indent=2))


if __name__=='__main__':main()
