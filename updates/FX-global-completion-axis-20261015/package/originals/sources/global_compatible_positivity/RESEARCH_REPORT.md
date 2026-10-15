# Compatible positivity beyond a moving interval
## Exact distortion-completion cones, a universal null correction, and a limit of linear heat

Research date: 15 October 2026.

**Status.** New analytic arguments and a universal rational certificate were constructed in this investigation. The standalone exact verifier passes. This is an internally checked, model-assisted mathematical result, not independent external review, formal proof verification, or historical-priority clearance. No concurrent Sol conclusion is a premise.

**Main distinction.** The new theorem allows the coefficient of the convex Cauchy–Riemann distortion fourth power to increase. It characterizes exactly which remaining coefficients admit *some finite such completion*. It does not identify the least coefficient, prove quasiconvexity of every rank-one-convex member at its original coefficient, or settle the nine-coefficient problem.

## 1. Definitions and theorem statements

For a real two-by-two matrix
\[
 A=\begin{pmatrix}a&b\\c&d\end{pmatrix},\qquad
 u=a^2+c^2,\quad v=b^2+d^2,\quad w=ab+cd,\quad j=ad-bc,
\]
set
\[
 \mathcal C A=(a-d,b+c),\qquad H(A)=|\mathcal C A|^4=(u+v-2j)^2.
\]
The coefficient of H will be denoted by alpha, to avoid confusion with the matrix entry a. Define
\[
 P_{\alpha,r}=\alpha H+\frac{r(r-1)}6u^2+j^2+r u j.
\]

### Theorem A: universal isotropic-heat completion

For every real r satisfying
\[
 q=r(r+2)>0,
\]
there is an explicitly defined finite number alpha_*(r) such that, for every alpha >= alpha_*(r),
\[
 P_{\alpha,r}-H
\]
is quasiconvex at every affine background. The proof uses ordinary componentwise heat, with diffusion matrix I, a rational moving Gram basis, and closed two-forms with quadratic coefficients in A.

There are two explicit constructions of alpha_* below. One is a single rational matrix formula on the whole set q>0. A less conservative construction uses absolute values and maxima and is piecewise rational. Neither requires an optimization oracle or a search over gradients. At rational r, both produce rational numbers by finite exact matrix arithmetic of order at most 18.

For every bounded Lipschitz domain Omega in R^2, B in R^(2x2), and phi in W_0^(1,4)(Omega;R^2),
\[
 \int_\Omega [P_{\alpha,r}(B+D\phi)-P_{\alpha,r}(B)]
 \ge \frac4{1875}\int_\Omega |D\phi|^4.                 \tag{1}
\]
The same coefficient applies to periodic rectangles and to finite periodic strips with zero perturbation profiles at both ends. It does not depend on the affine background or strip width.

The value 4/1875 is not sharp. It comes from subtracting one H and a classical nonsharp Beurling estimate, not a contemporary sharp-norm assertion.

### Theorem B: exact parameter projection for the curved family

For every real r,
\[
\begin{split}
 &\exists\alpha\in\mathbb R:\ P_{\alpha,r}\text{ is rank-one convex}\\
 \Longleftrightarrow\;&\exists\alpha\in\mathbb R:\ P_{\alpha,r}\text{ is quasiconvex}\\
 \Longleftrightarrow\;&r\in(-\infty,-2)\cup[0,\infty).
\end{split}                                                       \tag{2}
\]
At r=0, quasiconvexity follows from the familiar sum alpha H+j^2 for alpha>=0; a heat certificate is not asserted for that exceptional case.

For r!=0, rank-one convexity necessarily requires
\[
 \alpha\ge\frac{3r}{8(r+2)},\qquad r(r+2)>0.            \tag{3}
\]
In particular, r=-2 admits no finite completion, and the necessary coefficient diverges as r approaches -2 from below. This is a rank-one obstruction, not a failure of an ansatz.

### Theorem C: exact projection of the entire shear-contact cone

Consider
\[
 F_{\alpha,\beta,\gamma,\delta}
 =\alpha H+\beta u^2+\gamma j^2+\delta u j.             \tag{4}
\]
Then the following are equivalent:

(a) Some finite alpha makes F rank-one convex.

(b) Some finite alpha makes F quasiconvex.

(c) Its remaining coefficients obey one of the following alternatives:
\[
 \delta=0,\quad \beta\ge0,\quad\gamma\ge0,             \tag{5}
\]
or
\[
 \delta\ne0,\quad\gamma>0,\quad
 6\beta\gamma-\delta^2+\delta\gamma\ge0,\quad
 2\beta+\delta>0.                                     \tag{6}
\]
Equivalently, the two-by-two matrix
\[
 \begin{pmatrix}6\beta+\delta&\delta\\\delta&\gamma\end{pmatrix}
 \succeq0
\]
must hold, together with 2 beta+delta>0 or (beta,delta)=(0,0).

This is an equality of projected cones. Let R_sh and Q_sh be the rank-one-convex and quasiconvex cones in (4), and let pi delete the alpha coordinate. Then
\[
 \boxed{\pi(R_{\rm sh})=\pi(Q_{\rm sh})}
\]
with the explicit description (5)–(6). This does not assert equality of the original cones or equality of their least-alpha boundaries.

For delta!=0, an explicit sufficient coefficient is
\[
 \gamma_0=\frac{\delta^2}{6\beta+\delta},\qquad
 r_0=\frac{6\beta+\delta}{\delta},\qquad
 \alpha\ge\gamma_0\alpha_*(r_0).                       \tag{7}
\]
In this range F-gamma_0 H is quasiconvex, with integrated gradient margin 4 gamma_0/1875. The proof uses a heat certificate for the core plus a separate polyconvex determinant-square addition. It does not combine them into a single heat certificate.

### Theorem D: fixed linear heat misses even a polyconvex energy

The integrand f(A)=(det A)^2 is quasiconvex and polyconvex. For every fixed positive-definite constant input diffusion D, however, there is a smooth compatible periodic map whose f-energy increases under the corresponding componentwise heat flow.

For isotropic heat an explicit rational-amplitude example has
\[
 \left\langle\sum_{i=1}^2D^2f(D\psi)[\partial_iD\psi,\partial_iD\psi]\right\rangle
 =-\frac{212044959}{2000000000}<0.                      \tag{8}
\]
Thus no universally zero-integral correction can make this same dissipation nonnegative for all compatible maps. The obstruction is stronger than failure of a positive Gram representation: it is an actual compatible negative integrated dissipation. It is **not** negative quasiconvex energy and is not a counterexample to Morrey's implication.

## 2. Reconstruction of the incoming result

The supplied moving-family package was extracted and the following programs rerun:

```
python verify_moving_acoustic.py
python verify_structure.py
python reconstruct.py
```

They pass their exact checks, including the polynomial identity in r, the closed-form primitive, all 72 positive Bernstein LDL pivots on [-21/8,-5/2], the scalar subtraction, and the source G coefficient reconstruction. The analytic heat implication and coercivity argument were separately read and reconsidered.

The older result concerns alpha=3 on a small closed interval and supplies subtraction 3H/16000. Its certificate remains substantially sharper there than the conservative universal construction here. In particular, the new construction must not be presented as improving the coefficient required for G.

The input report proves that fixing the old rank-18 support allows only span{G,H}; its failed continuation at r=-8/3 concerns one selected matrix, not quasiconvexity. This investigation did not infer an impossibility from that failure. It released the free coefficients, separated the directions controlled by H, and constructed a new isotropic identity.

The new identity is checked directly from the polynomial (4) and the new JSON. Its correctness does not depend on the original numerical acquisition, original positive S matrix, or the old parameter-interval certificate. The moving support is inherited geometric capital.

## 3. Acoustic necessity and the full shear-contact face

Every left-SO(2)-invariant real homogeneous quartic has a unique expression
\[
 f_0u^2+f_1v^2+f_2uv+f_3w^2+f_4uw+f_5vw+f_6uj+f_7vj+f_8wj,
\]
using uv=w^2+j^2. If a rank-one-convex quartic has the contact
\[
 D^2F(I)[e_{12},e_{12}]=0,
\]
its nonnegative acoustic form and its first derivatives vanish at the contact. Exact elimination gives
\[
 f_1=-f_7/4,\qquad f_2+f_3=-f_7/2,\qquad f_4=f_5=f_8=0.
\]
These five independent constraints yield precisely the four-dimensional space (4). The verifier independently regenerates this linear system.

For (4), put
\[
 A_t=\begin{pmatrix}1&-s t\\s t&1\end{pmatrix},\qquad
 R_t=e_1\otimes(t,1).
\]
Here s is any real scalar. Differentiation gives
\[
\begin{split}
 D^2F(A_t)[R_t,R_t]
 ={}&[12\beta+2\gamma(1-s)^2+(6-4s)\delta]t^2\\
 &+2s^2(2\beta+\delta)t^4.                              \tag{9}
\end{split}
\]
Also F(e12)=alpha. Restriction to its rank-one ray forces alpha>=0. At A=[[0,1],[-1,0]], the acoustic direction e12 gives 2 gamma, forcing gamma>=0.

If gamma=0, nonnegativity of the t^2 coefficient in (9) for every s forces delta=0 and beta>=0. If gamma>0, minimize that coefficient at s=1+delta/gamma to obtain
\[
 6\beta\gamma-\delta^2+\delta\gamma\ge0.                \tag{10}
\]

A further condition was absent from the original narrow-wedge characterization. Consider the acoustic form D^2F(A)[e11,e11] and its principal quadratic block in the matrix entries (b,c):
\[
 M_{bc}=\begin{pmatrix}
 4\alpha&4\alpha-\delta\\
 4\alpha-\delta&4(\alpha+\beta)
 \end{pmatrix}.
\]
Positive semidefiniteness requires
\[
 \det M_{bc}=8\alpha(2\beta+\delta)-\delta^2\ge0.       \tag{11}
\]
For delta!=0 this forces 2 beta+delta>0 and the explicit lower bound alpha>=delta^2/[8(2 beta+delta)]. Together, (9)–(11) establish all the necessary conditions in Theorem C.

On the boundary beta=r(r-1)/6, gamma=1, delta=r, equation (11) becomes
\[
 \frac83\alpha r(r+2)-r^2\ge0.                         \tag{12}
\]
If r!=0, this forces r(r+2)>0. At r=-2 the determinant is -4, regardless of alpha. If alpha>0, the acoustic matrix at that parameter has the explicit negative vector (b,c)=(-(4 alpha+2),4 alpha); its quadratic value is -16 alpha. At alpha=0, (b,c)=(-2,1) gives -4. Negative alpha already fails on the e12 ray.

For r=-2-epsilon with epsilon>0, (3) reads
\[
 \alpha\ge\frac{3(2+\epsilon)}{8\epsilon}.
\]
The divergent coefficient is a real geometric obstruction. In particular, there is no finite uniform completion on the whole interval [-3,-2). This also supplies a concrete example of a nonclosed projection of a closed cone: the curved projected coefficient triples approach r=-2, whose completion is impossible.

## 4. What the moving kernel does and does not control

Let z=(z0,...,z5) denote compatible second jets and use
\[
 B_1=(z_0,z_1,z_3,z_4),\qquad B_2=(z_1,z_2,z_4,z_5),
 \qquad Z=(a,b,c,d)\otimes z.
\]
For the boundary family, the choice s=r+1 in (9) gives
\[
 D^2P_{\alpha,r}(A_t)[R_t,R_t]
 =\frac23r(r+1)^2(r+2)t^4.                             \tag{13}
\]
Every two-form correction vanishes on a rank-one second jet, because B1 and B2 are proportional. If Q is a positive semidefinite Gram certificate and Z(t) is the corresponding analytic bilinear vector, (13) forces
\[
 QZ(0)=0,\qquad QZ'(0)=0.
\]
Indeed Z(t)^TQZ(t)=|Q^(1/2)Z(t)|^2, so its first nonzero Taylor coefficient has even order. More generally, an O(t^(2k)) acoustic curve forces the derivatives of Z up to order k-1 into the kernel. This is a general elementary jet-order rule, not a claim that all positive compatible densities are Gram representable.

Three target rotations yield six independent forced vectors for r!=-1. The supplied moving C_r spans their orthogonal complement. Its fixed identity minor proves rank 18. The entries are rational in r; only four entries differ from the original G basis, with values +/-1/(r+1).

The decisive improvement here is not another continuation of the original positive matrix. The convex heat density of H has a rank-eight natural Gram S_H inside this moving support, and therefore a ten-dimensional kernel. No multiple of H can repair negativity within that kernel. It must first be repaired by a genuinely null correction.

## 5. Universal algebra: the 6+4+8 decomposition

`GLOBAL_COMPLETION_CERTIFICATE.json` contains C_r, S0(r), S_null, W0(r), W_null, S_H, N, and R, all with explicit rational entries and orderings. The polynomial data use the common denominator r+1. After cancellation, S_null and W_null are constant in r. The only matrices depending on r in the initial identity are C_r, S0(r), and W0(r).

The identities, for every r!=-1 and every A,z, are
\[
\begin{split}
 Z^TC_rS_0(r)C_r^TZ&=\mathcal D_{P_{3,r}}(A,z)+\omega_{0,r}(B_1,B_2),\\
 Z^TC_rS_{\rm null}C_r^TZ&=\omega_{\rm null}(B_1,B_2),\\
 Z^TC_rS_HC_r^TZ&=\mathcal D_H(A,z),                    \tag{14}
\end{split}
\]
where
\[
 \mathcal D_F=D^2F(A)[B_1,B_1]+D^2F(A)[B_2,B_2],
 \qquad d\omega_{0,r}=d\omega_{\rm null}=0.
\]
The verifier multiplies out denominators and checks the full polynomial identities and the polynomial primitives omega=d(i_E omega/4). No values of r or gradients are sampled for these checks.

### The null correction in ordinary coordinates

For readers wishing to inspect the new correction without the JSON, write
\[
 \omega_{\rm null}=\sum_{i<j}\omega_{ij}\,dx_i\wedge dx_j,
 \qquad(x_0,x_1,x_2,x_3)=(a,b,c,d).
\]
Its six coefficients are
\[
\begin{aligned}
 \omega_{01}&=-\tfrac12(a^2-2ad+3b^2+4bc+c^2+d^2),\\
 \omega_{02}&=ad-b^2-bc-d^2,\\
 \omega_{03}&=b(a-d),\\
 \omega_{12}&=d(b+c),\\
 \omega_{13}&=0,\\
 \omega_{23}&=-\tfrac12(a^2-4ad+b^2+2bc+c^2+3d^2).
\end{aligned}                                                        \tag{15}
\]
Its integral on compatible periodic gradients vanishes. It is not claimed to be nonnegative on all bilinear jets. Its role is selective positivity on a quotient where the H heat density is zero.

Let N be the constant 18-by-10 basis for ker S_H supplied in the certificate, reordered into six and four columns. Let R be the supplied constant 18-by-8 complement. The full matrix [N,R] is invertible. Then
\[
 N^TS_0N=\begin{pmatrix}A_6&B\\B^T&E\end{pmatrix},\qquad
 N^TS_{\rm null}N=\begin{pmatrix}0_6&0\\0&I_4\end{pmatrix}.             \tag{16}
\]
Put q=r(r+2) and s=r+1, so s^2=q+1. The acoustic block is
\[
A_6=\begin{pmatrix}
2q/3&0&0&0&0&0\\
0&2q/3+2&-2s&0&-2s&0\\
0&-2s&2s^2&0&4q/3+2&0\\
0&0&0&2s^2&0&0\\
0&-2s&4q/3+2&0&2s^2&0\\
0&0&0&0&0&2q/3
\end{pmatrix}.                                                       \tag{17}
\]
Its exact LDL pivots are
\[
 \frac{2q}3,\quad\frac{2(q+3)}3,\quad
 \frac{2qs^2}{q+3},\quad2s^2,\quad
 \frac{2q(5q+3)}{9s^2},\quad\frac{2q}3.                \tag{18}
\]
Every pivot is strictly positive for q>0. Its determinant is
\[
 \det A_6=\frac{64q^4s^2(5q+3)}{243}.
\]
This explicit factorization is why the new construction reaches two unbounded parameter components rather than a short interval.

The convex complement
\[
 H_8=R^TS_HR
\]
has constant positive LDL pivots
\[
 12,\ 4,\ 4,\ 32/3,\ 5/2,\ 12,\ 20/3,\ 4.
\]
The full S_H is positive semidefinite by its independently checked natural sum-of-squares representation, and ker S_H=range N.

### First completion: repair the directions invisible to H

Define
\[
 K_4=E-B^TA_6^{-1}B,
 \qquad\lambda=1+\max_i\sum_j|(K_4)_{ij}|.              \tag{19}
\]
The symmetric matrix K4+lambda I is strictly positive: every eigenvalue of K4 has absolute value at most its maximum absolute row sum. Therefore, setting
\[
 S_1=S_0+\lambda S_{\rm null},
\]
the ten-by-ten matrix N^T S1 N is positive definite by its Schur complement. This operation does not change the energy; it changes only a closed null correction.

### Second completion: add enough convex distortion

Write
\[
 [N,R]^TS_1[N,R]=\begin{pmatrix}P&U\\U^T&V\end{pmatrix},
 \qquad K_8=V-U^TP^{-1}U.
\]
Let H8=L_H D_H L_H^T be its fixed positive LDL factorization and set
\[
 \widetilde K_8=L_H^{-1}K_8L_H^{-T},
 \qquad\mu=1+\max_i\frac{\sum_j|\widetilde K_{8,ij}|}{D_{H,ii}}.       \tag{20}
\]
Then mu D_H+Ktilde8 is symmetric and strictly diagonally dominant with positive diagonal. It is positive definite. A second Schur complement proves
\[
 S_1+\mu S_H\succ0.                                    \tag{21}
\]
Choose alpha_*=4+mu. By (14), equation (21) is a certificate for
\[
 P_{\alpha_*,r}-H=P_{3+\mu,r}.
\]
The extra constant one in alpha_* reserves the claimed H subtraction. Larger alpha follows by adding the convex function (alpha-alpha_*)H.

### A single rational alternative

To avoid maxima and absolute values, one may instead use
\[
 \lambda=1+\operatorname{tr}(B^TA_6^{-1}B)+\operatorname{tr}(E^2).
\]
Because B^T A6^-1 B is positive semidefinite and ||E||op<=sqrt(tr E^2), the first Schur complement is at least 3I/4. With the resulting K8, choose
\[
 \mu=1+\operatorname{tr}\big((H_8^{-1}K_8)^2\big).
\]
The matrix H8^-1 K8 is similar to the symmetric matrix H8^-1/2 K8 H8^-1/2. Its squared trace is nonnegative and bounds the square of its operator norm. Hence the whitened second Schur complement is also at least 3I/4. These formulas are finite rational functions of r on q>0. They are much more conservative than (19)–(20).

Neither completion proves an optimal coefficient or a uniformly bounded coefficient near r=-2. Inverses are justified by (18) and the first completion, not assumed.

## 6. From the algebra to all-background quasiconvexity

Fix q>0 and the completed coefficient. Let F=P_{alpha_*,r}-H, with its fixed closed form omega from (14). For a compactly supported smooth perturbation phi define
\[
 \phi_t=e^{t\Delta}\phi,\quad A_t=B+D\phi_t,
 \quad E(t)=\int_{\mathbb R^2}
 [F(A_t)-F(B)-DF(B):D\phi_t].
\]
For t>0 all differentiated perturbations are rapidly decreasing. Quartic Taylor growth makes E finite. Since omega has homogeneous quadratic coefficients and is closed,
\[
 \omega=d\left(\tfrac14\iota_E\omega\right).
\]
Its pullback by A_t integrates to zero. The primitive contains a derivative of A_t and therefore is rapidly decreasing even at nonzero affine B. Integration by parts gives
\[
 E'(t)=-\int Z_t^TC_r(S_1+\mu S_H)C_r^TZ_t\le0.
\]
In two dimensions, the Gaussian estimate
\[
 \|D\phi_t\|_p\le C_p t^{-(1-1/p)}\|D\phi\|_1,
 \quad p=2,3,4,
\]
and the bound
\[
 |F(B+V)-F(B)-DF(B):V|
 \le C_F(|B|^2|V|^2+|B||V|^3+|V|^4)
\]
show E(t)->0 as t->infinity. Strong heat continuity gives E(t)->E(0) as t decreases to zero. Thus E(0)>=0. The linear integral vanishes, yielding quasiconvexity for smooth compact perturbations at every B.

Strong W^(1,4) density and the quartic difference estimate pass the result to every W_0^(1,4) perturbation in a bounded Lipschitz domain. On a torus the primitive is periodic and exact, and heat removes all nonconstant gradient modes, giving the same conclusion. No domain-dependent coercivity constant enters this part of the proof.

For the quantitative margin use, for vectors x,h in R^2,
\[
 |x+h|^4-|x|^4-4|x|^2x\cdot h\ge\tfrac13|h|^4.
\]
Subtracting the right-hand side gives the explicit nonnegative sum
\[
 6(x\cdot h+|h|^2/3)^2
 +2(|x|^2|h|^2-(x\cdot h)^2).
\]
Thus quasiconvexity of P-H implies an affine Jensen gap at least
\[
 \tfrac13\int|\mathcal CD\phi|^4.
\]
For f=phi1+i phi2, the Fourier identity partial f=B(partial_bar f), the classical complex-valued Beurling bound ||B||4<=sqrt(24), and
\[
 |D\phi|^2=2(|\partial f|^2+|\bar\partial f|^2),\qquad
 2\bar\partial f=\mathcal CD\phi
\]
give
\[
 \int|D\phi|^4\le\frac{625}{4}\int|\mathcal CD\phi|^4.
\]
This proves (1). The classical estimate is Theorem 1.1 of Banuelos–Janakiraman; its p=4 specialization was inspected in the original PDF. No sharp-norm claim is used.

For zero-boundary functions, zero extension supplies the whole-plane estimate. For periodic functions, apply the whole-plane estimate after multiplication by large smooth cutoffs, divide by area, and pass to the limit; the differentiated-cutoff terms vanish. Zero-end-profile strips may first be periodized across their zero traces. This establishes the asserted geometry-independent constant.

All these functions remain quadratically acoustically degenerate at (I,e12):
\[
 F_{\alpha,\beta,\gamma,\delta}(I+t e_{12})
 =F_{\alpha,\beta,\gamma,\delta}(I)+\alpha t^4.
\]
Subtracting any positive multiple of |A|^4 therefore destroys rank-one convexity there. The coercivity is pure fourth-order integrated coercivity, not positive quadratic acoustic curvature.

## 7. Completing the full coefficient projection

Necessity in Theorem C was proved in Section 3. For sufficiency, delta=0 is immediate from convexity of H and u^2 and polyconvexity of j^2.

If delta!=0 and (6) holds, 6 beta+delta>0, so the quantities gamma0 and r0 in (7) are defined and gamma0>0. Equation (10) implies gamma>=gamma0.

If delta>0, then r0=(6 beta+delta)/delta>0. If delta<0, the strict condition 2 beta+delta>0 gives beta>-delta/2 and hence r0=1+6 beta/delta<-2. Thus Theorem A applies. Direct algebra gives
\[
 \boxed{
 F_{\alpha,\beta,\gamma,\delta}
 =\gamma_0 P_{\alpha/\gamma_0,r_0}
 +(\gamma-\gamma_0)j^2.}                               \tag{22}
\]
The second summand is handled through its usual polyconvex Jensen inequality. This proves the finite completion and its gamma0 H subtraction. It also shows why the curved threshold family is sufficient for the entire projected face: the remaining gamma is a nonnegative determinant-square term.

For r!=0, (12) gives necessity in Theorem B; Theorem A gives sufficiency on q>0; r=0 is the explicit exceptional case. This completes all the stated equivalences.

There is also a normalization limitation. On this face the acoustic normalization is Lambda(F)=64 alpha+16 beta+4 gamma. For a fixed projected triple, increasing alpha sends F/Lambda(F) towards H/64. The theorem is global in the remaining coefficient ratios, but does not guarantee coverage of a uniformly large region away from that convex ray in the normalized nine-coefficient cone. No uniform positive separation from the polyconvex cone is asserted.

The projected result is not vacuous due to arbitrarily large alpha. For every r in (-3,-2),
\[
 P_{\alpha,r}(I)=\frac{(r+2)(r+3)}6<0
\]
independently of alpha. Let J0=diag(1,-1). Give each of +/-MI mass 1/[2(1+M^2)] and each of +/-J0 mass M^2/[2(1+M^2)]. This law has zero matrix mean and zero determinant mean, while
\[
 \mathbb E P_{\alpha,r}(A)
 =\frac{M^2}{1+M^2}[M^2P_{\alpha,r}(I)+P_{\alpha,r}(J0)]<0
\]
for sufficiently large finite M. Convex Jensen in (A,det A) is impossible. Thus the completed functions in this whole open interval are non-polyconvex. These discrete laws are not compatible gradient laws.

A simple checked new instance is
\[
 \boxed{27H+\tfrac{55}{32}u^2+j^2-\tfrac{11}{4}uj.}
\]
Its subtraction by H has an exact rational positive Gram certificate, so (1) holds. Its conformal value is -1/32. The standalone verifier reconstructs its certificate and all 18 positive LDL pivots. The original alpha=3 certificate for G remains better than the universal construction at r=-5/2.

Representative conservative sufficient integer coefficients from (19)–(20) are:

| r | sufficient alpha |
|---|---:|
| -3 | 49 |
| -11/4 | 27 |
| -5/2 | 57 |
| -9/4 | 1435 |
| -201/100 | 1298860576 |
| 1/2 | 584839 |

These are diagnostic illustrations of a universally proved construction, not empirical evidence for the theorem, and not optimal thresholds. The large values near -2 should not be confused with the much smaller necessary lower bound; only the divergence itself is unavoidable.

## 8. An actual obstruction to universal constant-heat positivity

Let the normalized torus be [0,2 pi]^2 and start with
\[
 f_0=\sin x+\sin y,\qquad g_0=f_0^2-1.
\]
The map psi0=(f0,g0) has determinant of its gradient identically zero. Along ordinary componentwise heat, writing k=e^(-t),
\[
 f_t=k(\sin x+\sin y),
\]
\[
 g_t=-\tfrac12 k^4(\cos2x+\cos2y)+2k^2\sin x\sin y.
\]
Its determinant is
\[
 J_t=2(k^3-k^5)\cos x\cos y(\sin x-\sin y).
\]
Direct integration, or exact extraction of the constant Laurent-Fourier coefficient, gives
\[
 E(t)=\langle J_t^2\rangle=\tfrac12(k^3-k^5)^2,
\qquad E'(t)=k^6(1-k^2)(5k^2-3).
\]
At k=9/10,
\[
 E'(t)=\frac{212044959}{2000000000}>0.
\]
The independent verifier checks the heat equations, determinant polynomial, constant Fourier coefficient, derivative, and the negative Hessian dissipation directly. It does not merely infer the last sign from a numerical heat simulation.

For a fixed positive-definite diffusion D, let L=D^(1/2), y=L^-1 x, and psi_D(x,t)=psi(y,t). Then psi_D solves that D-heat equation. Its gradient determinant is det(D_y psi)/det L, and its normalized energy on the transformed lattice torus is multiplied by (det L)^(-2)>0. Thus its derivative is still positive. Large smooth cutoffs also transfer the negative dissipation to compactly supported compatible maps: the normalized leading contribution is the negative periodic average times the positive integral of the fourth power of the cutoff, while differentiated-cutoff errors vanish.

For a universally null correction N[psi], any proposed positivity
\[
 \mathcal D_{D,j^2}[\psi]+N[\psi]\ge0,
 \qquad\int N[\psi]=0
\]
contradicts the negative integral just established. This excludes not just SOS corrections but *all* corrections retaining those two properties for the same fixed heat operation.

The conclusion is deliberately limited. It does not exclude nonlinear flows, a different Lyapunov quantity, auxiliary variables, or combining separate variational inequalities. In fact, the proof of Theorem C does combine them: heat for the completed core, determinant Jensen for the remaining j^2. Bruno–Pasqualotto's Appendix A also uses determinant-square polyconvexity as a separate addition. The present counterexample is an explicit independent explanation of why single-flow inclusion cannot be assumed.

## 9. Relation to the full nine-coefficient cone

There is a useful exact acoustic representation already implied by classical mathematics. For a left-SO(2)-invariant quartic, target rotation reduces rank-one testing to e1 tensor (n,m). Write its acoustic polynomial as
\[
 D^2F(A)[e_1\otimes(n,m),e_1\otimes(n,m)]
 =x^T(n^2M_{11}+2nmM_{12}+m^2M_{22})x,
\]
where x=vec A. This is a two-by-four biquadratic form. Calderon's sum-of-squares theorem for a two-dimensional factor implies that rank-one convexity is equivalent to existence of a skew four-by-four matrix K with
\[
 \begin{pmatrix}
 M_{11}&M_{12}+K\\M_{12}-K&M_{22}
 \end{pmatrix}\succeq0.                               \tag{23}
\]
This is an application of inherited mathematics, not a new theorem claimed here. The six free skew entries give an exact spectrahedral-shadow description of the acoustic cone.

It does not prove heat representability. The full corrected heat density is biquadratic in four matrix entries and six second-jet entries, not a two-dimensional factor. Moreover, Section 8 shows that even unrestricted pointwise positivity cannot repair every fixed-heat dissipation.

The shear face has a geometric covariance beyond its chosen coordinates. Suppose an invertible acoustic background A0 and a rank-one direction R0 satisfy
\[
 \operatorname{tr}(A_0^{-1}R_0)=0.
\]
After a target rotation and an invertible input-linear change, this is the contact (I,e12), up to rescaling the rank-one direction. To see it, write R0=a tensor b, choose a target rotation O with Oe1 parallel to a, and use S=O^-1 A0. The trace condition makes b^T proportional to e2^T S, so R0 is proportional to O e12 S. Composition F(O A S) preserves rank-one convexity and quasiconvexity and retains left rotational invariance. The corresponding transformed distortion is still elliptic on compatible gradients. Thus the completion theorem transports to these trace-free invertible contacts.

This does not cover trace-nonzero contacts, singular acoustic backgrounds, simultaneous multiple-contact intersections, or the sharp alpha boundary within the current face. Those are distinct remaining obligations.

## 10. Attribution, limitations, and decisive next work

Bruno–Pasqualotto supplies the heat/exact-form method and its two-sided rotational quartic theorem. The incoming Astra work supplies the particular G certificate, elliptic-distortion transfer, and moving acoustic support. Standard Schur complements, LDL factorizations, Gershgorin bounds, null-Lagrangian Jensen, and the Beurling estimate are inherited tools.

The newly constructed objects and deductions here are the universal isotropic identity, the explicit null correction with the quotient property (16), the positive acoustic block (17) on both unbounded parameter components, the exact full shear-face projection theorem, and the explicit compatible heat-monotonicity obstruction. Their historical novelty is not cleared by the literature inspected. The result is its proof and certificate, not an assertion that no earlier argument could imply it.

The current theorem decides whether a finite H-completion exists. It does not decide whether a particular already rank-one-convex coefficient alpha is large enough for quasiconvexity. Within an admissible projected triple, the ROC and QC fibres are upward intervals; this work proves both have finite thresholds, not that the thresholds coincide.

The next decisive mathematical target is therefore a *sharp fibre theorem* for this face, or a completion construction for a genuinely different acoustic-contact type. A universal theorem identifying the raw constant-heat cone with the rank-one-convex cone is now ruled out by j^2. Any proposed global operation must either include a separate minor-Jensen channel, change the flow, or move beyond heat monotonicity.

Failed-case records are preserved with their proper scope: the old r=-8/3 matrix failure is one-certificate failure; r=-2 is an actual ROC obstruction for the curved coefficients; j^2 is an actual universal fixed-heat obstruction but remains quasiconvex. None is a Morrey counterexample.

## 11. Verification and reproducibility

Run:

```
python verify_global_structure.py
```

It requires only Python and SymPy plus `GLOBAL_COMPLETION_CERTIFICATE.json`. It reads no network resource, discovery pickle, optimizer, or original repository checkout. Its receipt records the universal polynomial identities, closedness, primitives, quotient identities, pivot formulas, acoustic obstructions, full coefficient decomposition, exact periodic dissipation, and rational completed instances.

The universal positivity conclusion is proved by Sections 5–6. Sample instance checks are additional safeguards, not a substitute for that proof. The script also regenerates `SIMPLE_NONPOLYCONVEX_EXAMPLE.json`.

`compile_completion.py` evaluates either sufficient coefficient formula for any rational r with r(r+2)>0 and exports an exact instance. No polynomial-time bit-complexity bound or optimality guarantee is asserted. The fixed matrices are small, but rational numerator and denominator sizes can grow near singular parameter boundaries.

The original supplied package is kept separately as a pinned input, with its hash and fresh replay logs. Original repository files and user Library contents were not modified.

Primary sources and exact access scope are recorded in `SOURCES_AND_REVIEW.md`.
