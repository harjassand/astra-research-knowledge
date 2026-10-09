"""Fixed complex nonreversible diagnostic; stdout only, no fixture writes."""
import json
import math
import numpy as np

def power(a,p):
    q,U=np.linalg.eigh(a)
    assert min(q)>0
    return (U*q**p)@U.conj().T

raw=np.array([1.,2.,3.,4.]); svals=raw/np.linalg.norm(raw)
s=np.diag(svals); sigma=s@s; d=np.diag(np.sqrt(svals)); di=np.diag(1/np.sqrt(svals))
B=np.zeros((4,4),complex); B[1:,1:]=np.outer(np.array([1.,-1.,1j]),np.ones(3))
Y=B.conj().T@s@B; Z=B@s@B.conj().T
D=np.zeros_like(B)
for i in range(4):
    for j in range(4):
        D[i,j]=Y[i,i]/svals[i] if i==j else 2*(svals[i]*Y[i,j]-svals[j]*Z[i,j])/(svals[i]**2-svals[j]**2)
K=d@B@di; C=d@D@di
def Lstar(x): return (C@x+x@C.conj().T)/2-K@x@K.conj().T
def H(x): return (D.conj().T@x+x@D)/2-B.conj().T@x@B
A=np.array([[2,.2+.1j,.3,0],[0,1.7,.4j,.1],[.1j,0,1.5,.2],[.3,0,0,1.]],complex)
rho=A@A.conj().T;rho/=np.trace(rho).real
lam,U=np.linalg.eigh(rho); q=np.sqrt(lam); sqrt_rho=(U*q)@U.conj().T
logrho=(U*np.log(lam))@U.conj().T; logsigma=np.diag(np.log(svals**2))
j=float(np.trace(Lstar(rho)@(logrho-logsigma)).real)
e=float(np.trace(sqrt_rho@H(sqrt_rho)).real)
parts={}
for i in range(4):
    for k in range(4):
        if B[i,k]!=0:
            omega=round(math.log(svals[i]/svals[k]),13)
            parts.setdefault(omega,np.zeros_like(B))[i,k]+=B[i,k]
freq=list(parts); coeff=[U.conj().T@parts[w]@U for w in freq]

def kernel_j(x,y):
    z=(x+y)/2;h=(x-y)/2
    hc=.5 if abs(h)<1e-12 else h/np.tanh(2*h)
    hs=.5 if abs(h)<1e-12 else h/np.sinh(2*h)
    return 2*(np.exp(-z)*(-z-hc)+np.exp(z)*hs)

jg=0j;eg=0j
for i in range(4):
    for k in range(4):
        beta=math.log(q[i]/q[k]);vec=np.array([p[i,k] for p in coeff])
        x=np.array([beta-w for w in freq])
        kj=np.array([[kernel_j(a,b) for b in x] for a in x])
        ke=np.array([[np.cosh((a+b)/2)/np.cosh((a-b)/2)-1 for b in x] for a in x])
        jg+=q[i]*q[k]*np.vdot(vec,kj@vec)
        eg+=q[i]*q[k]*np.vdot(vec,ke@vec)
result={'scope':'One fixed complex four-dimensional non-KMS diagnostic; not proof of a universal bound',
    'stationarity':float(np.max(np.abs(Lstar(sigma)))),
    'trace_preservation':float(np.max(np.abs(C+C.conj().T-2*K.conj().T@K))),
    'J_direct':j,'J_gram_real':float(jg.real),'J_gram_imag':float(jg.imag),
    'E_direct':e,'E_gram_real':float(eg.real),'E_gram_imag':float(eg.imag),
    'J_error':float(abs(j-jg)),'E_error':float(abs(e-eg)),
    'noise_nonhermitian':float(np.linalg.norm(B-B.conj().T)),
    'frequency_count':len(freq)}
print(json.dumps(result,indent=2))
assert result['stationarity']<1e-10 and result['trace_preservation']<1e-10
assert result['J_error']<1e-10 and result['E_error']<1e-10
