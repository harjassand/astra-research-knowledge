"""Independent product-basis challenge of the three-copy necessary maps.

No constructor or prior-auditor source is imported. Clebsch-Gordan vectors
build the physical matrices; their actions are compared with the proposed
6j formulas. Tests include genuinely complex rank-two projectors and arbitrary
complex invariant operators, not only real or code-derived examples.
"""
from pathlib import Path
from functools import lru_cache
import hashlib
import json
import numpy as np
import sympy as s
from sympy.physics.wigner import clebsch_gordan, wigner_6j

ROOT=Path(__file__).resolve().parent


@lru_cache(None)
def cg(a,b,c,u,v,w):
    return float(clebsch_gordan(s.Rational(a,2),s.Rational(b,2),s.Rational(c,2),
                               s.Rational(u,2),s.Rational(v,2),s.Rational(w,2)))


def run(n):
    D=n+1;j=s.Rational(n,2);rng=np.random.default_rng(93000+n)
    pairs={}
    for l in range(D):
        C=np.zeros((D*D,2*l+1))
        for i in range(D):
            for k in range(D):
                u=2*i-n;v=2*k-n;m=u+v
                if abs(m)<=2*l:C[i*D+k,(m+2*l)//2]=cg(n,n,2*l,u,v,m)
        pairs[l]=C
    blocks={}
    for J2 in range(n%2,3*n+1,2):
        ls=[l for l in range(D) if abs(2*l-n)<=J2<=2*l+n]
        Q=np.zeros((D**3,J2+1,len(ls)))
        for i in range(D):
            for k in range(D):
                for z in range(D):
                    u,v,w=2*i-n,2*k-n,2*z-n;M=u+v+w
                    if abs(M)>J2:continue
                    for t,l in enumerate(ls):
                        Q[(i*D+k)*D+z,(M+J2)//2,t]=cg(n,n,2*l,u,v,u+v)*cg(2*l,n,J2,u+v,w,M)
        U=np.array([[float((-1)**(n+l+lp)*s.sqrt((2*l+1)*(2*lp+1))*
                          wigner_6j(j,j,l,j,s.Rational(J2,2),lp))
                     for lp in ls] for l in ls])
        V=np.diag([(-1)**(n-l) for l in ls])
        blocks[J2]={'ls':ls,'Q':Q,'U':U,'V':V}
    basis=np.concatenate([b['Q'].reshape(D**3,-1) for b in blocks.values()],axis=1)
    err_basis=np.max(abs(basis.conj().T@basis-np.eye(D**3)))
    A=rng.normal(size=(D,2))+1j*rng.normal(size=(D,2));A=np.linalg.qr(A)[0];P=A@A.conj().T
    Xraw=np.kron(np.kron(P,P),P);X=np.zeros_like(Xraw)
    errors={'basis_orthogonality':float(err_basis)}
    errs_swap=[];errs_anti=[];errs_kl0=[]
    for J2,b in blocks.items():
        Q,ls,U,V=b['Q'],b['ls'],b['U'],b['V'];h=len(ls)
        R=np.einsum('ami,ab,bmj->ij',Q,Xraw,Q)/(J2+1)
        b['R']=R
        X+=np.einsum('ami,ij,bmj->ab',Q,R,Q)
        SQ=Q.reshape(D,D,D,J2+1,h).transpose(0,2,1,3,4).reshape(D**3,J2+1,h)
        direct=np.einsum('ami,amj->ij',Q,SQ)/(J2+1)
        errs_swap.append(np.max(abs(direct-U)))
        I=np.eye(h);Pa=(I-V-U-V@U@V+V@U+U@V)/6
        errs_anti.append(np.max(abs(Pa@R)))
    errors['permutation_6j']=float(max(errs_swap))
    errors['rank2_antisymmetric_vanishes']=float(max(errs_anti))
    errors['trace8']=float(abs(np.trace(X)-8))
    # Direct product-basis partial time reversal on copy three.
    Y=np.zeros((D,D))
    for i in range(D):Y[n-i,i]=(-1)**(n-i)
    YY=np.kron(np.eye(D*D),Y)
    def reverse(Z):
        T=Z.reshape(D,D,D,D,D,D).transpose(0,1,5,3,4,2).reshape(D**3,D**3)
        return YY@T@YY.conj().T
    Z=reverse(X)
    expected={J2:np.einsum('ami,ab,bmj->ij',b['Q'],Z,b['Q'])/(J2+1)
              for J2,b in blocks.items()}
    # Also test the same linear map on arbitrary complex invariant blocks.
    arbitrary=np.zeros_like(X);arb_R={}
    for J2,b in blocks.items():
        h=len(b['ls']);A=rng.normal(size=(h,h))+1j*rng.normal(size=(h,h));R=A+A.conj().T
        arb_R[J2]=R;arbitrary+=np.einsum('ami,ij,bmj->ab',b['Q'],R,b['Q'])
    arbitrary_pt=reverse(arbitrary)
    arb_expected={J2:np.einsum('ami,ab,bmj->ij',b['Q'],arbitrary_pt,b['Q'])/(J2+1)
                  for J2,b in blocks.items()}
    ep=ea=0.0
    for l in range(D):
        for lp in range(D):
            allowed=[J2 for J2,b in blocks.items() if l in b['ls'] and lp in b['ls']]
            ranks=list(range(abs(l-lp),min(l+lp,n)+1))
            C=np.array([[float((-1)**(lp+j+s.Rational(J2,2)+r)*wigner_6j(l,j,s.Rational(J2,2),j,lp,r))
                         for r in ranks] for J2 in allowed])
            F=(C*np.array([(-1)**r*(2*r+1) for r in ranks]))@C.T@np.diag([J2+1 for J2 in allowed])
            vals=np.array([blocks[J2]['R'][blocks[J2]['ls'].index(l),blocks[J2]['ls'].index(lp)] for J2 in allowed])
            av=np.array([arb_R[J2][blocks[J2]['ls'].index(l),blocks[J2]['ls'].index(lp)] for J2 in allowed])
            pred=F@vals;apred=F@av
            for z,J2 in enumerate(allowed):
                ix=blocks[J2]['ls'].index(l);iy=blocks[J2]['ls'].index(lp)
                ep=max(ep,abs(pred[z]-expected[J2][ix,iy]));ea=max(ea,abs(apred[z]-arb_expected[J2][ix,iy]))
    errors['complex_rank2_partial_reversal']=float(ep)
    errors['arbitrary_complex_invariant_partial_reversal']=float(ea)
    # Pair-spin normalization and complement operator positivity.
    X2raw=np.kron(P,P);w=np.array([np.trace(C.conj().T@X2raw@C).real for C in pairs.values()])
    X2=sum((w[l]/(2*l+1))*(C@C.T) for l,C in pairs.items());B12=np.kron(X2,np.eye(D))
    errors['pair_weights_sum4']=float(abs(sum(w)-4))
    a=np.zeros(D);enum_b=np.zeros(D)
    for r in range(D):
        for q in range(-r,r+1):
            T=np.zeros((D,D))
            for u in range(D):
                for v in range(D):
                    if u-v==q:T[u,v]=(-1)**(n-v)*cg(n,n,2*r,2*u-n,n-2*v,2*q)
            a[r]+=(D/4)*abs(np.trace(P@T))**2
            enum_b[r]+=(D/2)*np.trace(P@T.conj().T@P@T).real
    M=np.array([[float((2*k+1)*(-1)**(n+k+l)*wigner_6j(j,j,k,j,j,l))
                 for l in range(D)] for k in range(D)])
    errors['enumerator_MacWilliams_b_equals_2Ma']=float(np.max(abs(enum_b-2*M@a)))
    errors['enumerator_a0_equals1']=float(abs(a[0]-1))
    errors['enumerator_sum_D_over2']=float(abs(sum(a)-D/2))
    errors['pair_weight_transform']=float(np.max(abs(w-(4/D)*M@(np.array([(-1)**l for l in range(D)])*a))))
    marginal=np.zeros(D,dtype=complex)
    for J2,b in blocks.items():
        for z,l in enumerate(b['ls']):marginal[l]+=(J2+1)*b['R'][z,z]
    errors['marginal_Kw']=float(np.max(abs(marginal-2*w)))
    eigmins={name:float(np.linalg.eigvalsh((T+T.conj().T)/2)[0])
             for name,T in [('R',X),('PPT',Z),('BminusR',B12-X),('BminusPPT',B12-Z)]}
    # Independently check the lifted-KL recoupling coefficient vectors by
    # product-basis rank-r operator contractions. A convention-dependent
    # common sign is harmless, but the complete J dependence must agree.
    coef_errors=[];common_factors=[];tested=0
    for l in range(D):
        for lp in range(D):
            allowed=[J2 for J2,b in blocks.items() if l in b['ls'] and lp in b['ls']]
            for r in range(abs(l-lp),min(l+lp,n,4)+1):
                A=np.zeros((2*l+1,2*lp+1))
                for u in range(-l,l+1):
                    if abs(u)<=lp:A[u+l,u+lp]=(-1)**(lp-u)*cg(2*l,2*lp,2*r,2*u,-2*u,0)
                T=np.diag([(-1)**(n-i)*cg(n,n,2*r,2*i-n,n-2*i,0) for i in range(D)])
                Op=np.kron(pairs[l]@A@pairs[lp].T,T)
                actual=[];pred=[]
                for J2 in allowed:
                    b=blocks[J2];Ql=b['Q'][:,:,b['ls'].index(l)];Qp=b['Q'][:,:,b['ls'].index(lp)]
                    actual.append(np.einsum('am,ab,bm->',Ql,Op,Qp))
                    pred.append((J2+1)*float((-1)**(lp+j+s.Rational(J2,2)+r)*wigner_6j(l,j,s.Rational(J2,2),j,lp,r)))
                actual=np.array(actual);pred=np.array(pred)
                scale=float(actual@pred/(pred@pred));assert abs(scale)>1e-10
                assert abs(scale-(-1)**r)<1e-10,(n,l,lp,r,scale)
                coef_errors.append(np.max(abs(actual-scale*pred)));common_factors.append(scale);tested+=1
    errors['lifted_KL_full_J_coefficient_vector']=float(max(coef_errors))
    for l in range(D):
        value=0j
        for J2,b in blocks.items():
            if l in b['ls']:
                z=b['ls'].index(l);coef=float((-1)**(l+j+s.Rational(J2,2))*wigner_6j(l,j,s.Rational(J2,2),j,l,0))
                value+=(J2+1)*coef*(b['R']@(b['U']-np.eye(len(b['ls']))/2))[z,z]
        errs_kl0.append(abs(value))
    errors['rank_zero_lift_for_arbitrary_complex_projector']=float(max(errs_kl0))
    assert max(errors.values())<1e-10,(n,errors)
    assert min(eigmins.values())>-1e-10,(n,eigmins)
    return {'n':n,'errors':errors,'minimum_eigenvalues':eigmins,
            'KL_coefficient_vectors_tested':tested,
            'KL_common_factor_range':[min(common_factors),max(common_factors)],
            'all_checks_passed':True}


if __name__=='__main__':
    results={'tests':[run(n) for n in [1,2,3,4]],
             'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
             'scope':'Finite independent convention checks, not substitutes for the general recoupling identities.'}
    (ROOT/'complex_recoupling_results.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps(results,indent=2))
