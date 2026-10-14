# CRAY — Equilibrium-free validation of a many-body comparison

Research record: 13 October 2026.

## Status

This continuation replaces Gibbs-state acquisition by a short coherent comparison experiment, local resets and a conditional-probability certificate. The environment may remain interacting, unequilibrated and history-dependent throughout. The result validates an operator comparison and hence bounds the full-system free-energy difference at every positive inverse temperature, as well as the ground-energy difference. It does not estimate a Gibbs observable from a non-Gibbs state.

The operation has substantive restrictions: coherently selectable Hamiltonian branches, a controllable finite collar covering the comparison residual, coarse local interaction bounds, calibrated reset/control/readout error, and a useful local comparison unitary. It is not a generic way to infer thermal free energies from short trajectories. The local comparison may fail even with exact Hamiltonian information.

The proofs below are self-contained except for the explicitly cited matrix-martingale concentration theorem used by the optional phase-readout implementation. They have not been independently refereed or formally verified. The exact-arithmetic scripts verify declared special cases, not the general proofs. Historical novelty is unestablished. Spectral pairing, polar decomposition, Ramsey/Loschmidt interference, local Hamiltonian learning, inverse measurement frames and martingale concentration are existing ingredients.

No laboratory data or independently specified hard material benchmark was obtained. All acquisition records here are simulated. A constructed positive family passes the mathematical test; all 40 independently modified diagnostic controls fail the proposed local search. An exact conditional certificate from one synthetic 100-million-trial count record needs an exceptionally small apparatus-error allowance. A separate simulation that actually propagates the same unreset quantum memory produces an inconclusive interval after 100 million trials even with ideal apparatus. This is a mathematically established acquisition bypass under an explicit access contract, not a demonstrated transformative materials capability.

## 1. Scientific task and physical access

The selected target is the stability of two held charge configurations near an interacting spin/quantum-dot register. The question is which configuration has lower constrained Helmholtz free energy after the register is allowed, in the definition of free energy, to equilibrate. The actual acquisition does not equilibrate it.

Use a dual-rail label: one fixed electron occupies one of two locations. Both label values have the same total charge. During an interrogation, the barrier holds the configurations and the model Hamiltonian is

    H_total = |0><0| tensor K0 + |1><1| tensor K1.

K0 and K1 act on the same host Hilbert space, including every host degree of freedom in the model. The output is

    DeltaF_beta = F_beta(K1)-F_beta(K0),
    F_beta(K) = -log Tr exp(-beta K)/beta.

Scalar electrostatic or other reference costs belong in K0,K1. A relative scalar energy is visible through the label's Ramsey phase; separate uncontrolled evolutions of the two hosts would not reveal it.

This is a constrained-sector comparison, not the free energy of an unconstrained tunnelling label and not an electron-addition reaction with an unspecified reservoir. Nonzero tunnelling during the hold, leakage, and any correction from constrained to unconstrained thermodynamics must be separately bounded.

For an encoded spin register with fixed charge on each physical site, local spin rotations/resets preserve total particle number. They need not preserve magnetization. We therefore trace over the full spin register at that fixed charge, not a simultaneously fixed magnetization sector. In a different encoding, the allowed reset and comparison gates must preserve the specified sector. A canonical fermion-number sector does not automatically factor as a collar tensor an outside system; the factorization used below must genuinely hold for the encoded degrees of freedom.

Semiconductor charge-qubit coherent control has been demonstrated [1], and a programmable germanium quantum-dot spin ladder combines digital spin preparation/readout with analog interacting evolution [2]. These are evidence for constituent operations, not a demonstration of the whole contract or its required precision. The electronic-to-spin effective-model discrepancy in a real device is not automatically zero. No device-specific bound on it is supplied here.

The proposed experiment requires reset and control of a small collar, not all host spins. In each trial the collar can be replaced by a known state while leaving the outside in its current, unknown state. A physical realization could use controlled measurement/reset or swaps with reset local ancillas. The time and error of those operations are charged. Calling them local does not make them instantaneous or perfect.

## 2. Why ordinary acquisition has no universal repair

Consider two binary variables n,z and the finite-range, interacting Hamiltonian

    H_b(n,z) = n(1-2z)+b z,
    V(n) = 1/2-n,
    beta = 2.

For b=-4, the free-energy change is approximately -0.44559429265; for b=+4 it is approximately +0.21348708968. `exact_certificate.py` proves their opposite signs using rational bounds on exp(1), without a floating-point energy calculation.

Start in the unobserved sector z=0. If every available intervention and measurement commutes with z, all accessible records are identical for the two models: their restrictions to z=0 are the same. Repeatedly manipulating n or checking its stationary statistics cannot identify the unvisited sector's partition weight.

Now add epsilon X_z. Relative to the zero-tunnelling model, a Duhamel bound limits the change of the quantum channel over total interrogation time T by order epsilon T/hbar. More precisely, the trace distance of the final accessible outputs of the two models is at most 2 epsilon T/hbar: compare each to its zero-tunnelling counterpart and use contractivity through every adaptive instrument. Thus equal-prior discrimination success is at most

    1/2 + epsilon T/hbar.

Achieving error alpha<1/2 requires

    T >= (1/2-alpha) hbar/epsilon.

Both variables can be encoded in fixed-one-particle dual rails. This obstruction does not rely on particle exchange, Gaussianity or a large example. It can be embedded next to any common interacting environment.

The point is not that all thermodynamic acquisition is slow. It is that a uniform guarantee cannot be deduced from local stationarity or a finite observed relaxation record when hidden-sector access is unconstrained. The positive operation below changes the access, rather than declaring that obstacle solved.

## 3. Comparison witnesses covering every state

### 3.1 Polar-intertwiner lemma

Let A be invertible on the host space, w real, and

    Q = K1 A - A K0 - w A,
    s = sigma_min(A)>0.

Write the polar decomposition A=UP, P>0. Then

    ||U^dagger K1 U-K0-wI|| <= ||Q||/s.                 (3.1)

**Proof.** Put B=U^dagger K1 U-wI, R=B-K0, Q'=U^dagger Q. We have

    Q'=BP-PK0,
    Q'+Q'^dagger=RP+PR.

The Sylvester equation has the integral solution

    R = integral_0^infinity exp(-tP)(Q'+Q'^dagger)exp(-tP) dt.

Its norm is at most 2||Q|| integral_0^infinity exp(-2st)dt=||Q||/s.

By the eigenvalue min-max principle, every ordered eigenvalue difference is in [w-r,w+r], r=||Q||/s. Summing the corresponding Boltzmann factors proves

    DeltaF_beta in [w-r,w+r]                           (3.2)

for every beta>0. The same interval contains the ground-energy difference.

The invertibility condition is essential. Take K0=diag(0,0.4), K1=diag(0.3,-2), A=diag(1,0), w=0.3. Q=0 but an unpaired state reverses the free-energy conclusion. A narrow observed spectral transition is not a full-spectrum comparison certificate.

### 3.2 Locality and constructing a candidate

If A is supported on a collar and all terms not touching it are common to the two systems, only the collar and its interaction shell enter Q. A purely local SVD search can propose A: expand it in a complete collar operator basis, minimize the Hilbert-Schmidt residual of the displayed linear equation, and inspect its smallest singular value. Take the polar unitary of a successful proposal.

This search is constructive, but not complete. It can return a singular or badly conditioned map, or a useless residual. Its local dimension grows exponentially with collar size. The numerical implementation uses exact model matrices to test this search; it does not claim they were obtained experimentally.

For physical use, a proposed U can come from coarse local calibration, a physical symmetry, or a fixed short gate circuit. A completely constructive alternative is to enumerate a finite, explicitly compiled gate catalogue and a scalar-frequency grid, validating each with confidence allowance alpha/M for M candidates. This requires no supplied optimal map and no reconstructed Hamiltonian, but can multiply acquisition cost by M and does not guarantee that any candidate succeeds. Coarse screening can reduce actual work, but no such reduction is assumed in the resource guarantee. The final acquisition test below validates that U directly. It does not assume the proposal is correct or optimal. Adaptive proposals must be frozen before the validation record or paid for by a simultaneous testing budget. The search and gate-synthesis costs are not eliminated.

Full-spectrum pairing is established research, including strong-zero-mode constructions [3]. Equation (3.1) and its use here are candidate comparison tools, not a claim to have invented spectral pairing.

## 4. A finite-time experiment with a relative, not absolute, error

Fix a local unitary U and a scalar w. Define

    A0 = K0,
    B = U^dagger K1 U-wI,
    R = B-A0.

Assume R is supported on a known collar S of dimension d. The outside can be arbitrarily large and interacting. Supply only coarse bounds

    ||R|| <= Rcap,
    J_S >= sum of norms of K0 terms touching S,
    Lambda = 2 J_S + Rcap.

They imply ||[K0,R]||<=2J_S||R||. These are not assumed small. A spectroscopy linewidth does not by itself establish either bound. Unknown interaction tails and extra label-dependent terms cannot be silently discarded.

Use units hbar=1 until Section 9. The echo is

    E(t)=exp(iK0 t) exp(-iBt).

Then

    ||E(t)-I+itR|| <= (Lambda t^2/2)||R||.             (4.1)

**Proof.** E'=-i exp(iK0t)R exp(-iBt). Differentiating again gives

    E''=exp(iK0t)([K0,R]-R^2)exp(-iBt).

Its norm is at most Lambda||R||. Integrating the Taylor remainder proves (4.1). The extensive norm of the common host Hamiltonian is absent.

The crucial feature is the factor ||R|| in the remainder. A generic short-time derivative estimate has an absolute truncation error and forces shorter times as the target accuracy increases. Here a fixed interrogation time proportional to 1/Lambda suffices for a relative comparison test.

### Physical sequence, without reversing the environment

Prepare the label in |+>. Apply controlled U to S on branch 1. Evolve under the actual branch Hamiltonian for time t. Apply controlled U^dagger on branch 1 and the calibrated relative phase exp(iwt). Read out the label in X or Y.

The branch evolutions are exp(-iK0t) and exp(-iBt), respectively. The label interference therefore measures the real or imaginary part of Tr(rho E(t)). No inverse evolution of the many-body host is physically implemented. The e^{iK0t} factor arises from interference between two forward branches.

This sequence is stronger access than passive charge sensing: the two alternatives must be coherently selectable on the same specimen, and the controlled collar gates must be available. It is not applicable to arbitrary independently fabricated molecules.

## 5. Main acquisition theorem: local resets, arbitrary outside memory

Before each trial, replace S by I_S/d. This makes the state

    rho_tau = I_S/d tensor tau,

where tau is arbitrary. It may depend on every earlier record and need not be stationary, Gibbs, weakly correlated, or known. The replacement discards old collar-outside correlations but does not reset or solve the outside. Use an ideal label |+>, the sequence above, and the X-basis failure outcome |->.

The failure probability is

    p_tau(t) = [1-Re Tr(rho_tau E(t))]/2
             = ||(E(t)-I)rho_tau^(1/2)||_2^2/4.

Locality gives

    ||R rho_tau^(1/2)||_2
        = sqrt[Tr_S(R^2)/d] >= ||R||/sqrt(d).

Using (4.1) and the reverse triangle inequality,

    p_tau(t) >= c(t)||R||^2,

    c(t) = t^2/4 [1/sqrt(d)-Lambda t/2]^2,             (5.1)

provided 0<t<2/(Lambda sqrt(d)). This is uniform over tau.

At t*=1/(Lambda sqrt(d)),

    p_tau(t*) >= ||R||^2/(16 Lambda^2 d^2).            (5.2)

This implication covers states never visited by the specimen: the local maximally mixed replacement has full support, and the unknown residual is an operator on that collar. Without the locality/full-support condition, small echo loss is only state-dependent evidence and does not imply a thermodynamic bound.

### Correlated observations: no independent-specimen assumption

Let Y_j be the observed failure bit. Suppose the combined apparatus error changes its conditional probability by at most gamma, for every allowed history and outside state. Then

    Pr(Y_j=1 | past) >= q_* := max(0,c(t)||R||^2-gamma).

A Bernoulli process with each conditional probability at least q is stochastically no smaller than Binomial(n,q). One proof uses independent uniform random variables to realize each conditional Bernoulli law, comparing pointwise to Bernoulli(q). Thus, for a fixed predeclared number n of trials and s failures, let q_up(s;n,alpha) be the usual lower-binomial-tail inversion. With probability at least 1-alpha,

    ||R|| <= sqrt[(q_up+gamma)/c(t)].                  (5.3)

This is binomial domination, not a claim that the data are iid or that q_up estimates one stationary bath-dependent probability. A simple alternative avoids numerical binomial inversion: with L=log(1/alpha), the lower-tail Chernoff inequality makes q_bar=min(1,[s+L+sqrt(L^2+2sL)]/n) a valid, somewhat looser upper bound. It uses only arithmetic, a logarithm and a square root on O(log n)-bit count inputs and admits outward-rounded polynomial-bit evaluation at a specified precision. At t=t*,

    radius = 4 Lambda d sqrt(q_up+gamma).             (5.4)

Intersect with Rcap. Insert the radius into (3.2) for a thermodynamic decision valid at every beta and for ground energies. No temperature measurement is needed to establish this particular all-temperature interval.

For s=0, q_up=1-alpha^(1/n)<=log(1/alpha)/n. Ideal best-case sample cost to certify radius epsilon is therefore

    n = O(Lambda^2 d^2 epsilon^(-2) log(1/alpha)).      (5.5)

The bound has no bath equilibration or correlation-time factor. It has local dimension, physical energy scale, and precision factors. It guarantees an interval, not successful sign determination on arbitrary systems.

The best possible floor from the additive apparatus allowance alone is

    epsilon_floor = 4 Lambda d sqrt(gamma).           (5.6)

Actual nonzero background failures can make the floor worse. Average gate fidelity is not the conditional, state-uniform probability-error bound required here.

## 6. Alternative acquisition: a finite-time phase matrix

The null test is simple but can be dominated by the square-root calibration floor. A second operation uses randomized local preparations and the echo's phase rather than rare failures.

For any outside state tau define the completely positive unital conditional expectation

    Phi_tau(O) = Tr_out[(I tensor tau)O],
    M_tau = -Im Phi_tau(E(t))/t.

Equation (4.1) implies

    ||M_tau-R|| <= a||R||,  a=Lambda t/2.             (6.1)

This holds for any tau. Choose a<1, without making t depend on the desired precision.

For ell qubits in S, d=2^ell. Independently on each qubit, choose uniformly one of the six Pauli eigenstates rho_i. Let

    sigma = tensor_i rho_i,
    D_sigma = tensor_i(3rho_i-I).

Choose the sign of the label Y readout y in {+1,-1} so its expectation is t Tr(sigma M_tau). The estimator

    Z = (d/t) D_sigma y

satisfies E[Z | past]=M_tau. The product-frame identity follows from the single-qubit identity

    E_rho[(3rho-I) Tr(rho M)]=M/2.

Fresh local randomization is independent of the outside before each reset/interrogation. Arbitrary memory between trials is allowed. Batching all settings against different uncontrolled outside states would not have this guarantee.

The estimator obeys

    ||Z|| <= d^2/t,
    E[Z^2 | past] = 10^ell/t^2 I.

The centered increments have norm at most B_m=2d^2/t and conditional variance at most v=10^ell/t^2. Matrix Freedman's inequality [4] gives, with probability at least 1-alpha,

    ||M_hat - average_j E[Z_j | past]|| <= e

provided

    n >= [2v+(2/3)B_m e] e^(-2) log(2d/alpha).        (6.2)

The average conditional mean remains within a||R|| of R despite outside drift. If a separately justified bound b_cal controls the operator bias from apparatus errors, then

    ||R|| <= [||M_hat||+e+b_cal]/(1-a).               (6.3)

This uses O(d^2) matrix memory and O(10^ell Lambda^2/e^2) leading sample cost at fixed relative time, apart from confidence and constant factors. It avoids the epsilon^(-3) cost of the elementary derivative scheme tested below. It is not claimed optimal: substantially stronger Hamiltonian-learning algorithms already exist [5,6].

Calibration is not free. A per-setting bound b on the signed Y expectation gives only the conservative operator-bias bound d^2 b/t through the inverse frame. Claiming b/t instead requires a stronger input-independent channel-error contract. Timing and coherent pulse errors must be included. This variant removes one avoidable precision penalty but does not establish adequate hardware calibration for a real correlated device.

## 7. Constructed and negative controls

### 7.1 Exact local algebra with an arbitrarily large interacting extension

Use three collar spins and

    K0 = .70 Z0 + .43 X1 + .31 Z1
       + .83 X0X1 + .61 Y0Y1 + .97 Z0Z1
       + .79 X1X2 + .57 Y1Y2 + .88 Z1Z2.

Let

    U=(I+iZ0X1)/sqrt(2),
    K1=U K0 U^dagger + (1/5)I + (3/100)Z0Z2.

U acts only on spins 0,1. Any common interacting extension attached to spin 2 or farther away cancels from the comparison. The exact residual is (3/100)Z0Z2 and its square is (9/10000)I. Rational/symbolic verification proves

    DeltaF_beta in [17/100,23/100]

for every beta>0 and the ground-energy difference, independent of the extension size. This does not solve the host. One can specify an 80-spin interacting extension without ever constructing its 2^80 matrix, but no 80-spin ground state or free energy was calculated.

The unrotated difference has numerical eigenvalue range approximately [-3.34419,3.79042], so the proposed local map matters to this comparison. Small three-spin diagonalization gives free-energy differences 0.2009031, 0.2091526, 0.2109714 and 0.2109720 at beta=0.2,1,3,10.

This family was constructed to admit a useful local comparison. It is an algebraic control, not an independently specified material benchmark. Its local matrices are known to the simulation; when evaluating acquisition, the estimator is supplied only the designated coarse bounds and its observed counts, not the exact residual.

### 7.2 Synthetic counts and a separate retained-memory quantum trajectory

A fourth spin has common terms

    1.1 Z2Z3 + .6 X2X3 + .5 X3.

Only the first two terms touch the reset collar. The certified coarse parameters are

    J_S=7.79, Rcap=2, Lambda=17.58, d=8, t=1/50.

Rcap=2 does NOT decide the sign of w=0.2. It is deliberately larger than the desired comparison margin and is not a supplied small residual.

One seeded conditional-probability simulation generates n=100,000,000 trial outcomes in blocks, choosing an outside-state parameter from the history of earlier counts. It yields 3 failures (its conditional expectation for the total is about 9). It is not a time-resolved simulation of an autonomous unreset quantum state, and the single seeded record is not a performance average or a coverage study. Conditional failure probabilities for the two selected memory states happen to be very close in this fixture; arbitrary-history validity comes from the proof, not from this generator.

The float-computed 99% intervals are:

| Apparatus probability allowance gamma | DeltaF interval |
|---:|---:|
| 0 | [0.021697, 0.378303] |
| 1e-8 | [0.013032, 0.386968] |
| 1e-7 | [-0.051876, 0.451876] |
| 1e-6 | [-0.390157, 0.790157] |

The exact verifier avoids numerical beta quantiles. It proves that q_up may safely be replaced by 101/10^9 because the binomial lower tail at s=3 is less than 0.01. It uses 35355/100000 as a rational lower bound on 1/sqrt(8), the rational time 1/50, and gamma=1/10^8. Exact arithmetic gives

    ||R|| < 47/250,
    DeltaF in [3/250,97/250] = [0.012,0.388].

The confidence statement is conditional on the stated physical contract. It does not verify that a device has gamma<=1e-8. This calibration requirement is a negative feasibility finding, not an omitted nuisance.

A stricter, separate calculation in `retained_memory_test.py` propagates the outside spin density matrix through the actual quantum measurement instrument, resetting only the collar and label. Its completely positive pass/fail maps are derived from the two branch unitaries. Long no-click runs are sampled with powers of the pass superoperator; no iid frame assumption or outside re-preparation is used. Starting from a pure +Y memory state, its fixed seeded 100-million-trial trajectory has 7 failures. The numerical 99% interval is [-0.025031,0.425031] even at gamma=0, so it does NOT certify the sign. At gamma=1e-8 it is [-0.031956,0.431956]. These are numerical quantum-trajectory diagnostics, not a laboratory experiment or rigorous floating-point interval calculation. This failed acquisition is more informative about robustness than the favorable three-failure conditional record. The latter must not be promoted as a reliable demonstrated runtime.

### 7.3 Phase acquisition and derivative comparison

A separate one-reset-spin, one-memory-spin phase test uses two million simulated, history-dependent shots. The true residual norm is 0.1769181. Its estimated phase-matrix norm is 0.1816634; the 99% matrix-martingale radius is 0.1549690. The resulting certified norm bound is 0.3852731, before physical calibration error. This demonstrates the valid data flow, not a precise material decision.

A prior straightforward local derivative prototype was also executed. One million simulated randomized-time records give a valid but broad interval for a coefficient -0.6. Its elementary bias/noise budget scales as epsilon^(-3); even the epsilon=0.1 accounting for 32 coefficients requires approximately 9.35e8 total trials. A deliberately invalid batched-time version estimates approximately -0.277 because the unobserved memory state changed between settings. The fixed-time echo/phase operation replaces that derivative pipeline rather than promoting its excessive acquisition cost.

### 7.4 Scope controls

The polar lemma passed 200 random complex matrix tests and 800 free-energy checks. The echo bound and phase relative bound passed 600 outside-state checks across 120 random models, including nonweak system-memory interactions. Exhaustive small product-frame checks verified the unbiasedness and second-moment identities numerically.

For 40 separate three-spin field/exchange modifications not generated by a conjugation, the same two-spin SVD search certified zero signs. The median interval width was approximately 1.98265. This is not a proof that no better witness exists, but it is direct evidence against treating a compact useful map as generic. No successful cases were selected from that group.

## 8. Obtaining the remaining inputs, without an oracle

A candidate circuit U is local and explicitly compiled. Its existence is not guaranteed. Pilot experiments or a calibrated local model may suggest it; the final test remains independent of that suggestion. An unsuccessful search must return no decision, not enlarge the collar without charging exponential resources.

The support promise says all noncommon interactions and all terms altered by U are contained in S. Finite-range geometry provides a constructive interaction shell when the model genuinely has finite range. For long-range electrostatics, omitted tails must have a certified summable norm bound after the correct scalar reference is chosen. Calling a screened interaction short-range is not a proof. A known upper bound on terms touching S suffices for J_S; distant internal host interactions need not be learned.

These are physically calibrated structural inputs. Finite-bandwidth observations alone cannot exclude arbitrarily strong unseen terms. No claim is made that the required support, bandwidth, coarse norms or state-uniform gate-error bounds can be recovered for an arbitrary unknown material with bounded samples.

If target/reference microscopic errors have total norm at most zeta_0,zeta_1, expand the final free-energy interval by zeta_0+zeta_1 on each side. For dynamics, a model error of norm zeta over time t changes a channel by at most 2t zeta in diamond norm (hbar=1), so the probability budget must also cover the corresponding measurement change. Common interacting host terms are retained, not estimated then subtracted. Common unknown terms touching S still affect J_S and cannot be ignored.

If reset, gates, timing and readout have appropriately state-uniform bounds, a telescoping channel bound supplies a valid gamma or phase-bias budget. Average process fidelity alone is insufficient. Coupling to a bath during a finite reset can correlate the freshly prepared state with the outside; this must be covered by the same contract. A nominally fast pulse does not establish a negligible error.

## 9. Complete resource and decision accounting

In physical units, the optimal null interrogation time is

    t_phys = hbar/(Lambda sqrt(d)).

The required local operation may be too fast for a particular platform; it is not available merely because a formula specifies it. The total acquisition duration is at least

    n [t_local_reset + 2 t_controlled_U + t_phys + t_label_readout]
      + pilot search + calibration.

No equilibration time or empirical bath autocorrelation correction is inserted because the uniform conditional-probability proof does not use either. The outside is the same ongoing specimen. Fresh randomness, local reset and a calibrated label are still physical resources.

For zero failures, alpha=.01 and an ideal apparatus, sufficient shot counts conditional on a zero-failure record, and necessary calibration ceilings, are:

| Reset spins | epsilon/Lambda | trials sufficient for zero-failure radius | necessary gamma ceiling for apparatus-only floor below epsilon |
|---:|---:|---:|---:|
| 1 | 0.1 | 29,474 | 1.5625e-4 |
| 2 | 0.1 | 117,893 | 3.90625e-5 |
| 3 | 0.1 | 471,570 | 9.765625e-6 |
| 3 | 0.01 | 47,156,943 | 9.765625e-8 |

Use `echo_results.json` for exact computed integer roundings; the displayed table rounds as indicated. Nonzero actual echo loss can make the desired radius unattainable even with infinitely many samples. Error-floor inequalities are necessary for success, not experimental achievements.

The null validator stores O(1) counts and an explicit local circuit, not a bath state. The phase variant stores a d by d matrix. Candidate local algebra and gate synthesis grow exponentially with collar size in the unrestricted case. Confidence inversion and arithmetic precision are inexpensive compared with trials in the supplied fixtures, but a general implementation must outward-round time, norms and statistical endpoints. The exact verifier uses only local symbolic matrices and rational arithmetic; its runtime is not a generic optimal sample-complexity proof.

The output is a numerical interval plus its finite certificate. It becomes a design decision only after reference, calibration and physical-model uncertainties have been included and the interval excludes the design threshold. There is no guarantee of reaching that outcome on every input.

## 10. Strong baselines and prior-art audit

Direct thermodynamics is a serious baseline. The July 29, 2026 Kondo-entropy experiment uses temperature-dependent charge sensing and a Maxwell relation, compared with numerical renormalization group [7]. It establishes useful equilibrium thermodynamics in an actual strongly coupled device; the present work does not supersede it. For an accessible equilibrated device, that direct route can be preferable to the demanding coherent control here.

Hamiltonian learning is also an established acquisition alternative. Quantum bootstrapping already used small quantum resources to learn larger devices [5]. A 2026 paper develops Heisenberg-limited learning without short-time control [6]. Thus short-time response, local calibration, or avoiding a thermal input is not by itself new. Our sample scaling is not asserted to beat their strongest access models. The proposed distinction is direct validation of a thermodynamic comparison under an arbitrary retained outside state, with no environment mixing condition.

Subsystem Loschmidt echoes have been measured in interacting quantum-gas experiments, including ergodicity breaking [8]. Ramsey/echo measurements are not an invented physical primitive here. The candidate contribution is the local full-support-to-operator-norm implication, relative finite-time remainder, history-valid confidence propagation, and its use in a sector-wide energy/free-energy comparison. Historical priority of that combination has not been established.

October 1, 2026 polynomial equilibrium results for constant-size quantum impurities in noninteracting fermion baths [9,10] remain essential computational baselines. This work retains an interacting host, but pays for physical branch control and a restricted successful comparison. It is not a new polynomial classical solver for arbitrary interacting baths.

Correlated-sampling AFQMC [11] already targets differences; FEMION [12] already addresses real metal-surface adsorption with local AFQMC and nonlocal screening. The present held-charge task has neither their first-principles chemical scope nor a matched-task performance demonstration. No runtime advantage over the strongest many-body solver or experimental thermodynamics was measured.

## 11. Result and remaining limitation

The positive theorem removes the requirement to prepare or certify equilibrium for comparisons admitting the specified local coherent witness. It provides an explicit alternative acquisition procedure, not an assumed Gibbs interface. Hidden environmental states are covered by operator validation rather than hoped-for sampling.

There are two decisive limits. First, useful local near-intertwining is stronger than one free-energy ordering and is not generic; the negative controls expose this. Second, the acquired operator guarantee can require a control-error budget much smaller than ordinary reported gate infidelity. The null-test control is not yet a practical materials result merely because its statistical computation is finite.

The completed output is therefore a substantive equilibrium-free comparison-validation mechanism, full resource/error accounting and exact conditional certificates. A consequential real correlated-device decision, verified physical calibration, a hard independent benchmark and a matched-method advantage remain unestablished. The previous histogram theorem is preserved, but generic acquisition by waiting longer or postulating independence is not advanced as a solution.

## References

[1] D. Kim et al., Microwave-driven coherent operations of a semiconductor quantum dot charge qubit. arXiv:1407.7607; Nature Nanotechnology 10, 243–247 (2015). https://arxiv.org/abs/1407.7607

[2] P. Cova Fariña et al., Site-resolved magnon and triplon dynamics on a programmable quantum dot spin ladder. Submitted 10 June 2025. https://arxiv.org/abs/2506.08663

[3] P. Fendley, Strong zero modes and eigenstate phase transitions in the XYZ/interacting Majorana chain. https://arxiv.org/abs/1512.03441

[4] J. A. Tropp, Freedman's inequality for matrix martingales. Electronic Communications in Probability 16 (2011), 262–270. https://arxiv.org/abs/1101.3039

[5] N. Wiebe, C. Granade, D. G. Cory, Quantum Bootstrapping via Compressed Quantum Hamiltonian Learning. https://arxiv.org/abs/1409.1524

[6] M. Shin, J. Lee, C. Oh, Heisenberg-limited Hamiltonian learning without short-time control. Submitted 30 April 2026. https://arxiv.org/abs/2604.27838

[7] J. Drayne et al., Entropic signatures of the single-impurity Kondo state. Submitted 29 July 2026. https://arxiv.org/abs/2607.27502

[8] S. Karch et al., Probing quantum many-body dynamics using subsystem Loschmidt echoes. https://arxiv.org/abs/2501.16995

[9] S. Arunachalam et al., Quantum impurity models: easy at equilibrium, universal in motion. Submitted 1 October 2026. https://arxiv.org/abs/2610.02130

[10] J. Jiang et al., Polynomial-time classical and quantum simulation of quantum impurity models. Submitted 1 October 2026, revised 5 October 2026. https://arxiv.org/abs/2610.02167

[11] J. Shee et al., Chemical Transformations Approaching Chemical Accuracy via Correlated Sampling in Auxiliary-Field Quantum Monte Carlo. https://arxiv.org/abs/1703.01545

[12] C. Cao et al., Quantum Many-Body Simulations of Catalytic Metal Surfaces. https://arxiv.org/abs/2508.13036

Research capital: prior CRAY local-histogram note read in full. Read-only GitHub searches for intertwiners and polar/Sylvester material in https://github.com/harjassand/astra-research-knowledge and https://github.com/openai/math returned no matching excerpts. No repository theorem is imported as an unverified premise; no repository was changed. These searches were selective, not an exhaustive priority audit.
