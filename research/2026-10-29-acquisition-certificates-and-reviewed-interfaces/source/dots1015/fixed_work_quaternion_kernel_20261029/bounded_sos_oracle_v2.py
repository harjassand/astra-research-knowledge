"""Fixed-loop floating proposals, exact one-pass congruence certificate.
No convergence assumption; all outputs carry a visible sound gap.
"""
import numpy as np,math,itertools
import sys
sys.set_int_max_str_digits(0)
from fractions import Fraction as F
import fixed_work_oracle as fw
E=np.array(fw.exps,dtype=int)

def vals(coeff,q,derivs=False):
 v=np.prod(q[:,None,:]**E[None,:,:],axis=2)@coeff
 if not derivs:return v
 g=np.zeros_like(q);H=np.zeros((len(q),4,4))
 for i in range(4):
  ee=E.copy();fac=ee[:,i].copy();ee[:,i]=np.maximum(ee[:,i]-1,0);g[:,i]=np.prod(q[:,None,:]**ee[None,:,:],axis=2)@(coeff*fac)
  for j in range(4):
   ee=E.copy();fac=ee[:,i]*(ee[:,j]-(i==j));ee[:,i]=np.maximum(ee[:,i]-1,0);ee[:,j]=np.maximum(ee[:,j]-1,0);H[:,i,j]=np.prod(q[:,None,:]**ee[None,:,:],axis=2)@(coeff*fac)
 return v,g,H

def candidate(f,iterations=32,lines=8,bits=24):
 coeff=np.array([float(f[e]) for e in fw.exps]);starts=list(np.eye(4))+[np.array(list(map(float,fw.stereo(list(map(F,u)))))) for u in itertools.product((-1,0,1),repeat=3)];q=np.array(starts);best=q.copy();bestv=vals(coeff,q)
 for _ in range(iterations):
  vv,g,H=vals(coeff,q,True);lag=np.sum(q*g,axis=1);d=[]
  for k in range(len(q)):
   M=np.zeros((5,5));M[:4,:4]=H[k]-lag[k]*np.eye(4)+1e-8*np.eye(4);M[:4,4]=q[k];M[4,:4]=q[k]
   try:dd=np.linalg.solve(M,np.r_[-g[k]+lag[k]*q[k],0])[:4]
   except np.linalg.LinAlgError:dd=-g[k]+lag[k]*q[k]
   dd=dd-q[k]*(q[k]@dd)
   if not np.all(np.isfinite(dd)) or g[k]@dd>=0:dd=-g[k]+lag[k]*q[k]
   dd=dd/max(1.,2*np.linalg.norm(dd));d.append(dd)
  d=np.array(d);desc=np.sum(g*d,axis=1);chosen=q.copy();done=np.zeros(len(q),dtype=bool)
  for b in range(lines):
   rate=2.**(-b);qq=q+rate*d;qq/=np.linalg.norm(qq,axis=1)[:,None];v=vals(coeff,qq);ok=(v<=vv+.01*rate*desc)&~done;chosen[ok]=qq[ok];done|=ok
  q=chosen;vv=vals(coeff,q);ok=vv<bestv;best[ok]=q[ok];bestv[ok]=vv[ok]
 q=best[int(np.argmin(bestv))];q=q/np.linalg.norm(q)
 if q[0]<0:q=-q
 u=q[1:]/(1+q[0]);m=2**bits;k=[round(float(v)*m) for v in u];ss=sum(v*v for v in k);den=m*m+ss;qr=[F(m*m-ss,den)]+[F(2*m*v,den) for v in k]
 return qr,fw.evaluate(f,qr)

def proposal(g0,ns,iterations=16,lines=16,levels=tuple(range(9))):
 g0=np.array(g0,dtype=float);dq=np.diag(list(map(float,fw.qdiag)));arr=np.array([-dq]+[np.array(v,dtype=float) for v in ns]);x=np.zeros(21);x[0]=-2.;chol_count=0
 def gram(xx):return g0+np.einsum('a,aij->ij',xx,arr)
 for lev in levels:
  mu=10.**(-lev)
  for _ in range(iterations):
   G=gram(x)
   try:L=np.linalg.cholesky(G);inv=np.linalg.solve(G,np.eye(10))
   except np.linalg.LinAlgError:
    x=np.zeros(21);x[0]=-2.;G=gram(x);L=np.linalg.cholesky(G);inv=np.linalg.solve(G,np.eye(10))
   B=np.einsum('ij,ajk->aik',inv,arr);grad=-mu*np.einsum('aii->a',B);grad[0]-=1;hess=mu*np.einsum('aij,bji->ab',B,B)
   try:step=np.linalg.solve(hess,-grad)
   except np.linalg.LinAlgError:step=-grad
   if not np.all(np.isfinite(step)) or grad@step>=0:step=-grad
   if not np.all(np.isfinite(step)):step=np.zeros(21)
   step=step/max(1.,np.linalg.norm(step)/8);descent=float(grad@step);old=-x[0]-2*mu*np.log(np.diag(L)).sum();chosen=x.copy();found=False
   for b in range(lines):
    rate=2.**(-b);xx=x+rate*step;valid=np.all(np.isfinite(xx)) and np.max(np.abs(xx))<=2**16;GG=gram(xx) if valid else gram(x);chol_count+=1
    try:LL=np.linalg.cholesky(GG);new=-xx[0]-2*mu*np.log(np.diag(LL)).sum();ok=valid and np.isfinite(new) and new<=old+.01*rate*descent
    except np.linalg.LinAlgError:ok=False
    if ok and not found:chosen=xx;found=True
   x=chosen
 assert chol_count==len(levels)*iterations*lines
 return x,chol_count

def jacobi_basis(G,sweeps=12,bits=32):
 diag=np.sqrt(np.array(list(map(float,fw.qdiag))));A=np.array(G,dtype=float)/diag[:,None]/diag[None,:];V=np.eye(10)
 for _ in range(sweeps):
  for p in range(10):
   for q in range(p+1,10):
    theta=.5*math.atan2(2*A[p,q],A[q,q]-A[p,p]);c=math.cos(theta);ss=math.sin(theta)
    ap=A[p,:].copy();aq=A[q,:].copy();A[p,:]=c*ap-ss*aq;A[q,:]=ss*ap+c*aq
    ap=A[:,p].copy();aq=A[:,q].copy();A[:,p]=c*ap-ss*aq;A[:,q]=ss*ap+c*aq
    vp=V[:,p].copy();vq=V[:,q].copy();V[:,p]=c*vp-ss*vq;V[:,q]=ss*vp+c*vq
 V=V/diag[:,None]
 if not np.all(np.isfinite(V)) or np.max(np.abs(V))>256:return [[F(int(i==j)) for j in range(10)] for i in range(10)]
 den=2**bits;return [[F(round(float(V[i,j])*den),den) for j in range(10)] for i in range(10)]

def congruence(G,V):
 GV=[[sum(G[i][k]*V[k][j] for k in range(10)) for j in range(10)] for i in range(10)]
 return [[sum(V[k][i]*GV[k][j] for k in range(10)) for j in range(10)] for i in range(10)]
def repair(G,V):
 A=congruence(G,V);D=[[fw.qdiag[i] if i==j else F(0) for j in range(10)] for i in range(10)];B=congruence(D,V);bs=[B[i][i]-sum(abs(B[i][j]) for j in range(10) if i!=j) for i in range(10)]
 if min(bs)<=0:
  V=[[F(int(i==j)) for j in range(10)] for i in range(10)];A=G;B=D;bs=fw.qdiag.copy()
 delta=max([F(0)]+[(sum(abs(A[i][j]) for j in range(10) if i!=j)-A[i][i])/bs[i] for i in range(10)])
 return delta,V

def solve(raw):
 if any(not isinstance(e,tuple) or len(e)!=4 or any(type(v) is not int for v in e) or e not in fw.exps for e in raw):raise ValueError('invalid monomial')
 original={e:F(raw.get(e,0)) for e in fw.exps};A=sum(abs(v) for v in original.values());scale=max(F(1),A);f={e:v/scale for e,v in original.items()};g0,ns=fw.gram(f)
 qr,upper=candidate(f);x,ncalls=proposal(g0,ns);bits=40;den=2**bits
 # Public bounded rounding: bad proposals use the canonical zero free coordinates.
 if not np.all(np.isfinite(x)) or max(abs(v) for v in x)>2**16:x=np.r_[-2.,np.zeros(20)]
 lam=F(math.floor(float(x[0])*den),den);ys=[F(round(float(v)*den),den) for v in x[1:]]
 G=[[g0[i][j]+sum(y*N[i][j] for y,N in zip(ys,ns))-(lam*fw.qdiag[i] if i==j else 0) for j in range(10)] for i in range(10)]
 V=jacobi_basis(G);delta,V=repair(G,V);lower=max((lam-delta)*scale,-A);upper*=scale
 assert upper>=lower
 return dict(status='sound_gap_certificate',quaternion=list(map(str,qr)),upper=str(upper),lower=str(lower),gap=str(upper-lower),scale=str(scale),lambda_proposal=str(lam),repair_shift=str(delta),rational_gram=[[str(v) for v in row] for row in G],rational_basis=[[str(v) for v in row] for row in V],line_cholesky_slots=ncalls,candidate_starts=31,candidate_iterations=32,candidate_line_slots=8,barrier_levels=9,barrier_iterations_per_level=16,barrier_line_slots=16,jacobi_pair_slots=12*45,proposal_bits=40,basis_bits=32,candidate_bits=24,scope='Fixed declared proposal budgets and one-pass exact congruence repair. No physical clock/padding or global accuracy promise.')

def verify(raw,c):
 if any(not isinstance(e,tuple) or len(e)!=4 or any(type(v) is not int for v in e) or e not in fw.exps for e in raw):raise ValueError('invalid monomial')
 f={e:F(raw.get(e,0)) for e in fw.exps};q=list(map(F,c['quaternion']));scale=F(c['scale']);lam=F(c['lambda_proposal']);delta=F(c['repair_shift']);G=[[F(v) for v in row] for row in c['rational_gram']];V=[[F(v) for v in row] for row in c['rational_basis']];assert delta>=0 and len(q)==4 and sum(v*v for v in q)==1
 assert scale==max(F(1),sum(abs(v) for v in f.values()))
 assert len(G)==10 and len(V)==10 and all(len(row)==10 for row in G+V)
 Q2={tuple(2*(int(i==a)+int(i==b)) for i in range(4)): F(1 if a==b else 2) for a in range(4) for b in range(a,4)}
 for e,grp in fw.groups.items():assert scale*sum(a*G[i][j] for i,j,a in grp)==f[e]-lam*scale*Q2.get(e,0)
 assert all(G[i][j]==G[j][i] for i in range(10) for j in range(10))
 A=congruence(G,V);D=[[fw.qdiag[i] if i==j else F(0) for j in range(10)] for i in range(10)];B=congruence(D,V)
 assert all(B[i][i]>sum(abs(B[i][j]) for j in range(10) if j!=i) for i in range(10))
 C=[[A[i][j]+delta*B[i][j] for j in range(10)] for i in range(10)]
 assert all(C[i][i]>=sum(abs(C[i][j]) for j in range(10) if j!=i) for i in range(10))
 up=fw.evaluate(f,q);lo=max((lam-delta)*scale,-sum(abs(v) for v in f.values()));assert up==F(c['upper']) and lo==F(c['lower']) and F(c['gap'])==up-lo>=0
 assert F(c['gap'])<=2*sum(abs(v) for v in f.values())
 return True
