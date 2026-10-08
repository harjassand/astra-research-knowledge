"""Exact finite diagnostics for the N77 phase-potential example.

This checks selected rational parameters and finite n,d windows. The all-n,
all-d stationarity argument is in FINAL_REPORT.md; this script is not its proof.
"""
from fractions import Fraction as Q
from math import factorial


def phase_potential(vertices, edges):
    """Return integer g with deltaA = g(v)-g(u), or a cycle obstruction.

    edges are directed multiedges (u, v, deltaA). Traversing an edge backward
    subtracts deltaA. Each weakly connected component gets an arbitrary zero.
    """
    adj = {v: [] for v in vertices}
    for u, v, delta in edges:
        if u not in adj or v not in adj:
            raise ValueError("edge endpoint omitted from finite phase set")
        adj[u].append((v, delta))
        adj[v].append((u, -delta))
    potential = {}
    for root in vertices:
        if root in potential:
            continue
        potential[root] = 0
        stack = [root]
        while stack:
            u = stack.pop()
            for v, delta in adj[u]:
                proposed = potential[u] + delta
                if v in potential:
                    if potential[v] != proposed:
                        return None, (u, v, delta, potential[v], proposed)
                else:
                    potential[v] = proposed
                    stack.append(v)
    return potential, None


def phase_weights(n, rates):
    k1, k2, k3, _, _ = rates
    return (
        Q(1, 2) / k1,
        Q(1, (n + 1)) / k2,
        Q(1, 2 * (n + 1) * (n + 2) * (n + 3)) / k3,
    )


def unnormalized_poisson_weight(d, rho):
    return rho**d / factorial(d)


def verify_balance(n, d, rates):
    """Check the global-balance equation at phases 0,1,2 and D=d."""
    k1, k2, k3, k4, k5 = rates
    r0 = 2 * k1
    r1 = (n + 1) * k2
    r2 = 2 * (n + 1) * (n + 2) * (n + 3) * k3
    birth = 2 * k4
    death_per_D = 2 * k5
    rho = k4 / k5
    weights = phase_weights(n, rates)
    pD = unnormalized_poisson_weight(d, rho)
    mass = [w * pD for w in weights]

    # Core cycle fluxes agree because each phase weight is inverse rate.
    assert mass[0] * r0 == mass[1] * r1
    assert mass[1] * r1 == mass[2] * r2

    # D immigration/death balances locally in phase 0.
    incoming_D = Q(0)
    if d > 0:
        incoming_D += mass[0] * unnormalized_poisson_weight(d - 1, rho) / pD * birth
    incoming_D += mass[0] * unnormalized_poisson_weight(d + 1, rho) / pD * death_per_D * (d + 1)
    outgoing_D = mass[0] * (birth + death_per_D * d)
    assert incoming_D == outgoing_D

    # Check total incoming == total outgoing in all three phases.
    incoming0 = mass[2] * r2 + incoming_D
    outgoing0 = mass[0] * (r0 + birth + death_per_D * d)
    incoming1 = mass[0] * r0
    outgoing1 = mass[1] * r1
    incoming2 = mass[1] * r1
    outgoing2 = mass[2] * r2
    assert incoming0 == outgoing0
    assert incoming1 == outgoing1
    assert incoming2 == outgoing2


def verify_reversible_completion(n, d):
    """Check pairwise detailed balance for the four-pair revision at unit rates."""
    q = n + 1
    raw = (Q(1, 2), Q(1, q), Q(1, 2 * q * (q + 1) * (q + 2)))
    z = sum(raw)
    p0, p1, p2 = (w / z for w in raw)
    pD = Q(1, factorial(d))  # e^-1 cancels from every detailed-balance equation
    pD_next = Q(1, factorial(d + 1))

    # Three reversible core pairs, written as forward flux = reverse flux.
    assert p0 * 2 == p1 * q
    assert p1 * q == p2 * 2 * q * (q + 1) * (q + 2)
    assert p2 * 2 * q * (q + 1) * (q + 2) == p0 * 2

    # Reversible catalyst pair at phase 0.
    assert p0 * pD * 2 == p0 * pD_next * 2 * (d + 1)

    # The original phase potential is unchanged by adding reversed arrows.
    g, obstruction = phase_potential(
        [0, 1, 2],
        [(0, 1, 1), (1, 0, -1), (1, 2, 2), (2, 1, -2),
         (2, 0, -3), (0, 2, 3), (0, 0, 0)],
    )
    assert obstruction is None and g == {0: 0, 1: 1, 2: 3}


def exact_rank(columns):
    rows = [[Q(col[i]) for col in columns] for i in range(len(columns[0]))]
    pivot_row = 0
    for col in range(len(columns)):
        pivot = next((r for r in range(pivot_row, len(rows)) if rows[r][col]), None)
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        scale = rows[pivot_row][col]
        rows[pivot_row] = [x / scale for x in rows[pivot_row]]
        for r in range(len(rows)):
            if r != pivot_row and rows[r][col]:
                factor = rows[r][col]
                rows[r] = [a - factor * b for a, b in zip(rows[r], rows[pivot_row])]
        pivot_row += 1
        if pivot_row == len(rows):
            break
    return pivot_row


def main():
    phase_edges = [(0, 1, 1), (1, 2, 2), (2, 0, -3), (0, 0, 0)]
    g, obstruction = phase_potential([0, 1, 2], phase_edges)
    assert obstruction is None
    assert g == {0: 0, 1: 1, 2: 3}

    # Every selected parameter tuple is positive and rational.
    rates = (Q(2, 3), Q(5, 7), Q(3, 2), Q(5, 4), Q(7, 6))
    for n in range(9):
        for d in range(31):
            verify_balance(n, d, rates)
            verify_reversible_completion(n, d)

    stoich = [
        (1, 1, -1, 0),
        (2, 1, -1, 0),
        (-3, -2, 2, 0),
        (0, 0, 0, 1),
        (0, 0, 0, -1),
    ]
    assert exact_rank(stoich) == 3
    assert all(v[1] + v[2] == 0 for v in stoich)

    n = 9
    Dn = (n + 1) ** 3 + 5 * (n + 1) ** 2 + 8 * (n + 1) + 5
    phase_probs = (
        Q((n + 1) * (n + 2) * (n + 3), Dn),
        Q(2 * (n + 2) * (n + 3), Dn),
        Q(1, Dn),
    )
    assert phase_probs == (Q(1320, 1585), Q(264, 1585), Q(1, 1585))
    assert sum(phase_probs) == 1
    expected_A_offset = phase_probs[1] + 3 * phase_probs[2]
    assert expected_A_offset == Q(267, 1585)

    ode_dI = (Q(1, 2) - Q(1, 2)) * Q(9, 4) + (Q(3, 2) - Q(1, 2)) * Q(3, 8) + (2 * Q(1, 2) - 2) * Q(1, 32)
    assert ode_dI == Q(11, 32)

    print("PASS: exact phase potential, rank/conservation, n=9 law, ODE drift,")
    print("      finite rational stationarity checks for original and reversible graphs")
    print("Scope: selected rational rates, n=0..8, d=0..30; see report for all-n, all-d algebraic proofs.")


if __name__ == "__main__":
    main()
