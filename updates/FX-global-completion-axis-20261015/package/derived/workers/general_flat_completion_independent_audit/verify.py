#!/usr/bin/env python3
"""Exact independent checks for the general flat-completion certificate.

The analytical proof is in REPORT.md. These are symbolic identities and
fixed-dimensional certificate fixtures, never a finite replacement for it.
"""

from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
from hashlib import sha256
from itertools import combinations, combinations_with_replacement, product
import json
from math import factorial
from pathlib import Path

import sympy as sp


OUT = Path(__file__).resolve().parent
CHECKS = []


def equal(name, left, right=0):
    residue = sp.factor(sp.expand(left-right))
    if residue != 0:
        raise AssertionError(f"{name}: {residue}")
    CHECKS.append({"name": name, "status": "PASS"})


a,b,c,d = V = sp.symbols("a b c d", real=True)
I = sp.Matrix([1,0,0,1])
at_I = dict(zip(V,I))
u=a*a+c*c; v=b*b+d*d; w=a*b+c*d; j=a*d-b*c
H=((a-d)**2+(b+c)**2)**2
basis=(u*u,u*v,v*v,u*w,v*w,w*w,u*j,v*j,w*j)
x=sp.symbols("x0:9", real=True)
G=sum(xx*bb for xx,bb in zip(x,basis))
lam,kap,M=sp.symbols("lambda kappa M", real=True)

# Frobenius-coordinate normalization of the quadratic support matrix.
Ddet = sp.hessian(j,V)/2
B = sp.hessian(G,V).subs(at_I)/2-lam*Ddet
Q = (sp.Matrix(V).T*B*sp.Matrix(V))[0]
equal("Q matrix normalization", Q, sum(sp.diff(G,z,zz).subs(at_I)*z*zz
      for z in V for zz in V)/2-lam*j)

# Generic exact Taylor identities, retaining the supplied null Lagrangian.
rho,zeta=sp.symbols("rho zeta", real=True)
E=sp.symbols("Ea Eb Ec Ed", real=True)
bg={zz: rho*ii+ee+zeta*zz for zz,ii,ee in zip(V,I,E)}
full=sp.Poly(sp.expand(G.subs(bg,simultaneous=True)),zeta)
only_E=sp.Poly(sp.expand(G.subs({zz:ee+zeta*zz for zz,ee in zip(V,E)},simultaneous=True)),zeta)
at_I_plus=sp.Poly(sp.expand(G.subs({zz:ii+zeta*zz for zz,ii in zip(V,I)},simultaneous=True)),zeta)
C=at_I_plus.coeff_monomial(zeta**3)
DC_E=sum(sp.diff(C,zz)*ee for zz,ee in zip(V,E))
equal("general mixed quadratic Taylor identity", full.coeff_monomial(zeta**2),
      rho**2*(Q+lam*j)+rho*DC_E+only_E.coeff_monomial(zeta**2))
equal("general mixed cubic Taylor identity", full.coeff_monomial(zeta**3),
      rho*C+only_E.coeff_monomial(zeta**3))
equal("general quartic Taylor identity", full.coeff_monomial(zeta**4),G)

# Every expanded homogeneous quartic has coefficient-l1 tensor norm bound.
groups=Counter(tuple(sorted(index)) for index in product(range(4),repeat=4))
assert len(groups)==35
for mon,n_entries in groups.items():
    counts=Counter(mon)
    multinomial=factorial(4)
    for multiplicity in counts.values():
        multinomial//=factorial(multiplicity)
    assert n_entries==multinomial
CHECKS.append({"name":"coefficient sum equals tensor-entry absolute sum by all 35 multiplicities",
               "status":"PASS","ordered_tensor_entries":256,"quartic_monomials":35})

# Both completion lower bounds, including the separate reserve /3 bound.
s,r,h=sp.symbols("s r h",real=True)
R=2*s*r+4*h*h+4*h*r+r*r
equal("simultaneous H Bregman lower bound",R-s*r-r*r/5,
      5*(h+2*r/5)**2+(s*r-h*h))
equal("reserve H Bregman lower bound",R-r*r/3,
      2*(s*r-h*h)+6*(h+r/3)**2)
equal("K4 from complex Beurling norm sqrt(24)",((24+1)/sp.Integer(2))**2,sp.Rational(625,4))
A0=2592*M*M/kap+8*M
B0=512*M*M/kap+3*M
alpha_star=401296*M*M/kap+sp.Rational(9391,4)*M
equal("exact completion threshold",alpha_star,A0/2+5*sp.Rational(625,4)*B0)
equal("exact reserve margin",1/(3*sp.Rational(625,4)),sp.Rational(4,1875))

# Zero-rank flatness imposes rank eight in the full invariant space.
third_indices=list(combinations_with_replacement(range(4),3))
third_equations=[sp.diff(G,*[V[ii] for ii in indices]).subs(at_I) for indices in third_indices]
third_matrix,_=sp.linear_eq_to_matrix(third_equations,x)
assert third_matrix.rank()==8
h_coordinates=sp.Matrix([1,6,1,0,0,-4,-4,-4,0])
assert third_matrix*h_coordinates==sp.zeros(20,1)
assert len(third_matrix.nullspace())==1
CHECKS.append({"name":"zero-rank flat invariant quartics equal span H","status":"PASS",
               "third_derivative_rank":8,"kernel_dimension":1,
               "H_invariant_coordinates":[str(q) for q in h_coordinates]})


def certificate(name, polynomial, supplied_lambda):
    """Independent exact certificate check, using no eigenvalue oracle."""
    matrix=sp.hessian(polynomial,V).subs(at_I)/2-supplied_lambda*Ddet
    minors=[]
    for size in range(1,5):
        for indices in combinations(range(4),size):
            minor=sp.factor(matrix.extract(indices,indices).det())
            minors.append(minor)
    assert all(q.is_Rational for q in minors)
    if any(q<0 for q in minors):
        return {"name":name,"admission":"UNRESOLVED_BY_THIS_CERTIFICATE","reason":"Q_NOT_PSD"}
    rank=matrix.rank()
    kernel=matrix.nullspace()
    violations=[]
    for ii,zi in enumerate(kernel):
        for jj in range(ii,len(kernel)):
            zj=kernel[jj]
            for ee in range(4):
                contraction=sum(sp.diff(polynomial,V[p],V[q],V[ee]).subs(at_I)*zi[p]*zj[q]
                                for p in range(4) for q in range(4))
                if contraction!=0:
                    violations.append((ii,jj,ee,str(sp.factor(contraction))))
    if violations:
        return {"name":name,"admission":"UNRESOLVED_BY_THIS_CERTIFICATE","reason":"FLATNESS_FAILS",
                "rank":rank,"flatness_violations":violations}
    coeff_norm=sum(abs(q) for q in sp.Poly(sp.expand(polynomial),V).coeffs())
    result={"name":name,"admission":"PASS","rank":rank,"M":str(coeff_norm),
            "matrix":[[str(q) for q in row] for row in matrix.tolist()]}
    if rank==0:
        # Recover c from a^4 coefficient, which equals c for H.
        cc=sp.Poly(polynomial,V).coeff_monomial(a**4)
        equal(f"zero-rank fixture {name} is cH",polynomial,cc*H)
        result.update({"H_coefficient":str(cc),"alpha_star":str(max(sp.Integer(0),-cc))})
        return result
    z=sp.symbols("z")
    detpoly=sp.Poly((sp.eye(4)+z*matrix).det(),z)
    er=detpoly.coeff_monomial(z**rank)
    erminus=detpoly.coeff_monomial(z**(rank-1))
    harmonic_lower=sp.factor(er/erminus)
    assert harmonic_lower>0
    # Independently check Q-kappa P_(Kperp) PSD, using rational projector.
    if kernel:
        N=sp.Matrix.hstack(*kernel)
        projector=sp.eye(4)-N*(N.T*N).inv()*N.T
    else:
        projector=sp.eye(4)
    assert projector.T==projector and projector*projector==projector
    lower_matrix=matrix-harmonic_lower*projector
    for size in range(1,5):
        for indices in combinations(range(4),size):
            assert sp.factor(lower_matrix.extract(indices,indices).det())>=0
    threshold=sp.factor(401296*coeff_norm**2/harmonic_lower+sp.Rational(9391,4)*coeff_norm)
    result.update({"kappa":str(harmonic_lower),"alpha_star":str(threshold),
                   "orthogonal_projection_checked":True})
    return result


fixtures=[
    certificate("rank four: Frobenius norm fourth power",(u+v)**2,sp.Integer(0)),
    certificate("rank three: strict contact slice",w*w+v*v,sp.Integer(0)),
    certificate("rank two: convex column fourth power",v*v,sp.Integer(0)),
    certificate("rank one: determinant square fails extra flatness",j*j,sp.Integer(2)),
    certificate("rank zero: negative H",-3*H,sp.Integer(0)),
    certificate("rank zero: zero polynomial",sp.Integer(0),sp.Integer(0)),
    certificate("bad supplied lambda is unresolved",v*v,sp.Integer(1)),
]
assert [q["admission"] for q in fixtures]==["PASS","PASS","PASS","UNRESOLVED_BY_THIS_CERTIFICATE",
                                          "PASS","PASS","UNRESOLVED_BY_THIS_CERTIFICATE"]
CHECKS.append({"name":"exact rational certificate fixtures","status":"PASS","count":len(fixtures)})

# Harmonic eigenvalue formula is an identity for every possible positive rank.
ll=sp.symbols("l1:5",positive=True)
for rank in range(1,5):
    vals=ll[:rank]
    er=sp.prod(vals)
    erminus=sum(sp.prod(subset) for subset in combinations(vals,rank-1))
    equal(f"harmonic eigenvalue lower bound identity rank {rank}",er/erminus,
          1/sum(1/q for q in vals))

result={"status":"ALL_EXACT_CHECKS_PASS","exact_checks":CHECKS,"fixtures":fixtures,
        "scope":"Symbolic identities and certificate fixtures; REPORT.md supplies the universal proof audit.",
        "construction_generalization_read":True,
        "construction_original_report_read_ranges":"Sections 8-9, only for the tensor estimate and explicit analytic constant",
        "primary_source":"https://www.math.purdue.edu/~banuelos/Papers/Beur_Ahl.pdf",
        "primary_source_scope":"Theorem 1.1, formula (1.4), complex-valued bound at p=4",
        "sympy_version":sp.__version__}
(OUT/"verification.json").write_text(json.dumps(result,indent=2)+"\n")
receipt={"recorded_utc":datetime.now(timezone.utc).isoformat(),"status":result["status"],
         "files":{name:sha256((OUT/name).read_bytes()).hexdigest()
                  for name in ("verify.py","verification.json","REPORT.md") if (OUT/name).exists()},
         "read_order":"Independent statement derivation first; GENERAL_FLAT_COMPLETION.md and scoped original report ranges afterward",
         "original_nonshear_audit_modified":False,"source_or_checkout_modified":False,
         "compiler_implementation_review":"Pending construction file availability; see REPORT.md for final status"}
(OUT/"receipt.json").write_text(json.dumps(receipt,indent=2)+"\n")
print(json.dumps({"status":result["status"],"exact_checks":len(CHECKS),"fixtures":len(fixtures)},indent=2))
