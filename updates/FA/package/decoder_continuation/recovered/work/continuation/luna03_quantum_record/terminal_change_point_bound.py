#!/usr/bin/env python3
"""Known-arrival homodyne miss bound for the inherited G106 Floquet carrier schedule.

This is a deterministic coherent-carrier model, not a jump-aware instrument.
It uses the source model's q-preserving linear pole schedule, keeps the cavity
pole coordinate continuous at an f->e change point, and applies the source
eta=0.5 collection scenario to the one monitored cavity carrier.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
from scipy.integrate import quad
from scipy.special import ndtr, ndtri

# Source: work/phase5/quantum_operation/floquet_record_300_noecho.json and the
# schedule() values reproduced by floquet_record_instrument.py (G=106.10699).
KAPPA = 2 * math.pi * 0.21  # us^-1
ETA = 0.5
ALPHA_FPR = 0.02  # false rejection of a no-jump code record, per full window
READ_T = 3.0
RESET_T = 0.8
T_DECISION = READ_T + RESET_T
LAMBDA_E = 0.6566397373540859 + 0j
LAMBDA_F = 0.6532249326634637 + 2j * math.pi * (5.011138786285301 - 4.015441048361026)
V_E = 0.9976149195061285
V_F = 0.9945578968993299
READ_DRIVE = 1.4718014543910638 + 0j
RESET_DRIVES = (
    -1.869440159721404 + 0.8871173164501848j,
    -1.804861391639724 - 0.6821989567129426j,
)
READ_BINS = 24
RESET_BINS = 8
# Source model's q=2->1 branch rate and total q=2 vacuum decay (per us).
# These rates only weight an illustrative event-time distribution; no jump
# photons are placed in the homodyne record.
RATE_FE = 0.04131524752645586
RATE_F_TOTAL = 0.04133833561408882
RATE_E_TOTAL = 0.01753125447611327


def schedule_segments(tail_us: float) -> list[tuple[float, float, complex]]:
    """Exact piecewise-constant input schedule and a finite passive tail."""
    segs: list[tuple[float, float, complex]] = []
    dt = READ_T / READ_BINS
    for i in range(READ_BINS):
        segs.append((i * dt, (i + 1) * dt, READ_DRIVE))
    reset_bin = RESET_T / RESET_BINS
    half_bins = RESET_BINS // 2
    for i in range(half_bins):
        segs.append((READ_T + i * reset_bin, READ_T + (i + 1) * reset_bin, RESET_DRIVES[0]))
    offset = RESET_T / 2
    for i in range(half_bins):
        segs.append((READ_T + offset + i * reset_bin,
                     READ_T + offset + (i + 1) * reset_bin, RESET_DRIVES[1]))
    if tail_us > 0:
        segs.append((T_DECISION, T_DECISION + tail_us, 0j))
    return segs


def advance(x: complex, lam: complex, drive_gain: float, u: complex, dt: float) -> complex:
    if dt <= 0:
        return x
    return x * np.exp(-lam * dt) + drive_gain * u * (-np.expm1(-lam * dt)) / lam


def state_at_f(t: float, segs: list[tuple[float, float, complex]]) -> complex:
    """No-jump physical-f branch amplitude at time t in the pole model."""
    x = 0j
    for a, b, u in segs:
        if t <= a:
            break
        end = min(t, b)
        x = advance(x, LAMBDA_F, V_F ** 2, u, end - a)
        if t <= b:
            return x
    if t > T_DECISION:
        x *= np.exp(-LAMBDA_F * (t - T_DECISION))
    return x


def exp_integral(z: complex, dt: float) -> complex:
    if abs(z) < 1e-13:
        return complex(dt)
    return np.expm1(z * dt) / z


def carrier_distance_piece(xe: complex, xf: complex, u: complex, dt: float) -> float:
    """Integral kappa*|x_e-x_f|^2 over one constant-drive piece."""
    if dt <= 0:
        return 0.0
    # x_q=v_q*alpha_q is the physical carrier field in the one-pole schedule.
    # The source schedule has alpha-dot=-lambda*alpha+v_q*u and beta=sqrt(kappa)*v_q*alpha.
    # x is continuous across the qutrit change, while its drive gain becomes v_q^2.
    xe_ss = V_E ** 2 * u / LAMBDA_E
    xf_ss = V_F ** 2 * u / LAMBDA_F
    coeffs = (
        (xe_ss - xf_ss, 0j),
        (xe - xe_ss, -LAMBDA_E),
        (-(xf - xf_ss), -LAMBDA_F),
    )
    total = 0j
    for ci, ri in coeffs:
        for cj, rj in coeffs:
            total += ci * np.conj(cj) * exp_integral(ri + np.conj(rj), dt)
    ans = KAPPA * total.real
    return max(0.0, float(ans))


def J_known_tau(tau: float, tail_us: float) -> float:
    """Raw monitored-carrier displacement norm before efficiency, for known tau."""
    W = T_DECISION + tail_us
    if tau >= W:
        return 0.0
    segs = schedule_segments(tail_us)
    xf = state_at_f(tau, segs)
    # The q-preserving pole state alpha is continuous at the qutrit change.
    # Since the measured carrier is x=v_q*alpha, its expectation can step when
    # q changes; the f->e jump photon itself is not included in this record.
    xe = (V_E / V_F) * xf
    total = 0.0
    current = tau
    for a, b, u in segs:
        lo = max(a, tau)
        hi = min(b, W)
        if hi <= lo:
            continue
        # Intervals are contiguous in the acquired schedule; handle any gap
        # explicitly with the drive off before entering the next segment.
        if lo > current:
            gap = lo - current
            xe = advance(xe, LAMBDA_E, V_E ** 2, 0j, gap)
            xf = advance(xf, LAMBDA_F, V_F ** 2, 0j, gap)
            current = lo
        dt = hi - lo
        total += carrier_distance_piece(xe, xf, u, dt)
        xe = advance(xe, LAMBDA_E, V_E ** 2, u, dt)
        xf = advance(xf, LAMBDA_F, V_F ** 2, u, dt)
        current = hi
    return total


def beta_homodyne(j_raw: float, alpha: float = ALPHA_FPR) -> float:
    """Exact NP miss probability for time-matched homodyne at size alpha."""
    shift = 2.0 * math.sqrt(ETA * max(0.0, j_raw))
    return float(ndtr(float(ndtri(1.0 - alpha)) - shift))


def beta_coherent_povm(j_raw: float, alpha: float = ALPHA_FPR) -> float:
    """Exact minimum miss for two pure coherent states at false-flag size alpha."""
    c2 = math.exp(-ETA * max(0.0, j_raw))
    if alpha >= c2:
        return 0.0
    return (math.sqrt((1.0 - alpha) * c2) - math.sqrt(alpha * (1.0 - c2))) ** 2


def direct_quad_distance(tau: float, tail_us: float) -> float:
    """Independent direct quadrature of the two exact piecewise ODE solutions."""
    W = T_DECISION + tail_us
    segs = schedule_segments(tail_us)
    xf_tau = state_at_f(tau, segs)

    def branch_at(t: float, q: str) -> complex:
        if t <= tau:
            return state_at_f(t, segs)
        x = (V_E / V_F) * xf_tau if q == 'e' else xf_tau
        lam, gain = (LAMBDA_E, V_E ** 2) if q == 'e' else (LAMBDA_F, V_F ** 2)
        for a, b, u in segs:
            lo = max(a, tau)
            hi = min(b, t)
            if hi > lo:
                x = advance(x, lam, gain, u, hi - lo)
        return x

    points = sorted({tau, W, *(x for a, b, _ in segs for x in (a, b) if tau < x < W)})
    total = 0.0
    for a, b in zip(points, points[1:]):
        def integrand(t):
            xe = branch_at(t, 'e')
            xf = branch_at(t, 'f')
            return KAPPA * abs(xe - xf) ** 2
        total += quad(integrand, a, b, epsabs=2e-13, epsrel=2e-11, limit=100)[0]
    return total


def gauss_integrate_missed(tail_us: float, order: int) -> tuple[float, float]:
    """Counterfactual diagnostic: hold e after each first f->e event through W."""
    W = T_DECISION + tail_us
    nodes, weights = np.polynomial.legendre.leggauss(order)
    segs = schedule_segments(tail_us)
    missed = 0.0
    mass = 0.0
    for a, b, _ in segs:
        xs = (a + b) / 2 + (b - a) / 2 * nodes
        ws = (b - a) / 2 * weights
        for t, w in zip(xs, ws):
            density = RATE_FE * math.exp(-RATE_F_TOTAL * t)
            mass += w * density
            missed += w * density * beta_homodyne(J_known_tau(float(t), tail_us))
    return missed, mass


def gauss_integrate_terminal_e(tail_us: float, order: int, start_time: float = 0.0) -> dict:
    """Terminal-e event and missed masses; excludes paths returning e->g before W."""
    W = T_DECISION + tail_us
    nodes, weights = np.polynomial.legendre.leggauss(order)
    segs = schedule_segments(tail_us)
    masses = {'terminal_e_mass': 0.0, 'homodyne_miss': 0.0, 'coherent_povm_miss': 0.0}
    for a, b, _ in segs:
        a = max(a, start_time)
        if b <= a:
            continue
        xs = (a + b) / 2 + (b - a) / 2 * nodes
        ws = (b - a) / 2 * weights
        for t, w in zip(xs, ws):
            density = RATE_FE * math.exp(-RATE_F_TOTAL * t) * math.exp(-RATE_E_TOTAL * (W - t))
            j = J_known_tau(float(t), tail_us)
            masses['terminal_e_mass'] += w * density
            masses['homodyne_miss'] += w * density * beta_homodyne(j)
            masses['coherent_povm_miss'] += w * density * beta_coherent_povm(j)
    return masses


def passive_tail_upper(tail_us: float) -> float:
    """Analytic uniform J upper bound for events during a finite free-decay tail."""
    if tail_us <= 0:
        return 0.0
    xf_T = state_at_f(T_DECISION, schedule_segments(0.0))
    # x_f=v_f*alpha_f is the output-carrier amplitude. For a passive tail,
    # alpha_f(tau)=alpha_f(T)*exp(-lambda_f*(tau-T)). At the change point
    # alpha_e(tau)=alpha_f(tau), so the output difference is proportional to
    # v_e*exp(-lambda_e*s)-v_f*exp(-lambda_f*s). For Re(lambda)>0,
    # |...| <= |v_e-v_f| + v_f*|lambda_e-lambda_f|*s. Integrating its square
    # gives a uniform upper bound on J over every tau in [T,T+L].
    alpha_f_T_sq = abs(xf_T / V_F) ** 2
    dv = abs(V_E - V_F)
    dl = abs(LAMBDA_E - LAMBDA_F)
    return float(KAPPA * alpha_f_T_sq * (
        dv ** 2 * tail_us + dv * V_F * dl * tail_us ** 2
        + V_F ** 2 * dl ** 2 * tail_us ** 3 / 3.0
    ))


def late_miss_intervals(tail_us: float, j_threshold: float) -> list[list[float]]:
    """Numerically locate connected tau intervals where homodyne miss >= .95."""
    W = T_DECISION + tail_us
    ngrid = 6001
    ts = np.linspace(0.0, W, ngrid)
    vals = [J_known_tau(float(t), tail_us) - j_threshold for t in ts]
    roots: list[float] = []
    for i in range(ngrid - 1):
        lo, hi = float(ts[i]), float(ts[i + 1])
        flo, fhi = vals[i], vals[i + 1]
        if flo == 0.0:
            roots.append(lo)
        if flo * fhi < 0.0:
            for _ in range(60):
                mid = (lo + hi) / 2
                fm = J_known_tau(mid, tail_us) - j_threshold
                if flo * fm <= 0:
                    hi, fhi = mid, fm
                else:
                    lo, flo = mid, fm
            roots.append((lo + hi) / 2)
    points = [0.0, *sorted(set(roots)), W]
    intervals = []
    for lo, hi in zip(points, points[1:]):
        if J_known_tau((lo + hi) / 2, tail_us) <= j_threshold:
            intervals.append([lo, hi])
    return intervals


def tail_beta_gate(tail_us: float) -> dict:
    W = T_DECISION + tail_us
    j_upper = passive_tail_upper(tail_us)
    beta_lower = beta_homodyne(j_upper)
    povm_beta_lower = beta_coherent_povm(j_upper)
    late_mass = (RATE_FE / RATE_F_TOTAL) * (
        math.exp(-RATE_F_TOTAL * T_DECISION) - math.exp(-RATE_F_TOTAL * W)
    )
    return {
        'tail_us': tail_us,
        'decision_us': W,
        'physical_carrier_field_squared_at_drive_off': abs(state_at_f(T_DECISION, schedule_segments(0.0))) ** 2,
        'pole_coordinate_alpha_squared_at_drive_off': abs(
            state_at_f(T_DECISION, schedule_segments(0.0)) / V_F
        ) ** 2,
        'J_upper_for_any_event_in_tail': j_upper,
        'homodyne_miss_probability_lower_bound_per_tail_event_surviving_as_e': beta_lower,
        'arbitrary_coherent_carrier_POVM_miss_probability_lower_bound_per_tail_event_surviving_as_e': povm_beta_lower,
        'source_scenario_FE_event_mass_per_initial_f_in_tail': late_mass,
    }


def main() -> None:
    alpha = ALPHA_FPR
    zcut = float(ndtri(1.0 - alpha))
    target = 0.95
    j95 = ((zcut - float(ndtri(target))) / (2.0 * math.sqrt(ETA))) ** 2
    tails = [0.0, 0.8, 1.6]
    rows = []
    convergence = {}
    for L in tails:
        miss16, mass16 = gauss_integrate_missed(L, 16)
        miss32, mass32 = gauss_integrate_missed(L, 32)
        miss64, mass64 = gauss_integrate_missed(L, 64)
        convergence[str(L)] = {
            'order16_missed_mass': miss16,
            'order32_missed_mass': miss32,
            'order64_missed_mass': miss64,
            'order32_to_64_abs_difference': abs(miss32 - miss64),
            'order64_event_mass': mass64,
        }
        W = T_DECISION + L
        times = sorted({0.0, 1.0, 2.0, 3.0, 3.4, 3.7, 3.79, 3.8, T_DECISION + L / 2, W})
        samples = []
        for tau in times:
            if 0 <= tau <= W:
                j = J_known_tau(tau, L)
                samples.append({'tau_us': tau, 'J_raw': j,
                                'collected_eta_J': ETA * j,
                                'homodyne_miss_at_2pct_FPR': beta_homodyne(j),
                                'coherent_POVM_miss_at_2pct_FPR': beta_coherent_povm(j)})
        terminal16 = gauss_integrate_terminal_e(L, 16)
        terminal32 = gauss_integrate_terminal_e(L, 32)
        terminal64 = gauss_integrate_terminal_e(L, 64)
        terminal_tail64 = gauss_integrate_terminal_e(L, 64, start_time=T_DECISION)
        rows.append({
            'tail_us': L,
            'decision_window_us': W,
            'counterfactual_fixed_e_hold_branch_missed_mass_from_first_FE_arrivals_per_initial_f': miss64,
            'first_FE_arrival_mass_before_decision_per_initial_f': mass64,
            'counterfactual_fixed_e_hold_branch_miss_fraction_among_first_FE_arrivals': miss64 / mass64 if mass64 else None,
            'terminal_e_only_scenario': {
                'terminal_e_mass_per_initial_f': terminal64['terminal_e_mass'],
                'homodyne_missed_terminal_e_mass_lower_bound_per_initial_f': terminal64['homodyne_miss'],
                'arbitrary_coherent_carrier_POVM_missed_terminal_e_mass_lower_bound_per_initial_f': terminal64['coherent_povm_miss'],
                'mixed_code_POVM_missed_terminal_e_mass_lower_bound': 0.5 * terminal64['coherent_povm_miss'],
                'mixed_code_homodyne_missed_terminal_e_mass_lower_bound': 0.5 * terminal64['homodyne_miss'],
                'homodyne_miss_fraction_lower_bound': terminal64['homodyne_miss'] / terminal64['terminal_e_mass'],
                'coherent_POVM_miss_fraction_lower_bound': terminal64['coherent_povm_miss'] / terminal64['terminal_e_mass'],
                'tail_terminal_e_mass_per_initial_f': terminal_tail64['terminal_e_mass'],
                'tail_homodyne_missed_terminal_e_mass_lower_bound_per_initial_f': terminal_tail64['homodyne_miss'],
                'tail_coherent_POVM_missed_terminal_e_mass_lower_bound_per_initial_f': terminal_tail64['coherent_povm_miss'],
                'tail_mixed_code_POVM_missed_terminal_e_mass_lower_bound': 0.5 * terminal_tail64['coherent_povm_miss'],
                'order16_to64_homodyne_abs_difference': abs(terminal16['homodyne_miss'] - terminal64['homodyne_miss']),
                'order16_to64_POVM_abs_difference': abs(terminal16['coherent_povm_miss'] - terminal64['coherent_povm_miss']),
            },
            'known_arrival_point_samples': samples,
            'connected_intervals_with_miss_at_least_95pct': late_miss_intervals(L, j95),
            'passive_tail_gate': tail_beta_gate(L),
        })

    # Exact analytic piece integration vs independent quadrature at representative
    # in-drive and in-tail change points.
    quad_checks = []
    for L, tau in [(0.0, 2.713), (0.0, 3.79), (0.8, 3.79), (0.8, 4.21), (1.6, 5.11)]:
        ja = J_known_tau(tau, L)
        jq = direct_quad_distance(tau, L)
        quad_checks.append({'tail_us': L, 'tau_us': tau, 'analytic_J': ja,
                            'direct_quadrature_J': jq, 'abs_error': abs(ja - jq)})

    # Exact whole-record Gaussian likelihood check for one representative event.
    tau_check, tail_check = 2.713, 0.8
    j_check = J_known_tau(tau_check, tail_check)
    shift = 2 * math.sqrt(ETA * j_check)
    c = zcut
    alpha_quad = quad(lambda z: math.exp(-z*z/2) / math.sqrt(2*math.pi), c, 12.0,
                      epsabs=1e-14)[0]
    beta_quad = quad(lambda z: math.exp(-(z-shift)**2/2) / math.sqrt(2*math.pi), -12.0, c,
                     epsabs=1e-14)[0]
    tradeoff = {
        'FPR_target': alpha,
        'threshold_sigma_above_nojump_mean': c,
        'J_raw': j_check,
        'collected_squared_displacement_eta_J': ETA * j_check,
        'Gaussian_mean_shift_sigma': shift,
        'FPR_from_direct_normal_integral': alpha_quad,
        'miss_from_closed_form': beta_homodyne(j_check),
        'miss_from_direct_normal_integral': beta_quad,
        'KL_event_vs_nojump_nats': shift**2 / 2,
    }

    out = {
        'status': 'INTERNAL_LINEAR_COHERENT_CARRIER_GAUSSIAN_LRT_ONLY',
        'model_inputs': {
            'candidate': 'G106 full-pull preferred300; source finite schedule no echo',
            'kappa_per_us': KAPPA,
            'eta_collected': ETA,
            'false_rejection_FPR_per_full_window': alpha,
            'read_us': READ_T, 'active_reset_us': RESET_T,
            'decision_windows_us': [T_DECISION + L for L in tails],
            'read_bins': READ_BINS, 'reset_bins': RESET_BINS,
            'lambda_e_per_us': [LAMBDA_E.real, LAMBDA_E.imag],
            'lambda_f_per_us': [LAMBDA_F.real, LAMBDA_F.imag],
            'carrier_v_e': V_E, 'carrier_v_f': V_F,
            'read_drive_per_us': [READ_DRIVE.real, READ_DRIVE.imag],
            'reset_drives_per_us': [[z.real, z.imag] for z in RESET_DRIVES],
            'f_to_e_branch_rate_per_us_scenario': RATE_FE,
            'total_f_loss_rate_per_us_scenario': RATE_F_TOTAL,
            'total_e_loss_rate_per_us_scenario': RATE_E_TOTAL,
            'jump_photon_collection': 'excluded; no jump outputs enter the homodyne record',
        },
        'gaussian_tradeoff_check': tradeoff,
        'tail_gate_threshold': {
            'target_miss_probability': target,
            'max_raw_J_for_that_miss_at_2pct_FPR': j95,
            'derivation': 'beta=Phi(Phi^-1(1-alpha)-2*sqrt(eta*J)); solve beta>=0.95',
        },
        'schedule_results': rows,
        'integration_convergence': convergence,
        'analytic_piece_vs_direct_quadrature': quad_checks,
        'scope': [
            'Event time tau is granted to the likelihood-ratio receiver; this is an optimistic pointwise benchmark.',
            'An unknown-arrival receiver with the same whole-window FPR cannot have a smaller miss at any fixed tau.',
            'Carrier-only coherent model; no f->e jump photons, sideband photons, other collected ports, or nonlinear jump-conditioned cavity states.',
            'Source rates and eta=0.5 are scenarios, not acquired operating-point measurements.',
            'The all-first-event fixed-e-hold integral is a counterfactual diagnostic; only terminal-e masses include e survival, and returned cascades need another change point.',
            'The arbitrary-POVM expression is the exact binary optimum only for the two pure coherent carrier states; it does not include collected jump photons or other output modes.',
            'Terminal-e weighting includes e-state survival exp(-Lambda_e*(W-tau)); returned e->g paths are excluded from terminal-e-only mass.',
            'A finite passive tail is explicitly charged as added decision latency; events continue during that tail.',
            'No universal quantum or hardware lower bound is asserted.',
        ],
    }
    path = Path(__file__).with_name('NUMERICAL_RESULTS.json')
    path.write_text(json.dumps(out, indent=2) + '\n')
    print(json.dumps({
        'status': out['status'],
        'whole_window': [{'tail_us': r['tail_us'],
                          'mixed_code_terminal_e_POVM_missed_mass_lb': r['terminal_e_only_scenario']['mixed_code_POVM_missed_terminal_e_mass_lower_bound'],
                          'terminal_e_mass_per_initial_f': r['terminal_e_only_scenario']['terminal_e_mass_per_initial_f'],
                          'terminal_e_POVM_miss_fraction_lb': r['terminal_e_only_scenario']['coherent_POVM_miss_fraction_lower_bound']}
                         for r in rows],
        'tail_gates': [r['passive_tail_gate'] for r in rows],
        'quad_max_abs_error': max(x['abs_error'] for x in quad_checks),
        'tradeoff': tradeoff,
        'result_path': str(path),
    }, indent=2))


if __name__ == '__main__':
    main()
