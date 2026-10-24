# Finite group-twirl conditional-expectation extension

24 October 2026. Independent reconstruction of the root's extension. The proof uses the metric integral established in conditional_depolarizing_upper_proof.md and no N675 result.

## Setting

Let M be a finite-dimensional unital matrix *-algebra, with its inherited faithful trace Tr. States are positive elements of M of trace one. Let E:M→N be the trace-preserving conditional expectation onto a unital *-subalgebra N⊂M.

Assume that E has a uniform finite-group twirl realization

E(X)=(1/N₀)∑_{g∈G} U_g X U_g*,

where |G|=N₀≥2, the identity conjugation occurs once, each conjugation preserves M, and the conjugation actions form a group. A projective unitary representation is sufficient: phases do not affect conjugation. It is not necessary that the chosen U_g themselves form a literal group without phases.

Define Φ_λ=λ id+(1−λ)E, for 0≤λ≤1, and

D_E(ρ||σ)=D(ρ||σ)−D(Eρ||Eσ).

Then for faithful ρ,σ∈M,

D_E(Φ_λρ||Φ_λσ)
≤ [(N₀−1)λ²/(1+(N₀−2)λ)] D_E(ρ||σ).                (1)

Here EΦ_λ=E, so the reference term on the output side is exactly D(Eρ||Eσ). The theorem also holds after tensoring the entire algebra and expectation with an arbitrary untouched finite reference algebra, with the same constant.

## 1. Gauge and its algebra membership

Let σ be faithful and H=H*∈M. Define L∈N by

L=Ω_{Eσ}^(−1)(EH), where Ω_a(X)=(aX+Xa)/2.

The inverse stays in N. For example,

Ω_a^(−1)(B)=2∫₀^∞ exp(−ta) B exp(−ta)dt

for faithful a, and the integrand lies in N when a,B∈N. Thus L is a legitimate element of the conditioning algebra.

Set H₀=H−Ω_σ(L). Bimodularity of E gives

EΩ_σ(L)=Ω_{Eσ}(L)=EH,

hence EH₀=0. A trace-preserving conditional expectation is self-adjoint for the Hilbert–Schmidt pairing. Therefore

Tr H₀L=Tr(EH₀)L=0,
Tr σL²=Tr(Eσ)L².

The same orthogonal SLD decomposition as in the partial-trace case yields

g^S_σ(H)−g^S_{Eσ}(EH)=g^S_σ(H₀).                    (2)

Because Φ_λ is N-bimodular,

Φ_λΩ_σ(L)=Ω_{Φ_λσ}(L),

and its conditioned baseline is still Eσ. Thus (2) also holds at the output with the same reference score L. This is the exact point at which the conditional-expectation and bimodule hypotheses are used. An arbitrary average of channels cannot replace E in this argument.

## 2. Group cancellation and the metric constant

For EH₀=0, twirling gives

∑_{g≠e}U_gH₀U_g*=−H₀.

The mixture representation of Φ_λ has identity weight p₀=[1+(N₀−1)λ]/N₀ and every other group weight p=(1−λ)/N₀. Joint convexity and unitary invariance of the SLD metric give the scalar optimization

min{p₀u²+(N₀−1)pv² : p₀u−pv=λ}
=λ²/[p₀+p/(N₀−1)]
=(N₀−1)λ²/[1+(N₀−2)λ].

This proves the uniform SLD bound on ker E, hence the conditional SLD bound through (2).

## 3. BKM and relative entropy

Apply the one-qubit auxiliary-reference identity

g^B_σ(H)=∫₀^∞ g^S_{σ⊗τ_s}(H⊗X) ds/[4(1+s)²],

with τ_s=diag(1,s)/(1+s), and apply it also to Eσ,EH. Use the extended conditional expectation E⊗id_{M₂}. Its group has the same cardinality and acts trivially on the new reference qubit. Integrating the conditional SLD inequality gives its conditional BKM counterpart. Integrating that metric inequality along σ+t(ρ−σ) proves (1).

The integration and faithfulness justifications are identical to those already given in conditional_depolarizing_upper_proof.md. All comparisons are finite-dimensional, and the auxiliary qubit is untouched.

## Examples and necessary scope distinctions

### Depolarization on a quantum d-level system

Take M=M_d⊗M_R and E(X)=I_d/d⊗Tr_A X. The d² Weyl conjugations form the needed group of conjugation actions. Thus N₀=d², recovering

(d²−1)λ²/[1+(d²−2)λ].

For Weyl representatives themselves, phases generally prevent a literal d²-element unitary group. Conjugation actions are the correct formulation.

### Uniform reset of an N-symbol classical input with quantum reference

Take the ambient algebra M=⊕_{x=1}^N M_R, represented as classical-quantum block-diagonal matrices. Let the cyclic group shift the classical blocks. Its average is

E(diag(X₁,…,X_N))=diag(X_R/N,…,X_R/N),
X_R=∑_x X_x.

This is a trace-preserving conditional expectation onto the identical-block subalgebra. The theorem gives

η_D^conditional ≤ (N−1)λ²/[1+(N−2)λ]

for this classical input channel with arbitrary quantum reference. For N=2 the bound is λ² and is sharp already without a reference, using an infinitesimal perturbation of the uniform binary distribution.

The ambient block-diagonal restriction matters: averaging cyclic permutations on all of M_N⊗M_R has additional fixed offdiagonal operators, so it is not the classical uniform-reset conditional expectation there. The N-element argument must not be silently applied to arbitrary coherent inputs on that larger algebra.

### An involutive unitary dephasing expectation

If E=(id+Ad_U)/2 with U² a scalar multiple of I, then N₀=2 and (1) gives λ² for contraction of D(ρ||σ)−D(Eρ||Eσ) under λ id+(1−λ)E. This is a conditional-information statement relative to E, not a claim that the channel's unrestricted full relative-entropy contraction coefficient is λ²; fixed-algebra directions have full contraction one.

## What is and is not established

The framework is broader than one depolarizing example: the same state-independent proof applies to finite group-twirl conditional expectations, including quantum and classical-quantum block algebras. The numerical constant depends on the chosen twirl realization; redundant or larger groups may give weaker constants. Optimality and the smallest admissible twirl cardinality are separate questions.

No claim is made that every unital channel is a conditional expectation, that arbitrary channel averages have the required bimodule property, or that the resulting coefficient is exact. Historical novelty remains to be checked against complete entropic inequalities, monotone-metric contraction, and conditional-expectation literature.

## Closest inspected generalized-depolarization prior

Gao–Zhao, “Tight Entropy Contraction of Generalized Quantum Depolarization,” arXiv:2608.19685, https://arxiv.org/html/2608.19685 , explicitly studies the same interpolation λ id+(1−λ)E, including complete amplification and index-based bounds. Its introduction, Eqs. following the definition of η, specifies the comparison D(Φ_λρ||Eρ)/D(ρ||Eρ): the initial state is compared to its own fixed-point projection. That is an important and closely related prior, but it is not the arbitrary TWO-STATE conditional difference D(ρ||σ)−D(Eρ||Eσ) bounded here. We must not claim its results are absent or subsumed, or assert novelty merely because the displayed functionals differ. Its sharper fixed-point-relative estimates can be stronger in that narrower setting.
