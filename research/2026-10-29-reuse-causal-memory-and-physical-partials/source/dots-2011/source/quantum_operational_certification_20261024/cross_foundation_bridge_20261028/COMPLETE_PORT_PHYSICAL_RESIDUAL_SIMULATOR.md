# A complete quantum-port residual certificate with true prefixes and physical CP suffixes

28 October 2026. **New theorem candidate; independent receiving pending.** This is the full-memory-core, external-coherent-controller extension of the received classical physical-residual and raw-joint-core results. It uses an actual fitted quantum input/output instrument, not merely individually CP causal-break maps. It is distinct from `SIGNED_CORE_COMPLETE_SERVICE_PREDICTION.md`: the present linear-in-horizon certificate pays for a physical hidden-memory candidate; the signed/Dyson route avoids that fit and pays a different stability/projection bound. Neither route is claimed efficient, novel in its general learning ingredients, or better than direct service tomography absent an actual acquisition-depth/reuse need.

## 1. Interface, raw core and the exact full-rank premise

Use the stationary quantum-port interface of the received `IC_PORT_SHORT_DEPTH_COMPLETE_RECOVERY.md` (SHA `9481fa0a4df758dfc0a4fcb264d19629c463c1e1308617cf8166ea03b796ef10`). A supplied upper bound d limits the inaccessible memory dimension. Native action a has accessible input A_a of dimension p_a, output B_a of dimension q_a, and a finite CLASSICAL native outcome o. The source has CP maps

    V_(a,o): L(M tensor A_a) -> L(M tensor B_a),
    sum_o V_(a,o) trace preserving.

Native labels are selected classically. The controller may keep quantum registers and references, entangle/recycle port inputs, measure, and choose subsequent native labels from its classical records. No coherent superposition of native action labels or access to native-outcome/environment amplitudes is given. A reset episode begins with the declared source-memory state product with the caller's payload/reference; arbitrary unknown correlated initialization is not acquired by this theorem. Independent whole-process starts, all controls, storage and resets are paid. The finite algorithmic claims use supplied rational/real-algebraic descriptions of known ideal preparations, readouts and local controls; actual compiled approximations require the explicit implementation allowance below. Arbitrary unspecified real coefficients are not a computability oracle. Take d>=1 and H>=0 to be integers, with a finite nonempty native library.

Calibration has ordinary IC input density matrices rho_(a,u) and output POVM effects E_(a,v). For z=(a,u,o,v), define the physical causal-break memory branch

    Phi_z(tau)=Tr_B[(I tensor E_(a,v)) V_(a,o)(tau tensor rho_(a,u))].

The next input is freshly prepared after measuring/discarding that output. Let r=d^2. Choose r raw branch-prefix words p_j and r future event words f_i, including the empty prefix/test first. Their actual source memory operators tau_j>=0 have mass <=1, and future effects satisfy 0<=F_i<=I, F_1=I. The learner acquires probabilities, NOT these hidden operators:

    H_ij=Pr(p_j then f_i)=Tr(F_i tau_j),
    H_z,ij=Pr(p_j then z then f_i),
    m_j=H_(1,j)=Tr tau_j,             tau_1=rho_initial.

Failed prefixes are retained as zero contributions to raw joint-event estimates. There is no conditional division or uncharged repeat-until-success preparation. In particular m is not silently replaced by the all-ones row.

A simultaneous confidence pool supplies entrywise bands |H-Hhat|<=D_H and |H_z-Hhat_z|<=D_z before any data-dependent core selection. Require

    U=Hhat^-1, A=|U|D_H, ||A||_infinity<1,
    M=(I-A)^-1|U|, K=max(1,sum_(j,i) M_(j,i)).                (1)

All inequalities and matrix arithmetic use exact algebraic numbers or certified outward bounds. The Neumann comparison proves H invertible and |H^-1|<=M on the confidence event. Its r=d^2 independent columns force the actual memory dimension to be exactly d and tau_j to span the full Hermitian memory algebra. Likewise the effects span its dual. This is genuine rank saturation from a supplied upper dimension bound, not a noisy inference that unseen modes are absent.

A lower-rank source can fail this full-core test forever. No rank-deficient extension is asserted. Replacing r=d^2 by a smaller minor requires a separate complete-interface rank/exhaustion theorem and, generally, an operator-compatible quotient argument; the received scalar/classical quotient theorem alone is insufficient.

## 2. Actual fitted ports, not a scalar surrogate

Supply a candidate density sigma_0 and FULL physical maps V^f_(a,o) on memory dimension at most d with exactly CP branch maps and TP branch sums. They use the same input/output spaces, classical outcomes, caller operations and legal preparation/test procedures. Symbolically executing those procedures gives subnormalized sigma_j, candidate tables H^f,H^f_z, and mass row m^f_j=Tr sigma_j, with sigma_1=sigma_0. Require H^f nonsingular. This can be verified directly, or follows from (1) if H^f lies in the same confidence bands. Full rank then also saturates the candidate memory algebra.

Define

    C_z=H^-1 H_z,     C^f_z=(H^f)^-1 H^f_z,
    Lambda(x)=sum_j tau_j tensor x_j,
    Lambda_f(x)=sum_j sigma_j tensor x_j.                   (2)

At both endpoints the initial coordinate tuple is e_1 tensor the caller state. The exact trace rows are m and m^f. Candidate Choi matrices may be singular; no Choi-interior margin is assumed. Certifying the full V^f is indispensable: separately fitting positive/CP maps Phi^f_(a,u,o,v) does not certify one physical map on an arbitrary entangled input A, nor compatibility of different input/output settings. An exact failure control is the qubit transpose map: every memoryless scalar IC branch Tr(E_v rho_u^T) is nonnegative and the POVM sums give a TP branch sum for each preparation, so each scalar memory map is CP. Nevertheless the assembled port Choi is SWAP, with eigenvalues 1,1,1,-1; its Bell output has eigenvalue -1/2. Scalar branch physicality alone is therefore inadequate even with a complete alphabet.

The candidate can be a checked heuristic proposal. A generally expensive finite fallback is exact real-algebraic feasibility in sigma_0 and full port Choi entries, imposing positivity, TP and all rational probability bands. Those word probabilities are polynomials; on the confidence event the actual dimension-d source is feasible. An exact algebraic witness exists whenever the semialgebraic set is nonempty. With r=d^2 and H^f in the bands, full candidate rank is automatic; there is no additional search over vanishing higher-rank minors. This removes that particular rank obligation, NOT the nonconvex physical-fit/bit-complexity burden. A resource-capped UNKNOWN is not charged to the sampling failure probability.

## 3. Operator-valued coefficients and the complete prefix bound

For an arbitrary caller/reference register R define

    Pi_j(X_MR)=sum_i (H^-1)_(j,i) Tr_M[(F_i tensor I_R) X],
    ||x||_Sigma=sum_j ||x_j||_1.                            (3)

The partial functional with F_i is CP: it equals sandwiching by sqrt(F_i) before tracing M. It is trace-nonincreasing since F_i<=I. Thus it is a trace-norm contraction on Hermitian operators, at EVERY reference dimension. By the triangle inequality,

    ||Pi(X)||_Sigma <= K ||X||_1,
    ||Lambda_f(x)||_1 <= ||x||_Sigma.                        (4)

The latter follows from sigma_j>=0, Tr sigma_j<=1 and the tensor-product trace norm; it also holds for signed Hermitian x_j. Here “complete norm” means the supremum of these Hermitian trace-norm ratios over arbitrary reference extensions; this is sufficient for the channel/strategy bounds below.

More concretely, at any positive unnormalized true prefix Omega_MR, Y_i=Tr_M[(F_i tensor I)Omega] is positive and Tr Y_i<=Tr Omega. Therefore

    sum_j ||Pi_j(Omega)||_1 <= K Tr Omega.                   (5)

The coordinate blocks need not be positive or commute. The scalar positive-cube vertex improvement in the classical residual source is NOT substituted for K without a separate matrix-cube proof. We use only the safe acquired sum-of-absolute-inverse bound.

Because the core spans the FULL memory algebra, Pi Lambda=id and Lambda Pi=id, with the same equalities after every reference extension. Candidate extraction Pi_f has the analogous inverse identities. Thus the quantum-port coordinate transfer is an exact representation of physical maps, not only equality of scalar word functionals. In particular, for the complete port map C_a defined next,

    V_a Lambda = Lambda C_a,    V^f_a Lambda_f = Lambda_f C^f_a, (6)

where the classical native outcome register and accessible output are retained. Caller-only operations commute with these coordinate changes. Neither Lambda_f Pi nor the algebraic switching hybrids are assumed positive, CP or trace preserving.

## 4. Paid IC duals make the residual complete

Use known Hermitian duals D_(a,u), B_(a,v) satisfying

    X_A=sum_u rho_(a,u) Tr(D_(a,u) X_A),
    Y_B=sum_v B_(a,v) Tr(E_(a,v) Y_B).                      (7)

Overcomplete frames are allowed; unused outcome duals may be zero. Choose certified bounds f_(a,u)>=||D_(a,u)||op and g_(a,v)>=||B_(a,v)||_1. These depend on the actual local input/output apparatus and its conditioning, not on horizon or reference dimension.

For a coordinate tuple x_j on current input A and remaining caller R, the exact coordinate port is

    [C_a(x)]_(i,o)
      =sum_(j,u,v) C_(a,u,o,v)[i,j]
          B_(a,v) tensor Tr_A[(D_(a,u) tensor I_R)x_j].      (8)

The same formula with C^f gives the candidate. To prove (8), expand the input in (7), apply each port to tau_j tensor rho_u, expand the output in its dual frame, and then use full-core memory reconstruction. This is an identity of full operators including all reference matrix entries. It does not assume that a classical transcript distance controls arbitrary coherent strategies.

For Hermitian x_AR, trace-norm duality gives

    ||Tr_A[(D tensor I)x]||_1 <= ||D||op ||x||_1;             (9)

tensoring B multiplies the norm by ||B||_1. Indeed the dual pairing is with D tensor T for arbitrary Hermitian T of operator norm <=1, whose norm is <=||D||op. Thus no hidden factor depending on the retained quantum memory/reference appears.

Compute the fitted residual bands

    E_z=M[D_z+D_H|C^f_z|+|Hhat C^f_z-Hhat_z|],
    epsilon_a=max_j sum_(i,o,u,v) f_(a,u)g_(a,v) E_(a,u,o,v)[i,j],
    epsilon=max_a epsilon_a,
    delta_m=max_j {D_H,(1,j)+|Hhat_(1,j)-m^f_j|}.            (10)

The identity H(C_z-C^f_z)=H_z-H C^f_z proves |C_z-C^f_z|<=E_z. Equations (8)-(9) then give the COMPLETE one-step coordinate bound

    ||(C_a-C^f_a)(x)||_Sigma <= epsilon_a ||x||_Sigma        (11)

uniformly over reference systems. All native outcomes are jointly summed. A classical adaptive native label costs max_a epsilon_a, not a sum over schedules; its classical register is a direct sum. Count, fit and algebraic repair residuals all remain visible. A nominal optimizer residual without certified arithmetic is insufficient.

Example of explicit apparatus constants: for qubits, use the six Pauli eigenstates rho_(P,s)=(I+sP)/2 as inputs, and POVM E_(P,s)=rho_(P,s)/3. Duals D_(P,s)=I/6+sP/2 and B_(P,s)=3D_(P,s) obey (7), with ||D||op=2/3 and ||B||_1=3. Every input/output pair has weight 2, and the sum of 36 pair weights is 72. These are local conditioning costs, not a factor 72^H. This example does not grant those controls to a device that lacks them.

## 5. The coherent physical-suffix theorem

**Theorem.** On the simultaneous confidence event, every allowed finite controller with at most H native calls has complete accessible endpoint states satisfying

    D_H(source,fit) <= min(1, eta_H),
    eta_H=(K/2)(H epsilon+delta_m).                         (12)

D_H is the supremum of half trace distance over caller inputs/references and all such coherent/adaptive controllers, with every declared accessible classical/quantum record retained. Controllers may be selected after reading the calibration data because the event and bound are simultaneous. More finely, a specified controller has native contribution (K epsilon/2) E_true[L] if L<=H; delta_m is paid once at the final end.

**Proof.** For a fixed controller, work in exact full-core coordinates, with all classical branches unnormalized. Isolate the final true/candidate memory trace rows and telescope native transfers in the orientation

    m T_H...T_1 - m^f T^f_H...T^f_1
      =(m-m^f)T_H...T_1
       +sum_k m^f T^f_H...T^f_(k+1)(T_k-T^f_k)T_(k-1)...T_1. (13)

Known local controller maps and their retained records are inserted at their actual locations, not commuted through native calls. Equivalently apply (13) branchwise on the finite adaptive tree with identity padding after stopping.

At a true active prefix Omega of mass p, its coordinate norm is <=Kp by (5). The local residual has coordinate norm <=epsilon_a Kp by (11). Lift that signed insertion with Lambda_f. By (4) its physical trace norm is no greater. By (6), the remaining coordinate continuation is exactly the candidate FULL physical instrument plus the same caller continuation and final discard of candidate memory. This CPTP continuation contracts the Hermitian trace norm, regardless of entanglement or nonpositivity of the insertion. Summing over true prefix masses at depth k gives Pr_true(L>=k), not a probability assigned to a signed hybrid. The native trace-norm sum is <=K epsilon E_true[L].

The endpoint term applies (m-m^f) to the true final coordinate tuple. The true terminal state is positive with total mass one, so (5) bounds this term by K delta_m. This remains true with the full terminal record retained. Divide by two. Both endpoint states are physical and normalized, giving the cap at one. This proves (12). QED.

The mass-row term is essential for raw cores: the received `RAW_JOINT_CORE_RESIDUAL_ACQUISITION.md` gives two persistent-bit models with identical C_z but different m and different transcript laws. We do not reuse its sharper scalar K or infer a low-rank coherent theorem from that example. If every core preparation is genuinely normalized in BOTH models, m=m^f=1^T and delta_m can be set exactly to zero. The empty prefix fixes initialization in coordinates; no additional unknown start factor is charged. For H=0 identical caller-only protocols agree exactly, even if the conservative displayed mass bound is positive.

This is a complete ACCESSIBLE-process comparison, not a physical trace-distance statement between hidden memories. It gives no uniform bound on normalized rare postselected branches. Unbounded quantum-memory controllers and stopping require a separate limiting statement; only finite bounded-call controllers are asserted here. Finite caller-register dimensions may be arbitrarily large, but their actual costs are not suppressed.

## 6. Acquisition, physical recovery and resource accounting

The finite IC alphabet has s=sum_a (#input settings)_a (#native outcomes)_a (#output outcomes)_a branches. If the actual memory is fully reachable and observable under this alphabet, the prefixes and futures of lengths <=d^2-1 contain a full d^2 core: reachable and dual spans stabilize when a stage ceases to grow. Empty prefix and trace test can be extended to bases. Shifted events have depth <=2d^2-1. With q=sum_(l=0)^(d^2-1)s^l, at most (1+s)q^2 event probabilities suffice before deduplication. The pool can be exponential, and many events share a physical setting. Each shot pays its whole reset and every attempted call, including failed prefixes; multinomial sharing is allowed, no separate independent bank per outcome is required.

For T predeclared events and a common width w, N>=log(2T/beta)/(2w^2) shots per relevant setting suffices by Hoeffding and a union bound, 0<beta<1. A selected core is sound on the joint event; no extra union bound for choosing it is needed. Actual effect/preparation uncertainty must either be included in the declared full implementation comparison or in explicit interval frame/residual bounds; nominal IC matrices are not free exact laboratory facts. A finite cap may return UNKNOWN when the core is ill-conditioned or the physical fit is not certified.

For a compatible physical candidate in the bands, put B_z=M(|Hhat_z|+D_z). The same inverse bound applies to H^f, so

    E_z <=2M[D_z+D_H B_z],    delta_m<=2 max_j D_H,(1,j).    (14)

For a fixed genuinely nonsingular core these bounds vanish as widths shrink; every fixed H,target can eventually be certified if exact physical search is funded. This is not a sample bound independent of conditioning, and not guaranteed success for a lower-rank source. Sequential acquisition must allocate a summable failure budget.

For a specified H-call service with payload L and finite accessible output Y, (12) implies half ||N_true-N_fit||diamond<=eta=min(1,eta_H). Optimize a decoder R:Y->L over ALL CPTP maps for the explicitly computed candidate channel, with certified optimization slack zeta. The received IC-port source's finite diamond SDP and paid Choi-factor/Stinespring/compiler construction apply unchanged. Triangle inequality and CPTP contractivity give

    half ||Rhat N_true-id||diamond
      <= inf_(R CPTP) half ||R N_true-id||diamond +2eta+zeta. (15)

No decoder menu, twirling premise or environment measurement is used. The fixed-time, forward-only, exactly-one-payload-USE service can be preserved if it is the declared service; the certificate does not silently change encoding, service time or controls. A general H-call service is a different expressly declared task.

Averaged ideal recordwise regret additionally pays beta. Forced physical fallback on good-event core/search/optimizer UNKNOWN histories pays their actual probability alpha_abort separately, unless the compared protocols both carry an explicit abort flag and throughput is reported. A full implementation allowance must retain the acquisition/selection record: actual good-record mass is at least 1-beta-nu_record, and one complete end-to-end half-diamond allowance nu_impl transfers the RECORD-AVERAGED deployed-channel guarantee. It does not automatically bound the expectation of record-conditioned diamond norms. Compiler error already included in nu_impl is not counted twice. These are the received IC-port accounting distinctions, not new claims.

Physical port fitting, any exact algebraic feasibility, inverse-core conditioning, IC frame weights, event-pool enumeration, H-step candidate contraction, accessible Choi dimension, caller records, decoder SDP precision, initialized ancillas, and universal local gate synthesis all have to be charged. No physical realization search or production compiler was executed for this theorem. An actual synthesized fitted simulator could incur a separately paid per-call complete-norm error; classical calculation from the candidate does not require constructing that hidden-memory simulator in hardware.

## 7. The strongest equally informed baseline

See the separate root companion `DIRECT_SERVICE_TOMOGRAPHY_COMPARATOR.md`. If calibration may run the SAME fixed H-call service, ordinary end-to-end channel tomography already learns its small p->k accessible channel without environment reconstruction, a memory-dimension promise or a hidden physical fit. With input dual D_u and final-output dual B_v,

    J_N=sum_(u,v) p_uv D_u^T tensor B_v,
    half ||Nhat-N||diamond <=(w/2) C_J,
    C_J=sum_(u,v)||D_u||_1||B_v||_1.                       (16)

For minimal p^2 input settings and at most k^2+1 outcomes, let T_direct=p^2(k^2+1). N_direct>=log(2T_direct/beta)/(2w^2) shots PER INPUT is enough; all outcomes share those shots. The total native calls are at most H p^2 N_direct. Project the signed accessible channel estimate to CPTP (factor two plus projection slack), then use the same full decoder SDP and synthesis. Thus a desired final physical channel error eta uses w<=eta/C_J absent projection slack. Preparations, readout, final record dimension and numerical work are still paid.

The short-core route can require w proportional to 1/H and hence H^2 sample growth, amplified by K, inverse-core powers and IC weights. The direct baseline need not pay that precision scaling when only this fixed service is wanted; it pays H calls per shot. The physical-candidate search can further disadvantage the present route. No practical advantage follows from (12) alone.

The distinctive possible benefit is a maximum ACQUISITION EPISODE DEPTH of 2d^2-1 and reusable prediction for many later coherent/adaptive controllers/services from one fixed short-word calibration. It matters only if that depth restriction or amortized multi-service goal is real. A final output containing exponentially many classical histories makes direct tomography costly, but can also make the candidate channel/decoder representation costly. Neither method removes that burden by renaming the output or silently discarding a record.

## 8. Prior art, separation and evidence scope

This theorem combines a full-core operator-valued coordinate argument, explicit IC dual-weighted residuals, and the existing true-prefix/physical-suffix telescope. It does not claim invention of spectral/Hankel identification, quantum process tomography, full-CPTP decoder optimization or HQMM learning. Ordinary IC process-tensor reconstruction is established in [White et al., PRX Quantum 3, 020344 (2022)](https://journals.aps.org/prxquantum/abstract/10.1103/PRXQuantum.3.020344); fitting HQMMs is established in [Srinivasan, Gordon and Boots, AISTATS 2018](https://proceedings.mlr.press/v84/srinivasan18a.html); CP realization/lifting obligations are studied by [Monras and Winter, TQC 2014](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.TQC.2014.99). The earlier received sources retain the Singer/equivalence and temporally correlated-noise decoding prior-art credits. No broad recovery-regret/depth novelty is inferred here.

Dependencies are the received IC-port theorem, `COUNT_CERTIFIED_PHYSICAL_RESIDUAL_SIMULATOR.md` (SHA `59b53f8b7a4d54e2f38cb7eb3d643c13d4b356646a3de14967dfa1df6d0da6f2`) and `RAW_JOINT_CORE_RESIDUAL_ACQUISITION.md`. This source does not alter their bytes or transfer their receipts to this coherent upgrade. `complete_port_physical_residual_check.py/.json` is a separate completed PASS author diagnostic, not independent receiving, statistical acquisition, generic physical fitting, or a generic decoder/compiler run. Its exact qubit fixture uses a full raw rank-four core with masses (1,1/3,1/3,1/3), a distinct mixed fitted start, full unitary and two-outcome nonunitary ports, retained native/local records and coherent Bell-reference recycling. It checks 192 full-port reconstructions on spanning physical inputs, eight complete entangled-reference actions, four exact endpoint telescope branches, and a nonpositive operator-coordinate minor -1/8. The source-to-fit core lift is genuinely non-CP (an exact negative Choi principal minor), yet the physical-suffix endpoint identity holds. Hypothetical width 10^-14 bands give K approximately 85.000000000071, epsilon approximately 0.00003098949, and horizon-three eta approximately 0.00395258. A certified entrywise upper bound on the actual complete endpoint half trace norm is approximately 2.28909 times 10^-7, below eta; this is an upper bound, not a claimed exact trace distance. The candidate need not lie inside those tiny bands in this general residual fixture: its mismatch is paid in (10). The transpose counterexample checks all 36 nonnegative scalar branches and six TP sums despite its negative Bell eigenvalue. These are exact rational/algebraic comparisons; decimals are display only. All source calls, episode starts, RNG and hardware uses are zero. The conservative gap demonstrates no numerical/practical advantage. Receipt status belongs in a separate artifact.
