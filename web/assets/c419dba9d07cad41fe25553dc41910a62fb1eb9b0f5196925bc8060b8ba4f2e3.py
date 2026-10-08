"""New finite cold-carrier kernel/gap conventions; not a uniform proof."""
import json
import math
from fractions import Fraction
from pathlib import Path

import numpy as np


def hs2(x):
    return float(np.vdot(x,x).real)


def representation(m):
    occ=[(a,b,m-a-b) for a in range(m+1) for b in range(m-a+1)]
    ix={x:i for i,x in enumerate(occ)}
    d=len(occ)
    e=[[np.zeros((d,d)) for j in range(3)] for i in range(3)]
    for col,n in enumerate(occ):
        for i in range(3):
            e[i][i][col,col]=n[i]
            for j in range(3):
                if i==j or not n[j]:
                    continue
                target=list(n)
                target[i]+=1
                target[j]-=1
                e[i][j][ix[tuple(target)],col]=math.sqrt((n[i]+1)*n[j])
    gen=[]
    for i,j in ((0,1),(0,2),(1,2)):
        gen.extend([(e[i][j]+e[j][i])/2,(e[i][j]-e[j][i])/(2j)])
    gen.extend([(e[0][0]-e[1][1])/2,
                (e[0][0]+e[1][1]-2*e[2][2])/(2*math.sqrt(3))])
    cas=np.zeros((d*d,d*d),complex)
    for t in gen:
        ad=np.kron(np.eye(d),t)-np.kron(t.T,np.eye(d))
        cas+=ad@ad
    eig,vec=np.linalg.eigh(cas)
    project=[]
    for ell in range(m+1):
        use=np.abs(eig-ell*(ell+2))<1e-8
        assert use.sum()==(ell+1)**3
        project.append(vec[:,use]@vec[:,use].conj().T)
    return occ,e,project


def nodes(m):
    x,w=np.polynomial.legendre.leggauss(m+1)
    t,wt=(x+1)/2,w/2
    phases=2*m+1
    for t1,w1 in zip(t,wt):
        for t2,w2 in zip(t,wt):
            amps=np.sqrt([t1,(1-t1)*t2,(1-t1)*(1-t2)])
            weight=w1*w2*2*(1-t1)/(phases*phases)
            for a in range(phases):
                for b in range(phases):
                    v=amps*np.exp(2j*math.pi*np.array([a,b,0])/phases)
                    yield v,weight


def kernel(m,temperatures):
    occ,e,project=representation(m)
    d=len(occ)
    bm=np.zeros((d*d,d*d),complex)
    sm={q:np.zeros_like(bm) for q in temperatures}
    z={q:sum((n+1)*q**n for n in range(m+1)) for q in temperatures}
    purity={q:sum((n+1)*q**(2*n) for n in range(m+1))/z[q]**2 for q in temperatures}
    for v,w in nodes(m):
        coherent=np.array([math.sqrt(math.factorial(m)/math.prod(math.factorial(n) for n in ns))*
                           math.prod(v[i]**ns[i] for i in range(3)) for ns in occ])
        pp=np.outer(coherent,coherent.conj())
        flat=pp.ravel(order='F')
        bm+=d*w*np.outer(flat,flat.conj())
        if temperatures:
            nv=sum(v[i]*v[j].conjugate()*e[i][j] for i in range(3) for j in range(3))
            ev,uv=np.linalg.eigh(nv)
            for q in temperatures:
                rho=(uv*(q**(m-ev)/z[q]))@uv.conj().T
                sm[q]+=d*w*np.kron(rho.T,rho)/purity[q]
    pure_error=0.
    for ell,p in enumerate(project):
        b=math.factorial(m)*math.factorial(m+2)/(math.factorial(m-ell)*math.factorial(m+ell+2))
        pure_error=max(pure_error,float(np.linalg.norm(bm@p-b*p,2)))
    assert pure_error<1e-10
    cases=[]
    for q,sq in sm.items():
        equiv_error=0.
        for ell,p in enumerate(project):
            c=float(np.trace(p@sq).real/(ell+1)**3)
            equiv_error=max(equiv_error,float(np.linalg.norm(sq@p-c*p,2)))
            b=math.factorial(m)*math.factorial(m+2)/(math.factorial(m-ell)*math.factorial(m+ell+2))
            assert (1-q)**4*(1-b)<=1-c+1e-10
            assert 1-c<=(1-q)**(-4)*(1-b)+1e-10
        assert equiv_error<1e-10
        cases.append({'q':q,'thermal_equivariance_error':equiv_error})
    return {'m':m,'d':d,'pure_kernel_error':pure_error,'thermal_cases':cases}


def gaps(rng):
    cases=[]
    for m in (1,2,4,8):
        occ,e,_=representation(m) if m<=4 else ([(a,b,m-a-b) for a in range(m+1) for b in range(m-a+1)],None,None)
        d=len(occ)
        for q1,q2 in ((0.,.5),(.2,.7),(.6,.6)):
            probs=np.array([q1**ns[0]*q2**ns[1] for ns in occ])
            probs/=probs.sum()
            rho=np.diag(probs)
            p=np.zeros((d,d))
            p[0,0]=1.
            b=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d))
            left=hs2(rho@b-b@rho)
            right=probs[0]**2*(1-max(q1,q2))**2*hs2(p@b-b@p)
            assert left>=right-1e-10
            cases.append({'m':m,'q1':q1,'q2':q2,'gap_left':left,'gap_right':right})
    return cases


def main():
    scalar=0
    for m in range(1,65):
        for ell in range(m+1):
            d=(m+1)*(m+2)//2
            norm=math.factorial(ell)**2*math.comb(m+ell+2,2*ell+2)
            symbol=(Fraction(2*math.factorial(ell)**2,math.factorial(2*ell+2))*
                    (math.factorial(m)//math.factorial(m-ell))**2)
            actual=Fraction(d,1)*symbol/norm
            expected=Fraction(math.factorial(m)*math.factorial(m+2),
                              math.factorial(m-ell)*math.factorial(m+ell+2))
            assert actual==expected
            scalar+=1
    kernels=[kernel(m,(.3,.6) if m<=3 else ()) for m in range(1,5)]
    gapcases=gaps(np.random.default_rng(1701))
    record={'status':'FINITE-EVIDENCE',
            'scope':'Exact monomial Berezin coefficients, four finite pure CP2 kernels, six isotropic thermal kernels and twelve anisotropic state-gap fixtures only',
            'exact_scalar_cases':scalar,'kernel_cases':kernels,'gap_cases':gapcases,
            'max_pure_kernel_error':max(x['pure_kernel_error'] for x in kernels),
            'asymptotic_or_external_validation':False,'old_tests_rerun':False}
    Path(__file__).with_suffix('.json').write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps({k:v for k,v in record.items() if k not in ('kernel_cases','gap_cases')},indent=2))


if __name__=='__main__':
    main()
