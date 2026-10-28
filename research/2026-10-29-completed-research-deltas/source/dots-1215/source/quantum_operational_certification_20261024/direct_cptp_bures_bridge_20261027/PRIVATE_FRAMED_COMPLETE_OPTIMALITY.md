# Exact private-framed complete-error comparator and near-optimal batch recovery

27 October 2026. A self-contained comparator corollary of `DIRECT_CPTP_BURES_RISK_RECOVERY.md`, with the one-common-frame batch interface in `../inverse_accuracy_bridge_20261027/joint_batch_recovery_amortization.md`. The original received files and their receipts are unchanged. This is a **private pre-noise framing** theorem, not an unframed optimal-diamond recovery theorem.

## Result and operational boundary

Let E:L(C²)→L(Cˢ) be a fixed stationary memoryless CPTP source, with a supplied valid normalized-Choi-rank bound R. Write

    a=f_opt(E)=max_{D:Cˢ→C² CPTP} F_e(D E),
    ell_*=1-a,
    F_e(Λ)=<Φ_d|(id⊗Λ)(|Φ_d><Φ_d|)|Φ_d>,
    |Φ_d>=d^(-1/2) Σ_i |i i>.

All diamond norms below are **unhalved**. The payload is an arbitrary M-qubit input, possibly entangled with an arbitrary reference. Each of its M uses of E is preceded by an independent uniform Pauli P_i; after receiver decoding the matching product Pauli is undone. These keys are independent of the input, reference and calibration. The recovered channel outputs only the logical quantum systems: keys and calibration transcripts are private/ignored, not provided to its distinguisher.

Define δ^*_{frame,M}(E) as the infimum of diamond distance from id_{2^M} over this model, allowing arbitrary key-dependent physical **collective** CPTP decoders D_P:(Cˢ)^⊗M→(C²)^⊗M, arbitrary internal receiver ancillas, and arbitrary independent pre-datum calibration banks. The comparator may know E exactly. No additional encoding across uses, sender/receiver entanglement bypass, postselection, payload-adaptive extra source queries, or altered source is included.

Then, exactly,

    f_opt(E^⊗M)=a^M,
    δ^*_{frame,M}(E)=2(1-a^M).                             (A)

The ordinary-six-input Bures learner, using a single joint reduction on its acquired bank and ALL M payload outputs, achieves

    ||Λ_actual,M-id||_diamond
       ≤ min{2,(1+gamma) δ^*_{frame,M}(E)+epsilon}           (B)

for 0<gamma,epsilon≤1. A deterministic calibration source cap is

    N=6 ceil[30720 D (log(2D)+1) M/(gamma epsilon)],
    k=min(s,2R), r=min(R,k), D=2^ceil(log₂(kr)),             (C)

when s≥2. Thus N=O(R² log(2R) M/(gamma epsilon)). The M payload calls are additional: total source calls are N+M. The joint bank is consumed; this is not a reusable decoder on later, separately reduced physical data. A high-confidence training event is **not necessary**: the expected Bures guarantee suffices, so no beta failure term or log(1/epsilon) confidence-copy factor is introduced by this corollary.

For M=1 this is a near-optimal complete-error result against the exact framed comparator, with N=O(R² log(2R)/(gamma epsilon)). For s=1 the source is constant, a=1/4, and a fixed maximally mixed logical replacement on each use realizes (A) without calibration.

## 1. Two elementary complete-error identities

### 1.1 Bell-test lower bound

For any CPTP logical channel Λ on dimension d,

    ||Λ-id||_diamond ≥ 2[1-F_e(Λ)].                         (1)

Use |Φ_d><Φ_d| as an input and measure its output with the two-outcome measurement {Φ_d,I-Φ_d}. The ideal distribution is (1,0); the real distribution is (F_e,1-F_e). Its l1 distance is 2(1-F_e), which is bounded by the trace norm and hence by the diamond norm. Neither square-root fidelity nor half-diamond conventions occur here.

### 1.2 Private Pauli twirl attains the Bell-test bound

For a channel on M qubits, average

    T(Λ)=4^(-M) Σ_P Ad_{P†} Λ Ad_P,

where P ranges over all M-fold tensor Paulis modulo phase. Orthogonality of Pauli characters removes every off-diagonal process-matrix coefficient. Complete positivity makes the remaining coefficients probabilities, so

    T(Λ)=Σ_Q p_Q Ad_Q,   p_I=F_e(Λ).

The identity coefficient is unchanged because F_e is linear and invariant under simultaneous input/output unitary conjugation. For a Pauli channel, orthogonal Bell Choi states give the lower bound 2(1-p_I), while

    ||Σ_{Q≠I} p_Q(Ad_Q-id)||_diamond ≤ 2 Σ_{Q≠I}p_Q

gives the reverse inequality. Consequently

    ||T(Λ)-id||_diamond=2[1-F_e(Λ)].                        (2)

Fresh input frames are essential: output-only randomization does not implement T. These are averaged-private-key channels; conditioning on or publishing the keys does not preserve (2).

## 2. Exact one-block framed optimum, including key-dependent decoders

Fix any CPTP source F on a d=2^M logical block. For a key-dependent decoder family, the averaged logical channel is

    Γ=4^(-M) Σ_P Ad_{P†} D_P F Ad_P.

For every P,

    F_e(Ad_{P†} D_P F Ad_P)=F_e(D_P F)≤f_opt(F).

One direct verification uses the Kraus formula F_e(Λ)=d^(-2)Σ_j|Tr L_j|²: conjugating every L_j by P does not change its trace. Linearity therefore gives F_e(Γ)≤f_opt(F), and (1) implies

    ||Γ-id||_diamond≥2[1-f_opt(F)].                         (3)

The averaged channel need not itself be Pauli if D_P varies with P; the lower bound does not assume that it is. Conversely choose an optimal fixed decoder D*, independent of P. The finite-dimensional CPTP feasible set is compact, so this maximum is attained. Equation (2) shows that its private twirl attains equality in (3). Thus

    δ^*_{frame}(F)=2[1-f_opt(F)].                           (4)

No recovery algorithm is needed for this exact comparator identity. The learner's role is to approach its generally unknown optimum at the stated calibration and processing costs.

## 3. Full collective entanglement-recovery fidelity tensorizes

This section permits arbitrary input dimension d, not only qubits, and does not restrict the collective decoder to products.

Let E:A→B have input dimension d and Kraus matrices K_j (rows B, columns A). Use an **unnormalized decoder Choi matrix**, with decoder input B first and logical output A second:

    X_D=Σ_b |L_b>><<L_b|,
    |L_b>>=Σ_{u∈B,v∈A}(L_b)_{v u}|u>_B|v>_A,
    X_D≥0, Tr_A X_D=I_B, Tr X_D=dim B.

Define the positive coefficient

    w_j=Σ_{u,v} conjugate((K_j)_{u v}) |u>_B|v>_A,
    H_E=d^(-2) Σ_j |w_j><w_j| ≥0.                          (5)

Equivalently H_E is the FULL transpose of the unnormalized source Choi matrix, with its factors swapped, divided by d². It is not a partial transpose. In particular Tr H_E=1/d. The Kraus trace identity gives

    F_e(D E)=Tr(H_E X_D).

The primal and dual SDPs are

    maximize Tr(H_E X),      X≥0, Tr_A X=I_B;
    minimize Tr Y,           Y=Y†, Y⊗I_A≥H_E.              (6)

There are strict feasible points X=I_B⊗I_A/d and Y=c I_B for c>||H_E||. Standard finite-dimensional SDP strong duality therefore applies; optimum certificates exist. Every feasible dual Y is positive semidefinite, since Y⊗I_A≥H_E≥0. This positivity is the tensorization mechanism.

For a second source F:C→D, a permutation grouping receiver inputs and logical outputs identifies

    H_{E⊗F}=H_E⊗H_F.                                      (7)

Tensoring primal optimizers gives f_opt(E⊗F)≥f_opt(E)f_opt(F). To obtain the reverse inequality, let A=Y_E⊗I_A≥H_E and B=Y_F⊗I_C≥H_F. All four matrices are positive semidefinite, and

    A⊗B-H_E⊗H_F
       =(A-H_E)⊗B+H_E⊗(B-H_F)≥0.

Hence Y_E⊗Y_F is dual feasible for the product problem, with trace (Tr Y_E)(Tr Y_F). This proves

    f_opt(E⊗F)=f_opt(E)f_opt(F),
    f_opt(E^⊗M)=f_opt(E)^M.                                (8)

Applying (4) to E^⊗M proves (A). This is the familiar one-sided singlet-fraction/conditional-min-entropy SDP structure; the direct normalization and product proof above avoid importing any unstated entropy convention. See [König–Renner–Schaffner, The operational meaning of min- and max-entropy](https://arxiv.org/abs/0807.1338) for the established operational relation. No novelty of the SDP product principle or Pauli twirl is claimed.

## 4. Why shared training noise does not spoil near-optimal batch error

Write E=Ad_W E₀ with common output-support dimension k. The exact joint reduction, applied once to all N calibration outputs and M payload outputs, has the arbitrary-operator identity already used in the received Bures proof. Its output is a mixture over one virtual U of

    [six training banks from E_U] ⊗ (id_ref⊗E_U^⊗M)(payload),
    E_U=Ad_U E₀.                                          (9)

The payload frames may be placed in the payload input in (9); they do not change the common physical output support. Conditional on U, the calibration state and every measured training record h are independent of the arbitrary payload and of its independent keys. The feasible learned CPTP decoder D_h acts on each reduced payload separately. Therefore after private-key averaging the exact-reference batch channel is

    Γ_M=E_{U,h} [T(D_h E_U)]^⊗M,                           (10)

a generally **correlated** Pauli channel, not the tensor power of its averaged marginal. Put f_h=F_e(D_h E_U). Frame-invariance of the unrestricted optimum gives, for every U,h,

    0≤f_h≤a=f_opt(E_U)=f_opt(E).                           (11)

The global identity probability is E f_h^M. Consequently

    ||Γ_M-id||_diamond=2[1-E f_h^M].                        (12)

Suppose only the averaged local-loss guarantee is available:

    E(1-f_h)≤(1+gamma)(1-a)+epsilon_0.                      (13)

For every f∈[0,a],

    a^M-f^M=(a-f)Σ_{j=0}^{M-1}a^(M-1-j)f^j
            ≤M a^(M-1)(a-f).

Also

    M a^(M-1)(1-a)≤(1-a)Σ_{j=0}^{M-1}a^j=1-a^M.

The endpoints a=0 or a=1 follow directly (physical qubit recovery in fact has a≥1/4). Taking expectations gives

    a^M-E f_h^M
       ≤gamma(1-a^M)+M a^(M-1)epsilon_0
       ≤gamma(1-a^M)+M epsilon_0.                         (14)

Combining (12), (14) and (A),

    ||Γ_M-id||_diamond
       ≤(1+gamma)δ^*_{frame,M}+2M epsilon_0.               (15)

The sharper additive coefficient 2M a^(M-1) is available if a is known, but no a-dependent tuning is needed. This argument explicitly uses the pointwise upper bound f_h≤a, not independence of learned errors. A high-probability event would also suffice, at the avoidable cost of an additional 2beta error and its sample-confidence factor.

## 5. Explicit finite-control allocation and source accounting

Use the finite Bures procedure from the received proof with its local accuracy parameter set to

    epsilon_loc=epsilon/(2M).

Its n per-bank samples, eigensolver accuracy and feasible SDP accuracy can be chosen as

    n=ceil[30720 D(log(2D)+1)M/(gamma epsilon)],
    a_eig²≤gamma epsilon/(6144M),
    m:=E delta≤gamma epsilon/(384M),
    eta≤gamma epsilon/(32M).                               (16)

Here a_eig is backward eigenvector/matrix error, not f_opt. The received uniform risk transfer yields for the exact-reference common-frame training/decoding protocol

    E(1-f_h)≤(1+gamma)ell_*+48m/gamma+4eta/gamma
            ≤(1+gamma)ell_*+epsilon/(4M).                 (17)

Equations (15)–(17) give total ideal additive complete error at most epsilon/2.

Independently allocate **total unhalved diamond discrepancy** nu≤epsilon/2 between the actually implemented complete block protocol and this exact-reference one. Include all N probe preparation errors, the single reduction on N+M systems, all six purification procedures, bounded-seed/randomization discrepancies, and every finite implementation error not already charged to m or eta. Include all M decoder uses and all input/output frame gates. For instance each use of a compiled learned decoder must have discrepancy at most its allocated total decoder budget divided by M. Telescoping and contractivity then make nu a bound on the whole block discrepancy, so (B) follows by the triangle inequality. Unlike Bell risk, the final diamond discrepancy is added as nu, not nu/2.

The approximate physical reduction is **not** asserted to retain a literal U decomposition. Equation (9) is used only for the exact-reference channel, and nu is transferred afterward. No beta-scale record-distribution accuracy or confidence amplification is needed for this expectation-only theorem.

The source cap is deterministic and includes every acquired calibration output even if later unused. Pauli framing requires no extra source calls, but it does require 2M private random key bits, storage or trusted delivery of those bits between pre-source control and receiver, and O(M) known logical frame gates. These are paid receiver/controller resources, not an automatic property of an already received unframed datum. If sender and receiver are separate parties, the private-key distribution/control interface must be supplied and charged. Both proposed method and conventional comparator receive the same interface.

The common reduction has N+M inputs; storage and latency include waiting for the entire block. Processing is theoretical polynomial in R,M,1/(gamma epsilon),log(s), using the imported joint reduction/purification primitives and the explicit conventional decoder SDP. The compressed decoder optimization is performed once; its use M times does not require training M independent banks. Initial physical storage is (N+M)ceil(log₂s) qubits, plus finite receiver workspace and key registers. Precision costs must be allocated across the complete actual gate cap. No practical hardware cost or noise threshold is inferred.

## 6. Comparator resource fairness and exclusions

For fixed E, any adaptive **pre-datum** calibration procedure—classical, quantum, entangled-probe, or mixed—prepares a fixed state tau_E on its retained banks and records. It is independent of the logical payload. Any subsequent collective receiver map A induces the ordinary CPTP decoder

    D_E(x)=A(tau_E⊗x).

Thus even unrestricted calibration banks and adaptive conventional training cannot exceed f_opt(E^⊗M). Key-dependent bank preparation can likewise be absorbed separately into D_{E,P}, provided it is payload-independent. Allowing the comparator exact knowledge of E is stronger than supplying the same finite calibration information, not an informational handicap. The benchmark is a fundamental decoder optimum, not a proof of source-complexity separation from the best conventional learner.

The strongest equally informed conventional alternative here is precisely reduced-frame output tomography plus a full CPTP recovery SDP, allowed its own adaptive calibration and collective decoder. The Bures construction **is** such a conventional measured-data learner after quantum frame acquisition. What this corollary removes is the distinction between its entanglement-loss comparator and the operational complete-error optimum **within the explicitly shared private-framing model**, including collective decoders. It does not establish a learning-speed separation, historical novelty, generic-noise scalability, or an efficient implementation for an arbitrary large physical-rank source.

Excluded changes of task include: an arbitrary encoder or lower-rate quantum code; additional source use on the unknown payload; feedback that changes future payload inputs based on earlier outputs; environment access; a source correlated across calibration and payload calls; a supplied payload-correlated ancilla; private key leakage to the tested channel's external registers; normalized postselected output without its success cost; and a reusable future-physical-input decoder. Arbitrary entanglement among the M block inputs and an untouched external reference is included.

## 7. Concrete nonextensions, preserved as counterexamples

### 7.1 Exposed keys do not have the linear Bell-loss formula

For the coherent qubit rotation U_theta=exp(-i theta Z), F_e(Ad_U)=cos²(theta). Its private Pauli twirl has diamond error 2sin²(theta), while each key-conditioned conjugate has diamond error 2|sin(theta)| for |theta|≤pi/2. With an output key flag, the maximally entangled input already gives the latter value in every branch. Thus private averaging, not merely writing a random Pauli in the protocol, is essential.

### 7.2 The generic unframed optimum is strictly different

Consider amplitude damping with 0<p<1, t=sqrt(1-p),

    K_0=diag(1,t),   K_1=sqrt(p)|0><1|.

In the (B,A) basis 00,01,10,11, (5) gives

    H=(|00+t11><00+t11|+p|01><01|)/4.

The identity decoder X=|00+11><00+11| is primal feasible. The dual

    Y=diag((1+t)/4, t(1+t)/4)

has the same value a=(1+t)²/4. Its slack Y⊗I-H has a two-by-two 00,11 block (t/4)[[1,-1],[-1,1]], and strictly positive entries t(1+t)/4 on both 01 and 10. Its kernel is exactly span{|00+11>}. Complementary slackness and the TP constraint therefore make the identity the **unique** entanglement-optimal decoder.

Yet the identity decoder's recovered channel, tested on |1><1|, has diamond error at least 2p, and

    2p > 2(1-a)   for 0<p<1.

If an unframed decoder achieved error ≤2(1-a), (1) and f_opt=a would force it to be entanglement-optimal, hence identity, a contradiction. Compactness and continuity imply that the unframed minimum is strictly greater than the privately framed minimum 2(1-a). This preserves an explicit counterexample to any accidental promotion of (A) or (B) to the generic unframed model. An exact formula for the unframed optimum is not needed or claimed.

## Evidence status

`private_framed_checks.py/.json` checks Choi/Kraus normalizations, random Pauli twirls, tensor-product coefficient order, primal/dual product certificates, the scalar batch-regret inequality, finite budgets, and the two nonextension examples. These are mathematical/numerical checks, not executions of collective Schur reduction, random purification, or a hardware decoder. Independent review is recorded separately in `private_framed_independent_*` files. No external upload or modification of the received proofs is part of this work.
