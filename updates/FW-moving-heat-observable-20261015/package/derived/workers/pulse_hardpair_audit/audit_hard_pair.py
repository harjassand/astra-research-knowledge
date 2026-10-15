"""Independent exact reconstruction of the frozen positive-RC pair.

No author code, numerical LP, binary float, scipy, mpmath, or interval package
is used.  Inputs are copied EIS decimal strings and copied rational atoms.
The exponential enclosure uses a positive Taylor sum with a geometric tail.
Every intermediate rounding is an explicit rational floor or ceiling.
"""
from pathlib import Path
from fractions import Fraction as F
import csv
import hashlib
import json
from math import comb, factorial

HERE = Path(__file__).resolve().parent
INPUT = HERE / "input_snapshot_final"
WITNESS = INPUT / "verified_hard_pair.json"
DATA = INPUT / "cell_001_eis.csv"
R = F(100)
F0 = F(1, 100)
EPS = F(1, 10)
GRID = 10**60
OUT = 10**25
ENCLOSURES_CHECKED = []


def floorq(x, den=GRID):
    return F((x.numerator * den) // x.denominator, den)


def ceilq(x, den=GRID):
    return -floorq(-x, den)


def decimal(x, digits=25):
    den = 10**digits
    assert x.denominator and (x * den).denominator == 1
    n = (x * den).numerator
    return ("-" if n < 0 else "") + str(abs(n) // den) + "." + str(abs(n) % den).zfill(digits)


def display_interval(lo, hi):
    assert lo <= hi
    return [decimal(floorq(lo, OUT)), decimal(ceilq(hi, OUT))]


def check_author_enclosure(bounds, lo, hi, label):
    alo, ahi = (F(str(b)) for b in bounds)
    assert alo <= lo <= hi <= ahi, label
    ENCLOSURES_CHECKED.append(label)


def atan_interval(inv, n):
    """Alternating arctan series; the next term brackets the remainder."""
    s = sum((F((-1)**k, (2*k + 1)*inv**(2*k + 1)) for k in range(n)), F(0))
    nxt = F((-1)**n, (2*n + 1)*inv**(2*n + 1))
    return min(s, s+nxt), max(s, s+nxt)


def pi_interval():
    # Machin identity pi = 16 arctan(1/5) - 4 arctan(1/239).
    a, b = atan_interval(5, 80), atan_interval(239, 30)
    return floorq(16*a[0] - 4*b[1]), ceilq(16*a[1] - 4*b[0])


EXP_STATS = {"positive_taylor_calls": 0, "largest_degree": 0, "large_u_caps": 0}


def exp_negative_at(u):
    """Exact rational enclosure of exp(-u), for an exact rational u >= 0."""
    assert u >= 0
    if u == 0:
        return F(1), F(1)
    if u >= 120:
        # e > 2, hence exp(-u) <= exp(-120) < 2**(-120).
        EXP_STATS["large_u_caps"] += 1
        return F(0), F(1, 2**120)
    EXP_STATS["positive_taylor_calls"] += 1
    tlo = thi = slo = shi = F(1)
    for n in range(1, 1001):
        tlo, thi = floorq(tlo*u/n), ceilq(thi*u/n)
        slo, shi = slo+tlo, shi+thi
        if n+2 <= u:
            continue
        # For k >= n+1, successive positive Taylor terms have ratio at
        # most u/(n+2).  thi bounds the n-th term from above.
        nxt = ceilq(thi*u/(n+1))
        tail = nxt / (1-u/F(n+2))
        elo, ehi = F(1)/(shi+tail), F(1)/slo
        if ehi-elo <= F(1, 10**48):
            EXP_STATS["largest_degree"] = max(EXP_STATS["largest_degree"], n)
            return elo, ehi
    raise AssertionError("Taylor series failed to reach its certified target")


def exp_negative_interval(lo, hi):
    assert 0 <= lo <= hi
    return exp_negative_at(hi)[0], exp_negative_at(lo)[1]


def w(x):
    return (1+x)/(1+x*x) - x/(1+R*R*x*x)


def unpack(atom):
    s = F(atom["s_exact"])
    mass = F(atom["mass_mohm_exact"])
    assert 0 < s < 1 and mass > 0
    x = s/(1-s)
    assert w(x) > 0
    return {"s": s, "x": x, "mass": mass, "resistance": mass/w(x)}


def eis(atom, f):
    z = f/F0 * atom["x"]
    real = atom["resistance"]/(1+z*z)
    return real, -z*real


def q_interval(atoms, t, api):
    lo = hi = F(0)
    for atom in atoms:
        ulo, uhi = api[0]*t/atom["x"], api[1]*t/atom["x"]
        elo, ehi = exp_negative_interval(ulo, uhi)
        lo += atom["resistance"]*(1-ehi)
        hi += atom["resistance"]*(1-elo)
    return lo, hi


def hidden_d_interval(t, delta, amp):
    elo, ehi = exp_negative_interval(delta[0]*t, delta[1]*t)
    return amp*(1-ehi)**2, amp*(1-elo)**2


def primitive_interval(t, delta, amp):
    if t == 0:
        return F(0), F(0)
    e1 = exp_negative_interval(delta[0]*t, delta[1]*t)
    e2 = exp_negative_interval(2*delta[0]*t, 2*delta[1]*t)
    p1 = ((1-e1[1])/delta[1], (1-e1[0])/delta[0])
    p2 = ((1-e2[1])/(2*delta[1]), (1-e2[0])/(2*delta[0]))
    return amp*(t-2*p1[1]+p2[0]), amp*(t-2*p1[0]+p2[1])


def ramp_interval(horizon, rho, delta, amp):
    if rho == 0:
        return hidden_d_interval(horizon, delta, amp)
    assert rho > 0
    a = primitive_interval(horizon, delta, amp)
    b = primitive_interval(max(F(0), horizon-rho), delta, amp)
    return (a[0]-b[1])/rho, (a[1]-b[0])/rho


def main():
    obj = json.loads(WITNESS.read_text())
    assert hashlib.sha256(DATA.read_bytes()).hexdigest() == obj["data_sha256"]
    with DATA.open(newline="") as fh:
        rows = [[F(s) for s in row] for row in list(csv.reader(fh))[1:]]
    full_count = len(rows)
    violation = max((1000*(zh-zl), fh, fl)
                    for fh, zh, _ in rows for fl, zl, _ in rows if fh > fl)
    assert violation[0]/2 == F("0.515")
    rows = [(f, 1000*zr, 1000*zi) for f, zr, zi in rows if f <= 1000]
    assert len(rows) == 58 == obj["n_eis_frequencies"]
    baseline = [unpack(a) for a in obj["common_baseline_components"]]
    assert len(baseline) == 19
    ell = F(obj["common_inductance_coefficient_mohm_exact"])
    assert ell > 0
    amp = F(obj["A_mohm_exact"])
    assert amp == 125 and F(obj["d_exact"]) == F(1, 40)
    fmax = max(f for f, _, _ in rows)
    pi = pi_interval()
    api = (2*F0*pi[0], 2*F0*pi[1])
    delta = (api[0]/40, api[1]/40)
    # mOhm divided by 2*pi*Hz gives mH, hence the /1000 for H.
    inductance = (ell/(2000*fmax*pi[1]), ell/(2000*fmax*pi[0]))
    check_author_enclosure(obj["delta_per_second_interval"], *delta, "delta")
    check_author_enclosure(obj["common_inductance_H_interval"], *inductance, "inductance")
    observed = {f: (zr, zi) for f, zr, zi in rows}
    observed_mass = observed[F0][0] - observed[F0][1] + observed[F(1)][1]/100
    mass_max = observed_mass + EPS*F(201, 100)
    assert observed_mass == F("71.2258") and mass_max == F("71.4268")
    result = {
        "status": "PASS: independent exact-rational model audit; physical validation absent",
        "dependencies": "Python standard library only; no author code imported or executed",
        "input_sha256": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in (WITNESS, DATA)},
        "source_rows_total": full_count,
        "full_band_monotonic_real_part_error_floor_mohm_exact": str(violation[0]/2),
        "full_band_floor_frequency_pair_hz_exact": [str(violation[1]), str(violation[2])],
        "eis_rows_checked": len(rows),
        "component_constraints_checked": 2*len(rows)*2,
        "baseline_positive_atoms": len(baseline),
        "pi_interval": display_interval(*pi),
        "delta_per_second_interval": display_interval(*delta),
        "positive_common_inductance_H_interval": display_interval(*inductance),
        "observed_normalization_mohm_exact": str(observed_mass),
        "normalization_mass_upper_mohm_exact": str(mass_max),
        "models": {},
    }
    qq = {}
    for name in ("minus", "plus"):
        hidden = unpack(obj["models"][name]["hidden_component"])
        assert hidden["x"] == (20 if name == "minus" else 40)
        assert hidden["resistance"] == (amp if name == "minus" else 2*amp)
        atoms = baseline+[hidden]
        residuals = []
        for f, zr, zi in rows:
            rs = [eis(a, f) for a in atoms]
            pr = sum((v[0] for v in rs), F(0))
            pi_ = sum((v[1] for v in rs), F(0)) + ell*f/fmax
            residuals.extend([(abs(pr-zr), f, "real"), (abs(pi_-zi), f, "imag")])
        err, atf, component = max(residuals)
        assert err < EPS
        assert err == F(obj["models"][name]["max_component_error_mohm_exact"])
        mass = sum((a["mass"] for a in atoms), F(0))
        assert mass == F(obj["models"][name]["positive_normalized_mass_mohm_exact"])
        assert mass <= mass_max
        check_author_enclosure(obj["models"][name]["max_component_error_mohm_outward"], err, err, name+".EIS_error")
        check_author_enclosure(obj["models"][name]["positive_normalized_mass_mohm_outward"], mass, mass, name+".normalization_mass")
        # The normalized mass identity is checked on actual reconstructed Z,
        # including exact cancellation of the common inductance.
        def pred(f):
            rs = [eis(a, f) for a in atoms]
            return sum((v[0] for v in rs), F(0)), sum((v[1] for v in rs), F(0))+ell*f/fmax
        p0, p1 = pred(F0), pred(F(1))
        assert p0[0]-p0[1]+p1[1]/100 == mass
        qi = {t: q_interval(atoms, F(t), api) for t in (10, 1000)}
        for t in (10, 1000):
            check_author_enclosure(obj["models"][name][f"Q{t}_mohm_interval"], *qi[t], name+f".Q{t}")
        qq[name] = qi
        assert qi[1000][1] < 200 if name == "minus" else qi[1000][0] > 200
        result["models"][name] = {
            "all_original_resistances_positive": True,
            "hidden_resistance_mohm_exact": str(hidden["resistance"]),
            "hidden_a_tau_exact": str(hidden["x"]),
            "max_component_error_mohm_interval": display_interval(err, err),
            "max_error_frequency_hz_exact": str(atf),
            "max_error_component": component,
            "strict_eis_feasibility_margin_mohm_interval": display_interval(EPS-err, EPS-err),
            "positive_normalized_mass_mohm_interval": display_interval(mass, mass),
            "Q10_mohm_interval": display_interval(*qi[10]),
            "Q1000_mohm_interval": display_interval(*qi[1000]),
        }
    gaps = {}
    for t in (1, 10, 30, 60, 1000):
        di = hidden_d_interval(F(t), delta, amp)
        gaps[str(t)] = {
            "exact_peak_bound_per_max_current_mohm_interval": display_interval(*di),
            "noise_budget_per_max_current_sufficient_to_hide_mohm_interval": display_interval(di[0]/2, di[1]/2),
        }
    gap1000 = hidden_d_interval(F(1000), delta, amp)
    check_author_enclosure(obj["Q1000_separation_mohm_interval"], *gap1000, "target_gap1000")
    check_author_enclosure(obj["absolute_error_lower_bound_if_indistinguishable_mohm_interval"], gap1000[0]/2, gap1000[1]/2, "minimax_if_hidden")
    assert qq["plus"][1000][0]-qq["minus"][1000][1] <= gap1000[1]
    assert qq["plus"][1000][1]-qq["minus"][1000][0] >= gap1000[0]
    result["hard_pair_gap_by_seconds"] = gaps
    result["minimax_Q1000_absolute_error_if_hidden_mohm_interval"] = display_interval(gap1000[0]/2, gap1000[1]/2)
    result["author_experiments_reconstructed"] = []
    for ex in obj["experiments"]:
        h, rho = F(ex["horizon_seconds"]), F(ex["ramp_seconds"])
        sep = ramp_interval(h, rho, delta, amp)
        check_author_enclosure(ex["optimal_full_path_separation_per_max_current_mohm_interval"], *sep, f"experiment_H{h}_rho{rho}")
        check_author_enclosure(ex["minimum_eta_to_hide_pair_mohm_interval"], sep[0]/2, sep[1]/2, f"experiment_eta_H{h}_rho{rho}")
        result["author_experiments_reconstructed"].append({
            "horizon_seconds_exact": str(h),
            "ramp_seconds_exact": str(rho),
            "optimal_path_separation_per_max_current_mohm_interval": display_interval(*sep),
            "minimum_eta_to_hide_pair_mohm_interval": display_interval(sep[0]/2, sep[1]/2),
        })
    result["critical_duration_brackets_independently_verified"] = []
    for rec in obj["critical_duration"]:
        eta, rho = F(rec["eta_mohm_exact"]), F(rec["ramp_seconds"])
        bracket = rec["duration_for_possible_certain_pair_discrimination"]
        left, right = F(bracket["lower_exact"]), F(bracket["upper_exact"])
        check_author_enclosure(bracket["seconds_outward"], left, right, f"critical_eta{eta}_rho{rho}")
        lower_signal = ramp_interval(left, rho, delta, amp)
        upper_signal = ramp_interval(right, rho, delta, amp)
        assert lower_signal[1] < 2*eta < upper_signal[0]
        result["critical_duration_brackets_independently_verified"].append({
            "eta_mohm_exact": str(eta),
            "ramp_seconds_exact": str(rho),
            "bracket_seconds": display_interval(left, right),
            "strict_lower_margin_mohm_interval": display_interval(2*eta-lower_signal[1], 2*eta-lower_signal[0]),
            "strict_upper_margin_mohm_interval": display_interval(upper_signal[0]-2*eta, upper_signal[1]-2*eta),
        })
    checks = 0
    for n in range(1, 13):
        for z in (F(0), F(1, 100), F(1, 3), F(1), F(7, 3), F(100)):
            value = sum(((-1)**(k+1)*comb(n, k)*F(k)/(z+k) for k in range(1, n+1)), F(0))
            denominator = F(1)
            for k in range(1, n+1):
                denominator *= z+k
            assert value == F(factorial(n))/denominator
            checks += 1
        for x in (F(0), F(1, 100), F(1, 3), F(1, 2), F(99, 100), F(1)):
            step = sum(((-1)**(k+1)*comb(n, k)*(1-x**k) for k in range(1, n+1)), F(0))
            impulse = sum(((-1)**(k+1)*comb(n, k)*k*x**k for k in range(1, n+1)), F(0))
            assert step == (1-x)**n
            assert impulse == n*x*(1-x)**(n-1)
            checks += 2
    result["binomial_family_exact_rational_diagnostics"] = checks
    result["corrected_author_decimal_enclosures_verified"] = ENCLOSURES_CHECKED
    result["corrected_author_decimal_enclosures_count"] = len(ENCLOSURES_CHECKED)
    result["exp_enclosure_statistics"] = EXP_STATS
    (HERE / "INDEPENDENT_RESULTS.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
