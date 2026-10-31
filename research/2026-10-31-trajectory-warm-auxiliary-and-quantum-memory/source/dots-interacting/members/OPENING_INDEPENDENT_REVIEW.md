# Independent opening review: damped bosonic reservoirs
31 October 2026. Reviewer: independent internal mathematical review.

## 1. Source and verdict

I read the complete FIRST_CONSTRUCTION_UNREVIEWED.md in damped_bosonic_reservoir_opening_20261031, 9,115 bytes, SHA-256 3b9a31235983ca4207a73922b2df52503afe0f06169889a9038259cf034cb2a4.

Verdict: the finite-cutoff occupation/count inequalities and controlled cutoff comparison are mathematically sound. The scalar immigration-death majorant, endpoint formula, factorized positive normalizer and first-jump envelope also check algebraically. The zero-frequency OU interpretation is the correct infinite-reservoir/dilation interface, not an exact statement about a finite Fock truncation. These findings do NOT constitute whole finite-bit compiler acceptance.

The source remains an opening candidate. Thermal doubling is separate. Infinite-generator domain identification, conditioned birth-death source arithmetic, finite-bit many-mode time/order control and complete CP assembly must not be inferred from the earlier finite-source theorem.

## 2. Occupation and emission bounds at finite cutoffs

Let N=sum n_i and V=z^N. The finite lowering matrix still satisfies a_L^dagger a_L=n_L and the weighted shift identities. Its commutator with its adjoint is NOT the identity at the top level, but the proof does not need that false identity.

After V^(-1/2) conjugation the relevant single-mode term has the form
i c_z A(a-a^dagger)-b_z a^dagger a,
where c_z=sqrt(gamma lambda)(sqrt(z)-1/sqrt(z)) and b_z=4lambda(1-1/z). Since A acts on the system and commutes with a, completing the square bounds this by c_z^2 A^2/b_z <=Gamma_i(z-1)/4. This uses positivity of a shifted operator's squared norm, not oscillator CCR.

Summing modes and applying finite-dimensional Dynkin/Gronwall from vacuum gives
E z^N(t)<=exp[Gamma t(z-1)/4].
Known number rotations and H0 commute with V. System/reference CPTP controls fix V in the adjoint, so the same estimate survives prescribed instruments with their records retained.

For jump-count tilt u=e^theta, replace b_z by 4lambda(1-u/z) and choose z=2u-1. Then c_z^2/b_z=gamma(u-1). The positive tilted evolution and V>=I give
E exp(theta N_emission(T))<=exp[Gamma T(e^theta-1)].
Here occupation N and the emitted-jump count are different quantities. The bound is an unconditional exponential-moment inequality, not a pointwise intensity bound, independent Poisson emission law or normalized-postselection guarantee. Its constants are valid uniformly in the finite cutoffs.

## 3. Finite-to-finite cutoff comparison and what limit it defines

Embed the smaller local-L Fock space into any larger cutoff. Acting on a density supported in the smaller space, all damping dissipators agree: lowering cannot leave the smaller space and a^dagger a is the same number operator there. Free number Hamiltonians also agree. Only the coupling's raising boundary block differs.

If P_L is the joint smaller projection, write B=(I-P_L)H_large P_L. Different mode crossings have orthogonal ranges, because exactly one mode is raised to L+1 while every other mode is at most L. Therefore
B^dagger B=(L+1)sum_i gamma_i lambda_i A_i^2 Pi_{n_i=L}
as an operator on the smaller subspace.
Consequently Tr(B^dagger B rho_L) is at most
(L+1)sum_i gamma_i lambda_i alpha_i^2 times Pr_rhoL(N>=L).

For a positive density, ||B rho||_1<=sqrt(Tr B^dagger B rho). The commutator source norm is at most twice this quantity. Finite-dimensional Duhamel and CPTP trace-norm contraction thus give
||rho_large(T)-rho_L(T)||_1
<=2T sqrt[(L+1)sum_i gamma_i lambda_i alpha_i^2] exp(Gamma T/8) 2^(-L/2).
The moment used here is that of the SMALL cutoff process, so there is no assumption about an already-existing infinite solution. References are harmless. At system-only prescribed instruments the comparison contracts, while the unconditionally retained smaller process obeys the same occupation bound. Summing time intervals uses total T, not an extra factor p.

This proves a uniform controlled Cauchy limit from vacuum on each finite horizon. The limit is positive, trace preserving and completely positive on the system/reference inputs. With finite-rank Fock test observables, generators stabilize once the cutoff exceeds their finite support by the needed bandwidth. Passing the integral identity to the limit identifies the formal master equation on that core.

That is a precise safe construction of the vacuum-initial controlled process. It is not, by itself, a theorem of uniqueness for every possible extension of an unbounded formal generator on every infinite-energy initial state. Identification with the conventional conservative oscillator GKLS/quantum-stochastic model should be stated on its standard finite-energy domain, or the model can explicitly be defined by this controlled cutoff limit. The opening appropriately calls for a domain check rather than silently importing finite-dimensional uniqueness.

The displayed logarithmic inequality gives the stated L scaling, with a harmless log(L+1) absorbed. Thus a precision-priced cutoff is earned; enumerating the joint (L+1)^r basis is not.

## 4. Zero-frequency OU interface and its boundary

In the usual vacuum input-field dilation, for Omega_i=0,
q_i(t)=e^(-2lambda_i t)q_i(0)
       -2sqrt(lambda_i) integral_0^t e^(-2lambda_i(t-s)) dQ_i(s),
up to the sign convention for the input quadrature. Initial vacuum q_i(0) has variance one, the input quadrature is a standard commuting real Wiener field, and different mode fields commute. Hence these q_i(t) commute jointly at all times and have stationary Gaussian covariance exp(-2lambda_i|t-s|).

The system interaction A_i q_i commutes with each q_i, even when different A_i do not commute. It therefore introduces no drift/backaction in this particular autonomous quadrature equation. In the free reservoir interaction picture, the system is driven by commuting Gaussian q_i(t). Its time-ordered evolution is exactly the classical Hamiltonian-noise evolution with independent stationary unit-variance OU sources and amplitudes sqrt(gamma_i lambda_i). Interleaved system-only operations preserve the same classical source representation and retained-record statistics. This is an exact process mechanism, not a white-noise limit.

This argument belongs to the infinite oscillator/input-field model and its justified cutoff limit. At a finite cutoff [a_L,a_L^dagger] is not I; one must not assert that finite q_L already obeys exact OU dynamics or has a Gaussian vacuum spectral law.

For nonzero Omega, the free quadrature commutator is generically nonzero:
[q(t),q(s)]=-2i exp(-2lambda(t-s)) sin(Omega(t-s)), t>=s.
Thus a generic classical commuting-noise interpretation is unavailable. Particular trivial couplings may still have simpler reduced dynamics; “genuinely quantum” should not be read as a universal impossibility theorem for every choice of system operators.

## 5. Scalar virtual process and endpoint formula

Set kappa=2lambda and g=alpha sqrt(gamma lambda). The positive operator
M=-kappa n+g(a+a^dagger)
has positive coherent Perron vector h_n proportional to (g/kappa)^n/sqrt(n!) and Perron value g^2/kappa=Gamma_i/2. This can also be checked by completing the displaced-oscillator square.

The row Doob transform has upward rate g^2/kappa=Gamma_i/2 and downward rate kappa n. Its count is pathwise bounded by initial occupation plus twice the number of immigration births. At a fixed time the population is Binomial(n,e^(-kappa t)) plus independent Poisson[Gamma_i(1-e^(-kappa t))/(4lambda)]. The source's explicit endpoint expression follows.

The displayed all-initial-dead/new-immigrants term is a valid positive endpoint lower bound when gamma_i,lambda_i,t>0. Zero coupling modes need a separate deterministic/diagonal treatment rather than division by that bound. For retained windows, beta<=Gamma_i t/2; therefore the endpoint-bound logarithm has the advertised polynomial L/log-rate character. This alone is not a finite coherent inverse-CDF compiler.

Using the untruncated positive bridge while selecting zero contraction as soon as a creation word crosses L is legitimate. It implements the killed finite matrix word, without conditional resampling on boundary avoidance. One must stop work at a finite virtual cap rather than actually generate a rare arbitrarily long path.

The birth-death rate is unbounded in occupation, unlike the earlier binary chain. A full source proof must first cap total births/virtual events, giving occupation at most initial L plus that cap, before using a uniform dominating intensity in endpoint/tie and recursive-duration estimates. This is an available route but not already proved by the opening's reference to prior methods.

## 6. Positive matrix and jump envelopes

The normal-order formula in the source has the correct constants:
alpha_t=g(1-e^(-2lambda t))/(2lambda),
c_t=Gamma_i t/2-Gamma_i(1-e^(-2lambda t))/(4lambda).
For input/output occupations at most L, its lowering-then-raising intermediate occupations remain at most L. Restricted raising and lowering matrices have row/column sums at most sqrt(L), so the positive endpoint block has row and column sums at most exp(c_t+2alpha_t sqrt(L)). Tensoring and Cauchy-Schwarz give exp[Gamma t/2+sqrt(2r Gamma L t)] as written. This is a factorized endpoint preparation route, not a joint-state enumeration.

The exact untruncated identity
a exp(Mt)=e^(-2lambda t) exp(Mt)a+alpha_t exp(Mt)
is also correct. The finite truncated positive kernel is entrywise bounded by the untruncated endpoint block. Applying the truncated lowering operator only requests pre-jump rows at most L, so the identity yields the proposed envelope with a universal constant:
sqrt(lambda_i L)e^(-2lambda_i t)+sqrt(Gamma_i).
The other-mode positive row/column factor remains bounded on the small windows. Squaring/integrating yields O(L+Gamma_i tau), hence total O(rL+Gamma tau) squared normalization. The occupation is lowered physically at a jump and the reservoir must be retained.

These local bounds support a polynomial-normalizer candidate. They do not close arbitrary endpoint bridge arithmetic, coherent preparation, zero-coupling cancellation, timestamp control, OAA perturbations or the global CP/private-clock ledger. Known Omega number phases are explicit diagonal operations, but virtual-time errors must include their occupation-weighted frequency sensitivity; a statement of logarithmic precision dependence alone is not the full error proof.

## 7. Strong primary comparators

The basic Gaussian pseudomode correspondence is established, not a new claim of this opening. Tamascelli et al. prove equivalence of reduced dynamics for Gaussian environments with matching free one- and two-time interaction correlations. [Nonperturbative Treatment of non-Markovian Dynamics of Open Quantum Systems, PRL120,030402](https://arxiv.org/html/1709.03509).

The controlled/multitime comparator is stronger than one-time matching: Smirne et al. explicitly include multitime expectations of completely positive trace-nonincreasing maps and sequential measurement statistics. I inspected the theorem and its operator/map formulation. Extending that formalism with retained references and instrument branch labels is the natural ordinary route, not an unprecedented process-level observation. [Non-perturbative treatment of open-system multi-time expectation values in Gaussian bosonic environments](https://arxiv.org/html/2209.00293).

Polylogarithmic inverse-error bosonic cutoff results already exist for Hamiltonian models, together with rigorous truncated dynamics. The present dissipative, rate-balanced moment estimate must be compared on its specific constants and interface, not advertised as the first precision-efficient bosonic truncation. [Tong et al., Quantum6,816(2022)](https://quantum-journal.org/papers/q-2022-09-22-816/).

A recent direct quantum-algorithm comparator is the ancilla-train construction for Gaussian environments. Its primary paper describes controlled truncation and arbitrary accuracy, with resource costs polynomial in inverse target accuracy. It is broader in bath shape but does not, from the inspected statements, provide this proposed logarithmic-accuracy/stiff-rate compiler. [Ancilla-train quantum algorithm for simulating non-Markovian open quantum systems](https://journals.aps.org/pra/abstract/10.1103/dc52-844x).

Coupled Lindblad pseudomode theory separately addresses economical bath representation, including polylogarithmic mode-count evidence under its hypotheses. Bath fitting/compression and fast simulation of the resulting stiff dynamics are distinct costs. Its coupled modes should not be silently equated with this opening's independently damped factorized modes. [Coupled Lindblad pseudomode theory](https://arxiv.org/html/2506.10308).

For the classical zero-frequency specialization, OU coarse-grid/bridge averaging is already an ordinary practical alternative. It must be credited without claiming it supplies the currently unproved high-precision quantum compiler. [Albash, Young and Jacobson, Temporal Coarse Graining for Classical Stochastic Noise in Quantum Systems](https://arxiv.org/html/2502.12296).

Thermal-to-vacuum environment mappings are also established. The proposed two-vacuum-mode thermal receiving interface still needs its own exact dynamical proof, including the chosen damping and opposite frequencies; it is not accepted here. [Tamascelli et al., Efficient Simulation of Finite-Temperature Open Quantum Systems](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.123.090402).

These comparisons are source-grounded scope checks, not an exhaustive originality search. Existing denied full-text restrictions were respected.

## 8. Final boundary

Accepted locally: finite-cutoff number/emission bounds; controlled finite-to-finite cutoff error and resulting vacuum Cauchy-limit construction; the stated scalar/positive-kernel/envelope algebra. The zero-frequency classical OU mechanism is sound on the ordinary infinite oscillator dilation, with the domain/limit distinction above.

Not accepted by implication: an arbitrary-domain unbounded-generator uniqueness theorem, a complete many-mode finite-bit compiler, thermal doubling, fitting a general physical bath for free, a public trajectory simulator, hardware noise suppression, practical advantage or novelty. The next useful work is the birth-death/coherent first-event and private-clock receiving proof, not another appeal to small activity alone.
