#!/usr/bin/env python3
"""Independent exact convention fixture and rectangular physical-channel checks."""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
from pathlib import Path
import numpy as np,sympy as sp,json,math
HERE=Path(__file__).parent;rng=np.random.default_rng(202610282314)
# Exact complex convention fixture, unrelated to root's random seed.
I=sp.eye(2);C=sp.diag(sp.Rational(3,5),sp.Rational(5,13));T=sp.diag(sp.Rational(4,5),sp.Rational(12,13))
F0=I.col_join(sp.zeros(2));F1=C.col_join(T)
U=sp.Matrix([[3,4*sp.I],[4,-3*sp.I]])/5;assert U.H*U==I
S=U.H*sp.diag(sp.Rational(1,3),sp.Rational(2,3))*U
Fs=[F0*U[0,j]+F1*U[1,j] for j in range(2)];M=Fs[0].row_join(Fs[1]);G=M.H*M;R=sp.kronecker_product(S,I/2)
TP=sum((S[i,j]*Fs[j].H*Fs[i] for i in range(2) for j in range(2)),sp.zeros(2));assert sp.simplify(TP)==I
tr=sp.simplify(sp.trace(R*G));wrong=sp.simplify(sp.trace(sp.kronecker_product(S.T,I/2)*G));assert tr==1 and wrong!=1
alpha=sp.Integer(2);m=3;P=sum((sp.binomial(2*j,j)/4**j*(sp.eye(4)-G/alpha**2)**j for j in range(m+1)),sp.zeros(4));A=P*M.H/alpha
success=(A*M-sp.eye(4)).H*(A*M-sp.eye(4));fail=M.H*(sp.eye(4)-A.H*A)*M
L=sp.simplify(sp.trace(R*(success+fail)));z=sp.simplify(sp.trace(R*A*M));assert sp.simplify(L-(2-2*z))==0
exact={'correct_source_trace':str(tr),'wrong_transpose_source_trace':str(wrong),'penalty':str(L),'z':str(z),'exact_noncommutator_nonzero':S[0,1]!=0 and G*R!=R*G}

def iso(d,k):
 Q,_=np.linalg.qr(rng.normal(size=(d,k))+1j*rng.normal(size=(d,k)));return Q[:,:k]
def soft(x,m):
 term=np.ones_like(x);c=1.;p=term.copy()
 for j in range(1,m+1):c*=1-1/(2*j);term*=1-x*x;p+=c*term
 return x*p
rows=[]
for trial in range(160):
 k,n,d=[(2,4,3),(2,3,8),(3,2,6),(2,2,4)][trial%4]
 F=[iso(d,k) for _ in range(n)]
 if trial%8==0:F[1]=F[0].copy()
 if trial%4==1:
  Q=iso(d,d);F=[Q[:,i*k:(i+1)*k] for i in range(n)]
  if trial%8==1:F=[np.linalg.qr(f+1e-3*iso(d,k))[0] for f in F]
 p=rng.dirichlet(np.ones(n));p[0]=0 if trial%7==0 else p[0];p/=sum(p);U=iso(n,n)
 source=[f*np.sqrt(q) for f,q in zip(F,p)]
 rotated=[sum(F[i]*U[i,j] for i in range(n)) for j in range(n)];S=U.conj().T@np.diag(p)@U;M=np.concatenate(rotated,axis=1);G=M.conj().T@M;R=np.kron(S,np.eye(k)/k)
 alpha=max(1.,float(np.linalg.norm(M,2)));eps=1e-5;m=math.ceil(4*alpha**2*math.log(2*alpha/eps));W,s,Vh=np.linalg.svd(M,full_matrices=False);A=(Vh.conj().T*soft(s/alpha,m))@W.conj().T
 fail=(np.eye(d)-A.conj().T@A);w,V=np.linalg.eigh((fail+fail.conj().T)/2);assert min(w)>-1e-11
 B=(V*np.sqrt(np.maximum(w,0)))@V.conj().T;recovery=[A[i*k:(i+1)*k] for i in range(n)]
 for j in range(d):
  H=np.zeros((k,d),complex);H[0]=B[j];recovery.append(H)
 tp=float(np.linalg.norm(sum(K.conj().T@K for K in recovery)-np.eye(d)))
 Fe=sum(abs(np.trace(D@K))**2 for D in recovery for K in source)/k**2
 penalty=float(np.trace(R@(np.eye(n*k)+G-A@M-M.conj().T@A.conj().T)).real)
 defect=float(np.trace(R@(G-np.eye(n*k))@(G-np.eye(n*k))).real);bound=20*defect/9+2*alpha*eps
 assert tp<1e-10 and 1-Fe<=penalty+1e-10 and penalty<=bound+1e-10
 rows.append({'trial':trial,'K':k,'N':n,'D':d,'defect':defect,'Fe':Fe,'penalty':penalty,'bound':bound,'TP_residual':tp,'min_sigma':float(min(s))})
# More general F_i need not be isometries: start from a normalized Kraus stack.
generic=[]
for trial in range(80):
 k,n,d=2,3,4
 stack=iso(n*d,k);Ks=[stack[i*d:(i+1)*d] for i in range(n)]
 probs=rng.dirichlet(np.ones(n)+1);U=iso(n,n)
 Fs=[sum(Ks[i]/np.sqrt(probs[i])*U[i,j] for i in range(n)) for j in range(n)]
 S=U.conj().T@np.diag(probs)@U;M=np.concatenate(Fs,axis=1);G=M.conj().T@M;R=np.kron(S,np.eye(k)/k)
 alpha=max(1.,float(np.linalg.norm(M,2)));eps=1e-5;m=math.ceil(4*alpha**2*math.log(2*alpha/eps));W,sv,Vh=np.linalg.svd(M,full_matrices=False);A=(Vh.conj().T*soft(sv/alpha,m))@W.conj().T
 w,V=np.linalg.eigh((np.eye(d)-A.conj().T@A));assert min(w)>-1e-10
 B=(V*np.sqrt(np.maximum(w,0)))@V.conj().T;Ds=[A[i*k:(i+1)*k] for i in range(n)]
 for j in range(d):
  Z=np.zeros((k,d),complex);Z[0]=B[j];Ds.append(Z)
 fe=sum(abs(np.trace(D@K))**2 for D in Ds for K in Ks)/k**2
 L=float(np.trace(R@(np.eye(n*k)+G-A@M-M.conj().T@A.conj().T)).real);b=float(np.trace(R@(G-np.eye(n*k))@(G-np.eye(n*k))).real)
 assert abs(np.trace(R@G)-1)<1e-10 and 1-fe<=L+1e-10 and L<=20*b/9+2*alpha*eps+1e-10
 generic.append({'Fe':fe,'defect':b,'penalty':L,'alpha':alpha})
out={'status':'PASS_INDEPENDENT_EXACT_CONVENTION_AND_RECTANGULAR_CHANNEL_CHECKS','exact_fixture':exact,'random_cases':rows,'generic_nonisometric_cases':generic,'max_TP':max(r['TP_residual'] for r in rows),'max_bound_violation':max(1-r['Fe']-r['bound'] for r in rows)}
(HERE/'check_independent_v1.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='random_cases'},indent=2))
