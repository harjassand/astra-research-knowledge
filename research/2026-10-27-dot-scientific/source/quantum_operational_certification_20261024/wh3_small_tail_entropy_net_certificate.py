"""Rigorous finite-net proof of the ENTIRE logical entropy face at t=1/4.
NumPy eigensystems are proposals only: every one has an outward interval
residual and orthogonality certificate. The cover and continuity error are analytic.
"""
import sympy as s,numpy as np,mpmath as mp,json,time,resource
from pathlib import Path
mp.mp.dps=50;mp.iv.dps=40;iv=mp.iv;start=time.perf_counter();m=64;eta=iv.mpf(1)/10**8;tol=mp.mpf('1e-10')
# Exact physical setup. The four-dimensional ambient kernel is removed exactly.
e=s.eye(9);psi=(4*e[:,1]+4*e[:,3]+4*e[:,7]+e[:,8])/7;phi=e[:,0];V=s.Matrix.hstack(psi,phi)
q0=e[:,4]+e[:,5]/4;q1=e[:,7]-e[:,1]-e[:,2]/4;q2=e[:,0]-e[:,4]
O=s.Matrix.hstack(e[:,6],-e[:,3],4*q0/s.sqrt(17),4*q1/s.sqrt(33),s.sqrt(s.Rational(17,18))*(q2+s.Rational(16,17)*q0))
assert s.simplify(O.T*O)==s.eye(5)
Ks=[]
for i,j in [(1,2),(2,0),(0,1)]:
 W=s.zeros(3);W[i,j]=1/s.sqrt(2);W[j,i]=-1/s.sqrt(2)
 A=s.kronecker_product(W,s.eye(3))*V
 assert s.simplify(O*O.T*A-A)==s.zeros(9,2)
 Ks.append(s.simplify(O.T*A))
N00=s.simplify(sum([K[:,0]*K[:,0].T for K in Ks],s.zeros(5)));N11=s.simplify(sum([K[:,1]*K[:,1].T for K in Ks],s.zeros(5)));NX=s.simplify(sum([K[:,0]*K[:,1].T+K[:,1]*K[:,0].T for K in Ks],s.zeros(5)))
M00=s.Matrix([[16,0,0],[0,32,4],[0,4,1]])/49;M11=s.diag(1,0,0);MX=s.Matrix([[0,s.Rational(4,7),0],[s.Rational(4,7),0,0],[0,0,0]])
def exact(x):
 if x.is_Rational:return iv.mpf(int(x.p))/int(x.q)
 if x.is_Add:return sum((exact(a) for a in x.args),iv.mpf(0))
 if x.is_Mul:
  y=iv.mpf(1)
  for a in x.args:y*=exact(a)
  return y
 if x.is_Pow:return exact(x.base)**exact(x.exp)
 raise TypeError(x)
def convert(X):return [[exact(X[i,j]) for j in range(X.cols)] for i in range(X.rows)]
NC=[convert(X) for X in [N00,N11,NX]];MC=[convert(X) for X in [M00,M11,MX]]
def upper(x):return mp.mpf(x._mpi_[1])
def lower(x):return mp.mpf(x._mpi_[0])
def absupper(x):return max(abs(lower(x)),abs(upper(x)))
def mix(C,x,c):return [[x*C[0][i][j]+(1-x)*C[1][i][j]+c*C[2][i][j] for j in range(len(C[0]))] for i in range(len(C[0]))]
worst_res=mp.mpf(0);worst_orth=mp.mpf(0)
def entropy_proposal(A):
 global worst_res,worst_orth
 d=len(A);mid=np.array([[float((lower(x)+upper(x))/2) for x in row] for row in A]);lam,Q=np.linalg.eigh(mid)
 assert max(abs(lam))<2
 qi=[[iv.mpf(float(Q[i,j])) for j in range(d)] for i in range(d)];li=[iv.mpf(float(x)) for x in lam]
 err=mp.mpf(0);orth=mp.mpf(0)
 for i in range(d):
  for j in range(d):
   rec=sum((qi[i][k]*li[k]*qi[j][k] for k in range(d)),iv.mpf(0))
   err=max(err,absupper(A[i][j]-rec))
   inner=sum((qi[k][i]*qi[k][j] for k in range(d)),iv.mpf(0))-int(i==j)
   orth=max(orth,absupper(inner))
 err*=d;orth*=d;assert err<tol and orth<tol
 worst_res=max(worst_res,err);worst_orth=max(worst_orth,orth)
 # Polar correction gives spectral error < err+5*orth <6e-10<eta.
 value=iv.mpf(0)
 for l in lam:
  f=min(1.,max(0.,float(l)))
  if f:value-=iv.mpf(f)*iv.log(iv.mpf(f))
 return value
minimum=mp.inf;argmin=None;count=0
for i in range(-m,m+1):
 for j in range(m+1):
  norm2=i*i+j*j
  if norm2<=m*m:
   bx=iv.mpf(i)/m;by=iv.mpf(j)/m;rad=iv.sqrt(iv.mpf(norm2))/m
  else:
   norm=iv.sqrt(iv.mpf(norm2));bx=iv.mpf(i)/norm;by=iv.mpf(j)/norm;rad=iv.mpf(1)
  x=(1+bx)/2;c=by/2
  SY=iv.mpf(0)
  if norm2<m*m:
   for l in [(1+rad)/2,(1-rad)/2]:SY-=l*iv.log(l)
  SN=entropy_proposal(mix(NC,x,c));SM=entropy_proposal(mix(MC,x,c))
  error=13*eta*(1-iv.log(eta))
  gap=2*SN-SY-SM-iv.log(3)-error
  lo=lower(gap)
  if lo<minimum:minimum=lo;argmin=[i,j]
  count+=1
 if (i+m)%32==0:print('Certified rows',i+m+1,'of',2*m+1,'current minimum',mp.nstr(minimum,14),flush=True)
delta=iv.sqrt(2)/(4*m);h=-delta*iv.log(delta)-(1-delta)*iv.log(1-delta);penalty=4*h+delta*iv.log(32);global_gap=iv.mpf(minimum)-penalty
assert lower(global_gap)>upper(iv.mpf('0.0904514158'))
receipt=dict(certified_global_gap_lower='0.0904514158',result='PASS: full logical entropy face at t=1/4',centers=count,mesh=m,minimum_center_gap_lower=str(minimum),argmin=argmin,max_residual_norm_bound=str(worst_res),max_orthogonality_norm_bound=str(worst_orth),trace_distance_cover=str(delta),continuity_penalty=str(penalty),global_gap_lower=str(lower(global_gap)),elapsed_seconds=time.perf_counter()-start,peak_rss_KiB_linux=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,scope='All normalized logical qubit states, including arbitrary coherence phase; fixed t=1/4 only.')
Path(__file__).with_suffix('.json').write_text(json.dumps(receipt,indent=2));print(json.dumps(receipt,indent=2))
