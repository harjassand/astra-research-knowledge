import sympy as s,json
from pathlib import Path
Q=s.Rational;I=s.eye(2)
T=s.Matrix([[Q(1,2),Q(1,6),Q(1,3)],[Q(1,3),Q(1,2),Q(1,6)],[Q(1,6),Q(1,3),Q(1,2)]])
root=s.Matrix([Q(1,3),Q(2,3),Q(2,3)]);v=s.Matrix([0,0,1])-root;V=(s.eye(3)-2*v*v.T/(v.T*v)[0])[:,:2].T
R0=[V[:,i]*V[:,i].T for i in range(3)];z=[root[i]*V[:,i] for i in range(3)]
e=Q(1,10000);delta=Q(1,10000);prior=[Q(1,3)]*3
R=[(x+e*I)/(1+3*e) for x in R0];B=[s.diag(delta*prior[i],R[i]) for i in range(3)]
H=[s.zeros(3) for i in range(3)]
for i in range(3):H[i][0,1:3]=z[i].T;H[i][1:3,0]=z[i]
assert sum(H,s.zeros(3))==s.zeros(3)
q=Q(3,20);EE=(q*s.eye(3)).col_join((1-q)*s.ones(1,3))
def apply(M,X):return [sum((M[y,i]*X[i] for i in range(3)),s.zeros(3)) for y in range(M.rows)]
def sld(M):
 score=0
 for A,K in zip(apply(M,B),apply(M,H)):
  zz=K[1:3,0];rr=A[1:3,1:3];dd=A[0,0];vv=2*(rr+dd*I).inv()*zz;O=s.zeros(3);O[0,1:3]=vv.T;O[1:3,0]=vv
  assert A*O+O*A==2*K
  score+=s.trace(K*O)
 return s.factor(score)
GE=sld(EE);GT=sld(T);gap=s.factor(GT-GE);assert gap>0
tr=sum(s.trace(b) for b in B);assert tr==2+delta
step=Q(1,1000)
plus=[(bb+step*hh)/tr for bb,hh in zip(B,H)];minus=[(bb-step*hh)/tr for bb,hh in zip(B,H)]
for bs in [plus,minus]:
 assert sum(s.trace(bb) for bb in bs)==1
 assert all(bb==bb.T and all(bb[:j,:j].det()>0 for j in [1,2,3]) for bb in bs)
assert sum(plus,s.zeros(3))==sum(minus,s.zeros(3))
# Exact covariance/radius threshold at the cyclic optimum.
w=s.ones(3,1)/3;qc=Q(2,11);DD=T.row_join(w) # overwritten below
D=(T-(1-qc)*w*s.ones(1,3))/qc;D=D.row_join(w)
Ec=(qc*s.eye(3)).col_join((1-qc)*s.ones(1,3))
assert D*Ec==T
for i in range(3):
 ti=T[:,i];C=s.diag(*ti)-D*s.diag(*Ec[:,i])*D.T
 chi=sum((w[y]-ti[y])**2/ti[y] for y in range(3));assert chi==qc/(1-qc)
 assert C==s.diag(*ti)-ti*ti.T-(1-qc)/qc*(ti-w)*(ti-w).T
 assert all(val>=0 for val in C.eigenvals())
out={'pass':True,'reference_dimension':3,'RLD_vector_reference_dimension':2,'reveal_q':'3/20','flag_delta':str(delta),'baseline_regularization':str(e),'SLD_target_advantage':str(gap),'SLD_target_advantage_decimal':float(gap),'state_pair_step':str(step),'binary_MMSE_target_advantage':str(s.factor(step**2*gap/tr)),'same_reference_marginal':True,'all_states_faithful':True,'signed_lift_exact_at_threshold_2_over11':True}
assert json.loads(Path(__file__).with_name('sld_flag_lift_check.json').read_text()) == out, 'Exact fixture mismatch';print(out)
