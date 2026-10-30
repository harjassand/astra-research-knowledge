# Excessive-envelope form of the additional restoring exit

This completion is separate from the frozen carried-face proposal. It gives a direct operator formulation of its Section2.

Fix the finite graded/phase flag state used in the accepted dormant processor. Regard seed, designated section and designated degree outputs as terminal; the physical chain otherwise has only connector jumps. Let P be its substochastic embedded continuation kernel. Write W for the nonnegative profile reward on the extended state and K W for the actual terminal-output reward. Define

    V = sum_{j>=0} P^j (W + K W).

The jump-envelope argument in the main note is precisely V<=C W. Also V>=W. Nonnegative iteration gives

    P V + K W = V-W.

Thus V is excessive for the process killed at its original terminal events (and has an additional nonnegative terminal margin). With q its total original jump intensity, the killed generator obeys

    L_killed V = q(PV-V) = -q(W+KW) <=0.

If some original transitions are flagged as terminal, their destinations are the cemetery in this equation; their reward has already been put in KW. Localize both state and time before using optional stopping. For ANY extra nonnegative killing rate k(x), including an arbitrarily large rate, the additional exit at sigma therefore satisfies

    E[V(Y_sigma); sigma<tau_original] <= V(Y_0),
    E[W(Y_sigma); sigma<tau_original] <= C W(Y_0).

Equivalently, with D_k the multiplication operator,

    (-(L_killed-D_k))^(-1) D_k W <= V <= C W.

The equality is interpreted as the nonnegative minimal potential, obtained by truncation; no a priori full-network recurrence is used. The same argument permits a jump kernel at the extra exit whenever its reward is bounded by the current W. A restoring event in the raw class has EXACTLY equal W because it preserves A,N,B and every rare-degree/initial-phase flag. Mixtures of restoring products do not change this equality.

This also shows why an extra exit is not charged degree one or degree m: it changes no counter. Finite marked versions use the extended-state W and the same nonnegative kernel identity, so killing cannot manufacture a rare mark. Terminal grading must use the ACTUAL flag and phase, never a later seed output.

Occupation domination alone would not prove the exit bound, because k can be unbounded. The earned excessive envelope V, or equivalently the jump-sum estimate, is essential. Constants may depend on the fixed requested profiles/tilts and rates but not on hidden mass or h(hidden).
