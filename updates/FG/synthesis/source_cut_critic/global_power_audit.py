#!/usr/bin/env python3
"""Independent exact same-envelope sharp-power family checks."""
from fractions import Fraction as F
from pathlib import Path
import json

from independent_audit import check_spd, invert, quad

BASE = Path(__file__).resolve().parent


def main():
    records = []
    for R in (3, 10, 100):
        for n in (10, 1000, 1000000):
            delta, T = F(1, n), F(n)
            c = delta * delta / T
            A0 = [[1 + c, -c], [-c, c]]
            check_spd(A0)
            G0 = invert(A0)
            assert G0 == [[F(1), F(1)], [F(1), 1 + 1 / c]]
            assert list(map(sum, A0)) == [F(1), F(0)]
            ell, u = [F(1), delta], [F(R), R * delta]
            sourceU, sourceL = [F(1), R * delta], [F(R), delta]
            assert all(lo <= x <= hi for lo, x, hi in zip(ell, sourceU, u))
            assert all(lo <= x <= hi for lo, x, hi in zip(ell, sourceL, u))
            tau0 = quad(G0, ell) / sum(ell)
            tauU = quad(G0, sourceU) / sum(sourceU)
            tauL = quad(G0, sourceL) / (R * sum(sourceL))
            assert tau0 == ((1 + delta) ** 2 + T) / (1 + delta)
            assert tauU == ((1 + R * delta) ** 2 + R * R * T) / (1 + R * delta)
            assert tauL == ((R + delta) ** 2 + T) / (R * (R + delta))
            assert F(1, R * R) <= tauL / tau0
            assert tauU / tau0 <= R * R
            assert tauU / tauL <= R ** 4
            records.append({"R": R, "delta": str(delta), "T": str(T),
                "tau0": str(tau0), "tauU": str(tauU), "tauL": str(tauL),
                "upper_over_baseline": str(tauU / tau0),
                "lower_over_baseline": str(tauL / tau0), "width": str(tauU / tauL),
                "upper_fraction_of_R_squared": str(tauU / (tau0 * R * R)),
                "lower_fraction_of_inverse_R_squared": str(tauL * R * R / tau0),
                "width_fraction_of_R_fourth": str(tauU / (tauL * R ** 4))})
    report = {"status": "PASS", "instances": len(records), "results": records,
              "scope": "same abstract CE source/form envelopes; source-dependent reversible rates; not a fixed min(weight)-edge law"}
    (BASE / "GLOBAL_POWER_RESULTS.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"status": "PASS", "instances": len(records),
        "last_record_decimal_ratios": {"upper_fraction_of_R_squared": float(F(records[-1]["upper_fraction_of_R_squared"])),
            "lower_fraction_of_inverse_R_squared": float(F(records[-1]["lower_fraction_of_inverse_R_squared"])),
            "width_fraction_of_R_fourth": float(F(records[-1]["width_fraction_of_R_fourth"]))}}, indent=2))


if __name__ == "__main__":
    main()
