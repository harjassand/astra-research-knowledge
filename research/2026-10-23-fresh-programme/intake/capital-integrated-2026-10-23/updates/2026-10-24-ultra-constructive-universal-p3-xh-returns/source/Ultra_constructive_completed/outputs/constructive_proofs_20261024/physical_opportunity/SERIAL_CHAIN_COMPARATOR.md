# Strong serial-chain comparator at the same total mass and static stiffness

This supplement is separate from the stable PHONON_OPTIMUM.md proof. It compares the positive pendant-resonator construction to a broader ordinary serial-chain family whose Bloch matrix is not generally the rank-one backbone form.

Consider any finite-period one-dimensional scalar chain with positive masses m_j and positive nearest-neighbor springs k_j in series, no extra side branch or onsite foundation. Each period contains total mass
M=sum_j m_j
and static end-to-end stiffness
K_eff=1/[sum_j(1/k_j)].
Allow arbitrary mass allocation, spring contrast, period length in sites and dimerization. Compare cells at the same physical period spacing, M and K_eff, with ideal intrinsic harmonic ballistic transport.

At the antiperiodic Bloch wave number q=pi the dynamic matrix is real, so a minimizing eigenvector can be chosen real. Extend that vector by u_(j+n)=-u_j. Let A=max_j|u_j|>0 and start the cell at a site attaining A. Its next-period copy has displacement -u_j, so the displacement change across the n consecutive links has magnitude2A.

Cauchy-Schwarz along those links gives
sum_j k_j (u_(j+1)-u_j)^2
>= [sum_j (u_(j+1)-u_j)]^2 / sum_j(1/k_j)
=4 K_eff A^2.
Meanwhile
sum_j m_j u_j^2 <= M A^2.
Each shifted cell counts every periodic spring and mass once. Therefore EVERY antiperiodic Rayleigh quotient is at least4K_eff/M, hence
lambda_min(q=pi)>=4K_eff/M.

The lowest Bloch eigenvalue is continuous in q and is zero at q=0 by rigid translation. Its image consequently contains every squared frequency from0 to4K_eff/M, even if its q dependence is not monotone. Except isolated stationary/degenerate frequencies of zero measure, time-reversal symmetry supplies a right-moving mode for each such frequency.

Thus the full intrinsic thermal transmission multiplicity is at least one throughout
[0,Omega_r], Omega_r=2sqrt(K_eff/M).
All additional acoustic/optical branches only add nonnegative conductance. At EVERY temperature,
J_serial >= integral_0^Omega_r g_theta(omega) domega = J_rigid.

The ordinary rigid-total-mass chain attains the lower bound. The positive construction in PHONON_OPTIMUM.md has the same M and K_eff=K but J_*<J_rigid at its specified finite temperature, so no purely serial mass redistribution, dimerization or positive linear stiffness allocation in this family reproduces that benefit. Its internal pendant degree of freedom is a load-bearing operation.

This is an exact scalar harmonic comparator theorem, not a claim about all alternative materials. Parallel/multiple intercell connections, nonlocal links, extra acoustic polarizations, disorder/localization, nonlinearity/damping and contact-resistance engineering remain different classes.

Root independently reconstructed this antiperiodic argument. No historical novelty or physical material validation is inferred.

