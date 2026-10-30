# A finite raw-mask transfer into a continuously operating native receiver
2026-10-30. Research candidate, NOT independently accepted. The old resource apparatus is the accepted **atomic** LOCC instrument machine; the new receiver is the accepted two-site-qudit/onsite-reset native memory. No native-old conclusion is imported. Earlier accepted results remain unchanged.

## Result sought and the actual mechanism
An unknown already-encoded CSS input Q is transferred into physical DATA B, which then remains in the ordinary zero-syndrome native memory with the SAME ordinary DATA recovery. The input may be entangled with an arbitrary reference. The entanglement resource begins as noisy physical Bell pairs A:B and is protected by the accepted atomic signed-Bell buffer; it is NOT an ideal encoded Bell factory.

There is a fixed finite endpoint, with real local measurement pointers, raw-bit communication, bounded control pulses, controller boot and a finite receiver activation ramp. The old atomic apparatus remains physically enabled throughout this endpoint. All its DATA-touching attempts—**Alice READ measurements as well as Bob read/correct commits**—are counted as arbitrary local operations during the endpoint. Their fixed positive rates are chosen sufficiently small. Fast old auxiliary-only watchdog/FIFO dynamics are not DATA faults. This is not a claim that relative QEC contracts while Bell masks are incomplete: quantum protection in this finite transition is earned by a common correctable span. No indefinitely reliable baseline, long-delay pending frame or unspecified mode conversion is used.

Once the raw physical Pauli mask has been applied and the native receiver is enabled, every remaining old DATA map is a bounded local perturbation of the new native generator, of norm at most twice its attempt rate. Choose those rates below the new native threshold. Ramp them off over a fixed finite interval while the new native memory protects B. Old caches, messages and records need not be clean, converted, erased or interpreted. This rate-separated overlap is the substantive interface.

## 1. Hardware, initialization and noise contracts
There are three code blocks Q,A,B of the same real CSS family with linear distance and the reviewed Tanner global-radius correction theorem. Q and A are in one laboratory with corresponding resource DATA sites colocated for the actual onsite CNOT used below. B may be remote. Classical links A-to-B have fixed finite path length, capacity and local dimension; there is O(N) parallel raw-bit bandwidth. These are explicit hardware resources, not consequences of grouping notation. Every physical site—including protected DATA, new/old controllers, pointers and channel registers—remains in ONE bounded-support/incidence model. Only an external retained bath is unrestricted in dimension.

Initially the unknown logical/reference input is independent of a fixed joint apparatus/resource/bath state. All subsequent correlations are retained. Raw physical Bell-pair preparation is supplied with the positive common support envelope of the accepted atomic theorem. Its bad-instrument mass is denoted delta_source; a sufficiently weak bounded-depth physical source has delta_source exponentially small. This does not supply remote entanglement acquisition for free.

During long waiting/storage, use the old resource theorem's exogenous local Poisson-CPTP fault-location class, with arbitrary state- and record-dependent local CPTP actions on the SAME bath. The native memory theorem applies to this subclass of its continuous perturbation class. This composition does NOT promote the old atomic resource theorem to generic coherent continuous noise. Additional bounded local coherent control/calibration error may be allowed only during the finite endpoint and subsequent native-only stage, where forward Duhamel/native estimates actually cover it. Rates and onsite control norms are uniformly bounded independently of N; all actual scheduled joint propagators and killed compressions exist and are normal CPTP/CP-TNI on every interval.

The old DATA instruments have rates <=ell, including Alice's atomic quantum READ and Bob's atomic current-read/correct commit. Their supports and incidence are fixed. Other old classical reset/watchdog/FIFO operations retain fixed rates. The old theorem's favorable word probability remains strictly positive for every ell>0, however impractically small; choose its service-window length and external fault threshold after ell.

## 2. Fixed finite endpoint: no encoded decoding or global parity computation
All durations below are fixed constants independent of N. Endpoint latency T_end is their sum, including ramps and bounded message propagation. If the supplied network has N-dependent latency or bounded aggregate rather than per-column bandwidth, that latency must replace T_end in all bounds; no constant-time claim then follows.

1. **Source access.** Use the accepted live-BUSY tail and finite first-initiation/payload shutoff on Q. Its remaining weak first edges during the ramp are charged as local insertions. The resulting physical Q DATA lie, up to exponentially small channel error, in a bounded-weight common Pauli span on Enc_Q; no ideal native-forest inverse occurs. The old A:B resource stays enabled. All its DATA attempts during this endpoint are charged as described below, so no Alice-check commutation with a partial Bell gate is assumed.
2. **Finite initialization.** New native B controllers, measurement pointers and private raw-message registers are reset by actual complete finite-rate onsite channels with their DATA couplings held off. Controller monitors need not be purified. There is no finite-time perfect reset: sparse unfinished parts are explicitly charged. The native B registers may be booted in parallel before the Bell stage, keeping these resets on until the activation stage. Old B correction is still physically on.
3. **Physical Bell instrument.** A bounded onsite Hamiltonian pulse implements CNOT Q_i -> A_i at every colocated column. Then finite local pointer instruments measure X on Q and Z on A. For Hermitian two-level observable O, a pointer has wait,+,- labels and jumps sqrt(kappa)|b><wait| tensor Pi_b^O. The unfinished effect after time T_meas is exactly exp(-kappa T_meas) I. Pointer outcomes are actual measured classical symbols, not perfect preexisting bits. Every calibration error and arbitrary local fault during partial gates/readout is charged by its fixed column light cone.
4. **Raw communication.** The two physical Bell bits at each column are sent through that column's private finite FIFO path to a B latch. No logical syndrome decoding or global parity computation is required. Registers are finitely booted first; a boot failure is an exceptional column, not an accepted stale epoch. On an otherwise clean column, the source waits until both pointer values exist, then the finite channel delivers them. Repeated fixed clock-word trials give a uniformly small unfinished-delivery probability after fixed T_msg. Actual fault locations affecting any pointer/slot/worker/latch mark that column (or the bounded set of columns sharing the physical patch). At the deadline a missing value is replaced by the declared default 00; this is not postselection.
5. **Finite actual mask pulse.** With p=(x,z) in the local latch, choose the Hermitian Pauli P_p in {I,X,Z,Y}, where Y differs from XZ only by a branch phase. During duration tau, use H_p=pi(I-P_p)/(2 tau). The actual unitary is P_p, not a decoder convention. Corrupt/missing latches and faults during the pulse are exceptional columns; correct latches are stable absent charged faults. A finite ramp/pulse shape is equally valid when its integrated scalar angle is pi/2. Norms and duration are fixed and calibration errors are included. No program register whose old phase must be undone is needed.
6. **Native activation and overlap.** Switch off the new-controller boot resets through a fixed waveform, then turn on the new native generator through a finite waveform. For the support estimate use its first-initiation-OFF generator as nominal and charge the weak first-edge Hamiltonians of amplitude epsilon_new as local insertions. Every other actual term preserves coarse ready owners and can touch DATA only in the initially nonready-owner footprints or footprints activated by charged insertions. At activation exit the full native generator is on. The old atomic DATA rates remain <=ell and are subsequently ramped to zero; their maps are arbitrary allowed local perturbations throughout that overlap. Remaining old auxiliary-only dynamics are spectators and need not be erased.

No interval assumes an instantaneous reliable feedforward, perfect native controller reset, encoded factory, decoder/re-encoder, or bath refresh. The old engine being enabled is not the proof of protection during steps 1–6; Section 4 is.

## 3. Uniform exceptional-set and insertion budgets
Let N count one block length; all additional counts are O(N). Fix small positive densities beta_boot, beta_meas, beta_msg and rho_P. Reserve a fixed finite DATA-support enlargement q_ep for all local endpoint/old-instrument/first-edge supports, their finite column gate cones, and the full native-owner footprints they can activate. Pointer-only and classical-latch faults count their associated DATA columns.

### 3a. Finite boot
Complete onsite reset at rate >=kappa gives a uniform joint unfinished-part inclusion bound exp(-kappa T_boot |S|) in the nominal model. The accepted backwards-test proof extends this to bounded continuous local noise with p_boot=[u+(1-u)e^{-kappa T_boot}] exp(C(u) eta T_boot). It holds for arbitrary incoming controller/bath correlations. The old DATA instruments do not act on the new controller registers. A subset union and bounded-incidence enlargement give at most beta_boot N affected native owners/teleportation columns except with exp(-cN) probability. The test is a positive effect, not a stochastic Pauli interpretation.

### 3b. Measurement and communication
On nonfaulted, successfully booted columns, finite X/Z pointer failure has tensor-product effect bounded by p_meas^|S|, p_meas<=2e^{-kappa T_meas} after assigning the two bits their bounded witnesses. Entanglement between columns and bath does not change that operator identity. The fixed-length private classical protocol has a finite successful clock word, hence a miss bound p_msg=(1-p_word)^J after J trials. The relevant exogenous clocks are private; a finite coloring suffices for bounded sharing. Declare fault-spoiled words exceptional rather than condition their success on an independent-noise assumption. Choose T_meas,T_msg so the combined unfinished/boot count exceeds (beta_boot+beta_meas+beta_msg)N with exponentially small positive-instrument mass.

### 3c. ALL old DATA attempts and actual faults
The old DATA attempt processes have total rate <=C_old ell N. Count every attempt, disabled or otherwise. The sum over the finite endpoint is Poisson-dominated, so for rho_old>0,

    Pr(K_old >= rho_old N) <= [e C_old ell T_end/rho_old]^(rho_old N)

when the bracket is <1 (a harmless exp(C_old ell T_end N) version also works). Their arbitrary DATA/control action and shared bath dependence do not alter the exogenous count law. External Poisson fault locations have the same form with eta in place of ell and their charged support constants. This is not a sparse conditional Pauli-mixture claim.

### 3d. Coherent controls and weak initiation
Use forward Duhamel expansion about the actual nominal CP endpoint propagator; never invert a dissipative propagator. The aggregate joint cb norm of coherent calibration plus weak first-edge perturbations is bounded by

    Lambda <= C N [eta_cal + epsilon_Q 1_source-ramp + epsilon_new 1_activation].

Over the fixed waveform let zeta=N^{-1} integral Lambda. The order-r tail at r>=rho_D N is at most

    exp(zeta N) [e zeta/rho_D]^(rho_D N).

For fixed small zeta/rho_D this is exp(-cN). Each retained order adds at most q_ep DATA/owner support on each ket/bra. The truncation is signed, not CP. Low-order support is observed only AFTER the tail is bounded in cb norm, so no exponential sum of Pauli coefficient magnitudes appears.

## 4. Common-channel support and warm entry (main proof obligation)
The start of the endpoint must be represented by ONE joint good CP/TNI channel on Q,A,B and every auxiliary/bath, not by multiplying reduced-state fidelities. In its canonical coefficient module, every term has the form

    E_Q Enc_Q(rho_L)  together with  (I_A tensor F_B) Omega_s,

with fixed bounded reduced weights for E_Q,F_B, arbitrary coherent signed sector s, and ONE joint auxiliary coefficient. Source access contributes its actual sparse busy/first-edge support. The coefficients are independent of the unknown logical input, although all auxiliaries can be mutually correlated. The joint-safe construction and Bell contraction are supplied in the companion common-span derivation, to be audited.

For ideal full physical Bell outcome P,

    T_(s,P)=Pi_s P^dagger/sqrt(KD),
    P T_(s,P)=Pi_(s+sigma(P))/sqrt(KD).

On the compatible encoded input sector, this is the identity logical map times an auxiliary scalar. Local input/resource/endpoint operators only add local DATA Pauli factors; arbitrary unfinished local Bell instruments and wrong masks are confined to the same exceptional columns. Expanding only finite system legs, every coefficient after the actual mask pulse has

    E_out Enc_B(rho_L),
    |supp E_out| <= r_Q N+r_AB N+r_access N
                   +q_ep[(beta_boot+beta_meas+beta_msg+rho_old+rho_fault+rho_D)N].   (4.1)

The output source Q,A/pointers/messages are retained auxiliaries. This is a common error MODULE, not a claim that the physical output is a Pauli mixture. Its span is correctable by the ordinary fixed zero-code DATA recovery whenever twice the right side is below d_N. The Pauli mask is physically present; the recovery does not apply it or a target logical gate.

During native activation the first-initiation-OFF readiness support theorem applies on every coherent malformed source mask. If S is the union of initially nonready owners and those touched by retained insertions, every nominal DATA coefficient is identity outside the union of their fixed footprints. Outside S the native forest is identity and every history flag is zero. Consequently after applying the new native forest ANALYTICALLY, the same module has

    canonical reduced weight <= w N,
    sum_h B_h <= b N,
    U+R sum_h B_h <= (c_U w+R b)N.                  (4.2)

This analytical change of representation is not a physical inverse or re-encoder. The constants w,b are fixed linear combinations of the small budgets in (4.1), the native boot density and the activation insertion density. They can be made as small as the already fixed native warm gap requires.

Let P_new be the accepted native global basin and F_new its positive proof observable, with F_new<=exp(gN) exp(s[U+R sum B]). Choose budgets so (4.2) is strictly inside P_new and

    nu_w = g+s(c_U w+R b) < s_prime e_cut-q_t-gap,

for a fixed gap>0 of the accepted warm theorem. Project analytically onto the bounded-controller/basin events. The actual positive channel differs from the common-span signed comparison only by the already bounded tails and gentle projections. In the canonical gauge the latter is Id_L tensor tau_signed. Extract a positive ancillary state sigma=Tr_L A(omega_L) from any fixed normalized omega_L under the actual projected CP/TNI channel A. Contractivity gives ||A-Id_L tensor sigma||_diamond at most twice the signed comparison error. Sigma has P_new support and the same warm moment bound, because the labels/basin projection commute the raw diagonal majorants. No signed map is called CP, and no arbitrary logical/bath correlation is reinitialized away.

Once this warm channel is earned, the actual new native killed evolution applies uniformly to sigma. Every remaining old DATA generator ell(Phi-id) has joint cb norm <=2ell, bounded support/incidence, and may be included even with garbage old records. Fast old auxiliary-only generators annihilate all new proof observables and commute the new basin. Thus the old-rate ramp is covered by the native theorem, not by a long endpoint count. Later native protection lasts for its exponential horizon.

## 5. Noncircular rate order and anticipated error bound
1. Fix code margins, actual new-native hardware and proof parameters, including its positive perturbation threshold eta_native, warm gap and sufficiently weak first initiation for the fixed activation/access waveforms.
2. Fix the allowed endpoint support densities, all physical boot/measurement/message/pulse/ramp durations and the finite protocol hardware. T_end depends on these, NOT on old DATA service.
3. Choose every old DATA rate ell>0 so C_old ell T_end is below the endpoint count budget AND 2 C_inc ell<eta_native/4. Keep the old watchdog/FIFO rates fixed. The old Bell machine still has a strictly positive finite service word, although its service time can become enormous.
4. Recompute the old resource's actual service window and Poisson fault threshold at these rates. Choose the external fault intensity below BOTH old and new thresholds and every finite endpoint bound. Choose endpoint calibration error and raw-source error budget last. Nothing forces ell*T_service small; only ell*T_end is small, and these are different times.

For waiting durations t_Q,t_AB and subsequent native storage t_rec, the target bound is of the form

    ||D_fixed output_B - Id_L||_diamond
       <= 2 delta_source + C poly(N)(1+t_Q+t_AB+t_rec) exp(-cN),

with the same fixed ordinary DATA recovery, fixed positive constants, and N>=N0. A destructive source measurement has transferred the unknown state; the recipient DATA remain quantum and protected. This does NOT supply a bare unknown-input encoder, physical quantum decoding/retrieval, ideal classical computer, arbitrary-latency routing, autonomous endpoint timing, universal computation or a native-old LOCC compiler.

## 6. Strong ordinary comparison
A scheduled implementation given exactly the same raw Bell source, colocated CNOTs, noisy local pointers, private finite-bandwidth channels, control waveforms and native receiver can perform the same transfer. Raw physical feedforward avoids global logical parity latency in BOTH routes. The rate-separated overlap is an explicit safe interface, not a new teleportation identity or an asymptotic speedup over ordinary teleportation/Pauli frames. If one instead permits an indefinitely deferred logical Pauli frame, that comparator must still reconcile the raw signed resource's extensive nonzero syndrome; the ordinary zero-code receiver cannot silently correct the wrong coset while waiting.

## Current proof status
The component resource, native memory, source access, boot and finite support lemmas are separately accepted. This document is NOT yet a whole receipt. The linked joint-channel Bell module, exceptional-column measurement/routing construction, positive warm replacement and exact finite activation accounting must be read together and independently reviewed before promoting the recipient claim.
