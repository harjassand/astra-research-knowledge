"""Exact rational theorem instantiation for the 80-bit nonmonotone target.

The target/reference calculations were executed. The high-precision 80-bit
native acquisition below is a proved budget, NOT an acquisition record.
All inequalities asserted here use Fraction arithmetic and rational bounds on
exponentials. The displayed decimal endpoints are rounded outward.
"""
from fractions import Fraction as F
from pathlib import Path
import json


def exp_lower(x, terms=100):
    x = F(x)
    assert x >= 0
    term = total = F(1)
    for k in range(1, terms+1):
        term *= x/k
        total += term
    return total


def exp_upper(x, terms=80):
    x = F(x)
    assert 0 <= x < terms+2
    term = total = F(1)
    for k in range(1, terms+1):
        term *= x/k
        total += term
    first_omitted = term*x/(terms+1)
    return total+first_omitted/(1-x/(terms+2))


def outward(x, places=18, upper=False):
    scale = 10**places
    k, rem = divmod(x.numerator*scale, x.denominator)
    if upper and rem:
        k += 1
    return f'{k//scale}.{k%scale:0{places}d}'


def main():
    here = Path(__file__).resolve().parent
    ref = json.loads((here.parent/'code_target/code_target_exact.json').read_text())
    n, m, eta = 80, 64, F(9, 20000)
    p0 = F(1, 2**m)
    b0 = 1-p0
    mean0 = F(ref['M0_exact'])
    assert ref['n'] == n and ref['m'] == m and F(ref['p_exact']) == p0

    # Stronger ordinary biased-bit coupling applies after any bit complement:
    # (1-eta)^n <= pi(x)/pi0(x) <= (1+eta)^n. Thus u=-n log(1-eta).
    u = F(181, 5000)
    assert n*eta/(1-eta) < u  # -log(1-eta)<=eta/(1-eta)
    v = F(367, 10000)
    assert u+eta/(1-eta) < v

    eu = exp_upper(u)
    e2uv = exp_upper(2*u+v)
    ev = exp_upper(v)
    kappa_squared_upper = n*(ev-1)**2
    lower_ratio = b0/(e2uv*(1+kappa_squared_upper))
    upper_ratio = e2uv*b0/(1-eu*p0)
    assert lower_ratio > F(4, 5)
    assert upper_ratio < F(28, 25)
    mean_lo, mean_hi = F(4, 5)*mean0, F(28, 25)*mean0
    gap_lo = F(37, 20)
    assert 2*(1-eta)/exp_upper(2*u) > gap_lo
    assert eu < 2
    p_plus, b_minus = 2*p0, 1-2*p0
    delta_hi = 1/(gap_lo*b_minus*mean_lo)
    assert delta_hi < F(1, 10**17)
    # Monotonicity of D permits evaluation at 10^-17. pi>=3 and log term<80.
    assert exp_lower(80) > 1+F(10**34, 4)
    shape_error = F(4*80+48, 3*10**17)
    cdf_error = (shape_error+p_plus)/b_minus+p_plus
    error_allowance = F(1, 10**14)
    assert cdf_error < error_allowance
    deadline = F(10**17)
    cdf_lo = 1-1/exp_lower(deadline/mean_hi)-error_allowance
    cdf_hi = 1-1/exp_upper(deadline/mean_lo)+error_allowance

    # Independent native acquisition protocol for five-bit single-flip cells.
    # A source within eta/2 leaves room for statistical admission at eta.
    h = 32*n-80
    gamma = eta/5
    rate_floor = F(9, 10)
    quota = 8*10**9
    horizon = 11*10**11
    assert (1+eta/2)*(1+gamma)/(1-gamma) <= 1+eta
    assert (1-eta/2)*(1-gamma)/(1+gamma) >= 1-eta
    exponent = rate_floor*quota*gamma**2/3
    assert exponent > 18
    failure_rate_upper = F(2*h)/exp_lower(18)
    assert failure_rate_upper < F(1, 10000)
    context_floor = F(3, 100)
    assert 1/(32*eu) > context_floor
    assert horizon > 4*quota/context_floor
    assert gap_lo*context_floor*horizon/8 > 100
    # Initial-density prefactor <=2^41 and H<2^12.
    assert h < 2**12
    failure_occupation_upper = F(2**53)/exp_lower(100)
    assert failure_occupation_upper < F(1, 10000)
    native_jump_upper = (1+eta)*n*horizon

    out = dict(
        status='Conditional theorem instantiation; no high-precision 80-bit native record was generated.',
        all_rational_checks_passed=True,
        source_cutoff='51ce47ce39f976517d60e2f87bbe280b651f6056',
        target='kernel of the saved 64x80 systematic binary parity matrix',
        target_states=2**16, target_stationary_mass_reference=str(p0),
        native_class='single-bit flips; supplied dependence range at most five consecutive bits; same positive support; time-homogeneous finite CTMC',
        reference='independent flips at unit rate',
        acquired_rate_box_required=str(eta),
        stationary_log_bound=str(u), flow_log_bound=str(v), actual_gap_lower=str(gap_lo),
        mean_reference_exact=str(mean0), mean_reference_decimal=outward(mean0, 6),
        native_mean_ratio_lower='4/5', native_mean_ratio_upper='28/25',
        native_mean_lower=outward(mean_lo, 6), native_mean_upper=outward(mean_hi, 6, True),
        cdf_shape_error_upper='1/100000000000000',
        deadline=int(deadline), deadline_cdf_lower=outward(cdf_lo),
        deadline_cdf_upper=outward(cdf_hi, upper=True),
        initial_law='actual stationary law conditioned on being outside the code',
        acquisition=dict(status='proved resource budget, not an executed source measurement',
                         number_of_cells=h, max_context_bits=5, quota_per_cell=quota,
                         relative_rate_estimation_tolerance=str(gamma),
                         true_distance_margin_for_completion_and_admission=str(eta/2),
                         deterministic_native_horizon=horizon,
                         expected_observed_native_jumps_upper=str(native_jump_upper),
                         confidence_lower='4999/5000 = 0.9998',
                         native_horizon_unit='inverse of the reference single-bit flip rate',
                         unknown_null_or_hardware_work_included=False),
        reference_cost='65536 codewords enumerated; exact weight transform; independent 40000-trial short receiver retained separately',
        caveats=['The rate support/dependence promise is not learned from finite data.',
                 'The favorable reference quotient is not assumed for the actual source.',
                 'The rate confidence and quota guarantee concern ideal complete ordered observations.',
                 'No physical performance, current-state hazard, or historical-priority claim is made.'])
    (here/'coded_target_certificate.json').write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps(out, indent=2))


if __name__ == '__main__':
    main()
