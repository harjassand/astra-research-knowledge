"""Own exact SU(d) algebra checks for the new full-separability audit.

No peer code is imported. These checks verify transcription, not the all-N
stopped process or membership theorem. Near-singular points need not be in
the candidate's chosen stopping domain. Matrices are at most 9-by-9.
"""
from pathlib import Path
import json
import time
import sympy as s

def simplify(M):
    return M.applyfunc(s.simplify)

def basis(d):
    out=[]
    for i in range(d):
        for j in range(i+1,d):
            X=s.zeros(d);X[i,j]=X[j,i]=1/s.sqrt(2);out.append(X)
            Y=s.zeros(d);Y[i,j]=-s.I/s.sqrt(2);Y[j,i]=s.I/s.sqrt(2);out.append(Y)
    for k in range(1,d):
        diag=[1]*k+[-k]+[0]*(d-k-1)
        out.append(s.diag(*diag)/s.sqrt(k*(k+1)))
    return out

def tensor(items):
    M=s.ones(1,1)
    for x in items:M=s.kronecker_product(M,x)
    return M

def dkernel(rho,X,N):
    d=rho.rows
    return sum((tensor([X if j==i else rho for j in range(N)]) for i in range(N)),s.zeros(d**N))

def hkernel(rho,X,N):
    d=rho.rows
    return sum((tensor([X if j in [i,k] else rho for j in range(N)])
                for i in range(N) for k in range(N) if i!=k),s.zeros(d**N))

def local(T,rho):
    t=s.simplify(s.trace(rho*T))
    V=simplify((T*rho+rho*T)/2-t*rho)
    R=simplify(-s.I*(T*rho-rho*T))
    DVV=simplify((T*V+V*T)/2-s.trace(V*T)*rho-t*V)
    DRR=simplify(-s.I*(T*R-R*T))
    return t,V,R,simplify(DVV-DRR/4)

def fixture(d,N,near=False,full=True):
    I=s.eye(d);Ts=basis(d);p=len(Ts)
    assert all(s.simplify(s.trace(Ts[i]*Ts[j]))==int(i==j) for i in range(p) for j in range(p))
    assert simplify(sum((T*T for T in Ts),s.zeros(d)))==s.Rational(p,d)*I
    swap=s.zeros(d*d)
    for i in range(d):
        for j in range(d):swap[j*d+i,i*d+j]=1
    assert simplify(sum((s.kronecker_product(T,T) for T in Ts),s.zeros(d*d)))==swap-s.eye(d*d)/d
    if near:
        eps=s.Rational(1,2**80)
        diag=[eps,1-eps] if d==2 else [eps,s.Rational(2,5),s.Rational(3,5)-eps]
        rot=s.eye(d);rot[0,0]=rot[1,1]=s.Rational(3,5);rot[0,1]=rot[1,0]=s.I*s.Rational(4,5)
        rho=simplify(rot*s.diag(*diag)*rot.conjugate().T)
    elif d==2:
        rho=s.Matrix([[s.Rational(7,12),s.Rational(1,20)+s.I/30],[s.Rational(1,20)-s.I/30,s.Rational(5,12)]])
    else:
        rho=s.Matrix([[s.Rational(5,12),s.Rational(1,20)+s.I/30,s.Rational(1,24)-s.I/32],
                      [s.Rational(1,20)-s.I/30,s.Rational(1,3),-s.Rational(1,28)+s.I/40],
                      [s.Rational(1,24)+s.I/32,-s.Rational(1,28)-s.I/40,s.Rational(1,4)]])
    assert s.trace(rho)==1
    alpha,delta=s.Rational(3,5),s.Rational(1,100)
    Tu=Ts[0]/5-Ts[1]/7+Ts[-1]/9
    Tb=Ts[1]/11+Ts[-1]/13
    terms=[(alpha,T) for T in Ts]+[(delta,Tu)]
    a=s.zeros(d);mCt=0;sC=0;corr=s.zeros(d)
    ell_quad=0;ell_qv=0
    inv=rho.inv()
    for lam,T in terms:
        t,V,R,cor=local(T,rho)
        assert s.simplify(s.trace(inv*V)+d*t)==0
        assert s.simplify(s.trace(inv*R))==0
        mCt+=lam*t*t;sC+=lam*s.trace(rho*T*T)
        a+=2*lam*t*V;corr+=lam*cor
        ell_quad+=lam*(-s.trace(inv*V*inv*V)+s.trace(inv*R*inv*R)/4)/N
        ell_qv+=2*lam*(s.trace(inv*V)**2-s.trace(inv*R)**2/4)/N
    bt=s.trace(rho*Tb)
    a=simplify(a+corr/N+local(Tb,rho)[1])
    Lell=s.simplify(s.trace(inv*a)+ell_quad)
    closed=s.simplify(-d*(2-s.Rational(1,N))*mCt-d*sC/N-d*bt)
    assert s.simplify(Lell-closed)==0
    assert s.simplify(ell_qv-2*d*d*mCt/N)==0
    Z=Ts[0]/3+Ts[1]/4+Ts[-1]/5
    z=s.trace(rho*Z);Y=Z-z*I
    form=sum((s.trace(Z*local(T,rho)[1])**2-s.trace(Z*local(T,rho)[2])**2/4 for T in Ts))
    assert s.simplify(form-s.trace(rho*Y*rho*Y))==0
    if full:
        k=tensor([rho]*N)
        U=s.simplify(N*mCt+sC-mCt+N*bt)
        G=U*k+dkernel(rho,a,N)
        K=s.zeros(d**N)
        for lam,T in terms:
            _,V,R,_=local(T,rho)
            G+=lam*(hkernel(rho,V,N)-hkernel(rho,R,N)/4)/N
            F=sum((tensor([T if j==i else I for j in range(N)]) for i in range(N)),s.zeros(d**N))
            K+=lam*F*F/N
        K+=sum((tensor([Tb if j==i else I for j in range(N)]) for i in range(N)),s.zeros(d**N))
        assert simplify(G-(K*k+k*K)/2)==s.zeros(d**N)
        traceK=s.simplify(s.trace(K)/d**N)
        Ctrace=alpha*p+delta*s.trace(Tu*Tu)
        assert s.simplify(traceK-Ctrace/d)==0
    return {'d':d,'N':N,'near_singular':near,'min_seed_eigenvalue_if_near':'2^-80' if near else 'positive by strict diagonal dominance',
            'logdet_drift_and_qv_exact':True,'isotropic_principal_form_exact':True,
            'basis_completeness_exact':True,'full_kernel_and_normalized_trace_exact':full}

if __name__=='__main__':
    start=time.monotonic()
    out={'scope':'Own exact SU2/SU3 fixtures; no peer imports, no all-N theorem by testing',
         'fixtures':[fixture(2,1),fixture(2,2),fixture(3,1),fixture(3,2),fixture(3,1,near=True,full=False)],
         'anisotropy_scope':'Rank-one coefficient perturbation is generic noncommuting algebra test, not asserted inside tiny separability radius.',
         'seconds':time.monotonic()-start}
    Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
