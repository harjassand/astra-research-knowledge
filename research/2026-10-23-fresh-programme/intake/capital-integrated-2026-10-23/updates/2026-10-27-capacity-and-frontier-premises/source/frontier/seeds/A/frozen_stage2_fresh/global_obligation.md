# Global discriminant and two opposition results

The full all-copy target remains open. This note records what the new
local transfer does not settle. `local_transfer.md` fixes all notation.

## Exact global remaining inequality

For arbitrary first-site factor blocks \(U_0,U_1,X\), \(V_0,V_1,Y\), put
\(U(t)=(U_0,U_1,tX)^T\), \(V(t)=(V_0,V_1,tY)^T\). Every resulting matrix
has rank at most two. The exact splitting is

\[
 q_{m+1}(U(t)V(t)^*)=a+t^2T+\tfrac12t^4d,
\quad a=q_{(2,3,\ldots,3)}(B),\quad d=q_m(XY^*).
\tag{1}
\]

Assuming the complete lower-copy target \(W_m\), both \(a,d\ge0\). Therefore
positivity of (1) for every real \(t\) is equivalent to

\[
 \boxed{\quad T\ge-\sqrt{2ad}.\quad}
\tag{2}
\]

If \(d>0,T<0\), minimize the polynomial in \(z=t^2\) at \(z=-T/d\).
The minimum is \(a-T^2/(2d)\). The cases \(d=0\) or \(T\ge0\) give the
same criterion by inspection. Thus (2), for all the arbitrary complex
two-column blocks, is equivalent to the entire next-copy target under
\(W_m\). It is not proved here. The local theorem proves \(T\ge0\) only in
its specified Gram slice near repeated block zeros.

## Exact failure of global nonnegativity of T, even in a Gram slice

At \(m=1\), use the rational matrices

\[
 U_0=\begin{pmatrix}0&-1\\-1&0\\-1&1\end{pmatrix},\quad
 U_1=\begin{pmatrix}0&0\\1&0\\-1&1\end{pmatrix},\quad
 V_0=\begin{pmatrix}1&0\\1&0\\-1&0\end{pmatrix},\quad
 V_1=\begin{pmatrix}0&0\\-1&0\\1&-1\end{pmatrix},
\]
\[
 X=\frac1{41}\begin{pmatrix}41&122\\-35&-246\\-49&-115\end{pmatrix},\quad
 Y=\frac1{41}\begin{pmatrix}83&205\\35&41\\-35&-171\end{pmatrix}.
\tag{3}
\]

They satisfy the two exact Gram slice equations
\(\langle U_i,X\rangle_F+\langle V_i,Y\rangle_F=0\). Direct rational
evaluation using \(q_1(Z)=\|Z\|_F^2-|\operatorname{Tr}Z|^2/2\) gives

\[
 a=67/4,\quad T=-147605/3362<0,\quad d=6714658676/2825761>0.
\tag{4}
\]

Replacing \(X,Y\) by \(X/100,Y/100\) keeps the slice and makes the third
Gram eigenvalue strictly smaller than the two binary eigenvalues. Thus
even the lowest-Gram-line choice does not make \(T\) globally nonnegative.
This is not a negative \(q_2\) witness: (2) is respected. It decisively
blocks extending the local coercivity claim to all gauged factors.

A further attempted simplification, that the sliced transverse form has
at most one negative complex direction, is also false. The function
`negative_plane()` in `exact_opposition.py` gives integer two-column
binary blocks and a rational two-dimensional subspace satisfying both
Gram constraints. The restriction of \(T\) there is exactly
\(\left[\begin{smallmatrix}-138093&91\\91&-6465\end{smallmatrix}\right]\),
with positive determinant \(892762964\), so it is negative definite.
This is an auxiliary obstruction, not a negative value of the full form.

## A countermodel to a black-box positivity/co-positivity induction

One might hope to prove (2) from lower-copy rank-two positivity and the
strictly positive crossed operator alone. This is impossible for arbitrary
forms with those properties. The following exact construction reconstructs
a familiar PPT activation mechanism; it is not a result about the specific
tensor powers of \(L\).

Let each of systems 1 and 2 be a pair of qutrits. Across pair \(i\), let
\(F_i\) be swap, \(A_i=(I-F_i)/2\), \(S_i=(I+F_i)/2\), and
\(P_i=|\Omega_3\rangle\langle\Omega_3|/3\). Define the state on local
dimension nine by

\[
 \sigma=\frac1{15}A_1\otimes P_2
            +\frac1{60}S_1\otimes(I-P_2).
\tag{5}
\]

Its trace is \(3/15+48/60=1\), and its positivity is explicit. Partial
transpose on Bob gives the other explicitly positive form

\[
 W=\sigma^\Gamma=\frac1{15}P_1\otimes A_2
                  +\frac1{60}(I-P_1)\otimes S_2\succeq0.
\tag{6}
\]

Both have operator norm \(1/15\). Let \(\varepsilon=1/450\), and use the
quadratic form \(r(Z)=\langle\operatorname{vec}Z,(W+\varepsilon I)
\operatorname{vec}Z\rangle\). It is strictly positive on *every* nonzero
matrix, and its crossed operator is \(\sigma+\varepsilon I\succ0\).

Nevertheless, with an additional qutrit pair labelled 0, the rank-two
vector

\[
 \psi=\left(\sum_{i=0}^2|ii\rangle_{A_0A_1}\right)
       \left(\sum_{j=0}^2|jj\rangle_{B_0B_1}\right)
       (|01\rangle-|10\rangle)_{A_2B_2}
\tag{7}
\]

has squared norm 18 and satisfies, with \(K_3=I-|\Omega_3\rangle
\langle\Omega_3|/2\),

\[
 \langle\psi,K_3\otimes W\,\psi\rangle=-1/15,\qquad
 \langle\psi,K_3\otimes I\,\psi\rangle=15,
\]
\[
 \boxed{\ \langle\psi,K_3\otimes(W+I/450)\,\psi\rangle=-1/30<0.\ }
\tag{8}
\]

The tensor order in (7)--(8) groups pairs \((A_i,B_i)\) for the operator
and groups all Alice and all Bob coordinates for Schmidt rank. Formula
(7) is a sum of two product vectors across that latter split, and its two
left and two right factors are independent. Its Schmidt rank is exactly
two. `exact_opposition.py` contracts its 18 nonzero integer coordinates
using `Fraction`; it also checks (6) entry by entry.

Even the numerical bounds of the Werner black-box ingredients can be
matched. Embed both nine-dimensional local spaces into
\(H_5=(\mathbb C^3)^{\otimes5}\), extend \(W\) and \(\sigma\) by zero, and
set \(\widetilde W=(450/31)(W_{\mathrm{emb}}+I/450)\). Then
\(\|\widetilde W\|=1\), \(\widetilde W\succeq0\), and
\(\widetilde W^\Gamma\succeq I/31\succeq2^{-5}I\). Its corresponding
rank-one crossed lower bound is at least the Werner bound. The embedded
rank-two vector (7) still has expectation \(-15/31\) after tensoring
\(K_3\). This form is **not** \(L^{\otimes5}\); that missing tensor
structure is exactly why it is an opposition model rather than a Werner
counterexample.

The source mechanism is prior: Vollbrecht and Wolf,
[quant-ph/0201103v2](https://arxiv.org/pdf/quant-ph/0201103), particularly
the projectors in equations (3)--(5), the point \(\tau^{(5)}\), and the
local projection protocol. The explicit rational contraction above was
reconstructed here. No discovery or historical novelty is claimed for PPT
activation.

## Live unresolved obligation

The local slice closes the first-stage cubic/quartic kernel issue
conditionally on \(W_m\). The remaining full problem is a certificate for
(2) using additional features of the actual tensor \(L^{\otimes m}\), or
an actual complex rank-two violation of it. The co-positive crossed norm,
lower-copy rank-two positivity, and a globally nonnegative transverse
coefficient are insufficient as a generic induction strategy. Neither
opposition result is a negative witness for the original \(q_n\).

`discriminant_probe.py` implements the exact scale elimination in (1).
It optimizes arbitrary complex \(N\)-by-two blocks, normalizing the
binary and transverse groups by their irrelevant common scales. Two
local descents for \(m=2\) approached \(T/\sqrt{2ad}=-1\), from above,
to floating point accuracy. Direct three-copy values at the optimizing
third-row scale were approximately \(5.25\times10^{-15}\) and
\(5.96\times10^{-14}\). These are local search observations with no
certified global optimum and no certified sign at rounding scale. Their
purpose was an unrestricted opposition test of the global discriminant,
not support-restricted evidence for an all-copy assertion.
