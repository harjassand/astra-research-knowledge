# Generic active matrix acquisition: finite-payload private-framed complete error

28 October 2026. Separate deployment corollary of the received generic matrix GLS/direct-decoder theorem and the received private-framed complete-optimality theorem. Independent receiving is pending. No frozen source is modified and no new acquisition mechanism is asserted.

## 1. The exact operational comparator

Keep the stationary/reset source, fixed four-real-coordinate isometric encoder family, supplied valid rank bound R, and paid retained output frame k<=8R of the received generic matrix theorem. There are NO known-flag, spectral-floor, zero-optimum or useful-seed assumptions. Put

    a(x)=max_(D CPTP) F_e(D E_x),
    a_*=max_x a(x), ell_*=1-a_*.

Fix an integer M>=1 BEFORE calibration. Each arbitrary logical payload qubit receives one independent uniform Pauli before its selected encoder/source call; undo the same Pauli after recovery. Keys are independent of payload/reference/calibration and remain private or discarded from the tested channel. Generation, storage or trusted delivery of2M key bits, and all framing controls, are paid.

The comparator may know the source exactly, choose any predetermined list of encoder settings x_1,...,x_M, and use arbitrary key-dependent COLLECTIVE CPTP recovery, receiver ancillas and payload-independent programs/calibration. There is exactly one source use per logical payload. Across-use encoding, lower-rate codes, payload-feedback encoder choices, extra payload-dependent source calls, postselection, a quantum bypass, and exported key/calibration records are excluded. Arbitrary entanglement among the M payload inputs and an untouched external reference IS included.

The positive recovery-SDP tensorization and private-frame Bell-test identity in `direct_cptp_bures_bridge_20261027/PRIVATE_FRAMED_COMPLETE_OPTIMALITY.md` give, for each such list,

    f_opt(E_(x_1) tensor ... tensor E_(x_M))=product_i a(x_i)
                                                          <=a_*^M.

Repeated optimal encoder/recovery attains the bound. Therefore the exact UNHALVED complete-error comparator in this fixed-one-use-per-payload family is

    Delta^*_(family,frame,M)=2[1-a_*^M].                    (1)

This includes collective recovery; it is not merely a comparison to a product decoder. It deliberately does not compare against changed coding rates.

## 2. Run the received active learner once, with one longer retained horizon

Set gamma_0=gamma/2 and zeta=epsilon/(4M), for0<gamma,epsilon<=1. Run `ordinary_generic_matrix_gls_direct_decoder_corollary_20261028.md` (SHA a9c040dc5884b3223400c24a46e857082d8ab509c91e816fa3c5d960b57d0067), using its received main/cap imports, at local parameters gamma_0,zeta. It returns one actual feasible encoder and full CPTP decoder from ordinary pre-datum calibration. The actual deterministic calibration cap obeys

    N_cal=O_tilde[k^4 M/(gamma epsilon)+k^(9/2) M/epsilon]. (2)

Use its explicit fixed-cap formulas at those parameters. Compile the common receiver frame for H=N_cal_bar+M, NOT N_cal_bar+1, before calibration starts. Retain the SAME causal frame through all adaptive homogeneous matrix-query banks and every subsequent payload. All local random-purification banks are consumed; no purification gauge is aligned or reused as an unknown program. The final classical decoder acts only in this retained frame. There is no fresh unknown decoder oracle after encoder selection.

The exact-reference part of the received local proof, including failure histories and all imported finite matrix-query statistics, gives

    E_(U,h) ell_h <=(1+gamma/2)ell_*+zeta.                 (3)

Here U is the one mathematical common output frame and h comprises pre-payload calibration records. The stronger good-branch bounds in the source leave slack for (3). One must use that exact-reference analysis and transfer complete physical implementation error ONCE in Section4, rather than insert a one-payload process discrepancy M times without accounting for it. Local query precision restrictions, including zeta_query<=m^(-2), remain those of the received fixed cap.

Conditional on U,h, every selected policy is physical, so f_h=1-ell_h<=a(x_hat)<=a_*. All M future source resets are the same selected encoded channel in that common frame. The arbitrary-operator causal law, including references, is what justifies this statement despite the processor's evolving quantum memory. Conditioning only on physical records is not substituted for that law.

## 3. Shared calibration errors do not require iid averaged payload noise

After the private independent Pauli average, the exact-reference block channel is

    Gamma_M=E_(U,h) [Twirl(D_h E_(x_hat,U))]^(tensor M).

This is generally a CORRELATED Pauli channel. Its identity probability is E f_h^M, NOT (E f_h)^M. Therefore

    ||Gamma_M-id||_diamond=2[1-E f_h^M].                  (4)

For any f in[0,a_*], the elementary power difference gives

    a_*^M-f^M<=M a_*^(M-1)(a_*-f),
    M a_*^(M-1)(1-a_*)<=1-a_*^M.

Using (3), taking expectations and including endpoints by continuity yields

    a_*^M-E f_h^M <=(gamma/2)(1-a_*^M)+M zeta.

Combining with (1),(4),

    ||Gamma_M-id||_diamond
       <=(1+gamma/2)Delta^*_(family,frame,M)+epsilon/2.    (5)

This compares to the exact global framed optimum, not only a union bound2M ell_*. It uses only the averaged local guarantee plus pointwise physical feasibility; it does not infer a conditional quality guarantee for any exposed record.

## 4. Complete finite bill and scope

Allocate total UNHALVED process discrepancy nu<=epsilon/2 between the implemented experiment and the exact reference. This includes all ordinary preparation/reset controls, matrix-query receiver instruments not already debited inside their received finite statistics, the entire H-step causal frame, all stored quantum memory/control, the M uses of the known decoder and selected encoder, private-key operations, and all finite arithmetic/synthesis debits. Use the deterministic worst-case gate/horizon caps to choose per-operation precision uniformly on every history. Decoder error is paid M times. The adaptive CPTP hybrid bound works with memory and arbitrary external references.

Discarding the keys, calibration transcript and internal memory is part of the tested logical-output convention. The triangle inequality gives the actual bound

    ||Lambda_actual,M-id||_diamond
       <=min{2,(1+gamma)Delta^*_(family,frame,M)+epsilon}.  (6)

Total source calls are N_cal+M; the additional M are payload calls. The chosen-x matrix-query invocation count is O_tilde(k^2), with logarithms now also depending on M. The received compiler still pays theoretical polynomial known gates/workspace in H,k,log ambient dimension and log inverse process tolerance. There is no claim of constant memory, a reusable future-physical-input decoder, practical conservative-cap runtime, hardware execution or quantum capacity. The same strongest equally informed conventional learner may use this construction.

This is a ONE-calibration, finite-horizon operational closure of the received generic learner. If a later separately received local learner improves the calibration function while preserving the same common-frame/averaged-risk contract, substitute that function in (2) at (gamma/2,epsilon/(4M)); equations(1),(3)-(6) do not change. In particular an unreceived clipped-GLS candidate is NOT silently promoted here.

Governing scientific imports are the frozen generic matrix main/cap/direct-decoder proofs and their receipts, the later explicit online causal compiler and receipt, and the already received private-framed complete-optimality/product-SDP theorem. The analogous received intrinsic-flag finite-payload note is precedent for the same scalar composition, not a source-structure assumption in this theorem.
