"""Independent transfer-matrix and exact sequence audit for FH-spectral.

This script uses only NumPy/SciPy and the parameter values transcribed from
the frozen producer README. It does not import the producer's optical model.
The optical calculations remain source-reference scenarios, not κ-ET fits.
"""
from __future__ import annotations

import itertools
import json
from pathlib import Path

import numpy as np
from scipy.integrate import simpson


OUT = Path(__file__).resolve().parent
SEQ_A = np.array([0, 1, 1, 0, 1, 0, 0, 1], dtype=int)
SEQ_B = SEQ_A[::-1].copy()


def eps_reference(nu_cm: float, isotope: int, loss: float = 1.0,
                  ideal_mass_only: bool = False,
                  material_overrides: dict[str, float] | None = None
                  ) -> tuple[complex, complex]:
    """Uniaxial Lorentz model, transcribed from producer README/code.

    isotope=0 denotes 10B and isotope=1 denotes 11B. The "ideal" option
    mass-scales both in-plane endpoints equally to enforce exact DC equality.
    """
    if isotope not in (0, 1) or loss <= 0:
        raise ValueError("isotope must be 0/1 and loss must be positive")
    p = {
        "eps_inf_t_10": 5.1, "eps_inf_t_11": 5.1,
        "eps_inf_z_10": 2.5, "eps_inf_z_11": 2.5,
        "to_t_10": 1394.5, "lo_t_10": 1650.0,
        "to_t_11": 1359.8, "lo_t_11": 1608.7,
        "to_z_10": 785.0, "lo_z_10": 845.0,
        "to_z_11": 785.0 * (1359.8 / 1394.5),
        "lo_z_11": 845.0 * (1359.8 / 1394.5),
        "gamma_t_10": 1.8, "gamma_t_11": 1.8,
        "gamma_z_10": 1.0, "gamma_z_11": 1.0,
    }
    if ideal_mass_only:
        p["lo_t_11"] = p["lo_t_10"] * p["to_t_11"] / p["to_t_10"]
    if material_overrides:
        p.update(material_overrides)
    suffix = "10" if isotope == 0 else "11"
    to_t, lo_t = p[f"to_t_{suffix}"], p[f"lo_t_{suffix}"]
    to_z, lo_z = p[f"to_z_{suffix}"], p[f"lo_z_{suffix}"]
    et_inf, ez_inf = p[f"eps_inf_t_{suffix}"], p[f"eps_inf_z_{suffix}"]
    gamma_t = p[f"gamma_t_{suffix}"] * loss
    gamma_z = p[f"gamma_z_{suffix}"] * loss
    nu = complex(nu_cm)
    et = et_inf * (1 + (lo_t**2 - to_t**2) /
                   (to_t**2 - nu**2 - 1j * nu * gamma_t))
    ez = ez_inf * (1 + (lo_z**2 - to_z**2) /
                   (to_z**2 - nu**2 - 1j * nu * gamma_z))
    return et, ez


def rp_transfer(nu_cm: float, q_per_m: np.ndarray | float,
                sequence: np.ndarray, layer_nm: float = 10.0,
                cap_nm: float = 5.0, loss: float = 1.0,
                ideal_mass_only: bool = False,
                host_eps: complex = 1.0,
                material_overrides: dict[str, float] | None = None,
                substrate_eps: complex = 1.0) -> np.ndarray:
    """Global amplitude-transfer-matrix reflection, independent of recursion.

    The incident and terminal media are isotropic half spaces (host_eps and
    substrate_eps). For source reproduction both are vacuum; target-load
    stress cases keep the incident side at vacuum and vary substrate_eps.
    This p-amplitude convention is checked against source outputs.
    """
    q0 = np.asarray(q_per_m, dtype=float)
    q = np.atleast_1d(q0).astype(complex)
    if layer_nm <= 0 or cap_nm < 0:
        raise ValueError("invalid geometric thickness")
    if len(sequence) == 0:
        raise ValueError("sequence must contain at least one internal layer")

    k0 = 2 * np.pi * 100 * float(nu_cm)
    eps_layers = [eps_reference(nu_cm, int(i), loss, ideal_mass_only,
                                material_overrides)
                  for i in np.r_[0, sequence, 0]]
    media = [(complex(host_eps), complex(host_eps))] + eps_layers + [
        (complex(substrate_eps), complex(substrate_eps))]
    thicknesses_m = [cap_nm * 1e-9] + [layer_nm * 1e-9] * len(sequence) + [cap_nm * 1e-9]

    kz: list[np.ndarray] = []
    admittance: list[np.ndarray] = []
    for et, ez in media:
        k = np.sqrt(et * k0**2 - et / ez * q**2 + 0j)
        flip = (k.imag < 0) | ((np.abs(k.imag) < 1e-15) & (k.real < 0))
        k = np.where(flip, -k, k)
        kz.append(k)
        admittance.append(et / k)

    eye = np.broadcast_to(np.eye(2, dtype=complex), (len(q), 2, 2)).copy()
    transfer = eye
    for idx, thickness in enumerate(thicknesses_m):
        yi, yj = admittance[idx], admittance[idx + 1]
        interface = np.empty_like(transfer)
        interface[:, 0, 0] = 0.5 * (1 + yj / yi)
        interface[:, 0, 1] = 0.5 * (1 - yj / yi)
        interface[:, 1, 0] = 0.5 * (1 - yj / yi)
        interface[:, 1, 1] = 0.5 * (1 + yj / yi)
        phase = kz[idx + 1] * thickness
        propagation = np.zeros_like(transfer)
        propagation[:, 0, 0] = np.exp(-1j * phase)
        propagation[:, 1, 1] = np.exp(1j * phase)
        transfer = transfer @ interface @ propagation

    yi, yj = admittance[-2], admittance[-1]
    interface = np.empty_like(transfer)
    interface[:, 0, 0] = 0.5 * (1 + yj / yi)
    interface[:, 0, 1] = 0.5 * (1 - yj / yi)
    interface[:, 1, 0] = 0.5 * (1 - yj / yi)
    interface[:, 1, 1] = 0.5 * (1 + yj / yi)
    transfer = transfer @ interface
    # The source uses the p-polarization Fresnel basis, opposite to tangential-E.
    reflected = -transfer[:, 1, 0] / transfer[:, 0, 0]
    return reflected.reshape(q0.shape)


def exact_balanced_sequences(n_layers: int) -> list[tuple[int, ...]]:
    """Enumerate 50:50 isotope partitions matching moments 1 and 2."""
    if n_layers % 2:
        return []
    half = n_layers // 2
    found: list[tuple[int, ...]] = []
    for chosen in itertools.combinations(range(n_layers), half):
        comp = tuple(j for j in range(n_layers) if j not in chosen)
        if chosen < comp and all(
            sum(j**degree for j in chosen) == sum(j**degree for j in comp)
            for degree in (1, 2)
        ):
            found.append(chosen)
    return found


def flip_matched_sequences(n_layers: int) -> list[tuple[int, ...]]:
    """Enumerate 50:50 stacks with zero first moment, modulo physical reversal.

    For a stack and its geometric mirror, the A and D laminate matrices are
    invariant and B changes sign. Thus zero centered first moment is the
    necessary and sufficient scalar isotope-order condition for equal A/B/D
    matrices for arbitrary fixed isotope coefficients.
    """
    if n_layers % 2:
        return []
    half = n_layers // 2
    target = n_layers * (n_layers - 1) // 4
    if n_layers * (n_layers - 1) % 4:
        return []
    found: list[tuple[int, ...]] = []
    for chosen in itertools.combinations(range(n_layers), half):
        if sum(chosen) != target:
            continue
        reverse = tuple(sorted(n_layers - 1 - j for j in chosen))
        if chosen <= reverse:
            found.append(chosen)
    return found


def unrestricted_flip_matched_sequences(n_layers: int) -> list[tuple[int, ...]]:
    """Enumerate all isotope fractions with zero first moment, modulo reversal.

    This is the physical flip-only static match condition. The same laminate
    is mounted in both orientations, so its isotope inventory is conserved
    across the pair automatically; a 50:50 inventory inside each laminate is
    an optional additional constraint, not part of mirror matching.
    """
    found: list[tuple[int, ...]] = []
    weights = [2 * j - (n_layers - 1) for j in range(n_layers)]
    for k in range(n_layers + 1):
        for chosen in itertools.combinations(range(n_layers), k):
            if sum(weights[j] for j in chosen) != 0:
                continue
            reverse = tuple(sorted(n_layers - 1 - j for j in chosen))
            if chosen <= reverse:
                found.append(chosen)
    return found


def laminate_moments(sequence: np.ndarray, values: tuple[float, float]) -> np.ndarray:
    """Exact-piecewise-constant moments z^0,z^1,z^2 for unit layers."""
    n = len(sequence)
    edges = np.arange(n + 1, dtype=float) - n / 2
    v = np.asarray(values)[sequence]
    return np.array([
        np.sum(v * (edges[1:] ** (k + 1) - edges[:-1] ** (k + 1)) / (k + 1))
        for k in range(3)
    ])


def witness(sequence: np.ndarray, nu_cm: float = 1470.0,
            z_nm: float = 20.0, loss: float = 1.0, n_q: int = 10_000,
            layer_nm: float = 10.0, cap_nm: float = 5.0,
            ideal_mass_only: bool = False,
            host_eps: complex = 1.0,
            material_overrides: dict[str, float] | None = None,
            substrate_eps: complex = 1.0) -> float:
    q = np.geomspace(1.2e6, 1.0e9, n_q)
    weights = q**2 * np.exp(-2 * q * z_nm * 1e-9)
    r = rp_transfer(nu_cm, q, sequence, layer_nm, cap_nm, loss,
                    ideal_mass_only, host_eps, material_overrides,
                    substrate_eps)
    return float(simpson(weights * r.imag, x=q))


def contrast(sequence: np.ndarray, **kwargs: float) -> float:
    a = witness(sequence, **kwargs)
    b = witness(sequence[::-1], **kwargs)
    return float(2 * (a - b) / (a + b))


def main() -> None:
    result: dict[str, object] = {
        "status": "Independent model audit; not experimental data or a kappa-ET loaded fit.",
        "code": "Global amplitude transfer matrix plus exact integer sequence enumeration.",
        "environment": "Python 3.13.2; NumPy 2.3.5; SciPy 1.17.0",
    }

    # Algebraic sequence checks and the source pattern's isotope convention.
    moments = [int(np.sum((1 - 2 * SEQ_A) * np.arange(8) ** k)) for k in range(4)]
    assert moments[:3] == [0, 0, 0]
    assert np.array_equal(SEQ_B, SEQ_A[::-1])
    result["source_sequence_signed_moments_degrees_0_to_3"] = moments
    result["balanced_exact_patterns_modulo_complement"] = {
        str(n): [list(p) for p in exact_balanced_sequences(n)]
        for n in (4, 6, 8, 10, 12, 14, 16)
    }
    flip_catalog = {}
    for n in (2, 4, 6, 8, 10, 12, 14, 16):
        reps = flip_matched_sequences(n)
        palindrome = [p for p in reps if tuple(sorted(n - 1 - j for j in p)) == p]
        flip_catalog[str(n)] = {
            "reversal_classes": len(reps),
            "palindromic_no_spectral_change_by_flip": len(palindrome),
            "nontrivial_reversal_pairs": len(reps) - len(palindrome),
            "representatives": [list(p) for p in reps],
        }
    result["flip_only_50_50_exact_static_match_catalog"] = flip_catalog
    unrestricted_catalog = {}
    for n in range(1, 17):
        reps = unrestricted_flip_matched_sequences(n)
        palindrome = [p for p in reps if tuple(sorted(n - 1 - j for j in p)) == p]
        unrestricted_catalog[str(n)] = {
            "reversal_classes": len(reps),
            "palindromic_no_spectral_change_by_flip": len(palindrome),
            "nontrivial_reversal_pairs": len(reps) - len(palindrome),
            "nontrivial_representatives": [list(p) for p in reps if p not in palindrome],
        }
    result["unrestricted_flip_only_exact_static_match_catalog"] = unrestricted_catalog

    # Compare the independent global matrix against the producer's output points.
    points = []
    for seq_name, seq in (("A", SEQ_A), ("B", SEQ_B)):
        for nu, q in ((1470.0, 51e6), (1450.0, 30e6), (1405.0, 20e6)):
            points.append({
                "sequence": seq_name, "nu_cm-1": nu, "q_per_m": q,
                "r_independent": [float(x) for x in (
                    rp_transfer(nu, q, seq).real,
                    rp_transfer(nu, q, seq).imag)],
            })
    result["cross_implementation_points"] = points

    # Exact static equality in ideal oscillator model and residual for published endpoints.
    q_static = np.geomspace(1.2e6, 4e8, 801)
    static_rows = {}
    for ideal in (True, False):
        ra = rp_transfer(0.0, q_static, SEQ_A, ideal_mass_only=ideal)
        rb = rp_transfer(0.0, q_static, SEQ_B, ideal_mass_only=ideal)
        static_rows["ideal" if ideal else "published_endpoints"] = {
            "max_abs_difference": float(np.max(np.abs(ra - rb))),
            "max_difference_over_global_max_abs_rA": float(
                np.max(np.abs(ra - rb)) / np.max(np.abs(ra))),
        }
    result["static_reflection"] = static_rows
    loaded_static = []
    for eps_substrate in (1.0, 2.0, 5.0, 10.0, 20.0):
        ra = rp_transfer(0.0, q_static, SEQ_A, ideal_mass_only=True,
                         substrate_eps=eps_substrate)
        rb = rp_transfer(0.0, q_static, SEQ_B, ideal_mass_only=True,
                         substrate_eps=eps_substrate)
        loaded_static.append({
            "dimensionless_real_isotropic_substrate_stress_case": eps_substrate,
            "max_abs_static_reflection_difference": float(np.max(np.abs(ra-rb))),
            "status": "same epsilon(0) in every hBN layer; substrate values are synthetic",
        })
    result["ideal_static_reflection_with_synthetic_substrate_loads"] = loaded_static

    # Material-input robustness: report changes to the proposed finite spectral witness.
    # Loss factors are the producer's explicit 1/3/6 cases. Geometric values below are
    # stress probes around the proposal, not asserted fabrication tolerances.
    base = contrast(SEQ_A, z_nm=20.0, loss=1.0, n_q=10_000)
    result["base_1470cm-1_20nm_contrast"] = base
    robustness = []
    for loss in (1.0, 3.0, 6.0):
        for z in (10.0, 20.0, 40.0, 80.0):
            robustness.append({"loss_multiplier": loss, "height_nm": z,
                               "signed_contrast": contrast(SEQ_A, z_nm=z,
                                                              loss=loss, n_q=10_000)})
    result["source_geometry_and_loss_contrasts"] = robustness
    substrate_rows = []
    for eps_substrate in (1.0, 2.0, 5.0, 10.0, 20.0):
        substrate_rows.append({
            "dimensionless_real_isotropic_substrate_stress_case": eps_substrate,
            "signed_contrast": contrast(
                SEQ_A, z_nm=20, loss=1, n_q=4000,
                substrate_eps=eps_substrate),
            "status": "synthetic loaded-stack stress case; not a measured kappa-ET dielectric",
        })
    result["terminal_substrate_load_stress_cases"] = substrate_rows

    # Local one-at-a-time sensitivity for every Lorentz-table input, including
    # assumptions shared between isotopes. A 1% perturbation is a derivative
    # probe only; it is not an uncertainty interval or a measured tolerance.
    model_parameters = {
        "eps_inf_t_10": 5.1, "eps_inf_t_11": 5.1,
        "eps_inf_z_10": 2.5, "eps_inf_z_11": 2.5,
        "to_t_10": 1394.5, "lo_t_10": 1650.0,
        "to_t_11": 1359.8, "lo_t_11": 1608.7,
        "to_z_10": 785.0, "lo_z_10": 845.0,
        "to_z_11": 785.0 * (1359.8 / 1394.5),
        "lo_z_11": 845.0 * (1359.8 / 1394.5),
        "gamma_t_10": 1.8, "gamma_t_11": 1.8,
        "gamma_z_10": 1.0, "gamma_z_11": 1.0,
    }
    parameter_sensitivity = []
    for name, nominal in model_parameters.items():
        shifts = []
        for factor in (0.99, 1.01):
            c = contrast(SEQ_A, z_nm=20.0, loss=1.0, n_q=4000,
                         material_overrides={name: nominal * factor})
            shifts.append(c)
        parameter_sensitivity.append({
            "parameter": name, "source_reference_value": nominal,
            "relative_probe": [-0.01, 0.01],
            "contrast_at_minus_1pct": shifts[0],
            "contrast_at_plus_1pct": shifts[1],
            "max_abs_change_from_1pct_probes": max(abs(x - base) for x in shifts),
            "status": "local mathematical sensitivity only; not uncertainty or a physical range",
        })
    result["all_lorentz_parameter_local_sensitivity"] = parameter_sensitivity

    geometric_sensitivity = []
    for parameter, nominal in (("layer_nm", 10.0), ("cap_nm", 5.0)):
        shifts = []
        for factor in (0.99, 1.01):
            kwargs = {parameter: nominal * factor}
            shifts.append(contrast(SEQ_A, z_nm=20.0, loss=1.0, n_q=4000,
                                   **kwargs))
        geometric_sensitivity.append({
            "parameter": parameter, "proposed_value_nm": nominal,
            "relative_probe": [-0.01, 0.01],
            "contrast_at_minus_1pct": shifts[0],
            "contrast_at_plus_1pct": shifts[1],
            "max_abs_change_from_1pct_probes": max(abs(x - base) for x in shifts),
            "status": "local mathematical sensitivity only; not a fabrication tolerance",
        })
    result["geometric_parameter_local_sensitivity"] = geometric_sensitivity

    # Exact static-match countermodel: Im chi for two passive damped harmonic
    # oscillators, centered in opposite-sign spectral lobes, yields opposite
    # signed responses. Their linewidths are synthetic countermodel settings.
    probe_nu = np.linspace(1380.0, 1650.0, 1081)
    probe_q = 51e6
    delta_im = np.array([
        rp_transfer(float(nu), probe_q, SEQ_A, ideal_mass_only=True).imag -
        rp_transfer(float(nu), probe_q, SEQ_B, ideal_mass_only=True).imag
        for nu in probe_nu
    ])
    passive_filters = []
    for center in (1470.0, 1572.0):
        gamma = 5.0
        filt = (gamma * probe_nu) / (
            (center**2 - probe_nu**2)**2 + (gamma * probe_nu)**2)
        weighted_delta = float(simpson(filt * delta_im, x=probe_nu) /
                               simpson(filt, x=probe_nu))
        passive_filters.append({
            "filter_center_cm-1": center,
            "synthetic_damping_cm-1": gamma,
            "weight": "Im[1/(center^2 - nu^2 - i gamma nu)]",
            "nonnegative_filter_weighted_delta_Im_r": weighted_delta,
            "sign": "negative" if weighted_delta < 0 else "positive",
        })
    result["exact_static_match_passive_probe_sign_countermodels"] = {
        "ideal_mass_model_max_static_reflection_difference": static_rows["ideal"]["max_abs_difference"],
        "q_per_m": probe_q,
        "integration_band_cm-1": [float(probe_nu[0]), float(probe_nu[-1])],
        "delta_Im_r_range": [float(delta_im.min()), float(delta_im.max())],
        "filters": passive_filters,
        "status": "synthetic passive damped-oscillator susceptibilities; not a kappa-ET susceptibility",
    }

    # Fixed total internal thickness (80 nm), using the source's stronger
    # complement-moment constraint. This is a stricter subset of flip matching.
    optimized = []
    for n in (8, 12, 16):
        patterns = exact_balanced_sequences(n)
        d = 80.0 / n
        n_q = 3000
        candidates = []
        for ten_boron_positions in patterns:
            seq = np.ones(n, dtype=int)
            seq[list(ten_boron_positions)] = 0
            c1 = contrast(seq, z_nm=20.0, loss=1.0, n_q=n_q,
                          layer_nm=d, cap_nm=5.0)
            c6 = contrast(seq, z_nm=20.0, loss=6.0, n_q=n_q,
                          layer_nm=d, cap_nm=5.0)
            candidates.append({
                "10B_layer_indices": list(ten_boron_positions),
                "layer_thickness_nm_for_80nm_internal_total": d,
                "contrast_loss1": c1,
                "contrast_loss6": c6,
            })
        optimized.append({"n_layers": n, "exact_pairs_modulo_complement": candidates,
                          "status": "scenario ranking only; source dielectric and vacuum output"})
    result["fixed_total_thickness_sequence_search"] = optimized

    # Broader physical flip design space: equal composition plus zero first
    # moment suffices for static A/B/D matching of a stack and its mirror.
    # The values remain a model-based ranking, not material performance claims.
    flip_search = []
    for n in (8, 12):
        reps = flip_matched_sequences(n)
        d = 80.0 / n
        candidates = []
        for ten_boron_positions in reps:
            seq = np.ones(n, dtype=int)
            seq[list(ten_boron_positions)] = 0
            reverse = seq[::-1].copy()
            palindromic = np.array_equal(seq, reverse)
            c1 = contrast(seq, z_nm=20.0, loss=1.0, n_q=2500,
                          layer_nm=d, cap_nm=5.0)
            c6 = contrast(seq, z_nm=20.0, loss=6.0, n_q=2500,
                          layer_nm=d, cap_nm=5.0)
            candidates.append({
                "10B_layer_indices": list(ten_boron_positions),
                "palindromic": bool(palindromic),
                "layer_thickness_nm_for_80nm_internal_total": d,
                "contrast_loss1": c1,
                "contrast_loss6": c6,
            })
        candidates.sort(key=lambda row: abs(row["contrast_loss1"]), reverse=True)
        flip_search.append({"n_layers": n, "reversal_classes": candidates,
                            "status": "flip-only static match; model-based ranking only"})
    result["fixed_total_thickness_flip_design_search"] = flip_search

    # The seven-layer minimum disappears if composition is not artificially
    # constrained to 50:50 within each parent laminate. Both examples have
    # zero centered first moment and therefore exact mirror-pair A/B/D match.
    unrestricted_n7 = []
    for positions in unrestricted_flip_matched_sequences(7):
        seq = np.ones(7, dtype=int)
        seq[list(positions)] = 0
        if np.array_equal(seq, seq[::-1]):
            continue
        d = 80.0 / 7
        unrestricted_n7.append({
            "10B_layer_indices": list(positions),
            "11B_layer_indices": [j for j in range(7) if j not in positions],
            "mirror_10B_layer_indices": list(sorted(6 - j for j in positions)),
            "layer_thickness_nm_for_80nm_internal_total": d,
            "signed_centered_first_moment_integer_scale_2": sum(2*j-6 for j in positions),
            "A_integral_moments_Q10_299_Q11_281": laminate_moments(seq, (299.0, 281.0)).tolist(),
            "B_integral_moments_Q10_299_Q11_281": laminate_moments(seq[::-1], (299.0, 281.0)).tolist(),
            "contrast_loss1": contrast(seq, z_nm=20.0, loss=1.0, n_q=4000,
                                        layer_nm=d, cap_nm=5.0),
            "contrast_loss3": contrast(seq, z_nm=20.0, loss=3.0, n_q=4000,
                                        layer_nm=d, cap_nm=5.0),
            "contrast_loss6": contrast(seq, z_nm=20.0, loss=6.0, n_q=4000,
                                        layer_nm=d, cap_nm=5.0),
            "status": "exact mirror-pair laminate match; source-reference vacuum optics only",
        })
    result["unrestricted_seven_layer_flip_examples"] = unrestricted_n7
    n7_seq = np.ones(7, dtype=int)
    n7_seq[[0, 4, 5]] = 0
    loaded_design_compare = []
    for eps_substrate in (1.0, 2.0, 5.0, 10.0, 20.0):
        loaded_design_compare.append({
            "dimensionless_real_isotropic_substrate_stress_case": eps_substrate,
            "seven_layer_pattern_0_4_5_contrast": contrast(
                n7_seq, z_nm=20, loss=1, n_q=3000,
                layer_nm=80/7, cap_nm=5,
                substrate_eps=eps_substrate),
            "source_eight_layer_pattern_contrast": contrast(
                SEQ_A, z_nm=20, loss=1, n_q=3000,
                layer_nm=10, cap_nm=5,
                substrate_eps=eps_substrate),
            "status": "synthetic substrate comparison; not a kappa-ET loaded fit",
        })
    result["loaded_design_comparison_stress_cases"] = loaded_design_compare

    # Verify exact equality of static mechanical laminate moments for unequal moduli.
    ma = laminate_moments(SEQ_A, (299.0, 281.0))
    mb = laminate_moments(SEQ_B, (299.0, 281.0))
    result["mechanical_moments_unequal_coefficients"] = {
        "A": ma.tolist(), "B": mb.tolist(),
        "max_abs_difference": float(np.max(np.abs(ma - mb))),
        "coefficient_pair_is_synthetic_identity_fixture": True,
    }
    seq_a_mech = laminate_moments(SEQ_A, (299.0, 281.0))
    seq_b_mech = laminate_moments(SEQ_B, (299.0, 281.0))
    result["mirror_pair_moments_unequal_coefficients"] = {
        "A": seq_a_mech.tolist(), "mirror_B": seq_b_mech.tolist(),
        "signed_difference": (seq_a_mech - seq_b_mech).tolist(),
        "interpretation": "z^0 and z^2 match by reflection; z^1 vanishes for both",
    }

    (OUT / "independent_results.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({
        "sequence_moments": moments,
        "sequence_counts": {n: len(exact_balanced_sequences(n)) for n in (4,6,8,10,12,14,16)},
        "balanced_flip_catalog_counts": {n: {
            "reversal_classes": flip_catalog[str(n)]["reversal_classes"],
            "nontrivial_reversal_pairs": flip_catalog[str(n)]["nontrivial_reversal_pairs"],
        } for n in (2,4,6,8,10,12,14,16)},
        "unrestricted_flip_catalog_counts": {n: {
            "reversal_classes": unrestricted_catalog[str(n)]["reversal_classes"],
            "nontrivial_reversal_pairs": unrestricted_catalog[str(n)]["nontrivial_reversal_pairs"],
        } for n in range(1,17)},
        "static_reflection": static_rows,
        "base_contrast": base,
        "substrate_load_stress": substrate_rows,
        "fixed_total_optimization": optimized,
        "fixed_total_flip_design_search": flip_search,
        "unrestricted_seven_layer_flip_examples": unrestricted_n7,
        "loaded_design_comparison_stress_cases": loaded_design_compare,
    }, indent=2))


if __name__ == "__main__":
    main()
