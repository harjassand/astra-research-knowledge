"""Exact-equilibrium diagnostic for the 3-state hidden-rotation example.

This is a numerical check of the asymptotic coefficients in
high_drive_acquisition.md, not a proof or a physical experiment.
Requires mpmath 1.3 or newer.
"""

import mpmath as mp


mp.mp.dps = 60
sqrt2 = mp.sqrt(2)
Q = mp.matrix([[1 / sqrt2, -1 / sqrt2], [1 / sqrt2, 1 / sqrt2]])
B = mp.matrix([[1, 0], [0, 2]])
b = mp.matrix([1, 1])
B_rot = Q.T * B * Q
b_rot = Q.T * b


def equilibrium(epsilon, input_level, hidden_matrix, coupling, port_guess):
    """Solve the exact equilibrium for alpha=a=1 by high-precision Newton."""
    hidden_guess_vector = -epsilon * port_guess * mp.lu_solve(
        hidden_matrix, coupling
    )

    def equations(y, z0, z1):
        return (
            y + y**3 + epsilon * (coupling[0] * z0 + coupling[1] * z1)
            - input_level,
            epsilon * coupling[0] * y
            + hidden_matrix[0, 0] * z0
            + hidden_matrix[0, 1] * z1
            + z0**3,
            epsilon * coupling[1] * y
            + hidden_matrix[1, 0] * z0
            + hidden_matrix[1, 1] * z1
            + z1**3,
        )

    return mp.findroot(
        equations,
        (port_guess, hidden_guess_vector[0], hidden_guess_vector[1]),
        solver="mdnewton",
        tol=mp.mpf("1e-50"),
        maxsteps=100,
    )


moderate_input = mp.mpf("0.7")
moderate_y0 = mp.findroot(lambda y: y + y**3 - moderate_input, mp.mpf("0.6"))
moderate_prediction = mp.mpf(7) * moderate_y0**3 / (
    32 * (1 + 3 * moderate_y0**2)
)
print("moderate bias u=0.7; predicted gap/epsilon^4:", mp.nstr(moderate_prediction, 14))
for eps_text in ("0.2", "0.1", "0.05", "0.025"):
    epsilon = mp.mpf(eps_text)
    first = equilibrium(
        epsilon, moderate_input, B, b, mp.mpf("0.6")
    )
    second = equilibrium(
        epsilon, moderate_input, B_rot, b_rot, mp.mpf("0.6")
    )
    print(
        "epsilon=",
        eps_text,
        " observed gap/epsilon^4=",
        mp.nstr((first[0] - second[0]) / epsilon**4, 14),
    )

scaled_t = mp.mpf("0.1")
high_prediction = mp.mpf(7) * scaled_t / 96
print("scaled bias t=0.1; predicted limit gap/epsilon^3:", mp.nstr(high_prediction, 14))
for eps_text in ("0.1", "0.05", "0.025", "0.0125"):
    epsilon = mp.mpf(eps_text)
    input_level = scaled_t**3 / epsilon**3
    port_guess = scaled_t / epsilon - epsilon / (3 * scaled_t)
    first = equilibrium(epsilon, input_level, B, b, port_guess)
    second = equilibrium(epsilon, input_level, B_rot, b_rot, port_guess)
    print(
        "epsilon=",
        eps_text,
        " observed gap/epsilon^3=",
        mp.nstr((first[0] - second[0]) / epsilon**3, 14),
    )
