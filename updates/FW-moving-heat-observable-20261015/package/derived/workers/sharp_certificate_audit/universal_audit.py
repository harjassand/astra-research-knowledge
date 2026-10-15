#!/usr/bin/env python3
"""Independent rational audit for the separate universal r<-2 certificate.

The common energy/jet definitions come from this auditor's own previous
independent construction. No producer Python or pickle is imported.
"""
from __future__ import annotations

import hashlib
import json
import sys
from itertools import combinations, combinations_with_replacement
from pathlib import Path

import sympy as sp

from independent_audit import (R, r, x, a, b, c, d, z, u, jac, H, alpha,
                               energy, hessian, jet1, jet2, pairs,
                               quadratic_pairs, require, zero, matrix_zero,
                               polynomial, certificate_matrix)

BASE=Path(__file__).resolve().parent
positive_parameter=sp.symbols("s",positive=True)


def branch_sign(expression, label, require_positive=False):
    """Prove a rational sign for all r<-2 through r=-2-s, s>0.

    Same-sign polynomial coefficients, with a nonzero coefficient, imply a
    strict sign on s>0. No interval samples or floating arithmetic are used.
    """
    transformed=sp.cancel(expression.subs(r,-2-positive_parameter))
    numerator,denominator=sp.fraction(transformed)
    numerator_poly=sp.Poly(numerator,positive_parameter,domain=sp.QQ)
    denominator_poly=sp.Poly(denominator,positive_parameter,domain=sp.QQ)
    require(not numerator_poly.is_zero and not denominator_poly.is_zero,
            label+" nonzero numerator and denominator")
    def coefficient_sign(poly):
        coefficients=poly.all_coeffs()
        if all(q>=0 for q in coefficients) and any(q>0 for q in coefficients):
            return 1
        if all(q<=0 for q in coefficients) and any(q<0 for q in coefficients):
            return -1
        raise AssertionError(label+" needs a stronger symbolic sign argument: "+str(poly.as_expr()))
    nsign=coefficient_sign(numerator_poly)
    dsign=coefficient_sign(denominator_poly)
    sign=nsign*dsign
    if require_positive:
        require(sign==1,label+" strictly positive for every r<-2")
    return {
        "expression":str(sp.factor(expression)),
        "r_substitution":"r=-2-s, s>0",
        "transformed_numerator":str(sp.factor(numerator)),
        "transformed_denominator":str(sp.factor(denominator)),
        "numerator_coefficients_descending":[str(q) for q in numerator_poly.all_coeffs()],
        "denominator_coefficients_descending":[str(q) for q in denominator_poly.all_coeffs()],
        "numerator_sign":nsign,"denominator_sign":dsign,"ratio_sign":sign,
        "strict_for_all_s_positive":True,
    }


def own_symbolic_ldl(matrix, label):
    """Own exact Q(r) elimination, with every pivot sign proved globally."""
    n=matrix.rows
    require(matrix.rows==matrix.cols and matrix_zero(matrix-matrix.T),
            label+" symmetric square")
    L=sp.eye(n)
    pivots=[]
    sign_proofs=[]
    for i in range(n):
        pivot=sp.cancel(matrix[i,i]-sum(L[i,k]**2*pivots[k] for k in range(i)))
        sign_proofs.append(branch_sign(pivot,f"{label} pivot {i}",True))
        pivots.append(pivot)
        for j in range(i+1,n):
            L[j,i]=sp.cancel((matrix[j,i]-sum(L[j,k]*L[i,k]*pivots[k]
                                           for k in range(i)))/pivot)
    require(matrix_zero(L*sp.diag(*pivots)*L.T-matrix),
            label+" exact own LDL reconstruction")
    return {"pivots":[str(sp.factor(q)) for q in pivots],
            "branch_sign_proofs":sign_proofs,
            "L":[[str(sp.factor(q)) for q in row] for row in L.tolist()]},pivots


def load_rational(entry):
    require(isinstance(entry,dict) and set(entry)=={"numerator","denominator"},
            "rational entry numerator/denominator schema")
    denominator=polynomial(entry["denominator"])
    require(denominator!=0,"nonzero rational input denominator")
    return sp.cancel(polynomial(entry["numerator"])/denominator)


def load_matrix(rows,shape,label):
    require(len(rows)==shape[0] and all(len(row)==shape[1] for row in rows),
            label+" matrix dimensions")
    return sp.Matrix([[load_rational(entry) for entry in row] for row in rows])


def universal_kernel():
    t,p,q=sp.symbols("t p q",real=True)
    oldA=sp.Matrix([[1,-(r+1)*t],[(r+1)*t,1]])
    newA=sp.Matrix([[-3*(r+1)*t/(2*r+1),(2*r+1)/3],
                    [1,(r+1)*t]])
    rotation=sp.Matrix([[p,-q],[q,p]])
    vectors=[]
    for A,xi,target_acoustic in [
        (oldA,sp.Matrix([t,1]),R(2,3)*r*(r+1)**2*(r+2)*t**4),
        (newA,sp.Matrix([1,t]),6*r*(r+1)**2*(r+2)*t**4/(2*r+1)**2)]:
        acoustic_direction=sp.Matrix([xi[0],xi[1],0,0])
        acoustic=(acoustic_direction.T*hessian*acoustic_direction)[0].subs(
            dict(zip(x,list(A))),simultaneous=True)
        require(zero(acoustic-target_acoustic),"universal independently rebuilt acoustic curve")
        target=rotation[:,0]
        rankonejet=sp.Matrix([target[0]*xi[0]**2,target[0]*xi[0]*xi[1],
                             target[0]*xi[1]**2,target[1]*xi[0]**2,
                             target[1]*xi[0]*xi[1],target[1]*xi[1]**2])
        lifted=sp.Matrix([xx*zz for xx in list(rotation*A) for zz in rankonejet])
        for order in [0,1]:
            vv=lifted.diff(t,order).subs(t,0)
            for mon in [(2,0),(1,1),(0,2)]:
                vectors.append(sp.Matrix([sp.Poly(q0,p,q).coeff_monomial(mon) for q0 in vv]))
    K=sp.Matrix.hstack(*vectors)
    require(K.shape==(24,12),"universal contact kernel dimensions")
    minor=sp.factor(K[:12,:].det())
    require(zero(minor-4*(r+1)**2*(r+2)**2*(2*r+1)/27),
            "universal kernel rank minor reconstructed exactly")
    sign_proof=branch_sign(minor,"universal contact-kernel minor")
    return K,sign_proof


def universal_certificate_audit(path):
    blob=path.read_bytes()
    data=json.loads(blob)
    require(data["schema"]=="astra.universal_sharp_negative_branch_heat_certificate.v1",
            "universal certificate schema")
    require(data["domain"]=="r < -2","universal negative branch domain")
    require(data["formula"]=={
        "alpha":"3*r/(8*(r+2))","beta":"r*(r-1)/6","gamma":"1","delta":"r"},
        "universal formula matches independently built energy")
    require(data["coordinates"]==["a","b","c","d"]
            and data["matrix_vectorization"]=="row_major"
            and data["Z_order"]=="(a,b,c,d) kronecker (z0,z1,z2,z3,z4,z5)",
            "universal gradient/lift order")
    require(data["jet_coordinates"]==[
        "phi1_xx","phi1_xy","phi1_yy","phi2_xx","phi2_xy","phi2_yy"],
        "universal compatible jet order")
    require(data["two_form_pair_order"]==[list(q) for q in pairs]
            and data["quadratic_monomial_order"]==[list(q) for q in quadratic_pairs],
            "universal two-form and monomial order")
    C=load_matrix(data["C"],(24,12),"C")
    S=load_matrix(data["S"],(12,12),"S")
    W=load_matrix(data["W"],(6,10),"W")
    V=load_matrix(data["congruence_basis_V"],(12,12),"V")
    diffusion=[load_rational(entry) for entry in data["diffusion"]]
    require(len(diffusion)==2
            and zero(diffusion[0]-(2*r+1)/(r-1))
            and zero(diffusion[1]+3/(r-1))
            and zero(sum(diffusion)-2),
            "independently verified natural diffusion")
    diffusion_signs=[branch_sign(q,f"diffusion {i}",True) for i,q in enumerate(diffusion)]
    # Check the raw exported denominators as well as the canceled formulas.
    # Thus no canceled, branch-undefined encoding can pass the audit.
    denominator_encodings=set()
    def visit(value):
        if isinstance(value,dict):
            if set(value)=={"numerator","denominator"}:
                denominator_encodings.add(tuple(value["denominator"]))
            else:
                for q in value.values():visit(q)
        elif isinstance(value,list):
            for q in value:visit(q)
    visit(data)
    denominator_signs={"|".join(encoding):branch_sign(polynomial(list(encoding)),
                        "exported rational denominator")
                       for encoding in sorted(denominator_encodings)}
    require(matrix_zero(S-S.T),"universal Gram symmetry")
    require(matrix_zero(C[12:24,:]-sp.eye(12)),
            "universal complement full rank: bottom twelve rows are identity")
    omega=sp.zeros(4)
    monomials=sp.Matrix([x[i]*x[k] for i,k in quadratic_pairs])
    for (i,k),q in zip(pairs,W*monomials):
        omega[i,k]=q;omega[k,i]=-q
    for i,k,l in combinations(range(4),3):
        require(zero(sp.diff(omega[k,l],x[i])-sp.diff(omega[i,l],x[k])
                     +sp.diff(omega[i,k],x[l])),"universal closedness")
    primitive=omega.T*x/4
    for i,k in pairs:
        require(zero(sp.diff(primitive[k],x[i])-sp.diff(primitive[i],x[k])-omega[i,k]),
                "universal global polynomial primitive")
    print("PASS: universal schema, all raw branch poles, diffusion, closedness, primitive",flush=True)
    Q=(C*S*C.T).applyfunc(sp.cancel)
    gram_coefficients={}
    for i in range(24):
        for k in range(i,24):
            if Q[i,k]==0:continue
            exponents=[0]*10
            exponents[i//6]+=1;exponents[k//6]+=1
            exponents[4+i%6]+=1;exponents[4+k%6]+=1
            key=tuple(exponents)
            gram_coefficients[key]=gram_coefficients.get(key,0)+Q[i,k]*(1 if i==k else 2)
    rhs=sum(D*(J.T*hessian*J)[0] for D,J in zip(diffusion,[jet1,jet2]))
    rhs+=(jet1.T*omega*jet2)[0]
    rhs_coefficients=dict(sp.Poly(sp.expand(rhs),*(list(x)+list(z)),
                                  domain=sp.QQ.frac_field(r)).terms())
    support=set()
    for i,k in quadratic_pairs:
        for q0,q1 in combinations_with_replacement(range(6),2):
            exponents=[0]*10
            exponents[i]+=1;exponents[k]+=1
            exponents[4+q0]+=1;exponents[4+q1]+=1
            support.add(tuple(exponents))
    require(len(support)==210 and set(gram_coefficients)<=support
            and set(rhs_coefficients)<=support,"universal full coefficient space")
    for key in sorted(support):
        require(zero(gram_coefficients.get(key,0)-rhs_coefficients.get(key,0)),
                "universal independently reconstructed heat identity "+str(key))
    print("PASS: universal rational corrected-heat identity, all 210 coefficients",flush=True)
    K,kernel_sign=universal_kernel()
    require(matrix_zero(K.T*C),"universal exact contact kernel annihilation")
    determinant=sp.factor(V.det())
    require(zero(determinant+432*(r+1)/(2*r+1)**3),
            "universal congruence determinant formula")
    determinant_sign=branch_sign(determinant,"universal V determinant")
    sizes=data["block_sizes"]
    require(sizes==[4,4,2,2],"universal congruence block sizes")
    transformed=(V.T*S*V).applyfunc(sp.cancel)
    indices=[];offset=0
    for size in sizes:
        indices.append(list(range(offset,offset+size)));offset+=size
    for i,group in enumerate(indices):
        for j,other in enumerate(indices):
            if i!=j:
                require(matrix_zero(transformed.extract(group,other)),
                        f"universal congruence off-diagonal block {i},{j}")
    blocks=[]
    require(len(data["block_LDL"])==4,"universal four saved block factorizations")
    for i,group in enumerate(indices):
        block=transformed.extract(group,group)
        own,ownpivots=own_symbolic_ldl(block,f"universal congruence block {i}")
        saved=data["block_LDL"][i]
        savedL=load_matrix(saved["L"],(sizes[i],sizes[i]),f"saved block {i} L")
        savedpivots=[load_rational(q) for q in saved["pivots"]]
        require(len(savedpivots)==sizes[i],"universal saved block pivot count")
        require(matrix_zero(savedL*sp.diag(*savedpivots)*savedL.T-block),
                f"universal saved block {i} LDL reconstruction")
        require(all(zero(q-p) for q,p in zip(ownpivots,savedpivots)),
                "universal independently derived pivots agree with export")
        blocks.append(own)
    require(sum(len(block["pivots"]) for block in blocks)==12,
            "twelve exact globally positive pivots")
    alpha_free=sp.symbols("alpha",real=True)
    free_energy=energy+(alpha_free-alpha)*H
    floor_witness=sp.diff(free_energy,a,2).subs(
        {a:0,b:(2*r+1)/3,c:1,d:0})
    prefactor=16*(r+2)**2/9
    require(zero(floor_witness-prefactor*(alpha_free-alpha)),
            "universal independent below-floor acoustic witness")
    floor_sign=branch_sign(prefactor,"universal below-floor prefactor",True)
    print("PASS: exact 4+4+2+2 congruence, own LDL, all 12 branch-positive pivots",flush=True)
    return {
        "status":"INDEPENDENT_UNIVERSAL_EXACT_PASS",
        "domain":"r<-2",
        "certificate_sha256":hashlib.sha256(blob).hexdigest(),
        "audit_script_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "own_common_energy_module_sha256":hashlib.sha256((BASE/"independent_audit.py").read_bytes()).hexdigest(),
        "no_producer_import_pickle_or_saved_PASS_premise":True,
        "universal_rational_heat_identity":True,"coefficient_count":210,
        "closedness_triples":4,"global_primitive_pairs":6,
        "all_exported_raw_denominators_branch_nonzero":True,
        "exported_denominator_sign_proofs":denominator_signs,
        "positive_diffusion_branch_proofs":diffusion_signs,
        "C_rank_entire_branch":12,"contact_kernel_rank_entire_branch":12,
        "contact_kernel_rank_sign_proof":kernel_sign,
        "ambient_Gram_rank_entire_branch":12,
        "congruence_basis_determinant":str(determinant),
        "congruence_invertibility_branch_proof":determinant_sign,
        "block_sizes":sizes,"own_exact_LDL_block_count":4,
        "globally_positive_pivot_count":12,"block_proofs":blocks,
        "below_floor_acoustic_witness":str(sp.factor(floor_witness)),
        "below_floor_positive_prefactor_proof":floor_sign,
        "branch_sign_method":"r=-2-s, s>0; all numerator and denominator coefficients have a common nonzero sign",
        "no_interval_samples_or_floating_arithmetic":True,
        "negative_delta_face_algebra":negative_delta_face_audit(),
        "scope":"Exact rational certificate and negative-delta face algebra only. Heat-to-QC, polyconvex additions, approximation, and claim/novelty scope require analytic review.",
    }


def negative_delta_face_audit():
    """Independent acoustic necessities and exact decomposition for delta<0.

    Turning the decomposition into QC uses the analytic universal base
    theorem and the polyconvexity of j^2, and is separately reviewed.
    """
    al,be,ga,de=sp.symbols("alpha beta gamma delta",real=True)
    n,m,t,k=sp.symbols("n m t k",real=True)
    F=al*H+be*u**2+ga*jac**2+de*u*jac
    direction=sp.Matrix([n,m,0,0])
    acoustic=(direction.T*sp.hessian(F,x)*direction)[0]
    M=sp.hessian(acoustic,x)/2
    M0=M.subs({n:0,m:1})
    M1=M.subs({n:1,m:0})
    require(zero(M0[0,0]-4*al),"negative-delta face alpha nonnegativity")
    require(zero(M0.extract([1,2],[1,2]).det()-24*al*ga),
            "negative-delta face gamma nonnegativity after alpha positivity")
    require(zero(M1.extract([1,2],[1,2]).det()
                 -(16*al*be+8*al*de-de**2)),
            "negative-delta face principal determinant necessity")
    A=sp.Matrix([[1,-k*t],[k*t,1]])
    dir0=sp.Matrix([t,1,0,0])
    curve=(dir0.T*sp.hessian(F,x)*dir0)[0].subs(
        dict(zip(x,list(A))),simultaneous=True)
    coefficient=sp.Poly(sp.expand(curve),t).nth(2)
    target=2*(6*be-2*de*k+3*de+ga*(k-1)**2)
    require(zero(coefficient-target),"negative-delta face free-slope contact coefficient")
    require(zero(coefficient.subs(k,1+de/ga)
                 -2*(6*be*ga+de*ga-de**2)/ga),
            "negative-delta face optimized contact coefficient")
    # A positive-symbol reparameterization proves all denominator and branch
    # signs in the final decomposition, with no numerical cases omitted.
    D,B=sp.symbols("D B",positive=True)
    substitutions={de:-D,be:D/2+B}
    gamma0=de**2/(6*be+de)
    alpha0=de**2/(8*(2*be+de))
    r0=(6*be+de)/de
    require(zero(gamma0.subs(substitutions)-D**2/(2*D+6*B)),
            "negative-delta decomposition positive gamma0")
    require(zero(alpha0.subs(substitutions)-D**2/(16*B)),
            "negative-delta decomposition positive alpha0")
    require(zero(r0.subs(substitutions)-(-2-6*B/D)),
            "negative-delta decomposition r0 lies strictly below -2")
    require(zero(gamma0*alpha.subs(r,r0)-alpha0),
            "negative-delta normalization matches universal alpha floor")
    require(zero(gamma0*(r*(r-1)/6).subs(r,r0)-be),
            "negative-delta normalization matches beta")
    require(zero(gamma0*r0-de),"negative-delta normalization matches delta")
    decomposition=gamma0*energy.subs(r,r0)+(al-alpha0)*H+(ga-gamma0)*jac**2
    require(zero(F-decomposition),"negative-delta universal base decomposition")
    P=sp.Matrix([[6*be+de,de],[de,ga]])
    Q=sp.Matrix([[8*al,de],[de,2*be+de]])
    require(zero(P.det()-((6*be+de)*ga-de**2)),
            "negative-delta first PSD determinant")
    require(zero(Q.det()-(8*al*(2*be+de)-de**2)),
            "negative-delta second PSD determinant")
    return {
        "principal_minor":"16*alpha*beta+8*alpha*delta-delta^2",
        "free_slope_t2_coefficient":str(sp.factor(coefficient)),
        "optimized_t2_coefficient":"2*(6*beta*gamma+delta*gamma-delta^2)/gamma",
        "necessary_conditions_for_delta_negative":[
            "alpha>0", "2*beta+delta>0", "gamma>0",
            "alpha>=delta^2/(8*(2*beta+delta))",
            "gamma>=delta^2/(6*beta+delta)"],
        "gamma_zero_exclusion":"At gamma=0 the contact t^2 coefficient is affine in k with nonzero slope -4*delta; it is negative for sufficiently negative k when delta<0.",
        "gamma0":str(gamma0),"alpha0":str(alpha0),"r0":str(r0),
        "strict_branch_parameterization":"delta=-D, beta=D/2+B, D>0, B>0 gives r0=-2-6B/D",
        "exact_decomposition":True,
        "equivalent_two_by_two_PSD_conditions":[
            "[[6*beta+delta,delta],[delta,gamma]] >= 0",
            "[[8*alpha,delta],[delta,2*beta+delta]] >= 0"],
        "decomposition":"P=gamma0*Fsharp_r0+(alpha-alpha0)*H+(gamma-gamma0)*j^2",
        "analytic_dependency":"Universal-base QC plus convex H and polyconvex j^2; these analytic implications are separate from rational algebra.",
    }


if __name__=="__main__":
    if len(sys.argv)>1:
        receipt=universal_certificate_audit(Path(sys.argv[1]))
        output=BASE/"UNIVERSAL_INDEPENDENT_AUDIT_RECEIPT.json"
        output.write_text(json.dumps(receipt,indent=2)+"\n")
        print("INDEPENDENT_UNIVERSAL_EXACT_PASS; receipt: "+str(output))
    else:
        receipt=negative_delta_face_audit()
        (BASE/"NEGATIVE_DELTA_FACE_ALGEBRA_RECEIPT.json").write_text(json.dumps(receipt,indent=2)+"\n")
        print(json.dumps(receipt,indent=2))
