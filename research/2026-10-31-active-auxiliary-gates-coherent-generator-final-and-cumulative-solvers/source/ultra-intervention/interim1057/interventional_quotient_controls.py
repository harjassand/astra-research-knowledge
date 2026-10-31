#!/usr/bin/env python3
"""Adversarial quotient controls: weak lumping, hidden fuel and bad input."""
from fractions import Fraction as F
from pathlib import Path
import copy
import json
import sys
import time

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'outputs/interventional_generator'
sys.path.insert(0,str(ROOT/'work'))
from interventional_tomography import fixture4,controlled,resolvent,ProbabilityOracle,make_table,recover,entropy,mm,mv,rmv,diagonal


def weak_expansion(q,pi,f):
    r=len(q);n=2*r;z=[[F(0)]*n for _ in range(n)]
    for x in range(r):
        for a in range(2):
            i=2*x+a;z[i][2*x+1-a]=1
            for y in range(r):
                if y==x:continue
                for b in range(2):z[i][2*y+b]=q[x][y]/2
    # Outgoing rates to TWO distinct cells vary, but total label-crossing
    # hazard stays fixed. Averaging the source hidden bit cancels both.
    for a,sign in enumerate((1,-1)):
        for b in range(2):z[a][2*2+b]+=sign*F(1,6);z[a][2*3+b]-=sign*F(1,6)
    for i in range(n):z[i][i]=-sum(z[i])
    L=[[F(x==i//2,2) for i in range(n)] for x in range(r)]
    K=[[F(i//2==x) for x in range(r)] for i in range(n)]
    return z,[pi[i//2]/2 for i in range(n)],[f[i//2] for i in range(n)],L,K


def invisible_cycle(q,pi,f):
    r=len(q);n=3*r;z=[[F(0)]*n for _ in range(n)]
    for x in range(r):
        for a in range(3):
            i=3*x+a;z[i][3*x+(a+1)%3]+=2;z[i][3*x+(a-1)%3]+=1
            for y in range(r):
                if y!=x:z[i][3*y+a]+=q[x][y]
    for i in range(n):z[i][i]=-sum(z[i])
    L=[[F(x==i//3,3) for i in range(n)] for x in range(r)]
    return z,[pi[i//3]/3 for i in range(n)],[f[i//3] for i in range(n)],L


def stationary(q):
    n=len(q);A=[[q[j][i] for j in range(n)] for i in range(n)];A[-1]=[F(1)]*n
    from coherent_generator_control import inverse
    return mv(inverse(A),[F(0)]*(n-1)+[F(1)])


def main():
    start=time.perf_counter();q,pi,f=fixture4();base_ep=entropy(q,pi)
    weak,pw,fw,L,K=weak_expansion(q,pi,f)
    assert all(weak[i][j]>0 for i in range(8) for j in range(8) if i!=j)
    assert rmv(pw,weak)==[F(0)]*8
    assert mm(weak,K)!=mm(K,q),'this example must NOT be strongly lumpable'
    for t in (F(1,2),F(1),F(2),F(3)):
        assert mm(L,controlled(weak,fw,t))==mm(controlled(q,f,t),L)
    weak_ep=entropy(weak,pw);assert weak_ep[0]>base_ep[1]
    expanded,px,fx,Lx=invisible_cycle(q,pi,f)
    for t in (F(1,2),F(1),F(2),F(3)):
        assert mm(Lx,controlled(expanded,fx,t))==mm(controlled(q,f,t),Lx)
    extra_ep=entropy(expanded,px)
    from interventional_tomography import log_bounds
    log2=log_bounds(F(2),64)
    assert extra_ep[0]>=base_ep[0]+log2[0]-F(1,2**94)
    assert extra_ep[1]<=base_ep[1]+log2[1]+F(1,2**94)
    # A corrupted probability table must not become a physical certificate.
    table=make_table(ProbabilityOracle(q,pi,f),4);bad=copy.deepcopy(table)
    bad['H_shifted'][0][0][0]=str(F(bad['H_shifted'][0][0][0])+F(1,100000))
    try:recover(bad)
    except (AssertionError,RuntimeError,ValueError,ZeroDivisionError):corrupt_rejected=True
    else:raise AssertionError('corrupted probability table accepted')
    # Local detailed balance alone permits a common symmetric kinetic
    # prefactor. It is an explicitly wrong actuator for(A1), even though
    # all reciprocal rate ratios have the correct potential shift.
    oracle=ProbabilityOracle(q,pi,f);wrong=controlled(q,f,F(2));wrong=[[F(11,10)*x for x in row] for row in wrong]
    B=resolvent(wrong,F(1))
    for k,bit in enumerate((-1,1)):oracle.T[2+k]=mm(B,diagonal([F(x==bit) for x in f]))
    for i in range(4):
        for j in range(4):
            if i!=j:assert wrong[i][j]/wrong[j][i]==q[i][j]/q[j][i]*F(2)**(f[j]-f[i])
    try:recover(make_table(oracle,4))
    except (AssertionError,RuntimeError,ValueError,ZeroDivisionError):wrong_actuator_rejected=True
    else:wrong_actuator_rejected=False  # self-consistency is not a universal calibration test
    # Observable joint degeneracy is a genuine boundary of this prototype.
    dg=[[F(0),F(1),F(2),F(3)],[F(1),F(0),F(4),F(1)],
        [F(1),F(1),F(0),F(1)],[F(2),F(4),F(2),F(0)]]
    for i in range(4):dg[i][i]=-sum(dg[i])
    pd=stationary(dg);deg_table=make_table(ProbabilityOracle(dg,pd,f),4)
    try:recover(deg_table)
    except RuntimeError:degenerate_rejected=True
    else:raise AssertionError('globally degenerate prototype spectrum accepted')
    data={'status':'INTERVENTIONAL_QUOTIENT_ADVERSARIAL_CONTROLS_PASSED',
          'canonical_entropy_interval':list(map(str,base_ep)),
          'weak_expansion':{'hidden_states':8,'stationary_lifting_and_all_control_intertwining_exact':True,
                            'strong_lumpability':False,'entropy_rate_preview':[float(x) for x in weak_ep],
                            'correction':'common quotient in stationary law does not imply strong lumpability for every hidden initialization'},
          'independent_hidden_driven_cycle':{'hidden_states':12,'controlled_laws_unchanged_exactly':True,
                                            'extra_entropy_rate':'log(2)','entropy_rate_preview':[float(x) for x in extra_ep]},
          'corrupted_table_rejected':corrupt_rejected,
          'wrong_symmetric_actuator_prefactor_rejected_on_this_fixture':wrong_actuator_rejected,
          'wrong_actuator_scope':'local detailed balance ratios are insufficient; receiver self-consistency cannot generally acquire calibration',
          'observable_joint_degeneracy':{'rank_four_table_invertible':True,'hazards':['5','5','2','6'],
                                        'prototype_rejected':degenerate_rejected,'not_a_nonidentifiability_or_hardness_theorem':True},
          'new_acquisitions':0,'physical_experiments':0,'elapsed_wall_seconds':time.perf_counter()-start}
    (OUT/'quotient_receipt.json').write_text(json.dumps(data,indent=2)+'\n');print(json.dumps(data,indent=2))


if __name__=='__main__':main()
