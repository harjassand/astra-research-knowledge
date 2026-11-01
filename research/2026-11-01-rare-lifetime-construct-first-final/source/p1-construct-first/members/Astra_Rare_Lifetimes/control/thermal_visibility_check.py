"""Exact-formula diagnostics; the all-size proof is in thermal_visibility.md."""
from fractions import Fraction
import json
from pathlib import Path

rows=[]
for n in [3, 10, 100, 1000, 1000000]:
    partition_gap=Fraction(n-1,2*n-1)
    energy_gap=Fraction(n*n,(2*n-1)*(3*n-2))
    relative_separation=Fraction(n-1,5*n-3)
    assert energy_gap > Fraction(1,6)
    assert relative_separation >= Fraction(1,6)
    rows.append(dict(N=n,relative_partition_gap=float(partition_gap),
                     energy_gap_in_delta=float(energy_gap),
                     relative_error_separation=float(relative_separation)))
result={"scope":"Exact rational checks of the crossover formulas; not a proof of novelty or practical advantage", "rows":rows}
Path(__file__).with_name("thermal_visibility_results.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result,indent=2))
