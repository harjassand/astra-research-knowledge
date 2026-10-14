#!/usr/bin/env python3
"""Finite rational interval checks, not a formal proof or hardware validation.

Uses only a separately copied pinned PR87 exact-arithmetic primitive. Original
source bytes and the earlier frozen overlap audit are not changed.
"""
from pathlib import Path
import sys
import json
import argparse
import hashlib
import importlib.util
parser=argparse.ArgumentParser()
parser.add_argument('--primitive',type=Path,default=Path(__file__).parent/'replays'/'verify_snapshot_operation.py',
                    help='exact pinned PR87 source primitive, retained separately from authored integration')
args=parser.parse_args()
assert hashlib.sha256(args.primitive.read_bytes()).hexdigest()=='02c76587799b84c5c3c8573e797fdf0a8f2b5aaaebad8e8d6f56488b80eacee1'
spec=importlib.util.spec_from_file_location('pr87_exact_primitive',args.primitive)
v=importlib.util.module_from_spec(spec)
sys.modules[spec.name]=v
spec.loader.exec_module(v)
F=v.F


def joint_clock_score(q,pi,b,r,times,kernel,eta=F(0)):
    size=len(times)
    assert all(kernel[i][j]==kernel[j][i] for i in range(size) for j in range(size))
    assert all(x>=0 for row in kernel for x in row)
    assert sum(map(sum,kernel))==1
    marginal=list(map(sum,kernel))
    mean_gap=sum(p*t for p,t in zip(marginal,times))
    pt=[v.transition(q,t) for t in times]
    score=sum(kernel[a][d]*pi[i]*pt[a][i][j]*pt[d][j][k]
              *b[j]*(b[i]-r)*(b[k]-r)
              for a in range(size) for d in range(size)
              for i in range(len(q)) for j in range(len(q)) for k in range(len(q)))
    p_b=sum(x*y for x,y in zip(pi,b))
    penalty=eta*max(r,1-r)**2*p_b
    d_eff=-score-penalty
    bound=None
    if d_eff.lo>0:
        bound=v.negative_log_one_minus(d_eff*(1/(r*(1-r))))*(1/mean_gap)
    return dict(score=v.show(score),mean_gap=str(mean_gap),clock_marginal=list(map(str,marginal)),
                kernel=[[str(x) for x in row] for row in kernel],eta=str(eta),
                spectral_penalty=str(penalty),effective_D=v.show(d_eff),
                floor=v.show(bound) if bound else None),score


def main():
    kernels={
        'iid':[[F(1,4),F(1,4)],[F(1,4),F(1,4)]],
        'shared_gap':[[F(1,2),F(0)],[F(0),F(1,2)]],
        'conditional_iid_mixture':[[F(5,16),F(3,16)],[F(3,16),F(5,16)]],
        'anti_correlated':[[F(0),F(1,2)],[F(1,2),F(0)]],
    }
    # The mixture is 1/2 p+ p+^T +1/2 p- p-^T, p+=(3/4,1/4).
    plus,minus=[F(3,4),F(1,4)],[F(1,4),F(3,4)]
    assert kernels['conditional_iid_mixture']==[[
        (plus[i]*plus[j]+minus[i]*minus[j])/2 for j in range(2)] for i in range(2)]
    for name in ('iid','shared_gap','conditional_iid_mixture'):
        k=kernels[name]
        assert k[0][0]>=0 and k[1][1]>=0 and k[0][0]*k[1][1]-k[0][1]**2>=0
    assert kernels['anti_correlated'][0][0]*kernels['anti_correlated'][1][1]-kernels['anti_correlated'][0][1]**2<0
    # Marginal=(1/2,1/2); normalized anti-correlated kernel has eigenvalues +1,-1.
    eq=[[F(-1),F(1)],[F(1),F(-1)]]
    controls={}
    for name,k in kernels.items():
        rec,score=joint_clock_score(eq,[F(1,2)]*2,[F(0),F(1)],F(3,4),
                                    [F(1,10),F(1)],k,eta=F(name=='anti_correlated'))
        assert rec['floor'] is None
        if name=='anti_correlated': assert score.hi<0
        else: assert score.lo>=0
        controls[name]=rec
    q=F(1,20)
    ring=[[-(1+q),F(1),q],[q,-(1+q),F(1)],[F(1),q,-(1+q)]]
    examples={}
    for name in ('iid','shared_gap','conditional_iid_mixture'):
        rec,score=joint_clock_score(ring,[F(1,3)]*3,[F(0),F(1),F(1)],F(9,10),
                                    [F(1,5),F(2,5)],kernels[name])
        assert score.hi<0 and rec['floor'] is not None
        examples[name]=rec
    # A reversible specimen independent of a driven ring detector has zero
    # specimen EP and the same full output law as the detector ring.
    joint=[[F(0)]*6 for _ in range(6)]
    for s in range(2):
        for d in range(3):
            i=3*s+d
            for e in range(3): joint[i][3*s+e]+=ring[d][e]
            joint[i][3*(1-s)+d]+=1
            joint[i][i]-=1
    assert all(sum(row)==0 for row in joint)
    assert all(sum(joint[i][j] for i in range(6))==0 for j in range(6))
    fixed,_,_=v.certificate(ring,[F(1,3)]*3,[F(0),F(1),F(1)],F(9,10),[(F(1),F(3,10))])
    joint_fixed,_,_=v.certificate(joint,[F(1,6)]*6,[F(0),F(1),F(1)]*2,F(9,10),[(F(1),F(3,10))])
    a,b=fixed['mean_score'],joint_fixed['mean_score']
    assert max(F(a['lower_decimal']),F(b['lower_decimal']))<=min(F(a['upper_decimal']),F(b['upper_decimal']))
    p=F(2,3);independent_memoryless=p*(p-F(9,10))**2
    assert independent_memoryless==F(49,1350)>0
    memory=dict(specimen_generator=[['-1','1'],['1','-1']],specimen_EP='0 exactly',
                actual_detector='autonomous driven q=1/20 ring, independent of specimen',
                one_time_P_Y1_given_specimen_state='2/3 at either state',
                memoryless_single_time_matched_score=str(independent_memoryless),
                actual_joint_score=joint_fixed['mean_score'],
                interpretation='positive certificate belongs to combined detector+specimen, not specimen alone')
    result=dict(status='PASS',scope='exact finite interval checks and algebra only',
                equilibrium_clock_controls=controls,ring_correlated_clock_examples=examples,
                detector_memory_attribution_counterexample=memory,novelty='UNKNOWN',
                independent_correctness='UNKNOWN',physical_acquisition='NOT_ESTABLISHED')
    target=Path(__file__).with_name('PR87_CLOCK_EXTENSION_RESULTS.json')
    target.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',ring_floors={k:x['floor'] for k,x in examples.items()},
                          equilibrium_anti_score=controls['anti_correlated']['score'],output=str(target)),indent=2))


if __name__=='__main__':main()
