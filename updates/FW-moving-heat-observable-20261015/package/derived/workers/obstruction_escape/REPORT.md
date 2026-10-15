# Angular determinant supports are necessary for the exposed FV quartic

Research date: 15 October 2026. Status: exact internal mathematical derivation; external correctness review and historical priority UNKNOWN. The original goal of a new positive certificate operation, or a decision of unrestricted PC/QC for the FV ray, is **NOT ACHIEVED**.

The main result in Sections 1–6 passed an independent internal analytic and exact audit in `../smooth_null_classification/pc_multiplier_audit/AUDIT.md`; its separate verifier imports no author script. This is internal corroboration, not external validation. The separately scoped higher-jet discussion in Section 7 has not received the same complete audit.

A concrete new obstruction is achieved. The exposed FV quartic has no determinant-support selection with a second-order Peano expansion at the zero matrix. In particular it has no polynomial minor support of any degree, no SOS-polyconvex certificate of any degree, and no convex polynomial lift of any degree. This is stronger than failure of a particular SOS search: the proof only uses pointwise nonnegativity of a support remainder.

Actual polyconvexity and quasiconvexity of the quartic remain **UNKNOWN**. If it is polyconvex, its supporting determinant coefficient must have genuinely angular second-order behavior at the origin. The result does not construct such a coefficient.

## 1. Inputs, notation, and precise theorem

For row-major matrix coordinates

\[
 A=\begin{pmatrix}a&b\\c&d\end{pmatrix},\qquad
 u=a^2+c^2,\quad v=b^2+d^2,\quad w=ab+cd,\quad q=ad-bc,
\]

put \(r=u-v\), and retain exactly the supplied polynomial

\[
 F=u^2+v^2+\frac{166}{3}uv-\frac{460}{9}w^2
       -\frac{52}{9}qr.                                      \tag{1}
\]

Its rank-one convexity, exposed extremality in the full nine-coefficient left-SO(2)-invariant ROC cone, pointwise lower bound \(F(A)\ge |A|^4/2\), and exclusion from every specified fixed strongly parabolic output-matrix corrected-heat class are inherited claims. The present result does not use their full proofs: it reconstructs the polynomial symmetries and acoustic contact identities that it needs directly from (1).

Define the planar determinant-support remainder

\[
 \mathcal R_\lambda(A,H)
 =F(A+H)-F(A)-DF(A):H-\lambda(A)q(H).                       \tag{2}
\]

A differentiable finite planar integrand is polyconvex exactly when there is some selection \(\lambda\) with \(\mathcal R_\lambda\ge0\) for all A,H. No regularity of that selection is part of the criterion. This is the classical minor-support characterization, recalled in [Fantuzzi et al., Proposition 2.3](https://arxiv.org/html/2604.11124v1#S2.SS2), and specialized in the supplied FV addendum using Aubert's general planar criterion.

**Theorem.** There is no function \(\lambda\), defined on a neighborhood of zero, such that (2) is nonnegative for every A in that neighborhood and every H, and

\[
 \lambda(A)=c+L(A)+Q(A)+o(|A|^2)\quad(A\to0),              \tag{3}
\]

where c is constant, L is linear, and Q is a homogeneous quadratic polynomial. It is enough to require (2) for all sufficiently small A and H; homogeneity supplies the global quadratic limit.

Consequently:

* no globally valid determinant-support selection is C2 at zero;
* no globally valid determinant-support selection is polynomial, of any degree;
* F is not SOS polyconvex in Definition 2.5 of the cited Fantuzzi et al. paper, even when arbitrary polynomial degrees are allowed;
* F has no convex polynomial lift \(g(A,z)\) with \(g(A,q(A))=F(A)\), of any degree;
* F has no convex lift that is C3 near \((A,z)=(0,0)\).

These implications do not establish non-polyconvexity. The definition permits nonsmooth lifts and irregular/angular support selections.

## 2. Homogeneity reduces any Peano selection to a quadratic one

Quartic homogeneity gives the exact identity

\[
 F(tA+tH)-F(tA)-DF(tA):(tH)
 =t^4\,[F(A+H)-F(A)-DF(A):H].                            \tag{4}
\]

Apply (2) at \((tA,tV)\), where V is any fixed matrix with positive or negative determinant. Dividing by \(t^2\), one obtains

\[
 t^2\,[F(A+V)-F(A)-DF(A):V]-\lambda(tA)q(V)\ge0.         \tag{5}
\]

Use, for example, V=I and V=diag(1,-1). The two signs show \(\lambda(tA)=O(t^2)\) for every fixed A. At A=0 the same argument forces c=0, and (3) then forces L=0. Substitute (3) in (5), divide by \(t^2\), and let t decrease to zero. The result is

\[
 F(A+H)-F(A)-DF(A):H-Q(A)q(H)\ge0
 \quad\text{for every }A,H.                              \tag{6}
\]

Thus a Peano selection would supply a homogeneous quadratic support. This analytic step uses no SOS restriction, optimizer output, or assumption of a polynomial convex lift.

There is also a useful size bound with no regularity hypothesis. The Hessian consequence of (2), tested on I and diag(1,-1), bounds lambda(A) between two homogeneous quadratic polynomials in A. Thus every valid selection is O(|A|^2). A global polynomial selection would consequently have degree at most two even without the Peano limit argument.

## 3. Symmetry reduces the quadratic multiplier to two coefficients

F is invariant under every proper target rotation and under input-column exchange

\[
 A\longmapsto OA\quad(O\in SO(2)),\qquad
 A\longmapsto AP,\quad P=\begin{pmatrix}0&1\\1&0\end{pmatrix}.
\]

If a linear transformation T preserves F and changes determinant by the sign \(\sigma_T\), then \(\sigma_T Q(TA)\) is another valid support multiplier. Average over SO(2), then average the original and the determinant-sign-transformed input swap. Convex combinations preserve (6), since it is affine in Q.

Every left-rotation-invariant homogeneous quadratic is a combination of u,v,w,q. The column-swap antisymmetry leaves exactly

\[
 Q(A)=\alpha q(A)+\beta r(A).                            \tag{7}
\]

The standalone verifier independently solves the general ten-coefficient quadratic symmetry system and finds a two-dimensional kernel. This is an exact reduction of every quadratic multiplier, not an initially imposed ansatz.

## 4. The acoustic contact forces one exact relation

Set

\[
 P_0(k)=17k^4-314k^2+17,
\]

\[
 A(k)=\begin{pmatrix}
 203-17k^2&k(85k^2-1551)\\
 2k(944-51k^2)&134
 \end{pmatrix},\qquad
 R(k)=e_1\otimes(1,k).
\]

The polynomial P0 has four distinct real roots. Exact substitution gives

\[
 D^2F(A(k))[R(k),R(k)]=0\quad(P_0(k)=0).                 \tag{8}
\]

For any valid support (2), its Hessian with respect to H at H=0 is

\[
 K_A=D^2F(A)-\lambda(A)D^2q\succeq0.                    \tag{9}
\]

At the contacts q(R)=0, so (8) gives \(R^T K_A R=0\). A PSD matrix annihilates every vector of zero quadratic value. Therefore

\[
 D^2F(A(k))R(k)=Q(A(k))D^2q\,R(k).                     \tag{10}
\]

All four coordinates of (10) are reduced exactly modulo P0. In particular

\[
 q(A(k))\equiv185744-11024k^2,
 \qquad r(A(k))\equiv\frac6{13}q(A(k)),                  \tag{11}
\]

and \(q(A(k))\ne0\) at every root, as verified by the polynomial gcd. The complete linear system in alpha,beta has exactly the solution

\[
 \boxed{\alpha+\frac6{13}\beta=\frac{3968}{39}.}          \tag{12}
\]

Equivalently every surviving quadratic multiplier is

\[
 Q(A)=\frac{3968}{39}q(A)
       +\beta\left(r(A)-\frac6{13}q(A)\right).           \tag{13}
\]

## 5. Two integer test pairs contradict that entire family

For a homogeneous quartic,

\[
 F(A+H)-F(A)-DF(A):H
 =F(H)+DF(H):A+\frac12D^2F(A)[H,H].                     \tag{14}
\]

Put H=tV in (2). For t nonzero and \(F(V)>0\), its nonnegativity for every real t requires the discriminant condition

\[
 2F(V)D^2F(A)[V,V]-(DF(V):A)^2
              -4Q(A)F(V)q(V)\ge0.                    \tag{15}
\]

After (13), the left side is \(C_0-\beta C_b\). Here are two exact integer pairs, together with values reconstructed from (1):

| Pair | A in row-major order | V in row-major order | C0 | Cb | Necessary bound |
|---|---|---|---|---|---|
| upper | (-6,-3,-1,6) | (1,-2,0,1) | -1142144/27 | 14560/3 | beta <= -35692/4095 |
| lower | (2,0,0,1) | (3,0,0,-2) | 957266072/1053 | -1465992/13 | beta >= -119658259/14843169 |

The bounds are incompatible:

\[
 -\frac{119658259}{14843169}>-\frac{17}{2}
 >-\frac{35692}{4095},                                 \tag{16}
\]

with exact gap

\[
 \frac{4420201927}{6753641895}>0.
\]

Writing U and L for the two displayed left sides of (15), the independent audit found the compact positive-combination contradiction

\[
 549747\,U(\beta)+23660\,L(\beta)
 =-\frac{141446461664}{81}<0.
\]

Both weights are positive, so U and L cannot both be nonnegative.

Thus no quadratic multiplier survives. Sections 2–3 prove the theorem for every Peano selection.

These are actual rational support-countertests, rather than merely negative eigenvalues. The inner quadratic in t is minimized at

\[
 t_\mathrm{upper}=-\frac8{91},\qquad
 t_\mathrm{lower}=-\frac{6442}{20361}.
\]

For any beta at least -17/2, the upper test gives a negative value of (2); for any beta at most -17/2, the lower test does. The two directions use different backgrounds, so this proves failure of one globally quadratic selection. It is not a single-background failure of all scalar supports.

## 6. Why this excludes SOS supports and polynomial convex lifts

A general polynomial minor support would take the form

\[
 F(Y)-F(A)-p(A):(Y-A)-\ell(A)[q(Y)-q(A)]\ge0.
\]

At Y=A the nonnegative remainder vanishes, so its derivative in Y vanishes. Hence

\[
 p(A)=DF(A)-\ell(A)\operatorname{cof}A.
\]

Use

\[
 q(A+H)-q(A)-\operatorname{cof}A:H=q(H)
\]

to recover (2) with lambda=ell. A polynomial ell contradicts the theorem. An SOS-polyconvex support is a polynomial minor support with an additional SOS condition, so it is excluded without using that extra condition.

Likewise, a differentiable convex lift supplies the supporting coefficient

\[
 \lambda(A)=\partial_z g(A,q(A)).
\]

If g is polynomial, this lambda is polynomial; if g is C3 near (0,0), lambda is C2 near zero. Both are impossible.

**Matched scope.** [Fantuzzi et al., Remark 2.1](https://arxiv.org/html/2604.11124v1#S2.SS4) leaves the possible PC versus SOS-PC gap open for planar quartics in the inspected version. A proof that this particular F is PC would therefore supply a counterexample in precisely that regime. No such PC proof is supplied here. Their Proposition 2.4 already demonstrates that polynomial convex lifts can be too restrictive, using a different quartic that *does* have a polynomial SOS minor support. Our obstruction is against polynomial minor supports themselves, a stronger certificate restriction for this F. Historical priority of the present exact example is not established.

Using the inherited exposed-ray decomposition theorem, there is also no finite positive decomposition of F into left-invariant heat-certified quartics from its stated class and homogeneous quartic SOS-polyconvex addends. The inherited theorem makes every heat summand zero; the remaining sum would itself be SOS polyconvex. The unrestricted heat-plus-PC question remains unchanged and UNKNOWN.

**The angular alternative is precise, but unresolved.** Let K(A) be the set of scalar values making (2) nonnegative for all H. If F is PC, K(A) is a nonempty compact interval, bounded by the Hessian tests above. It satisfies K(tA)=t^2 K(A), K(OA)=K(A), and K(AP)=-K(A). Its midpoint is therefore an equivariant degree-two homogeneous selection. It is O(|A|^2) and differentiable at zero with derivative zero; the theorem proves it has no quadratic second-order Peano expansion.

The radial H variable can be eliminated explicitly. Since F(V)>0 for V nonzero, put

\[
 J_A(V)=\tfrac12D^2F(A)[V,V]
       -\frac{(DF(V):A)^2}{4F(V)}.
\]

Then the candidate interval endpoints are

\[
 L_F(A)=\sup_{q(V)<0}\frac{J_A(V)}{q(V)},\qquad
 U_F(A)=\inf_{q(V)>0}\frac{J_A(V)}{q(V)}.
\]

Directions of zero determinant already satisfy the support inequality by the supplied rank-one convexity of F. Thus PC is exactly the remaining all-A inequality L_F(A)<=U_F(A); when it holds, their midpoint is an explicit angular support selection. This eliminates the radial increment and regularity assumptions from the next search. We have not proved that width inequality.

## 7. A separately scoped higher-jet reduction

This section records a useful failed route. It uses classical null-Lagrangian facts rather than asserting historical originality.

Let E(A,z2) be any fixed linear-heat dissipation density, quadratic in the compatible second jet z2. Let

\[
 N(A,z_2,z_3,\ldots,z_m)
\]

be a C2 finite-order local correction, regular on the entire compatible jet space. Assume explicitly:

1. its integral is zero for every constant affine background plus compactly supported smooth perturbation;
2. \(N(A,0,\ldots,0)=0\);
3. \(E+N\ge0\) on **every** compatible finite jet, with no PDE imposed on those jets.

Nullness, after freezing lower jets, makes the highest-order dependence affine on every line in a principal wave direction \(a\otimes\xi^{\otimes m}\). This is the standard higher-order Legendre-Hadamard/null-Lagrangian necessity; [Ball–Currie–Olver (1981), Theorems 3.2–3.4](https://www-users.cse.umn.edu/~olver/e_/bco.pdf) provide the classical framework.

If m is at least 3, E is independent of that highest jet. A nonnegative affine function on the whole real line is constant. The principal wave directions span the symmetric highest-jet space, so N is independent of z_m. Repeating removes all orders above two. This step is a principal-symbol reduction and should be reviewed independently before promotion.

At order two, freezing A gives a planar highest-derivative null integrand. Classical null-Lagrangian classification makes it an affine combination of Hessian Jacobians, hence degree at most two in z2. The stipulated zero baseline kills its constant part; nonnegativity for arbitrarily small positive and negative z2 kills its linear part. Thus N is quadratic in the compatible Hessian. The supplied moving-kernel report's Proposition 2 then represents it as a closed two-form pullback, and its Proposition 3 reduces C2 coefficient dependence at A=0 to a quadratic form in A.

Subject to that classical freezing step, merely adding arbitrarily high but finite regular local jets to a **null correction of the same second-order flow** cannot escape the prior exposed-ray obstruction. This does not address a different higher-order evolution, nonlocal dependence, singular coefficient dependence in A, or a certificate requiring only integrated positivity. The normalization in assumption 2 matters: the broad phrase “variationally null” by itself can include constants or first-order null baselines.

## 8. Nonlinear and nonlocal operations actually tested or derived

**Nonlinear gradient descent.** The formal nonlinear evolution

\[
 \partial_t\phi=\operatorname{div}DF(B+D\phi)
\]

has the exact smooth-solution identity

\[
 \frac{d}{dt}\int [F(B+D\phi)-F(B)]
 =-\int|\partial_t\phi|^2.
\]

This truly escapes the fixed linear operator class. However, its all-background global well-posedness and convergence to the affine state are not established. Those are load-bearing obligations; the identity by itself does not prove QC. At B=0, the supplied pointwise coercivity and quartic homogeneity give decay estimates in a finite-dimensional Galerkin system, but QC at zero was already immediate from F>=0. No new all-background capability follows.

**Exact nonlocal redistribution.** For periodic scalar heat, let e(x) be the uncorrected dissipation and let its spatial mean be bar e. The zero-integral correction

\[
 N=\Delta\Delta^{-1}(\bar e-e)=\bar e-e
\]

makes the corrected density equal to the constant bar e. This is an explicit nonlocal compensation, but positivity is exactly the unresolved integrated heat-monotonicity condition \(\int e\ge0\). It cannot repair a genuine negative integral. It is therefore not a new positivity certificate.

**Compatible Fourier searches.** The scripts tested real sine perturbations with frequency sets

\[
 \{(1,0),(0,1),(1,1)\},
\]

then added (1,-1), then additionally (2,0),(0,2). All output amplitudes were free, the gradient L2 norm was normalized to one, and the affine B was minimized analytically from its quadratic dependence. Two hundred local SLSQP starts were run per reduced class. The smallest observed dissipations were approximately 6, 6, and 4.868377569259287. No negative scalar-heat integral was found. These are finite numerical searches with restricted phases and frequencies, not lower bounds for the full class, proofs of monotonicity, or quasiconvexity certificates.

**Unrestricted PC probes.** Four hundred local minimizations of the contact support remainder found no negative value beyond numerical roundoff. Sixteen further backgrounds, including both conformal orientations, rank-one background, an eigenvector-adapted background, and random backgrounds, passed finite support probes using a multiplier in the middle of the Hessian-support interval. These inconclusive searches motivated the exact obstruction to a *globally smooth selection*. They do not prove a pointwise valid angular selection exists.

**Additional-null/cubic route at the FV contacts.** The forced contact support Hessian has rank exactly three: one principal 3x3 minor reduces to

\[
 -\frac{193857643872256}{459}(2465740k^2-45411777),
\]

whose gcd with P0 is one. Its nullspace is therefore exactly the acoustic rank-one span R(k), and \(DF(R(k)):A(k)=0\) modulo P0. The extra non-rank-one-null/cubic failure available in the incoming F_r family does not transfer directly to these contacts.

## 9. Reproduction, provenance, and remaining work

Run

```sh
python3 verify_pc_multiplier_obstruction.py
```

from this worker directory. The verifier requires only SymPy and the standard library. It reads no optimizer output, saved certificate JSON, upstream manuscript, or pickle. It regenerates F, its invariant quadratic multiplier space, the Bregman identity, four real contact identities, the forced relation, two integer cuts, and their strict rational incompatibility. Its JSON receipt distinguishes checked algebra from the analytic implications proved above.

The discovery scripts use NumPy and SciPy. SciPy was reused read-only through the existing measurement-search dependency directory; it is not required for the exact theorem verifier. Numerical arrays and cut-search history are preserved. An initial SciPy import failure was repaired by setting that existing PYTHONPATH; no upstream scientific bytes were modified.

`READ_SOURCE_RECEIPT.json` hashes each actually inspected local source. The task supplied prior pin 33c1ff7. A later read-only W HEAD check returned `8a1e001ac128468ae8d151c9a859b89ef3b9a664`; this worker did not edit W or infer source identity from that changed branch position. The byte hashes are the source-level anchors.

The next decisive positive route is an explicit non-Peano angular minor support satisfying (2), or a genuine single-background proof that no scalar support exists. For QC, a globally justified nonlinear/nonlocal operation or an exact compatible negative Jensen field is still required. Additional polynomial multiplier degree, a larger SOS minor-support SDP, and regular finite-jet null corrections of the same fixed flow cannot close those obligations.
