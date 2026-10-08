"""Back-of-envelope acquisition check for Yang, Stone & Egan (2025).

This is an independently written local calculation from the published
first-order two-colour equations, not a replay of the authors' raw-data code.
"""

from math import sqrt

R = 8.31446261815324  # J mol^-1 K^-1
T = 303.0  # K, representative paper isotherm
NU_RED = 194.368624e12  # Hz, 1542.3912 nm
NU_BLUE = 473.611873e12  # Hz, 632.9919 nm
A_EPS_CM3_MOL = 0.51725408
A2_CM3_MOL = 1.332465e-4
CM3_TO_M3 = 1e-6


def pressure_slope(nu_hz: float) -> float:
    """First-order dn/dp slope using A_R(nu)=A_eps+A2*(nu/1e14)^2."""
    x = nu_hz / 1e14
    ar_m3_mol = (A_EPS_CM3_MOL + A2_CM3_MOL * x**2) * CM3_TO_M3
    return 3.0 * ar_m3_mol / (2.0 * R * T)


def estimate_pressure(z_red: float, z_blue: float) -> float:
    """Estimate p from z_i = a_i*p + d, eliminating an arbitrary shared d."""
    a_red = pressure_slope(NU_RED)
    a_blue = pressure_slope(NU_BLUE)
    return (z_blue - z_red) / (a_blue - a_red)


def main() -> None:
    a_red = pressure_slope(NU_RED)
    a_blue = pressure_slope(NU_BLUE)
    delta_a = a_blue - a_red

    # Finite algebraic check: a common fill-dependent nuisance d cancels.
    common_distortion_slope = -1.0e-11  # Pa^-1; illustrative, not fit data
    for p in (50e3, 100e3, 250e3, 500e3):
        d = common_distortion_slope * p
        z_red = a_red * p + d
        z_blue = a_blue * p + d
        p_hat = estimate_pressure(z_red, z_blue)
        assert abs(p_hat / p - 1.0) < 1e-12

    # Noise propagation under independent, equal 200-Hz per-channel errors.
    # The paper reports <200-Hz precision for resonance-frequency changes;
    # this treats that as a conservative per-channel standard deviation.
    sigma_f = 200.0
    sigma_delta_z = sigma_f * sqrt(NU_RED**-2 + NU_BLUE**-2)
    print(f"frequency coordinates nu/1e14: {NU_RED/1e14:.8f}, {NU_BLUE/1e14:.8f}")
    print(f"delta(nu/1e14)^2: {(NU_BLUE/1e14)**2-(NU_RED/1e14)**2:.8f}")
    print(f"pressure-slope difference: {delta_a:.6e} Pa^-1")
    print(f"combined fractional-refractivity noise: {sigma_delta_z:.6e}")
    for p in (50e3, 100e3, 250e3, 500e3):
        signal = delta_a * p
        rel_ppm = 1e6 * sigma_delta_z / signal
        print(f"p={p/1e3:6.0f} kPa: differential signal={signal:.6e}, "
              f"predicted readout uncertainty={rel_ppm:.3f} ppm")

    # A wavelength-dependent nuisance d_blue-d_red is confounded with p.
    target_ppm = 5.7  # reported combined standard uncertainty
    max_delta_slope = delta_a * target_ppm * 1e-6
    p = 250e3
    length = 0.15
    max_differential_length = max_delta_slope * p * length
    print(f"max differential nuisance slope for {target_ppm} ppm: "
          f"{max_delta_slope:.3e} Pa^-1")
    print(f"equivalent differential length at 250 kPa over 15 cm: "
          f"{max_differential_length*1e12:.3f} pm")

    # Design sensitivity if a 750-THz blue channel were available and had the
    # same absolute-frequency noise; actual coatings/laser noise may differ.
    nu_blue_750 = 750e12
    a_blue_750 = pressure_slope(nu_blue_750)
    print(f"sensitivity gain at 750 THz vs present blue channel: "
          f"{(a_blue_750-a_red)/delta_a:.3f}x")


if __name__ == "__main__":
    main()
