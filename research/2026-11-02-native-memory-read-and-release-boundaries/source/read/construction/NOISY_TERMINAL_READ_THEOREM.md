# Constructive terminal READ: witness dilution and CSS teleportation

2026-11-02. A new conditional terminal-interface derivation, using the supplied actual decoder and native Gibbs witness premises. This is NOT a noisy WRITE theorem. The physical service-noise model and all remaining compiler/implementation gates are explicit below.

## Result first

The actual thermal witness argument extends to fixed-rate local-stochastic TERMINAL fault supports without inventing a new joint thermal/fault witness complex. Delete the entire valid thermal witness even when service faults have filled some of its missing defects. Its energy penalty loses only a bounded amount per fault-touching check. An exponential-moment bound absorbs those losses into a reduced witness tension.

This proves a threshold for the entire operator algebra on sampled fault supports, not only independent Pauli values. Combined with a transversal CSS Bell measurement against an encoded Bell resource, it yields reference-safe quantum extraction to a conventional actively protected output. Actual stored-state syndrome coherences are allowed.

The theorem remains conditional on an explicitly admitted local-stochastic service model, a sufficiently reliable Bell resource, and a reliable classical processor. The storage theorem alone supplies none of those physical access guarantees.

## 1. Inherited exact premises

Work in the dressed frame after the fixed-depth native U†. Let μ(s) be the ACTUAL Gibbs syndrome distribution, with clocks and finite environment traced only for this classical distribution. From the supplied native perturbation theorem, for any valid syndrome translation τ,

 |log[W(s)/W(s+τ)] + β[F0(s)-F0(s+τ)]| ≤ Λ |τ| + 4r_n,

where

 F0(s)=c-J0 sum_g s_g+R0(s),
 sup_g sum_(A contains g)|r_A|≤ε0 J0.

Use defect bits x_g=(1-s_g)/2. The source's unstable set B_X∪B_Z admits valid, occupied witnesses τ and the previously earned witness entropy bound at tension B. Let

    B = 2βJ0(1-ε0)-Λ,
    h = 4βJ0.

All quantities are fixed in size apart from the small remainder r_n. X/Z statistical independence is not assumed.

The full-space decoded logical observables Q_X,Q_Y,Q_Z form an exact qubit algebra. The actual decoder's stability lemma says that an elementary Pauli at a stable intermediate syndrome does not change that decoded logical algebra. Consequently, if every syndrome translate obtained by Paulis on a set S remains stable, the entire operator algebra supported on S preserves the decoded logical algebra on that initial syndrome subspace.

## 2. Explicit admitted service model

A finite-depth local terminal front end consists of U†, matched-pair transversal Bell gates and destructive local measurements. After transporting faults through its ideal finite-depth lightcones, each possible fault location ℓ can affect at most b syndrome checks. At most a|τ| locations can affect any given check set τ. Constants a,b include both CSS sectors, clock conjugation, ancillary carrier errors and circuit depth.

A classical fault support F is sampled independently of the stored input/reference/environment state. Its distribution may have spatial correlations, but satisfies

    Pr(A⊆F) ≤ q^|A|

for every location set A. Conditional on F, arbitrary coherent/CPTP operations on the corresponding bounded lightcones are permitted; their values need not be Pauli or independent. This is a precise local-stochastic SUPPORT assumption, not an assertion about arbitrary Hamiltonian noise.

Faults in destructive measurement outcomes are represented by premeasurement Pauli flips. A Bell-resource A block may carry additional local-stochastic released faults, included as locations. A separate ε_Bell accounts for its residual logical/resource error outside this model, in FULL JOINT trace norm at the decoded-logical output interface, including the stored input, its reference and its bath, as specified below; a marginal resource-quality claim is not substituted for this joint interface. The output B block remains actively fault-tolerant, rather than being noisily decoded to a bare qubit.

The fault sampler's independence is substantive. A state-dependent adversarial fault instrument is not justified merely by a bound on its unconditional location probabilities. One can replace independence by a suitable conditional operator domination assumption, but that is another hypothesis.

## 3. Partial occupancy surgery: the key inequality

For a fixed fault support F let N(F) be the union of syndrome checks touched by its possible effective data errors. If some Pauli supported on the fault lightcones can make a witness τ fully occupied, then initially

    τ \ N(F) ⊆ x.

This is a necessary condition regardless of the Pauli values. Define A_(τ,F) to be this partial-occupancy event. For every x in A_(τ,F), at most m=|τ∩N(F)| elements of τ are unoccupied.

Translate by the FULL τ, not by its occupied subset. This translation is valid and injective because the original witness τ is a valid coboundary. The reference energy difference is at least

    F0(x)-F0(x+τ) ≥ 2J0[(1-ε0)|τ|-2m].

The actual Gibbs ratio and injectivity therefore imply, also conditional on the other CSS syndrome,

    μ(A_(τ,F)) ≤ exp[-B|τ| + h |τ∩N(F)| + 4r_n].       (1)

No assumption that τ\N(F) is itself a valid syndrome is needed. That is the principal simplification.

Let I_τ contain all fault locations whose lightcones touch τ. Since |I_τ|≤a|τ| and each location touches at most b checks,

 exp[h |τ∩N(F)|] ≤ product_(ℓ∈I_τ) [1+(exp(hb)-1)1_(ℓ∈F)].

Expand this product and use the local-stochastic support bound term by term. Then

 E_F exp[h |τ∩N(F)|] ≤ [1+q(exp(hb)-1)]^(a|τ|).

Define the reduced tension

    B_q = B - a log[1+q(exp(hb)-1)].                    (2)

Averaging (1) yields

    E_F μ(A_(τ,F)) ≤ exp(4r_n) exp[-B_q |τ|].          (3)

This is valid at every fixed q for which B_q retains the original strict witness-counting margin. Such q>0 exists. This exponential-moment bound is valid but unnecessarily pessimistic at low temperature. The coverage-splitting improvement below removes its artificial exp(-O(βJ0)) read-noise penalty; inherited combinatorial/geometric constants can still be extreme.

## 4. Entire-support logical correctness

For each F, let Bad_F consist of initial syndromes for which ANY Pauli on the effective data support can reach B_X∪B_Z. Every such syndrome is in A_(τ,F) for some original source witness τ. Apply (3), then the actual source's unchanged witness entropy sum.

For example, with the original source notation,

 W(B_q)=(1+exp(-B_q/4))^(M_ell)-1,
 z(B_q)=2(Delta+1)^2 W(B_q)^[1/(1+Delta_level^4)].

If z(B_q)<1 with strict fixed slack, the source sum and the dual-sector sum give

    p_read(n):=E_F μ(Bad_F) ≤ poly(n) exp[-c_q n^η].   (4)

The full-trace alternative instead gives the conservative criterion K_trace exp(-B_q/A_trace)<1. Neither proof requires X/Z thermal independence.

No union over exponentially many Pauli values is required: partial occupancy already covers them all. No additional union over Pauli prefixes is required: every prefix is itself supported on the same fault support and was included in Bad_F.

Let G_F be the syndrome projector complementary to Bad_F, tensored with all clock/environment spaces. For any operator E on the fault data support (with arbitrary coefficients acting on touched clock/bath spaces),

    [Q_mu,E] G_F = 0.

This follows by decomposing E into data Paulis and using the elementary stability identity at every prefix. It is an algebraic statement on the whole good subspace, not a diagonal-state argument.

For a CPTP channel Φ_F with such Kraus operators, Φ_F†(Q_mu)-Q_mu annihilates G_F on the right. It is Hermitian, so it also annihilates G_F on the left, and has norm at most 2. Thus reference correlations and good/bad coherences do not force a square-root bound: its expectation against any norm-one reference observable is at most 2 Tr[(I-G_F)Γ].

## 5. Exact ideal quantum extraction

Let V:C²→H_A be the SAME CSS code's ground-space encoding, and let W encode a qubit into an actively protected output B. Prepare, independently of the stored input/reference/environment,

    |Φ_code〉_(A,B) = (V⊗W)|Φ_2〉.

Place each A data carrier next to its matching source data carrier; this requires a constant-factor density increase and charged resource preparation/routing, not nonlocal free gates. Perform all physical Bell measurements transversally between source S and A, after U†. These measure pairwise XX and ZZ in constant quantum depth using local gates and noisy measurements admitted above.

For a physical Bell outcome labelled by a Pauli P, the uncorrected Kraus operator on source S is proportional to

    W V† P

(up to transpose/conjugation conventions fixed by the Bell basis). Decompose the Pauli coset using the ACTUAL decoder's syndrome representative E_s and logical Pauli. The physical outcome identifies s because A is in the code ground space; the classical decoder identifies the corresponding logical Pauli frame. Correct that frame on B, or track it reliably.

For every syndrome s, V† P E_s V is either zero or the identified logical Pauli. Consequently the full corrected instrument implements exactly

    σ_S → W Tr_gauge[D σ_S D†] W†.

It therefore works on arbitrary syndrome coherences and arbitrary reference entanglement; it is not merely a measurement of classical logical X or Z. Clock/environment entanglement is retained as an external reference for this identity and then appropriately traced.

A physical Pauli error on A transposes through the physical Bell bra to the matching source carrier. Errors on S and A therefore combine into an effective Pauli on their union of matched supports. More generally, expand arbitrary support-local Kraus operators in Paulis; each resulting corrected teleportation Kraus operator intertwines Q_mu with the output logical Pauli on G_F. Linearity gives the same result for coherent errors, including joint S–A faults. This is why the entire-support version of (4), rather than a probability claim for particular Pauli values, was needed.

## 6. Stored-state domination, generic coherences and final error

Assume the stored physical marginal Γ_SE obeys the all-effect bound

    Tr(A Γ_SE) ≤ K Tr(A Ω_SE) + δ_st

for every 0≤A≤I. The supplied ideal overwrite/storage consumer gives such a bound with a constant K (in particular K=2) and the actual twirl discrepancy, with its exact constant convention retained. It is important that this is an all-effect bound, not only one particular bad-set estimate.

Because the fault sampler is independent, average its bad projectors FIRST. Their average is one effect. Equation (4) then gives

    E_F Tr[(I-G_F)Γ_SE] ≤ K p_read(n)+δ_st.

The δ_st term is paid once, not once per witness or fault location. The intertwining/adjoint argument in Section 4 applies to the corrected teleportation channel as well. Expanding output operators in the three Pauli matrices gives the conservative reference-safe trace-norm bound

    ||(D_B ∘ READ_physical)(Γ_RSE)-ideal_decoded_logical(Γ_RSE)||₁
      ≤ 6[K p_read(n)+δ_st] + ε_Bell + 2p_class + ε_out. (5)

Here D_B is a specified mathematical recovery/decoder of the FT output, not a physical bare-qubit release operation. ε_Bell is the full-joint resource discrepancy in this logical-output interface specified below; p_class is the classical computation/frame-tracking failure probability; and ε_out is a reference-safe trace-norm/diamond bound for DECODED LOGICAL maintenance of the encoded output through the charged classical processing interval. Thus ε_class=2p_class if that shorthand is used elsewhere. A failure-probability bound p contributes at most 2p in trace norm.

Add the already-earned storage logical channel error to (5) to compare the delivered quantum output with the original entangled input. No later passive hold of the noisy released resource is invoked.

## 7. Resource and implementation gates that must remain visible

- Bell-resource preparation is a real task: a conventional FT computer can supply the same-code encoded A half and an active B half only under its own admitted noisy universal-gate/reset model, with its full circuit, geometry, ancilla and runtime overhead. The final A release must deliver the stated local-stochastic support model plus ε_Bell. This is an interface specification, not a free perfect resource.
- Classical decoder computation and Pauli-frame tracking require a reliable classical implementation under a stated classical noise model. Its failure probability is p_class; the potentially long computation is performed while B is actively maintained, and that storage cost enters ε_out/resources. Merely calling the mathematical decoder is not noisy classical computation.
- The source-side quantum access depth is fixed. If the circuit depth grows with size, a,b grow and the fixed-q threshold may disappear. Bell resource creation can be long because it is prepared and protected separately; its errors must already meet the specified release interface.
- Actual always-on Hamiltonian exposure during access must be compensated, included exactly in the ideal access circuit, or proved to satisfy the service fault model. A generic coherent residual Hamiltonian is NOT automatically independent sampled stochastic support noise. The naive Duhamel global bound is O(n v τ_access), which is insufficient at fixed speed/strength. No equilibrium theorem removes this issue.
- Arbitrary native qudit faults are allowed only after their finite-depth lightcones are included in b and their support sampler meets the model. No perfect clock readout is needed; clocks are not required as extracted logical output.
- The same control strengths, switches, reset quality, classical electronics and output FT apparatus must be available to the active-memory comparator.

## Scientific status

Equations (1)–(5) provide a substantive conditional terminal READ gate from the actual supplied witness ratio and decoder stability premises. They handle generic equilibrium coherences and deliver an entangled logical output, rather than only a classical read bit. They do not prove that the existing native device has the requisite access controls or service noise model, nor do they manufacture a cheap Bell resource.

Most importantly, this terminal argument does not apply to WRITE followed by long passive storage: immediate logical correctability of service faults does not restore the necessary stationary syndrome–bath preparation. The noisy loader/write gate remains open.

## Appendix: normalized Bell channel and noisy intertwining

Let n_d be the number of DATA qubits (excluding clocks), d=2^(n_d), and choose the real CSS ground encoding V:C²→C^d. For a non-real encoding the resource's A half would instead use V*; the actual CSS choice permits V*=V. Let the syndrome representatives selected by the ACTUAL decoder be E_s, and put V_s=E_s V. Then

    V_s† V_t=δ_st I_2,       sum_s V_s V_s†=I_d,
    D|ψ〉=sum_s (V_s†|ψ〉)_L⊗|s〉_G.

There are d/2 valid independent stabilizer syndromes. Redundant measured checks merely encode these same sectors with constraints.

Use phase-free n_d-qubit Pauli representatives P to define the physical Bell basis

    |Φ_P〉_(S,A)=(P†⊗I)|Φ_d〉,
    |Φ_d〉=d^(-1/2) sum_i |i〉|i〉.

The encoded resource is 2^(-1/2) sum_(l=0,1) V|l〉_A W|l〉_B. Direct contraction gives the UNCORRECTED Kraus map

    K_P = (2d)^(-1/2) W V† P.

For each P there is exactly one syndrome s=s(P) such that V†P V_s is nonzero; it is a logical Pauli L_P up to phase. Therefore V†P=L_P V_s†. The decoder's output determines L_P. Apply/track its inverse on B. The corrected Kraus is

    Ktilde_P=(2d)^(-1/2) W V_s†

up to an irrelevant phase. Each syndrome s has exactly 2d Pauli outcomes: four logical classes times d/2 stabilizers. Hence

    sum_P Ktilde_P σ Ktilde_P†
       =sum_s W V_s† σ V_s W†
       =W Tr_G[DσD†] W†.

Completeness follows immediately, including for coherent superpositions of different syndrome sectors. The syndrome measurement destroys precisely the gauge coherence that the ideal partial trace discards; it does not destroy the logical/reference coherence. The outcome's syndrome can be computed directly from its commutation signs with stabilizer generators. Obtaining L_P then uses the actual decoder representatives and logical coset calculation.

For Pauli errors E on S and F on A, the Bell identity gives

    <Φ_P|(E⊗F) = <Φ_d|(F^T P E⊗I).

Since Paulis commute or anticommute, write F^T P E=P E_P with E_P=P†F^T P E. Its support lies in supp(E)∪supp(F), independently of the outcome-dependent sign. The same observed-P correction therefore yields a Kraus operator Ktilde_P E_P, NOT a correction based on an unobserved shifted outcome. This distinction preserves the actual decoder frame.

Expand any joint support-local fault Kraus operator on S,A into Pauli tensors, allowing arbitrary clock/environment operator coefficients. After Bell contraction the resulting Kraus operator is Ktilde_P M_(P,a), where each M_(P,a) belongs to the entire data-support algebra already protected on G_F. The operator M may depend on P and need not separately define a trace-preserving map. The sum over the full physical instrument's outcomes and environmental Kraus labels is trace preserving.

The ideal corrected Kraus satisfy Ktilde_P Q_mu = (Wσ_muW†)Ktilde_P globally on the code-output range. Since [M_(P,a),Q_mu]G_F=0, each noisy corrected Kraus J_(P,a) satisfies

    J_(P,a) Q_mu G_F = (Wσ_muW†) J_(P,a) G_F.

Because [Q_mu,G_F]=0 and sum J†J=I, this implies

    [READ_F†(σ_mu^out)-Q_mu]G_F=0.

Its Hermiticity gives left annihilation as well. This is the precise two-sided-bad-subspace argument underlying the linear bad-weight bound and its reference-safe use in (5). It does not assume that the stored state is syndrome diagonal, that clock faults are Clifford/Pauli mixtures, or that outcome-dependent effective errors form independent stochastic channels.

## Resource-lighter corollary: a destructive classical X or Z READ

If only a chosen logical Pauli measurement is required, no Bell resource is needed. For the actual separate-sector CSS correction convention, after U† measure every data qubit in Z (respectively X). Products of outcomes reveal the compatible stabilizer syndrome and the raw logical Z (respectively X) representative. The actual corresponding CSS decoder computes the Pauli-frame sign. This implements the exact full-space Q_Z (respectively Q_X) measurement, with its effect on an external reference, rather than assuming that the input lies in the code ground space.

Apply the same support-wise stability and fault-witness proof to measurement bit flips and arbitrary support-local premeasurement faults. It yields the corresponding noisy classical measurement guarantee, with ε_class and access-Hamiltonian assumptions retained, but without ε_Bell or a quantum output-maintenance resource.

This is a useful strictly cheaper terminal capability. It is not interchangeable with extraction of an unknown quantum state, and measuring both incompatible bases destructively does not provide quantum READ. The Bell construction above is the quantum-output gate.

## Secondary normalization check

`check_bell_normalization.py` exhaustively checks all 64 physical Pauli Bell outcomes for a three-data-qubit CSS fixture (not the actual recursive memory). It verifies the 2d outcomes per syndrome, complete channel Choi equality to the full-space decoder partial trace, trace preservation, and the observed-outcome A-fault transpose formula including Y phases. All reported residuals are zero in double precision for this exact fixture; see `check_bell_normalization.txt`. This checks normalization and conventions only, not the actual-code witness estimates or a physical fault threshold.

For an explicit threshold, choose any fixed B_req exceeding the source witness-counting threshold and below B. Then

    0 ≤ q < [exp((B-B_req)/a)-1]/[exp(hb)-1]

ensures B_q>B_req (also restrict q≤1). This expression makes the possibly severe operating constants visible; it is not a practical noise-tolerance estimate.


## Required Bell-resource independence and joint error specification

The exact contraction proof starts with Γ_RSE⊗|Φ_code〉〈Φ_code|_AB. The Bell resource is supplied independently of the stored input, its inaccessible reference, and its storage environment. The reference service model may then apply the sampled A-release faults and the terminal circuit faults; those are already included in the state-independent local-stochastic fault-support model. Conditional fault operations may correlate the systems, but the ideal initial resource and the classical support sampler cannot secretly encode information about Γ.

The actual resource/preparation interface must differ from this reference model by at most ε_Bell in trace norm on the FULL joint state at the logical-B interface, including R,S,E, physical A, decoded logical B and any retained classical fault labels relevant to the model, or satisfy a corresponding diamond-norm preparation-interface guarantee uniformly in the stored state. A stronger physical-B joint bound is sufficient but not required; see the explicit output-correctness section below. Its error is then charged once by contractivity. A statement only about an isolated resource marginal is not used as this joint guarantee; any proposed conversion from a measured marginal fidelity to a decoupling guarantee requires its own explicit bound and error conversion. Likewise, if resource construction touches the storage bath, its induced disturbance must be included in this joint ε_Bell or in the admitted service map, not ignored.

With these conventions, the complete delivered logical trace-norm error is at most

    ε_storage + 6[K p_read(n)+δ_st] + ε_Bell + 2p_class + ε_out.

A bare final physical output qubit would introduce its own terminal fault floor. The stated quantum result instead returns an FT-encoded output with its maintenance channel charged by ε_out.


## Sharper coverage-splitting bound: no artificial cold-temperature noise penalty

The root supplied this improvement to the original exponential-moment estimate. Let m=|τ| and C_F=|τ∩N(F)|. The partial-occupancy inequality also gives

    μ(A_(τ,F)) ≤ min{1, exp[-Bm+h C_F+4r_n]}.

Fix a coverage fraction θ>0. Split fault patterns into C_F≤θm and C_F>θm. The first class contributes at most exp[-(B-hθ)m+4r_n]. For the second, at least k=floor(θm/b)+1 relevant locations must be faulty, since one location covers at most b checks. There are at most a m relevant locations. If k exceeds their number the probability is zero; otherwise the local-stochastic union bound gives

    Pr(C_F>θm) ≤ binom(|I_τ|,k) q^k
                ≤ (e a m q/k)^k
                ≤ (e a b q/θ)^k
                ≤ (e a b q/θ)^(θm/b),

where the last step assumes eabq/θ<1. This handles the integer threshold without an omitted ceiling prefactor. Consequently

    E_F μ(A_(τ,F))
      ≤ exp(4r_n) exp[-B_thermal m] + exp[-B_fault m],

    B_thermal = B-hθ,
    B_fault = (θ/b) log[θ/(eabq)].                    (6)

Apply the original witness entropy sum separately to these two exponentials. In particular, choose any B_req strictly above BOTH CSS source witness-counting thresholds, and impose

    0<θ<(B-B_req)/h,
    q < θ/(eab) exp[-b B_req/θ].                      (7)

Then both witness sums have fixed slack, and (4) follows with a new constant c_q>0. The full-trace alternative may instead take B_req>A_trace log K_trace with slack. There is no unsupported claim that witnesses of top weight m are counted by a simple μ^m; the already-earned actual witness sum is applied twice.

The noise threshold in (7) has no explicit exp(-βJ0) penalty. If θ can be kept fixed while increasing β within a domain where the inherited actual Gibbs ratio and witness premises remain valid, colder temperature improves B_thermal rather than forcing exponentially cleaner service gates. For a compact admitted temperature interval, choose θ below the infimum of (B-B_req)/h on that interval. This does NOT extend the native perturbation theorem uniformly to β→∞: its own allowed perturbation strength and ratio hypotheses must continue to hold.

The stronger bound replaces the conservative B_q threshold whenever advantageous; all entire-support, Bell-extraction and reference-safe arguments are unchanged. Read tolerances can still be extremely small because a,b,B_req and the code constants are severe, but an exponential penalty in β introduced solely by the earlier moment bound is not a physical requirement.


## Output correctness is decoded-logical, not physical-codeword trace distance

Equation (5) is a statement AFTER the specified mathematical output recovery/decoder D_B. The physical deliverable remains an encoded FT block. Correctable physical errors on that block can have large trace distance from W|ψ〉; ordinary FT does not establish physical trace-distance closeness to the ideal codeword, and none is claimed here. D_B is used to define the correctness of that encoded output, not proposed as an ideal physical final operation.

The Bell-resource joint-error requirement is interpreted consistently in this logical-output interface. Either one supplies the stronger physical joint bound against the ideal W-encoded Bell state (a sufficient but unnecessary condition), or one certifies the full joint A–logical-B resource after D_B, including R,S,E and fault labels, with an error ε_Bell. In the latter formulation B's correctable physical errors are not incorrectly charged as logical errors. All terminal S–A operations commute with an abstract decoder on B, so the normalized Bell proof may be applied with W=I on the abstract logical-B subsystem.

Active maintenance of B is separately charged by ε_out as a reference-safe DECODED-LOGICAL channel guarantee, with a compatible recovery/interface for the admitted resource state. It must preserve entanglement with A and all other references. The resource/output FT interface must jointly establish this composition, not merely supply two unrelated marginal fidelities. Logical corrections may remain a reliable classical Pauli frame until after mathematical decoding; no uncharged bare physical B correction or release is assumed.

Equivalently, a single reference-safe FT resource-and-maintenance interface can provide the required independent Bell resource at the abstract logical-B port and physical A port, with total error ε_Bell+ε_out. This is often the cleanest service specification. The input/Bell-frame classical failure remains separately bounded by 2p_class.


## Independent review status

The fresh independent audit in `FRESH_NOISY_READ_AUDIT.md` passes the frozen theorem with SHA256 `9258892544090c560792b8aea3f19c8cd7963e6df814e1690c612fb5fd8487ba`, preserved as `NOISY_TERMINAL_READ_THEOREM_REVIEWED_92588925.md`. The current file differs only by the auditor-requested notation correction (Section 7 failure probability is p_class, while its trace-norm charge is 2p_class) and this review-status paragraph. Audit receipt SHA256: `0b90a7a4e5fcf4cfb037539a8e60bf30a5809fd1094e43981e87b07eed0ee79d`.

The pass is conditional on the declared service-noise and FT resource/output interfaces. It is not a claim that Delivery 83 already supplies those access controls, nor a noisy WRITE or usable complete memory theorem.
