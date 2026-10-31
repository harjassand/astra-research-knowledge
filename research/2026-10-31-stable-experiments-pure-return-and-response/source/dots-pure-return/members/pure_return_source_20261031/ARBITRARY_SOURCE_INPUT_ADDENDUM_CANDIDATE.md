# Arbitrary source inputs and prescribed joint interventions
31 October 2026. Addendum candidate. It receives the pure-return first-event construction only after that whole base has separately passed review. It does not assert an unreviewed base by implication.

## 1. Stronger quantum task, not a stronger classical-source identity
Keep the acquired finite-register channel Φ, fixed vector ψ, coefficient state c, controlled circuits, centered Hermitian K, system-only H0, and operator return certificate (Φ†)^mQ<=Q/16. The source dynamics between interventions remain exactly the same.

Now permit an arbitrary initial source-system-reference state and p arbitrary joint source-system CPTP instruments at prescribed times, with their reference/output records retained. The final quantum source may also be included in the requested output. All such state preparation and instrument costs are supplied and paid. Event times, artificial Kraus records and other private simulation coordinates are still not exposed.

This is a quantum-source task. The classical signed-shuffle equivalence still requires its separately specified invariant observable/control algebra. Arbitrary quantum source interventions or invalid classical encodings do not describe an unchanged classical stochastic noise model.

## 2. Uniform activity bound
Let V=sum_(j=0)^(m-1)(Φ†)^jQ and κ=e^θ-1<=1/(32m). The base proof uses

    Zθ=I+32κV,  I<=Zθ<=2I,
    Gθ†Zθ<=256κ b^2m^2 Zθ

on the high-rate branch. These operator inequalities already hold on the whole source/system space, not only on ψ.

For any normalized initial joint state, Tr(Zθ rho)<=2. For any trace-preserving instrument C with its outcomes retained, positivity/unitality of the adjoint gives

    C†(Zθ tensor I_records)<=2I<=2Zθ.

This remains true when the instrument acts jointly on source, system and existing records, because its output weight still lies between I and2I. Thus each prescribed intervention multiplies the weighted comparison by at most2, and the exact dark-count bound becomes

    E exp(θ N_T)<=2^(p+1) exp[256κ b^2m^2 T].           (1)

No division by an outcome probability or normalized postselection is allowed. Formula (1) is uniform over arbitrary initial references and all admitted instruments.

At θ=log(1+1/(32m)), a sufficient count cap is

    ceil(64m[8 b^2T m+(p+1)log2+log(1000/epsilon)])+1. (2)

Its order is b^2m^2T+m(p+log(1/epsilon)+1). The same extra prescribed boundaries occur in the no-event-window count. Replace Scap and EVERY per-call error budget in the base construction consistently; do not reuse budgets computed for the smaller vacuum-only cap.

## 3. Why the numerical/CP receiver survives
The acquired P/Q projectors, source-label blocks, scaled fast kernels, actual jump stack and complete first-event isometry are already defined and norm-controlled on every physical source input. Their operator/isometry error estimates do not require the current source to equal ψ. Every actual post-jump source state was already retained.

The count-augmented exact future generator has the same dimension-independent norm bound. Joint CPTP instruments contract trace distance just as system-only instruments do. A backward hybrid through the larger cap therefore prices local errors, representative-time changes and skipped tiny windows exactly as in the base proof. The exact tail bound (1) is now uniform over ALL joint inputs, so the discarded-tail CP effect is bounded on the full physical input space. This gives the corresponding full joint-channel diamond bound, with the private time/environment coordinates traced out.

A final source output is just part of that finite physical space, not disclosure of the internal time record. No claim of trace-distance proximity between continuous and discrete exposed timestamps is made.

The ordinary low-rate Poisson-channel construction also acts on arbitrary source inputs and retains them across joint controls. Its timing-near-control and Hamiltonian error estimates use only the number of slots, operator norms and CPTP contraction. Those costs remain paid.

## 4. The b=0 exception must change
The base shortcut 'b=0 implies only H0 evolution' relied on initially fixed ψ and system-only controls. It is FALSE for an arbitrary initial source or an intervention that excites the source: lambda(Φ-I) still acts.

For T>0, choose a conservative acquired coupling normalization

    bbar>=max(b,T^(-1/2)), Bbar=bbar^2 T.

Use a certified dyadic upper normalization within a factor2 of max(b,T^(-1/2)); then max(b^2T,1)<=Bbar<=4max(b^2T,1). This avoids an exact irrational comparison. All subsequent formulas use the actual chosen bbar and Bbar.

Rescale the supplied coupling block to K/bbar by a known attenuation. If K=0, use an explicit zero good block with failure flag. The source/first-event construction can then be run with bbar in every scalar envelope, branch threshold, cap and error bound. Its proof uses upper norms, so this is valid even when the true coupling is zero. The cost remains polynomial in 1+b^2T and the other declared parameters; it is not optimized for this special case.

For T=0 use the specified zero-duration controls/identity channel directly. For lambda=0 the source has no dissipative or sqrt(lambda) coupling evolution; simulate H0 and the prescribed joint controls while retaining the arbitrary source. These branches do not evaluate source-rate denominators.

## 5. Concrete encoding validity
For an abstract full-register source, the certificate is required on that full register. A concrete permutation source may instead first be defined on its valid n!-dimensional subspace. An arbitrary identity extension on invalid binary strings would not satisfy the full return certificate.

An acquired fix is to compute validity, apply the intended source Stinespring isometry on the valid branch, and on the invalid branch transfer the old source into a flagged private environment and prepare ψ. Distinct flags pinch valid/invalid cross terms. This is a CPTP extension with a unitary Stinespring completion and polynomial validity/preparation cost. Invalid inputs return to ψ in one source-channel application; the overlap contraction A annihilates them. Set K=0 on invalid encodings. The full return/power certificates then hold, and arbitrary full-register source inputs have a defined quantum interpretation.

Alternatively one may retain a carefully invariant valid-subspace theorem with its projector explicitly inserted throughout. One cannot mix the two conventions without proof. Neither convention turns an invalid permutation string into a physical classical card configuration.

## 6. Optional fixed-window action accounting
The earlier reviewed fixed-window accounting can also be earned here, rather than assuming path durations add to T. Put H=alpha0 T, ellerr=1+ceil(log2(1000/epsilon)), and choose an exact downward dyadic maximum window within a constant factor of

    tau*=1/[1024 m^2(Bbar+p+ellerr+1)].

This is below the base scalar-normalizer limit. Recompute the no-event window count, total call cap S, t0/p0 and every subsequent budget using that maximum. The exact count cap (2) is O(Bbar m^2+m(p+ellerr)), so S=O(m^2(Bbar+p+ellerr+1)) and S*tau*=O(1), including fixed prescribed boundaries.

The conditional virtual cap contains s*tau* and logarithms of its endpoint/precision bounds. It is therefore polynomial in m and logarithmic parameter/input sizes, with no additional factor Bbar or p per call. The scaled-kernel operation has the same polynomial-m/log-error cost on each virtual dwell, independently of lambda times that dwell.

Each padded H0 interval is stored as a binary fraction of the known maximum tau*. A B_time-bit implementation uses controlled fixed durations T*tau*/2^j, whose actual sum is at most T*tau* PER SLOT. There are O(S*Aamp*(Kcap+1)) such slots, so their ordinary Hamiltonian action cost is O(Aamp*(Kcap+1)*H), plus the explicitly repeated finite-precision query overhead. This is deterministic circuit accounting, not charging only one selected trajectory.

The LOW-rate branch needs the same windowing; its original single global Poisson-CDF scan alone did not establish near-linear source work. Under mu=lambda T<4096 Bbar m^2 and the new maximum tau*, every window has Poisson mean at most4. For each of the W=O(1/tau*+p) fixed windows, cap its count at O(1+log(W/epsilon)), scan only that many Poisson CDF entries, sample/sort the corresponding uniform times within that window, and allocate O(epsilon/W) tail/source error. Overflow receives an unconditional CPTP continuation. The union of windows has exactly the original Poisson-channel law before truncation; source and all private records are retained across boundaries.

This has W polylog(W/epsilon) finite source work, rather than an unpriced large-mean scan. Prescribed controls lie at window boundaries. Rounding/near-boundary event errors and finite source-bit errors receive their per-window budgets just as in the base low branch; every number of comparisons, time slots and precision bits is now bounded by the logarithmic window cap. Each padded Hamiltonian slot is a binary fraction of the same maximum tau*, so summing its ACTUAL fixed-duration calls over the W windows pays O((H+sqrt(mu Bbar)) polylog(W/epsilon)) action, since W*tau*=O(1). The low-branch inequality sqrt(mu Bbar)<=64 Bbar m keeps this within the stated near-linear extensive envelope, with polynomial m factors. This re-pricing is required for the both-branches claim; the base polynomial theorem itself was already valid.

Consequently the resulting query/arithmetic envelope is near-linear in 1+b^2T+H+p, multiplied by a fixed polynomial in m, circuit/register sizes and logarithmic rate/precision/input-conditioning factors. Keep the REAL per-query encoding costs multiplicative: a query theorem does not make an opaque W or K oracle cheap in elementary gates. No optimal polynomial in m, optimal precision dependence, small constant or practical crossover is claimed.

## 7. Scope
This addendum changes the initial-state and prescribed-control domain, not the acquisition assumptions. A known prepared ψ is still needed to implement its reflection and the source coefficient interface, even when the physical source is not initialized in ψ. No unknown-state reflection oracle is supplied. The return certificate, source/channel circuits and consumer operations remain paid.

Adaptive choices of operations on retained outcomes are allowed at the prescribed slots. Arbitrarily chosen intervention times, public jump/time records, normalized rare postselection and arbitrary time-dependent source generators are not established. No implementation, practical advantage or novelty claim follows.
