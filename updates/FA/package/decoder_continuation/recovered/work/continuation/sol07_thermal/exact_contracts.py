#!/usr/bin/env python3
"""Exact rational thermal identifiability, calibration, and alarm certificates.

Only standard-library arithmetic is used. No hardware data are simulated or
claimed. The radiometer confidence statements are conditional on independent
proper complex Gaussian modes and an acquired upper bound on total power.
"""
from fractions import Fraction as F
from math import isqrt, factorial
from pathlib import Path
import hashlib
import json
import time

HERE = Path(__file__).resolve().parent


def encode(x):
    if isinstance(x, F):
        return {"rational": str(x), "decimal": float(x)}
    if isinstance(x, dict):
        return {k: encode(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [encode(v) for v in x]
    return x


def dot(x, y):
    return sum((a*b for a, b in zip(x, y)), F(0))


def transpose(A):
    return list(map(list, zip(*A)))


def mm(A, B):
    return [[dot(a, b) for b in transpose(B)] for a in A]


def inverse(A):
    n = len(A)
    aug = [list(row)+[F(i == j) for j in range(n)]
           for i, row in enumerate(A)]
    for i in range(n):
        j = next(j for j in range(i, n) if aug[j][i])
        aug[i], aug[j] = aug[j], aug[i]
        p = aug[i][i]
        aug[i] = [v/p for v in aug[i]]
        for j in range(n):
            if j != i:
                p = aug[j][i]
                aug[j] = [x-p*y for x, y in zip(aug[j], aug[i])]
    return [row[n:] for row in aug]


def identity(n):
    return [[F(i == j) for j in range(n)] for i in range(n)]


def csq(z):
    return z[0]**2+z[1]**2


def cmul(a, b):
    return (a[0]*b[0]-a[1]*b[1], a[0]*b[1]+a[1]*b[0])


def cadd(a, b):
    return (a[0]+b[0], a[1]+b[1])


def sqrt_up(x, scale=10**12):
    """A rational upper enclosure, with an exact square check."""
    n = (x.numerator*scale*scale+x.denominator-1)//x.denominator
    r = isqrt(n)
    if r*r < n:
        r += 1
    answer = F(r, scale)
    assert answer*answer >= x
    return answer


def exp_lower(x, terms=100):
    return sum((x**k/F(factorial(k)) for k in range(terms)), F(0))


def power_error(power_cap, modes, x):
    # Gamma(m, scale=P/m) Chernoff/Laurent--Massart enclosure.
    return power_cap*(sqrt_up(2*x/modes)+x/modes)


def loss_coordinate_witness():
    """Continuous LP primal/dual certificates, no floating integration."""
    L, A = F(100), F(1, 5)
    amin, amax = F(1, 1000), F(3, 1000)
    vlo, vhi = 1/amax, 1/amin
    mu = [F(9, 100), F(1, 50), F(9, 100)]
    T = [F(300), F(350), F(300)]
    lo_hot, hi_hot = vlo, vhi
    lo_cold = (L-mu[1]*lo_hot)/(mu[0]+mu[2])
    hi_cold = (L-mu[1]*hi_hot)/(mu[0]+mu[2])
    vmin, vmax = [lo_cold, lo_hot, lo_cold], [hi_cold, hi_hot, hi_cold]
    for v in [vmin, vmax]:
        assert dot(mu, v) == L
        assert all(vlo <= x <= vhi for x in v)
        assert sum(mu) == A
    mean_min = dot(T, [m*v for m, v in zip(mu, vmin)])/L
    mean_max = dot(T, [m*v for m, v in zip(mu, vmax)])/L
    lam = F(300)
    dual_max = lam*L+sum(m*max((t-lam)*vlo, (t-lam)*vhi)
                              for m, t in zip(mu, T))
    dual_min = lam*L+sum(m*min((t-lam)*vlo, (t-lam)*vhi)
                              for m, t in zip(mu, T))
    assert dual_max/L == mean_max == 310
    assert dual_min/L == mean_min == F(910, 3)
    # Replacing the step by a continuous 50 K triangle on the same u interval
    # preserves exactly half the excess area. Its physical Lipschitz bound is
    # 5000*a_max = 15 K/m, including the endpoints of the hot interval.
    triangular_min = 300+(mean_min-300)/2
    triangular_max = 300+(mean_max-300)/2
    assert triangular_max-triangular_min == F(10, 3)
    return {
        "status": "EXACT_RATIONAL_PRIMAL_DUAL_WITNESS_AND_ANALYTIC_ALL_FREQUENCY_GAUGE",
        "length_m": L, "integrated_loss_A": A,
        "local_loss_bounds_per_m": [amin, amax],
        "common_loss_coordinate_intervals": [[0, mu[0]], [mu[0], mu[0]+mu[1]], [mu[0]+mu[1], A]],
        "common_step_temperatures_K": T,
        "v_dx_du_bounds": [vlo, vhi],
        "minimum_mean_model": {"v": vmin, "a_per_m": [1/v for v in vmin],
                               "physical_cell_lengths_m": [m*v for m, v in zip(mu, vmin)],
                               "physical_mean_K": mean_min},
        "maximum_mean_model": {"v": vmax, "a_per_m": [1/v for v in vmax],
                               "physical_cell_lengths_m": [m*v for m, v in zip(mu, vmax)],
                               "physical_mean_K": mean_max},
        "dual_multiplier_K": lam,
        "dual_objective_min_K_m": dual_min,
        "dual_objective_max_K_m": dual_max,
        "exact_mean_interval_K": [mean_min, mean_max],
        "mean_diameter_K": mean_max-mean_min,
        "any_point_estimator_minimax_absolute_error_lower_K": (mean_max-mean_min)/2,
        "continuous_triangular_temperature_witness": {
            "T_of_u": "300+50*max(0,1-abs(u-1/10)/(1/100))",
            "physical_Lipschitz_bound_K_per_m": F(15),
            "mean_interval_K": [triangular_min, triangular_max],
            "minimax_error_lower_K": (triangular_max-triangular_min)/2},
        "data_generously_granted_exact": ["absolute full S(f) at all frequencies",
            "full two-port emitted covariance C(f) at all frequencies",
            "all remote heated/unheated terminations", "exact T(u)",
            "geometry length and phase velocity", "local loss envelope"],
        "preserved_data_proof": "For z/Z0=Z0*y=a(x)+s/v0, boundary S depends only on A,L; C depends only on T(u),A. Both models share these exactly. Thus R=Z0*a, G=a/Z0, L=Z0/v0 and C=1/(Z0*v0) are passive and L,C are known constants. A common positive-real h(s) replacing a by a*h extends the same gauge but is unnecessary.",
        "model_boundary": "Passive constant-impedance distortionless RLGC family with known constant L,C; does NOT prove nonidentifiability within the narrower inherited 40-scale sqrt(f)/f loss-law template.",
        "strongest_boundary_controls": "Endpoint sensors see 300 K in both; arbitrary calibrated active TDR/VNA and all coherent thermal boundary measurements agree exactly. Internal probes change the access contract.",
    }


def interval_square(lo, hi):
    return (F(0) if lo <= 0 <= hi else min(lo*lo, hi*hi), max(lo*lo, hi*hi))


def recovered_parameter_bounds(q, error):
    box = [(v-e, v+e) for v, e in zip(q, error)]
    beta_lo, beta_hi = box[1]
    if beta_lo <= 0:
        return {"status": "NO_POSITIVE_BETA_LOWER_BOUND", "q_intervals": box}
    dr = [(box[2][0]/beta_lo), (box[2][0]/beta_hi),
          (box[2][1]/beta_lo), (box[2][1]/beta_hi)]
    di = [(box[3][0]/beta_lo), (box[3][0]/beta_hi),
          (box[3][1]/beta_lo), (box[3][1]/beta_hi)]
    sq2, sq3 = interval_square(*box[2]), interval_square(*box[3])
    Glo = box[0][0]+(sq2[0]+sq3[0])/beta_hi
    Ghi = box[0][1]+(sq2[1]+sq3[1])/beta_lo
    return {"status": "DETERMINISTIC_OUTER_INTERVALS", "q_intervals": box,
            "d_real_interval": [min(dr), max(dr)],
            "d_imag_interval": [min(di), max(di)],
            "G_interval": [Glo, Ghi],
            "abs_c_squared_interval": [max(F(0), Glo)/beta_hi, Ghi/beta_lo],
            "phase_c": "EXACTLY_UNIDENTIFIED_WITHOUT_INDEPENDENT_COHERENT_REFERENCE"}


def calibration_contract():
    # A deliberately well-spread five-standard reference geometry. True values
    # define this constructed certificate, not purchased/acquired standards.
    gammas = [(F(0), F(0)), (F(1,2), F(0)), (-F(1,2), F(0)),
              (F(0), F(1,2)), (F(0), -F(1,2))]
    c, d, G = (F(1001,1000), F(1,1000)), (F(1,1000), -F(2,1000)), F(1)
    reported = [cadd(d, cmul(c, z)) for z in gammas]
    assert all(csq(g) <= 1 for g in reported)
    A = [[F(1), -csq(z), 2*z[0], 2*z[1]] for z in reported]
    z = [G*(1-csq(g)) for g in gammas]
    B = mm(inverse(mm(transpose(A), A)), transpose(A))
    assert mm(B, A) == identity(4)
    q = [dot(row, z) for row in B]
    expected = [G*(1-csq(d)/csq(c)), G/csq(c),
                G*d[0]/csq(c), G*d[1]/csq(c)]
    assert q == expected
    assert [dot(row, q) for row in A] == z
    norms = [sum(abs(x) for x in row) for row in B]
    Qmax = [F(2), F(2), F(1,50), F(1,50)]
    assert all(abs(x) <= Q for x, Q in zip(q, Qmax))
    eps_report, eps_hotcold = F(1,100000), F(1,100000)
    dT, deltaT_each, Gmax = F(50), F(1,100), F(2)
    Rmax, Qnoise_max = F(350), F(50)
    switch_residual, Mcurvature = F(1,100), F(1,100000)
    subdwell, switch_dead = F(1), F(1,100)
    abba_drift = Mcurvature*(subdwell+switch_dead)**2
    temperature_error = 2*Gmax*deltaT_each/dT
    hotcold_match_error = Gmax*((2*eps_hotcold+eps_hotcold**2)*Rmax+
                             2*Qnoise_max*eps_hotcold)/dT
    row_error = (2*eps_report+eps_report**2)*Qmax[1]+2*eps_report*(Qmax[2]+Qmax[3])
    systematic = temperature_error+hotcold_match_error+(switch_residual+abba_drift)/dT+row_error
    plans = []
    for label, bins, bandwidth, x in [
            ("490_independent_100kHz_bins", 490, F(100000), F(13)),
            ("one_flat_50MHz_interface_ONLY_IF_FLATNESS_ACQUIRED", 1, F(50000000), F(6))]:
        power_count = 2*len(gammas)*bins
        alpha = F(1,20)
        exp_proof = exp_lower(x)
        assert exp_proof > 2*power_count/alpha
        for tau in [F(2), F(10), F(100), F(1000)]:
            assert (tau/(2*subdwell)).denominator == 1
            modes = bandwidth*tau
            stat = power_error(F(1000), modes, x)
            total = 2*stat/dT+systematic
            err = [n*total for n in norms]
            bounds = recovered_parameter_bounds(q, err)
            wall = 3*(2*len(gammas)*tau)*(1+switch_dead/subdwell)
            plans.append({"interface": label, "bins": bins, "seconds_per_hot_or_cold_state": tau,
                          "complex_mode_count_each_power": modes, "x": x,
                          "joint_failure_probability_strictly_below": alpha,
                          "single_power_statistical_error_K_counts": stat,
                          "contrast_plus_design_total_error": total,
                          "parameter_error_radii": err,
                          "parameter_outer_bounds": bounds,
                          "calibration_sequence_wallclock_s_at_one_third_duty": wall,
                          "including_inherited_1800s_VNA_warmup_s": wall+1800,
                          "excluded_unknown_costs": ["thermal equilibration and temperature metrology",
                              "two thermostated copies per nominal impedance", "VNA acquisition",
                              "commissioning, correlated-mode qualification and validation"]})
    return {
        "status": "EXACT_LINEAR_DUAL_AND_DETERMINISTIC_INTERVAL_PROPAGATION_CONDITIONAL_FINITE_SAMPLE_COVERAGE",
        "design": A, "left_inverse_dual_certificates": B,
        "checked_B_times_A": mm(B, A), "true_constructed_q": q,
        "dual_L1_error_amplifications": norms,
        "exact_nonidentifiability": "All heated contrasts are invariant under c -> exp(i phi)c and gamma -> exp(-i phi)gamma. Rotating receiver cross correlation consistently preserves powers and PSD. An independently acquired coherent phase reference is necessary.",
        "systematic_budget_inputs_not_hardware_acquired": {
            "nominal_hotcold_contrast_K": dT, "each_standard_local_temperature_error_K": deltaT_each,
            "complex_reported_Gamma_error_radius": eps_report,
            "complex_hotcold_Gamma_change_radius": eps_hotcold,
            "gain_upper": Gmax, "max_abs_Tu_minus_Th_K": Rmax,
            "receiver_noise_correlation_magnitude_upper_K": Qnoise_max,
            "differential_switch_power_error_K_counts": switch_residual,
            "common_gain_and_offset_drift_curvature_K_counts_per_s2": Mcurvature,
            "ABBA_subdwell_s": subdwell, "switch_dead_s": switch_dead,
            "q_absolute_component_envelope": Qmax},
        "separate_normalized_contrast_error_bounds": {
            "standard_temperature": temperature_error, "hotcold_match_and_correlated_receiver_noise": hotcold_match_error,
            "ABBA_common_drift": abba_drift/dT, "switching": switch_residual/dT,
            "coherent_reported_Gamma_design_error": row_error,
            "total_systematic_floor": systematic},
        "infinite_integration_parameter_error_floor": [n*systematic for n in norms],
        "plans": plans,
        "not_a_cable_mean_certificate": "These intervals constrain only the shared affine calibration. A spatial mean additionally requires absolute phase, global model injectivity and a certified local kernel enclosure over the entire admissible model set.",
        "non_gaussian_coverage_formula": "For m independent proper complex Gaussian modes and true P<=Pcap, |P_hat-P|<=Pcap*(sqrt(2*x/m)+x/m) except probability 2 exp(-x). Union over all powers needs no independence between different powers."
    }


def thermal_alarm():
    # Passive reciprocal two-mode network: a lossless hybrid mixes two equally
    # absorbing modes, one 360 K and one 300 K. S=sqrt(1/2)*I, A=(1/2)*I.
    absorption = [[F(1,2), F(0)], [F(0), F(1,2)]]
    C = [[F(165), F(15)], [F(15), F(165)]]
    limit = F(340)
    D = [[C[i][j]-limit*absorption[i][j] for j in range(2)] for i in range(2)]
    v = [F(1), F(1)]
    assert dot(v, [dot(row, v) for row in D])/dot(v,v) == 10
    assert [C[i][i]/absorption[i][i] for i in range(2)] == [330,330]
    # Independent held-out validation of the chosen combiner mode.
    source_power, reference_power = F(450), F(440)  # includes 100 K receiver
    pcap, B, tau, x, alpha = F(500), F(1000000), F(1), F(5), F(1,20)
    assert exp_lower(x) > 4/alpha
    stat = 2*power_error(pcap, B*tau, x)
    budget = {"threshold_bath_temperature": F(1), "upstream_noise_covariance": F(1,5),
              "receiver_in_out_noise_correlation": F(1,5), "switch_transfer": F(1,5),
              "receiver_offset_and_gain_drift": F(3,10)}
    systematic = sum(budget.values())
    margin = source_power-reference_power-stat-systematic
    assert margin > 0
    # Exact deterministic entrywise certificate, independent of stochastic model.
    error_diag, error_real_offdiag = F(1,2), F(1,2)
    quadratic = dot(v, [dot(row, v) for row in D])
    entry_error = 2*error_diag+2*error_real_offdiag
    assert quadratic-entry_error == 18
    # Optional absolute temperature lower bound needs absorption calibration.
    absorption_upper = F(51,100)
    Tmin_hot = limit+margin/absorption_upper
    return {
        "status": "EXACT_PASSIVE_NETWORK_ALGEBRA_AND_CONDITIONAL_FINITE_UNCERTAINTY_ALARM",
        "operation": "Certify that some dissipative region exceeds Tlim, without assigning a location or reconstructing RLGC.",
        "theorem": "If C=integral T(x)W(x)dx, W(x)>=0 and A=integral W=I-S*Sdagger, then T(x)<=Tlim everywhere implies C-Tlim*A<=0. Any certified positive quadratic form disproves that temperature bound.",
        "constructed_absorption_A": absorption, "constructed_C_in_kB_units": C,
        "threshold_K": limit, "constructed_D_C_minus_threshold_A": D,
        "single_port_noise_temperatures_K": [F(330), F(330)],
        "coherent_plus_mode_noise_temperature_K": F(360),
        "coherent_plus_mode_threshold_power_margin_K": F(10),
        "exact_entrywise_dual_certificate": {"v_unnormalized": v, "quadratic_form": quadratic,
            "entry_error_bound": entry_error, "strict_positive_lower_bound": quadratic-entry_error},
        "sign_comparison_receiver_contract": "An acquired matched upstream thermal bath at Tlim with uncorrelated forward receiver noise gives Y_DUT-Y_direct_threshold=H*(C-Tlim*A)*Hdagger. Arbitrary fixed nonsingular H, including unknown phase, preserves the sign. Finite bath/correlation/switch/drift errors require the stated simultaneous norm bound.",
        "heldout_mode_power_certificate": {
            "constructed_measured_power_centers_K_counts": [source_power, reference_power],
            "power_upper_bound_K_counts": pcap, "equivalent_independent_bandwidth_Hz": B,
            "integration_s_each_state": tau, "finite_sample_x": x,
            "conditional_joint_failure_below": alpha,
            "statistical_difference_error_bound_K_counts": stat,
            "hypothetical_acquired_systematic_budgets_K_counts": budget,
            "strict_positive_margin_after_all_stated_errors_K_counts": margin,
            "measurement_wallclock_s_at_one_third_duty": 3*2*tau,
            "reference_equilibration_isolation_and_validation_cost": "UNKNOWN; not included in six-second constructed integration",
            "optional_local_temperature_lower_K_with_absorption_upper_0p51": Tmin_hot},
        "correlated_receiver_noise_failure_boundary": "Without a bound on upstream noise covariance and input/output noise correlation, a uniform safe DUT can produce a positive measured difference. Additive independent receiver-noise subtraction alone is insufficient.",
        "matched_controls": {"endpoint_temperature_sensors": "May miss an internal hot region; do not supply full physical temperature coverage.",
            "active_TDR": "Cannot distinguish the exact loss-coordinate gauge pair and has no thermometer guarantee without acquired constitutive temperature dependence.",
            "optimal_mode_conventional_Johnson_noise_thermometry": "A calibrated lossless hybrid plus a conventional one-channel radiometer measures the SAME 360 K plus mode. It matches this certificate with the same reference, bandwidth and system-noise budget.",
            "claimed_advantage_over_strongest_control": False},
        "prior_art": "Characteristic noise-temperature eigenvalues and lossless mode diagonalization are present in Bosma 1967; this is a finite-error alarm formulation, not a novelty-cleared new sensing law.",
        "physical_validation": False,
    }


def main():
    started = time.perf_counter()
    outputs = {"exact_identifiability.json": loss_coordinate_witness(),
               "finite_calibration.json": calibration_contract(),
               "boundary_alarm.json": thermal_alarm()}
    receipts = []
    for name, result in outputs.items():
        payload = (json.dumps(encode(result), indent=2)+"\n").encode()
        (HERE/name).write_bytes(payload)
        receipts.append({"path": name, "sha256": hashlib.sha256(payload).hexdigest(), "bytes": len(payload)})
    receipt = {"status": "ALL_EXACT_ASSERTIONS_PASSED", "arithmetic": "Python Fraction and integer square roots",
               "wallclock_s": time.perf_counter()-started, "outputs": receipts,
               "scope": "Constructed certificates; no acquired thermometry data, no hardware accuracy or novelty claim."}
    (HERE/"RUN_RECEIPT.json").write_text(json.dumps(receipt, indent=2)+"\n")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
