"""Exact four-agent witness for per-link PoC versus sampled connectivity.

At each of three event phases, every receiver is missing one different
incoming link of K_4. The partial-information baseline averages its own value
and the two successfully received neighbors. The fail-closed protocol requires
all three neighbor values and makes no update on an incomplete sample.

This is a finite exact calculation, not a simulation of physical energy or a
proof about all event-triggered controllers.
"""

from fractions import Fraction


def matmul(left, right):
    n = len(left)
    return [[sum((left[i][k] * right[k][j] for k in range(n)), Fraction(0))
             for j in range(n)] for i in range(n)]


def dobrushin_coefficient(matrix):
    n = len(matrix)
    overlap = min(
        sum((min(matrix[i][k], matrix[j][k]) for k in range(n)), Fraction(0))
        for i in range(n) for j in range(n)
    )
    return 1 - overlap, overlap


def phase_matrix(offset, n=4):
    """Rows average self and all but sender i+offset (mod n)."""
    matrix = []
    for receiver in range(n):
        row = [Fraction(0) for _ in range(n)]
        row[receiver] = Fraction(1, 3)
        missing_sender = (receiver + offset) % n
        for sender in range(n):
            if sender != receiver and sender != missing_sender:
                row[sender] = Fraction(1, 3)
        matrix.append(row)
    return matrix


phases = [phase_matrix(offset) for offset in (1, 2, 3)]
# State updates are x[k+1] = P_k x[k], hence the backward product.
block = matmul(phases[2], matmul(phases[1], phases[0]))
coefficient, overlap = dobrushin_coefficient(block)

print("three-phase product:")
for row in block:
    print(" ".join(str(value) for value in row))
print(f"minimum row overlap = {overlap}")
print(f"Dobrushin coefficient = {coefficient}")
print(f"diameter contraction per 3-event block <= {coefficient}")

# Per-link outage parameters for rho = delta/10 and attack period 3 delta:
rho_over_delta = Fraction(1, 10)
phi = rho_over_delta / 3 + Fraction(1, 3)
print(f"per-link phi (rho=delta/10, tau_f=3 delta) = {phi}")
