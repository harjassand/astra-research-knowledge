# Final scientific boundary and capability audit

Audited: `phase8/root/CAUSAL_CLOSURE_AND_JOINT_ADMISSION.txt`.

## Decision

The general passive-scattering result is a useful physical interface theorem. It can be sharpened to a necessary-and-sufficient statement for an **unmeasured controlled-displacement product channel** under finite homogeneous thermal/vacuum input, after removing data-independent displacements. It cannot be advertised as a universally necessary two-closure boundary for an arbitrary terminal measurement instrument. A terminal measurement may intentionally erase the coherence that carries incoming-memory dependence; a record-inclusive no-influence instrument also need not have a product retained channel.

The exact full-instrument boundary is the record-inclusive complete-map identity in root Eq. (1). The two closures are a constructive criterion for the stronger gate-channel interface, and in the stated homogeneous Gaussian setting they are generically necessary for that stronger interface.

The justified scientific advance is physical admission and interface construction for a retained unbounded bosonic apparatus, joined to a real noisy receiver. No demonstrated information-processing capability exceeds the finite dirty-qubit comparator or ordinary fault-tolerant encoded circuits. The bosonic dynamics and physical-admission result remain nontrivial even though the resulting parity and consumed CNOT capabilities are conventional.

## 1. A precise sharp statement for the unmeasured channel

Use the complete passive dilation, including any vacuum inputs needed to complete an isometry to a unitary scattering model. Let

\[
 U_z=e^{i\phi_z}D(d_z)U_0,
\]

and let z range over the actual data eigenvalue labels. Fix a reference label z0 and set

\[
 \delta d_z=d_z-d_{z_0}.
\]

A common displacement can be absorbed into the data-independent apparatus channel; its Weyl phase contributes only a known scalar data phase. Conditions should therefore be imposed on displacement **differences**, not automatically on every coefficient in a redundant data-observable expansion.

Assume:

- The fresh field is independent of the old apparatus and arbitrary data/reference inputs.
- It is a finite-occupation homogeneous Gaussian thermal field, including vacuum.
- Forces and displacement vectors are finite.
- The data output is the full unmeasured controlled-displacement channel; no final data measurement has already removed selected coherences.

Then the product-channel identity

\[
 \Lambda_{DM}=\Phi_D\otimes\mathcal E_M
\]

holds for every correlated input if and only if

\[
 P_{\rm old}S^\dagger\delta d_z=0,
 \qquad P_{\rm ret}\delta d_z=0
\]

for all relevant labels z. Equivalently, impose the same conditions on all pairwise differences.

### Necessity of incoming closure

For a pair of data labels z,z', the reduced-data off-diagonal coefficient is determined by a relative Weyl operator. Its old-mode part is

\[
 D_M\!\left(P_{\rm old}S^\dagger(d_z-d_{z'})\right),
\]

multiplied by the fresh-field characteristic function. A finite Gaussian thermal characteristic function is strictly nonzero at every finite displacement. Independence from **every** old input operator therefore requires this old Weyl operator to be scalar. In the usual oscillator representation, that occurs only for zero displacement.

A non-Gaussian fresh state can have characteristic-function zeros, so this necessity statement should not be extended without qualification to arbitrary fresh states. A terminal instrument can also remove the relevant coherence, as discussed below.

### Necessity of outgoing closure

Prepare the data in an eigenstate z and the old apparatus in a fixed coherent state, for example vacuum. The retained output is the free Gaussian output displaced by \(P_{\rm ret}d_z\). A product channel requires the same retained channel for every z. A normalizable finite-covariance Gaussian state is not invariant under a nonzero displacement, so every retained displacement difference must vanish.

### Sufficiency

This is the existing mode-splitting proof: incoming closure puts the controlled displacement span in the fresh field; outgoing closure makes it orthogonal to the fresh directions feeding retained outputs. Homogeneous thermal/vacuum input factors over that passive mode split. The off-diagonal-block proof then gives the product channel on arbitrary entangled inputs.

This is a sharp statement for its declared unmeasured channel class. Calling it a sharp theorem for **all full instruments** would be stronger than what these arguments prove.

## 2. Covariance: sufficient factorization versus the minimal condition

Root's statement that zero covariance between K and its entire complement is the additional condition for a general Gaussian input is a safe sufficient condition. It is stronger than necessary.

Only fresh directions that feed the retained output need to be separated from the controlled directions. For example, K may be correlated with another fresh mode that is entirely discarded, while remaining independent of every fresh mode entering the retained apparatus. Such correlations do not prevent the reduced retained product channel.

An exact Gaussian condition can be expressed through characteristic functions. Let ζ range over the pulled-back controlled displacement differences, and let w range over fresh components of pulled-back retained-output Weyl tests. Once the two closure conditions hold, the required condition is

\[
 \chi_F(\zeta+w)=\chi_F(\zeta)\chi_F(w)
\]

for those ζ and w. In real phase-space coordinates, a Gaussian characteristic function reduces this to vanishing covariance pairing

\[
 \zeta^{\mathsf T}V_Fw=0.
\]

The covariance condition need only hold on the real span of the displacement differences actually probed by the data. If both quadratures of a whole controlled mode subspace are available, the familiar block-covariance condition is recovered. Full factorization between K and all of K-perpendicular is a convenient stronger hypothesis.

Homogeneous thermal covariance is proportional to identity and satisfies the condition automatically because of the passive orthogonality. Returning field modes belong to the old apparatus, not to a fresh covariance assumption.

## 3. The sharp boundary for a delivered instrument

For a delivered outcome y, the exact no-influence condition is

\[
 \operatorname{Tr}_{M'}\Lambda_y(\rho_{DM})
 =\mathcal I_y(\operatorname{Tr}_M\rho_{DM})
\]

for all inputs including references. Equivalently, for every data observable O and outcome y,

\[
 \Lambda_y^*(O\otimes I_{M'})
 =\mathcal I_y^*(O)\otimes I_M.
\]

This is necessary and sufficient. It is also the appropriate boundary when fine analog records, random keys, or apparatus measurements are delivered to future consumers.

A general product-channel test can likewise be stated exactly. Define the retained off-diagonal block maps

\[
 \mathcal T_{zz'}(X)=\operatorname{Tr}_E[V_z X V_{z'}^\dagger].
\]

The product channel holds exactly when there are one retained CPTP map E and scalar coefficients czz' such that

\[
 \mathcal T_{zz'}(X)=c_{zz'}\mathcal E(X)
\]

for every X and every label pair. A terminal measurement changes these block maps. One cannot infer necessity of the original premeasurement closure equations from a different measured instrument without analyzing that measurement.

### Why a terminal measurement can relax incoming closure

Consider a controlled old-apparatus unitary

\[
 U=\sum_s P_s\otimes V_s
\]

followed by an actual projective measurement of the data observable with projectors Ps. For outcome s,

\[
 \operatorname{Tr}_M[P_sU\rho U^\dagger P_s]
 =P_s(\operatorname{Tr}_M\rho)P_s.
\]

The old-apparatus operation may differ substantially between sectors, but it does not affect the delivered data/record instrument. The terminal measurement has removed precisely the cross-sector coherence on which the relative old-mode operator acted.

Thus even a nontrivial incoming controlled displacement can be harmless for a particular measured task. The retained apparatus may still undergo outcome-dependent channels, so this example need not have the stronger product interface. If the old subsystem is subsequently discarded/replaced by an appropriate passive swap with a fresh subsystem, even a product measured instrument can be obtained without the premeasurement incoming null.

The correct statement is therefore: nonzero incoming displacement spoils a uniform all-state coherence claim **for a coherence retained by the target channel and having nonzero fresh characteristic coefficient**. This is enough for the force-gate derivation, but it is not a universal prohibition for measured tasks.

## 4. Audit of the projected cross-form controllability sentence

The intended linear-algebra observation is useful, but its scope needs refinement.

Let the actual admissible waveform spaces of the two independent force channels be K1=ker C1 and K2=ker C2. These spaces must already include the physical quadrature restrictions. Let Q1,Q2 be bases for those spaces, and let the actual real geometric cross phase be

\[
 \theta(u,v)=\mathfrak b(u,v).
\]

The clean existence criterion is:

\[
 \mathfrak b|_{K_1\times K_2}\not\equiv0.
\]

In a suitable real basis this is simply a nonzero projected cross matrix. In a complex sesquilinear representation, use the real or imaginary part that actually enters the physical angle, with the allowed phase freedoms specified.

Under independent unrestricted amplitudes in these spaces, a nonzero matrix element supplies a pair of controls with nonzero geometric cross phase. Conversely, a zero cross form rules out such a phase in that family. This is the valid small-signal controllability statement.

### It does not prove the following stronger conclusions

1. **A self form is not a cross form.** Nonzero Q†AQ on a stacked control space may arise entirely from self phases. Two independent oscillators can each acquire a geometric self phase while having zero coupling between the useful data systems. The relevant off-diagonal channel block must be nonzero.
2. **Physical real constraints matter.** A nonzero complex matrix can have zero relevant real bilinear form on an allowed real-quadrature control space. “Hermitian/skew form” should not conceal this distinction. A real skew form also has identically zero single-vector quadratic form, so a generic appeal to quadratic polarization is imprecise unless the chosen convention is stated.
3. **Nonzero does not reach π/4 under caps.** At fixed duration, amplitude, slew, and bandwidth limits, a nonzero cross form may produce only a tiny attainable phase. Scaling to the desired parity angle costs resources and requires a separate feasibility calculation.
4. **Radiation orthogonality is an additional constraint.** Closure plus a nonzero geometric cross form does not guarantee two orthogonal controlled radiation modes. For example, in a one-dimensional closed waveform space, take geometric cross form A=1 and radiation Gram form G=1. The projected geometric form is nonzero, but two nonzero controls cannot satisfy u*Gv=0. More generally, if A is proportional to G on the closed subspace, imposing radiation orthogonality also kills that cross phase. The independent parity CP-tag interface therefore needs a simultaneous noise-geometry feasibility argument.
5. **The cross observable must be useful.** The resulting product J1J2 must act nontrivially on the desired logical degrees of freedom. A nonzero phase that is global or purely gauge is not the requested logical entangling action.

The root sentence is defensible if narrowed to “a nonzero closed geometric cross-phase generator exists” with the actual cross form and control spaces specified. It should not serve as the entire feasibility certificate for the exact parity instrument.

Also, in the fully general scattering setup, p old modes and q retained modes give at most p+q complex linear closure constraints per force channel. The count 2p assumes the retained mode count is also p.

## 5. Old memory, surviving data errors, and fresh faults

Record-inclusive no-influence already prevents an old apparatus perturbation from affecting the useful output of a later nominal operation. The product channel is a stronger and convenient way to establish this. It is not the only possible way.

Neither property says that a surviving **data** error has disappeared. If a correctable error remains at a recovery boundary and a new fault occurs, the receiver must handle their combined support. Root correctly retains that obligation in its inherited 5×5 / 7×7 support analysis. The finite dirty-qubit comparator needs the same obligation.

For a new physical fault that can consult arbitrary apparatus memory, the local error bound must be complete on that joint memory space, or obtained by the declared cap/replacement argument. Uniform CP effects or complete-norm bounds then compose without independent error coins. The nominal memory interface alone does not establish the strength of a physical perturbation.

One sentence in root §8 warrants explicit interpretation: “common faults affecting two sites are charged twice.” A single common physical event of probability or norm O(p) cannot be converted into two independent local faults of order O(p²). It must retain its first-order weight with its actual multi-site support. Two local insertion factors are justified only when the physical generator or instrument actually supplies that factorization. Otherwise enlarge the correctable error class/code or retain the first-order failure contribution. This matters to the stated degree-at-least-two majorant.

The signed/coherent marked-set bound in root Eq. (15) is correctly distinguished from a probability law. Its CP special case gives joint probability domination. The single global high-sector replacement remainder is likewise correctly kept separate from per-operation conditional probabilities.

## 6. Capability and novelty decision

### Already provided by strong ordinary mechanisms

- A finite dirty mediator can implement an exact entangling gate and two-data parity measurement for arbitrary mediator/reference state, with no mediator preparation.
- Ordinary noisy fault-tolerant Clifford circuits can turn those operations into repeated encoded parity extraction and a consumed CNOT with a retained noisy receiver.
- GPI supplies strong bosonic gadget constructions with inherited-error and fresh-fault budgets; its particular preprint probability argument has a narrower independent-jump premise, but general fault-tolerance machinery already supports suitable complete local-noise models with memory.
- Cat and erasure constructions can provide dominant-fault transparency or located-error information, when their physical preparation/readout/instrument costs are honestly included.

Consequently the abstract requested capability is not new once mediator/encoding changes are permitted. The finite dirty mediator also has an intrinsic uniform-control advantage: its harmful operators can be bounded independently of an oscillator energy tail.

### What the present work usefully adds

The useful result is a physical route from a particular unbounded bosonic open-system model to the interface required by an existing noisy consumer:

- It separates incoming memory influence from outgoing retained displacement.
- It proves a full correlated-input product channel, rather than only a good oscillator mean or one coherence.
- It derives the two-sector parity CP tags from the actual thermal-field geometry.
- It retains the exact damping dynamics and uses physical finite readout/records.
- It supplies a finite-lifetime global tail/replacement route and a restricted-input dilation comparison for calibration perturbations.
- It keeps microscopic residual dispersive/Kerr terms and controller/readout assumptions visible.

That is a meaningful physical-admission/interface result. It is not a new logical gate, a new fault-tolerance principle, an established device threshold, or a demonstrated overall resource advantage. Priority for the generalized theorem would require a more targeted literature comparison; the current packet appropriately avoids claiming it.

The stronger scientific direction is therefore to identify hardware whose actual control algebra satisfies this interface with useful exposure costs, or to prove a weaker receiver-specific instrument condition that safely admits more hardware. Enlarging the code fixture or optimizing another isolated fidelity is not, by itself, a new enabling capability.

## Suggested concise claim

“For passive linear mediator gates with independent homogeneous thermal input, two distinct null constraints characterize a data–retained-apparatus product channel, after removing common displacements and before terminal measurements. We use this interface, orthogonal radiation modes, and a complete finite-time noise-admission argument to implement a noisy two-sector parity instrument consumed by an existing fault-tolerant receiver. The logical capability is conventional; the contribution is its physical realization and complete-history certification in the stated bosonic model.”

For a statement intended to cover arbitrary delivered instruments, replace “two null constraints characterize” by “record-inclusive absence of apparatus influence characterizes,” and present the two nulls as a sufficient construction of a stronger channel interface.
