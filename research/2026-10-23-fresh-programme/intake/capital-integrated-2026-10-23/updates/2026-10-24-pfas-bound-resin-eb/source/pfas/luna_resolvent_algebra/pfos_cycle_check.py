#!/usr/bin/env python3
"""Transparent arithmetic fixture for PFOS capture + hydrated-electron competition.

All concentrations are mol/L; rate constants are L mol^-1 s^-1. The branching
calculation is a homogeneous initial-collision model. Omitting unlisted
scavengers makes it an upper bound only within the explicitly named homogeneous
competitor fixture; it is not a bound on electron transfer at a resin-bound
interface. It is not a radiolysis-spur model and it does not turn initial
electron transfer into a PFOS destruction yield.
"""
from math import log

# PFOS anion C8F17SO3- (g/mol); use rounded atomic weights for a ledger fixture.
MW_PFOS = 8 * 12.011 + 17 * 18.998403 + 32.06 + 3 * 15.999
MW_F = 18.998403
MW_SO4 = 32.06 + 4 * 15.999

# Literature bracket for the initial hydrated-electron/PFOS interaction.
K_PFOS = (7.3e7, 2.4e9)
# Primary-source values for common scavengers, used only in the idealized branch.
K_O2 = 1.9e10
K_NO3 = 9.7e9
# Primary electron-pulse-radiolysis range, expressed per mole of organic carbon.
K_DOM = (0.51e8, 2.11e8)


def share(cp, competitors):
    """Fraction of e_aq^- captures going to PFOS for listed competitors."""
    rows = []
    for kp in K_PFOS:
        target = kp * cp
        other = sum(k * c for k, c in competitors)
        rows.append(target / (target + other))
    return tuple(rows)


def cp_for_share(target_fraction, kp, other_pseudo_first_order):
    """Required PFOS molarity for a specified initial capture fraction."""
    return target_fraction / (1 - target_fraction) * other_pseudo_first_order / kp


def share_with_dom(cp, competitors, dom_carbon_molar):
    """Conservative range over independently reported PFOS and DOM rate bounds."""
    other = sum(k * c for k, c in competitors)
    low = K_PFOS[0] * cp / (K_PFOS[0] * cp + other + K_DOM[1] * dom_carbon_molar)
    high = K_PFOS[1] * cp / (K_PFOS[1] * cp + other + K_DOM[0] * dom_carbon_molar)
    return low, high


def k_selectivity_for_site_share(q, c_competitor, c_pfos):
    """One-site Langmuir Kp/Kc threshold, considering one monovalent competitor."""
    return (q / (1 - q)) * c_competitor / c_pfos


def main():
    # 0.1 mg/L PFOS anion = ~0.20 uM.
    cp = 0.1e-3 / MW_PFOS
    cl = 1.0e-3
    nitrate = 0.10e-3
    oxygen = 0.25e-3
    # Convert 2 mg-C/L to mol C/L for k_DOM reported in M_C^-1 s^-1.
    dom_carbon = 2.0e-3 / 12.011
    sinks = [(K_O2, oxygen), (K_NO3, nitrate)]
    o2_sink = K_O2 * oxygen
    no3_sink = K_NO3 * nitrate
    all_listed_sink = o2_sink + no3_sink

    print(f"MW(PFOS anion) = {MW_PFOS:.6f} g/mol")
    print(f"0.1 mg/L PFOS = {cp*1e6:.6f} uM")
    print(f"listed competing pseudo-first-order sink = {all_listed_sink:.6g} s^-1 "
          f"(O2 {o2_sink:.6g}; nitrate {no3_sink:.6g})")
    dom_sink = (K_DOM[0] * dom_carbon, K_DOM[1] * dom_carbon)
    print(f"2 mg-C/L NOM electron sink range = {dom_sink[0]:.6g}..{dom_sink[1]:.6g} s^-1")
    for cp_uM in (0.01, cp * 1e6, 1.0):
        cshare = share_with_dom(cp_uM * 1e-6, sinks, dom_carbon)
        print(f"at PFOS={cp_uM:.6g} uM plus 2 mg-C/L NOM, e-capture share = "
              f"{cshare[0]:.6g} .. {cshare[1]:.6g}")
    for name, factor in (("feed", 1), ("PFOS-only x100", 100), ("PFOS-only x1000", 1000),
                         ("all three co-concentrated x1000", 1000)):
        if name == "all three co-concentrated x1000":
            cshare = share(cp * factor, [(k, c * factor) for k, c in sinks])
        else:
            cshare = share(cp * factor, sinks)
        print(f"initial PFOS electron-capture share; {name:34s}: "
              f"{cshare[0]:.6g} .. {cshare[1]:.6g}")

    no_o2 = [(K_NO3, nitrate)]
    print("with O2 removed but nitrate left at 0.1 mM: "
          f"{share(cp, no_o2)[0]:.6g} .. {share(cp, no_o2)[1]:.6g}")
    print("with O2 and nitrate removed but 2 mg-C/L NOM left: "
          f"{share_with_dom(cp, [], dom_carbon)[0]:.6g} .. "
          f"{share_with_dom(cp, [], dom_carbon)[1]:.6g}")
    print("PFOS concentration needed for 1% share at feed O2+nitrate: "
          f"{cp_for_share(0.01, K_PFOS[1], all_listed_sink)*1e6:.6g} .. "
          f"{cp_for_share(0.01, K_PFOS[0], all_listed_sink)*1e6:.6g} uM "
          "(high k to low k)")
    print("including aqueous NOM, PFOS concentration needed for 1% share: "
          f"{cp_for_share(0.01, K_PFOS[1], all_listed_sink + dom_sink[0])*1e6:.6g} .. "
          f"{cp_for_share(0.01, K_PFOS[0], all_listed_sink + dom_sink[1])*1e6:.6g} uM "
          "(high k/min DOM to low k/max DOM)")

    # Matrix and site-selectivity/load inventory for 1 m^3 feed.
    for cp_uM in (0.01, cp * 1e6, 1.0):
        c = cp_uM * 1e-6
        cp_cl_ratio = cl / c
        print(f"PFOS={cp_uM:.6g} uM vs 1 mM Cl concentration ratio = 1:{cp_cl_ratio:.1f}")
        for q in (0.50, 0.99):
            req = k_selectivity_for_site_share(q, cl, c)
            print(f"  one-site K_PFOS/K_Cl for {q:.0%} PFOS occupancy: {req:.6g}")

    V_L = 1000.0
    n_pfos = cp * V_L
    n_comp_equiv = (1.0e-3 + 2 * 0.5e-3 + 0.10e-3 + 2.0e-3) * V_L
    print(f"1 m^3 feed PFOS = {n_pfos*1e3:.6g} mmol = {n_pfos*MW_PFOS:.6g} g")
    print(f"listed inorganic competitor charge = {n_comp_equiv:.6g} eq "
          f"(Cl + 2*sulfate + nitrate + bicarbonate); ratio to PFOS = "
          f"{n_comp_equiv/n_pfos:.6g}:1")

    # Ideal mineralization products; a balance only, not a claimed pathway.
    n_f = 17 * n_pfos
    n_sulfate = n_pfos
    print(f"ideal 1 m^3 mineralization balance: F-={n_f*1e3:.6g} mmol "
          f"({n_f*MW_F*1e3:.6g} mg F), SO4={n_sulfate*1e3:.6g} mmol "
          f"({n_sulfate*MW_SO4*1e3:.6g} mg sulfate), "
          f"H+ equivalent={18*n_pfos*1e3:.6g} mmol")

    # If an EB parent-loss slope is transported unchanged: hypothetical only.
    kD = 0.0184  # kGy^-1, source-reported for 0.1 mg/L PFOS in neutral deaerated solution
    D90_kGy = log(10) / kD
    kWh_per_kg = D90_kGy * 1000 / 3.6e6  # 1 kGy = 1 kJ/kg
    mass_pfos_kg_per_m3 = n_pfos * MW_PFOS / 1000
    kWh_water_m3 = kWh_per_kg * 1000.0
    kWh_per_kg_removed = kWh_water_m3 / (0.9 * mass_pfos_kg_per_m3)
    print(f"source-slope D90 = {D90_kGy:.6f} kGy; absorbed energy = "
          f"{kWh_per_kg*1000:.6f} Wh/kg irradiated material")
    print(f"conditional water-only transferred-slope estimate = {kWh_water_m3:.6f} kWh/m^3 "
          f"= {kWh_water_m3/mass_pfos_kg_per_m3:.6g} kWh/kg input PFOS")
    print(f"at 90% parent loss, conditional = {kWh_per_kg_removed:.6g} "
          "kWh/kg PFOS removed")
    print(f"conditional 1 kg wet-concentrate dose energy = {kWh_per_kg:.6f} kWh "
          "(1000x less irradiated mass than 1 m^3 water, if same dose response)")

    # Product-ion burden from complete release into a 0.1-L concentrate.
    V_conc_L = 0.1
    print(f"if the 1 m^3 feed is fully converted and its F/S products remain in "
          f"0.1 L: [F-]={n_f/V_conc_L*1e3:.6g} mM; "
          f"[SO4]={n_sulfate/V_conc_L*1e3:.6g} mM")

    # Assertions protect unit and dilution invariants.
    assert abs(cp * MW_PFOS * 1000 - 0.1) < 1e-12  # g/L to mg/L
    assert abs(share(cp, sinks)[0] - 2.55695e-6) < 1e-10
    assert abs(share(cp, sinks)[1] - 8.40573e-5) < 1e-9
    assert max(abs(a - b) for a, b in zip(
        share(cp, sinks), share(cp * 1000, [(k, c * 1000) for k, c in sinks]))) < 1e-15
    assert max(abs(a - b) for a, b in zip(
        share_with_dom(cp, sinks, dom_carbon),
        share_with_dom(cp * 1000, [(k, c * 1000) for k, c in sinks], dom_carbon * 1000))) < 1e-15
    assert abs(D90_kGy - 125.07) < 0.1
    assert abs(kWh_per_kg_removed - kWh_water_m3 / mass_pfos_kg_per_m3 / 0.9) < 1e-8


if __name__ == "__main__":
    main()
