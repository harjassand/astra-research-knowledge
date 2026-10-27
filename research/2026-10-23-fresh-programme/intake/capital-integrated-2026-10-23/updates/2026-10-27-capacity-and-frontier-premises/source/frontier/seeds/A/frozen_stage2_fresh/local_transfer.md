# Complete local transfer at repeated rank-one block zeros

27 October 2026. This is a conditional local theorem for the fixed full
Werner functional. It does not prove its lower-copy premise. No novelty
claim is made.

Write \(H=(\mathbb C^3)^{\otimes m}\), \(L(X)=X-\operatorname{Tr}(X)I_3/2\),
\(q_m(X)=\langle X,L^{\otimes m}X\rangle\), and let \(b_m\) be its
conjugate-linear-first polarization. We use two elementary inherited facts:

\[
 \|L^{\otimes m}\|_{HS\to HS}=1,\qquad
 R_m=\prod_{i=1}^m(I-F_i/2)\succeq\delta I,\quad\delta=2^{-m},
\tag{1}
\]
\[
 b_m(ab^*,cd^*)=\langle a\otimes d,R_m(c\otimes b)\rangle.
\tag{2}
\]

The lower-copy assertion \(W_m\) means \(q_m(Z)\ge0\) for **all complex
rank-at-most-two** \(Z\) on \(H\).

## The local theorem

**Theorem.** Assume \(W_m\). For every nonzero rank-one \(R=uv^*\),
\(C_0=\operatorname{diag}(R,R,0)\) has a neighborhood within the complex
rank-at-most-two variety on which \(q_{m+1}\ge0\). Every zero in a sufficiently
small such neighborhood has a common physical two-plane at the first site:
after one local unitary conjugation its row and column supports at that
site both lie in \(\operatorname{span}(e_0,e_1)\).

Consequently the following are equivalent at each fixed \(m\):

1. \(W_m\).
2. Every nonzero repeated rank-one block zero above is a local minimum of
   \(q_{m+1}\) on rank at most two.
3. The full Hessian at every such zero is positive semidefinite.

The implication 3 to 1 is the already supplied exact lift, and is not a new
induction. The useful addition is 1 to 2, including all degenerate kernel
directions and all orders, with no classification of lower-copy zeros.

### A finite separable decomposition for a binary first site

Let \(a,b\) range over the six ordered orthogonal pairs consisting of the
two eigenvectors of each Pauli matrix, in both orders. Set \(A=ab^*\).
Direct two-by-two algebra gives

\[
 I_4-\tfrac12|\Omega_2\rangle\langle\Omega_2|
 =\tfrac12\sum_{(a,b)}|\operatorname{vec}(ab^*)\rangle
                    \langle\operatorname{vec}(ab^*)|.
\tag{3}
\]

For example the six matrices are \(E_{01},E_{10}\),
\(\frac12\left[\begin{smallmatrix}1&-1\\1&-1\end{smallmatrix}\right]\),
\(\frac12\left[\begin{smallmatrix}1&1\\-1&-1\end{smallmatrix}\right]\),
\(\frac12\left[\begin{smallmatrix}1&i\\i&-1\end{smallmatrix}\right]\), and
\(\frac12\left[\begin{smallmatrix}1&-i\\-i&-1\end{smallmatrix}\right]\).
Thus for a matrix \(B\) on \(\mathbb C^2\otimes H\),

\[
 q_{(2,3,\ldots,3)}(B)
 =\tfrac12\sum_{(a,b)}q_m((a^*\otimes I)B(b\otimes I)).
\tag{4}
\]

Each contraction has rank at most \(\operatorname{rank}B\). Under \(W_m\),
(4) is therefore nonnegative when \(B\) has rank at most two. This uses
separability of the binary factor; merely observing that its quadratic
form is positive semidefinite would not justify this rank-sensitive step.

### A physical-plane slice removes the transverse null directions

Normalize \(u,v\) to norm one; scaling handles every other nonzero \(R\).
Near \(C_0\) choose smooth full-column-rank factors \(C=UV^*\), with

\[
 U_0=(u,0),\quad U_1=(0,u),\quad U_2=0,
 \qquad V_0=(v,0),\quad V_1=(0,v),\quad V_2=0
\tag{5}
\]

at the base. Subscripts are physical-site blocks, each an \(\dim H\)-by-two
matrix. Such factors exist in a rank-two chart because the base has rank
exactly two.

Define the three-by-three Gram matrix
\(G_{ij}=\langle U_i,U_j\rangle_F+\langle V_i,V_j\rangle_F\).
At (5), \(G=\operatorname{diag}(2,2,0)\). Its lowest eigenline is isolated
and varies continuously near the base. Choose a local unitary conjugation
so that its eigenvector is the third coordinate. This leaves \(q\)
unchanged, keeps the factors close to (5), and imposes the exact slice
conditions

\[
 \langle U_i,U_2\rangle_F+\langle V_i,V_2\rangle_F=0,
 \qquad i=0,1.
\tag{6}
\]

This slice is chosen by a physical unitary, rather than by changing the
rank-two constraint.

### Exact splitting and coercivity

Put \(X=U_2\), \(Y=V_2\), \(B_{ij}=U_iV_j^*\) for \(i,j<2\), and
\(A=B_{00}+B_{11}\). The first-site partial-trace identity gives exactly

\[
 q_{m+1}(UV^*)=q_{(2,3,\ldots,3)}(B)+T_P(X,Y)
                       +\tfrac12q_m(XY^*),
\tag{7}
\]
\[
 T_P(X,Y)=\sum_{i=0}^1[q_m(U_iY^*)+q_m(XV_i^*)]
                    -\operatorname{Re}b_m(A,XY^*),
\tag{8}
\]

where \(P=(U_0,U_1,V_0,V_1)\). Both the first and last terms in (7) are
nonnegative under \(W_m\), by (4) and \(\operatorname{rank}(XY^*)\le2\).

At the base (5), writing the columns of \(X,Y\) as \(x_a,y_a\), (2) gives

\[
 T_0(X,Y)=\sum_{a=0}^1
 \langle x_a\otimes v-u\otimes y_a,
 R_m(x_a\otimes v-u\otimes y_a)\rangle.
\tag{9}
\]

Its kernel is exactly \(x_a=\lambda_a u,\ y_a=\lambda_a v\). Conditions
(6) at the base remove that kernel: their left sides are
\(\langle u,x_a\rangle+\langle v,y_a\rangle\).
Hence (1) implies coercivity on the slice. The following explicit estimate
also makes persistence under perturbation precise.

Let \(\varepsilon^2=\sum_{i<2}(\|U_i-U_i^0\|_F^2+
\|V_i-V_i^0\|_F^2)\) and \(w^2=\|X\|_F^2+\|Y\|_F^2\). From (6),

\[
 \sum_a|\langle u,x_a\rangle+\langle v,y_a\rangle|^2
 \le\varepsilon^2 w^2.
\]

The squared norm of the projection of \((X,Y)\) onto the kernel of (9)
is one half of this sum. On its orthogonal complement,
\(\sum_a\|x_a\otimes v-u\otimes y_a\|^2\ge w^2\).
It follows that

\[
 T_0(X,Y)\ge\delta(1-\varepsilon^2/2)w^2.
\tag{10}
\]

Using \(\|L^{\otimes m}\|\le1\),
\(\|EF^*\|_F\le\|E\|_F\|F\|_F\), and Cauchy--Schwarz in the two block
indices, direct subtraction of (8) at \(P\) and at the base gives

\[
 |T_P-T_0|\le[(2\sqrt2+1)\varepsilon+\tfrac54\varepsilon^2]w^2.
\tag{11}
\]

For completeness the two squared terms contribute at most
\((2\sqrt2\varepsilon+\varepsilon^2)w^2\). The change in
\(A=\sum_iU_iV_i^*\) has norm at most
\(2\varepsilon+\varepsilon^2/2\); pairing it with \(XY^*\) adds at most
\((\varepsilon+\varepsilon^2/4)w^2\).

For \(\varepsilon\le\delta/10\), (10)--(11) imply

\[
 \boxed{\quad T_P(X,Y)\ge(\delta/2)(\|X\|_F^2+\|Y\|_F^2).\quad}
\tag{12}
\]

Indeed \(0<\delta\le1\), so the bracket divided by \(\delta\) is at least
\(1-(2\sqrt2+1)/10-1/80-1/200>1/2\).
By continuity of the factor chart and the isolated Gram eigenline, every
rank-two \(C\) sufficiently near \(C_0\) admits the above slice with this
bound. Equations (7) and (12) prove the theorem, including the statement
about nearby zeros. The base's distance from rank one lets us use a
rank-exactly-two chart throughout a sufficiently small neighborhood.

The mechanism is more general than the lower Werner tensor. If a Hermitian
form on \(\operatorname{End}(H)\) is nonnegative on rank at most two, has
strictly positive crossed operator \(R\), and its Hilbert--Schmidt operator
norm is \(M\), the same proof applies to tensoring it with the added
qutrit factor. Replace \(\delta\) by \(\lambda_{\min}(R)\) and choose
\(\varepsilon\) small compared with \(\delta/M\). Thus this is a local
transfer principle for that class of forms. The PPT countermodel in
`global_obligation.md` shows why the principle cannot simply be made
global using those hypotheses.

### Necessity and the exact unresolved global boundary

For any lower-copy rank-two \(Z=av^*+ub^*\), the supplied exact lift is

\[
 C(t)=\begin{pmatrix}uv^*&tZ&0\\0&uv^*&0\\0&0&0\end{pmatrix},
 \qquad q_{m+1}(C(t))=t^2q_m(Z),\quad\operatorname{rank}C(t)\le2.
\tag{13}
\]

The nontrivial rank-two case allows \(u,v\ne0\). Thus positivity in all
these local neighborhoods implies \(W_m\). The local theorem is an exact
transfer of the lower-copy global problem; it does not establish that
problem, and does not control distant arbitrary rank-two matrices at
\(m+1\) copies.

## Consequence for the frozen Hessian's cubic and quartic obligation

Use the frozen factors \(C(t)=(U^0+tX)(V^0+tY)^*\), and write
\(C=C_0+tH+t^2D\), \(D=XY^*\). Its exact polynomial is

\[
 q_{m+1}(C(t))=t^2Q+2t^3\operatorname{Re}b_{m+1}(H,D)
                         +t^4q_{m+1}(D).
\tag{14}
\]

Under \(W_m\), the theorem proves local positivity of this entire curve.
Consequently on **every** full Hessian kernel direction \(Q=0\),

\[
 \boxed{\operatorname{Re}b_{m+1}(H,D)=0,
                   \qquad q_{m+1}(D)\ge0.}
\tag{15}
\]

The cubic must vanish because both signs of small real \(t\) are allowed;
the quartic then has nonnegative sign. This does not assume positivity for
arbitrary same-copy \(D\): it proves it only for the constrained products
whose full quadratic coefficient vanishes. It resolves the specific
all-orders compatibility obligation left by the first-stage handoff,
conditional on exactly the lower-copy target already needed for its
Hessian. It supplies no free induction.

An additional algebraic check is available: under \(W_m\), the restriction
of \(q_m\) to \(\mathcal T_{u,v}\) is PSD, so its zero set is a complex
linear kernel. If \(Z_j=a_jv^*+ub_j^*\) lie in that kernel, every pencil
\(Z_0+tZ_1\) is a rank-two zero. Stationarity at those zeros, applied to
the tangent \((a_0+t a_1)z^*\), and comparison of coefficients of \(t\)
and \(\bar t\), gives \(b_m(Z_0,a_1z^*)=0\); there is an analogous row
identity. These annihilation identities cancel the binary cubic directly.
The slice argument above also handles the third physical coordinate and
the quartic, without relying on this optional pencil calculation.

## Provenance and comparison

The inherited full Hessian and the already known exact-lift obstruction
are in `../frozen_stage1/RESULT.md`; they are preserved without edits.
The public CT source proves local positivity near a different moving
binary spin-flip family and warns that arbitrary entangled repeated block
zeros re-encode the lower-copy target. The public BD/LA094/LA095 lifting
identities concern a restricted transverse family. None is asserted to
prove the present arbitrary-tangent local transfer. The binary separable
factor and physical Gram slice are elementary machinery; historical
novelty of their combination has not been assessed.

The unrestricted target for every finite \(n\) and every complex rank-two
\(C\) remains unchanged and unresolved.
