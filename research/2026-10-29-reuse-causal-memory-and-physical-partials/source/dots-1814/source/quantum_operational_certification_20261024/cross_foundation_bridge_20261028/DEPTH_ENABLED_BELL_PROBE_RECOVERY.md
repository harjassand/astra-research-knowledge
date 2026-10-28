# One more calibration call: endpoint Bell probes and the exact two-world risk

28 October 2026. **Reviewer-derived constructive addendum; separate independent receiving pending.** Derived while reviewing `SHORT_EPISODE_ONE_USE_RECOVERY_LOWER_BOUND.md` (SHA256 `122f5e11b1d2b2ce284515f8b9276dcaf82e775a678ba444ba8930ff008d20bc`). This note preserves the source's prescribed fixed-time, identity-encoded, one-use, forward-only deployment. It changes only the allowed calibration depth from `r-2` to `r-1`; it does not add native actions or inspect the environment. No novelty claim is made.

## 1. The precise additional resource

Keep the source's known two-candidate promise: the common maps, dimension, initial-state candidates and late channels are known; the unknown label is `j in {1,2}`. All deployment starts are fresh and independent of calibration. Let

    Delta=(1-lambda)v,       c=1/2-lambda/4,       t=lambda/4,
    lambda=1/4,
    w_1=(c+Delta/2, c-Delta/2, t, t),
    w_2=(c-Delta/2, c+Delta/2, t, t),                   (1)

in Pauli order `I,X,Y,Z`. In particular `Delta>=9/256`, `c=7/16`, `t=1/16`. These are the Pauli probabilities of the prescribed endpoint channels, not probabilities for an extra native noise flag.

Allow at most n calibration episodes with native length at most `r-1`, together with any amount of the original shorter calibration. Each longer episode starts from a fresh `rho_j`. Calibration may still use arbitrary references, entanglement, recycling, feedback and measurements. Deployment remains exactly `r-2` forwards then one USE on the independent arbitrary payload, with identity encoding. No extra deployment USE, reset, encoder or change of service time is used.

## 2. Constructive endpoint experiment, without environment tomography

For each of n independent calibration episodes:

1. Prepare a Bell pair `|Phi+>` locally and keep its second qubit as reference.
2. Execute exactly `r-2` forward calls and one USE on the first qubit.
3. Perform a Bell-basis measurement on the output qubit and the retained reference.

A Pauli P on the first half produces the corresponding orthogonal Bell state (global phases are irrelevant). Thus the measurement gives one sample `P in {I,X,Y,Z}` with exactly distribution `w_j`. The measurement is an ordinary allowed terminal calibration measurement, not a supplied environmental flag. It neither reconstructs the hidden memory nor needs coherent control of the forward action.

Let `N_I,N_X` be the observed counts. At fresh deployment, use decoder I if `N_I>N_X`, X if `N_X>N_I`, and an independent fair I/X choice on a tie. The retained Bell reference never contains the future payload. The procedure compares only the two candidate effective service channels; it is not a general unknown-channel or memory identification algorithm.

The complete calibration bill is n whole-process starts, `n(r-2)` forward calls, n USE calls, n Bell-pair preparations and n Bell measurements, plus classical counting and compilation. Native length per episode is `r-1=d^2-d`. All waiting forwards are charged. No source samples have actually been collected for this note.

## 3. Exact finite-n minimax theorem

Define `P_j=w_j^(tensor n)` as the classical distribution of all n Bell labels. For both Bell loss and half-diamond error relative to the world-informed best decoder for this same service, the exact minimax **expected additive regret** is

    R_n = (Delta/2)[1-TV(P_1,P_2)].                    (2)

This includes arbitrary quantum calibration strategies within the stated depth/count budget and arbitrary CPTP deployment decoders. It also permits additional short episodes, which carry no world information. In particular

    R_0=Delta/2.                                       (3)

Consequently the source lower bound is the exact short-calibration minimax value for this two-world family, not only a lower estimate: the equiprobable I/X correction attains it.

### Upper bound and symmetric optimal decision

For a Bell-label sequence h, its likelihood ratio is

    P_1(h)/P_2(h)
       =[(c+Delta/2)/(c-Delta/2)]^(N_I-N_X).            (4)

Y/Z labels cancel. The decoder in Section 2 is therefore the equal-prior likelihood-ratio decision, with error probability

    p_e=(1/2) sum_h min(P_1(h),P_2(h))
       =(1-TV(P_1,P_2))/2.                            (5)

A correct I/X decision attains oracle loss `L*=1-c-Delta/2`; an incorrect one has loss `L*+Delta`. Both corrected channels are Pauli channels, so these statements hold exactly for Bell loss and half-diamond error. Swapping worlds and swapping I/X labels leaves the experiment and tie rule invariant. Hence both worlds have the same regret `Delta p_e`, proving the worst-world upper bound (2), not merely a prior-average bound.

### Lower bound against all calibration strategies

An episode of at most `r-1` calls has only one possible world-informative event: its first USE after precisely `r-2` forwards. Such a USE is the last call. Every earlier USE is an identical complete channel in the two worlds and resets the memory to common tau; an episode without USE exposes nothing. The full reset/source interface is essential to this statement.

For a proof-only relaxation, draw an independent hidden classical label `P~w_j` for each of the n potentially long episodes. If the strategy reaches its late first USE, implement it as the known unitary `Ad_P`; otherwise do not use that label and implement the relevant common channel. This is exactly a realization of the endpoint Pauli channel on any entangled input. The remaining learner operations, common short channels, adaptive episode choices, measurements and outputs are all independent of j. Thus every allowed calibration experiment is a common CPTP postprocessing of the classical register with law `P_j`. Giving the labels to the learner can only help. This relaxation does **not** assert that the native source supplies a flag: Bell probes happen to attain the relaxed information by a paid allowed experiment.

Condition on a label sequence h. Any calibration postprocessing and any retained quantum ancilla can be absorbed into a single CPTP decoder `R_h`, since deployment is fresh and the payload starts independent. Define its nonnegative Pauli Bell coefficients `a_P(h)` as in the source; they sum to one. The prior-weighted Bell scores for choosing I or X are

    (1/2)[P_1(h)(c+Delta/2)+P_2(h)(c-Delta/2)],
    (1/2)[P_1(h)(c-Delta/2)+P_2(h)(c+Delta/2)].

Both dominate the Y/Z score `t[P_1(h)+P_2(h)]/2`, since `c-Delta/2>t`. Therefore no CPTP decoder improves the conditional maximum beyond I or X. Summing the larger score gives

    maximum prior-average Bell fidelity
       = c + (Delta/2) TV(P_1,P_2).                   (6)

Subtracting from oracle fidelity `c+Delta/2` proves the prior-average regret bound (2); worst-world regret is at least the prior average. Half-diamond loss is at least Bell loss for any decoder, while the attained Pauli corrections make the two losses equal. Thus the same lower bound is tight for half-diamond regret. This proves the theorem without an environment-tomography or channel-discrimination oracle.

If the implementation randomizes its decoder, (2) covers expected loss conditional on the random record. For the attaining Pauli strategy it also equals the error of the averaged corrected channel, because Pauli half-diamond loss is affine in its identity weight.

## 4. A transparent finite confidence certificate

In world 1 define a random variable Z equal to `+1` for I, `-1` for X and zero for Y/Z. Then `Z in [-1,1]` and `E Z=Delta`; world 2 is its reflection. The tie-randomized decision error obeys the simple Hoeffding bound

    p_e <= exp(-n Delta^2/2).                         (7)

Thus

    n >= (2/Delta^2) log(1/eta)                       (8)

suffices for probability at least `1-eta` of selecting an exactly oracle-optimal decoder. The expected regret is at most `Delta eta`. A dimension-uniform sufficient budget replaces `Delta` in (8) with `9/256`. The native-call budget remains proportional to `d^2 log(1/eta)`; the number of episodes being dimension-uniform is not a dimension-free total-resource claim.

The exact Bhattacharyya bound can improve the constant:

    p_e <= (1/2)[2 sqrt(c^2-Delta^2/4)+2t]^n.          (9)

It follows directly from `min(a,b)<=sqrt(ab)` and product distributions. Equation (8), rather than an informal asymptotic or uncomputed tomography constant, is already a complete finite certificate. Outward rounding of logarithms/roots and actual apparatus errors would be paid in an implementation; none has been executed here.

For `q=2,d=3,r=7`, the exact rational checks give `Delta≈0.05033886163` and `R_0≈0.02516943081`. At 64 Bell-probe episodes, the exact decision risk is `p_e≈0.33333118233` and `R_64≈0.01677951226`. This is a deterministic calculation, not an empirical experiment. The larger-than-zero sample cost is visible: allowing the informative depth does not make the weak statistical decision free.

## 5. Boundary learned from the obstruction

A calibration policy that never reaches the actual fixed service depth cannot discover the hidden late correction preference, even with unlimited short experiments. Increasing this family's maximum episode length by **one** call permits a direct endpoint decision experiment. The successful procedure preserves independent starts, the actual forward clock, the same one-use service, and the payload/reference restrictions; it changes the missing resource rather than pretending that a learned classical simulator supplies coherent guarantees.

The result is specific to the known two-candidate Pauli endpoint family and this depth cap. It does not claim a generic efficient quantum learner from the classical short-word theorem, no-rank/core memory tomography, near-perfect correctability, fixed mixing margins, or sample/computational optimality outside this family. The source's positive oracle noise floor remains unchanged.

Directly relevant recovery-decision prior art is [Morales-Hashemi–Smith–Cao, arXiv:2610.03545v1](https://arxiv.org/html/2610.03545v1), Sections III.3/V and Appendices B/H/I: it treats retained quantum calibration, CPTP recovery regret and delay-dependent calibration costs; Appendix B.5 gives a multiplicative Pauli decision bound. Equations (2)–(6) here are a specialized exact attainment calculation, not a new general recovery-information principle. Its near-correctable QEC construction and this noisy Singer endpoint family have different hypotheses.

The underlying Singer/difference-set quantum mechanism remains credited to Singer and the close Mereghetti–Palano (2002) / Bertoni–Mereghetti–Palano (2003) automata antecedents identified in the governing source. Bell-diagonal channel probing, likelihood-ratio testing and the Pauli simplex calculation are elementary established techniques; this note makes no priority or novelty claim for their combination.

`short_episode_recovery_independent_check.py/.json` checks the lower-bound bridge and exact finite-n risks. The n-step risk calculation uses integer recurrence coefficients of `(p z + m z^(-1) + 2t)^n`, with `p=c+Delta/2`, `m=c-Delta/2`; it uses no RNG, acquired data or hardware. This constructive theorem requires a separate receiver and does not inherit the lower-bound receipt.
