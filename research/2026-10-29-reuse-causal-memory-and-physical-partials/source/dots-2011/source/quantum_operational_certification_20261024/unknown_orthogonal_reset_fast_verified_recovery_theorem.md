# Fast reusable recovery with a full-qutrit learned-throughput certificate

27 October 2026. Local post-cutoff assembly. Independent component receipts exist; whole assembly receiving requested. No historical novelty claim.

## Source promise and output

A stationary memoryless qutrit-input source is promised to have

 E(rho)=p V(rho tensor sigma)V*+(1-p)Tr(rho)tau,

where V, sigma, tau and p are unknown, tau V=0, rank sigma<=a supplied integer r, and p>=a supplied p0>0. The finite output dimension s is known. No nonzero eigenvalue, code basis, inverse, reset spectrum or physical whitening operation is supplied.

For target0<nu<=1 and confidence0<beta<1, the procedure below acquires a classical reusable CPTP accepted/erasure decoder and, with probability at least1-beta, a fresh full-qutrit certificate specifying the known estimated-throughput channel

 G_ahat(rho)=ahat rho+(1-ahat)Tr(rho)|erase><erase|,

such that its complete unhalved diamond error is at most nu ahat. The certified actual acceptance is at least p0/4; the classical estimate satisfies ahat>=3p0/8. On the training good event the original signal throughput p is retained up to the explicit small losses below.

All training and holdout probes are ordinary known, classically labelled, unentangled qutrit states. Receiver-side training measurements are collective, with the resource limits stated below. No calibration quantum program is consumed at deployment.

## 1. Fast actual-access training

Set d=3s and

 t=nu²p0/(10^7 r), beta_train=beta/2.

Apply the received corrected `acquired_sylvester_filtered_fast_utility_child_theorem.md`. The actual available states are labelled-two-design T=(J+3omega)/4 and omega; there are NO physical Choi J copies. Its pilot is a constant-relative estimate of T=A/4, producing known G. Fresh pairs of independent Keyl batches produce the contrast4Y_T-6Y_omega, and known Sylvester filtering followed by classical recenter-and-clip acquisition estimates H=J-3omega.

Solve the finite low-trace accepted-decoder SDP to a FEASIBLE solution with additive objective gap kappa<=rt. This finite tolerance is charged, not treated as free exact optimization. The received localization theorem gives, on a training event of probability at least1-beta_train,

 L<=140rt+2kappa<=142rt,
 L/p<=142nu²/10^7.                                   (1)

On a declared learning abort use the erasure decoder; every computed feasible SDP solution still defines a CPTP decoder on other histories.

The received utility-to-complete-error bound gives

 ||D_hat E-G_p||_diamond<=6sqrt(3pL/2)+9L<0.028nu p.  (2)

For its actual acceptance a and accepted mismatch b, the separately received SDP-to-holdout bridge gives

 b<=15L/4, |a-p|<=6L, a>=3p/4,
 q=b/a<=5L/p<=71nu²/10^6<nu²/6144.                  (3)

The deliberately coarse three-quarter acceptance bound preserves enough numerical slack. Thus the SAME fast-trained decoder meets the small-mismatch completeness premise of the learned-throughput verifier; no smaller training accuracy parameter or nu^-4/nu^-8 retraining is required.

## 2. Independent full-qutrit certification

Hold the acquired decoder fixed. Invoke `full_qutrit_holdout_learned_throughput_corollary.md` with target nu, confidence beta_hold=beta/2, and supplied ACCEPTANCE floor p0/2. This differs from the source signal floor p0 because actual a can be slightly below p.

Explicitly, the accepted-sample holdout uses

 L_hold=ln(16/beta),
 m=ceil(9216 L_hold/nu²),
 Ncap_hold=ceil(5m/(2p0)).

It uses fresh labelled qutrit2design probes until m acceptances or the cap, then the received mismatch/acceptance rule; the classical throughput estimate is ahat=m/N. The invoked actual-acceptance verifier has target nu/2. Condition (3) is exactly sufficient for its completeness.

Conditional on every good training output, the verifier certifies with probability at least1-beta_hold. Hence the entire procedure supplies a certificate with probability at least1-beta_train-beta_hold=1-beta. Soundness of an issued certificate is uniform over EVERY fixed CP accepted map, even after bad training; no bad-training event is assumed observable. Its complete guarantee targets the specified learned G_ahat, not an unobserved p or an unobserved actual a.

No guarantee is claimed on an inconclusive holdout result. Selection or retraining on the same holdout would require separately paid multiple-testing control. A certificate does not verify the hidden source decomposition or future nonstationarity.

## 3. Charged source-copy cap and accuracy exponent

In the fast acquisition set

 n0=ceil(4096d/t),
 J*=min{j:4*2^-j<=sqrt t},
 k=ceil[2048 ln(8dJ*/beta_train)].

The filtered-contrast routine has deterministic cap2J*k*n0, counting BOTH independent T and omega batches. Add the received constant-relative T pilot cap at regularization t/4, accuracy1/8 and failure beta_train/2. For example its explicit bound is

 Npilot <= (8208d/t) ceil[6400 ln(4d Kpilot/beta_train)],
 Kpilot<=ceil(log2(4/t))+2.

The existing acquisition primitive supplies the exact stage schedule and cap. Consequently the full training cap is

 O(sr/(p0 nu²) polylog(sr/(p0 nu beta))).              (4)

Holdout adds the deterministic cap Ncap_hold=O(log(1/beta)/(p0nu²)). For a fixed trained device with a>0 its expected holdout cost is at most m/a, and the received negative-binomial bound gives the same O(log(1/beta)/(a nu²)) high-probability cost. These actual-a bounds are NOT deterministic caps on every random path.

If an averaged training-channel error is also desired, replace beta_train by min{beta/2,nu p0/8}; only logarithms change, and (2) plus universal bad-event distance2 gives an averaged bound below nu p. This is a statement about the trained decoder before conditioning on its subsequent holdout outcome, not an uncharged postselection guarantee.

## 4. Physical and computational resource contract

Every n0-copy PSW batch is a collective measurement on n0 physical source output systems plus locally prepared known-label registers and measurement ancillas. The T and omega batches can be measured separately, but a constant-quantum-memory realization is not supplied. Source-query savings are not cheap-gate or small-quantum-memory claims.

Pelecanos--Spilecki--Wright explicitly identify general-n computational efficiency as unknown in Section1.8, item4 of their [debiased Keyl paper](https://people.eecs.berkeley.edu/~jswright/papers/debiased-keyl.pdf), with n=1 as the stated exception. That limitation was checked directly. No general-n POVM circuit synthesis is acquired by this theorem. Known G/Sylvester processing and the decoder SDP are finite-dimensional classical computations; no bit/gate complexity guarantee is asserted. Approximate POVM or deployed-instrument implementation requires its own charged error budget in addition to the explicit SDP gap kappa.

All source-dependent quantum training/holdout systems may be discarded after the classical decoder is acquired. Future deployment uses the original source once per datum plus the learned decoder, with no fresh calibration calls. Many-use joint error accumulates; the training/certificate confidence events are one-off shared events, not resampled per datum.

## 5. Scope of the improvement

Equation (4) is a nu^-2 UPPER accuracy rate for the promised exact orthogonal-reset source. It improves the received nu^-4 acquisition route but does not invalidate that earlier theorem. It does not prove a matching nu^-2 lower bound against arbitrary coherent adaptive training: unitary query subclasses may admit metrological advantages. The separately received compilation lower theorems concern fixed-relative-accuracy rank/ambient/throughput dependence and their explicitly stated source/memory regimes.

The separately received `known_erasure_flag_all_p_compilation_lower.md`
gives the distinct worst-case known-flag subclass lower

 n>=(s-1)r/[32p ln(3(s-1)/r)]

for every0<p<=1 and s>=3r+1, at fixed complete relative error1/4 and
classical post-calibration deployment. This matches rank/ambient/signal
exponents up to logarithms, not the accuracy exponent. It is not a
universal pointwise lower for each noise state. The separate
`full_ambient_reset_compilation_lower_root.md` has its own full-complement
reset information budget and must not be conflated with this all-p
revealed-flag hard subclass.

No arbitrary overlapping-reset fast theorem, unrestricted entropy recovery theorem, unassisted quantum-capacity claim, historical-priority assertion, or structural-promise certification is inferred by this exact-source assembly. Such extensions require their own received interfaces.
