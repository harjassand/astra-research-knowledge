# Quantitative rigidity at every acoustic mean of the certified arc

The first tranche proved that the angular boundary quartics are exposed
extreme rays of the full homogeneous-quartic rank-one-convex cone. The
authorized partner construction proved strict quasiconvexity from the
four rank-one-free planes containing the singular set of their acquired
heat certificate. Neither fact alone supplies a quantitative estimate
for sequences or a theorem about limiting gradient measures.

The further result here is a global-in-amplitude estimate at **every
mean in those four planes**, with a uniform explicit constant. It comes
from an actual finite sum-of-squares minor-support certificate. No
gradient measure is assumed to be supported in the planes.

## The quantitative statement

Put

\[
 H_\tau=1+3\tau^2,\quad B_\tau=1-3\tau^2,\qquad
 \beta(\tau)=B_\tau/H_\tau,\quad r(\tau)=4-12\tau/H_\tau,
\]
\[
 F_\tau(A)=|A|^4+4(r(\tau)-1)(\det A)^2
                      +4\beta(\tau)(\det A)X(A).
\]

Use \(T=|A|^2\), \(X=a^2+c^2-b^2-d^2\),
\(Y=2(ab+cd)\), \(Z=2\det A\). Define

\[
 \kappa_\tau=\frac{2\tau}{1-3\tau^2},\qquad
 \sigma_\tau=
 \frac{(\tau-1)(3\tau-1)(1+3\tau^2)}{(3\tau^2-2\tau+1)^2},
\]
\[
 \mathcal S_\tau=
 \{A:X(A)=\kappa_\tau Z(A),\quad
           Z(A)^2=\sigma_\tau T(A)^2\}.
\]

For every

\[
 |\tau-1/30|\le2^{-206},\qquad A\in\mathcal S_\tau,
\]

there is a real scalar \(\lambda_\tau(A)\) such that, for **every** real
matrix \(V\),

\[
 \boxed{F_\tau(A+V)-F_\tau(A)-DF_\tau(A):V
          -\lambda_\tau(A)\det V\ \ge\ \frac1{64}|V|^4.}       \tag{1}
\]

The closed interval is the scope of the new algebraic support
certificate. When relying on the inherited global quasiconvexity and
non-polyconvexity theorem, retain its stated open interval
\(|\tau-1/30|<2^{-206}\).

At the central seed,
\(\kappa=20/299\), \(\sigma=78561/78961\).
For \(0<\tau<1/3\), \(\mathcal S_\tau\) is exactly a union of four
two-dimensional real linear planes, all containing no nonzero rank-one
matrix. The inherited heat-singular set is contained in this union.

## Consequences for fields and limiting measures

For any bounded Lipschitz domain \(U\), any \(A\in\mathcal S_\tau\),
and any \(\varphi\in W^{1,4}_0(U;\mathbb R^2)\), integration of (1)
and the null-Lagrangian identities give

\[
 \boxed{\int_U[F_\tau(A+D\varphi)-F_\tau(A)]
          \ge\frac1{64}\int_U|D\varphi|^4.}                    \tag{2}
\]

There is no amplitude or frequency restriction. The constant is
independent of the nonzero scale of \(A\), its plane and orientation,
the domain, and the parameter within the certified interval.
The same holds for periodic perturbations on any periodic cell.
Thus normalized energy gaps tending to zero imply normalized strong
\(L^4\) convergence of the gradient perturbations to zero, for such
means. This controls approximate minimizers, rather than just exact
equality for individual test maps.

The quartic order is sharp at these nonzero acoustic means. The partner's
exact soft wave has gap \((3/8)\varepsilon^4(1+t^2)^2\), whereas its
\(L^p\) gradient moment is a positive constant times \(\varepsilon^p\).
Therefore no positive small-amplitude lower bound by that moment can
hold for any \(p<4\). This establishes the order, not optimality of the
constant \(1/64\).

More generally, let \(\nu\) be any probability measure on matrix space
with finite fourth moment, barycenter \(A\in\mathcal S_\tau\), and

\[
 \int\det B\,d\nu(B)=\det A.
\]

Then (1), and
\(\det(A+V)=\det A+\operatorname{cof}A:V+\det V\), give

\[
 \boxed{\int F_\tau(B)\,d\nu(B)-F_\tau(A)
             \ge\frac1{64}\int|B-A|^4\,d\nu(B).}              \tag{3}
\]

In particular every homogeneous gradient Young measure with that
barycenter and equality in quasiconvex Jensen is \(\delta_A\). Its
support may range over all matrix space. Only the mean is constrained
to the four acoustic planes.

For a second interpretation, the affine function of \((B,\det B)\)
on the left support in (1) is a global polyconvex minorant of \(F_\tau\)
which touches only at \(A\). Hence the polyconvex envelope agrees with
\(F_\tau\) on \(\mathcal S_\tau\), although the energy is globally
non-polyconvex on the inherited open arc. This does not determine the
envelope off those planes.

## The exact support construction

Let \(t_\tau\) be the smaller positive root of

\[
 m_\tau(t)=B_\tau^2(1-t^2)^2
           -(1-4\tau+3\tau^2)H_\tau(1+t^2)^2.
\]

Set \(R=(1,t_\tau,0,0)\), using row-major matrix coordinates, and
normalize the actual source acoustic gradient by its first component:

\[
\begin{aligned}
 \widetilde K_0&=-B_\tau[\tau(1-t^2)+H_\tau t^2](1+t^2),\\
 \widetilde K_1&=B_\tau t[H_\tau-\tau(1-t^2)](1+t^2),\\
 \widetilde K_2&=B_\tau^2t(1-t^2)-\tau H_\tau t(1+t^2)^2,\\
 \widetilde K_3&=B_\tau^2t^2(1-t^2)+\tau H_\tau(1+t^2)^2,\\
 K_\tau&=\widetilde K/\widetilde K_0.
\end{aligned}
\]

The denominator is nonzero on the interval. Define

\[
 \lambda_\tau(K_\tau)
   =\big(D^2F_\tau(K_\tau)R\big)_3.                          \tag{4}
\]

Exact generic identities in \(\mathbb Q(\tau)[t]/m_\tau\) give

\[
 D^2F_\tau(R)\widetilde K=0,\qquad
 [D^2F_\tau(\widetilde K)
    -(D^2F_\tau(\widetilde K)R)_3D^2\det]R=0.                 \tag{5}
\]

These are actual acoustic constraints, not a positive pointwise
selection oracle. In particular a quadratic coercivity argument fails
in the direction \(R\). The partner's quartic-order wave is retained;
no quadratic strong-quasiconvexity conclusion is inferred.

Write an arbitrary increment as

\[
 V=(z,tz+v_1,v_2,v_3).
\]

Let \(\Psi\) consist of \(v_1,v_2,v_3\) followed by all ten quadratic
monomials in \((z,v_1,v_2,v_3)\), in the literal order of
`support_gram.json`. A symmetric \(13\times13\) matrix \(G_\tau\)
satisfies the polynomial identity

\[
 F_\tau(K_\tau+V)-F_\tau(K_\tau)-DF_\tau(K_\tau):V
 -\lambda_\tau(K_\tau)\det V-\frac1{64}|V|^4
 =\Psi^TG_\tau\Psi.                                         \tag{6}
\]

At \(\tau=1/30\), the monic acoustic polynomial is
\(t^4-(83981/2710)t^2+1\). `support_gram.json` defines all entries of
\(G\) literally in that quotient field. The verifier reconstructs
(6) from the actual seed coefficients by the independent quartic Taylor
formula

\[
 F(K+V)-F(K)-DF(K):V
 =\tfrac12D^2F(K)[V,V]+DF(V):K+F(V).
\]

The finite Gram coefficient map is integral and independent of
\(\tau,t\): 60 coefficient equations on 91 symmetric entries. For the
continuing family, keep the 31 literal rational free entries fixed, and
solve the same listed pivot entry in each coefficient equation. The
only monomials outside that map are the quadratic \(z^2,zv_i\) and
the cubic \(z^3\); they vanish by (5). This defines a concrete rational
Gram family in \((\tau,t)\), rather than assuming a continuous positive
selection exists.

The smaller positive root is enclosed using the exact formula

\[
 C_\tau=\frac{9\tau^4-6\tau^3-2\tau+1}
                   {\tau(3\tau^2-3\tau+1)},\qquad
 t_\tau=\sqrt{\frac{C_\tau-\sqrt{C_\tau^2-4}}2}.
\]

Rational interval arithmetic with outward rounding to 256 binary bits
encloses every Gram entry throughout the full parameter interval.
Interval LDL elimination verifies 13 strictly positive pivots. The
smallest certified pivot lower bound is approximately
\(0.0002005153726\); all stored bounds are exact rationals. Thus
\(G_\tau>0\) uniformly, proving (6) and the support at \(K_\tau\).
Numerical acquisition and the displayed decimal are not sign premises.

## Transport to the complete singular geometry

For a fixed normalized Hopf triple, write the matrix columns as complex
numbers \(z_1,z_2\). The fibre is

\[
 z_2=\rho_{\varepsilon\delta}z_1,\qquad
 \rho_{\varepsilon\delta}
 =\frac{\delta e+i\varepsilon\sqrt\sigma}
        {1+\kappa\varepsilon\sqrt\sigma},\qquad
 e^2=1-(1+\kappa^2)\sigma>0.
\]

Each nonzero plane is one orbit under positive scaling and output
\(SO(2)\). The two exact energy symmetries
\(A\mapsto CAC\), \(C=\operatorname{diag}(1,-1)\), and column swap
generate all four sign choices \((\varepsilon,\delta)\). They are
isometries on matrix space. The first reverses \(Y\); the second
reverses \(X,Z\). Thus the one acquired support transports to all
nonzero \(A\in\mathcal S_\tau\).

Explicitly, if \(A=sL K_\tau R_0\), where \(L,R_0\) are the relevant
orthogonal maps and \(s>0\), then

\[
 \lambda_\tau(A)=s^2\det(L)\det(R_0)\lambda_\tau(K_\tau).
\]

Homogeneity of degree four leaves the constant \(1/64\) unchanged.
At the origin use

\[
 F_\tau-\tfrac12T^2
 =\tfrac12(X+2\beta Z)^2+\tfrac12Y^2
   +\frac{3(\tau-1)^2(3\tau-1)^2}{2(1+3\tau^2)^2}Z^2\ge0.
\]

This completes (1), including zero.

## The failed extension to all means

The strongest ordinary competitor is a global affine-minor support at
each base. The new SOS constructs it on the acoustic planes. Trying to
use only first moments and determinant moments to extend (3) to every
base fails, for an explicit reason rather than a missing numerical
margin.

`moment_obstruction.py` converts the source's two opposite minor-support
cuts into an exact rational four-atom probability measure. At
\(M=\operatorname{diag}(36,35)\), it has

\[
 \sum_iw_iB_i=M,\qquad \sum_iw_i\det B_i=\det M,
\]
\[
 \sum_iw_iF_*(B_i)-F_*(M)
 =-\frac{806785107359686592469}{923780137704312799232}<0.
                                                                    \tag{7}
\]

Every atom and weight is rational and listed in
`moment_obstruction.json`. The construction uses two mean-zero
two-point distributions along the source's full-rank directions
\(R_+,R_-\), with rational small step \(1/64\); mixture weights cancel
their opposite determinant moments. Both mean identities and the energy
gap are checked exactly. This base is outside the acoustic planes:
\(X(M)-(20/299)Z(M)=-29171/299\ne0\).

The measure in (7) **is not a gradient Young measure**. Its negative gap
is forbidden by the accepted quasiconvexity of \(F_*\). It is an exact
control showing where ordinary moment relaxation loses gradient
compatibility, not a Morrey counterexample. It also gives the explicit
upper bound
\(F_*^{pc}(M)\le F_*(M)-806785107359686592469/923780137704312799232\)
for the polyconvex envelope there.

Consequently the strong support on the acoustic planes does not retract
the unrestricted non-polyconvexity result, nor produce a global
homogeneous polyconvex summand. The first-tranche exposed-ray obstruction
to such summands remains valid.

## Scope and remaining obligation

This proves a uniform quartic estimate and equality-measure rigidity at
the entire singular-mean geometry of the certified non-polyconvex arc.
Together with the partner theorem, it separates exact strictness for
all affine means from quantitative control of approximate minimizers
and limiting measures at the acoustically degenerate means.

General affine means remain unresolved for a uniform quartic estimate
and for equality gradient Young measures. Equation (7) blocks a proof
using only minor moments there; a further argument must retain gradient
compatibility. Nothing here certifies the rest of the curved branch as
quasiconvex or settles general planar Morrey equivalence. Historical
priority has not been investigated.

## Local sources and exact replay

Only the supplied angular case, this run's first-return artifacts, and
the specifically authorized completed partner snapshot were read.
The partner inputs are
[RIGIDITY.md](producer-workspace/RIGIDITY.md),
[verify_rigidity.py](producer-workspace/verify_rigidity.py),
and
[rigidity_results.json](producer-workspace/rigidity_results.json).
The pointwise identities and inherited family are from the unchanged
case `PROOF.txt`, `ARC_PROOF.txt`, and `seed_299_301.json`.

All new work is in this separate `phase2` directory. Exact replay uses
local Python and SymPy:

```sh
python3 verify_support.py
python3 verify_arc_support.py
python3 moment_obstruction.py
```

`support_sos.py` additionally uses local NumPy only to regenerate the
initial free-coefficient proposal. Its solver status is not used by the
exact replay. The new mathematical certificates are `support_gram.json`,
`support_certificate.json`, `arc_support_certificate.json`, and
`moment_obstruction.json`.
