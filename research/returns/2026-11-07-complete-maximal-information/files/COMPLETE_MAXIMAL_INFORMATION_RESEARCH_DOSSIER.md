# Complete maximal-information profiles and canonical channels

Research dossier • 6 November 2026 • N1690, N1698 and their current research family

## 1. Result of this round

The strongest structural extension proved here is an **exact-versus-approximate greatest-channel trichotomy for infinite quantum output**. In the faithful tracial setting, approximate greatest members exist exactly when the invariant algebra is injective/hyperfinite (Theorem B). Noninjective algebras forbid even a common pointwise dominating sequence; an explicit free-group channel realizes this obstruction. This is stronger than the sufficient-filtration result with which the investigation began. The companion exact-existence criterion is as follows. For a finite-input channel whose normalized-output invariant has a faithful **tracial** state, a greatest representative with a separable density-operator output exists exactly when its generated von Neumann algebra is a countable product of finite matrix factors. This recovers the tracial finite case and gives explicit faithful binary channels with **no greatest quantum representative**. The restriction to density-operator outputs matters: a diffuse classical reverse experiment can still exist in the broader von Neumann-algebra category. The atomicity obstruction has substantial predecessors; the proof below identifies the additional bridge from complete-profile greatestness to that obstruction.

The strongest finite-dimensional counterexample is independently constructed and exactly checked. Rational qubit-to-four-dimensional channels retain a fixed identity output and a common strictly positive Choi floor while their greatest-profile quantum-capacity ceiling jumps from at least **25/64 bits** to **zero**. A one-shot entanglement-fidelity ceiling jumps from **29/32** to at most **3/4**. Acquiring which ceiling applies requires order **t⁻²** physical channel uses along the explicit perturbation line, even with adaptive quantum experiments. This obstruction is inside full Choi support; it is stronger than a rank-changing example.

Two constructive results remain available despite that obstruction:

1. **Efficient symbolic separation:** inequivalent complete profiles admit faithful rational physical witnesses constructible in deterministic polynomial bit time from explicit rational Choi matrices. This improves the acquired N1698 statement, which guaranteed finite witnesses without a polynomial witness-generation bound.
2. **Approximate operational simulation:** a supplied heralded conversion, combined with offline Choi preparation and established product-resource port-based teleportation, gives an n-use adaptive simulator with polynomial expected primitive-use cost. This is an application of existing machinery, with classical communication, storage, local measurements and precision paid explicitly; it is not a new teleportation theorem or an unassisted capacity increase.

A finite noisy-data repair is also proved: fixed-dimensional profile classes can be separated by a linear number of rational RLD probes after potentially expensive preprocessing. On a quantitative full-algebra generation promise, those probes control channel distance up to output unitaries with a computable Hölder modulus. More general fixed algebra strata admit an explicitly conditioned Lipschitz lift. None of these conditioning promises follows from a Choi floor alone.

**Historical-priority correction.** The additional audit found that the atomic/exact versus injective/approximate structural split already appears in Okamura–Ozawa (2015) for normal extensions of instruments, on top of older injectivity and amenable-trace theory. It cannot be advertised as a new general trichotomy. The proved result here translates it into exact complete-profile membership and universal diamond postprocessing. The possible original contribution is that specific bridge, not a first operational characterization of amenability. No first-in-literature claim is made.

**Not achieved:** a general ordinary quantum-capacity approximation algorithm, a practical quantum communication advantage, an unrestricted noise-stable canonicalizer, or a greatest-realization criterion for arbitrary nontracial infinite-output invariants. Historical priority of the combined extensions is not established.

The complete independent reports, proofs, challenges and executable checks accompany this dossier in [the research record](MAXIMAL_INFORMATION_RESEARCH_RECORD/README.md). This is a research round, not a publication or an external peer review.

## 2. Sources, exact inherited scope and independent checking

The Astra retrieval skill was applied through its local read-only published adapter. All N1690/N1698 continuation pages and current notices were read. The published main revision checked was `c6c7966fa8ebdfb5207d2a11b6648ea95c9ecf3e`; its research input version matched the served immutable source revision `99c8478ff216d6d60a6690f65c36eb19dbc795b5`:

`5e1ce8b083b48e1a5ba57d768f5e4dc802c87938e7ccd312dbe9b008ffb0a5b3`.

The governing visible texts are:

| Governing source | SHA-256 |
|---|---|
| N1690 complete native response | `15feec287a6412d8a524381a4a34b3649ad2e63df7a2c7399eb56f262f18c602` |
| N1698 native prefix, explicitly partial | `dc0d731dbf9067a953ff02475a5765c76a70771e8803852bd1404bb9fd4a8445` |
| N1698 complete rendered response | `5c364abf615b56e212cd3a655dfc6819d9fb59e6d42deef11b4176644a8d27e6` |

Their current content versions and evidence routes are retained in the record. N1690's original detailed 19-page package and N1698's original compiler/proof/certificate package remain unacquired. No historical execution is claimed to have been replayed merely because its source reports completion.

Exactly three independent GPT-6.1 Sol researchers at maximum reasoning investigated machinery, construction and hostile audit alongside the principal. Each saved an initial report before receiving competitors' mathematical results. Source-location/correction updates were shared during independence. The challenge phase then compared the constructions. The finite path-to-moment classification, conditional expectation/Petz lift, rational closure and support padding were independently reconstructed; new explicit certificates were executed locally. The original N1690 general inequality evaluator and held historical capacity certificate remain inherited source-reported results, rather than newly reproduced theorems.

The later notices identify N1708 as existing capital, including full-rank/noisy-qubit finite broadcasting, the all-dimensional support-module criterion, a fixed-source finite-memory normal form and the optimal source-dependent inverse-linear recovery exponent. Their exact statements and acquired visible returns were retrieved. Those results, their qubit capacity spectra, and the Bell-filter approach toward a replacer are **not discoveries of this round**. Fixed-source polynomial work in numerical receiver count is not uniform polynomial work in arbitrary source descriptions; no fixed representative simultaneously broadcasts to every number of receivers.

## 3. Definitions and the best simplified proof of the finite theorem

Use Schrödinger channels E:M_a→M_b and unnormalized, input-first Choi matrices J_E. Compress to the joint output support P=supp E(I). On that support set

\[
 \Omega_E=E(I_a),\quad T_E(X)=\Omega_E^{-1/2}E(X)\Omega_E^{-1/2},
 \quad \mathcal A_E=C^*(T_E(M_a)),\quad
 \tau_E(Z)=a^{-1}\operatorname{Tr}(\Omega_E Z).
\]

T_E is unital CP. The state τ_E is faithful; it generally is **not tracial**. For every finite untouched reference R, faithful density ρ_AR and traceless Hermitian H_AR, define

\[
 g_E(\rho,H)=\operatorname{Tr}
 [E_R(H)E_R(\rho)^{-1}E_R(H)],\qquad E_R=E\otimes\mathrm{id}_R.
\]

The inverse is on P⊗R. Faithful ρ gives E_R(ρ)≥λ_min(ρ)Ω_E⊗I, so this support is exact. Complete profile equality means equality of these numbers for **all** such tests, not optimization over a channel's input, and not comparison with an external output state.

### 3.1 Physical tests recover ordered moments

Choose a rational Hermitian input basis with norm at most one. For a word i₁…iₙ use a reference path of r=n+1 vertices and edges A_j=|j−1⟩⟨j|+|j⟩⟨j−1|. Put

\[
 \rho_t=(I-t\sum_{j=1}^n H_{i_j}\otimes A_j)/(ar),
 \quad Q_E(t)=I-t\sum_jT_E(H_{i_j})\otimes A_j.
\]

For 0<t≤1/(2n), ρ_t≥I/(2ar). For a rank-one reference projector D, the tangent H_D=I_a⊗D−aρ_t has trace zero. Direct multiplication inside the ordinary full matrix trace gives

\[
 g_E(\rho_t,I\otimes D)
 =a^2r\operatorname{Tr}_R
 [D(\tau_E\otimes\mathrm{id})(Q_E(t)^{-1})].
\]

Centering subtracts exactly a², independently of E. The four projectors onto e₀, eₙ, (e₀+eₙ)/√2 and (e₀+i eₙ)/√2 recover the real and imaginary parts of the endpoint resolvent entry. Its first possible nonzero Taylor coefficient, at tⁿ, is

\[
 \tau_E[T_E(H_{i_1})\cdots T_E(H_{i_n})].
\]

There is exactly one shortest path from vertex 0 to vertex n. This preserves multiplication order even though all path parameters equal t. Complex reference tests are essential; τ is never moved cyclically through a product.

Equal ordered moments identify the labelled *-algebras: if a *-polynomial p vanishes in one representation, its faithful expectation of p* p is zero, hence it vanishes in the other. The resulting isomorphism θ obeys θT_E=T_F and τ_Fθ=τ_E. Conversely it preserves amplified inverses and functional calculus. Invertible congruence of maximal perspectives then gives equality of the full reference-valued perspectives, including all covered maximal f-divergences. Tensor products carry the product invariant, so the corresponding all-block equality follows.

### 3.2 Greatest and smallest representative

Let Π_E be the ordinary-trace conditional expectation onto A_E and Z_E=Π_E(Ω_E). Then

\[
 \Gamma_E(X)=Z_E^{1/2}T_E(X)Z_E^{1/2}
\]

is CPTP, has the same invariant, and is converted back to E by

\[
 R_E(Y)=\Omega_E^{1/2}Z_E^{-1/2}\Pi_E(Y)
 Z_E^{-1/2}\Omega_E^{1/2}.
\]

The adjoint effect is Π_E(Z_E⁻¹/²Ω_E Z_E⁻¹/²)=I by bimodularity. On Γ_E(X) the expectation fixes the middle algebra element, giving R_EΓ_E=E. This is the established Petz transpose mechanism applied to **new lifted outputs**, not a recovery theorem for the ordinary coarse-grained original outputs.

Intrinsically write A₀=⊕_jM_nj with one copy of each simple block and let h>0 represent aτ under the multiplicity-one trace. The channel Γ₀(X)=h¹/²T₀(X)h¹/² is greatest and has minimum output dimension ∑_j n_j. Every class member is

\[
 F(X)=\Omega_F^{1/2}\pi(T_0(X))\Omega_F^{1/2},\qquad
 \operatorname{Tr}[\Omega_F\pi(A)]=\operatorname{Tr}(hA),
\]

for a faithful finite representation π. Block pinching, conjugation by h⁻¹/², π and conjugation by Ω_F¹/² give a CPTP simulator from Γ₀. Each faithful representation contains each simple block, proving minimality. This parameterization is an elementary consequence of the earlier classification, not a newly discovered recovery principle.

For rational Choi input, avoid square roots in the equality algorithm: raw multiplication is B⋆C=BΩ_E⁺C, with identity Ω_E. Retain actual paired words using breadth-first **right multiplication by one generator**. The paired span has dimension at most

\[
 N=(\operatorname{rank}\Omega_E)^2+(\operatorname{rank}\Omega_F)^2,
\]

and stabilizes at word length at most N−1. Equality is the vanishing of (Tr B−Tr C)/a on that basis. This is familiar finite linear-closure/weighted-automaton machinery. Arbitrary products of long retained words would not by themselves prove a polynomial bit bound.

The rational raw Gram projection yields K_E>0 and a rectangular rational C with C*C=K_E. Γ_C=Ad_C E is a greatest CPTP channel. A full-space target converter includes the reset term

\[
 R(Y)=L_{E\to F}(C^+YC^{+*})+
 \operatorname{Tr}[(I-CC^+)Y]F(I_a/a).
\]

Its effect is I. Omitting this term would leave a trace defect outside the support. C is generally not a deterministic physical filter on an existing device. The compiler synthesizes a new channel from its complete description; existing-device conversion requires a success instrument with an explicitly paid probability.

## 4. Polynomial-bit faithful physical witnesses

**Theorem W.** Given explicit rational-complex CPTP Choi matrices E,F with the same input, there is a deterministic polynomial-bit algorithm that either certifies equality of complete maximal/RLD profiles, or returns faithful rational states ρ,σ on A⊗R, dim R≤N, and an exact nonzero rational difference of their maximal quadratic divergences. It also supplies a positive rational margin with polynomial encoding length. This is an inequivalence witness; it need not certify failure in a specified direction of the complete order.

**Proof.** The closure algorithm returns a differing word of length 1≤n≤N−1. Let d be a nonzero real or imaginary component of its normalized moment difference and r=n+1. Define the path pencil above with

\[
 t=\min\{1/(2n),\ |d|/(8n^{n+1})\}.
\]

The selected component of the endpoint resolvent difference is d tⁿ plus a tail bounded by

\[
 2\sum_{m=n+1}^\infty(nt)^m
 \le4n^{n+1}t^{n+1}\le|d|t^n/2.
\]

At least one of the four projector expectations has magnitude at least |d|tⁿ/4. Its centered RLD gap is therefore at least a²r|d|tⁿ/4. Set s=1/(8ar) and σ=ρ_t+sH_D. Since ||H_D||<2, σ≥I/(4ar); ρ_t≥I/(2ar). For f₂(x)=(x−1)²,

\[
 \widehat D_{f_2}(E_R\sigma\Vert E_R\rho_t)=s^2g_E(\rho_t,H_D),
\]

so the absolute divergence gap is at least |d|tⁿ/(256r)>0.

All inverses are rational after adding the rational support-complement projector to output baselines. Short words, rank calculations, t, σ and exact matrix inversions have polynomial bit length and complexity in the explicit input. An independent alternative avoids the tail estimate: each scalar univariate gap has a numerator of degree at most r(b_E+b_F); evaluating the four projectors at one more than that many rational t values guarantees a nonzero value. Both routes have polynomial bit complexity. ∎

The guarantee is stronger than the acquired N1698 finite-grid witness scope. The gap can be exponentially small in numerical size; the theorem gives neither polynomial samples nor a free physical divergence oracle.

### Worked reference-necessity example

Let E(X)=X/4+3Tr(X)I₂/8 and F(X)=E(X)^T. They are rational qubit channels, with Choi eigenvalues respectively {7/8,3/8,3/8,3/8} and {5/8,5/8,5/8,1/8}. Every unreferenced maximal perspective agrees by transpose covariance and trace invariance. Nevertheless the normalized ordered XYZ moments are ±i/64. A four-level untouched reference, path parameter t=1/16 and the imaginary endpoint projector give

\[
 g_E=49924/4159,\qquad g_F=48388/4031,
 \qquad g_E-g_F=-2048/16764929.
\]

The exact script checks the faithful baseline and centered tangent. The example explains why scalar unreferenced geometry cannot substitute for complete geometry. It is not a capacity separation.

## 5. Linear-count finite probes and the noisy-data repair

**Theorem P.** Fix a,b≥2 and rational λ>0. Let X_λ be the compact set of CPTP channels M_a→M_b with E(I)≥λI. Put m=a²(b²−1). There is an effectively constructible list of **2m+1 rational faithful RLD probes**, all with untouched reference dimension r=2b², such that two channels in X_λ have equal probe values exactly when their complete profiles agree. No polynomial bound on preprocessing, coefficient size or experimental precision is asserted.

**Proof.** A finite explicit equality predicate is already available: use every word of length at most L=2b²−1, the univariate path pencil, four endpoint projectors and D+1 rational parameters, D=2br, in a fixed faithful interval. Clearing the two baseline determinants gives degree at most D, so these probes imply equality of every retained moment.

Now parameterize one probe by its faithful trace-one baseline and traceless Hermitian tangent in an open rational box around the maximally mixed baseline. For every inequivalent pair E,F, its probe-gap function is analytic, rational and not identically zero on this connected physical domain: the bounded-reference equality predicate supplies a nonzero test somewhere, and analytic continuation brings nonzeroness into the box. Each zero fiber has codimension at least one. Smaller path references may be padded with isolated vertices to this fixed r without losing the nonzero endpoint coefficient. For k probes the incidence set of inequivalent channel pairs and k simultaneous zero gaps has dimension at most 2m+k(d−1), where d is the probe-parameter dimension. If k>2m, its projection has dimension less than kd. Outside its closure every tuple separates all pairs. This is the established generic-identification mechanism behind Sontag's 2m+1-experiment theorem.

All sets are semialgebraic; the complement contains a rational point. Enumerating rational tuples and using exact real quantifier elimination on the universal separating property terminates. This earns rational physical probes without claiming efficient preprocessing. ∎

For words w of length at most b²−1, including the empty word, form the normalized word matrix V_E with columns vec w(T_E(H)). For fixed rational κ>0 impose the additional **generation margin** V_EV_E*≥κI. Together with Ω≥λI this defines a compact semialgebraic set K_(λ,κ) of full-algebra channels.

**Theorem S.** For a separating probe list on X_λ there are effectively computable C>0 and integer q≥1 such that, for E,F∈K_(λ,κ),

\[
 \min_{U\in U(b)}\|F-\operatorname{Ad}_U E\|_\diamond
 \le\sqrt{ab}\,[C\max_j|g_E(\rho_j,H_j)-g_F(\rho_j,H_j)|]^{1/q}.
\]

**Proof.** The minimum unitary-orbit Frobenius distance between the unnormalized Choi matrices is continuous and semialgebraic. The probe gap is also continuous and semialgebraic, since outputs of faithful baselines have a positive floor. Zero gap implies a labelled state-preserving isomorphism M_b→M_b, which is inner; the faithful-state identity then identifies Ω as well. Thus zero gap implies zero unitary-orbit distance. Basu–Mohammad-Nezhad, Theorem 2.2, applies on K² and gives d^q≤Cf. All hypotheses have now been earned. Quantifier elimination and enumeration of dyadic C, integer q compute some valid constants. Finally ||L||_diamond≤||J_L||₁≤√(ab)||J_L||_F. ∎

This is a reusable finite noisy-profile identification theorem **up to an output unitary**. From measurements accurate to δ, semialgebraic feasibility supplies a candidate in K whose error obeys the bound with 2δ. It does not identify a physical output basis or establish polynomial sample complexity. Basu–Mohammad-Nezhad explicitly warn that the constant C cannot be controlled from degree and dimension alone.

On a proper fixed algebra stratum one can instead choose a common word basis and lower-bound its smallest singular value. Then Π_E=V_EV_E⁺, Z_E=Π_EΩ_E and Z_E¹/²Ω_E⁻¹/² vary Lipschitz-continuously with explicitly conditioned constants. The full derivation is in the hostile challenge report. A fixed-rank promise is essential; extending these formulas across a rank change is invalid.

## 6. Exact full-support instability and physical acquisition

### Theorem D: fixed fixture and quantitative conclusions

Let `E ~ F` mean equality of N1698's complete RLD profiles: same input space,
all finite untouched references, faithful baselines, traceless Hermitian
tangents. Equivalently these are complete maximal-perspective profiles, with
both arguments passed through the same channel. For qubit-input channels put

\[
 f_*(E)=\sup_{F\sim E,\ D:F_{out}\to M_2\ CPTP}
 \langle\phi_2|({\rm id}\otimes DF)(\phi_2)|\phi_2\rangle,
 \qquad Q_*(E)=\sup_{F\sim E}Q(F).
\]

There is an explicit rational affine family `E_t:M_2 -> M_4` such that, for
every real `0<t<=1/65536`,

\[
 \|E_t-E_0\|_\diamond\le2t,\quad
 E_t(I_2)=\Omega=\operatorname{diag}(25,1,1,1)/14,\quad
 J_{E_t}\succeq I_8/448.
\]

Choi matrices here are unnormalised and input-first. Every `E_t`, including
`E_0`, is antidegradable and has `Q(E_t)=0`. Nevertheless:

1. `E_0` has exactly the profile of
   `Delta(X)=(7/8)X+(Tr X)I_2/16`. The latter is greatest in the class and its
   minimum output dimension is two.
2. For every `0<t<1`, the normalized output algebra of `E_t` is `M_4`.
   Consequently `E_t` itself is a minimum-dimensional greatest representative.
3. The class ceilings obey
   \[
   f_*(E_0)=29/32,\quad f_*(E_t)\le3/4,\qquad
   Q_*(E_0)\ge25/64,\quad Q_*(E_t)=0.
   \]
4. For deterministic output deficiency
   `delta(A,B)=inf_R ||B-RA||_diamond`,
   \[
   \delta(E_t,\Delta)\ge5/16,\qquad \delta(\Delta,E_t)\le2t.
   \]
   Hence **no selection** of greatest class representatives is continuous in
   mutual deterministic-simulation distance. This statement does not require
   comparing matrices of different output dimensions directly.
5. Any physical `N`-query procedure distinguishing `E_0` and `E_t` with average
   success at least `2/3`, allowing arbitrary ancillas and adaptive quantum
   operations, has
   \[
   N\ge\frac{\ln(13/9)}{\ln(1+(512t)^2)}.
   \]
   Thus for `t=2^-m`, `m>=16`, `N>2^(2m-20)`. A uniform additive estimate of
   `f_*` with error strictly below `5/64` and success at least `2/3` would give
   such a procedure.

The construction extends parametrically: for every positive rational `epsilon`
there is a rational `2 -> 4` fixture and a rational sequence `E_j -> E_0`, with
fixed `E_j(I)` and one common positive Choi floor, for which
`Q_*(E_0)>1-epsilon` and `Q_*(E_j)=0`. The floor may depend on `epsilon`; it
does not decrease along the sequence for a fixed fixture.

**Status:** proved below; exact fixed-fixture checks executed. Historical novelty
is not established. Instability of exact algebra decompositions is not itself new.


The construction and analytic proof follow. These new exact matrix checks were independently replayed by the principal and hostile reviewer; they do not rely on the held N1690 certificate.

### Rational interior antidegradable seed

Let `sigma_0=I,sigma_1=X,sigma_2=Y,sigma_3=Z`, `q=(5,1,1,1)`, and

\[
 [E_0(X)]_{jk}=\frac{q_jq_k}{28}
       \operatorname{Tr}[\sigma_j\Delta(X)\sigma_k]. \tag{3.1}
\]

For CP/TP and the profile identity, write in the Bell tensor representation
`P=|phi_2><phi_2|`, `S=I_4/4+P`, `kappa=7/8`. Up to the Bell-basis unitary,

\[
 E_0(X)=\kappa^{-1}S(\Delta(X)\otimes I_2)S. \tag{3.2}
\]

All entries of (3.1) are rational-complex. Equation (3.2) is CP and
`Tr_aux S^2=kappa I_2` proves TP. Since `J_Delta>=I_4/16` and `S>=I_4/4`,
`J_E0>=I_8/224`. Its identity output is `diag(25,1,1,1)/14`.

Invertible-congruence covariance of the maximal perspective and
`Tr_aux(S^2/kappa)=I_2` prove reference-valued perspective equality for every
finite untouched reference. Thus `E_0~Delta` directly. The normalized map is
left multiplication by `Delta(X)` on the Pauli matrix basis, so its algebra
is `M_2` with multiplicity two. Since `A_Delta=M_2`, Section 3 proves `Delta`
greatest in that class.

#### Full-space symmetric extension certificate

Put `V=(X^T,Y^T,Z^T)^T`, so `V*V=3I_2`, and `nu=1/1024`. In output-first
order define the `8 x 8` matrix

\[
 H=\begin{pmatrix}aI_2&bV^*\\bV&qI_6+rVV^*\end{pmatrix},\qquad
 a=\frac{11271}{14336},\quad q=\frac{121}{28672},\quad
 r=\frac1{32},\quad b=\frac5{32}.
\]

It is positive definite: on `range(V)^perp` the lower block is `qI`; on its
range the strict Schur determinant is

\[
 a(q+3r)-3b^2=\frac{1554639}{411041792}>0.
\]

Let `W:C^4 -> C^4 tensor C^4` be rational with
`W|0>=|00>`, `W|j>=|0j>+|j0>`, `j=1,2,3`. After reordering `H` input-first,

\[
 B=(I_2\otimes W)H_{in}(I_2\otimes W)^*+\nu I_{32}/16. \tag{3.3}
\]

Both complete output marginals of `B` equal `J_E0`, the entire four-dimensional
outputs can be swapped, and `B>=I_32/16384`. These exact identities were
executed. The core first subtracts the maximally mixed replacer from the desired
marginal: its top coefficient is `11/14+nu/2`, bottom scalar coefficient
`1/224-nu/4`, while the last term restores both marginals. That padding earns
a **full-dimensional** positive margin; a thin single-excitation extension
alone would not prove an open neighbourhood.

The standard symmetric-extension/dilation argument now proves antidegradability
for the actual complement. It is constructive: choose eight independent
vectorised Kraus columns `T` with `TT*=J_E0` by exact algebraic Cholesky. Then

\[
 J_{\mathcal A}=(T^{-1}\otimes I_4)B(T^{-*}\otimes I_4)
\]

is positive, has output partial trace `I_8`, and the Choi purification identity
gives `A E_0^c=E_0` for that Kraus complement. This is not an assertion that
classical labels constitute the whole environment.

For any CPTP `F`, write `D=J_F-J_E0`, `Tr_C D=0`, and `tau=I_4/4`. The
symmetric correction

\[
 B_F=B+D_{RC_1}\otimes\tau_{C_2}+D_{RC_2}\otimes\tau_{C_1}
\]

has both marginals `J_F`. Its norm is at most `||D||/2 <= ||F-E_0||_diamond`
(input dimension two). Thus diamond distance at most `1/32768` preserves a
positive extension with floor at least `1/32768`. This supplies an explicitly
proved antidegradable ball without an SDP or a held certificate.

### Fixed-Omega full-algebra perturbation

Keep `Omega=diag(25,1,1,1)/14`. Set

\[
 D_0=\operatorname{diag}(0,1,2,3)-\tfrac3{14}I_4,\qquad
 B_0=\mathbf1\mathbf1^T-I_4.
\]

Both have zero `Omega`-weighted trace. Define `R` on the Pauli basis by

\[
 R(I)=\Omega,\quad R(X)=\tfrac1{16}\Omega^{1/2}B_0\Omega^{1/2},\quad
 R(Z)=\tfrac1{16}\Omega^{1/2}D_0\Omega^{1/2},\quad R(Y)=0.
\]

All entries are rational, since `Omega^(1/2)=diag(5,1,1,1)/sqrt(14)` and
square roots occur in pairs. Weighted traces give TP. The normalized Choi
pencil has floor
`[1-(3+39/14)/16]/2=143/448`, hence `J_R>=143 I_8/6272`.
The normalized `Z` image has distinct diagonal entries; every off-diagonal
entry of the `X` image is nonzero. Their common commutant is scalar, so they
generate `M_4`.

Put `E_t=(1-t)E_0+tR`. Then `Omega` is fixed, `||E_t-E_0||_diamond<=2t`,
and `J_Et>=I/448` for `t<=1/2`. The ball above proves antidegradability for
`t<=1/65536`.

For the full algebra at **all** `0<t<1`, form commutator constraints for
`T_Et(X),T_Et(Z)` on an unknown `4 x 4` matrix. A specified `15 x 15` minor
(indices in `instability_checks.json`) is exactly

\[
 \frac{-1618261995-331887829i}{2^{48}}
 t^5(t-1)^7\left(t-\frac{182+28i}{173}\right)q(t),
\]
\[
 q(t)=t^2+\left(-\frac{46921}{23258}+\frac{441i}{11629}\right)t
                   +\frac{11809-392i}{11629}.
\]

For real `t`, `Im q(t)=0` only at `t=8/9`, where `q=1/81`. The linear root
is nonreal. This exact polynomial is nonzero throughout `(0,1)`, proving
scalar commutant and full `M_4`. The script proves the polynomial identity
and independently checks four small dyadic parameters.

More generally, full normalized algebra is open dense in any full-Choi-rank
CPTP slice with fixed faithful `Omega` and input dimension at least two:
small weighted-trace-zero Hermitian images around a replacer can generate the
full output algebra. Along a line toward that endpoint, a nonzero commutator
minor has degree at most `b^2-1`. There are finitely many exceptional points;
testing `b^2` distinct rational parameters in any small interval finds a full
algebra perturbation. This uses standard finite matrix-algebra genericity,
not a claimed novel generic-algebra theorem.

### Operational discontinuity and acquisition proof

For two equal qubit-output marginals of a symmetric extension let
`P1=phi_RB1 tensor I_B2`, `P2=phi_RB2 tensor I_B1`. The identity
`P1 P2 P1=P1/4` gives `||P1+P2||=3/2`. Hence each singlet fraction is at most
`3/4`. The same deterministic decoder on both copies retains the extension.
This proves the antidegradable postprocessing ceiling. Antidegradability
persists under tensor powers and coding, so no positive ordinary quantum
rate is possible (for target dimension `d>=2`, the corresponding bound is
`(d+1)/(2d)<=3/4`).

The identity decoder for `Delta` gives `29/32`; no decoder improves it, because
the identity component contributes at most one and the replacer component
exactly `1/4`. Section 3 and the full-algebra calculation give the asserted
class ceilings. A singlet-fraction gap `5/32` forces full trace-norm gap at
least `5/16`, proving the deficiency lower bound. Conversely `Delta` simulates
`E_0` by (3.2) and approximates `E_t` within `2t`.

The maximally mixed-input coherent information of `Delta` is
`1-H(29/32,1/32,1/32,1/32)=0.4025452768...`. The coding theorem yields a
capacity lower bound. Using `-(1-x)log_2(1-x)<=x log_2 e` and `log_2 e<3/2`,
the entropy is less than `39/64`; hence `Q(Delta)>25/64`. No exact capacity
evaluation or coding-efficiency claim is made.

#### Adaptive acquisition cost

Let `G=R-E_0`, `s=1/512`. Both `E_+=E_0+sG` and `E_-=E_0-sG` are CPTP.
Indeed `||J_G||<=2` since the positive Choi matrices each have trace two, so
`J_E- >=(1/224-1/256)I=I/1792`. For `|t|<=s`,

\[
 E_t=(\tfrac12+\tfrac{t}{2s})E_+
          +(\tfrac12-\tfrac{t}{2s})E_-.
\]

Every `N`-query adaptive experiment is therefore a fixed quantum operation
on `N` independent classical selector coins. Revealing the coins only helps
discrimination. Against the unbiased coin, the one-copy chi-square divergence
of bias `z=t/s` is `z^2`; for the product it is `(1+z^2)^N-1`.
Cauchy--Schwarz bounds total variation by half its square root. Success `2/3`
requires variation at least `1/3`, which proves
`N>=ln(13/9)/ln(1+(512t)^2)`. For `t=2^-m` the bound
`ln(1+x)<=x`, `ln(13/9)>1/4` gives `N>2^(2m-20)`.

Descriptions have `O(m)` bits at these fixed dimensions; physical acquisition
requires exponentially many uses in that bit length. This covers fully
adaptive quantum acquisition, not merely Choi tomography. It directly rules
out uniformly robust estimation of the canonical ceiling at error below
`5/64`, even with the stated fixed positive rank floors.

### Arbitrarily near-unit capacity ceiling jump

The compact fixture is not a limiting bound. For rational `0<lambda<1`, take
`Delta_lambda(X)=lambda X+(1-lambda)Tr(X)I/2`, rational `u>0`,

\[
 S_u=uI+P,\quad\kappa_u=2u^2+u+1/2,\quad
 E_u=\kappa_u^{-1}\operatorname{Ad}_{S_u}(\Delta_\lambda(\cdot)\otimes I).
\]

In its Bell coordinates set
`p0=(1+u)^2/[(1+u)^2+3u^2]`, `p=u^2/[(1+u)^2+3u^2]`. The single-excitation
extension core has coefficients

\[
 a=p_0-3p,\quad b=\lambda\sqrt{p_0p},\quad q=p(1-\lambda),\quad r=p\lambda.
\]

The square root is rational: `(1+u)u/[(1+u)^2+3u^2]`. The core is strictly
positive whenever

\[
 (p_0-3p)(1+2\lambda)>3p_0\lambda^2.
\]

For every `lambda<1`, sufficiently small rational `u` works because
`1+2lambda-3lambda^2=(1-lambda)(1+3lambda)>0`. Subtract a sufficiently small
rational maximally mixed replacer in the core and restore its full product
extension as in (3.3). Strict positivity persists. Rational halving searches
find `u`, padding and a positive extension floor. The Choi floor is
`(1-lambda)u^2/(2 kappa_u)>0`.

The profile is exactly `Delta_lambda`. Generic rational fixed-`Omega`
perturbations remain inside this antidegradable ball and are themselves
greatest. As `lambda->1`, the canonical depolarizing coherent information
tends to one. This proves the `1-epsilon` ceiling-jump claim. No uniform floor
as `epsilon->0` is asserted. At `lambda=1` the strict Schur condition is
impossible, preserving N1708's unitary/noisy boundary.


### Matching acquisition upper bound and general resource regularization

For the promised pair, sending |0⟩ and measuring the first output coordinate has success probability 25/28−(75/6272)t. Hoeffding sampling therefore distinguishes E₀ from E_t using O(t⁻²) calls at fixed confidence, matching the lower-bound exponent. This is a promised-pair acquisition theorem, not a universal tomography rate.

For any continuous isometry-invariant output-processing monotone M, let C_M(E)=M(Γ_E). On the finite-dimensional full-Choi-rank interior, C_M=M on an open dense full-measure set: full normalized output algebra is generic. The raw-word determinant is nonzero at a rational generating seed, so its exceptional zero set has measure zero. A small generating Hermitian-pair perturbation proves density, even with fixed faithful Ω. This concerns the output-generated algebra, not Perron–Frobenius irreducibility of a channel.

C_M is upper semicontinuous. Along E_n→E, choose concrete greatest lifts in the same original output dimension. A common Ω floor gives a common Z=ΠΩ floor. Compactness and continuity of each fixed faithful RLD probe put any subsequential lift limit in E's profile class, so its resource is at most C_M(E). Continuity of M finishes the argument. Furthermore

\[
 M(E)=\lim_{\epsilon\downarrow0}\inf_{\|F-E\|_\diamond<\epsilon} C_M(F).
\]

Indeed C_M(F)≥M(F) gives the lower inequality by continuity, and dense full-algebra F with C_M(F)=M(F) gives the upper one. For M=Q, Leung–Smith Corollary 14 supplies the needed continuity. This identity does not evaluate Q. The resource that jumps in Theorem D is the optimized exact-profile ceiling; ordinary Q remains continuous.

No uniformly reliable finite-data estimator of this discontinuous ceiling can halt almost surely at the limiting channel: truncate its high-answer event at a sufficiently large finite query count, then use continuity of that finite experiment on a sufficiently close E_t. The argument does not forbid pointwise infinite-data estimators or prove ordinary capacity noncomputable on rational symbolic inputs.

## 7. Strongest structural extension: an infinite-output greatest-realization criterion

The following proofs survived independent challenge of the unbounded-inverse definition, normality, moment reconstruction, atomicity and approximate-dominance steps. It is an extension of the finite theorem, not a claim that the original finite compiler handles infinite descriptions.

### Statement

Let E:M_a -> T(H) be a channel, with finite a>=2 and separable effective output H. Put Omega=E(I), faithful trace-class with TrOmega=a. Define bounded UCP normalized generators T(X) by E(X)=Omega^.5 T(X)Omega^.5. Let M=W*(T(M_a)) and tau(Z)=Tr(Omega Z)/a. Assume tau is TRACIAL on M (faithful normal already follows from Omega). Same complete profile means equality of the referenced maximal/RLD tests, with bounded-normalized-sandwich definitions at faithful input baselines. All comparison channels also have finite input a and separable trace-class output, and postprocessings are normal CPTP Schrödinger maps.

**Theorem T.** The class has a greatest member under deterministic output processing if and only if M is atomic finite type I:
 M is normally *-isomorphic to a finite or countable direct sum/product of finite matrix factors M_(n_j).
Here bounded algebra elements have uniformly bounded blocks (von Neumann direct product), while normal densities/output states live in the trace-norm direct sum. No type-I-infinite block is allowed. The criterion is intrinsic to the profile and does not require a uniform bound on n_j. If M is so atomic, tau=Σ p_j Tr_(n_j)/n_j, with p_j>0,sum p_j=1, and
 Gamma(X)=⊕_j (a p_j/n_j) T_j(X)
is a greatest channel on H0=⊕_j C^(n_j).

For commutative M this becomes precisely the binary theorem's purely-atomic-measure criterion. A diffuse component forbids a greatest trace-class quantum realization, although the generalized operator-algebraic experiment itself can still serve as the appropriate canonical object. This theorem does not address the general nontracial infinite-output case.

### Lemma: profiles classify the normal invariant triple

Physical path pencils from N1698 continue to work because every T(H_i) is bounded and UCP. For small t, I−tΣT(H_i)⊗edge_i>=I/2. The bounded normalized RLD form is
 g_E(rho,H)=Tr[(Omega⊗I) T_R(H) T_R(rho)^(-1) T_R(H)].
No inverse of compactOmega is used in this formula. Polar decomposition of (Omega^.5⊗I)T_R(rho)^.5 identifies it with the usual maximal perspective/closed-form quadratic on the effective output support.

Path-reference tests therefore determine all ordered tau-moments. Conversely moments determine the C*-norm: for a positive B in a C*-algebra with faithful state tau, ||B||=lim_n tau(B^n)^(1/n). To prove lower bound, pick any epsilon>0 and a continuous nonnegative function f supported in [||B||−epsilon,||B||] with f(B)nonzero; faithfulness gives tau(f(B))>0 and the resulting lower moment bound. The upper bound is immediate. Thus equal moments identify kernels AND norms of all evaluated *-polynomials, yielding a state-preserving C*-isomorphism. Its GNS unitary gives a normal *-isomorphism of the generated von Neumann algebras; the given faithful normal representations are normally isomorphic to that GNS realization. Hence the normal triple (M,T,tau) is determined. Conversely such an isomorphism preserves all inverses and continuous functional calculus used for finite referenced baselines, so it preserves the complete profiles.

### Necessity

Take any member G in the class and write its Omega,T,M,tau in its own output representation. Because the invariant state is tracial, for EVERY projection P in M the trace-class density
 Omega_P=P Omega P+(I-P)Omega(I-P)
is faithful and represents exactly the same state on M:
 Tr Omega_P Z=a tau(P Z P+(I-P)Z(I-P))=a tau(Z).
Define G_P(X)=Omega_P^.5 T(X)Omega_P^.5. It is CPTP (state restriction impliesTP), has the same normalized labelled algebra, and has exactly the same complete profiles.

For a selfadjoint input X, B=T(X), the profile determines
 u(X)=Tr Omega |B|=a tau(|B|).
Every member satisfies ||G(X)||_1<=u(X), by splitting B into positive and negative parts. Choose P=1_(0,infinity)(B). Omega_P commutes with this cut; the positive and negative output parts are then orthogonal, so ||G_P(X)||_1=u(X).

If G is greatest, it dominates G_P, and trace-norm contraction under the deterministic simulator forces ||G(X)||_1=u(X) for EVERY selfadjoint X. In particular take X=H_i−t I for each Hermitian basis generator and thresholds t with tau(1_{t}(T(H_i)))=0. Equality in the positive trace-class triangle inequality forces orthogonal positive and negative supports, hence
 (T(H_i)−t)_+ Omega (t−T(H_i))_+=0.
Bounded inverse on epsilon-truncated positive/negative spectral subspaces and a strong limit imply the cross-cut block ofOmega vanishes. Faithfulness removes the equality spectral subspace at these thresholds. Thus Omega commutes with a dense family of spectral cuts of every generator, hence allT(H_i) andM.

Omega has a countable orthogonal decomposition into finite-dimensional positive-eigenvalue spaces H_l spanning H (compactness and faithfulness). Every H_l reduces M because Omega commutesM. Restriction pi_l:M->B(H_l) is a normal finite-dimensional representation; their kernels intersect only at zero. The kernel of each normal representation is a central ideal M(1−z_l), and M z_l is finite-dimensional. The central supports z_l have supremum1. Decomposing their countable union into disjoint central pieces shows M is atomic with finite matrix factors. This conclusion concerns the von Neumann algebra, not a false assertion that its norm-closed C*-subalgebra must be an algebraic direct sum.

### Sufficiency

Suppose M=product_j M_(n_j), tau=Σ p_j tr_(n_j), p_j>0. The given Gamma has trace-one outputs: TrGamma(X)=a tau(T(X))=TrX, and positivity/complete positivity hold blockwise. Its normalized map is the multiplicity-oneT and its state is tau; thus it is in the same profile class.

For any class member F on H_F, let pi:M->W*(T_F(M_a)) be the normal labelled state-preserving isomorphism and Omega_F=F(I). For each finite block define
 R_j(Y)= [n_j/(a p_j)] Omega_F^.5 pi_j(Y) Omega_F^.5,
where pi_j(Y) is zero off the jth intrinsic central summand. Each R_j:M_(n_j)->T(H_F) is CP and trace preserving, since Tr Omega_F pi_j(Y)=(a p_j/n_j)TrY. Define
 R(Y)=Σ_j R_j(P_j Y P_j)
for Y in T(H0), with block pinching. Positive inputs have positive trace-norm-summable terms with total traceTrY; general inputs extend linearly as a contractive CPTP map. Its adjoint is the bounded block-diagonal normal UCP map whose jth block is R_j^*. Thus no unbounded global inverse or infinite norm Kraus matrix is assumed.

On Gamma(X), h_j=a p_j/n_j cancels in each term. Normality of pi and strong sum of central projectors imply
 R Gamma(X)=Omega_F^.5 pi(T(X)) Omega_F^.5=F(X),
with trace-norm convergence of these dominated series. Hence Gamma is greatest.

### Scope, consequences and open operation

This theorem extends the finite greatest-member mechanism to a complete criterion for TRACIAL infinite-output invariants and exhibit diffuse obstructions. It subsumes atomic binary reverse tests and their failure to fit as a greatest normal density-operator output when diffuse. It does not claim that every invariant has tracialtau; the original finite theorem explicitly allows nontracial states. Nor does it claim practical synthesis, efficient tomography of infinitely many matrix blocks, an ordinary quantum-capacity evaluator, or a nontracial general-infinite greatest theorem. The general nontracial infinite case is the decisive remaining operator-algebraic question.

Primary predecessors: faithful noncommutative moment/GNS reconstruction; Matsumoto spectral reverse tests; Hiai maximal divergences and diffuse L-infinity reverse tests; finite atomic normal conditional expectations. Newness of the criterion as a combined statement is not established by its proof.

### Explicit binary channel with no greatest output realization

H=L2([1/4,3/4],nu), nu normalized Lebesgue measure. Let e_n(x)=exp(4pi i n(x-1/4)), n in Z, the Fourier ONB with |e_n(x)|=1. Set
 Omega=sum_(n in Z) (2/3)2^(-|n|)|e_n><e_n|,
 A=M_x.
Omega is positive, faithful, trace class, trace2. For bounded f,
 Tr Omega f(A)=sum c_n int f dnu=2int f dnu.
Thus mu=nu is diffuse with mean1/2. The states rho0=Omega^.5 A Omega^.5 and rho1=Omega^.5(I-A)Omega^.5 are faithful trace-one density operators; each is >=Omega/4 and <=3Omega/4. Their likelihoods are uniformly comparable even though no trace-class state can have an infinite-dimensional uniform eigenvalue floor. The binary channel has no greatest member within its complete profile class.


In the binary case the complete invariant is the measure μ(B)=Tr[Ω1_B(A)]/2, of mean 1/2. Zero RLD for the input Pauli X and Y tangents forces every same-profile channel to kill input coherences. Scalar RLD tests around the uniform input determine all moments of 2A−I, and hence μ. Thus the binary class has a greatest density-operator-output member exactly when μ is purely atomic. Its diagonal outputs are (2μ_j λ_j)_j and (2μ_j(1−λ_j))_j.

Each binary Bayes prior separately has a maximizer: pinch Ω at the corresponding spectral cut of A. With diffuse μ no single density-operator-output channel maximizes all these decision problems. Hiai's normal spectral reverse test does realize the associated generalized classical experiment on L∞(μ); this is an important existing comparator, not a contradiction. The general nontracial infinite-output criterion remains open here.

### Uniform finite operational envelopes under a supplied filtration

**Theorem A.** The supplied-filtration result below is proved and independently checked.

#### Statement

Use Theorem T's finite-input invariant (M,T,tau), tau faithful normal tracial. Assume a supplied increasing sequence of finite-dimensional unital von Neumann subalgebras M_k with union dense in L2(M,tau). Let E_k:M->M_k be the tau-preserving conditional expectations. For each k form the finite full-M_k block lift Lambda_k associated with T_k=E_k T and the restricted tracial state. Use Gamma_k=Lambda_k in the formulas below. T_k need not generate all M_k; this lift is a finite external approximant, not necessarily the minimum greatest member of its own profile class. Alternatively take its actual canonical greatest channel and compose its deterministic simulator to Lambda_k before every displayed R_(k,F). Then for EVERY exact-profile realization F:M_a->T(H_F), there is a normal CPTP R_(k,F) with

 ||F-R_(k,F)Gamma_k||diamond
 <= a sum_(i,j=1)^a ||T(E_ij)-E_kT(E_ij)||_(2,tau).

The bound tends to zero and is UNIFORM over all class members, all separable output spaces and all untouched reference inputs. Gamma_k generally does NOT lie in the exact profile class. Its fixed finite-reference RLD/maximal profiles converge pointwise to the original ones. Output dimensions and rate of convergence depend on the supplied filtration; no universal computability/efficiency or practical synthesis follows.

#### Proof

Write M_k=directsum_j M_(n_kj), tau|M_k=sum_j p_kj tr_nkj. Define h_kj=a p_kj/n_kj and Gamma_k(X)=directsum_j h_kj [E_kT(X)]_j. This is finite CPTP by the same block trace calculation as in TheoremT. For any classmember F, transport M normally into its normalized algebra with pi_F and letOmega_F=F(I). The finite-block channels
 R_j(Y)=h_kj^-1 Omega_F^.5 pi_F(Y_j) Omega_F^.5
are CP and TP because tau restricted to that finite block is p_kj times normalizedtrace. Sum them after block pinching. Their composition with Gamma_k is exactly
 Omega_F^.5 pi_F(E_kT(X)) Omega_F^.5.

For arbitrary B∈M,
 ||Omega_F^.5 pi_F(B) Omega_F^.5||1
 <=||Omega_F^.5 pi_F(B)||2 ||Omega_F^.5||2
 =a [tau(BB*)]^.5=a||B||2tau,
where TRACIALITY is used in the final equality (or use tau(BB*) consistently for the right L2 norm). For any referenced trace-class X=Σ_ij E_ij tensor X_ij with||X||1<=1, each block||X_ij||1<=1. The triangle bound gives at most aΣ_ij||T(Eij)-E_kT(Eij)||2tau. This bound is independent of reference dimension andF. L2 projection convergence gives the limit.

For fixed referenced faithful rho and Hermitian H, S=T_R(rho)>=cI and S_k=(E_k tensor id)S>=cI. The tangentD andD_k are bounded, and S_k->S,D_k->D in finite-reference L2. The resolvent identity S_k^-1-S^-1=S_k^-1(S-S_k)S^-1 gives L2 convergence of inverses, since operator norms are at most1/c. Products with bounded D,D_k converge in L2; the trace tau tensor Tr is continuous in L2. Thus the RLD profiles converge. For continuous maximal perspective functions on the common positive spectral interval, uniformly approximate f by polynomials, use L2 product continuity and the bounded inverse/square-root functional calculus (or uniform polynomial approximation for those functions too). This proves pointwise complete-profile convergence, not a uniform bound over every baseline spectral floor/reference dimension.

#### Binary constructive specialization

For diffuse binary invariant A with measuremu, partition[0,1] into intervals of diameter<=h. For bin j letmu_j>0 andlambda_j be its conditionalmean; the external finiteclassicalchannel has outputs p_j=2mu_jlambda_j,q_j=2mu_j(1-lambda_j). It has at mostceil(1/h)nonemptybins. Every exactclassF is simulated with preparation state sigma_j=Omega_F^.5P_jOmega_F^.5/(2mu_j). Each of its two output errors is<=2h, hence cq diamond error<=2h. Chooseh<=epsilon/2, output countO(1/epsilon). All realmean/measure values must be supplied/computable for an effective compiler; the Fourier uniform example hasexplicit rationalweights/means forrationalbins. This is spectralreverse-test discretization/LeCam approximation, not new general approximation machinery.

#### Exact limitation and constructive next question

This is a strong positive counterpart to the absence of an exact greatest member: a supplied hyperfinite filtration supplies finite external universal envelopes for the entire class. It does not say the finite envelope has exactly the originalprofile (TheoremT forbids that for diffuseM). A generic nontracialstate need not admit the required state-preserving finite-dimensional filtration. The following Theorem B resolves the converse for approximate greatest members inside the exact class. A different converse for arbitrary finite external envelopes is not asserted. Moment microstates alone do not supply normal CP simulators; an embedding/conjecture slogan is not a proof of this bridge.

### Theorem B: exact versus approximate greatest representatives

This closes the converse left open in the preceding external-envelope construction. Retain ALL of Theorem T's assumptions: finite input, separable trace-class outputs, faithful normal TRACIAL invariant state, equality of all finite-reference profiles, and normal CPTP physical postprocessings. Write

\[
 d(G,F)=\inf_R\|F-RG\|_\diamond.
\]

**Theorem B.** The following are equivalent:

1. For every epsilon>0 there is ONE exact-profile member G with sup_(F in the class) d(G,F)<epsilon.
2. There is ONE sequence G_k of exact-profile members with d(G_k,F)->0 for EVERY fixed class member F.
3. M is injective, equivalently hyperfinite in this separable finite tracial setting.

Outputs of G_k may be infinite dimensional. The decoder may depend on k and F. Condition 2 asserts existence of a common pointwise sequence; it does not assert that that particular sequence converges uniformly. No computable filtration, convergence modulus or physical source acquisition follows.

Together with T this is a complete trichotomy:

| Invariant algebra | Realization consequence |
|---|---|
| Countable product of finite matrix blocks | An exact greatest trace-class-output channel exists. |
| Injective but not of that atomic form | No exact greatest channel; arbitrarily accurate greatest members exist inside the exact class. |
| Noninjective | No common sequence can even approach every fixed class target by deterministic processing. |

**Proof of 3 implies 1.** The exact structural import is Connes' injectivity/approximate-finite-dimensionality theorem for von Neumann algebras on separable Hilbert spaces; the original general-center primary theorem and independent checks are recorded below. Adjoin I to each finite-dimensional subalgebra if its original unit is smaller. The filtration is L2(tau)-dense. Haar-average a representing density over U(M_k): Omega^(k)=integral u Omega u*du, a trace-norm Bochner integral. Traciality preserves its restriction to ALL of M, positivity makes it faithful, and Haar invariance makes it commute with M_k. Consequently

 G_k(X)=Omega^(k)^.5 T(X) Omega^(k)^.5

lies in the EXACT original class. Decompose M_k=directsum_j M_nj tensor I_Kj. Its commuting density is directsum_j I_nj tensor omega_j with Tr omega_j=h_j=a p_j/n_j. Normal block partial trace S_k onto directsum M_nj is CPTP. Pairing with Y in M_k gives

 Tr[S_kG_k(X)Y]=a tau(T(X)Y)=a tau(E_kT(X)Y),

so S_kG_k=Lambda_k, the full finite-algebra lift in A. Theorem A's simulators therefore give

\[
 \sup_F d(G_k,F)\le a\sum_{i,j=1}^a
  \|T(E_{ij})-E_kT(E_{ij})\|_{2,\tau}\longrightarrow0.
\]

This proves 1; 1 implies 2 by choosing epsilon_k->0.

**Proof of 2 implies 3.** Fix ONE base representative. For every input generator H_i and a countable dense set of nonatom thresholds t, pinch that BASE density at the corresponding spectral cut. These are fixed targets F_(i,t); their norm at H_i-tI attains a tau|T(H_i)-tI|. Pointwise approximation to those fixed targets gives the deficit limit used in the following argument. The targets need not depend on k, so uniformity is unnecessary in this direction.

Write pi_k for the normal labelled representation and Omega_k=G_k(I), Tr Omega_k pi_k(Z)=a tau(Z). For selfadjoint X, pinching a fixed representative at the sign of T(X) gives an exact-class target F_X attaining a tau(|T(X)|). Thus the deficit a tau(|T(X)|)-||G_k(X)||1 tends to zero, by output trace-norm contraction and diamond approximation. Apply X=H_i-t I for every Hermitian input generator and every nonatom spectral threshold t.

Put C=pi_k(T(H_i))-t I, A=Omega_k^.5 C_+ Omega_k^.5, D=Omega_k^.5 C_- Omega_k^.5. Let s=Tr(A+D)=a tau(|T(H_i)-t I|), Delta=s-||A-D||1. For a Helstrom projection Q, e_A=Tr((I-Q)A), e_D=Tr(QD) satisfy e_A+e_D=Delta/2. Factoring x=Omega_k^.5 C_+^.5 and y=Omega_k^.5 C_-^.5, split x*y at Q and apply Schatten Cauchy--Schwarz:

    F_k:=||C_+^.5 Omega_k C_-^.5||1
       <=sqrt(Tr A e_D)+sqrt(Tr D e_A)<=sqrt(s Delta/2)->0.

For P_t=1_(t,infinity)(pi_k T(H_i)), split the offdiagonal block at t±h. Far cuts permit bounded inversion and contribute <=F_k/h. Each near-cut term contributes <=a sqrt(tau 1_{[t-h,t+h]}(T(H_i))). Therefore

    ||[Omega_k,P_t]||1 <=2F_k/h+4a sqrt(tau 1_{[t-h,t+h]}(T(H_i))).

Take k->infinity, then h->0. Dense nonatom cuts and step approximation give centrality for each generator. Products, adjoints, norm closure give it on A=C*(T(M_a)). Kaplansky L2-density plus ||[Omega_k,pi_k(Z-p)]||1<=2a||Z-p||2,tau extends it to every Z in M.

On H=directsum H_k, pi=directsum pi_k is faithful normal. States supported in block k with density Omega_k/a restrict exactly to tau and are asymptotically M-central. Any weak-star cluster phi on B(H) is a hypertrace restricting to the faithful normal tau.

For X>=0, psi_X(Y)=phi(X pi(Y)) is positive and <=||X||tau, by centrality. Hence it is normal with a bounded tracial Radon--Nikodym density P(X) in M, defined by tau(P(X)Y)=phi(X pi(Y)). Uniqueness gives unitality, identity on M, linearity and bimodularity. For [X_ij]>=0 and m_i in M,

    tau(sum m_i* P(X_ij)m_j)=sum phi(pi(m_i)* X_ij pi(m_j))>=0.

Density of m_i in L2(M,tau) proves CP. Thus P is a UCP projection onto pi(M), proving injectivity. P is generally NOT normal.


This supplies injectivity directly; the limiting CP projection need NOT be normal. It is a mathematical certificate, not one of the normal physical converters. Thus its existence is consistent with diffuse hyperfinite examples. Infima over converters are handled with error d(G_k,F)+1/k. This completes the equivalence. The detailed independent checks are retained in the record.

**Finite obstruction consequence.** For noninjective M, there are finitely many fixed pinched targets F_1,...,F_l and eta>0 such that EVERY exact-class G has max_j d(G,F_j)>=eta. Otherwise choose one G_k approximating the first k of the countable spectral-cut targets within 1/k. The same necessity proof yields injectivity, a contradiction. Neither the list nor eta is made effective by this compactness/diagonal argument.

### Explicit noninjective class: even approximate greatestness fails

Let G=F_2, M=L(G) on ell2(G), with left free-generator unitaries U,V and canonical trace tau. Define T:M_3->M by its operator Choi matrix

\[
 J_T=\begin{pmatrix}I/3&U/12&V/12\\U^*/12&I/3&0\\V^*/12&0&I/3\end{pmatrix}.
\]

Its positive floor is (1/3-sqrt(2)/12)I: the off-diagonal row [U,V] has squared norm two. T(I)=I and tau T(X)=Tr(X)/3. Its entries generate L(F_2). On the group basis set Omega=diag_g 3/(5*4^|g|). The reduced-word count gives sum_g 4^-|g|=5, so Omega is faithful trace class of trace three. Right-regular invariance gives constant diagonal coefficient tau(Z) for Z in M; hence Tr Omega Z=3tau(Z). Thus E(X)=Omega^.5 T(X)Omega^.5 is an explicit CPTP channel with this invariant. Its matrix entries in the group basis are rational; the trace tail outside word length L is (12/5)(3/4)^L. This is an effectively described infinite-output channel, not a finite Choi table.

For completeness, noninjectivity needs no capacity or Connes algorithm. An expectation B(ell2 G)->L(G), followed by tau and restricted to diagonal ell-infinity(G), would be a left-invariant mean. The four reduced-word first-letter sets A,Aminus,B,Bminus partition G minus its identity. The decompositions G=A disjointunion u Aminus and G=B disjointunion v Bminus give m(A)+m(Aminus)=m(B)+m(Bminus)=1, contradicting their total mass one; singletons have mean zero. The projection characterization of injectivity is representation independent by the UCP extension theorem. Therefore the displayed class has the finite obstruction above and no common pointwise dominating sequence. This applies the classical free-group obstruction; it does not discover nonamenability.

### Explicit sixty-target obstruction



This uses the standard Arveson extension theorem: a UCP map from an operator
system in B(K) into B(H) extends to B(K). For any normal labelled
representation pi of L(F2) on H, extend pi to a UCP map
`Phi:B(ell2(F2))->B(H)`. Its group unitaries belong to its multiplicative
domain. For any density Omega of trace a define the mean

\[
 m(f)=\operatorname{Tr}[\Omega\Phi(M_f)]/a\quad(f\in\ell^\infty(F2)).
\]

Let W_s be the nonempty reduced words whose first letter is s. The exact
relations `u(F2 minus W_u^-1)=W_u` and the analogous V relation imply

\[
 d_u+d_v\ge1,\quad
 d_u=1-m(W_u)-m(W_{u^{-1}}),\quad
 d_v=1-m(W_v)-m(W_{v^{-1}}).
\]

Multiplicative-domain covariance and the Helstrom bound for an effect give
`d_u<=||[Omega,pi(U)]||1/(2a)`, and similarly for V. Thus in **every** such
representation,

\[
 \|[\Omega,\pi(U)]\|_1+\|[\Omega,\pi(V)]\|_1\ge2a. \tag{F.1}
\]

This is a quantitative form of the usual first-letter nonamenability argument;
it does not assume the projection or mean is normal.

Take four Hermitian input matrices
`H1=6(E01+E10)`, `H2=6i(E10-E01)`,
`H3=6(E02+E20)`, `H4=6i(E20-E02)`.
Their normalized images are respectively
`A1=Re U,A2=Im U,A3=Re V,A4=Im V`.
Use the fifteen thresholds `t_j=-1+j/8`, j=1,...,15, and h=1/2048.
Each A_i has the arcsine tau-law on [-1,1], because U,V have Haar spectral
measure under tau. These near-cut intervals lie in [-15/16,15/16], where
the density is at most `16/(pi sqrt31)<1`. Thus their mass is at most
`2h=1/1024`.

For any exact-class member G, let

\[
 \Delta_{ij}=a\tau|A_i-t_j|-\|G(H_i-t_j I)\|_1.
\]

If all sixty normalized deficits `Delta_ij/a` were at most `2^-34`, the
principal's cut bound would give
`||[Omega_G,pi(P_tj)]||1<=5a/32`.
The midpoint step function

\[
 B_i=-15I/16+(1/8)\sum_{j=1}^{15}1_{(t_j,\infty)}(A_i)
\]

approximates A_i in norm to 1/16. Consequently
`||[Omega_G,pi(A_i)]||1<=7a/16` (a deliberately conservative bound).
Summing the four generators yields a commutator sum at most `7a/4`,
contradicting (1). Therefore one of the sixty deficits exceeds `a*2^-34`.

For each cut define the fixed target F_ij by pinching the original Omega at
`P_tj(A_i)` and keeping the same normalized T. Traciality makes it an exact
class member and its selected Bayes trace norm is exactly the upper ceiling.
Since `||H_i-t_j I||1=12+|t_j|<13`, output trace-norm contraction implies

\[
 \max_{i,j}\inf_R\|F_{ij}-RG\|_\diamond
 >\frac{3}{13\cdot2^{34}}\quad\text{for every exact-class }G. \tag{F.2}
\]

Thus this explicit class has a positive uniform failure gap for an explicit
finite family of at most sixty targets. They have separable infinite outputs;
no finite-output realization, efficient apparatus, or physical demonstration
is inferred. This optional constant strengthens the qualitative converse but
does not establish historical priority. The historical-priority audit is recorded in Section 15.

The CP extension import here is [Arveson, *Subalgebras of C*-algebras*, Acta Math.123 (1969), Theorem1.2.3, p149](https://archive.ymsc.tsinghua.edu.cn/pacm_download/117/6082-11511_2006_Article_BF02392388.pdf). Its hypotheses are a norm-closed self-adjoint unital subspace S of a unital C*-algebra B and a CP map S->B(H). Take S=L(F_2), B=B(ell2(F_2)), and the normal representation pi. The extension agrees on I and is therefore UCP; it need not be normal. The original theorem passage was checked in the primary PDF. No new extension theorem is claimed.

**Realization lemma.** The structural scope is not peculiar to free groups. Every finitely generated finite von Neumann algebra with faithful normal trace and separable predual occurs as such an invariant. Choose m>=1 centered Hermitian contractive generators B_1,...,B_m, a=m+1 (a dummy zero generator handles the scalar algebra); set T(E_ii)=I/a, T(E_0j)=T(E_j0)=B_j/(2am), and all remaining off-diagonal images zero. The operator Choi off-diagonal norm is at most 1/(2a), so it has floor I/(2a); T is UCP, tau T=Tr/a, and the images generate M. On L2(M,tau) choose a countable family of unitary vectors u_n whose linear span is dense and set Omega=a sum_(n>=1)2^-n|u_n><u_n|. It is faithful trace class and represents a tau because tau(u_n* Z u_n)=tau(Z). The sandwich E is CPTP. This proves realization without assuming an unproved finite-generator theorem for arbitrary finite algebras.

**Dependency and novelty.** The profile-to-normal-triple lemma, tracial Bayes pinching, Haar averaging and the spectral-deficit-to-hypertrace bridge are proved here. Injectivity versus hyperfiniteness is Connes' established theorem; finite matrix representations and the free-group obstruction are established machinery. Historical priority of this exact complete-profile characterization is unresolved. No nontracial analogue, effective amenability algorithm or laboratory capability is asserted.

## 8. Paid approximate simulation from offline Choi acquisition

**Theorem O.** The following is a proved application of standard product-port teleportation, with an independently checked dilation refinement. It is not a new PBT theorem.

### A complete offline simulation theorem

Let `Phi:M_a -> M_b` and `Psi:M_a -> M_c` be finite CPTP channels, `a>=2`.
Suppose a supplied physical CP trace-nonincreasing map `S:M_b -> M_c` satisfies

\[
 S\Phi=p\Psi,\qquad 0<p\le1. \tag{1}
\]

The identity is an identity of complete maps, not just matching scalar success
probabilities. The implementation is fixed and memoryless; fresh trials begin
with uncorrelated ancillary systems. Local operations, authenticated classical
herald feedback and forward port-index communication are available. Quantum
storage is ideal during preparation and online use. Unknown input and untouched
reference states may be arbitrary, but are initially independent of the resource
bank and its preparation apparatus. The target protocol's ordinary adaptive
interfaces do not acquire the simulator's port bookkeeping as extra data.

Write `chi_Psi=(id tensor Psi)(phi_a)` and `C_a=2a(a-1)`. For any positive
integers `n,M`, there is a protocol with these properties:

1. Before unknown data arrives, prepare `m=nM` copies of `chi_Psi`. Each copy
   costs `1/p` expected calls to `Phi`, so total expected source calls are `nM/p`.
2. After readiness, arbitrary `n`-slot adaptive use of `Psi`, on unknown and
   referenced inputs, is simulated by a deterministic online operation. Its
   final honest/reference full trace-norm error is at most
   \[
   n\delta_M\le C_a n/M, \tag{2}
   \]
   where `delta_M` is the standard `M`-port identity-channel error.
3. If the full online apparatus environment is retained, including resource
   purifications, discarded ports, measurements and public port transcripts,
   then there exists a fixed environment alignment to a dilation of the ideal
   target protocol, with joint trace distance at most
   \[
   u_{n,M}=\sqrt{1-(1-\delta_M/2)^n}
       \le\sqrt{C_a n/(2M)}. \tag{3}
   \]
   This alignment is a proof comparison, after sufficient environment padding.
   It neither gives the users access to Eve nor requires implementing an
   operation on her registers.
4. Therefore receiver full-norm accuracy `epsilon` requires `M>=C_a n/epsilon`;
   full-environment trace-distance accuracy `u` requires `M>=C_a n/(2u^2)`.
   Primitive source calls are respectively
   `O(a^2 n^2/(p epsilon))` and `O(a^2 n^2/(p u^2))` in expectation.

All quantities count actual source calls. Dependence on `1/p` is explicit; a
polynomial-in-`n` claim does not make `1/p` polynomial in source description
length. The result requires a supplied verified converter; it does not acquire
one from a noisy unknown device or evade the initial report's tomography
obstruction.

#### Proof: the resource bank and an actual processor

Prepare a maximally entangled `a x a` pair locally, keep one half, send the other
through `Phi`, and apply the success/failure instrument containing `S`. By (1),
the success probability is `p` and the normalized accepted state is exactly
`chi_Psi`. Failure occurs on a freshly prepared pair, never on the future data.
Independent trials give independent accepted states. Stopping after `m` successes
has negative-binomial expectation `m/p`.

This also accounts for the preparation environment. A purified implementation of
the normalized successful map is a Stinespring dilation of `Psi`, because (1)
holds on all inputs and its success effect on the source input is `p I`.
Accepted resources, failure records and stopping history may all be purified.
Their accepted honest marginal is `chi_Psi^tensor m`, independent of the stopping
history. The extra history is input-independent and can be retained in the
environment comparison. Input-independent heralding by itself would not prove
this conclusion; (1) is the needed channel identity.

For each target use, apply standard deterministic port-based teleportation to
the input and `M` independent resource states. The sender's POVM depends only on
`a,M`; Bob keeps the announced output port and discards the others. A finite
exact specification is the square-root measurement on the usual signal states

\[
 \sigma_i=\phi_{A_0A_i}\otimes I_{A_{\ne i}}/a^{M-1},\quad
 \Sigma=\sum_i\sigma_i,\quad
 \Pi_i=\Sigma^{+1/2}\sigma_i\Sigma^{+1/2}+P_{\ker\Sigma}/M.
\]

Here `Sigma^{+1/2}` means the square root of the Moore--Penrose inverse. The POVM
sums to identity. Its matrix size is `a^(M+1)`. Rational signal matrices have
exact algebraic square roots and inverses, so this is a finite constructive
processor, not a claim of a polynomial-size rational processor or practical
generic local compilation.

Because Bob's port selection commutes with applying `Psi` to every receiver
half before the measurement, the implemented receiver channel is exactly

\[
 \Psi_M=\Psi\circ\Gamma_M, \tag{4}
\]

where `Gamma_M` is standard PBT's approximate identity. Equation (4) holds for
non-covariant targets and arbitrary references. The target need not admit
ordinary one-Choi teleportation simulation. Standard PBT gives

\[
 \delta_M=\|\Gamma_M-id\|_\diamond
       =2[1-F_e(\Gamma_M)]\le C_a/M.
\]

The receiver error (2) follows by an `n`-term telescoping/contractivity argument
through the fixed adaptive interleavers. Interleavers can use all honest
quantum/classical records permitted by the original protocol. Extra simulator
communication is paid separately below.

#### Full environment: why a square-root bound is enough

Standard `Gamma_M` is depolarizing. Its Weyl random-unitary representation has
identity-branch probability `w0=F_e(Gamma_M)=1-delta_M/2`. A valid dilation of
`Psi_M` applies the Weyl error, records its label coherently in a new environment,
then applies a Stinespring isometry of `Psi`.

In the purified `n`-slot protocol, the all-identity Weyl branch is exactly the
ideal target dilation multiplied by `w0^(n/2)`. This is true with adaptive
interleavers because each conditional Weyl branch is a scalar times an
isometry and its probability is independent of the slot input. The other error
patterns carry orthogonal environment labels. For every purified initial
input/reference state, the overlap with the ideal dilation padded by zero error
labels is `w0^(n/2)`. Pure-state trace distance is consequently
`sqrt(1-w0^n)`, proving (3); mixed states follow by purification and partial trace.

The actual PBT apparatus and this convenient Weyl dilation are dilations of the
same receiver channel (4). Stinespring uniqueness aligns them by a fixed
environment partial isometry, extendible after padding. It acts on the full
apparatus environment; no honest target-interface system is moved. This proves
a final joint-state comparison, not physical control of Eve. Discarding any
trusted portions of that environment can only improve the bound.

#### Precise privacy consequence and limitation

In the fixed memoryless, passive-complement eavesdropper model with authenticated
public communication, apply the comparison to a target key protocol and retain
all source/preparation/port environments and public records on Eve's side.
Arbitrary later processing by Eve preserves the bound. The ideal comparison
includes a fixed Eve-side simulation/alignment and independent preparation
history. If the target final key state satisfies

\[
 D(\rho^{id}_{KE},\gamma_K\otimes\rho^{id}_E)\le s,
\]

then the actual simulated protocol satisfies the safe bound `s+2u_{n,M}` in
this same actual-marginal definition. One factor `u` compares the joint states,
and the other compares their Eve marginals. The honest output correctness
probabilities also change by at most the joint trace distance. A definition
allowing an arbitrary ideal Eve state can omit the second factor.

This is not a claim about an actively modified source device, correlated
non-memoryless noise, side-channel leakage from trusted input registers, or a
new universally composable simulator against arbitrary interactions during
resource preparation. The theorem's joint final-state comparison is the exact
security statement established here. The external unknown input/reference is
fresh relative to the resource bank; allowing initial adversarial correlations
with that bank would change the channel model.

### Noisy resources and a finite confidence budget

Let the actual source/instrument be fixed memoryless CP operations with

\[
 \|\widetilde S\widetilde\Phi-p\Psi\|_\diamond\le\eta<p.
\]

For one offline Choi trial let `q` be its actual success probability and `omega`
its normalized successful state. Then

\[
 q\ge p-\eta=:p_-,\qquad
 \|\omega-\chi_\Psi\|_1\le e:=\min\{2,2\eta/(p-\eta)\}.
\]

Indeed the unnormalised states differ by at most `eta`, their traces differ by
at most `eta`, and normalization costs at most another `eta/q`. The accepted
state need not itself be a Choi state of a TP map; that is unnecessary. The
PBT processor with any independent density-operator program is CPTP.

Contractivity and a product-state telescoping bound give the safe receiver
full-norm error

\[
 \varepsilon_{rec}\le\min\{2,C_a n/M+nM e\}. \tag{5}
\]

For the environment comparison, purifications of `omega` and `chi_Psi` can be
chosen with root overlap at least `1-e/2` (the state case of the verified
Stinespring/Bures bound). Product purifications therefore differ in trace
distance by at most `sqrt(nM e)`. Uhlmann/Stinespring alignment is only on the
preparation environment, not the stored resource registers or the target input.
Running the same online apparatus and interleavers cannot increase that
distance. Together with (3),

\[
 u_{total}\le\min\{1,\sqrt{C_a n/(2M)}+\sqrt{nM e}\}. \tag{6}
\]

This uses independent trials and fixed memoryless implementation. Marginal
one-use error bounds without those assumptions would not justify the product
resource bank or (5)--(6).

An explicit conservative design achieving receiver error at most `epsilon` and
joint distance at most `u` chooses

\[
 M\ge\max\{2C_a n/\epsilon,\;2C_a n/u^2\},\qquad m=nM,
\]
\[
 \eta\le\min\left\{\frac{p\epsilon}{4m+\epsilon},
                    \frac{p u^2}{8m+u^2}\right\}. \tag{7}
\]

The two terms in each error budget receive half the allocation. In particular,
accuracy of the offline conversion is a paid requirement, not a uniform
noise-independent benefit.

#### Fixed stopping cap

Given `0<zeta<1`, choose integer `L>=1` with `2^-L<=zeta`. Make at most

\[
 T=\left\lceil\frac{2m+8L}{p_-}\right\rceil \tag{8}
\]

fresh trials and keep the first `m` successes. With `X~Binomial(T,q)`, its mean
`mu>=2m+8L`. Thus `Pr[X<m]<=Pr[X<mu/2]<=exp(-mu/8)<=2^-L<=zeta`.
The uncapped mean is `m/q<=m/p_-`; a capped run uses at most `T` source calls.
Readiness is decided before accepting unknown data. On failure the experiment
never touches that data; it is not retried. Conditioning on readiness does not
alter the accepted product state, since the independent accepted state is
independent of success locations and stopping history.

If comparing to a target that never aborts, the preparation shortfall adds at
most `2zeta` to a full receiver norm bound, or `zeta` to joint trace distance.
If abort is part of the declared protocol, readiness has probability at least
`1-zeta` and the conditional bounds (5)--(6) apply. No zero-failure finite
preparation claim is made.

### Resource ledger and interpretation

At most `T` backward herald bits suffice (one per trial), plus `n ceil(log2 M)`
forward port-index bits. Preparing all resources before input arrival stores
`m` Alice systems of dimension `a` and `m` Bob systems of dimension `c`, namely
`m log2 a` and `m log2 c` qubits up to register rounding. A trial also uses
its source/instrument ancillas; all actual environment registers are retained
for the security statement. The PBT sender measurement has dimension
`a^(M+1)`. Local synthesis, storage duration/decoherence and gate complexity
are not free experimental resources merely because source-call counting is
polynomial. Exact algebraic full-matrix construction may be enormous.

[pbt_budget.py](MAXIMAL_INFORMATION_RESEARCH_RECORD/constructor/pbt_budget.py) is an exact rational budget compiler and
`pbt_budgets.json` its executed output. With `a=2,n=2,p=1/7`, receiver tolerance
`1/4`, joint distance tolerance `1/4` and shortfall `1/1000`, it returns
`M=64`, `m=128`, expected source cost `896`, cap `2352`, twelve forward bits,
and at most `2352` backward bits. The receiver bound is `1/8` and joint bound
`1/4`. The generic full POVM already has dimension `2^65`.

For `n=10`, both tolerances `1/100`, the same source has `M=200000`, two
million Choi resources, fourteen million expected source calls, cap `28000560`
and 180 forward bits. This deliberately exposes why a mathematical polynomial
source-use improvement is not a present practical advantage. The N1690 click
probability and noisy split-budget examples are also computed in that JSON.

Same-profile classes have the converter (1), so they admit this approximate,
paid, finite-block, assisted operational interconversion. Ordinary unassisted
capacity equality does not follow: feedback is used, and the source cost grows
with desired block length/accuracy. An exact generic finite-port simulation is
not supplied. Teleportation-covariant targets retain the stronger special exact
`n/p` source-use simulation already described in N1698.

### Primary imports and priority

The standard PBT statements used are Pirandola--Laurenza--Lupo--Pereira,
[arXiv:1803.02834](https://arxiv.org/html/1803.02834), Lemma 1, Eq. (9), and
Lemma 2: product Choi resources, depolarizing identity simulation, its diamond
bound and adaptive peeling. The article was inspected and cached. The
offline heralded resource bank and explicit budgets are the present
application of those established operations. There is no claim to invent
channel-state simulation or PBT stretching.

The environment uniqueness/Bures comparison is Kretschmann--Schlingemann--Werner,
[arXiv:0710.2495v1](https://arxiv.org/html/0710.2495), Theorem 1, Eqs. (6)--(7),
with sufficiently padded common dilations. It permits choosing aligned
dilations; it does not assert arbitrary unaligned environments are close.
The sharper exact-resource estimate (3) is proved directly from the Weyl
identity branch, rather than asserted from receiver closeness alone.

Broader searches found older programmable-channel/PBT literature and recent
multiport/finite-memory work. No historical-priority clearance for this
particular combination is established. The proper description is a complete
operational application with explicit physical costs and scope.


## 9. Complete RLD order is strictly weaker than canonical processing

### Binary classical channels with arbitrary quantum references

Let a channel measure the computational basis of its qubit input and apply a
classical channel `W`, with row vectors `w_z=(W(z|0),W(z|1))`. For an arbitrary
faithful referenced input let `rho_0,rho_1>0` be its two diagonal reference
blocks and `H_0,H_1` the Hermitian diagonal tangent blocks. Off-diagonal input
blocks are discarded. Its reference-valued RLD operator is

\[
 Q_W=\sum_z(w_{z0}H_0+w_{z1}H_1)
       (w_{z0}\rho_0+w_{z1}\rho_1)^{-1}
       (w_{z0}H_0+w_{z1}H_1).
\]

No scalar-reference congruence invariance is assumed. Instead set
`S=rho_0+rho_1`, `A=S^−1/2 rho_0 S^−1/2`, and
`K_i=S^−1/2 H_i S^−1/2`. Then

\[
 Q_W=S^{1/2}\left[\sum_z(w_{z0}K_0+w_{z1}K_1)
    (w_{z0}A+w_{z1}(I-A))^{-1}
    (w_{z0}K_0+w_{z1}K_1)\right]S^{1/2}.
\]

Write `A=sum_j x_j P_j`, `y_j=1−x_j`. For a scalar baseline `(x,y)`, define

\[
 C_W(x,y)=\sum_z\frac{w_z^T w_z}{w_{z0}x+w_{z1}y}.
\]

The bracketed **operator difference** for `W,V` is

\[
 \sum_j\sum_{i,l=0}^1
   [C_W(x_j,y_j)-C_V(x_j,y_j)]_{il}\,K_iP_jK_l.
\]

If every real symmetric coefficient matrix is PSD, each summand is positive:
factor the coefficient matrix and write it as a sum of operators
`(sum_i c_i K_i) P_j (sum_l c_l K_l)`. Hence `Q_W−Q_V>=0`, and undoing the
whitening by the displayed congruence retains positivity. This proves the
comparison for all noncommuting reference blocks and tangents, stronger than
the scalar trace inequality needed for complete RLD order. Faithfulness gives
`0<x_j<1`; endpoints follow by ordinary support limits when needed.

### Scalar coefficient identity

For a BSC with crossover `p`, put `c=1−2p`. Let `C_tr` be the coefficient
matrix of the one-output erasure/replacer channel. Direct algebra gives

\[
 C_{\mathrm{BSC}(p)}(x,y)-C_{\rm tr}(x,y)
 =\frac{c^2}{(x+y)((1-p)x+py)(px+(1-p)y)}
      \begin{pmatrix}y\\-x\end{pmatrix}
      \begin{pmatrix}y&-x\end{pmatrix}.
\]

For `x+y=1` and `z=x−y`, the scalar multiplier is
`4c²/(1−c²z²)`. Now let `W` be the flagged mixture of probability `alpha`
of `BSC(p_E)` and probability `1−alpha` of an erasure symbol. Let
`V=BSC(p_F)` with `0<=c_F<=c_E<=1`. Their coefficient difference is PSD
for every baseline iff

\[
 \boxed{\alpha c_E^2\ge c_F^2.}
\]

Indeed, after positive denominators are cleared its multiplier numerator is

`(alpha c_E²−c_F²)+c_E² c_F² z²(1−alpha)`.

Necessity is the uniform baseline `z=0`; sufficiency is termwise positivity.
The reference-operator argument above lifts this exact condition to complete
RLD order, without treating scalar RLD as invariant under nonunitary filters.

### Full-Choi-rank counterexample

Choose `alpha=1/3`, `p_E=1/10`, `p_F=3/10`. The classical matrices, with
input columns, are

\[
 W=\begin{pmatrix}3/10&1/30\\2/3&2/3\\1/30&3/10\end{pmatrix},\qquad
 V=\begin{pmatrix}7/10&3/10\\3/10&7/10\end{pmatrix}.
\]

Define quantum channels by `E_W(X)=diag(W diag(X))` and similarly for `V`.
They are rational CPTP, their unnormalized Choi matrices are diagonal, and

`J_W>=I_6/30`, `J_V>=3I_4/10`.

Here `c_E=4/5`, `c_F=2/5`, so
`alpha c_E²=16/75>4/25=c_F²`. Consequently

\[
 Q_W(\rho,H)\succeq Q_V(\rho,H)
\]

for every finite untouched reference, faithful input and Hermitian tangent.
In particular `E_W` completely RLD-dominates `E_V`.

Both channels already are greatest representatives. Their normalized output
generators distinguish all three, respectively two, posterior labels, so the
generated algebras are `C³` and `C²`. Their `Omega` matrices are diagonal and
fixed by the conditional expectations onto those algebras; thus the greatest
lift is the original channel. Both are also multiplicity-one representations.

Yet the trace norms of the two basis-output differences are

\[
 \|E_W(|0\rangle\langle0|-|1\rangle\langle1|)\|_1=8/15,
 \qquad
 \|E_V(|0\rangle\langle0|-|1\rangle\langle1|)\|_1=4/5.
\]

No CPTP output map can increase that norm. More quantitatively, if
`||E_V−R E_W||_diamond<=epsilon`, the two individual state errors give

`4/5 <= 8/15+2epsilon`, hence

\[
 \boxed{\inf_{R\,\mathrm{CPTP}}\|E_V-R E_W\|_\diamond\ge2/15.}
\]

This is a decisive counterexample to the suggested general order collapse,
strictly inside full-Choi-rank channel sets. It does not affect equality-class
classification or the universal greatest member **within one class**.

Exact symbolic verification of the coefficient identity, Choi floors, trace
distances and a noncommuting complex reference example is in
`../checks/machinery_order.py` and `.json`. In that example the full reference
operator difference is exactly positive definite, not merely positive-trace.

### Restricted positive order theorem and predecessors

Within the single BSC family `0<=p<=1/2`, complete RLD order **does** coincide
with deterministic processing: it holds from `p` to `q` iff `p<=q`. Necessity
comes from the maximally mixed baseline and `sigma_z` tangent, which give a
quadratic form proportional to `(1−2p)²`. Sufficiency is the bit-flip
postprocessing with crossover `(q−p)/(1−2p)`; the endpoint `p=1/2` is handled
separately. Within erasure channels, the complete order likewise coincides
with decreasing reveal probability, directly from
`g_BEC=alpha g_identity+(1−alpha)g_trace` and erasing additional labels.

The broad separation is established classical machinery. In particular
[Nair, *Capacity regions of two new classes of 2-receiver broadcast
channels*](https://staff.ie.cuhk.edu.hk/~cnair/pub/papers/BC/twoclass-full.pdf),
**Claim 4**, gives BEC/BSC less-noisy-but-not-degraded parameter ranges.
[Makur–Polyanskiy, arXiv:1609.06877](https://arxiv.org/pdf/1609.06877) establishes
classical less-noisy comparison through chi-square divergence in **Theorem 1**:
for two Markov kernels on the same source space, less-noisy comparison is
equivalent to chi-square comparison for every pair of input probability measures.
Our finite classical channels meet those hypotheses. The present
counterexample uses that mechanism plus the explicit binary reference-operator
lifting proof. It is not a new separation of the classical less-noisy and
degradation orders. The useful conclusion is that this known separation
survives precisely the complete physical RLD interface and canonicalization.

A terminology check matters here: the recent
[Hirche, arXiv:2610.03706](https://arxiv.org/pdf/2610.03706), §3.2 equation (3.13),
explicitly uses the **BKM** metric for its quantity called quantum chi-square.
Its complete-order results cannot be transferred to the present RLD form just
by identifying the names of the divergences.


## 10. Exact existing machinery and novelty audit

### Exact Connes import for Theorem B


Primary statements independently inspected:

* A. Connes, *On the Classification of von Neumann Algebras and Their
  Automorphisms*, IHES/P/76/132, February 1976,
  [author's archive PDF](https://repo-archives.ihes.fr/FONDS_IHES/I_Prepublications/CONNES/1976-1984/P_76_132/P_76_132_web.pdf),
  **Theorem 4.1, printed p43 / PDF p46**. For arbitrary von Neumann algebras
  on separable H, the theorem equates approximate finite dimensionality with
  property P, property E/injectivity and semidiscreteness. Approximate finite
  dimensionality is defined on printed p41 / PDF p44 using an increasing
  sequence of finite-dimensional *-algebras. Immediately after Theorem 4.1,
  Connes explicitly explains how the original factor proof extends to general
  centers using Choi--Effros direct-integral semidiscreteness and decomposability
  of injectivity. Thus no factor-only theorem is silently strengthened.
* A. Connes, *Noncommutative Geometry*, 1994,
  [author's monograph PDF](https://webhomes.maths.ed.ac.uk/~v1ranick/papers/connes.pdf),
  **Chapter V, section 7, Theorem 6, p504** gives the same equivalence for an
  arbitrary von Neumann algebra on separable H. **Definition 17, p500** defines
  hyperfiniteness by an increasing finite-dimensional sequence for separable
  predual. Property 4 on p502 explicitly handles factor direct integrals.

**Representation independence needed in the F2 obstruction:** Connes's
monograph **Chapter V, section 7 beta, Definition 2 and the following paragraph,
p502**, defines property E by a norm-one projection B(H)->M and states its
independence of the Hilbert space on which M acts; the following sentence
identifies it with injectivity using Arveson's extension theorem. The same
statement is in the 1976 survey, **printed p42 / PDF p45**. In particular,
injectivity established in a faithful normal direct-sum representation gives
a norm-one projection in any other faithful normal representation, including
the standard left-regular representation of L(F2). Tomiyama's theorem makes
this projection CP and bimodular. **Normality of the projection is not claimed.**

The acquired-source hashes and URLs are preserved in the record literature manifest. Full primary PDFs remain in the working cache. Only the finite tracial
case is needed; later type-III_1 uniqueness results are irrelevant.

The given M acts on separable H, so the import's hypotheses are met. If its
finite-dimensional algebras are not unital in M, replace N_n by N_n+C I;
they remain finite-dimensional and increasing. Von Neumann generation gives
L2(tau) density by Kaplansky density and normality of the finite trace.
Conversely L2 density gives von Neumann generation. Tau-preserving expectations
onto the finite algebras are the finite trace pairing projections; their L2
extensions are orthogonal projections. This verifies (1)<->(2).


### Infinite-output priority comparison

[Hiai, *Quantum f-divergences in von Neumann algebras II. Maximal
f-divergences*, arXiv:1807.03118v1](https://arxiv.org/pdf/1807.03118v1),
**Lemma 6.1** constructs the normal CP spectral reverse test on
`L_infinity([0,1],nu)` using the spectral measure of the bounded likelihood.
**Theorem 6.3** says it attains the maximal-divergence reverse-test minimum
and allows a standard Borel probability space on `[0,1]`. This is already the
ideal possibly diffuse classical experiment used here. The atomic construction
is its countable discrete specialization.

[Kuramochi, arXiv:1701.03394v2](https://arxiv.org/pdf/1701.03394v2),
**Lemma 6 and Theorem 5**, pp. 25–26, prove that a POVM is postprocessing
equivalent to a discrete POVM iff its channel is CP-concatenation equivalent
to one with a fully quantum outcome algebra `B(H)`. **Remark 4** explicitly
connects the absence of a continuous fully-quantum realization to the absence
of a normal conditional expectation onto a diffuse abelian subalgebra and
credits Holevo 2012 for that observation.

The operator-algebraic obstruction is even older. I acquired and visually
read the scanned primary
[Størmer, *On Projection Maps of von Neumann Algebras*, Math. Scand. 30
(1972), 46–50](https://doi.org/10.7146/math.scand.a-11062). Its unnumbered
**Theorem on p. 47** characterizes complete families of normal projection maps
from a type-I algebra `R` onto a subalgebra containing its center: the
subalgebra is type I and its center is totally atomic over the center of `R`.
A faithful normal conditional expectation is a complete family by itself.
For `R=B(H)` this yields the atomic-algebra obstruction. The original scanned pages were visually inspected. The retained source PDF supports that check; generated page PNGs were later removed during cache compaction. No invented theorem number is used.

The exact inference “a greatest trace-class member must attain every Bayes
envelope, hence realize the spectral reverse experiment” is the applicability
bridge supplied by the principal's proof. Hiai's theorem by itself concerns
a reverse-test minimizer in a larger algebraic category; Kuramochi's theorem
by itself concerns ordinary concatenation equivalence. Neither should be
silently relabelled as the new profile-class greatest theorem. Conversely,
calling the diffuse/atomic normal-realization obstruction new would overstate
the contribution. Historical priority for the assembled criterion remains
unassessed.


### Checked finite and statistical primary machinery

The following primary import audit was completed independently before the challenge phase; it is retained with exact version numbers and applicability. Further robust and continuity imports follow it.

#### Maximal equality is not ordinary sufficiency

[Hiai–Mosonyi, *Different quantum f-divergences and the reversibility of quantum
operations*, arXiv:1604.03089v4](https://arxiv.org/pdf/1604.03089v4), Theorem 3.34,
assumes positive matrices `rho,sigma` with `supp rho <= supp sigma` and a positive
trace-preserving map `D`. Equality for any non-linear operator-convex maximal
f-divergence is equivalent to equality for the quadratic divergence, to
`D(rho sigma^-1 rho) = D(rho) D(sigma)^-1 D(rho)`, and to perspective preservation
for every scalar function on the relevant spectrum. For 2-positive `D`, it is
equivalent to `sigma^-1/2 rho sigma^-1/2` belonging to the multiplicative domain
of the normalized map `D_sigma`.

Applicability here: all displayed physical postprocessings are CP and TP; a
faithful input baseline has full joint output support. Thus the support
hypothesis holds after compression. This theorem explains why a normalized
output *-homomorphism preserves all maximal perspectives. It cannot be applied
directly to two unrelated channels without first constructing their relation.
Their §4.2 and Example 4.8 explicitly separate maximal equality from ordinary
reversibility. The source's capacity separation is therefore not a contradiction
of Petz sufficiency.

#### The canonical binary specialization is already a reverse test

[Matsumoto, *A new quantum version of f-divergence*,
arXiv:1311.4722v4](https://arxiv.org/pdf/1311.4722v4), Theorem 6.1 gives the
maximal-divergence reverse-test formula and attains it by the spectral reverse
test. Theorem 6.9 proves essential uniqueness of optimal reverse tests under
its additional integral-measure support condition (6.15); that extra condition
must not be dropped when citing this uniqueness theorem.

For two positive density matrices `rho,sigma`, put `Omega=rho+sigma` and
`A=Omega^-1/2 rho Omega^-1/2`. Then the normalized generators are `A` and `I-A`,
so their algebra is commutative. In the spectral basis of `A`, the greatest
channel's two outputs are distributions with weights
`p_j=lambda_j Tr(Omega P_j)` and
`q_j=(1-lambda_j) Tr(Omega P_j)`. The preparation map sends `j` to
`Omega^1/2 P_j Omega^1/2 / Tr(Omega P_j)`. This directly verifies that the binary
canonical lift is Matsumoto's minimal reverse test, with the reference chosen
as `rho+sigma`. It is a specialization of an established theorem.

#### Petz transpose supplies the displayed reconstruction

Hiai–Mosonyi equations (3.19)–(3.20), Theorem 3.18 and Remark 3.17(2) give the
Petz transpose formula and explain completion outside the relevant support.
For a trace-preserving conditional expectation `E_A`, a positive density
proportional to `Omega`, and `Z=E_A(Omega)`, that formula is exactly

`R(Y)=Omega^1/2 Z^-1/2 E_A(Y) Z^-1/2 Omega^1/2`.

Here `Z` is invertible on the joint support because `Omega >= omega I` there
for some `omega>0` and the expectation is unital positive. The formula is CP,
and its effect is `Z^-1/2 E_A(Omega) Z^-1/2=I`. Its use on the new lifted outputs
is valid. It does not assert that ordinary coarse graining of the original
outputs is reversible.

#### Canonical moments and minimal experiments have strong predecessors

[Guţă–Jenčová, *Local asymptotic normality in quantum statistics*,
arXiv:quant-ph/0606213v2](https://arxiv.org/pdf/quant-ph/0606213v2), Corollary 3.4
and Theorem 3.5 characterize equivalence of faithful quantum experiments by a
state-preserving isomorphism of their minimal sufficient algebras and by a
canonical state built from all ordered Connes-cocycle moments. Theorem 3.3
uses ordinary statistical sufficiency. These are not the N1698 normalized
generator moments, and their equivalence classes are different.

[Kuramochi, *Minimal sufficient statistical experiments on von Neumann
algebras*, arXiv:1701.03394v2](https://arxiv.org/pdf/1701.03394v2), Theorem 1 and
Corollary 2 prove existence and uniqueness up to isomorphism of a minimal
sufficient experiment/channel in the ordinary CP-concatenation class, including
general von Neumann algebras. This cannot identify the greatest member of the
larger maximal-profile class: Section 6 gives equal maximal profiles
with strictly different ordinary binary decision performance.

The applicable lesson is that faithful-state moment classification and
canonical algebraic representatives are established organizing machinery. The
new bridge, if any, has to be the particular family of physical tests and the
particular equivalence class they determine.

#### Finite closure and short separating words are old algorithmic machinery

[Li–Qiu, *A Polynomial-Time Algorithm for the Equivalence between Quantum
Sequential Machines*, arXiv:quant-ph/0604085v2](https://arxiv.org/pdf/quant-ph/0604085v2),
Theorem 2, gives a polynomial algorithm returning a distinguishing word for
inequivalent machines. Its proof retains a basis of reachable matrices and
expands children only for linearly independent basis words. The same finite
linear-closure operation applies to our direct-sum raw channel algebra. No
claim that the channel itself is a sequential machine is needed: the elementary
closure proof is supplied in §4.

[Volčič, *Matrix coefficient realization theory of noncommutative rational
functions*, arXiv:1505.07472](https://arxiv.org/pdf/1505.07472), Theorem 6.1,
gives a finite matrix-size identity test from realization dimension. Its
Example 4.3 also warns that matrix-coefficient minimal realizations need not
be pairwise similar. One must not import scalar realization uniqueness into
arbitrary matrix-coefficient realizations without its hypotheses. Here the
faithful state and *-algebra, rather than generic realization uniqueness,
provide the relevant uniqueness.

#### The operational approximate comparator is already complete

[Jenčová, *Comparison of quantum channels and statistical experiments*,
arXiv:1512.07016v2](https://arxiv.org/pdf/1512.07016v2), Theorem 1, uses
`delta(Phi,Psi)=inf_D ||Phi-D Psi||_diamond`. It characterizes
`delta(Phi,Psi)<=epsilon` by complete input-ensemble guessing inequalities
with additive term `(epsilon/2) P_succ(input ensemble)`. It suffices to use an
ancilla of dimension equal to the target output dimension and equiprobable
ensembles of its square cardinality.

This theorem applies directly to any pair of finite canonical channels, or to
any proposed approximate simulator. It gives a bounded-ancilla operational
test and an SDP-based alternative to noisy moment inversion. It does not
replace the N1698 classification: its data are decision profiles, not maximal
divergence profiles. Any claimed new general approximate-channel comparison
capability should be matched against this theorem.

#### Recent prior work must be kept separate from the whole-channel invariant

[Buscemi, *Quantum f-divergences from retrodictive tests: a unifying classical
variational principle*, arXiv:2610.29696](https://arxiv.org/pdf/2610.29696),
Theorem 3.1 fixes faithful `rho,sigma,gamma` and minimizes a coupled classical
f-divergence over preparation/retrodiction tests; Theorem 6.1 inserts a fixed
quantum channel. Both are spectral optimality statements with prescribed
states and reference. Neither theorem states whole-channel classification by
all normalized-output moments or a greatest member of that profile class.

[Okayasu, *Operator-valued maximal f-divergences for completely positive
maps*, arXiv:2609.00554v1](https://arxiv.org/pdf/2609.00554v1), Definition 3.1 and
Proposition 3.4 construct an operator-valued maximal divergence from a common
Stinespring–Radon–Nikodym realization. Theorems 4.3 and 4.4 respectively prove
monotonicity under unital CP precomposition and normal CP postcomposition;
Theorem 4.9 gives monotone convergence along increasing von Neumann
subalgebras. This is a strong existing route for generalized CP-map divergence
questions. Its arguments compare **two CP maps** through their common
dominating dilation; the present invariant compares both state arguments
after **one** channel. Equating these two interfaces without proof would be a
scope error. In particular it does not supply finite-dimensional greatest
representatives for arbitrary infinite-dimensional generated algebras.


### Remaining exact imports and a relevant approximation comparator

[Sontag, *For Differential Equations with r Parameters, 2r+1 Experiments Are Enough for Identification*](https://www.sontaglab.org/FTPDIR/ident-experiments.pdf), J. Nonlinear Sci. 12 (2002), Theorem 2, assumes an analytic response family on its finite-dimensional parameter and connected analytic experiment domains. Theorem P's rational physical probe gaps have those properties. Its direct incidence proof is the same established generic-identification mechanism; semialgebraicity additionally earns a rational, terminating selector. The selector has not been executed and has no proved polynomial complexity.

[Basu–Mohammad-Nezhad, *Improved effective Łojasiewicz inequality and applications*](https://doi.org/10.1017/fms.2024.66), Forum Math. Sigma 12 (2024), e115, Theorem 2.2, assumes a closed bounded semialgebraic set A, continuous semialgebraic f,g, and f^{-1}(0) contained in g^{-1}(0). It proves |g|^q<=C|f|, with degree-dependent q<=(8d)^{2(n+7)} for descriptions of degree d. In S, A=K², f is the probe gap and g the minimum unitary-orbit Choi distance; full algebra generation earns its zero-set hypothesis. Real quantifier elimination supplies the required descriptions and a terminating search for constants. Remark 2.7 rules out a bound on C from degrees/dimensions alone. The exact rational coefficients and conditioning are material.

[Leung–Smith, arXiv:0810.4931v2](https://arxiv.org/pdf/0810.4931v2), Corollaries 13 and 14, give continuity of classical and ordinary quantum capacity respectively at fixed finite output dimension (bound 8 epsilon log d_out+4 h2(epsilon) in the stated range). Padded finite flag paths retain that dimension. These statements justify the resource-envelope and spectrum limits without supplying capacity evaluation. Earlier tentative notes citing Corollary 7 are superseded by this checked numbering.

[Myhr–Lütkenhaus, arXiv:0812.3667v1](https://arxiv.org/pdf/0812.3667v1), Lemma 5, identifies antidegradability with a symmetric extension of the whole channel Choi output. The explicit B satisfies the complete marginal and swap identities; labels alone would not suffice. [Devetak, arXiv:quant-ph/0304127v6](https://arxiv.org/pdf/quant-ph/0304127v6), Theorem 5 and Proposition 7, earn the coherent-information achievable-rate lower bound for the finite memoryless depolarizing target. No exact capacity computation or efficient coding claim is imported.

For tracial word invariants, [Jing, arXiv:1504.06790v1](https://arxiv.org/pdf/1504.06790v1), Theorem 2.2, and Marcoux–Mastnak–Radjavi, Corollaries 3.10–3.11 ([author version](https://cs.smu.ca/~mmastnak/papers/approxspecht.pdf)), supply existing Specht/unitary-similarity machinery under their adjoint-closure assumptions. The Hermitian labelled tuples meet closure. Those results do not supply a finite noisy-profile inverse; S earns that different claim with the generation margin and error bound.

A further primary-source check found [Hollands–Ranallo, *Channel Divergences and Complexity in Algebraic QFT*](https://doi.org/10.1007/s00220-023-04855-x), CMP 404 (2023), 927–962. Lemma 3.9 and Proposition 3.10 use finite-algebra approximations and generalized conditional expectations for divergence convergence; Proposition 3.12 proves composition subadditivity on hyperfinite algebras. This is a strong predecessor for the approximation machinery. It compares divergences between channels, and does not identify greatest members inside a complete-profile class. Its generalized expectations do not automatically preserve the exact invariant state required here.

Targeted searches did not locate an identical exact-versus-approximate complete-profile theorem. That is not priority clearance. Connes' equivalence, hypertrace criteria, normal projection atomicity, reverse tests, Specht theory, semialgebraic bounds and PBT remain established machinery.

## 11. Routine stronger consequence: the finite capacity spectrum

Let Gamma be the finite greatest representative and Q_*=Q(Gamma). Over ALL finite-dimensional real-coefficient representatives in its exact class, the set of ordinary quantum capacities is {0} if Q_*=0; otherwise it is either (0,Q_*] or [0,Q_*]. This is a routine consequence, not a capacity evaluator.

Proof: for equivalent E,F, the flagged path (1-t)E directsum tF has the same labelled invariant: the normalized generators form the graph of their common algebra and the state remains tau. Capacity is continuous on the fixed padded output by Leung–Smith. The already-existing Bell-filter construction supplies same-profile representatives approaching a replacer, so their capacities approach zero. Greatestness attains Q_*. Continuous flagged paths fill every strictly positive intermediate value. Zero attainment is a separate exact question; it does not follow from arbitrarily small positive values. Real parameters are used here. Rational compiler families give dense values/closures when their base compiler outputs are rational, not every real capacity value as an exact rational model.

The all-dimensional Bell dilution, qubit spectra, finite broadcasting laws and inverse-linear recovery exponent reported in N1708 are prior family capital. This general interval argument does not promote them to new discoveries or identify zero capacity with symmetric extendibility.

## 12. Status, novelty and dependency ledger

“Proved here” means a mathematical proof is supplied and has been challenged by the three-researcher process. It does not mean external peer review, experimental validation or established historical priority.

| Claim | Status | Dependencies and novelty boundary |
|---|---|---|
| Finite profile equality iff labelled faithful-state algebra isomorphism; greatest and minimum representative | Prior N1698 capital; core proofs independently reconstructed | Physical path tests to moments are the family-specific bridge. Faithful-state algebra theory, conditional expectations and Petz recovery are established. |
| N1690 general complete-order evaluator and historical capacity fixture | Inherited/source-reported; original packages unacquired | Not inferred from the new equality witness or from a successful finite script. |
| W: polynomial-bit faithful rational inequivalence witness | Proved here at explicit rational Choi input scope | Known short-word closure plus the physical path/tail or univariate-grid operation. Improves the acquired finite-witness scope; no efficient experiment follows. |
| P: 2m+1 fixed rational separating probes | Proved here; generic selector not executed | Sontag dimension mechanism plus effective semialgebraic rational selection; no polynomial preprocessing or bit bound. |
| S: conditioned Hölder inverse up to output unitary | Proved application | Basu–Mohammad-Nezhad after full generation and compactness are proved. Choi floors alone are insufficient. |
| Conditioned proper-stratum Lipschitz concrete lifts | Proved in supporting audit | A common spanning word list, fixed dimension, positive singular-value and Omega margins; a theorem from Choi data, not a noisy-profile inverse. |
| D: fixed-Omega full-Choi antidegradable capacity-ceiling jump and Theta(t^-2) promised-pair acquisition | Proved; exact finite certificates executed and independently replayed | Fresh explicit matrix fixture; coherent-information and symmetric-extension imports. Ordinary physical Q of every source channel is zero and remains continuous. |
| T: exact greatest trace-class realization iff countable finite matrix blocks, for tracial invariants | Proved here | Moment/GNS classification and Bayes-envelope bridge, with established atomic normal-realization predecessors. |
| A: finite external universal envelopes under supplied tracial filtration | Proved here | Conditional expectations, finite block lifts and Schatten estimates; finite approximants generally leave the exact class. |
| B: exact-class approximate greatest members iff injectivity/hyperfiniteness | Proved here, with verified Connes import | Haar inside-class repair plus the profile/Bayes-deficit-to-hypertrace bridge checked here, against substantial existing instrument and amenable-trace theory. Equivalence of pointwise-common and uniform existence is proved; no uniformization of a particular sequence is claimed. |
| Explicit L(F_2) obstruction and general finitely-generated realization lemma | Proved here | Applies known free-group nonamenability; infinite output with an explicit trace-norm description, not finite rational Choi input. |
| O: paid adaptive approximate simulator including full-environment alignment | Proved application with dilation refinement | Standard PBT and exact supplied heralded converter; iid memoryless resources, fresh input, communication, large local measurement, storage and noise costs are retained. |
| Complete RLD order fails to imply canonical processing | Proved at exact physical reference interface | Known less-noisy/degraded separation plus an explicit operator-reference lift. |
| General finite capacity-spectrum interval shape | Proved routine consequence | Existing Bell dilution, flagging, greatestness and capacity continuity. General zero attainment remains unresolved here. |
| N1708 broadcasting/support-module/finite-memory/inverse-linear results | Prior reported family capital | Current visible returns acquired; held full proof/compiler packages not silently promoted to reproduced results. |
| Nontracial infinite criteria, practical advantage, ordinary capacity algorithm, priority | Not achieved / open here | No claim follows from the deposit, scripts or smooth finite approximants. |

## 13. Decisive remaining operations and constructive attacks

1. **Remove the tracial restriction.** The step that currently fails is explicit: pinching a density at a general likelihood spectral cut need not preserve a nontracial invariant state, and Haar averaging may change that state. First determine the state-preserving normalized UCP extensions required by same-profile simulators, using maximal-equality multiplicative domains. Seek a modularly compatible substitute for the Bayes cut and the Haar lift. Do not extrapolate the finite-matrix-block condition to a nontracial B(H) block carrying a faithful normal density.
2. **Make the hyperfinite construction effective, or identify a precise obstruction.** B proves existence of a filtration and of inside-class approximate greatest sources. It does not extract a filtration/modulus from an arbitrary description. A supplied conditional-expectation circuit with verified L2 error on the finitely many T(E_ij) already yields a checked diamond certificate through A. That is a concrete compiler interface to pursue. General moment microstates are insufficient: normal CP target simulators and preservation of the invariant state are the missing operations.
3. **Turn conditioned profile calibration into an efficient acquisition procedure.** P and S give a finite exact identifiability theorem and a promise-dependent error modulus. The next operation is an explicit probe design and inversion algorithm with controlled algebra margin, coefficient growth and samples, compared with Jenčová deficiency/guessing-game methods. D rules out a repair based only on full Choi rank and a fixed floor. It does not rule out a genuinely promised calibration theorem.
4. **Characterize zero-capacity attainment in a general finite profile class.** Bell dilution proves infimum zero, not attainment. Existing all-dimensional broadcasting criteria identify a particular antidegradable route; they do not automatically classify every possible zero-capacity mechanism. Test singular classes and protected unitary factors against exact Choi extensions and coding bounds before asserting an equivalence.
5. **Improve the actual processor in O.** Polynomial primitive calls are already supplied by established PBT. The decisive practical operation is a much smaller verified online measurement/storage representation with a noise budget that survives the full block. Current generic POVMs have dimension a^(M+1), and a fixed program-state error accumulates as nM e. No fixed-noise or laboratory advantage has been established.
6. **Resolve historical priority of B at the correct interface.** Compare the full theorem, including fixed finite input, all referenced maximal profiles, exact-class membership, trace-class normal outputs and the universal target quantifier, against quantum experiment comparison and amenable-trace literature. The older injectivity, reverse-test and finite approximation theorems must remain credited. A search result failing to match the words of B is not enough.

The strongest remaining candidate opening after the priority correction is B's bridge between a complete information profile and amenability of the generated operator algebra. Its practical consequences remain to be constructed. It does not by itself supply a communication advantage, an effective amenability test or a general capacity algorithm.

## 14. Research record and execution boundary

The [record directory](MAXIMAL_INFORMATION_RESEARCH_RECORD/README.md) retains all four initial reports, all substantive challenges, corrected follow-ups, pinned Astra source returns, primary-literature manifests and executable checks. The [record ZIP](COMPLETE_MAXIMAL_INFORMATION_RESEARCH_RECORD.zip) contains the same materials. Its machine-readable theorem ledger mirrors Section 12.

Exactly three GPT-6.1 Sol maximum-reasoning subagents and the principal were used for this round. Independent initial reports preceded mathematical exchange. Follow-ups reused the same three researchers. No further agents, experiment, quantum hardware, large generic semialgebraic selector or generic high-dimensional PBT compilation was used. Total model-token and hardware-resource costs were not metered; no numerical full-cost advantage is claimed.

New local exact scripts verify nontracial ordered-word extraction, the rational physical witnesses, the reference-necessity fixture, the order obstruction, the 32-dimensional symmetric extension, fixed-Omega perturbation, nonvanishing commutant polynomial and resource budgets. Small PBT processors at M=1,2,3 were checked numerically to about 1e-15; those checks are diagnostics, not proofs of all-port error bounds. The infinite-output proofs, Connes import and hypertrace argument are analytic, not certified by finite scripts.

The source-return corrections and failed overclaims are retained: unacquired original packages, nontracial-state cyclicity, incomplete support padding, fixed-rank versus Choi-rank promises, full-environment versus receiver-only error, a full finite-algebra lift versus its smaller generated algebra, and common-pointwise versus per-target source sequences. Original independent notes are not retroactively rewritten. No prior manuscript or public release has been altered in this research round.

## 15. Dedicated historical-priority pass

The user explicitly requested this additional pass to avoid duplicate papers. Full query and citation trails, primary theorem hypotheses, and actual subsumption tests are retained in [priority_structural.md](MAXIMAL_INFORMATION_RESEARCH_RECORD/followups/priority_structural.md), [priority_principal.md](MAXIMAL_INFORMATION_RESEARCH_RECORD/followups/priority_principal.md), and the finite/construction priority reports. Mathematical proof status is separate from historical novelty.

The closest older structural result is **Okamura–Ozawa, [Measurement theory in local quantum physics, arXiv:1501.00239v3](https://arxiv.org/pdf/1501.00239v3), Theorems IV.1, IV.3, IV.4 and the paragraph immediately after IV.4, p17**. Exact normal extensions of all instruments, with range in the original algebra, characterize atomicity; the point-ultraweak approximate extension property characterizes injectivity. The singleton-outcome identity instrument reduces this to normal expectations and approximate normal retractions. Thus the broad atomic/exact versus injective/approximate physical-realizability pattern is established. B is not a new general trichotomy. The older theorem does not directly assert one source inside a fixed exact complete-profile fiber uniformly dominating all its targets in diamond norm. Whether the checked Bayes/Haar bridge is an original refinement remains a narrow priority question.

The extension machinery is older still. **Anantharaman–Delaroche, [Amenable correspondences and approximation properties for von Neumann algebras](https://msp.org/pjm/1995/171-2/pjm-v171-n2-p02-s.pdf), Pacific J. Math.171 (1995), Corollary3.9, p331**, identifies a norm-one projection N->M with point-ultraweak normal CP approximate retractions, when modular automorphisms of a faithful normal semifinite weight on M are implemented in N. A trace makes that hypothesis automatic. **Lemma3.7, p328**, already supplies almost-central normal states with controlled trace restriction. **Brown, [math/0304009v2](https://arxiv.org/pdf/math/0304009v2), Theorems3.1.6, 3.2.2 and 6.3.3(4)**, supplies amenable/uniform amenable trace and hyperfinite-GNS criteria, retaining the correct normal trace restriction on the weak closure. The central-state and generator-extension parts of B are established machinery.

The topology difference is real but not a novelty certificate: densities 1+sin(nx) on the circle converge against every bounded test to the uniform density while staying L1 distance 2/pi away. Convexification or exact-state-extension lemmas might strengthen an earlier approximation result; they must be tested, rather than treating a different norm as automatically a new theorem. Here exact profile membership and the common-source quantifier are earned by the supplied constructions.

T also has strong antecedents: Størmer normal-projection atomicity, Holevo's diffuse-output warning, Kuramochi's discrete-POVM/fully-quantum equivalence, and **Kuramochi, [Directed-completeness of quantum statistical experiments in the randomization order, arXiv:1805.04357v2](https://arxiv.org/pdf/1805.04357v2), Theorems3–5 and p27**, on order completion in the larger von Neumann category and missing diffuse bounds for type-I outputs. T is a profile-specific application/extension of that structural theory.

Additional older operational precedents read by the principal include **Paterson, [Amenability and Translation Experiments](https://doi.org/10.4153/CJM-1983-004-6), Canadian J. Math.35 (1983), Theorem1**, reducing amenable-group translation-experiment deficiency to convolution approximation; **Matsumoto, [quant-ph/0511170v1](https://arxiv.org/pdf/quant-ph/0511170v1), Theorem3**, characterizing globally RLD-optimal classical reverse families in the faithful finite setting; and **Matsumoto, [arXiv:1006.0300v1](https://arxiv.org/pdf/1006.0300v1), Theorem3**, on maximal tangent-channel metrics through program simulation. They do not state B's full fiber theorem, but prohibit claiming statistical amenability, RLD reverse estimation or simulation-based extremal metrics as new.

A particularly strong information-theoretic predecessor is **Ganesan–Gao–Pandey–Plosker, [Quantum Majorization on Semifinite von Neumann Algebras, arXiv:1909.10038](https://arxiv.org/abs/1909.10038), JFA279 (2020),108650, Theorem3.5**, characterizing injectivity of semifinite M by a conditional-min-entropy/projective-tensor norm equality with an infinite ancillary algebra. **Theorems3.13 and3.18** characterize exact and cb-norm approximate channel postprocessing under injective output-algebra hypotheses. Choosing their physical output B(H) tests each deficiency even when the hidden normalized algebra is noninjective; it does not select a common exact-profile source. Choosing the hidden M as output instead changes the physical category and assumes injectivity. B is not the first information-theoretic characterization of injectivity; the actual reduction check is in the constructor priority report.

**Jenčová, [Recoverability of quantum channels via hypothesis testing](https://doi.org/10.1007/s11005-024-01775-2), Lett.Math.Phys.114 (2024),31, Theorem4**, already relates preservation of all binary Bayes errors for trace-class state pairs under a channel to sufficiency. Here one must additionally turn tests for changing type-I realizations into exact-trace centrality of the generated algebra. Testing and recovery are established links; different terminology is not a contribution.

The finite lift has another close predecessor: **Bluhm–Capel–Costa Rico–Jenčová, [Belavkin–Staszewski Quantum Markov Chains](https://doi.org/10.1007/s00023-025-01644-1), AHP2025, Theorems5.7 and5.13**, gives whitened Petz-triple structure and normalized multiplicative-domain characterizations for supplied pair/channel saturation. **Corollary5.10 and Proposition5.11** give reconstruction, with complete positivity not automatically trace preservation. Thus whitening, ordinary block structure and sandwich reconstruction are old mechanisms. The extra finite-family burden is extracting the common algebra from complete physical tests and building one TP greatest source for every unrelated member of the fiber.

Recent sufficient/Jordan algebra papers were also checked: **Yamagata, [arXiv:2604.23292v4](https://arxiv.org/pdf/2604.23292v4), Theorem4**, requires likelihood inclusion AND modular closure; **van Luijk–Wilming, [arXiv:2604.08380v2](https://arxiv.org/pdf/2604.08380v2), Theorem5.1 and Theorem8.5/Corollary8.6**, concerns PTP-equivalent experiments and actual Neyman–Pearson tests of rho-t sigma. Equal complete maximal profiles are not by definition PTP equivalence, and the normalized cuts T(H)-tI are not automatically those physical output tests. The exact version/interface comparisons are retained in the finite priority report.

A final actual reduction was tested in [the ordinary-experiment addendum](MAXIMAL_INFORMATION_RESEARCH_RECORD/followups/addendumpriority_generic_experiment.md). The abstract tracial experiment K(X)=aT(X) in L1(M,tau) is CPTP, and every F is its ordinary coarse graining R_F(aB)=Omega_F^.5 pi_F(B) Omega_F^.5. A finite faithful affine basis subexperiment has minimal sufficient algebra M. Its exact ordinary type-I realization criterion is already a minimal-sufficiency/normal-expectation consequence. **Guţă–Jenčová Theorem3.16** does not give the desired general approximation theorem: it requires uniform domination of canonical states and type-I/discrete-center approximating sufficient algebras; its proof also places the limit in an atomic central summand. It cannot cover diffuse hyperfinite K. No generic published Le Cam approximation-iff-injectivity theorem at the needed scope was verified. Such a result would still need an exact-fiber lifting lemma and the converse from physical-target dominance to recovery of K. **Jenčová2024 Theorem5 and Remark3** give a strong binary-deficit recovery bound for trace-class pairs through an existing channel, with finite projective metric for a nontrivial estimate, rather than the arbitrary von Neumann approximation statement.

One recent comparison remains only partially inspected. **Morgan Jones, [arXiv:2610.16270v1](https://arxiv.org/html/2610.16270v1)** studies divergence fragility between two CP maps and continuity in their Arveson–Radon–Nikodym coordinate. It does not state D's optimized exact-profile capacity ceiling. The expanded [Hexagon book v1](https://hexagonmath.org/2610.00611v1), *Continuity, Testing Regions and Fragility of Quantum Channel Divergences*, was located at its primary deposit; its abstract, contents and opening theorem summaries were retrieved. Further theorem-passage requests timed out, and a direct in-memory PDF request returned HTTP403. It is not represented as fully audited. This leaves a specific recent priority lead unresolved; title or abstract differences do not clear it.

**Current publication verdict:** no directly subsuming primary theorem for B's fixed profile, exact in-fiber sources and universal diamond quantifiers was verified. This is not historical clearance. The broad structural pattern is known. W likewise requires careful framing: N1698 already constructs physical witnesses from differing words; the polynomial-bit analysis strengthens the acquired stated bound but may already occur in the unacquired compiler package. It is not a new word-equivalence algorithm. D's explicit full-support profile fixture is distinct from a generic rank-instability observation, but instability and statistical t^-2 acquisition scaling are old phenomena.

Separate novelty papers are not justified by PBT, generic 2m+1 identifiability, semialgebraic Holder estimates, binary reverse tests, word-closure algorithms, normal-expectation atomicity or injectivity theory alone. Any potential paper should center the actual complete-profile classification and its dictionary to greatest representatives, credit the older extension theory immediately, and retain the precise remaining priority uncertainty. No public release was made in this round.
