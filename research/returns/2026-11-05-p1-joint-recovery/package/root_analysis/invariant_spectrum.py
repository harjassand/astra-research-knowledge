"""Exploratory singular spectrum in the SU(2)-scalar operator sector.
This does not establish a spectral gap on all operators or an asymptotic law.
"""
import numpy as np
from scipy.linalg import svdvals
import json, math
from pathlib import Path
from spectrum import swap_matrix

def dyck_paths(length):
    def rec(p,j):
        if len(p)==length:
            if j==0: yield p
            return
        left=length-len(p)-1
        for new in (j-1,j+1):
            if 0<=new<=left:
                yield from rec(p+[new],new)
    yield from rec([],0)

def state_for_path(path):
    states={0:np.ones(1)}
    j=0
    for J in path:
        newstates={}
        for M in range(-J,J+1,2):
            v=np.zeros(2*len(next(iter(states.values()))))
            # j,J,M are doubled angular momenta.
            if M-1 in states:
                coef=math.sqrt((j+M+1)/(2*(j+1))) if J==j+1 else -math.sqrt((j-M+1)/(2*(j+1)))
                v[::2]+=coef*states[M-1]
            if M+1 in states:
                coef=math.sqrt((j-M+1)/(2*(j+1))) if J==j+1 else math.sqrt((j+M+1)/(2*(j+1)))
                v[1::2]+=coef*states[M+1]
            newstates[M]=v
        states,j=newstates,J
    return states[0]

def scalar_basis(n):
    y=np.array([[0.,1.],[-1.,0.]])
    yn=np.ones((1,1))
    for _ in range(n): yn=np.kron(yn,y)
    return np.array([state_for_path(p).reshape(2**n,2**n)@yn.T for p in dyck_paths(2*n)])

def run(n,theta,basis):
    d=2**n
    u=np.eye(2*d,dtype=complex)
    for j in range(1,n+1):
        # Avoid a dense permutation multiplication.
        w=swap_matrix(n+1,0,j)
        idx=np.argmax(w,axis=1)
        u=np.cos(theta)*u+1j*np.sin(theta)*u[idx]
    ks=[u[a*d:(a+1)*d,b*d:(b+1)*d]/np.sqrt(2) for a in range(2) for b in range(2)]
    out=np.zeros(basis.shape,complex)
    for k in ks: out+=k@basis@k.conj().T
    mat=basis.reshape(len(basis),-1).conj()@out.reshape(len(basis),-1).T
    leakage=float(np.linalg.norm(out.reshape(len(basis),-1).T-basis.reshape(len(basis),-1).T@mat))
    vals=svdvals(mat)
    return dict(n=n,theta=theta,sector_dimension=len(basis),scalar_second=float(vals[1]) if len(vals)>1 else None,largest=vals[:10].tolist(),closure_residual=leakage)

if __name__=='__main__':
    out=[]
    for n in range(2,8):
        basis=scalar_basis(n)
        for theta in [.1,.4,.8]:
            r=run(n,theta,basis)
            out.append(r)
            print(json.dumps(r),flush=True)
    with Path(__file__).with_name('invariant_spectrum.json').open('w') as f: json.dump(out,f,indent=2)
