"""Small exact check of the conditional signed-reference theorem.

All acquisition/certification accepts only the raw interval interface.
Hidden source access is confined to post-choice finite verification.
"""
from fractions import Fraction as F
from pathlib import Path
import json
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "p1_next" / "code"))
import noisy_quotient as nq
import native_source as ns
import continuous_certificate as cc


class ShiftedOracle:
    def __init__(self, oracle, reference):
        self._call = oracle.call
        self.reference = list(reference)

    def call(self, x):
        return self._call([a + b for a, b in zip(self.reference, x)])


def nominal_F(model, d):
    r = len(model.landmarks)
    if not r:
        return sum(d, F(0))
    h = [row[:] for row in model.Wmid]
    q = [F(0)] * r
    for i, di in enumerate(d):
        c = model.col(i)
        for j in range(r):
            q[j] += di * c[j]
            for k in range(r):
                h[j][k] += di * c[j] * c[k]
    assert nq.positive_definite(h)
    return sum(d, F(0)) - nq.dot(q, nq.mv(nq.inverse(h), q))


def signed_certificate(model, reference, u, prices):
    n = model.n
    assert len(u) == len(reference) == len(prices) == n
    assert min(u) >= 0 and sum(u) <= F(1, 5)
    alpha = [p[1] * t[1] for p, t in zip(model.P, model.Tdiag)]
    gamma = 1 - nq.dot(reference, alpha)
    sd = [model.nominal_entry(i, i) for i in range(n)]
    gamma_star = 1 - sum((w * p[1] * s for w, p, s in zip(reference, model.P, sd)), F(0))
    if gamma <= 0 or gamma_star <= 0:
        return {"status": "unresolved_coercivity", "gamma": gamma, "gamma_star": gamma_star}
    x = [ui - wi for ui, wi in zip(u, reference)]
    a = [abs(xi) * p[1] for xi, p in zip(x, model.P)]
    dl = [min(xi * p[0], xi * p[1]) for xi, p in zip(x, model.P)]
    du = [max(xi * p[0], xi * p[1]) for xi, p in zip(x, model.P)]
    dm = [xi * nq.mid(p) for xi, p in zip(x, model.P)]
    agg = model.certificate_aggregates(a)
    L = sum(a, F(0))
    kappa = agg["kappa_fit"] + agg["kappa_residual"]
    B = 1 + sum((ai * s[1] for ai, s in zip(a, model.Sdiag)), F(0)) / gamma
    Bs = 1 + nq.dot(a, sd) / gamma_star
    ferr = L * B * Bs * kappa
    fl, fu = nominal_F(model, dl) - ferr, nominal_F(model, du) + ferr
    zl, zu = model.z0
    denlo, denhi = max(zl + fl, gamma * zl), zu + fu
    assert 0 < denlo <= denhi
    zi = (max(zl * zl / denhi, zl / (1 + nq.dot(u, alpha))),
          min(zu * zu / denlo, zu / gamma))
    assert zi[0] <= zi[1]
    k0 = cc.nominal_k(model, dm)
    roots = [nq.sqrt_bounds(si, model.bits)[1] for si in sd]
    pterm = sum((roots[j] * abs(x[j]) * nq.rad(model.P[j]) * abs(k0[j]) for j in range(n)), F(0)) / gamma_star
    factor = ((zi[0] / zu) ** 2, (zi[1] / zl) ** 2)
    gradients, kintervals = [], []
    for i in range(n):
        err = B * nq.sqrt_bounds(L * agg["fit_row_squares"][i], model.bits)[1]
        err += B * nq.sqrt_bounds(L * model.rho[i] * agg["kappa_residual"], model.bits)[1]
        err += B * Bs * kappa * nq.sqrt_bounds(L * agg["nominal_row_squares"][i], model.bits)[1]
        err += roots[i] * pterm
        ki = (k0[i] - err, k0[i] + err)
        ks = cc.square_interval(ki)
        gradients.append((factor[0] * model.P[i][0] * ks[0] - prices[i],
                          factor[1] * model.P[i][1] * ks[1] - prices[i]))
        kintervals.append(ki)
    lower, upper = [g[0] for g in gradients], [g[1] for g in gradients]
    base = -nq.dot(u, lower)
    regret = max([F(0), base] + [base + F(1, 5) * upper[i] - u[i] * (upper[i] - lower[i]) for i in range(n)])
    return {"status": "certified", "u": u, "reference": reference, "prices": prices,
            "displacement": x, "gamma": gamma, "gamma_star": gamma_star,
            "F_interval": (fl, fu), "F_error": ferr, "Z_interval": zi,
            "gradient_intervals": gradients, "k_intervals": kintervals,
            "global_regret": regret, "B_true": B, "B_nominal": Bs}


def contains(iv, v):
    return iv[0] <= v <= iv[1]


def main():
    source = ns.NativeSource([[F(1), F(1)], [F(0), F(1)]], label="two_control_initially_dark")
    reference = [F(1, 40), F(1, 40)]
    oracle = ns.CalibratedOracle(source, eta=F(1, 10**10))
    acquired = nq.acquire(ShiftedOracle(oracle, reference), 2,
                          delta=F(1, 5) - sum(reference), landmark_budget=1, bits=64)
    assert acquired.model is not None and acquired.status.startswith("resolved")
    # Later commands include every kind of sign pattern and original faces.
    commands = [[F(0), F(0)], reference, [F(1, 5), F(0)], [F(0), F(1, 5)],
                [F(1, 10), F(1, 10)], [F(1, 100), F(3, 20)],
                [F(7, 50), F(1, 25)]]
    prices = [F(3, 5), F(0)]
    certs = [signed_certificate(acquired.model, reference, u, prices) for u in commands]
    source_calls_after_choices = len(oracle.records)
    # The source is inspected only here, after command/certificate choices.
    for cert in certs:
        assert cert["status"] == "certified"
        z, reward, gradient = source.state_and_gradient(cert["u"], prices)
        assert contains(cert["Z_interval"], z)
        assert all(contains(iv, g) for iv, g in zip(cert["gradient_intervals"], gradient))
        tangent = max([F(0), -nq.dot(cert["u"], gradient)] +
                      [F(1, 5) * g - nq.dot(cert["u"], gradient) for g in gradient])
        assert tangent <= cert["global_regret"]
        cert.update({"checker_Z": z, "checker_gradient": gradient, "checker_tangent_bound": tangent})
    for record in oracle.records:
        u = [F(0), F(0)]
        for i, x in record["requested_sparse"]:
            u[i] = x
        assert contains(record["R_interval"], source.independent_response(u))
    assert len(oracle.records) == source_calls_after_choices == 6
    assert source.response([F(0), F(1, 5)]) == source.response([F(0), F(0)])
    assert source.response([F(1, 10), F(1, 10)]) != source.response([F(1, 10), F(0)])
    chain = []
    for depth in (1, 2, 4):
        vs = []
        for j in range(depth):
            v = [F(0)] * (depth + 1)
            v[j] = v[j + 1] = F(1)
            vs.append(v)
        vs.append([F(0)] * depth + [F(1)])
        s = ns.NativeSource(vs, label=f"bounded_norm_chain_depth_{depth}")
        w = [F(1, 20 * (depth + 1))] * (depth + 1)
        q = s.matrix(w)
        state = ns.solve(q, [F(1)] + [F(0)] * depth)
        product = F(1)
        for t in w[:-1]:
            product *= t
        expected = (-1) ** depth * product / ns.determinant(q)
        assert state[-1] == expected
        delta = F(1, 5)
        z_effect = delta * (delta / depth) ** (2 * depth)
        chain.append({"depth": depth, "reference": w, "terminal_coupling": expected,
                      "terminal_P": expected ** 2, "uniform_Z_deletion_bound": z_effect,
                      "uniform_R_deletion_bound": (1 + 2 * delta) ** 2 * z_effect})
    results = {"scope": "Fresh finite checks of conditional theorem; no device and no independent whole-proof audit.",
               "status": acquired.status, "landmarks": acquired.model.landmarks,
               "reference": reference, "ledger": oracle.ledger(), "certificates": certs,
               "dark_chain_checks": chain, "all_exact_checks_passed": True}
    raw = {"calibration": oracle.calibration, "alpha": oracle.alpha, "beta": oracle.beta,
           "records": oracle.records, "acquisition_ledger": acquired.ledger,
           "unresolved_controls": acquired.unresolved_controls, "rejected_pivots": acquired.rejected_pivots}
    (HERE / "shifted_results.json").write_text(json.dumps(ns.jsonable(results), indent=2) + "\n")
    (HERE / "shifted_raw.json").write_text(json.dumps(ns.jsonable(raw), indent=2) + "\n")
    print(json.dumps({"source_reactions": len(oracle.records), "total_scalar_readings": oracle.ledger()["total_scalar_readings"],
                      "gamma": float(certs[0]["gamma"]), "gamma_star": float(certs[0]["gamma_star"]),
                      "max_Z_interval_width": max(float(c["Z_interval"][1] - c["Z_interval"][0]) for c in certs),
                      "all_exact_checks_passed": True}, indent=2))


if __name__ == "__main__":
    main()
