#!/usr/bin/env python3
"""Independent sparse/finite and exact-integer diagnostics of local current bounds.
Not a laboratory experiment or a rigorous floating-point verifier.
"""
import itertools, json, math, time
from pathlib import Path
from fractions import Fraction
import numpy as np
from scipy import sparse
from scipy.sparse.linalg import spsolve
ROOT=Path(__file__).resolve().parent

def basis_system(n,K,fields=None,U=0,t=1):
    states=[sum(1<<i for i in c) for c in itertools.combinations(range(n),K)]
    index={b:i for i,b in enumerate(states)};m=len(states)
    occ=np.array([[(b>>i)&1 for i in range(n)] for b in states],dtype=int)
    T=np.zeros((m,m),dtype=int);B=np.zeros((m,m),dtype=int)
    for x,b in enumerate(states):
        for i in range(n):
            j=(i+1)%n
            if (b>>i)&1 and not (b>>j)&1:
                y=index[b^(1<<i)^(1<<j)]
                T[y,x]=-t;T[x,y]=-t
                B[y,x]=t;B[x,y]=-t
    if fields is None:fields=np.zeros(n,dtype=int)
    E=occ@np.asarray(fields)+U*np.sum(occ*np.roll(occ,-1,axis=1),axis=1)
    ham=np.sum(np.abs(occ[:,None,:]-occ[None,:,:]),axis=2)
    return states,occ,T,1j*B,E,ham

def spectral_width(w,eta):
    return eta+(32/25)*w*w/(np.hypot((15/4)*eta,w)+(15/4)*eta)

def exact_integer_identities():
    rows=[]
    for n in [4,5,6,7,8]:
        for K in range(1,n):
            states,occ,T,J,E,ham=basis_system(n,K,fields=np.array([(-1)**i for i in range(n)]))
            B=J.imag.astype(int);m=len(states)
            assert np.array_equal(T@B,B@T)
            norm=int(np.sum(B*B))
            expected=2*n*Fraction(K*(n-K),n*(n-1))*m
            assert norm==expected
            item={'n':n,'K':K,'states':m,'hopping_current_commutes_exact':True,'bare_norm_per_site':str(Fraction(norm,n*m))}
            if n%2==0 and n>=6:
                G=(E[:,None]-E[None,:])*B
                C=T@G-G@T
                normC=int(np.sum(C*C))
                expectedC=8*4*n*Fraction(K*(n-K),n*(n-1))*m
                assert normC==expectedC
                assert np.all(C[E[:,None]!=E[None,:]]==0)
                item.update(staggered_second_commutator_norm_per_site=str(Fraction(normC,n*m)),commutes_D_exact=True)
            rows.append(item)
    return rows

def solve_current(n,K,eta,eps,fields,U=0,custom_gamma=None):
    states,occ,T,J0,E,ham=basis_system(n,K,fields=fields,U=U);m=len(states)
    de=E[:,None]-E[None,:]
    psi=lambda z:(32/25)*z*z/(np.hypot((15/4)*eta,z)+(15/4)*eta)
    if custom_gamma is None:gamma=eta*ham/2+psi(de)
    else:
        # Symmetric Gaussian phase law with phi(Delta)=custom_gamma-eta.
        delta=2*abs(float(fields[0])); coeff=(custom_gamma-eta)/delta**2
        gamma=eta*ham/2+coeff*de**2
    H=sparse.csc_matrix(np.diag(E)+eps*T);I=sparse.eye(m,format='csc')
    L=sparse.diags(gamma.flatten(order='F'),format='csc')-1j*(sparse.kron(I,H,format='csc')-sparse.kron(H.T,I,format='csc'))
    j=(eps*J0).flatten(order='F');v=np.eye(m).flatten(order='F')/math.sqrt(m)
    Z=sparse.bmat([[L,sparse.csc_matrix(v[:,None])],[sparse.csc_matrix(v[None,:]),None]],format='csc')
    f=spsolve(Z,np.r_[j,0j])[:-1]
    val=float(np.vdot(j,f).real/(n*m))
    residual=float(np.linalg.norm(L@f-j)/np.linalg.norm(j))
    Jn=float(np.sum(np.abs(J0)**2)/(n*m))
    on=np.abs(J0)>0
    weighted=float(np.sum(np.abs(J0[on])**2*(gamma[on]+de[on]**2/gamma[on]))/(n*m))
    bare=eps**2*Jn**2/weighted
    W=float(np.max(np.abs(de[on])))
    universal=.97*eps**2*Fraction(K*(n-K),n*(n-1))/max(eta,W)
    assert val>=bare-1e-10 and bare>=float(universal)-1e-10
    return val,residual,bare,float(universal)

def staggered_fourier(n,K,eta,eps,delta,gamma):
    # JW boundary twist is (-1)^(K-1) in a fixed K-particle sector.
    shift=0. if K%2 else .5
    k=2*np.pi*(np.arange(n)+shift)/n
    den=gamma+delta**2/(gamma+16*eps**2*np.cos(k)**2/eta)
    alpha=K*(n-K)/(n*(n-1))
    return float(alpha*np.mean(4*eps**2*np.sin(k)**2/den))

def finite_checks():
    rows=[]
    for n,K in [(4,2),(5,2),(6,3),(7,3)]:
        fields=np.array([((i*7+3)%11)-5 for i in range(n)],dtype=int)
        for eps in [.05,.5,2.]:
            v,r,b,u=solve_current(n,K,1,eps,fields,U=3)
            rows.append({'class':'interacting_disordered','n':n,'K':K,'eps':eps,'kappa':v,'bare_certificate':b,'universal_lower':u,'residual':r})
    for n,K in [(6,1),(6,2),(6,3),(8,2),(8,3),(8,4)]:
        for eps in [.05,.5,2.]:
            delta=6.;eta=1.;gam=float(spectral_width(delta,eta));fields=np.array([3*(-1)**i for i in range(n)])
            v,r,b,u=solve_current(n,K,eta,eps,fields)
            exact=staggered_fourier(n,K,eta,eps,delta,gam)
            alpha=K*(n-K)/(n*(n-1));kin=eps**2*2*alpha*gam/(gam*gam+delta*delta)
            upper=kin*(1+4*eps**2*delta**2/(eta*gam*(gam*gam+delta*delta)))
            assert abs(v-exact)<1e-10
            assert v>=kin-1e-10 and v<=upper+1e-10
            rows.append({'class':'staggered','n':n,'K':K,'eps':eps,'gamma':gam,'kappa':v,'fourier_formula':exact,'kinetic':kin,'uniform_upper':upper,'residual':r})
    return rows

def adverse_strong_hopping():
    # A simple allowed baseline controller can beat the kinetic-matched choice.
    n=2048;K=n//2;eta=1.;delta=100.;eps=10000.
    gm=float(spectral_width(delta,eta))
    km=staggered_fourier(n,K,eta,eps,delta,gm)
    kb=staggered_fourier(n,K,eta,eps,delta,eta)
    assert km/kb<.02
    return dict(n=n,K=K,eta=eta,detuning=delta,hopping=eps,matched_current=km,baseline_current=kb,matched_over_baseline=km/kb,
                scope='floating exact-formula diagnostic; strong hopping, not a counterexample to small-hopping uniform perturbative law')

if __name__=='__main__':
    tic=time.perf_counter()
    out={'integer_identities':exact_integer_identities(),'finite_checks':finite_checks(),'strong_hopping_falsifier':adverse_strong_hopping()}
    out['wall_seconds']=time.perf_counter()-tic
    (ROOT/'independent_current_results.json').write_text(json.dumps(out,indent=2))
    print(json.dumps({'identity_cases':len(out['integer_identities']),'finite_cases':len(out['finite_checks']),'max_solve_residual':max(x['residual'] for x in out['finite_checks']),'strong_hopping_ratio':out['strong_hopping_falsifier']['matched_over_baseline'],'wall_seconds':out['wall_seconds']},indent=2))
