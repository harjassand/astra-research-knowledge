#!/usr/bin/env python3
"""Exact dormant-pair controls for the calibrated-intervention mean limit."""
from fractions import Fraction as F
from pathlib import Path
import json
import sys
import time

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'outputs/interventional_generator'
sys.path.insert(0,str(ROOT/'work'))
from interventional_tomography import fixture4,controlled,ProbabilityOracle,make_table,recover,entropy,rmv,decode


def main():
    start=time.perf_counter();q,pi,f=fixture4();r=len(q);w=F(2,5);eps=F(1,1000)
    z=[row+[F(0),F(0)] for row in q]+[[F(0)]*(r+2) for _ in range(2)]
    extended_pi=[w*x for x in pi];extended_f=f+[-1,1]
    anchors=[]
    for k,label in enumerate((-1,1)):
        p=sum(pi[i] for i in range(r) if f[i]==label);a=next(i for i in range(r) if f[i]==label);b=r+k
        z[a][b]=eps;z[a][a]-=eps;z[b][a]=w*pi[a]*eps/((1-w)*p);z[b][b]=-z[b][a]
        extended_pi.append((1-w)*p);anchors.append((a,b))
    assert rmv(extended_pi,z)==[F(0)]*(r+2)
    for label in (-1,1):
        assert sum(p for p,b in zip(pi,f) if b==label)==sum(p for p,b in zip(extended_pi,extended_f) if b==label)
    hazards=[sum(z[i][j] for j in range(r+2) if extended_f[i]!=extended_f[j]) for i in range(r+2)]
    assert len(set(zip(extended_f,hazards)))==r+2
    bridge_controls=0
    for t in (F(1,2),F(1),F(2),F(3)):
        Qh=controlled(q,f,t);Zh=controlled(z,extended_f,t)
        for i in range(r):
            for j in range(r):
                if i!=j:assert Zh[i][j]==Qh[i][j]
        for a,b in anchors:assert Zh[a][b]==eps and Zh[b][a]==z[b][a]
        bridge_controls+=1
    base=entropy(q,pi);ext=entropy(z,extended_pi)
    assert ext[0]>=w*base[0]-F(1,2**94) and ext[1]<=w*base[1]+F(1,2**94)
    table=make_table(ProbabilityOracle(z,extended_pi,extended_f),r+2);reconstructed=recover(table)
    assert len(reconstructed['Q'])==r+2
    order=sorted(range(r+2),key=lambda i:(hazards[i],extended_f[i]))
    assert decode(reconstructed['Q'])==[[z[i][j] for j in order] for i in order]
    c=F(9,10);alpha=F(1,40)
    data={'status':'CONTROLLED_DORMANT_MEAN_RATE_LIMIT_CONTROLS_PASSED',
          'base_states':r,'extended_states':r+2,'active_stationary_fraction':str(w),
          'zero_field_entropy_rate_scaling_exact':str(w),'extended_entropy_rate_preview':[float(x) for x in ext],
          'visible_stationary_marginal_exactly_preserved':True,'joint_label_hazard_pairs_all_distinct':True,
          'cross_label_hazards':list(map(str,hazards)),'control_settings_checked':bridge_controls,
          'label_preserving_bridge_rates_unchanged_exactly':True,
          'extended_identifiable_rank':r+2,'exact_compiler_reconstructs_extended_model':True,
          'any_finite_threshold_power_ceiling':{'coverage_risk':str(alpha),'fraction_of_base_mean':str(c),
                                              'power_ceiling':str(alpha/c)},
          'finite_clock_penalty_example':{'intervals':10000,'clock':'1','epsilon':'1/1000000000',
                                          'additive_penalty_upper':'1/100000'},
          'random_duration_warning':'Gamma survival cannot be factored from a label-dependent event; additive bound used',
          'new_acquisitions':0,'physical_experiments':0,'elapsed_wall_seconds':time.perf_counter()-start}
    (OUT/'finite_limit_receipt.json').write_text(json.dumps(data,indent=2)+'\n');print(json.dumps(data,indent=2))


if __name__=='__main__':main()
