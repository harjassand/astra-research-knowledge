#!/usr/bin/env python3
"""Exact finite SU(4)/SU(5) falsification diagnostics for spectral profiles.

Uses the adjacent exact_lr_search.py integer LR-tableau and zero-weight
tableau routines. The tested stable window C2(nu)<(1+min_i a_i)^2 is an
explicit diagnostic hypothesis, not an imported theorem. All arithmetic in
the checks is integer/Fraction exact.
"""

from fractions import Fraction
from itertools import product

from exact_lr_search import (
    canonical_partition,
    casimir,
    dimension,
    end_decomposition,
    zero_weight_multiplicity,
)


CASES = (
    (4, (1, 1, 1)),
    (4, (2, 2, 2)),
    (4, (1, 2, 1)),
    (5, (1, 1, 1, 1)),
    (5, (2, 2, 2, 2)),
    (5, (3, 3, 3, 3)),
    (5, (2, 1, 2, 1)),
)


def candidate_labels_below(m: int, cutoff: Fraction):
    """Enumerate all dominant labels with C2<cutoff using a safe norm cap.

    For type A, <omega_i,omega_j> >= 0 and ||omega_i||^2 >= (m-1)/m.
    Hence C2(sum a_i omega_i) >= (m-1)/(2m) * a_i^2 for every i.
    """
    if cutoff <= 0:
        return
    max_coordinate = 0
    while Fraction(m - 1, 2 * m) * (max_coordinate + 1) ** 2 < cutoff:
        max_coordinate += 1
    for labels in product(range(max_coordinate + 1), repeat=m - 1):
        if casimir(canonical_partition(labels)) < cutoff:
            yield labels


def check_normalization(m: int):
    fundamental = (1,) + (0,) * (m - 2)
    adjoint = (1,) + (0,) * (m - 3) + (1,)
    cf = casimir(canonical_partition(fundamental))
    ca = casimir(canonical_partition(adjoint))
    assert cf == Fraction(m * m - 1, 2 * m), (m, cf)
    assert ca == m, (m, ca)
    assert dimension(canonical_partition(adjoint)) == m * m - 1
    return cf, ca


def analyze(m: int, labels: tuple[int, ...]):
    lam, dual, decomposition, witnesses = end_decomposition(labels)
    carrier_dim = dimension(lam)
    total_dim = sum(
        mult * dimension(canonical_partition(nu))
        for nu, mult in decomposition.items()
    )
    assert total_dim == carrier_dim**2
    assert decomposition.get((0,) * (m - 1), 0) == 1
    adjoint = (1,) + (0,) * (m - 3) + (1,)
    assert decomposition.get(adjoint, 0) == m - 1

    # Empirical stable-window diagnostic. Include absent nu in the comparison:
    # their End multiplicity is exactly zero.
    delta = min(labels) + 1
    cutoff = Fraction(delta * delta)
    tested = []
    discrepancies = []
    for nu in candidate_labels_below(m, cutoff):
        c = casimir(canonical_partition(nu))
        actual = decomposition.get(nu, 0)
        zero = zero_weight_multiplicity(canonical_partition(nu))
        tested.append((nu, c, actual, zero))
        if actual != zero:
            discrepancies.append((nu, c, actual, zero))

    # Find the first supported output where equality with zero-weight
    # multiplicity ceases. This locates an exact finite boundary beyond the
    # candidate window; only support labels are scanned here.
    first_output_mismatch = None
    compared_outputs = 0
    for nu, actual in sorted(
        decomposition.items(),
        key=lambda item: (casimir(canonical_partition(item[0])), item[0]),
    ):
        zero = zero_weight_multiplicity(canonical_partition(nu))
        compared_outputs += 1
        if actual != zero:
            first_output_mismatch = (
                nu, casimir(canonical_partition(nu)), actual, zero
            )
            break
    assert first_output_mismatch is not None
    assert first_output_mismatch[1] > cutoff

    # Exact Casimir shell masses and right-continuous D(T).
    shell_mass = {}
    for nu, mult in decomposition.items():
        part = canonical_partition(nu)
        c = casimir(part)
        shell_mass[c] = shell_mass.get(c, 0) + mult * dimension(part)
    levels = sorted(shell_mass)
    positive_levels = [c for c in levels if c > 0]
    assert positive_levels and positive_levels[0] == m
    assert shell_mass[Fraction(m)] == (m - 1) * (m * m - 1)
    cumulative = 0
    shell_rows = []
    # Continuous-T suprema can be evaluated at shell-entry points because D
    # is a right-continuous step function and each denominator is increasing.
    # Remove the trivial shell for the unshifted T^p ratio: otherwise
    # sup_{T>0} D(T)/T^p is infinite on 0<T<m (D(T)=1 there).
    max_Dplus_over_T_pow_p = None
    max_Dplus_ratio_at = None
    max_Dplus_over_1_plus_T_pow_p = Fraction(0)
    max_Dplus_shifted_ratio_at = None
    max_D_over_1_plus_T_pow_p = Fraction(1)  # attained at T=0
    max_D_shifted_ratio_at = Fraction(0)
    p = m * (m - 1) // 2
    for c in levels:
        cumulative += shell_mass[c]
        shell_rows.append((c, shell_mass[c], cumulative))
        if c > 0:
            Dplus = cumulative - 1
            ratio = Fraction(Dplus, 1) / c**p
            if max_Dplus_over_T_pow_p is None or ratio > max_Dplus_over_T_pow_p:
                max_Dplus_over_T_pow_p, max_Dplus_ratio_at = ratio, c
            shifted_plus_ratio = Fraction(Dplus, 1) / (1 + c) ** p
            if shifted_plus_ratio > max_Dplus_over_1_plus_T_pow_p:
                max_Dplus_over_1_plus_T_pow_p = shifted_plus_ratio
                max_Dplus_shifted_ratio_at = c
            shifted_total_ratio = Fraction(cumulative, 1) / (1 + c) ** p
            if shifted_total_ratio > max_D_over_1_plus_T_pow_p:
                max_D_over_1_plus_T_pow_p = shifted_total_ratio
                max_D_shifted_ratio_at = c
    # This is the finite-carrier C=1 shell-count test stated in the receipt.
    assert max_D_over_1_plus_T_pow_p == 1, (m, labels, max_D_over_1_plus_T_pow_p)
    assert cumulative == carrier_dim**2

    # Selected exact cumulative values at the adjoint and candidate cutoff.
    def D(t):
        return sum(mass for c, mass in shell_mass.items() if c <= t)

    stable_last = max((c for c in levels if c < cutoff), default=Fraction(-1))
    key_T = sorted({Fraction(0), Fraction(m), stable_last, cutoff})
    key_D = [(t, D(t)) for t in key_T]
    head_shells = shell_rows[: min(12, len(shell_rows))]

    return {
        "m": m,
        "labels": labels,
        "dual_partition": dual,
        "carrier_dim": carrier_dim,
        "output_irreps": len(decomposition),
        "decomposition_dimension_sum": total_dim,
        "delta": delta,
        "stable_cutoff": cutoff,
        "stable_candidates": len(tested),
        "stable_discrepancies": discrepancies,
        "stable_zero_weight_positive": sum(1 for row in tested if row[3] > 0),
        "stable_end_positive": sum(1 for row in tested if row[2] > 0),
        "stable_examples": tested,
        "first_output_mismatch": first_output_mismatch,
        "outputs_compared_to_first_mismatch": compared_outputs,
        "shell_levels": len(levels),
        "first_positive_shell": (positive_levels[0], shell_mass[positive_levels[0]]),
        "D_key": key_D,
        "first_shells": head_shells,
        "last_shell": shell_rows[-1],
        "max_Dplus_over_T_pow_p_for_T_positive": max_Dplus_over_T_pow_p,
        "max_Dplus_ratio_at": max_Dplus_ratio_at,
        "max_Dplus_over_1_plus_T_pow_p_for_T_positive": max_Dplus_over_1_plus_T_pow_p,
        "max_Dplus_shifted_ratio_at": max_Dplus_shifted_ratio_at,
        "max_D_over_1_plus_T_pow_p_for_T_nonnegative": max_D_over_1_plus_T_pow_p,
        "max_D_shifted_ratio_at": max_D_shifted_ratio_at,
        "p": p,
    }


def main():
    for m in (4, 5):
        cf, ca = check_normalization(m)
        print(f"SU({m}) normalization: C2(fund)={cf}; C2(adj)={ca}; dim(adj)={m*m-1}")
    for m, labels in CASES:
        result = analyze(m, labels)
        print(
            f"SU({m}) lambda={labels}: d={result['carrier_dim']}, "
            f"End irreps={result['output_irreps']}, "
            f"sum mult*dim={result['decomposition_dimension_sum']}, "
            f"Delta={result['delta']}, tested C2<Delta^2={result['stable_cutoff']}: "
            f"{result['stable_candidates']} weights, "
            f"positive zero-weight={result['stable_zero_weight_positive']}, "
            f"positive End={result['stable_end_positive']}, "
            f"discrepancies={len(result['stable_discrepancies'])}"
        )
        if result["stable_discrepancies"]:
            print("  FIRST STABLE-WINDOW DISCREPANCY:", result["stable_discrepancies"][0])
        print(
            f"  first supported mismatch with zero-weight multiplicity after "
            f"{result['outputs_compared_to_first_mismatch']} outputs: "
            f"{result['first_output_mismatch']}"
        )
        print(
            f"  p={result['p']}, distinct Casimir shells={result['shell_levels']}, "
            f"first positive shell={result['first_positive_shell']}, "
            f"key D(T)={result['D_key']}, "
            f"max exact (D(T)-1)/T^p for T>0="
            f"{result['max_Dplus_over_T_pow_p_for_T_positive']} "
            f"at T={result['max_Dplus_ratio_at']}; "
            f"max D(T)/(1+T)^p for T>=0="
            f"{result['max_D_over_1_plus_T_pow_p_for_T_nonnegative']} "
            f"at T={result['max_D_shifted_ratio_at']}; "
            f"max (D(T)-1)/(1+T)^p for T>0="
            f"{result['max_Dplus_over_1_plus_T_pow_p_for_T_positive']} "
            f"at T={result['max_Dplus_shifted_ratio_at']}"
        )
        print("  first shells (C2, shell mass, cumulative D):", result["first_shells"])
        print("  final shell (C2, mass, cumulative D):", result["last_shell"])
        assert not result["stable_discrepancies"]


if __name__ == "__main__":
    main()
