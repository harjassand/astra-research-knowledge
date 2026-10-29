# Acquire a syndrome-conditioned receiver without normalizing rare branches

28 October2026. Author derivation, source-informed numerical oracle and explicit counterexample. Independent review requested. This is channel-adapted recovery using ordinary qubit instruments and SDPs, not a new optimization algorithm or a claimed advantage over equally informed standard methods.

## Instrument and correct objective

Let E_s be the actual trace-decreasing qubit-input to qubit-output channel conditioned on terminal syndrome s, BEFORE the final syndrome-conditioned correction. Its Pauli transfer matrix is

    M_s = [[a_s,b_s^T],[c_s,T_s]].

The sum over s is TP; individual branches generally are not. A deterministic CPTP qubit receiver D_s has transfer matrix [[1,0],[t_s,R_s]]. The complete instrument-and-receiver channel has entanglement fidelity

    F_e = (1/4) sum_s [a_s + b_s dot t_s + Tr(R_s T_s)].

This follows from F_e(Lambda)=Tr(M_Lambda)/4 and matrix multiplication. Importantly b_s describes input-dependent syndrome probability. Its dot product with receiver translation is absent from the TP single-channel quasi-inversion objective, but present here. Applying a TP Procrustes/unitalization theorem separately to normalized syndrome branches is invalid in general: the conditioning is input dependent and not a linear TP channel.

Use unnormalized recovery Choi J_s on output tensor input, J_s>=0, Tr_output J_s=I. Define

    C_s = (1/8) sum_(i,j=0)^3 (M_s)_(j,i) sigma_i tensor sigma_j^T.

Then the branch objective is Tr(C_s J_s), including terms which vanish under the TP constraint. The exact optimum separates into S four-by-four SDPs. The dual is minimize Tr(Y_s) subject to I tensor Y_s>=C_s. All syndrome branches count, without postselection. Per-branch unitary optimization is the proper SO(3) Procrustes solution for T_s, with a_s added as the constant term; it is generally a lower bound on full CPTP recovery.

## Strict nonunital example and a useful failure on the actual pipeline

Consider two branches E_0(rho)=<0|rho|0>I/2 and E_1(rho)=<1|rho|1>I/2. Every conditional unitary leaves the mixed output unchanged, giving total F_e=1/4. Resetting the output to |s> using the syndrome gives F_e=1/2, which is optimal since this channel is entanglement breaking. Adding a distinguished identity branch of probability1−p and weighting these branches by p gives full optimum1−p/2 versus unitary optimum1−3p/4. The analytic CPTP upper bound also follows directly: each erased branch can only produce a density matrix, whose Bloch vector has norm at most1. At p=.2 the respective values are.9 and.85. This example is elementary; no historical novelty is claimed.

The actual noisy pulse-pipeline instrument was obtained from continuous_inverse_control_20261028/endpoint_instrument_v1.json, after actual unknown-input encoding,32 native uses,16 noisy EC windows, the actual inverse Clifford and four measured syndrome bits. It precedes the final one-unit correction. Full CPTP optimization gives F_e=.8159958704865569, while unitary-only gives.8159958707849425. The summed numerical dual upper is.8159958708169421. These agree within solver tolerance; there is NO meaningful nonunital advantage in this instance. The prior actual noisy lookup receiver gives approximately.8155702929. Its difference from the ideal endpoint oracle is only about.000426, before paying for different receiver synthesis/time. That tiny source-informed ceiling is not a demonstrated practical gain and does not justify an expensive acquisition claim.

All optimization values here are floating numerical diagnostics, with saved primal CP/TP residuals, dual slack eigenvalues and solver statuses. They are not outward-rounded exact certificates. The strict erased-branch fixture is analytically exact, independently of the solver. Physical implementation of a general CPTP receiver, including reset ancillas, timing, noise and output SPAM, remains separate. An ideal optimized endpoint cannot replace the executed one without paying those costs.

## Ordinary unnormalized data

On every fresh trial choose input axis j uniformly from X,Y,Z and sign u uniformly from±1; prepare rho_ju. Independently choose output measurement axis k uniformly and observe sign v and syndrome s. For each branch h, record the vector/matrix estimates

    a_hat_h: 1{s=h},
    b_hat_h,l: 3u 1{j=l,s=h},
    c_hat_h,l: 3v 1{k=l,s=h},
    T_hat_h,lm: 9uv 1{k=l,j=m,s=h}.

Average these records over ALL N trials, not only trials having branch h. Direct summation over the private settings and Born outcomes gives unbiased estimates of M_h. No probability p_h is divided out. One record's squared Euclidean norm over the entire 16S-dimensional transfer array is1+9+9+81=100, independent of how many branches exist or how rare a particular one is.

For independent trials of one frozen stationary instrument, let E_N be the combined Frobenius estimation error. Independence gives E E_N<=10/sqrt(N). Changing one record changes E_N by at most20/N. McDiarmid therefore gives, with probability at least1−beta,

    E_N <= 10[1+sqrt(2 log(1/beta))]/sqrt(N) = eta_N.

This is a deliberately simple dimension-free vector concentration bound; converting to the S independently chosen receivers incurs a branch factor. For a qubit CPTP D, the full transfer matrix has Frobenius norm at most2: its unnormalized Choi is PSD with trace2, so Tr(J_D²)<=4, and Pauli orthogonality identifies these squared Frobenius norms. Consequently every candidate receiver family has score-estimation error at most sqrt(S) eta_N/2. An empirical optimizer whose objective is within zeta of the empirical optimum obeys

    F_e(optimal true receiver) − F_e(chosen receiver)
        <= sqrt(S) eta_N + zeta.

The optimizer is constrained to physical CPTP receivers even when empirical instrument estimates are not CP. The additive objective error zeta must be verified or honestly retained, not replaced by a numerical solver success label. This theorem guarantees performance of the ideal selected CPTP channels; it does not certify their noisy implementations. No inverse rare-branch probability appears. The bound may be loose and vacuous at modest N; no finite sample superiority is claimed.

A fresh direct whole-pipeline holdout, after compiling the actual selected receivers, can certify the operation actually used. Such a holdout cannot reuse selection data or the old fixed-receiver probabilities. Calibrated tester assumptions are explicit in ../terminal_decoder_scope_20261028/WHOLE_PIPELINE_TESTER_CERTIFICATE_v1.md.

## Restricted reset policy needs even less information

If a branch receiver is restricted to discard-and-prepare, its optimum prepares the pure Bloch direction b_s/||b_s|| when b_s!=0; its score is(a_s+||b_s||)/4. It needs only input setting/sign and syndrome, not output measurements or T_s,c_s. Replacing b_s by an unnormalized estimate yields branch regret at most||b_hat_s−b_s||/2, by the support-function inequality. Thus reset proposal acquisition also need not resolve rare outcomes conditionally. This is a restricted classical-record recovery policy, not preservation of the branch's original quantum coherence.

## Dependencies and preservation

The new oracle program only READS the frozen instrument. It writes separate receiver models and diagnostics in this folder. No earlier proof, received artifact or simulated count bank is altered. The original endpoint source, inherited frame-acquisition costs, mandatory-link/no-bypass promise, native/background model and physical resource comparisons remain in force. Historical background is ordinary channel-adapted recovery SDP machinery (including Fletcher–Shor–Win); this note does not supersede any full-CPTP recovery result.

## A sharp bound on what nonunital branch recovery can add

Define the record-dependence quantity L=sum_s||b_s||, where E_s†(I)=a_s I+b_s dot sigma. Positivity of each effect implies||b_s||<=a_s and total TP implies sum_s a_s=1, so0<=L<=1. Then

    0 <= F_e(best CPTP branch receivers)−F_e(best unitary branch receivers)
      <= L/4 <= 1/4.

Proof: every qubit CPTP map with affine parameters(t,R) has a unital CPTP map with the SAME R. For completeness, define the qubit spin flip S(X)=sigma_y X^T sigma_y. Although S alone is not CP, S composed with D composed with S is CP, with Kraus operators sigma_y K_l^* sigma_y, and is TP when D is TP. Its affine parameters are(−t,R). Averaging it with D therefore gives(0,R). Every unital qubit CPTP map is mixed-unitary: rotate the real R to signed diagonal form by proper left/right rotations; positivity of its Choi matrix says the resulting diagonal entries lie in the Pauli-channel tetrahedron, and its four vertices are Pauli unitaries. Undoing the rotations gives the mixed-unitary decomposition. Thus Tr(R T_s) cannot exceed the best unitary value. The remaining translation contribution satisfies b_s dot t<=||b_s|| because D(I/2) is a state and ||t||<=1. Sum the branch objectives to prove the bound.

The erased-record example attains L/4, including the identity-mixture parameter p where L=p. Hence no smaller coefficient works uniformly over qubit instruments. In particular, when the syndrome distribution is independent of the logical input (all b_s=0), branch unitaries attain the full CPTP optimum. This does not mean a fixed conventional Pauli lookup is optimal; coherent unitary refinements may still help. It also does not extend the qubit mixed-unitary step to higher output dimension.

The actual physical-pipeline instrument has L/4=.0000009505683474412754. This source-informed diagnostic is an analytic ceiling on any benefit specifically requiring nonunital branch recovery, before its physical costs. It explains why the full CPTP and unitary SDPs agree numerically and is more informative than pursuing that tiny apparent difference. A certificate from experimental records would replace each b_s by an estimate and add its norm confidence radius; source parameters are not supplied to a learner here.

Operationally, b_s is exactly the part of the terminal classical record that distinguishes input states. Approximate input-independence therefore limits how much a reset/nonunital receiver can add beyond coherent per-branch controls. This is a scoped mathematical connection between classical record leakage and receiver choice, not a new noise-independence assumption or a general statement about arbitrary environment access.

## Exact record-channel interpretation of the bound

Let M_record map the input qubit to the actual classical syndrome record, and let K_record be the input-independent record channel having the probabilities induced by the maximally mixed input:

    M_record(rho)=sum_s Tr[(a_s I+b_s dot sigma)rho]|s><s|,
    K_record(rho)=Tr(rho) sum_s a_s |s><s|.

Then, with the ordinary unhalved diamond norm,

    ||M_record−K_record||_diamond = sum_s ||b_s|| = L.

For the upper bound, the scalar functional X maps to Tr(B_s X), with B_s=b_s dot sigma, has diamond norm||B_s||_infinity=||b_s||. This follows equivalently by duality from the completely bounded operator norm of the map z maps to z B_s. The block-diagonal classical output and triangle inequality bound the total by the sum. For the lower bound, feed a normalized Bell state with a retained qubit reference. The s block of the difference output is B_s^T/2, with trace norm||b_s|| because its two eigenvalues are plus/minus||b_s||/2. All branch contributions are attained by the SAME Bell input, giving equality.

Consequently the general receiver-choice bound can be written

    full CPTP receiver advantage over branch unitaries
        <= (1/4)||M_record−K_record||_diamond.

Equivalently it is at most half the reference-complete trace-distance distinguishability between this syndrome record and the specified input-independent record. The comparator K_record is fixed by maximally mixed input probabilities; this is NOT a minimization over all constant records. The theorem concerns the actual classical record channel, not an arbitrary unmeasured environment, and it does not infer future-memory decoupling. An instrument whose terminal record is nearly independent even of an input reference cannot obtain a large nonunital recovery premium from that record. Equality is attained by the erased-record fixture above. The use of qubit spin flip/mixed-unitary structure is essential; no corresponding higher-dimensional equality or premium bound is asserted here.

## Fixed-record sharpness, not only a special example

In fact the bound is sharp for EVERY fixed qubit POVM {F_s=a_s I+b_s dot sigma}. Among all quantum instruments having this same classical record channel, the largest possible full-CPTP-versus-unitary receiver premium is exactly L/4. The preceding argument is the upper bound for every such instrument. For attainment, use the erased-output instrument

    E_s(rho)=Tr(F_s rho) I/2.

It is CP, has exactly the prescribed POVM, and its sum is TP. Any branch unitary leaves the output I/2, so its total entanglement fidelity is1/4. An arbitrary branch receiver can replace I/2 by a pure state with Bloch vector b_s/||b_s|| (any state if b_s=0), attaining total fidelity(1+L)/4. This realizes premium L/4 and proves the fixed-record supremum is achieved.

Thus the exact record-channel distinguishability has a precise extremal operational meaning: it is four times the largest additional Bell fidelity that nonunital receiver operations can provide, beyond all branch unitaries, for an instrument with that record POVM. Attainment uses an explicitly erased output; it is not an assertion that every instrument achieves the bound or that the erased-output channel preserves quantum coherence. The result is a qubit statement with classical records and all outcomes included, not postselection.
