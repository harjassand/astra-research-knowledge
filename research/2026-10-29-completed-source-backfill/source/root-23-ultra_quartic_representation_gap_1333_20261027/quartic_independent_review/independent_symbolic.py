#!/usr/bin/env python3
"""Independent literal quartic/certificate check through SymPy exact algebra.

No producer/root verifier imported. Analytic all-degree/global conclusions
are reviewed separately; finite algebra alone is not that argument.
"""
from itertools import combinations_with_replacement as cwr
from pathlib import Path
import hashlib
import json
import time
import sympy as S


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    started=time.perf_counter()
    folder=Path(__file__).resolve().parent
    base=folder.parent
    pp=base/"quartic_alternative/sector_gap/EXACT_MULTIPLIER_SUPPORT.json"
    np=base/"principal_combined_quartic/EXACT_SUPPORT_SEPARATOR.json"
    pos=json.loads(pp.read_text())
    neg=json.loads(np.read_text())
    A=S.symbols("a b c d")
    X=S.symbols("h i j k")
    variables=A+X
    a,b,c,d=A
    u=a*a+c*c
    v=b*b+d*d
    cross=a*b+c*d
    determinant=a*d-b*c
    F=u*u+v*v+3*cross*cross+S.Rational(113,10)*determinant**2+4*determinant*(u-v)
    kappa=S.Rational(14611,2500)*(u-v)+S.Rational(110757,5000)*determinant
    detX=X[0]*X[3]-X[1]*X[2]
    normX=sum(x*x for x in X)
    replacement={z:z+x for z,x in zip(A,X)}

    def bregman(f):
        return S.Poly(S.expand(f.xreplace(replacement)-f-
                              sum(S.diff(f,z)*x for z,x in zip(A,X))),*variables)

    BF=bregman(F)
    P=BF-S.Poly(kappa*detX,*variables)
    target=S.Poly(normX,*variables)*P
    z60=[z*x*y for z in A for x,y in cwr(X,2)]
    z60 += [x*y*z for x,y,z in cwr(X,3)]
    assert len(z60)==60
    exps=[S.Poly(z,*variables).monoms()[0] for z in z60]
    R=S.Matrix([[S.Rational(q) for q in row] for row in pos["gram"]])
    assert R==R.T and R.shape==(60,60)
    gram={}
    for i in range(60):
        for j in range(60):
            if R[i,j]:
                e=tuple(x+y for x,y in zip(exps[i],exps[j]))
                gram[e]=gram.get(e,S.Rational(0))+R[i,j]
    gram_poly=S.Poly.from_dict(gram,variables)
    assert gram_poly==target
    L,D=(R-S.eye(60)/200).LDLdecomposition(hermitian=False)
    assert all(D[i,i]>0 for i in range(60))
    assert L*D*L.T==R-S.eye(60)/200
    positive_seconds=time.perf_counter()-started

    functional={tuple(e):S.Rational(q) for e,q in zip(neg["monomial_order"],neg["lambda"])}

    def pair(poly):
        return sum(q*functional[e] for e,q in poly.terms())

    z26=[z*x for z in A for x in X]+[x*y for x,y in cwr(X,2)]
    assert len(z26)==26
    M=S.Matrix(26,26,lambda i,j:pair(S.Poly(z26[i]*z26[j],*variables)))
    assert M==S.Matrix([[S.Rational(q) for q in row] for row in neg["moment26"]])
    l,dmat=M.LDLdecomposition(hermitian=False)
    assert all(dmat[i,i]>0 for i in range(26))
    assert l*dmat*l.T==M
    annihilators=[pair(S.Poly(x*y*detX,*variables)) for x,y in cwr(A,2)]
    assert annihilators==[0]*10
    energy_pairing=pair(BF)
    assert energy_pairing==-S.Rational(39,125000)

    sensitivity=S.Rational(0)
    monomial_count=0
    for indices in cwr(range(4),4):
        monomial=S.prod(A[i] for i in indices)
        B=bregman(monomial)
        assert sum(abs(q) for q in B.coeffs())==11
        weighted=S.Poly(normX,*variables)*B
        assert sum(abs(q) for q in weighted.coeffs())==44
        sensitivity+=abs(pair(B))
        monomial_count+=1
    assert monomial_count==35 and sensitivity==S.Rational(69749,25000)

    # Check the full perturbation image is in the degree6 Gram-product span,
    # independently of which particular Gram entry an implementation chooses.
    products={tuple(x+y for x,y in zip(e,f)) for e in exps for f in exps}
    required=set()
    for na,nx in ((2,4),(1,5),(0,6)):
        for ia in cwr(range(4),na):
            for ix in cwr(range(4),nx):
                e=[0]*8
                for i in ia:e[i]+=1
                for i in ix:e[i+4]+=1
                required.add(tuple(e))
    assert len(required)==658 and required==products
    epsilon=S.Rational(1,616000)
    assert S.Rational(1,200)-1540*epsilon==S.Rational(1,400)
    perturbed_pairing_upper=energy_pairing+epsilon*sensitivity
    assert perturbed_pairing_upper<0

    # Row-major cofactor is the derivative of determinant, not adjugate.
    cofactor=[d,-c,-b,a]
    assert [S.diff(determinant,z) for z in A]==cofactor
    det_expansion=S.expand(determinant.xreplace(replacement)-determinant-
                           sum(z*x for z,x in zip(cofactor,X))-detX)
    assert det_expansion==0
    euler=S.expand(sum(S.diff(F,z)*z for z in A)-4*F)
    assert euler==0
    xminus={x:-z for x,z in zip(X,A)}
    assert S.expand(P.as_expr().xreplace(xminus)-(3*F-kappa*determinant))==0

    result={"status":"exact literal algebra independently passed; analytic review separate",
            "positive_input_sha256":sha(pp),"negative_input_sha256":sha(np),
            "positive_gram_size":60,"negative_moment_size":26,
            "all_positive_shifted_LDL_pivots":True,
            "all_negative_LDL_pivots":True,
            "positive_polynomial_identity":True,
            "feature_product_exponent_count":len(products),
            "all_ten_unrestricted_selector_annihilators":[str(z) for z in annihilators],
            "literal_energy_pairing":str(energy_pairing),
            "full_35_monomial_sensitivity":str(sensitivity),
            "coefficient_sup_radius":str(epsilon),
            "guaranteed_perturbed_Gram_margin":"1/400",
            "perturbed_dual_pairing_upper":str(perturbed_pairing_upper),
            "cofactor_Euler_XminusA_identities":True,
            "positive_stage_seconds":positive_seconds,
            "total_seconds":time.perf_counter()-started,
            "scope":"independent SymPy exact arithmetic, no producer/root verifier imports"}
    (folder/"SYMBOLIC_RESULT.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))


if __name__=="__main__":
    main()
