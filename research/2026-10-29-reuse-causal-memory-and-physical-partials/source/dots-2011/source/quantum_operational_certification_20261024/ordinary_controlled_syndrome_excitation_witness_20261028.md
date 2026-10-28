# Paid pre-noise syndrome injection removes the rare-noise excitation bottleneck in a concrete code

28 October 2026. **New author-derived candidate witness; independent receiving pending.** This is a changed, explicit physical access contract, not an operation silently available at the original logical black-box port. The native-noise repetition witness and all earlier sources remain unchanged.

## 1. Extra access and the actual operation

The calibration apparatus exposes the output of a KNOWN three-qubit repetition encoder BEFORE an unknown physical channel consisting of independent bit flips with probability p in [0,1/2] followed by a fixed unknown three-qubit unitary V. The usual encoded codeword is |0> -> |000>, |1> -> |111>. In addition to ordinary logical Pauli probes, the learner may apply a known physical X on one encoded wire before the unknown channel. It must genuinely have this intermediate control port; knowing the abstract encoder is not enough if that port is enclosed inside an inaccessible source.

For every calibration call, draw two fresh private fair bits and uniformly select one operation from

    {I, X1, X2, X3}.                                  (1)

Apply it AFTER the known encoder and BEFORE the unknown physical noise and V. Then use the actual ordinary input labels and output product-Pauli readout required by local gap acquisition. This is a classical mixture of ordinary encoded probes, not an entangled calibration-reference bypass, control of an inaccessible environment, or a free gauge-preparation oracle. The current injection label is averaged in each conditional feedback mean; it must not be exposed to a source choosing its current noise map before that map is fixed.

Pay two random bits and at most one extra physical one-qubit X gate per calibration block, along with the known encoder's resets and two CNOT gates, all physical qubit traffic, timing and control errors. There is no extra unknown-channel call per probe. The ordinary Pauli probe and actual readout schedules remain unchanged. TURN OFF the injection for the genuine payload service. It is an exploration operation, not an advertised improvement to the payload code.

The unknown V is fixed and may entangle all three outputs. Thus applying a local Pauli AFTER V is not a substitute for (1): the corresponding pre-V action is generally unknown. Post-source depolarization can fill an output marginal while destroying its signed contrasts and does not establish the certificate proved here.

## 2. Fixed logical subsystem, changed calibration gauge blocks

Let e_g be the four bit strings 000,100,010,001 and let U_maj|l,g>=|l*111 XOR e_g>. Set U=V U_maj. A bit pattern f has probability w_f=p^(|f|)(1-p)^(3-|f|). Averaging the injected e uniformly, the actual calibration channel is exactly

    E_cal(rho)=U[rho tensor A_I+X rho X tensor A_X]U^dagger,
    (A_I)_gg=(1/4)sum_e w_(e XOR e_g),
    (A_X)_gg=(1/4)sum_e w_(e XOR e_g XOR 111).          (2)

This is a full quantum channel identity on every logical matrix unit, not only an equality of computational probabilities. The logical identification U is the SAME one used by the uninjected payload channel. Physical pre-noise errors and the injected physical X operations commute in this specified bit-flip model. The conclusion is not asserted for arbitrary unknown input-dependent noise or an arbitrary Pauli/gauge source merely by analogy.

Let t=1-2p in [0,1]. Exact simplification of (2) gives

    A_I+A_X=I4/4,
    H_X=A_I+A_X=I4/4,
    (H_Z)_00=(3t-t^3)/8,
    (H_Z)_gg=(t+t^3)/8 for the three weight-one gauges. (3)

All signed blocks are nonnegative and A_I-A_X=H_Z>=0. Thus the qualitative positivity and identity-dominance assumptions are preserved by THIS specifically proved calibration operation. Such preservation is not automatic for arbitrary syndrome mixing on a general noise model.

The unsigned calibration marginal is exactly rho_cal=I8/8, regardless of p and the unknown V. The two signed contrasts are

    Delta_X=U(X/2 tensor I4/4)U^dagger,
    Delta_Z=U(Z/2 tensor H_Z)U^dagger.                 (4)

Their true signed gaps are

    gamma_X=1/8,
    gamma_Z=(t+t^3)/16.                              (5)

For p<1/2 the minimum gap is gamma_cal=gamma_Z. The largest admissible pointwise relative contrast lower bound is (t+t^3)/2. That numerical bound is not supplied by default: the margin-free direct-gap learner can acquire the useful gap from ordinary records under the trusted qualitative p<=1/2 model. If using the older supplied-margin coarse learner instead, a separately supplied positive margin bound is still required.

## 3. The improvement is real but not universal

Without injection, the physical-noise repetition witness has

    gamma_native=p(1-p)(1-2p)/2.                      (6)

Hence, for 0<p<1/2,

    gamma_cal/gamma_native
       =(1+t^2)/(2(1-t^2)).                          (7)

The active calibration gap is better only when t>1/sqrt(3), equivalently p<(1-1/sqrt(3))/2. It is WORSE close to p=1/2; this is not a universal statistical dominance claim. In the useful small-noise limit, however, gamma_native tends to zero linearly in p while gamma_cal tends to 1/8. The direct signed-gap source-call rate O_tilde(3^3/(gamma^2 epsilon)) therefore loses the native p^(-2) rare-syndrome penalty. At p=0 the native full-patch certificate cannot see dormant syndromes, while these permitted input operations deliberately excite them and can certify the same fixed U. This does not contradict the no-access hidden-completion obstruction: the experiment now enters the previously unexposed source input subspaces.

Calibration logical noise can actually get WORSE while information improves. Its oracle loss is

    Tr A_X=(3p-3p^2+2p^3)/2,                          (8)

which is order p, compared with the uninjected payload's order-p^2 loss 3p^2-2p^3. Those extra errors affect known probes only. The payload is encoded normally without (1), and after operator certification the learned decoder is uniformly valid on its gauge states. At p=1/2 the Z contrast is zero and the routine must not claim acquisition of the complementary generator.

## 4. What the example establishes

This is a concrete paid operation that supplies informative gauge excitation without reconstructing a microscopic environment. It applies to an explicit repetition-encoder/intermediate-control/physical-bit-flip/fixed-mixer interface. The unknown physical mixer can make the logical observables genuinely nonlocal and unknown inside the known width-three patch. The calibrated decoder can be obtained through the received coherent local extraction mechanism, rather than granting V^dagger or a classical majority operation for free.

The strongest equally informed conventional learner receives the SAME syndrome-injection port, records, bits, gates and structural noise promise. It can use exactly the same moment/sign tomography. No quantum learning advantage over that comparator, no fault-tolerance threshold, and no improved payload noise rate is claimed. Source calls, known encoder preparation, extra injection controls, output readout, finite rational fitting, decoder synthesis, routing and their complete-process error budgets all remain paid. If only the original logical input port is accessible, operation (1) is unavailable and the native rare-noise witness/abstention results remain the applicable statements.

The companion exact script checks the complete injected physical-error Choi channel against (2), the full-support marginal, both signed gaps, CP dominance, the gap comparison and calibration-vs-payload loss at rational p values including the endpoints. It uses zero source outcomes or random draws, and is not an execution of the acquisition learner. This candidate does not amend the received parent theorem until its separate interface and proof are reviewed.
