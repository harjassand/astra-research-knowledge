# Conditional consequences of a universal good-schedule bound

These deductions assume the producer proves one event G in the independent proposal-clock/location space such that every supported Pauli history on G, at every physical time under consideration, is corrected by the same recovery with zero accumulated logical action. Assume P(G^c)<=B_L(T)=A L^4(1+kappa T)e^(-cL). This note does not certify that premise.

## Bounded measurable time-dependent generator drift

For each fixed patch type a at location x, keep an actual baseline floor nu_a(D_a-Id), with local dimension d_a. Let E_(x,a)(t) be a bounded measurable, time-dependent HP trace-annihilating map on that same patch, with

    ||E_(x,a)(t)||_diamond <= nu_a/d_a^2

for almost every t. Preserve the same summed local proposal-rate and overlap budget required by the envelope theorem. Define

    Psi_(x,a)(t) = D_a + E_(x,a)(t)/nu_a.

With normalized Choi convention J(D_a)=I/d_a^2, the norm bound implies J(Psi)>=0; trace annihilation gives trace preservation. Thus Psi(t) is CPTP at every allowed time, and exactly

    nu_a(D_a-Id)+E_(x,a)(t) = nu_a(Psi_(x,a)(t)-Id).

The nonautonomous propagator has the same independent, fixed-rate Poisson clocks; only the channel applied at an event depends on its time. Conditional on a good clock/location schedule, expand every fault Kraus operator into supported Paulis. The premise corrects all histories in each common Kraus record, so every recovered Kraus operator on the code is scalar times identity. The conditioned channel is CPTP and therefore is logical identity. Averaging schedules gives

    ||Dec U(T,0) Enc - Id||_diamond <= min(2,2 B_L(T)).

Constants can absorb the factor 2 according to the producer's bad-event convention. No derivative or total-variation bound on E(t) is used. This gives a meaningful conditional extension to time-dependent coherent and dissipative drift, beyond the producer's stated time-independent ball.

This remains a Markovian/time-local construction with state-independent proposal times and the specified supports. It is not an arbitrary non-Markovian bath theorem. Adversarial state-dependent clocks, rate modulation beyond the budget, growing supports and quantum environment memory require additional hypotheses and proof.

For Hamiltonian drift E(t)=-i[H(t),.], the sufficient condition ||H(t)||<=nu_a/(2d_a^2) implies the displayed diamond bound. It is an absolute pointwise local strength condition, not an integrated T||E|| condition. The floor/completion remain actual parts of the baseline.

## Explicit endpoint error budget

Let the actual preparation Enc' and final readout/recovery Dec' be CPTP maps with

    ||Enc'-Enc||_diamond <= eta_enc,
    ||Dec'-Dec||_diamond <= eta_dec.

Channel contractivity and the triangle inequality give

    ||Dec' U(T,0) Enc' - Id||_diamond
       <= eta_enc + eta_dec + min(2,2 B_L(T)),

capped at 2 overall. This cleanly separates storage protection from endpoint acquisition. Constant per-qubit preparation/readout error does not automatically give a small global eta_enc or eta_dec; fault-tolerant endpoint protocols need their own analysis.

## Storage scale with the polynomial factor retained

For target unhalved diamond error eta, if A L^4 e^(-cL)<eta, the original displayed bound guarantees any T satisfying

    kappa T <= eta e^(cL)/(A L^4)-1.

This is a lower guarantee. Choosing any a<c yields exponential time e^(aL)/kappa for sufficiently large L. No practical size estimate follows without usable A,c,epsilon and an implementation meeting the local budgets.

## What these corollaries do not add

They do not establish historical priority, external mathematical correctness, a useful threshold, a 3D physical realization, logical gates, noisy recovery thresholds, or robustness of the original non-completed active-jump generator. The time-dependent extension is a deduction from the stated universal schedule premise; it is not an independent proof of that premise or a new discovery of Choi regularization/linear-span correction.
