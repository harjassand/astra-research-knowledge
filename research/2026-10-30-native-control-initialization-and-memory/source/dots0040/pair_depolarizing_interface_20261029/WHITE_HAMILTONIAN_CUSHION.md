# Joint depolarizing cushion from stationary classical Hamiltonian modulation

2026-10-29. Derived here; independent review pending. Exact in an ideal white-noise model, not a finite-bandwidth implementation theorem.

## Verdict

**Yes, in the ideal stochastic-Hamiltonian Markov model.** Full pair depolarization can be produced by classical white modulation of a complete basis of at-most-two-site Hermitian couplings. No syndrome-conditioned or correcting joint jump is required. This genuinely simplifies the *type* of engineered operation: it is destructive, state-blind classical random driving.

**No, this does not establish the original bounded deterministic two-site-Hamiltonian plus onsite-dissipation architecture.** It adds ideal spatially joint Markov noise, implemented through singular classical modulation and an enlarged control basis. In the reduced generator it is exactly a joint dissipative primitive. Finite-bandwidth realizations do not satisfy the exact identity, and no exponentially long memory approximation is supplied.

There is an even simpler ideal randomized alternative: synchronized local Weyl kicks at pair-local Poisson times. Thus the white-noise construction is not a uniquely powerful new operation, and the stochastic-Hamiltonian mechanism itself is established physics, not a novelty claim.

## 1. Exact normalization

Let the two physical site dimensions be d_A,d_B and D=d_A d_B. Choose Hermitian operator bases

    A_0=I_A,  Tr(A_i A_j)=d_A delta_ij,  i=0,...,d_A^2-1,
    B_0=I_B,  Tr(B_i B_j)=d_B delta_ij,  j=0,...,d_B^2-1.

The traceless generalized Gell-Mann matrices, rescaled to these Hilbert-Schmidt norms, provide such bases in every finite dimension. Put F_ij=A_i tensor B_j. Completeness gives, for arbitrary operators X on AB (and completely, with a reference),

    sum_ij F_ij X F_ij = D Tr(X) I = D^2 Delta_AB(X),
    sum_ij F_ij^2 = D^2 I.

With D[F](X)=FXF-(1/2){F^2,X}, the identity direction contributes zero and

    sum_(ij != 00) D[F_ij] = D^2(Delta_AB-id).             (1)

Take independent real Wiener processes W_ij and the Stratonovich stochastic Hamiltonian increment, with hbar=1,

    H_noise(t) dt = (sqrt(delta)/D) sum_(ij != 00) F_ij o dW_ij(t).

Equivalently, the density-operator SDE is

    d rho = L_base(rho) dt
       -i (sqrt(delta)/D) sum_(ij != 00) [F_ij,rho] dW_ij
       +(delta/D^2) sum_(ij != 00) D[F_ij](rho) dt.

The displayed equation is the Ito form; L_base can include the original deterministic Hamiltonian and onsite dissipators. Taking the mean and using (1) gives EXACTLY

    d E[rho]/dt = [L_base + delta(Delta_AB-id)] E[rho].    (2)

No commutation of L_base with the F_ij is needed, and overlapping edges add their generators if their driving noises are independent. Unknown deterministic-time-dependent local Markov perturbations may be included in L_base. Arbitrary correlations of those perturbations with the engineering noise are not covered by simply taking this mean.

The equivalent white fields xi_ij have covariance

    E[xi_ij(t) xi_kl(s)] = (delta/D^2) delta_ik delta_jl delta(t-s).

The delta in the last factor is the Dirac distribution; the first delta is the desired depolarizing rate.

## 2. Exact resource counts

Per declared pair:

- D^2-1 independent real white-noise channels.
- (d_A^2-1)(d_B^2-1) genuinely two-site Hermitian couplings.
- d_A^2+d_B^2-2 onsite Hermitian couplings.
- No identity modulation is needed.
- Each normalized basis coefficient has Wiener amplitude sqrt(delta)/D.

For two qubits: D=4, fifteen channels, nine two-body Pauli products and six single-body Pauli terms, amplitude sqrt(delta)/4. The effective dissipative rate is delta, not fifteen times delta.

The count is constant only because each physical site dimension is a fixed constant. Our hub sites can have large fixed dimensions; the control-channel count may consequently be impractical. A bounded-degree graph has O(N) such channels overall. Access to a single existing coupling with one random scalar multiplier does NOT generate full pair depolarization. A complete spanning noise covariance is required.

If one insists on strictly two-nonidentity-factor terms, the onsite terms must be supplied separately. The genuine-cross subset alone is not full depolarization: it has different decay rates on single-site and two-site operator sectors.

## 3. Exact consequence for the Markov cushion

For a Hermiticity-preserving, trace-annihilating pair perturbation N with ||N||_diamond<=epsilon, choose delta>=D^2 epsilon. The normalized Choi argument gives

    Phi=Delta_AB+N/delta  CPTP,
    N+delta(Delta_AB-id)=delta(Phi-id).

Thus (2) supplies precisely the physical depolarizing term required by the previously established Poissonization lemma, on the FULL pair Hilbert space, including controller/workspace dimensions when applicable. Its total selected rate must still fit the memory's incident-noise threshold. No unknown N is estimated or cancelled by feedback.

This is an ensemble-channel statement with the classical drive record ignored, not protection against every realization of that record. It does not cushion an inaccessible shared bath. Implementation deviations can be absorbed only if they themselves admit the declared bounded local Markov-generator description and leave sufficient rate margin.

## 4. Strong ordinary randomized alternative

Let {W_a}_{a=1}^{d_A^2} and {V_b}_{b=1}^{d_B^2} be onsite Weyl unitary error bases. The elementary twirling identity is

    (1/D^2) sum_ab Ad_(W_a tensor V_b) = Delta_AB.

At one pair-local Poisson clock of rate delta, independently choose uniform a,b and apply W_a and V_b simultaneously. The exact averaged generator is again

    delta(Delta_AB-id).

This uses one clock and D^2 equiprobable product-unitary choices per event, with entropy 2 log_2 D bits per event. It needs no entangling gate or correcting jump. Identity draws may be retained; alternatively omit the joint identity and reduce the event rate to delta(1-1/D^2).

Crucially the two onsite actions share a tick. Independent onsite Poisson randomizations generate a SUM of onsite depolarizers, not the joint replacement generator. General unknown pair perturbations cannot be assigned the same full-pair Choi cushion merely by renaming that sum.

This alternative is exact under instantaneous-kick semantics. Finite-duration gates in the presence of the continuously running memory do not automatically implement the same generator. Classical synchronization, gate accuracy, pulse exposure, and collisions on overlapping pairs must then be included in an actual physical proof. This is not a hidden assumption that those controls are noiseless or infinitely fast.

## 5. Why finite bandwidth is a real boundary

White noise is a distribution, not a bounded Hamiltonian function. Its instantaneous variance and bandwidth are unbounded; the Wiener amplitude has units sqrt(rate), not a deterministic bounded coupling strength. The averaged generator is time independent, while individual Hamiltonian trajectories are stochastic and time dependent. Statistical stationarity does not turn them into a deterministic autonomous Hamiltonian.

There is a simple exact obstruction to replacing white noise by ordinary finite-variance modulation while retaining (2): for a system initially independent of a stationary finite-variance classical field, averaging short-time unitary evolution gives a Hamiltonian first derivative; the added dissipative contribution begins at order t^2. The target depolarizer has a nonzero dissipative derivative delta(Delta-id) at t=0. Thus such modulation cannot implement the exact universal Markov semigroup from time zero. This does not rule out useful approximations after a correlation time.

A colored-noise or finite-pulse approximation may converge on each fixed finite time interval. That fact alone says nothing uniform on memory times exponential in sqrt(N). A naive global channel-error bound can grow with both N and time. One must either prove a threshold directly for that colored-noise implementation, or prove a uniform local effective-noise description strong enough for the memory theorem. No such approximation result is asserted here.

## 6. Capability and novelty accounting

The construction removes the need to posit arbitrary *correcting* pair Lindblad jumps, quantum ancilla-mediated dissipator synthesis, or syndrome-dependent noise engineering. It replaces those by complete-basis classical stochastic Hamiltonian control. That is a meaningful interface simplification if those controls are independently available.

It does NOT remove the ideal joint Markov reservoir assumption at the reduced-dynamics level. The classical field is precisely a realization of that reservoir. It does NOT prove bounded-strength finite-bandwidth hardware, deterministic Hamiltonian-plus-onsite-reset universality for this primitive, or a practical advantage over synchronized random onsite kicks.

The next hard obligation supported by this calculation is an explicit finite-bandwidth stochastic-control model with a memory-stability proof uniform in N and storage time, including its control faults. Without that, the justified endpoint remains an ideal Markov architecture with simple destructive stochastic pair operations.

## Primary-source comparison

Chenu, Beau, Cao and del Campo, *Quantum Simulation of Generic Many-Body Open System Dynamics Using Classical Noise*, PRL 118, 140403 (2017), derive many-body dissipators by stochastic modulation of Hamiltonian couplings; white fluctuations give the Markov limit and colored fluctuations retain memory. The complete-basis specialization and normalization above are derived directly here, not claimed as a new stochastic-simulation mechanism. [Primary accepted manuscript](https://link.aps.org/accepted/10.1103/PhysRevLett.118.140403).

Duer, Hein, Cirac and Briegel, *Standard forms of noisy quantum operations via depolarization*, PRA 72, 052326 (2005), already study random-local-operation reductions of noisy maps and dynamical interactions. Our addition of independent destructive random kicks is not a claim that twirling the unknown perturbation alone yields the required additive cushion. [Primary paper](https://arxiv.org/abs/quant-ph/0507134).

### Exact distinction from separate onsite noise
For clarity, separate onsite depolarizers are not merely an inefficient substitute for the full pair cushion. Let H=A tensor B with A,B nonzero traceless Hermitian onsite operators. In normalized Choi space, the generators of onsite depolarization have support inside the span of vectors for operators X tensor I and I tensor Y. The vector |H> is orthogonal to this span. The Hamiltonian generator has a nonzero off-diagonal Choi element between |I> and |H>, but zero diagonal on |H>. Hence, for any finite positive lambda, the putative channel

    id + [ -i[H,.] + onsite-depolarizer generators ]/lambda

has zero Choi diagonal in direction |H> and a nonzero cross element with |I>. Its corresponding 2-by-2 principal minor has negative determinant. It is not CP, regardless of the onsite depolarizing rates. This directly explains why a shared pair tick or genuine pair white-noise directions are needed for this particular exact Poissonization argument.

Regression: `check_pair_basis.py` checks the complete dissipator and product-Weyl identities for dimensions 2x2, 2x3 and 3x3. It verifies finite-dimensional algebra only, not a hardware approximation.
