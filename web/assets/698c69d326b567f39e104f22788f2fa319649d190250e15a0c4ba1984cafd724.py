#!/usr/bin/env python3
"""Exact carbon bounds and transfer thresholds for the CDT-1/GH1-1 route.

The measured 5 mM U-13C12-cellobiose pulse in the Miller et al. source is an
initial substrate concentration, not a measured uptake or secretion flux.
All outputs below are therefore stoichiometric limits or symbolic assay gates,
not estimates of actual T-cell leakage.
"""

from fractions import Fraction
import json


def max_lactate_mM(cellobiose_feed_mM, uptake_fraction=Fraction(1),
                   lactate_branch_fraction=Fraction(1)):
    """Upper lactate concentration (mM) for batch feed and stated fractions.

    One cellobiose yields two C6 glucose units; full conversion to lactate
    yields four C3 lactate molecules.  Fractions refer to substrate consumed
    and carbon routed to lactate, respectively.
    """
    feed = Fraction(cellobiose_feed_mM)
    uptake = Fraction(uptake_fraction)
    branch = Fraction(lactate_branch_fraction)
    if feed < 0 or not (0 <= uptake <= 1) or not (0 <= branch <= 1):
        raise ValueError("feed must be nonnegative and fractions in [0, 1]")
    return 4 * feed * uptake * branch


def tumor_glucose_equivalent_flux(q_cellobiose_per_effector_h,
                                  effector_to_target_ratio,
                                  lactate_export_fraction,
                                  target_capture_fraction):
    """Tumor-available glucose equivalents per target per hour.

    q is mol cellobiose / effector / h.  Two C6 glucose equivalents are
    available per cellobiose.  This is a carbon-equivalent comparison; it does
    not claim equal ATP yield from lactate and glucose.
    """
    q = Fraction(q_cellobiose_per_effector_h)
    ratio = Fraction(effector_to_target_ratio)
    export = Fraction(lactate_export_fraction)
    capture = Fraction(target_capture_fraction)
    if min(q, ratio) < 0 or not (0 <= export <= 1) or not (0 <= capture <= 1):
        raise ValueError("flux/ratio must be nonnegative and fractions in [0, 1]")
    return 2 * q * ratio * export * capture


def required_export_fraction(target_deficit_glucose_eq_per_target_h,
                             q_cellobiose_per_effector_h,
                             effector_to_target_ratio,
                             target_capture_fraction):
    """Required cellobiose-carbon-to-lactate fraction for a target flux gate."""
    deficit = Fraction(target_deficit_glucose_eq_per_target_h)
    q = Fraction(q_cellobiose_per_effector_h)
    ratio = Fraction(effector_to_target_ratio)
    capture = Fraction(target_capture_fraction)
    if deficit < 0 or min(q, ratio) < 0 or not (0 <= capture <= 1):
        raise ValueError("deficit/flux/ratio must be nonnegative; capture in [0, 1]")
    capacity = 2 * q * ratio * capture
    if capacity == 0:
        return None
    return deficit / capacity




def tracer_mass_mg(cellobiose_mM, sample_volume_mL, labeled_sample_count,
                   molecular_weight_g_mol=Fraction(35421, 100)):
    """Nominal U-13C12-cellobiose mass required for a batch of tracer samples."""
    concentration = Fraction(cellobiose_mM)
    volume = Fraction(sample_volume_mL)
    count = Fraction(labeled_sample_count)
    molecular_weight = Fraction(molecular_weight_g_mol)
    if min(concentration, volume, count, molecular_weight) < 0:
        raise ValueError("concentration, volume, count, and molecular weight must be nonnegative")
    # mM * g/mol = mg/L; mL to L contributes the factor 1/1000.
    return concentration * molecular_weight * volume * count / 1000


def target_available_fraction(lactate_export_fraction, target_capture_fraction):
    """Share of consumed carbon reaching targets through the lactate branch."""
    export = Fraction(lactate_export_fraction)
    capture = Fraction(target_capture_fraction)
    if not (0 <= export <= 1) or not (0 <= capture <= 1):
        raise ValueError("export and capture fractions must be in [0, 1]")
    return export * capture


def interface_completion(cellobiose_mM, target_available_share):
    """Stoichiometric completion for any interface share in [0, 1].

    Choose lactate export fraction equal to the requested share and target
    capture equal to one. This is an outer-interface witness, not a fit to the
    source's full intracellular isotope measurements or T-cell kinetics.
    """
    amount = Fraction(cellobiose_mM)
    share = Fraction(target_available_share)
    if amount < 0 or not (0 <= share <= 1):
        raise ValueError("feed must be nonnegative and share must be in [0, 1]")
    carbon = 12 * amount
    return {
        "cellobiose_feed_mM": amount,
        "carbon_input_mM": carbon,
        "lactate_export_fraction": share,
        "target_capture_fraction": Fraction(1),
        "target_available_carbon_mM": carbon * share,
        "other_carbon_mM": carbon * (1 - share),
        "lactate_export_mM": 4 * amount * share,
    }


def carbon_partition(cellobiose_mM, public_fraction):
    """Atom-balance split: public lactate carbon vs other carbon."""
    amount = Fraction(cellobiose_mM)
    public = Fraction(public_fraction)
    if amount < 0 or not (0 <= public <= 1):
        raise ValueError("cellobiose must be nonnegative; fraction in [0, 1]")
    total_c = 12 * amount
    return {
        "input_carbon_mM": total_c,
        "public_lactate_carbon_mM": total_c * public,
        "other_carbon_mM": total_c * (1 - public),
        "lactate_mM": 4 * amount * public,
    }


def main():
    feed = Fraction(5)
    assert max_lactate_mM(feed) == 20
    assert max_lactate_mM(feed, Fraction(1), Fraction(1, 4)) == 5
    no_leak = carbon_partition(feed, Fraction(0))
    all_lactate = carbon_partition(feed, Fraction(1))
    zero_transfer = target_available_fraction(Fraction(0), Fraction(1))
    maximal_transfer = target_available_fraction(Fraction(1), Fraction(1))
    zero_completion = interface_completion(feed, Fraction(0))
    maximal_completion = interface_completion(feed, Fraction(1))
    tracer_200uL_mg = tracer_mass_mg(Fraction(5), Fraction(1, 5), 120)
    tracer_1mL_mg = tracer_mass_mg(Fraction(5), Fraction(1), 120)
    assert no_leak["public_lactate_carbon_mM"] == 0
    assert all_lactate["other_carbon_mM"] == 0
    assert (no_leak["input_carbon_mM"] == all_lactate["input_carbon_mM"] == 60)
    assert (zero_transfer, maximal_transfer) == (Fraction(0), Fraction(1))
    result = {
        "status": "stoichiometric ceiling only; no actual leak inferred",
        "source_pulse_cellobiose_mM": str(feed),
        "source_pulse_duration_h": 16,
        "carbon_atoms_input_mM": str(12 * feed),
        "glucose_equivalents_max_mM": str(2 * feed),
        "lactate_max_if_all_consumed_and_fermented_mM": str(
            max_lactate_mM(feed)
        ),
        "target_available_fraction_outer_envelope_from_reported_measurement_interface":
            {"lower": "0", "upper": "1", "supremum": "1"},
        "envelope_scope": (
            "Stoichiometric measurement-interface no-go; endpoints are not "
            "claimed to fit every intracellular isotope peak exactly."
        ),
        "missing_quantities": [
            "total cellobiose uptake in coculture",
            "species-resolved extracellular labeled-carbon balance",
            "target capture/use of secreted products",
        ],
        "proton_symport_stoichiometry": "1 H+ imported per cellobiose (source-reported)",
        "illustrative_acquisition_budget": {
            "media_sample_count": 240,
            "tracer_fed_sample_count": 120,
            "labeled_cellobiose_molecular_weight_g_mol": "354.21",
            "nominal_tracer_mass_mg_at_200uL_per_tracer_sample": str(tracer_200uL_mg),
            "nominal_tracer_mass_mg_at_1mL_per_tracer_sample": str(tracer_1mL_mg),
            "excludes": ["standards", "dead volume", "pilot losses", "repeats"],
            "vendor_price": "quote-only",
        },
        "example_fraction_for_5mM_lactate": str(Fraction(5, 20)),
        "example_fraction_for_10mM_lactate": str(Fraction(10, 20)),
        "examples_are_not_empirical_thresholds": True,
        "measurement_interface_completion_witnesses_not_full_isotope_fits": {
            "zero_transfer": {k: str(v) for k, v in zero_completion.items()},
            "upper_limit": {k: str(v) for k, v in maximal_completion.items()},
            "target_available_fraction_endpoints": {
                "zero": str(zero_transfer),
                "upper_limit": str(maximal_transfer),
            },
        },
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
