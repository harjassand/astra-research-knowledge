# Measured endpoints replace private stabilizer wrappers in the scheduled pulse model

Date: 2026-10-15. Verdict: **PASS, under the explicit instrument, locality, and implementation assumptions below.**

This is a conditional mathematical bridge, not a hardware qualification or a new operation family. It removes physical initial/final randomizer gates and any need to observe the internal dephasing trajectory. It retains exact trusted endpoint syndrome measurements, exact correction first, fixed clean reservations, independent ideal Markov stabilizer dephasers, and all other scheduled-memory premises.

The equality is to a hypothetical tracked-frame model **with the same actual endpoint measurements**. It is not an equality to the original unmeasured wrapper channel. Adding these measurements generally changes that channel. Their effect on the support proof is benign for a different reason: stabilizer projections are scalar or zero on each encoded Pauli-history sector.

A simpler deterministic-cell variant is proved separately in DETERMINISTIC_MEASUREMENT_CELL_COROLLARY.md. It gives actual joint-parent budget p_i=min{1,sum_l a_(i,l)^2}, hence p_i<=J_i^2 tau_i^2/M_i for equal cells, without a continuous dephaser or a generator-count factor. Its exact intermediate measurements must still be priced in the total reservation.

## 1. Exact actual model and records

Let the memory stabilizer code have stabilizer group S_code, with no minus identity. The persistent bath B is arbitrary and finite-dimensional; arbitrary initial memory-bath correlations and an untouched reference are allowed in the effect theorem.

For selected geometrically clean completed pulse i:

1. G_i is a finite subgroup of S_code with commuting Hermitian Pauli generators S_(i,a), a=1,...,m_i. Independent generators are convenient; redundant independent seed bits still push forward to a uniform group element, with a potentially looser m_i factor.
2. At the prescribed beginning, an exact projective measurement of G_i records trusted syndrome s_i. Write its projectors P_(i,s), and lambda_s(g) for the eigenvalue of g in sector s.
3. The checks resolve the intended correction decision j_i(s). The exact bath-independent correction Q_i(s)=Q_(j_i(s)) is completed first. Q_i(s) is a Pauli, and

       Q_i(s) P_(i,s) = P_(i,r_i(s)) Q_i(s) P_(i,s),
       r_i(s) = s xor syndrome_Gi(Q_i(s)).

   This can instead be implemented by measuring G_i immediately after the already exact correction; then that trusted observed sector is r_i directly. A possibly corrupted internal correction decision is never the expected-syndrome comparator.
4. During a fixed weak-noise interval I_i of length tau_i, the Hamiltonian term V_i(t) is supported on the whole declared error patch A_i tensor B, with ||V_i(t)|| <= J_i. Its only additional local noise is the ideal Markov generator

       sum_a gamma_(i,a) [Ad(S_(i,a)) - I].

   The different dephasers admit independent Poisson-jump streams of the specified rates, independent of the input, geometry, and all other chosen streams. These trajectories are an unobserved unraveling, not available controller records.
5. An exact actual measurement of G_i occurs at completion, with trusted retained outcome t_i. The actual bad-parent flag is

       b_i = 1[t_i != r_i(s_i)].

The pre/post outcomes are genuine classical instrument records. They may drive later fixed classical control, but may not be coherently erased and recombined. They, or an equivalent protected comparison flag, survive long enough to define the claimed event. No normalized conditioning on a particular generated record is used in the probability theorem.

Every data/check/measurement-ancilla/controller/reset resource, and the full physical support of every generator, belongs to the declared reservation. Concurrent selected clean reservations have disjoint full memory/ancilla resources throughout their intervals; sharing B is allowed. Their geometry and timing are fixed by exogenous primitives. Every other memory operation intersecting such a reservation must be part of its stipulated implementation or makes it dirty/bad. Later reuse after actual completion and fresh reset is allowed.

## 2. Single-branch identity

Fix a finite Poisson path eta_i(t) in G_i, initially identity, with terminal value eta_T. Let U_eta be the physical weak-interval propagator including its actual stabilizer jumps. For one record the actual branch is

    A_(t,s,eta) = P_t U_eta Q(s) P_s.

Purely for the proof, introduce a uniform g in G_i, insert g immediately after the completed correction, and insert (g eta_T)^dagger immediately before the actual postmeasurement. The hypothetical branch is

    B_(t,s,g,eta) = P_t (g eta_T)^dagger U_eta g Q(s) P_s.

Since g Q(s)P_s = lambda_r(g) Q(s)P_s and P_t(g eta_T)^dagger = conjugate(lambda_t(g eta_T)) P_t,

    B_(t,s,g,eta)
      = lambda_r(g) conjugate(lambda_t(g))
        conjugate(lambda_t(eta_T)) A_(t,s,eta).          (1)

All scalar factors have modulus one. With real Pauli characters the conjugates can be omitted. Thus each outcome-resolved CP map is identical, for every fixed path and every input, before any future operation or final decoder. The physical input need not begin in a fixed syndrome sector: the actual premeasurement provides the branch projection and its outcomes are summed.

Equivalently, write U_eta=eta_T W_eta in the toggling frame. Then

    A_(t,s,eta) = lambda_t(eta_T) P_t W_eta Q(s)P_s,
    B_(t,s,g,eta) = P_t g^dagger W_eta g Q(s)P_s.

Neither g nor eta_T needs to be physically known or corrected in the actual model.

## 3. Full chronology, shared bath, overlap, and reuse

Fix the full genuine classical record alpha and unobserved dilation index beta, but do not normalize that branch. Apply (1) at the actual insertion/removal locations for every selected pulse. Each inserted g acts immediately next to its trusted entering-sector map, and each final inverse acts immediately next to its actual postprojector. They strip off as scalars without commuting any bath operator or serializing any joint pulse channel.

The entire actual record Kraus operator A_(eta,alpha,beta) and hypothetical tracked operator satisfy

    B_(g,eta,alpha,beta)
      = omega_(eta,alpha) product_i chi_(Delta_i(alpha))(g_i)
        A_(eta,alpha,beta),                            (2)

where |omega|=1 and Delta_i(alpha)=r_i(s_i) xor t_i. This remains true for crossing pulse intervals, common noncommuting bath operators, later reuse of the same patch, and later control on protected classical records. The proof never replaces a completed branch merely by a final-decoder-equivalent channel; it proves its actual outcome-resolved CP map is equal at its endpoint.

The separate role of cleanliness is to derive a useful toggling-frame Hamiltonian for the hypothetical construction. At time t multiply the active frames g_i eta_i(t). Disjoint full reservations ensure the frame for i commutes with every other memory operation while active; bath-only terms also commute. Consequently the exact toggled Hamiltonian is

    H_(g,eta)(t)=H_0(t)+sum_i Ad[(g_i eta_i(t))^dagger](V_i(t)),   (3)

with only the displayed private dependence. Endpoint measurements and exact correction maps are fixed seed-independent interventions. Their coherent common-dilation implementations may be used for norm bounds; the final outcomes are still resolved as genuine classical records. Selected windows and generator definitions cannot depend on earlier selected private paths or seeds. Fixed outcome-controlled operators with a common dilation are allowed; separately recalibrated branch Hamiltonians are not a substitute.

If two selected noisy regions A_i are disjoint but their full check/dephaser supports overlap, (3) has not been justified. They must be classed as conflicting or separately proved to satisfy the interface. Reuse is harmless after completion because the hypothetical cumulative frame has already been removed and the actual postmeasurement has already occurred.

## 4. Formal CP instrument and exact Fourier transfer

For the actual experiment define

    M_alpha(X) = E_eta sum_beta A_(eta,alpha,beta) X A_(eta,alpha,beta)^dagger.

The maps M_alpha are CP and sum to a trace-preserving map. An explicit retained classical register gives sum_alpha |alpha><alpha| tensor M_alpha(X). If the finite-horizon path environment is continuous, this integral itself defines the channel; one may compress its final CP instrument to a finite Stinespring representation. No finite-dimensional physical Poisson reservoir is asserted, only a finite persistent bath.

Fourier-transform the purely mathematical uniform g tuple:

    K_(chi,eta,alpha,beta)
      = E_g conjugate(chi(g)) B_(g,eta,alpha,beta).

Equation (2) gives the exact delta identity

    K_(chi,eta,alpha,beta)
      = 1[chi=Delta(alpha)] omega_(eta,alpha)
        A_(eta,alpha,beta).                            (4)

Thus the mathematical Fourier character is simply a duplicate of the actual trusted syndrome-change record. It is neither a hidden physical randomizer record nor a fictitious online measurement outcome.

For any selected subset R,

    F_R := sum_(alpha: b_i=1 for all i in R) M_alpha^*(I)
         = E_eta sum_(chi: chi_i!=0 for all i in R)
                   sum_(alpha,beta) K^dagger K.        (5)

This is exact equality of positive full-input operators. There is no state-dependent success conditioning, Markov assumption on B, independent-bad-flag assertion, or chronological conditional-probability assertion.

## 5. Rate-sensitive effect bound

Apply the existing direct global-Fourier theorem to (3). For one chosen generator bit of pulse i, condition all other initial coordinates and other independent paths. Splitting its conjugated V_i into even and odd parts gives

    H_base(t) + (-1)^(f_i) xi_i(t) A_i^odd(t),
    ||A_i^odd(t)|| <= J_i,

where H_base is independent of the selected initial bit and its entire selected telegraph trajectory. The independent rate-gamma_(i,a) sign has correlation exp(-2 gamma_(i,a) |t-u|). A nonzero pulse character has an odd witness coordinate. A union over one witness per selected pulse yields

    F_R <= product_(i in R) p_i I,
    p_i = min{1, sum_a B(J_i,gamma_(i,a),tau_i)},        (6)

with

    B(J,gamma,tau) = ( exp(-gamma tau)
       [cosh(d tau)+(gamma/d)sinh(d tau)] - 1 )/2,
    d = sqrt(gamma^2+4J^2).

For equal rates, p_i=min{1,m_i B(J_i,gamma_i,tau_i)}. The gamma=0 continuation is sinh^2(J tau). For gamma>0,

    B <= [exp(2J^2 tau/gamma)-1]/2.

At small J, B=J^2[tau/gamma-(1-exp(-2gamma tau))/(2gamma^2)]+O(J^4), approaching the familiar J^2 tau/gamma scale for long intervals relative to 1/gamma.

For completeness, the direct proof uses initial-bit Fourier cancellation to force odd insertion counts on both ket and bra. Averaging the selected telegraph path produces a nonnegative alternating-pair correlation kernel. Ordered-time domains across species partition the Cartesian product and the scalar majorants factorize; no commutativity of bath operators is used. Actual seed-independent instruments are norm-one interventions in the common dilation.

The selected eta average in (5) is essential. Conditional on a rare no-jump trajectory one generally loses the finite-rate improvement. Geometry/clean selection can be conditioned; selected private internal paths and normalized generated syndrome outcomes cannot be conditioned away.

Separately, the deletion-null/action bound gives F_R <= product_i a_i^2 I, with a_i=integral ||V_i||. The same actual instrument satisfies both bounds. In the homogeneous setting one may take

    p_eff=min{1,a^2,m B(J,gamma,tau_noise)}.

For heterogeneous pulses, the immediate justified conclusion is the minimum of the two full subset products; this note does not infer a product of heterogeneous per-pulse minima without a hybrid proof.

The effect result itself requires no code-correctability or no-local-logical condition. Those enter next.

## 6. Precise full-footprint condition and completion support

Let Pauli(A_i) mean all memory Paulis supported in the ENTIRE pulse footprint A_i, including products of arbitrarily many local interaction insertions. The precise needed condition is

    Pauli(A_i) intersect Centralizer(G_i)
       subset phase times S_code.                    (7)

A common sufficient formulation splits (7) into:

- G_i detects the full code syndrome of every Pauli in A_i: a patch Pauli commuting with G_i commutes with all of S_code.
- A_i supports no nontrivial logical Pauli: a patch Pauli commuting with all code stabilizers is itself a stabilizer up to phase.

Checking each elementary Hamiltonian term separately is insufficient. The support of their full products matters. For a correction-first interval, the exact Pauli correction is already completed, no subsequent ideal non-Pauli gates propagate errors, and conjugation by stabilizer jumps does not enlarge A_i. Hence A_i can be the whole weak-pulse error footprint. If errors occur during a larger correction circuit or propagate outside A_i, the full propagated error footprint must replace A_i. For a general noisy gadget the union with the intended correction support can also be required; that extension is not supplied by this correction-first rate proof.

The full generator/measurement support D_i can be larger than A_i. It must be fully reserved, but it need not itself satisfy (7) when all extra operations there are exact code-stabilizer measurements and jumps. If those operations can fault arbitrarily, their entire fault footprint becomes part of the region that needs a new analysis.

For support, fix eta and an actual unnormalized record. In the toggling representation expand V_i into memory Paulis with chronological bath coefficients. Move only its memory factors to completion across disjoint other memory operations; never reorder the bath coefficients. The resulting net E_i is supported in A_i. The endpoint projections imply

    syndrome_Gi(E_i) = t_i xor r_i(s_i) = Delta_i.

Choose a representative P_(i,Delta_i) supported on A_i, with P_(i,0)=I. Equation (7) implies E_i differs from this representative by a code stabilizer and a phase. On every encoded Pauli orbit E V_code this stabilizer acts as a scalar independent of the logical vector. Absorb that scalar into the chronological bath/auxiliary coefficient.

Therefore every actual record Kraus operator has the same completion-support certificate as the private-frame construction: exact clean corrections at their justified starts; no support birth for b_i=0; a patch representative at each b_i=1 completion; and arbitrary geometrically bad/pending prefixes kept at their actual times. Exact extra pre/post stabilizer projections act as scalar or zero on these histories. They refine the channel but add no memory support.

A universal common decoder then works simultaneously on all coherent Pauli histories admitted by a good support record. Summing those actual record maps defines a genuine good CP subchannel, which after decoding is logical identity tensor an auxiliary/bath CP map. This is not a positive Pauli-mixture representation.

## 7. Conditional scheduled-memory composition and its actual cost

The old unmeasured physical channel must be replaced by the newly measured model, and its total reserved resources must be counted anew. Let theta be the NEW TOTAL gadget duration, including premeasurement, exact correction, weak interval, actual postmeasurement, all ancillary reset/comparison time, and any permitted tails. Let tau_noise be only the weak interval entering B.

If an exact instantaneous projector is used, its zero time is an explicit model idealization. If an exact finite measurement circuit is intended, its resources and timing must be supplied and reserved. Removing randomizer wrappers is not evidence that the detector is free or that theta equals the old duration. No uncharged coherent noise during detector operations is qualified by this bridge.

Recompute enlarged conflict/guard constants D,N,F,Q whenever the support changes. With the source's block length Delta and original start rate kappa, the same type of coarse budget, after those geometric checks, is

    d0_new = delta_ideal
       + 2DN kappa^2 theta(Delta+2theta)
       + F nu(Delta+2theta) + N kappa theta,
    mu_new = kappa N(Delta+2theta),
    q_new = (d0_new+p_eff mu_new)^(1/Q).

The terminal term remains local to the terminal strip. Pending measurements have not completed, so their parent is pending/bad; no missing postprojection may be inserted fictitiously at readout.

Under the unchanged named contour/common-decoder imports and the newly checked geometry, the same smallness condition d0_new+p_eff mu_new <= q_star^Q gives the source's recovered joint-input lifetime form. This is a new conditional composition using actual measured records, not an independent reproof of the contour machinery or an equivalence claim about the old physical channel.

## 8. Exact small failures when assumptions are dropped

### No actual completion postmeasurement

Take one qubit initially |0>, R=exp(-i pi X/4), then a Z-dephasing interval of duration d, and later apply R again. Do not measure Z at the first interval's completion. With untracked dephasing, final Pr(Z=-1)=(1+exp(-2gamma d))/2. With exact trajectory tracking and final jump inverse before the later R, the probability is 1. On a fixed odd-jump branch the actual final state is |0> while the tracked state is |1>, up to phase. An actual intermediate Z measurement makes the recordwise scalar argument valid and removes this discrepancy. Final-decoder invariance alone therefore cannot justify dropping the completion projection.

### Ignoring the full generator support

Take G=<Z_1 Z_2>, pulse error patch A={1}, and V_i=0. Premeasure G in |00>. An allegedly remote X_2 during the interval flips the postsyndrome with certainty. The claimed own-pulse budget would be B(0,gamma,tau)=0. It fails because the physical support of G includes qubit 2 and the reservation was not clean.

### Checking only elementary detectable errors

In the three-qubit repetition code G=<Z_1 Z_2,Z_2 Z_3>, the operator X_1 X_2 X_3 is logical and commutes with all dephasers and measurements. A pulse h X_1 X_2 X_3 produces a nontrivial logical rotation with every trusted mismatch flag zero. Even when individual terms are single-qubit errors, their products can generate this logical on the entire footprint. Condition (7) on the full patch excludes this case. Stabilizer dephasing cannot detect logical dynamics inside one syndrome sector.

### Wrong comparator

Predicting t using a noisy internal decision merely verifies that the possibly wrong chosen correction occurred. The trusted comparator must use the intended j(s), as in the explicit wrong-internal-branch example in ../deletion_null_detector_bridge/DETECTOR_SUBSET_AUDIT.md. Exact correction first makes that intended map available here.

## 9. Original shared-bath computation

check_shared_bath.py independently constructs the actual Lindblad instrument on two memory syndrome qubits A,C and one common bath qubit. An inert logical spectator could be adjoined without changing any calculation. It uses noncommuting pulse/bath Hamiltonians, pulses A:[0,0.9] and C:[0.2,1.15], then reuse A:[1.3,2]. The corrections reset A to syndrome 0, C to syndrome 1, and leave the reused A syndrome unchanged. Thus the expected label is not uniformly zero and the input syndrome is not fixed.

Results in shared_bath_results.json:

- All 64 pre/post record branches and 8 seed tuples satisfy the pathwise phase identity exactly in floating point; the Fourier delta error is 1.80e-16.
- The fixed-path instrument normalization error is 6.72e-16.
- Exact Lindblad matrix exponentials, summing all unobserved Poisson trajectories, verify every nonempty subset bound at gamma=0,0.3,2,7. This is 28 full-input positive-operator checks, not sampling a favorable bath state.
- Maximum normalization error is 1.16e-15. Every B-product minus actual effect is positive in the numerical test. At gamma=7 the all-three bad-effect maximum eigenvalue is 1.42255e-8, below its B-product 9.33412e-8.
- The common-bath pulse commutator norm is 0.0522721, so the check does not reduce to independent commuting local channels.

These are numerical sanity checks. Sections 2-6 give the operator proof. A separate independent audit and its own fixed-path computation are recorded alongside this file.

## 10. Established operation family and scope

For one Hermitian Pauli S, write the nonselective projective measurement M_S(X)=(X+SXS)/2. Then exactly

    gamma(Ad S-I)=2gamma(M_S-I)=-(gamma/2)[S,[S,.]].

Its free semigroup is a convex mixture of identity and Ad S with weights (1+exp(-2gamma t))/2 and (1-exp(-2gamma t))/2. Thus the dephaser can equally be described by unobserved Poisson unitary jumps, unobserved Poisson projective measurements at rate 2gamma, or the usual continuous-dephasing generator. These are established measurement/dephasing primitives, and no jump record is produced for the actual controller by choosing the first description.

Measurement-induced syndrome protection is established prior art: Paz-Silva, Rezakhani, Dominy and Lidar combine weak measurements with stabilizer error-detection/correction codes and derive protection bounds (Phys. Rev. Lett. 108, 080501 (2012), https://arxiv.org/abs/1104.5507). Dominy et al. analyze nonselective weak measurement of either the stabilizer group or a generating set (J. Phys. A 46, 075306 (2013), https://arxiv.org/abs/1207.5880). Noise-induced formation of Zeno subspaces is discussed by Pascazio (https://arxiv.org/abs/quant-ph/0311195). Continuous syndrome-measurement feedback correction is also an older distinct architecture, e.g. Ahn, Doherty and Landahl, Phys. Rev. A 65, 042301 (2002), https://arxiv.org/abs/quant-ph/0110111.

The precise result proved here is an exact outcome-resolved transfer to the scheduled finite-rate joint subset-effect/support framework. No priority claim is made for the operation family or for a general Zeno principle. This note does not establish noisy measurement circuits, noisy dephaser implementations, a fully autonomous local controller, arbitrary continuous uncharged data coupling, global logical-history detection, a useful numerical hardware threshold, or a physical memory lifetime without the stated scheduled assumptions.
