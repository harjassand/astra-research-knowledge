"""ASTRA 2026-10-25: chemistry-of-completion and error-removal bounds.

Reproducible arithmetic only. Not a simulation or validation of chemical kinetics.
Only externally sourced number used for the illustrative ring example is the
22% cyclic / 78% linear outcome for one tested substrate in Lee et al. (2025),
Nature Communications, doi:10.1038/s41467-025-60126-4.

Chemically distinct outcomes:
 DNA upstream 3'-O-acyl donor -> empty 3'-OH by productive transfer OR hydrolysis.
 Ribosome P-site peptidyl-tRNA -> empty donor by product transfer OR hydrolysis,
 but ONLY transfer installs the chain on A-site tRNA.
 Linear hydrazinedione precursor retains an accessible hydrazine; ring closure
 consumes that nucleophile (Lee 2025, aldehyde-labeling diagnostic).
"""
from math import log


def max_wrong_to_right_retention(start_correct: float, target_purity: float) -> float:
    """Bayes rule for correct/incorrect retention after a downstream filter."""
    assert 0 < start_correct < 1 and start_correct < target_purity < 1
    return start_correct*(1-target_purity)/(target_purity*(1-start_correct))


def min_per_step_fidelity(length: int, chain_yield: float) -> float:
    assert length >= 1 and 0 < chain_yield < 1
    return chain_yield**(1/length)


def donor_only_certification() -> None:
    # Empty donor is produced by both transitions. Thus no function of the
    # single observable 'donor_empty' can discriminate their outcomes.
    productive = {"donor_empty": True, "recipient_carries_chain": True,
                  "free_chain": False}
    hydrolysis = {"donor_empty": True, "recipient_carries_chain": False,
                  "free_chain": True}
    assert productive["donor_empty"] == hydrolysis["donor_empty"]
    assert productive["recipient_carries_chain"] != hydrolysis["recipient_carries_chain"]
    # The ribosome's chemistry uniquely distinguishes occupancy of the next
    # carrier in this pair of outcomes; do not infer the motor senses occupancy.


def main() -> None:
    donor_only_certification()
    p = 0.22  # illustrative substrate-specific observed cyclization fraction
    print("LEE 2025 substrate example: observed ring fraction",p)
    print("Assuming independent repeated events (UNMEASURED for multi-ring products):")
    for n in [1,2,3,5]:
        initial=p**n
        if initial <= 0 or initial>=.99: continue
        maxratio=max_wrong_to_right_retention(initial,.99)
        print(f"{n} motifs: unfiltered all-correct={initial:.8f}; "
              f"wrong/correct retention <= {maxratio:.8f}; "
              f"needed rejection discrimination >= {1/maxratio:.1f}x")
    print("If correct-retention=0.90 for one ring, maximum wrong-retention=",
          .9 * max_wrong_to_right_retention(p,.99))
    print("Minimum independent per-step fidelity for 99% 20-step correct chain:",
          min_per_step_fidelity(20,.99))
    # Algebraic posterior identity using a high-level, not kinetic, filter.
    r=max_wrong_to_right_retention(p,.99)
    post=p/(p+(1-p)*r)
    assert abs(post-.99) < 1e-12
    print("Passed exact outcome aliasing and Bayesian purity consistency checks")

if __name__ == '__main__':
    main()
