# Independent review: common-stationary CQ calibration robustness

## Source and verdict

PASS as a finite-rate, complete CQ controlled-process perturbation theorem, conditional on the stated exact common stationary law, centering and uniform kernel-error premises. I read the complete 13,018-byte `COMMON_STATIONARY_CQ_ROBUSTNESS.md` and verified SHA-256 `467b02dac2c0b5326ce2de8356b4255c49ad1d68f081e840c11bdd024b99ac01`. No correction or additional hypothesis is needed for its displayed bounds. This review does not acquire the statistical/model premises or extend the result to quantum source coherences.

## 1. Norm and amplification

For every finite retained reference, the direct-sum trace-class norm is sum_x ||X_x||_1. A scalar matrix M acting on the label coordinate has induced norm at most its maximum absolute column sum, by the triangle inequality; this proof is unchanged by the reference dimension and applies to non-Hermitian operator tuples too. In particular stochastic maps and Pi are contractions, Delta has norm at most eta, and Q has norm at most two. The range of Q is precisely the tuples with zero operator-valued sum. Replacing this by scalar trace zero would invalidate the proof, but the source does not make that replacement.

Physical CQ channels are completely trace-norm contractive: their adjoints are unital CP maps on the corresponding direct-sum operator algebra. This remains true with retained records and references. No assertion of positivity or contractivity of Q or of the QQ propagator is used. The norm of a difference of two physical channels is at most two in this same complete CQ sense; this is not an assertion about arbitrary coherences between label basis states.

Common stationarity and column stochasticity imply both Delta Pi=0 and Pi Delta=0. These separate identities are essential to the two-sided argument. Zero entries of pi cause no division or failure: Pi is still a norm-one projection and the proof remains valid.

## 2. Acquired fast-sector decay

The telescoping difference of powers has norm at most m eta in every amplified CQ norm. On range Q, P0^m vanishes, and consequently P1^m contracts by at most 1/4; the same weaker bound holds for P0. In the maximum norm |q|_i=max_{0<=r<m}4^(r/m)||P_i^r q||, the last shifted term uses that m-step contraction. Thus |P_i q|_i<=4^(-1/m)|q|_i and ordinary-to-weighted norm comparison costs at most four, not a dimension or stationary-minimum factor.

Poissonization yields decay lambda(1-4^(-1/m)). The inequality 1-4^(-1/m)>=3/(4m) follows from concavity on 1/m in [0,1]. Common H0 commutes with the label matrices and gives an isometry even on operator-valued tuples. The perturbation bound |QVq|_i<=16b|q|_i follows from ||V||<=2b and ||Q||<=2. Hence sqrt(lambda)>=64bm leaves decay at least lambda/(2m); using beta=lambda/(4m) is conservative. The resulting S_i bound 4 exp(-beta t) is valid as an operator on range Q, regardless of full coupled-system mixing.

## 3. Correctly oriented off-sector bounds

The first variation-of-constants identity removes the Pi V Q block from the full generator. With an initial input already in range Q, the removed-block evolution is exactly S_i. Integrating the remaining coupling with physical E_i contraction gives 4 exp(-beta t)+a, a=32bm/sqrt(lambda). This is a restricted-domain estimate, not the same bound for E_i Q on arbitrary inputs.

For Q E_i on arbitrary inputs, the initial Q costs two. Centering gives QV Pi=V Pi, and ||Pi E_i||<=1; this yields 8 exp(-beta t)+a. The same value of a is valid in both estimates. There is no extra factor two on the left side of the Duhamel integrand because Delta's output already lies in range Q. This is the important constant/domain seam, and it is handled correctly.

## 4. Duhamel and constants

Applying the restricted left bound and unrestricted right bound to lambda E1(t-s) Delta E0(s) gives exactly

lambda eta [32 t exp(-beta t)+12a(1-exp(-beta t))/beta+a^2 t].

In the high-rate branch a<=1/2. The first term is bounded by (128/e)m eta, the middle by 24m eta, and the last by 1024 b^2 m^2 t eta. Since 128/e+24<72, the displayed high-rate bound is valid. In the complementary branch ordinary complete-channel Duhamel gives lambda t eta<=4096 b^2m^2t eta. The unified bound and cap at two therefore follow. Lambda=0 gives identical channels. For b=0 and positive lambda the high-rate argument has a=0 and no division by b.

The rate cancellation is substantive: a generic one-sided full-generator estimate would retain lambda T. Here the perturbation annihilates the stationary sector at both ends, while the driven Q-facing factors have leakage of order b m/sqrt(lambda). The surviving extensive term is of order eta b^2m^2 T. This argument does not require the system itself to forget its state.

## 5. Instruments and receiving scope

A common prescribed CQ-preserving instrument, with all outcomes retained, is CPTP and contractive in the same complete norm. Telescoping the p+1 physical interval channels proves the stated error eta[72(p+1)m+4096b^2m^2T], capped at two. Joint source-label/system operations need not preserve pi or the analysis norms; arbitrary CQ inputs at each interval were already covered. Adaptive operations through retained classical records are admissible at these prescribed slots. A discarded or normalized rare postselected branch is not covered by this CPTP contraction argument. Nor is an arbitrary coherent quantum operation on the label register.

An exact-model simulator can be received by adding its error only if its existing guarantee covers this same CQ input/control/output task. Interval-dependent couplings must independently satisfy the common centering and uniform b premises. The proof does not learn a clock, stationary law, interaction or uniform eta; it does not make the earlier exact affine model promise robust against every misspecification. Acquisition and numerical implementation costs remain separate.

## 6. Bias counterexample

The sign-refresh calculation is consistent. With initial uniform signs, the biased source has mean epsilon(1-exp(-lambda t)); integrating gives the displayed mean phase. Conditional refresh dynamics yield Cov(xi(s),xi(t))=exp(-lambda(t-s))Var(xi(s)), even though the initial distribution is not the biased stationary law. Double integration bounds Var(phi) by 8T. At T=1/128 each characteristic function is within 1/4 of the phase of its mean. Taking epsilon=64pi/sqrt(lambda) makes the biased mean phase approach pi, while the unbiased mean is zero; the resulting trace-norm separation is at least 3/2-pi/(lambda T). The qubit off-diagonal entries are f/2, so their difference indeed has trace norm |f1-f0|, without an extra factor two.

This supplies an actual family refuting a uniform O(epsilon) bound when a source bias changes the Hamiltonian mean. It violates the hypotheses of the accepted theorem and is not a counterexample to it. A scalar identity mean remains commutator-trivial.

## 7. Ordinary primary comparison and limitations

I inspected the accessible primary [Mitrophanov 2005 paper](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/26A9854BCB8D103B3A63A9B272616EC0/S0021900200001066a.pdf/sensitivity_and_convergence_of_uniformly_ergodic_markov_chains.pdf). Its classical perturbation analysis explicitly relates kernel sensitivity to convergence of iterated kernels. Thus source-only rate cancellation and mixing-based sensitivity are ordinary prior machinery, not a novelty claim here.

I also inspected [Szehr–Wolf, Theorem 6](https://arxiv.org/html/1210.1171), including its continuous-time Duhamel proof. That theorem assumes convergence of the full unperturbed semigroup to a unique stationary state and integrates a contraction envelope. The present source-plus-system need not satisfy that premise; its proof instead uses two restricted fast-sector factors. The comparison in the candidate is accurate. This does not establish that no broader ordinary semigroup, singular-perturbation or homogenization theorem subsumes the structured estimate.

No attempt was made to access the previously denied Kurtz article or an alternate copy. This is a bounded source-grounded comparison, not a priority survey. The proof is a transparent application of standard weighted-norm perturbation, variation-of-constants and CPTP telescoping techniques to the stated CQ structure.

## Final status

Accepted mathematical robustness module with no source edits. It provides a meaningful switching-rate-independent calibration bound under exact common stationarity and centered coupling, for prescribed CQ-controlled experiments with arbitrary retained quantum references. It does not provide a general quantum-source diamond bound, statistical calibration certificate, executable estimator/compiler, general misspecification guarantee, novelty assertion or practical advantage claim.
