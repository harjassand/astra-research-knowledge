"""Inventory-only evaluation; no kinetics, parameter sweep, or fitted trajectory."""
import csv
from pathlib import Path
root=Path(__file__).resolve().parents[2]
src=Path(__file__).parent/'inputs/digitized_experiments.csv'
F=20/(60*22.414)
S500_cap=F*50*(500-298.15)
rows=[]
for r in csv.DictReader(src.open()):
    x=float(r['NOx_pct'])/100
    P=float(r['power_W'])
    hmin=F*x/(1+x/2)*33100
    hmax=F*x*90290
    rows.append(dict(mode=r['mode'],reported_power_W=P,x_center=x,
        chemical_enthalpy_min_W=hmin,chemical_enthalpy_max_W=hmax,
        rejection_min_IF_absorbed_equals_reported_W=P-hmax,
        rejection_max_IF_absorbed_equals_reported_W=P-hmin,
        sufficient_loss_ceiling_for_positive_500K_duty_IF_absorbed_equals_reported_W=P-hmax-S500_cap))
with (Path(__file__).parent/'conditional_inventory_ledger.csv').open('w') as f:
    w=csv.DictWriter(f,fieldnames=rows[0]); w.writeheader(); w.writerows(rows)
assert 0 < min(r['chemical_enthalpy_min_W'] for r in rows)
assert all(r['chemical_enthalpy_max_W']<r['reported_power_W'] for r in rows)
print('Eight observed graphical centers evaluated; all power-to-heat numbers explicitly conditional.')
