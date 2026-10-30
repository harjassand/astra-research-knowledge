"""Population checks for the sparse internal-load construction.

Exact rational detailed balance with unknown state-dependent conductances;
marked current and energy identities; finite quasi-static work inequalities;
canonical multi-band thermodynamic limit. No acquired or hardware data.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import math


def compositions(total, parts):
    if parts == 1:
        yield (total,)
    else:
        for n in range(total + 1):
            for rest in compositions(total - n, parts - 1):
                yield (n,) + rest


def product_weight(g, weights):
    p = F(1)
    for n, w in zip(g, weights):
        p *= w ** n
    return p


def conductance(g, gp, i, hidden):
    # Symmetric in the paired configurations, but otherwise state dependent.
    key = (i + 1) * sum((j + 1) * (a + b)
                        for j, (a, b) in enumerate(zip(g, gp)))
    return F(2 + (key + hidden) % 11, 7)


def transitions(g, weights, hidden, anchored):
    m = len(g)
    for i in range(1 if anchored else 0, m):
        prev = (i - 1) % m
        for direction in (1, -1):
            source, target = (i, prev) if direction == 1 else (prev, i)
            if not g[source]:
                continue
            gp = list(g)
            gp[source] -= 1
            gp[target] += 1
            gp = tuple(gp)
            c = conductance(g, gp, i, hidden)
            rate = c * weights[prev] / weights[i] if direction == 1 else c
            yield gp, i, direction, rate


def exact_case(m, h, weights, hidden, anchored):
    states = list(compositions(h, m))
    unnormalized = {g: product_weight(g, weights) for g in states}
    z = sum(unnormalized.values())
    pi = {g: w / z for g, w in unnormalized.items()}
    balance = {g: F(0) for g in states}
    current = [F(0) for _ in range(m)]
    edge_count = 0
    energy_residual = 0.0
    weights_float = list(map(float, weights))
    energy = {g: -sum(n * math.log(w) for n, w in zip(g, weights_float))
              for g in states}
    for g in states:
        for gp, i, direction, rate in transitions(g, weights, hidden, anchored):
            reverse = next(r for gg, ii, dd, r in
                           transitions(gp, weights, hidden, anchored)
                           if gg == g and ii == i and dd == -direction)
            assert pi[g] * rate == pi[gp] * reverse
            flow = pi[g] * rate
            balance[g] -= flow
            balance[gp] += flow
            current[i] += direction * flow
            force = math.log(weights_float[(i - 1) % m] / weights_float[i])
            energy_residual = max(
                energy_residual,
                abs(direction * force - (energy[g] - energy[gp])))
            edge_count += 1
    assert all(v == 0 for v in balance.values())
    assert all(v == 0 for v in current)

    energies = list(energy.values())
    emin = min(energies)

    def mean_energy(lam):
        probs = [math.exp(-lam * (e - emin)) for e in energies]
        normalizer = sum(probs)
        return sum(p * e for p, e in zip(probs, energies)) / normalizer

    d_relative = sum(float(p) * math.log(float(p) * len(states))
                     for p in pi.values())
    e0, e1 = mean_energy(0), mean_energy(1)
    work_rows = []
    for stages in [1, 2, 4, 8, 16, 64]:
        work = sum(mean_energy(j / stages) for j in range(stages)) / stages - e1
        excess = work - d_relative
        upper = (e0 - e1) / stages
        assert excess >= -2e-12
        assert excess <= upper + 2e-12
        work_rows.append({"stages": stages, "mean_ideal_cycle_work": work,
                          "excess_over_relative_entropy": excess,
                          "proved_excess_upper": upper})
    return {
        "M": m, "H": h, "weights": [str(w) for w in weights],
        "hidden_class": hidden, "anchored": anchored,
        "states": len(states), "marked_transitions": edge_count,
        "exact_detailed_balance": True, "exact_stationarity": True,
        "exact_marked_currents_zero": True,
        "max_motion_energy_residual": energy_residual,
        "relative_entropy": d_relative,
        "quench_formation_mean_force_work": e0 - e1,
        "finite_step_work": work_rows,
    }


def negbin_probabilities(shape, rho, maximum):
    p = [0.0] * (maximum + 1)
    p[0] = rho ** shape
    w = 1 - rho
    for k in range(maximum):
        p[k + 1] = p[k] * (k + shape) * w / (k + 1)
    return p


def entropy_bernoulli(rho):
    return -rho * math.log(rho) - (1 - rho) * math.log(1 - rho)


def three_band_case(scale):
    # Three groups contain 2L particles each. Their desired lengths are
    # 3L, 4L, 6L and their target densities are 2/3, 1/2, 1/3.
    shape = 2 * scale
    m, h, n = 6 * scale, 7 * scale, 13 * scale
    rhos = [2 / 3, 1 / 2, 1 / 3]
    ps = [negbin_probabilities(shape, rho, h) for rho in rhos]
    total = 0.0
    first_moments = [0.0, 0.0, 0.0]
    for a in range(h + 1):
        for b in range(h - a + 1):
            c = h - a - b
            mass = ps[0][a] * ps[1][b] * ps[2][c]
            total += mass
            first_moments[0] += a * mass
            first_moments[1] += b * mass
            first_moments[2] += c * mass
    means = [x / total for x in first_moments]
    assert abs(sum(means) - h) < 1e-8
    log_z = math.log(total) - shape * sum(math.log(r) for r in rhos)
    entropy = log_z - sum(mu * math.log(1 - rho)
                          for mu, rho in zip(means, rhos))
    log_count = math.lgamma(n) - math.lgamma(m) - math.lgamma(h + 1)
    relative_entropy = log_count - entropy
    target_rate = entropy_bernoulli(6 / 13) - sum(
        ell * entropy_bernoulli(rho)
        for ell, rho in zip([3 / 13, 4 / 13, 6 / 13], rhos))
    return {
        "scale": scale, "N": n, "M": m,
        "conditioning_probability": total,
        "canonical_mean_block_holes": means,
        "canonical_mean_block_lengths": [shape + x for x in means],
        "target_block_lengths": [3 * scale, 4 * scale, 6 * scale],
        "relative_entropy_per_length": relative_entropy / n,
        "proved_thermodynamic_limit": target_rate,
        "absolute_rate_error": abs(relative_entropy / n - target_rate),
    }


def main():
    cases = []
    for m in range(2, 6):
        for h in range(1, 5):
            weights = [F(1, 4), F(1, 2), F(3, 4)]
            w = [weights[i % 3] for i in range(m)]
            for hidden, anchored in [(0, True), (7, False)]:
                cases.append(exact_case(m, h, w, hidden, anchored))
    cases.append(exact_case(5, 4, [F(1, 2)] * 5, 3, True))
    macro = [three_band_case(scale) for scale in [1, 2, 4, 8, 16, 32, 64, 128]]
    assert macro[-1]["absolute_rate_error"] < macro[0]["absolute_rate_error"]
    root = Path(__file__).resolve().parent
    proof = root / "SPARSE_INTERNAL_LOADS_PREPARE_NATIVE_PROFILES.md"
    result = {
        "scope": "Exact/population model checks, not acquisition or device tests.",
        "code_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "proof_sha256": hashlib.sha256(proof.read_bytes()).hexdigest(),
        "finite_cases": len(cases),
        "total_states_checked": sum(c["states"] for c in cases),
        "total_marked_transitions_checked": sum(c["marked_transitions"] for c in cases),
        "max_motion_energy_residual": max(c["max_motion_energy_residual"] for c in cases),
        "all_rational_balance_and_marked_current_residuals": "exactly zero",
        "four_band_lattice_free_energy_per_length":
            0.75 * math.log(1.5) + 0.25 * math.log(0.5),
        "four_band_rod_free_energy_per_length": math.log(3) / 4,
        "finite_results": cases,
        "three_band_canonical_convergence": macro,
        "not_tested": [
            "The continuous Poincare theorem is proved analytically, not inferred from this code.",
            "No mixing time, physical force delivery, prepared hidden state or detector was acquired.",
            "No apparatus cost or historical novelty is inferred from a model calculation.",
        ],
    }
    output = root / "SPARSE_LOADS_CHECK.json"
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items()
                      if k not in {"finite_results"}}, indent=2))


if __name__ == "__main__":
    main()
