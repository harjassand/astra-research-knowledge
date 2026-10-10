"""Interval calculation for a failed conditional EPnI extension.

Uses mpmath.iv to enclose the exact two-mode Gaussian example documented in
../e6_entropy_transfer.txt. Covariance convention: vacuum variance 1/2.
"""

import mpmath as mp

iv = mp.iv
iv.dps = 50


def g(x):
    return (1 + x) * iv.ln(1 + x) - x * iv.ln(x)


def sinh(x):
    return (iv.exp(x) - iv.exp(-x)) / 2


def cosh(x):
    return (iv.exp(x) + iv.exp(-x)) / 2


def symplectic_eigenvalues(a, b, c):
    # Covariance blocks are a I, b I, and c Z.
    delta = a * a + b * b - 2 * c * c
    determinant = (a * b - c * c) ** 2
    radical = iv.sqrt(delta * delta - 4 * determinant)
    return (
        iv.sqrt((delta + radical) / 2),
        iv.sqrt((delta - radical) / 2),
    )


def gaussian_entropy(a, b, c):
    plus, minus = symplectic_eigenvalues(a, b, c)
    half = iv.mpf("0.5")
    return g(plus - half) + g(minus - half)


# Exact input parameters: two-mode squeezing s=1/4 applied to
# tau_{1/2} tensor tau_{1/2}; amplifier gain G=6/5 on mode A; mode B is vacuum.
s = iv.mpf(1) / 4
gain = iv.mpf(6) / 5
a = cosh(2 * s)
c = sinh(2 * s)
reference_entropy = g(a - iv.mpf("0.5"))
input_conditional_entropy = 2 * g(iv.mpf("0.5")) - reference_entropy

output_a = gain * a + (gain - 1) / 2
output_c = iv.sqrt(gain) * c
output_joint_entropy = gaussian_entropy(output_a, a, output_c)
output_conditional_entropy = output_joint_entropy - reference_entropy

# Monotonicity of g and these strict interval comparisons certify
# N(A|R)>0.3895 and N(C|R)<0.6607. The proposed bound would then require
# N(C|R) >= (6/5)*N(A|R)+1/5 > 0.6674, a contradiction.
lower_input_test = g(iv.mpf("0.3895"))
upper_output_test = g(iv.mpf("0.6607"))
conditional_epi_lhs = iv.exp(output_conditional_entropy)
conditional_epi_rhs = gain * iv.exp(input_conditional_entropy) + (gain - 1)
assert input_conditional_entropy.a > lower_input_test.b
assert output_conditional_entropy.b < upper_output_test.a
assert conditional_epi_lhs.a > conditional_epi_rhs.b

print("S(A|R) =", input_conditional_entropy)
print("g(0.3895) =", lower_input_test)
print("S(C|R) =", output_conditional_entropy)
print("g(0.6607) =", upper_output_test)
print("(6/5)*0.3895 + 1/5 =", iv.mpf("0.6674"))
print("conditional EPI lhs =", conditional_epi_lhs)
print("conditional EPI rhs =", conditional_epi_rhs)
print("conditional EPnI extension is false for this product-with-vacuum input")
