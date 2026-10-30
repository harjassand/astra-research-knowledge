# Bilateral Bell target: exact LOCC algebra and remaining interface
2026-10-30. Independent ordinary proof and audit; the algebra is standard CSS entanglement purification. The proposed consequence is its compatibility with native autonomous relative-error protection, not a new entanglement-distillation identity.

## Result first

**The Bell-only initialization escape is algebraically valid.** Physical Bell pairs need neither a known common syndrome nor an encoded-state factory before a relative-syndrome controller can start. A matched pair of local check instruments sees only the error DIFFERENCE. It may measure/dephase the common syndrome without disturbing the target encoded Bell factor. Arbitrarily large common Pauli errors are harmless to this TARGET, including common logical Paulis.

This is a target-state/coherent-span statement, **not** a quantum code of distance d protecting arbitrary 2k logical inputs against common Pauli errors. A final decoder must first correct the small relative error; applying two unrelated ordinary local decoders to signed sectors is insufficient. The ideal instruments below are genuinely LOCC. A coherent inter-half parity gate is not a substitute.

A particularly useful strengthening: n perfect physical Bell pairs already lie in the entire good Bell-target span. There need not be a complete initialization syndrome-measurement round, a global barrier, or global feedforward before waiting. This removes the persistent classical baseline from the algebra. It does not by itself compile the asynchronous noisy classical communication and controller schedule.

## 1. Conventions and exact target span

Let S have r=n-k independent commuting stabilizer generators g_1,...,g_r for an [[n,k,d]] code. CSS generators are real, so the same check is measured on the two sides. For a general stabilizer code, Bob measures the entrywise conjugate g_j*; this handles Y signs correctly. Write

    Pi_s = product_j [I+(-1)^(s_j) g_j]/2,
    |Phi_n> = 2^(-n/2) sum_x |x>_A |x>_B,
    |Omega_s> = 2^(r/2) (Pi_s tensor I)|Phi_n>.

The Pi_s have rank 2^k. The Omega_s are orthonormal. The identity

    (M tensor I)|Phi_n> = (I tensor M^T)|Phi_n>

implies that Omega_s occupies C_s on Alice and its conjugate C_s* on Bob. For any orthonormal basis {|s,l>} of C_s,

    |Omega_s> = 2^(-k/2) sum_l |s,l>_A |s,l>*_B.             (1)

Choose an isometry V_0 into the ordinary code and write Phi_L=(V_0 tensor V_0*)Phi_k. If T_s is ANY unitary Pauli taking C_0 to C_s, then

    |Omega_s> = (T_s tensor T_s*)|Phi_L>.                   (2)

Equation (2) is independent of the choice of T_s: two choices differ by a normalizer operation, and U tensor U* fixes a maximally entangled state. No minimum-weight or efficient choice of T_s is required for this identity.

Let W: |s>_G -> |Omega_s>. Its range B is the good Bell-target subspace, of dimension 2^r. For an arbitrary reference/bath R and arbitrary state tau_GR,

    (D_A tensor D_B* tensor id_R) W tau W†
      = |Phi_k><Phi_k| tensor J tau J†,                    (3)

where D is a matched full signed-sector decoder, D|s,l>=|s>|l>, and J|s>=|s>_A|s>_B. Equation (3) is an exact factorization of the LOGICAL BELL TARGET, uniformly for coherent gauge states entangled with a retained bath. It does not require sampling a classical syndrome s.

One may choose D to be a Clifford stabilizer decoder. Then a fixed symplectic set of physical logical generators becomes the usual logical Pauli set. B is equivalently stabilized by:

- g_j,A tensor g_j,B* for all r generators;
- bar X_a,A tensor bar X_a,B* and bar Z_a,A tensor bar Z_a,B* for all k logical qubits.

These are r+2k=n+k independent commuting checks on 2n qubits, leaving dimension 2^r. Local g_j,A and g_j,B measurements do not measure a logical Bell degree of freedom.

## 2. Exact physical-Bell initialization instrument

Alice and Bob independently measure their complete local stabilizer families. The joint Kraus operator for outcomes a,b is

    K_ab = Pi_a tensor Pi_b*.

On the raw Bell source,

    K_ab |Phi_n> = delta_(a,b) 2^(-r/2)|Omega_a>.            (4)

Each matched syndrome has probability 2^(-r). Thus the postmeasurement state contains k encoded ebits in an unknown common signed code sector. No nonlocal measurement or entangling inter-half gate was used; classical communication is not even needed to establish (4), only to compare noisy later outcomes.

More strongly,

    |Phi_n> = 2^(-r/2) sum_s |Omega_s> = W|+>^r.            (5)

Consequently the raw source is already in B. The controller may acquire the common syndrome gradually and asynchronously. Clean local measurements simply dephase/project its G factor. This is the sense in which a full preparation barrier can be omitted. It is not a claim that 2n arbitrary separable qubits can be turned into Bell pairs by LOCC.

## 3. Common versus relative Pauli errors

For a Pauli P, let sigma(P) be its commutation syndrome. Up to physically irrelevant Pauli conventions,

    (P tensor P*) W = W Gamma_P,
    Gamma_P |s> = |s+sigma(P)>.                            (6)

Common logical Paulis have zero syndrome and act identically on B. A general paired Pauli error reduces to a relative error on one side:

    (P_A tensor Q_B) W
      = (I tensor P^T Q) W Gamma_P                        (7)

up to an overall phase from Pauli ordering. The relative binary symplectic label is p+q. Its occupied column support is contained in the union of the physical A/B fault supports. There is no need to expand an unknown common error into an extensive relative error.

Equations (6)-(7) are linear identities, so a local CPTP fault with a retained environment can be expanded into local Pauli coefficients without sampling those coefficients as stochastic errors. Different terms may have coherent relative errors and coherent gauge changes. A future common-correctable-span proof must control ALL terms compatible with a positive physical record. The algebra supports that proof; it does not by itself supply the needed record probability estimate.

## 4. A genuinely LOCC relative-GPT transaction

Let I_h index the commuting local checks read by a particular bounded hub. Write Pi^h_a for their joint local spectral projector. Alice measures Pi^h_a, Bob measures (Pi^h_b)*, and their classical records are compared. Let f_h(a+b) be the prescribed finite GPT move, applied on Bob only. An ideal fine-result Kraus operator is

    K^h_ab = [I tensor P_(f_h(a+b))]
             [Pi^h_a tensor (Pi^h_b)*].                   (8)

This is a local measurement on each side, classical communication/computation, and a local Pauli. It is LOCC. The source-side outcome register must actually be dephased/measured before an alleged classical communication channel is used. Coherently measuring only g_A tensor g_B* is a different operation: it need not be LOCC and can generate entanglement from a product input.

For a relative Pauli E, set e=sigma(E)|_(I_h). On a definite common-syndrome component,

    K^h_ab (I tensor E)|Omega_s>
      = 1[a=s|_(I_h), b=a+e]
        (I tensor P_(f_h(e)) E)|Omega_s>.                 (9)

On W with a coherent gauge state, replace the first indicator by the gauge projector onto s|_(I_h)=a. In particular, the correction decision depends only on e, never on the unknown common syndrome. Nominal local measurement outcomes can be extensive/random, while the syndrome DIFFERENCE is the ordinary small-error syndrome.

Thus clean instruments preserve the same relative Pauli/GPT trajectory as the ordinary controller, tensored with a gauge instrument. Errors in extraction, stale caches, transmission or reset are not magically canceled: they are actual local transaction faults and need the parent's charged read/dependency/scheduler proof. Inter-half classical latency must be included in the physical service window. No bounded-distance classical channel or instantaneous global feedforward is granted here.

The full-table consistency caveat in the fixed-baseline approach does not arise nominally: the difference of two actual simultaneous valid syndrome vectors is valid. Asynchronous mixed-age caches can be inconsistent, but that is the ordinary transactional read-consistency issue, not a permanently invalid target syndrome.

## 5. What is actually protected, and the correct output decoder

Choose the usual correctable family of small relative Pauli representatives R_delta, with a deterministic tie rule. A suitable ideal OUTPUT decoder is the following LOCC map:

1. Locally measure full syndromes a and b, and communicate their difference delta=a+b.
2. Compute the relative recovery R_delta and apply it to Bob.
3. Decode both now-matched signed sectors using the SAME signed-sector convention D (or equivalently apply matched T_a† and T_a^T before ordinary local decoding).
4. Discard the syndrome/gauge registers.

For every relative error E in the decoder's guaranteed family, R_delta E is a stabilizer on the original code, and it is a scalar on each signed sector. Therefore the corrected output of every vector (I tensor E)W|gamma> is Phi_k times a gauge vector. The same remains true for any coherent superposition of these correctable errors and any retained bath. This is the exact common-span target relation needed by an autonomous memory proof.

For sequential trajectories, the reviewed canonical-edge condition suffices in relative coordinates: if consecutive representatives R,R' and one local relative move f obey

    sigma(R+f+R')=0,    |R|+|f|+|R'|<d,

then R+f+R' is a stabilizer. The target Bell action is identity, regardless of the common syndrome and its previous measurement record. This uses the original SINGLE-BLOCK code distance for relative errors, not a purported distance of the joint Bell-target code.

**Why two independent decoders alone fail.** A small physical error need not have trivial logical component in a fixed signed-sector decoder. For the Steane code with bar X=X^7, a single Z on Bob flips bar X_A bar X_B even though it is correctable. A decoder that simply exposes these fixed logical observables outputs the wrong Bell phase unless relative recovery is performed first. Likewise, independently chosen T_a and T_b do not cancel when a differs from b. One cannot drop step 1-2 on the ground that each half is in some valid code coset.

This decoder is a mathematical output interface unless physically compiled and fault-protected. It is sufficient to define retained encoded entanglement and to prove its fidelity. It is NOT a claim of exponentially accurate bare Bell-pair delivery through an unprotected final port. Finding ANY T_a is ordinary binary linear solving, rather than decoding a high-energy random syndrome to minimum weight; that distinction removes a computational problem but not its noisy implementation/latency.

## 6. The subsystem-code overclaim to avoid

Common P tensor P* errors act only on the G label when restricted to B because B has a FIXED logical Bell target. On the larger space C_s tensor C_s*, common logical Paulis generally act nontrivially on arbitrary two-sided logical states. For example bar Z_A bar Z_B fixes Phi+ but changes the sign of a superposition of Phi+ and Psi+.

Thus declaring every common physical Pauli a gauge operation of a subsystem protecting arbitrary 2k logical qubits would be false. The algebra generated by all common single-column Paulis also includes common logical Paulis. What is valid is:

- an exact Bell-target/gauge factorization (3);
- a common correctable span around that target;
- relative logical preservation and decoded entanglement fidelity.

Because the target is pure, on a good positive record its decoded Bell output is decoupled from all remaining gauge, controller and environment registers. If the total bad-record weight is at most delta and the good/bad split is a genuine CP-instrument split, the output trace-distance error is at most 2delta. A diamond-norm theorem for arbitrary input logical states does not follow from this target-state argument. One can state a diamond bound from the gauge-input channel to the constant Bell-output channel, including arbitrary gauge references, if the same uniform bad-record bound is proved.

## 7. Noise scope and initialization seed

For a depth-O(1), bounded-incidence raw physical Bell source with local faulty locations, each fault has only bounded paired-column spread. Expanding arbitrary local CPTP source faults into Pauli coefficients yields a common relative-support majorant. A local-stochastic source-location law or appropriate positive-record moment bound then supplies a sparse initial relative seed. This is not an assumption of perfect encoded Bell pairs. If the physical source is only promised a high average fidelity per pair, with unrestricted correlations, that does NOT imply an exponentially small total-error tail; the source locality/moment hypothesis must be explicit.

The same autonomous protection would require:

- all actual LOCC check/read/correction operations, classical packets and mode changes included in the noisy apparatus;
- finite physical propagation time or a geometrically specified classical network, not free instantaneous remote gates;
- clean/charged controller initialization and one positive record controlling every coherent Pauli history;
- no extra uncontrolled cross-half Hamiltonian or environment supplying free entanglement.

The last point is a resource-accounting requirement. An arbitrary retained bath shared across the laboratories can itself carry entanglement. A performance theorem may still tolerate it adversarially, but an assertion that the actual implementation is LOCC must restrict the bath/communication realization accordingly. Local baths with shared classical randomness suffice for strict LOCC. It is legitimate to prove a stronger robustness statement allowing non-LOCC adversarial local interactions with a shared bath, provided it is not counted as a free LOCC resource.

## 8. Constructive ordinary alternative and honest consequence

The baseline is standard CSS entanglement purification. Shor–Preskill explicitly describe separate CSS-check measurements on the two halves, the common signed code obtained from ideal physical Bell pairs, syndrome disagreement under bit/phase errors, recovery, and local decoding. Bennett–DiVincenzo–Smolin–Wootters place this in the broader equivalence between one-way purification and quantum error correction. Sources:

- https://arxiv.org/pdf/quant-ph/0003004 , p.2, equations around the signed code Q_(x,z) and the following purification paragraph.
- https://arxiv.org/html/quant-ph/9604024 , sections 3 and 5.

With equal access to noisy physical Bell sources, local CSS-check apparatus and classical communication, an ordinary active implementation can repeatedly schedule the same bounded local relative-GPT transactions. It can also use its usual global decoder if that computational resource is equally available. Neither comparison is denied perfect classical memory solely to favor autonomy.

The new useful possibility is not distillation from nothing. It is a positive-rate, long-lived store of distributed encoded ebits initialized directly from physical Bell pairs, without first producing a known signed-sector encoded state, without storing a persistent random baseline, and without a high-energy global syndrome decoder before the protected wait. The reviewed autonomous service/noise theorem must still be extended to the actual LOCC transaction architecture. Successful extension would supply a real Bell-resource initialization bridge; arbitrary unknown-state loading and fault-tolerant bare extraction would remain separate tasks.
