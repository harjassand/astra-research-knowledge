# Actual finite activation, positive warm entry, and the same ordinary DATA decoder
2026-10-30. Companion derivation for the atomic-old/native-new recipient candidate. NOT an independent receipt.

## 1. Actual new receiver and its first-initiation-OFF mode
The new B apparatus is the exact accepted unified native generator, including complete A_i>=1 aborts, actual finite monitors, fixed positive later-acquisition amplitude zeta, and weak first amplitude epsilon_new. Its controller, lock, workspace and monitor registers are DISTINCT from the old atomic classical machine. Their physical dimension/number is a fixed extra factor. They share B DATA; grouping does not authorize remote coherent operations.

Before activation, ALL new-native label-changing transitions are OFF: acquisition/reversal, consistency-abort drives and resets, C payload/commit/terminal dynamics, verification, cleanup and ready transitions. The ONLY enabled new-controller dynamics are the complete onsite clock/workspace/tag boot resets stated next and optional label-preserving monitor terms. This exact choice is required for the primitive product backwards-reset bound; arbitrary fast label-changing auxiliary dynamics are not silently retained. Complete onsite resets prepare its hub clock/workspace to A0,W0 and its resource tags to free at finite rates. They act as identity on DATA. Label-only monitors may remain on; no pure monitor is required. Their actual finite noisy boot bound is uniform even when those registers and the retained bath are correlated with the incoming quantum-transfer process.

At a fixed time after the physical Pauli mask pulse, first ramp the boot reset rates to zero, then ramp the chosen native terms from zero to their final values. The waveform has fixed duration Delta_on and uniformly bounded coefficients. The final generator is exactly the accepted native instance. Keep the old atomic DATA instruments enabled at their small rates throughout. No instantaneous state reset, gauge transformation or unitary kick occurs.

For analysis only, remove the new first A0<->A1 Hamiltonian edges from this time-dependent generator. This leaves a legitimate CP nominal generator L_0(t), because Hermitian edge-plus-adjoint terms are removed together; all other Hamiltonian coefficients and resolved jump rates follow their actual nonnegative ramp. The omitted Hamiltonians have total local norm O(epsilon_new) per owner and are restored by forward Duhamel, not replaced by ideal random starts.

## 2. Strong ready masks and full-Hilbert support during activation
Define the strong ready projector of owner h by

    P_h^ready = P_(A0,W0),h product_(r in R_h)(I-P_o_h,r-P_z_h,r),
    BUSY_h=I-P_h^ready.

Monitor states are unrestricted. With first initiation off, EVERY actual native Hamiltonian and resolved reset preserves the ready subspace of every h. This follows termwise from the frozen alphabet and singleton-BUSY proofs, not merely a summed drift:
- a ready h has no own/z tags, so its consistency-abort and later-acquisition/cleanup/verification/payload edges have no source there;
- its A0 refresh leaves A0,W0 fixed;
- another owner's changes of its own tag never create an h-tag and never touch h's private clock/workspace;
- resource and clock monitor terms preserve the relevant label projectors and do not act on DATA;
- the only edge leaving a ready h was precisely the removed first initiation.

This remains true on all malformed sectors of OTHER owners. Each physical DATA Hamiltonian is a C payload term of an owner that is busy. Physical terminal, abort, commitment, workspace, ready and monitor resets are DATA identity. Scaling the actual terms during activation preserves these facts.

For an owner set S let Q_S=product_(h not in S) P_h^ready. The nominal propagator preserves Q_S. Its Kraus/Stinespring coefficients restricted to this source act as DATA identity outside D(S), the union of full DATA footprints of owners in S. Coherent superpositions S,S' are treated on each coefficient separately; no mask pinching or union over all possible masks occurs.

For a physical local insertion Z, let A(Z) contain all h whose strong ready support meets Z. Every finite-system coefficient commutes P_h^ready outside A(Z), even with arbitrary bath coefficients. It maps Q_S only into Q_(S union A(Z)), and acts directly on DATA only in Z. Bounded native incidence gives constants a_act,q_act with

    |A(Z)|<=a_act,    |DATA(Z) union D(A(Z))|<=q_act.

The same statement holds for an old atomic DATA attempt: although its controller semantics may be garbage, its actual CPTP support is bounded. Old auxiliary-only dynamics cannot activate new owners because they act on distinct registers. Their shared-bath faults are already in the charged local perturbation.

Thus after k retained insertions/attempts, starting with at most beta_boot N nonready owner witnesses,

    |S_final| <= c_boot beta_boot N+a_act k,
    DATA support <= w_in N+r_D c_boot beta_boot N+q_act k.       (2.1)

The whole nominal activation may be order one and may run committed nonmonomial payloads. Its DATA support still lies inside this union. It is NOT charged as an extensive order-one generator error.

## 3. Finite norm bounds with the exact whole-bundle split
Every old atomic DATA channel has generator ell(Phi-id), norm <=2ell. Remove the ENTIRE Alice-worker and Bob-commit bundles from the nominal endpoint, including their loss terms, and include them as bounded local perturbations. EXACT_ENDPOINT_GKLS_SPLIT.md proves that the remaining old generator is DATA-independent and CPTP. No endpoint guarded-jump record is needed. All old Alice quantum READ actions are included; there is no commutation assumption during partial Bell gates. The source/access and new activation first edges, endpoint control/calibration deviations and all endpoint noise join the same forward Duhamel perturbation, with

    zeta <= C[ell T_end+eta_endpoint T_end
                +epsilon_Q Delta_access+epsilon_new Delta_on].

Forward Duhamel about the actual nominal CP propagator gives the order-r norm bound (N zeta)^r/r! and an exponentially small tail above rho N when zeta/rho is sufficiently small. The retained expansion is signed; each coefficient has the support bound (2.1), with k now counting retained local generator insertions. Auxiliary/basin projections may be interposed as CP/TNI maps without increasing this norm tail. No inverse dissipative map and no sum of Pauli coefficient norms is used.

All physical waveform durations are priced. Choose the code, fast native hardware and later-acquisition zeta first. The accepted small-epsilon family has fixed support/fast-BUSY constants and a uniform positive warm/barrier allowance once epsilon lies in a sufficiently small interval: activity/useful no-jump entropy costs g(epsilon),q_t(epsilon) tend to zero, while the selected s_prime e_cut margin remains positive. Choose support densities and all boot/carrier/pulse/ramp durations within this uniform allowance BEFORE fixing epsilon. Then choose epsilon_Q,epsilon_new in that interval to fit the integrated weak-edge budget. Only now fix their actual native thresholds and choose ell. These are one-time construction choices before operation, not a change of an already running or frozen physical generator.

## 4. Actual positive compression, not a signed initial state
At the boot deadline, compress ANALYTICALLY onto at most beta_boot N nonready primitive reset blocks. The accepted finite-reset moment bounds its lost probability by exp(-cN), uniformly over the actual joint logical/reference input; gentle compression has exponentially small diamond cost. These primitive projectors are auxiliary-only. Their bounded-incidence union supplies S above.

At the carrier deadline, similarly compress onto at most beta_carrier N unfinished columns using the unconditional carrier moment. This is another analytical CP/TNI comparison, not postselection by the apparatus. Boot-failed pointer/carrier columns, local inserted faults and unfinished columns are combined into the exceptional set for the signed-Bell module. Every actual channel comparison is made BEFORE propagating a signed truncation; subsequent actual CP maps are contractive.

The common-module lemma then says that the projected low-order comparison map at activation exit has DATA coefficients E_out Enc_B with the weight bound (2.1) plus the source/resource/endpoint budgets. No ideal decoder/re-encoder has acted. Apply the fixed new forest inverse ONLY AS A PROOF REPRESENTATION. Each forest factor is nonidentity only in C/R(C), hence only for owners in S. It preserves the strong ready projectors. Its DATA coefficient support is inside the SAME D(S), not an additional extensive union. Outside S all history flags B_h are zero. Therefore every coefficient in this represented map has

    r_can <= w N,        M_BUSY=sum BUSY_h <= b N,
    E=U+R sum B_h <= (c_U w+R b)N,                  (4.1)

where w,b are explicit fixed linear combinations of the small input, boot, carrier, retained-insertion order densities. c_U is the actual unary-energy/Pauli-weight constant for both CSS sectors; it is not a raw-syndrome bit count.

Choose these budgets AFTER the new native proof parameters so w is strictly below its linear canonical radius and E_0=c_U w+R b is strictly below its energy cutoff. Let P_small be the simultaneous raw-diagonal projector imposing r_can<=wN, E<=E_0N and M_BUSY<=bN. These projectors commute: the strong busy mask is controller-only in this forest frame and commutes the raw syndrome/history algebra. The signed comparison has support in P_small. Its actual positive counterpart differs in diamond norm by epsilon_D, so the actual mass outside P_small is at most epsilon_D. A final gentle compression costs at most 2sqrt(epsilon_D).

Let A be this final actual CP/TNI compressed map in the canonical logical gauge. The low-order comparison is Id_L tensor tau_signed with the SAME logical identity for every Bell outcome, resource gauge and coefficient. If ||A-Id_L tensor tau_signed||_diamond<=epsilon, choose any fixed normalized logical omega and set sigma=Tr_L A(omega). Then sigma>=0 and

    ||A-Id_L tensor sigma||_diamond<=2epsilon.

This is dimension-free and reference-stable. Sigma is allowed to retain ALL old/new controllers, raw Bell outcomes, consumed Q,A, classical carriers and the SAME external bath. There is no reinitialization or independence assumption on these auxiliaries. Because A is supported on P_small and the raw majorants are logical identity, sigma has the same support and moment bounds. In particular, with the accepted bound F_new<=e^(gN)e^(sE),

    Tr F_new sigma <= exp([g+s E_0]N).              (4.2)

Choose g+sE_0 below the accepted warm-start barrier coefficient by a fixed extensive gap. Merely having a small trace error, a small syndrome count or an O(1) gap from the barrier would not suffice.

## 5. Actual overlap followed by long native protection
After the activation ramp the full new native generator is on. The old quantum READ and commit attempt rates remain <=ell and are ramped to zero over another fixed finite waveform. Each actual map is arbitrary but bounded-local CPTP, so the total additional per-site joint cb budget is <=2 C_inc ell. This does NOT apply to an old native coherent prefix apparatus with fast DATA Hamiltonians; the first theorem is explicitly atomic-old/native-new.

The old auxiliary-only watchdog/FIFO/copy dynamics, together with any old controllers left in arbitrary states, commute F_new and P_new because they touch neither new DATA nor new native registers. They may remain on. All cross-system/common-bath faults are retained in the common physical incident budget. Choose eta_ext+eta_cal+2 C_inc ell below the fixed new threshold. The accepted native warm killed trajectory now protects the logical identity for its exponential horizon with initial exponent (4.2). No old record is declared clean and no old baseline is converted.

## 6. Why the ordinary DATA decoder is STILL the same
The native theorem is formulated in a forest/canonical representation. It would be wrong to replace the promised ordinary DATA recovery by a forest-dependent ideal inverse at later times.

The accepted full-state singleton BUSY drift has a positive observable G_busy with

    e^(2c delta M_BUSY)<=G_busy<=e^(2C delta M_BUSY),
    d log x/du <= -lambda log x + rho N,

with the stated fixed-rate noise and apparatus constants. This operator drift does not require a clean initial controller state. From (4.1), the positive warm input has

    log x(0) <=2C delta b N.

Consequently at EVERY fixed requested future time,

    log x(u) <= N max(2C delta b, rho/lambda).

Choose b, the native first amplitude and the total perturbation strength so this coefficient is strictly below 2c delta beta_out. Then the full-state probability of M_BUSY>=beta_out N is exponentially small, uniformly in u. This is a pointwise tail, not an anytime absence of busy excursions. The physical forest commutes the busy masks, so the same observable and initialization apply before/after the proof representation. The old maps during overlap are included in its actual local noise budget.

Combine this full-state tail with the native actual/killed comparison and killed canonical radius <=alpha_new N. On the joint good projector, the physical B state has a common Pauli coefficient span of weight

    alpha_new N+r_D beta_out N.

The forest contribution is supported only on the busy-owner footprints; no physical forest inverse occurs. Choose twice this bound below the CSS code distance. The SAME ordinary zero-code DATA recovery corrects every coefficient, independent of the dense Bell mask, signed syndrome, classical outcomes, old controller state and elapsed storage time. It is used only to state the logical channel; no physical quantum decoding/retrieval is asserted.

This earns a genuinely quantum protected recipient after a destructive source Bell measurement, rather than a classical readout endpoint or a decoder that manufactures the transferred state.
