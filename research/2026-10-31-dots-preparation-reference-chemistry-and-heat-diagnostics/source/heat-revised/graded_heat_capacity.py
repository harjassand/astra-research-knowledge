"""Proposal: graded heat completion for the actual near-boundary ROC fixture.

A positive result is only numerical until a universal exact certificate is
reconstructed. A failure is a limitation of this primitive/Gram ansatz.
"""
from pathlib import Path
from fractions import Fraction as R
from itertools import combinations,product
import sys,json,time
import numpy as np,scipy.linalg as la,cvxpy as cp
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root/'outputs/acoustic_capacity'))
from receive import r,b,ca,dot,quadratic
start=time.perf_counter();F,C,T=r.m.acquired();base=json.loads((root/'outputs/hopf_structure/certificate.json').read_text());P=[b.literal(rows,4) for rows in base['primitive']]
HF=[[b.diff(b.diff(F,i),j) for j in range(4)] for i in range(4)];HC=[[b.diff(b.diff(C,i),j) for j in range(4)] for i in range(4)];Avars=[b.var(4,i) for i in range(4)]
Omega={}
for i,j in combinations(range(4),2):Omega[i,j]=b.add(b.mul(T,b.add(b.diff(P[j],i),b.scale(b.diff(P[i],j),-1))),b.scale(b.add(b.mul(Avars[i],P[j]),b.scale(b.mul(Avars[j],P[i]),-1)),-2))
L1=np.zeros((4,6));L2=np.zeros((4,6))
for i,j in enumerate((0,1,3,4)):L1[i,j]=1
for i,j in enumerate((1,2,4,5)):L2[i,j]=1
pairs4=list(combinations(range(4),2));pairs6=list(combinations(range(6),2));Wedges=[]
for i,j in pairs4:
 O=np.zeros((4,4));O[i,j]=1;O[j,i]=-1;W=L1.T@O@L2;Wedges.append((W+W.T)/2)
Wedges=np.array(Wedges)
def poly_arrays(poly):return np.array(list(poly),int),np.array([float(v) for v in poly.values()])
def value(poly,v):
 pw,co=poly_arrays(poly);return float(np.prod(np.asarray(v)[None,:]**pw,axis=1)@co) if len(co) else 0.
FHA=[[poly_arrays(p) for p in row] for row in HF];ON=[poly_arrays(Omega[pair]) for pair in pairs4]
def eval_array(data,v):
 pw,co=data;return float(np.prod(v[None,:]**pw,axis=1)@co) if len(co) else 0.
def SF(v):
 v=np.asarray(v,float);tt=v@v;H=np.array([[eval_array(d,v) for d in row] for row in FHA]);omega=np.array([eval_array(d,v)/tt**2 for d in ON]);return L1.T@H@L1+L2.T@H@L2+np.einsum('p,pij->ij',omega,Wedges)
def SF_exact(v,deriv=None):
 tt=sum(z*z for z in v);H=[[b.evaluate(b.diff(p,deriv) if deriv is not None else p,v) for p in row] for row in HF];out=[[R(0) for _ in range(6)] for _ in range(6)]
 for aa,LL in enumerate((L1,L2)):
  inds=(0,1,3,4) if aa==0 else (1,2,4,5)
  for i in range(4):
   for j in range(4):out[inds[i]][inds[j]]+=H[i][j]
 for pair,W in zip(pairs4,Wedges):
  N=Omega[pair]
  co=b.evaluate(N,v)/tt**2 if deriv is None else b.evaluate(b.add(b.scale(b.mul(T,b.diff(N,deriv)),1),b.scale(b.mul(Avars[deriv],N),-4)),v)/tt**3
  for i in range(6):
   for j in range(6):out[i][j]+=co*R(float(W[i,j]))
 return out
# Closed linear two-forms have 24 coefficients and four closure equations.
dependent=[pairs4.index((i,j))*4+k for i,j,k in combinations(range(4),3)];free=[i for i in range(24) if i not in dependent];V=np.zeros((24,20))
for k,j in enumerate(free):V[j,k]=1
for i,j,k in combinations(range(4),3):V[pairs4.index((i,j))*4+k]=V[pairs4.index((i,k))*4+j]-V[pairs4.index((j,k))*4+i]
X0=np.zeros((4,6,6));XB=np.zeros((4,6,6,80))
for a in range(4):
 ea=[R(int(i==a)) for i in range(4)];H=np.array([[float(b.evaluate(p,ea)) for p in row] for row in HC]);X0[a]=(L1.T@H@L1+L2.T@H@L2)/2
 for l in range(20):XB[a,:,:,l]=sum(V[p*4+a,l]*Wedges[p]/2 for p in range(6))
 for k,(i,j) in enumerate(pairs6):XB[a,i,j,20+15*a+k]=1;XB[a,j,i,20+15*a+k]=-1
coeff=cp.Variable(80);oq=cp.Variable(6);nu=cp.Variable(nonneg=True)
def X(v):
 v=np.array(v,float);const=np.einsum('a,aij->ij',v,X0);co=np.einsum('a,aijl->ijl',v,XB).reshape(36,80);return const+cp.reshape(co@coeff,(6,6),order='C')
DQ=2*nu*np.diag([1,2,1,1,2,1])+sum(oq[p]*Wedges[p] for p in range(6));constraints=[DQ>>0]
av=list(map(R,base['ray']['A0']));aa,bb,cc,dd=av;av2=[-bb,aa,dd,-cc];jets=[]
for av,hindex in ((av,0),(av2,2)):
 S=SF_exact(av);assert all(S[hindex][j]==0 for j in range(6));I=[j for j in range(6) if j!=hindex];Ds=[SF_exact(av,a) for a in range(4)];B=[[Ds[a][j][hindex] for a in range(4)] for j in I];RR=[R(1 if i==(0 if hindex==0 else 1) else 0) for i in range(4)];H=[[b.evaluate(p,RR) for p in row] for row in HF]
 top=[[S[i][j] for j in I]+B[k] for k,i in enumerate(I)]+[[B[j][a] for j in range(5)]+H[a] for a in range(4)]
 r.psd(top);assert b.rank(top)==7
 vals,vecs=la.eigh(np.array(top,float));W=(vecs[:,2:]/np.sqrt(vals[2:])[None,:]).T;N=vecs[:,:2]
 jets.append((np.array(av,float),hindex,I,W,N));print('jet',hindex,'positive eigenvalues',vals[2:].tolist(),flush=True)
 for theta in np.linspace(0,np.pi,12,endpoint=False):
  c,s=np.cos(theta),np.sin(theta);UA=np.array([[c,0,-s,0],[0,c,0,-s],[s,0,c,0],[0,s,0,c]]);UH=np.kron(np.array([[c,-s],[s,c]]),np.eye(3));Pperp=UH[:,I];kh=UH[:,hindex]
  Y=cp.vstack([Pperp.T@X(UA@np.array(av,float))@UH]+[cp.reshape(kh@X(UA[:,a])@UH,(1,6),order='C') for a in range(4)])
  constraints +=[N.T@Y==0,cp.bmat([[np.eye(7),W@Y],[(W@Y).T,UH.T@DQ@UH]])>>0]
# Interior sphere points constrain the whole scale Gram, not just the jets.
rng=np.random.default_rng(810431);points=[]
for _ in range(100):
 v=rng.normal(size=4);v/=la.norm(v);points.append(v)
for vals0 in product((-1.,0,1.),repeat=4):
 v=np.array(vals0)
 if la.norm(v)>0:points.append(v/la.norm(v))
for v in points:
 S=SF(v);vals,vecs=la.eigh(S)
 if vals[0]<-1e-8:raise AssertionError(('F completion numerical mismatch',v,vals))
 W=(vecs/np.sqrt(np.maximum(vals,1e-12))[None,:]).T
 constraints.append(cp.bmat([[np.eye(6),W@X(v)],[(W@X(v)).T,DQ]])>>0)
# The independently admitted ROC boundary supplies an exact critical
# background. Float sphere grids can miss this narrow positive valley.
qc=json.loads((root/'outputs/quadratic_boundary/certificate.json').read_text());uu=list(map(R,qc['lower_rank_one_output']));nn=list(map(R,qc['lower_rank_one_spatial']));ray=[uu[i]*nn[j] for i in range(2) for j in range(2)]
H=[[b.evaluate(p,ray) for p in row] for row in HF];gg=[b.evaluate(b.diff(C,i),ray) for i in range(4)];critical=[-v for v in r.m.linear_solve(H,gg)]
Scritical=SF_exact(critical);hh=[uu[0]*nn[0]**2,uu[0]*nn[0]*nn[1],uu[0]*nn[1]**2,uu[1]*nn[0]**2,uu[1]*nn[0]*nn[1],uu[1]*nn[1]**2]
assert quadratic(Scritical,hh)==sum(v*v for v in nn)*quadratic([[b.evaluate(p,critical) for p in row] for row in HF],ray)
def exact_whitener(mat):
 n=len(mat);LL=[[R(int(i==j)) for j in range(n)] for i in range(n)];DD=[]
 for j in range(n):
  pp=mat[j][j]-sum(LL[j][k]**2*DD[k] for k in range(j));assert pp>0;DD.append(pp)
  for i in range(j+1,n):LL[i][j]=(mat[i][j]-sum(LL[i][k]*LL[j][k]*DD[k] for k in range(j)))/pp
 return np.diag(1/np.sqrt(np.array(DD,float)))@la.solve_triangular(np.array(LL,float),np.eye(n),lower=True)
Wcrit=exact_whitener(Scritical);constraints.append(cp.bmat([[np.eye(6),Wcrit@X(critical)],[(Wcrit@X(critical)).T,DQ]])>>0)
constraints.append(nu>=float(R(qc['ROC_lower'])))
print('critical background normalized', (np.array(critical,float)/la.norm(np.array(critical,float))).tolist(),'SF inverse factor norm',float(la.norm(Wcrit)),flush=True)
problem=cp.Problem(cp.Minimize(nu+1e-14*(cp.sum_squares(coeff)+cp.sum_squares(oq))),constraints);problem.solve(solver='CLARABEL',tol_feas=1e-8,tol_gap_abs=1e-7,tol_gap_rel=1e-8,max_iter=250)
out={'status':problem.status,'nu':None if nu.value is None else float(nu.value),'primitive_closed_linear_two_form':None if coeff.value is None else (V@coeff.value[:20]).reshape(6,4).tolist(),'skew_cross_coefficients':None if coeff.value is None else coeff.value[20:].reshape(4,15).tolist(),'quadratic_two_form':None if oq.value is None else oq.value.tolist(),'sphere_points':len(points),'acoustic_jet_constraints':24,'seconds':time.perf_counter()-start,'scope':'Numerical sufficient heat-Gram proposal on a finite sphere set plus exact leading acoustic jet matrices. Neither QC nor failure of QC is inferred without a universal exact certificate.'}
(root/'work/graded_heat_capacity_proposal.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k] for k in ('status','nu','sphere_points','acoustic_jet_constraints','seconds')},indent=2),flush=True)
