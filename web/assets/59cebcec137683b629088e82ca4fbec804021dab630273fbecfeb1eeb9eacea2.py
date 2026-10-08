from fractions import Fraction
import json
from pathlib import Path


rows = []
for d in (2, 3, 4, 5, 8, 16, 32, 64):
    lam_clone = Fraction(d + 2, 2 * (d + 1))
    lam_eb = Fraction(1, d + 1)
    gap_clone = 1 - lam_clone
    gap_eb = 1 - lam_eb
    ratio = gap_eb / gap_clone
    assert ratio == 2
    for c in (Fraction(1), Fraction(3, 2), Fraction(1999, 1000)):
        assert gap_eb <= c * gap_clone if c >= 2 else gap_eb > c * gap_clone
    rows.append(
        {
            "d": d,
            "clone_eigenvalue": str(lam_clone),
            "eb_eigenvalue": str(lam_eb),
            "clone_dirichlet_gap": str(gap_clone),
            "eb_dirichlet_gap": str(gap_eb),
            "ratio": str(ratio),
        }
    )

out = Path(__file__).with_name("cloner_calibration.json")
out.write_text(json.dumps(rows, indent=2) + "\n")
print(out)
