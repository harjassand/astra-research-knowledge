"""ONE structurally seeded finite-Fourier ordinary-heat proposal.

This can propose a negative STATIC heat dissipation. A floating proposal
is not accepted until exact rational qualification. It is not a QC test.
"""
from pathlib import Path
import hashlib,json,time
import numpy as np
from scipy.optimize import minimize


def main():
    start=time.perf_counter()
    modes=[(1,0),(0,1),(1,1),(1,-1),(2,0),(0,2),(2,1),(1,2),(2,-1),(1,-2)]
    n=16
    xx,yy=np.meshgrid(2*np.pi*np.arange(n)/n,2*np.pi*np.arange(n)/n,indexing='ij')
    xx,yy=xx.ravel(),yy.ravel()
    basis=[]; labels=[]; rates=[]
    for out in range(2):
        for mode in modes:
            phase=mode[0]*xx+mode[1]*yy
            for trig in ('sin','cos'):
                derivative=np.cos(phase) if trig=='sin' else -np.sin(phase)
                z=np.zeros((4,n*n))
                z[2*out]=mode[0]*derivative;z[2*out+1]=mode[1]*derivative
                basis.append(z);labels.append([out,list(mode),trig]);rates.append(sum(j*j for j in mode))
    basis=np.array(basis);rates=np.array(rates)
    atbasis=-rates[:,None,None]*basis
    signs=np.array([1,-1,1,-1])[:,None]
    def fields(x):return np.einsum('v,vag->ag',x,basis),np.einsum('v,vag->ag',x,atbasis)
    def get(x,coeff=(1.,12.,4.)):
        A,At=fields(x);ka,kq,kx=coeff
        norm=np.sum(A*A,axis=0);q=A[0]*A[3]-A[1]*A[2]
        hopf=np.sum(signs*A*A,axis=0);cof=A[[3,2,1,0]]*np.array([1,-1,-1,1])[:,None]
        dq=np.sum(cof*At,axis=0);dx=2*np.sum(signs*A*At,axis=0)
        grad=4*ka*norm*A+(2*kq*q+kx*hopf)*cof+2*kx*q*signs*A
        hat=(4*ka*norm*At+8*ka*np.sum(A*At,axis=0)*A
             +(2*kq*dq+kx*dx)*cof+(2*kq*q+kx*hopf)*At[[3,2,1,0]]*np.array([1,-1,-1,1])[:,None]
             +2*kx*dq*signs*A+2*kx*q*signs*At)
        diss=-np.mean(np.sum(grad*At,axis=0));den=np.mean(norm*norm)
        gd=-np.mean(np.sum(basis*hat[None]+atbasis*grad[None],axis=1),axis=1)
        gg=4*np.mean(np.sum(basis*A[None]*norm[None,None],axis=1),axis=1)
        return diss/den,(gd*den-diss*gg)/(den*den),diss,den
    x=np.zeros(len(labels))
    def setcoef(out,mode,trig,val):x[labels.index([out,list(mode),trig])]=val
    # The SAME g/parabola heat state, exp(-t)=7/8, already exact in ROOT26.
    r=7/8
    setcoef(0,(1,0),'sin',r);setcoef(0,(0,1),'sin',r)
    setcoef(1,(2,0),'cos',-r**4/4);setcoef(1,(0,2),'cos',-r**4/4)
    setcoef(1,(1,-1),'cos',r*r/2);setcoef(1,(1,1),'cos',-r*r/2)
    control=get(x,(2.**-100,1.,0.))
    expected=-(93530955/4294967296-2.**-100*10646839890629509/1125899906842624)
    assert abs(control[2]-expected)<1e-12
    first=get(x)
    history=[]
    def fun(z):
        y,g,_,_=get(z);history.append(float(y));return y,g
    result=minimize(fun,x,jac=True,method='BFGS',options={'gtol':1e-9,'maxiter':700})
    final=get(result.x)
    out={'scope':'one fixed endpoint; one structured Fourier start, float proposal only',
         'grid_size':n,'modes':modes,'variable_labels':labels,'initial_coefficients':x.tolist(),
         'final_coefficients':result.x.tolist(),'initial_ratio':float(first[0]),'final_ratio':float(final[0]),
         'final_dissipation':float(final[2]),'normalizer_norm4':float(final[3]),
         'status':str(result.message),'success':bool(result.success),'iterations':int(result.nit),
         'evaluations':len(history),'min_history':min(history),'random_starts':0,
         'control_is_frozen_old_static_state':True,'control_difference':float(control[2]-expected),
         'seconds_after_imports':time.perf_counter()-start,
         'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    Path(__file__).with_name('HEAT_FIELD_PROPOSAL.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ('initial_ratio','final_ratio','status','iterations','evaluations','seconds_after_imports')},indent=2))


if __name__=='__main__':main()
