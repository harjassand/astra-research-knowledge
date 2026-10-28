# Independent review: finite small-loss decoder bandit

28 October 2026. Auditor: `producer-workspace/review_prequential_memory_recovery`.

**PASS / received at its stated averaged, privately timed, one-shot terminal-service scope.** Source: `ordinary_prequential_small_loss_decoder_bandit_20261028.md`, SHA-256 `6edb6a3af1118947c1a864113a24d77eef437386eafb7d8694a4aa651dc8d1dc`. This is a new learning apparatus and a new all-probe occupation law. The accepted slow source and its receipt remain unchanged. No new source samples, production convex-solver run, sampled learning trajectory or hardware execution occurred in this review.

## 1. Actual positive feedback and its conditional law

After a physical decoder with normalized Choi matrix C is fixed, the actual mismatch measurement has probability

`q(C)=(1/6)sum_(j,s) Tr[Pi_(j,-s) D_C(r_(j,s))] = d Tr(C T)`.

The transpose and normalization in T are correct. T is positive; q lies in `[0,1]` on the entire feasible Choi set because it is an actual binary event probability. The exact six-state identity gives `q=(2/3)(1-F_e)` for every TP qubit channel, including nonunital channels. No microscopic error variable, learned T matrix or noiseless expected loss is provided to the algorithm: the acquired outcome is the actual integer bit y.

For the new instrument, the preceding record includes past exploratory decoder choices, preparation labels and actual return outcomes. It conditions a genuine retained quantum memory state. Because the **current** decoder and fresh input labels are private until the source's complete current map is fixed/executed, the channel E_(t,h) does not depend on current exploration coins except through the prescribed physical logical input. This permits conditional affine-loss learning without iid observations or a reset. Subsequent conditioning of memory can depend on the entire actual decoder-return instrument; it is not replaced with the old physical-Pauli instrument.

## 2. Affine geometry, exact rational exploration and the noisy-bit variance

There are `D=3d^2` independent tangent coordinates. The Pauli matrices `E_a` have zero output partial trace and Gram matrix `k I`, where `k=2d`. Thus all TP Choi differences are represented and coordinate diameter is at most `sqrt(2/k)<=1`. At a positive rational center, the log-det gradient and Hessian are rational and the Hessian identity in (4) follows by conjugation with `C^(-1/2)`.

A certified rational V with `(1/2)I<=V^T H V<=I` gives each played perturbation local norm at most `1/2`; hence `Cplay>=C/2>0` and exact TP. The two signs average to the **center** but each actually executed decoder is separately physical. The inverse dual must be `V^(-T)` exactly, as specified; separately rounding it would spoil exact unbiasedness.

Writing `u_i=V^(-T)e_i`, the actual two-sign difference gives

`E[2D y z u_i | h] = sum_i u_i v_i^T l = l`.

The variance calculation correctly retains `y^2=y`, not `q^2`:

`||ghat||_(H^-1)^2 =4D^2 y e_i^T(V^T H V)^(-1)e_i <=8D^2 y`.

This remains valid for arbitrary adaptive conditional source memory. Both the exploration average and the inverse-metric equality are exact; there is no additional bias term from rational whitening.

## 3. Direct approximate mirror descent is sufficient

Let `e=eta ghat+grad R(new)-grad R(old)`. The exact residual certificate and coordinate diameter imply `|<e,theta_new-theta_*>|<=delta`. The Bregman three-point identity then gives (11) with the displayed sign and negative `B(new,old)` term.

The guarded displacement has conjugated eigenvalues in `[-1/2,1/2]`. The scalar bound `x-log(1+x)>=x^2/3` on that interval implies `B(new,old)>=r^2/3`. Cauchy–Schwarz and `ar-r^2/3<=3a^2/4<=a^2` give the pathwise inequality (12). This proof needs neither ideal FTRL nor an unproved extension of a fixed-loss-vector bandit theorem.

For `C_*=(1-zeta)C_D+zeta C0`, every eigenvalue of `k C_*` is at least zeta, and the center's affine linear Bregman term vanishes. Therefore `B(C_*,C0)<=k log(1/zeta)`. Affine loss smoothing costs at most zeta per round. Predictability of the center, conditional unbiasedness and the variance bound yield

`(1-8 eta D^2) L <= E sum q_t(C_D)+zeta N+k log(1/zeta)/eta+N delta/eta`.

It is important that the residual allowance is charged every round, even though a zero bit permits a literal zero update. It is equally important that the observed bit is **not** replaced by its mean inside the adaptive learning rule.

## 4. Finite whitening, a real finite prox construction, and bit bounds

### Whitening

Trace-one positivity gives `k I<=H<=k mu^(-2)I`. For an exact Cholesky factor `H=R^T R`, the target `(3/4)R^-1` has whitened Gram matrix `(9/16)I`. Entrywise error at most `mu/(128kD)` gives weighted operator error at most `1/(128 sqrt(k))`; hence its squared singular values remain strictly inside `[1/2,1]`. Rational exact PSD tests certify this interval. Known spectral bounds permit bounded-precision Cholesky/inverse arithmetic with polynomial bit size; exact eigenbasis alignment is unnecessary. The exact rational inverse dual also has polynomial bit size by standard determinant/minor bounds.

### Existence and location of the exact prox point

The unrestricted positive-TP proximal objective is strictly convex, has a unique minimizer, and diverges at the boundary of the compact Choi set. For its displacement with conjugated eigenvalues x_b, stationarity yields

`sum_b x_b^2/(1+x_b) <= a r_*`,

while `x_b<=r_*` gives the lower bound `r_*^2/(1+r_*)`. For a nonzero displacement this implies `r_*<=a/(1-a)`. The pathwise estimator bound and chosen eta give `a<=sqrt(8)/(64D)<1/16`, so `r_*<=1/15`. Thus the exact minimizer is strictly inside `C_t/2<=C<=3C_t/2` with a substantial relative margin. The box is not an unearned restriction on the desired optimum.

### Objective tolerance and rational rounding

The Hessian on the box is at least `k I` and at most `L I`, `L=4k/mu^2`. A feasible weak minimizer with the displayed objective error has distance at most

`sqrt(2 tau_obj/k) <= delta mu^2/(32 sqrt(2) k)`.

Its gradient error is therefore at most `delta/(8 sqrt(2))<delta/4`. Rounding coordinates to the stated fixed dyadic mesh adds at most `sqrt(D)u` in Euclidean norm and at most `sqrt(kD)u/mu<1/64` in the old local norm. The objective-error displacement adds at most `delta mu/(32 sqrt(2k))`; together with `1/15` this stays well below `1/2`. Thus the rounded point and the connecting segment remain in the matrix box, justifying the same Hessian upper bound. The rounding's gradient error is at most `delta/(32 sqrt(D))<=delta/32`. The final radius and squared residual certificates therefore have ample slack.

TP holds exactly by affine coordinates; the radius guard gives positivity. Zero outcomes can retain the center exactly. Every updated center returns to a prescribed grid, so inverse/determinant arithmetic does not recursively grow the center's denominator without control.

### Why the finite solve does not cost polynomial in 1/mu

The generated bound `mu=2^(-(N+2))/k` follows by halving from the replacement center, including played decoders and the solve box. It is a **learner-generated** numerical bound, not a source spectrum premise. Its reciprocal can be exponential, but its binary representation has only O(N+log d) bits.

The box has a known rational interior center, a Euclidean interior ball with radius bounded below by a constant times `mu/sqrt(k)`, and a bounded outer radius. Exact rational PSD separation is available. On this domain, rational inverse/traces provide exact gradients; bounded-precision logarithms of positive rational determinants provide objective values. The gradient magnitude and objective range have bounds whose logarithms are polynomial in N, D and the rational input precision. In particular `||ghat||_2<=2D sqrt(2k)/mu` is sufficient for a known bound; it does not introduce an inverse-mu iteration count. Standard rational ellipsoid/value-subgradient weak optimization therefore achieves the stated objective tolerance with polynomial **bit** complexity in those quantities. Its tolerance, oracle precision and inner-radius logarithms all require polynomially many bits.

This is a valid finite algorithmic existence/cap argument with exact output certificates, not a demonstrated implementation of a production ellipsoid solver. Rational parameter description length remains part of the input-precision bill expressly stated in §6. A failed numerical certificate is not a new small-probability statistical event and cannot inherit regret for free.

## 5. Actual terminal channel and the comparator boundary

The previous accepted complete-port transfer applies to **any fixed actual probe instrument**, including these synthesized exploratory decoders and return measurements. Conditional on `T=t`, the first `t-1` histories have the law of this new all-probe process. The full stored QR state is still product with conditional source memory. Fresh current `(i,z)` is sampled and its physical decoder frozen before the call; at the terminal slot that decoder is actually applied to the unknown payload. There is no terminal mismatch measurement or update.

The averaged payload channel is the mixture of these actual conditional source/played-decoder compositions. It remains an equality after tensoring an arbitrary reference. Averaging current exploration gives the center channel by linearity, so its Bell loss is exactly `(3/2)L/N`; this does not falsely assert that the center was itself executed on the payload.

The complete source port/map, hidden current role/decoder, padded timing/routing, full initial QR product, trusted storage and isolated terminal output remain essential. Matching input marginals alone would not suffice. No post-payload memory-equivalence or future prediction is used.

The benchmark is a **fixed** decoder evaluated on this algorithm's actual expected all-probe occupation. It is not the old Pauli-learner occupation, a per-path hindsight minimizer, or a history distribution generated by another earlier control policy. Under the previously received CP-memory dominance family, the same fixed inverse-unitary/gauge-trace decoder remains pointwise optimal on every new conditional memory state. Thus the strong per-history full-CPTP oracle corollary transfers without changing its proof or gaining access to source memory.

## 6. Constants, resources and scope

With the stated N, the three additive terms per round are at most `epsilon/16`, `epsilon/8`, and `epsilon/64`. Also `8 eta D^2=gamma/8`, and `1/(1-gamma/8)<=1+gamma/7<=1+gamma`. Thus the terminal additive constant is

`(3/2)(8/7)(1/16+1/8+1/64)=39/112`.

The power-of-two cap is `N<1024D^2 k L0/(gamma epsilon)=18432 d^5 L0/(gamma epsilon)`. It includes the single payload; this is not N training calls plus an uncharged service call. Adding one complete ideal-versus-implemented process discrepancy at most `epsilon/2` leaves additive error `95 epsilon/112<epsilon`, against the declared ideal occupation benchmark. The accepted common-interface convention must be retained; replacing the benchmark by a separately perturbed process would require paying its difference too.

The improved epsilon dependence has a real control cost: **every probe** receives a general CPTP decoder, dense synthesis and a return measurement. The accepted Kraus/environment/unitary bounds and two added reset qubits still apply, but now every potential round is charged. Finite whitening/prox computation, O(N)-bit conditioning precision, repeated compilation, padded schedules and trusted payload idle storage are all included. The source-call result is not a practical runtime or favorable memory-coherence claim.

Both integer samplers succeed with probability at least one half; the finite caps and union bound give total failure at most `2N 2^-R<=nu_rng/2`. The stated bit count includes both signs and all potential rounds. Aborts, trusted compilation and storage errors belong to one whole-process allowance; no iid confidence event is inserted.

## 7. Independent exact evidence and limitations

`ordinary_prequential_small_loss_bandit_independent_check_20261028.py` was written independently and uses no author's fixture code. Its successful JSON records:

* A complex rational noncentral Choi matrix and exact rational Hessian; rational LDL and integer-square-root approximations construct a nonorthogonal dyadic V. Exact rational strict-PSD tests certify both sides of the whitening interval, and the exact inverse dual obeys the metric identity.
* 288 individual actual six-state decoder-return probability laws across two coherent, noncommuting conditional memories. The second memory is produced by an actual exploratory-decoder return-mismatch instrument, not a reset or a guessed hidden state.
* Two exact conditional estimator means and two loss-weighted second-moment bounds. This includes the physical output decoding and measurement probabilities, not merely substitution of an analytic loss into an abstract estimator.
* Two nonzero actual-gradient mirror steps obtained by **exact rational bisection**, with exact TP/PSD, local-radius and tangent-stationarity certificates. Their residual squared is about `6.10e-49`, below the required `1.80e-13`; no floating prox proposal is used in these checks.
* Exact checks of `39/112` and the source-cap coefficient 18432.

The bisection examples are commuting one-coordinate fixtures, not a generic ellipsoid implementation. These deterministic matrix checks are not source samples, a learning-performance pilot, empirical runtime evidence or hardware validation. The universal result is justified by the mathematical review above.

## Verdict

No unresolved load-bearing objection remains for the frozen candidate. Receive it as a fully specified finite positive-loss decoder-bandit **construction theorem**, yielding multiplicative-plus-additive expected Bell risk for one privately timed terminal payload on its own actual non-reset occupation law, under the stated structural/privacy/implementation contracts. Do not promote it to per-history confidence, reusable future service, counterfactual-policy regret, iid state acquisition, unknown encoder/patch discovery, an executed acquisition result, or an advantage over the equally informed conventional learner that can use the same apparatus.
