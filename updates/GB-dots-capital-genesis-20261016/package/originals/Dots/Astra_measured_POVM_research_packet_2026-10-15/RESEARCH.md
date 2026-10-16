# Exact construction and experimental interpretation

## Capability established

The mathematical capability is a strict decrease of binary squared-error risk by the measured-receiver model relative to the ideal erasure-source optimum, conditional on an explicit deterministic uncertainty set and ideal preparations. The comparison includes the same quantum reference system. Both selected source parameters remain above the ordinary no-reference SLD threshold, so the reference-assisted witness does not arise by moving below that threshold.

This analysis evaluates the actual printed Huang θ=π/4 EJM matrices directly. It does not apply a Bell-fidelity certificate to an EJM, infer Bell equivalence from high fidelity, or presume an unmeasured entangling operation.

## States, labels, and loss

Let X,Y,Z denote Pauli matrices and put a=9/10, b=9√2/20, r=6/11, z=9/11. The uniform classical input is i∈{−1,+1}; the independent uniform estimation label is ℓ∈{−1,+1}. Define

σᵢ=(I+bZ+i bX)/2,

τℓ,ᵢ=(I+ℓ i rX+zZ)/2,

ρℓ=(1/2)Σᵢ σᵢ⊗τℓ,ᵢ.

The target states have Bloch length a=0.9. Conditional reference states have length √117/11<1. Every specified single-qubit preparation is faithful. The reference marginal (I+zZ)/2 is independent of ℓ.

For a real stereographic vector t, use the exact local unitary

U(t)=[(1−|t|²)I−2i(tₓX+tᵧY+t_zZ)]/(1+|t|²).

Freeze t_output=(20,−27,−16)/1000 and t_reference=(−471,−263,−453)/1000. The joint preparation is

ρ′ℓ=(U_output⊗U_reference)ρℓ(U_output⊗U_reference)†.

For outcomes E1,E2,E3,E4, freeze s=(−719,646,−270,149)/1000 and loss (ℓ−sₖ)². The resulting loss matrices are

Lₖ=(1/2)Σℓ(ℓ−sₖ)²ρ′ℓ,

and any physical receiver F has risk R(F)=ΣₖTr(FₖLₖ).

The local rotations and scores were chosen using the existing calibration fit. They are frozen for this computation, but a prospective validation must freeze them before collecting independent evaluation data. The exact unitary product is explicitly reconstructed in both constructor and audit.

## Source optimum and ordinary comparison

The ideal source reveals i with probability q; otherwise it outputs only the reference. In an erased branch the reference marginal is the same for both labels, so the optimal score is zero and risk is one. In a revealed branch, the two reference states differ along X with amplitude r, yielding optimal squared-loss risk 1−r². Consequently

R_source(q)=1−q r².

A common unitary on the reference rotates the optimal measurement without changing this optimum. The output local unitary only changes the target basis; the ordinary source comparison threshold remains c=b²=0.405. Both q=.45 and q=.43 exceed c. No source benefit is removed by restricting its reference basis or by keeping its estimator artificially fixed.

The exact source risks are R_source(.45)=524/605 and R_source(.43)=2638/3025. These correspond to distinct source experiments.

## Data basis and physicality

Huang's mathematical basis is |00>,|01>,|10>,|11>, ordered B1⊗B2, polarization then spatial. Outcomes E1,E2,E3,E4 correspond to +++, +−−, −+−, −−+. The circuit drawing's vertical wire order must not replace the mathematical tensor ordering. Full state overlaps were used during acquisition to cross-check the printed fidelities and outcome convention.

The printed θ=0 and θ=π/4 matrices retain three-decimal entries, including last-digit failures of exact Hermiticity and completeness. The maximum Hermiticity discrepancy is .001 for both. The Hermitian part of the π/4 tuple has minimum eigenvalue about −.0007031293 and completeness-defect operator norm about .0018507811. Thus the printed tuple is not itself an exact physical POVM.

The raw diagnostic uses the real part of the direct loss functional, including its noncompleteness: Re ΣₖTr(EₖLₖ)=.86387183275112979939. A shortcut based on one minus explained variance would not be justified for these incomplete printed matrices. No silent projection, Hermitization, renormalization or substitution of an existence witness is used to label the prediction physical.

A bounded 24-start local-rotation search found a θ=0 best risk .9272297199248583, which does not reverse q=.45. That search is not a global no-go proof. For π/4 the pre-freeze best found risk was .8638705102127158. The mathematical guarantee uses the exact frozen parameters above, not the optimizer's unrounded result. Search optimality is unnecessary to verify the witness.

## Deterministic box certificates

For τ∈{1/2000,1/1000}, define the uncertainty set as all four-effect POVMs F satisfying Fₖ=Fₖ†≥0, ΣₖFₖ=I, and

|Re(Fₖ−Eₖ)ₐᵦ|≤τ,   |Im(Fₖ−Eₖ)ₐᵦ|≤τ

for every printed entry, including both conjugate entries independently.

The tighter bound uses all 16 independent real Hermitian coordinates. For each coordinate, intersect the tolerance intervals from the two printed conjugate positions. Completeness fixes the sum of four effect coordinates to the matching identity coordinate. The risk is linear in these coordinates. Dropping positive semidefiniteness yields a separable bounded-sum linear program whose optimum upper-bounds the risk of every physical POVM in the box.

The constructor maximizes each coordinate contribution by exact ordered allocation. Coefficient ordering is proved algebraically in Q(√2). The independent audit instead enumerates all vertices of each four-variable bounded-sum polytope and verifies every maximizing comparison exactly. It then checks equality with the stored symbolic expressions.

This yields the bounds listed in README. At ±.0005 the q=.45 gap exceeds .000245; at ±.001 the q=.43 gap exceeds .004602. The relaxed risk maximizer need not be PSD; it is used only as an upper bound.

An additional simpler certificate subtracts a common Hermitian center Y, using completeness to write

R(F)=Tr(Y)+ΣₖTr[Fₖ(Lₖ−Y)].

Its algebraic base is below 864558/1000000 and its componentwise sensitivity coefficient below 3187/1000. At q=.43, τ=.001 this gives the weaker but independently useful exact lower gap 104571/24200000≈.00432111570248.

For physical nonemptiness, the packet contains rational matrices with denominator 100000000. All leading principal minors are strictly positive, each effect is exactly Hermitian, and their sum is exactly I. Every component lies in the stated box. The tighter witness proves both boxes nonempty; another witness for ±.001 has maximum component error .00059732. These are existence proofs, not estimates of the actual measurement.

## Welte result and convention

The four public CSV effects use the Bell basis Φ+,Φ−,Ψ+,Ψ−. The outcome mapping verified against the dataset and 2021 journal is AA→Φ+, AD→Φ−, DA→Ψ+, DD→Ψ−. A later author manuscript contains a reversed-label fidelity sentence; the code follows the dataset and journal convention.

The effects are positive and complete to floating-point precision (minimum eigenvalue approximately .00154465). The requested ideal-input states are transformed into that Bell basis, and probabilities are evaluated by Tr(Eₖρℓ). Fixed ideal Bell scores give risk 1.0056355173125497 and gap −.13951981483321085 at q=.45. The best scores for these same conditional probabilities are (p₊−p₋)/(p₊+p₋); their risk .9624734837175528 is still higher than the source risk.

These effects describe the success-conditioned fit. The published overall success rate is about .1%; failed-trial effects and input-resolved success probabilities are not represented by the normalized four-effect model. No all-trial conclusion follows. Preparation-related errors may also be incorporated in that fit. The computation does not optimize every local rotation or rule out general hardware capability.

## Closest experimental precedents and missing operation

Huang's existing EJM implementation and numerical tomography are the closest measured receiver evidence for the positive conditional construction. Welte provides directly machine-readable Bell POVM data and a verified negative result for this fixed test. Neither publication is being credited with performing the proposed source-versus-target estimation experiment, and the present reanalysis is not a newly measured result. These are the closest concrete experimental precedents examined here; this packet does not claim an exhaustive priority determination.

The missing operation is a verified implementation and calibration of the two specified local preparation rotations, followed by an independently evaluated, matched source/target task. No evidence here establishes that the local controls can realize the rational settings at the required accuracy, that the detector model transfers unchanged to those preparations, or that actual effects belong to either box.

Huang's reported individual and aggregate fidelity error bars cannot be turned into the componentwise boxes without additional counts and a joint uncertainty analysis. Its 36 product-Pauli probe tomography and restricted five-phase noise fit do not supply this missing guarantee. Neither printed precision nor a nonempty rounding box proves a confidence region for the physical apparatus. Postselection, preparation errors, drift and outcome-dependent efficiencies must be included in the intended task's accounting.

## Consequence and decisive test

The result narrows the next experiment to a concrete local-preparation/scoring design with a checkable target loss. It gives a deterministic implication: if an independently justified physical measurement model belongs to the declared set, and ideal preparation assumptions hold, the stated gap follows. It does not establish those antecedents experimentally.

A decisive test would:

1. Freeze q, local rotations, scores, label/input distribution, outcome mapping, inclusion rules and risk estimator before new data collection. Choose q=.45 or .43 explicitly; do not switch the source after observing test outcomes.
2. Verify the local preparation mapping and include preparation uncertainty. Acquire full-precision effects or raw 36×4 calibration counts, probe-state calibrations and a defensible joint uncertainty construction. Separate calibration used for design from held-out task evaluation.
3. Record trial denominators, herald/no-click/failure outcomes and input-resolved efficiencies. Either explicitly restrict the claim to an appropriate conditional task or include failed trials in a loss-inclusive comparison.
4. Collect matched source and target task trials across repeated blocks; account for drift and correlations. Retain source optimality and include the same allowed reference access in both arms.
5. Demonstrate a task-specific positive risk gap with valid uncertainty coverage. A justified deterministic uncertainty set containing the apparatus and preparations, or a statistically valid independent direct-risk interval, must support the sign. If measured calibration uncertainty exceeds the stated boxes, recompute the bound rather than treating printed fidelity as a substitute.

This would test the operational claim that the present algebra only predicts conditionally.
