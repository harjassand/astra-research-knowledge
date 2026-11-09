# Tangential acoustic rigidity of the transformed invariant quartic cone

Date: 9 November 2026.
Status: author-derived analytic candidate. No independent review, numerical search, scientific execution, general quasiconvexity solution, or historical-priority claim is made.

## 1. Question and answer at the earned scope

Can the original anisotropic planar quartic J_r in Astra N1496 be certified merely by positive combinations and coefficientwise limits of arbitrary invertible left/right coordinate transforms of the full bi-rotational rank-one-convex quartic cone?

The answer is NO for every r>0. This includes the entire cone covered by Bruno and Pasqualotto, arXiv:2608.06367v1, Theorem 2 and Appendix A, not just the Dacorogna--Marcellini one-parameter subfamily. The obstruction survives singular-transform limits, arbitrary positive mixtures and coefficientwise closure.

This is a certificate-class exclusion. It does not show that J_r is not quasiconvex. It does not settle the unrestricted original normal-coupling problem. The source itself reports r=1 as an already proved quasiconvex control, so a negative Jensen interpretation would be particularly wrong.

## 2. Exact cone

For F in R^(2x2), set s(F)=|F|_F^2 and d(F)=det F. Define

  W_t(F)=s(F)^2+4t s(F)d(F)+(6t^2-2)d(F)^2,  -1<=t<=1.

The primary theorem gives the complete bi-SO(2)-invariant rank-one-convex homogeneous quartic cone:

  Q(F)=a s(F)^2+b s(F)d(F)+c d(F)^2,
  a>0, |b|<=4a, c>=-2a+3b^2/(8a),

or a=b=0,c>=0. Equivalently,

  Q=a W_t+mu d^2, t=b/(4a), mu>=0.

The primary also proves these Q are quasiconvex. We use its algebraic cone characterization; the exclusion below does not require importing its quasiconvexity proof.

Let C be the coefficientwise closed positive conic hull of Q(L F R), for all such Q and all real invertible L,R. Coefficients are in the finite-dimensional vector space of real homogeneous quartics in the four entries of F.

Invertible left/right transformations preserve quasiconvexity: use a linear change of target and domain in the defining gradient inequality. Positive sums preserve it, and coefficientwise convergence preserves each fixed compactly supported test integral. Hence C is a legitimate sufficient quasiconvexity cone, provided the primary theorem is accepted.

## 3. General tangential-contact theorem

THEOREM. If f belongs to C and there are matrices A,H satisfying

  det A != 0, rank H=1, cof(A):H=0,
  D^2 f(A)[H,H]=0,

then f=C0+nu (det F)^2 for a convex homogeneous quartic C0 and nu>=0. In particular f is polyconvex.

The condition describes a full-rank point on a constant-determinant rank-one line: det(A+zH)=det A for every z.

### 3.1 Compact normalization pays arbitrary transforms and limits

Normalize L and R to Frobenius norm one, absorbing their fourth-power scale into the nonnegative coefficient a. Every finite conic combination has a representation

  f_n(F)=integral W_t(L F R) dmu_n(t,L,R)+nu_n d(F)^2,

where mu_n is a finite positive measure on the compact set
[-1,1] x {||L||_F=1} x {||R||_F=1}; at this stage its support uses invertible L,R, and nu_n>=0.

Let Lambda(f) be the average of f(x y^T) over independent uniform unit-circle vectors x,y. Since det(x y^T)=0,

  Lambda(W_t(L F R))
  =average |Lx|^4 * average |R^T y|^4
  >=1/16.

Indeed, for a positive 2x2 matrix B with tr B=1,

  average (x^T B x)^2=[(tr B)^2+2 tr(B^2)]/8>=1/4.

Thus the masses mu_n(K) are bounded by 16 Lambda(f_n). If f_n converges coefficientwise, these masses are uniformly bounded. Also |W_t(L R)|<=9/4, because |LR|_F<=1 and |det(LR)|<=1/4. Evaluation at F=I consequently bounds nu_n:

  0<=nu_n<=|f_n(I)|+(9/4)mu_n(K).

Taking a weakly convergent subsequence of measures and an ordinary convergent subsequence of nu_n gives

  f(F)=integral W_t(L F R) dmu+nu d(F)^2,

now permitting singular L or R. Polynomial coefficients are continuous on the compact parameter set, so this representation is exact, not a pointwise approximation assertion.

### 3.2 Every genuinely non-polyconvex atom charges the contact

All atoms are rank-one convex, including singular-transform limits, so their acoustic values at (A,H) are nonnegative.

For invertible L,R, put A'=LAR and H'=LHR. These retain det A'!=0, rank H'=1, and cof(A'):H'=0. Proper target and domain rotations put H'=sigma E11, sigma>0. Write the rotated A' as [[x,y],[z,w]]. The determinant derivative forces w=0, while det A'=-yz!=0, so y and z are both nonzero.

For any homogeneous quartic, polarization gives

  D^2 W_t(A')[H',H']=D^2 W_t(H')[A',A'].

A direct differentiation at E11 gives

  D^2 W_t(E11)[A',A']
  =12(x+t w)^2+4[(y-tz)^2+(1-t^2)z^2].

It is strictly positive when |t|<1. Therefore an invertibly transformed atom with zero contact must have |t|=1. At these endpoints,

  W_(+1)=(s+2d)^2,
  W_(-1)=(s-2d)^2,

which are convex: s+2d=(F11+F22)^2+(F12-F21)^2 and s-2d=(F11-F22)^2+(F12+F21)^2.

If L or R is singular, det(L F R)=0 and the atom is |L F R|^4, also convex.

Finally, D^2(d^2)(A)[H,H]=2(cof(A):H)^2=0. Zero total contact in the positive integral therefore forces almost every contributing atom to be convex. Its integral C0 is convex. This proves the theorem.

## 4. Application to the ORIGINAL J_r

Use the exact original source convention

  F=[[a,b],[c,d]], u=a^2+c^2, v=b^2+d^2, j=ad-bc,
  alpha=3r/[8(r+2)], beta=r(r-1)/6,
  J_r=alpha(u+v-2j)^2+beta u^2+j^2+r u j, r>0.

Set

  k=(2r+1)/3>1/3,
  B=(3k-1)/[8(k+1)]>0,
  F0=(5k+1)/[2(k+1)].

(The scalar F0 here is a coefficient, not a matrix or a changed density.) Then exactly

  J_r=B[k^2 u^2+v^2+2uv+4k u j-4v j]+F0 j^2.

Choose

  A=[[0,k],[1,0]], H=E11.

We have det A=-k, cof(A):H=0 and

  D^2 J_r(A)[H,H]=0.

For clarity, the coefficient of a^2 at this A is
2Bk^2+2Bk^2-4Bk^2=0. No limiting r or approximate contact is used.

The general theorem would make J_r polyconvex if J_r belonged to C. Section 5 shows directly that it is not polyconvex for any r>0. Therefore

  J_r NOT IN C, for every r>0.

This is stronger than excluding one chosen heat metric, one finite grid, or one bounded collection of isotropic atoms.

## 5. Explicit local obstruction to polyconvexity

This calculation is included in full rather than assuming source status.

If a finite polynomial J is polyconvex, J(F)=g(F,det F) for a convex g. Since g is finite on the determinant graph and that graph has convex hull R^5, g is finite everywhere and has a supporting affine functional at every (A,det A).

To verify the convex-hull statement, for arbitrary (A,z) choose R with det R=z-det A. The midpoint of (A+R,det(A+R)) and (A-R,det(A-R)) is (A,z).

Consequently there must be a real lambda with

  P(X)=J_r(A+X)-J_r(A)-DJ_r(A):X-lambda det X>=0

for every X. Thus D^2 J_r(A)-lambda D^2 det is positive semidefinite. Because H=E11 has zero quadratic value, its whole row in that positive semidefinite form must vanish. The (a,d) entry fixes

  lambda=-(3/2)k(k+1).

The (b,c) block of this corrected Hessian is exactly

  [[(3k+1)^2/2, k(3k+1)],
   [k(3k+1),     2k^2]].

It has null vector (h,1), where h=-2k/(3k+1). Put

  V=[[0,h],[1,0]].

Then the constant, linear and quadratic coefficients of P(tV) vanish. The cubic coefficient is

  C3=2 k^2(3k-1)(k+1)/(3k+1)^3>0.

A direct expansion verifies this as

  C3=[(3k-1)h^3+(9k+1)h^2+4kh]/2.

Since J_r is homogeneous quartic,

  P(tV)=C3 t^3+J_r(V)t^4.

For sufficiently small negative t this is negative, contradicting the supporting-plane requirement. This proves non-polyconvexity for every r>0.

This is a local support obstruction, not a compatible periodic gradient construction. V need not be rank one, and the negative polynomial P is not the quasiconvex Jensen gap.

## 6. What remains genuinely hard

No positive quasiconvexity certificate or negative compatible Jensen field has been produced for the unrestricted original J_r. The source's corrected density, Hessian/normal-free theorem, and finite Fourier searches do not settle this.

The new route exclusion says that arbitrary positive closure of all coordinate-transformed bi-rotational quartics cannot bridge the gap. A successful argument must use more than that cone, for example a genuinely coupled compatible-gradient identity, a nonlocal gradient-aware evolution, or an actual negative Jensen field.

The source reports J_1 as a proved QC control. Subject to that separate theorem, J_1 gives a QC density outside C. We have not independently reconstructed that positive source proof in this note, and do not use it to prove the exclusion.

## 7. Source and overlap ledger

Astra pin:
bb16dbf0e9c9b9ecaacfd10f577aedef51bd2e0e.

Governing original density/ROC and restricted completion:
research/2026-10-31-coupled-quartic-extension-original-roc-and-fixed-fiber-cost/source/final/outputs/quartic_coupling/PROOF.txt,
SHA256 948c720458f8e1eafd1da31442603dae912797a5bd1395f7a2156a5274ab9ff1.
Read Sections 1-7 and 8-13 through GitHub connector in this task. The source explicitly leaves general-U QC of original J_r unresolved and reports no negative proposal from its bounded Fourier search.

The original_roc.py source was read, not run. It verifies a different global ROC calculation; no execution is claimed here.

Strong primary:
Bruno and Pasqualotto, Quasiconvexity for the Dacorogna--Marcellini Energy,
arXiv:2608.06367v1, https://arxiv.org/html/2608.06367v1.
Directly read Theorems 1-2, heat/exact-form strategy and Appendix A. Appendix A supplies the full invariant cone and its explicit boundary family, rather than an isotropic-subfamily guess. We do not claim absence of other prior or a full independent audit of that paper.

The 1993 Dacorogna--Koshigoe primary was search-located; its full proof was not read. It is not cited as resolving the one-sided anisotropic family.

Active-user overlap searches for quasiconvexity returned research monitoring/ranking conversations, not an identified active original-quartic assignment. Search is not proof of universal absence. Complete quantum channel comparison, sharp signing, edit codes, lithium recovery, DAC and current fluid/kinetic/inference lanes were avoided.

## 8. Evidence and resource status

All new statements here are hand-derived polynomial/compactness arguments. No numerical optimization, symbolic solver, Fourier search, PDE, hardware experiment, source-code replay or data acquisition occurred. Writing/hashing the note is not scientific validation.

The finite-dimensional closure proof pays possible diverging coordinate transforms instead of silently restricting condition numbers. It gives an analytic obstruction, not an evaluated separation distance or efficient complete quasiconvexity algorithm.

Independent review and exact arithmetic qualification remain pending. Historical priority and field-level impact are unestablished. This does not solve Morrey's problem or establish a material device capability.

