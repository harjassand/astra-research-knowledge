"""Reproduce a two-patch rate-and-state linear-stability counterexample.

The stiffness matrix is a grounded two-node elastic network. The local
spring-slider comparison K_ii > sigma_i (b_i-a_i)/Dc_i holds at both
patches, while the exact memory-bearing matrix pencil has an unstable pair.
This is a finite-dimensional model counterexample, not an Earth observation.
"""

import numpy as np


def main() -> None:
    # Nondimensional choices: V0 = Dc = sigma = 1, a = 1/2.
    # K is the SPD stiffness of two nodes with unit grounding and unit
    # mutual coupling; its off-diagonal terms are the elastic interaction.
    stiffness = np.array([[2.0, -1.0], [-1.0, 2.0]])
    a = np.array([0.5, 0.5])
    b = np.array([2.1, 1.9])
    dc = np.array([1.0, 1.0])
    sigma = np.array([1.0, 1.0])
    v0 = 1.0

    # Linearized rate-and-state equation after eliminating the aging-law
    # state variable and multiplying by diag(V0 + s Dc):
    # [A s^2 + B s + C] u = 0.
    A = np.diag(sigma * a * dc / v0)
    B = np.diag(dc) @ stiffness + np.diag(sigma * (a - b))
    C = v0 * stiffness

    zero = np.zeros_like(stiffness)
    identity = np.eye(2)
    companion = np.block(
        [[zero, identity], [-np.linalg.solve(A, C), -np.linalg.solve(A, B)]]
    )
    roots = np.linalg.eigvals(companion)

    # A sitewise use of the scalar k_crit formula would compare the diagonal
    # self stiffness with each local threshold. Both margins are positive.
    local_kcrit = sigma * (b - a) / dc
    local_margins = np.diag(stiffness) - local_kcrit

    np.set_printoptions(precision=8, suppress=True)
    print("local kcrit:", local_kcrit)
    print("local diagonal margins K_ii-kcrit_i:", local_margins)
    print("roots of the exact quadratic matrix pencil:", roots)
    print("unstable roots:", roots[np.real(roots) > 0])


if __name__ == "__main__":
    main()
