#!/usr/bin/env python3
"""Decimal replay of the complete-source coherent-decoder fixture."""

from decimal import Decimal, getcontext

getcontext().prec = 60
D = Decimal
t = D(1) / D(2).sqrt()
q = (D(1) + t) / 2
r = (D(1) - t) / 2

# Bloch vectors: pass/fail states for x=0,1, and d,n measurement axes.
states = {
    (0, "P"): (D(0), D(0), D(1)),
    (0, "F"): (D(0), D(0), D(-1)),
    (1, "P"): (D(1), D(0), D(0)),
    (1, "F"): (D(-1), D(0), D(0)),
}
d = (-t, D(0), t)
n = (D("-0.5"), t, D("0.5"))


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def close(a, b, tol=D("1e-50")):
    return abs(a - b) < tol


assert close(dot(d, d), 1)
assert close(dot(n, n), 1)
assert close(dot(d, n), t)
# d x n = (-1/2,0,-1/2), so the PVMs are noncommuting.
cross = (d[1] * n[2] - d[2] * n[1],
         d[2] * n[0] - d[0] * n[2],
         d[0] * n[1] - d[1] * n[0])
assert cross == (D("-0.5"), D(0), D("-0.5"))
# N0's off-diagonal entry is -1/4 - i t/2, explicitly non-real.
assert t / 2 > 0

# Preselection decoder errors and full-vector defect for each actual Alice
# branch. L_x is the Helstrom projector whose Bloch sign is (-1)^x d.
errors = {}
defects = {}
for (x, f), bloch in states.items():
    correct = (1 + (D(1) if x == 0 else D(-1)) * dot(d, bloch)) / 2
    errors[x, f] = 1 - correct
    defects[x, f] = 2 * errors[x, f]
assert close(errors[0, "P"], r)
assert close(errors[1, "P"], r)
assert close(errors[0, "F"], q)
assert close(errors[1, "F"], q)
e = sum(errors.values()) / 4
mean_defect2 = sum(defects.values()) / 4
assert close(e, D("0.5"))
assert close(mean_defect2, 2 * e)

# Per-branch joint fine law after the coherent decoder and original N PVM.
# P(g,gamma|rho)=Tr(rho L_g) Tr(L_g N_gamma).
def actual_joint(x, f, g, gamma):
    bloch = states[x, f]
    pg = (1 + (D(1) if g == 0 else D(-1)) * dot(d, bloch)) / 2
    overlap = (1 + (D(1) if g == gamma else D(-1)) * t) / 2
    return pg * overlap


for x in (0, 1):
    for f in ("P", "F"):
        accepted = sum(actual_joint(x, f, g, g) for g in (0, 1))
        assert close(accepted, q)
        total = sum(actual_joint(x, f, g, gamma)
                    for g in (0, 1) for gamma in (0, 1))
        assert close(total, 1)

# Ideal event: the true label is copied, then original gamma is measured.
def ideal_gamma(x, f, gamma):
    bloch = states[x, f]
    return (1 + (D(1) if gamma == 0 else D(-1)) * dot(n, bloch)) / 2


p = sum(ideal_gamma(x, f, x) for x in (0, 1) for f in ("P", "F")) / 4
p_actual = sum(sum(actual_joint(x, f, g, g) for g in (0, 1))
                for x in (0, 1) for f in ("P", "F")) / 4
assert close(p, D("0.5"))
assert close(p_actual, q)

# A concrete changed full fine law: x=0 pass, ideal g=0 and gamma=(3/4,1/4),
# while the actual coherent-decoder-plus-N sequence has support on g=1 too.
table = {(g, gamma): actual_joint(0, "P", g, gamma)
         for g in (0, 1) for gamma in (0, 1)}
assert close(table[0, 0], (1 + t) ** 2 / 4)
assert close(table[0, 1], D("0.125"))
assert close(table[1, 0], (1 - t) ** 2 / 4)
assert close(table[1, 1], D("0.125"))
assert table[1, 0] + table[1, 1] > 0

# Event and complement root-mass differences are controlled by sqrt(2e).
root_bound = (2 * e).sqrt()
accept_root_diff = (p_actual.sqrt() - p.sqrt()).copy_abs()
loss_root_diff = ((1 - p_actual).sqrt() - (1 - p).sqrt()).copy_abs()
assert accept_root_diff <= root_bound
assert loss_root_diff <= root_bound

# Pass-conditioned diagnostics are separate from the complete-source e.
p_pass = sum(ideal_gamma(x, "P", x) for x in (0, 1)) / 2
p_pass_actual = sum(sum(actual_joint(x, "P", g, g) for g in (0, 1))
                    for x in (0, 1)) / 2
e_pass = r
pass_bound = (2 * e_pass).sqrt()
assert close(p_pass, D("0.75"))
assert close(p_pass_actual, q)
assert (p_pass_actual.sqrt() - p_pass.sqrt()).copy_abs() <= pass_bound
assert ((1 - p_pass_actual).sqrt() - (1 - p_pass).sqrt()).copy_abs() <= pass_bound

print("t=", t)
print("q=", q, " r=", r)
print("complete-source e=", e, " mean squared full-vector defect=", mean_defect2)
print("ideal p=", p, " actual p'=", p_actual)
print("acceptance-root difference=", accept_root_diff, " loss-root difference=", loss_root_diff)
print("pass-conditioned: e=", e_pass, " p=3/4, p'=q")
print("pass x=0 fine table:", table)
print("PASS: complete branches, coherent defect identity, and post-decoder original fine PVM")
