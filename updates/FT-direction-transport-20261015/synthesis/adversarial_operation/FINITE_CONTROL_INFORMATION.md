# Finite controls with unknown skew: exact information, not support inference

Date: 2026-10-15. Independent reconstruction before reading other current worker scratch. The incoming source was `sources/closure/RESEARCH_NOTE.md`; source lines below refer to that file. This is a mathematical review and conditional alternative acquisition contract. No physical operation, historical novelty, competitive advantage, or external correctness is certified.

## 1. Incoming adjoint formula

The hypotheses at lines 19–32 are sufficient. In particular, the reciprocal hidden block **and reciprocal cross couplings**, invertibility of the hidden block, known accessible port injection, a common loaded operator, and known same-regime control derivatives are load-bearing.

Write the Schur complement S=B−EC⁻¹Eᵀ and measured H=S⁻¹. For z=A⁻¹c, z_P=H(c_P−EC⁻¹c_Q). The transpose solution has λ_P=Hᵀ(c_P−EC⁻¹c_Q), hence δ_P=(Hᵀ−H)H⁻¹z_P. The source Pβ with β=H⁻¹δ_P changes the hidden field by −C⁻¹Eᵀδ_P, exactly the needed hidden transpose correction. Thus λ=z+Yβ, including any sensed subset of coordinates. No step reconstructs the unknown reciprocal interior.

The source's counterexample at lines 98–115 is correct: with A_±=I±e₂e₄ᵀ, all responses to Q=[e₁,e₂,e₃,e₅] agree, but the control v=e₁−e₄ has J_±(p)=∓p/(1+2p). Both symmetric parts have minimum eigenvalue 1/2. This disproves support certification by those probes on the unrestricted stable linear class. It does not contradict the conditional theorem.

Static symmetric-part positivity is a mathematical invertibility/stability surrogate for this real model. Actual dynamic stability, loading, control calibration, common operating conditions and signed-source accessibility still require physical qualification; see source lines 152–160.

## 2. General exact sensor/source criterion

Let T=A⁻¹ be unknown and range over an open set of real matrices whose symmetric part is positive definite. Equivalently, A ranges over the open accretive cone: sym(T)=A⁻ᵀ sym(A) A⁻¹. Fixed source columns Q and sensor rows R supply M=RTQ, with exact calibrated real readings. A target is a linear functional ℓ_W(T)=tr(WᵀT).

**Theorem.** ℓ_W is uniquely determined by M on this class if and only if W lies in the real span of the measurement matrices r_i q_jᵀ, where r_i are the transposed sensor rows and q_j the source columns.

Proof: membership gives an explicit linear combination of measured entries. Otherwise finite-dimensional orthogonality supplies Δ with RΔQ=0 but tr(WᵀΔ)≠0. Around any admissible T₀, both T₀±εΔ remain accretive for sufficiently small ε. They give identical M and different target values. Inversion yields admissible A_±. This proves exact nonidentifiability at every interior admissible data realization; it does not assert that every target has an unbounded feasible range or opposite signs.

For a nonzero rank-one target cᵀTv, W=cvᵀ, the criterion reduces to c∈range(Rᵀ) and v∈range(Q). To see necessity, left and right project onto the orthogonal complements of the two spans. For full readout R=I and c≠0, it is exactly v∈range(Q).

This is a statement about an unrestricted open **mathematical** response class. Extra physical identities can shrink the class. With justified reciprocity, for example, T is symmetric and the appropriate criterion is membership after symmetrizing both measurement matrices and W. One must not replace real physical admissibility by the unrestricted class without stating that modeling step.

The rank-one conductance gradient is −(vᵀx)cᵀTv. If vᵀx=0, its first derivative vanishes independently of the missing target response, and an isolated update pvvᵀ leaves x unchanged at every invertible p. Otherwise the criterion applies directly. It gives exact value necessity, not a universal sign-impossibility statement: e.g. c=v outside the source span still has cᵀTc>0 by accretivity.

## 3. A support-free known-control operation

Suppose a finite family of actual updates has the known form A_D=A+VDVᵀ, with fixed b,c and invertible updated matrices. Let Y=TV, H=VᵀY, t=Vᵀx and wᵀ=cᵀY. The baseline x=Tb, source profiles given by columns of V, and sensors cᵀ,Vᵀ acquire J₀=cᵀx, t,H,w. Then

    J(D)=J₀−wᵀ(I+DH)⁻¹Dt.

Proof: solve x_D=x−YDx_{D,V}. Taking Vᵀ gives (I+HD)x_{D,V}=t. The equivalent identity D(I+HD)⁻¹=(I+DH)⁻¹D yields the formula. No inverse of D is required. The determinant identity shows invertibility of I+DH precisely when A_D is invertible.

The number of independent source profiles can be the dimension of the update column span after a known basis change. The formula includes all cross-control interactions inside that subspace; individual control tests do not automatically identify those interactions. For general known local derivatives, tangent sources g_j=b_pj−A_pj x give the local gradient cᵀTg_j directly and only their relevant span needs probing.

This avoids identifying hidden skew support by changing what is acquired. It requires actual source access to V or the tangent directions, appropriate sensors, calibrated derivative/update laws, linear operation, and common loading. It is standard forward response and low-rank elimination, not a novelty claim. If only a few finite actions matter, randomized direct comparisons may require fewer or cheaper resources and do not require the derivative law. Parent work develops error/stability refinements; they are outside this independent initial derivation.

## 4. Approximate coverage can still close a decision

If an independently justified bound sym(A)≥aI, a>0, is available, then ∥T∥₂≤a⁻¹. With full readout, v=Qα+e gives

    |cᵀTv−cᵀ(TQ)α|≤∥c∥₂∥e∥₂/a.

Add the jointly valid measurement error for cᵀ(TQ)α. If the resulting interval excludes zero by the required margin, a local sign decision can be closed without exact coverage or support identification. The norm/coercivity bound, residual distance, joint error and stability under the contemplated finite step are paid hypotheses. A sign certificate at the operating point does not certify finite-step improvement.

For a finite catalogue, exact optimal action identification requires the observed information fiber to have a common optimal feasible action. Exact mechanism identification is stronger and unnecessary. Conversely, exact response nonidentifiability alone need not prevent a decision if every compatible response selects the same action.
