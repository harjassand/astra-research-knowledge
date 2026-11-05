import numpy as np
from scipy.linalg import svdvals
import json
from pathlib import Path

def swap_matrix(q,a,b):
    n=2**q
    p=np.arange(n)
    ba=(p>>(q-1-a))&1
    bb=(p>>(q-1-b))&1
    p=p^((ba^bb)<<(q-1-a))^((ba^bb)<<(q-1-b))
    return np.eye(n)[p]

def data(n,theta):
    d=2**n
    u=np.eye(2*d,dtype=complex)
    for j in range(1,n+1):
        w=swap_matrix(n+1,0,j)
        u=np.cos(theta)*u+1j*np.sin(theta)*(w@u)
    k=[u[a*d:(a+1)*d,b*d:(b+1)*d]/np.sqrt(2) for a in range(2) for b in range(2)]
    t=sum(np.kron(x.conj(),x) for x in k)
    vals=svdvals(t)
    return dict(n=n,theta=theta,largest=vals[:20].tolist(),smallest=vals[-10:].tolist(),mean_square=float(np.mean(vals**2)),mean=float(vals.mean()),near1=int(np.sum(vals>1-1e-10)))

if __name__=='__main__':
    out=[]
    for theta in [0.1,0.4,0.8]:
        for n in [1,2,3,4]:
            r=data(n,theta)
            out.append(r)
            print(json.dumps(r),flush=True)
    with Path(__file__).with_name('spectrum.json').open('w') as f:
        json.dump(out,f,indent=2)
