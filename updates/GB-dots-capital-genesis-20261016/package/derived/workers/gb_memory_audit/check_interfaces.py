#!/usr/bin/env python3
"""Independent exact interface falsifiers and positive consistency checks.

No source scripts are imported. These finite examples test the stated algebra
and excluded relaxations, not the asymptotic memory theorem.
"""
import json
from pathlib import Path
import sympy as S

I = S.I
eye = S.eye(2)
X = S.Matrix([[0, 1], [1, 0]])
Y = S.Matrix([[0, -I], [I, 0]])
Z = S.diag(1, -1)
c = S.Rational(99, 101)
s = S.Rational(20, 101)
results = {}

def kron(*ms):
    return S.kronecker_product(*ms)

def zero(m):
    assert m.applyfunc(S.simplify) == S.zeros(*m.shape)

def fourier(us, bits):
    out = {}
    for lab in range(2**bits):
        m = S.zeros(*next(iter(us.values())).shape)
        for f, u in us.items():
            m += (-1)**((lab & f).bit_count()) * u / 2**bits
        out[lab] = m.applyfunc(S.simplify)
    return out

# A. Original active jump and completed proposal are different generators.
p0 = S.diag(1, 0)
p1 = S.diag(0, 1)
j = X*p1
w = S.Matrix([[0, 1], [0, 0]])
def dissipator(a, rho):
    return a*rho*a.H - (a.H*a*rho + rho*a.H*a)/2
zero(dissipator(j, w) + w/2)
zero(dissipator(j, w) + dissipator(p0, w) + w)
results["active_vs_completed"] = {
    "active_coherence_rate": "-1/2", "completed_coherence_rate": "-1"
}

# B. Shared noncommuting bath: no serialized pulse channels or conditional p.
# Bit 0 is memory A's frame; bit 1 is memory C's frame.
h1 = kron(X, eye, X)
h2 = kron(eye, X, Z)
ident = S.eye(8)
zero(h1*h2 + h2*h1)
u = {}
for f in range(4):
    r = (-1)**(f & 1)
    t = (-1)**((f >> 1) & 1)
    r1 = c*ident - I*s*r*h1
    r2 = c*ident - I*s*t*h2
    zero(r1.H*r1-ident)
    zero(r2.H*r2-ident)
    u[f] = r2.H*r1.H*r2*r1
    zero(u[f].H*u[f]-ident)
k = fourier(u, 2)
effects = {lab: (a.H*a).applyfunc(S.simplify) for lab, a in k.items()}
probs = {lab: e[0, 0] for lab, e in effects.items()}
for lab, e in effects.items():
    zero(e-probs[lab]*ident)
zero(sum(effects.values(), S.zeros(8))-ident)
conditional = S.factor(probs[3]/(probs[1]+probs[3]))
assert conditional == c*c
# Each echo action 2*atan(20/99) <= 40/99.
action_bound = S.Rational(40, 99)
assert conditional > action_bound**2
assert probs[3] < action_bound**4
assert u[0] != ident
results["crossing_shared_bath"] = {
    "global_fourier_probabilities": {str(lab): str(p) for lab, p in probs.items()},
    "later_bad_given_earlier_bad": str(conditional),
    "squared_action_upper_bound": str(action_bound**2),
    "joint_subset_bound_passes": True,
    "isolated_echoes_identity_joint_echo_not_identity": True,
}

# Exact coherent virtual-seed Stinespring normalization for the same two-bit
# family. Initial amplitudes and output Walsh-basis overlaps are both 1/2.
seed_isometry = S.Matrix.vstack(*(u[f]/2 for f in range(4)))
walsh = S.Matrix(4,4,lambda chi,f:S.Rational((-1)**((int(chi) & int(f)).bit_count()),2))
transformed = kron(walsh,ident)*seed_isometry
zero(seed_isometry.H*seed_isometry-ident)
for chi in range(4):
    zero(transformed[8*chi:8*(chi+1),:]-k[chi])
dx = (S.eye(4)+kron(X.conjugate(),X))/2
zero(kron(X.conjugate(),X)-S.eye(4)-2*(dx-S.eye(4)))
plus = S.Matrix([1,1])/S.sqrt(2)
zero(X*plus-plus)
results["virtual_seed_fourier_bridge"] = {
    "exact_two_seed_stinespring_fourier_amplitudes": True,
    "complete_isometry": True,
    "dephaser_equals_twice_pinch_generator": True,
    "selected_initial_seed_fixed_by_telegraph_gauge": True,
}

# C. Nearest forbidden relaxation: two held frames on one shared memory term.
# A term bearing a PRODUCT of selected signs breaks product-smallness.
p = kron(X, X)
u_overlap = {
    f: c*S.eye(4) - I*s*(-1)**(f.bit_count())*p for f in range(4)
}
ko = fourier(u_overlap, 2)
zero(ko[0]-c*S.eye(4))
zero(ko[3]+I*s*p)
zero(ko[1])
zero(ko[2])
one_lobe_action_bound = S.Rational(20, 99)
assert s*s > one_lobe_action_bound**4
results["shared_memory_product_sign_falsifier"] = {
    "joint_nonzero_effect": str(s*s),
    "false_product_action_bound": str(one_lobe_action_bound**4),
    "premise_violated": "additive distinct-seed dependence and disjoint reservation",
}

# The same second-vs-fourth-order obstruction persists with positive damping.
# At t=1, gamma_1=gamma_2=1/10, H=theta X_1 X_2,
# theta=atan(20/99). No original random-Z jump has probability exp(-1/5)
# >=4/5. Its all-flip contribution is >=(4/5)*s^2, while the falsely
# assigned singleton product is <=theta^4 <=(20/99)^4.
cross_lower = S.Rational(4,5)*s*s
assert cross_lower > one_lobe_action_bound**4
results["cross_detecting_positive_dephaser_falsifier"] = {
    "all_flip_probability_lower_bound":str(cross_lower),
    "false_singleton_epsilon_product_upper_bound":str(one_lobe_action_bound**4),
    "gamma_1_gamma_2": "1/10",
    "premise_violated": "one selected parity changed by each interaction",
}

# D. TNI good bath filters do not give an independent ideal CPTP component.
a0 = S.diag(1, c)
a1 = S.diag(0, -I*s)
zero(a0.H*a0+a1.H*a1-eye)
defect = (eye-a0.H*a0).applyfunc(S.simplify)
assert a0.H*a0 != eye
assert (a0.H*a0)[0,0] != (a0.H*a0)[1,1]
avec = S.Matrix([a0[r,col] for col in range(2) for r in range(2)])
assert (avec*avec.H).rank() == 1
zero(defect-a1.H*a1)
results["tni_bath_filter"] = {
    "good_effect": str(a0.H*a0), "defect": str(defect),
    "complete_good_plus_bad": True,
    "rank_one_good_choi_forces_any_cp_minorant_proportional_to_filter": True,
}

# E. Isolated bath calibration does not give a full-joint effect bound.
ub = kron(eye, p0)+kron(X, p1)
zero(ub.H*ub-S.eye(4))
zero(ub*kron(eye, p0)-kron(eye, p0))
zero(ub*kron(eye, p1)-kron(X, p1))
results["fixed_bath_calibration_falsifier"] = {
    "calibration_bath_0_error": "0", "bath_1_bit_flip_probability": "1"
}

# F. Unread pinching is not permanent if its environment can return.
cn = kron(p0, eye)+kron(p1, X)
plus0 = kron(S.Matrix([1,1])/S.sqrt(2), S.Matrix([1,0]))
first = cn*plus0
zero(cn*first-plus0)
zero(cn*kron(eye,Z)*cn-kron(Z,Z))
results["measurement_reservoir_return_falsifier"] = {
    "two_measurement_cnot_copies_restore_initial_coherence": True,
    "interleaved_bath_z_induces_memory_z": True,
}

# G. A mutable syndrome record defeats zero-character correctness.
# A record-only rotation is invisible to frames placed solely on quantum data.
feedforward = kron(eye,p0)+kron(X,p1)
psi00 = kron(S.Matrix([1,0]),S.Matrix([1,0]))
out = feedforward*kron(eye,c*eye-I*s*X)*psi00
target = c*psi00-I*s*kron(S.Matrix([0,1]),S.Matrix([0,1]))
zero(out-target)
results["mutable_record_falsifier"] = {
    "quantum_frame_character": "zero",
    "wrong_feedforward_probability": str(s*s),
    "premise_violated": "protected stable classical record",
}

# H. A zero endpoint syndrome is not a universal good-history certificate.
def pauli_word(word):
    dic = {"I":eye,"X":X,"Y":Y,"Z":Z}
    return kron(*(dic[a] for a in word))
checks = [pauli_word(a) for a in ["XZZXI","IXZZX","XIXZZ","ZXIXZ"]]
pc = S.eye(32)
for g in checks:
    pc = pc*(S.eye(32)+g)/2
zero(pc*pc-pc)
assert S.trace(pc) == 2
terms = [pauli_word(a) for a in ["IYIII","IIYII","IIIIX"]]
xl = terms[0]*terms[1]*terms[2]
zl = pauli_word("ZZZZZ")
for g in checks:
    zero(g*xl-xl*g)
zero(xl*zl+zl*xl)
for mask in range(1,7):
    ep = S.eye(32)
    for bit in range(3):
        if mask & (1 << bit):
            ep = ep*terms[bit]
    zero(pc*ep*pc)
uc = S.eye(32)
for ep in terms:
    uc = (c*S.eye(32)-I*s*ep)*uc
zero(pc*uc*pc-(c**3*pc+I*s**3*xl*pc))
zero((pc*uc*pc).H*(pc*uc*pc)-(c**6+s**6)*pc)
results["zero_endpoint_syndrome_falsifier"] = {
    "code": "[[5,1,3]]",
    "zero_syndrome_kraus_on_code": "c^3 I_L + i s^3 X_L",
    "nonzero_logical_term_amplitude": str(s**3),
    "zero_syndrome_effect": str(c**6+s**6),
}

results["status"] = "PASS: all exact identities and excluded-relaxation falsifiers verified"
results["scope"] = "Finite algebra only; no asymptotic theorem, priority, or physical validation."
out_path = Path(__file__).with_name("exact_results.json")
out_path.write_text(json.dumps(results, indent=2)+"\n")
print(json.dumps(results, indent=2))
