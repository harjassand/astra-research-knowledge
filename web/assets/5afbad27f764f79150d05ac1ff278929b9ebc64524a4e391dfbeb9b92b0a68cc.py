#!/usr/bin/env python3
"""Exact arithmetic and frozen-import checks; not a quantum proof verifier."""
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
checks = []


def check(name, inequality):
    assert inequality, name
    checks.append({"name": name, "pass": True})


# Each root inequality is reduced to an exact rational/integer comparison.
check("ln2 Jensen lower bound suffices for 16/ln2<=24", 16 / F(2, 3) <= 24)
check("pair H coefficients fit 25(1+x)", 24 <= 25 and 16 <= 25)
check("sqrt(3/2)<5/4", F(3, 2) < F(25, 16))
check("5sqrt(2)<8", 50 < 64)
check("2sqrt(15)+8<16", 15 < 16)
check("Petz root constant fits 5/2", 2 < F(9, 4))
check("sqrt(5)/2<6/5", F(5, 4) < F(36, 25))
check("17^(1/8)<3/2", 17 * 2**8 < 3**8)
check("16+(6/5)(3/2)<18", 16 + F(6, 5) * F(3, 2) < 18)
check("18*2^(1/96)<19", 2 * 18**96 < 19**96)
check("sqrt(48)<7", 48 < 49)
check("beta coefficient bounded by 24", F(5, 2) * 7 + 5 < 24)
check("24^(1/192)<3/2", 24 * 2**192 < 3**192)
check("2^(193/192)<3", 2**193 < 3**192)
check("prefactor<1000", 152 * F(3, 2) * 3 < 1000)
check("smoother exponential coefficient<9", 8 * F(193, 192) < 9)
check("tail exponent equals -L/1536", F(1, 768) - F(9, 13824) == F(1, 1536))
check("tail ratio decreases in admissible range", F(193, 384) * 1536 == 772 < 13824)
check("1000e^-9<1 from e>5/2", 1000 * 2**9 < 5**9)
check("3sqrt(13824)<400", 9 * 13824 < 400**2)

imports = {
    "work/agents/broadcasting_proof_sol/cycle03_tree/UNIVERSAL_C4_CANDIDATE.txt":
        "1f666b1b6a6a8ee33191e656f4124489b1545206326157adc5bf9d6bc0555b90",
    "work/agents/broadcasting_proof_sol/cycle03_affinity_bridge/PAIR_BRIDGE_PROOF.txt":
        "1b0bc6f9069b5b59762f90289f419cdc189d5efd01538092088c26433598213a",
    "work/agents/spin1_anisotropic_sol/cycle03_centralization/CENTRALIZATION_AND_WEIGHTED_C4_AUDIT.txt":
        "1baeb0cecca33b3eae2a3f528bb20622b4c8a95b78250f4e6372f8f1e27d5708",
}
import_checks = []
for path, expected in imports.items():
    actual = sha256((HERE / Path(path).name).read_bytes()).hexdigest()
    assert actual == expected, path
    import_checks.append({"path": path, "sha256": actual, "pass": True})

result = {
    "scope": "exact scalar arithmetic and frozen-import identity only",
    "quantum_theorem_formally_verified": False,
    "external_validation": False,
    "arithmetic_checks": checks,
    "frozen_import_checks": import_checks,
}
(HERE / "constant_checks.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({"arithmetic_checks": len(checks), "frozen_import_checks": len(import_checks),
                  "all_pass": True, "scope": result["scope"]}))
