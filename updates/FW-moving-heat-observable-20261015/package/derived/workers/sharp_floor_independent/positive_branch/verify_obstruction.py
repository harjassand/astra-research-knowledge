#!/usr/bin/env python3
"""Exact, exhaustive checker for the positive r=1 input-diffusion obstruction.

Only adjacent CERTIFICATE.json is an input. No discovery pickle, numerical
optimizer, sampled grid, external source, or global SOS assumption is used.
See REPORT.md for the analytic implications of the exact identities.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path
import sys

import sympy as s

HERE = Path(__file__).resolve().parent
certificate_bytes = (HERE / "CERTIFICATE.json").read_bytes()
certificate = json.loads(certificate_bytes)
X = s.Matrix(s.symbols("a b c d", real=True))
a, b, c, d = X
z = s.Matrix(s.symbols("z0:6", real=True))
t = s.symbols("t0:8", real=True)
v, tau = s.symbols("v tau", real=True)
local = {str(q): q for q in list(X) + list(z) + list(t) + [v, tau]}
pairs = list(itertools.combinations(range(4), 2))
monomials = [X[i] * X[j] for i in range(4) for j in range(i, 4)]
checks = {}


def parse(expression):
    return s.sympify(expression, locals=local)


def zero(name, expression):
    values = list(expression) if isinstance(expression, s.MatrixBase) else [expression]
    checks[name] = bool(all(s.cancel(value) == 0 for value in values))
    if not checks[name]:
        raise AssertionError(name)


def exact_true(name, value):
    checks[name] = bool(value)
    if not value:
        raise AssertionError(name)


def skew(entries):
    result = s.zeros(4)
    for (i, j), entry in zip(pairs, entries):
        result[i, j] = entry
        result[j, i] = -entry
    return result


def polynomial_coefficients(expressions, variables):
    result = []
    for expression in expressions:
        result.extend(s.Poly(s.expand(expression), variables).coeffs())
    return result


F = parse(certificate["energy"])
A = s.Matrix([[a, b], [c, d]])
S = s.diag(1, -1)
K = s.Matrix([[0, 1], [1, 0]])
P = s.zeros(4)
for i, j in enumerate([1, 0, 3, 2]):
    P[i, j] = 1
S4 = s.diag(1, -1, -1, 1)

for name, transformed in [("input_swap", A*K), ("paired_reflection", S*A*S)]:
    zero(f"energy_symmetry_{name}", F.subs(dict(zip(X, transformed)), simultaneous=True)-F)

generator = s.Matrix([-c, -d, a, b])
generator_jacobian = generator.jacobian(X)
zero("energy_left_rotation_generator", sum(generator[i]*s.diff(F,X[i]) for i in range(4)))

# Exact dihedral average of every symmetric input diffusion.
group = {tuple(s.eye(2))}
frontier = [s.eye(2)]
while frontier:
    current = frontier.pop()
    for right_generator in [S, K]:
        new = current*right_generator
        key = tuple(new)
        if key not in group:
            group.add(key)
            frontier.append(new)
exact_true("input_dihedral_group_size", len(group) == 8)
d00, d01, d11 = s.symbols("d00 d01 d11", real=True)
D = s.Matrix([[d00,d01],[d01,d11]])
averaged_D = s.zeros(2)
for entry in group:
    R = s.Matrix(2,2,entry)
    averaged_D += R*D*R.T/len(group)
zero("input_diffusion_group_average", averaged_D - (d00+d11)*s.eye(2)/2)

# Alternation fixes the orientation sign in the pullback transformation.
qconstant = s.symbols("qconstant0:6", real=True)
constant_form = skew(qconstant)
Uvec = s.Matrix(s.symbols("U0:4", real=True))
Vvec = s.Matrix(s.symbols("V0:4", real=True))
r00,r01,r10,r11 = s.symbols("r00 r01 r10 r11", real=True)
first = r00*Uvec+r10*Vvec
second = r01*Uvec+r11*Vvec
zero("alternating_input_orientation_parity", (first.T*constant_form*second)[0] - (r00*r11-r01*r10)*(Uvec.T*constant_form*Vvec)[0])

# All homogeneous quadratic two-forms: six entries times ten monomials.
unknowns = s.symbols("q0:60", real=True)
Omega = skew([sum(unknowns[10*i+j]*monomials[j] for j in range(10)) for i in range(6)])
closed_expressions = [
    s.diff(Omega[j,k],X[i])-s.diff(Omega[i,k],X[j])+s.diff(Omega[i,j],X[k])
    for i,j,k in itertools.combinations(range(4),3)
]
lie = Omega.applyfunc(lambda expression: sum(generator[i]*s.diff(expression,X[i]) for i in range(4))) + generator_jacobian.T*Omega + Omega*generator_jacobian
Omega_swap = Omega.subs(dict(zip(X,P*X)), simultaneous=True)
anti = Omega + P.T*Omega_swap*P
equations = polynomial_coefficients(closed_expressions + [lie[i,j] for i,j in pairs] + [anti[i,j] for i,j in pairs], list(X))
constraint_matrix, constraint_rhs = s.linear_eq_to_matrix(equations, unknowns)
zero("homogeneous_constraint_rhs_zero", constraint_rhs)
exact_true("complete_quadratic_constraint_rank", constraint_matrix.rank() == 52)

displayed_basis = [skew([parse(entry) for entry in row]) for row in certificate["invariant_closed_two_form_basis"]]
exact_true("displayed_basis_count", len(displayed_basis) == certificate["invariant_closed_space_dimension"] == 8)
basis_columns = []
for index, form in enumerate(displayed_basis):
    column = []
    for i,j in pairs:
        polynomial = s.Poly(form[i,j],list(X))
        column.extend(polynomial.coeff_monomial(monomial) for monomial in monomials)
    basis_columns.append(s.Matrix(column))
basis_matrix = s.Matrix.hstack(*basis_columns)
zero("displayed_basis_satisfies_all_constraints", constraint_matrix*basis_matrix)
exact_true("displayed_basis_rank_complete_kernel", basis_matrix.rank() == 8 == 60-constraint_matrix.rank())

reduced_omega = s.zeros(4)
for parameter, form in zip(t, displayed_basis):
    reduced_omega += parameter*form
B1 = s.Matrix([z[0],z[1],z[3],z[4]])
B2 = s.Matrix([z[1],z[2],z[4],z[5]])
HF = s.hessian(F,X)
corrected = s.expand((B1.T*HF*B1 + B2.T*HF*B2 + B1.T*reduced_omega*B2)[0])
M = s.hessian(corrected,z)/2
base_A = {a:1,b:0,c:0,d:1}
base_z = dict(zip(z,[0,0,1,0,0,0]))
base = base_A | base_z
base_vector = s.Matrix([0,0,1,0,0,0])
zero("acoustic_contact_value", corrected.subs(base))

curve = {a:1,b:-2*tau,c:2*tau,d:1,z[0]:tau*tau,z[1]:tau,z[2]:1,z[3]:0,z[4]:0,z[5]:0}
curve_value = corrected.subs(curve, simultaneous=True)
zero("flat_contact_curve_exact_value", curve_value - 8*tau**4*(1+tau*tau))
tangent = s.Matrix([0,-2,2,0,0,1,0,0,0,0])
full_variables = list(X)+list(z)
full_hessian = s.hessian(corrected,full_variables).subs(base)
contact_equations = list(M.subs(base_A)*base_vector) + list(full_hessian*tangent)
contact_matrix, contact_rhs = s.linear_eq_to_matrix(contact_equations,t)
exact_true("contact_equations_rank", contact_matrix.rank() == certificate["contact_constraint_rank"] == 5)
solution = s.Matrix([parse(expression) for expression in certificate["contact_constraints"]])
zero("contact_solution_satisfies_all_equations", contact_matrix*solution-contact_rhs)
solution_parameters = s.Matrix([t[0],t[5],t[7]])
exact_true("contact_solution_exhaustive_dimension", solution.jacobian(solution_parameters).rank() == 3 == 8-contact_matrix.rank())
sub = dict(zip(t,solution))
M_reduced = M.subs(sub, simultaneous=True)
corrected_reduced = corrected.subs(sub, simultaneous=True)
zero("base_full_gradient_vanishes", s.Matrix([s.diff(corrected_reduced,q).subs(base) for q in full_variables]))
zero("flat_tangent_full_hessian_kernel", full_hessian.subs(sub, simultaneous=True)*tangent)

block_I = M_reduced.subs(base_A).extract([0,4],[0,4])
expected_block = s.Matrix([[parse(entry) for entry in row] for row in certificate["I_block_04"]])
zero("I_principal_block", block_I-expected_block)
zero("I_principal_block_determinant", block_I.det()-parse(certificate["I_block_04_determinant"]))

M_diag = M_reduced.subs({a:1,b:0,c:0,d:v})
indices = certificate["principal_jet_indices_zero_based"]
minor = s.factor(M_diag.extract(indices,indices).det())
zero("diagonal_principal_minor_full_polynomial", minor-parse(certificate["principal_minor"]))
zero("diagonal_principal_minor_independent_t0", s.diff(minor,t[0]))
zero("diagonal_principal_minor_independent_t5", s.diff(minor,t[5]))
zero("diagonal_principal_minor_zero_at_minus_one", minor.subs(v,-1)-parse(certificate["principal_minor_at_v_minus_one"]))
zero("diagonal_principal_minor_derivative_at_minus_one", s.diff(minor,v).subs(v,-1)-parse(certificate["principal_minor_derivative_at_v_minus_one"]))
zero("negative_remaining_case_t_minus_one", minor.subs({v:0,t[7]:-1})-parse(certificate["t7_minus_one_principal_minor_at_v_zero"]))
zero("negative_remaining_case_t_minus_two", minor.subs({v:0,t[7]:-2})-parse(certificate["t7_minus_two_principal_minor_at_v_zero"]))
exact_true("contradictory_minor_values_are_strictly_negative", parse(certificate["t7_minus_one_principal_minor_at_v_zero"])<0 and parse(certificate["t7_minus_two_principal_minor_at_v_zero"])<0)

# Algebra needed to pass from an arbitrary C2 closed form to its quadratic jet.
constant_pullback = s.expand((B1.T*constant_form*B2)[0])
constant_polynomial_coefficients = polynomial_coefficients([constant_pullback],list(z))
constant_map,_ = s.linear_eq_to_matrix(constant_polynomial_coefficients,qconstant)
exact_true("constant_two_form_pullback_injective", constant_map.rank()==6)
rank_one_jets = []
for target in [[1,0],[0,1]]:
    for xi in [[1,0],[0,1],[1,1]]:
        rank_one_jets.append(s.Matrix([target[0]*xi[0]**2,target[0]*xi[0]*xi[1],target[0]*xi[1]**2,target[1]*xi[0]**2,target[1]*xi[0]*xi[1],target[1]*xi[1]**2]))
exact_true("rank_one_Hessian_jets_span_six_space", s.Matrix.hstack(*rank_one_jets).rank()==6)
for index,jet in enumerate(rank_one_jets):
    zero(f"constant_form_zero_on_rank_one_jet_{index+1}", constant_pullback.subs(dict(zip(z,jet))))

old_files = ["REPORT.md","ACOUSTIC_CERTIFICATE.json","verify.py","VERIFICATION.json"]
preserved_hashes = {name:hashlib.sha256((HERE.parent/name).read_bytes()).hexdigest() for name in old_files}
receipt = {
    "schema":"astra-positive-r1-input-diffusion-obstruction-verification/v1",
    "status":"PASS",
    "checks_count":len(checks),
    "checks":checks,
    "certificate_sha256":hashlib.sha256(certificate_bytes).hexdigest(),
    "verifier_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "python":sys.version.split()[0],
    "sympy":s.__version__,
    "complete_quadratic_two_form_dimension":8,
    "remaining_parameters_after_contacts":3,
    "contradiction_scope":"all constant SPD input diffusion, all C2 closed two-form corrections, universal pointwise nonnegativity",
    "global_SOS_assumption":False,
    "numerical_optimizer_or_grid":False,
    "general_constant_output_matrix_operators":"NOT_COVERED",
    "quasiconvexity_of_positive_sharp_branch":"UNKNOWN",
    "external_review":"NOT_PERFORMED",
    "preserved_original_proof_file_sha256":preserved_hashes,
}
(HERE/"VERIFICATION.json").write_text(json.dumps(receipt,indent=2)+"\n")
print(json.dumps({"status":"PASS","checks_count":len(checks),"certificate_sha256":receipt["certificate_sha256"],"receipt":str(HERE/"VERIFICATION.json")}))
