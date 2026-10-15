#!/usr/bin/env python3
"""Independent non-SOS positive-branch input-heat obstruction audit.

Reconstructs the integrand, all 60 quadratic two-form coefficients, compatible
jets, and every necessary equality. No producer generator or pickle is used.
"""
from __future__ import annotations

import hashlib
import json
import sys
from itertools import combinations
from pathlib import Path

import sympy as sp
from sympy.polys.matrices import DomainMatrix

from independent_audit import (R,r,x,a,b,c,d,z,u,jac,H,alpha,energy,hessian,
                               jet1,jet2,pairs,quadratic_pairs,
                               require,zero,matrix_zero,polynomial)

BASE=Path(__file__).resolve().parent
variables=list(x)+list(z)


def candidate():
    parameters=list(sp.symbols("w0:60"))+list(sp.symbols("d1 d2"))
    coefficients=sp.Matrix(6,10,parameters[:60])
    monomials=sp.Matrix([x[i]*x[k] for i,k in quadratic_pairs])
    omega=sp.zeros(4)
    for (i,k),entry in zip(pairs,coefficients*monomials):
        omega[i,k]=entry;omega[k,i]=-entry
    d1,d2=parameters[-2:]
    P=sp.expand(d1*(jet1.T*hessian*jet1)[0]
                +d2*(jet2.T*hessian*jet2)[0]
                +(jet1.T*omega*jet2)[0])
    return parameters,omega,P


def linear_matrix(equations,parameters,label):
    matrix,constant=sp.linear_eq_to_matrix(equations,parameters)
    require(matrix_zero(constant),label+" has no affine constant")
    return matrix


def branch_nonzero(polynomial_expression,label,positive=False):
    numerator,denominator=sp.fraction(sp.cancel(polynomial_expression))
    def sign(poly):
        coefficients=sp.Poly(poly,r,domain=sp.QQ).all_coeffs()
        if all(q>=0 for q in coefficients) and any(q>0 for q in coefficients):return 1
        if all(q<=0 for q in coefficients) and any(q<0 for q in coefficients):return -1
        raise AssertionError(label+" lacks a whole-positive-branch coefficient proof: "+str(poly))
    nsign,dsign=sign(numerator),sign(denominator)
    if positive:require(nsign==dsign,label+" strictly positive for every r>0")
    return {"expression":str(sp.factor(polynomial_expression)),
            "numerator_coefficients_descending":[str(q) for q in sp.Poly(numerator,r).all_coeffs()],
            "denominator_coefficients_descending":[str(q) for q in sp.Poly(denominator,r).all_coeffs()],
            "numerator_sign":nsign,"denominator_sign":dsign,
            "strict_ratio_sign":nsign*dsign,
            "domain":"every real r>0"}


def pure_jet_and_averaging_audit(parameters,omega,P):
    """Check algebra supporting the non-SOS analytic necessities."""
    t,p,q=sp.symbols("t p q",real=True)
    J=sp.Matrix([[0,-1],[1,0]])
    oldA=sp.eye(2)+(r+1)*t*J
    zold=sp.Matrix([t*t,t,1,0,0,0])
    old_value=P.subs(dict(zip(variables,list(oldA)+list(zold))),simultaneous=True)
    d1,d2=parameters[-2:]
    expected=(d1*t*t+d2)*R(2,3)*r*(r+1)**2*(r+2)*t**4
    require(zero(old_value-expected),"independent old-flat-curve corrected density")
    newA=sp.Matrix([[-3*(r+1)*t/(2*r+1),(2*r+1)/3],
                    [1,(r+1)*t]])
    znew=sp.Matrix([1,t,t*t,0,0,0])
    new_value=P.subs(dict(zip(variables,list(newA)+list(znew))),simultaneous=True)
    new_expected=(d1+d2*t*t)*6*r*(r+1)**2*(r+2)*t**4/(2*r+1)**2
    require(zero(new_value-new_expected),"independent new-flat-curve corrected density")
    rotation=sp.Matrix([[p,-q],[q,p]])
    generalA=sp.Matrix([[a,b],[c,d]])
    require(zero(energy.subs(dict(zip(x,list(rotation*generalA))),simultaneous=True)
                 -(p*p+q*q)**2*energy),
            "all-target-rotation plus homogeneity energy covariance")
    rotatedA=rotation
    rotatedz=sp.Matrix([0,0,p,0,0,q])
    require(zero(P.subs(dict(zip(variables,list(rotatedA)+list(rotatedz))),simultaneous=True)),
            "independent exact target-rotated contact")
    base=list(sp.eye(2))+[0,0,1,0,0,0]
    require(zero(P.subs(dict(zip(variables,base)))),"old joint contact is an exact zero")
    vold=sp.Matrix(list((r+1)*J)+[0,1,0,0,0,0])
    vrot=sp.Matrix(list(J)+[0,0,0,0,0,1])
    zbar=sp.Matrix([0,1,0,0,0,-(r+1)])
    vbar=sp.Matrix([0,0,0,0]+list(zbar))
    require(matrix_zero(vold-(r+1)*vrot-vbar),
            "pure-jet vector is exact difference of two flat tangents")
    Hzz=sp.hessian(P,z).subs(dict(zip(x,list(sp.eye(2)))))
    Pbar=P.subs(dict(zip(variables,list(sp.eye(2))+list(zbar))),simultaneous=True)
    require(zero((zbar.T*Hzz*zbar)[0]/2-Pbar),
            "pure-jet quadratic value uses same zz Hessian at every base jet")
    # Explicitly verify all underlying energy and compatible-jet covariance.
    target_integer=sp.Matrix([[1,0,-1,0],[0,1,0,-1],[1,0,1,0],[0,1,0,1]])
    target_jet=sp.Matrix.vstack(sp.Matrix.hstack(sp.eye(3),-sp.eye(3)),
                               sp.Matrix.hstack(sp.eye(3),sp.eye(3)))
    require(zero(energy.subs(dict(zip(x,target_integer*x)),simultaneous=True)/4-energy),
            "pi/4 target-energy covariance")
    reflection=sp.diag(1,-1,-1,1)
    reflection_jet=sp.diag(1,-1,1,-1,1,-1)
    require(zero(energy.subs(dict(zip(x,reflection*x)),simultaneous=True)-energy),
            "paired reflection energy invariance")
    require(matrix_zero(jet1.subs(dict(zip(z,reflection_jet*z)),simultaneous=True)-reflection*jet1)
            and matrix_zero(jet2.subs(dict(zip(z,reflection_jet*z)),simultaneous=True)+reflection*jet2),
            "paired reflection compatible-jet covariance")
    h=(2*r+1)/3
    K=sp.Matrix([[0,h],[1,0]])
    A=sp.Matrix([[a,b],[c,d]])
    AK=sp.Matrix(list(A*K))
    kz=sp.Matrix([z[2],h*z[1],h*h*z[0],z[5],h*z[4],h*h*z[3]])
    TA=sp.Matrix([[0,1,0,0],[h,0,0,0],[0,0,0,1],[0,0,h,0]])
    require(zero(energy.subs(dict(zip(x,AK)),simultaneous=True)-h*h*energy),
            "positive-branch input-involution energy covariance")
    require(matrix_zero(K*K-h*sp.eye(2)),"positive-branch K square")
    require(matrix_zero(jet1.subs(dict(zip(z,kz)),simultaneous=True)-TA*jet2)
            and matrix_zero(jet2.subs(dict(zip(z,kz)),simultaneous=True)-h*TA*jet1),
            "positive-branch input-involution jet covariance")
    # Hessian covariance follows independently by differentiating F(TA)=h²F.
    H_at_AK=hessian.subs(dict(zip(x,AK)),simultaneous=True)
    require(matrix_zero(TA.T*H_at_AK*TA-h*h*hessian),
            "input-involution Hessian covariance")
    d12=sp.symbols("d12",real=True)
    heat=d1*(jet1.T*hessian*jet1)[0]+2*d12*(jet1.T*hessian*jet2)[0]+d2*(jet2.T*hessian*jet2)[0]
    transformed_heat=heat.subs(dict(zip(variables,list(AK)+list(kz))),simultaneous=True)/h**3
    expected_heat=h*d2*(jet1.T*hessian*jet1)[0]+2*d12*(jet1.T*hessian*jet2)[0]+d1/h*(jet2.T*hessian*jet2)[0]
    require(zero(transformed_heat-expected_heat),"all-input-diffusion congruence transform")
    # No square roots are needed: determinant and positive diagonals establish
    # the SPD preservation of D -> [[h*d2,d12],[d12,d1/h]].
    D=sp.Matrix([[d1,d12],[d12,d2]])
    transformed_D=sp.Matrix([[h*d2,d12],[d12,d1/h]])
    require(zero(D.det()-transformed_D.det()),"input SPD transformation determinant")
    reflected_heat=heat.subs(dict(zip(variables,list(reflection*x)+list(reflection_jet*z))),
                             simultaneous=True)
    require(zero(reflected_heat-heat.subs(d12,-d12)),
            "paired reflection kills only diffusion cross coefficient")
    input_jet_matrix=kz.jacobian(z)
    require(matrix_zero(TA*target_integer-target_integer*TA)
            and matrix_zero(input_jet_matrix*target_jet-target_jet*input_jet_matrix),
            "left target and input involution actions commute")
    require(matrix_zero(TA*reflection+reflection*TA)
            and matrix_zero(input_jet_matrix*reflection_jet-reflection_jet*input_jet_matrix),
            "input involution and paired reflection commute on biquadratic densities")
    require(matrix_zero(reflection*target_integer*reflection-target_integer.T)
            and matrix_zero(reflection_jet*target_jet*reflection_jet-target_jet.T),
            "paired reflection conjugates target rotation to its inverse")
    h_sign=branch_nonzero(h,"positive input involution h",True)
    require(zero(P.subs(dict(zip(variables,list(h*x)+list(h*h*z))),simultaneous=True)
                 -h**6*P),"scaled input operation is an involution on biquadratic densities")
    return {
        "old_curve_corrected_value":str(sp.factor(expected)),
        "new_curve_corrected_value":str(sp.factor(new_expected)),
        "all_target_rotations_energy_covariant":True,
        "target_rotated_contact_exact":True,
        "v_old":"((r+1)J, phi1_xy)","v_rotation":"(J, phi2_yy)",
        "pure_jet_difference":"v_old-(r+1)*v_rotation=(0,phi1_xy-(r+1)phi2_yy)",
        "P_I_zbar_equals_half_zz_Hessian_quadratic":True,
        "necessity_argument":"At the exact contact a nonnegative smooth P has zero gradient and PSD joint Hessian. Both flat tangents have zero Hessian value, hence are in its kernel. Their difference is pure jet zbar, forcing P(I,zbar)=0; nonnegativity then forces its A gradient to vanish. No SOS assumption.",
        "target_pi_over_4_covariance":True,"paired_reflection_covariance":True,
        "input_involution_covariance":True,"h_positive_branch_proof":h_sign,
        "finite_symmetry_group_compatibility_verified":True,
        "all_SPD_input_diffusion_transform":"D -> [[h*d2,d12],[d12,d1/h]], preserving determinant and positive diagonals",
        "averaging_argument":"Average the positive involution, paired reflection, and target rotations. Closure is preserved under scaled pullback. This yields d12=0, d1=h*d2, d2>0, and all three polynomial symmetries. The finite actions commute up to signs harmless for a biquadratic density; reflection conjugates target rotations to their inverses.",
        "output_coupled_heat_excluded":False,
    }


def regenerate(parameters,omega,P):
    """Own construction of the published ordered necessary-equality rows."""
    t,p,q=sp.symbols("t p q",real=True)
    grad=sp.Matrix([sp.diff(P,y) for y in variables])
    contact=[]
    rotation=sp.Matrix([[p,-q],[q,p]])
    curve_definitions=[(sp.Matrix([[1,-(r+1)*t],[(r+1)*t,1]]),(t,1)),
                       (sp.Matrix([[-3*(r+1)*t/(2*r+1),(2*r+1)/3],
                                   [1,(r+1)*t]]),(1,t))]
    for A,xi in curve_definitions:
        target=rotation[:,0]
        n,m=xi
        jet=sp.Matrix([target[0]*n*n,target[0]*n*m,target[0]*m*m,
                       target[1]*n*n,target[1]*n*m,target[1]*m*m])
        substitution=dict(zip(variables,list(rotation*A)+list(jet)))
        for component in grad:
            restricted=sp.expand(component.subs(substitution,simultaneous=True))
            for order in [0,1]:
                at_contact=sp.expand(sp.diff(restricted,t,order).subs(t,0))
                contact.extend(sp.Poly(at_contact,p,q).coeffs())
    for i,k,l in combinations(range(4),3):
        exterior=sp.expand(sp.diff(omega[k,l],x[i])-sp.diff(omega[i,l],x[k])
                           +sp.diff(omega[i,k],x[l]))
        contact.extend(sp.Poly(exterior,*x).coeffs())
    contact=[sp.cancel(q0) for q0 in contact if q0!=0]
    Econtact=linear_matrix(contact,parameters,"contact/closedness")
    zbar=[0,1,0,0,0,-(r+1)]
    point=dict(zip(variables,list(sp.eye(2))+zbar))
    newzero=[sp.cancel(sp.diff(P,y).subs(point)) for y in x]
    d1,d2=parameters[-2:]
    natural=[3*d1-(2*r+1)*d2]
    T=sp.Matrix([[1,0,-1,0],[0,1,0,-1],[1,0,1,0],[0,1,0,1]])
    Tz=sp.Matrix.vstack(sp.Matrix.hstack(sp.eye(3),-sp.eye(3)),
                         sp.Matrix.hstack(sp.eye(3),sp.eye(3)))
    reflection=sp.diag(1,-1,-1,1)
    reflectionz=sp.diag(1,-1,1,-1,1,-1)
    h=(2*r+1)/3
    AK=sp.Matrix([b,h*a,d,h*c])
    Kz=sp.Matrix([z[2],h*z[1],h*h*z[0],z[5],h*z[4],h*h*z[3]])
    sections=[{"kind":"new_zero_A_gradient","rows":len(newzero)},
              {"kind":"natural_diffusion","rows":len(natural)}]
    rows=[linear_matrix(newzero,parameters,"new zero"),
          linear_matrix(natural,parameters,"natural diffusion")]
    for label,tx,tz,scale in [("target_pi_over_4",T*x,Tz*z,R(1,4)),
                              ("paired_reflection",reflection*x,reflectionz*z,1),
                              ("input_involution",AK,Kz,1/h**3)]:
        restricted=P.subs(dict(zip(variables,list(tx)+list(tz))),simultaneous=True)*scale-P
        equations=[sp.cancel(q0) for q0 in sp.Poly(restricted,*variables,domain="EX").coeffs()]
        section_matrix=linear_matrix(equations,parameters,label)
        rows.append(section_matrix)
        sections.append({"kind":label,"rows":section_matrix.rows})
    rows.append(Econtact)
    sections.append({"kind":"contact_and_closedness","rows":Econtact.rows})
    E=sp.Matrix.vstack(*rows)
    badjet=dict(zip(variables,[0,0,1,0,0,1,0,0,0,0]))
    L=linear_matrix([sp.cancel(P.subs(badjet))],parameters,"actual bad jet")
    return E,L,sections


def verify(path):
    blob=path.read_bytes();data=json.loads(blob)
    require(data["schema"]=="astra.positive_sharp_input_heat_obstruction.v1"
            and data["domain"]=="r>0","positive obstruction schema/domain")
    require(data["two_form_pair_order"]==[list(q) for q in pairs]
            and data["quadratic_monomial_order"]==[list(q) for q in quadratic_pairs],
            "positive obstruction all sixty form coefficients ordering")
    require(data["variable_order"]=="60 two-form coefficients row-major, then d1,d2",
            "positive obstruction variable order")
    parameters,omega,P=candidate()
    analytic_algebra=pure_jet_and_averaging_audit(parameters,omega,P)
    print("PASS: independent flat contact, forced pure jet, and all-SPD-input symmetry algebra",flush=True)
    E,L,sections=regenerate(parameters,omega,P)
    require(E.shape==(411,62) and data["system_shape"]==[411,62],
            "independently regenerated 411 by 62 system")
    require(sections==data["row_sections"],"independent equality row sections/order")
    print("PASS: independently regenerated all 411 necessary equality rows",flush=True)
    lam=sp.zeros(411,1);raw_denominator_proofs={}
    require(len(data["dual_terms"])==48,"48 sparse equality dual terms")
    seen=set()
    for term in data["dual_terms"]:
        index=term["row"]
        require(isinstance(index,int) and 0<=index<411 and index not in seen,
                "unique valid sparse dual row")
        seen.add(index)
        numerator=polynomial(term["multiplier"]["numerator"])
        denominator=polynomial(term["multiplier"]["denominator"])
        raw_denominator_proofs[str(sp.factor(denominator))]=branch_nonzero(
            denominator,"raw equality dual denominator")
        lam[index]=sp.cancel(numerator/denominator)
        require(lam[index]!=0,"every listed dual term is nonzero")
    cscalar=r*(r+1)*(2*r+1)/(r+2)
    target=L.T+sp.eye(62)[:,61]*cscalar
    residual=(E.T*lam-target).applyfunc(sp.cancel)
    require(residual==sp.zeros(62,1),"independent exact equality dual, every one of 62 columns")
    c_sign=branch_nonzero(cscalar,"forced negative jet coefficient",True)
    # Every coefficient of regenerated E must also be defined on r>0.
    system_denominators={str(sp.factor(sp.denom(sp.cancel(q)))):sp.denom(sp.cancel(q)) for q in E}
    system_denominator_proofs={key:branch_nonzero(q,"regenerated equality coefficient denominator")
                               for key,q in system_denominators.items()}
    print("PASS: all 62 dual columns, all positive-branch poles, strict actual-jet contradiction",flush=True)
    # The physical jet can be independently realized by a polynomial map.
    X,Y=sp.symbols("X Y",real=True)
    map_components=[X*Y,X]
    gradient=sp.Matrix([sp.diff(f,v0) for f in map_components for v0 in [X,Y]])
    second=sp.Matrix([sp.diff(f,X,2) for f in map_components])
    jet=sp.Matrix([sp.diff(f,v0,v1) for f in map_components
                   for v0,v1 in [(X,X),(X,Y),(Y,Y)]])
    origin={X:0,Y:0}
    require(gradient.subs(origin)==sp.Matrix([0,0,1,0])
            and jet.subs(origin)==sp.Matrix([0,1,0,0,0,0]),
            "bad actual jet is compatible via (XY,X)")
    return {
        "status":"INDEPENDENT_POSITIVE_INPUT_OBSTRUCTION_EXACT_PASS",
        "domain":"every real r>0, including r=1",
        "certificate_sha256":hashlib.sha256(blob).hexdigest(),
        "audit_script_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "own_common_energy_module_sha256":hashlib.sha256((BASE/"independent_audit.py").read_bytes()).hexdigest(),
        "no_producer_import_pickle_or_saved_PASS_premise":True,
        "all_sixty_quadratic_form_coefficients_admitted":True,
        "necessary_system_shape":[411,62],"row_sections":sections,
        "exact_sparse_dual_nonzero_terms":48,"all_62_dual_columns_exact":True,
        "raw_dual_denominator_proofs":raw_denominator_proofs,
        "regenerated_system_denominator_proofs":system_denominator_proofs,
        "forced_negative_coefficient_proof":c_sign,
        "forced_negative_actual_jet":"P(e21,(0,1,0,0,0,0))=-r*(r+1)*(2*r+1)*d2/(r+2)<0",
        "compatible_polynomial_map":"phi(X,Y)=(X*Y,X)",
        "pure_jet_and_symmetry_necessity":analytic_algebra,
        "SOS_assumption":False,"all_constant_SPD_INPUT_diffusions_excluded":True,
        "output_coupled_heat_excluded":False,"quasiconvexity_refuted":False,
        "scope":"No homogeneous-quadratic closed local two-form can make the corrected heat density pointwise nonnegative for any constant positive input diffusion. This is a method obstruction, not an integrated dissipation or QC counterexample. Smooth-C2 extension is a separate analytic Taylor argument.",
    }


if __name__=="__main__":
    path=Path(sys.argv[1]) if len(sys.argv)>1 else BASE/"positive_frozen/POSITIVE_INPUT_HEAT_OBSTRUCTION.json"
    receipt=verify(path)
    output=BASE/"POSITIVE_INDEPENDENT_AUDIT_RECEIPT.json"
    output.write_text(json.dumps(receipt,indent=2)+"\n")
    print("INDEPENDENT_POSITIVE_INPUT_OBSTRUCTION_EXACT_PASS; receipt: "+str(output))
