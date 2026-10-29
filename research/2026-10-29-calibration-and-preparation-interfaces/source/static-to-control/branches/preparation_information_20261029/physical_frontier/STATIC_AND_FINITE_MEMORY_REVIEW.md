# Independent review: static bridge and fixed-sensor finite memory

29 October 2026. Reviewed exact root versions:

    STATIC_INFORMATION_TO_CONTROL.md
    aa48c7d73ccd0b82694331666946596ce8d5da2c1b2b61f19fe7710749f2284f

    FIXED_SENSOR_FINITE_MEMORY_CONTROL.md
    c6953860a7ab0579170713aa70919a4d9b78777604ab7902aac9d791cf576e7b

Both ordinary proofs are valid at their stated scopes. No empirical test
was needed or performed. The additional stronger endpoint lemma in
`QUANTITATIVE_STATIC_FORCE_BALANCE.md` is separate from this review;
the reviewed root static theorem already follows from its quadratic
all-set bound.

## 1. Static information and explicit approximation

The two-parameter reuse corollary correctly uses the bounded-gradient
candidate class. Uniform convergence of normalized candidate potentials,
plus matching complete position laws, identifies their limit potential
through the positive Gibbs density. Distributional gradient convergence
then matches the source force limit. No full path fit is needed.

The Stein residual has the correct sign and constants. In the convention
(Dphi)_ik=partial_k phi_i, its exact expression is

    <Fnu-tau grad nu,phi>=tau E[r dot (gamma phi-Dphi p)].

The displayed sum bound is valid, and the stated quadrature improvement
follows from stationary E[p dot grad |phi|^2]=0. The cutoff and moment
domains suffice; no uniform force derivative enters.

The all-set lower bound is also correct. Inverse Girsanov gives
E_P Z^(-2)<=exp[A^2t/(2gamma tau)]. Free terminal position, conditional
on any initial position and momentum, has the positive wrapped Gaussian
floor in root equation (6). Cauchy--Schwarz gives the square of the free
event probability, exactly as in root equation (8).

The smoothing-floor constant is correctly normalized for u_T of total
mass one: kernel core height (2pi)^d kappa_min delta^(-d), multiplied by
the squared normalized volume of a radius-delta/2 ball, leaves
c_mass kappa_min v_d^2/[2^(2d)(2pi)^d] times delta^d.

Convolution of the residual, division by that floor, and nonnegativity
of the smoothing kernel give the stated gradient ceiling A+epsilon_delta.
Rescaling changes the potential by oscillation <=D epsilon_delta.
Hoeffding applied to the centered potential difference gives the KL
bound, and Pinsker gives TV<=D epsilon_delta/(4tau). The smoothing
coupling then proves equation (14), including its clipped trivial bound.
The static exponent 1/(4d+4) follows by balancing the two powers.

No acquired complete configurations, entropy ceiling, independent
sampling or effective controlled error modulus is silently supplied.
The distinction between the quantitative static construction and the
qualitative dynamical transfer is correctly retained.

## 2. The common sensor reference is causally valid

The reference law R_0 must include the specified sensor draws in their
actual chronological filtration. Under that reference, sensors do not
change the physical free path, so its physical marginal is P_0.
Brownian motion remains Brownian when independent sensor randomizations
are revealed at their scheduled times.

The bounded continuous Brownian exponential is the ONLY additional
likelihood needed when the same sensor operations are used on both
sources. To verify this carefully, let L_t be its density martingale and
let t_ell be a report time. It has no jump there, and L_(t_ell) is
measurable immediately before the fresh draw: past controls use only
already available reports. For any bounded pre-draw chi,

    E_0[L_T chi (1_(A_ell=a)-K_(ell,Hprev)(a|past))]
      =E_0[L_(t_ell) chi
                         (1_(A_ell=a)-K_(ell,Hprev)(a|past))]=0.

The first step is the martingale conditional-expectation identity,
including the newly drawn report; the second is the fixed reference
sensor conditional law. Multiplication by an initial density r_j does
not change the argument. This proves that the causal report kernels
survive the feedback change of measure and establishes root equation (5).

It would be incorrect to claim that reports retain those same conditional
probabilities given the ENTIRE future physical path under feedback. The
root proof does not make that claim: it uses pre-observation histories.

The likelihood second-moment estimate is conditional on the initial
state and remains valid in this enlarged filtration. Thus root equation
(3), with only the square of the initial L2 norm, is correct. No inverse
sensor probabilities or unsupported independence of reports are used.

## 3. Limit identification retains the acquired finite memory

There are finitely many branch fields, so a common weak-* subsequence
exists. On each branch interval, the history indicator in root equation
(4) is a fixed bounded function on the joint reference space. Dropping
its absolute value can only increase the squared occupation error.
The reference physical marginal is P_0, so the already proved full-state
compact occupation lemma gives convergence in L2(R_0).

This remains valid for truncated martingale intervals and after a bounded
past multiplier. Summing finitely many nodes is legitimate; no uniform
claim is being made as the tree size diverges. The source-force term is
handled by the same compactness argument.

Fixed sensor conditional identities pass under weak L2 likelihood
convergence because their integrands are bounded measurable joint
functions. Native martingale identities plus those causal draw identities
uniquely determine the joint law: solve each bounded-force segment,
apply the prescribed sensor kernel to its actual past, and continue.
Bounded Girsanov uniqueness applies at every segment with its available
report history. This is a chronological construction and has no access
to future reports.

The common-limit contradiction therefore establishes inf_U sup_program.
Initial TV errors contract through the entire causal experiment, and the
static selection argument matches the initial Gibbs limit and force as
before. Complete finite transcript TV, fixed-record Scheffe consequences
and physical-path W_p upgrades follow at their stated scopes.

The maintained boundary is appropriate: the sensor acquisition kernels
are fixed, while branch Markov fields may vary. Finite output alphabet
alone does not supply this property for a changing exact-path test.
Retained apparatus memory, command readouts and initialization must obey
the declared interface. No hidden thermal bath for controller memory is
assumed or required by this finite-tree proof.
