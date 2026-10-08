"""Exact/numerical tests of local projections on two Werner copies."""
import numpy as np
import itertools

def swap(d):
    return np.eye(d*d).reshape(d,d,d,d).transpose(0,1,3,2).reshape(d*d,d*d)

def grouped_tensor(rho,d,k):
    a=rho
    for _ in range(1,k): a=np.kron(a,rho)
    # input coordinates A1 B1 A2 B2 ...; group all Alice then Bob.
    p=list(range(0,2*k,2))+list(range(1,2*k,2))
    return a.reshape((d,)*(4*k)).transpose(p+[2*k+x for x in p]).reshape(d**(2*k),d**(2*k))

def filter_same(rho,d,k,filter):
    f=np.kron(filter,filter)
    return f@grouped_tensor(rho,d,k)@f.conj().T

if __name__=='__main__':
    for d in (3,4):
        F=swap(d)
        v=[]
        for i,j in itertools.combinations(range(d),2):
            a=np.zeros((d,d));a[i,j]=1;a[j,i]=-1;v.append(a.ravel()/np.sqrt(2))
        filt=np.array(v)
        for alpha in (-1,-.5,-1/d):
            out=filter_same(np.eye(d*d)+alpha*F,d,2,filt)
            m=len(v);Fm=swap(m)
            coeff=np.linalg.lstsq(np.array([np.eye(m*m).ravel(),Fm.ravel()]).T,out.ravel(),rcond=None)[0]
            res=np.linalg.norm(out-coeff[0]*np.eye(m*m)-coeff[1]*Fm)
            print(d,alpha,'coeff',coeff,'ratio',coeff[1]/coeff[0],'residual',res)
