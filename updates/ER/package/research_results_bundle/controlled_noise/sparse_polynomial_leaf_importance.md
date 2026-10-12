# Degree-independent sparse-polynomial leaves

Compiler addendum, 2026-10-12. This is an application of the known Karpinski–Luby polynomial-counting structure, not a new claim of a sparse-polynomial FPRAS.

## Input and known inequality

Let F(U)=sum_A c_A t_A(U) be an explicitly listed Boolean multilinear vector polynomial over F_2, with m nonzero coefficient vectors and distinct monomials. Combine duplicates and remove zero coefficients first. There is no degree bound. U is uniform on the supplied independent bits.

For a linear functional ell, put p_ell=Pr[ell(F(U))=1] and

    Z_ell=sum_(A:ell(c_A)=1) 2^(-|A|).

Karpinski–Luby's union-to-odd-parity bound implies

    Z_ell <= m^2 p_ell.                                (1)

Indeed, at most m satisfied-term indicators contribute to the union measure, and the union measure is at most m times the odd-parity measure. The result includes a constant monomial. See Luby–Wigderson, section 6.3, Theorem 6.1, which attributes the counting method to Karpinski and Luby (1993): https://www.math.ias.edu/~avi/PUBLICATIONS/LubyWig2005.pdf .

## A single explicit proposal serving every linear cut

Choose one of the m monomials uniformly, then draw U uniformly conditional on that monomial being one. This means fixing its variables to one and drawing every other used variable independently. The proposal's density relative to uniform input is

    h(U)=(1/m) sum_(A:t_A(U)=1) 2^(|A|).

It is explicitly evaluable. Set g(U)=1/h(U). A proposal always has h>0. Inputs not covered by the proposal satisfy no monomial, hence F(U)=0 and are irrelevant to every nonzero cut.

Whenever ell(F(U))=1, at least one cut-active monomial A is true. Therefore

    g(U)<=m 2^(-|A|)<=m Z_ell<=m^3 p_ell.               (2)

Importance sampling is unbiased:

    E_proposal[g(U) 1_{ell(F(U))=1}]=p_ell.

Equation (2) bounds its variance by m^3 p_ell^2. Bernstein and a union bound over 2^D linear cuts imply that

    L=O(m^3 [D+log(1/delta)]/eta^2)

independent proposals produce a simultaneous relative 1+/-eta cut summary with failure probability delta. Give sampled vector F(U_i) the positive weight g(U_i)/L, multiplied by the leaf intensity when present. No output-state or input-cube enumeration is used.

All proposal probabilities and weights are rational with polynomial bit descriptions. Large monomial degrees produce powers of two with polynomial encoded length, not an exponential number of operations. Generating and evaluating a proposal is polynomial in the explicit polynomial input size.

## Acquiring the true conditional mark outside a subspace

Let a=Pr[M F(U) is outside W] for any supplied linear context M and any subspace W. Suppose a>0. A simultaneous cut summary gives an upper estimate a_up satisfying

    a <= a_up <= c a

for a fixed constant c, on its successful preprocessing event. For example, a factor-two upper estimate follows from a sufficiently accurate outside-mass query.

On every outside input, choose a functional ell annihilating W but not M F(U). Apply (2) to ell composed with M. Its cut probability is at most a, so

    g(U)<=m^3 a<=m^3 a_up.

Generate a fresh proposal as above. Reject if its output is inside W; otherwise accept with probability

    g(U)/(m^3 a_up).

The accepted input is exactly uniform input conditioned on the outside event: proposal density times g is the original uniform density. Acceptance probability is a/(m^3 a_up)>=1/(c m^3). The output mark therefore comes from the true leaf law, not the sparse summary. Fresh proposals are independent of preprocessing. If preprocessing fails, cap/clamp behavior is included in its error budget.

The construction works uniformly for adaptive W and arbitrary linear contexts because the summary guarantee covers every linear cut. Exact coefficient-span tests identify genuinely zero outside mass.

## Compiler consequence and boundary

Replace the bounded-degree leaf sampling and rejection steps in the compressed Poisson linear-control compiler by these two operations. Its cost becomes polynomial in the explicit sparse-polynomial input size, grammar size, output dimension, probability/rate bit lengths, and inverse error. The previous 2^degree factor is unnecessary for this input class.

This does not cover arbitrary succinct Boolean circuits, shared latent inputs between occurrences, or binary-long random noncommuting control products. It is a larger supplied-noise interface within the existing deterministic linear-control compiler. The scalar sparse-polynomial counting baseline remains the established Karpinski–Luby result.

## Additional consequence: discrete sparse-polynomial slots of arbitrary degree

The same known inequality closes the high/low compiler for once-per-slot sparse polynomial marks, not only Poisson bursts.

Center each slot at F(0): write G=F+F(0), propagate F(0) as deterministic grammar drift, and let m count the nonconstant nonzero monomials of G. If m=0, the slot is deterministic. Otherwise set w_A=2^(-|A|). For a current final-frame uncertainty span W and a supplied suffix map M, define

    q(W)=Pr[M G(U) is outside W],
    Z(W)=sum_(A:M c_A outside W) w_A.

The scalar KL inequalities, averaged over annihilators of W, give

    q(W)<=Z(W)<=m^2 q(W).                              (3)

Also, a scalar polynomial with no constant term and at most m monomials is zero with probability at least 1/(m+1), by the KL even-parity corollary. If U,V are fresh independent inputs, average the identity 2p(1-p) for scalar pair differences over those annihilators to obtain

    Pr[M(G(U)+G(V)) outside W] >= 2q(W)/(m+1).         (4)

These are unconditional algebraic bounds; no rare conditional polynomial solve is assumed.

Fix tau on the order of epsilon/D. Mark a coefficient term heavy when w_A>=tau/m. Use the deterministic coefficient-span grammar search to find a residual slot occurrence with a transformed heavy coefficient outside W. By (3), q(W)>=tau/m^3; by (4), the exact pair representation increases rank with probability at least

    2tau/[m^3(m+1)].

Process that entire slot with fresh U,V using

    C <- C+M G(U),
    W <- W+span(M[G(U)+G(V)]),

and remove its occurrence by persistent grammar path copying. The law is exactly preserved. There are at most D innovations and polynomially many expected active occurrences, with a negative-binomial tail cap. Use a global upper bound on leaf monomial counts to state one uniform polynomial work bound.

When no heavy coefficient remains outside the resulting W*, every residual slot obeys Z(W*)<=tau and hence q(W*)<=tau. For analysis only, replace marks already in W* by zero. They are absorbed by the initialized Uniform(W*) throughout all subsequent additive faults. Each residual slot is now a lazy categorical law with nonzero mass at most tau, hence has an exact heatbath representation with activation at most 2tau.

The original-prefix rank-budget Poissonization lemma therefore bounds replacement of every residual slot by its compound-Poisson law by 2D tau, independent of the number of occurrences. The actual Poisson compiler may retain all original centered polynomial marks; inside-W* marks are null and need not be filtered explicitly. Its degree-independent leaf sketches and true conditional sampling are supplied above.

Consequently the compressed deterministic linear-control endpoint sampler covers independent once-per-slot explicit sparse Boolean-polynomial marks of arbitrary degree, with work polynomial in their explicit representation size and inverse endpoint error. This is still an explicit sparse-polynomial interface, not an arbitrary Boolean-circuit interface, and still deterministic linear controls rather than binary-long random noncommuting controls.
