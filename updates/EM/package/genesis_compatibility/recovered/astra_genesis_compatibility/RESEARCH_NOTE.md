# ASTRA Primitive Genesis — Compatibility completion and its curvature

**Date:** 12 October 2026.  
**Status:** research checkpoint with complete written proof candidates, exact symbolic checks, and an unresolved positive theorem. Not externally reviewed; historical originality is not established. This is not a proof of planar Morrey's conjecture or the sharp general Beurling–Ahlfors bound. No repository publication was performed.

## 1. Target, selection, and prior-work boundary

The selected obstruction is the passage from stability under rank-one variations to stability under arbitrary compatible planar gradients. The original goal is not a new notation for an energy estimate: it is an implication from pointwise rank-one convexity to a global quasiconvexity inequality. Convex-geometric and interacting-system opportunities were screened before concentrating on this problem. The earlier cumulative-strain theorem is not a premise.

Let `M = R^{2x2}`. A C2 function F is rank-one convex when

\[
 D^2F(A)[\eta\otimes\xi,\eta\otimes\xi]\geq0
\]

for all A, eta, xi. Quasiconvexity asks that

\[
 \int_U F(A+D\varphi)\,dx\geq |U|F(A),
 \qquad \varphi\in W^{1,\infty}_0(U;\mathbb R^2).
\]

**Important prior work.** Bruno–Pasqualotto [R1] already prove the planar Dacorogna–Marcellini threshold and the equivalence of rank-one convexity and quasiconvexity for rotationally invariant homogeneous quartic polynomials. Their method adds an exact matrix-space two-form to heat dissipation. Their appendix already separates a nonnegative determinant-square term. Neither the heat/exact-form method nor this separation in the invariant class is an Astra invention.

Astala–Iwaniec–Prause–Saksman [R2] establish Burkholder inequalities with a pointwise distortion restriction. Guerra [R3] treats symmetric matrices. Neither restriction is imposed on the obstruction theorem below. The matrix-polynomial sum-of-squares theorem used in Section 3 is established prior machinery [R4].

Scoped searches of the two requested research repositories did not identify this specific compatibility-curvature theorem. That is not comprehensive priority clearance. Repository claims were not imported as proof premises.

## 2. The established heat/exact-form interface

For matrices A,B1,B2 define

\[
 E_F(A;B_1,B_2)=\sum_{i=1}^2D^2F(A)[B_i,B_i].
\]

A compatible pair is a possible second derivative of a vector-valued map:

\[
 B_1=\begin{pmatrix}a&b\\d&e\end{pmatrix},\qquad
 B_2=\begin{pmatrix}b&c\\e&f\end{pmatrix}.
 \tag{2.1}
\]

Equivalently B1 e2 = B2 e1. For a two-form omega on matrix space, seek

\[
 E_F(A;B_1,B_2)+\omega_A(B_1,B_2)\geq0.\tag{2.2}
\]

For polynomial F, a globally closed polynomial omega is exact. Its pullback by Dv integrates to zero for an affine map plus a Schwartz perturbation. Integration of (2.2), followed by componentwise heat evolution, proves quasiconvexity. This interface is credited to [R1], not counted as new.

For clarity, the analytic implication also follows directly. If v_t=A x+e^{t\Delta}\varphi, then the relative energy after subtracting the affine term has derivative minus the integral of E_F. For a quartic integrand its absolute value is controlled by a fixed multiple of |A|^2|D\varphi_t|^2+|A||D\varphi_t|^3+|D\varphi_t|^4. The heat estimates make these integrals tend to zero. Thus the initial relative energy is nonnegative. Smooth approximation gives the stated Sobolev tests. This argument does not assert the existence of omega.

## 3. Pointwise completion: the algebraic problem always has a solution

**Proposition 3.1.** If F is C2 and rank-one convex, then at each fixed A there exists a two-form omega_A such that (2.2) holds for all compatible pairs. No smoothness, closedness, or common polynomial dependence of this choice on A is asserted.

**Proof.** A pure compatible second jet is

\[
 (a,b,c,d,e,f)=(u x^2,u x y,u y^2,v x^2,v x y,v y^2).
\]

Equivalently B_i=xi_i(eta tensor xi). On such jets,

\[
 E_F=|\xi|^2D^2F(A)[\eta\otimes\xi,\eta\otimes\xi]\geq0.
\]

This is a nonnegative binary quartic in xi, with a symmetric 2x2 matrix of coefficients acting on eta. Dehomogenize in xi. The positive-semidefinite univariate matrix-polynomial factorization [R4] writes that matrix as Q^TQ. The entries of Q have degree at most two: a higher-degree term cannot cancel in a sum of real squares. Homogenizing gives a sum of squares of expressions linear in eta and quadratic in xi. Each is a linear function of the six compatible jet coordinates. Hence a positive-semidefinite quadratic form P on all six coordinates agrees with E_F on pure jets.

The restriction map from quadratic forms in six variables (dimension 21) to polynomials of bidegree (2,4) in (eta,xi) (dimension 15) is onto: every target monomial is obtained from a product of two jet coordinates. Its kernel has dimension six. The six independent kernel elements are

\[
 ac-b^2,\quad ae-bd,\quad af-be,\quad be-cd,\quad bf-ce,\quad df-e^2.
 \tag{3.1}
\]

They are exactly the six two-form evaluations on the two columns of

\[
 \begin{pmatrix}a&b\\b&c\\d&e\\e&f\end{pmatrix}.
\]

Thus P-E_F is omega_A(B1,B2) for a unique two-form at A. QED.

**What this does and does not remove.** There is no residual pointwise existence problem for an unrestricted two-form. The unresolved issue is selecting such forms across matrix space with the differential constraint d omega=0. A pointwise sum of squares is not a quasiconvexity proof.

## 4. An explicit completion for the Burkholder family

Use the complex coordinates

\[
 z=\frac{A_{11}+A_{22}}2+i\frac{A_{21}-A_{12}}2,
 \qquad
 w=\frac{A_{11}-A_{22}}2+i\frac{A_{21}+A_{12}}2.
\]

Let r=|z|, s=|w|, R=r+s, and work first on the open set

\[
 \mathcal U=\{A:r>0,\ s>0\}.
\]

For p>2 take the rank-one-convex sign of the Burkholder integrand,

\[
 F_p(A)=((p-1)s-r)R^{p-1}.
 \tag{4.1}
\]

Let omega_z=d(Re z) wedge d(Im z), omega_w=d(Re w) wedge d(Im w), and set

\[
 K_p=2p(p-1)R^{p-2},\qquad
 \Omega_p=K_p(\omega_z+\omega_w).
 \tag{4.2}
\]

Rotate target and domain so z=r and w=s are real; then A=diag(R,r-s). Express compatible jets in these rotated coordinates as in (2.1).

**Theorem 4.1 (exact square identity).**

\[
 \boxed{E_{F_p}+\Omega_p(B_1,B_2)
 =p(p-2)R^{p-3}
 \left[(p-1)s(a^2+b^2)
 +\frac{R^2}{4r}\big((c-e)^2+(b-d)^2\big)\right].}
 \tag{4.3}
\]

**Proof.** The radial and angular Hessian coefficients are

\[
\begin{aligned}
 F_{rr}&=p(p-1)R^{p-3}[-r+(p-3)s],\\
 F_{rs}&=p(p-1)(p-2)sR^{p-3},\\
 F_{ss}&=p(p-1)R^{p-3}[r+(p-1)s],\\
 F_r/r&=pR^{p-2}[-r+(p-2)s]/r,\\
 F_s/s&=p(p-1)R^{p-2}.
\end{aligned}
\]

At the diagonal representative,

\[
\begin{aligned}
 2z_x&=a+e+i(d-b),&2z_y&=b+f+i(e-c),\\
 2w_x&=a-e+i(d+b),&2w_y&=b-f+i(e+c).
\end{aligned}
\]

Substitute these into the radial Hessian and the two area forms and collect coefficients. This gives (4.3). The supplied script checks the identity symbolically with p left as a parameter. QED.

The identity also verifies the interior rank-one convexity without an import: on pure compatible jets both two-form evaluations vanish. Across z=0 the slope jump along a nonconstant rank-one line is nonnegative because F_r(0,s)=p(p-2)s^{p-1}>0. Across w=0 there is no adverse slope jump. Homogeneity p>2 treats the origin. Thus the rank-one-line convexity extends to all matrices.

**Crucial failure:** d Omega_p=d K_p wedge (omega_z+omega_w) is nonzero. Stokes cannot eliminate this correction. Section 5 proves that this is not repaired by a different smooth closed two-form.

## 5. Forced-curvature obstruction, without a polynomial ansatz

**Theorem 5.1.** For each p>2, there is no C1 closed two-form omega on all of U for which

\[
 E_{F_p}(A;B_1,B_2)+\omega_A(B_1,B_2)\geq0
 \tag{5.1}
\]

for every A in U and every compatible pair. The form is not required to be homogeneous, polynomial, bounded at the axes, or exact.

**Proof, including the symmetry reduction.** Under A mapsto P A Q^T with P,Q in SO(2), the integrand and U are invariant. The compatible jets transform by the same matrix action combined with rotation of their spatial index. Average a putative certificate over these compact rotations. This preserves (5.1) and closedness, and makes the coefficients invariant under independent rotations of z and w.

Also use P=Q=diag(1,-1). This conjugates z,w simultaneously and reverses the orientation of the spatial jet pair. Therefore its action on a certificate is minus the pullback, rather than the ordinary pullback. Averaging with this action preserves the certificate and closedness. It eliminates the dr wedge ds and dtheta wedge dphi components. With z=r exp(i theta), w=s exp(i phi), the general surviving form is

\[
 \omega=rU\,dr\wedge d\theta+rV\,ds\wedge d\theta
       +sW\,dr\wedge d\phi+sZ\,ds\wedge d\phi,
 \tag{5.2}
\]

where U,V,W,Z are C1 functions of r,s. The polar one-forms are globally meaningful on U; no choice of a single-valued angle function is required.

At z=r,w=s, (5.2) is

\[
 U\,dz_R\wedge dz_I+V\,dw_R\wedge dz_I
 +W\,dz_R\wedge dw_I+Z\,dw_R\wedge dw_I.
\]

Write Q=E_F+omega(B1,B2), a quadratic form in a,b,c,d,e,f.

First set all jet coordinates except f to zero. The diagonal coefficient of f^2 is zero. In a nonnegative quadratic form, a zero diagonal coefficient forces the entire corresponding row to vanish. The f b and f d coefficients therefore give

\[
 U-V=K_p,\qquad W-Z=-K_p.
 \tag{5.3}
\]

After (5.3), the jet with c=e and all other coordinates zero is also a null direction. Its mixed coefficient with a forces

\[
 Z=K_p,\qquad W=0.
 \tag{5.4}
\]

These conditions can be verified from the Hessian formulas of Section 4; the exact script verifies both null-row deductions after normalization by p R^{p-3}.

Closedness of (5.2) requires its dr wedge ds wedge dphi component to vanish:

\[
 \partial_r(sZ)-\partial_s(sW)=0.
\]

But the algebraically forced values give

\[
 \boxed{\partial_r(sZ)-\partial_s(sW)
 =2p(p-1)(p-2)sR^{p-3}>0.}
 \tag{5.5}
\]

Contradiction. QED.

Equation (5.5) is a forced component of the exterior derivative for every symmetrized positive completion, not merely the derivative of the explicit choice (4.2). Calling it a curvature obstruction is descriptive terminology, not a claim that differential forms or their exterior derivatives are newly invented.

**Corollary 5.2.** Replacing the heat equation by any constant positive-definite spatial diffusion tensor does not produce a closed two-form certificate for F_p on U.

Indeed, a certificate with tensor M transforms to one with tensor Q^T M Q. Simultaneously average the tensor and form over spatial rotations. Linearity gives (tr M/2)I and a closed positive certificate. Rescaling contradicts Theorem 5.1.

**Exact scope.** This rules out gradient-dependent closed two-form completions for these constant diffusion generators. It does not disprove quasiconvexity, does not rule out nonlinear or nonlocal flows, and does not rule out integrated inequalities with no such pointwise certificate. Singularities confined to z=0 or w=0 do not avoid the theorem: the contradiction already lies in the interior r,s>0. At p=2 the obstruction vanishes and F_2=-det A, consistent with the null-Lagrangian identity.

## 6. Why a universal heat route is wrong even for quartics

Let F(A)=(det A)^2. It is quasiconvex directly: the average determinant of A+Dphi is det A, and Jensen applied to the scalar square gives the inequality. Nevertheless its energy is not monotone under componentwise heat flow.

On the 2pi-periodic torus set h=sin x+sin y and v_0=(h,h^2). Initially det Dv_0=0 pointwise. Its exact heat evolution is

\[
\begin{aligned}
 v_t^1&=e^{-t}(\sin x+\sin y),\\
 v_t^2&=1-\tfrac12e^{-4t}(\cos2x+\cos2y)
          +2e^{-2t}\sin x\sin y.
\end{aligned}
\]

A direct calculation gives

\[
 \det Dv_t=2e^{-t}(e^{-2t}-e^{-4t})\cos x\cos y(\sin x-\sin y),
\]

and, with normalized torus average,

\[
 \boxed{\left\langle(\det Dv_t)^2\right\rangle
 =\tfrac12 e^{-2t}(e^{-2t}-e^{-4t})^2>0\quad(t>0).}
 \tag{6.1}
\]

Thus the energy rises from zero. A universal assertion that all rank-one-convex quartics admit a direct heat certificate is false. The determinant-square term must at least be handled separately. The analogous separation in the rotationally invariant class is already in [R1].

## 7. A structural operation on arbitrary quartics

Write Delta(A)=det A. For a homogeneous quartic polynomial F, let T be its symmetric four-linear polarization. Then

\[
 D^2F(A)[H,H]=12T(A,A,H,H)=D^2F(H)[A,A].\tag{7.1}
\]

**Proposition 7.1.** If F is rank-one convex and R is rank one, then the full matrix Hessian D2F(R) is positive semidefinite.

Proof: (7.1) converts D2F(R)[H,H] to D2F(H)[R,R], which is a rank-one-convexity test. QED.

**Proposition 7.2 (unique rank-one-invisible quartic ray).** Suppose F is a homogeneous quartic polynomial, is rank-one convex, and vanishes on all rank-one matrices. Then

\[
 F=c\,\Delta^2,\qquad c\geq0.
 \tag{7.2}
\]

Proof: vanishing on the determinant-zero variety gives F=Delta Q with Q quadratic. One can see the divisibility by setting A22=A12 A21/A11 on the open subset A11 not equal to zero and performing polynomial division; this identity forces determinant divisibility globally.

At each nonzero rank-one R, Proposition 7.1 gives D2F(R) positive semidefinite, and homogeneity gives D2F(R)[R,R]=12F(R)=0. Hence D2F(R)[R,H]=0 for every H. Differentiated Euler homogeneity gives D2F(R)[R,H]=3 DF(R)[H], so DF(R)=0.

But DF(R)=Q(R) DDelta(R), and DDelta(R) is nonzero at a nonzero rank-one matrix. Therefore Q vanishes on the rank-one variety. The same divisibility argument gives Q=c Delta. Rank-one convexity along diag(1,t) forces c nonnegative. QED.

This does NOT prove determinant-square is the only obstruction to a global closed completion. It proves the precisely narrower statement (7.2), and motivates separating that ray rather than treating it as evidence against quasiconvexity.

**Canonical admissible minor-removal interval.** Define

\[
 \gamma_*(F)=\inf_{\substack{\operatorname{rank}H=1\\D\Delta(A)[H]\ne0}}
 \frac{D^2F(A)[H,H]}{2(D\Delta(A)[H])^2}.
 \tag{7.3}
\]

For a rank-one-convex quartic this is finite and nonnegative. Then

\[
 \boxed{F-\gamma\Delta^2\text{ is rank-one convex}
 \ \Longleftrightarrow\ 0\leq\gamma\leq\gamma_*(F)}
 \tag{7.4}
\]

where the displayed equivalence is restricted to gamma>=0. On a rank-one line Delta(A+tH) is affine in t, so its square has second derivative 2(DDelta(A)[H])^2. The tests with zero denominator are unchanged; every other test gives the corresponding bound in (7.3). This proves (7.4), including the endpoint, without requiring the infimum to be attained.

The maximal-removal residual is G*=F-gamma_* Delta^2. A search may begin there, but maximal removal is not assumed necessary for the final positive gate below. For Delta^2 itself gamma_*=1 and G*=0. For |A|_F^4, gamma_*=2: the Cauchy bound |cof A:H|<=|A|_F|H|_F gives the lower bound, with equality in the required ratio at A=diag(1,0), H=diag(0,1).

The identities (7.1)–(7.4) are elementary structural results; their historical novelty is not claimed.

## 8. Closing a nonclosed polynomial completion: an explicit budget

Let G be a homogeneous quartic polynomial and Omega a two-form with homogeneous quadratic coefficients. Let Rcal be the Euler vector field A mapsto A. Cartan's formula gives

\[
 d(\iota_{\mathcal R}\Omega)+\iota_{\mathcal R}d\Omega=4\Omega.
\]

Consequently

\[
 \Omega^{\rm cl}=\tfrac14d(\iota_{\mathcal R}\Omega)
 =\Omega-\tfrac14\iota_{\mathcal R}d\Omega
 \tag{8.1}
\]

is a globally exact polynomial form. In particular the finite-coefficient inequality

\[
 E_G(A;B_1,B_2)+\Omega_A(B_1,B_2)
 \geq \tfrac14\left|d\Omega_A(A,B_1,B_2)\right|
 \tag{8.2}
\]

for all compatible jets suffices for quasiconvexity of G, hence of G+gamma Delta^2 when gamma>=0.

This is an explicit sufficient operation, not a theorem that the budget is always available. It uses standard homotopy machinery. In particular pointwise completion in Section 3 does not imply (8.2), does not imply polynomial dependence on A, and does not supply a margin near null directions. Those are substantial gaps.

## 9. The retained positive proof obligation

**Gate Q4 (unproved, falsifiable).** For every rank-one-convex homogeneous quartic polynomial F on M, do there exist

- gamma in [0,gamma_*(F)],
- a constant symmetric positive-definite 2x2 matrix M, normalized by tr M=2,
- a globally closed two-form omega whose coefficients are homogeneous quadratic polynomials in A,

such that, for G=F-gamma Delta^2,

\[
 \boxed{\sum_{i,j=1}^2M_{ij}D^2G(A)[B_i,B_j]
       +\omega_A(B_1,B_2)\geq0}
 \tag{Q4}
\]

for every A and every compatible pair?

A stronger first test fixes gamma=gamma_*. The retained gate allows the whole interval rather than confusing that stronger choice with a necessary one.

**Consequence if proved.** The constant elliptic heat equation with tensor M and the exact-form argument imply quasiconvexity of G. Jensen and the determinant null-Lagrangian identity imply quasiconvexity of gamma Delta^2. Their sum proves quasiconvexity of every rank-one-convex planar homogeneous quartic, without rotational invariance.

This addresses the entire 35-dimensional coefficient space of quartic polynomials in four entries, rather than the three-dimensional rotationally invariant subspace covered in [R1]. It is still not the full C2 planar Morrey problem. In particular F_4 of Section 4 is not a quartic polynomial in the entries: it contains the term 8|z||w|^3. Q4 would therefore not settle the general Burkholder inequality.

**Why this is a concrete gate rather than a solution-dependent continuation criterion.** A two-form has six coefficients, each a homogeneous quadratic in four variables, giving 60 real coefficient parameters. Closedness imposes 15 independent linear conditions, leaving 45. After writing (2.1), the positivity test is a polynomial of bidegree (2,2) in the four entries of A and six jet variables. M and gamma add only finitely many parameters. Rank-one convexity of the input is itself a quantified polynomial condition. Thus Q4 is a fixed-dimensional semialgebraic assertion about coefficients, with no unknown PDE trajectory, observed regularity norm, or prediction horizon in its assumptions.

This finite formulation is NOT an efficient decision algorithm, and an unsuccessful sum-of-squares relaxation is NOT a counterexample. Positivity of a general multivariate matrix polynomial is not equivalent to any particular low-degree SOS ansatz. Exact real-algebraic elimination could in principle verify a proposed instance or its infeasibility, but no such general implementation or cost claim is made here. A rigorous rejection needs a rank-one-convex input together with an exact impossibility certificate for every allowed gamma, M, omega, not a failed optimizer.

**Reason to retain it.** Pointwise completion is guaranteed, a canonical otherwise-misleading minor component is exactly isolated, quartic Hessian reciprocity supplies an extra constraint absent in the Burkholder family, and the invariant subcone has a known positive certificate. These facts justify a targeted test, not confidence that Q4 is true. Other global selection obstructions may remain. Failure would require a genuinely different operation, not another label for d omega.

## 10. Reproducibility and failure ledger

`verify_exact.py` produced 67 passing symbolic checks with SymPy 1.14.0. The checks include the arbitrary-p identity, radial derivatives, forced null rows and curvature, the six-dimensional compatible-minor kernel, Hessian reciprocity for all 35 quartic monomials, the exact determinant heat example, and the 45-dimensional closed-form coefficient count. They do not formalize the analytic proofs or establish external novelty. Full output is `verification.json`.

A separate exploratory optimization found a negative *numerical* heat-dissipation integral for F_4 with an affine background and three Fourier modes. The saved optimizer record pairs pre-step diagnostics with post-step coefficients; its original displayed objective is therefore not used as the rechecked value. `check_numeric.py` recomputes the saved coefficients independently. At a 512x512 grid the normalized mean dissipation is approximately -0.0001512503. The grid contains very small |w| values. `numerical_recheck.json` is explicitly uncertified floating quadrature; no theorem depends on its sign. The symbolic determinant example is the rigorous heat-flow counterexample retained in the main argument.

Discarded or restricted routes:

1. A pointwise two-form completion is insufficient without its closedness or a valid integrated correction.
2. A closed completion for the Burkholder family is impossible even off its singular axes, and constant anisotropic diffusion does not repair it.
3. A universal direct-heat certificate for rank-one-convex quartics is false because of (6.1).
4. The rotationally invariant quartic theorem and its determinant separation are prior work, not new output.
5. Q4 remains open. No claim of global nonlinear regularity, full planar quasiconvexity, or sharp general Beurling norm is made.

## References and access record

[R1] Giuseppe Bruno and Federico Pasqualotto, *Quasiconvexity for the Dacorogna–Marcellini Energy*, arXiv:2608.06367v1. Full HTML and appendix inspected on 12 October 2026. The arXiv record gives submission on 6 August 2026; the rendered manuscript has a 24 August 2026 header. `https://arxiv.org/html/2608.06367v1`

[R2] Kari Astala, Tadeusz Iwaniec, Istvan Prause, Eero Saksman, *Burkholder integrals, Morrey's problem and quasiconformal mappings*, arXiv:1012.0504v1; J. Amer. Math. Soc. 25 (2012), 507–531. Abstract used for the scoped comparison; no theorem imported from its full proof. `https://arxiv.org/abs/1012.0504`

[R3] Andre Guerra, *Quasiconvexity of the Burkholder function on symmetric matrices*, arXiv:2608.23388v1, submitted 24 August 2026. Abstract used for scope comparison. `https://arxiv.org/abs/2608.23388`

[R4] Christoph Hanselka and Rainer Sinn, *Positive Semidefinite Univariate Matrix Polynomials*, arXiv:1707.08261v1, 26 July 2017. Uses established PSD univariate matrix-polynomial SOS factorization; the paper credits Blekherman–Plaumann–Sinn–Vinzant for the minimal-size real factorization. `https://arxiv.org/abs/1707.08261`

Requested repositories consulted through the GitHub connector: Astra README, 00_START_HERE.txt, state/branches.tsv, and scoped lexical searches; OpenAI/math README and scoped searches. Reads were not an atomic repository snapshot. OpenAI/math search results carried revision fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb. Nothing from either repository is a mathematical premise above. No exhaustive current-priority claim is made.
