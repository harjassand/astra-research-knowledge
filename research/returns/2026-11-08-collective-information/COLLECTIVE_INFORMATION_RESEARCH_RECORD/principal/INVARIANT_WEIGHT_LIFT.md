# Pressure reuse for sector-invariant and approximately invariant weights

This strengthens the prescribed-test-weight restriction of the final cell attack. It concerns weights in an observable/Feynman-Kac test, not an uncontrolled feedback change of the microscopic generator. It does not by itself prove a nonlinear hydrodynamic forecast.

## Exact sector-invariant extension

Use the one-dimensional ring and L-site closed block generators G_x from the constructor's pressure lemma. The positive full generator is G_N, and sum_x G_x=(L-1)G_N. Assume every W_x is centered conditional on the block count and exterior, |W_x|<=B, every nontrivial conditional gap is at least g, and every conditional resolvent variance is at most V. Empty sectors must have W_x=0. Use distinct-site geometry with all bare-rate exterior bits included, for example N>2(L+2r), and an admissible corrector supported inside each block.

Let a_x(t,eta) be measurable functions, |a_x|<=A, that are invariant under every exchange internal to their own block. Equivalently a_x is measurable with respect to that block's outside configuration and count. They may be nonlinear functions of those variables. Their prescribed functional dependence can vary with time. For any positive tilt b satisfying b A B/(N g)<=1/2,

    lambda_max[-N^2G_N+(bN/L)sum_x a_x(t,eta)W_x(eta)]/N
        <=2b^2 A^2 V/L.

Consequently, from any microscopic initial law,

    |E integral_0^T (1/L)sum_x a_x(t,eta_t)W_x(eta_t)dt|
        <=log(2)/b+2b A^2 T V/L.

Here b is an entropy/test tilt, not inverse temperature. The absolute value is OUTSIDE the expectation; E|integral| and a path supremum are not claimed.

**Proof.** Condition each block form on its exterior and count. Its a_x is a scalar on that fiber, so a_xW_x is centered there and its variance is a_x^2 times that of W_x. Apply the proved finite-dimensional inequality with s=b a_x(L-1)/(NL). The gap condition bounds its denominator by 1/2. Conditional quadratic forms can be integrated and summed without requiring independent or disjoint blocks. The same counting gives the displayed full-generator bound. Integrate the instantaneous spectral bound for prescribed time-dependent functions, apply entropy inequality against stationary Bernoulli(1/2), and use H(mu_0|Bernoulli(1/2)^N)<=Nlog2. Repeat with -a_x for the opposite sign. No step assumes that a_x is independent of eta; only fiber invariance is used.

## Approximate invariance

If bounded a_x have invariant approximants abar_x with |a_x-abar_x|<=e_a and |abar_x|<=A, then the same integrated signed expectation bound has the additional deterministic error T N B e_a/L. A bounded conditional average on the uniform count fiber is one possible approximant; one need not compute it if its existence and uniform error are proved analytically. Arbitrary state dependence has no such guarantee: in a two-state symmetric chain W=+/-1 and a=W make aW=1, producing a first-order pressure rather than the centered quadratic one.

## Explicit density-height example

Index ring sites by integers modulo N. For a prescribed u_j(t) in [0,1], put e_j=eta_j-u_j and define the mean-zero discrete primitive

    h_x=N^(-2)sum_(j=0)^(N-1) [j-(N-1)/2]e_(x+j).

Then |h_x|<=1 and h_(x+1)-h_x=(e_x-mean(e))/N. For the forward block {x,...,x+L-1}, average h_x over all configurations with its count fixed and the outside frozen. The deterministic u contribution cancels in the difference, and

    |h_x-abar_h_x|<=N^(-2)sum_(j=0)^(L-1)j
                     <=L^2/(2N^2).

Thus h_x is an approximately invariant test weight with a pressure-replacement error at most T B L/(2N), in addition to the measured-variance terms. This holds even when that forward block wraps around the ring: the formula uses offsets relative to x and the fixed-count constant part cancels.

The height is linear in the density. A nonlinear function Phi(h_x) inherits the same error multiplied by a declared Lipschitz constant for Phi; boundedness alone does not suffice.

More generally, a weight N^(-1)sum_j K_x(j/N)(eta_j-u_j) with kernel Lipschitz constant C_K has oscillation under its own fixed-count block at most C_K L^2/N^2, provided K_x has no jump inside that block. Finite Fourier test kernels satisfy this with a computable C_K depending on the retained mode count. This is a route to testing nonlinear macroscopic error energies, without the false independence assumption for overlapping cells.

## Unclosed operation

The exact conditional-invariance extension and the deterministic approximation bound are complete finite-system statements. Turning them into the nonlinear density PDE theorem still needs the microscopic current decomposition, corrector time-boundary terms, nonlinear local-equilibrium/one- or two-block replacement, finite-mode stochastic errors and stability of the resulting limit equation, with compatible scales. Neither the height lemma nor the variance assay supplies those terms. In particular, multiplying a microscopic residual by a state-dependent weight cannot be declared harmless merely because the weight is macroscopically smooth; the displayed oscillation budget must be paid.
