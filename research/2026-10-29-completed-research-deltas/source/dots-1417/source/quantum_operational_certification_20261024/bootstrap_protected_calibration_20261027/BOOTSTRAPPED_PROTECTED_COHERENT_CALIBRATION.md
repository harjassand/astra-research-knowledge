# Protected coherent calibration bootstrapped from an ordinary constant-quality seed

27 October 2026. New composed theorem candidate; independent receiving required. This is a mathematical communication/reference bootstrap using trusted, explicitly paid local operations. It is not a hardware threshold, a fault-model discovery theorem, an ordinary-output-only encoder learner, or a novelty claim.

## 0. Result and exact scope

Use the stationary independently reset CPTP source, known quaternion encoder family, calibrated controlled-anchor phases, and valid four-anchor normalized-Choi-rank bound R from `../coherent_encoder_bures_bridge_20261027/COHERENT_ENCODER_UNRESTRICTED_RECOVERY.md`. Thus E_x=N Ad_(V_x), x in S^3, and

    ell_* = min_(x,D CPTP) [1-F_e(D E_x)].

All source outputs from this family lie in one unknown subspace S of dimension at most k=min(s,8R); each E_x has Choi rank at most 4R. No support basis is supplied. Assume the CONSTANT-MARGIN seed promise

    0 < p0 < 1/20,  0 < 4 Delta < p0,
    ell_* <= p0-4 Delta.                                    (P)

For example p0=1/25 and Delta=1/200 give the promise ell_*<=1/50. Neither a seed encoder nor its decoder is supplied. The fixed positive Delta is a substantive promise; the result does not find a positive-capacity channel under arbitrary noise.

An ordinary finite-grid six-input Bures learner and independent SAME-FRAME holdout first find a constant-quality seed. Concatenated five-qubit coding then sends all THREE coherent calibration reference qubits (two control qubits I and one Bell qubit A) through additional calls to N. No quantum reference is transported around N. All subsequent data, reference-codeword, and final payload calls use one continuously retained online receiver frame.

For a fixed finite payload horizon M>=1, define the family private-frame comparator

    delta^*_(family,M)=2[1-(1-ell_*)^M].                     (1)

It permits a selected fixed family encoder and arbitrary key-dependent collective physical CPTP decoders, exact source knowledge, and arbitrary pre-datum calibration. It does not permit cross-use coding of the unknown deployed payload or extra payload-dependent source calls. Each deployed logical qubit uses N once. Under the stated local-control and frame-compiler accuracy contract, the construction below achieves

    ||Lambda_actual,M-id||diamond
       <= min{2,(1+gamma)delta^*_(family,M)+epsilon},          (2)

for 0<gamma,epsilon<=1, with a deterministic source cap

    H = N_warm + n_Gamma(1+3·5^L) + M
      = O_tilde(R^2 M/(gamma epsilon))                      (3)

when p0,Delta are fixed constants. The suppressed factor includes a reference-code overhead of order log^(log_2 5)(n_Gamma/epsilon), not a constant. The final learned x,D deploy directly in the SAME persistent frame: there is no fresh recovery bank and no second multiplicative recovery-optimization factor.

For M=1, the unframed exact-reference Bell-risk argument also gives a near-optimal discovered encoder and decoder. Pauli-framed deployment supplies the complete-error interpretation (2); no generic unframed diamond-optimality claim follows.

The entire post-warmup calibration uses entangled multi-use source queries. Calling the whole method ordinary-output-only would be false. Only the warm-start acquisition and holdout have that restricted interface.

## 1. Frozen imports and the compiler dependency

The following received results are imported, not re-proved or strengthened silently:

* `../direct_cptp_bures_bridge_20261027/DIRECT_CPTP_BURES_RISK_RECOVERY.md`: six-bank positive Bures risk, high-confidence finite tomography, certified full-CPTP SDP and known decoder synthesis.
* `../direct_cptp_bures_bridge_20261027/PRIVATE_FRAMED_COMPLETE_OPTIMALITY.md`: private Pauli complete-error identity, arbitrary collective-decoder fidelity tensorization, expected-regret transfer.
* `../coherent_encoder_bures_bridge_20261027/COHERENT_ENCODER_UNRESTRICTED_RECOVERY.md`: coherent Gamma contraction, anchor-rank/common-support bounds, uniform positive Bures risk, global S^3 net, and finite feasible joint encoder/decoder search.
* `../explicit_online_random_dimension_reduction_compiler_20261027.md`: complete causal common-frame law on arbitrary operators, including references and adaptive linking, and polynomial known local compilation over a prescribed finite horizon. The canonical source SHA256 is `b1cc6fbd5fac507f04adaa85e5831132e1f4bf1f57b290b5a5032799db0715a8`, matching the independent receipt created 2026-10-27T20:51:24.342642Z. This receipt was absent at initial task assignment but is now present and hash-matched. Its downstream statistical conclusions are expressly not received by that compiler audit.

`../streaming_bures_recovery_persistent_frame_20261027.md` motivates the chronology, but its downstream corollary is not used as a substitute for the causal identity and the statistical proof here. Without the received efficient compiler, the causal-existence version alone would give a finite, potentially exponentially expensive receiver and would NOT justify the polynomial-gate statement.

Use one causal frame with common k and horizon H. Its exact-reference restricted comb is operationally equal to sampling one mathematical Haar U and using E_(x,U)=Ad_U E_(x,0) on every slot. Equality holds on all common-supported operators, so entangled inputs, retained references, measurements of earlier outputs, and record-controlled later encoders may be linked into it. U is not an implemented or exposed classical variable. After observing warm records its posterior generally is not Haar. All later arguments are pointwise in U and therefore survive this posterior change.

## 2. Ordinary seed search without target-quality recovery

### 2.1 A constant grid is sufficient

For fixed CPTP D the true family loss ell(x,D)=x^T G_D x has 0<=G_D<=I. At a globally minimizing pair (x*,D*), x* is a minimum eigenvector of G_(D*). Therefore a unit y at chord distance h obeys

    ell(y,D*)-ell(x*,D*) <= h^2.

Take all eight signed cube faces in R^4, grid the three free coordinates with spacing 2/m0, and normalize, with

    m0=ceil(sqrt(3/Delta)),  K<=8(m0+1)^3.                 (4)

The normalization map on a fixed signed unit face is 1-Lipschitz, giving h^2<=3/m0^2<=Delta. Thus at least one grid point j* has ell_opt(E_(x_j*))<=ell_*+Delta. For fixed Delta, K is a constant independent of target epsilon and R. The grid need not know x*.

### 2.2 All candidate training banks share the persistent frame

Put

    r_w=min(4R,k), D_w=2^ceil(log_2(k r_w)),
    gamma_w=Delta, m_w=Delta^2/96, eta_w=Delta^2/8,
    n_w=ceil[(80 D_w/m_w) log(12 D_w K/beta_t)].             (5)

For every j acquire n_w ordinary outputs of each of the six Pauli eigenstates through E_(x_j). Feed every physical output immediately into the next SAME frame step, and store its emitted k-register. All candidate banks are acquired before their Bures tomography/SDPs; the persistent quantum memory is retained. Run the received random-purification and finite-Clifford procedures separately on each homogeneous bank, with backward eigensolver error <=sqrt(m_w)/4. Compile each certified feasible candidate D_j. Ideal synthesis is part of the exact-reference process; all actual synthesis deviations are in Section 7's global finite budget.

For every fixed U, a union bound using the received confidence theorem gives an event T of probability at least 1-beta_t on which, simultaneously for all candidates,

    p_j := 1-F_e(D_j E_(x_j,U))
      <= (1+Delta)ell_opt(E_(x_j))+48m_w/Delta+4eta_w/Delta
      <= ell_opt(E_(x_j))+2Delta.                         (6)

The last inequality uses ell_opt<=1. Hence under (P), on T the distinguished candidate satisfies p_(j*)<=p0-Delta. This learns only constant-quality recovery. No epsilon-quality channel, protected Bell reference, or coherent control of N was assumed to obtain it.

### 2.3 Fresh same-frame holdout and honest abort accounting

After all D_j are fixed, acquire for each candidate v fresh holdout uses. In each use choose a uniformly random six-state input, decode its emitted k-output with D_j, and test return to that known input. For mismatch Y in {0,1}, the six-state identity gives

    q_j=E(Y|U,training)=2p_j/3,
    p_hat_j=(3/2)(1/v)sum Y,
    v=ceil[(9/(2Delta^2)) log(2K/beta_v)].                 (7)

For fixed U and the entire frozen training record, future reset source calls are independent, so Hoeffding and a union bound give

    Pr(V^c|U,training)<=beta_v,
    V={all j: |p_hat_j-p_j|<=Delta/2}.                    (8)

Accept the first candidate satisfying p_hat_j<=p0-Delta/2; call it x0,D0. If none passes, ABORT with an explicit flag and a fixed logical replacement output on any requested payload ports. No retry-until-success or normalized postselected source procedure is used.

On V, every accepted seed has p<=p0. On T intersect V, at least j* passes. Therefore

    Pr(accept AND p>p0)<=beta_v,
    Pr(abort)<=beta_t+beta_v,
    Pr(abort OR (accept AND p>p0))<=beta_t+beta_v.          (9)

These are bounds in the exact common-U experiment. They are not a claim that every displayed acceptance record certifies p<=p0. If an acceptance-conditioned formulation is wanted, the false-seed mass is at most beta_v/[1-beta_t-beta_v], under (P); the division cannot be omitted. The main theorem is unconditional and pays bad history mass directly.

The source cap of this warm stage is

    N_warm=K(6n_w+v).                                    (10)

It includes unsuccessful candidate tests. Finite six-label sampling can use a capped generator with its discrepancy in the finite budget. Nothing is estimated at accuracy epsilon in the warm stage; only its failure probability decreases with epsilon, logarithmically increasing n_w,v.

## 3. Where independent Pauli errors DO and DO NOT come from

Freeze U and the ENTIRE warm record w, including holdout outcomes and the selected candidate. On an accepted good history, the exact local source/decoder map is the same fixed qubit channel

    Lambda_(U,w)=D0 E_(x0,U),  1-F_e(Lambda_(U,w))=p<=p0.

For each subsequent seed-channel use put an independent uniform private Pauli P BEFORE V_(x0), and undo P AFTER D0. Average the private keys, which are not provided to an external tester or the later learner. This is exactly the Pauli channel

    P_(U,w)=sum_Q pi_Q Ad_Q,  pi_I=1-p.                  (11)

The memoryless/reset N assumption, the exact common-U causal law, the frozen D0, and independent per-use keys imply that any number of these logical uses is P_(U,w)^tensor t, as a COMPLETE map, even when their inputs are entangled with each other, the data output, the source environment, or another untouched reference. Equivalently, their Pauli-error variables are iid conditional on U,w and independent of the input state. Averaging over U,w afterward creates correlations and must not be replaced by a product of marginal averages.

**Holdout alone does not prove (11)'s tensor-power assertion.** An arbitrary correlated receiver/frame/control fault process can have small measured one-use p yet fail an entire block with probability of order p, not p^2. Such faults are never inserted into p and then squared. The theorem either uses the exact trusted local process or charges uniform per-operation/whole-interactive-circuit discrepancy separately. No local-stochastic hardware fault model is inferred from marginal observations. Relative phases of the known controlled E_i also remain separately qualified.

## 4. Five-qubit coding of three calibration references

Use a standard deterministic [[5,1,3]] stabilizer encoder and syndrome recovery. It exactly corrects every weight-zero or weight-one Pauli error; residual errors are logical Pauli errors. With ideal local controls and independent Pauli error probability p_l on its five subblocks,

    p_(l+1)<=Pr(at least two subblocks err)
             <=binom(5,2)p_l^2=10p_l^2.

Thus for L concatenation levels and b=5^L physical seed uses per reference qubit,

    p_L <= (10p0)^(2^L)/10,
    ||Q_L-id_2||diamond=2p_L.                            (12)

Disjoint blocks have independent state-independent Pauli error variables conditional on U,w, even for entangled encoded inputs. Induction therefore applies at every concatenation level without assuming product codeword states.

Three separately encoded references have complete identity discrepancy at most 6p_L. Choose the smallest L>=0 for which

    (3n_Gamma/5)(10p0)^(2^L)<=nu_ref.                    (13)

Then all n_Gamma reference triples together have discrepancy <=6n_Gamma p_L<=nu_ref. More generally the same hybrid bound is valid for arbitrary intervening data preparation and later processing. For fixed p0<1/20,

    5^L=O([log(n_Gamma/nu_ref)]^(log_2 5)).               (14)

There is no postselection and no source retry. This is standard concatenated quantum communication coding, not a new fault-tolerance threshold. The code is charged once per actual physical seed-source use, and each such use includes the learned ordinary encoder, frame update, D0, and its private Pauli pair.

The separate `../bootstrap_five_qubit_pauli_independent_receipt_20261027.md` receives this code-transfer component, including all 1024 Pauli errors and biased distributions, but does not receive the warm good-event construction or the present full theorem. The standard five-qubit code and single-error correction are established background: [Laflamme et al., Perfect Quantum Error Correction Code](https://arxiv.org/abs/quant-ph/9602019). The simple recurrence above is the independent-Pauli union bound, not a claim that arbitrary hardware faults satisfy that model.

## 5. Actual chronological preparation of one Gamma copy

After successful warmup, for t=1,...,n_Gamma, use the following FIXED data/control preparation, independent of the warm record. Only the reference-transport encoder/decoder depends on that record. The warm classical record may control the seed choice, but the frame quantum memory and its coherent path are never exported as a warm record.

1. At the sender, prepare Bell A,L and the two-qubit control I in (1/2)sum_i |i>. Apply V0 to L and the calibrated known controlled E_i to the physical data. The source N is NOT controlled or inverted.
2. Send the physical data through N ONCE. Feed that output into the next frame step and store its emitted k-register B_t at the receiver. I,A remain at the sender, coherently entangled with this data and possibly its source environment.
3. Locally encode each of the three reference qubits into the level-L five-qubit code. Transmit its b physical codeword qubits sequentially using the seed encoder x0, the same N, the next persistent-frame steps, D0, and fresh private Pauli pairs. Apply deterministic local QEC decoding at the receiver. All three original reference qubits are consumed by these transmissions; none travels around N.
4. Store the recovered I_t,A_t with B_t. Keep the frame memory alive, unmeasured and unreset. Move to the next fresh Gamma preparation.

The untransmitted codeword qubits and other references must remain coherent locally while waiting. Receiver storage must retain B_t and recovered references. These local memories are trusted/paid resources and their errors belong in nu_fin. Eliminating a supplied quantum link around N does NOT eliminate trusted local memory, local QEC controls, classical key delivery, or frame-memory lifetime.

Conditional on fixed U,w, replacing only the three logical reference-transport channels by identities makes the stored state exactly Gamma_U, and all copies are iid Gamma_U. This replacement is an ANALYSIS comparison, not a supplied physical bypass. It is justified in the virtual whole comb, after all physical outputs including reference calls have been linked to the causal frame. One must not physically delete the reference-call frame steps and infer that an independently reset frame stays aligned.

The data/reference entanglement across sequential N calls causes no gap: the channel comparisons are complete and the common-frame law is an arbitrary-operator/causal-comb identity. No assumption of product inputs to N is used after warmup.

## 6. Complete-bank comparison, not an actual-rank assertion

Define an ideal comparison process B as follows: it has the SAME warm experiment and mathematical U, but ignores the warm accept/abort decision, supplies perfect reference transport after every data call, learns from the exact Gamma_U bank, and serves the final payloads. This is a legitimate comparison channel, not a claimed implementable resource. The actual process A aborts or uses the QEC links as stated.

On accepted good histories, (13) bounds the difference between A and B by nu_ref. On the remaining histories, two normalized complete channels differ by at most two. Equations (9) and convexity therefore give, for arbitrary external reference and arbitrary payload input,

    ||A_exact-B||interactive <= 2(beta_t+beta_v)+nu_ref.  (15)

The bad-history weight is pre-payload and input-independent. B's future Gamma banks conditional on U,w are iid regardless of whether warmup would have aborted. Their quality theorem is uniform in U,w, so the fictitious no-abort comparison has the ordinary coherent learner's statistical guarantee without a conditional-success normalization.

The noisy actual Gamma bank may have greater rank, even full rank. We DO NOT apply an exact low-rank theorem to it. The known reduction/purification/tomography/optimization circuit is globally a CPTP process; it is run on the actual input, while its rank-based statistical guarantee is invoked ONLY for B's exact low-rank input. Contractivity transfers (15) through that same circuit, final encoder-label selection, and deployment. This comparison includes all copies and later outputs, not merely an O(epsilon) single-copy calibration transfer certificate.

All actual known-control/compiler approximation discrepancies, including those in warmup, add to (15) as one nu_fin. Approximate frame implementations are not asserted to possess a literal U. Their complete comparison to the exact frame is made first/last by the uniform interactive error contract.

## 7. Coherent learning and direct same-frame deployment

For the exact Gamma_U comparator let

    d_s=8k, r_s=min(4R,d_s),
    D_s=2^ceil(log_2(d_s r_s)), L_s=log(2D_s)+1,
    e=epsilon/(2M),
    n_Gamma=ceil[40960 D_s L_s/(gamma e)]
           =ceil[81920 D_s L_s M/(gamma epsilon)].        (16)

Run the received whole-Gamma random-purification/Bures tomography and joint global encoder/full-CPTP decoder optimization, with

    m<=gamma e/512, eta<=gamma e/16,
    a_eig^2<=gamma e/8192.                               (17)

The exact statistical proof then gives, conditional on each U,w and averaged over the new Gamma learner record g,

    E_g ell_U(x_hat,D_hat)
       <=(1+gamma)ell_*+128m/gamma+4eta/gamma
       <=(1+gamma)ell_*+epsilon/(4M).                    (18)

Unlike the old fresh-frame deployment construction, retain the feasible D_hat as well as x_hat and compile D_hat using the received finite known-matrix synthesis. After the Gamma bank is measured and the classical optimization is complete, the frame remains alive. Each future payload is privately Pauli-framed, encoded by x_hat, sent through N once, entered into the next frame step, decoded by that SAME D_hat, and unframed. No Gamma system carries unknown payload information around the source.

For fixed U,w,g the local logical channel is fixed and has fidelity f<=a*=1-ell_*. The final exact-reference privately averaged block is a mixture of its Pauli-twirled tensor powers, with complete error 2[1-E f^M]. Applying the received pointwise-regret inequality to (18) gives

    ||B_M-id||diamond
       <=(1+gamma)2[1-(a*)^M]+epsilon/2.                (19)

Here the family benchmark (1) follows by the received collective-decoder tensorization for each fixed x, followed by maximizing f_opt(E_x). Randomizing encoder choices cannot improve that maximum. Calibration QEC uses extra known-state/reference source calls BEFORE payload arrival and is not cross-use coding of the deployed payload.

Choose, for example,

    beta_t=beta_v=epsilon/32,
    nu_ref=epsilon/8,
    nu_fin<=epsilon/4.                                  (20)

Then (15) plus finite errors is at most epsilon/2. Triangle inequality with (19) proves (2). No second (1+theta) recovery factor is introduced because D_hat is used in its own continuing frame. There is no learned reusable physical-space decoder after the frame is reset or lost.

Only the final logical payload outputs are compared in (2). Frame memory, code syndromes, private Pauli keys and calibration records are not exported. The records are generated before payload arrival; an optional exposed-record theorem must specify its ideal record law and pay any changed record-distribution errors, not claim quality for every record.

## 8. Finite implementation, cap, storage and scaling

The predetermined maximum number of actual N calls is exactly

    H=K(6n_w+v)+n_Gamma(1+3b)+M,  b=5^L.                 (21)

An early abort uses fewer calls and releases replacement outputs; it never exceeds H. One may pad with dummy calls to a fixed length without improving the guarantee or hiding source use. No empirical-until-success stopping rule is needed. The frame compiler is initialized for this horizon and common k, INCLUDING reference-codeword uses.

The total nu_fin contract is a worst-case complete/interactive discrepancy between the actual deterministic-cap control process and its exact-reference process, uniformly over retained memory and reference inputs. It includes:

* ordinary warm probe preparations, all holdout measurements, finite random-seed generation, and all warm decoder uses;
* every one of at most H causal frame updates;
* every Bell/control-Gamma preparation, with calibrated relative anchor phases;
* every QEC encoding, syndrome recovery, intermediate local storage operation and all 3bn_Gamma seed encoder/decoder uses;
* the known Pauli controls and trusted classical key interface;
* every random-purification/Clifford operation not already covered by the deterministic statistical arithmetic tolerances;
* feasible final decoder synthesis, all M decoder uses, and final encoder controls.

Allocate errors over an explicit polynomial gate/operation cap G, e.g. per-operation complete discrepancy O(nu_fin/G); per-step frame discrepancies sum to their portion of nu_fin. Arithmetic already paid in m,eta is not charged twice. Unknown uncontrolled source drift, adversarial frame-memory faults, or systematic unknown control phases are not hidden inside an assumed marginal p0. If such errors lack a uniform bound or an independently justified fault model, the hardware claim is BLOCKED, even when holdout accepts.

The receiver compiler has polynomial gate/arithmeticproducer-workspace/workspace-qubit cost in H,k,log(s),log(1/nu_fin); its persistent quantum memory may grow with H. The Gamma bank stores n_Gamma(log_2 k+3) reduced qubits plus purification/learner workspace. Warm candidate banks require O(K n_w log k) storage before measurement, which can then be freed except for the frame memory and classical records. Sender codeword storage can use O(b) qubits per reference triple, plus the supplied physical encoder/preparation space. The emitted physical data need not all be retained in dimension s, but the persistent representation memory remains an important long-lived quantum resource. Reference transfers and payloads consume exactly 2(3bn_Gamma+M) private random key bits, plus trusted key delivery/storage as needed.

For fixed Delta, warm source use is O(R^2 log(R/beta_t))+O(log(1/beta_v)), with constants depending on Delta and K. The main source count is n_Gamma times the polylogarithmic coding factor. Known local QEC circuits use polynomially many gates in b; controlled encoders and family preparation costs are separately charged at their actual supplied cost. R may itself be exponential in the number of physical qubits. No practical gate count, generic-noise scalability, unknown-rank adaptation, fault-tolerant hardware implementation, or indefinite horizon is established. Indeed the deliberately conservative checked example p0=0.04, Delta=0.005, R=1, s>=8, gamma=0.1, epsilon=0.01, M=1 gives K=140608, N_warm=214594497410500480 and H=221710211848591997 source calls. These are theoretical caps, not experimentally plausible requirements; optimizing constants and warm acquisition is a substantial practical open task.

## 9. What the bootstrap qualifies, and fair conventional comparisons

The ordinary warmup plus code construction qualifies an approximate quantum REFERENCE COMMUNICATION link through the same unknown reset source. It does not empirically certify all unknown calibration hardware at target accuracy. Known coherent controlled-E_i phases, trusted local computational operations, stationarity, and a persistent frame with the complete-error contract remain prerequisites. If relative control phases are unknown, the old `../coherent_program_deployment_transfer_budget.md` obstruction remains: individually qualified channels do not identify their coherent relative phases, and a candidate holdout does not prove a uniform encoder-policy transfer theorem.

The construction avoids the old epsilon^-2 empirical UNIFORM transfer-estimation route only because it supplies an explicit error-corrected transport with a whole-bank error bound from a constant-quality source seed. Its source errors are suppressed by standard concatenated coding; local hardware inaccuracies are separately paid, not learned away.

A fair conventional comparator receives the same trusted local controls, source calls, quantum output access, memory, private keys, and ability to use entangled calibration. It can perform this same seed search, reference coding, reduced operational-state tomography, and full decoder SDP. This is a constructive integration of standard QEC with conventional coherent-channel estimation, not a separation from those methods. [Chuang and Nielsen's process-tomography framework](https://arxiv.org/abs/quant-ph/9610001) is established background; no complete source environment is reconstructed here, but an operational reduced Gamma state IS tomographed.

No claim is made that ordinary labelled probes alone simulate coherent calibration at no extra cost. No known source inverse, controlled unknown source, noiseless remote link, uncharged failed postselection, source-capacity oracle, target-quality seed, or secretly fixed physical support is supplied.

## 10. Evidence and unresolved receiving scope

`bootstrap_protected_calibration_checks.py/.json` checks 12000 actual signed-face grid roundings, constant-grid/holdout allocations and exact binomial tails, high-precision finite source caps, concatenation overhead, 15000 scalar family-comparator cases, a correlated-fault negative control, and final scalar error budgets. It hash-binds the separate independent five-qubit receipt/check (all 1024 Pauli errors and 1771 exact-rational distributions); it does not claim to duplicate that exhaustive evidence. These are finite algebraic/numerical checks, not executions of the high-dimensional frame or random-purification circuit and not hardware measurements.

The novel receiving obligation is this composition: warm false-accept/abort accounting, causal linking of entangled reference transmissions, whole-bank ideal-input comparison, and same-frame final decoder deployment. The compiler's independent receipt does not by itself receive those claims. All original imported proofs and receipts are unchanged.
