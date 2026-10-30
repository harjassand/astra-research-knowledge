#!/usr/bin/env python3
"""Finite algebra regressions, not threshold proofs or full monitor simulations."""
import json
import numpy as np
from scipy.sparse import csr_matrix, eye, kron
from scipy.sparse.linalg import expm_multiply
from scipy.linalg import expm

def unit(n,i,j):
    a=np.zeros((n,n),complex); a[i,j]=1; return a

def gen(H,jumps):
    n=len(H); I=eye(n,format='csr',dtype=complex); H=csr_matrix(H)
    L=-1j*(kron(I,H)-kron(H.T,I))
    for J in jumps:
        J=csr_matrix(J); A=J.conj().T@J
        L+=kron(J.conjugate(),J)-.5*kron(I,A)-.5*kron(A.T,I)
    return L.tocsr()

def gain(J): return kron(csr_matrix(J.conjugate()),csr_matrix(J)).tocsr()
def unvec(v,n): return v.reshape((n,n),order='F')

g=.31; Om=.9; kap=.8; mu=.37; T=3.1
U=np.eye(4,dtype=complex); c=np.sqrt(1-g); s=np.sqrt(g)
U[np.ix_([1,2],[1,2])]=[[c,s],[-s,c]]
# U|10> = s|01>+c|10>.
C0,C1,B00,B11,B10,QS,QA=range(7)
n=28
H=np.zeros((n,n),complex)
for a,b,V in [(C1,C0,U),(B10,B11,U.conj().T)]:
    h=Om*np.kron(unit(7,a,b),V); H+=h+h.conj().T
jumps=[]; success=[]; abort=[]
for a,b in [(B00,C0),(B11,C1)]:
    jumps.append(np.sqrt(mu)*np.kron(unit(7,a,b),np.eye(4)))
for dest,src,collection in [(QS,C1,success),(QA,B00,abort),(QA,B10,abort)]:
    for w in range(2):
        J=np.sqrt(kap)*np.kron(unit(7,dest,src),np.kron(np.eye(2),unit(2,0,w)))
        collection.append(J); jumps.append(J)
L=gen(H,jumps)
F=np.zeros((n,n),complex)
for cc in range(7): F+=np.kron(unit(7,cc,cc),U if cc in [C1,B11] else np.eye(4))
paulis=[np.eye(2),np.array([[0,1],[1,0]]),np.array([[0,-1j],[1j,0]]),np.diag([1,-1])]
inputs=[np.kron(unit(7,C0,C0),np.kron(P,unit(2,0,0))) for P in paulis]
V=np.stack([x.reshape(-1,order='F') for x in inputs],axis=1)
outs=[unvec(x,n) for x in expm_multiply(T*L,V).T]
def block_data(rho,cc):
    b=rho[4*cc:4*cc+4,4*cc:4*cc+4].reshape(2,2,2,2)
    return np.trace(b,axis1=1,axis2=3)
K0=np.diag([1,c]); K1=np.array([[0,s],[0,0]],complex)
def phi(P): return K0@P@K0.conj().T+K1@P@K1.conj().T
ps=float(np.trace(block_data(outs[0],QS)).real/2)
pa=float(np.trace(block_data(outs[0],QA)).real/2)
succ=max(np.linalg.norm(block_data(r,QS)-ps*phi(P)) for r,P in zip(outs,paulis))
abrt=max(np.linalg.norm(block_data(r,QA)-pa*P) for r,P in zip(outs,paulis))
residual=[]
for rho in outs:
    fr=F.conj().T@rho@F
    residual.append(sum((block_data(fr,cc) for cc in range(5)),start=np.zeros((2,2),complex)))
pr=float(np.trace(residual[0]).real/2)
reserr=max(np.linalg.norm(r-pr*P) for r,P in zip(residual,paulis))
# A small negative calibration makes the OLD gain deletion nonpositive.
J=unit(2,0,1); eps=.017; t=.43
La=gen(np.zeros((2,2)),[np.sqrt(1-eps)*J])
Kbad=La-gain(J)
r=unvec(expm_multiply(t*Kbad,unit(2,1,1).reshape(-1,order='F')),2)
formula=np.diag([-eps/(1-eps)*(1-np.exp(-(1-eps)*t)),np.exp(-(1-eps)*t)])
report={"scope":"Algebraic single-transaction regression only; no finite-monitor, locality-threshold or asynchronous-service proof.",
"success_probability":ps,"abort_probability":pa,"unfinished_probability":pr,
"normalization_error":abs(ps+pa+pr-1),"success_channel_error":float(succ),
"inverse_abort_identity_error":float(abrt),"forest_unfinished_identity_error":float(reserr),
"old_gain_deleted_min_eigenvalue":float(np.linalg.eigvalsh(r)[0]),
"negative_calibration_formula_error":float(np.linalg.norm(r-formula))}
assert max(succ,abrt,reserr,abs(ps+pa+pr-1),np.linalg.norm(r-formula))<1e-11
assert report['old_gain_deleted_min_eigenvalue']<0
print(json.dumps(report,indent=2))
