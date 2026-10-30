# Signed-sector physical Bell swapping: exact encoded-recipient interface
2026-10-30. Independent algebraic proof, including coherent gauge inputs and bounded-spread noise. This is ordinary entanglement swapping used with the signed Bell buffer; no novelty claim for swapping itself.

## Main result

Two signed-sector Bell resources can be joined WITHOUT decoding their extensive common syndromes and without first converting either link to the zero-syndrome code. The middle station performs a full transversal PHYSICAL Bell measurement, sends its entire 2n-bit Pauli mask to one remote endpoint, and that endpoint applies the mask. The output is again a signed-sector Bell resource. The instrument preserves coherent common-syndrome superpositions within the measured relative-gauge sector.

The remote correction is an actual physical one-qubit Pauli layer, not a free ideal decoder. The mask transmission time must be bounded and charged. Before that correction the byproduct is generally extensive, so ordinary small-relative-error protection cannot simply continue through an arbitrarily delayed mask arrival.

## 1. Exact vectorization convention

Let D=2^n, K=2^k, and Pi_s be the real CSS syndrome projector of rank K. Use

    vec(M)=sum_(i,j) M_(i,j)|i>|j>,
    Omega_s=vec(Pi_s)/sqrt(K),
    beta_P=vec(P)/sqrt(D),

where P=X^x Z^z is a REAL unitary Pauli representative. P may be antisymmetric, but P^T=P† and the Pauli-labelled beta_P form a complete orthonormal physical Bell basis. A different conventional phase for each Bell ket has no physical effect.

Consider Omega_s on R,A and Omega_t on B,S. Project A,B onto beta_P. The unnormalized R,S vector is

    vec(Pi_s P Pi_t)/(K sqrt(D)).                         (1)

The real-Pauli convention removes conjugation ambiguity; for general conventions one must carry the corresponding transpose/conjugate in the applied mask.

Because P maps syndrome t to t+sigma(P), (1) vanishes unless

    sigma(P)=s+t.                                        (2)

If the outcome is compatible, apply P on S. Since (I tensor P)vec(M)=vec(M P^T),

    (I tensor P) [contraction (1)]
       =vec(Pi_s P Pi_t P^T)/(K sqrt(D))
       =Omega_s/sqrt(KD).                               (3)

Thus the normalized output is EXACTLY Omega_s. No recovery map is used in (3), and the common syndrome s need not be known. Each compatible P occurs with probability 1/(KD). There are KD=2^(n+k) compatible masks; all other masks have zero probability.

The middle operation is local at the station containing A and B, and is implemented by matching-column CNOT, H, and single-qubit measurement. The endpoints are connected only by classical messages after the input entangled links have been supplied. A quantum interaction between A and B at the same middle station is an accounted swapping operation, not an uncharged entangling channel between R and S.

## 2. Coherent common-syndrome input: exact gauge Kraus map

Let W|s>=Omega_s. Permit an arbitrary coherent gauge state on the two links, entangled with an arbitrary retained reference/bath:

    sum_(s,t) |Omega_s>_(RA)|Omega_t>_(BS)|chi_(s,t)>_E.

For a given physical outcome P, put delta=sigma(P). After the same physical correction P on S, the unnormalized output is

    (KD)^(-1/2) sum_s |Omega_s>_(RS)|chi_(s,s+delta)>_E.  (4)

Equivalently, define

    V_delta |s,t>=1[t=s+delta]|s>.

The corrected instrument restricted to the link target spaces is

    K_P^corrected (W tensor W)
       =(KD)^(-1/2) W V_(sigma(P)).                     (5)

Here V_delta†V_delta is the projector onto the specified relative-gauge sector; V_delta V_delta†=I. There are KD masks for every delta, so summing (5) over P gives a trace-preserving channel on both input gauge factors. It measures their difference and retains one common gauge factor.

For arbitrary density matrix tau on the two gauge factors,

    Pr(P)=Tr[V_delta†V_delta tau]/(KD).                  (6)

Conditional on delta, masks are uniform among the KD compatible Pauli labels, regardless of common-syndrome coherence or the bath. Equation (4) shows that common-syndrome coherences are not inadvertently measured by transmitting the full physical mask. This is a common-span statement, not merely a calculation on a classical mixture of sectors.

After any matched mathematical signed-sector decoding of the output, the logical factor is the same pure k-Bell state and all input-gauge/record/bath dependence remains elsewhere.

## 3. Incoming relative errors: no extensive amplification

Place the left link's relative Pauli E1 on A and the right link's relative Pauli E2 on S. This loses no generality: a Pauli on the other half is transferred to the relative half with a common-syndrome change, using the algebra audit.

Before normalization, the physical Bell contraction followed by P on S gives

    vec(Pi_s E1^T P Pi_t E2^T P^T)/(K sqrt(D)).          (7)

It is nonzero only if

    sigma(P)=s+t+sigma(E1).                             (8)

Paulis commute up to signs. On the compatible sector, (7) therefore equals

    phase(P,E1,E2) · (I tensor E2 E1)Omega_s/sqrt(KD).   (9)

The phase is irrelevant for a single branch and belongs to the gauge/record/bath amplitude in a coherent sum. The output relative binary Pauli label is e1+e2. Hence

    |e_out|_R <= |e1|_R+|e2|_R.                         (10)

The reduction in (10) is modulo the ordinary single-block stabilizer group. Input stabilizer factors contribute only signed-sector phases, including when the input gauge labels are coherent. Choose each input residual bound small enough that their sum plus the charged terminal-fault allowance remains within the subsequent buffer's correction radius and below d/2.

Equation (9) is precisely the desired encoded-to-encoded use interface. It does not require a zero-syndrome link or a global syndrome decoder at the middle station.

## 4. Noisy measurement, transmission, and correction

The ideal quantum terminal circuit has fixed depth and bounded column spread. Expand every local CPTP fault in a Pauli basis while retaining its bath coefficients. Such terms can be moved to:

- a bounded-support input/output relative Pauli;
- a bounded number of flipped physical Bell-outcome bits;
- faulty local Pauli-correction locations.

A reported mask differing from the ideal P in one bit changes the applied correction by a single-column Pauli, up to phase. It does not produce a dense correction error merely because P itself is dense. If K_tail counts actual faulty locations in the complete fixed-duration use stage, there is a common coefficient-independent support envelope with

    |e_out|_R <= |e1|_R+|e2|_R+c_tail K_tail.            (11)

Classical send/correction registers can use the measured CPTP gates of BILATERAL_SCHEDULED_CPTP_ADDENDUM.md. Their temporary storage, idle DATA noise, physical propagation time, and failures must all be counted. Full-mask communication needs 2n classical bits and adequate parallel bandwidth; it is not compressed to 2k logical bits for free.

The terminal circuit is an entire D0-style bounded-spread use stage. It must not overlap an incompatible relative-GPT controller that interprets the large uncorrected P byproduct as an ordinary small error. A controlled pause with charged fixed duration suffices for the scheduled architecture. An asynchronous autonomous handoff would require its own actual message/lock/mode-change construction.

If every input safe record satisfies its residual bound and the full terminal record satisfies K_tail<=f_tail n, (11) places ALL coherent output histories in one common small-relative-error Bell span. Exact final relative recovery then gives the factorization proved in the scheduled addendum. Union-bound the positive bad-input and bad-tail instruments unconditionally; do not restart a noise theorem conditioned on a rare Bell outcome.

## 5. Latency boundary and ordinary comparison

The byproduct P has typical weight proportional to n. Before P is applied, the new R,S resource can be far outside the ordinary relative-error basin. Arbitrary waiting for its mask is therefore NOT covered. A bounded physical delay with suppressed/accounted incompatible correction dynamics and a small total fault tail is sufficient. Alternatively one would need a separately proved large-known-frame-aware controller; that has not been assumed.

This is standard physical entanglement swapping with a CSS signed-sector identity. Its useful consequence here is operational: the maintained common-syndrome Bell resources can actually be routed to encoded recipients without a global preparation frame or a perfect global decoder. Ordinary active Bell buffers with equal access can use the same interface. No bare-output claim, magic-state supply, or universal quantum computation theorem follows merely from this bridge.
