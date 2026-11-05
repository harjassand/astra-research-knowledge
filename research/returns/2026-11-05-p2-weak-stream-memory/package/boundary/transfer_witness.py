"""Exact MPO contractions of bath-transfer trial operators.

The auxiliary transfer matrix is 64x64 regardless of the prefix length.
These give variational UPPER bounds on the commutator gap, not lower bounds.
"""
import json
from pathlib import Path
import numpy as np

P=[np.eye(2,dtype=complex),np.array([[0,1],[1,0]],complex),
   np.array([[0,-1j],[1j,0]],complex),np.diag([1.,-1.]).astype(complex)]
W=np.array([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]],complex)


def local_data(theta,phi):
    u=np.cos(theta)*np.eye(4)+1j*np.sin(theta)*W
    pp=[np.kron(a,b) for a in P for b in P]
    g=np.array([[np.trace(a@u.conj().T@b@u)/4 for b in pp] for a in pp]).real
    g=g.reshape(4,4,4,4)
    f=[(np.cos(phi)+.5j*np.sin(phi))*P[0]]+[.5j*np.sin(phi)*a for a in P[1:]]
    b=[sum(np.kron(g[:,q,:,p].T,f[p]) for p in range(4)) for q in range(4)]
    e=sum(np.kron(t,t.conj()) for t in b)
    e0=sum(np.kron(t,t.conj()) for t in f)
    z=np.zeros((4,4));z[0,0]=1
    z=np.kron(z,np.eye(2)/2)
    return e,e0,np.kron(z,z.conj()),f,b


def witness(n,theta,phi):
    e,e0,zz,f,b=local_data(theta,phi)
    norm=float((np.trace(np.linalg.matrix_power(e0,n))/4).real)
    image=float(np.trace(zz@np.linalg.matrix_power(e,n)).real)
    scalar=abs(np.cos(phi)+.5j*np.sin(phi))**(2*n)
    denom=norm-scalar
    return {'n':n,'theta':theta,'phi':phi,'norm2':norm,'image_norm2':image,
            'traceless_norm2':denom,'gap_upper_bound':(8/3)*(norm-image)/denom if denom>1e-14 else None}


def diagnostic():
    from commutant_probe import source_swap
    for n in (1,2,3,4):
        theta=.3;phi=.47;d=1<<n
        u=np.eye(2*d,dtype=complex);v=u.copy()
        for j in range(1,n+1):
            swap=source_swap(n,j)
            u=(np.cos(theta)*np.eye(2*d)+1j*np.sin(theta)*swap)@u
            v=(np.cos(phi)*np.eye(2*d)+1j*np.sin(phi)*swap)@v
        k=(v[:d,:d]+v[d:,d:])/2
        out=u.conj().T@np.kron(np.eye(2),k)@u
        image=(out[:d,:d]+out[d:,d:])/2
        ans=witness(n,theta,phi)
        assert abs(ans['norm2']-np.trace(k.conj().T@k).real/d)<1e-11
        assert abs(ans['image_norm2']-np.trace(image.conj().T@image).real/d)<1e-11


if __name__=='__main__':
    diagnostic()
    result=[]
    for theta in (.1,.3):
        for phi in (theta,.3,.6,1.,np.pi/2):
            for n in (2,10,100,1000,10000):
                item=witness(n,theta,phi)
                result.append(item)
                print(json.dumps(item),flush=True)
    (Path(__file__).parent/'transfer_witness.json').write_text(json.dumps(result,indent=2)+'\n')
