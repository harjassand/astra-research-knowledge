#!/usr/bin/env python3
"""Exact checker for the universal flat-contact elimination of output skew.

Reads only OUTPUT_SKEW_CERTIFICATE.json; hashes the frozen input obstruction
as a dependency. No other worker, optimizer, grid, or floating point is used.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path
import sys

import sympy as s

HERE = Path(__file__).resolve().parent
certificate_bytes = (HERE/"OUTPUT_SKEW_CERTIFICATE.json").read_bytes()
certificate = json.loads(certificate_bytes)
X = s.Matrix(s.symbols("a b c d", real=True))
a,b,c,d = X
z = s.Matrix(s.symbols("z0:6", real=True))
r,tau,eta,d1,d2 = s.symbols("r tau eta d1 d2", real=True)
h = s.symbols("h", positive=True)
local = {str(q):q for q in list(X)+list(z)+[r,tau,eta,d1,d2,h]}
checks = {}


def parse(expression):
    return s.sympify(expression,locals=local)


def zero(name,expression):
    expressions = list(expression) if isinstance(expression,s.MatrixBase) else [expression]
    checks[name] = bool(all(s.cancel(value)==0 for value in expressions))
    if not checks[name]:
        raise AssertionError(name)


def exact_true(name,value):
    checks[name] = bool(value)
    if not value:
        raise AssertionError(name)


F = parse(certificate["energy"])
HF = s.hessian(F,X)
A = s.Matrix([[a,b],[c,d]])
J = s.Matrix([[0,-1],[1,0]])
S = s.diag(1,-1)
J4 = s.Matrix([-c,-d,a,b]).jacobian(X)

# General output-matrix coefficients project to the rotation commutant.
c00,c01,c10,c11 = s.symbols("c00 c01 c10 c11",real=True)
C = s.Matrix([[c00,c01],[c10,c11]])
C_average = (C+J.T*C*J)/2
scalar_part = (c00+c11)/2
skew_part = (c10-c01)/2
zero("target_rotation_projection",C_average-scalar_part*s.eye(2)-skew_part*J)
zero("projected_output_skew_real_quadratic_zero",(s.Matrix([a,c]).T*J*s.Matrix([a,c]))[0])
zero("output_reflection_reverses_J",S*J*S+J)

# Exact family symmetries and homogeneous right involution.
zero("paired_target_input_reflection_energy_symmetry",F.subs(dict(zip(X,S*A*S)),simultaneous=True)-F)
generator = s.Matrix([-c,-d,a,b])
zero("target_rotation_energy_generator",sum(generator[i]*s.diff(F,X[i]) for i in range(4)))
h_r = parse(certificate["right_involution_h"])
K = s.Matrix([[0,h_r],[1,0]])
zero("right_involution_energy_homogeneous_identity",F.subs(dict(zip(X,A*K)),simultaneous=True)-h_r**2*F)
zero("right_K_squared",K*K-h_r*s.eye(2))
zero("right_K_determinant",K.det()+h_r)
zero("paired_reflection_right_K_dihedral_relation",S*K*S+K)

# Finite dihedral average of both scalar and skew input coefficient matrices.
T = s.Matrix([[0,s.sqrt(h)],[1/s.sqrt(h),0]])
a11,a12,a22,b11,b12,b22 = s.symbols("a11 a12 a22 b11 b12 b22",real=True)
input_scalar = s.Matrix([[a11,a12],[a12,a22]])
input_skew = s.Matrix([[b11,b12],[b12,b22]])
group = [(s.eye(2),1),(-s.eye(2),1),(T,1),(-T,1),(S,-1),(-S,-1),(S*T,-1),(-S*T,-1)]
average_scalar = s.zeros(2)
average_skew = s.zeros(2)
for R,output_parity in group:
    average_scalar += R*input_scalar*R.T/8
    average_skew += output_parity*R*input_skew*R.T/8
zero("full_group_scalar_diffusion_average",average_scalar-s.diag((a11+h*a22)/2,(a22+a11/h)/2))
zero("full_group_skew_diffusion_average",average_skew-s.Matrix([[0,b12],[b12,0]]))
zero("averaged_diffusion_has_forced_ratio",average_scalar[0,0]-h*average_scalar[1,1])
normalized_d1 = (2*h/(h+1)).subs(h,h_r)
normalized_d2 = (2/(h+1)).subs(h,h_r)
zero("normalized_diffusion_first",normalized_d1-parse(certificate["normalized_input_diffusion"][0]))
zero("normalized_diffusion_second",normalized_d2-parse(certificate["normalized_input_diffusion"][1]))

B1 = s.Matrix([z[0],z[1],z[3],z[4]])
B2 = s.Matrix([z[1],z[2],z[4],z[5]])
heat = s.expand((d1*B1.T*HF*B1+d2*B2.T*HF*B2+eta*(B1.T*HF*J4*B2+B2.T*HF*J4*B1))[0])
base_A = {a:1,b:0,c:0,d:1}
base_z = dict(zip(z,[0,0,1,0,0,0]))
base = base_A|base_z
zero("base_acoustic_contact_zero_for_all_operator_parameters",heat.subs(base))
curve_A = s.Matrix([[parse(entry) for entry in row] for row in certificate["flat_curve_A"]])
curve_z = s.Matrix([parse(entry) for entry in certificate["flat_curve_z"]])
curve_sub = dict(zip(X,curve_A))|dict(zip(z,curve_z))
zero("flat_curve_heat_density_exact",heat.subs(curve_sub,simultaneous=True)-parse(certificate["flat_curve_density"]))
zero("flat_curve_has_zero_second_density_derivative",s.diff(parse(certificate["flat_curve_density"]),tau,2).subs(tau,0))
tangent = s.Matrix([parse(entry) for entry in certificate["flat_curve_tangent"]])
full_variables = list(X)+list(z)
full_hessian_times_tangent = s.hessian(heat,full_variables).subs(base)*tangent
expected_A_components = s.Matrix([parse(entry) for entry in certificate["full_hessian_times_tangent_A_components"]])
zero("full_hessian_flat_tangent_background_components",full_hessian_times_tangent[:4,:]-expected_A_components)
zero("background_component_forces_eta_zero",full_hessian_times_tangent[2]+4*eta)

# The correction contribution vanishes independently of any coefficient law.
# Its value and z1 derivative at the contact vanish identically in arbitrary
# two-form entries, so every background derivative of these is also zero.
q = s.symbols("q0:6",real=True)
Omega = s.zeros(4)
for (i,j),coefficient in zip(itertools.combinations(range(4),2),q):
    Omega[i,j]=coefficient
    Omega[j,i]=-coefficient
omega_pullback = (B1.T*Omega*B2)[0]
zero("arbitrary_alternating_correction_contact_value",omega_pullback.subs(base_z))
zero("arbitrary_alternating_correction_tangent_jet_derivative",s.diff(omega_pullback,z[1]).subs(base_z))

# Exact form relating the unsymmetrized and symmetrized mixed densities.
DF = s.Matrix([s.diff(F,qvar) for qvar in X])
one_form_coefficients = J4.T*DF
exact_two_form = one_form_coefficients.jacobian(X).T-one_form_coefficients.jacobian(X)
mixed_difference = (B1.T*HF*J4*B2-B2.T*HF*J4*B1)[0]
zero("mixed_representatives_differ_by_exact_two_form",(B1.T*exact_two_form*B2)[0]-mixed_difference)
for i,j,k in itertools.combinations(range(4),3):
    zero(f"mixed_correction_closed_{i}{j}{k}",s.diff(exact_two_form[j,k],X[i])-s.diff(exact_two_form[i,k],X[j])+s.diff(exact_two_form[i,j],X[k]))

# At r=1 the normalized input diffusion is I, giving the frozen dependency.
zero("r1_normalized_diffusion_is_identity",s.Matrix([normalized_d1,normalized_d2]).subs(r,1)-s.Matrix([1,1]))
frozen_names = ["REPORT.md","CERTIFICATE.json","verify_obstruction.py","VERIFICATION.json"]
frozen_hashes = {name:hashlib.sha256((HERE/name).read_bytes()).hexdigest() for name in frozen_names}
dependency_receipt = json.loads((HERE/"VERIFICATION.json").read_text())
exact_true("frozen_input_obstruction_dependency_passed",dependency_receipt["status"]=="PASS" and dependency_receipt["checks_count"]==36)
exact_true("frozen_input_obstruction_certificate_hash_matches",dependency_receipt["certificate_sha256"]==frozen_hashes["CERTIFICATE.json"])

receipt = {
    "schema":"astra-positive-sharp-output-skew-reduction-verification/v1",
    "status":"PASS",
    "checks_count":len(checks),
    "checks":checks,
    "certificate_sha256":hashlib.sha256(certificate_bytes).hexdigest(),
    "verifier_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "python":sys.version.split()[0],
    "sympy":s.__version__,
    "universal_positive_r_output_skew_necessary":"eta=0",
    "all_constant_real_strongly_parabolic_operator_reduction":True,
    "independent_r1_complete_constant_operator_obstruction":True,
    "all_positive_r_input_obstruction_read":False,
    "quasiconvexity_positive_branch":"UNKNOWN",
    "global_SOS_assumption":False,
    "external_review":"NOT_PERFORMED",
    "frozen_input_obstruction_file_sha256":frozen_hashes,
}
(HERE/"OUTPUT_SKEW_VERIFICATION.json").write_text(json.dumps(receipt,indent=2)+"\n")
print(json.dumps({"status":"PASS","checks_count":len(checks),"certificate_sha256":receipt["certificate_sha256"],"receipt":str(HERE/"OUTPUT_SKEW_VERIFICATION.json")}))
