#!/usr/bin/env python3
"""Independent numerical audit of the published six-species photocycle.

The rates, species ordering, branch equations, initial concentrations, and RF
schedule are transcribed from the primary sources cited in SOURCES.md.  The
script uses only Python's standard library.  Concentrations are micromolar,
time is seconds, and the bimolecular constants are converted to µM^-1 s^-1.
"""
from __future__ import annotations

from dataclasses import dataclass
import json
import math
from pathlib import Path


@dataclass(frozen=True)
class Rates:
    label: str
    lis_ref: float
    ksr: float
    ktr: float
    kisc: float
    kred: float
    kox: float
    kdis: float

    def light_rate(self, i520: float) -> float:
        # The code's 1652 s^-1 reference corresponds to 1.7 W cm^-2.
        return self.lis_ref * i520 / 1.7

    def a(self, i520: float) -> float:
        return self.kisc * self.light_rate(i520) / (self.ksr + self.kisc)


TABLE1 = Rates("JACS Table 1 converted", 1652.0, 2.5e8, 224.0, 1.85e5,
               50.0, 3375e-6, 5000.0)
REPO = Rates("authors MATLAB repository default", 1652.0, 2.5e8, 224.0,
             185497.528691897, 50.5406, 0.003675, 5000.0)

Y0 = (50.0, 0.0, 0.0, 20.0, 330.0, 0.0)  # G,T,R,F,H,Q in µM
BETA0 = 0.68
DBETA_PER_MT = 0.117


def rhs(y: tuple[float, ...], beta: float, p: Rates, i520: float) -> tuple[float, ...]:
    g, t, r, f, h, q = y
    a = p.a(i520)
    u = beta * p.kred * h * t
    v = p.kox * f * r
    w = p.kdis * q * q
    return (
        -a * g + (p.ktr + (1.0 - beta) * p.kred * h) * t + v,
        a * g - p.ktr * t - p.kred * h * t,
        u - v,
        -v + w,
        -u + w,
        u - 2.0 * w + v,
    )


def rk4_step(y: tuple[float, ...], beta: float, p: Rates, i520: float,
             dt: float) -> tuple[float, ...]:
    k1 = rhs(y, beta, p, i520)
    y2 = tuple(x + 0.5 * dt * k for x, k in zip(y, k1))
    k2 = rhs(y2, beta, p, i520)
    y3 = tuple(x + 0.5 * dt * k for x, k in zip(y, k2))
    k3 = rhs(y3, beta, p, i520)
    y4 = tuple(x + dt * k for x, k in zip(y, k3))
    k4 = rhs(y4, beta, p, i520)
    return tuple(x + dt * (a + 2*b + 2*c + d) / 6.0
                 for x, a, b, c, d in zip(y, k1, k2, k3, k4))


def state_from_q(q: float, beta: float, p: Rates, i520: float):
    c = p.kdis / p.kox
    disc = math.sqrt((q - 40.0)**2 + 8.0 * c * q*q)
    f = (40.0 - q + disc) / 4.0
    r = 2.0 * f + q - 40.0
    h = 350.0 - f - q
    a = p.a(i520)
    C = p.ktr + p.kred * h
    Am = 50.0 - r
    g = Am * C / (a + C)
    t = Am * a / (a + C)
    beta_q = p.kdis * q*q * (a + C) / (a * p.kred * h * Am)
    return (g, t, r, f, h, q), beta_q


def steady(beta: float, p: Rates, i520: float):
    # Find a physical root on the small-Q branch used by the reported fit.
    lo, hi = 1e-12, 0.0383
    blo = state_from_q(lo, beta, p, i520)[1]
    bhi = state_from_q(hi, beta, p, i520)[1]
    if not (blo < beta < bhi):
        raise ValueError(f"failed root bracket: beta range {blo}, {bhi}")
    for _ in range(100):
        mid = (lo + hi) / 2.0
        _, bm = state_from_q(mid, beta, p, i520)
        if bm < beta:
            lo = mid
        else:
            hi = mid
    q = (lo + hi) / 2.0
    y, _ = state_from_q(q, beta, p, i520)
    err = max(abs(z) for z in rhs(y, beta, p, i520))
    return y, err


def rf_is_on(t: float) -> bool:
    return 0.0 <= t < 5.0 or 10.0 <= t < 15.0


def pulse_beta(t: float, beta_off: float, beta_on: float) -> float:
    # Fig. 2G / Supplementary Data Fig. 6: RF on for 0-5 and 10-15 s.
    return beta_on if rf_is_on(t) else beta_off


def invariant_values(y):
    g, t, r, f, h, q = y
    return (g+t+r, f+h+q, g+t+2*f+q)


def simulate_pair(y_pulse, y_control, p: Rates, i520: float, beta_low: float,
                  beta_high: float, duration: float, dt: float):
    n = round(duration / dt)
    if abs(n * dt - duration) > 1e-10:
        raise ValueError("dt must divide duration")
    yp, yc = tuple(y_pulse), tuple(y_control)
    rows = []
    sample_stride = round(0.1 / dt)
    for j in range(n + 1):
        t = j * dt
        if j % sample_stride == 0:
            dG = yp[0] - yc[0]
            dR = yp[2] - yc[2]
            invp = invariant_values(yp)
            invc = invariant_values(yc)
            rows.append({"t": t, "G_pulse": yp[0], "G_control": yc[0],
                         "R_pulse": yp[2], "R_control": yc[2],
                         "dG": dG, "dR": dR,
                         "rho_critical": (-dG / dR if dR > 1e-15 else None),
                         "rf_on": rf_is_on(t),
                         "invariant_error_inf": max(abs(invp[0]-50.0), abs(invp[1]-350.0),
                                                     abs(invp[2]-90.0), abs(invc[0]-50.0),
                                                     abs(invc[1]-350.0), abs(invc[2]-90.0)),
                         "min_species": min(min(yp), min(yc))})
        if j == n:
            break
        beta = pulse_beta(t + dt/2.0, beta_low, beta_high)
        yp = rk4_step(yp, beta, p, i520, dt)
        yc = rk4_step(yc, beta_low, p, i520, dt)
    return rows


def extrema(rows, predicate, key):
    xs = [r[key] for r in rows if predicate(r) and r[key] is not None]
    if not xs:
        return None
    return {"min": min(xs), "max": max(xs)}


def observable_fractional_changes(g0: float, r0: float, dg: float, dr: float):
    out = {}
    for rho in (0.0, 0.5, 1.0, 2.0, 10.0):
        out[str(rho)] = (dg + rho * dr) / (g0 + rho * r0)
    # Limit as the detector becomes radical-only; any positive constant
    # background lowers this bound.
    out["rho_infinity"] = dr / r0 if r0 > 0 else None
    return out


def run():
    result = {
        "source_parameter_conventions": {
            "table1": "kred=5e7 M^-1 s^-1 = 50 µM^-1 s^-1; kox=3375 M^-1 s^-1 = 0.003375 µM^-1 s^-1; kdis=5e9 M^-1 s^-1 = 5000 µM^-1 s^-1",
            "repository": "MFE_kinetic_model.m default vector transcribed exactly",
            "beta_law": "beta_sep = 0.68 + 0.117*B1_mT, with B1=0.3 mT giving 0.7151",
            "observable_family": "Fdet = G + rho*R + constant; rho=0 is source's nonfluorescent-radical map",
            "initial_state": list(Y0),
            "invariants_initial": {"M=G+T+R": 50.0, "L=F+H+Q": 350.0,
                                    "I=G+T+2F+Q": 90.0},
        },
        "steady": [],
        "transient_from_source_initial_conditions": [],
        "transient_from_low_beta_photostationary_state": [],
        "complement_counterexample": [],
    }
    for p in (TABLE1, REPO):
        for i520 in (0.5, 1.7, 3.8):
            low, e0 = steady(BETA0, p, i520)
            high, e1 = steady(BETA0 + DBETA_PER_MT * 0.3, p, i520)
            lower_sep, ecomp = steady(BETA0 - DBETA_PER_MT * 0.3, p, i520)
            complement_beta_low, ec0 = steady(1.0 - BETA0, p, i520)
            complement_beta_high, ec1 = steady(1.0 - (BETA0 + DBETA_PER_MT*0.3), p, i520)
            dG = high[0] - low[0]
            dR = high[2] - low[2]
            result["steady"].append({
                "rates": p.label, "I520_W_cm2": i520,
                "a_s-1": p.a(i520), "beta_low": BETA0,
                "beta_high_B1_0.3mT": BETA0 + DBETA_PER_MT * 0.3,
                "low_state_G_T_R_F_H_Q_uM": low,
                "high_state_G_T_R_F_H_Q_uM": high,
                "delta_G_uM": dG, "delta_R_uM": dR,
                "rho_threshold_for_positive_steady_signal": -dG/dR,
                "delta_G_over_G_percent": 100*dG/low[0],
                "no_background_fixed_emissivity_fractional_changes":
                    observable_fractional_changes(low[0], low[2], dG, dR),
                "radical_only_limit_percent": 100*dR/low[2],
                "low_root_rhs_inf_norm": e0, "high_root_rhs_inf_norm": e1,
                "initial_Gdot_change_at_equilibrium_uM_s": -(
                    DBETA_PER_MT * 0.3 * p.kred * low[4] * low[1]),
            })
            result["complement_counterexample"].append({
                "rates": p.label, "I520_W_cm2": i520,
                "same_beta_i_with_slope_reversed": {
                    "beta_sep_off": BETA0,
                    "beta_sep_RF_on": BETA0 - DBETA_PER_MT*0.3,
                    "delta_G_uM": lower_sep[0] - low[0],
                    "delta_G_over_G_percent": 100*(lower_sep[0]-low[0])/low[0],
                    "states_off_G_R_uM": [low[0], low[2]],
                    "states_RF_on_G_R_uM": [lower_sep[0], lower_sep[2]],
                    "rhs_residuals_inf": [e0, ecomp],
                },
                "Nature_beta_reinterpreted_as_recombination_fraction": {
                    "beta_recomb_off": BETA0,
                    "beta_recomb_RF_on": BETA0 + DBETA_PER_MT*0.3,
                    "implied_beta_sep_off": 1.0-BETA0,
                    "implied_beta_sep_RF_on": 1.0-(BETA0+DBETA_PER_MT*0.3),
                    "delta_G_uM": complement_beta_high[0]-complement_beta_low[0],
                    "delta_G_over_G_percent":
                        100*(complement_beta_high[0]-complement_beta_low[0])/complement_beta_low[0],
                    "states_off_G_R_uM": [complement_beta_low[0], complement_beta_low[2]],
                    "states_RF_on_G_R_uM": [complement_beta_high[0], complement_beta_high[2]],
                    "rhs_residuals_inf": [ec0, ec1],
                },
            })

            # The endpoint and time-domain checks use low/high illumination
            # plus the repository's exact defaults at the higher intensity.
            dynamic_case = ((p == TABLE1 and i520 in (0.5, 3.8))
                            or (p == REPO and i520 == 3.8))
            if dynamic_case:
                # The exact S8 initial condition and published 0-5/10-15 s RF train.
                trans = simulate_pair(Y0, Y0, p, i520, BETA0,
                                      BETA0 + DBETA_PER_MT*0.3, 20.0, 1e-4)
                on = lambda row: row["rf_on"] and row["t"] <= 5.0
                result["transient_from_source_initial_conditions"].append({
                    "rates": p.label, "I520_W_cm2": i520,
                    "dt_s": 1e-4, "first_pulse_delta_G_extrema_uM": extrema(trans, on, "dG"),
                    "sampled_invariant_error_inf_uM": max(r["invariant_error_inf"] for r in trans),
                    "minimum_sampled_species_uM": min(r["min_species"] for r in trans),
                    "first_pulse_delta_R_extrema_uM": extrema(trans, on, "dR"),
                    "first_pulse_rho_threshold_extrema": extrema(trans, on, "rho_critical"),
                    "radical_only_fractional_delta_extrema": extrema(
                        [dict(r, radical_only=(r["dR"]/r["R_control"] if r["R_control"]>0 else None))
                         for r in trans], on, "radical_only"),
                    "max_on_pulse_fractional_change_by_rho": {
                        str(rho): max((r["dG"]+rho*r["dR"])/(r["G_control"]+rho*r["R_control"])
                                      for r in trans if on(r))
                        for rho in (0.0, 0.5, 1.0, 2.0, 10.0)
                    },
                    "samples_s": [next(r for r in trans if abs(r["t"]-t)<1e-10)
                                  for t in (0.1, 1.0, 2.5, 5.0)],
                })

                # Same RF pulse after equilibration under green light at beta_i.
                trans_eq = simulate_pair(low, low, p, i520, BETA0,
                                         BETA0 + DBETA_PER_MT*0.3, 20.0, 1e-4)
                on_eq = lambda row: row["rf_on"] and row["t"] <= 5.0
                result["transient_from_low_beta_photostationary_state"].append({
                    "rates": p.label, "I520_W_cm2": i520,
                    "dt_s": 1e-4, "first_pulse_delta_G_extrema_uM": extrema(trans_eq, on_eq, "dG"),
                    "sampled_invariant_error_inf_uM": max(r["invariant_error_inf"] for r in trans_eq),
                    "minimum_sampled_species_uM": min(r["min_species"] for r in trans_eq),
                    "first_pulse_delta_R_extrema_uM": extrema(trans_eq, on_eq, "dR"),
                    "first_pulse_rho_threshold_extrema": extrema(trans_eq, on_eq, "rho_critical"),
                    "radical_only_fractional_delta_extrema": extrema(
                        [dict(r, radical_only=(r["dR"]/r["R_control"] if r["R_control"]>0 else None))
                         for r in trans_eq], on_eq, "radical_only"),
                    "max_on_pulse_fractional_change_by_rho": {
                        str(rho): max((r["dG"]+rho*r["dR"])/(r["G_control"]+rho*r["R_control"])
                                      for r in trans_eq if on_eq(r))
                        for rho in (0.0, 0.5, 1.0, 2.0, 10.0)
                    },
                    "samples_s": [next(r for r in trans_eq if abs(r["t"]-t)<1e-10)
                                  for t in (0.1, 1.0, 2.5, 5.0)],
                })

                if p == TABLE1 and i520 == 3.8:
                    # Rescue checks: (i) same separation-fraction baseline,
                    # corrected sign of its RF change; (ii) Nature's numeric
                    # parameter relabelled as the recombination fraction.
                    alternatives = [
                        ("same beta_i, negative separation-fraction increment",
                         BETA0, BETA0 - DBETA_PER_MT*0.3),
                        ("Nature beta interpreted as recombination fraction",
                         1.0-BETA0, 1.0-(BETA0+DBETA_PER_MT*0.3)),
                    ]
                    for label, beta_off_alt, beta_on_alt in alternatives:
                        alt = simulate_pair(Y0, Y0, p, i520, beta_off_alt,
                                            beta_on_alt, 5.0, 1e-4)
                        s5 = next(r for r in alt if abs(r["t"]-5.0)<1e-10)
                        result["complement_counterexample"].append({
                            "rates": p.label, "I520_W_cm2": i520, "mapping": label,
                            "beta_sep_off": beta_off_alt, "beta_sep_on": beta_on_alt,
                            "at_t5_G_control_uM": s5["G_control"],
                            "at_t5_G_RF_uM": s5["G_pulse"],
                            "at_t5_delta_G_uM": s5["dG"],
                            "at_t5_fractional_delta_G": s5["dG"]/s5["G_control"],
                            "at_t5_R_control_uM": s5["R_control"],
                            "at_t5_R_RF_uM": s5["R_pulse"],
                            "at_t5_fractional_delta_R": s5["dR"]/s5["R_control"],
                        })
    out = Path(__file__).with_name("sign_audit_results.json")
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(out)
    print(json.dumps({k: result[k] for k in ("steady", "transient_from_source_initial_conditions",
                                              "transient_from_low_beta_photostationary_state")}, indent=2))


if __name__ == "__main__":
    run()
