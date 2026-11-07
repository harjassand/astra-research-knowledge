# Review of invariant-weight pressure reuse and succinct correctors

Auditor, 7 November 2026. Exact files checked:

- principal/INVARIANT_WEIGHT_LIFT.md: SHA256 **518f72e0eedf3127ba326fc13f8d85e1d38760ebfdb68addf99467481cb14189**.
- principal/SUCCINCT_POISSON_CORRECTOR.md: SHA256 **0d7e8332871fac07b89aaf2b56e22565b403d62f1fedfa12eabf14c47f10cfdc**.

No main/source edits made. **PASS at their stated auxiliary scope**, with the score-rounding clarification below. These statements do not close finite-N nonlinear hydrodynamics.

## Invariant-weight theorem

Condition on a block's outside configuration and count. Its connected internal exchange graph makes a_x constant on that fiber. Thus even nonlinear a_x is a scalar in the conditional form; a_x W_x remains centered and has variance a_x^2 V_x. The local spectral estimate applies with s_x=b a_x(L-1)/(NL). Summing the conditional forms and using sum_x G_x=(L-1)G_N proves the stated pressure/N bound under bAB/(Ng)<=1/2. Overlap and dependence on other blocks' states require no independence. Use L>=2, or handle the trivial L=1, W=0 case separately.

Prescribed time-dependent current-state functions give bounded Feynman–Kac multiplication potentials. The instantaneous spectral bound, entropy inequality and H(mu_0|Bernoulli(1/2)^N)<=Nlog2 give exactly the signed integrated expectation bound, with the absolute value OUTSIDE expectation. It is not E|integral|, an integral of absolute values or a path-supremum statement.

This extends **test weights**, not feedback-controlled transition rates. If feedback changes the generator, centering, reversibility, gap, rate bounds and block-counting identity need new verification. History dependence not represented by a prescribed current-state function also needs a separate argument. No physical readout/control primitive for arbitrary outside functions is granted.

## Approximate invariance and height

The deterministic discrepancy is pathwise <=TNB e_a/L, directly by summing N bounded terms. For the height, coefficients sum to zero, so sum_x h_x=0. Reindexing gives h_(x+1)-h_x=(e_x-mean(e))/N. On its own FORWARD block, the deterministic u contribution cancels, count conservation removes the constant coefficient, and

|h_x-E[h_x|outside,count]|<=N^(-2)sum_(j=0)^(L-1)j
 =L(L-1)/(2N^2)<=L^2/(2N^2).

Thus the stated TBL/(2N) replacement term is valid, including wraparound in global labels. The alignment matters: at N=8,L=2, block offsets {7,0}, one occupied bit at offset0 and prescribed u=1/2, the deviation is 7/128, exceeding L^2/(2N^2)=1/32. A centered block containing the kernel jump cannot inherit the forward-block bound. Reanchoring must be explicit or its error paid.

A Lipschitz kernel without a jump inside its own block gives O(C_K L^2/N^2) by subtracting a constant kernel value. Finite Fourier kernels have computable C_K. Nonlinear Phi(h) needs a known Lipschitz constant to inherit small oscillation, for example with invariant approximant Phi(abar_h); boundedness alone is insufficient. The height is linear in eta-u, even when used in a nonlinear energy test. It also omits the mass mode: a constant discrepancy has h=0. Mass must be controlled separately.

B, g, L and T must retain their actual certified sizes. A favorable e_a power does not alone make TBL/N small when W's bound grows, and the original small-tilt condition remains necessary. Exact Fraction checks over N=2,...,9 and every L<N verify the difference identity and forward bound on every binary input; the misaligned counterexample is reproduced in checks/check_invariant_height.py and its JSON. This is a finite diagnostic, not a hydrodynamic proof.

## Succinct Poisson corrector

The tail choice gives J p_*^(-1/2)exp(-g tau)/g<=e/4. The random-time score is bounded by tau J; Hoeffding at e/2 plus a union over P2^m inputs gives exactly the stated M. Independent blocks for each fixed input suffice; correlations across inputs do not matter. Each call must reset stored blocks to their original seed positions, with fixed rounding/caps, to retain one deterministic local function.

The Poisson cap and logarithmic tail choice are conservative. The finite-bit coupling budget includes capped Poisson labels, local categorical labels and the grid-time discrepancy. Their numeric mean and all bit/evaluation costs are polynomial in the declared parameters. Shared-seed uniform approximation, the common-cap translated-energy estimate, source-prescribed shrinking cutoff and fresh residual validation justify the auxiliary observed stopping theorem as previously reviewed.

**Local implementation clarification:** clip implemented drift/trajectory scores to [-J,J] or [-tau J,tau J] before using those exact bounds in digital-score concentration, or enlarge B_score and M to cover numerical rounding. Clipping to an interval containing the ideal score cannot increase error and preserves every polynomial budget. The current phrase applying bounded concentration directly to rounded scores should make this explicit.

The energy normalization, endpoint-safe Bernoulli modulus, independent validation, acquired-rate inflation and stage confidence schedule are sound. Unknown source convergence constants enter the polynomial termination assurance rather than the returned residual certificate. Actual systematic hardware floors remain attached to attainable physical precision.

## Final boundary

The invariant/approximately invariant pressure tests, aligned height lemma and finite-program corrector are checked. Their use in nonlinear density-error energies still needs the actual current decomposition, inhomogeneous reference/profile/large-deviation terms, finite-mode stochastic errors, replacement and stability with compatible scales. No full finite-N nonlinear or feedback/force-driven prediction theorem is certified by this review.
