"""Exact finite SDP for the rank-three Hessian covariance face.

R(x,y)=T(x,y) tensor (x,y). The 5x5 ROC block is a homogeneous
binary quartic matrix, hence a degree-two matrix SOS. Its two acoustic
kernel vectors remove two Gram coordinates, giving one 13x13 PSD Gram.
This is lossless on the conic, not a finite direction test. Extending a
strict negative conic result to global ROC still requires its own proof.
"""
from pathlib import Path
from fractions import Fraction as R
from itertools import product
import json,sys,time
import numpy as np, cvxpy as cp
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root/'work'));import roc_inner_model as m
b,ca,r,h=m.b,m.ca,m.r,m.h
T=[[R(1),R(0)],[R(0),-R(981203,385371)]]
x,y=b.var(2,0),b.var(2,1);xi=[x,y];u=[b.add(*(b.scale(p,v) for p,v in zip(xi,row))) for row in T];ray=[b.mul(u[i],xi[j]) for i,j in product(range(2),repeat=2)];HH=[[r.compose(P,ray,2) for P in row] for row in h.HF];CC=[[r.compose(b.diff(P,i),ray,2) for i in range(4)] for P in m.CP];Hcoef=np.array([[[float(P.get((4-j,j),0))/256 for P in row] for row in HH] for j in range(5)]);Ccoef=np.array([[[float(col[i].get((4-j,j),0))/16 for c,col in enumerate(CC)] for i in range(4)] for j in range(5)]);null1=list(map(R,h.base['ray']['A0']));null2=[-null1[1],null1[0],null1[3],-null1[2]]
def rot(A,u):
 xx,yy=u;return [xx*A[0]-yy*A[2],xx*A[1]-yy*A[3],yy*A[0]+xx*A[2],yy*A[1]+xx*A[3]]
kernels=[]
for j,K,u0 in ((0,null1,[T[0][0],T[1][0]]),(2,null2,[T[0][1],T[1][1]])):
 kk=rot(K,u0);v=[R(0)]*15
 for i in range(4):v[5*j+i]=kk[i]
 kernels.append(v)
 assert all(sum(row[i]*kk[i] for i in range(4))==0 for row in [[b.evaluate(P,[R(1),R(0)] if j==0 else [R(0),R(1)]) for P in rr] for rr in HH])
piv=[max(range(15),key=lambda i:abs(v[i])) for v in kernels];free=[i for i in range(15) if i not in piv];E=[[R(int(i==j)) for j in free] for i in range(15)]
for v,p in zip(kernels,piv):
 for col,j in enumerate(free):E[p][col]=-v[j]/v[p]
assert ca.mm(ca.transpose(kernels),E) if False else all(sum(v[i]*E[i][j] for i in range(15))==0 for v in kernels for j in range(13))
Ef=np.array(E,float);blocks=[Ef[5*j:5*j+5] for j in range(3)];Tin=np.linalg.inv(np.array(T,float));A=[b.var(4,i) for i in range(4)];Gm=[[b.add(*(b.scale(A[2*k+j],Tinv) for k,Tinv in enumerate(row))) for j in range(2)] for row in [[R(1),R(0)],[R(0),1/T[1][1]]]];a,c=Gm[0][0],Gm[1][1];bb=b.scale(b.add(Gm[0][1],Gm[1][0]),R(1,2));Qext=[b.scale(P,R(1,2)) for P in (b.mul(a,a),b.mul(a,bb),b.mul(bb,bb),b.mul(bb,c),b.mul(c,c))]

class Model:
 def __init__(self):
  self.G=cp.Variable((13,13),symmetric=True);self.c=cp.Variable(12);self.q=cp.Variable(5);self.ell=cp.Parameter(12);self.qmom=cp.Parameter(5);constraints=[self.G>>0]
  for j in range(5):
   coeff=sum(blocks[a]@self.G@blocks[bb].T for a in range(3) for bb in range(3) if a+bb==j);cross=Ccoef[j]@self.c
   for a in range(4):
    for bb in range(a,4):constraints.append(coeff[a,bb]==Hcoef[j,a,bb])
    constraints.append(coeff[a,4]==cross[a])
   constraints.append(coeff[4,4]==self.q[j])
  self.constraints=constraints;self.problem=cp.Problem(cp.Minimize(self.ell@self.c+self.qmom@self.q),constraints)
 def solve(self,ell,qmom):
  self.ell.value=np.array(ell,float);self.qmom.value=np.array(qmom,float);self.problem.solve(solver='CLARABEL',tol_gap_abs=1e-9,tol_gap_rel=1e-9,tol_feas=1e-10,max_iter=400)
  if self.c.value is None:return None
  c=np.array(self.c.value);q=np.array(self.q.value);G=np.array(self.G.value);residual=0.
  for j in range(5):
   coeff=sum(blocks[a]@G@blocks[bb].T for a in range(3) for bb in range(3) if a+bb==j);target=np.zeros((5,5));target[:4,:4]=Hcoef[j];target[:4,4]=Ccoef[j]@c;target[4,:4]=target[:4,4];target[4,4]=q[j];residual=max(residual,float(np.max(abs(coeff-target))))
  return {'status':self.problem.status,'objective':float(self.problem.value),'cubic_coordinates':c.tolist(),'quadratic_coordinates':q.tolist(),'Gram':G.tolist(),'minimum_numerical_Gram_eigenvalue':float(np.linalg.eigvalsh(G)[0]),'maximum_numerical_coefficient_residual':residual,'scope':'Numerical solution of the lossless conic ROC SDP. Strict negative candidates require rational conic Gram and global ROC extension, plus exact actual-field verification.'}

if __name__=='__main__':
 out={'T':[[str(v) for v in row] for row in T],'Gram_feature_projection':[[str(v) for v in row] for row in E],'fixed_acoustic_Gram_kernels':[list(map(str,v)) for v in kernels],'Gram_dimension':13,'conic_rank_one_map':[sorted([list(ee)+[v.numerator,v.denominator] for ee,v in P.items()]) for P in ray],'scope':'Exact lossless binary matrix-SOS reduction for this covariance face; every direction on the conic is retained. Actual-field QC remains a separate moment-extension question.'};(root/'work/conic_capacity_model.json').write_text(json.dumps(out,indent=2)+'\n');print('Conic 13x13 Gram model built exactly.',flush=True)
