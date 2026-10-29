# Acquired local frame plus standard five-qubit correction preserves information under unknown non-Pauli product noise

28 October 2026. New bridge candidate; independent review pending. The code and its single-error correction are standard. The contribution being tested is completion of the ACQUIRED FRAME interface: ordinary local calibration supplies an actual inverse operation before a known code, so the result ends in protected logical information rather than only an estimated frame. No advantage over equally informed standard QEC is asserted.

## 1. Actual apparatus and target

A payload qubit is encoded by a known [[5,1,3]] code into five physical inputs. One native block has reduced channel

    N = Ad_V composed (E_1 tensor E_2 tensor ... tensor E_5),

where E_i are initially unknown qubit CPTP channels. V is a fixed unknown output mixer with the local support/physical access promised by the separate acquired-algebra source. Ordinary calibration can prepare and measure every physical input/output; this is stronger than access only to an enclosed logical channel. Calibration finishes before an unknown payload is requested.

For the concrete unknown-axis amplitude-damping family, E_i has unknown fixed damping axis and rate. Its Bloch contraction is symmetric positive definite for rate<1. Thus the received positive-Bloch/positive-operator construction can acquire the V-conjugated qubit algebras from actual signed local responses, without the axes or microscopic environment being supplied. A canonical positive-polar extension can instead target V_eff and residual product channels E_i'; in that case use E_i' and V_eff consistently throughout this theorem, not an unidentifiable original V.

Let the accepted frozen physical receiver Dhat satisfy

    half ||Dhat - Ad_Vdagger||diamond <= zeta

on all five-qubit inputs with arbitrary external reference. This must be an ACTUAL implemented receiver obtained from the finite operator certificates and coherent extraction circuit, not a free inverse oracle. The same receiver can precede the known code decoder R. Its own calibration failure, implementation and control costs are carried below.

The guarantee is for the logical output and arbitrary reference, with the noise environment and receiver syndrome discarded. This is a complete LOGICAL channel norm. It does not assert the same bound for the full joint bath state or an arbitrary future operation that exposes that bath.

## 2. Explicit known encoding and CPTP syndrome recovery

Use commuting stabilizer generators

    XZZXI, IXZZX, XIXZZ, ZXIXZ,

with logical X=XXXXX and Z=ZZZZZ. Let P_C=product_g(I+g)/2. Normalize P_C|00000> to |0_L> and define |1_L>=XXXXX|0_L>. The 32-by-2 isometry C has these two columns.

Let F_a enumerate I and all15 weight-one single-qubit Paulis. Their syndrome sectors are disjoint and exhaust dimension32. Directly,

    Cdagger F_a dagger F_b C = delta_ab I_2.

The16 known Kraus operators R_a=Cdagger F_a dagger give a CPTP decoder because sum_a R_a dagger R_a=I_32. They implement the usual syndrome correction followed by logical decoding. Equivalently the known32-by-32 unitary with blocks R_a maps F_a C|j> to |a>_syndrome tensor|j>_logical. Discarding four syndrome qubits is the decoder; its inverse with four initialized |0> ancillas is an encoder. Their actual finite gate synthesis, routing, initialized ancillas and storage costs are paid. The construction does not presume noiseless syndrome hardware in an implementation claim.

Every single-qubit CPTP channel E_i is corrected EXACTLY by this fixed C,R. Its Kraus matrices lie in the linear span of I,X_i,Y_i,Z_i; the displayed orthogonality and trace preservation give R composed(E_i tensor id_others) composed C=id_L. No knowledge of its damping axis is needed.

## 3. Non-Pauli product bound: all first-order terms cancel

Put Delta_i=E_i-id and p_i=half||Delta_i||diamond. Expand the product channel multilinearly:

    tensor_i E_i = id + sum_i Delta_i + sum_(|S|>=2) tensor_(i in S)Delta_i,

with identities on other sites. Exact single-site correction implies R Delta_i C=0. Complete CPTP pre/post-processing contracts diamond norm; its tensor norm is submultiplicative. Therefore the EXACT-INVERSE logical channel L_* obeys

    half||L_*-id_L||diamond
      <= min(1, (1/2)[ product_i(1+2p_i)-1-2 sum_i p_i ]).    (1)

This is a conservative expansion bound, not a binomial Pauli-error probability. It applies to nonunital and coherent single-qubit channels as long as the actual reduced block channel is the declared product. For p_i<=p the right side before clipping is

    20p^2+40p^3+40p^4+16p^5.

The learned inverse adds at most zeta by complete contractivity:

    half||R Dhat N C-id_L||diamond <= min(1,B(p_1,...,p_5)+zeta). (2)

On a simultaneous calibration good event, zeta is deterministic for the frozen matrices. For a complete protocol sharing abort branches, add the bad-certificate probability beta once and a WHOLE encoder/native-interface/learned-receiver/known-decoder implementation discrepancy nu. Conditional-on-acceptance risk retains its denominator; finite caps may abstain.

A convenient conservative AD parameter bound avoids assuming an unexecuted diamond SDP. With rate gamma, K0=diag(1,sqrt(1-gamma)) and jump K1, the identities

    K0 rho K0-rho=(K0-I)rho K0+rho(K0-I)

and ||K0||<=1, ||K1||^2=gamma give

    p_AD <= 1-sqrt(1-gamma)+gamma/2 = gamma+O(gamma^2).

Unitary rotation of the damping axis leaves this bound unchanged. Substituting these upper bounds in (1) proves quadratic suppression in the physical AD rates without reconstructing their axes. No claim that this elementary bound is the exact diamond distance is needed.

## 4. Calibration and complete-system bill

The inverse certificate must be accurate enough to reveal the code's quadratic gain. Set zeta=O(p^2), beta=O(p^2), and total physical implementation error nu=O(p^2). A control/encoder/decoder error floor of order p would mask the nominal improvement. Unknown p does not automatically provide a stopping rule: use a supplied service error target, or a separately acquired valid local-channel bound, and account for that acquisition.

For the ordinary operator-norm inverse route, sufficient per-generator error is delta<=zeta/(3n), n=5. The actual three-controlled-reflection extraction uses15 controlled blocks and five fresh mixed receiver qubits. The original five noisy carriers are discarded after extraction; known code decoding then returns one logical qubit and discards its four syndrome qubits. Mixed-state preparation, control delivery, all storage time, rotations and finite synthesis are real resources.

At fixed local support width and positive conditioning, the conservative ordinary acquisition scales as inverse-square in zeta, hence O_tilde(p^-4) calibration BLOCK calls for zeta~p^2, with substantial width/contrast/Gram or positive-block conditioning factors. Every block contains five physical preparations, native exposures and readouts. General positive-operator fitting can carry additional large finite computation costs. This is not efficient fault-tolerance merely because the formal error is quadratic.

If a fixed source/mixer remains valid for B later independently initialized code blocks, the same frozen inverse can be reused; total native carrier exposure is five times(calibration blocks+B), before additional reset/control operations. A joint B-block output bound can accumulate at most B(B_native+zeta)+beta+nu_total by an ordinary channel hybrid under the ACTUAL appropriate independent/product channel contract. The calibration failure is paid once, not B times. Amortization lowers calibration cost per block but does not remove the accuracy requirement or accumulated physical error. No new measurement of an unknown payload is used for training.

## 5. Memory, correlations and fair comparator

A reduced product channel from one reset environment does not imply a product complete-memory instrument. For a single logical use with initially independent environment, (1) is reference-complete after tracing that environment. Repeated interaction with a coherent retained bath needs a stronger operational/process promise and is NOT justified by tensoring this one-use reduced statement. The separate acquired-inverse complete-norm bound alone does not turn native noise into a product process.

If a classical latent component selects a whole product block, (1) can be averaged component-wise when every component has the stated small p_i bounds. A product of averaged marginals is not the actual mixture. Arbitrary correlations are excluded: with probability p applying XXXXX produces a logical X with probability p despite each physical marginal having error p. This violates quadratic suppression based only on marginal errors.

The equally informed ordinary comparator is exactly the same known five-qubit code and decoder after the same learned frame. Its performance is identical. The code is not a new invention, and the quadratic cancellation is standard QEC algebra. A curve omitting the inverse diagnoses the unknown-frame obstruction, not a superiority claim over conventional adaptive QEC.

## 6. Reproducible complete-channel fixture and its limits

learned_five_qubit_nonpauli_bridge_20261028.py constructs the32-by-2 encoder and all16 recovery Kraus operators, verifies all256 Knill–Laflamme matrix-pair identities, and exactly corrects five arbitrary-axis single-site AD channels numerically. It uses a fixed nontrivial block-local mixer V12 tensor V34 tensor V5 and five different unknown damping axes.

For each two-qubit or one-qubit block it constructs the actual three-axis noisy contrasts, adds explicitly bounded deterministic Hermitian perturbations, Gram-whitens, takes signs, and builds the actual mixed-ancilla controlled-reflection extraction channel. It then propagates the full logical matrix basis through encoding, native non-Pauli channels, mixer, learned receiver and syndrome recovery. No inverse oracle is substituted for the learned receiver in that curve.

The six maximum-rate fixtures gamma=.08,.04,.02,.01,.005,.001 show quadratic logical scaling. At gamma=.01 the learned-receiver logical entanglement infidelity is approximately1.5769e-4; its normalized-Choi half-distance gives a diagnostic half-diamond lower bound and twice that distance an upper bound. These floating channel bounds are not interval-certified numerical theorems. The analytic bound (1)-(2) is the governing guarantee.

The perturbations are NOT RNG-acquired Born counts. Guard evaluations are floating diagnostics, not outward-rounded rational acceptance certificates. The separate acquisition theorem provides the procedure and statistical bill; this fixture tests composition and actual CPTP mechanisms. For example its deliberately conservative contrast radius at gamma=.01 is1e-8, which would make the basic16*3^W*L/a^2 bank prescription enormous. No feasible calibration budget or hardware implementation is claimed.

## Sources and dependencies

Primary standard-code sources: Laflamme, Miquel, Paz and Zurek, Perfect Quantum Error Correction Code, https://arxiv.org/abs/quant-ph/9602019 ; Knill and Laflamme, A Theory of Quantum Error-Correcting Codes, https://arxiv.org/abs/quant-ph/9604034 . Their standard general single-qubit correction claim is the baseline; the explicit matrices above are independently checked in this fixture.

Acquisition dependencies retain their own exact receipts: ordinary_unknown_axis_positive_bloch_whitening_20261028.md; positive_operator_clifford_acquisition_20261028.md; ordinary_local_inverse_coherent_memory_fallback_20261028.md; local_noise_polar_identifiability_extension_20261028.md. Do not infer acceptance of this new code composition from their receipts. No historical novelty, broad unknown-noise solution, threshold or practical advantage is established by this scoped bridge.
