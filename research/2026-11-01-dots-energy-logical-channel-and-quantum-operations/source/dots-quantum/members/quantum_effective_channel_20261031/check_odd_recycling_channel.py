#!/usr/bin/env python3
"""Small finite-matrix diagnostics, not a channel-error or hardware certificate."""
import json,math
from pathlib import Path
import numpy as np
from scipy.linalg import expm
I2=np.eye(2);X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1,-1]);sm=np.array([[0,1],[0,0]],complex);sp=sm.T
P=np.diag([1,0,0]);Q=np.eye(3)-P;H=Q;ket=np.eye(3,dtype=complex)
K=np.kron(np.outer(ket[:,1],ket[:,0]),sm)+.5*np.kron(np.outer(ket[:,2],ket[:,0]),sp);K=K+K.conj().T
Hp=np.kron(np.eye(3),Z/3);S=K.copy();prep=np.kron(ket[:,0,None],I2);prepmap=np.kron(prep.conj(),prep)
def ham(A):n=len(A);return -1j*(np.kron(np.eye(n),A)-np.kron(A.T,np.eye(n)))
def diss(A):n=len(A);B=A.conj().T@A;return np.kron(A.conj(),A)-.5*(np.kron(np.eye(n),B)+np.kron(B.T,np.eye(n)))
def adj(Ls,A):return sum(L.conj().T@A@L-.5*(L.conj().T@L@A+A@L.conj().T@L) for L in Ls)
def chnorm(M):return float(np.linalg.norm(np.block([[M[:,i+2*j].reshape(2,2,order='F') for j in range(2)] for i in range(2)]),ord='nuc'))
trace=np.zeros((4,36),complex)
for j in range(36):
 a=np.zeros((6,6));a[j%6,j//6]=1;trace[:,j]=np.einsum('aiaj->ij',a.reshape(3,2,3,2)).reshape(4,order='F')
Le=ham(Z/3)+diss(math.sqrt(2)*sm)+diss(sp/math.sqrt(2));eff=expm(Le)
ctrl=np.kron(X.conj(),X);fullctrl=np.kron(np.kron(np.eye(3),X).conj(),np.kron(np.eye(3),X))
rows=[];identities=[]
for p in [.25,.5,1.]:
 split=[math.sqrt(2*p)*np.outer(ket[:,0],ket[:,1]),math.sqrt(2*(1-p))*np.outer(ket[:,2],ket[:,1]),math.sqrt(2)*np.outer(ket[:,0],ket[:,2])]
 mixed=[math.sqrt(2)*np.outer(math.sqrt(p)*ket[:,0]+math.sqrt(1-p)*ket[:,2],ket[:,1]),split[2]]
 for name,src in [('split',split),('coherent_output',mixed)]:
  Ls=[np.kron(L,I2) for L in src];G=sum(diss(L) for L in Ls)
  h=sum(L.conj().T@L for L in src)/2;drift=adj(src,H)
  assert np.linalg.norm(h-H)<1e-12
  assert np.linalg.eigvalsh(drift+2*p*H).max()<1e-12
  bdef=0.;adef=0.
  for O in [I2,X,Y,Z]:
   full=np.kron(np.eye(3),O);F=1j*(S@full-full@S);V=1j*(K@full-full@K)
   B=adj(Ls,F)+V;bdef=max(bdef,float(np.linalg.norm(B,2)))
   VF=1j*(K@F-F@K);D=prep.conj().T@VF@prep;A=VF-np.kron(np.eye(3),D)
   adef=max(adef,float(np.linalg.norm(A-np.kron(Q,I2)@A@np.kron(Q,I2),2)))
  if name=='split':assert bdef<1e-12 and adef<1e-12
  identities.append(dict(p=p,source=name,first_defect_norm=bdef,QQ_support_error=adef))
  for lam in [100,10000,1000000]:
   Gen=lam*G+ham(Hp)+math.sqrt(lam)*ham(K)
   for control in [False,True]:
    if control:
     Ehalf=expm(Gen/2);actual=trace@Ehalf@fullctrl@Ehalf@prepmap
     Eeh=expm(Le/2);target=Eeh@ctrl@Eeh
    else:actual=trace@expm(Gen)@prepmap;target=eff
    error=chnorm(actual-target)
    kap=2*p;gamma=28/3;nu=4 if control else 0
    bound=(8/kap+32/kap**2+4*(gamma+nu)/kap)/lam
    if name=='split':assert error<=bound+1e-8
    rows.append(dict(p=p,source=name,rate=lam,system_X_control=control,choi_trace_norm_upper_diagnostic=error,cold_bound_if_split=bound if name=='split' else None))
# Direct four-Kraus GAD target, including commuting Z unitary.
eta=math.exp(-2.5);ground=.8;U=np.diag([np.exp(-1j/3),np.exp(1j/3)])
Ks=[math.sqrt(ground)*np.diag([1,math.sqrt(eta)]),math.sqrt(ground*(1-eta))*sm,math.sqrt(1-ground)*np.diag([math.sqrt(eta),1]),math.sqrt((1-ground)*(1-eta))*sp]
KG=sum(np.kron((U@A).conj(),U@A) for A in Ks)
assert np.linalg.norm(KG-eff)<1e-12
out=dict(scope=__doc__,identities=identities,rows=rows,GAD_superoperator_error=float(np.linalg.norm(KG-eff)),nonunitality_trace_norm=float(np.linalg.norm((eff@I2.reshape(4,order='F')).reshape(2,2,order='F')-I2,ord='nuc')))
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print('PASS',len(rows),'channels;',len(identities),'identity cases; GAD error',out['GAD_superoperator_error'])
