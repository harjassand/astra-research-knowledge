"""Exact arithmetic witness for the sourcewise-cone quantifier mismatch.

Two one-species mass-action networks:
  N  : 0 -> A, A -> 0
  N' : 0 -> 2A, A -> 0

The signatures are (nu, nu^2). At source 0 the positive rays are disjoint;
at source A the cones coincide. Equality of Langevin generators would require
incompatible positive rate constants at source 0.
"""

from fractions import Fraction


def signature(nu: int) -> tuple[int, int]:
    return nu, nu * nu


def same_positive_ray(a: tuple[int, int], b: tuple[int, int]) -> bool:
    # In R^2, the two nonzero vectors span the same positive ray iff their
    # determinant is zero and their dot product is positive.
    det = a[0] * b[1] - a[1] * b[0]
    dot = a[0] * b[0] + a[1] * b[1]
    return det == 0 and dot > 0


empty_source_n = signature(+1)
empty_source_np = signature(+2)
shared_source_n = signature(-1)
shared_source_np = signature(-1)

assert not same_positive_ray(empty_source_n, empty_source_np)
assert same_positive_ray(shared_source_n, shared_source_np)

# Generator coefficients, ordered as (constant drift, x-drift,
# constant diffusion, x-diffusion):
# N:  (k0, -kA, k0, kA)
# N': (2k0', -kA', 4k0', kA')
# Equality forces k0 = 2 k0' from drift and k0 = 4 k0' from diffusion.
# Since k0' > 0, these equations cannot both hold.
k0_prime = Fraction(1, 1)
k0_from_drift = 2 * k0_prime
k0_from_diffusion = 4 * k0_prime
assert k0_from_drift != k0_from_diffusion

print("PASS: empty-source positive cones are disjoint")
print("PASS: shared-source positive cones intersect")
print("PASS: generator equality would force a zero, hence forbidden, rate")
