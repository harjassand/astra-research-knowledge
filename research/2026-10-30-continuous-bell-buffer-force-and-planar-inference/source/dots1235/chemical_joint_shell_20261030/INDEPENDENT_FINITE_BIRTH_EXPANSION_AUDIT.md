# Independent audit: finite-birth tail-return expansion

Reviewed 2026-10-30. Scope: the norm remainder and finite-computation mechanism in `FINITE_BIRTH_TAIL_EXPANSION_CANDIDATE.md`, not existence of a finite-head negative certificate or a larger recurrence theorem.

## 1. Renewal decomposition and norm remainder

Let A be the zero-birth head-return kernel and T the first-birth transition operator, stopped at head return, cap exit, or low-residual exit. A first birth landing in the head may be treated by making the head continuation the identity. Cap/threshold exits have zero continuation. Then R=A+TR. A preserves the residual exactly and has row mass at most one. T changes it by a bounded amount and has first-birth probability <=s^{-g+o(1)}, uniformly on the cap.

For phi as displayed, T's weighted row norm is <=s^{-(g-alpha J)+o(1)}. After increasing the threshold its global weighted norm is below 1/2, so the positive Neumann expansion converges and R has norm at most two. This can be established from the series directly; boundedness of R need not be assumed in advance. The ordinary birth probabilities are also uniformly below one, so infinitely many successive birth restarts have probability zero. Each zero-birth descent visits finitely many finite conservative fibers. Thus the construction does not conceal an explosion or assume recurrence.

The exact remainder after fewer than K births is T^K R. Before those K births the residual differs from its initial value by at most KJ. Consequently all K local norm estimates are evaluated at s+O(K), and their product is s^{-K(g-alpha J)+o(1)}. The norm bound in the source should be understood rowwise at initial residual s; a global operator norm instead takes the supremum over those rows. This harmless notational distinction does not change the estimate.

The same argument holds in psi(s)=(1+s)^D phi(s) for every fixed D>=0. This stronger formulation is necessary when terminal head data grow as phi(s)s^D: after an unbounded number of births the terminal residual is not bounded by its initial value. The author explicitly added this repair during review. The resulting remainder acting on such data is <=C psi(s)s^{-K(g-alpha J)+o(1)}.

For a running cost, write the corresponding renewal equation with the expected cost of a single stopped zero-birth/first-birth attempt as its inhomogeneous term. The earned absorption-time estimate bounds that term in an appropriate polynomially enlarged weight; the same remainder proof applies. For cost phi(s) in the stated resource-gap setting, the no-birth attempt time is s^{-q+o(1)}, so phi itself already bounds this term at large s. If a different cost needs an extra polynomial factor, that exponent must be included in D rather than omitted.

## 2. Fixed K really gives finite computation

A physical jump from a fixed composition head enters a bounded N range. Conservative motion leaves N fixed, clearing decreases it, and each birth increases it by at most a fixed amount. Before the Kth birth, N is therefore bounded by a constant depending on K and the head, not on s. Residual offsets also range over finitely many integers in [-KJ,KJ]. Once s is sufficiently large, all these fibers lie strictly below the polylog cap, so the moving cap contributes no unknown state space to the fixed truncation.

One can augment the finite states by the birth counter and residual offset, then use ordinary killed resolvents or successive conservative-shell inverses. Arbitrarily many conservative transitions are summed exactly by those finite inverses; they do not require a mixing approximation or a finite jump-count truncation.

The finite-algebra assertion needs a coordinate hypothesis: on each fixed fiber, physical resource counts must be affine or rational functions of s, as B=s+g_N is here, and the actual rate coefficients must have the corresponding fixed rational dependence. Mass action plus an arbitrary bounded-jump residual alone is insufficient. The source was amended to state the coordinate requirement explicitly. This assertion should not silently inherit the earlier arbitrary state-dependent-coefficient scope.

Exact factorial weight ratios for bounded integer residual shifts and rational alpha are generally algebraic, with Puiseux expansions at infinity, not rational functions of s^(1/q). For example, sqrt(s+1) is not rational in sqrt(s). This distinction was raised and repaired in the source. The additional subexponential tilt remains an explicit nonalgebraic analytic factor. Its logarithmic asymptotics must be retained or controlled to finer order than the proposed negative margin; finite matrix inversion alone does not certify that sign.

## 3. Head-entry shift correction

If a head-to-tail transition changes residual from s to s+ell, the remainder is initially evaluated in psi(s+ell), not psi(s). A raw rate bound C s^Q therefore produces error

    C phi(s) s^{D+Q+alpha J_head,+ -K(g-alpha J)+o(1)},

where J_head,+ bounds positive entrance shifts. Thus a sufficient strict inequality is

    K(g-alpha J)>D+Q+alpha J_head,+ +m.

Equivalently, define Q as the exponent of the phi-weighted head-to-tail entrance operator, incorporating phi(s+ell)/phi(s), and retain the original D+Q+m criterion. The author was asked to make this correction explicit. For the original hard-network H=8 head, entrance residual shifts are nonpositive, but that special fact does not justify the omission in a generic statement.

## Scope

Subject to the stated repairs, the finite-birth expansion is a valid verification mechanism. It supplies a controlled approximation of the ACTUAL return kernel and cost, not a stationary average. It does not prove that a positive profile with strict finite-head sign exists, that increasing K eventually finds one, that a rational profile class is complete, or that global collar feedback can be absorbed. Those remain explicit independent obligations.

### Final repair verification

The current source now defines Q as the PHI-weighted head-to-tail entrance exponent, explicitly including phi(s+ell)/phi(s). This resolves the fourth issue above and makes the displayed D+Q+m criterion correct. The heavier terminal-profile weight, algebraic-versus-rational distinction, and resource-coordinate representation requirement are also present. Verdict on the amended norm/finite-computation mechanism: **pass**, with finite-head sign and global interface still unproved.

### Reviewed source hash
96dca109ff42f51a59fb4d582d6c49415f1bce2412a46be55de52c540a257edc  chemical_joint_shell_20261030/FINITE_BIRTH_TAIL_EXPANSION_CANDIDATE.md
