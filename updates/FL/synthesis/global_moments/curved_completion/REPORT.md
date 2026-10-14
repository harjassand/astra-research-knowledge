# Curved shears: an explicit all-background N794 completion

## Result and scope

For the left-SO(2)-invariant planar quartics in N794, the non-affine sheared
family from work/FL-phase-geometry/REPORT.md has an explicit 8x8 PSD dual
completion at every affine background. It is the sum of two positive pieces:

1. a zero-background flux completion $Y_0$, where the integrated phase
   curvature defect cancels under the two weighted conditions in the phase
   theorem; and
2. a Fourier sum $Y_H(B)$ of acoustic rank-one atoms representing the
   background Hessian contribution.

The resulting matrix is $Y_B=Y_0+Y_H(B)$. Its nine N794 pairings are exactly

\[
m_i(B,\varphi)=\left\langle f_i(B+D\varphi)-f_i(B)\right\rangle,
\qquad i=1,\ldots,9,
\]

and its six skew-block constraints vanish. For every rank-one-convex quartic
in this nine-coefficient class, the complete affine-background minimum on
this structured family is attained at the common optimizer $B=0$.

This joins the phase-geometry and global-moment derivations internally; it is
not external verification of either source. It does not give a completion for
arbitrary compatible gradients and does not close the general N794 gate. The
curvature cancellation below uses left-SO(2) invariance. No full35 curved
completion is asserted.

## Family and zero-background cancellation

Use the standard $2\pi$-periodic torus, normalized average
$\langle\cdot\rangle$, and the circular carrier

\[
V(\theta)=(\cos\theta,\sin\theta),\quad W=V',\quad
\theta(x,y)=ny+g(x),\quad k=\nabla\theta=(g'(x),n),
\]

where $n\in\mathbb Z\setminus\{0\}$ and $g$ is periodic. Let $r$ be smooth
and periodic with

\[
r(x,y+\pi/|n|)=r(x,y),\qquad
\mu(x)=\frac1{2\pi}\int_0^{2\pi}r(x,y)^4\,dy.
\]

Assume the two exact weighted curvature cancellations

\[
\int_0^{2\pi}\mu(x)g''(x)\,dx=0,\qquad
\int_0^{2\pi}\mu(x)g'(x)g''(x)\,dx=0. \tag{1}
\]

Set $\varphi=rV(\theta)$, $X=D\varphi$, $P=rW\otimes k$, and
$Q=V\otimes\nabla r$, so $X=P+Q$.

For an invariant quartic in N794's basis

\[
f=(u^2,v^2,uv,w^2,uw,vw,qu,qv,qw),
\]

write its orientation-odd part as $q(Lu+Mv+Nw)$. The phase-flux report
derives, at $B=0$,

\[
\mathcal E_F=\frac{r^4}{4}\operatorname{div}\Xi(k),\qquad
\Xi(k)=(Lk_1^2+Mk_2^2+Nk_1k_2)(k_2,-k_1).
\]

For $k=(g',n)$,

\[
\operatorname{div}\Xi(k)=n(2Lg'+nN)g'',
\]

and hence

\[
\langle\mathcal E_F\rangle=
\frac{n}{8\pi}\left(
  2L\int_0^{2\pi}\mu g'g''\,dx+
  nN\int_0^{2\pi}\mu g''\,dx
\right)=0. \tag{2}
\]

The six reflection-even coefficients contribute no curvature field. Conditions
(1) therefore cancel the integrated defect for every invariant quartic,
coefficient by coefficient.

The variable-phase flux identity, with its signed defect, is

\[
\langle F(X)\rangle=
\left\langle\mathcal R_F(P,Q)\right\rangle+
\left\langle\int_0^1 t r^2
 D^2F(tP)[V\otimes k,V\otimes k]\,dt\right\rangle-
\langle\mathcal E_F\rangle,
\]

where $\mathcal R_F(P,Q)=\int_0^1(1-s)D^2F(P+sQ)[Q,Q]\,ds$. The last
term vanishes after averaging by (2). Here the circular carrier has
$|V|=1$ and curvature coefficient $a(\theta)=1$.

For a pointwise $U\in SO(2)$ with $Ue_1=V/|V|$, put

\[
x_U(A)=\operatorname{vec}_{\rm row}(U^TA),\qquad
z_U(A,b)=\begin{pmatrix}b_1x_U(A)\\b_2x_U(A)\end{pmatrix}\in\mathbb R^8.
\]

If $Q_F(K)$ is the N794 acoustic Gram matrix for any skew completion $K$,
then

\[
D^2F(A)[V\otimes b,V\otimes b]
=|V|^2z_U(A,b)^TQ_F(K)z_U(A,b).
\]

The zero-background matrix is therefore the explicit flux integral

\[
\boxed{\begin{aligned}
Y_0={}&\left\langle\int_0^1(1-s)|V|^2
 z_U(P+sQ,\nabla r)z_U(P+sQ,\nabla r)^T\,ds\right.\\
&\left.\hspace{1.8em}+r^2\int_0^1t|V|^2
 z_U(tP,k)z_U(tP,k)^T\,dt\right\rangle.
\end{aligned}} \tag{3}
\]

Both terms are integrals of PSD outer products. Their off-diagonal 4x4
blocks are symmetric, so $Y_0\succeq0$ and it annihilates all six N794
skew-block constraints. Pairing (3) with an arbitrary coefficient vector
recovers $\langle F(X)\rangle$, since the signed defect is zero. Comparing
coefficients gives the nine zero-background pairings
$\langle B_i,Y_0\rangle=\langle f_i(X)\rangle$.

## All backgrounds by half-turn symmetry and Fourier atoms

The imposed half-turn gives

\[
\varphi(x,y+\pi/|n|)=-\varphi(x,y),\qquad
X(x,y+\pi/|n|)=-X(x,y).
\]

Thus $X$ has a centrally symmetric distribution. For every homogeneous
quartic $F$, its exact Taylor expansion at any fixed matrix $B$, followed by
averaging, is

\[
\boxed{\left\langle F(B+X)-F(B)\right\rangle
=c+\frac12\left\langle D^2F(B)[X,X]\right\rangle,\quad
c=\langle F(X)\rangle.} \tag{4}
\]

The linear term has zero average because $X$ is a periodic gradient; the
cubic term vanishes by $X\mapsto-X$. Quartic tensor symmetry also gives the
reciprocity identity $D^2F(B)[X,X]=D^2F(X)[B,B]$ pointwise.

Choose one representative from each pair of nonzero torus frequencies and
write the real Fourier expansion

\[
\varphi=\widehat\varphi_0+
\sum_{\kappa\in K_+}
  \left(\alpha_\kappa\cos(\kappa\cdot x)+
   \beta_\kappa\sin(\kappa\cdot x)\right),\qquad
\kappa\in\mathbb Z^2\setminus\{0\}.
\]

Orthogonality, with normalized torus average, fixes the factor exactly:

\[
\frac12\langle D^2F(B)[X,X]\rangle=
\frac14\sum_{\kappa\in K_+}\left(
 D^2F(B)[\alpha_\kappa\otimes\kappa,\alpha_\kappa\otimes\kappa]+
 D^2F(B)[\beta_\kappa\otimes\kappa,\beta_\kappa\otimes\kappa]\right).
 \tag{5}
\]

For each nonzero amplitude $a\in\{\alpha_\kappa,\beta_\kappa\}$, choose
$U_a\in SO(2)$ with $U_ae_1=a/|a|$. Define

\[
\boxed{Y_H(B)=\frac14\sum_{\kappa\in K_+}
 \left(
 |\alpha_\kappa|^2 z_{U_{\alpha_\kappa}}(B,\kappa)
                    z_{U_{\alpha_\kappa}}(B,\kappa)^T+
 |\beta_\kappa|^2 z_{U_{\beta_\kappa}}(B,\kappa)
                    z_{U_{\beta_\kappa}}(B,\kappa)^T
 \right),} \tag{6}
\]

omitting zero amplitudes. This is a convergent PSD series for a smooth
profile. Each term is an acoustic atom, so its off-diagonal block is
symmetric. By the N794 acoustic identity and (5),

\[
\langle B_i,Y_H(B)\rangle=
\frac12\langle D^2f_i(B)[X,X]\rangle,\qquad
\langle C_j,Y_H(B)\rangle=0.
\]

Combining with (3),

\[
\boxed{Y_B=Y_0+Y_H(B)\succeq0,\quad
\langle B_i,Y_B\rangle=m_i(B,\varphi),\quad
\langle C_j,Y_B\rangle=0.} \tag{7}
\]

This is an explicit N794 dual completion at every background for this
profile.

If $F$ is rank-one convex, each acoustic Hessian in (5) is nonnegative, so
the second term in (4) is nonnegative. The first term is nonnegative by (3).
Therefore

\[
\inf_{B\in\mathbb R^{2\times2}}
\langle F(B+D\varphi)-F(B)\rangle
=\langle F(D\varphi)\rangle\ge0,
\]

with the common minimum at $B=0$ for every rank-one-convex quartic in this
class. The Fourier-Hessian extension itself is broader: for any smooth
compatible periodic gradient with a half-turn $X\mapsto-X$, (5)-(6) provide
the background increment $\frac12\langle D^2F(B)[X,X]\rangle$. What remains
profile-specific is the base completion $Y_0$ for $\langle F(X)\rangle$.
Thus, once a zero-background PSD completion is known, half-turn symmetry and
Fourier atoms extend it to every background.

## Exact curved example and factors

Take

\[
g(x)=\tfrac14\sin x,\quad \theta=y+g(x),\quad
r(x,y)=1+\tfrac15\cos(2\theta),\quad V=(\cos\theta,\sin\theta).
\]

It is non-affine, $r$ depends on both coordinates, $r\in[4/5,6/5]$, and

\[
\mu(x)=\langle r^4\rangle_y=\frac{5603}{5000},\qquad
\int\mu g''=\int\mu g'g''=0.
\]

Here $X=(r_\theta V+rW)\otimes(g',1)$, so this exact example has rank-one
gradient pointwise. Exact averaging gives

\[
\langle f(X)\rangle=
\left(\frac{19377}{10240000},\frac{6459}{5000},
\frac{6459}{160000},\frac{6459}{160000},0,0,0,0,0\right).
\]

The corresponding exact matrix (3), with rank 6, is

\[
Y_0=\begin{pmatrix}
3/2560000&0&0&0&0&1/40000&0&0\\
0&1/40000&0&0&1/40000&0&0&0\\
0&0&19233/40960000&0&0&0&0&6411/640000\\
0&0&0&6411/640000&0&0&6411/640000&0\\
0&1/40000&0&0&1/40000&0&0&0\\
1/40000&0&0&0&0&1/1250&0&0\\
0&0&0&6411/640000&0&0&6411/640000&0\\
0&0&6411/640000&0&0&0&0&6411/20000
\end{pmatrix}.
\]

Its nine exact N794 pairings equal the displayed moment vector. The curved
phase theorem's separate example, with $g(x)=\frac14\sin x$ and an amplitude
transported by a distinct nonconstant phase $h(x)=\frac13\sin(2x)$, has a
full-rank gradient on an open set. It confirms that the analytic family is
not restricted to the rank-one example used for the rational matrix check.

For this same rank-one exact profile, $rV$ has the Bessel expansion

\[
\varphi_1=\frac{11}{10}\cos\theta+\frac1{10}\cos(3\theta),\qquad
\varphi_2=\frac9{10}\sin\theta+\frac1{10}\sin(3\theta).
\]

With $J_\ell$ the Bessel functions of the first kind and representatives
$\kappa=(\ell,j)$ for every positive vertical frequency $j\in\{1,3\}$, its
real Fourier coefficients are

\[
\alpha_{\ell,j}=a_jJ_\ell(j/4)e_1,\qquad
\beta_{\ell,j}=b_jJ_\ell(j/4)e_2,
\]

where $(a_1,b_1)=(11/10,9/10)$ and $(a_3,b_3)=(1/10,1/10)$. Thus (6) is an
explicit convergent series for the actual curved example; use $U_{e_1}=I$
and $U_{e_2}=\begin{psmallmatrix}0&-1\\1&0\end{psmallmatrix}$. The Bessel
series decays rapidly and each summand is PSD.

An independent finite-mode exact check uses
$\varphi=(\cos x+\sin y,\sin x+\cos y)$ at
$B=\begin{psmallmatrix}1/2&-1/3\\2/5&3/4\end{psmallmatrix}$. The translation
$(\pi,\pi)$ reverses $X$. Direct Fourier arithmetic confirms all nine
pairings of (6) equal

\[
\left(\frac{41}{25},\frac{97}{36},\frac{3901}{3600},
\frac{3901}{7200},\frac4{15},\frac4{15},
\frac{61}{60},\frac{61}{60},0\right),
\]

which is also the exact increment $m(B)-m(0)$. This fixes the normalized
Fourier weight at $1/4$ per cosine/sine amplitude.

## Boundary: this does not generate arbitrary compatible moments

The new family has the exact anti-period property
$\varphi(x,y+\pi/|n|)=-\varphi(x,y)$. A profile that has no translation
sending it to its negative cannot be a member of this family, even after an
invertible input-coordinate change. The connected-triad profile already
recorded in work/FL-global-moments/REPORT.md is

\[
\psi_1=\cos x-\sin x+\cos y-\sin y,\quad
\psi_2=\cos x+\sin x+\cos y-\sin y+\cos(x+y)+\sin(x+y).
\]

It has nonzero frequency classes $e_1,e_2,e_1+e_2$. An anti-period
translation $t=(t_x,t_y)$ would require simultaneously

\[
t_x=\pi,\qquad t_y=\pi,\qquad t_x+t_y=\pi\pmod{2\pi},
\]

which is impossible. This is an exact profile obstruction to direct
pointwise generation by the curved family. The old packet also gives its
exact nine-moment vector, but neither this translation test nor that profile
vector separates its moment from the conic hull of curved-family moments.
No moment-cone separation is claimed.

Consequently, (7) does not put arbitrary compatible-gradient moments in
$C_9^*$. The Fourier atoms supply the background correction for any
compatible gradient after its zero-background moment is completed; they do
not provide that missing base completion. The earlier closed-cone polar
generation statement for the straight modulation family also remains only a
dual-cone characterization, not membership for arbitrary compatible
gradients.

## N794, N809, N806, and full35 boundaries

- **N794 / left-SO(2), nine coefficients:** this packet supplies a structured
  family of explicit 8x8 dual completions, including every affine background.
  It does not satisfy the general nine-moment compatibility-completion gate
  for arbitrary periodic gradients.
- **Full35:** the Fourier expansion (5) and its acoustic rank-one increment
  are not restricted to left-SO(2) at the level of Hessians. The zero-background
  cancellation (2), however, uses the nine-coefficient invariant reduction
  and says nothing for the other 26 coefficients. There is no full35 curved
  $Y_0$ or 35-coefficient completion claim here.
- **N809:** its current dossier/notices concern all-background stability near
  simple rank-three transverse contacts in full35; tangent/rank-two and global
  closure remain open. The present family does not meet that result's role as
  a general global compatibility theorem.
- **N806:** its current dossier/notices concern fixed-contact cubic
  compensation in the nine-coefficient class. The phase-flux cancellation
  here applies only to profiles satisfying (1), not arbitrary moving phase
  curvature or contact concentration.

The proof and checks are internal, source-derived and unreviewed externally.
The exact script verifies finite examples, moment pairings, normalization,
and cancellation identities; it does not certify the analytic theorem in a
proof assistant, establish novelty, or close Morrey's implication.
