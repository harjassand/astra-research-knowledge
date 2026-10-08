"""Scale check for the Moore bound in the exact permutation route.

The graph-theoretic implication is proved in PROOF.txt. This script evaluates
its exponent comparison; it does not validate the source's trace construction.
"""

from decimal import Decimal, getcontext

getcontext().prec = 40

degree = 128
word_radius = 4
m = 783_519
actual_q_exponent = 24 * m - 7
actual_input_qubit_exponent = 2 * actual_q_exponent

# The Moore BFS tree has at least degree*(degree-1)^(2m-1) vertices on its
# outer shell, so log2(q^2) >= 2 log2(degree) + 2(2m-1)log2(degree-1).
log2 = lambda x: x.ln() / Decimal(2).ln()
lower_q_bits = log2(Decimal(degree)) + Decimal(2 * m - 1) * log2(
    Decimal(degree - 1)
)
lower_input_bits = 2 * lower_q_bits
asymptotic_coefficient = Decimal(4) * log2(Decimal(degree - 1))
ratio = Decimal(actual_input_qubit_exponent) / lower_input_bits

assert actual_input_qubit_exponent == 48 * m - 14
assert lower_input_bits < Decimal(actual_input_qubit_exponent)

print(f"m={m}, source input exponent={actual_input_qubit_exponent}")
print(f"Moore lower bound on input exponent > {lower_input_bits}")
print(f"leading lower-bound coefficient per m = {asymptotic_coefficient}")
print(f"source exponent / Moore lower bound = {ratio}")
