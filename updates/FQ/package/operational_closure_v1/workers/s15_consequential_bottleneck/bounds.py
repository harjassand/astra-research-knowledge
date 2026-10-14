"""Reproduce illustrative mass and lattice-diffusion checks in REPORT.md.

Literature input for D_l: Majima and Mitani (1978), DOI
10.2320/matertrans1960.19.663. Feed and target concentrations are the
illustrative 0.4 and 0.1 wt% values discussed by Daehn et al. (2019), DOI
10.1007/s11663-019-01537-9. No physical process is simulated.
"""

import math


def required_copper_removal(feed_mass_kg, feed_cu_fraction, target_cu_fraction,
                            iron_loss_kg=0.0):
    """Solve (Cu_in-R)/(M_in-R-L) <= target for R."""
    return (feed_mass_kg * (feed_cu_fraction - target_cu_fraction)
            + target_cu_fraction * iron_loss_kg) / (1 - target_cu_fraction)


def copper_lattice_diffusivity(temp_c):
    gas_constant = 8.314462618  # J mol^-1 K^-1
    return 4.16e-4 * math.exp(-305_000 / (gas_constant * (temp_c + 273.15)))


if __name__ == "__main__":
    feed_mass = 1000.0
    initial_cu = feed_mass * 0.004
    removal = required_copper_removal(feed_mass, 0.004, 0.001)
    print(f"Cu removal for 0.4 to 0.1 wt%, 1 t, no Fe loss: {removal:.6f} kg")
    print(f"Fraction of all Cu: {removal / initial_cu:.6f}")
    print(f"Capture if accessible fraction is 0.90: {removal / (0.90 * initial_cu):.6f}")
    temp_c = 1150.0
    dwell_s = 3600.0
    diffusivity = copper_lattice_diffusivity(temp_c)
    length_m = math.sqrt(2 * diffusivity * dwell_s)
    slab_m = 0.001
    ideal_sink_fraction = 4 * math.sqrt(diffusivity * dwell_s / math.pi) / slab_m
    print(f"Cu lattice D at 1150 C: {diffusivity:.6e} m^2/s")
    print(f"sqrt(2Dt) for 1 h: {length_m * 1e6:.3f} micrometres")
    print(f"Ideal two-face 1-mm slab early-time uptake: {ideal_sink_fraction:.6f}")
