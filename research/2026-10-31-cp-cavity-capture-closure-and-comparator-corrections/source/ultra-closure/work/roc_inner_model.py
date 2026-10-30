"""A globally sufficient ROC cone via the deflated acoustic Schur matrix.

This numerical model uses exact polynomial construction followed by a
fixed Bernstein inner approximation. Solver output is a proposal until
rationalized and rigorously received. No finite point admission is used.
"""
from pathlib import Path
from fractions import Fraction as R
from itertools import combinations,product
from math import comb,ceil,log2
import json,sys,time
import numpy as np, scipy.linalg as la,cvxpy as cp
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root/'work'));import heat_model as h
b,r,ca=h.b,h.r,h.ca;start=time.perf_counter();qc=json.loads((root/'outputs/quadratic_boundary/certificate.json').read_text());powers=qc['cubic_powers'];rawbasis=[list(map(R,row)) for row in qc['normal_form_basis']];scales=[R(2)**(-ceil(log2(max(float(abs(x)) for x in row)))) for row in rawbasis];basis=[[v*s for v in row] for row,s in zip(rawbasis,scales)];CP=[{tuple(pw):v for pw,v in zip(powers,row) if v} for row in basis];qpowers=[pw for pw in product(range(3),repeat=4) if sum(pw)==2 and pw!=(1,0,0,1)];QP=[{pw:R(1)} for pw in qpowers];assert len(QP)==9
s,t=b.var(2,0),b.var(2,1);one={(0,0):R(1)};zero={};null1=list(map(R,h.base['ray']['A0']));null2=[-null1[1],null1[0],null1[3],-null1[2]]
def pmat(A,B):return [[b.add(*(b.mul(x,y) for x,y in zip(row,col))) for col in zip(*B)] for row in A]
def ptrans(A):return list(map(list,zip(*A)))
def contract(P,images):return r.compose(P,images,2)
charts=[]
for side,oc in product((0,1),repeat=2):
 x,y=(one,s) if oc==0 else (s,one);xi=(one,t) if side==0 else (t,one);ray=[b.mul(x,xi[0]),b.mul(x,xi[1]),b.mul(y,xi[0]),b.mul(y,xi[1])];UA=[[x,zero,b.scale(y,-1),zero],[zero,x,zero,b.scale(y,-1)],[y,zero,x,zero],[zero,y,zero,x]];null=null1 if side==0 else null2;P0=[[null[i]]+[R(int(i==j)) for j in range(3)] for i in range(4)];PU=pmat(UA,[[{(0,0):v} if v else {} for v in row] for row in P0]);HH=[[contract(p,ray) for p in row] for row in h.HF];TOP=pmat(ptrans(PU),pmat(HH,PU))
 for i in range(4):
  for j in range(4):
   n=int(i==0)+int(j==0);assert all(ee[1]>=n for ee in TOP[i][j]);TOP[i][j]={(ee[0],ee[1]-n):v for ee,v in TOP[i][j].items()}
 CC=[]
 for P in CP:
  DC=[contract(b.diff(P,i),ray) for i in range(4)];col=[b.add(*(b.mul(PU[i][j],DC[i]) for i in range(4))) for j in range(4)];assert all(ee[1]>=1 for ee in col[0]);col[0]={(ee[0],ee[1]-1):v for ee,v in col[0].items()};CC.append(col)
 # Positive congruence diag(1/|u| I4, |u|) reduces the top output
 # factor |u|^4 to |u|^2 and multiplies the scalar block by |u|^2.
 norm=b.add(one,b.mul(s,s))
 def divide_norm(P):
  rem=dict(P);out={}
  while rem and max(e[0] for e in rem)>=2:
   ee=max(rem);v=rem[ee];f=(ee[0]-2,ee[1]);out[f]=out.get(f,R(0))+v;rem=b.add(rem,b.scale(b.mul({f:R(1)},norm),-v))
  assert not rem
  return {e:v for e,v in out.items() if v}
 TOP=[[divide_norm(p) for p in row] for row in TOP]
 QQ=[b.mul(norm,b.scale(contract(P,ray),2)) for P in QP];charts.append((TOP,CC,QQ))
 assert all(ee[0]<=4 and ee[1]<=2 for family in ([p for row in TOP for p in row],[p for col in CC for p in col],QQ) for p in family for ee in p)

def bw(a,c,n):return np.array([[float(sum((R(comb(k,j)*comb(i,j),comb(n,j))*a**(k-j)*(c-a)**j for j in range(min(k,i)+1)),R(0))) for k in range(n+1)] for i in range(n+1)])
def coeffs(polys,box):
 out=np.zeros((len(polys),5,3))
 for k,P in enumerate(polys):
  for ee,v in P.items():out[(k,)+ee]=float(v)
 return np.einsum('ia,jb,kab->ijk',bw(box[0],box[1],4),bw(box[2],box[3],2),out,optimize=True).reshape(15,len(polys))

tops=[];cross=[];bottom=[];metadata=[];cover=[]
for ch,(TOP,CC,QQ) in enumerate(charts):
 stack=[((R(-1),R(1),R(-1),R(1)),0)]
 while stack:
  box,depth=stack.pop();A=coeffs([p for row in TOP for p in row],box).reshape(15,4,4);chol=[]
  try:
   for AA in A:chol.append(la.cholesky((AA+AA.T)/2,lower=True))
  except la.LinAlgError:
   assert depth<36,(ch,box,la.eigvalsh(A[7]).tolist());axis=1;l,u=box[2*axis:2*axis+2];mid=(l+u)/2;b1=list(box);b2=list(box);b1[2*axis+1]=mid;b2[2*axis]=mid;stack.extend(((tuple(b1),depth+1),(tuple(b2),depth+1)));continue
  # Refine the already-positive leading cover to reduce admission loss.
  if max(float(box[1]-box[0]),float(box[3]-box[2]))>.25:
   axis=0 if box[1]-box[0]>=box[3]-box[2] else 1;mid=(box[2*axis]+box[2*axis+1])/2;b1=list(box);b2=list(box);b1[2*axis+1]=mid;b2[2*axis]=mid;stack.extend(((tuple(b1),depth+1),(tuple(b2),depth+1)));continue
  G=coeffs([p for col in CC for p in col],box).reshape(15,12,4).transpose(0,2,1);Q=coeffs(QQ,box)
  for k,(H,C) in enumerate(zip(A,chol)):
   W=la.solve_triangular(C,np.eye(4),lower=True);cross.append(W@G[k]);bottom.append(Q[k]);tops.append(H);metadata.append((ch,box,k))
  cover.append((ch,box))
cross=np.array(cross);bottom=np.array(bottom);N=len(cross)
print('deflated global ROC inner model',N,'SOC coefficients',len(cover),'boxes','seconds',time.perf_counter()-start,flush=True)

class Model:
 def __init__(self):
  self.c=cp.Variable(12);self.q=cp.Variable(9);self.ell=cp.Parameter(12);self.qmom=cp.Parameter(9);gg=cp.reshape(cross.reshape(N*4,12)@self.c,(N,4),order='C');constraints=[cp.sum(cp.square(gg),axis=1)<=bottom@self.q,cp.norm(self.c,'inf')<=1e5,cp.norm(self.q,'inf')<=1e7];self.problem=cp.Problem(cp.Minimize(self.ell@self.c+self.qmom@self.q),constraints)
 def solve(self,ell,qmom):
  self.ell.value=np.array(ell,float);self.qmom.value=np.array(qmom,float);self.problem.solve(solver='CLARABEL',tol_gap_abs=1e-8,tol_gap_rel=1e-8,tol_feas=1e-9,max_iter=300)
  if self.c.value is None:return None
  c=np.array(self.c.value);q=np.array(self.q.value);slack=bottom@q-np.sum(np.einsum('nik,k->ni',cross,c)**2,axis=1);return {'status':self.problem.status,'objective':float(self.problem.value),'cubic_coordinates':c.tolist(),'quadratic_coordinates':q.tolist(),'least_numerical_Bernstein_slack':float(np.min(slack))}

if __name__=='__main__':
 out={'cubic_basis':[[str(v) for v in row] for row in basis],'cubic_powers':powers,'quadratic_powers':qpowers,'cover':[{'chart':ch,'box':list(map(str,box))} for ch,box in cover],'scope':'Exact polynomial deflation and numerical globally sufficient Bernstein inner cone. Solver output still requires independent rigorous reception.'};(root/'work/roc_inner_model.json').write_text(json.dumps(out,indent=2)+'\n');np.savez(root/'work/roc_inner_model.npz',cross=cross,bottom=bottom,top=np.array(tops))
