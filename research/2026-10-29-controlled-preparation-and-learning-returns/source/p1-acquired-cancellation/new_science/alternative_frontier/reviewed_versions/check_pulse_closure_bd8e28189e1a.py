#!/usr/bin/env python3
"""Exact rational synthetic checks. No physical observations or sample claims."""
from fractions import Fraction as F
from pathlib import Path
import json
import numpy as np

def mat(rows): return np.array([[F(x) for x in row] for row in rows], dtype=object)
def eye(n): return mat([[int(i == j) for j in range(n)] for i in range(n)])
def ones(n): return mat([[1] for _ in range(n)])
def diag(v): return np.diag(np.array([F(x) for x in v], dtype=object))
def inv(A):
    n=len(A); B=np.concatenate([A.copy(),eye(n)],axis=1)
    for i in range(n):
        p=next(j for j in range(i,n) if B[j,i])
        B[[i,p]]=B[[p,i]]; B[i]=B[i]/B[i,i]
        for j in range(n):
            if j!=i: B[j]=B[j]-B[j,i]*B[i]
    return B[:,n:]
def rank(A):
    B=A.copy(); k=0
    for i in range(B.shape[1]):
        p=next((j for j in range(k,len(B)) if B[j,i]),None)
        if p is None: continue
        B[[k,p]]=B[[p,k]]; B[k]=B[k]/B[k,i]
        for j in range(len(B)):
            if j!=k: B[j]=B[j]-B[j,i]*B[k]
        k+=1
        if k==len(B): break
    return k
def zero(A): return all(x==0 for x in A.flat)
def tilt(Q,h):
    n=len(Q); A=Q.copy()
    for i in range(n):
        for j in range(n):
            if i!=j: A[i,j]=Q[i,j]*h[j]/h[i]
        A[i,i]=-sum(A[i,j] for j in range(n) if j!=i)
    return A
def resolvent(Q,alpha): return alpha*inv(alpha*eye(len(Q))-Q)
def record(Q,features,h,alpha):
    n=len(Q); W=diag([x*x/F(n) for x in h]); S=resolvent(tilt(Q,h),alpha)
    G=features.T@W@features; K=features.T@W@S@features
    D=features.T@W@S@S@features; residual=D-K@inv(G)@K
    C=inv(G)@K; L=alpha*(eye(len(G))-inv(C))
    return G,K,D,residual,L
def serial(x):
    if isinstance(x,F): return str(x)
    if isinstance(x,np.ndarray): return [[serial(y) for y in r] for r in x.tolist()]
    if isinstance(x,dict): return {k:serial(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)): return [serial(y) for y in x]
    return x
def survival_interval(A,t,lam=F(64),N=96):
    """Substochastic uniformization with exact rational exponential bounds."""
    P=eye(len(A))+A/lam
    assert all(x>=0 for x in P.flat)
    assert all(sum(r)<=1 for r in P)
    x=lam*t; term=F(1); es=F(1); v=ones(len(A)); s=F(1)
    for j in range(1,N+1):
        term*=x/F(j); es+=term; v=P@v
        s+=term*sum(v[:,0])/F(len(A))
    tail=(term*x/F(N+1))/(1-x/F(N+2))
    return s/(es+tail),(s+tail)/es

out={"scope":"Exact rational synthetic checks; no native samples or acquired calibration."}
Q=mat([[-21,10,10,1],[10,-22,10,2],[10,10,-24,4],[1,2,4,-7]])
H=mat([[F(2,3),F(-1,3),F(2,3),0],[F(-1,3),F(2,3),F(2,3),0],
       [F(2,3),F(2,3),F(-1,3),0],[0,0,0,1]])
Q2=H@Q@H; E=diag([0,0,0,1]); O=ones(4)
assert zero(H@H-eye(4)) and zero(H@O-O) and zero(H@E-E@H)
assert zero(Q2-Q2.T) and zero(Q2@O)
assert all(Q2[i,j]>0 for i in range(4) for j in range(4) if i!=j)
h=[F(1),F(1),F(1),F(2)]
A=tilt(Q,h)[:3,:3]; B=tilt(Q2,h)[:3,:3]; v=ones(3)
jets=[]
for j in range(4):
    Ap=eye(3); Bp=eye(3)
    for _ in range(j): Ap=Ap@A; Bp=Bp@B
    jets.append((v.T@(Ap-Bp)@v)[0,0]/3)
assert jets==[F(0),F(0),F(0),F(-160,27)]
lo,hi=survival_interval(A,F(1,10)); lo2,hi2=survival_interval(B,F(1,10))
gap=(lo-hi2,hi-lo2); assert gap[1]<0
out['passive_gauge']={"Q":Q,"Q_other":Q2,"orthogonal_label_preserving":True,
    "all_passive_visible_laws":"Equal by exact conjugation, not finite sampled checks",
    "biased_survival_derivative_gaps_0_to_3":jets,
    "biased_survival_gap_at_t_1_over_10":gap,
    "gap_float_for_display":[float(x) for x in gap]}

# A source whose COMPLETE passive predictive span misses a controlled direction.
v=mat([[-2],[0],[1],[1]]); Qd=16*(O@O.T/F(4)-eye(4))+F(1,4)*(v@v.T)
alpha=F(128); Ra=resolvent(Qd,F(16)); eB=E@O; eA=O-eB
F3=np.column_stack([eA,eB,(eye(4)-E)@Ra@eB])
G=F3.T@F3/F(4); L0=inv(G)@(F3.T@Qd@F3/F(4))
assert rank(F3)==3 and zero(Qd@F3-F3@L0)
assert zero(E@F3-F3@inv(G)@(F3.T@E@F3/F(4)))
r0=record(Qd,F3,[F(1)]*4,alpha); rb=record(Qd,F3,h,alpha)
assert zero(r0[3]) and not zero(rb[3])
j=next(i for i in range(3) if rb[3][i,i]>0)
new=(eye(4)-E)@resolvent(tilt(Qd,h),alpha)@F3[:,j:j+1]
F4=np.column_stack([F3,new]); assert rank(F4)==4
out['dormant_control_direction']={"Q":Qd,"passive_rank":3,
    "baseline_pulse_defect":r0[3],"finite_bias_defect":rb[3],
    "strict_positive_bias_defect_entry":rb[3][j,j],
    "appended_feature":"1_A S_bias f_"+str(j),"completed_rank":4}

# Add a genuinely hidden independent two-state coordinate; eight states, rank four.
Qs=mat([[-5,5],[5,-5]])
Q8=np.kron(Qd,eye(2))+np.kron(eye(4),Qs)
F8=np.repeat(F4,2,axis=0); E8=np.kron(E,eye(2)); h8=[x for x in h for _ in range(2)]
rr0=record(Q8,F8,[F(1)]*8,alpha); rrb=record(Q8,F8,h8,alpha)
assert zero(rr0[3]) and zero(rrb[3]); G8=rr0[0]
Pi=inv(G8)@(F8.T@E8@F8/F(8)); Hred=eye(4)+Pi
L=rr0[4]; Wb=L@Hred-Hred@rrb[4]
assert zero(F8@Wb-diag((Q8@np.repeat(eB,2,axis=0))[:,0])@F8)
checks=[]
for hb,ha in [(F(3,2),F(5,4)),(F(4),F(1)),(F(1),F(3)),(F(7,5),F(9,8))]:
    HH=hb*Pi+ha*(eye(4)-Pi)
    Lh=inv(HH)@(L@HH-(hb-ha)*Wb)
    hv=[hb if i//2==3 else ha for i in range(8)]
    assert zero(tilt(Q8,hv)@F8-F8@Lh)
    checks.append([hb,ha])
out['finite_record_completion']={"native_states":8,"predictive_rank":4,
    "label_count":2,"alpha":alpha,"source_exit_ceiling":max(-Q8[i,i] for i in range(8)),
    "zero_baseline_and_bias_defects":True,"new_bias_checks":checks,
    "constant_preserved":bool(zero(L@inv(G8)@(F8.T@ones(8)/F(8)))),
    "raw_gram_condition_number_float_diagnostic":float(np.linalg.cond(np.array(G8,dtype=float)))}

# A false compression test using one future sample includes variance, unlike our Gram.
one_step=Ra@eB
second=Ra@(eB*eB)
intrinsic=second-one_step*one_step
assert any(x>0 for x in intrinsic.flat)
out['trajectory_variance_correction']={"one_future_variance_nonzero":True,
    "note":"A single-future square is not the squared conditional expectation."}
out['result']='PASS'
p=Path(__file__).with_name('PULSE_CLOSURE_EXACT_RESULTS.json')
p.write_text(json.dumps(serial(out),indent=2)+'\n')
print(json.dumps({"result":"PASS","checks":["full passive gauge equivalence",
 "rigorous finite-time intervention separation","dormant controlled dimension",
 "actual controlled-feature expansion","eight-state/four-coordinate exact completion"],
 "gap_at_t_0_1":[float(x) for x in gap],"output":str(p)},indent=2))
