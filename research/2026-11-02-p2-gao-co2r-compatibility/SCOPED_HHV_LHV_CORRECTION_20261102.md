# Scoped correction, 2026-11-02: Gao methane HHV/LHV boundary

**Preserves originals.** This does not rewrite `README.md`, `ENERGY_FRONTIER.md` or `verify.py` on this branch. Those earlier files incorrectly called the 55.5 MJ/kg methane energy value "LHV." It is approximately **HHV**. This correction changes only the heating-value labels and derived comparisons; charge, moles methane, pulse counts and reduction-only 5.017 MJ/mol calculations are unchanged.

Authoritative thermochemistry: Cantera stable heating-value worked example, https://cantera.org/stable/userguide/heating-value.html : at its 298K reference, CH4 **LHV=50.025 MJ/kg** and **HHV=55.511 MJ/kg** (liquid product water for HHV), lines 25–66. Take M(CH4)=0.016043 kg/mol and F=96485.33212 C/mol.

At illustrative source operating values |V_red|=3.9V, FE_CH4=0.6, the reduction-only input per methane mole is E_red=8F*3.9/0.6=5.01723727024 MJ/mol. LHV output=0.802551075 MJ/mol, HHV output=0.890562973 MJ/mol. Therefore reduction-only LHV recovery is 0.1599587645 (~**16.00%**) and reduction-only HHV recovery is 0.1775006692 (~**17.75%**). **Neither is full-cycle or plant efficiency.**

Necessary REDUCTION-ONLY inequality for fuel/output electrical input >50%:
  |V_red|/FE_CH4 < 2 * (heating value per mole) / (8F).
On LHV basis this is **|V_red|/FE_CH4 < 2.07946394 V** (not the original 2.307 V); on HHV basis **<2.30750870 V**. At FE=.6 these require |V_red|<1.24767836 V (LHV) or <1.38450522 V (HHV). The illustrative current ratio |V|/FE=6.5 V must fall by factors >3.12581 (LHV) and >2.81689 (HHV), respectively, to cross the respective **reduction-only** 50% gate. Full-process electricity, if net consumed outside reduction, makes these necessary but not sufficient for 50% plant recovery. If oxidation generates recoverable net energy, it must be explicitly measured, and these reduction-only necessary plant implications cannot be silently made.

This correction is a **source-based quantitative repair**, not a changed scientific source/version. Gao et al. https://doi.org/10.1038/s41560-025-01883-w remains the original source for representative operation. No new measured efficiency is asserted.
