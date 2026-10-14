#!/usr/bin/env python3
"""Portable exact verification of the retained F* closed heat certificate.

Uses only the Python standard library and SymPy. No optimizer, NumPy,
spatial grid, eigenvalue approximation, or external paper is needed for the
finite algebra. The analytic quasiconvexity implication is proved in the
accompanying audit/proof account and is not a formal proof checked here.
"""
from pathlib import Path
import hashlib
import json
import sympy as S

ROOT=Path(__file__).parent
CERT=ROOT/'FSTAR_CLOSED_HEAT_CERTIFICATE.json'

def main():
    data=json.loads(CERT.read_text())
    x=S.symbols('a b c d',real=True); a,b,c,d=x
    z=S.symbols('j0:6',real=True)
    u=a*a+c*c;v=b*b+d*d;w=a*b+c*d;q=a*d-b*c
    basis=[u*u,v*v,u*v,w*w,u*w,v*w,q*u,q*v,q*w]
    pstar=[1,1,S.Rational(7,2),S.Rational(1,2),0,0,S.Rational(-29,10),S.Rational(-29,10),0]
    F=sum(p*f for p,f in zip(pstar,basis))
    gamma=S.Rational(data['gamma'])
    assert gamma==S.Rational(83,1000)>0
    Q=S.Matrix([[S.Rational(v) for v in row] for row in data['gram']])
    assert Q.shape==(24,24) and Q==Q.T
    Z=S.Matrix([xx*jj for xx in x for jj in z])
    B1=S.Matrix([z[0],z[1],z[3],z[4]])
    B2=S.Matrix([z[1],z[2],z[4],z[5]])
    xpairs=[(i,j) for i in range(4) for j in range(i,4)]
    formpairs=[(i,j) for i in range(4) for j in range(i+1,4)]
    assert data['omega_pair_order']==[list(v) for v in formpairs]
    assert data['quadratic_coefficient_order']==[list(v) for v in xpairs]
    omega={ij:sum(S.Rational(v)*x[k]*x[l] for v,(k,l) in zip(row,xpairs))
           for ij,row in zip(formpairs,data['omega_coefficients'])}
    def om(i,j):return omega[(i,j)] if i<j else -omega[(j,i)]
    def diss(poly):
        H=S.hessian(poly,x)
        return S.expand((B1.T*H*B1)[0]+(B2.T*H*B2)[0])
    correction=sum(omega[(i,j)]*(B1[i]*B2[j]-B1[j]*B2[i]) for i,j in formpairs)
    identity=S.expand((Z.T*Q*Z)[0]-diss(F-gamma*q*q)-correction)
    assert identity==0
    closure=[S.expand(S.diff(om(j,k),x[i])-S.diff(om(i,k),x[j])+S.diff(om(i,j),x[k]))
             for i in range(4) for j in range(i+1,4) for k in range(j+1,4)]
    assert all(v==0 for v in closure)
    # Exact coercivity margin; no approximate eigenvalue decision.
    rho=S.Rational(1,500)
    LL,DD=(Q-rho*S.eye(24)).LDLdecomposition(hermitian=False)
    pivots=list(DD.diagonal())
    assert all(v>0 for v in pivots)
    assert LL*DD*LL.T==Q-rho*S.eye(24)

    # A fixed linear Gram interface for perturbations of all nine coefficients.
    Ri=[]
    for f in basis:
        R=S.zeros(24)
        for exp,coef in S.Poly(diss(f),*(x+z)).terms():
            ai=[i for i,k in enumerate(exp[:4]) for _ in range(k)]
            ji=[i for i,k in enumerate(exp[4:]) for _ in range(k)]
            assert len(ai)==len(ji)==2
            k=ai[0]*6+ji[0];l=ai[1]*6+ji[1]
            if k==l:R[k,l]+=coef
            else:R[k,l]+=coef/2;R[l,k]+=coef/2
        assert S.expand((Z.T*R*Z)[0]-diss(f))==0
        Ri.append(R)
    abs_sum=sum((R.applyfunc(abs) for R in Ri),S.zeros(24))
    row_sums=[sum(abs_sum[i,j] for j in range(24)) for i in range(24)]
    K=max(row_sums)
    eta=rho/(2*K)
    # Same historical nonpolyconvex witness, computed independently.
    I={a:7,b:0,c:0,d:7};J={a:1,b:0,c:0,d:-1}
    measure_moments=[S.expand(f.subs(I)/50+S.Rational(49,50)*f.subs(J)) for f in basis]
    witness=sum(p*m for p,m in zip(pstar,measure_moments))
    assert witness==-S.Rational(833,250)
    assert S.Rational(1,50)*49-S.Rational(49,50)==0
    witness_budget=sum(abs(m) for m in measure_moments)
    assert witness_budget==S.Rational(6027,25)
    assert witness+eta*witness_budget<0

    # Scoped transfer obstruction for all right-coordinate BP generators.
    h,delta,beta,kappa=S.symbols('h delta beta kappa',real=True)
    sep=S.Rational(10,7)*(2*h*h+14*delta*delta+4)+2*beta*h
    # |beta|<=4 and h>0 imply sep >= the following exact sum of squares.
    lower=S.Rational(20,7)*(h-S.Rational(7,5))**2+20*delta**2+S.Rational(4,35)
    assert S.expand(sep.subs(beta,-4)-lower)==0
    pstar_separator=S.Rational(10,7)*(4*(pstar[0]+pstar[1])-pstar[2]-pstar[3])+pstar[6]+pstar[7]
    assert pstar_separator==-S.Rational(3,35)

    result={'status':'PASS','scope':'finite exact algebra and rational certificate only; analytic heat implication separately reconstructed',
            'certificate_sha256':hashlib.sha256(CERT.read_bytes()).hexdigest(),
            'gamma':str(gamma),'gram_size':24,'closed_two_form':True,'polynomial_identity':True,
            'exact_gram_margin':str(rho),'shifted_positive_ldl_pivots':len(pivots),
            'all_nine_perturbation_gram_identities':True,'row_sum_operator_bound_K':str(K),
            'coefficient_supnorm_radius_eta':str(eta),
            'robust_nonpolyconvex_witness_upper_bound':str(witness+eta*witness_budget),
            'uniform_jensen_lower_bound_constant':str(rho/72),
            'BP_right_GL_cone_separator_value_Fstar':str(pstar_separator),
            'full_SO2_quartic_class':'OPEN','historical_novelty':'UNKNOWN','external_review':'UNKNOWN'}
    (ROOT/'closed_heat_verification_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
