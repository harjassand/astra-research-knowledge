"""Same endpoint, same structured start; ordinary exact background elimination.

Float proposal only. P is PSD by ROC on each rank-one Fourier amplitude,
not by a numerical Hessian hypothesis. No negative result is a QC test.
"""
from pathlib import Path
import hashlib,json,time
import argparse
import numpy as np
from scipy.optimize import minimize


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--seed',choices=['parabola','triad'],default='parabola')
    args=parser.parse_args()
    start=time.perf_counter()
    modes=[(1,0),(0,1),(1,1),(1,-1),(2,0),(0,2),(2,1),(1,2),(2,-1),(1,-2)]
    n=16
    xx,yy=np.meshgrid(2*np.pi*np.arange(n)/n,2*np.pi*np.arange(n)/n,indexing='ij')
    xx,yy=xx.ravel(),yy.ravel();basis=[];labels=[];rates=[]
    for out in range(2):
        for mode in modes:
            phase=mode[0]*xx+mode[1]*yy
            for trig in ('sin','cos'):
                derivative=np.cos(phase) if trig=='sin' else -np.sin(phase)
                z=np.zeros((4,n*n));z[2*out]=mode[0]*derivative;z[2*out+1]=mode[1]*derivative
                basis.append(z);labels.append([out,list(mode),trig]);rates.append(sum(k*k for k in mode))
    basis=np.array(basis);atbasis=-np.array(rates)[:,None,None]*basis
    signs=np.array([1,-1,1,-1])[:,None]
    cof=lambda z:z[[3,2,1,0]]*np.array([1,-1,-1,1])[:,None]
    def data(A):
        T=np.sum(A*A,axis=0);q=A[0]*A[3]-A[1]*A[2];x=np.sum(signs*A*A,axis=0)
        return T,q,x,cof(A)
    def df(A):
        T,q,x,c=data(A)
        return 4*T*A+(24*q+4*x)*c+8*q*signs*A
    def haction(A,V):
        T,q,x,c=data(A);dq=np.sum(c*V,axis=0);dx=2*np.sum(signs*A*V,axis=0)
        return (4*T*V+8*np.sum(A*V,axis=0)*A+(24*dq+4*dx)*c
                +(24*q+4*x)*cof(V)+8*dq*signs*A+8*q*signs*V)
    def hm(A):
        return np.column_stack([haction(A[:,None],np.eye(4)[:,i,None])[:,0] for i in range(4)])
    def evaluate(z,details=False):
        B=np.einsum('v,vag->ag',z,basis);Bt=np.einsum('v,vag->ag',z,atbasis)
        linear=-np.mean(haction(B,Bt),axis=1)
        P=np.zeros((4,4))
        for j,k in enumerate(modes):
            for trig in range(2):
                a=np.array([z[(out*len(modes)+j)*2+trig] for out in range(2)])
                R=np.array([a[0]*k[0],a[0]*k[1],a[1]*k[0],a[1]*k[1]])
                P+=(sum(t*t for t in k)/2)*hm(R)
        vals=np.linalg.eigvalsh(P)
        background=-.5*np.linalg.pinv(P,rcond=1e-12)@linear
        A=B+background[:,None]
        grad=df(A);hat=haction(A,Bt)
        diss=-np.mean(np.sum(grad*Bt,axis=0))
        T=np.sum(B*B,axis=0);den=np.mean(T*T)
        gd=-np.mean(np.sum(basis*hat[None]+atbasis*grad[None],axis=1),axis=1)
        gg=4*np.mean(np.sum(basis*B[None]*T[None,None],axis=1),axis=1)
        if details:return diss/den,background,vals,diss,den
        return diss/den,(gd*den-diss*gg)/(den*den)
    z=np.zeros(len(labels))
    def put(out,k,trig,value):z[labels.index([out,list(k),trig])]=value
    r=7/8
    put(0,(1,0),'sin',r);put(0,(0,1),'sin',r)
    put(1,(2,0),'cos',-r**4/4);put(1,(0,2),'cos',-r**4/4)
    put(1,(1,-1),'cos',r*r/2);put(1,(1,1),'cos',-r*r/2)
    if args.seed=='triad':
        z[:]=0
        # First genuine three-wave cubic background resonance, k1+k2=k3.
        put(0,(0,1),'sin',1.)
        put(0,(1,1),'sin',.5)
        put(1,(1,0),'sin',.5)
        put(1,(1,1),'cos',.5)
    initial=evaluate(z,True);history=[]
    def fun(x):
        y,g=evaluate(x);history.append(float(y));return y,g
    result=minimize(fun,z,jac=True,method='BFGS',options={'gtol':1e-9,'maxiter':700})
    final=evaluate(result.x,True)
    out={'scope':'same endpoint/structured Fourier start with ordinary4x4 background elimination; float proposal',
         'seed':args.seed,
         'modes':modes,'grid_size':n,'variable_labels':labels,'initial_coefficients':z.tolist(),
         'coefficients':result.x.tolist(),'background':final[1].tolist(),
         'initial_ratio':float(initial[0]),'final_ratio':float(final[0]),'dissipation':float(final[3]),
         'normalizer':float(final[4]),'background_quadratic_eigenvalues':final[2].tolist(),
         'optimizer_status':str(result.message),'iterations':int(result.nit),'evaluations':len(history),
         'seconds_after_imports':time.perf_counter()-start,
         'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'random_starts':0}
    name='BACKGROUND_HEAT_PROPOSAL.json' if args.seed=='parabola' else 'TRIAD_BACKGROUND_HEAT_PROPOSAL.json'
    Path(__file__).with_name(name).write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ('initial_ratio','final_ratio','background','optimizer_status','iterations','evaluations','seconds_after_imports')},indent=2))


if __name__=='__main__':main()
