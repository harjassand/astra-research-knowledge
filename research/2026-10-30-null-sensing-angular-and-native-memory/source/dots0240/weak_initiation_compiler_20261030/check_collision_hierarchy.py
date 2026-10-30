"""Finite diagnostic only: exact operator inequality, not a compiler simulation."""
import json
import numpy as np
from itertools import product

def embed(a,j,n):
    r=np.array([[1.]],complex)
    for k in range(n): r=np.kron(r,a if j==k else np.eye(2))
    return r

def adj_diss(j,o):
    a=j.conj().T@j
    return j.conj().T@o@j-(a@o+o@a)/2

cases=[]
product_cases=[]
for n in range(2,7):
    ps=[embed(np.diag([0,1]),j,n) for j in range(n)]
    hs=[embed(np.array([[0,1],[1,0]]),j,n) for j in range(n)]
    js=[embed(np.array([[0,1],[0,0]]),j,n) for j in range(n)]
    pairs=[(j,j+1) for j in range(n-1)]
    P=sum(ps); Q=sum(ps[j]@ps[k] for j,k in pairs)
    A=128.; B=1.; C=8.
    for eps in [0.001,0.003,0.01,0.03,0.05]:
        F=A*eps**2*P+B*Q
        H=eps*sum(hs)
        LF=1j*(H@F-F@H)+sum(adj_diss(j,F) for j in js)
        # Claimed concrete diagnostic inequality has source proportional to n.
        residual=LF+0.5*A*eps**2*P+0.5*B*Q-C*A*eps**4*n*np.eye(2**n)
        top=float(np.linalg.eigvalsh(residual)[-1])
        cases.append(dict(n=n,epsilon=eps,max_eigenvalue=top))
        delta=.01
        G=np.diag(np.exp(2*delta*np.diag(F).real))
        LG=1j*(H@G-G@H)+sum(adj_diss(j,G) for j in js)
        rhs=(-.25*delta*A*eps**2*P-.25*delta*B*Q+C*delta*A*eps**4*n*np.eye(2**n))@G
        ginv=np.diag(1/np.sqrt(np.diag(G)))
        product_top=float(np.linalg.eigvalsh(ginv@(LG-rhs)@ginv)[-1])
        product_cases.append(dict(n=n,epsilon=eps,max_relative_eigenvalue=product_top))
assert max(c['max_eigenvalue'] for c in cases)<=1e-11
assert max(c['max_relative_eigenvalue'] for c in product_cases)<=1e-11
print(json.dumps({'scope':'Independent reset qubits on paths; exact dense operator check only','A':128,'B':1,'C':8,'inequality':'L F <= -.5 A eps^2 sum P -.5 B sum adjacent PiPj + C A eps^4 n I','cases':cases,'multiplicative_delta':.01,'multiplicative_cases':product_cases,'all_pass':True},indent=2))
