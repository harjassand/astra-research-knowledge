# Independent compiler reconstruction and actual-correction synthesis

16 October 2026. Worker `gd_compiler_adversary`. All statements below concern finite-dimensional exact generators. The memory implication is conditional on the supplied completed-pair clock-envelope theorem and its external imports. This file does not establish historical originality, physical implementation, a useful threshold, or a theorem for the original active-only pair generator.

The new results are: (i) the source's `4M` correlated-edge clock is minimax optimal among **all fixed CPTP centers** for that coefficient disk; (ii) bounded single-face unitary errors in an actual pair-correction jump admit a fixed local floor with an exact minimax clock rate; and (iii) a slightly more expensive floor can be implemented with the same common unknown rotation error, because its conditional Pauli average is invariant under that error.

## 1. Reconstruction of the finite-rate criterion

Use normalized Hilbert–Schmidt inner product and normalized Choi matrices. Let `F_a` be a complete traceless orthonormal operator basis and let

`L(X)=Σ_ab C_ab(F_a X F_b† - {F_b†F_a,X}/2) - i[H,X]`, `C=C†`.

Put `S=Σ_ab C_ab F_b†F_a`, `s=Tr(S)/d=Tr C`, `H_0=H-Tr(H)I/d`, and `B_0=-(S-sI)/2-iH_0`. Write `b_a=<F_a,B_0>`.

Since the normalized vectorization of the identity has norm one,

`J(λ Id+L) = [[λ-s,b†],[b,C]]`.

Indeed, `J(L)=Σ C_ab |F_a><F_b|+|G><I|+|I><G|`, where `G=-S/2-iH_0`. This derivation fixes the signs in the off-diagonal block; they are not interchangeable with the sign of the Hamiltonian.

For a Hermitian block matrix, positivity requires `C>=0`. If `v∈ker C`, restricting the quadratic form to `(z,tv)` forces `v†b=0`. Thus positivity also requires `b∈Ran C`. Under this condition,

`[z*,x†] J(λ Id+L) [z,x]^T`

`=(x+C^+bz)†C(x+C^+bz)+(λ-s-b†C^+b)|z|²`.

Consequently an exact finite-rate representation exists precisely when

`C>=0`, `b∈Ran C`, and `λ>=s+b†C^+b`.

Trace preservation of `Id+L/λ` follows from trace annihilation of `L`. For `L=0`, the infimum is zero and every positive rate works with identity proposal. A nonzero pure Hamiltonian has `C=0,b≠0` and fails at every finite rate.

If finitely many, or a finite-intensity distribution of, CPTP clocks represent the generator, their rate-weighted average is one CPTP proposal at the sum rate. Hence additional clocks on the same system cannot bypass the range obstruction. Residual continuous dynamics or enlargement of the system changes the problem.

### Gauge reconstruction, including conjugation

Factor `C=VV†` and let `L_j=Σ_a V_aj F_a`. For the minimum-norm solution `z=V^+b`, set `α_j=conj(z_j)` and `K_j=L_j+α_j I`. Then

`Σ_j α_j* L_j=B_0`, `Σ_j |α_j|²=b†C^+b`.

Therefore

`Σ_j K_j†K_j=S+B_0+B_0†+(b†C^+b)I=(s+b†C^+b)I`,

and

`Σ_j K_j X K_j† = L(X)+(s+b†C^+b)X`.

This proves both the source gauge sign and its optimum. At a larger rate, append `sqrt(λ-λ_min)I` to the unnormalized Kraus family. In a singular case, no generalized inverse removes a nonzero null-space component of `b`.

As a concrete singular obstruction, amplitude damping `D[|0><1|]` gives the Euler-channel principal minor `-1/(16λ²)`. Adding `γD[Z]` makes the residual `Z` direction available and gives `λ_min=κ/2+γ+(κ²/16+h²)/γ` for longitudinal Hamiltonian `hZ`. This repairs a different generator and charges the actual dephasing.

## 2. Reconstruction of the fixed signed floor

For distinct canonical Hermitian Paulis, suppose a specified family satisfies `|C_ab|<=M_ab`, `M_ab=M_ba>=0`, and `|h_p|<=u_p`. The error coefficient matrix may be indefinite. Set

`r_p=Σ_q M_pq`,

`τ_p=Σ_{a≠b: P_bP_a is a phase times P_p} M_ab`,

`β_p=τ_p/2+u_p`, `F=Σ_p(r_p+β_p)D[P_p]`.

For any vector `x`, each off-diagonal contribution is bounded below by `-M_ab(|x_a|²+|x_b|²)` and `C_aa>=-M_aa`. Thus `C+diag r>=0`. Since each Pauli square is identity, the floor changes `S` only by a scalar, so the original residual `b` is unchanged. The triangle inequality gives `|b_p|<=β_p`. The completed coefficient matrix satisfies

`D=C+diag(r+β)>=diag β`.

If `v∈ker D`, then `Σ_p β_p |v_p|²=0`; every component of `v` in a positive-β direction vanishes. Every zero-β component of `b` vanishes. Hence `b∈Ran D`, including exact cancellations and zero floor directions.

The variational formula

`b†D^+b = sup_x {2 Re(b†x)-x†D x}`

gives `b†D^+b<=Σ_{β_p>0}|b_p|²/β_p<=Σ β_p`. Therefore the rate is at most

`Tr C+Σ r+2Σ β <= 2Σ_ab M_ab+2Σ_p u_p`.

Both the floor and this rate are chosen before the error. Using the weaker floor for positive semidefinite `C` is invalid for a generic difference of correction dissipators. The source's signed version is needed for those differences unless additional joint identities are proved.

## 3. The four-Kraus edge, and a sharp minimax lower bound

Let `P,Q` be distinct nonidentity canonical Hermitian Paulis. Write `QP=ωR` for a canonical Hermitian Pauli `R`, with `|ω|=1`. For `|z|<=M`, define

`E_z(X)=z(PXQ-{QP,X}/2)+z*(QXP-{PQ,X}/2)`.

The fixed floor `F=M(D[P]+D[Q]+D[R])` gives coefficient block `[[M,z],[z*,M]]` on `P,Q`, coefficient `M` on `R`, scalar intensity `3M`, and residual `b_R=-Re(zω)=-a`. Thus the minimum rate is `3M+a²/M<=4M`.

Writing `z=t exp(iθ)`, the source's four unnormalized Kraus operators are

`K_+=sqrt((M+t)/2)(P+exp(-iθ)Q)`,

`K_-=sqrt((M-t)/2)(P-exp(-iθ)Q)`,

`K_R=sqrt(M)R-a I/sqrt(M)`, `K_0=sqrt(M-a²/M)I`.

The first two adjoint products sum to `2M I+2aR`; the last two sum to `2M I-2aR`. Their total is `4M I`. Their Kraus generator is exactly `F+E_z`. Boundary `|z|=M` and `|a|=M` merely remove zero Kraus operators. There is no hidden invertibility assumption. All supports lie in `supp P∪supp Q`.

**New lower bound.** Fix a channel `N` and a positive rate `Λ` before `z` is chosen. Suppose `N+E_z/Λ` is CPTP for every `|z|<=M`. Then necessarily `Λ>=4M`. Thus the source construction is minimax optimal even if the center is allowed to be any CPTP map, rather than only a Pauli mixture.

To prove this, choose `z=M conj(ω)`. In the orthonormal Choi directions `I,P,Q,R`, `J(E_z)` consists of two disjoint `2×2` off-diagonal blocks: the `P,Q` block has entries of modulus `M`, and the `I,R` block has entries `-M`. Its eigenvalues are `M,M,-M,-M`. For any Hermitian `A` and `X` with `X±A>=0`, testing the positive and negative spectral subspaces of `A` yields

`Tr X>=Tr A_+ +Tr A_-=||A||_1`.

Both signs of the chosen `z` are admissible. Taking `X=J(N)` and `A=J(E_z)/Λ`, and using `Tr J(N)=1`, gives `1>=4M/Λ`.

The source center is

`N=Id+F/(4M)=(Id+Ad_P+Ad_Q+Ad_R)/4`.

It attains the bound. The lower witness also has ordinary unhalved diamond norm exactly `4M`: normalized Choi trace norm gives the lower bound and the termwise multiplication norm bound gives the upper bound. This is a coefficient-disk minimax theorem, rather than an arbitrary diamond-ball theorem.

The diagonal-only coefficient class likewise forces `2Σ M_aa`: its extremal signed generator has normalized Choi trace norm `2Σ M_aa`. A single Hamiltonian interval `|h|<=u` with a Pauli dephasing floor forces `min_γ(γ+u²/γ)=2u`. Thus there is no universal factor improvement of the source total bound without exploiting more joint structure. Overlap among product labels can improve particular aggregated families; separate edges need not attain their separate lower bounds simultaneously.

## 4. Actual correction jumps: exact fixed-floor minimax synthesis

This section uses the actual projector structure, rather than inserting an unrelated sparse error.

For one completed pair correction let

`Π=(I-S)(I-T)/4`, `A=QΠ`, `Πbar=I-Π`,

`C_0(X)=AXA†+Πbar X Πbar`.

Here `S,T` are the two independent commuting edge checks and `Q` is the correcting single-face Pauli, anticommuting with both checks. The support is the union of two six-face checks sharing the written face, hence 11 qubits. The nominal term is `κ(C_0-Id)`; its inactive dissipator is retained.

Let `P_1,...,P_m`, `1<=m<=3`, be selected single-face Pauli axes. They anticommute pairwise. For any real unit vector `u∈R^m`, `P(u)=Σ_j u_j P_j` is a Hermitian unitary. Define actual unitary action errors

`A_{θ,u}=exp(-iθP(u))A`, `|θ|<=θ_0`,

`C_{θ,u}(X)=A_{θ,u}X A_{θ,u}†+Πbar X Πbar`,

`E_{θ,u}=κ(C_{θ,u}-C_0)=κ(D[A_{θ,u}]-D[A])`.

These are actual differences of correction generators. They include coherent interference and can be non-Lindblad as isolated differences. Nevertheless `A_{θ,u}†A_{θ,u}=Π`, so the active jump intensity is unchanged. No identity-component gauge convention is needed in the channel derivation.

Put `B_j=-iP_j A`. Then

`A_{θ,u}=cos θ A+sin θ Σ_j u_j B_j`.

Each channel `C_j(X)=B_j X B_j†+Πbar X Πbar` is CPTP on the same 11-qubit patch. For all three axes, one action may be a conditional do-nothing action and the others may change both CSS syndromes; they are charged as arbitrary local fault proposals, not as correct ideal actions.

### Theorem: exact optimal fixed clock rate for this physical family

Assume `θ_0>=0`. Define `θ_c=arctan(1/sqrt(m))`. For `0<θ_0<=θ_c`, put

`q_0=sin²θ_0`, `t_0=sin θ_0 cos θ_0`,

`α=κ(q_0+sqrt(m)t_0)`,

`β=κ(t_0/sqrt(m)-q_0)`,

`Λ=α+mβ=κ(2sqrt(m)t_0-(m-1)q_0)`.

For `θ_0>=θ_c`, use `α=κ`, `β=0`, `Λ=κ`. At `θ_0=0`, omit the zero generator and zero floor.

Install the fixed floor

`F=α(C_0-Id)+βΣ_j(C_j-Id)`.

Then for every admitted `θ,u`,

`F+E_{θ,u}=Λ(Ψ_{θ,u}-Id)`

with `Ψ_{θ,u}` CPTP on the same 11-qubit patch. Neither `F` nor `Λ` depends on the unknown error. Moreover **no fixed CPTP center at a smaller rate can absorb every error in this physical family**. Formally,

`inf {λ>0: exists CPTP N, N+E_{θ,u}/λ CPTP for all |θ|<=θ_0,u} = Λ`.

For `m=3`, the small-angle rate is `Λ=2sqrt(3)κθ_0-2κθ_0²+O(κθ_0³)`. For a fixed known axis, `m=1`, the rate is `κ sin(2θ_0)` until `θ_0=π/4`, after which it is `κ`.

#### Constructive proof

For the small-angle branch, `β>=0` follows from `tan θ_0<=1/sqrt(m)`. Define

`N=(αC_0+βΣ_j C_j)/Λ`.

This is a fixed CPTP map and `F=Λ(N-Id)`. The active part of `ΛΨ_{θ,u}=ΛN+E_{θ,u}` has coefficient matrix, on the displayed jump family `A,B_1,...,B_m`,

`T_{θ,u}=diag(α,βI_m)+κ(w w^T-e_0 e_0^T)`,

`w=(cos θ,sin θ u)`.

The inactive Kraus coefficient is `Λ`. On directions perpendicular to `u`, the active matrix has eigenvalue `β`. On `span{e_0,u}`, with `q=sin²θ`, it is

`[[α-κq, κ sin θ cos θ],[κ sin θ cos θ, β+κq]]`.

Its determinant is

`αβ+κq(α-β-κ)=κ(q_0-q)(κ+β-α)`.

At the endpoint `q_0` this is zero. On `0<=q_0<=1/(m+1)`,

`α-β-κ=κ[2q_0+(m-1)t_0/sqrt(m)-1]<=0`.

The bracket increases from `-1` to zero on that interval. Hence the determinant is nonnegative for `q<=q_0`. Both diagonal entries are nonnegative. Thus `T_{θ,u}>=0`.

Diagonalize this matrix into active Kraus combinations. Because `C_j` and `C_{θ,u}` are trace preserving, the resulting map plus the inactive term is trace preserving. Equivalently, the cross adjoint products cancel: `A†B_j+B_j†A=0`, and the pairwise anticommutation of the `P_j` makes real symmetric off-diagonal `B_j,B_k` terms cancel. Therefore the proposal uses at most `m+2` Kraus operators, including `Πbar`; for one axis it uses at most three, and for all three at most five. Singular endpoint matrices cause no problem.

For the large-angle branch, `N=C_0`, `Λ=κ`, and `N+E_{θ,u}/κ=C_{θ,u}` directly.

#### Minimax proof against every fixed CPTP center

Restrict the input to the active subspace `Π`, of dimension `r=d/4`, and use the maximally entangled vector normalized on that subspace. Write `|a>,|b_j>` for the Choi vectors of `A,B_j` on that input. They have unit norm. They are mutually orthogonal:

`<a,b_j>=-i Tr(ΠQ†P_jQ)/r=0`,

`<b_j,b_k>=Tr(ΠQ†P_jP_kQ)/r=δ_jk`.

For the actual 11-qubit pair checks, `Π` has Pauli support `{I,S,T,ST}` and none of `P_j` or `P_jP_k` is one of those nonidentity stabilizer products. This proves the trace equalities without a dimension assumption or dense-matrix computation.

Suppose a fixed channel `N` and rate `λ` absorb the entire family. Project the normalized Choi matrix of its restricted-input channel onto `span{a,b_1,...,b_m}`. Let the projected matrix be `X`. Then `X>=0` and `Tr X<=1`. In this subspace,

`J_r(E_{θ,u})=κ(w w^T-e_0e_0^T)`.

Thus `D=λX` must satisfy `D+κ(w w^T-e_0e_0^T)>=0` for all admitted `θ,u`, with `Tr D<=λ`.

Average `D` over sign changes and permutations of the `b_j` coordinates. The uncertainty family is invariant under those transformations, so the averaged matrix remains feasible and has the same trace. It is `diag(a,bI_m)`, with `a,b>=0`. The endpoint two-dimensional block requires

`a>=κq_0 + κ²q_0(1-q_0)/(b+κq_0)`.

Therefore

`λ>=a+mb >= inf_{b>=0} [mb+κq_0+κ²q_0(1-q_0)/(b+κq_0)]`.

When `q_0<=1/(m+1)`, differentiating this one-variable convex function gives

`b=κ(t_0/sqrt(m)-q_0)`, `a=κ(q_0+sqrt(m)t_0)`.

The minimum is exactly the displayed `Λ`. For a larger uncertainty interval, choose the included angle with `q=1/(m+1)`; it forces `λ>=κ`. The explicit center `C_0` attains `κ`. The lower bound allowed arbitrary output leakage of `N`, arbitrary Kraus rank, and arbitrary correlations on the whole patch; projection and the trace bound already rule out a smaller fixed-rate center.

### Exact norm comparison and limits

For `0<=|θ|<=π/2`, the ordinary unhalved diamond norm is

`||E_{θ,u}||_diamond=2κ|sin θ|`.

The upper bound follows by composing `Ad_{exp(-iθP(u))}-Id` with the trace-nonincreasing CP map `X->AXA†`, whose diamond norm is one. For the matching lower bound, choose a pure state in `Π` whose corrected state has zero expectation of `P(u)`. Such a state exists because the compression of `Q†P(u)Q` to `Π` is Hermitian and has trace zero. The two corrected pure states then have overlap `cos θ` and trace distance `2|sin θ|`.

The uncertainty set is a correlated finite-dimensional manifold of correction differences, not the arbitrary HP, trace-annihilating diamond ball. There is no contradiction with the source `2ν/d²` ball radius. The actual fixed floors above also differ from full-patch depolarization and are charged explicitly.

## 5. A floor invariant under the same common actuator error

The optimum above assumes its added `C_j` channels are implemented as declared. If they inherit the same common unknown single-face postrotation as the active correction, the weighted optimum generally rotates and is no longer the specified fixed floor. The following alternative closes that particular implementation dependence under an explicit shared-error model.

For all three axes, define

`N_av=(C_0+C_1+C_2+C_3)/4`.

Its active part is complete depolarization of the written face applied to `AXA†`; its inactive part is `Πbar X Πbar`. If every active action, including each floor action, is followed by the same arbitrary unitary `U` on that face, then

`(1/4)Σ_{j=0}^3 U A_j X A_j† U† = D_face(AXA†)`,

where `A_0=A`, `A_j=B_j`. Thus the physically averaged floor remains exactly `N_av`. This uses only the Pauli averaging identity and does not estimate the unknown axis or angle.

For `0<=θ_0<=π/2`, install `F_av=ν(N_av-Id)` with

`ν=4κ sin θ_0`.

The active coefficient matrix of `νN_av+E_{θ,u}` is

`(ν/4)I_4+κ(w w^T-e_0e_0^T)`.

The second term has eigenvalues `κ|sin θ|,-κ|sin θ|,0,0`. Consequently it is positive for every admitted error. The proposal `N_av+E_{θ,u}/ν` is CPTP, with the same 11-qubit support. The installed floor can be realized by four completed conditional Pauli-action streams at rate `ν/4`; their common postrotation cancels in the average.

This costs a rate `4κθ_0+O(κθ_0³)` near zero, versus the optimal `2sqrt(3)κθ_0+O(κθ_0²)`. No optimality claim is made for the extra invariant-floor constraint. The shared postrotation assumption must be acquired from the apparatus; command-dependent rotations, faulty predicates, leakage, and faulty inactive branches are outside this result.

## 6. General bounded action-amplitude errors and Pauli cost

A second direct bridge to actual correction generators is available without the unitary constraint. Suppose the jump is `sqrt(κ)(A+δ)` and the declared perturbation has full Pauli coefficient one-norm `||δ||_{P,1}<=ε`. The ideal `A=QΠ` has exactly four Pauli terms of magnitude `1/4`, so `||A||_{P,1}=1`, despite its 11-qubit support.

Write `δ=aI+δ_0`, `t=||δ_0||_{P,1}`, `|a|+t<=ε`. Since `A` is traceless, the traceless coefficient difference satisfies

`Σ_ab |C_ab| <= κ(2t+t²)`.

Removing the identity component changes the Hamiltonian by

`H_a=(iκ/2)[a*(A+δ_0)-a(A+δ_0)†]`,

and its Pauli coefficient norm is at most `κ|a|(1+t)`. The fixed signed compiler therefore gives, for coefficient bounds with that total budget,

`Λ<=2κ[2t+t²+|a|(1+t)]<=4κε+2κε²`.

The last inequality follows by maximizing at `t=ε`. For a specific uncertainty set, install coefficientwise bounds first; an aggregate norm promise alone does not determine a sparse fixed pattern. This is a uniform ceiling when the known coefficientwise bounds have total error amplitude budget `ε`.

For a hardware action error `(Q+Δ)Π` with `Δ` supported on `k` qubits and `||Δ||_op<=ε_op`, normalized Parseval and Cauchy–Schwarz give the per-instance inequality `||Δ||_{P,1}<=2^k ε_op`. Multiplication by `Π` has coefficient norm one. This is not automatically a fixed-box budget: with no finer information, bounding each of the `4^k` coefficients separately by `ε_op` produces a fixed coefficientwise budget `4^k ε_op`. One must not sum separately attained coordinatewise maxima as if they had aggregate budget `2^k ε_op`. A known sparse hardware expansion can provide the smaller coefficientwise budget directly. In either case, a single-face action interface avoids converting an arbitrary operator on the full 11-qubit star. All resulting Pauli labels lie inside the correction star union the declared hardware-error support. This does not treat arbitrary projector errors or unrestricted patch perturbations as sparse.

## 7. Overlapping supports and the conditional memory interface

Independent clocks remain an exact generator sum when their supports overlap and their channels do not commute. On a finite lattice, the superposition of independent Poisson clocks with marked channels gives the ordered semigroup expansion. No Trotter approximation or simultaneous diagonalization is involved.

Rates, however, must be charged at the guard level. For a physical plaquette in the primal sector, its four boundary edges each appear in three outgoing pair predicates at their edge-origin vertex. The two edges sharing the plaquette's lower corner produce one duplicate pair. The other origins are distinct. Therefore it lies in exactly `4·3-1=11` primal correction supports. Duality gives another 11, for 22 in both sectors. A periodic side-five enumeration checks this exact incidence; the counting proof is independent of that finite test for sufficiently large tori.

For a uniform rate `Λ` per pair, the added proposal rate is `12Λ` per vertex owner cell over both CSS sectors and at most `22Λ` incident to one physical face. For a face set `G`, a simple guard bound is `Σ_{events meeting G} rate <=22Λ |G|`; double counting only enlarges this bound. Patch-boundary boxes and the coarse primitive guard must still be enlarged by the fixed geometric support radius.

The new floors and proposals in Sections 4–5 have exactly the original pair patch support. Thus the source's completed-pair theorem can be applied conditionally if these charged local rates fit its qualitative ceiling. The physical generator is

`Σ_pairs {κ(C_0-Id)+F_pair+κ(D[A_actual]-D[A])}`

`=Σ_pairs {κ(C_0-Id)+Λ_pair(Ψ_pair-Id)}`.

Its good ideal clocks are retained with rate `κ`; all floor/error contributions are conservatively counted as rare arbitrary local fault proposals. The source's simultaneous Kraus-span argument then has the correct clock/location-only input. The theorem's envelope, guard forcing, LSS, HT, stopped replay, accumulated homology, ideal encoding and decoding remain imported obligations. This synthesis does not verify those global obligations.

It cannot be transferred to the active-only generator by deleting the inactive dissipator. It also cannot be applied when the new floors are merely mathematical terms without implementation. A bounded-body catalog without a bounded geometric diameter is insufficient: a weight-two pair joining sites at distance proportional to `L` requires a growing guard and falls outside the fixed-range premise.

## 8. Relation to the arbitrary diamond-ball obstruction

For fixed channel `N` and rate `ν`, the largest universal HP, trace-annihilating diamond ball that can be absorbed by `N+E/ν` is at most `2ν/d²`; depolarization attains that value. Its proof uses an orthonormal Weyl Choi basis and channel differences of diamond norm two. The factor-two sufficiency uses `Tr J(E)=0`, which gives `||J(E)||_op<=||J(E)||_1/2`.

That result fixes both a full uncertainty ball and a fixed affine rate. Our edge minimax fixes a coefficient disk. Our actual-correction minimax fixes a jointly constrained unitary-action family and allows a floor adapted to its known projector and action structure. The dimension-independent rates here therefore do not improve the arbitrary-ball theorem. Conversely the arbitrary-ball minimax is not a lower bound on these structured rates or on the robustness of every quantum memory architecture.

## 9. Verification scope and prior boundary

`independent_checks.py` reconstructs the gauge and edge maps independently, tests 48 signed coefficient samples with one fixed floor, tests 360 actual correction error instances across one/two/three axes and singular endpoints, checks the common-rotation floor identity, and enumerates overlapping geometric support incidence. The three-qubit dense representation preserves the two-check local algebra; actual 11-qubit trace orthogonality is checked symbolically from Pauli supports. All general statements above rest on the displayed proofs.

Choi positivity, singular Schur complements, Lindblad gauge freedom, convex channel mixing, Pauli averaging, and robust conic-center optimization are standard machinery. The exact rates and construction above are independent derivations in this session. Limited primary searching found nearby general channel robustness and coherent-control analyses, without establishing whether this precise conditional-action minimax formula has appeared before. Historical originality remains UNKNOWN; see `PRIOR_NOTES.md`.
