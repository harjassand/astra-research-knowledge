"""Exact finite checks for the archive-channel interface audit.

This is a finite diagnostic of normalizations and the proper-score coefficient,
not a proof of the asymptotic memory theorem or its quantum information bound.
"""
from fractions import Fraction as F
import json
from pathlib import Path


def periodic_hat_channel(J=4, N=16):
    assert N % J == 0
    nodes = [F(j, J) for j in range(J)]

    def hat(j, k):
        x = F(k, N)
        delta = abs(x - nodes[j])
        delta = min(delta, 1 - delta)
        return max(F(0), 1 - J * delta)

    phi = [[hat(j, k) for k in range(N)] for j in range(J)]
    assert all(sum(phi[j][k] for j in range(J)) == 1 for k in range(N))
    masses = [sum(row, F(0)) / N for row in phi]
    decoder = [[phi[j][y] / (N * masses[j]) for j in range(J)]
               for y in range(N)]  # decoder[y][j]
    assert all(sum(decoder[y][j] for y in range(N)) == 1 for j in range(J))
    kernel = [[sum(phi[j][x] * decoder[y][j] for j in range(J))
               for x in range(N)] for y in range(N)]
    assert all(sum(kernel[y][x] for y in range(N)) == 1 for x in range(N))
    assert all(sum(kernel[y][x] for x in range(N)) == 1 for y in range(N))
    assert all(kernel[y][x] == kernel[x][y]
               for y in range(N) for x in range(N))
    # K is a Gram matrix: z^T K z = sum_j (sum_x z_x phi_j(x))^2/(N m_j).
    z = [F((k * 7) % 11 - 5, 3) for k in range(N)]
    quadratic_form = sum((sum(z[x] * phi[j][x] for x in range(N)) ** 2)
                          / (N * masses[j]) for j in range(J))
    assert quadratic_form >= 0
    return {"labels_D": J, "output_points": N,
            "reference_masses": [str(x) for x in masses],
            "column_sums_one": True, "row_sums_one": True,
            "symmetric": True, "gram_quadratic_form": str(quadratic_form)}


def proper_score_and_tv():
    # Common reference mu on {-1,0,1}; P_±(x)=mu(x)(1±s x), s=1/2.
    mu = {F(-1): F(1, 3), F(0): F(1, 3), F(1): F(1, 3)}
    s = F(1, 2)

    def Fscore(p):
        if p < F(1, 4):
            return F(3, 8) - p
        if p <= F(3, 4):
            return 2 * (p - F(1, 2)) ** 2
        return p - F(5, 8)

    def dF(p):
        if p < F(1, 4):
            return F(-1)
        if p <= F(3, 4):
            return 4 * p - 2
        return F(1)

    def loss(t, p):
        endpoint = Fscore(F(t))
        return endpoint - Fscore(p) - (F(t) - p) * dF(p)

    plus = {x: mu[x] * (1 + s * x) for x in mu}
    minus = {x: mu[x] * (1 - s * x) for x in mu}
    tv_plus = sum(abs(plus[x] - mu[x]) for x in mu) / 2
    tv_minus = sum(abs(minus[x] - mu[x]) for x in mu) / 2

    def posterior(x):
        return (1 + s * x) / 2

    # D_F(r,q)=s(U-V)^2/4 for these posterior values.
    distortion = sum(mu[x] * mu[y] *
                     (Fscore(posterior(x)) - Fscore(posterior(y))
                      - (posterior(x) - posterior(y)) * dF(posterior(y)))
                     for x in mu for y in mu)
    expected_square = sum(mu[x] * mu[y] * (x - y) ** 2 for x in mu for y in mu)
    assert distortion == s * expected_square / 4
    # Directly check the average proper-score risk difference under T-X-Y,
    # where the D=1 decoder outputs an independent reference sample Y~mu.
    risk_x = sum(mu[x] *
                 (posterior(x) * loss(1, posterior(x))
                  + (1 - posterior(x)) * loss(0, posterior(x)))
                 for x in mu)
    risk_y = sum(mu[x] * mu[y] *
                 (posterior(x) * loss(1, posterior(y))
                  + (1 - posterior(x)) * loss(0, posterior(y)))
                 for x in mu for y in mu)
    assert risk_y - risk_x == distortion
    all_losses = [loss(t, posterior(x)) for t in (0, 1) for x in mu]
    assert min(all_losses) >= 0 and max(all_losses) <= 1
    return {"D": 1, "tv_plus": str(tv_plus), "tv_minus": str(tv_minus),
            "expected_squared_feature_error": str(expected_square),
            "expected_Bregman_regret": str(distortion),
            "risk_difference": str(risk_y - risk_x),
            "loss_range": [str(min(all_losses)), str(max(all_losses))]}


def prior_average_is_not_uniform():
    eta = F(1, 100)
    p0 = {0: F(1, 2), 1: F(1, 2)}
    p1 = {0: F(1, 4), 1: F(3, 4)}
    tv = sum(abs(p0[x] - p1[x]) for x in p0) / 2
    average = eta * tv  # zero-memory decoder always emits P_0
    worst = tv
    assert average == F(1, 400) and worst == F(1, 4)
    return {"parameter_prior_mass_on_hard_state": str(eta),
            "D": 1, "prior_average_tv": str(average),
            "worst_case_tv": str(worst)}


def main():
    result = {
        "scope": "finite exact interface and normalization checks only",
        "periodic_hat_channel": periodic_hat_channel(),
        "proper_score_tv_transfer": proper_score_and_tv(),
        "average_vs_uniform": prior_average_is_not_uniform(),
    }
    path = Path(__file__).with_name("interface_audit.json")
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
