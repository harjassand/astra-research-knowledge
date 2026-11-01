# A paid monitored-source construction for phase resources — ordinary baseline wins

31 October 2026. Author candidate; independent mathematical review pending. This is a construction and exact known-model comparison, not a new physical principle, calibrated apparatus, quantum hardware execution, fault-tolerance threshold, or demonstrated advantage over ordinary environment-assisted correction.

## Useful result first

The actual finite-rate X-source/Z-data model can prepare an arbitrary graph/weighted-phase resource layer while continuing to emit. Every local source's **initial bit, total jump parity and final bit** suffice to remove its disturbance exactly. No timestamps, mid-layer feedback, source-conditioned transverse gate, source reset between graph edges, or full-source simulator is required for this commuting task. The strongest ordinary method already supplies this operation.

An imperfect detector changes the answer. We constructed the actual one-click-per-bin/dead-time instrument, including both thermal jump channels, dark counts and continuing source dynamics. Its ordinary optimal Bayesian terminal Pauli decoder is strictly better than blindly trusting a noisy terminal source readout. It may ignore that readout. Thus endpoint assignment infidelity is **not** an unavoidable logical-error floor. The finite comparisons below are rigorous rationally enclosed; their detector parameters are declared inputs, not measured hardware capabilities.

A further ordinary receiver simplification is earned below: for sufficiently damped cold sources, omit the terminal source readout entirely and pay its remaining source-excitation probability. This avoids assuming an accurate source measurement during continuing coupling.

The meaningful frontier is physical collection/local observation with controlled backaction and sufficiently accurate endpoint apparatus. The accepted complete-observable admission does not supply that service. For this restricted commuting task ordinary exact trajectory algebra is stronger and simpler than invoking the admission theorem. We preserve the latter for generic noncommuting local controls and extra imperfections meeting its actual premises.

## 1. Entire operation, not a source-only fixture

For n data qubits and n LOCAL source qubits, take

    H(t) = H_phase(t) + sum_i c_i(t) X_si Z_i,
    H_phase(t) = sum_i h_i(t) Z_i + sum_(ij in E) J_ij(t) Z_i Z_j,
    L_i,- = sqrt(lambda_i) sigma^-_si,
    L_i,+ = sqrt(a_i) sigma^+_si.

All operators and ports are ACTUAL local ones. Each source and detector has its own port; no unmodeled shared bath, controller fanout, reflection or detector feedback to the source is omitted. Extra source detuning proportional to Z_si is allowed by the algebra but absent from the numeric fixtures. Coefficients and source rates may be time-dependent in the exact trajectory identity; the numerical instrument uses constant values within each bin.

Start each source in a genuinely known computational bit q_i,0, initially uncorrelated with the arbitrary data/reference input. A cold prepared source is one option. A local source-Z measurement whose result is actually known is another for fresh resource-state preparation. An unrecorded hot source is NOT equivalent. Measuring an initially data-correlated source may disturb the data, so the older theorem's arbitrary-initial-correlation permission is not imported here.

Preparing data |+>^n and implementing the displayed Z/ZZ interactions produces weighted graph resources. Arbitrary phases include non-Clifford phase rotations. Standard cluster graph preparation is included. This is NOT itself a complete universal computation: preparation, adaptive noncommuting readout, inter-layer operations, and error-correcting resource consumption still require their own paid services.

## 2. Exact finite-rate correction

Let W be the product of source-controlled data Z gates. It is a proof frame, not a gate silently performed on the device. Direct conjugation gives

    W (X_si Z_i) W = X_si,
    W sigma^±_si W = sigma^±_si Z_i,
    W H_phase W = H_phase.

In this frame the source Hamiltonians are data independent. Every actual loss OR injection jump contributes Z_i to the data. The no-jump anticommutator is source only. Since H_phase commutes with every Z_i, the complete conditional evolution has data operation

    U_phase product_i Z_i^(N_i + q_i,T + q_i,0),

after the final source bits are measured. The scalar probability of each fully resolved source trajectory is independent of the data input, including a reference. Correcting the displayed parity recovers U_phase exactly for all finite rates, couplings and times. This is a full channel identity, not just preservation of one state. End correction may be carried as a Pauli frame for a compatible downstream consumer. It must be physically applied, with its error charged, if an actual frame-free data output is required.

Continuous target Z/ZZ gates, arbitrary graph edges and thermal source cycling do not change the identity. A thermal upward jump must be included in N_i even when its port is not observable; taking eta_plus=0 is a legitimate imperfect receiver, not permission to discard upward jumps. An ideal photon-counting dilation has been assumed, not inferred from any mathematically equivalent Lindblad representation.

With unobserved outputs the old exact dephasing floor remains correct. The monitored protocol changes the output/information available and adds observation. It does not contradict that floor. Perfect recovery with changed information is the established environment-assisted-error-correction principle.

## 3. Actual finite dead-time instrument

Work at one source and let J_- = lambda [rho -> sigma^- rho sigma^+], J_+ = a [rho -> sigma^+ rho sigma^-]. Set

    A rho = -ic[X,rho] - {lambda Q + a P,rho}/2,
    C = eta_- J_- + eta_+ J_+.

The detector starts active at each interval of duration Delta. A captured jump gives one click and makes the detector blind until the next bin. Each active true event is independently captured with its supplied efficiency eta_±. An independent active dark count has rate d, gives a click, and also makes the detector blind. Source evolution NEVER stops while the detector is blind. Rearming and report delivery are real detector services; no per-emission reset is hidden in the model.

For z=+1 or -1 define

    A_z = A + z[(1-eta_-)J_- + (1-eta_+)J_+] - d id,
    B_z = A + z(J_-+J_+),
    C_z = C + z d id,
    M_z = [[A_z, 0], [C_z, B_z]].

The top-left and lower-left blocks of exp(Delta M_z) are Phi_0(z), Phi_1(z), the no-click/click instruments. At z=+1 they are positive source instruments. At z=-1 they propagate the difference of residual even- and odd-parity source density matrices after the known click parity has been removed. Captured true jumps do not flip residual parity, missed jumps do, and a false click does. These equations therefore include repeated real events inside a blind bin, not a fitted effective miss probability.

For record r=(r_1,...,r_m), define D_r=Phi_(r_m)(-1)...Phi_(r_1)(-1)(|q0><q0|). Endpoint source measurement is ideal, followed by an INDEPENDENT symmetric report flip of probability e. This is an explicit classical error model, not a claim that arbitrary faulty measurements reduce to bit flips. After correcting click parity and the reported endpoint bit, the two signed residual weights are

    s_(r,0)=(1-e)(D_r)_00 - e(D_r)_11,
    s_(r,1)=(1-e)(D_r)_11 - e(D_r)_00.

A decoder chooses an extra Z iff the relevant s is negative. Its exact minimum average Pauli-error risk over all terminal binary decisions on THESE records is

    p_Bayes = [1 - sum_(r,b) |s_(r,b)|]/2.

The same probability laws are data independent, so minimizing this classical risk also minimizes the complete dephasing-channel error within the allowed terminal Pauli decisions. Unconditional risk is sufficient here; postselected risk on a rare record is not asserted small.

Online filtering stores one 2x2 signed matrix and takes m constant-size matrix-vector operations per source; an unsigned matrix may also be stored to normalize posterior probabilities. Offline exact enumeration of the optimal average risk in the provided implementation costs O(2^m), and is NOT advertised as polynomial. Blind click-parity decoding instead uses [Phi_0(-1)+Phi_1(-1)]^m and costs O(log m) constant-size matrix products. The model-aware Bayesian decoder can always select the fixed correction that ignores all records; consequently its risk is no worse than the best fixed-Pauli no-record baseline. This fact prevents manufacturing a comparison win by forcing an ordinary comparator to trust an unreliable readout.

## 4. Scalable receiver and paid imperfect operations

For product known source bits, independent local ports/detectors and commuting H_phase, each source/record process is independent even though the target data become entangled. Residual Z errors are independent with the actual local risks p_i. Therefore every selected VERTEX subset S obeys

    Pr(all vertices in S have a residual Z) = product_(i in S) p_i.

This is a one-resource-layer stochastic error statement. It is not the old all-selected arbitrary circuit-location amplitude theorem, and it does not survive arbitrary shared detector failures, unknown source correlations, source-dependent controller errors, overlapping bath blocks or unverified calibration. Correlated known initial bits give a conditional product model and a uniform product upper only if the risk bound is uniform in those bits.

For |G_theta>=U_phase|+>^n, the vectors Z^e|G_theta> are orthonormal. Hence the unencoded target fidelity is EXACTLY product_i(1-p_i), and the trace distance without a factor 1/2 is 2[1-product_i(1-p_i)]. A fixed local p does not give a globally accurate arbitrarily large unencoded state. An actual error-correcting graph-state/MBQC consumer must be specified before claiming reliable scalable computation.

Physical preparation, finite gate errors, final source measurement, detector calibration, data correction and subsequent consumption remain paid. If a full actual per-source record instrument differs from the declared model by a complete instrument diamond bound eps per bin, telescoping gives at most m eps process distance and hence a conservative m eps addition to the decoder's risk. Locality and independence of those discrepancies need separate proof for high-order receiving. Scalar observed fit errors do not supply this instrument bound.

A finite endpoint apparatus may be modeled by an explicit ideal measurement-control generator plus its residual. Omitting the always-on local c X_s Z_d interaction during endpoint duration t_ro changes its full channel by at most 2c t_ro in diamond norm (Duhamel and CP contraction), while source loss/injection must still be included in that apparatus model. This is a conservative paid duration term, not a construction of fast readout. If source loss changes the measured source bit during the apparatus operation, one cannot model the result as an instantaneous bit flip without proving the full measurement instrument. The same warning applies to source preparation. No measured endpoint instrument has been supplied here.

## 5. A simple cold-loss budget — and limits

For a cold loss-only source, constant |c(t)|<=c and lambda>0, let U=4c^2 T/lambda. From p_exc'<=-lambda p_exc+2c sqrt(p_exc), one gets sqrt(p_exc(t))<=2c/lambda and E N_T<=U. Immediately after a true loss jump the source is exactly cold. Therefore after each captured event its expected emissions during the remaining blind time <=Delta are at most 4c^2 Delta/lambda. Summing conditional expectations gives

    E(number of dead-time missed emissions) <= U^2/m,
    p_blind <= min(1, e + (1-eta_-)U + U^2/m),             (d=0).

The independently missed active emissions contribute at most (1-eta_-)E N. The last inequality uses Pr(odd misses)<=E misses and is deliberately conservative. It is NOT an exact risk or a lower bound. The Bayesian filter often substantially beats it. With dark counts a conservative extra term dT can be added for false-click parity, but dark-created blind windows also need charging; one cannot simply add dT while retaining the previous true-click-only dead-time bound. The exact instrument handles both effects.

A known initially excited source adds an initial-loss transient; strong Markov restart gives E N_T<=1+U, not the cold U bound. An unrecorded hot source can additionally introduce an unknown initial parity. Thermal upward cycling invalidates the cold emission bound; both rates must be used in the actual instrument. The separate root energy/jump-MGF construction can bound record overflow for a compatible broader actual source, but does not turn a generic source's quantum jumps into correctable Zs or replace this detector model.

## 6. Executed exact comparisons and ordinary controls

`certify_receiver.py` uses exact rational/Gaussian-integer Taylor scaling-and-squaring on the positive source x (missed parity) x (active/clicked) direct-sum generator. No floating expm enters its certificate. Each bin's 16x16 density-block matrix is a CP trace-preserving semigroup on a four-sector qubit algebra. The completely bounded rounding bound is conservatively 2*8^3*2^-112. Scaled generator norm <=1/4 and degree48 give Taylor tail <=2/4^49. Contractivity yields the explicit final error enclosure; all finite-record absolute values and final decisions are rational. Full decimal displays below summarize those exact intervals.

For c=T=1, cold q0=0, a=d=0, eta_-=0.99, four detector bins, and independent terminal report flip e=0.001:

| lambda | No record, no pulses | Three ideal echo pulses | Blind record correction | Optimal ordinary record decoder |
|---:|---:|---:|---:|---:|
| 16 | 0.184819988861 | 0.0722731467883 | 0.00429637296589 | 0.00429637296589 |
| 64 | 0.0572254144262 | 0.0466490368323 | 0.00188458470468 | 0.00185940277479 |
| 256 | 0.0152686814587 | 0.0145577580605 | 0.00118048315649 | 0.000241850781025 |
| 1024 | 0.00388351964472 | 0.00383809535879 | 0.00104067815045 | 0.0000445740279334 |
| 4096 | 0.000975134467664 | 0.000972279010863 | 0.00100985457773 | 0.0000101127401432 |

All entries are physical residual Pauli probabilities in their respective declared ideal-control models, not fault amplitudes. At lambda4096 blind correction is WORSE than doing nothing; ordinary Bayesian decoding avoids that mistake. This is not a claim that 99% collection and the stipulated endpoint instrument are available hardware.

The echo comparator uses the exact two-moment telegraph equations with alternating coupling signs, not a weak-coupling approximation. It is given identical lambda,c,T information. Global data-X echo preserves ZZ targets between pulses, with intended Z phases toggled appropriately. Finite pulse durations, target refocusing/switching, pulse imperfections and extra elapsed time must be paid. The displayed echo has ideal instantaneous pulses and is therefore a strong optimistic comparator, not an executed pulse service. With many pulses it can win: the diagnostic grid includes 64 bins/63 pulses and low-lambda cases where echo is much better than monitored correction. Detector rearm rate and pulse count are different physical resources; no scalar hardware-cost equivalence is asserted. A comparator with the same records can use the same optimal filter and wins equally—this construction does not outperform ordinary methods.

## 6a. Remove the terminal source-measurement service rather than idealize it

A photon-only receiver applies the known click parity and initial bit, and TRACES the source without measuring it. The remaining error parity is M_missed XOR q_T. Its blind risk is

    p_photon = [1 - Tr(Z [Phi_0(-1)+Phi_1(-1)]^m rho0)]/2.

The optimal photon-only decoder uses sum_r |(D_r)_00-(D_r)_11| instead. This is equivalent in information to a completely uninformative endpoint report, but the physical endpoint measurement is **absent**, not performed and randomized. A calibrated source-readout service and its finite-duration disturbance are therefore unnecessary for this variant.

For the same cold loss-only/dark-free assumptions as Section5,

    p_photon <= min(1, (1-eta_-)U + U^2/m + 4c^2/lambda^2).

The last term is the residual source excitation, from the same sqrt(p_exc) bound. No loss-rate elimination or replacement channel is used. At fixed diffusion c^2=lambda b^2, this bound becomes

    4(1-eta_-)b^2 T + 16 b^4 T^2/m + 4b^2/lambda.

This changes the information-access task relative to the old unconditional floor. Spectral collection still must actually be supplied; m is a detector rearm count, not an earned optical capture bandwidth. It is not evidence that a fixed-bandwidth physical detector has uniform eta as lambda changes.

The exact certificate's photon-only column is 0.0183745724110940 at lambda16; at lambda64,256,1024,4096 it equals the optimal noisy-endpoint risks in the table. In those four operating points the ordinary optimal policy gains no additional average accuracy from the supplied noisy endpoint bit, and the blind photon-only parity policy already attains its optimum. Thus an **entire unearned measurement service can be omitted**, instead of treated as perfect or charged as a mandatory error floor. At lambda16 the accurate endpoint readout genuinely helps, so the simplification is not universal.

The result is an output channel/state AT the declared time T (and may be extended through a longer monitored diagonal/idle interval). Continuing interaction during later noncommuting consumption or data readout still has to be received. This does not silently provide a detached stable output register. Cold preparation or equivalent initial-source knowledge remains paid.

## 7. A physically simpler receiver already exists — but its raw reliability is paid

A field-parity ancilla avoids event-by-event readout/rearm in principle. Besse et al. implement an ordinary Ramsey parity detector for propagating microwave fields, with each reflected photon supplying an ancilla phase flip. This is NOT a new operation proposed here. Their inspected primary full text reports a 1 microsecond window, T2*=3.5 microseconds, 78% source-to-detector transmission, and approximately 85% single-shot parity assignment for that experiment. Appendix B distinguishes this raw assignment from calibration-corrected parity expectation values. In particular, correcting plotted contrast does not physically repair an individual wrong correction bit.

Those historical figures do not prove a current optimum or a universal no-go, and are not transplanted into our source model as a calibrated implementation. Source waveform overlap, nonlinear multi-photon response, loss ports, carrier frequency, isolation, ancilla lifetime, endpoint readout and thermal population must all be compatible. A low mean emission count alone gives no detector spectral-response certificate. Conversely the source decay rate alone is not a universal required capture-bandwidth lower bound; resonance-fluorescence elastic and inelastic components differ. Spectral collection efficiency and temporal dead time are deliberately separate inputs here.

## 8. Scientific decision

This branch earns an explicit end-to-end KNOWN-MODEL ordinary phase-resource preparation/decoding operation, an imperfect-detector receiver, and a corrected exact comparison. It does not earn a new paid quantum capability over ordinary theory or a realizable operating point. The original observable admission is valuable for other noise/control structure, but is not what makes this commuting operation possible. Calling the ordinary construction novel, using a perfect recorder as the main uncharged service, or replacing actual detector calibration with these matrices would misstate the result.

Further theory is not the missing item for this selected task: an actual local source/collection/endpoint model with support and accuracy evidence is needed to decide whether the operation survives its full physical bill. No equipment, purchase, outreach, or experiment was performed or requested. All old source files remain unchanged.

### Primary sources actually opened

- Gregoratti and Werner, *Quantum Lost and Found*, https://arxiv.org/html/quant-ph/0209025 — environment-assisted random-unitary correction.
- Ahn, Wiseman and Milburn, *Quantum error correction for continuously detected errors*, https://arxiv.org/html/quant-ph/0302006 — detected-error control, imperfect detection (IV.4), universal encoded gates (V).
- Besse et al., *Parity Detection of Propagating Microwave Fields*, https://arxiv.org/html/1912.09896 — finite physical parity receiver, raw assignment versus calibrated means, especially Appendix B.
