# Acquiring a contact hyperplane and counting its critical rays

This note audits the residue geometry and higher-ring lifting used by the parent's raw contact-form compiler. `contact_hyperplane_audit.py` contains independently executed acquisition and lifting code. It does not replace the parent's raw ordinary-fit step. The governing conditions below are checked from the acquired ordinary cubic and its residue third form; no hyperplane, chart decomposition, or root list is supplied.

Write `b=2r+1>=5`, `F=F_(2^d)`, and `A=F[t]/t^e`. A homogeneous ordinary cubic `H` has residue alternating third form `T`. Its traced phase is `lambda_e(H)`, where `lambda_e` is the field trace of the top ring coefficient.

## 1. The hyperplane is the kernel of a manufactured covector

Suppose `T=ell wedge omega`, where `omega` restricts to a nonsingular alternating form on `W=ker(ell)`. Then

\[
\ker\bigl(V^*\longrightarrow\Lambda^4V^*,\ a\longmapsto a\wedge T\bigr)=F\ell.
\]

To prove this, choose `v0` with `ell(v0)=1` and decompose `a=c ell+beta`, with `beta` a covector on `W`. The condition becomes `beta wedge omega=0`. The map `beta -> beta wedge omega` is injective when `dim(W)>=4`: a symplectic basis change sends any nonzero `beta` to `x1`, and `x1 wedge omega` contains the nonzero term `x1 wedge x2 wedge y2`. This argument is valid in characteristic two.

Conversely, a nonzero solution to `ell wedge T=0` implies that the restriction of `T` to `ker ell` is zero. Hence `T=ell wedge i_(v0)T`. Checking that the latter alternating form is nonsingular on the kernel certifies the claimed structure. The algorithm therefore solves the exterior equation, requires a one-dimensional solution space, and checks the nonsingular restriction. It does not assume contact type from a resemblance to an example.

In coordinates, there is one equation for each four-element index set `J`:

\[
\sum_{j\in J}\ell_j T_{J\setminus\{j\}}=0.
\]

This is a `binom(b,4) by b` field matrix, polynomial in `b`. Normalize a nonzero component of `ell` to one. A vector `v0` and a basis of `ker ell` are then immediate. Symplectic elimination on the latter basis makes

\[
T=Z\wedge\sum_{i=1}^rX_i\wedge Y_i.
\]

The audit code checks every transformed third-form coefficient against this identity. This replaces the exponentially growing fixed-rank Macaulay matrix by polynomial-size, acquired linear algebra on this class.

## 2. The hyperplane-at-infinity condition is explicit

On `Z=0`, the cubic has no squarefree monomials, because the residue third tensor restricts to zero. Write it uniquely as

\[
H_0(w,0)=\sum_{i,j}M_{ij}w_iw_j^2,
\qquad \nabla_w H_0(w,0)=M w^{[2]}.
\]

The compiler checks that `M` is invertible. Then every residue critical vector on `Z=0` is zero. Thus every nonzero critical residue lies in the single chart `Z=1`. This is a substantive admissibility condition: for `H=Z sum XiYi`, one has `M=0`, and there are nonzero critical vectors with `Z=0`; a one-chart counter would miss them.

On `Z=1`, the transverse gradient is

\[
g(w)=M w^{[2]}+B w+c,
\]

where `B` is the nonsingular symplectic Hessian. It is an affine binary-linear map on `(b-1)d` bits. Solve it by binary Gaussian elimination and let `kappa` be the dimension of its binary kernel. If consistent, the entire root set is one affine coset containing exactly `2^kappa` points. Every root is simple since the ordinary Jacobian is `B`. Bézout also gives `kappa<=b-1`; invertibility of `M` gives a finite degree-two system with no solutions at projective infinity.

Retain exactly the transverse roots satisfying `H_0(w,1)=0`. Euler's identity `H_0=sum X_i partial_i H_0` shows that these and only these are full projective critical points. The equation is checked only modulo `t` here. The lifted critical value can be nonzero in higher nilpotent layers and must be retained for the radial sum.

The parameter `kappa` is acquired by an exact matrix-rank computation. The generic counting bound is `2^kappa poly(n,L)`, rather than a fixed-module-rank claim. To obtain polynomial space, production must stream the affine-kernel combinations and their lifted rays. Retaining all root or per-ray certificate records costs exponential space; the audit helpers intentionally retain those lists only for their small examples.

## 3. A residue hyperplane suffices for arbitrary higher mixed coefficients

Lift the acquired field basis to the coefficient field of `A`. It is still an invertible `A`-linear basis. The residue covector consequently defines an exact ring-linear coordinate `Z`, whether or not it divides the full ring third form. Any vector on a nonzero critical residue ray has unit `Z`; it is uniquely `u(w,1)` with `u in A^*`.

Higher nilpotent mixed coefficients can make the full transverse gradient nonlinear over the binary coordinates and its Hessian dependent on `w`. No full-ring affine-linearity claim is needed. Each residue transverse root lifts uniquely by ordinary Hensel correction, because its Jacobian modulo `t` is the nonsingular matrix `B`.

Explicitly, having a solution modulo `t^j`, correct it by `t^j v`. The degree-two gradient obeys

\[
g(w+t^jv)=g(w)+t^jBv\pmod {t^{j+1}},\qquad j>=1.
\]

Solve `Bv=[t^j]g(w)` over the field. This manufactures the unique center modulo the next power. After `e-1` corrections, verify every full-ring transverse derivative. The radial critical value is the computed `C=H(w,1)`; only `C mod t=0` is required.

There is a strict example where a global contact lift fails. In rank seven, take

\[
T=Z\wedge(X_1\wedge Y_1+X_2\wedge Y_2+X_3\wedge Y_3)
  +t X_1\wedge X_2\wedge X_3\pmod {t^2}.
\]

A lifted factor `Z+t beta` would require `X1 wedge X2 wedge X3=beta wedge omega` on the transverse space. Every monomial on the right contains a complete symplectic pair; the left contains none. Thus there is no such lift. Uniqueness of the residue exterior-annihilator line rules out a factor with a different residue hyperplane. The audit verifies the corresponding inconsistent field linear system, while successfully acquiring and lifting all 36 critical rays. Four of their computed critical values are nonzero in the nilpotent layer. Therefore requiring a global ring contact factorization would unnecessarily reject a case handled by residue acquisition and Hensel lifting.

## 4. The weighted local sum and its arithmetic

Let `v=(w,1)` be a lifted center and let `C=H(v)`. Suppose a binary quadratic weight `Q` depends only on the first `h` digits, with `3h<=e+1`. Write `m=b-1=2r`.

For fixed radial unit `u`, the complete transverse residue-cell sum is

\[
q^{re}\epsilon_v^{e\bmod2}
(-1)^{\lambda_e(Cu^3)+Q(uv)},
\]

where `epsilon_v` is the normalized sign of the nonsingular residue quadratic Taylor form on the transverse space. To check the exponent, when `e=2s`, summing the last `s` digits in each of the `2r` transverse coordinates forces the unique center modulo `t^s`, leaving `q^(2rs)=q^(re)` free summands. When `e=2s+1`, one remaining field quadratic contributes `q^r epsilon_v`, while the other high digits contribute `q^(2rs)`. The weight is constant on the surviving transverse fibers because `h<=floor(e/2)`.

The unit scale `u_0^3` does not change the normalized sign: every nonzero field scalar has a unique square root, and scaling all transverse variables by that root is a bijection for a homogeneous quadratic. In symplectic coordinates, if the square coefficients of the Taylor form are `A_1,...,A_(2r)`, then

\[
\epsilon_v=(-1)^{\operatorname{Tr}(\sum_{i=1}^r A_{2i-1}A_{2i})}.
\]

The radial sum is the difference of two exact binary Gaussian sums:

\[
U_v=\sum_{u\in A^*}(-1)^{\lambda_e(Cu^3)+Q(uv)}
=\sum_{u\in A}(-1)^{F_v(u)}
 -\sum_{s\in A/(t^{e-1})}(-1)^{F_v(ts)}.
\]

The function `F_v` is quadratic in the `ed` bits of its argument: `u^3=u u^2`, squaring is binary linear, multiplication is binary bilinear, and `u -> uv` is linear. Its rank can be arbitrary. No Walsh expansion is required.

The origin alone recurses. Substitution `X=tY` gives factor `q^(2b)` and new length `e-3`; the quotient weight height falls by one. At lengths two and three the origin contributes `(-1)^Q(0) q^(b(e-1))`. Therefore

\[
S_e=q^{2b}S_{e-3}
+\sum_{\text{acquired residue critical rays }v}
 q^{re}\epsilon_v^{e\bmod2}U_v,
\]

with the stated origin terminals. The condition `3h<=e+1` is stable under recursion. There is no branching recursion tree: only the origin continues. At `e=1`, a separate finite-field terminal remains; a small number of critical rays does not by itself evaluate that field sum. The unconditional executed polynomial family below uses `e=0 or 2 mod3`.

The polynomial input size is explicit: `H` has at most `binom(b+2,3)` coefficients of `ed` bits, `Q` has at most `1+n+binom(n,2)` binary coefficients, and `n=bed`. Hyperplane acquisition, symplectic normalization, polynomial substitution, binary root solving, Hensel lifting, and quadratic elimination all have polynomial-bit cost in `n` and this description. The only root multiplicity factor is the acquired `2^kappa`. Final counts and multipliers have `O(n)` bits. Raw representation acquisition and ordinary fitting are additional charged polynomial steps supplied by the parent compiler. None of these statements says that arbitrary raw cubics acquire this structure.

## 5. A one-ray family at unbounded odd module rank

The parent's stronger family is

\[
J_r=\sum_{i=1}^r
 (X_i^3+X_iY_i^2+Y_i^3+ZX_iY_i),\qquad b=2r+1.
\]

Its transverse square matrix has invertible blocks

\[
M_i=\begin{pmatrix}1&1\\0&1\end{pmatrix},
\qquad B_i=\begin{pmatrix}0&1\\1&0\end{pmatrix}.
\]

On `Z=1`, the equations are

\[
X_i^2+Y_i^2+Y_i=0,\qquad Y_i^2+X_i=0.
\]

Substituting `X_i=Y_i^2` gives `Y_i(Y_i^3+Y_i+1)=0`. The degree-three factor has no binary root, hence is irreducible over `F2`. It has roots in `F_(2^d)` exactly when `3` divides `d`. Consequently, for every `d` not divisible by three the entire transverse binary kernel is zero, independently of `r`. There is exactly one projective critical ray, the `Z` axis, and its critical value and Arf bit are zero.

Arbitrary higher nilpotent coefficients preserve all these residue conditions. An arbitrary allowed quotient quadratic also preserves acquisition and transverse pullout. Thus, after the parent's raw fitting and admissibility checks, this yields `kappa=0` and polynomial time with unbounded odd module rank, for lengths zero or two modulo three. Taking `d>=3` as required by the raw ordinary-fit completeness proof leaves infinitely many degrees, beginning with four and five. The coefficient-level audit additionally checks degrees one and two.

The field divisibility boundary is exact, not heuristic. When `3|d`, each pair has a two-dimensional binary kernel, so `kappa=2r`. At nonzero roots `y` of the irreducible cubic, the chart critical value of one pair is `y+1`. These three values are binary independent: each is nonzero, no two sum to zero, and their total is one. Hence, for the constant-coefficient family, the number of retained critical rays is

\[
N_J(d,r)=
\begin{cases}
1,&3\nmid d,\\
\bigl(4^r+3\cdot2^r+(-2)^r\bigr)/8,&3\mid d.
\end{cases}
\]

The second formula counts length-`r` sums from `{0,e1,e2,e3}` returning to zero in `F2^3`. A surviving tuple uses an even number of nonzero entries, so its total Arf bit is zero. Its full critical value is also zero for the constant-coefficient family. This provides an aggregated count oracle even on the divisibility boundary, but arbitrary nilpotent coefficients or quotient weights need not preserve aggregation. The general robust complexity parameter remains the acquired kernel dimension.

## 6. An all-field family with an exact field terminal

A complementary explicit family is

\[
K_r=Z\sum_{i=1}^rX_iY_i+
\sum_{i=1}^r(X_i^2Y_i+X_iY_i^2),\qquad r>=2.
\]

It has `(4^r+2^r)/2` critical rays over every binary field. Indeed, chart critical coordinates are `Xi,Yi in {0,1}` and the full critical condition is `sum XiYi=0`. Their critical values vanish exactly over every ring depth. At a pair `(a,b)`, the quadratic Taylor form is `b U^2+UV+a V^2`; hence its total Arf trace is `Tr(sum ab)=0`. All rays have the same positive sign.

For this family alone, those identical contributions can be aggregated without visiting exponentially many rays. Put

\[
N_K=(4^r+2^r)/2.
\]

For `e>=4`, its signed count satisfies

\[
S_e(K_r)=q^{2(2r+1)}S_{e-3}(K_r)
 +N_K(q-1)q^{(r+1)e-1}.
\]

The same ray term applies at lengths two and three, with origin contribution `q^((2r+1)(e-1))`. There is also an exact polynomial field terminal, which removes any point-counting dependency for this specific family.

For fixed `Z`, summing one `Y` variable gives `q` exactly when

\[
X^2+ZX+\sqrt X=0.
\]

After squaring, its nonzero solutions are the roots of `X^3+Z^2X+1`. Let their number be `r_Z`. This cubic is separable: its derivative vanishes at `X=Z`, where the cubic equals one. Thus `r_Z` is zero, one, or three. Define

\[
G=\sum_{x\in F}(-1)^{\operatorname{Tr}(x^3)}.
\]

The numbers `n_0,n_1,n_3` of parameters with the respective root counts are

\[
n_3=(q-2+G)/6,\qquad
n_1=(q-G)/2,\qquad
n_0=(q+1+G)/3.
\]

Here is a direct derivation. Each nonzero `x` determines one parameter `Z^2=x^2+1/x`, so `sum_Z r_Z=q-1`. Two distinct nonzero `x,y` determine the same parameter precisely when `xy(x+y)=1`. Put `s=x+y` and `x=su`; then `u^2+u=s^(-3)`. The number of ordered pairs is

\[
\sum_{s\ne0}\bigl(1+(-1)^{\operatorname{Tr}(s^{-3})}\bigr)=q-2+G.
\]

This is `sum_Z r_Z(r_Z-1)=6n_3`. Together with `n_0+n_1+n_3=q`, the formulas follow. Summing the `r` independent transverse pairs at each fixed `Z` now gives

\[
S_1(K_r)=q^r\left(n_0+2^r n_1+4^r n_3\right).
\]

The remaining `G` is a binary quadratic Gaussian, since `x^3=x x^2`. Thus the displayed terminal and ring recurrence are polynomial in `d,e,r`, using integers of `O((2r+1)ed)` bits. For rank five this specializes to `S_1=q^2(5(q-1)+G)`. This exact aggregation is a useful independent oracle; it does not assert recognition of an arbitrary disguised uniform family or persistence under arbitrary weights.

The original F8 nine-ray example is obtained by deleting `Z^3` from the earlier smooth rank-five family with `c1=alpha,c2=alpha^2`. In its chart, each pair has four transverse critical possibilities, and the critical value is `c1 epsilon1+c2 epsilon2`. Independence forces both products zero, leaving `3*3=9` critical rays. All transverse Hessians remain nonsingular. Taking equal `c1,c2` instead gives ten rays over every binary field.

## 7. Executed evidence and API boundaries

The audit functions are:

```python
acquire_contact_hyperplane(T, b, h)
residue_critical_rays(R, P)
lift_transverse_center(R, P, residue_root, B)
acquire_lifted_rays(R, P)
uniform_field_sum(h, pair_count)
uniform_chain_sum(h, e, pair_count)
```

Here `T` is the field alternating third-form coefficient map and `P` is a full homogeneous ordinary ring cubic in packed coefficient form. The first four APIs acquire and audit geometry; they are not the raw ANF compiler. The last two evaluate only the explicit uniform family `K_r`.

`contact_hyperplane_checks.py` and `contact_hyperplane_results.json` retain these executed checks:

- Three instances have random field-linear disguises and arbitrary higher nilpotent coefficients. They recover the expected hyperplane exactly, acquire 10, 9, and 1 critical rays respectively, and verify every full-ring transverse derivative after lifting. The one-ray instance has rank seven over F16 at ring length three. Their critical values are generally nonzero at higher nilpotent orders; no false full-value-zero filter is used.
- Twelve kernel-dimension cases check `J_r` across extension degrees one through six, including the exact transition from zero to `2r` when `3|d`. A thirteenth, variable-rank instance has `b=11,d=4,e=2` and one acquired ray.
- Eleven complete truth-table checks cover **4,342,784 assignments**. They include the all-field Gaussian terminal identity, the uniform ring recurrence, and the one-ray family. Over `F4[t]/t^2`, rank five has 20 independent bits: the uniform family has signed sum `31744`, while the one-ray family has signed sum `4096`, both verified on all `1,048,576` assignments.
- An inconsistent affine chart system is verified to have zero rational critical rays and signed sum `1024` over `F4[t]/t^2`, again by all 20-bit assignments. The singular hyperplane-restriction example is explicitly rejected.
- The rank-seven nilpotent example above has no global contact-factor lift, as verified by an inconsistent first-order linear system, but all 36 residue rays lift correctly. Four computed critical values are nonzero in its first nilpotent layer.

All tables are exact correctness evidence, not practical performance comparisons. Established ingredients include exterior algebra, symplectic elimination, finite-field linearized equations, Hensel lifting, local stationary phase, and binary quadratic sums. The claims here are the explicit acquired conditions, their closure under the stated ring deformations and weights, the measured-kernel complexity, and the complete formulas and checks above. No generic cubic, generic nodal hypersurface, or unrestricted computational representation is claimed to meet the conditions.
