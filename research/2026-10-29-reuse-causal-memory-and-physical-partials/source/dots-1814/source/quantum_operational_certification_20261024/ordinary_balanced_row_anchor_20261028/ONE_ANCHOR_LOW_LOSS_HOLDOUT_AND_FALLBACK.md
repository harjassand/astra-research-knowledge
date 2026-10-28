# A complementary one-anchor low-loss holdout fast path

28 October 2026. **New author construction; independent receiving pending.** The acquired/automatic row fast path is already received and is not changed or weakened here. This note combines received fixed-encoder recovery, an elementary fresh six-state holdout, and the received generic fallback. It claims a complementary sufficient condition for fast completion, not a new generic rank-squared global learner or a new fixed-encoder recovery primitive.

## 1. Result, resources, and the distinction from the row route

Keep the stationary/reset ordinary-source and fixed four-real-coordinate isometric encoder family. Let

    ell(x,D)=1-F_e(D E_x),
    ell_*=min_(x,D CPTP) ell(x,D),
    ell_0=min_(D CPTP) ell(x0,D),

where x0 is ONE predetermined implementable encoder, e.g. a coordinate anchor. No useful decoder, low-loss promise, row structure, row balance, flags, source spectral floor, or microscopic noise description is supplied. All candidate decoders are full CPTP maps, including on unsuccessful learner records.

There are two permitted output interfaces:

1. An actual known k-dimensional output register, using its identity frame.
2. The received causal common-frame processor, retained over the WHOLE prescribed finite experiment. A valid uniform encoded-Choi rank bound R gives common output dimension k<=min(s,8R), and actual loss-density rank r<=min(2k,3R). The same one mathematical frame U is used for training, holdout, fallback if needed, and payload. Its complete arbitrary-operator adaptive law and finite compiler are received imports, not a reset of its physical memory.

The fast condition here is basis-invariant, so unlike the row condition it can use interface 2 without assuming that a random frame preserves any special diagonal geometry. In interface 1 use any supplied valid loss-state rank bound r, or r=2k.

For 0<gamma,epsilon<=1, the procedure has actual private-framed one-payload unhalved complete error

    Delta_actual <= min{2,(1+gamma)2 ell_*+epsilon}.       (1)

Its deterministic worst-case source cap is

    O_tilde(k^4/(gamma epsilon))+1.                     (2)

If the chosen anchor happens to satisfy

    ell_0 <= epsilon/2^14,                              (3)

then with actual probability at least 1-3epsilon/1024 it instead completes after

    O_tilde((dr+1)/epsilon)+1, d=2k,                   (4)

ordinary calls. In the paid rank-compressed interface this is O_tilde(R^2/epsilon)+1. The fast bill has NO inverse-gamma factor. Perfect recovery at this single encoder is sufficient, including perfectly recoverable mixed-spectator channels. One need not learn a global encoder landscape when an actual tested policy is already absolutely good.

Condition (3) is needed for the stated fast-completion guarantee, not for soundness. Mere existence of a good encoder elsewhere does not imply that this one-anchor route accepts. The algorithm tests only x0 before fallback; it does not discover all useful x. Conversely the received row route can globally optimize sources with large ell_0 or large ell_*; it does not need a near-perfect seed. These are different sufficient mechanisms.

## 2. One fixed-encoder acquisition, followed by a fresh decoder test

Declare all maxima before data. Put

    m=epsilon/2^18, eta=epsilon/2^16,
    beta_train=beta_test=epsilon/1024,
    D0=nextpow2(dr),
    n_train=ceil[(80D0/m) log(12D0/beta_train)].          (5)

Conservative integer upper logarithms are permitted. Acquire n_train actual ordinary loss densities T_(x0) and run the received Bures matrix query. The estimate tau is a physical normalized density. Minimize (3/2)Tr(C^T tau) over full-CPTP decoder Choi matrices C, with deterministic objective debit eta and finite physical feasibility/synthesis as in the received known-coefficient decoder contract. On any explicit numerical failure return a fixed replacement CPTP decoder; do not output a nonphysical matrix.

The loss-density preparation is the ordinary six-state mixture

    T_x=(1/6) sum_l E_x(P_l) tensor (I-P_l)^T,

with receiver-local anti-state register and the label discarded for this bank. There is no source-entangled input or retained sender reference. Its root-fidelity guarantee is 1-f(T_(x0),tau)<=m except beta_train, conditional on each ideal common U and any earlier allowed history.

Freeze the resulting classical finite description of D_hat. On each of n_test NEW ordinary source calls, draw a uniformly random one of the six Pauli eigenstates P_l, send it through E_(x0), apply D_hat, and measure {P_l,I-P_l}. Record failure Y=1 for the latter outcome. This consumes fresh ancillas and fresh source calls, not copies of an unknown quantum decoder program. Labels are used for this holdout measurement, then remain private. Set

    a=epsilon/192,
    n_test=ceil[(768/epsilon) log(1/beta_test)].          (6)

Accept the fast decoder if the integer failure count K satisfies K<=floor(n_test a). On rejection run the received generic clipped learner on COMPLETELY FRESH calls at local parameters (gamma/2,epsilon/128), in the same identity or retained causal frame. All calibration, including fallback, precedes the unknown payload. No early history is reused as fresh training data.

Only one fixed encoder setting is used by the entire fast route. The six logical probe states and the receiver-local controls are, of course, separately paid settings. The generic fallback retains its independently paid encoder queries.

## 3. The observable holdout mean and its two uniform tails

For any TP qubit channel Lambda, the six-state 2-design identity gives

    (1/6)sum_l Tr[P_l Lambda(P_l)]=(1+2F_e(Lambda))/3.

Thus, conditional on every frozen training history (and U in interface 2), the holdout samples are iid Bernoulli with

    p=E Y=(2/3)ell(x0,D_hat).                           (7)

The common-frame statement is a consequence of the received adaptive arbitrary-operator law. It is not an assertion that the evolving physical frame memory independently resets. Integration over U and the training histories is performed only after applying the conditional bound.

If the actual ideal decoder loss exceeds epsilon/64, then p>epsilon/96=2a. The multiplicative lower-tail estimate gives

    Pr(accept | frozen history) <= exp(-n_test p/8)
                                <= exp(-n_test epsilon/768)
                                <= beta_test.          (8)

If the loss is at most epsilon/1024, then p<=epsilon/1536=a/8. For lambda=log 2, the Bernoulli moment-generating function obeys E exp(lambda Y)=1+p<=exp(p). Therefore

    Pr(reject | frozen history)
       <= exp[-n_test a(log 2-1/8)]
       <= exp(-n_test a/2) <= beta_test.                (9)

Here log 2>=5/8, and the integer acceptance threshold is harmless: rejection K>floor(n_test a) implies K>n_test a. Equations (8)-(9) control unconditional masses after averaging; neither divides by the probability of acceptance. A publicly exposed accepted record has not been certified to have conditional loss epsilon/64.

The holdout soundness is independent of whether the tomography bank or optimizer succeeded. Consequently its beta_train failure budget is NOT additionally charged in the all-source risk proof below. Training quality is used only to prove fast completion.

## 4. All-source risk with a fresh fallback

Let A be acceptance. Equation (8), valid on every frozen history, gives

    Pr(A and ell_fast>epsilon/64)<=beta_test.

All decoders are physical, so loss is in [0,1]. The accepted contribution is at most Pr(A)epsilon/64+beta_test. Conditional on every prior rejected record, the fresh generic learner has ideal expected loss at most (1+gamma/2)ell_*+epsilon/128. Hence

    E ell_selected
      <=Pr(A)epsilon/64+Pr(not A)[(1+gamma/2)ell_*+epsilon/128]
          +beta_test
      <=(1+gamma/2)ell_*+17epsilon/1024.               (10)

The only global fact needed on the accepted branch is ell_*>=0. This is why absolute near-perfect recovery supplies a global additive guarantee without learning a surrogate for all encoders.

Private independent Pauli framing of the unknown payload makes the ideal averaged unhalved complete error exactly 2 E ell_selected. Allocate one WHOLE-process discrepancy at most epsilon/2, including the full frame, all source/preparation controls, finite sampling/estimation/arithmetic, holdout measurements, selected decoder, possible fallback and payload framing. Then

    Delta_actual <= (1+gamma/2)2ell_*+17epsilon/512+epsilon/2
                 <=(1+gamma)2ell_*+epsilon.

The compared records, private keys, internal memory and calibration are discarded from the tested logical channel. This does not prove correctness conditioned on exposed records or make a claimed unframed diamond-error estimate linear in Bell loss.

## 5. Why the near-perfect anchor finishes quickly

The received full-decoder root-risk transfer on the good bank gives

    sqrt(ell_fast)<=sqrt(ell_0)+2sqrt(6m)+sqrt(eta).      (11)

Indeed each fixed decoder objective changes in square root by at most sqrt(6m), and the eta-inexact surrogate minimizer adds at most sqrt(eta). Under (3)-(5), using sqrt(6)<5/2,

    sqrt(ell_fast)<(11/512)sqrt(epsilon),
    ell_fast<121epsilon/2^18<epsilon/1024.               (12)

The ideal probability of failing to accept is thus at most beta_train+beta_test=epsilon/512. The ideal event estimate is not silently reused for finite controls: reserve predecision record-channel discrepancy

    nu_pre<=epsilon/1024

INSIDE the whole epsilon/2 allowance. This covers the entire training, known-decoder compilation and holdout decision instrument, with its branch record retained in the comparison. Actual fast-completion failure is therefore at most 3epsilon/1024<epsilon/256. This debit is not added again outside the final risk budget.

The cap (5) is O_tilde(dr/epsilon), and (6) is O_tilde(1/epsilon). The maximum permitted experiment reserves these calls PLUS the fresh generic fallback and one payload; all finite control and memory precision is fixed against that maximum, not retroactively chosen after early acceptance. Rejection need not physically consume the unused fast payload or acceptance consume the fallback. This is an instance-sensitive HIGH-PROBABILITY actual bill, not a smaller generic deterministic cap or an expected-stopping-time replacement.

For interface 2, define the common support using the entire encoder family before data, not only x0. The common frame then remains valid even when fallback visits other encoders. Its k<=8R support argument and compiler are already accepted. Near-correctability and (7) are invariant under its unknown common U, so no structural-basis inference is required.

## 6. Exact physical separation from rank-one row structure

Let the physical sender space be C^2 tensor C^4 in logical-first order, and use the known linear isometry

    V_x|0>=(x,0), V_x|1>=(0,x), x in S^3.

Let O be the real 4-by-4 block diagonal matrix consisting of two 60-degree rotations. Every row o_s of O has unit norm and e_s^T o_s=1/2. Define the (potentially unknown) physical unitary source

    W=(1/sqrt(2)) [[I_4,O],[I_4,-O]].                   (13)

Orthogonality of O proves W^*W=I_8. Every E_x(rho)=W V_x rho V_x^* W^* is an isometric channel. Its optimal Bell loss is zero at EVERY x. Recovery by the inverse isometry on its two-dimensional range, with any CPTP extension on the complement, proves this mathematical fact; that inverse is not supplied to the learner.

For output b=(s,t), t=+ or -, the two encoded amplitudes are x_s/sqrt(2) and t(o_s^T x)/sqrt(2). Since the actual ordinary loss density is

    T_x=[2 rho_bar,x tensor I_2-J_x]/3,

its two reference-coordinate diagonal quadratic effects are

    B_(s,t,0)=(1/12)e_s e_s^T+(1/6)o_s o_s^T,
    B_(s,t,1)=(1/6)e_s e_s^T+(1/12)o_s o_s^T.           (14)

There are sixteen effects. Each has rank TWO, trace 1/4, and nonzero eigenvalues

    lambda_+=(3+sqrt(3))/24,
    lambda_-=(3-sqrt(3))/24.                            (15)

To verify (15), use tr B=1/4 and the nonzero-eigenvalue product (1/12)(1/6)(1-(1/2)^2)=1/96. Also sum_i B_i=I_4, as normalization requires. Their total best-rank-one trace tail is exactly

    tau_row=sum_i[Tr B_i-lambda_max(B_i)]
           =16 lambda_-=2-2/sqrt(3)>0.                 (16)

Thus the exact-row hypothesis fails, and the approximation-tail oracle cannot have a vanishing target-accuracy penalty at this fixed tail. Nevertheless the one-anchor low-loss route has its fast-completion guarantee for every chosen x0.

This does NOT assert that the received residual-validation row algorithm can never accidentally accept such a source; that is a different statement about its learned predictors and thresholds. The proven separation is between sufficient subclass hypotheses, not an impossibility for all row-based attempts.

The example also admits a mixed-spectator strengthening. Append a fixed spectator state sigma to the source output. In a tensor basis diagonalizing sigma, each effect in (14) is multiplied by one spectator eigenvalue; their total tail remains (16). Tracing the spectator and applying the mathematical inverse still gives perfect recovery. Its normalized encoded Choi purity is Tr sigma^2, so Choi impurity need not vanish. This is an explicit family of perfect mixed-spectator anchors, not just a pure-Choi special case. The learner is not supplied sigma, its eigenbasis, or W.

## 7. Imports, evidence, and boundaries

Frozen import hashes and their receiving files are in `one_anchor_low_loss_source_bindings.json`. The scientific imports are:

- `ordinary_bures_matrix_query_confidence_20261027.md`: actual ordinary loss density, rank, finite high-probability Bures bank and whole-decoder root-risk transfer.
- `direct_cptp_bures_bridge_20261027/DIRECT_CPTP_BURES_RISK_RECOVERY.md` and its independent receipt: the six-state identity, finite full-CPTP optimization/control and Bures estimator foundations.
- `explicit_online_random_dimension_reduction_compiler_20261027.md` and its independent receipt: OPTIONAL retained common-frame interface and its arbitrary-operator finite horizon.
- `ordinary_generic_matrix_gls_sylvester_clipping_20261028.md` and its independent receipt: fresh generic fallback with its all-history cap and ideal averaged-risk contract.
- `direct_cptp_bures_bridge_20261027/PRIVATE_FRAMED_COMPLETE_OPTIMALITY.md` and its receipt: the exact private-frame comparator.

The new checks establish algebraic fixture identities, exact scalar risk/budget inequalities, deterministic physical six-probe expectations, and binomial tails. They do not execute the quantum Bures acquisition, a production SDP, the common-frame circuit, or hardware. No source trial outcomes are sampled. The construction and all its new checks remain UNREVIEWED until independently received. No historical priority, external peer review, practical runtime, generic fast acceptance, or advantage over an equally informed conventional learner is claimed.
