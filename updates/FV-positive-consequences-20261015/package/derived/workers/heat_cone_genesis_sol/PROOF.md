# An exposed quartic ray beyond constant linear corrected heat

Research date: 15 October 2026. Repository pin:
`a6190a1083f688a7e4bf64adbc5244ef150ff2c4`.

This note gives an exact limitation of a certificate operation. It does not
give a counterexample to quasiconvexity. The polyconvexity and quasiconvexity
of the displayed quartic remain **UNKNOWN**. Historical priority and external
correctness review remain **UNKNOWN**.

The principal verifier, `verify_heat_separation.py`, uses SymPy only and
reconstructs every mathematical constant from its own source. The companion
`verify_null_corrections.py` uses Python's standard library only. Neither
verifier reads an optimizer result or trusts a saved certificate as an input.

## 1. The exact result

For a real planar matrix A with row-major entries `(a,b,c,d)`, put

\[
u=a^2+c^2,\quad v=b^2+d^2,\quad w=ab+cd,\quad q=ad-bc,
\]

and define

\[
\boxed{F=u^2+v^2+\frac{166}{3}uv-\frac{460}{9}w^2
                  -\frac{52}{9}q(u-v).}                 \tag{1}
\]

Let R be the cone of all left-SO(2)-invariant rank-one-convex homogeneous
quartics, with all nine coefficients unrestricted. Let H be the subset of
that space admitting a pointwise corrected-heat certificate for some fixed
real constant-coefficient strongly parabolic operator

\[
Lv=\sum_{i,j=1}^2 C^{ij}\partial_i\partial_jv,
\qquad C^{ij}\in\mathbb R^{2\times2},\quad C^{ij}=C^{ji},
\]

where the symmetric part of its output principal symbol satisfies

\[
\operatorname{sym}\!\left(\sum_{i,j}n_i n_jC^{ij}\right)
\succeq \kappa |n|^2 I_2\quad\text{for some }\kappa>0.    \tag{2}
\]

The permitted correction is **any** closed two-form on matrix space with
homogeneous quadratic coefficients. Pointwise positivity is required on
every compatible second jet. No sum-of-squares restriction is imposed.

Theorem.

1. F lies on an exposed extreme ray of R, and F(A) is at least
   `|A|^4/2` pointwise. The normalized ray is `(9/2432)F` for the section
   `Lambda=16(p1+p2)+8p3+4p4=1`.
2. F is not in H. In fact `F-gamma q^2` is not in H for any `gamma>=0`.
   Thus a determinant-square supplement does not repair this example.
3. In any finite positive decomposition of F into left-invariant members
   of H and arbitrary homogeneous quartic polyconvex addends, every heat
   summand is zero. Such a decomposition exists if and only if F itself is
   polyconvex.

The third assertion does not decide that final polyconvexity question.
There is no claim here about coefficient closures of positive constructions
with unbounded output diffusion coefficients, time-dependent or nonlinear
flows, nonlocal certificates, or signed decompositions justified by a
different inequality.

## 2. Rank-one convexity by a small rational factor

Left rotations preserve u,v,w,q. Consequently it suffices to test rank-one
directions `e1 tensor n`: rotate the output vector of any rank-one matrix
to e1 and use the chain rule.

For `n=(1,k)` let M(k) be the symmetric matrix satisfying

\[
D^2F(A)[e_1\otimes(1,k),e_1\otimes(1,k)]
           =\operatorname{vec}(A)^TM(k)\operatorname{vec}(A).
\]

Write `M=M11+2k M12+k^2 M22`. Define the skew matrix K by its upper
triangle, in pair order `(01,02,03,12,13,23)`, as

\[
(8/9,8/9,0,0,-8/9,488/9).
\]

Then

\[
Q=\begin{pmatrix}M_{11}&M_{12}+K\\M_{12}-K&M_{22}\end{pmatrix}
   =B\operatorname{diag}(8/3,4/3,8/9,4/9)B^T,              \tag{3}
\]

where B has four columns. The first two are supported in positions
`(0,3,5,6)` with entries respectively `(2,-1,2,-1)` and `(1,-9,-1,9)`;
the last two are supported in `(1,2,4,7)` with entries respectively
`(3,2,3,2)` and `(1,1,-1,-1)`. All unlisted entries are zero.

These columns are independent. Identity (3) is an exact rank-four PSD
factor. For `Y=(n1 vec(A),n2 vec(A))`, skewness gives
`Y^T Q Y=D^2F(A)[e1 tensor n,e1 tensor n]`. This includes `n1=0` by the
polynomial identity, rather than by division by n1. Thus F is rank-one
convex.

For a separate pointwise observation, put `r=u-v, t=2w, d=2q`. The Gram
identity is `(u+v)^2=r^2+t^2+d^2`, and

\[
F=(r-13d/9)^2+\frac{14}{9}t^2+\frac{992}{81}d^2.         \tag{4}
\]

Subtracting half the Gram identity leaves a positive definite quadratic
form in `(r,t,d)`, as the verifier checks by exact principal minors. This
proves the stated pointwise lower bound. Pointwise nonnegativity is not
being substituted for an all-background Jensen inequality.

## 3. Four exact acoustic contacts and exposed extremality

Set

\[
P(k)=17k^4-314k^2+17,
\quad A(k)=\begin{pmatrix}
203-17k^2&k(85k^2-1551)\\
2k(944-51k^2)&134
\end{pmatrix}.                                         \tag{5}
\]

P has four distinct real roots: its two roots in `k^2` are distinct and
positive. Direct exact reduction modulo P gives

\[
M(k)\operatorname{vec}(A(k))=0,\qquad
\det M(k)=\frac{1024}{729}P(k)^2.                         \tag{6}
\]

The vector A(k) is nonzero because its last entry is 134. If
`R(k)=e1 tensor (1,k)`, then

\[
\operatorname{cof}A(k):R(k)
\equiv4(8-k^2)\pmod P,                                 \tag{7}
\]

which is nonzero at every root of P.

For a general coefficient vector p in the basis
`(u^2,v^2,uv,w^2,uw,vw,qu,qv,qw)`, let `M_p(k)` be its acoustic matrix.
If its quartic is rank-one convex and vanishes acoustically at all four
contacts (5), nonnegativity implies that the first derivatives with respect
to A and k also vanish. Therefore

\[
M_p(k)A(k)=0,\qquad A(k)^TM_p'(k)A(k)=0                  \tag{8}
\]

at all four roots. Reducing the five polynomials in (8) modulo P gives a
20-by-9 rational linear map. Its exact rank is eight, and its kernel is
precisely the coefficient vector of (1). The verifier reconstructs this
map directly from the nine displayed basis polynomials.

For completeness, sum the four nonnegative acoustic evaluations over the
roots of P. Newton sums evaluate this as a positive multiple of the rational
linear functional

\[
\ell(p)=910741p_1+1453621p_2+324775p_3+321232p_4
                         +244987p_7-432907p_8.           \tag{9}
\]

It is nonnegative on R and vanishes at F. If it vanishes at another member
of R, all four acoustic evaluations vanish, so (8) places that member on
the same one-dimensional ray. This proves exposed extremality, not merely
extremality of one chosen acoustic Gram matrix.

## 4. Why the certificate must annihilate the contact jets

For compatible jets `h=(h0,...,h5)`, write

\[
B_1=\begin{pmatrix}h_0&h_1\\h_3&h_4\end{pmatrix},
\qquad B_2=\begin{pmatrix}h_1&h_2\\h_4&h_5\end{pmatrix}.
\]

The heat density associated with L is

\[
E_{F,L}(A,h)=\sum_{i,j}D^2F(A)[B_i,C^{ij}B_j].           \tag{10}
\]

A certificate is a closed quadratic two-form omega such that
`E_{F,L}(A,h)+omega_A(B1,B2)>=0` for every A,h. For fixed A this is a
quadratic form in h.

At an acoustic contact, use `h=(1,k,k^2,0,0,0)`. The derivative matrices
are `B1=R(k), B2=k R(k)`. Every two-form vanishes on this proportional
pair. The acoustic output matrix is PSD and has e1 in its kernel. Hence
all terms in (10) vanish there, including output-coupled terms. A PSD
quadratic form with zero value at a vector must annihilate that vector.
Thus the six h derivatives of the corrected density vanish at each contact.
These necessary kernel equations are what the exact calculation uses.

This step requires pointwise positivity, but it does not require that the
density admit a global bilinear SOS Gram.

## 5. Averaging every fixed strongly parabolic linear operator

The energy is invariant under all left output rotations and under the two
finite transformations

\[
A\mapsto A\begin{pmatrix}0&1\\1&0\end{pmatrix},\qquad
A\mapsto\begin{pmatrix}1&0\\0&-1\end{pmatrix}
 A\begin{pmatrix}1&0\\0&-1\end{pmatrix}.                 \tag{11}
\]

Transform a proposed certificate together with its operator, then average.
The corrected density remains nonnegative. Pullback and exterior
differentiation commute; the two-form acquires the orientation sign of
the input transformation and remains closed. The associated operator
remains strongly parabolic because its symmetric symbol is averaged from
uniformly positive symbols.

Averaging the output matrices under SO(2) gives `alpha I+beta J`, with
`J=[[0,-1],[1,0]]`. The combined reflection in (11) removes the diagonal
skew-output coefficients and the mixed scalar coefficient. The input swap
makes the two diagonal scalar coefficients equal. Therefore the averaged
operator is

\[
c\Delta+2bJ\partial_{xy},\qquad c>0.                    \tag{12}
\]

Divide the certificate by c and write `beta=b/c`. Its density becomes

\[
D^2F[B_1,B_1]+D^2F[B_2,B_2]
 +\beta\{D^2F[B_1,JB_2]+D^2F[B_2,JB_1]\}
 +\omega_A(B_1,B_2).                                    \tag{13}
\]

The averaged density is invariant under the compatible jet transformations
induced by (11). No assumption that the original operator was componentwise,
isotropic, symmetric in its output matrices, or chosen before F is needed.

## 6. Every closed correction is included in the calculation

A closed two-form with quadratic coefficients has the polynomial primitive
`alpha=(1/4)i_E omega`, by the Euler-field homotopy identity. Cubic one-forms
on R4 have 80 coefficient coordinates. Their exterior derivatives span a
45-dimensional space of closed quadratic two-forms.

The pullback map to compatible jets is injective: its six wedge minors have
distinct identifying monomials, for example `h0 h2`, `h3 h5`, `h0 h4`,
`h0 h5`, `h2 h3`, and `h1 h5`. Thus no form disappears merely because
the second jets are compatible.

Let the common infinitesimal output rotation act on A and h. Applying it to
the 80 generating pullback densities has exact rank 30; the pullback map
itself has rank 45. Hence the invariant closed-correction space has dimension
15. The following cubic primitives give an independent basis after exterior
differentiation:

\[
\begin{array}{llll}
u\,dv,&u\,dw,&u\,dq,&u\theta_u,\\
u\theta_v,&u\theta_c,&u\zeta,&v\,dw,\\
v\,dq,&v\theta_u,&v\theta_v,&v\theta_c,\\
v\zeta,&w\theta_c,&w\zeta.
\end{array}                                             \tag{14}
\]

Here
`theta_u=a dc-c da`, `theta_v=b dd-d db`,
`theta_c=a dd+b dc-c db-d da`, and
`zeta=a db+c dd-b da-d dc`. All dimensions and independence assertions
are reconstructed exactly in the standalone heat verifier.

Impose the contact-kernel equations of Section 4 and the two finite jet
symmetries of Section 5 on (13), with all 15 coefficients in (14) and beta
free. The resulting rational linear system has rank 15 in 16 unknowns.
Its complete solution forces beta to zero. In the gauge (14), every
remaining form is `omega=d alpha_t`, where

\[
\begin{split}
\alpha_t={}&\left(-\frac{93}{59}t-\frac{5456}{177}\right)(u-v)\,dw\\
&+\left(\frac{83}{177}t-\frac{9920}{531}\right)
                                      (u\theta_u-v\theta_v)\\
&+\left(\frac{21328}{531}-\frac{382}{177}t\right)
                                      (u\theta_v-v\theta_u)\\
&+t(u+v)\zeta.
\end{split}                                             \tag{15}
\]

This is an exact solved linear system, not a numerical face restriction.
The verifier forms the full density, differentiates it in all six h
variables, substitutes (5), and reduces every polynomial modulo P. It also
forms the complete polynomial symmetry equations. Substitution of (15)
verifies every equation, and the exact rank excludes other solutions.

## 7. Two rational jets give an exact contradiction

Evaluate the corrected density with (15) at

\[
\begin{array}{c|c}
A&h\\ \hline
(1,0,0,2)&(0,1,0,0,0,-1)\\
(1,-1,0,2)&(0,0,1,-1,0,0).
\end{array}
\]

The values are respectively

\[
V_1(t)=\frac{274}{59}t-\frac{192260}{531},\qquad
V_2(t)=\frac{25120}{177}-\frac{1172}{177}t.               \tag{16}
\]

Positivity would require simultaneously

\[
t\ge\frac{96130}{1233}>\frac{6280}{293}\ge t.
\]

Equivalently, the positive combination

\[
586V_1(t)+411V_2(t)=-\frac{81691400}{531}<0              \tag{17}
\]

is independent of t. This proves that no corrected density (13) is
pointwise positive. Averaging proves the exclusion for every operator (2).
The test pairs are legal pointwise compatible jets; they are **not** a
periodic gradient law or a negative quasiconvexity test.

## 8. The determinant-square supplement and arbitrary polyconvex pieces

First note that any corrected certificate for an operator (2) implies
rank-one convexity. For a fixed A,n, let S be the symmetric 2-by-2 acoustic
output matrix and C the output principal symbol of L. On pure jets the
closed correction vanishes. Positivity gives `C^T S+SC>=0`. Condition (2)
makes C positive stable, and

\[
S=\int_0^\infty e^{-C^Tt}(C^TS+SC)e^{-Ct}\,dt\succeq0. \tag{18}
\]

This elementary Lyapunov identity proves the required implication even for
nonsymmetric output diffusion matrices.

At any contact (5),

\[
D^2(F-\gamma q^2)[R,R]
       =-2\gamma(\operatorname{cof}A:R)^2.
\]

By (7), this is strictly negative for gamma>0. Thus the subtraction cannot
have any strongly parabolic corrected-heat certificate; gamma=0 is already
excluded by (17).

Now suppose F is a finite positive sum of invariant heat-certified quartics
and homogeneous quartic polyconvex addends. Collect all polyconvex addends
into one polynomial P. It is polyconvex by closure under positive sums, and
it is left-invariant because F and every heat summand are left-invariant.
Heat certificates imply ROC by (18), and polyconvexity implies ROC.
Applying the exposed functional (9) to the invariant heat summands and
the collected P forces each of those polynomials onto the ray of F. A
nonzero heat summand would therefore supply a certificate for a positive
multiple of F, contrary to (17). All heat summands vanish, leaving P=F.
This proves the localized mixed-cone statement. No assertion is made that
the original noninvariant polyconvex addends are individually proportional
to F. Noninvariant heat summands are outside this decomposition theorem:
averaging their energy and operator jointly need not factor into a
certificate for one averaged energy and one averaged operator. No polynomial
lift or SOS-support restriction is placed on the collected polyconvex P.

## 9. Completeness of polynomial null corrections at this order

There is a second classification that does not assume rotational invariance
or closed-form representation in advance.

Let W consist of all real polynomial densities P(A,h) homogeneous of degree
two in A and degree two in h. Its dimension is `10*21=210`. Call P null
if its integral is zero for every smooth compactly supported perturbation
of every affine planar map. Then

\[
\boxed{P\text{ is null }\Longleftrightarrow
 P(A,h)=\omega_A(B_1,B_2),\quad d\omega=0,}
\]

with omega a unique homogeneous-quadratic two-form. The null space has
dimension 45, and its left-SO(2)-invariant part has dimension 15.

Here is the full finite proof interface. For each component of the potential,
form the Euler operator

\[
\mathcal E_c(P)=\sum_{1\le|I|\le2}(-D)^I
                                  \frac{\partial P}{\partial u^c_I}.
\]

Formal jets through order four are algebraically independent. First variation
and the fundamental lemma show that nullity implies this polynomial is zero.
Conversely, zero Euler operators make the integral constant along
`u_s=Bx+s phi`; at s=0 its Hessian is zero and the integral is zero.
Therefore nullity is exactly the kernel of this explicit linear Euler map.

The standalone stdlib checker constructs its 696-by-210 integer matrix E,
the 210-by-80 integer cubic-one-form pullback map N, and checks **E N=0
over the integers**. It supplies nonzero minors modulo the prime 1009 of
sizes 165 and 45 respectively. A nonzero modular determinant is a rigorous
nonzero integer determinant. Hence `rank E>=165`, `rank N>=45`, and
`E N=0` forces exact equality and `ker E=im N` over the reals. This proves
the classification, rather than treating a numerical rank as a theorem.

For the invariant statement the checker additionally constructs the output
rotation map, 72 explicit invariant densities, and 15 explicit invariant
null densities. Exact nonzero modular minors and exact annihilation give
invariant density dimension 72 and invariant null dimension 15.

Thus replacing a closed quadratic correction by an arbitrary polynomial
divergence whose final density is still in W does not enlarge this method.
This says nothing about higher jets, nonpolynomial corrections, different
homogeneities, nonlinear evolution, or direct global gradient inequalities.

## 10. What has actually been resolved

The established strict inclusion is the pointwise corrected-linear-heat
certificate family, even with a determinant-square supplement, inside the
full invariant ROC cone. The exposed-ray calculation further proves that
positive polyconvex addends cannot contribute alongside a heat piece on this
ray. Its remaining mixed-cone question is exact unrestricted polyconvexity
of F, not SOS feasibility and not a search for another heat metric.

No compatible negative field has been acquired. Finite lifted Jensen searches
and forced-polyconvex-support optimization did not find a negative witness;
those numerical failures establish no lower bound. An SOS-support search
with a quadratic support multiplier was infeasible; that does not prove
nonpolyconvexity. The relevant exploratory receipts are retained separately.

This is not a new proof of G quasiconvexity, its anisotropic distortion margin,
or the prior pure-heat obstruction for `q^2+10^-4|A|^4`. Those inputs were
read, and G's copied exact certificate passed all seven verification groups.

## 11. Prior machinery and priority boundary

[Bruno and Pasqualotto, arXiv:2608.06367v1](https://arxiv.org/html/2608.06367v1)
provide the heat/exact-form method and prove ROC=QC for quartics invariant
under both left and right SO(2). Their Appendix A separates a determinant
square from the heat-certified boundary family. Neither that theorem nor
the method is claimed as an invention here.

[Ball, Currie and Olver (1981)](https://www-users.cse.umn.edu/~olver/e_/bco.pdf)
develop the Euler/divergence interface and classify highest-order null
Lagrangians. Our density depends on first and second derivatives together,
so their highest-order-only statement is not invoked by freezing the lower
jets. The explicit Euler-map calculation above supplies that specialization.

[Olver and Sivaloganathan (1988)](https://www-users.cse.umn.edu/~olver/e_/null.pdf)
give a differential-form representation of first-order inhomogeneous null
Lagrangians and discuss higher-order extension. The structural idea is
classical. No historical novelty is asserted for the dimension calculation.

[Fantuzzi et al., arXiv:2604.11124v1](https://arxiv.org/html/2604.11124v1)
distinguish unrestricted polyconvexity from polynomial lifted and SOS-support
certificates. That distinction is why the candidate's failed SOS-support
search remains inconclusive. The exact arithmetic and analytic argument here
are internally checkable, not external review or formal proof-assistant
verification.
