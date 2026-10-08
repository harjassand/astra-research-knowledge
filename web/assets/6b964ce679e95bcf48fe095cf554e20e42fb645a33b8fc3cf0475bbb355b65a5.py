#!/usr/bin/env python3
"""Reproduce cycle4's finite Haar-existence gate and entropy arithmetic.

This is a Decimal arithmetic diagnostic. It does not generate Haar matrices
or produce a finite seed. The source-constant extraction is recorded in
CONSTANT_AUDIT.txt; this script checks its numerical consequences.
"""

from decimal import Decimal, getcontext


getcontext().prec = 60
D = Decimal

K = 260
d = 65
k = 2
ball1 = 1 + 2 * d * k
coeff_n = 2 * ball1
C = D(50).sqrt()
score_slack = D("0.165")
bell_entropy_tolerance = D("0.001")
score_e = score_slack / (D(6) * D(ball1 + 1) * C)
net_radius = score_slack / (D(2) * D(K))
net_log_size = D(K * K - 1) * (D(1) + D(2) / net_radius).ln()

# Exact fibre counts in the r=2 free quotient.
fibre_size_1 = K * K // 2 - K
fibre_size_2 = K * K // 4
assert fibre_size_1 + 2 * fibre_size_2 + K == K * K
assert 1 + fibre_size_1 + fibre_size_2 == 50441

def entropy_from_fibres():
    terms = [
        (1, K),
        (fibre_size_2, 2),
        (fibre_size_1, 1),
    ]
    return -sum(
        D(count) * (D(size) / D(K * K)) * (D(size) / D(K * K)).ln()
        for count, size in terms
    )


bell_entropy = entropy_from_fibres()
minimum_entropy_free = -((D(K) + C * C) / D(K * K)).ln()
minimum_entropy_slack = -((D(K) + (C + score_slack) ** 2) / D(K * K)).ln()
free_gap = D(2) * minimum_entropy_free - bell_entropy
slack_gap = D(2) * minimum_entropy_slack - bell_entropy
gap_after_bell_tolerance = slack_gap - bell_entropy_tolerance
assert free_gap > D("0.011")
assert slack_gap > D("0.001")

# Audenaert: h_2(T) + T ln(D-1) <= tolerance for D=K^2.
out_dim = K * K
lo, hi = D(0), D("0.001")
for _ in range(300):
    t = (lo + hi) / 2
    h2 = -(t * t.ln() + (D(1) - t) * (D(1) - t).ln())
    bound = h2 + t * D(out_dim - 1).ln()
    if bound > bell_entropy_tolerance:
        hi = t
    else:
        lo = t
trace_distance_tolerance = lo
# Each Bell matrix entry is K^-2 times a normalized word trace. If all raw
# traces are within delta, every entry is within delta/K^2; hence
# ||Delta||_F<=delta and T=||Delta||_1/2<=K*delta/2.
entry_trace_tolerance = D(2) * trace_distance_tolerance / D(K)

# Meckes product-Haar one-sided tail, then a union bound over the score net.
conc_N = (
    D(2)
    + D(96 * d * k)
    * (net_log_size + D(3).ln())
    / (score_e / D(2)) ** 2
)

# Bordenave-Collins Lemma 9.3 extended via Theorem 5.1's ell_0 condition:
# with N=n_prefactor*p^power, allocate half of
# log(1+e/2) to the known factor and half to the extracted c_E<=780 factor.
# The source's Theorem 1.1 selects power 16d+80, but its Theorem 5.1
# moment estimate directly permits every even p up to the ell_0 gate
# 12d+56. Reconstruct that stronger range with the exact leading factor
# N_prefactor=(2*(2d)^(7/2))^4=16*(2d)^14.
power = 12 * d + 56
n_prefactor = 16 * (2 * d) ** 14
n_prefactor_D = D(n_prefactor)
known_log_budget = (D(1) + score_e / D(2)).ln() / D(2)
def known_log_r(p):
    return (
        D(3) * D(2 * coeff_n).ln()
        + D(3) * n_prefactor_D.ln()
        + (D(3 * power) + D(9)) * p.ln()
    ) / p

lo_p, hi_p = D(1), D("1e16")
for _ in range(300):
    mid_p = (lo_p + hi_p) / 2
    if known_log_r(mid_p) > known_log_budget:
        lo_p = mid_p
    else:
        hi_p = mid_p
p_root = hi_p
p_even = int(p_root.to_integral_value(rounding="ROUND_CEILING"))
if p_even % 2:
    p_even += 1
p = D(p_even)
assert known_log_r(p) <= known_log_budget
log2_p = p.ln() / D(2).ln()
log2_N = D(power) * log2_p + n_prefactor_D.ln() / D(2).ln()
input_qubits_per_use = D(k) * log2_N
two_use_qubits = D(2) * input_qubits_per_use
flagged_input_qubits_per_use = input_qubits_per_use + D(1)
flagged_two_use_qubits = D(2) * flagged_input_qubits_per_use
c0 = D(780)
ln_N = D(power) * p.ln() + n_prefactor_D.ln()
# The complete hidden factor is (1+c0/sqrt(N))^2. Since ln(1+x)<=x,
# it suffices to verify 2*c0/sqrt(N)<=known_log_budget.
hidden_upper_ln = (D(2) * c0).ln() - ln_N / D(2)
assert hidden_upper_ln <= known_log_budget.ln()
assert known_log_r(p) <= known_log_budget

# Optional Bell trace-convergence diagnostic. The exact product-conjugate
# quotient-Gram majorization proves the entropy bound at every finite N, so
# this trace threshold is not part of the existence theorem.
bell_log_failure_budget = (D(24) * D(K**4)).ln()
bell_trace_N_sq_rhs = D(3072) * bell_log_failure_budget / entry_trace_tolerance**2
bell_trace_N = int((D(1) + (D(1) + bell_trace_N_sq_rhs).sqrt()).to_integral_value(rounding="ROUND_CEILING"))
bell_mean_N = int((D(2) / entry_trace_tolerance).sqrt().to_integral_value(rounding="ROUND_CEILING"))
bell_gate_N = max(bell_trace_N, bell_mean_N)

# Check the source hypotheses at the selected d=65 point.
ln_N = D(power) * p.ln() + n_prefactor_D.ln()
assert ln_N >= D(70) * D(d).ln()  # N >= d^70
assert p.ln() <= ln_N / D(power)  # p <= N^(1/(12d+56))
ell0_lhs = D(2).ln() + D("3.5") * D(2 * d).ln() + D(3 * d + 14) * p.ln()
assert ell0_lhs == ln_N / D(4)  # Theorem 5.1 ell_0 gate, equality by N0 choice
assert (
    D(4 * d + 16) * p.ln() + D(d**4).ln()
    <= ln_N / D(2)
)  # displayed second-moment simplification
assert D(2).ln() + D("3.5") * p.ln() <= D(2) * ln_N  # q<=p in Theorem 11
# The concentration threshold is negligible relative to the p-range scale.
assert log2_N > conc_N.ln() / D(2).ln()

print(f"K={K}, d={d}, k={k}, |B1|={ball1}, coefficient dimension={coeff_n}")
print(f"Bell fibre counts: size K: 1; size 2: {fibre_size_2}; size 1: {fibre_size_1}")
print(f"H_B={bell_entropy}")
print(f"C={C}")
print(f"free gap={free_gap}")
print(f"score-slack gap={slack_gap}")
print(f"gap after optional 0.001-nat Bell continuity debit={gap_after_bell_tolerance}")
print(f"eta={net_radius}")
print(f"log net size<={net_log_size}")
print(f"e={score_e}")
print(f"concentration N threshold≈{conc_N}; log2≈{conc_N.ln()/D(2).ln()}")
print("source gates: N>=d^70, p<=N^(1/(12d+56)), ell0 equality, second-moment and Theorem 11 path-count bounds all pass")
print(f"even p≈{p_even}; log2 p≈{log2_p}")
print(f"N_prefactor={n_prefactor}; N=N_prefactor*p^{power}")
print(f"log2 N≈{log2_N}")
print(f"extracted c0 upper bound={c0}; log2(2*c0/sqrt(N))={hidden_upper_ln/D(2).ln()}")
print(f"input qubits/use≈{input_qubits_per_use}")
print(f"two-use witness qubits≈{two_use_qubits}")
print(f"flagged input qubits/use≈{flagged_input_qubits_per_use}")
print(f"flagged two-use witness qubits≈{flagged_two_use_qubits}")
print(f"Audenaert trace distance T<={trace_distance_tolerance}")
print(f"sufficient entrywise length-4 trace tolerance<={entry_trace_tolerance}")
print(f"finite Bell trace N threshold={bell_gate_N}; log2≈{D(bell_gate_N).ln()/D(2).ln()}")
print(f"score event probability >= 2/3 at N=n_prefactor*p^{power}; exact product-conjugate Bell entropy bound needs no trace event")
print("optional finite Bell trace-approximation diagnostic is not used in the theorem")
