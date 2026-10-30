#!/usr/bin/env python3
"""Actual 2-site + retained-bath GKLS cavity, including a rotated reset."""
import numpy as np
from scipy.linalg import expm
import json
I=np.eye(2,dtype=complex); X=np.array([[0,1],[1,0]],complex)
Y=np.array([[0,-1j],[1j,0]],complex); Z=np.diag([1,-1]); m=np.array([[0,1],[0,0]],complex)
def ten(a,b,c): return np.kron(np.kron(a,b),c)
def gen(H,js):
 n=len(H); eye=np.eye(n); L=-1j*(np.kron(eye,H)-np.kron(H.T,eye))
 for j in js:
  a=j.conj().T@j; L+=np.kron(j.conj(),j)-.5*np.kron(eye,a)-.5*np.kron(a.T,eye)
 return L

def reduce_super(L,ds=2,do=4):
 out=np.zeros((do*do,do*do),complex)
 for a in range(do):
  for b in range(do):
   e=np.zeros((do,do),complex);e[a,b]=1
   v=(L@np.kron(np.eye(ds)/ds,e).reshape(-1,order='F')).reshape(ds,do,ds,do,order='F') if False else None
   v=(L@np.kron(np.eye(ds)/ds,e).reshape(-1,order='F')).reshape(ds*do,ds*do,order='F')
   tr=np.trace(v.reshape(ds,do,ds,do),axis1=0,axis2=2)
   out[:,a+b*do]=tr.reshape(-1,order='F')
 return out

def lift_super(M,ds=2,do=4):
 n=ds*do;out=np.zeros((n*n,n*n),complex)
 for a in range(n):
  for b in range(n):
   sa,oa=divmod(a,do);sb,ob=divmod(b,do)
   e=np.zeros((do,do),complex);e[oa,ob]=1
   r=(M@e.reshape(-1,order='F')).reshape(do,do,order='F')
   eS=np.zeros((ds,ds),complex);eS[sa,sb]=1
   out[:,a+b*n]=np.kron(eS,r).reshape(-1,order='F')
 return out

def choi(S,n):
 out=np.zeros((n*n,n*n),complex)
 for a in range(n):
  for b in range(n):
   e=np.zeros((n,n),complex);e[a,b]=1
   y=(S@e.reshape(-1,order='F')).reshape(n,n,order='F')
   out+=np.kron(e,y)
 return out

h_touch=.2*ten(X,X,I)+.13*ten(Z,I,I)
h_out=.17*ten(I,Z,I)+.23*ten(I,I,X)
H0=h_touch+h_out
jS=np.sqrt(.8)*ten(m,I,I);jO=np.sqrt(.6)*ten(I,m,I)
eps=.08
Ha=H0+eps*(ten(X,I,Z)+ten(I,X,Y))
ja=[jS+eps*ten(Z,I,X),jO]
L0=gen(H0,[jS,jO]);La=gen(Ha,ja);N=La-L0
Nr=reduce_super(N);cut=L0+lift_super(Nr)
# Independent GKLS reconstruction from actual reduced jump blocks.
hr=np.trace(Ha.reshape(2,4,2,4),axis1=0,axis2=2)/2
bar=np.trace(h_touch.reshape(2,4,2,4),axis1=0,axis2=2)/2
jr=[]
for j in ja:
 blocks=j.reshape(2,4,2,4)
 for a in range(2):
  for b in range(2): jr.append(blocks[a,:,b,:]/np.sqrt(2))
reconstructed=lift_super(gen(hr,jr))+gen(h_touch-np.kron(I,bar),[jS])
t=.31; gain=np.kron(jS.conj(),jS)
cpcut=choi(expm(t*(cut-gain)),8)
cpactualbad=choi(expm(t*(La-gain)),8)
# Commuting superoperator cavities on the two physical sites.
swap=np.zeros((8,8),complex)
for a in range(2):
 for b in range(2):
  for c in range(2):swap[4*b+2*a+c,4*a+2*b+c]=1
S=np.kron(swap.conj(),swap)
def EA(M):return lift_super(reduce_super(M))
def EB(M):return S@EA(S@M@S)@S
report={"scope":"Finite 2-physical-site plus retained-qubit-bath algebra check only.",
 "generator_reconstruction_error":float(np.linalg.norm(cut-reconstructed)),
 "cavity_idempotence_error":float(np.linalg.norm(EA(EA(N))-EA(N))),
 "cavity_commutator_error":float(np.linalg.norm(EA(EB(N))-EB(EA(N)))),
 "cavity_nominal_reset_deleted_choi_min":float(np.linalg.eigvalsh(cpcut)[0]),
 "actual_nominal_reset_deleted_choi_min":float(np.linalg.eigvalsh(cpactualbad)[0])}
assert report['generator_reconstruction_error']<1e-11
assert report['cavity_idempotence_error']<1e-11
assert report['cavity_commutator_error']<1e-11
assert report['cavity_nominal_reset_deleted_choi_min']>-1e-11
assert report['actual_nominal_reset_deleted_choi_min']<-1e-6
print(json.dumps(report,indent=2))
