# From chosen-state classical samples to an exactly reusable affine source law

31 October 2026. Conditional receiving theorem and elementary identification construction. This is a restricted active-learning model with an explicit structural promise, not an unrestricted source learner, a new system-identification principle, or an implemented downstream quantum simulator. Independent review is pending.

## 1. Promised data access and desired output

The unknown transition kernel on fully observed n-bit states, n>=1, is promised to have the form

    Y = F x + beta + eta,       eta uniform on U subset GF(2)^n,

where U is one unknown fixed linear subspace, F is an unknown binary linear map, and beta is an unknown offset. Noise draws are fresh, independent and identically distributed at every call, conditional on the chosen input and entire past. The learner can choose and reset to any input x and observe the complete next state Y exactly. The state coordinates and their interpretation are known. No coherent oracle, F, generator matrix for U, stationary state or mixing horizon is supplied.

This excludes passive trajectory-only access, latent coordinates, noisy state readout, restricted reset sets, drifting or correlated noise, nonuniform noise on U, and unpromised nonlinear dynamics. The structural promise is an assumption, not something a finite transcript certifies.

The output is a finite classical description of the entire transition law, not necessarily the original F, beta or random coins. If its exact controllability test passes, feed that description to the separately reviewed affine realization synthesizer, which acquires a coherent pure-return source and the existing compiler inputs. Future system couplings and their real acquisition/execution costs remain separate.

## 2. Fixed-sample learner, including unknown rank

Fix 0<delta<1 and set

    M = n + ceil(log2(2/delta)).

1. Query x=0 once, receiving Y0, then M further independent times, receiving Y1,...,YM.
2. Let Uhat be the binary span of Dj=Yj+Y0, j=1,...,M. No rank is supplied or guessed.
3. Compute a full-row-rank quotient matrix Rhat with ker Rhat=Uhat. Put c=Rhat Y0.
4. Query each basis state e_i once, receiving Zi. Define the quotient-map columns H_i=Rhat Zi+c.
5. Choose a right section J of Rhat, so Rhat J=I on its row space, and output

       Fhat=J H, betahat=J c, Ghat=any basis matrix for Uhat.

The zero-row quotient when Uhat is the whole space has the canonical empty section, giving Fhat=0 and betahat=0. When Uhat=0, Rhat may be the identity. These are explicit branches, not inverse operations on singular matrices.

The learned kernel samples Fhat x+betahat+Ghat r with fresh fair r. It is a generative algebraic model, not a resampling cache of observed outputs.

## 3. Exact recovery event and probability

Write d=dim U. Conditional on Y0, the shift eta0=Y0+beta is fixed in U. Each Dj=eta_j+eta0 is therefore still independent uniform on U. This conditional law does not depend on Y0. In particular the shared Y0 does not introduce the troublesome dependence that would arise for general noise distributions.

If the Dj fail to span U, some nonzero linear functional on the d-dimensional space U annihilates all M samples. There are 2^d-1 such functionals, and each event has probability 2^(-M). Thus the single event E={Uhat=U} satisfies

    Pr(E^c) <= (2^d-1) 2^(-M) <= 2^(n-M) <= delta/2.

For d=0 the failure probability is exactly zero.

On E, the quotient removes every future noise draw exactly. Hence c=Rhat beta and, for every i, H_i=Rhat F e_i with probability one. Consequently

    im(Fhat-F) subset U, betahat-beta in U, im Ghat=U.

For EVERY input x, the learned affine coset Fhat x+betahat+U equals F x+beta+U, and both conditional distributions are uniform on that coset. Therefore the learned transition kernel equals the true kernel globally, exactly, on E. There is no additional union bound over input states, future queries, future tasks, or the size of the state space.

The individual matrices F and beta are identifiable only modulo this fibre freedom. The theorem does not claim to recover invisible original parameters or private original random bits.

## 4. Controllability admission and conditional confidence

Compute the learned controllability span

    Vhat=span{Ghat,Fhat Ghat,...,Fhat^(n-1)Ghat}.

Admit the pure-return realization exactly when dim Vhat=n. The ordinary exact verifier checks only the learned model and its synthesized circuit. It does not turn statistical truth of E into a deterministic certificate about the unknown source.

A useful stronger fact holds even on E^c, under the structural promise. Always Uhat subset U. From Rhat(Fhat e_i)=Rhat(Zi+Y0), one obtains

    Fhat e_i - F e_i in U,
    betahat-beta in U.

Let V=span{U,FU,...,F^(n-1)U} be the true reachable subspace. It contains U and is F-invariant. Since im(Fhat-F) subset U, it is also Fhat-invariant; it contains Uhat. Therefore Vhat subset V on EVERY transcript generated by the promised kernel.

It follows that a truly uncontrollable kernel can never be falsely declared controllable by this procedure. If the true kernel is controllable, then on E the learned one is controllable as well (feedback changes with image in U preserve the reachable span). Admission probability is at least 1-delta/2, and

    Pr(E^c | admission) <= (delta/2)/(1-delta/2) <= delta.

Thus the conditional confidence claim after admission is valid, not a silent conditioning on a potentially rare success flag. This probability averages over the admitted training transcripts for the fixed unknown kernel. It is not a posterior correctness probability for every particular observed transcript, nor a guarantee after conditioning on a rare later event. If the true kernel is uncontrollable, admission has probability zero and no conditional execution theorem is asserted. A rare erroneous rejection of a controllable kernel is included in E^c; it is not automatically evidence against the model.

## 5. Acquisition-to-reuse receiving

On admission, run the exact affine realization construction on (Fhat,Ghat,betahat). Its independently reviewed specification is `AFFINE_PROGRAM_REALIZATION_SPECIFICATION.md`, SHA256 9e810f64f08ead6182627693747d71dc34f767fdf0797d8d00df3f9628340f0e. Its reviewed executable frontend is separate. The resulting quantum source has psi=|+>^n, phase-safe c, acquired Stinespring/control/inverse/reflection circuits and an n-step exact pure-return certificate.

On the same event E, this realization preserves the TRUE classical controlled process: system interactions diagonal in the observed source labels, prescribed outcome-retaining interventions preserving the system-valued diagonal observable algebra, and public source-label observations have the right law. A future consumer may choose its operations adaptively using the entire public learned description and training transcript, subject to the execution theorem's prescribed-slot interface. Since the law is exact on all inputs on E, public cache disclosure does not introduce the support-membership attack against empirical resampling.

This is not an equivalence with an unknown quantum dilation. Classical training samples do not identify source coherence, environment records, or behavior under arbitrary quantum source interventions. Arbitrary quantum operations on the newly synthesized source define its own quantum task. Original random tapes and artificial simulator jump/timing records are not public outputs of the claimed classical equivalence.

The statistical event supports any number of future finite reuses without a query-count factor multiplying delta. It does NOT eliminate numerical execution errors or operation costs. For a prescribed finite consumer, let its implemented simulator have uniform full trace-norm error at most epsilon_exec relative to the learned exact model, conditional on each admitted transcript. Comparing ideal and implemented experiments with the SAME transcript/admission information gives

    conditional-on-admission output error <= epsilon_exec + 2 delta.

The factor two is the maximal trace norm between states. Without conditioning, and comparing an ideal experiment with the same reject/accept convention, the corresponding bound is epsilon_exec+delta because Pr(E^c)<=delta/2. TV or half-trace-distance conventions halve the statistical term appropriately. These bounds retain arbitrary consumer reference systems permitted by the diagonal-process task and concern the joint transcript/output experiment (or its admitted-transcript average). Numerical epsilon_exec is uniform per admitted transcript, but the statistical delta bound must not be upgraded to such a pointwise transcript guarantee. They are not statements about a postselected source state or about outputs conditioned on an arbitrarily rare future outcome.

For many executions, allocate the numerical budgets separately (for example a summable sequence). No single finite-precision simulation circuit is promised zero cumulative error over an infinite lifetime. No statistical relabeling of epsilon_exec as delta is allowed.

## 6. Full costs and centering distinction

The number of one-step transition calls is exactly

    Ncalls = M+1+n = 2n+ceil(log2(2/delta))+1.

Each call needs a chosen-state preparation/reset if that is how the sampling device is accessed, including all repeated zero-input calls. Charge up to Ncalls such preparations, not merely the n basis-state preparations. Full observations alone contain n*Ncalls bits. Elementary streaming elimination and quotient/section construction cost polynomial(n,log(1/delta)); retaining the learned matrices takes O(n^2) bits apart from confidence metadata. The entire training transcript may also be retained and is charged if retained. Circuit synthesis and exact verification incur their actual polynomial costs. The transition clock rate, if relevant, must be separately known or acquired with an explicitly priced clock-estimation procedure; it is not learned from one-step state samples here.

Future coupling access is not produced by learning the source. For a supplied acquired K/b and known psi preparation, ordinary compression already gives a block encoding of

    Hbar=(I_system tensor <psi|) K (I_system tensor |psi>).

Prepare an auxiliary psi, apply the K block on system plus that auxiliary source, unprepare, and take the success block. Its normalization is b; no numeric mean or normalized postselection is required. An LCU with K then encodes K-Hbar tensor I at normalization 2b. This is standard block compression, not a new learned operation.

What remains costly is the real system term sqrt(lambda) Hbar, or certifying it is zero / acquiring a sharper normalization. The same physical generator must retain that term, except for an explicitly removed scalar identity commutator. Sparse Pauli lists admit exact numeric means and cancellations through the already reviewed stabilizer procedure. Arbitrary Boolean diagonal functions do not automatically admit exact classical numeric means: for psi=|+>^n their means contain satisfying-assignment counts. That numeric-counting limitation does NOT imply that their mean BLOCK ENCODING is unavailable when K's circuit is acquired.

## 7. Why the model promise is essential

The sample span is not a distribution-free support certificate. A nonuniform distribution with a very rare additional component can be indistinguishable on this training budget but differ after many future uses. Likewise a nonlinear kernel can agree at zero and all basis states yet disagree elsewhere. Correlated noise can invalidate the rank-tail probability even while each individual observation has a superficially correct marginal. Full-state access and chosen resets remove obstructions that persist in latent or passive identification. None is obtained from the algebra after the fact.

Therefore the exact lifetime confidence is a theorem inside the promised affine/uniform-subspace model. It cannot be upgraded by testing a few extra inputs to a guarantee over arbitrary unknown sources.

## 8. Strong ordinary comparison and scientific scope

This learner is classical Gaussian elimination plus active affine probing. An equally informed ordinary learner receives the same samples, can retain exactly the same finite model and has exactly the same reusable-law guarantee. The acquisition advantage is over an interface that assumes a coherent source oracle or merely caches samples, not over strong active system-identification methods.

[Angluin, Queries and Concept Learning](https://homepages.math.uic.edu/~lreyzin/papers/angluin88.pdf), formalizes the role of chosen queries versus random examples. The present oracle is a stochastic one-step chosen-state oracle rather than her deterministic membership oracle; it should not be compared to a passive learner without acknowledging the stronger access.

[Chen–De–Vijayaraghavan, Learning a mixture of two subspaces over finite fields](https://arxiv.org/abs/2010.02841), already studies substantially harder finite-field subspace acquisition, including polynomial recovery for incomparable subspaces and an LPN-related boundary for nested mixtures. Our single uniform noise subspace has the elementary span recovery above; no advance over that literature is claimed.

[Bianchin, Data-Driven Exact Pole Placement for Linear Systems](https://arxiv.org/abs/2303.11469), demonstrates that acquiring feedback from finite data rather than a supplied model is an established objective. Its stated trajectory/control setting is not silently identified with our finite-field uniform-noise oracle, and its abstract is not used as a theorem proving this particular sample bound.

The additional receiving conjunction is explicit: purely classical observations identify a global algebraic law with one confidence event; known-program realization synthesis then supplies coherent pure-return compiler inputs; future acquired couplings can reuse them. This is a narrow but genuine sample-to-reusable-program closure, not a demonstrated novel learner, unrestricted cumulative intelligence, practical superiority, or a new physical experiment.

No new restricted-source retrieval occurred in this comparison. Previously denied sources remain excluded. Primary sources above establish the ordinary comparators at the stated scopes, not completeness of a literature search.
