"""Acquire latent binary variables from noisy scalar energy experiments.

No true partition, rank, graph, or full matrix is passed to the learner. It
proposes partitions spectrally, verifies their contraction with exact rational
certificates, and compiles an exact finite coarse-forest executor. Full acquired
data are returned separately for a same-information conventional baseline.
"""

from __future__ import annotations

import itertools
import json
import math
from fractions import Fraction
from pathlib import Path

import numpy as np


def as_fraction(value):
    if isinstance(value, Fraction):
        return value
    if isinstance(value, (int, np.integer)):
        return Fraction(int(value))
    if isinstance(value, (float, np.floating)):
        return Fraction.from_float(float(value))
    return Fraction(value)


def fraction_string(value):
    return str(value) if value is not None else None


def nearest_units(value, denominator):
    q = as_fraction(value)*denominator
    floor, remainder = divmod(q.numerator, q.denominator)
    if 2*remainder > q.denominator or (2*remainder == q.denominator and floor % 2):
        floor += 1
    return int(floor)


class ScalarQuadraticExperiment:
    def __init__(self, A, b, offset=1000., sigma=5.e-6, seed=1):
        self._A = np.asarray(A, dtype=float)
        self._b = np.asarray(b, dtype=float)
        self._offset = float(offset)
        self.n = len(b)
        self.sigma = float(sigma)
        self.rng = np.random.default_rng(seed)
        self.last = None
        self.energy_shots = 0
        self.prepared_batches = 0
        self.control_bit_changes = 0
        self.configuration_bits_written = 0
        self.raw_readout_bits = 0
        self.maximum_report_magnitude = 0.

    def measure(self, configuration, shots=1):
        x = np.asarray(configuration, dtype=np.int8)
        if x.shape != (self.n,):
            raise ValueError("Wrong prepared configuration size")
        self.control_bit_changes += (self.n if self.last is None
                                     else int(np.count_nonzero(x != self.last)))
        self.last = x.copy()
        self.energy_shots += shots
        self.prepared_batches += 1
        self.configuration_bits_written += self.n
        self.raw_readout_bits += 64*shots
        mean = self._offset+self._b@x+.5*x@self._A@x
        # All charged source noise draws are actually made.
        report = float(mean+self.rng.normal(0., self.sigma, shots).mean())
        self.maximum_report_magnitude = max(self.maximum_report_magnitude, abs(report))
        return report

    def measure_many(self, configurations, repetitions=1):
        """Explicitly prepare every requested row; return its replicate mean."""
        return np.asarray([self.measure(x, shots=repetitions) for x in configurations])

    def costs(self):
        return {"energy_shots": self.energy_shots, "prepared_batches": self.prepared_batches,
                "control_bit_changes": self.control_bit_changes,
                "configuration_bits_written": self.configuration_bits_written,
                "raw_readout_bits": self.raw_readout_bits,
                "maximum_report_magnitude": self.maximum_report_magnitude}


def scalar_tomography(experiment, n, coefficient_radius, grid_bits=30,
                      failure=.01, readout_radius=Fraction(1, 10**9)):
    """Every coefficient uses four NEW readout batches; no shared oracle data."""
    denominator = 1 << grid_bits
    a = as_fraction(coefficient_radius)
    rho = as_fraction(readout_radius)
    statistical_radius = a-rho-Fraction(1, 2*denominator)
    if statistical_radius <= 0:
        raise ValueError("Requested radius is below readout/quantization resolution")
    number = n*(n-1)//2+n
    shots = max(1, math.ceil(experiment.sigma**2/(2*float(statistical_radius)**2)
                             * math.log(2*number/failure)))
    plus = np.ones(n, dtype=np.int8)
    minus = -plus
    A = [[0 for _ in range(n)] for _ in range(n)]
    b = []
    for i in range(n):
        one_plus = plus.copy()
        one_plus[i] = -1
        one_minus = minus.copy()
        one_minus[i] = +1
        ep = as_fraction(experiment.measure(plus, shots))
        epi = as_fraction(experiment.measure(one_plus, shots))
        emi = as_fraction(experiment.measure(one_minus, shots))
        em = as_fraction(experiment.measure(minus, shots))
        b.append(nearest_units((ep-epi+emi-em)/4, denominator))
    for i in range(n):
        for j in range(i+1, n):
            one_i, one_j, both = plus.copy(), plus.copy(), plus.copy()
            one_i[i] = -1
            one_j[j] = -1
            both[i] = both[j] = -1
            ep = as_fraction(experiment.measure(plus, shots))
            ei = as_fraction(experiment.measure(one_i, shots))
            ej = as_fraction(experiment.measure(one_j, shots))
            eij = as_fraction(experiment.measure(both, shots))
            units = nearest_units((ep-ei-ej+eij)/4, denominator)
            A[i][j] = A[j][i] = units
    for i in range(n):
        A[i][i] = -sum(A[i][j] for j in range(n) if j != i)
    full = {"A_units": A, "b_units": b, "denominator": denominator,
            "coefficient_radius": str(a), "confidence_failure": failure,
            "readout_radius": str(rho), "grid_bits": grid_bits}
    record = {"coefficient_count": number, "fresh_batches_per_coefficient": 4,
              "shots_per_batch": shots, "coefficient_radius": str(a),
              "statistical_radius": str(statistical_radius),
              "readout_radius": str(rho), "grid_bits": grid_bits,
              "confidence_failure": failure,
              "matrix_operator_error_bound": str(2*(n-1)*a),
              "objective_oscillation_error_bound": str(2*n*n*a),
              "source_precision_status": "Floating Gaussian simulation; the stated absolute readout radius is an instrument assumption, not established by this simulator",
              "source": experiment.costs()}
    return full, record


def rational_positive_definite(matrix):
    """Exact unpivoted Fraction LDL. Only strictly positive pivots accept."""
    size = len(matrix)
    L = [[Fraction(0) for _ in range(size)] for _ in range(size)]
    pivots = []
    max_num = max_den = 1
    products = 0

    def account(value):
        nonlocal max_num, max_den
        max_num = max(max_num, abs(value.numerator).bit_length())
        max_den = max(max_den, value.denominator.bit_length())

    for j in range(size):
        pivot = as_fraction(matrix[j][j])
        for h in range(j):
            pivot -= L[j][h]*L[j][h]*pivots[h]
            products += 2
        account(pivot)
        if pivot <= 0:
            return False, {"dimension": size, "failed_pivot_index": j,
                           "failed_pivot": str(pivot), "max_numerator_bits": max_num,
                           "max_denominator_bits": max_den, "rational_products": products}
        pivots.append(pivot)
        L[j][j] = 1
        for i in range(j+1, size):
            value = as_fraction(matrix[i][j])
            for h in range(j):
                value -= L[i][h]*L[j][h]*pivots[h]
                products += 2
            value /= pivot
            account(value)
            L[i][j] = value
    return True, {"dimension": size, "positive_pivot_count": size,
                  "minimum_pivot": str(min(pivots)) if pivots else None,
                  "max_numerator_bits": max_num, "max_denominator_bits": max_den,
                  "rational_products": products}


def canonical_partition(labels):
    mapping = {}
    result = []
    for value in labels:
        if value not in mapping:
            mapping[value] = len(mapping)
        result.append(mapping[value])
    return result


def row_clusters(coordinates, threshold):
    n = len(coordinates)
    parent = list(range(n))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    for i in range(n):
        for j in range(i+1, n):
            if np.linalg.norm(coordinates[i]-coordinates[j]) <= threshold:
                aa, bb = find(i), find(j)
                parent[bb] = aa
    return canonical_partition([find(i) for i in range(n)])


def coarse_data(A, b, labels):
    r = max(labels)+1
    clusters = [[i for i, a in enumerate(labels) if a == group] for group in range(r)]
    sizes = [len(c) for c in clusters]
    T = [[sum(A[i][j] for i in cluster) for j in range(len(A))] for cluster in clusters]
    C = [[sum(T[a][j] for j in clusters[c]) for c in range(r)] for a in range(r)]
    coarse_b = [sum(b[i] for i in cluster) for cluster in clusters]
    return clusters, sizes, T, C, coarse_b


def forest_from_integer_coarse(C):
    r = len(C)
    parent = list(range(r))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    edges = []
    selected = set()
    candidates = sorted(((abs(C[a][b]), a, b) for a in range(r) for b in range(a+1, r)),
                        reverse=True)
    for absolute, a, b in candidates:
        aa, bb = find(a), find(b)
        if aa != bb:
            parent[bb] = aa
            selected.add((a, b))
            if C[a][b]:
                edges.append((a, b, C[a][b]))
    dropped = sum(abs(C[a][b]) for a in range(r) for b in range(a+1, r)
                  if (a, b) not in selected)
    return edges, dropped


def square_root_upper(value, bits=40):
    """An exact rational upper bound; no floating square-root decision."""
    value = as_fraction(value)
    if value < 0:
        raise ValueError("Square-root argument must be nonnegative")
    scale = 1 << bits
    scaled_numerator = value.numerator*scale*scale
    ceiling = (scaled_numerator+value.denominator-1)//value.denominator
    units = math.isqrt(ceiling)
    if units*units < ceiling:
        units += 1
    answer = Fraction(units, scale)
    assert answer*answer >= value
    return answer


def certify_partition(full, labels, H, epsilon_per_site,
                      source_regret_bound=None, confidence_failure=None):
    A, b, denominator = full["A_units"], full["b_units"], full["denominator"]
    n = len(A)
    labels = canonical_partition(labels)
    clusters, sizes, T, C, coarse_b = coarse_data(A, b, labels)
    r = len(clusters)
    H = as_fraction(H)
    alpha = max(Fraction(max(0, C[group][group])
                         +sum(abs(C[group][other]) for other in range(r) if other != group),
                         denominator*sizes[group]) for group in range(r))
    beta = max(Fraction(abs(value), denominator) for value in b)+H
    forest, dropped_units = forest_from_integer_coarse(C)
    coarse_tail = Fraction(2*dropped_units, denominator)
    if source_regret_bound is None:
        source_regret_bound = full.get("source_regret_bound")
    if source_regret_bound is None:
        source_regret_bound = 2*n*n*Fraction(full["coefficient_radius"])
    calibration = as_fraction(source_regret_bound)
    if confidence_failure is None:
        confidence_failure = full.get("confidence_failure", .01)
    record = {"groups": r, "sizes": sizes, "labels": labels,
              "alpha": str(alpha), "alpha_method": "positive_coarse_diagonal_plus_offdiagonal_absolute_rows",
              "beta": str(beta),
              "calibration_oscillation": str(calibration),
              "coarse_dropped_edge_oscillation": str(coarse_tail)}
    if r == n:
        record.update({"alignment": "singleton_partition", "gamma": None,
                       "gap": None, "exact_alignment": True,
                       "contraction_loss": "0", "cross_bound_squared": "0"})
        contraction = Fraction(0)
    else:
        # Integer spanning columns e_i-e_anchor. QR/eigenvalues propose gamma;
        # the exact rational LDL alone authorizes the transverse lower bound.
        normal_pairs = [(i, cluster[0]) for cluster in clusters for i in cluster[1:]]
        B = np.zeros((n, len(normal_pairs)))
        for j, (i, anchor) in enumerate(normal_pairs):
            B[i, j], B[anchor, j] = 1., -1.
        orthogonal, _ = np.linalg.qr(B, mode="reduced")
        numeric_A = np.asarray(A, dtype=float)/denominator
        minimum = float(np.linalg.eigvalsh(orthogonal.T@numeric_A@orthogonal)[0])
        record["numeric_proposed_normal_eigenvalue"] = minimum
        # A deliberately interior rational proposal. Gamma and the subsequent
        # gap may be NEGATIVE: approximate contraction has no positivity floor.
        interior = minimum-max(.05*abs(minimum), 1/1024)
        gamma = Fraction(math.floor(interior*1024), 1024)
        normal_verified = False
        normal_attempts = []
        for attempt in range(8):
            M = []
            for i, anchor_i in normal_pairs:
                row = []
                for j, anchor_j in normal_pairs:
                    gram = int(i == j)-int(i == anchor_j)-int(anchor_i == j)+int(anchor_i == anchor_j)
                    entry = Fraction(A[i][j]-A[i][anchor_j]-A[anchor_i][j]+A[anchor_i][anchor_j], denominator)
                    row.append(entry-gamma*gram)
                M.append(row)
            normal_verified, normal_work = rational_positive_definite(M)
            normal_attempts.append({"gamma": str(gamma), **normal_work})
            if normal_verified:
                break
            gamma -= max(Fraction(1), abs(gamma))
        record["normal_LDL"] = normal_work
        record["normal_LDL_attempts"] = normal_attempts
        if not normal_verified:
            record["rejection"] = "Exact transverse LDL rejected every proposal"
            return None, record
        gap = gamma-2*alpha-2*beta
        record.update({"gamma": str(gamma), "gap": str(gap)})
        # G=P^T A(I-W)A P, formed exactly using integer acquired coefficients.
        G = [[Fraction(sum(T[a][j]*T[c][j] for j in range(n)), denominator**2)
              -sum((Fraction(C[a][h]*C[c][h], denominator**2*sizes[h]) for h in range(r)),
                   Fraction(0)) for c in range(r)] for a in range(r)]
        frobenius_squared = sum((G[a][a]/sizes[a] for a in range(r)), Fraction(0))
        if frobenius_squared < 0:
            raise ArithmeticError("Exact cross-Gram computation has a negative squared norm")
        if all(value == 0 for row in G for value in row):
            operator_upper = Fraction(0)
            cross_work = {"dimension": r, "exact_zero_Gram": True}
            cross_attempts = []
        else:
            numeric_G = np.array([[float(value) for value in row] for row in G])
            root_sizes = np.sqrt(np.asarray(sizes))
            eigenvalue = float(np.linalg.eigvalsh(numeric_G/root_sizes[:, None]/root_sizes[None, :])[-1])
            if eigenvalue <= 0:
                operator_upper = frobenius_squared
            else:
                exponent = math.floor(math.log2(eigenvalue))+1
                operator_upper = Fraction(2**exponent) if exponent >= 0 else Fraction(1, 2**(-exponent))
            cross_attempts = []
            for attempt in range(64):
                upper_matrix = [[(operator_upper*sizes[a] if a == c else 0)-G[a][c]
                                 for c in range(r)] for a in range(r)]
                ok, cross_work = rational_positive_definite(upper_matrix)
                cross_attempts.append({"operator_squared_proposal": str(operator_upper), **cross_work})
                if ok:
                    break
                operator_upper *= 2
            else:
                raise ArithmeticError("Could not certify a finite cross-Gram upper bound")
        d2 = min(frobenius_squared, operator_upper)
        exact_alignment = gap > 0 and gap*gap > 4*n*d2
        root_upper = square_root_upper(gap*gap+4*d2)
        continuous_loss = n*(root_upper-gap)/4
        # For psi=2*Lambda/n this is the exact 2x2 PSD certificate. It
        # authorizes the full continuous bound without a square-root oracle.
        psi = 2*continuous_loss/n
        assert psi >= 0 and gap+psi >= 0 and psi*(gap+psi) >= d2
        contraction = Fraction(0) if exact_alignment else continuous_loss
        record.update({"cross_Frobenius_squared": str(frobenius_squared),
                       "cross_operator_squared_upper": str(operator_upper),
                       "cross_bound_squared": str(d2), "cross_LDL": cross_work,
                       "cross_LDL_attempts": cross_attempts,
                       "exact_alignment": exact_alignment,
                       "continuous_contraction_upper": str(continuous_loss),
                       "continuous_2x2_PSD_verified": True,
                       "contraction_loss": str(contraction),
                       "alignment": "exact" if exact_alignment else "approximate"})
    total = calibration+coarse_tail+contraction
    budget = as_fraction(epsilon_per_site)*n
    accepted = total <= budget
    record.update({"regret_bound": str(total), "regret_bound_float": float(total),
                   "requested_regret": str(budget), "accepted": accepted,
                   "coarse_forest_edges": len(forest)})
    if not accepted:
        record["rejection"] = "Total operation regret exceeds requested accuracy"
        return None, record
    service = LatentForestDesign(labels, coarse_b, forest, denominator, H, total,
                                 confidence_failure)
    return service, record


class LatentForestDesign:
    def __init__(self, labels, coarse_b_units, forest, denominator, H, regret_bound, failure):
        self.labels = list(labels)
        self.n = len(labels)
        self.r = len(coarse_b_units)
        self.coarse_b_units = list(coarse_b_units)
        self.forest = list(forest)
        self.denominator = denominator
        self.H = as_fraction(H)
        self.regret_bound = as_fraction(regret_bound)
        self.failure = failure
        adjacency = [[] for _ in range(self.r)]
        for a, b, weight in forest:
            adjacency[a].append((b, weight))
            adjacency[b].append((a, weight))
        self.children = [[] for _ in range(self.r)]
        self.roots, self.order = [], []
        parent = {}
        for root in range(self.r):
            if root in parent:
                continue
            self.roots.append(root)
            parent[root] = None
            stack = [root]
            while stack:
                a = stack.pop()
                self.order.append(a)
                for b, weight in adjacency[a]:
                    if b == parent[a]:
                        continue
                    if b in parent:
                        raise ValueError("Compiled graph is not a forest")
                    parent[b] = a
                    self.children[a].append((b, weight))
                    stack.append(b)

    def solve(self, fields):
        if len(fields) != self.n:
            raise ValueError("Wrong number of site fields")
        h = [as_fraction(value) for value in fields]
        if any(abs(value) > self.H for value in h):
            raise ValueError("Query exceeds the experimentally certified field box")
        scale = self.denominator
        for value in h:
            scale = math.lcm(scale, value.denominator)
        multiplier = scale//self.denominator
        coarse = [value*multiplier for value in self.coarse_b_units]
        for i, value in enumerate(h):
            coarse[self.labels[i]] += value.numerator*(scale//value.denominator)
        dp, choices = {}, {}
        comparisons = 0
        for a in reversed(self.order):
            for z in (-1, 1):
                value = coarse[a]*z
                for b, weight in self.children[a]:
                    minus = dp[b, -1]-weight*multiplier*z
                    plus = dp[b, 1]+weight*multiplier*z
                    chosen = -1 if minus <= plus else 1
                    choices[a, z, b] = chosen
                    value += minus if chosen == -1 else plus
                    comparisons += 1
                dp[a, z] = value
        z_values = [0]*self.r
        stack = [(root, -1 if dp[root, -1] <= dp[root, 1] else 1) for root in self.roots]
        while stack:
            a, z = stack.pop()
            z_values[a] = z
            stack.extend((b, choices[a, z, b]) for b, _ in self.children[a])
        answer = np.asarray([z_values[a] for a in self.labels], dtype=np.int8)
        return answer, {"exact_integer_DP": True, "site_fields_consumed": self.n,
                         "coarse_variables": self.r, "integer_comparisons": comparisons,
                         "common_denominator_bits": scale.bit_length(),
                         "maximum_DP_integer_bits": max((abs(v).bit_length() for v in dp.values()), default=0),
                         "retained_labels": self.n,
                         "retained_scalar_coefficients": self.r+len(self.forest)}

    def compiled_energy(self, configuration, fields):
        x = np.asarray(configuration)
        representative = [next(i for i, a in enumerate(self.labels) if a == group) for group in range(self.r)]
        z = [int(x[i]) for i in representative]
        value = sum(Fraction(w*z[a], self.denominator) for a, w in enumerate(self.coarse_b_units))
        value += sum(Fraction(w*z[a]*z[b], self.denominator) for a, b, w in self.forest)
        value += sum((as_fraction(h)*int(v) for h, v in zip(fields, x)), Fraction(0))
        return value


def acquire_latent_design(experiment, n, H=Fraction(1, 5), epsilon_per_site=Fraction(1, 50),
                          coefficient_radius=None, grid_bits=30, failure=.01):
    if coefficient_radius is None:
        coefficient_radius = as_fraction(epsilon_per_site)/(16*n)
    full, acquisition = scalar_tomography(experiment, n, coefficient_radius, grid_bits, failure)
    service, compilation = compile_acquired(
        full, H, epsilon_per_site, acquisition["objective_oscillation_error_bound"], failure)
    record = {"acquisition": acquisition, **compilation}
    return service, record, full


def compile_acquired(full_model, H=Fraction(1, 5), epsilon_per_site=Fraction(1, 50),
                     source_regret_bound=None, confidence_failure=None):
    """Compile any paid acquisition's quadratic and uniform regret event.

    The bound is an oscillation/optimizer-regret bound, not a pointwise error:
    sup_x|E-Ehat|<=Delta supplies source_regret_bound=2*Delta. The complete
    learned matrix is used here but is not retained inside the returned service.
    """
    full = full_model
    n = len(full["b_units"])
    numeric_A = np.asarray(full["A_units"], dtype=float)/full["denominator"]
    _, eigenvectors = np.linalg.eigh(numeric_A)
    threshold_base = 1/(3*math.sqrt(n))
    attempts, proposals, seen = [], [], set()
    service = None
    accepted_record = None
    for proposed_r in range(1, n+1):
        for factor in (.5, 1., 2.):
            labels = row_clusters(eigenvectors[:, :proposed_r], factor*threshold_base)
            number = max(labels)+1
            proposals.append({"spectral_dimension": proposed_r, "threshold_factor": factor,
                              "resulting_group_count": number})
            key = tuple(labels)
            if number != proposed_r or key in seen:
                continue
            seen.add(key)
            candidate, certificate = certify_partition(
                full, labels, H, epsilon_per_site, source_regret_bound, confidence_failure)
            certificate["spectral_dimension"] = proposed_r
            certificate["threshold_factor"] = factor
            attempts.append(certificate)
            if candidate is not None:
                service, accepted_record = candidate, certificate
                break
        if service is not None:
            break
    record = {"proposal_log": proposals,
              "exact_certificate_attempts": attempts, "accepted_certificate": accepted_record,
              "status": "accepted" if service is not None else "no certified compact operation",
              "compilation_work": {
                  "numeric_symmetric_eigendecompositions": 1,
                  "spectral_proposals": len(proposals),
                  "row_distance_coordinate_visits": sum(
                      n*(n-1)//2*p["spectral_dimension"] for p in proposals),
                  "distinct_partition_certificates": len(attempts),
                  "exact_LDL_rational_products": sum(
                      work.get("rational_products", 0)
                      for attempt in attempts for name in ("normal_LDL_attempts", "cross_LDL_attempts")
                      for work in attempt.get(name, [])),
                  "max_exact_LDL_numerator_bits": max(
                      [work.get("max_numerator_bits", 0)
                       for attempt in attempts for name in ("normal_LDL_attempts", "cross_LDL_attempts")
                       for work in attempt.get(name, [])]+[0]),
                  "max_exact_LDL_denominator_bits": max(
                      [work.get("max_denominator_bits", 0)
                       for attempt in attempts for name in ("normal_LDL_attempts", "cross_LDL_attempts")
                       for work in attempt.get(name, [])]+[0]),
                  "full_acquired_model_retained_separately_for_baselines": True}}
    return service, record


def make_fixture(n, r, seed, transverse_scale=20., cross_amplitude=.3, generic_scale=.03):
    if n % r:
        raise ValueError("Fixture uses equal hidden cluster sizes")
    rng = np.random.default_rng(seed)
    labels = np.repeat(np.arange(r), n//r)
    rng.shuffle(labels)
    P = np.eye(r)[labels]
    D = np.diag(P.sum(axis=0))
    W = P@np.linalg.inv(D)@P.T
    normal = np.eye(n)-W
    random_G = rng.normal(size=(n, n))
    L = transverse_scale*normal@(np.eye(n)+random_G.T@random_G/n)@normal
    C = np.zeros((r, r))
    for b in range(1, r):
        a = int(rng.integers(b))
        C[a, b] = C[b, a] = rng.choice((-1, 1))*rng.uniform(.1, .3)
    S = np.linalg.inv(D)@P.T
    coarse = S.T@C@S
    u = W@rng.normal(size=n)
    u -= u.mean()
    u /= np.linalg.norm(u)
    v = normal@rng.normal(size=n)
    v /= np.linalg.norm(v)
    cross = cross_amplitude*(np.outer(u, v)+np.outer(v, u))
    perturb = rng.uniform(-1, 1, (n, n))
    perturb = generic_scale/n*(perturb+perturb.T)/2
    np.fill_diagonal(perturb, 0.)
    A = L+coarse+cross+perturb
    b = rng.uniform(-.05, .05, n)
    return A, b, labels.tolist(), L, {"transverse_scale": transverse_scale,
                                      "pure_cross_amplitude": cross_amplitude,
                                      "generic_entry_scale": generic_scale/n}


def true_energy(A, b, x, h):
    x = np.asarray(x, dtype=float)
    one = x.ndim == 1
    if one:
        x = x[None, :]
    result = x@(b+np.asarray(h))+.5*np.einsum("bi,ij,bj->b", x, A, x, optimize=True)
    return float(result[0]) if one else result


def verify_fixture(n, r, seed, transverse_scale=20., cross_amplitude=.3,
                    generic_scale=.03, global_enumeration=False):
    A, b, hidden_labels, L, fixture_parameters = make_fixture(
        n, r, seed, transverse_scale, cross_amplitude, generic_scale)
    experiment = ScalarQuadraticExperiment(A, b, sigma=5.e-6, seed=seed+1)
    service, record, full = acquire_latent_design(experiment, n)
    record.update({"n": n, "hidden_group_count_for_fixture_only": r,
                   "fixture_parameters": fixture_parameters,
                   "source_offset": 1000., "source_sigma": experiment.sigma})
    if service is None:
        return record, full
    learned_partition = {frozenset(i for i, a in enumerate(service.labels) if a == group)
                         for group in range(service.r)}
    true_partition = {frozenset(i for i, a in enumerate(hidden_labels) if a == group)
                      for group in range(r)}
    assert learned_partition == true_partition
    denominator = full["denominator"]
    acquired = np.asarray(full["A_units"], dtype=float)/denominator
    acquired_b = np.asarray(full["b_units"], dtype=float)/denominator
    offmask = ~np.eye(n, dtype=bool)
    maximum_coefficient_error = max(float(np.max(np.abs((acquired-A)[offmask]))),
                                    float(np.max(np.abs(acquired_b-b))))
    assert maximum_coefficient_error <= float(Fraction(full["coefficient_radius"]))
    frustrated = sum(A[i, j]*A[j, k]*A[i, k] > 0
                     for i in range(n) for j in range(i+1, n) for k in range(j+1, n))
    assert frustrated > 0
    assert np.any(A[offmask] > 0) and np.any(A[offmask] < 0)
    assert np.linalg.matrix_rank(L, tol=1e-8) == n-r
    aligned = np.array([[z[a] for a in service.labels]
                        for z in itertools.product((-1, 1), repeat=service.r)], dtype=np.int8)
    all_x = (np.array(list(itertools.product((-1, 1), repeat=n)), dtype=np.int8)
             if global_enumeration else None)
    rng = np.random.default_rng(seed+2)
    queries = []
    previous = np.ones(n)
    for t in range(8):
        h = .16*rng.uniform(-1, 1, n)+.03*previous*((-1)**t)
        answer, work = service.solve(h)
        # This exact enumeration compares against all learned aligned states.
        # Global 2^n enumeration is separately performed only on the small case.
        compiled_values = [service.compiled_energy(x, h) for x in aligned]
        assert service.compiled_energy(answer, h) == min(compiled_values)
        physical_answer = true_energy(A, b, answer, h)
        aligned_optimum = float(np.min(true_energy(A, b, aligned, h)))
        global_optimum = float(np.min(true_energy(A, b, all_x, h))) if all_x is not None else None
        if global_optimum is not None:
            assert physical_answer-global_optimum <= float(service.regret_bound)+1e-8
        queries.append({"query": t, "true_regret_vs_all_aligned": physical_answer-aligned_optimum,
                        "true_regret_vs_global": None if global_optimum is None else physical_answer-global_optimum,
                        "actual_executor": work})
        previous = answer
    bad_field = [Fraction(0)]*n
    bad_field[0] = service.H+1
    try:
        service.solve(bad_field)
    except ValueError as error:
        box_failure = str(error)
    else:
        raise AssertionError("Field box violation was silently accepted")
    wrong = service.labels.copy()
    first = 0
    second = next(i for i, label in enumerate(wrong) if label != wrong[first])
    wrong[first], wrong[second] = wrong[second], wrong[first]
    wrong_service, wrong_record = certify_partition(full, wrong, Fraction(1, 5), Fraction(1, 50))
    assert wrong_service is None
    wide_service, wide_record = certify_partition(full, service.labels, Fraction(50), Fraction(1, 50))
    assert wide_service is None
    record.update({"learned_partition_matches_hidden_fixture": True,
                   "nonzero_ambient_offdiagonal_pairs": int(np.count_nonzero(np.triu(A, 1))),
                   "positive_offdiagonal_pairs": int(np.sum(np.triu(A, 1) > 0)),
                   "negative_offdiagonal_pairs": int(np.sum(np.triu(A, 1) < 0)),
                   "frustrated_triangles": int(frustrated), "transverse_rank": n-r,
                   "max_actual_acquired_coefficient_error": maximum_coefficient_error,
                   "all_aligned_configurations_checked_per_query": len(aligned),
                   "all_ambient_configurations_checked_per_query": len(all_x) if all_x is not None else None,
                   "queries": queries, "out_of_box_query_rejection": box_failure,
                   "wrong_partition_rejection": wrong_record,
                   "widened_field_box_rejection": wide_record,
                   "retained_service_labels": n,
                   "retained_service_scalar_coefficients": service.r+len(service.forest),
                   "full_model_stored_outside_service": True})
    return record, full


def main():
    outputs, models = [], {}
    for name, parameters in [
        ("small_strong", dict(n=12, r=3, seed=191, global_enumeration=True)),
        ("large_strong", dict(n=24, r=6, seed=277)),
        ("weak_transverse", dict(n=24, r=6, seed=319, transverse_scale=1.6,
                                 cross_amplitude=.10, generic_scale=.001))]:
        record, full = verify_fixture(**parameters)
        record["name"] = name
        outputs.append(record)
        models[name] = full
    target = Path(__file__).with_name("latent_design_results.json")
    target.write_text(json.dumps({"status": "completed paid acquisition and exact certificate attempts",
                                  "fixtures": outputs}, indent=2)+"\n")
    Path(__file__).with_name("latent_design_acquired_models.json").write_text(
        json.dumps(models, indent=2)+"\n")
    print(json.dumps({"fixtures": [{"name": r["name"], "status": r["status"],
                                     "accepted_certificate": r["accepted_certificate"],
                                     "source": r["acquisition"]["source"]}
                                    for r in outputs]}, indent=2))


if __name__ == "__main__":
    main()
