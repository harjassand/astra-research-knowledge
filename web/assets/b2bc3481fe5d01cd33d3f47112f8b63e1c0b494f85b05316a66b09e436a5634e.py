"""Reproduce the finite-state cell-size calculations in v1.txt.

Uses only the Python standard library. All volumes are dimensionless.
"""

from math import exp, log


EPS = 0.1
B = [1.0 - EPS, 1.0, 1.0 + EPS]
P_ADDER = [
    [0.5, 0.5, 0.0],
    [0.5, 0.0, 0.5],
    [0.0, 0.5, 0.5],
]
P_SIZER = [
    [0.0, 1.0, 0.0],
    [0.25, 0.5, 0.25],
    [0.0, 1.0, 0.0],
]


def row_means(matrix, values):
    return [sum(p * x for p, x in zip(row, values)) for row in matrix]


def stationary_row(matrix, iterations=100000, tolerance=1e-15):
    n = len(matrix)
    pi = [1.0 / n] * n
    for _ in range(iterations):
        nxt = [sum(pi[i] * matrix[i][j] for i in range(n)) for j in range(n)]
        if max(abs(nxt[i] - pi[i]) for i in range(n)) < tolerance:
            return nxt
        pi = nxt
    raise RuntimeError("stationary iteration did not converge")


def ols_slope(x, y, weights):
    xbar = sum(w * z for w, z in zip(weights, x))
    ybar = sum(w * z for w, z in zip(weights, y))
    cov = sum(w * (xx - xbar) * (yy - ybar)
              for w, xx, yy in zip(weights, x, y))
    var = sum(w * (xx - xbar) ** 2 for w, xx in zip(weights, x))
    return cov / var


def leading_eigenpair(matrix, iterations=10000, tolerance=1e-14):
    n = len(matrix)
    vector = [1.0] * n
    for _ in range(iterations):
        nxt = [sum(matrix[i][j] * vector[j] for j in range(n))
               for i in range(n)]
        scale = max(nxt)
        nxt = [z / scale for z in nxt]
        if max(abs(nxt[i] - vector[i]) for i in range(n)) < tolerance:
            vector = nxt
            break
        vector = nxt
    rayleigh = sum(vector[i] * sum(matrix[i][j] * vector[j]
                                   for j in range(n))
                   for i in range(n)) / sum(z * z for z in vector)
    return rayleigh, vector


def tree_tilt(matrix, birth_sizes, generation_times):
    """Euler-Lotka tilt for a random extant tip's ancestral lineage.

    A_ij(r) = 2 exp(-r T_i) P_ij. Solve rho(A)=1, then
    Q_ij = A_ij v_j / v_i, where A v = v.
    """
    n = len(matrix)

    def tilted(r):
        return [[2.0 * exp(-r * generation_times[i]) * matrix[i][j]
                 for j in range(n)] for i in range(n)]

    low = 0.0
    high = 10.0 / min(generation_times)
    for _ in range(100):
        mid = (low + high) / 2.0
        rho, _ = leading_eigenpair(tilted(mid), iterations=3000)
        if rho > 1.0:
            low = mid
        else:
            high = mid
    growth_rate = (low + high) / 2.0
    a = tilted(growth_rate)
    _, reproductive_value = leading_eigenpair(a)
    q = [[a[i][j] * reproductive_value[j] / reproductive_value[i]
          for j in range(n)] for i in range(n)]
    phase_weights = stationary_row(q)
    mean_added = [2.0 * sum(q[i][j] * birth_sizes[j] for j in range(n))
                  - birth_sizes[i] for i in range(n)]
    slope = ols_slope(birth_sizes, mean_added, phase_weights)
    return growth_rate, q, phase_weights, mean_added, slope


def main():
    mean_next_adder = row_means(P_ADDER, B)
    delta_adder = [2.0 * x - b for x, b in zip(mean_next_adder, B)]
    pi_adder = [1.0 / 3.0] * 3
    var_adder = sum(pi_adder[i] * (B[i] - 1.0) ** 2 for i in range(3))

    mean_next_sizer = row_means(P_SIZER, B)
    delta_sizer = [2.0 * x - b for x, b in zip(mean_next_sizer, B)]
    pi_sizer = stationary_row(P_SIZER)
    mean_sizer = sum(pi_sizer[i] * B[i] for i in range(3))
    var_sizer = sum(pi_sizer[i] * (B[i] - mean_sizer) ** 2
                    for i in range(3))

    print("finite-state forward models")
    print("volumes:", B)
    print("adder P stationary: ", pi_adder)
    print("adder row E[B_next|H]:", mean_next_adder)
    print("adder E[Delta|H]:    ", delta_adder)
    print("adder stationary Var(B):", var_adder)
    print("sizer P stationary: ", pi_sizer)
    print("sizer row E[B_next|H]:", mean_next_sizer)
    print("sizer E[Delta|H]:    ", delta_sizer)
    print("sizer stationary Var(B):", var_sizer)
    print("adder do(B) Delta slopes:", [1.0 / b for b in B])
    print("sizer do(B) Delta slopes:", [2.0 / b - 1.0 for b in B])

    print("\nvariable-timer population tilt for forward adder P")
    result = tree_tilt(P_ADDER, B, [0.2, 1.0, 2.0])
    growth_rate, q, phase_weights, mean_added, slope = result
    print("Euler-Lotka r:", growth_rate)
    print("retrospective Q:")
    for row in q:
        print("  ", row)
    print("retrospective phase weights:", phase_weights)
    print("retrospective E[Delta|H]:", mean_added)
    print("retrospective OLS slope:", slope)


if __name__ == "__main__":
    main()
