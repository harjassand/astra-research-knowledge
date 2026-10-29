"""Finite candidate + independently checkable rational SOS lower certificate.
Floating logdet search is only a certificate FINDER, never its verifier.
No completeness claimed if a desired gap is not reached.
"""
import itertools,json,math,time,sys
from pathlib import Path
from fractions import Fraction as Q
import numpy as np
from scipy.optimize import minimize
D=4
pairs=list(itertools.combinations_with_replacement(range(D),2))
def expo(pair):
 a=[0]*D
 for i in pair:a[i]+=1
 return tuple(a)
zexp=[expo(p) for p in pairs]
exps=sorted(set(tuple(a+b for a,b in zip(x,y)) for x in zexp for y in zexp))
groups={e:[] for e in exps}
for i in range(10):
 for j in range(i,10):groups[tuple(a+b for a,b in zip(zexp[i],zexp[j]))].append((i,j,1 if i==j else 2))
assert len(exps)==35 and sum(len(v)-1 for v in groups.values())==20

def add(a,b,scale=1):
 r=a.copy()
 for e,c in b.items():r[e]=r.get(e,0)+scale*c
 return {e:c for e,c in r.items() if c}
def mul(a,b):
 r={}
 for x,c in a.items():
  for y,d in b.items():
   e=tuple(i+j for i,j in zip(x,y));r[e]=r.get(e,0)+c*d
 return r
def mono(i,j,c=1):return {expo((i,j)):c}
def lin(*terms):
 r={}
 for c,i,j in terms:r=add(r,mono(i,j,c))
 return r
Qpoly=lin(*[(1,i,i) for i in range(4)])
R=[[lin((1,0,0),(1,1,1),(-1,2,2),(-1,3,3)),lin((2,1,2),(-2,0,3)),lin((2,1,3),(2,0,2))],
   [lin((2,1,2),(2,0,3)),lin((1,0,0),(-1,1,1),(1,2,2),(-1,3,3)),lin((2,2,3),(-2,0,1))],
   [lin((2,1,3),(-2,0,2)),lin((2,2,3),(2,0,1)),lin((1,0,0),(-1,1,1),(-1,2,2),(1,3,3))]]
def bank_polynomial(bank,edge):
 f={e:3*bank['probe_calls']*c for e,c in mul(Qpoly,Qpoly).items()}
 for a,b in itertools.product(range(3),repeat=2):
  f=add(f,mul(Qpoly,R[a][b]),-9*bank['B'][edge][a][b])
  for c,d in itertools.product(range(3),repeat=2):f=add(f,mul(R[a][b],R[c][d]),-81*bank['C'][edge][a][b][c][d])
 return {e:int(f.get(e,0)) for e in exps}
def zero_mat():return [[Q(0) for _ in range(10)] for _ in range(10)]
def gram_param(f):
 g0=zero_mat();ns=[]
 for e,grp in groups.items():
  i,j,a=grp[0];g0[i][j]=g0[j][i]=Q(f.get(e,0),a)
  for k,l,b in grp[1:]:
   nn=zero_mat();nn[k][l]=nn[l][k]=Q(1);nn[i][j]=nn[j][i]=-Q(b,a);ns.append(nn)
 gq=zero_mat()
 for i,pair in enumerate(pairs):gq[i][i]=Q(1 if pair[0]==pair[1] else 2)
 return g0,gq,ns
E=np.array(exps,dtype=int)
def value_grad(coeff,q):
 powers=np.prod(q[None,:]**E,axis=1);v=float(coeff@powers);g=[]
 for i in range(4):
  ee=E.copy();fac=ee[:,i].copy();ee[:,i]=np.maximum(0,ee[:,i]-1)
  g.append(float((coeff*fac)@np.prod(q[None,:]**ee,axis=1)))
 return v,np.array(g)
def rational_candidate(q,bits=24):
 q=np.array(q)/np.linalg.norm(q)
 if q[0]<0:q=-q
 u=q[1:]/(1+q[0]);m=2**bits;k=[round(float(x)*m) for x in u];ss=sum(x*x for x in k);den=m*m+ss
 return [Q(m*m-ss,den)]+[Q(2*m*x,den) for x in k]
def exact_eval(f,q):return sum(Q(c)*math.prod(q[i]**e[i] for i in range(4)) for e,c in f.items())
def find_candidate(f,seed=11,starts=20):
 coeff=np.array([float(f[e]) for e in exps]);rng=np.random.default_rng(seed);best=(float('inf'),None)
 for q0 in list(np.eye(4))+[rng.normal(size=4) for _ in range(starts)]:
  q0=q0/np.linalg.norm(q0)
  res=minimize(lambda q:value_grad(coeff,q),q0,jac=True,method='SLSQP',bounds=[(-1.,1.)]*4,constraints=[{'type':'eq','fun':lambda q:q@q-1,'jac':lambda q:2*q}],options={'ftol':1e-13,'maxiter':400})
  q=res.x/np.linalg.norm(res.x);v=value_grad(coeff,q)[0]
  if v<best[0]:best=(v,q)
 qr=rational_candidate(best[1]);assert sum(x*x for x in qr)==1
 return qr,exact_eval(f,qr)
def barrier_search(g0,gq,ns,mu_final=1e-10):
 g0=np.array(g0,dtype=float);arr=np.array([-np.array(gq,dtype=float)]+[np.array(x,dtype=float) for x in ns]);x=np.zeros(len(arr));x[0]=-max(2,2*np.linalg.norm(g0,2));trace=[]
 def gram(x):return g0+np.einsum('a,aij->ij',x,arr)
 for mu in [10.**(-k) for k in range(0,1+int(round(-math.log10(mu_final)))) if 10.**(-k)>=mu_final*.999]:
  for it in range(100):
   G=gram(x)
   try:L=np.linalg.cholesky(G)
   except np.linalg.LinAlgError:raise RuntimeError('lost interior')
   inv=np.linalg.solve(G,np.eye(10));B=np.einsum('ij,ajk->aik',inv,arr)
   grad=-mu*np.einsum('aii->a',B);grad[0]-=1
   hess=mu*np.einsum('aij,bji->ab',B,B)
   try:step=np.linalg.solve(hess,-grad)
   except np.linalg.LinAlgError:step=np.linalg.lstsq(hess,-grad,rcond=1e-12)[0]
   descent=float(grad@step)
   if descent>=0:step=-grad;descent=float(grad@step)
   if -descent<1e-17:break
   old=-x[0]-2*mu*np.log(np.diag(L)).sum();rate=1.
   for bt in range(80):
    xx=x+rate*step
    try:
     LL=np.linalg.cholesky(gram(xx));new=-xx[0]-2*mu*np.log(np.diag(LL)).sum()
     if new<=old+.01*rate*descent:break
    except np.linalg.LinAlgError:pass
    rate*=.5
   if rate<2**-60:break
   x=xx
  trace.append(dict(mu=mu,steps=it+1,lower=float(x[0]),min_eigenvalue=float(np.linalg.eigvalsh(gram(x))[0])))
 return x,trace

def exact_ldl(G):
 n=len(G);L=[[Q(int(i==j)) for j in range(n)] for i in range(n)];d=[]
 for j in range(n):
  dj=G[j][j]-sum(L[j][k]**2*d[k] for k in range(j))
  if dj<=0:return None
  d.append(dj)
  for i in range(j+1,n):L[i][j]=(G[i][j]-sum(L[i][k]*L[j][k]*d[k] for k in range(j)))/dj
 return d

def rational_certificate(g0,gq,ns,x,bits=42,repair_start_bits=34):
 den=2**bits;ys=[Q(round(float(v)*den),den) for v in x[1:]];lam=Q(math.floor(float(x[0])*den),den)
 correction=Q(1,2**repair_start_bits)
 for attempts in range(80):
  ll=lam-correction;G=[[g0[i][j]-ll*gq[i][j]+sum(y*N[i][j] for y,N in zip(ys,ns)) for j in range(10)] for i in range(10)]
  piv=exact_ldl(G)
  if piv is not None:return ll,ys,G,piv,attempts+1
  correction*=2
 raise RuntimeError('could not rationally repair')
def verify_identity(f,lam,G):
 got={e:Q(0) for e in exps}
 for e,grp in groups.items():got[e]=sum(a*G[i][j] for i,j,a in grp)
 want=add(f,mul(Qpoly,Qpoly),-lam)
 assert all(got[e]==want.get(e,0) for e in exps)
 assert exact_ldl(G) is not None

def solve_bank(path,edge,out):
 bank=json.load(open(path));raw=bank_polynomial(bank,edge);scale=2**max(0,max(abs(v) for v in raw.values()).bit_length());f={e:Q(c,scale) for e,c in raw.items()};start=time.time()
 g0,gq,ns=gram_param(f);qr,upper=find_candidate(f,seed=190+edge)
 x,trace=barrier_search(g0,gq,ns);lower,ys,G,piv,tries=rational_certificate(g0,gq,ns,x);verify_identity(f,lower,G)
 # Objective was4 times cumulative estimated delta; normalized per probe gap below.
 gap=(upper-lower)*scale/(4*bank['probe_calls'])
 result=dict(source=str(path),edge=edge,probe_calls=bank['probe_calls'],scale=scale,quartic_coefficients=[dict(exponents=e,coefficient=int(raw[e])) for e in exps],rational_quaternion=[str(v) for v in qr],rational_upper=str(upper),rational_lower=str(lower),rational_gram=[[str(v) for v in row] for row in G],positive_LDL_pivots=[str(v) for v in piv],normalized_mean_loss_upper=float(upper*scale/(4*bank['probe_calls'])),normalized_mean_loss_lower=float(lower*scale/(4*bank['probe_calls'])),certified_global_mean_loss_gap=float(gap),certificate_repair_attempts=tries,barrier_trace=trace,seconds=time.time()-start,scope='Exact rational global lower/upper certificate; floating searches only propose objects. SOS relaxation need not be tight for every quaternary quartic.')
 Path(out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ['rational_gram','positive_LDL_pivots','quartic_coefficients','rational_quaternion','barrier_trace']},indent=2))
if __name__=='__main__':solve_bank(sys.argv[1],int(sys.argv[2]),sys.argv[3])
