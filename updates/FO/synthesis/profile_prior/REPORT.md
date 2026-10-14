# Profile circulation: proof reconstruction and primary-source comparison

**Scope.** This is a targeted mathematical audit of `work/FM-sources/resonant/PROFILE_CIRCULATION.md`, with particular attention to (i) the two-amplitude profile-circulation identity, (ii) the six signed area moments for quartic integrands, (iii) the finite opposite-carrier graph calibration for (G), and (iv) whether the result transfers from N794/N812 or follows from laminate/calibration theory. This is not exhaustive novelty clearance. Literature versions and read depths are in [READ_LEDGER.md](READ_LEDGER.md); downloaded third-party PDFs are kept under `primary/`.

## Finding

The cancellation theorem is a valid, exact sufficient criterion for all-affine Jensen positivity of every rank-one-convex polynomial of degree at most four on (mathbb R^{m\times2}), for the specified two-profile fields. Its mechanism is an exact rank-one Bregman decomposition plus a profile-space line integral; Green's theorem reduces the latter to six signed winding-area moments. This gives an energy-independent family of compatible fields. It is not a theorem that the resulting gradient law is a laminate: the proof cancels polynomial one-forms of degree at most three, while laminate Jensen requires every rank-one-convex test.

The separate graph certificate is more than a reformulation. It establishes a quantitative all-background inequality for **every finite closed walk** in one specified 81-vertex, five-width graph for (G), even though 104 individual raw edges have negative action. Telescoping an exact potential removes all enumeration over closed walks. The result remains a finite-library/single-energy statement, not a calibration for arbitrary profile paths or arbitrary integrands. It is complementary to N812's single-carrier families, not a generalization of them.

The strongest potential superseding result found is Pedregal's arXiv:1905.06571v5 (18 June 2026), Theorems 1.1–1.2, which **claims** every homogeneous gradient Young measure in (2\times2) is a laminate, equivalently rank-one convexity implies quasiconvexity in that dimension. I read its fixed-point setup and the full proof-critical Section 7. I do not accept the claim as established by this audit: Proposition 7.1's Step 2 passes from local openness/full linear span and dimension matching to surjectivity over the feasible split parameters, without a proof that the image of the constrained feasible set is the whole gradient space. Local openness and full span do not imply surjectivity. This is a proof gap in the submitted argument as read, not a counterexample to the theorem. If the theorem is independently repaired, it would subsume every compatible (2\times2) profile result here. It says nothing for target dimension (m>2).

## Reconstructed profile theorem

Let (F:\mathbb R^{m\times2}\to\mathbb R) be (C^1) and rank-one convex. For a smooth periodic potential φ on a rectangular two-torus, write

\[
 P=(\phi_x\mid0),\qquad Q=(0\mid\phi_y),\qquad
 R_F(C,Z)=F(C+Z)-F(C)-DF(C)[Z].
\]

Both (P,Q) have rank at most one. Direct expansion—not an estimate—gives for every constant (B)

\[
F(B+P+Q)-F(B)=R_F(B+Q,P)+R_F(B,Q)
 +DF(B+Q)[P]+DF(B)[Q]. \tag{1}
\]

Rank-one convexity makes both remainders nonnegative. The (y)-mean of (DF(B)[Q]) is zero because it is linear in φ_y. Treat (U(x)=\phi(x,\cdot)) as a closed path in the space of periodic profiles, and set

\[
\alpha_{F,B}(U)[V]
 =\mathbb E_y DF(B+(0\mid U_y))[(V\mid0)]. \tag{2}
\]

Then α evaluated on (U_x) is exactly the remaining term in (1), so the normalized Jensen gap is the integral of the two nonnegative remainders plus the single circulation ∮α. This proves the identity for arbitrary smooth periodic φ; it does not assert that the circulation has a sign.

Now choose two fixed smooth profiles ψ₁,ψ₂ and write

\[
\phi(x,y)=r(x)\psi_1(y)+s(x)\psi_2(y).
\]

For polynomial (F) of degree at most four, the two coefficients of the pulled-back α are polynomials of degree at most three in ((r,s)): (DF) has degree at most three and (B+(0\mid r\psi_1'+s\psi_2')) depends affinely on ((r,s)). Therefore the circulation is a linear combination of ∮ (r^i s^j,dr) and ∮ (r^i s^j,ds) for (i+j\le3).

For a closed piecewise-(C^1) amplitude curve (a=(r,s)), let (w_a) be its signed winding number and

\[
M_{ij}=\int_{\mathbb R^2} w_a(r,s)r^i s^j\,dr\,ds,
\qquad i+j\le2.
\]

Green's theorem gives ∮ α (=\int w_a(\partial_r\alpha_s-\partial_s\alpha_r),drds); the curl has degree at most two. Thus the six equations

\[
M_{00}=M_{10}=M_{01}=M_{20}=M_{11}=M_{02}=0 \tag{3}
\]

kill every possible quartic profile circulation for every (B), every pair ψ₁,ψ₂, and every rank-one-convex quartic (F). The six are also the complete list of independent area moments needed to annihilate all polynomial one-forms of degree at most three: any polynomial curl (p(r,s)) of degree at most two is realized by αₑ=0, αₒ(=\int_0^r p(t,s)dt); the other cubic line-integral monomials reduce to these by integration by parts. With (3), (1) proves (J_F(B,D\phi)\ge0) for all (B).

There is a quantitative strengthening. For a rank-one (Z), restriction (f(t)=F(C+tZ)=At^4+Lt^3+C_2t^2+Dt+E) is convex on ℝ. When (A>0), (f''\ge0) implies (C_2\ge3L^2/(8A)), and

\[
f(1)-f(0)-f'(0)-A/3
=\frac{3(L+4A/3)^2}{8A}+C_2-\frac{3L^2}{8A}\ge0.
\]

For (A=0), global nonnegativity of (f'') forces (L=0,C_2\ge0), giving the same bound. Define μᶠ as the minimum of the homogeneous quartic part (F_4) on unit rank-one matrices. Each remainder in (1) is at least μᶠ times the fourth power of its increment divided by three. Since (x^2+y^2\ge(x+y)^2/2), this yields

\[
\inf_B J_F(B,D\phi)\ge\frac{\mu_F}{6}\,\mathbb E|D\phi|^4. \tag{4}
\]

The proof is independent of rotational invariance and target dimension. For two profiles, (3) is a complete annihilator of the circulation term, not a complete characterization of when the original field has nonnegative Jensen gap. The construction does not show that the new field preserves the energy of a starting path.

The source's illustrative third finite difference is exact. For a unit square Γ and (v=(2,0)), the oriented current Γ − (3T_v\Gamma+3T_{2v}\Gamma-T_{3v}\Gamma) kills translations of every polynomial one-form of degree at most three: its integral under translation by (tv) is a polynomial in (t) of degree at most two (the potential cubic coefficient is a constant one-form around a closed loop and vanishes), so its third finite difference is zero. The six moments vanish, but (M_{30}=-48) and ∮ (r^4ds=4M_{30}=-192). This is a construction of a different compatible field with a nonzero higher-order current, not an energy-preserving reduction of an arbitrary test field.

## The finite opposite-carrier calibration for (G)

For profiles (U_{r,s}(y)=r e^{iy}+s e^{-iy}), interpreted as real two-component profiles, a directed edge (U\to V) of width τ is the actual compatible strip

\[
\phi(x,y)=(1-x/\tau)U(y)+(x/\tau)V(y),\quad 0\le x\le\tau.
\]

The graph has vertices (r,s\in\{0,1/4,\ldots,2}), so 81 vertices, and widths {1/8,1/4,1/2,1,2}, giving (81^2\cdot5=32{,}805) directed edge/width choices. For each edge, its action (W_B(U,V,\tau)) is the exact strip integral of (F(B+D\phi)-F(B)). The certificate uses (B=0) and the adjusted edge cost

\[
w_e=\int G(D\phi_e)-\tfrac14\int|D\phi_e|^4.
\]

A rational vertex function (P) satisfies (w_e\ge P(V)-P(U)) on every edge/width. Summation around any finite closed walk telescopes (P), proving the zero-background quartic lower bound even when some individual edges have negative action. The source algorithm computes exact rational Laurent-polynomial means, exact edge costs, takes the minimum adjusted cost over widths for each ordered pair, runs Bellman–Ford from zero labels, and checks all 32,805 edge inequalities exactly. The supplied certificate reports common denominator 245760, eight Bellman passes, 93 tight constraints, 104 negative raw edges, 2,046 negative adjusted edges, and minimum slack zero. This audit inspected the proof source and supplied certificate but did not run the source verifier.

For every such closed walk the two carriers are odd under (y\mapsto y+\pi), so (X=D\phi) changes to −(X). The mean (X) and cubic moments vanish. For homogeneous quartic (G), its all-background gap is consequently (c+\tfrac12 B^THB), where (c=\mathbb E G(X)) and (H=\mathbb E D^2G(X)). The quartic polarization identity gives (D^2G(X)[B,B]=D^2G(B)[X,X]). Fourier expansion of (X=D\phi), Parseval and rank-one convexity make (B^THB\ge0): every real/imaginary Fourier coefficient of a potential mode produces a rank-one real matrix. Thus the graph certificate proves

\[
\inf_B\mathbb E[G(B+D\phi)-G(B)]\ge\tfrac14\mathbb E|D\phi|^4
\]

for all finite closed walks over that exact graph. This supplies positivity for an infinite set of walks (unbounded walk length), but only for one (G), this carrier pair, these vertices and these widths.

The rational acoustic witness for (G) has a skew completion (K) with upper-left six-dimensional block leading principal minors (107/2,642,1605/8,8445/16,2815/8,26865/4), and zero final Schur complement. This is an all-directions rank-one-convexity certificate, not angular sampling. It is distinct from the graph potential: the former validates the rank-one-convexity premise; the latter certifies the finite library's compatible actions.

## Primary results and exact transfer boundaries

| Primary source/result | Reconstructed theorem or proof mechanism | Relation to this profile work |
|---|---|---|
| K. Astala, T. Iwaniec, I. Prause, E. Saksman, *A hunt for sharp (L^p)-estimates and rank-one convex variational integrals*, arXiv:1403.1095v1, Proposition 5.1 | For rank-one-concave (E), their radial map (f(x)=\Lambda(|x|)x) obeys an integral comparison obtained by applying a rank-one tangent/supporting inequality to its radial derivative component on spheres and integrating. Apply (E=-F) for a rank-one-convex Jensen form. | A genuine positive integrated class and close method precedent, but the geometry is radial; it is not the arbitrary two-profile path, its six-moment cancellation, or the opposite-carrier graph. |
| T. Lyons, D. Yang, arXiv:1503.06175v2, Theorem 5 and surrounding construction | Polynomial one-forms of bounded degree are represented as closed one-forms on a finite-step nilpotent group, preserving their path integrals; signatures encode these finite-order path functionals. | Establishes the general path-data framework. It neither supplies the rank-one Bregman decomposition nor proves Jensen positivity; the six-moment fact here follows directly from Green's theorem. |
| S. Müller, V. Šverák, *Convex integration with constraints and applications to phase transitions and PDE*, JEMS 1 (1999), Theorem 3.1, Corollary 1.5 | A laminate is a measure satisfying Jensen for every rank-one-convex function. Their Theorem 3.1 approximates any such laminate supported on compact (K) by finite-order laminates in any open neighborhood of (K^{rc}); it does not turn a general gradient Young measure into a laminate. Their four diagonal wells have no rank-one connections while the functional rank-one-convex hull contains a square, so finite splitting and functional rank-one convexity differ. | Explains why finite path moments do not by themselves prove “is a laminate.” It supplies abstract finite-order approximation once laminate status is known, not a universal profile calibration or a moment-cancellation theorem. |
| G. Bruno, F. Pasqualotto, arXiv:2608.06367v1, Theorems 1–2 and Appendix A | Proves rank-one convexity implies quasiconvexity for the Dacorogna–Marcellini energy range and for homogeneous quartics invariant under both left and right planar rotations, using a heat/exact-form method. | (G) is not right-(SO(2))-invariant: for (A=\mathrm{diag}(2,1)), (G(A)=31/3), whereas (G(A R_{\pi/2})=83/24). Thus that theorem does not cover this (G). |
| P. Pedregal, arXiv:1905.06571v5, Theorems 1.1–1.2 | Claims each (2\times2) homogeneous gradient Young measure is a laminate by a Kakutani fixed-point argument coordinating (H_n)-decompositions on a three-normal triangulation; concludes rank-one convexity implies quasiconvexity for all two-component maps. | If valid, it strictly subsumes all compatible (2\times2) profile inequalities here, without needing moments or a graph. The proof-critical surjectivity in Section 7 is not closed in the paper as read (see next section), so treat it as an unreviewed preprint claim, not an established theorem. It does not cover (m>2). |

Bernard's closed/holonomic measure framework supplies a useful loop/action analogy, but its hypotheses concern Tonelli/fiberwise-convex Lagrangians. No result there found in this audit transfers to the nonconvex rank-one profile action. Likewise, graph shortest-path duality is standard: on a finite directed graph, no-negative-cycle is equivalent to a vertex potential satisfying the edge inequalities. The graph's mathematical content is the compatible edge-cost computation and exact certificate, not a new graph-duality theorem.

## Pedregal v5: scope and proof-critical audit

The arXiv record lists v1 (16 May 2019), v2 (27 September 2019), v3 withdrawn (29 August 2024), v4 (12 May 2025), and current v5 (18 June 2026). The withdrawal reason for v3 is not stated in the record and is not inferred here. The paper's abstract, Theorem 1.1/1.2, Sections 3–7 and conclusion were read; the high-risk passage is Theorem 1.1's reduction through Proposition 7.1, not the standard Kakutani theorem itself.

The proof sets a compact convex weight set Θₗ and a set-valued map (T) matching decomposition directions from the two scalar components. Section 6 checks upper semicontinuity, compactness and convexity of (T(t)), contingent on nonempty values. Section 7 seeks nonemptiness by fixing (u,t), varying split parameters (S), enforcing cross-interface linear constraints and requiring final leaves to lie on opposite sides of interface barycenters (Claim 7.5). For generic ((u,t)), it argues the (S\mapsto\tilde U) linear operation has full range and that the feasible image contains a neighborhood of the original (u). The next inference says that dimension matching and linearity imply the image over the whole feasible set is all of ℙₗ.

That inference is not proved by the preceding facts: a proper convex subset (for example a ball) can have nonempty interior and full linear span. The feasible set includes convex-side inequalities, so its image is not established to be a vector subspace. Surjectivity for every target (w\in\mathbb P_l) is essential to show (T(t)\ne\varnothing), which is essential to apply Kakutani and conclude every discrete gradient law is a laminate. I therefore mark Pedregal's headline theorem **unverified / proof gap identified**, not false. The version history and proof gap make it unsafe to cite as a settled superseding theorem.

## N794 and N812: the exact comparison

N794's retained energy is

\[
F^*(A)=u^2+v^2+4w^2+\tfrac72q^2-\tfrac{29}{10}q(u+v),
\]

and its internal closed-heat certificate is for (F^*-(83/1000)q^2): a closed homogeneous-quadratic two-form and a positive rational compatible-jet Gram yield quasiconvexity and the stated (1/36000) Jensen gap. Correct direct evaluation at (I) uses (u=v=q=1,w=0): (F^*(I)=1+1+0+7/2-29/5=-3/10). It is not the graph-calibrated energy.

N812's energy is

\[
G(A)=3(u+v-2q)^2+\tfrac{35}{24}u^2+q^2-\tfrac52qu.
\]

It has (G(I)=-1/24), is rank-one convex by its own acoustic Gram, and is not right-rotation invariant by the calculation above. N812 proves all-background positivity for the broad one-carrier family φ(x)=r(x)V(k\cdot x)), with a closed convex carrier (V) and arbitrary scalar amplitude (r); it also proves a one-coordinate complex-envelope family and other stated restricted completions. The independent two-carrier profile is

\[
U_{r,s}(y)=(r+s)\cos y+i(r-s)\sin y.
\]

It is a scalar multiple of one fixed profile only when (r-s) and (r+s) keep a fixed ratio (a one-dimensional amplitude subfamily). Thus N812's one-carrier identity does not directly prove the whole independent ((r,s))-loop class. Its packet assembly needs exact joint degree-four moment factorization; the source gives a compatible determinant-square example where unrestricted additivity fails.

The finite (G) graph certificate is therefore genuine additional **restricted** mathematical power over N812's single-carrier theorem: it covers nonzero circulation and exact interacting opposite carriers with a uniform (1/4) all-background quartic margin, on every closed walk of the finite graph. It is not a new universal positivity mechanism for all profiles. N794's heat identity for (F^*) cannot be transferred to (G) by naming them both quartics, by their values at (I), or by comparing coefficient vectors. I did not derive a valid invariant separating (G) from the positive cone of right-(GL(2)) transforms of (F^*) plus (q^2); that relation is left **UNKNOWN**. The earlier attempted even-part rank argument is invalid because (q^2=uv-w^2) contributes to the even Gram form.

## Status, cost, and decisive next gate

The exact profile identity and six-moment implication are analytic arguments reconstructed from the frozen source. The graph certificate's mathematics is the exact shortest-path witness plus rank-one convexity/Parseval argument; this audit did not execute the source's nine-group verifier, so its finite-rational replay remains a producer receipt rather than an independent replay. The Pedregal proof issue is a textual/logical audit of the stated surjectivity step, not a formal counterexample to its theorem. External correctness, external review, comprehensive historical priority and novelty remain **UNKNOWN**.

All source operations are mathematical. No physical measurement, experimental acquisition, calibration, noise, conditioning or external service acquisition is involved. The graph enumeration covers 32,805 exact rational edge/width computations; source reports 5.1156 seconds on its recorded machine for certificate construction, but machine identity and independent timing are not established here. Literature-download expense and investigator time were not measured. No aggregate inference cost is available.

The decisive next mathematical gate is independent scrutiny of Pedregal v5's feasible-set surjectivity argument, plus an exact audit of whether the N794 closed-heat certificate cone contains (G) after allowed right-(GL(2)) operations and determinant-square addition. Until then, the defensible conclusion is: six moments completely cancel the quartic circulation; the finite graph proves a separate exact (G) family; neither result closes arbitrary-gradient compatibility.
