# Joint signed-resource to ordinary receiver: common-channel module
2026-10-30. Independent construction aid. **Exact algebra/interface lemma, not a whole recipient-hardware receipt.** The source, resource and endpoint record bounds and actual finite-control realization must be supplied by the governing construction. This note avoids multiplying marginal fidelities, an independent receiver bath, an ideal encoded factory and a decoder/re-encoder operation.

## 1. Joint incoming module, not a product-state promise
Let V encode the unknown logical input L into the ordinary zero-syndrome CSS code on Q. Let Pi_s be the real syndrome projectors of rank K in physical dimension D, and W|s>=Omega_s=vec(Pi_s)/sqrt(K) on A,B. Use real unitary Pauli representatives X^x Z^z consistently.

The needed incoming assertion is one COMMON coefficient module on one positive physical record:

    K = sum_(E,F) [E_Q V tensor (I_A tensor F_B) W] A_(E,F),       (1)

where |E|<=r_Q N, |F|<=r_R N, and A_(E,F) acts only on the input syndrome/source/controller/bath variables, not on L. Its output may retain every actual controller, channel, pointer and external bath. Coefficients for E and F may be arbitrarily correlated and coherent; no tensor product of reduced Q and AB states is asserted. Each E/F may be a chosen small canonical representative with its stabilizer phase absorbed into A_(E,F).

Initial apparatus/resource/bath inputs are fixed independently of L; L may be arbitrarily entangled with an external reference. This channel premise is stronger than a pair of small decoded marginal errors. A purely marginal Bell-target estimate is insufficient to infer (1).

The actual native source safe-edge proof and the atomic signed-Bell safe-edge proof earn (1) JOINTLY when run on the same physical system/fault decomposition: expand finite system legs of each local fault with arbitrary retained-bath coefficients; source canonical edges are identity on L, and resource canonical edges preserve the same Bell-target module. Local faults touching both systems change E and F in the same coefficient; they do not become independent faults. Analytical source-basin projections are syndrome/history functions and preserve this module. Nominal AB-only and Q-only operations preserve the other module.

One can restrict AB to its actual exogenous safe fault/clock records while killing Q at its accepted basin boundary. AB's support/clock envelope is a state-independent positive-record bound; inserting CP/TNI Q-kill compressions cannot increase its bad-record mass. The union of AB bad records and Q loss is therefore bounded unconditionally. This is NOT a restart of either theorem conditioned on a Bell outcome. The physical support of Q,A,B stays in the common incidence budget; other protected DATA is never reclassified as an unconstrained bath.

## 2. Exact joint Bell contraction
The physical Bell bra labelled P gives T_(s,P)=Pi_s P^dagger/sqrt(KD). If the actual mask is P, a term of (1) becomes

    P F Pi_s P^dagger E V /sqrt(KD)
      = phase(F,P) 1[s+sigma(P)=sigma(E)] F E V /sqrt(KD).         (2)

Consequently the corrected outcome operator on the full joint module is a sum of F E V tensored with the retained coefficient

    phase(F,P) <sigma(E)+sigma(P)|_G A_(E,F)/sqrt(KD).             (3)

All dependence on the dense P, the coherent signed gauge, the fault record, controllers and common bath sits outside L. The logical transfer is the same in EVERY coefficient. Summing physical outcomes is the ordinary TP teleportation instrument on the fixed encoded-input sector. No computation or physical application of a syndrome preimage is required.

This identity is valid on a common correlated module, not merely on a product encoded input and Bell resource. In particular, any source/resource logical correlations a dangerous common bath might have created are excluded by the *joint safe module*, not by an independence assumption at the endpoint.

## 3. Actual QND snapshot measurements, if used
A nominal measurement of any subset of Alice's stabilizers acts only on the W gauge: Pi_a,A Omega_s is zero or Omega_s. It cannot measure the unknown input logical factor. Asynchronous measurements can dephase a coherent s, which is harmless to (2)-(3).

If every relevant check is measured before Alice is consumed and Alice suffers local faults during this finite interval, compare the stored values to the final Alice syndrome in each coefficient. Their disagreement is confined to checks whose support meets a capture-interval fault, plus unfinished/defective pointer sites. Bounded incidence gives a common defect-set enlargement. This is a finite-window statement, not a reliable immutable baseline for exponential time.

All old Alice QUANTUM READ operations must be disabled or redirected before they overlap Bell gates, unless their action is explicitly counted in the endpoint error support. A subsequent stabilizer measurement on partially Bell-processed Q,A is not merely a harmless refresh of the original baseline. A construction that counts all old Bob DATA commits during a fixed endpoint need not use a snapshot at all.

## 4. Partial Bell completion and missing masks: no perfect readout oracle
Let J be a set of matched physical columns on which the endpoint is arbitrary: faulty Bell gates, unfinished/incorrect pointers, wrong delivered bits, missing/coherent Pauli-control labels, or any retained local Q,A output. Outside J the actual endpoint equals the declared full physical Bell instrument and applies its raw mask.

The same conclusion holds with output errors enlarged by |J| (or the fixed full-column DATA count if a column groups several DATA factors). To prove this, do NOT assert that unmeasured columns already have classical Bell outcomes. On J, expand the local Q,A input functional in the complete Bell-bra basis, retaining its arbitrary output and bath coefficients. Each term has a *virtual algebraic* Bell label P'_J. Together with the actual labels outside J it forms a full P'. The applied mask differs from P' only on J, so D=P_actual P'^dagger is supported on J. Equation (2) becomes

    phase · D F E V.                                               (4)

The virtual labels are never measured, sampled, communicated or used by the apparatus. Coherences between them remain in the retained coefficients. This is why an unfinished measurement on a correctably small set of columns does not require a perfect measurement-completion oracle.

For arbitrary CPTP faults during a bounded-column-lightcone Bell circuit, expand their finite system legs before the norm estimate only as a SUPPORT observation. The common record support union, not the number or norm sum of Pauli coefficients, bounds J. A pointer-only or message-only fault is charged the associated output DATA column. Private constant-length per-column channels have bounded such routing cones; an uncharged global fanout would invalidate this assertion.

The first governing endpoint can simply use fixed-deadline, latch-controlled finite physical Pauli pulses. Choose HERMITIAN representatives I,X,Y,Z and H_p=pi(I-P_p)/(2 tau), so exp(-i tau H_p)=P_p exactly. Real XZ is anti-Hermitian and must NOT be inserted into this Hamiltonian formula; its Bell-vector phase is instead absorbed algebraically. An actual Pauli program, if separately used, can have coherent wrong labels. In each program-label block, its physical unitary differs from the target P only on unfinished/wrong columns. Equation (4) applies coefficientwise. Exact representative phases in the controlled hops u_v u_g^dagger matter physically, but global output Pauli phases are absorbed in the ancillary coefficient. The permanent program gauge must itself start at the identity label up to a charged sparse source/boot envelope; arbitrary uncharged labels would create extensive resource-relative error.

## 5. Fixed-duration old-engine activity can be charged exactly
In the atomic-old/native-new hybrid, EVERY old DATA-touching instrument, including Alice quantum READ measurements as well as Bob commits, has generator ell(Phi_h-Id) and cb norm at most 2 ell, with fixed bounded DATA/controller footprints. During a fixed endpoint of duration T_end, count EVERY such attempted operation as a local arbitrary event, irrespective of its guard, baseline or cache semantics. The total support majorant has a Poisson exponential moment with exponent O(N ell T_end), in addition to the external fault support. Auxiliary-only watchdog/FIFO dynamics are not DATA insertions, but faults in their mask-routing roles receive their full associated DATA-column support. This avoids any claim that the old relative engine usefully corrects a partially applied dense mask or that an Alice READ is harmless during a partial Bell circuit.

This tactic is unavailable for an old native coherent prefix engine whose fast DATA Hamiltonians remain on. It is also not an arbitrary-latency pending-frame theorem. It is a finite, priced protected operation; old commits remain physically active while their entire action is paid in the correctable endpoint envelope.

If a first-initiation Hamiltonian or calibration remainder is included by forward Duhamel rather than a positive Poisson record, use the signed common-span/positive replacement in Section 7 below. Do not call the signed truncation a positive record.

## 6. Ordinary canonical receiver factor and warm basin
Let w_out bound the total Pauli weight of EVERY coefficient in (4), including incoming radii, endpoint support, incomplete columns and the DATA footprint activated by sparse fresh-receiver controllers. Suppose 2 w_out<d and w_out is inside the selected linear native canonical radius. The ordinary fixed canonical map sends every such E_out V to

    I_L tensor |ancillary(E_out)>                                  (5)

up to stabilizer phase. It does not depend on P, the signed resource sector, the command, or a target logical gate. Thus the entire common span has the SAME logical identity; no decoder/re-encoder is physically applied.

For a new native controller let C bound its primitive non-ready parts. Its actual forest is identity at ready owners and preserves those controller projectors. On C<=alpha_ctrl N, its inverse has a coefficient expansion on at most r_F alpha_ctrl N DATA sites. Include this in w_out before invoking (5). History flags are bounded by a fixed incidence enlargement of C. Consequently the raw global energy is bounded deterministically on the joint span by

    E_native <= 2 w_out + R c_hist alpha_ctrl N.                    (6)

Use the actual sector constants if the global energy uses a different normalization. If the right side is below the selected energy cutoff and the canonical radius margin, the span lies in the positive native basin. If F_native<=exp(gN)exp(s E_native), then

    Tr F_native rho_good <= exp{[g+s(2 w_out/N+R c_hist alpha_ctrl)]N}.

The exponent must be below the accepted warm-start barrier margin. A small correctable radius alone does NOT supply an O(N) moment, and no such claim is made here.

## 7. Positivity and signed truncations
If the complete good endpoint is a CP/TNI instrument whose Kraus operators lie in the module, (5) gives exactly id_L tensor tau with tau positive; it may retain all Bell outcomes, old/new controllers, messages, pointers and the shared bath. This proves the genuine receiver *channel*, not only decoded output on known inputs.

If the actual positive compressed map A is only epsilon-close in diamond norm to a signed low-order endpoint map B=id_L tensor tau_signed, the signed coefficient must not be declared positive. Fix a normalized logical state omega and put tau_pos=Tr_L A(omega). Then tau_pos>=0 and

    ||tau_pos-tau_signed||_1<=epsilon,
    ||A-id_L tensor tau_pos||_diamond<=2epsilon.                    (7)

Trace deficits and analytical projection/gentle errors are charged separately. Because A has the actual basin support and bounded moment, so does this positive ancillary replacement. All bounds are reference-stable and involve no logical-dimension prefactor.

Only AFTER this common-channel and warm-input construction may the accepted native killed trajectory be continued. Future local old atomic commits can be retained as weak noise below the new native threshold while their rates are ramped to zero. Their old auxiliaries need not be decoded, reset perfectly, de-correlated from the bath, or semantically converted into new controller states.

## 8. What this earns and what it does not
This lemma closes the algebraic receiver seam once the actual finite endpoint support, boot/mask-completion tails, unified rates and mode controls are proved. The source is consumed by a Bell measurement; no cloning or nondestructive retention of the source is claimed. The recipient remains quantum and can continue in the ordinary native memory with the same fixed DATA decoding convention.

It does not itself supply physical Bell pairs, the atomic-old stochastic resource theorem, generic continuous-noise robustness of that old LOCC engine, arbitrary-delay network protection, a native-old two-site compilation, magic states, or an advantage over equally informed scheduled teleportation. The first hybrid theorem retains the old resource's Poisson-CPTP physical fault-location scope, except for separately bounded finite-duration control remainders explicitly charged by Duhamel.

## 9. Finite diagnostic, not a hardware proof
`check_joint_span.py` uses a three-qubit repetition CSS code, a nonproduct correlated source-error/resource-error/signed-gauge/common-bath isometry, and all 64 raw physical Bell outcomes. The corrected common logical-factor residual is exactly zero and their scalar normalization is 0.9999999999999999. Leaving one matched Bell column unmeasured and retaining its quantum Q/A outputs gives common output-module residual 4.89e-17, with normalized actual partial channel; no virtual outcome is measured. The Hermitian-Pauli pulse residual is 4.30e-16, whereas real XZ has non-Hermiticity norm 2.83. A dense uncharged wrong mask implements logical X in this diagnostic, explicitly testing the necessary support restriction. This code corrects the chosen X-error family only; it is not a full-distance Tanner or native-apparatus simulation.
