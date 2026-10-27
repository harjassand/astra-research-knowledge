"""Independent source equations and exact verification of the certificates.

Small controls enumerate every state, construct BACKWARD H independently,
and solve killed Dirichlet and pinned Poisson equations using Fraction.
The 64-site control reconstructs graph-ball powers by row evaluation at
predetermined Hamming balls, independently of the certificate's spreading
operator and detailed-balance weight propagation.
"""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import argparse
import json
import math
import resource
import platform
import sys
import time

sys.dont_write_bytecode = True
from nonproduct_certificate import certify, box, unbox


def graph_source(width, height, periodic):
    """Direct coordinate adjacency and Gibbs weights, no production helpers."""
    n = width * height
    adjacency = [[] for _ in range(n)]
    for i in range(n):
        yi, xi = divmod(i, width)
        for j in range(n):
            if i == j:
                continue
            yj, xj = divmod(j, width)
            dx, dy = abs(xi - xj), abs(yi - yj)
            if periodic:
                dx, dy = min(dx, width - dx), min(dy, height - dy)
            if dx + dy == 1:
                adjacency[i].append(j)
    edges = [(i, j) for i in range(n) for j in adjacency[i] if i < j]
    return n, adjacency, edges


def source_rate(x, i, adjacency):
    k = sum((x >> j) & 1 for j in adjacency[i])
    ratio = F(1, 4) * F(9, 8)**k
    return (1 if x >> i & 1 else ratio) / (1 + ratio)


def source_weight(x, edges):
    n = x.bit_count()
    e = sum(((x >> i) & 1) * ((x >> j) & 1) for i, j in edges)
    return F(1, 4)**n * F(9, 8)**e


def dense_solve(matrix, rhs):
    """Independent forward elimination and back substitution."""
    a = [[F(x) for x in row] for row in matrix]
    b = list(map(F, rhs))
    n = len(b)
    for k in range(n):
        pivot = next(i for i in range(k, n) if a[i][k])
        a[k], a[pivot] = a[pivot], a[k]
        b[k], b[pivot] = b[pivot], b[k]
        for i in range(k + 1, n):
            if not a[i][k]:
                continue
            factor = a[i][k] / a[k][k]
            a[i][k] = F(0)
            for j in range(k + 1, n):
                a[i][j] -= factor * a[k][j]
            b[i] -= factor * b[k]
    x = [F(0)] * n
    for i in reversed(range(n)):
        x[i] = (b[i] - sum(a[i][j] * x[j]
                            for j in range(i + 1, n))) / a[i][i]
    assert all(sum(F(v) * xx for v, xx in zip(row, x)) == target
               for row, target in zip(matrix, rhs))
    return x


def dense_control(width, height, periodic=False):
    started = time.perf_counter()
    n, adj, edges = graph_source(width, height, periodic)
    m, a, b = 1 << n, 0, (1 << n) - 1
    H = [[F(0)] * m for _ in range(m)]
    weights = [source_weight(x, edges) for x in range(m)]
    for x in range(m):
        for i in range(n):
            y = x ^ (1 << i)
            q = source_rate(x, i, adj)
            H[x][x] += q
            H[x][y] -= q
    assert all(sum(row) == 0 for row in H)
    assert all(weights[x] * H[x][y] == weights[y] * H[y][x]
               for x in range(m) for y in range(m))
    rho = weights[b]
    u = [rho if x == a else -F(1) if x == b else F(0) for x in range(m)]
    assert sum(w * z for w, z in zip(weights, u)) == 0

    # Dirichlet h(a)=0,h(b)=1 and Hh=0 on the interior.
    interior = list(range(1, b))
    killed = [[H[x][y] for y in interior] for x in interior]
    h = [F(0)] + dense_solve(killed, [-H[x][b] for x in interior]) + [F(1)]
    assert all(sum(H[x][y] * h[y] for y in range(m)) == 0 for x in interior)
    R_a = H[a][a]
    p = sum(-H[a][y] * h[y] for y in range(1, m)) / R_a

    # Gauge f(a)=0. The missing a equation follows from stationarity.
    poisson = [[H[x][y] for y in range(1, m)] for x in range(1, m)]
    f = [F(0)] + dense_solve(poisson, u[1:])
    assert all(sum(H[x][y] * f[y] for y in range(m)) == u[x]
               for x in range(m))
    I = sum(w * z * v for w, z, v in zip(weights, u, f)) / rho
    assert I == -f[b]
    assert p == rho / (R_a * I)

    result, (op, vectors, gram, alpha) = certify(
        width, height, periodic, max_degree=3, epsilon=F(1, 10**12),
        return_internal=True)
    assert rho == op.rho and R_a == op.Ra
    assert all(op.direct_weight(x) == op.B * weights[x] for x in range(m))
    # Every integer power is checked against independent full H rows.
    for k in range(1, len(vectors)):
        previous = vectors[k - 1]
        for x in range(m):
            expected = sum(H[x][y] * previous.get(y, 0) * op.D
                           for y in range(m))
            assert expected == vectors[k].get(x, 0)
    degrees = []
    for record in result["degrees"]:
        k = record["degree"]
        coefficients = [unbox(v) for v in record["coefficient_alpha"]]
        y = [F(op.D, op.B) * sum(coefficients[j] * vectors[j].get(x, 0)
                                 for j in range(k)) for x in range(m)]
        Hy = [sum(H[x][z] * y[z] for z in range(m)) for x in range(m)]
        residual = [u[x] - Hy[x] for x in range(m)]
        residual_mean = sum(w * r for w, r in zip(weights, residual))
        assert residual_mean == 0
        direct_L = sum(w * (2 * uu * yy - yy * hh)
                       for w, uu, yy, hh in zip(weights, u, y, Hy)) / rho
        direct_error = sum(w * r * r for w, r in zip(weights, residual)) / (rho * op.gap)
        assert direct_L == unbox(record["raw_Galerkin_lower"])
        assert direct_L + direct_error == unbox(record["raw_residual_upper"])
        assert unbox(record["I_lower"]) <= I <= unbox(record["I_upper"])
        assert unbox(record["p_lower"]) <= p <= unbox(record["p_upper"])
        # Independent completion-of-square check with exact Poisson solution.
        err = [f[x] - y[x] for x in range(m)]
        energy_error = sum(weights[x] * err[x] * sum(H[x][z] * err[z]
                           for z in range(m)) for x in range(m)) / rho
        assert I - direct_L == energy_error
        degrees.append({"degree": k, "explicit_full_residual_match": True,
                        "completion_of_square_match": True,
                        "p_and_I_contained": True,
                        "I_lower": record["I_lower"], "I_upper": record["I_upper"]})
    return {"width": width, "height": height, "periodic": periodic,
            "states_enumerated_for_control": m, "sites": n, "edges": len(edges),
            "exact_dirichlet_p": box(p), "exact_pinned_poisson_I": box(I),
            "potential_identity_exact": True, "detailed_balance_exact": True,
            "full_backward_powers_exact": True, "degrees": degrees,
            "elapsed_seconds": time.perf_counter() - started}


def masks_of_size(n, size):
    for positions in combinations(range(n), size):
        yield sum(1 << i for i in positions)


def verify_64():
    started = time.perf_counter()
    result, (op, vectors, gram, alpha) = certify(return_internal=True)
    n, adj, edges = graph_source(8, 8, True)
    assert n == 64 and len(edges) == 128
    assert tuple(edges) == op.edges
    neighbor_masks = [sum(1 << j for j in row) for row in adj]
    # Derive the integer rates independently; do not use op's rate table.
    denominators = [4 * 8**k + 9**k for k in range(5)]
    D = math.lcm(*denominators)
    rate = [[D * 9**k // denominators[k] for k in range(5)],
            [D * 4 * 8**k // denominators[k] for k in range(5)]]
    assert D == op.D and op.B == 2**512
    reference = {0: 9**128, (1 << n) - 1: -(2**512)}
    power_checks = []
    for degree in range(1, 4):
        candidates = set()
        for size in range(degree + 1):
            for x in masks_of_size(n, size):
                candidates.add(x)
                candidates.add(x ^ op.b)
        current = {}
        for x in candidates:
            center_value = reference.get(x, 0)
            diagonal = 0
            off_diagonal = 0
            for i, neighbor_mask in enumerate(neighbor_masks):
                adjacent_value = reference.get(x ^ (1 << i), 0)
                if center_value or adjacent_value:
                    occupied = (x >> i) & 1
                    context = (x & neighbor_mask).bit_count()
                    q = rate[occupied][context]
                    if center_value:
                        diagonal += q
                    off_diagonal += q * adjacent_value
            value = diagonal * center_value - off_diagonal
            if value:
                current[x] = value
        assert current == vectors[degree]
        power_checks.append({"degree": degree, "candidate_states": len(candidates),
                             "nonzeros": len(current), "full_row_power_exact": True})
        reference = current
    # Independently evaluate the Gibbs weight by direct occupied-edge counts.
    independent_weights = {}
    edge_masks = [(1 << i) | (1 << j) for i, j in edges]
    for x in vectors[-1]:
        e = sum(x & mask == mask for mask in edge_masks)
        weight = (2**(512 - 2 * x.bit_count() - 3 * e)) * 9**e
        assert weight == op.weights[x]
        independent_weights[x] = weight
    independent_gram = [[sum(independent_weights[x] * v * w.get(x, 0)
                              for x, v in vector.items())
                         for w in vectors] for vector in vectors]
    assert independent_gram == gram
    return {"sites": n, "edges": len(edges), "full_source_states_enumerated": False,
            "power_checks": power_checks,
            "direct_gibbs_weights_checked": len(independent_weights),
            "all_moments_match_independent_weights": True,
            "p_lower": result["p_lower"], "p_upper": result["p_upper"],
            "elapsed_seconds": time.perf_counter() - started}


def structural_checks():
    n, adjacency, edges = graph_source(8, 8, True)
    i, j = 0, 1
    cross_ratio = (source_weight((1 << i) | (1 << j), edges) *
                   source_weight(0, edges) /
                   (source_weight(1 << i, edges) * source_weight(1 << j, edges)))
    assert cross_ratio == F(9, 8) and cross_ratio != 1
    adjacent = (1 << 0) | (1 << 1)
    separated = (1 << 0) | (1 << 36)
    loss_adjacent = sum((source_rate(adjacent, i, adjacency)
                         for i in range(n) if adjacent >> i & 1), F(0))
    loss_separated = sum((source_rate(separated, i, adjacency)
                          for i in range(n) if separated >> i & 1), F(0))
    assert adjacent.bit_count() == separated.bit_count() == 2
    assert loss_adjacent == F(64, 41) and loss_separated == F(8, 5)
    assert loss_adjacent != loss_separated

    def count_edges(x):
        return x.bit_count(), sum(((x >> i) & 1) * ((x >> j) & 1)
                                  for i, j in edges)

    line = (1 << 0) | (1 << 1) | (1 << 2)
    corner = (1 << 0) | (1 << 1) | (1 << 8)
    assert count_edges(line) == count_edges(corner) == (3, 2)
    rate_line = sum((source_rate(line, i, adjacency) for i in range(n)
                     if count_edges(line ^ (1 << i)) == (4, 4)), F(0))
    rate_corner = sum((source_rate(corner, i, adjacency) for i in range(n)
                       if count_edges(corner ^ (1 << i)) == (4, 4)), F(0))
    assert rate_line == 0 and rate_corner == F(81, 337)
    p = [F(9**k, 4 * 8**k + 9**k) for k in range(5)]
    nonlinear_difference = p[2] - 2 * p[1] + p[0]
    assert nonlinear_difference != 0
    return {"adjacent_conditional_cross_ratio": box(cross_ratio),
            "nonproduct_proved": True,
            "occupied_count_lumpability_counterexample": {
                "common_count": 2, "target_count": 1,
                "adjacent_rate": box(loss_adjacent),
                "separated_rate": box(loss_separated)},
            "count_and_edges_lumpability_counterexample": {
                "common_counts": [3, 2], "target_counts": [4, 4],
                "line_rate": box(rate_line), "L_shape_rate": box(rate_corner)},
            "birth_rate_second_difference": box(nonlinear_difference),
            "scope": "Natural site-bit product and count/count-plus-edge lumpings are excluded. No claim to exclude every possible hidden representation."}


def ordinary_mc_bound():
    """Analytic sample/event upper bound; no Monte Carlo is executed here."""
    rho = F(9**128, 2**512)
    p = [F(9**k, 4 * 8**k + 9**k) for k in range(5)]
    gap = 1 - 4 * max(p[k + 1] - p[k] for k in range(4))
    Rstar, T, eta, delta = 64, F(15), F(1, 4000), F(1, 20)
    mu = (1 + rho) / (2 * Rstar)
    # Lower Taylor polynomial proves exp(gap*T) >= required reciprocal tail.
    exp_lower = sum(((gap * T)**j / math.factorial(j) for j in range(65)), F(0))
    assert exp_lower >= (1 + rho) / (eta * mu * gap)
    # exp(4)>40 proves log(2/delta)=log(40)<4.
    assert sum((F(4)**j / math.factorial(j) for j in range(13)), F(0)) > 40
    bound = (1 + 3 * rho)**2 * T**2 * 4 / (2 * eta**2 * mu**2)
    samples = (bound.numerator + bound.denominator - 1) // bound.denominator
    return {"executed": False, "kind": "conservative analytic Hoeffding bound",
            "epsilon_requested": "1/1000", "delta": str(delta),
            "eta": str(eta), "mu_lower": box(mu), "T": str(T),
            "tail_bound_verified_by_exact_Taylor_lower_polynomial": True,
            "log_40_less_than_4_verified_by_exact_Taylor_lower_polynomial": True,
            "independent_replicates_sufficient": samples,
            "exact_law_trajectories_per_replicate": 2,
            "expected_uniformisation_events_upper": 2 * samples * Rstar * int(T),
            "relative_interval_width_on_success_at_most": str(3 * eta),
            "scope": "Same exact source, rho, positive gap and exact-law simulation promises. Polynomial sample/event bound has no 1/p; it is not a timing benchmark, optimal cost, implementation, or finite-bit simulation theorem."}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="INDEPENDENT_CHECKS.json")
    args = parser.parse_args()
    started = time.perf_counter()
    controls = []
    for dims in ((2, 2), (2, 3)):
        control = dense_control(*dims)
        controls.append(control)
        print("full-state", dims, "p", control["exact_dirichlet_p"]["approx"],
              "I", control["exact_pinned_poisson_I"]["approx"], "seconds",
              control["elapsed_seconds"], flush=True)
    large = verify_64()
    print("independent 64-site row and weight checks passed; seconds",
          large["elapsed_seconds"], flush=True)
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    out = {"status": "ALL_EXACT_CHECKS_PASS", "small_full_state_controls": controls,
           "independent_64_site_source_check": large,
           "structural_checks": structural_checks(),
           "ordinary_mc_analytic_comparator": ordinary_mc_bound(),
           "elapsed_seconds": time.perf_counter() - started,
           "peak_process_RSS_bytes": rss if platform.system() == "Darwin" else 1024 * rss}
    Path(args.output).write_text(json.dumps(out, indent=2) + "\n")
