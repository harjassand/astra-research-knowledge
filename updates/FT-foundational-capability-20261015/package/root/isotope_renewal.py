"""Exact model formulas and bounded arithmetic checks, not physical validation."""
import json
import math
from pathlib import Path

P = 0.01109
# Susi 2016 supplementary Table 1 central experimental estimates in millibarn.
TABLE = {90: (10.9, 2.0), 95: (56.6, 2.1), 100: (328.0, 13.3)}
MB_TO_NM2 = 1e-13
ELECTRONVOLT_J = 1.602176634e-19


def renewal(p, sigma_l, sigma_h, target):
    d = math.log(target * (1 - p) / (p * (1 - target))) / (sigma_l - sigma_h)
    eh, el = math.exp(-sigma_h * d), math.exp(-sigma_l * d)
    a = p * eh + (1 - p) * el
    one_dose = (p * (-math.expm1(-sigma_h * d)) / sigma_h if sigma_h else p * d)
    one_dose += (1 - p) * (-math.expm1(-sigma_l * d)) / sigma_l
    return {"screening_fluence_e_per_nm2": d, "success_probability_per_attempt": a,
            "heavy_fraction_accepted": p * eh / a,
            "expected_attempts": 1 / a, "expected_refills": (1 - a) / a,
            "expected_total_fluence_e_per_nm2": one_dose / a,
            "refill_mass_balance_lower_bound": (target - p) / p}


def discrete_blind(p, sigma_l, sigma_h, steps):
    q = p
    for d in steps:
        q = q * math.exp(-sigma_h * d) + p * (
            1 - q * math.exp(-sigma_h * d) - (1 - q) * math.exp(-sigma_l * d))
    return q


def main():
    rows = []
    checks = 0
    for kv, (sl_mb, sh_mb) in TABLE.items():
        sl, sh = sl_mb * MB_TO_NM2, sh_mb * MB_TO_NM2
        b = P * sl + (1 - P) * sh
        ceiling = P * sl / b
        for target in (.2, .5, .9, .99):
            r = renewal(P, sl, sh, target)
            assert abs(r["heavy_fraction_accepted"] - target) < 2e-15
            assert r["expected_refills"] >= r["refill_mass_balance_lower_bound"] - 1e-12
            r.update({"beam_kV": kv, "sigma_L_millibarn": sl_mb,
                      "sigma_H_millibarn": sh_mb, "target_heavy_fraction": target,
                      "blind_ceiling": ceiling,
                      "incident_kinetic_energy_J_per_nm2": r["expected_total_fluence_e_per_nm2"] * kv * 1000 * ELECTRONVOLT_J,
                      "attempt_cap_for_99pct_output_yield": math.ceil(math.log(.01) / math.log1p(-r["success_probability_per_attempt"]))})
            rows.append(r)
            checks += 2
        # A finite set of staged blind protocols must lie below immediate refill.
        for dose in (1e9, 1e11, 1e12, 1e13):
            ideal = ceiling - (ceiling - P) * math.exp(-b * dose)
            for count in (1, 2, 10, 100):
                got = discrete_blind(P, sl, sh, [dose / count] * count)
                assert got <= ideal + 2e-14
                checks += 1
    out = {"status": "bounded arithmetic only; model assumptions supplied",
           "p_planning_not_measured_refill": P,
           "table_source": "Susi et al. 2016 supplementary Table 1 central estimates",
           "source_uncertainty": "not propagated; point calculations are not covered physical predictions",
           "incident_energy_note": "electron kinetic energy through addressed area; not absorbed heat or complete instrument energy",
           "assertions_passed": checks, "rows": rows}
    dest = Path(__file__).with_name("isotope_renewal_results.json")
    dest.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({"assertions_passed": checks, "output": str(dest),
                      "95kV_90pct": next(r for r in rows if r["beam_kV"] == 95 and r["target_heavy_fraction"] == .9)}, indent=2))


if __name__ == "__main__":
    main()
