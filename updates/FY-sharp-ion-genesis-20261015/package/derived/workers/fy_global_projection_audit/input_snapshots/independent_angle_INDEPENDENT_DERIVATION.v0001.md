# Independent reconstruction of the oblique contact projection

15 October 2026. Worker `fy_contact_independent_audit`.

This derivation was completed from the parent-supplied equations and the
inherited N873 / GENERAL_FLAT_COMPLETION proof before reading the new
constructor's proof. After deriving the boundary obstruction, I requested
only the constructor's final statement and path. Its statement agrees with
the result below. A separate comparison records the subsequent proof read.
External correctness, formal verification, and historical priority remain
UNKNOWN.

The protected input checkout is
`/Users/harjas/Documents/ChatGPT/ultra/work/astra-sharp-ion-20261015`, at
`b32943eeb62d0d79929a9e572a344219a785ebf9`. This worker writes only its own
directory in the research tree. No source, W, or Git files are modified.

## Exact theorem reconstructed

Let V be the real nine-dimensional space of homogeneous quartics on real
2 by 2 matrices invariant under left SO(2). Write

\[
A=\begin{pmatrix}a&b\\c&d\end{pmatrix},\quad
u=a^2+c^2,\ v=b^2+d^2,\ w=ab+cd,\ j=ad-bc,
\]
\[
H=((a-d)^2+(b+c)^2)^2.
\]

Fix any finite real t != 0, and put

\[
n=1+t^2,\quad R=\binom t1\otimes e_1,\quad
L=tw-j+v,\quad B=v(j-2L/n).
\]

If F is rank-one convex and D2F(I)[R,R]=0, then uniquely

\[
F=\alpha H+kL^2+\ell B+mv^2. \tag{1}
\]

For every real k, ell, m, the following are equivalent:

1. Some finite real alpha makes (1) globally rank-one convex.
2. Some finite real alpha makes (1) quasiconvex at every affine background.
3. Either k=ell=0 and m>=0, or

\[
2m>|\ell|,\qquad
\Delta:=k n^2(2m-\ell)(2m+\ell)
-\ell^2[t^2(2m+\ell)+3(2m-\ell)]>0. \tag{2}
\]

Condition (2) automatically implies k>0. The quasiconvexity contract is
every bounded planar Lipschitz domain, every real affine background, and
every vector perturbation in W0^(1,4), with the periodic analogue. These
are existential projections in alpha. No least coefficient, fixed-alpha
ROC/QC equality, sharp Beurling bound, or full unprojected cone equality
is established by this theorem.

## Contact span without a new proof premise

Use the invariant basis

\[
(u^2,v^2,uv,w^2,uw,vw,uj,vj,wj).
\]

For an ROC quartic, the acoustic polynomial
P_F(A,eta,xi)=D2F(A)[eta tensor xi,eta tensor xi]/2 is nonnegative. At a
zero, its derivatives in the four background entries and the four vector
coordinates vanish. The resulting homogeneous linear system has rank five
for every t!=0. In the exact reconstruction, rows
(P,P_a,P_b,P_c,P_q) and coefficient columns (f0,f2,f3,f4,f5) have determinant

\[
-24t(1+t^2)^3(t^2+3),
\]

which never vanishes in the stated domain. The four coefficient vectors
for H,L2,B,v2 all annihilate the full stationarity system. They are
independent: on rows (f0,f2,f7,f1), their determinant is (n+2)/n>0.
Consequently they span exactly the solution space. This uses ROC and the
contact, not the contact equality alone.

## The quadratic support is necessary, with forced slope

Set G=kL2+ell B+mv2 and q(X)=D2G(I)[X,X]/2. For an arbitrary increment
X=(a,b;c,d), let

\[
x=-a+t(b+c)+d.
\]

Direct differentiation gives

\[
q(X)-3\ell\det X
=kx^2+\frac{2\ell}{n}(tb-3d)x
 +(2m-\ell)b^2+3(2m+\ell)d^2=:Q(X). \tag{3}
\]

The coordinate map X -> (x,b,d) has kernel span{R}. Thus Q annihilates R
in its polar form. Rank-one nonnegativity of q forces Q>=0 without needing
a separate quadratic polyconvexity theorem: if Q(X)<0 and the determinant
polar pairing of X with R is nonzero, there is a real s with det(X+sR)=0,
and Q(X+sR)=Q(X)<0. The directions with nonzero pairing are dense, so the
same contradiction applies by continuity to any negative direction.

Moreover, if q-lambda det is any PSD support, its value at R is zero and
therefore its polar pairing with R vanishes. Equation (3) forces
lambda=3ell, since the determinant pairing with R is not identically zero.
There is no hidden support-finding input in this contact stratum.

In coordinates (x,b,d), the symmetric support matrix is

\[
C=\begin{pmatrix}
k&\ell t/n&-3\ell/n\\
\ell t/n&2m-\ell&0\\
-3\ell/n&0&3(2m+\ell)
\end{pmatrix},\qquad \det C=3\Delta/n^2. \tag{4}
\]

When ell!=0 and t!=0, positivity forces
A:=2m-ell>0 and C0:=2m+ell>0: a zero diagonal with a nonzero off-diagonal
entry is impossible for a PSD matrix. Schur complementation then gives

\[
k\ge\frac{\ell^2}{n^2}\left(\frac{t^2}{A}+\frac3{C0}\right). \tag{5}
\]

Strict inequality is exactly (2). Equality is treated next. For ell=0,
positivity gives simply k>=0 and m>=0, with its singular cases treated
separately below.

## Singular ell != 0 boundary: a second rank-one contact

Assume equality in (5). Here m>0. Divide G by m, which preserves the
existence question, and set r=ell/m and y=t2. Then -2<r<2 and r!=0, and
the normalized coefficient k/m is forced by (5). Put

\[
S=2-r+t^2(2+r),\qquad
Z=\binom{-t(2+r)}{2-r}\otimes(S,2rt).
\]

This is a nonzero rank-one matrix. Direct substitution in (4) shows Z is
in the support kernel. It is independent of R: its determinant polar
pairing with R is exactly t Z_d-Z_b=8r t2, which is nonzero.
Thus P_G(I,Z)=0.

Every finite-alpha ROC completion would have zero first background
derivative of its acoustic polynomial at (I,Z). The H contribution is
zero because D3H(I)=0. Define

\[
U=(r+2)^2y+(r-2)^2(2r+1),
\]
\[
V=(r+2)^3y^2+2(r-2)(r+2)(3r-4)y-3(r-2)^3.
\]

Exact differentiation of the normalized G gives

\[
\nabla_A P_G(I,Z)
=\frac{-4r^3t^3}{(r-2)n}(-4tU,V,V,4tU). \tag{6}
\]

The prefactor is nonzero. The polynomial identity

\[
(r+2)V
=U[(r+2)^2y-2r^3+13r^2-24r+12]
 +4r^2(r-4)(r-2)^3 \tag{7}
\]

prevents U and V from both vanishing for -2<r<2, r!=0. Hence (6) is
nonzero. Choosing a background displacement opposite this derivative
produces a negative acoustic value for sufficiently small displacement,
for every fixed finite alpha. This excludes the equality boundary by an
actual ROC obstruction, not a failed sufficient compiler check.

## All ell = 0 cases

Weak positivity gives k,m>=0. If k=0, G=mv2 is ordinarily convex, so any
alpha>=0 works. If k,m>0, (4) is strictly positive on (x,b,d), and the
sufficiency argument below applies.

The only remaining possibility is k>0,m=0. Set

\[
Z_0=\binom1{-t}\otimes e_2
=\begin{pmatrix}0&1\\0&-t\end{pmatrix}.
\]

Then x(Z0)=0, L(Z0)=n, and P_G(I,Z0)=0 for G=kL2. Exact differentiation
gives

\[
\nabla_A P_G(I,Z_0)=2kn(-1,t,t,1)\ne0. \tag{8}
\]

Again D3H(I)=0, so no finite alpha can repair this local acoustic sign
change. This completes every weak PSD boundary case.

## Strict-support sufficiency and finite coefficient

Under (2), Q is PSD of rank three with kernel exactly span{R}.
The contact-span stationarity identities give

\[
D^3G(I)[R,R,E]=0\quad\hbox{for every }E.
\]

Thus the exact two-kernel-vector cubic-flatness assumption of the inherited
GENERAL_FLAT_COMPLETION theorem holds. Its proof is applicable with the
forced lambda=3ell. Choose any positive lower bound kappa for Q on the
Euclidean orthogonal complement of its kernel and any positive four-linear
tensor bound M for G. Its conclusion supplies the finite coefficient

\[
\alpha_*=401296 M^2/\kappa+(9391/4)M.
\]

Every alpha>=alpha_* is QC with the stated all-background and periodic
contracts. A further reserve nu H gives Jensen margin
(4nu/1875) integral |Dphi|4. For rational t,k,ell,m, the matrix of Q on the
original four increment entries is rational and rank three, so
kappa=e3/e2 is an exact valid lower bound, and M can be the sum of absolute
expanded polynomial coefficients. These fixed-dimensional rational
operations furnish an explicit finite certificate. No claim of the least
alpha follows. Necessity QC -> ROC is the usual rank-one test for smooth
finite polynomial integrands.

## Why t = 0 is not excluded

The strict generic theorem requires t!=0. Both steps that exclude the
ell!=0 boundary fail at t=0: the determinant pencil no longer creates an
independent second rank-one contact, and (6) has the zero factor t3.

For example, after a right SO(2) column swap the inherited sharp
J_{-5/2} has G=j2-(5/2)vj+(35/24)v2. In the t=0 coordinates this is
k=1, ell=-1/6, m=1/8. It has Delta=0. Its known QC status comes from the
separate inherited heat theorem, not this derivation. The identity and
boundary placement are checked independently in the exact verifier.
Nothing here contradicts that example or makes general cubic flatness
necessary in the full invariant space.

## Coverage and projection quantifiers

At I, any nonzero rank-one R=eta tensor xi can be transformed by simultaneous
SO(2) conjugation so xi points along e1. If the transformed eta is parallel
to e1, the contact is the inherited e11 stratum. Otherwise rescale R so its
second component is one, giving (t,1) tensor e1. Its trace is t. The t=0
case is the inherited trace-free stratum; t!=0 is exactly the present
generic case. The normalization preserves H, left-SO(2) invariance,
compatibility, ROC, and QC.

This covers all conformal-background contact angles when combined with
the two inherited strata. To glue a theorem for the full eight-dimensional
H projection, one must also handle the case of no conformal-background
rank-one contact (strict acoustic positivity at I), and retain the exact
existential completion statements of the inherited t=0 and e11 results.
The present contact theorem alone is not the gluing proof. Even a valid
full projected-cone equality does not decide QC for an arbitrary fixed
alpha representative, and cannot settle the positive sharp fixed-alpha
J_r problem.
