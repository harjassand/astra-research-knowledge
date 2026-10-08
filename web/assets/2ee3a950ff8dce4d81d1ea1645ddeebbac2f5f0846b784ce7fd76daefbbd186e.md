# Source reconstruction and audit notes

**Scope.** Stable-polynomial/determinant mechanisms in the pinned `openai/math` snapshot `adc7f1241b42e322a6451854ab7e4b4c146bf78a`. The assigned target is the October 5 manuscript *An Exact Semidefinite Lift of a Nonspectrahedral Hyperbolicity Cone*. This is a source reconstruction and a standard conic-duality consequence, not an independent proof audit of the whole manuscript and not a novelty claim.

## Pinned source set

1. OpenAI, *An Exact Semidefinite Lift of a Nonspectrahedral Hyperbolicity Cone* (Oct. 5, 2026), pinned PDF: <https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/An-Exact-Semidefinite-Lift-of-a-Nonspectrahedral-Hyperbolicity-Cone-October-5-2026/Exact-Semidefinite-Lift-of-a-Nonspectrahedral-Hyperbolicity-Cone.pdf>. Local copy and extracted text: `family_cone_lift/lift.pdf`, `family_cone_lift/lift.txt`. Git blob `5f5d99899e05ab637c4c1f40b3b9fa1487d81e2f`.
2. OpenAI, *A nonspectrahedral hyperbolicity cone* (Sep. 24, 2026), pinned PDF: <https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/A-Nonspectrahedral-Hyperbolicity-Cone-September-24-2026/nonspectrahedral-hyperbolicity-cone.pdf>. Local copy and extracted text: `family_cone_lift/cone.pdf`, `family_cone_lift/cone.txt`. This is the companion proof that the particular cone has no direct finite homogeneous LMI.
3. OpenAI, *Hyperbolicity Cones Without Semidefinite Lifts* (Oct. 5, 2026), pinned PDF: <https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/Hyperbolicity-Cones-Without-Semidefinite-Lifts-October-5-2026/nonliftable-hyperbolicity.pdf>. Local PDF: `family_cone_lift/nonlift/nonlift.pdf`. This is a distinct construction, relevant only as a source-reported counterexample to universal liftability; it was not independently reconstructed here.

Snapshot tree and GitHub file metadata are saved at `openai_tree.json`, `family_cone_lift/lift_files.json`, `family_cone_lift/cone_files.json`, and `family_cone_lift/nonlift/files.json`. The target PDF history returned one commit, the pinned initial commit (2026-10-06T21:58:50Z); this is provenance for this snapshot, not evidence of peer review or formal verification.

## Main exact theorem and determinant mechanism

The target paper takes (V=S^4\times S^4\times\mathbb R^3\cong\mathbb R^{23}), ordered by the ten upper-triangular coordinates of (X\), then those of (Z\), then (y_1,y_2,y_3\). It defines the coefficient-one Choi–Lam quadratic matrix
\[
Q(y)=\begin{pmatrix}
y_1^2+y_2^2&-y_1y_2&-y_1y_3\\
-y_1y_2&y_2^2+y_3^2&-y_2y_3\\
-y_1y_3&-y_2y_3&y_3^2+y_1^2
\end{pmatrix},
\]
the positive map \(\Phi_y:S^4\to S^4\) displayed in (2), and
\[
p(X,Z,y)=\det\big((\det X)Z-\Phi_y(\operatorname{adj}X)\big),\qquad e=(I_4,I_4,0).
\]
The determinant has degree 20 and (p(e)=1). Its closed hyperbolicity cone (K=\Lambda_+(p,e)) is the object represented.

The exact lift mechanism (target pp. 3–9) is:

* Cover (\mathbb R^3_y) by (Y_\theta(\eta,\xi)=\eta(\cos\theta,\sin\theta,0)+\xi(0,0,1)).
* Factor (Q(Y_\theta(\eta,\xi))=\widetilde F_\theta\widetilde F_\theta^T), with a (3\times4) realified factor whose entries are linear in \((\eta,\xi)\) and have angular degree at most 3.
* Stack the four skew-block maps (B(r_j)) built from its columns to obtain the symmetric size-20 pencil
  \[
  L_\theta(X,Z,\eta,\xi)=\begin{pmatrix}I_4\otimes X&B_\theta\\B_\theta^T&Z\end{pmatrix}.
  \]
  The block determinant identity proves \(\det L_\theta=p(X,Z,Y_\theta)\) first for invertible (X\), then for all (X\) by polynomial identity. Since \(L_\theta(e)=I_{20}\), this gives hyperbolicity and, on each angular slice, (K\iff L_\theta\succeq0\), including singular (X\).
* Replace angle evaluation by a linear functional \(\Lambda\) on the 330-dimensional space (E\) of degree-\(\le7\) trigonometric coefficients times the 22 slice coordinates. Impose \(\Lambda(X)=X\), \(\Lambda(Z)=Z\), \(\Lambda(Y_\theta(\eta,\xi))=y\), and positivity on (q^TL_\theta q\) for every (q\in(T_2)^{20}\). With (T_2=(1,\cos\theta,\sin\theta,\cos2\theta,\sin2\theta)\), this is (H(\Lambda)\succeq0\) for one (100\times100\) moment/localizing matrix.
* The load-bearing converse is the degree-two matching lemma (target Sec. 3): for (S\in S^3), (z\in\mathbb R^3\) with \((z_1,z_2)\ne0\), there is a degree-two trigonometric factor \(\widetilde C_\theta\) matching both its Gram matrix and its pairing with \(F_\theta\). These tests force the scalar inequality (23). Kernel tests give \(\operatorname{range}B_j\subseteq\operatorname{range}X\); a pseudoinverse test gives \(Z\succeq\sum_jB_j^TX^\dagger B_j\); completing the square yields (L_{\theta_0}\succeq0\) for a slice containing (y\). This proves exactness without representing arbitrary feasible \(\Lambda\) by a measure and without taking closure of the projected set.

The source specifies the 100-by-100 coefficient pencil by a finite coefficient rule, not by printing all matrix entries, and claims only the bounds (N=100,m=307), with no minimality assertion.

## Exact (x=e) moments and strict feasibility

Use the source basis of (T_7\):
\[
f_0=1,\quad f_{2r-1}=\cos(r\theta),\quad f_{2r}=\sin(r\theta)\quad(1\le r\le7).
\]
For a function (g\in E\), set
\[
\Lambda_0(g)=\frac1{2\pi}\int_0^{2\pi}g(\theta,I_4,I_4,0,0)\,d\theta.
\]
Let \(\mu_k=(2\pi)^{-1}\int f_k\), so 
\[
(\mu_0,\ldots,\mu_{14})=(1,0,0,0,0,0,0,0,0,0,0,0,0,0,0).
\]
This gives **all 330 coordinates** of \(\Lambda_0\): for every (i\le j\), (k=0,\ldots,14\),
\[
\Lambda_0(f_kX_{ij})=\mu_k\delta_{ij},\quad
\Lambda_0(f_kZ_{ij})=\mu_k\delta_{ij},\quad
\Lambda_0(f_k\eta)=\Lambda_0(f_k\xi)=0.
\]
In the source's 23-output order the ten (X) moments are
\[
(\Lambda X_{11},\Lambda X_{12},\Lambda X_{13},\Lambda X_{14},\Lambda X_{22},\Lambda X_{23},\Lambda X_{24},\Lambda X_{33},\Lambda X_{34},\Lambda X_{44})
=(1,0,0,0,1,0,0,1,0,1),
\]
the ten (Z) moments have the identical tuple, and the last three outputs are
\[
(y_1,y_2,y_3)=(\Lambda_0(\eta\cos\theta),\Lambda_0(\eta\sin\theta),\Lambda_0(\xi))=(0,0,0).
\]
Thus (O(\Lambda_0)=e\) exactly.

At these moments (L_\theta(e)=I_{20}). The Gram matrix of (T_2) under normalized angular integration is (G=\operatorname{diag}(1,1/2,1/2,1/2,1/2)), so
\[
H(\Lambda_0)=I_{20}\otimes G\succ0,\qquad \lambda_{\min}=1/2.
\]
This is a strict feasible point for the exact finite lift.

## Coefficient maps and dual cone

Write the 330 coordinates in the canonical basis (f_kX_{ij},f_kZ_{ij},f_k\eta,f_k\xi\). Let (P\) be the 23 indices corresponding to (X_{ij}f_0,Z_{ij}f_0) for (i\le j), \(\eta\cos\theta,\eta\sin\theta\), and \(\xi f_0\). Define (O:E^*\to\mathbb R^{23}) by reading exactly these coordinates in source order; thus (O(\Lambda)=(X_{ij},Z_{ij},y_1,y_2,y_3)) with the last three entries \((\Lambda(\eta\cos\theta),\Lambda(\eta\sin\theta),\Lambda(\xi))\). Let (S:\mathbb R^{23}\to E^*\) insert the 23 coordinates at (P) and set every other moment to zero. For each of the remaining 307 canonical moment-coordinate vectors (u_j\) (ordered by the underlying (T_7\) and variable bases), (u_j\) is a basis of \(\ker O\).

Define the linear map \(\mathcal H:E^*\to S^{100}\) by the source rule
\[
\mathcal H(\Lambda)_{(i,a),(j,b)}=\Lambda\!\left(f_af_b(L_\theta)_{ij}\right),\quad 1\le i,j\le20,\ a,b\le5.
\]
Every argument is in (E\) since its angular degree is at most (3+2+2=7\). The exact coefficient maps are
\[
\mathcal A x=\mathcal H(Sx)=\sum_{\nu=1}^{23}x_\nu A_\nu,\quad A_\nu=\mathcal H(S e_\nu),
\]
\[
\mathcal B t=\mathcal H\!\left(\sum_{j=1}^{307}t_ju_j\right)=\sum_{j=1}^{307}t_jB_j,\quad B_j=\mathcal H(u_j).
\]
Then the source equivalence is exactly
\[
K=\{x\in\mathbb R^{23}:\exists t\in\mathbb R^{307},\ \mathcal A x+\mathcal B t\succeq0\}.
\]
For the trace/Frobenius pairing on (S^{100}\), the adjoints are
\[
(\mathcal A^*Y)_\nu=\langle A_\nu,Y\rangle=\operatorname{tr}(A_\nu Y),\qquad
(\mathcal B^*Y)_j=\langle B_j,Y\rangle=\operatorname{tr}(B_jY).
\]

**Derived corollary (standard SDP duality; not a novelty claim).** For the closed cone (K\) represented above,
\[
K^*=\{\mathcal A^*Y:Y\succeq0,\ \mathcal B^*Y=0\}.
\]
Indeed, for (c\in K^*\), the primal conic LP is minimize (c^Tx\) subject to \(\mathcal A x+\mathcal B t-W=0\), (W\succeq0\), with (x,t\) free. Its value is zero (the origin is feasible, and (c\) is nonnegative on (K\)). Strict feasibility follows from (x=e,t=0,W=H(\Lambda_0)\succ0\). Slater strong duality and dual attainment yield (Y\succeq0), (\mathcal A^*Y=c), (\mathcal B^*Y=0). Conversely, any such (Y) certifies (c^Tx=\langle Y,\mathcal A x+\mathcal B t\rangle\ge0) for every feasible (x,t). No closure qualification is needed in this application because strict feasibility and finite optimum give dual attainment. The conclusion is an exact 100-by-100 PSD certificate for every linear functional nonnegative on (K\).

## Primary-source context and scope barriers

* Gårding (1959), *An inequality for hyperbolic polynomials*, DOI <https://doi.org/10.1512/iumj.1959.8.58061>: convexity background. The target proves its own needed hyperbolicity by the slice determinant.
* Choi–Lam (1977), *Extremal positive semidefinite forms*, DOI <https://doi.org/10.1007/BF01360024>: source named for the coefficient-one Choi–Lam biquadratic; the companion also gives a self-contained proof of the precise weak-extremality fact it uses.
* Helton–Vinnikov (2007), *Linear matrix inequality representation of sets*, DOI <https://doi.org/10.1002/cpa.20155>, and Lewis–Parrilo–Ramana (2005), *The Lax conjecture is true*, <https://arxiv.org/abs/math/0304104>: three-variable context only, not used in the lift construction.
* Netzer–Sanyal (2015), *Smooth hyperbolicity cones are spectrahedral shadows*, <https://arxiv.org/abs/1208.0441>, and Scheiderer (2025), *Smooth hyperbolicity cones are second-order cone representable*, <https://arxiv.org/abs/2509.17121>: nearby sufficient-condition results, not the target's premise. The target has a singular boundary stratum (its companion records (p(te-w)=(t-1)^{16}t^4) at (w=(I_4,0,0)\notin\mathbb Re)); thus those smooth-boundary hypotheses do not yield this example's lift.
* Lasserre (2001, 2009) moment/SOS references are cited for the general positivity-on-test-space idea. The exact converse here is the bespoke degree-two matching identity, not a generic moment convergence theorem.

Two transfer traps are explicitly separated. First, “nonspectrahedral” means no direct pencil in the original variables; this (K) is nonetheless a spectrahedral shadow by the 307-variable lift. Second, this example gives no universal liftability theorem: the pinned Oct. 5 *Hyperbolicity Cones Without Semidefinite Lifts* is a different source-reported cone with no finite affine lift. The latter's proof is outside this audit.

## Failed attempt retained

An initial apparent inconsistency in target Lemma 3.1 (matching factor) came from text extraction losing complex-conjugation overbars. The source uses (-\overline g) in the affected matrix entry, not (-g). With the rendered page images (`family_cone_lift/render/lift_p5.png`, `lift_p6.png`) inspected, the proposed numerical counterexample (g=-i\sqrt2,h=-\sqrt2,\kappa=i,\delta=4) satisfies the source matrix identity in the second row. Retract the bug claim: it was a PDF text-extraction artifact, not a mathematical counterexample. The visual render is the deciding evidence; the original scratch claim is superseded by this correction.

## Bounded subsequent-literature search

As of 2026-10-08, exact-title and construction-specific searches for the paper, its degree-two matching identity, and the Choi–Lam 100-by-100 lift found the pinned release/index entry and older general literature, but no later primary source specifically extending or correcting this construction. This is only a bounded search (three days after the displayed manuscript date), not an exhaustive novelty or priority check. The source's pinned GitHub history for the target PDF contains one commit at the pinned snapshot. Priority and correctness remain externally unvalidated.

## Evidence status / costs / next gate

* Status: theorem and coefficient/moment map reconstructed from source; exact strict point and duality corollary derived internally. No independent formal proof, solver replay, or external expert review performed.
* Input/cost interface: source gives a finite (23\to(100,307)) exact coefficient rule. It does not claim minimal dimensions. To generate matrices from the rule one needs symbolic expansion of the (T_7\)-moments of the size-20 slice pencil; no runtime, bit-height, conditioning, or numerical implementation bound is stated in the source or established here.
* Sharp current barrier: the matching lemma's proof and the source's singular-(X) range argument are the load-bearing exactness steps. This audit sampled the latter from extracted pages but did not independently formalize every trigonometric identity. For the dual corollary, the exact required gate is standard Slater conic duality after confirming the explicit strict witness; that gate is discharged mathematically in these notes.
* Next meaningful verification: independently expand the finite coefficient rule over exact rationals/algebraic trig coefficients and check (H(\Lambda_0)\succ0), then proof-review the degree-two matching identity directly against the rendered equations. Numerical/finite verification would validate only the checked expansion, not the universal theorem.
