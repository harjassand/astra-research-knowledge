# Preserved reviewer counterexample to the original blanket halo application

The original exact halo INTERFACE identity was correct, but its first receiving application incorrectly skipped all-zero-residual components.

Reviewer example:

    0 → A+B →3A+2B →0, all rates1,
    J={B=0}, unbounded count A.

The residual set Z={0} gives halo phases{0,1,2}. With beta=(0,−1,−3), every lifted residual increment is0. Thus the full halo decomposes into finite residual classes and cannot have strictly negative adjoint at all its states.

This is not repaired merely by restricting to a fixed physical class: the original network has full stoichiometric rank, and all(n,0), n≥0, lie in the class of0. Starting from(n,0), the enabled sequence immigration, connector, connector, clear, connector, clear adds net(1,0); weak reversibility gives return paths.

The corrected application solves the finite killed phase system on J versus H\\J at each conserved residual. It produces local strict negativity in J, without asserting negativity on the entire neutral halo. The correction is recorded in FINITE_HALO_EXACT_CORNER_INTERFACE.md. No earlier failure is silently relabeled as an independently reviewed success.
