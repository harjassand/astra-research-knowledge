# Independent audit: exact privately framed complete-error optimum

2026-10-27. Independent derivation by the receiving audit agent. This audit checks the new corollary against `DIRECT_CPTP_BURES_RISK_RECOVERY.md` and `../inverse_accuracy_bridge_20261027/joint_batch_recovery_amortization.md`; it does not re-prove or execute their imported collective dimension-reduction/purification circuits. No external upload was made.

## Verdict

**PASS, with an improvement:** the framed one-shot and collective comparator identities are exact. The expected local Bures guarantee already proves the collective near-optimal complete-error guarantee; a high-probability event, beta penalty, or confidence logarithm is unnecessary. All claims require the input frames to precede the source and the independent keys to be discarded from the compared recovered channel.

The result is an exact comparator transfer in the specified physical interface, not an unframed diamond-optimality theorem or a practical/generic-noise scalability result.

## 1. Comparator class and exact framed optimum

Let E:A→B be fixed CPTP, with dim(A)=d and maximally entangled normalized input Phi_d. Define

    a(E) = max_{D:B→A CPTP} F_e(D E).

For qubits let P be uniformly sampled from I,X,Y,Z, applied to the input before E. The receiver may choose an arbitrary CPTP D_P, and undo P afterward. Every branch is

    Ad_(P†) D_P E Ad_P.

Its entanglement fidelity is F_e(D_P E), by the Kraus expression d^(-2) sum_j |Tr K_j|² and cyclicity of trace. Hence each branch has fidelity ≤a(E), and the key-averaged channel Gamma has F_e(Gamma)≤a(E).

For every CPTP Gamma, the Bell input followed by the two-outcome measurement {Phi_d,I−Phi_d} proves

    ||Gamma−id||_diamond ≥ 2[1−F_e(Gamma)].

This is the **unhalved** diamond norm. It gives a lower bound 2[1−a(E)] even for arbitrary key-dependent recovery maps. A key-independent fidelity-optimal decoder followed by the full Pauli twirl attains it: the resulting Pauli channel has identity probability a(E); orthogonal Bell states give the matching lower bound, and a convex sum of Pauli-channel distances gives the upper bound. Therefore

    delta_frame^*(E) = 2[1−a(E)].

The equality is only for the framed model. It does not require the comparator to ignore the private key; the comparator may use it arbitrarily. Attainment uses a key-independent optimal decoder because that suffices.

Any adaptive pre-datum calibration strategy leaves a source-dependent state tau_E independent of the payload. Arbitrary joint receiver processing of tau_E with B gives an ordinary CPTP map B→A after fixing E. Thus calibration banks, adaptive source-query histories, and collective receiver work do not exceed this oracle benchmark. For M payloads the same argument yields a CPTP map B^M→A^M. It also accommodates key-dependent banks tau_(E,P). The source must be stationary/memoryless and the payload input may not bypass the stated source through an uncharged transmission path. An input encoder using extra source calls, a changed communication rate, assistance across the source boundary, or a different exposed-key output specification is a different comparator contract.

## 2. Independent SDP normalization and multiplicativity

Take Kraus operators K_alpha:A→B. A decoder Kraus operator L_beta:B→A is vectorized input first:

    |L_beta>> = sum_(b,a) (L_beta)_(a,b) |b>_B |a>_A.

Define

    w_alpha = sum_(b,a) conjugate[(K_alpha)_(b,a)] |b>_B |a>_A,
    H_E = (1/d²) sum_alpha |w_alpha><w_alpha|.

Then H_E≥0, Tr H_E=1/d, and the **unnormalized** decoder Choi matrix C_D satisfies C_D≥0 and Tr_A C_D=I_B. Direct expansion gives

    F_e(D E) = Tr(H_E C_D).

Consequently the primal/dual pair is

    maximize Tr(H_E C),        C≥0, Tr_A C=I_B;
    minimize Tr Y,             Y=Y†, Y⊗I_A≥H_E.

There is no extra factor d in either objective. In terms of the normalized source Choi state rho_AB, H_E is the fully transposed, factor-swapped rho_AB divided by d. It is not its partial transpose.

The primal has strict point I_B⊗I_A/d, and the dual has strict point tI_B for large t. The primal feasible set is compact, strong duality holds, and optima are attained. Every feasible dual Y is PSD, because Y⊗I_A≥H_E≥0.

For two sources, after harmless tensor-factor reordering, H_(E tensor F)=H_E tensor H_F. Product primal optimizers give a lower bound a(E)a(F). If A_i=Y_i⊗I_(A_i) are dual optimizers, then A_i≥H_i≥0, so

    A_1⊗A_2−H_1⊗H_2
      = (A_1−H_1)⊗A_2 + H_1⊗(A_2−H_2) ≥0.

Therefore Y_1⊗Y_2 is feasible for the product dual and its objective is a(E)a(F). This proves

    a(E tensor F)=a(E)a(F),
    a(E^tensor M)=a(E)^M.

The upper bound is over **all collective CPTP decoders**, not product decoders alone. Independent product Pauli frames form the full M-qubit Pauli twirl, so

    delta_frame,M^*(E) = 2[1−a(E)^M].

No claim about quantum capacity, block encoding, or varying code rate follows from this fixed-input/full-logical-system recovery identity.

## 3. Expected-risk transfer is enough

For the exact-reference joint-frame learner, let U denote the virtual common frame and h its training record. For fixed U,h define

    f_(U,h) = F_e(D_h E_U),    a=a(E).

Support restriction/extension and unitary covariance give a(E_U)=a. Thus **pointwise** 0≤f_(U,h)≤a. The pre-datum training bank is independent of the payload conditional on U; decoder histories are independent of the newly sampled payload Pauli keys. Applying the learned decoder to all M compressed payloads gives a mixture of tensor powers, not the tensor power of an average. Private independent frames produce exactly

    delta_alg,M = 2[1−E_(U,h) f_(U,h)^M].

Suppose the expected Bures guarantee gives

    E[1−f_(U,h)] ≤ (1+gamma)(1−a)+epsilon_0,

or E[a−f_(U,h)]≤gamma(1−a)+epsilon_0. For every f≤a,

    a^M−f^M ≤ M a^(M−1)(a−f).

Also M a^(M−1)(1−a)≤1−a^M, because the right side is (1−a) sum_(j=0)^(M−1) a^j and each summand is ≥a^(M−1). Taking expectations therefore yields

    a^M−E f^M ≤ gamma(1−a^M)+M epsilon_0,
    delta_alg,M ≤ (1+gamma) delta_frame,M^* + 2M epsilon_0.

The sharper additive multiplier is actually 2M a^(M−1), but M is the known uniform bound. There is no beta term. This argument uses nonnegative local regret a−f and does not incorrectly assert that averaged payload errors are independent.

Set epsilon_0=epsilon/(4M). Allocate total actual-versus-exact-reference **batch diamond** error zeta≤epsilon/2. The resulting actual recovered channel obeys

    delta_actual,M ≤ (1+gamma) delta_frame,M^* + epsilon.

The direct Bures rate supplies N=O(R² M log(2R)/(gamma epsilon)) calibration calls. No confidence logarithm in epsilon or M is required by this expected-risk route. The source cap includes all training outputs and is in addition to M payload calls; validation, if used, costs extra. Single-block training/reduction errors count once, while M uses of the compiled decoder and all M input/output frame implementations must fit the total zeta budget. Per-operation accuracies can shrink with M, affecting processing/precision, not the stated copy exponent.

## 4. What must remain explicit

- All payload frames are applied **before** their E calls; output-only twirling cannot simulate this interface.
- Keys are private and discarded. The guarantee is not for a channel that releases the key as an extra classical output, nor for every key-conditioned channel.
- The virtual Haar U is only a decomposition of the joint reduction, not an exposed record. Approximate joint reduction is transferred in diamond norm at the averaged batch-channel level; one cannot simply claim the same latent U law holds literally for the actual circuit.
- Training and payloads enter one joint reduction. The quantum bank is consumed. A future independently reduced datum is not in the learned frame.
- Every learned decoder must be a bona fide CPTP map, including finite arithmetic/synthesis; otherwise f≤a cannot be used. The base document supplies a feasible decoder construction and separate implementation budget.
- The bound compares with a known-source oracle over all collective physical decoders. An equally informed conventional method is allowed exactly the same inputs, quantum storage, joint reduction, tomography, private frame controls, and adaptive decisions. Indeed the present learner is a conventional reduced-frame Bures tomography plus decoder-SDP method. This corollary is not evidence of an advantage over that alternative.
- The exact identity improves the earlier benchmark 2M ell_opt to the actual framed optimum 2[1−(1−ell_opt)^M]. It does not remove intrinsic noise, generic rank growth, memory/latency cost, or physical gate errors.

## 5. Preserved scope counterexample

For a fixed residual coherent qubit error U_theta=diag(exp(−i theta),exp(i theta)),

    F_e(Ad_Utheta)=cos²(theta),
    privately twirled diamond=2sin²(theta),
    unframed diamond=2|sin(theta)|.

At theta=0.12 these are approximately 0.028662 versus 0.239424. If the Pauli key is flagged at the output, input |+> has trace distance 2|sin(theta)| in every branch (the branches are U_theta or U_(−theta)); the block-diagonal flagged output retains the larger distance. Thus the linear private-key identity cannot be exported to exposed keys or fixed unframed decoded channels. This is a scope counterexample for a fixed residual channel, **not** a claim that the oracle optimum for a known unitary source is nonzero: an oracle can invert that source.

## 6. Reproducible checks and limits

`private_framed_independent_checks.py` independently checks:

1. Random-channel Kraus versus positive-SDP objective normalization, trace normalization, and decoder TP, in output dimensions 2,3,4.
2. Fidelity invariance under key-conjugation and Bell-diagonalization under Pauli twirling.
3. Exact rational primal/dual certificates for three Pauli-channel examples, tensorized to two and three uses.
4. 606 latent-mixture/scalar cases for the expected-regret transfer.
5. The explicit coherent-residual/private-versus-exposed-key counterexample.

Run result: PASS; maximum objective/TP/trace residual below 9.8e−16, twirl off-diagonal residual below 1.1e−16, maximum scalar inequality excess below 3.7e−16. Rational Pauli certificates are exact; the other tests are floating checks only. The general conclusions rest on the arguments above, not on a solver status or these finite experiments.

## 7. Final author-text receiving and stronger boundary check

The completed `PRIVATE_FRAMED_COMPLETE_OPTIMALITY.md` was read in full. Its explicit copy cap and precision constants check: n=30720 D[log(2D)+1]M/(gamma epsilon) makes the two mixed root-infidelity contributions at most gamma epsilon/(768M) each, hence m≤gamma epsilon/(384M). Together with eta≤gamma epsilon/(32M), the ideal local additive loss is epsilon/(4M). Multiplication by 2M spends epsilon/2, leaving total batch implementation diamond error epsilon/2. The final document correctly uses the exact-reference shared-frame identity and transfers approximate implementation only afterward.

Its additional **amplitude-damping counterexample to equality of the optimized unframed and framed benchmarks is valid**. With t=sqrt(1−p) in (0,1),

    H=(|00+t11><00+t11|+p|01><01|)/4,
    Y=diag((1+t)/4,t(1+t)/4),
    a=(1+t)^2/4.

The dual slack has spectrum 0,t/2,t(1+t)/4,t(1+t)/4 and kernel span{00+11}. Thus the only fidelity-optimal feasible decoder Choi matrix is the identity decoder. Its unframed diamond error is at least 2p, whereas

    2p−2(1−a)=(1−t)(1+3t)/2>0.

Any unframed decoder attaining the framed lower bound would have to attain optimal fidelity and hence be the identity, a contradiction. Compactness makes the optimized gap strictly positive. This does not rely on finding the exact optimized unframed error. The independent script now checks the symbolic slack, nullspace, objectives, and strict-gap factorization. This strengthens the earlier fixed-residual example without changing the private-framing theorem.

Receiving verdict for the inspected final author text: **PASS**. Established historical SDP/twirling structure is acknowledged rather than claimed novel. The scientific improvement is exactly the operational comparator transfer and collective near-optimal guarantee under the paid private-framing and one-block quantum-memory interface.

### Author-check replay

The author script `private_framed_checks.py` was inspected and independently rerun after the final proof was available. Result: PASS with the matching proof hash. Coverage: 54 Choi-normalization cases, 24 one-/two-qubit twirls, three nontrivial receiver-dimension tensor reorder/positive-dual checks, exact rational amplitude-damping and two-copy certificates, 3,360 scalar mixture cases, 36 **floating numerical** finite-budget checks, and the exposed-key Bell test. The exact algebraic proof, not floating budget tests, establishes the allocation inequalities. No additional issue was found.
