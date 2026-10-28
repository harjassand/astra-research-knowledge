# Independent statistics audit: positive-loss decoder bandit

28 October 2026. Reviewer: `producer-workspace/audit_count_pilot_fresh`.

**PASS at the expected one-shot terminal-service scope.** Source `ordinary_prequential_small_loss_decoder_bandit_20261028.md`, SHA-256 `6edb6a3af1118947c1a864113a24d77eef437386eafb7d8694a4aa651dc8d1dc`. The source was not edited. No source calls, RNG draws, acquisition simulation, generic convex-optimizer execution or hardware claim is made by this review.

## 1. Physical return bit and exact conditional law

Condition on the actual prior classical record and its induced quantum source-memory state. The new independently prepared qubit then sees a CPTP channel E_h. A played decoder is fixed before this call using private coins that are not leaked through the complete source port. The source may distinguish its quantum input; it may not choose a different complete map from an extra classical decoder/role label. The later receiver instrument can change future conditional memory states, which are included in the NEW decoder-return occupation law.

For each ordinary six-state input, the actual mismatch probability is

`d Tr[C (Pi_(j,-s) tensor r_(j,s)^T)]`.

Averaging gives q(C)=dTr(CT), T>=0, exactly linear on the normalized TP Choi affine set, and in [0,1] for every physical C. It is also `(2/3)(1-F_e)` for the conditional qubit channel. T is an analytic effect, not acquired source data. The acquisition is the bit y; its identity y^2=y is essential.

The Pauli tangent coordinates have Gram kI and zero output partial trace. The normalized TP affine space has exactly D=3d^2 real dimensions. The known center, gradient and Hessian formulas are consistent with the output-first Choi convention.

## 2. Rational exploration and exact dual

For a rational V with `(1/2)I<=V^T H V<=I`, its columns v_i have H-norm at most 1. Thus the played perturbation z v_i/2 has normalized matrix norm at most 1/2, ensuring `C_play>=C_t/2>0` and exact TP. Its mean over the independent sign is exactly C_t, not an approximately centered decoder.

Write `u_i=V^{-T}e_i`, with the inverse EXACT. The two sign-specific return probabilities differ by `l_t^T v_i`. Consequently

`E[2D y z u_i | h]=sum_i u_i v_i^T l_t=l_t`.

The equality relies on exact primal/dual cancellation, not orthogonal columns. A separately rounded dual would generally introduce bias. Further,

`||2D y z u_i||_(H^{-1})^2=4D^2 y e_i^T(V^T H V)^{-1}e_i<=8D^2 y`.

Averaging gives the loss-dependent local second moment at most `8D^2 q_h(C_t)`. This is not a deterministic-loss oracle, a microscopic error indicator or the false substitution y^2=q^2. It remains valid for adaptively changing conditional channels and actual noisy return measurements.

## 3. Residual telescope and fixed comparator

The certified stationarity residual is at most delta in coordinate norm; the coordinate diameter is at most 1. The Bregman three-point identity therefore contributes at most delta in one step. The first update certificate ensures every relative perturbation eigenvalue lies in [-1/2,1/2]. On that interval,

`x-log(1+x)>=x^2/3`.

One elementary proof differentiates the difference: its derivative is `x(1-2x)/(3(1+x))`, with the sign of x. Summing over eigenvalues gives Bregman divergence at least r^2/3. Cauchy-Schwarz and `ar-r^2/3<=3a^2/4<=a^2` then give exactly the pathwise inequality (12), including its `N delta/eta` debit.

For a fixed physical D, mix its Choi matrix with zeta of the replacement center. This comparator is strictly positive, its initial divergence is at most `k log(1/zeta)`, and its loss is at most q(D)+zeta. Predictability and the conditional estimator identity allow expectations against this fixed comparator. With `L=E sum y_t`, the variance term is exactly bounded by `8eta D^2 L`, giving

`(1-8eta D^2)L <= E sum q_t(D)+zeta N+k log(1/zeta)/eta+N delta/eta`.

The infimum is over deterministic fixed decoders in this expected actual-history objective. It is not a random sample-path hindsight comparator, nor the source occupation law of a policy that deployed D earlier. Taking a deterministic minimizer of the compact expected objective is valid without a simultaneous high-probability concentration statement.

## 4. Finite prox and arithmetic

I independently checked the stated local-norm and arithmetic constants. The main independent receipt supplies a separate complete finite-control/prox review and is imported for its implementation construction, without a dependency cycle.

The local gradient size gives `a<=sqrt(8)eta D<=1/16`. Stationarity at the exact minimizer implies `r_*^2/(1+r_*)<=a r_*`, hence r_*<=1/15. The matrix box therefore contains the minimizer with strict relative margin. The learner-created lower bound mu has O(N+log d) bits and is not a source spectrum premise.

On the box, the proposed objective accuracy yields distance at most `delta mu^2/(sqrt(2048) k)` and gradient residual below delta/4. The prescribed coordinate mesh adds at most delta/32 to that residual and less than 1/64 to the H displacement. Thus the exact rational guards have genuine slack. A dyadic mesh within a factor two of the displayed rational upper bound is an available finite choice with the claimed bit length. TP is exact in tangent coordinates. The known convex solve must return certificates on every history; numerical failure cannot be relabeled as a fresh statistical event.

The rational V certificate likewise has ample slack after the stated approximation of (3/4) times inverse Cholesky. Exact inversion of V then produces the dual. No unknown-source eigenbasis or source inverse is supplied. The finite implementation is polynomial in N,d and the precision bits, not polynomial in inverse mu. This review does not assert that its generic finite optimizer was run.

## 5. Terminal transfer, budgets and finite randomness

The stable received terminal-prefix proof applies to this new all-probe process, not to the older physical-Pauli occupation. At a terminal slot the sampled physical decoder, rather than an undeployed center, is applied. Averaging its fresh exploration coins and the prefix histories gives actual Bell loss `(3/2)L/N`, preserving arbitrary initially independent payload-reference states under the complete-port assumptions.

For the stated parameters, `8eta D^2=gamma/8`. The additive terms per round are bounded respectively by epsilon/16, epsilon/8 and epsilon/64. Since `1/(1-gamma/8)<=8/7`, their Bell-loss total is exactly bounded by

`(3/2)(8/7)(1/16+1/8+1/64)epsilon = (39/112)epsilon`.

The comparator multiplier is at most `1+gamma/7<=1+gamma`. Adding the one complete operational discrepancy epsilon/2 leaves less than epsilon total additive loss. Neither comparator perturbations nor numerical failures receive an extra free allowance.

The least power-of-two horizon gives

`N<1024 D^2 k L0/(gamma epsilon)=18432 d^5 L0/(gamma epsilon)`.

The cap counts the payload. Every probe pays its compiled exploratory general decoder, return measurement and classical update. Payload idle storage, all padded computation, local reset ancillas and precision/routing overhead remain paid. This faster source rate does not retain the slow method's cheaper measurement-only receiver.

Uniform integer i and axis j are generated by separate finite rejection samplers. Each trial succeeds with probability at least 1/2. For at most 2N draws, `R=ceil(log2(4N/nu_rng))` gives exhaustion probability at most `2N 2^{-R}<=nu_rng/2`. Exact T uses log2 N fair bits; the signs use two per possible round. Thus the stated `log2 N+N[2+R(ceil log2 D+2)]` bit cap is valid. A capped implementation couples to the ideal label process until exhaustion, then pays bounded utility loss within the single operational allowance. It is not analyzed by conditioning the regret theorem on favorable sampler records.

There is no hidden acquisition confidence event: the theorem is expected averaged terminal risk. It does not certify individual histories, future reuse or every terminal time. The supplied common CP-memory dominance promise can identify a single per-history optimal oracle on this occupation, but is not inferred by the learner. Equally informed conventional positive-loss online learners may use the same apparatus.

## 6. Independent evidence and scope

The distinct script `prequential_small_loss_statistics_check_20261028.py/.json` records:

* two rational whitening/exact-dual certificates, including a complex noncentral Choi center;
* 48 strictly positive rational played decoders and exact TP;
* 1,728 actual Born bit-event terms for six conditional channel/center pairs, including complex nonunital and pure-replacement channels;
* exact estimator mean, mean played loss and loss-dependent local second-moment checks;
* detection of bias from an independently rounded dual;
* 144 exact one-coordinate proximal certificates across 12 parameter/sign cases;
* 60 exact expected-risk, horizon and random-bit budget cases.

Floating arithmetic proposes whitening matrices only; all accepted matrix and decoder certificates are exact rational checks. The prox witnesses are exact dyadic bisection outputs. These are deterministic mathematical fixtures, not sampled acquisition, a complete bandit run, a production convex-solver implementation or hardware validation.

The proof above is direct; no fixed-loss-vector or noiseless-feedback theorem is imported from the source's COLT historical citation. The received base's terminal controls and the new main finite-prox receipt are separately pinned. No unresolved load-bearing statistical or resource objection remains within the frozen premises.
