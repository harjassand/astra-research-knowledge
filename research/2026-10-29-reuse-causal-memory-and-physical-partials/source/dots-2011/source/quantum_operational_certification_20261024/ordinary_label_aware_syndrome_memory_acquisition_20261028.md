# Label-aware syndrome exploration with complete retained-memory control

28 October 2026. **New candidate, independent receiving pending.** This source preserves the earlier stationary injection source and all receipts. It gives (A) its concrete physical retained-memory extension and (B) a stronger same-port coordinate learner. No source outcomes are simulated by the companion exact check. No generic-error, threshold, practical advantage or priority claim is made.

## 1. Actual physical interface, and two distinct structural promises

A known repetition encoder maps |l> to |l l l>. Its three output wires are exposed BEFORE an unknown physical bit-pattern instrument and a fixed unknown three-qubit mixer V. Fresh calibration bits select e uniformly from E={000,100,010,001}, then apply the corresponding known X_e. Logical input probes are independent uniform X/Z eigenstates with sign s. After the unknown source, all three physical outputs undergo ordinary random product-Pauli measurements. The injection label e is a known control record, not a syndrome flag returned by the source. It costs two fair bits and at most one extra physical X, in addition to the known encoder's two CNOTs, two resets, input preparation and readout. There is one unknown-channel call per block. Injection is OFF for payload service.

Allow arbitrary incoming quantum memory M and outgoing retained memory M'. At each complete prior history h, the physical noise is

    N_h = (Ad_V tensor id) o sum_f (Ad_Xf tensor F_(f,h)),             (1)

where f ranges over three-bit patterns, each F_f:M->M' is CP and T=sum_f F_f is TP. V is fixed across calibration and service; the F_f may depend arbitrarily on time and exposed past history, but not on current private axis, sign, injection or readout labels except through the quantum physical input as specified by (1). This is a classical physical-X error label with arbitrary coherent retained memory, not an arbitrary joint system-memory unitary.

Part A uses the stronger physical mixture-of-iid form

    F_f = sum_a p_a^|f| (1-p_a)^(3-|f|) K_a,
    0<=p_a<=1/2, sum_a K_a TP, K_a CP.                            (2)

An unobserved memory instrument selects the error rate before the three conditional iid physical flips. The K_a can preserve/coherently transform memory; they need not be rank one or commute. Rates and the instrument can change at every past history. They are not supplied numerically. Formula (2) also covers countable/integral instruments if the maps converge, but all exact fixtures use finite instruments.

Part B needs only the THREE qualitative CP inequalities

    H_i := sum_f (-1)^(f_i) F_f is CP,  i=1,2,3.                    (3)

Always T-H_i=2 sum_(f:f_i=1) F_f is CP. Independent physical flips with possibly unequal, history/instrument-dependent p_(a,i)<=1/2 satisfy (3). General correlated CP error-pattern instruments can also satisfy it. No positive numerical bias, spectral gap, majority-sector dominance or noise stationarity is supplied. These are model promises, NOT conclusions certified from finite data. Part A implies (3), but Part B is genuinely wider.

The final recovery comparison always concerns the same fixed majority subsystem U=V U_maj, U_maj|l,g>=|l*111 XOR e_g>. Its exact extraction is D_*=Tr_G Ad_Udagger. For arbitrary (1), uninjected payload blocks are F_(e_g) and F_(e_g XOR111) in gauge g, so the complete Pauli/gauge form remains valid. D_* is a full-CPTP Bell-loss oracle only under the separate CP inequalities F_(e_g)-F_(e_g XOR111)>=_CP0 for every g. They hold for (2), including mixtures at every memory history. They do NOT follow from (3).

## 2. Part A: complete-map excitation for mixture-of-iid memory

Let A_I,g=(1/4)sum_e F_(e XOR e_g) and A_X,g=(1/4)sum_e F_(e XOR e_g XOR111). The injected channel, including memory and every off-diagonal logical matrix unit, is exactly

    E_cal = (Ad_U tensor id) o sum_g [id_L tensor |g><g| tensor A_I,g
                                  +Ad_X tensor |g><g| tensor A_X,g]. (4)

Here a displayed tensor with a memory map means the corresponding map L M->L G M'. The underlying equality X_(e XOR f) Enc|l>=U_maj|l XOR alpha(e XOR f),g(e XOR f)> has no phase and therefore proves (4) on all operators, not only classical states.

For EVERY physical f, the four e labels put one representative in each complement pair {e_g,e_g XOR111}. Therefore, for arbitrary (1),

    A_I,g+A_X,g=T/4.                                             (5)

The full injected mixed-input joint output is consequently I8/8 tensor T(omega), after V, on EVERY memory operator omega. This is complete physical-output/retained-memory decoupling for the averaged calibration input. It does not assert that individual observed readout branches leave memory unchanged.

For (2), writing t_a=1-2p_a, the signed gauge CP maps are

    A_I,0-A_X,0=sum_a [(3t_a-t_a^3)/8] K_a,
    A_I,g-A_X,g=sum_a [(t_a+t_a^3)/8] K_a, g!=0.                  (6)

All coefficients are nonnegative. H_X,g=T/4. Thus the earlier margin-free common-algebra theorem applies to the SAME fixed U with no supplied numeric kappa. At a prior memory state omega, let

    c(omega)=sum_a Tr[K_a(omega)] (t_a+t_a^3).

The least signed gap is c(omega)/16. At any finite reached bank its predictable-average least gap is the average c/16, because all contrasts have the same fixed U and positive gauge blocks. The nominal stationary p^-2 rare-syndrome penalty is absent when the actual average c is bounded away from zero, including noise-free memory branches. Persistent informative histories, a funded finite cap, and the accepted-risk/implementation qualifications of the received theorem still matter. Arbitrarily long all-p=1/2 episodes can cause abstention. Marginal flatness alone does not certify the signed gap.

Because future payload has injection OFF, its logical loss and memory instrument are the original ones, not the noisier calibration mixture. The complete operator certificate transfers to every future gauge/memory state of the same U. A future mixture of iid rates in [0,1/2] retains oracle dominance; more general future (1) only retains the specified exact-extraction comparator unless separately dominant. This is an actual memory mechanism, not an assumption that the calibration output is iid or its conditional memory unaffected by measurement.

## 3. Part B: the injection labels reveal physical-coordinate contrasts

Part A averaged the injection label before assigning the logical sign. Retain that label in a different, fully legitimate estimator. For logical Z input with sign s=(-1)^l, the prepared computational string is x=l*111 XOR e. As l and e range uniformly, x is uniform over ALL eight strings. Its i-th known bit sign is

    u_i=s (-1)^(e_i).                                             (7)

For a physical output shadow Z_out=tensor_k(3 Pi_(a_k,b_k)-I), use the FOUR actual records

    Y_X=2 1{j=X} s Z_out,
    Y_i=2 1{j=Z} s (-1)^(e_i) Z_out, i=1,2,3.                    (8)

They are computed from the SAME block. They are correlated; no sample independence, cloned outputs, incompatible measurements or extra channel calls are claimed. The current e label is averaged inside the conditional mean even though its known sign is multiplied into the statistic. It is not exposed to a source choosing F_f in advance of its current action.

Define C_X=V(X1 X2 X3)Vdagger and C_i=V Z_i Vdagger. On every complete prior record with conditional source memory omega,

    E[Y_X|past]=C_X/8,
    E[Y_i|past]=C_i Tr[H_i(omega)]/8.                             (9)

The stronger output-plus-memory signed operator identities, BEFORE tracing M', are C_X/8 tensor T(omega) and C_i/8 tensor H_i(omega). To prove the latter, sum over uniform x and change variable y=x XOR f:

    (1/8)sum_x (-1)^(x_i) |x XOR f><x XOR f|
       =(-1)^(f_i) Z_i/8.

For X input, uniform e maps its signed input operator to X1 X2 X3/8. Every X_f commutes with that operator. Both calculations extend by linearity to all memory matrix units and any memory reference. Output product-shadow unbiasedness then proves (9).

Under (3), theta_i=Tr H_i(omega) lies in [0,1]. Thus every reached bank has predictable contrasts C_i*theta_bar_i/8, with no unknown eigenbasis or gauge weight; all nonzero eigenvalues have equal magnitude. Its sign is the SAME fixed C_i whenever theta_bar_i>0. The X gap is always exactly 1/8. Different physical-coordinate generators may be informative in different stages and permanently retained. There is no requirement that all theta_i be positive at each call.

For (2), all theta_i=sum_a Tr K_a(omega) t_a. Its label-aware coordinate gap is theta_i/8, at least the Part A minimum c/16 and at most twice it when theta_i>0. This compares INFORMATION GAPS, not complete acquisition source budgets: Part B estimates more operators and requires tighter component accuracy, so it is not a proved statistical dominance result.

## 4. Finite certified coordinate learner and literal majority extraction

The physical patch is known width three; no support search is necessary. Set d=8, choose rational 0<epsilon<=1, 0<beta<=epsilon/8 and a supplied finite stage cap S>=0. Let b be the largest positive dyadic with b^2<=epsilon/18 (hence b<=1/4), and set c=b/8. For s=0,...,S use fresh banks

    a_s=2^(-s)/(16d),
    L=ceil log2(8d(S+1)/beta),
    N_s=8*3^3*L/a_s^2.                                           (10)

Every N_s is an integer. Use the four records (8) and the received finite rational Jacobi primitive. The same matrix martingale argument as the received margin-free source applies: each conditional second moment is <=2*3^3 I, every centered increment has norm <=4d, and a union over FOUR matrices and S+1 stages gives, with probability at least 1-beta,

    ||Deltahat_v,s-Delta_bar_v,s||op<=a_s                         (11)

simultaneously for every reached bank v=X,1,2,3. This remains true under arbitrary coherent retained memory and correlations between the four records. No conditioning on a favorable future excitation event is performed.

For each unresolved v, obtain C=Q D Qdagger with exact rational unitary Q and residual ||C-Deltahat||F<=a_s/4. Let e_s=5a_s/4 and h=min|D_kk|, and retain S_v=Q sign(D) Qdagger at its FIRST stage passing

    h>e_s,       2 e_s<=c(2h-e_s).                              (12)

All comparisons and operators are rational and finite. On (11), the received opposite-sector sign lemma gives ||S_v-C_v||op<=c. If a true stage gap gamma_v satisfies a_s<=c gamma_v/5, the guard passes. The X generator has gamma_X=1/8; the i-th coordinate has gamma_i=theta_bar_i/8. If an item never becomes informative within the cap, ABSTAIN before requesting an unknown payload. Saved certificates remain valid at later stages because V and C_v are fixed.

Once all four items are certified, form the KNOWN Hermitian rational matrix T_hat=S_1+S_2+S_3. Apply finite rational Jacobi again to construct C_hat=Q_0 D_0 Q_0dagger with ||C_hat-T_hat||F<=b/8. Define the exactly physical reflection

    S_Z=Q_0 sign(D_0) Q_0dagger,       S_X=S_X-record.             (13)

Do NOT assume that the learned S_i commute. The true T=C_1+C_2+C_3 is V(Z1+Z2+Z3)Vdagger; its spectrum is {3,1,-1,-3}. Its sign is the true majority observable

    B_Z=V(Z1+Z2+Z3-Z1 Z2 Z3)Vdagger/2,
    B_X=C_X.                                                     (14)

The actual perturbation satisfies ||C_hat-T||op<=3c+b/8=b/2. The sign lemma at true gap 1 yields

    ||S_Z-B_Z||op<=b/(2-b/2)<b,
    ||S_X-B_X||op<=c<=b.                                         (15)

No unknown spectral basis, exact commuting fit or nonphysical polynomial in approximate reflections is used. The final receiver is the literal three-controlled-reflection SWAP construction with one mixed receiver qubit, then discard all original physical outputs. It is CPTP on every accepted record, including bad ones. The received complete-reference bound gives, for EVERY future gauge state and its coherent memory/reference,

    ell_0(g)<=3[delta_Z(g)+delta_X(g)/2]<= (9/2)b^2<=epsilon/4.   (16)

This is the operator-uniform majority-subsystem certificate needed by the received complete CP-domination theorem. Subsequent finite adaptive service requires fresh privately retired frame keys, discarded gauge/receiver records, the SAME common controller, and its paid whole-horizon resources. Nothing here re-proves or weakens those requirements. Its comparator is the PARTICULAR exact-majority extraction process, not a collective recovery oracle or ideal computation.

## 5. Finite resources, completion, accepted risk

All elapsed geometric stages count. Exact maximum source cap is

    N_base (4^(S+1)-1)/3,  N_base=8*27*L*(16d)^2.                  (17)

If every unresolved coordinate's reached-bank predictable bias is persistently >=theta_*>0 almost surely, the first sufficient scale a_s<=b theta_*/320 is within the funded cap, and the simultaneous event holds, all certificates are acquired by that scale. More generally each item needs its own sufficiently informative reached stage; mere eventual information does not bound the waiting cost. With gamma_*=min(1,theta_*)/8, the first sufficient bank costs

    N_s < 51200*27*L/(b^2 gamma_*^2),
    cumulative calls < (4/3)N_s = O_tilde(27/(gamma_*^2 epsilon)). (18)

The constants deliberately pay the tighter c=b/8 component fits. This is an instance rate, not floor-free worst-case success; gamma_* is not an algorithm input. The first-stage case also obeys the displayed loose bound since b<=1/4 and gamma_*<=1/8. All copies of the source prepare three physical qubits and measure three outputs. Four 8-by-8 known matrices, finite rational rotations, readout-axis generation, exact comparisons, injection controls, synthesis/routing and their errors are paid. No global channel SDP or V inverse is supplied.

Let nu_cal bound the discrepancy of the full retained calibration record (including frozen labels, acceptance and stopping), and let nu_svc uniformly bound the complete one-service implementation error at its ACTUAL future memory. Take nu_cal+nu_svc<=epsilon/4. Every good accepted physical record gives (15) independently of subsequent gauge states, so false accepted certificates have probability <=beta+nu_cal. As in the received parent,

    E[1_accept (ell_actual-ell_exact/current_oracle)]
       <=epsilon/4+beta+nu_cal+nu_svc<epsilon.                    (19)

The oracle term requires the separate future dominance promise. Conditioning on acceptance divides bad mass by Pr(accept); no record-by-record posterior theorem is claimed. A proved nominal fast-completion record event transfers with nu_cal; a favorable physical memory trajectory cannot silently replace the declared one. Additional readout-axis sampler exhaustion and arithmetic/synthesis budgets lie inside the stated implementation allowance. Calibration input has no unknown payload; the caller supplies it only after acceptance.

## 6. A class extension, and the preserved failure boundary

Take stationary independent flips with p=(1/4,1/4,1/100). All three coordinate biases (1/2,1/2,49/50) are positive, so Part B can acquire the true majority algebra. But even NATIVE majority gauge e=001 has signed weight

    w_001-w_110=9/1600-99/1600=-9/160<0.

Uniform syndrome injection also has negative majority sectors for some unequal-rate examples (the companion check supplies an exact witness). Thus a majority raw-sign learner cannot simply invoke the old nonnegative-majority-contrast theorem on this broader family. Coordinate acquisition bypasses that orientation obstruction by exploiting the actual known PRE-noise injection label, not by assuming its desired majority sign.

The majority decoder need not be optimal here: for the displayed p its loss is 53/800 while the optimal syndrome decision has loss 1/100. This is why (19) distinguishes its exact-extraction comparator from an oracle. In the equal-rate mixture-of-iid subclass, ordinary majority dominance holds completely and the oracle label is justified at each actual memory state.

Native deterministic X1 noise is perfectly correctable, but is outside (3). Under uniform injection its majority signed blocks are (1,1,-1,-1)/4; raw signs select a different logical orientation on two gauge sectors. Reusing that orientation after future deterministic X2 can fail. Neither native correctability nor full calibration marginal I8/8 certifies the fixed majority orientation. This preserved failure is not evaded by claiming that arbitrary active mixing preserves model structure.

The strongest equally informed conventional learner receives exactly the same pre-noise port, labels, source promise and controls; it can use (8)--(15). This is a finite physical information-and-control construction, not a quantum advantage claim. It does not solve general unknown-code acquisition or unknown microscopic-environment identification.
