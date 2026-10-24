# Intrinsic index bound and a sharp pinching class

**Update:** The formerly open full-matrix inclusion case is now resolved in `general_inclusion_sharpness.md`. A Crann–Kribs–Pereira unitary basis with Markov trace supplies the missing flat code for every multiplicity list. Sections 5–7 below retain the original discovery-stage limitation; they are superseded for inclusions into a full matrix algebra, not for all abstract multi-matrix inclusions.

24 October 2026. Constructive extension following the exact simplex result. The goal is to remove dependence on a redundant finite-group representation. No historical novelty claim is made.

## 1. Intrinsic complete order index

Let E:M→N be a trace-preserving conditional expectation between finite-dimensional unital matrix algebras. Define its complete Pimsner–Popa order index by

C_cb(E)=inf{C≥1: Z≤C(E⊗id_k)(Z) for every k≥1 and every Z≥0}.

This is intrinsic to E. Adding redundant group elements to a twirl representation cannot change it. For the results below, it is enough to have any certified finite C satisfying these amplified inequalities. If C=1, E=id and the conditional divergence is identically zero; we exclude that trivial case when discussing ratios.

For finite-dimensional expectations the complete index is a standard established object. Gao–Zhao, “Tight Entropy Contraction of Generalized Quantum Depolarization,” https://arxiv.org/html/2608.19685 , introduces this same order parameter and its matrix amplification in its discussion of complete entropy contraction. The present derivation concerns arbitrary two-state conditional divergence, not only D(ρ||Eρ).

## 2. A centered quadratic bound from a 2×2 amplification

Let X=X* and EX=0. The operator matrix

Z = [ X²   X ]
    [ X    I ]

is positive because it is [X;I][X,I]. Apply the complete index inequality to Z:

[ X²   X ] ≤ C [ E(X²)   0 ].
[ X    I ]     [   0     I ]

Equivalently,

[ C E(X²)−X²    −X    ] ≥0.
[     −X      (C−1)I ]

Since C>1, taking its Schur complement gives

C E(X²)−X²−X²/(C−1)≥0,

and therefore

X²≤(C−1)E(X²).                                       (1)

Only the 2×2 amplification of the index bound was needed for this step. To retain the same bound after an arbitrary untouched reference is adjoined, the complete index is the appropriate uniform quantity.

A finite group of N conjugations gives the elementary centered bound with N−1. Equation (1) replaces that representation-dependent N by the intrinsic C_cb(E).

## 3. Conditional relative-entropy bound with intrinsic constant

Let Φ_λ=λ id+(1−λ)E and D_E(ρ||σ)=D(ρ||σ)−D(Eρ||Eσ). The already established SLD gauge and dual conditional-variance formulas apply to E without any group assumption.

For EX=0, write

A=TrσX²,
T=Tr(Eσ)X²,
B=Tr(Eσ)L²,

where L is the optimal reference score. Then the fixed-baseline conditional SLD quotient is optimized over

λ²(A−B)/[λA+(1−λ)T−λ²B].

Equation (1) gives A/T≤C−1, while B≥0. The quotient decreases in B and increases in A/T after B is set to zero. Hence

D_E(Φ_λρ||Φ_λσ)
≤ [(C−1)λ²/(1+(C−2)λ)]D_E(ρ||σ).                  (2)

The passage from SLD to BKM uses the untouched-qubit integral, and the passage to relative entropy uses line-segment Bregman integration, exactly as in conditional_depolarizing_upper_proof.md. Both operations are valid for E⊗id_k. Thus (2) holds uniformly over all finite untouched references with C=C_cb(E), or with any larger certified index bound.

The relative two-channel upper similarly becomes

J_λ/J_μ≤(λ/μ)²[1+(C−2)μ]/[1+(C−2)λ],

where J_t=D_E(Φ_tρ||Φ_tσ). The universal Loewner lower bound from relative_two_sided_comparison.md is unchanged.

Equation (2) is an upper bound for a general conditional expectation. It is not asserted sharp solely because C is the optimal index.

## 4. A concrete sharp algebraic class: arbitrary finite pinching

Let P₁,…,P_m be nonzero mutually orthogonal projections summing to I, and let

E(X)=∑_{j=1}^m P_j X P_j.

Their ranks may be arbitrary. Then C_cb(E)=m.

Upper index proof: the pinching inequality Z≤m∑_jP_j ZP_j holds for every positive Z, and also after arbitrary amplification, because there remain exactly m orthogonal projections. It follows, for example, by applying vector Cauchy–Schwarz to rank-one positive operators and then summing a positive decomposition.

Lower index proof: choose unit vectors e_j∈range P_j and v=m^(−1/2)∑_j e_j. Then E(|v><v|)=P_S/m, where S=span{e_j}. Taking the expectation in v shows that any index bound must be at least m. Thus the amplified upper and unamplified lower agree.

The conditional contraction bound (2) is sharp for this E. On S choose the Fourier basis

f_i=m^(−1/2)∑_{j=1}^m exp(2πi ij/m)e_j,

and let F_i=|f_i><f_i|. These projectors are pairwise orthogonal, sum to P_S, and satisfy E(F_i)=P_S/m. Consequently

Φ_λ(F_i)=λF_i+(1−λ)P_S/m.

Encoding the classical label i into F_i, while retaining arbitrary quantum reference blocks, exactly simulates K_{λ,m}. Input and output relative entropy are preserved by the orthogonal-sector encoding, and the conditioned state is P_S/m tensored with the original reference marginal. The simplex construction for K_{λ,m} therefore proves the matching lower bound.

If S is smaller than the whole physical space, the encoded states are initially faithful only on S⊗R. This is not a gap: S and S^perp are invariant under all P_j and Φ_λ. Add the same arbitrarily small full-rank blank state on S^perp⊗R to both hypotheses. The input/output conditional divergences scale by the same active-sector weight, the ratio is unchanged, and the states become faithful on the full space. Equality of the conditioned states is also preserved.

Therefore, for pinching into m nonzero sectors,

η_E^complete(Φ_λ)=η_E^conditional(Φ_λ)
=(m−1)λ²/[1+(m−2)λ].                                (3)

Here “complete” means the equal-conditioned-state restriction Eρ=Eσ, with arbitrary untouched finite reference, not an unrestricted full relative-entropy ratio. Fixed-algebra directions would give full relative-entropy contraction one.

The parameter m is intrinsic: it equals C_cb(E), independently of the ranks of the sectors and independently of how many redundant phases are included in a group representation. For m=2, (3) is exactly λ².

## 5. A sufficient module-geometry criterion for sharpness

The pinching and depolarizing proofs share a stronger structural property. Suppose an amplification of E contains an invariant code projection P and N pairwise orthogonal rank-one projectors F₁,…,F_N summing to P, with

(E⊗id)(F_i)=P/N for every i.

Then encoding a classical label into F_i exactly embeds K_{λ,N}, including its conditional divergence and equal-conditioned-state witnesses. If in addition C_cb(E)=N, equation (2) and simplex sharpness prove equality with the intrinsic index bound.

Pinching has this property through the Fourier basis above. Quantum depolarizing expectation E(X)=I_d/d⊗Tr_A X has it after a d-dimensional amplification, through the d² Bell projectors; C_cb(E)=d².

This criterion is sufficient, not claimed necessary. An index-achieving rank-one vector alone does not automatically supply a complete orthogonal family of such vectors. In more general finite-dimensional inclusions, that additional basis/module geometry may be a genuine obstruction. The present note does not assume that every inclusion possesses it.

## 6. A safe direct-sum extension

If the ambient algebra is itself a direct sum M=⊕_k M_k and E=⊕_k E_k preserves those central sectors, then the conditional divergences split as sums weighted by the numerator's central probabilities; the classical central relative-entropy terms cancel. Therefore the optimized conditional coefficient is the maximum of the sector coefficients. A faithful common blank mixture allows any one sector's supremum to be approached while preserving full faithfulness.

The complete index is likewise max_k C_cb(E_k). Hence direct sums of sharp pinching or tensor-factor depolarizing expectations yield further intrinsic sharp cases. This statement does NOT cover an arbitrary inclusion into one full matrix algebra that also erases coherences between central blocks and depolarizes nontrivial multiplicity spaces; its index and flat-code geometry require a separate analysis.

## 7. Serious limit of the argument

The intrinsic upper is rigorous and the pinching class is exactly solved. A blanket assertion that every finite-index conditional expectation attains the bound would require proving the flat orthogonal code criterion or another sharpness construction. Neither index optimality nor existence of a finite group representation establishes that criterion. We leave general sharpness open rather than identifying a redundant group cardinality with an intrinsic invariant.
