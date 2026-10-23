"""Reproduce the conditional arithmetic in EB_QUANTITATIVE_CHALLENGE.md.

This is a source-based dose/loading calculation, not an EB-on-resin model.
The resin scenarios assume (without evidence) that the clean-water dose
response transfers unchanged to resin-bound PFOS.
"""

from math import isclose, log

AVOGADRO = 6.022_140_76e23
PFOS_MOLAR_MASS_G_MOL = 500.1
K_DOSE_PER_KGY = 0.0184
PFOS_FEED_KG_PER_M3 = 0.0001  # 0.1 mg/L
SITE_CAPACITY_MOL_PER_G = 1.59e-3  # PSR2 Plus Cl, 1.59 meq/g
PARENT_LOSS_FRACTION = 0.90

d90_kgy = log(10) / K_DOSE_PER_KGY
water_kwh_per_m3 = d90_kgy / 3.6
water_pfos_lost_kg_per_m3 = PFOS_FEED_KG_PER_M3 * PARENT_LOSS_FRACTION
water_kwh_per_kg_fed = water_kwh_per_m3 / PFOS_FEED_KG_PER_M3
water_kwh_per_kg_lost = water_kwh_per_m3 / water_pfos_lost_kg_per_m3
pfos_feed_g_per_l = PFOS_FEED_KG_PER_M3 * 1000 / 1000
molecules_lost_per_l = (
    pfos_feed_g_per_l / PFOS_MOLAR_MASS_G_MOL
    * AVOGADRO * PARENT_LOSS_FRACTION
)
water_molecules_lost_per_j = molecules_lost_per_l / (d90_kgy * 1_000)

print(f"D90 extrapolation: {d90_kgy:.2f} kGy")
print(f"Dilute-water absorbed energy: {d90_kgy / 3.6:.2f} kWh/m^3")
print(f"Energy/kg PFOS fed: {water_kwh_per_kg_fed:,.0f} kWh/kg")
print(f"Energy/kg PFOS lost: {water_kwh_per_kg_lost:,.0f} kWh/kg")
print(f"PFOS molecules lost per absorbed joule: {water_molecules_lost_per_j:.3e}")

for theta in (0.014, 0.034):
    pfos_mol_per_g = SITE_CAPACITY_MOL_PER_G * theta
    pfos_mg_per_g = pfos_mol_per_g * PFOS_MOLAR_MASS_G_MOL * 1000
    molecules_lost_per_g = pfos_mol_per_g * AVOGADRO * PARENT_LOSS_FRACTION
    molecules_per_j_dry = molecules_lost_per_g / d90_kgy
    lost_g_per_g = pfos_mol_per_g * PFOS_MOLAR_MASS_G_MOL * PARENT_LOSS_FRACTION
    kwh_per_kg_lost_dry = (d90_kgy / lost_g_per_g) / 3600
    print(
        f"theta={theta:.3f}: {pfos_mg_per_g:.2f} mg/g inferred; "
        f"{PARENT_LOSS_FRACTION * theta:.4f} lost PFOS/site; "
        f"{molecules_per_j_dry:.3e} molecules/J; "
        f"{kwh_per_kg_lost_dry:.2f} kWh/kg lost (dry-only, conditional)"
    )

assert isclose(d90_kgy, 125.14049418445902, rel_tol=1e-12)
assert isclose(water_kwh_per_kg_fed, 347_612.4838457195, rel_tol=1e-12)
assert isclose(water_kwh_per_kg_lost, 386_236.09316191054, rel_tol=1e-12)
