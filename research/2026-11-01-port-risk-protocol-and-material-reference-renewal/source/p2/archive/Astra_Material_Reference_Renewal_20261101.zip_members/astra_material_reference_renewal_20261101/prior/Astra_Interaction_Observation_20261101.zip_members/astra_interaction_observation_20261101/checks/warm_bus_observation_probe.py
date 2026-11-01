"""Exact finite passive-collision dilation; exploratory, no network."""
import numpy as np
from scipy.linalg import block_diag

def model(N=80,T=2.,kh=.3,kc=1.,phase=.1):
    dt=T/N
    ch=np.exp(-kh*dt/2); sh=np.sqrt(1-ch*ch)
    cc=np.exp(-kc*dt/2); sc=np.sqrt(1-cc*cc)
    r=ch*cc
    m=1+2*N
    U=np.eye(m); d=np.zeros(m,complex); phi=0.; E=0.
    # prescribed finite closed trajectory
    B=(np.exp(2j*np.pi*np.arange(N+1)/N)-1)*np.sqrt(phase/(2*np.pi))
    for k in range(N):
        alpha=B[k+1]-r*B[k]
        phi+=np.imag(alpha*np.conj(d[0]))
        d[0]+=alpha; E+=abs(alpha)**2/dt
        for mode,c,s in ((1+2*k,ch,sh),(2+2*k,cc,sc)):
            old0=U[0].copy(); oldm=U[mode].copy()
            U[0]=c*old0+s*oldm; U[mode]=-s*old0+c*oldm
            x,y=d[0],d[mode]; d[0]=c*x+s*y; d[mode]=-s*x+c*y
    hot=np.zeros(m);hot[0]=1;hot[1::2]=1
    H=U@np.diag(hot)@U.T
    L=np.column_stack((np.sqrt(2)*d.imag,-np.sqrt(2)*d.real)).reshape(-1)
    O=np.kron(np.eye(m),np.array([[0,1],[-1,0]]))
    inds=np.ravel(np.column_stack((2*np.arange(2,m,2),2*np.arange(2,m,2)+1)))
    C=np.eye(2*m)[inds]
    return H,L,O,C,phi,E,d,U

def run():
    H,L,O,C,phi,E,d,U=model()
    print('phi',phi,'E',E,'closure',abs(d[0]))
    out=[]
    for n in (0,1,10,100,1e3,1e4,1e6):
        V=np.kron(.5*np.eye(H.shape[0])+n*H,np.eye(2))
        Y=C@V@C.T+.5*np.eye(C.shape[0])
        k=np.linalg.solve(Y,C@V@L)
        residual=L-k@C
        var=residual@V@residual+.5*(k@k)
        shift=.5*L@O@C.T@k
        out.append((n,var,phi-shift,shift,k@k))
    for row in out:print(row)
    return out

if __name__=='__main__':run()
