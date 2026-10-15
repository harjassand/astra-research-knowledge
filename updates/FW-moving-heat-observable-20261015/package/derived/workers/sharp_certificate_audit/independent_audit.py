#!/usr/bin/env python3
"""Independent exact audit of the sharp-boundary heat certificate.

This file constructs the energy and compatible Hessian jets itself. It never
imports a producer module, loads pickle, or accepts a saved PASS as evidence.
The JSON certificate parser is added only after a frozen certificate exists.
"""
from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction
from itertools import combinations, combinations_with_replacement
from math import comb
from pathlib import Path

import sympy as sp

BASE = Path(__file__).resolve().parent
R = sp.Rational
r, tau = sp.symbols("r tau", real=True)
x = sp.Matrix(sp.symbols("a b c d", real=True))
a, b, c, d = x
z = sp.Matrix(sp.symbols("z0:6", real=True))
u = a**2 + c**2
v = b**2 + d**2
jac = a*d - b*c
H = ((a-d)**2 + (b+c)**2)**2
alpha = 3*r/(8*(r+2))
energy = alpha*H + r*(r-1)*u**2/6 + jac**2 + r*u*jac
hessian = sp.hessian(energy, x)
# A is the row-major gradient of a two-component map. Each row of its
# Hessian is symmetric, so these are its two spatial derivative columns.
jet1 = sp.Matrix([z[0], z[1], z[3], z[4]])
jet2 = sp.Matrix([z[1], z[2], z[4], z[5]])
bilinear = sp.Matrix([xx*zz for xx in x for zz in z])
pairs = list(combinations(range(4), 2))
quadratic_pairs = list(combinations_with_replacement(range(4), 2))
lo, hi = R(-21,8), R(-5,2)


def require(ok, explanation):
    if not ok:
        raise AssertionError(explanation)


def zero(value):
    return sp.cancel(sp.expand(value)) == 0


def matrix_zero(value):
    return all(zero(q) for q in value)


def heat(diffusion):
    d1, d2 = diffusion
    return sp.expand(d1*(jet1.T*hessian*jet1)[0]
                     + d2*(jet2.T*hessian*jet2)[0])


def baseline_audit():
    """Verify definitions, quartic contact, and exact acoustic necessities."""
    require(zero(H-(u+v-2*jac)**2), "independent H definition")
    require(zero(energy.subs(dict(zip(x, 2*x)))-16*energy),
            "quartic homogeneity")
    require(zero(energy.subs({r: R(-5,2)})
                 -(R(15,8)*H+R(35,24)*u**2+jac**2-R(5,2)*u*jac)),
            "sharp endpoint specialization")
    # A target e1 rank-one variation with domain covector (n,m).
    n, m, t, p, q = sp.symbols("n m t p q", real=True)
    direction = sp.Matrix([n, m, 0, 0])
    acoustic = sp.expand((direction.T*hessian*direction)[0])
    acoustic_matrix = sp.hessian(acoustic, x)/2
    require(zero(acoustic_matrix.det()-9*n**4*m**4*r**4),
            "full acoustic determinant at sharp alpha")
    oldA = sp.Matrix([[1, -(r+1)*t], [(r+1)*t, 1]])
    newA = sp.Matrix([[-3*(r+1)*t/(2*r+1), (2*r+1)/3],
                      [1, (r+1)*t]])
    oldac = acoustic.subs({n: t, m: 1}).subs(
        dict(zip(x, list(oldA))), simultaneous=True)
    newac = acoustic.subs({n: 1, m: t}).subs(
        dict(zip(x, list(newA))), simultaneous=True)
    require(zero(oldac-R(2,3)*r*(r+1)**2*(r+2)*t**4),
            "old contact curve order four")
    require(zero(newac-6*r*(r+1)**2*(r+2)*t**4/(2*r+1)**2),
            "new contact curve order four")
    # A necessary alpha floor follows from one rank-one second variation;
    # no stored Gram or producer-contact expression is used here.
    aa = sp.symbols("alpha", real=True)
    energy_aa = aa*H+r*(r-1)*u**2/6+jac**2+r*u*jac
    floor_test = (sp.Matrix([1,0,0,0]).T
                  * sp.hessian(energy_aa,x)
                  * sp.Matrix([1,0,0,0]))[0].subs(
                      {a:0,b:(2*r+1)/3,c:1,d:0})
    require(zero(floor_test-16*(r+2)**2*(aa-alpha)/9),
            "explicit rank-one alpha-floor witness")
    # Construct the contact-generated ambient kernel independently. At t=0,
    # a PSD quartic lift must annihilate the contact vector and its first
    # derivative, since the acoustic value has fourth-order contact.
    rotation = sp.Matrix([[p,-q],[q,p]])
    kernel_vectors = []
    for A, xi in [(oldA, sp.Matrix([t,1])),
                  (newA, sp.Matrix([1,t]))]:
        target = rotation[:,0]
        rankonejet = sp.Matrix([target[0]*xi[0]**2,
                               target[0]*xi[0]*xi[1],
                               target[0]*xi[1]**2,
                               target[1]*xi[0]**2,
                               target[1]*xi[0]*xi[1],
                               target[1]*xi[1]**2])
        Ax = list(rotation*A)
        lift = sp.Matrix([xx*zz for xx in Ax for zz in rankonejet])
        for order in [0,1]:
            vv = lift.diff(t,order).subs(t,0)
            for exponent in [(2,0),(1,1),(0,2)]:
                kernel_vectors.append(sp.Matrix([
                    sp.Poly(q0,p,q).coeff_monomial(exponent) for q0 in vv]))
    K = sp.Matrix.hstack(*kernel_vectors)
    require(K.shape==(24,12), "contact-generated kernel dimensions")
    pivot_rows = K.T.rref()[1]
    require(len(pivot_rows)==12, "generic contact kernel rank")
    minor = sp.factor(K[list(pivot_rows),:].det())
    require(minor != 0, "nonzero contact-kernel minor")
    # Save the exact factored minor and establish interval nonvanishing.
    num, den = sp.fraction(minor)
    for polynomial, label in [(num,"kernel minor numerator"),
                              (den,"kernel minor denominator")]:
        require(sp.Poly(polynomial,r).count_roots(lo,hi)==0,
                label+" has no zero in the certified interval")
    require(lo+(hi-lo)*tau==(tau-21)/8,
            "independent interval reparameterization")
    multiplier = -(r+2)
    require(multiplier.subs(r,lo)==R(5,8)
            and multiplier.subs(r,hi)==R(1,2),
            "positive interval scaling endpoints")
    return {
        "baseline_status":"EXACT_PASS",
        "energy_definition":str(energy),
        "alpha_star":str(alpha),
        "interval":[str(lo),str(hi)],
        "tau_map":"r=(tau-21)/8, tau in [0,1]",
        "positive_scaling":"-(r+2)=(5-tau)/8 in [1/2,5/8]",
        "contact_kernel_rank":12,
        "contact_kernel_pivot_rows":list(pivot_rows),
        "contact_kernel_minor":str(minor),
        "acoustic_determinant":"9*m^4*n^4*r^4",
        "old_contact":"2*r*(r+1)^2*(r+2)*t^4/3",
        "new_contact":"6*r*(r+1)^2*(r+2)*t^4/(2*r+1)^2",
        "rank_one_floor_witness":str(sp.factor(floor_test)),
        "checks_are_independent_of_certificate":True,
    }, K


def polynomial(coefficients):
    require(isinstance(coefficients,list) and coefficients,
            "nonempty ascending polynomial coefficient list")
    return sum(R(q)*r**k for k,q in enumerate(coefficients))


def certificate_matrix(data, name, shape):
    rows = data[name]
    require(len(rows)==shape[0] and all(len(row)==shape[1] for row in rows),
            name+" dimensions")
    return sp.Matrix([[polynomial(entry) for entry in row] for row in rows])


def fraction_ldl(matrix):
    """Own exact rational, unpivoted LDL; no SymPy LDL call is used."""
    N = matrix.rows
    require(matrix.rows==matrix.cols and matrix==matrix.T,
            "rational LDL input symmetric and square")
    A = [[Fraction(int(q.p),int(q.q)) for q in row] for row in matrix.tolist()]
    L = [[Fraction(i==j) for j in range(N)] for i in range(N)]
    D = []
    for i in range(N):
        pivot = A[i][i]-sum(L[i][k]**2*D[k] for k in range(i))
        require(pivot>0, f"exact rational LDL pivot {i} positive")
        D.append(pivot)
        for j0 in range(i+1,N):
            L[j0][i] = (A[j0][i]-sum(L[j0][k]*L[i][k]*D[k]
                                      for k in range(i)))/pivot
    for i in range(N):
        for j0 in range(N):
            require(sum(L[i][k]*D[k]*L[j0][k] for k in range(N))==A[i][j0],
                    "independent exact LDL reconstruction")
    return [str(q) for q in D]


def certificate_audit(path, baseline, K):
    blob = path.read_bytes()
    data = json.loads(blob)
    require(data["schema"]=="astra.sharp_acoustic_heat_certificate.v1",
            "certificate schema")
    require(data["formula"]=={
        "alpha":"3*r/(8*(r+2))", "beta":"r*(r-1)/6", "gamma":"1", "delta":"r"},
        "certificate formula metadata agrees with independent energy")
    require(data["coordinates"]==["a","b","c","d"],
            "row-major gradient coordinate order")
    require(data["jet_coordinates"]==[
        "phi1_xx","phi1_xy","phi1_yy","phi2_xx","phi2_xy","phi2_yy"],
        "compatible Hessian jet order")
    require(data["matrix_vectorization"]=="row_major", "matrix vectorization")
    require(data["Z_order"]=="(a,b,c,d) kronecker (z0,z1,z2,z3,z4,z5)",
            "bilinear lift order")
    require(data["two_form_pair_order"]==[list(q) for q in pairs],
            "two-form pair ordering")
    require(data["quadratic_monomial_order"]==[list(q) for q in quadratic_pairs],
            "quadratic monomial ordering")
    require(list(map(R,data["interval"]))==[lo,hi], "specified interval")
    cn = certificate_matrix(data,"C_numerator",(24,12))
    sn = certificate_matrix(data,"S_numerator",(12,12))
    wn = certificate_matrix(data,"W_numerator",(6,10))
    cd = polynomial(data["C_denominator"])
    sd = polynomial(data["S_denominator"])
    wd = polynomial(data["W_denominator"])
    require(zero(cd-9*(r+1)*(2*r+1)), "independent C denominator factorization")
    require(zero(sd+(r+2)) and zero(wd-sd), "S and W scaling denominators")
    require(sn==sn.T, "Gram numerator symmetry")
    for factor, label in [(cd,"C denominator"),(sd,"S denominator")]:
        require(sp.Poly(factor,r).count_roots(lo,hi)==0,
                label+" has no pole in the interval")
    diffusion = [polynomial(q) for q in data["diffusion"]]
    require(len(diffusion)==2 and zero(sum(diffusion)-2), "diffusion normalization")
    require(zero(diffusion[0]-(R(27,50)-R(6,25)*r))
            and zero(diffusion[1]-(R(73,50)+R(6,25)*r)),
            "independent selected diffusion functions")
    d_bounds=[]
    for D in diffusion:
        endpoints=[D.subs(r,lo),D.subs(r,hi)]
        require(all(q>0 for q in endpoints), "positive affine diffusion interval")
        d_bounds.append([str(min(endpoints)),str(max(endpoints))])
    omega_num = sp.zeros(4)
    monomials = sp.Matrix([x[i]*x[k] for i,k in quadratic_pairs])
    for (i,k),entry in zip(pairs, wn*monomials):
        omega_num[i,k]=entry
        omega_num[k,i]=-entry
    for i,k,l in combinations(range(4),3):
        require(zero(sp.diff(omega_num[k,l],x[i])
                     -sp.diff(omega_num[i,l],x[k])
                     +sp.diff(omega_num[i,k],x[l])),
                f"independent closedness triple {i,k,l}")
    primitive_num = omega_num.T*x/4
    for i,k in pairs:
        require(zero(sp.diff(primitive_num[k],x[i])
                     -sp.diff(primitive_num[i],x[k])-omega_num[i,k]),
                f"independent polynomial primitive pair {i,k}")
    print("PASS: independent energy, pole signs, diffusion, closedness, primitive",flush=True)
    # Multiply by cd^2*sd and compare all 210 a^2 z^2 coefficients.
    # No polynomial or matrix from the producer verifier is used.
    gram_matrix_num = (cn*sn*cn.T).applyfunc(sp.expand)
    gram_coefficients = {}
    for i in range(24):
        for k in range(i,24):
            if gram_matrix_num[i,k]==0:
                continue
            exponents=[0]*10
            exponents[i//6]+=1
            exponents[k//6]+=1
            exponents[4+i%6]+=1
            exponents[4+k%6]+=1
            key=tuple(exponents)
            coefficient=gram_matrix_num[i,k]*(1 if i==k else 2)
            gram_coefficients[key]=gram_coefficients.get(key,0)+coefficient
    # Clear the energy denominator before multiplying the large numerator.
    rhs = sp.expand(cd**2*(
        sum(D*(J.T*(hessian*sd).applyfunc(sp.cancel)*J)[0]
            for D,J in zip(diffusion,[jet1,jet2]))
        +(jet1.T*omega_num*jet2)[0]))
    rhs_coefficients=dict(sp.Poly(rhs,*(list(x)+list(z))).terms())
    support=set()
    for i,k in quadratic_pairs:
        for q0,q1 in combinations_with_replacement(range(6),2):
            exponents=[0]*10
            exponents[i]+=1
            exponents[k]+=1
            exponents[4+q0]+=1
            exponents[4+q1]+=1
            support.add(tuple(exponents))
    require(len(support)==210 and set(gram_coefficients)<=support
            and set(rhs_coefficients)<=support,
            "complete x-quadratic, jet-quadratic coefficient space")
    for key in sorted(support):
        require(zero(gram_coefficients.get(key,0)-rhs_coefficients.get(key,0)),
                "universal corrected-heat polynomial coefficient "+str(key))
    print("PASS: all 210 independent cleared polynomial coefficients",flush=True)
    # Establish every rank statement on the full closed interval, not only in
    # the generic rational function field.
    require(matrix_zero(K.T*cn), "contact kernel annihilates C numerator")
    pivot_rows=cn.T.rref()[1]
    require(len(pivot_rows)==12,"generic reduced coordinate rank")
    cminor=sp.factor(cn[list(pivot_rows),:].det())
    cminor_num,cminor_den=sp.fraction(cminor)
    require(sp.Poly(cminor_num,r).count_roots(lo,hi)==0
            and sp.Poly(cminor_den,r).count_roots(lo,hi)==0,
            "C has rank twelve on the full closed interval")
    print("PASS: exact 12-dimensional kernel and full-rank complement on interval",flush=True)
    require(data["bernstein"]["degree"]==5,"specified Bernstein degree")
    require(data["bernstein"]["coordinate"]=="t=8*(r+21/8)",
            "specified Bernstein parameterization")
    st = sn.subs(r,(tau-21)/8).applyfunc(sp.expand)
    require(all(sp.Poly(q,tau).degree()<=5 for q in st if q!=0),
            "degree-five scaled Gram numerator")
    # Recover Bernstein coefficients by exact interpolation at six rational
    # nodes, independently of the producer's power-to-Bernstein formula.
    nodes=[R(i,5) for i in range(6)]
    evaluation=sp.Matrix([[comb(5,k)*q**k*(1-q)**(5-k)
                          for k in range(6)] for q in nodes])
    inverse=evaluation.inv()
    samples=[st.subs(tau,q) for q in nodes]
    bernstein=[sum((inverse[i,k]*samples[k] for k in range(6)),sp.zeros(12))
               for i in range(6)]
    stored=data["bernstein"]["matrices"]
    require(len(stored)==6,"six saved Bernstein matrices")
    for i,block in enumerate(stored):
        require(len(block)==12 and all(len(row)==12 for row in block),
                f"saved Bernstein matrix {i} dimensions")
        saved=sp.Matrix([[R(q) for q in row] for row in block])
        require(bernstein[i]==saved,
                f"independent Bernstein coefficient {i} matches saved matrix")
    reconstruction=sum((comb(5,i)*tau**i*(1-tau)**(5-i)*B
                        for i,B in enumerate(bernstein)),sp.zeros(12))
    require(matrix_zero(reconstruction-st), "universal Bernstein reconstruction")
    pivots=[fraction_ldl(B) for B in bernstein]
    require(sum(map(len,pivots))==72,"72 positive exact rational pivots")
    print("PASS: exact independent interpolation, six LDL decompositions, 72 positive pivots",flush=True)
    # Exact supplemental claims in the producer report are checked from F,
    # without using the report's formulas as algebraic premises.
    alpha0,beta0,gamma0=sp.symbols("alpha beta gamma",real=True)
    normalized = alpha0*H+beta0*u**2+gamma0*jac**2+gamma0*r*u*jac
    require(zero(normalized-gamma0*energy
                 -(alpha0-gamma0*alpha)*H
                 -(beta0-gamma0*r*(r-1)/6)*u**2),
            "coefficient-sector normalization and positive-addition identity")
    t=sp.symbols("t",real=True)
    oldA=sp.Matrix([[1,-(r+1)*t],[(r+1)*t,1]])
    direction=sp.Matrix([t,1,0,0])
    oldac=(direction.T*sp.hessian(normalized,x)*direction)[0].subs(
        dict(zip(x,list(oldA))),simultaneous=True)
    require(zero(sp.Poly(sp.expand(oldac),t).nth(2)
                 -(12*beta0-2*gamma0*r**2+2*gamma0*r)),
            "coefficient-sector acoustic necessity coefficient")
    h=(2*r+1)/3
    right_symmetry=sp.Matrix([[0,h],[1,0]])
    A=sp.Matrix([[a,b],[c,d]])
    require(matrix_zero(right_symmetry**2-h*sp.eye(2)),
            "elliptic symmetry square")
    require(zero(energy.subs(dict(zip(x,list(A*right_symmetry))),simultaneous=True)
                 -h**2*energy),"elliptic right reparameterization identity")
    FI=sp.factor(energy.subs({a:1,b:0,c:0,d:1}))
    FJ=sp.factor(energy.subs({a:1,b:0,c:0,d:-1}))
    require(zero(FI-(r+2)*(r+3)/6),"non-polyconvex conformal value")
    require(sp.diff(FI,r).subs(r,lo)<=0 and sp.diff(FI,r).subs(r,hi)<=0,
            "affine derivative sign for conformal value")
    require(FI.subs(r,lo)==-R(5,128),"uniform negative conformal value")
    derivative_num,derivative_den=sp.fraction(sp.factor(sp.diff(FJ,r)))
    require(sp.Poly(derivative_num,r).count_roots(lo,hi)==0
            and derivative_num.subs(r,lo)>0
            and derivative_den.subs(r,lo)>0
            and sp.Poly(derivative_den,r).count_roots(lo,hi)==0,
            "positive anti-conformal derivative on full closed interval")
    require(FJ.subs(r,hi)==R(839,24)<R(4507,128),
            "report's uniform anti-conformal upper bound")
    require(1600*(-R(5,128))+R(4507,128)<0,
            "four-atom lifted Jensen witness strictly negative")
    # For the stated probabilities, the law of +/-40 I and +/-J is centered
    # in both the matrix and determinant coordinates.
    require(R(1,1601)*1600-R(1600,1601)==0,
            "four-atom expected determinant is zero")
    print("PASS: sector normalization, elliptic symmetry, exact non-polyconvex witness bounds",flush=True)
    # The producer metadata is descriptive only. Its chosen y expressions,
    # face-rank statement, source claims, status, and saved PASS are never
    # premises of any audit check above.
    return {
        "status":"INDEPENDENT_EXACT_PASS",
        "certificate_path":str(path.resolve()),
        "certificate_sha256":hashlib.sha256(blob).hexdigest(),
        "audit_script_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "sympy_version":sp.__version__,
        "baseline":baseline,
        "energy_and_jet_rebuilt_independently":True,
        "universal_cleared_polynomial_identity":True,
        "coefficient_count":len(support),
        "closedness_triples":4,
        "primitive_pairs":6,
        "C_rank_on_closed_interval":12,
        "C_rank_minor_rows":list(pivot_rows),
        "C_rank_minor":str(cminor),
        "ambient_Gram_rank_on_closed_interval":12,
        "ambient_Gram_kernel":"exactly the independently reconstructed 12-column contact span",
        "diffusion_interval_bounds":d_bounds,
        "independent_bernstein_method":"exact interpolation at tau=0,1/5,2/5,3/5,4/5,1 and polynomial reconstruction",
        "bernstein_matrix_count":6,
        "independent_ldl_method":"own fractions.Fraction unpivoted elimination with exact L D L^T reconstruction",
        "positive_pivot_count":72,
        "positive_pivots":pivots,
        "coefficient_sector_reparameterization":True,
        "elliptic_right_reparameterization":True,
        "uniform_nonpolyconvex_four_atom_witness":True,
        "exact_anticonformal_maximum":"839/24",
        "no_producer_import_or_pickle_or_PASS_premise":True,
        "analytic_scope":"This establishes exact algebraic certificate validity, not by itself the heat-to-quasiconvexity analytic implication, novelty, or external review.",
    }


if __name__ == "__main__":
    baseline, kernel = baseline_audit()
    output = BASE/"BASELINE_RECEIPT.json"
    output.write_text(json.dumps(baseline,indent=2)+"\n")
    if len(sys.argv)>1:
        receipt=certificate_audit(Path(sys.argv[1]),baseline,kernel)
        (BASE/"INDEPENDENT_AUDIT_RECEIPT.json").write_text(json.dumps(receipt,indent=2)+"\n")
        print("INDEPENDENT_EXACT_PASS; receipt: "+str(BASE/"INDEPENDENT_AUDIT_RECEIPT.json"))
    else:
        print(json.dumps(baseline,indent=2))
