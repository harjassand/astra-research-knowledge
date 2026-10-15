# Exact finite lift for all nine invariant ROC coefficients

This is a coefficient-level corollary of established two-by-n biquadratic
SOS / univariate matrix positivity theory. It is not a claim to have proved
quasiconvexity of the full cone.

Write `A=[[a,b],[c,d]]`, `u=a^2+c^2`, `v=b^2+d^2`, `w=ab+cd`, `j=ad-bc`.
The complete invariant basis is

\[
 F=p_0u^2+p_1v^2+p_2uv+p_3w^2+p_4uw+p_5vw
                          +p_6ju+p_7jv+p_8jw.           \tag{1}
\]

The relation `uv=w^2+j^2` eliminates one of the ten quadratic invariant
monomials. No coefficient vanishing, orientation equality or right rotation
symmetry is assumed in (1).

For `x=(a,b,c,d)^T`, define three symmetric 4 by 4 matrices:

\[
 M_{11}=\begin{pmatrix}
12p_0&3p_4&0&3p_6\\
3p_4&2p_2+2p_3&-p_6&p_8\\
0&-p_6&4p_0&p_4\\
3p_6&p_8&p_4&2p_2
\end{pmatrix},                                          \tag{2}
\]

\[
 M_{12}=\begin{pmatrix}
3p_4&2p_2+2p_3&-p_6&p_8\\
2p_2+2p_3&3p_5&-p_8&p_7\\
-p_6&-p_8&p_4&p_3\\
p_8&p_7&p_3&p_5
\end{pmatrix},                                          \tag{3}
\]

\[
 M_{22}=\begin{pmatrix}
2p_2+2p_3&3p_5&-p_8&p_7\\
3p_5&12p_1&-3p_7&0\\
-p_8&-3p_7&2p_2&p_5\\
p_7&0&p_5&4p_1
\end{pmatrix}.                                          \tag{4}
\]

**Theorem.** F is rank-one convex exactly when a real skew-symmetric 4 by 4
matrix K exists such that

\[
 \boxed{\begin{pmatrix}
 M_{11}&M_{12}+K\\
 M_{12}-K&M_{22}
 \end{pmatrix}\succeq0.}                               \tag{5}
\]

There are six free entries in K. This is an exact semidefinite lift, including
all boundary degeneracies.

**Proof.** For a C2 polynomial, ROC is equivalent to nonnegative second
derivative on every rank-one direction. Left SO(2) invariance lets the output
factor of a rank-one matrix be rotated to `e1`; its length is harmless.
It is therefore necessary and sufficient that

\[
 D^2F(A)[e_1\otimes(s,t),e_1\otimes(s,t)]
 =x^T(s^2M_{11}+2stM_{12}+t^2M_{22})x\ge0              \tag{6}
\]

for every x,s,t. Direct differentiation gives (2)-(4).

By [Calderón (1973)](https://doi.org/10.1016/0024-3795(73)90052-9),
every nonnegative biquadratic form with one variable group of dimension two
is a sum of squares of bilinear forms. Equivalently, apply the established
univariate matrix SOS theorem to
`M11+2t M12+t^2 M22`; the factor polynomials can have degree at most one,
because squared leading coefficients cannot cancel. Homogenizing recovers
(6), including s=0. See also
[Hanselka and Sinn (2017)](https://arxiv.org/abs/1707.08261).

The Gram of these bilinear forms, in order `(s x,t x)`, has fixed diagonal
blocks M11 and M22. Its off-diagonal block B is constrained only by
`(B+B^T)/2=M12`, hence `B=M12+K` with K skew. This proves (5).
Conversely, (5) immediately makes (6) nonnegative. QED.

An approximate feasible K is not an exact ROC certificate. Rational or
specified real-algebraic matrices and exact PSD factors can establish
individual membership. The existence theorem is over the real numbers; it
does not assert rational Gram feasibility for every rational boundary form.

## Determinant extraction and normalization

For every ROC F, the exact finite optimization

\[
 \tau_*(F)=\max\{\tau\ge0:F-\tau j^2\text{ is ROC}\}   \tag{7}
\]

uses (5) with one additional scalar variable. Its feasible set is closed,
nonempty and bounded: evaluating at `A=e22, R=e11` bounds tau above.
Consequently the maximum is attained. The residual is ROC and lies on the
boundary of that cone; otherwise a further small `j^2` subtraction would be
possible. Thus (7) canonically removes one known polyconvex ray before a
heat-plus-PC experiment. It does not remove the whole polyconvex cone and
does not prove that the residual has a heat certificate.

The natural rank-one angular average is

\[
 n(F)=\frac1{2\pi}\int F(e_1\otimes(\cos t,\sin t))\,dt
      =[3(p_0+p_1)+p_2+p_3]/8.                         \tag{8}
\]

ROC implies `n(F)>=0`. If it is zero, the nonnegative rank-one restriction
vanishes identically, so `p0=p1=p4=p5=0` and `p3=-p2`. Reciprocity of quartic
polarization gives `D2F(e11)=M11>=0` and `D2F(e12)=M22>=0`. Their zero diagonal
entries force `p6=p7=p8=0` and `p2>=0`. Hence

\[
 \{F\text{ ROC}:n(F)=0\}=\{\gamma j^2:\gamma\ge0\}.  \tag{9}
\]

In particular, the slice `n(F)=1` is unbounded because adding arbitrary
positive `j^2` leaves n unchanged. Calling it a compact normalized base would
be incorrect. Compactness needs a separate justification after choosing a
coefficient normalization or performing an extraction such as (7).

The matrices in (2)-(4), their acoustic identity, complete invariant dimension,
and the zero-average special case are checked by `verify.py`. Their universal
SOS implication is the cited established theorem, not a finite numerical
experiment.

## The determinant-squared ray cannot be extracted from G

For the exact N850 integrand G, the canonical scalar in (7) is zero.
This is an exact directional boundary statement, and does not say that no
polyconvex component of any kind can be subtracted from G.

Set

\[
 A(t)=\begin{pmatrix}1&3t/2\\-3t/2&1\end{pmatrix},
 \qquad R(t)=\begin{pmatrix}t&1\\0&0\end{pmatrix}.
\]

The perturbation direction R(t) has rank one. Direct differentiation gives

\[
 D^2G(A(t))[R(t),R(t)]=\frac{15}{8}t^4,\qquad
 D^2(j^2)(A(t))[R(t),R(t)]=\frac{25}{2}t^2.
\]

Therefore, for every tau>0,

\[
 D^2(G-\tau j^2)(A(t))[R(t),R(t)]
 =\frac{15}{8}t^4-\frac{25}{2}\tau t^2<0
 \quad\text{if }0<t^2<\frac{20}{3}\tau.
\]

Thus `G-tau(det A)^2` is neither ROC nor QC for every positive tau, and
`tau_*(G)=0`. This is compatible with the inherited N860 positive subtraction
of `kappa|C A|^4`: that convex quartic is a different direction in the cone.

One floating acoustic SDP returned `optimal_inaccurate` with a spurious
positive maximum about `6.1e-5`; it was a discovery diagnostic, not a theorem.
The exact displayed rank-one family resolves the scalar optimization at zero.
