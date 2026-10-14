# Post-isolation critique: phase geometry and global moments

## Finding

I found no fatal counterexample to either incoming theorem at its stated scope. The non-affine phase theorem has a sound route from its signed curvature identity to positivity at every affine background: the weighted curvature conditions make the defect average vanish; the amplitude half-turn makes the affine linear coefficient vanish; and compatibility plus rank-one convexity makes the remaining affine Hessian positive semidefinite. The global-moments construction also has a correct atomwise PSD completion for its modulation family, and its polar argument identifies the **closed conic hull** of those family moments with the dual of the rank-one-convex cone.

The distinction that remains decisive is the one the reports themselves state: these results do not put the moment vector of every compatible periodic gradient into that closed cone. The connected-triad example rules out two direct profile templates or the current support-partition recipe; it is not a separating functional, a failed PSD completion, or a negative Jensen gap.

Two presentation points need care but do not invalidate the results. First, the non-affine report omits the cubic-in-background term in its displayed quartic expansion. It vanishes because (D^3F(X)) is linear in (X) and every periodic gradient has zero mean. Half-turn symmetry is needed for the separate coefficient ⟨DF(X)⟩, which is cubic in (X). Second, “ellipse modulation” is an imprecise name for the rank-one sine test used in the polar proof. If the allowed loops are required to be nondegenerate ellipses, the sine test is still obtained as a limit of such ellipses; the polar conclusion survives by continuity.

## Reconstructing the non-affine theorem

For (P=rW\otimes k), (Q=V\otimes\nabla r), and θ with (k=\nabla\theta), differentiate

\[
\mathcal A_i(x)=\int_0^{r(x)}DF(B+sW(\theta)\otimes k)[V(\theta)\otimes e_i]ds.
\]

The upper-limit term is (DF(B+P)[Q]). The (V'=W), (W'=-aV) phase terms yield (F(B+P)-F(B)) and the negative acoustic integral. Differentiating the variable (k) contributes (+\mathcal E_F) to (\operatorname{div}\mathcal A). Since the periodic divergence averages to zero, rearranging the rank-one Bregman identity gives

\[
\langle F(B+D\varphi)-F(B)\rangle
=\langle\mathcal R_F(B+P,Q)\rangle
+\left\langle a(\theta)\int_0^r sD^2F(B+sW\otimes k)[V\otimes k,V\otimes k]ds\right\rangle
-\langle\mathcal E_F\rangle.
\]

The sign is consequential: rank-one convexity signs the first two terms, but not the mixed-Hessian defect. The formula is valid for negative (r) as well: (\int_0^r sG(s)ds=r^2\int_0^1 tG(tr)dt). It also has no division by (r), (V), or (k), so zeros and degenerate loop points are harmless. On the torus with the stated smoothness, all terms are integrable; no separate growth condition is needed for these quartic polynomials.

For the circular carrier and a homogeneous left-\(\mathrm{SO}(2)\)-invariant quartic, only the orientation-odd coefficients (L,M,N) contribute at zero background. Direct differentiation gives

\[
\Xi(k)=(Lk_1^2+Mk_2^2+Nk_1k_2)(k_2,-k_1),\qquad
\mathcal E_F=\frac{r^4}{4}\operatorname{div}\Xi(\nabla\theta).
\]

With (\theta=ny+g(x)), this becomes

\[
\operatorname{div}\Xi=n(2Lg'+nN)g'',\qquad
\langle\mathcal E_F\rangle=\frac{n}{8\pi}\left(2L\int m g'g''dx+nN\int m g''dx\right).
\]

Thus (9) cancels the defect for every choice of (L,N). At (B=0), the two positive terms are (\mathcal R_F(P,Q)\geq0) and the acoustic term (r^4D^2F(W\otimes k)[V\otimes k,V\otimes k]/4\geq0). Hence (c=\langle F(X)\rangle\geq0).

The half-turn (y\mapsto y+\pi/|n|) leaves (r,\nabla r,k) fixed and sends (V,W) to (-V,-W); so (X\mapsto-X). For a quartic, (DF) is odd and therefore (b=\langle DF(X)\rangle=0). For any periodic gradient (X), the cubic-in-(B) term in the exact expansion

\[
\langle F(B+X)-F(B)\rangle
=c+\langle DF(X)\rangle:B+\tfrac12 B:H B+
\tfrac16\langle D^3F(X)\rangle[B,B,B]
\]

is already zero because (D^3F) is linear and (\langle X\rangle=0). This fills the omitted line in the report's expansion. Finally, for every constant matrix (A), quartic polarization gives

\[
A:HA=\langle D^2F(X)[A,A]\rangle=\langle D^2F(A)[X,X]\rangle\geq0.
\]

To see the last sign, Fourier-expand (X=D\varphi). Each nonzero complex mode is (z\otimes\xi) with real (\xi); its real and imaginary parts are real rank-one matrices. Rank-one convexity makes both acoustic evaluations nonnegative, and Parseval sums them. It follows that the complete affine gap is (c+\frac12B:HB\geq c\), with equality at (B=0). This proves the stated infimum, including singular (H\), without a strict Legendre–Hadamard bound.

The defect cannot be dropped or assigned a sign. For (F_c=(u+v-2q)^2=\big((a-d)^2+(b+c)^2\big)^2), the linear map (A\mapsto(a-d,b+c)) followed by the convex function |z|⁴ shows global convexity. At (\theta=x+\sin y), its (\operatorname{div}\Xi=-4\sin2y). Pairing with (r^4=1\mp\frac12\sin2y) gives (\langle\mathcal E_{F_c}\rangle=\pm1/4) exactly. These amplitudes are smooth and positive after taking the fourth root. This is a defect-sign example, not a negative optimized gap.

The half-turn hypothesis also does real work in the all-background proof. Without it, for the convex quartic (F_0(A)=|A|^4), affine phase (\theta=y), and (r(y)=1+\varepsilon\cos y), direct integration gives the active-column component of (b=\langle DF_0(D\varphi)\rangle) as ((0,4\varepsilon)). Thus (b=0) cannot be inferred from periodicity or (\langle X\rangle=0) alone. This example does not refute positivity: the affine-phase flux identity proves that case directly. It shows why one cannot omit half-turn symmetry from this proof without a replacement bound for (b).

The explicit sheared profile does meet the hypotheses. Its (m(x)=\langle r^4\rangle_y=5603/5000) is constant, and at ((x,y)=(0,\pi/4)), (\det D\varphi=r r_y(h'-g')=-1/6\neq0). It therefore has full-rank gradients on an open set. The positivity theorem covers sign-changing or zero amplitudes too; the example happens to be strictly positive.

## Reconstructing the moment completion and polar statement

For a quartic, the first term of the global identity is

\[
\mathcal R_F(C,Q)=\int_0^1(1-s)D^2F(C+sQ)[Q,Q]ds.
\]

At each point, rotate output by (U\in SO(2)) with (Ue_1=V/|V|). In the N794 row-major coordinates, (D^2F(A)[V\otimes b,V\otimes b]=|V|^2z(A,b)^TQ_F(K)z(A,b)), where (z=(b_1x(A),b_2x(A))) and (x(A)=\operatorname{vec}(U^TA)). Substituting this acoustic Gram formula into the Bregman and acoustic integrals yields exactly (Y_B) in the incoming report. Its weights are ((1-s)|V|^2) and (a r^2t|V|^2), all nonnegative; hence it is an integral of PSD atoms.

The coefficient/skew correspondence checks out. If (K^T=-K), its full Gram perturbation is (\Delta Q=\begin{psmallmatrix}0&K\\-K&0\end{psmallmatrix}). For an acoustic vector (z=(b_1x,b_2x)), (z^T\Delta Qz=2b_1b_2x^TKx=0). For each atom (zz^T), its off-diagonal block is (b_1b_2xx^T), which is symmetric. Therefore (\langle\Delta Q,zz^T\rangle=0), exactly the six constraints (\langle C_j,Y_B\rangle=0). The other nine pairings recover the moment coefficients. Independently differentiating each of the nine basis quartics reproduces the acoustic blocks and the displayed rational example

\[
m=(3/128,227/128,17/128,0,0,0,0,0,0),\quad
Y=\operatorname{diag}(1/512,0,0,17/256,0,0,0,227/512).
\]

The original N794 dual equivalence has a strict-feasibility premise, rather than relying on an implicit closed-image assumption: the source supplies a positive-definite acoustic Gram for (F=|A|^4) after one skew completion. I reconstructed this Slater point and its principal minors in the independent check file. Thus the reports' use of the N794 moment-completion interface has the required finite-dimensional dual attainment behind it.

For the closed-cone claim, write (S_d) for the modulation moment set and (C_d) for rank-one-convex quartic coefficients. The identity proves (S_d\subseteq C_d^*). If (p\) is nonnegative on every (m\in S_d), take a nondegenerate ellipse

\[
V_\delta(t)=\alpha\cos t+\delta\gamma\sin t,\quad \delta>0,
\]

with independent (\alpha,\gamma\), and (\varphi_{\varepsilon,\delta}=\varepsilon V_\delta(k\cdot x)). For integer carrier (k), these are periodic members of the allowed loop family. As (\delta\to0), the averaged gap tends to

\[
\frac{\varepsilon^2}{4}D^2F_p(B)[\alpha\otimes k,\alpha\otimes k]
+\frac{3\varepsilon^4}{8}F_p(\alpha\otimes k).
\]

Nonnegativity, division by (\varepsilon^2), and (\varepsilon\to0) force the acoustic Hessian nonnegative. Density of integer directions supplies every real input direction by continuity. Therefore ((\operatorname{cone}S_d)^*=C_d), and finite-dimensional bipolar duality gives (\overline{\operatorname{cone}S_d}=C_d^*). If the family definition already admits the degenerate line loop, the limit is unnecessary; if it insists on strict ellipses, this limit repairs the wording. This proves a statement about the closed conic hull of the structured modulation moments only.

The connected triad is an obstruction to direct generation by the displayed loop/envelope templates and the support-partition rule. Its exact moment vector may still admit an N794 PSD completion or lie in the closed conic hull. No separator or negative Jensen gap is provided. The global compatibility inclusion for arbitrary gradients remains the missing theorem.

## Gate scope, source boundary, and verification

The original N794 review gate is open. It requires external proof/priority review and, for greater leverage, inclusion of the entire nine-coefficient acoustic rank-one cone in a valid closed heat-certificate cone or a rigorous separating obstruction plus a new compatibility mechanism. The two reports provide a modulation-family completion and characterize (C_9^*); they do not prove that arbitrary compatible-gradient moments admit such a completion. No N794 global gate is discharged here.

The original N809/FK proof covers full-35 planar quartics only near a simple transverse acoustic contact, with its rank-three PSD remainder, determinant balance, and relative (L^2/L^4) closeness assumptions. The original notice explicitly leaves rank-two tangent contacts, large-transverse profiles, global Morrey, and independent review open. The FL non-affine theorem is all-background but profile-specific; it proves neither the moving reduced-Schur estimate at a tangent contact nor an exact compatible negative gap. The N809 gate also asks for the global left-SO(2) compatibility-to-nine-moment completion or an exact separating profile, and independent validation/application of the multi-constraint result. It remains open.

N806/FJ supplies fixed-contact differential cubic compensation and contact-plane positivity for compatible near-line gradients. Its gate still asks for concentration-stable control against the reduced denominator (h_*) or an exact compatible negative optimized gap; the scoped notice says the reduced denominator can be much smaller than the unreduced Hessian on compatible fields. The phase-curvature identity is a different mixed-Hessian term and does not establish this estimate. None of these comparisons imports a prior general quasiconvexity theorem; the internally certified (F^*\) special case is not used to infer a cone-wide result.

The source reports and exact scripts were read from their original locations. The three replay scripts were copied into this owned `replay/` directory before execution; all outputs remained there. The source global verifier passed its nine groups; the phase-geometry verifier passed all logged checks; the moment bridge verifier passed its two exact example groups. A separate implementation passed 88 exact checks, including the nine acoustic coefficient maps, all six skew freedoms, strict Slater feasibility, the displayed dual moment pairings, the exact half-turn countertest, 35 quartic affine expansions, both defect signs, and the explicit full-rank profile point. These checks support the displayed algebra only; they do not formally verify the analytic proofs or provide external correctness or priority review.

The initial isolated packet at `work/FL-global-audit/` was not edited. Its original five-file hashes were checked before this review and are rechecked in the ledger. All writes for this critique are confined to `work/FL-global-audit/post_review/`.
