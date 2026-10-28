# Frozen on-site receiver: exact repeated-service output-noise factorization

2026-10-28. New root construction, independent review pending. Governing acquisition source: ordinary_onsite_two_axis_frozen_memory_recovery_20261028.md, SHA256 7df4d169cc544b79456e7410da7ac3ec991482311a0d3831569efc573455dd53, with root and independent statistics receipts. This is a finite repeated-service extension, not a claim that the source header's one-service theorem already proves reuse.

## Interface and comparator

Keep the exact fixed on-site logical algebra and uniform conditional X/Z CP contrasts of the governing source. Calibrate before introducing unknown payloads. Thereafter use T predetermined service slots, each with q logical inputs; their joint input may be arbitrary and entangled with an external reference. For the stated qT-input diamond-channel comparison, the full payload/reference is initially product with the source memory conditional on the calibration record. The algebraic identities also hold on the enlarged input domain including memory, even with initial correlations, but those are not an induced channel on payload alone. Source memory may be retained and coherent across slots. Outputs of completed slots are isolated: no output-dependent feedback, reinsertion, or later joint operation involving them until all services finish. Future input registers are held outside source access until their slot. Any required input/output storage is a charged interface, not free quantum memory. The current private input/output Pauli frames remain hidden and nonanticipating through the complete source port.

The benchmark is the SAME multi-call physical source, with the TRUE fixed on-site extraction at every slot. Denote its joint channel E_exact. It may be a correlated memory channel. We do not assert that this benchmark is a collective full-CPTP optimum. Global CP identity dominance is unnecessary for closeness to this benchmark (it is only needed for the earlier one-slot oracle interpretation). Calibration supplies one fixed record h and thus matching and fitted rotations; on good records the matching is correct.

## Exact instrument identity

For each logical site let W_i=Vhat_i^dagger V_i and W=tensor_i W_i. Conditional on any source Pauli label alpha, the exact on-site extraction yields P_alpha on the logical inputs and the CP gauge-memory map G_alpha. On the actual learned service, draw Q uniformly among q-qubit Pauli operators, apply Q before the source and Q^dagger after the fitted inverse rotations. The logical operator is

    Q^dagger W P_alpha Q = phase(alpha,Q) (Q^dagger W Q) P_alpha.

The phase cancels in the CP map. Since G_alpha is independent of the fresh private Q, averaging the complete instrument gives

    E_learned,framed = (Lambda_W tensor id_gauge,memory) composed E_exact,
    Lambda_W = average_Q Ad_(Q^dagger W Q).                    (1)

This identity is completely linear and holds also when the current logical input is correlated with retained memory or other payload registers. It is not merely an equality of single-input Bell fidelities. Expanding W in orthonormal Pauli operators gives the exactly physical channel

    Lambda_W(rho)=sum_P |Tr(P^dagger W)/2^q|^2 P rho P^dagger.  (2)

Since W is a product, Lambda_W=tensor_i Lambda_(W_i). Its identity probability is

    p0=product_i |Tr(W_i)/2|^2 = 1-e_h.                       (3)

The frames must be independently refreshed at EVERY service slot; reusing a hidden frame does not yield the tensor factorization below.

## Retained-memory composition

The error channel in (1) acts only on the isolated completed output. It commutes with every later source operation, including those on later inputs initially entangled with that output, because those operations act on disjoint tensor factors. Move each such channel to the end of the circuit. Conditional on the fixed calibration record and initial service memory, the entire learned joint channel satisfies

    E_learned^(T) = Lambda_W^(tensor T) composed E_exact^(T).  (4)

No independence of the source Pauli labels, gauge states or memory evolution is used. This includes correlated Pauli histories and coherent retained memory. The comparison uses the actual pre-service memory conditional on the calibration record, not a counterfactual calibration trajectory. Source-side classical dependence on external schedules is allowed if it does not reveal fresh frames or depend on isolated outputs; unrestricted decoder-output feedback is excluded.

The half-diamond distance between a Pauli channel and identity equals its nonidentity probability: upper bound by the convex decomposition and lower bound by orthogonal Bell states. The tensor Pauli channel on DISTINCT output registers has identity probability p0^T. Hence

    half ||E_learned^(T)-E_exact^(T)||_diamond
       <=1-(1-e_h)^T <= T e_h.                              (5)

The first inequality need not be equality after a noisy source. It is equality if E_exact is identity and the hypotheses W are fixed. We do not replace E[(1-e_h)^T] by (1-E[e_h])^T, nor silently condition away bad calibration records.

## Finite calibration and implementation

Let target 0<epsilon<=1, beta<=epsilon/8, and choose the governing fine-bank accuracy parameter epsilon0=epsilon/T. Apply its confidence derivation, sections 2–6, at (epsilon0,beta). That derivation allows arbitrary beta; the earlier final one-service corollary beta<=epsilon0/8 is NOT invoked here. Thus the same fixed banks are

    N0=ceil(3072 ceil(log2(8qn/beta))/kappa^2),
    N1=ceil(4096 q T ceil(log2(24q/beta))/(kappa^2 epsilon)),
    delta_fit=kappa epsilon/(32qT).

On a record event of probability >=1-beta, the fixed rotations have e_h<=9epsilon/(32T), uniformly over every possible subsequent source memory. With calibration-record TV error nu_cal and a uniform WHOLE-T-SERVICE half-diamond implementation debit nu_svc, actual mean joint-channel error to the benchmark on the actual post-calibration memory is at most

    9epsilon/32+beta+nu_cal+nu_svc <=21epsilon/32

when nu_cal+nu_svc<=epsilon/4. The good-record event is the same state-uniform event as in the received on-site proof. Flagged or undefined matching histories deploy a physical replacement. Other latent bad records need not be detectable and deploy their physical fitted receiver; their joint-channel distance is at most one and is charged by the same single bad-event probability debit, not T separate debits. If nominal source controls or frame secrecy fail, this statement is not certified.

Source calls: N0+N1 calibration plus exactly T payload calls. Every calibration prepares q inputs and reads n outputs. Fine classical storage and finite rational quaternion fits are unchanged except log(T) precision. Service uses q inverse single-qubit rotations and 2q fresh frame bits per slot, optional routing per slot, and paid storage of unserved inputs/completed outputs. Compiling a per-slot control half-diamond error nu_svc/T is sufficient for the whole service debit by a complete hybrid, including all routing, holding and reset operations actually used. No environment reconstruction, source reset or protected calibration entanglement is added.

## What this changes and what it does not

Under exact on-site structure, one fixed classical calibration supports a chosen finite block of future quantum service, even when noise retains quantum memory. The risk is controlled at the joint-channel level, not only each payload marginal. The price is a fine bank linear in T and trusted isolation/storage of the finite service batch. The conventional on-site estimator remains the learner; the addition is the exact output-noise commutation/factorization and its paid composition. This is not indefinite reuse, generic redundant quantum coding, a collective oracle theorem, a fault-tolerance threshold, or a hardware/practical advantage claim. Approximate locality destroys the exact factorization and requires a separate error analysis.
