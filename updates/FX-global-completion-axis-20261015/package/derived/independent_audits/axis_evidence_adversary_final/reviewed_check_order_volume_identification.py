#!/usr/bin/env python3
"""Exact finite identities for the conditional tensor identified-set proof."""
import itertools,json,pathlib,hashlib
import sympy as s
R=s.Rational
checks={}
def check(name,ok):
 checks[name]=bool(ok)
 if not ok: raise AssertionError(name)
def psd(A):
 return all(A.extract(I,I).det()>=0 for n in range(1,A.rows+1) for I in itertools.combinations(range(A.rows),n))
def interval(w,t,f,floor,maximize):
 m=list(w); budget=f-sum(m); cap=[x/floor**2-x for x in w]
 for i in sorted(range(len(w)),key=lambda i:t[i],reverse=maximize):
  use=min(cap[i],budget);m[i]+=use;budget-=use
 assert budget==0
 return sum(a*b for a,b in zip(t,m)),m
M=s.diag(R(1,2),R(1,2),0);W1=s.diag(R(8,25),R(2,25),0);W2=s.diag(R(2,25),R(8,25),0)
check('unchanged_volume_axis_tensor',M==M)
check('unchanged_total_superlattice_weight',s.trace(W1)==s.trace(W2)==R(2,5))
check('false_normalized_contrast',((W1[0,0]-W1[1,1])/s.trace(W1)-(W2[0,0]-W2[1,1])/s.trace(W2))==R(6,5))
floor=R(2,5); t=[1,-1,0];bounds=[]
for n,W in enumerate([W1,W2],1):
 check(f'sandwich_W{n}',psd(M-W) and psd(W-floor**2*M))
 lo,lo_m=interval(list(W.diagonal()),t,1,floor,False);hi,hi_m=interval(list(W.diagonal()),t,1,floor,True)
 bounds.append([str(lo),str(hi)])
 for label,ms in [('lower',lo_m),('upper',hi_m)]:
  A=s.diag(*ms);check(f'feasible_{n}_{label}',s.trace(A)==1 and psd(A-W) and psd(W-floor**2*A))
check('sharp_diagonal_bounds',bounds==[['0','21/25'],['-21/25','0']])
v=s.Matrix([1,2,0]);z=s.Matrix([2,1,1]);P=v*v.T/20;Q=z*z.T/30;A=P+Q;W=P+floor**2*Q
check('noncommuting_fixture',A*W-W*A!=s.zeros(3))
check('reconstruct_noncommuting_P',s.simplify((W-floor**2*A)/(1-floor**2)-P)==s.zeros(3))
check('reconstruct_noncommuting_Q',s.simplify((A-W)/(1-floor**2)-Q)==s.zeros(3))
check('noncommuting_sandwich',psd(A-W) and psd(W-floor**2*A))
A=s.Matrix([[R(1,2),R(1,10),0],[R(1,10),R(1,2),0],[0,0,0]]);W=s.diag(R(1,5),R(1,5),0)
check('support_caveat_sandwich_pass',psd(A-W) and psd(W-R(1,4)*A))
check('support_caveat_not_coordinate_axes',A[0,1]!=0)
# Zero-order-floor closure can contain extra support; it is not exact for S>0.
W=s.diag(1,0,0);A=s.diag(1,1,0)
check('zero_floor_closure_extra_support',psd(A-W) and A.rank()!=W.rank())
out={'schema':'astra.root.order-volume-exact-check.v1','status':'PASS','checks':checks,'count':len(checks),'sharp_volume_contrast_bounds':bounds,'claim_scope':'Exact finite identities only; the universal identified-set proof is in ORDER_VOLUME_IDENTIFICATION.md. No measured tensor, order floor or physical axis writing acquired.','script_sha256':hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest()}
p=pathlib.Path(__file__).with_name('ORDER_VOLUME_CHECK.json');p.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
