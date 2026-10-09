"""Candidate global Pick-boundary inversion. Research prototype, no certified rounding."""
import numpy as np
from scipy.linalg import eigh

def free_stieltjes(z, atoms, weights, variance, tol=2e-15):
    z=np.asarray(z,dtype=complex); atoms=np.asarray(atoms); weights=np.asarray(weights)
    g=1/(z-np.dot(atoms,weights))
    for it in range(20000):
        gn=np.sum(weights/(z[:,None]-variance*g[:,None]-atoms),axis=1)
        if np.max(np.abs(gn-g))<tol: return gn
        g=.5*(g+gn)
    raise RuntimeError('Stieltjes fixed point did not converge')

def matrices(z,g,t):
    w=z-t*g
    K=-(g[:,None]-g.conj()[None,:])/(w[:,None]-w.conj()[None,:])
    K=(K+K.conj().T)/2
    S=K-np.outer(g,g.conj())
    L=w[:,None]*K-np.ones((len(z),1))*g.conj()[None,:]
    L=(L+L.conj().T)/2
    return w,K,S,L

def inverse(z,g,iterations=55):
    z=np.asarray(z,dtype=complex);g=np.asarray(g,dtype=complex)
    if np.any(z.imag<=0) or np.any(g.imag>=0): raise ValueError('upper nodes/lower transform required')
    base=matrices(z,g,0.)[2]
    if np.linalg.eigvalsh(base)[0]<-1e-12*max(1.,np.linalg.norm(base,2)):
        raise ValueError('normalized Pick covariance is indefinite at zero; no silent PSD repair')
    upper=float(np.min(1/np.abs(g)**2-z.imag/(-g.imag)))
    if upper < -1e-10: raise ValueError('inconsistent probability transform data')
    lo=0.; hi=max(0.,upper)
    for _ in range(iterations):
        mid=(lo+hi)/2
        v=np.linalg.eigvalsh(matrices(z,g,mid)[2])[0]
        if v>=0:lo=mid
        else:hi=mid
    t=(lo+hi)/2
    w,K,S,L=matrices(z,g,t)
    d,U=eigh(K)
    if d[0]<=0: raise ValueError('singular/nonpositive K; rank reduction needed')
    invroot=(U*(1/np.sqrt(d)))@U.conj().T
    A=invroot@L@invroot
    atoms,V=eigh((A+A.conj().T)/2)
    e=invroot@g
    weights=np.abs(V.conj().T@e)**2
    return {'variance':t,'atoms':atoms,'weights':weights,'K_eigenvalues':d,
            'S_eigenvalues':np.linalg.eigvalsh(S),'mass':float(weights.sum()),
            'interpolation_residual':float(np.max(np.abs(np.sum(weights/(w[:,None]-atoms),axis=1)-g)))}

if __name__=='__main__':
    import json,time
    out=[]
    cases=[([-1,.2,1],[.25,.5,.25]),(np.linspace(-1,1,5),np.ones(5)/5)]
    for a,p in cases:
        a=np.asarray(a);p=np.asarray(p);k=len(a)
        z=np.linspace(-1.4,1.4,k)+.6j
        for t in [.0625,.5625]:
            g=free_stieltjes(z,a,p,t)
            start=time.perf_counter();r=inverse(z,g);r['seconds']=time.perf_counter()-start
            r.update(k=k,true_variance=t,atom_error=float(np.max(abs(r['atoms']-a))),weight_error=float(np.max(abs(r['weights']-p))),variance_error=abs(r['variance']-t))
            out.append({key:value.tolist() if isinstance(value,np.ndarray) else value for key,value in r.items()})
    print(json.dumps(out,indent=2))
