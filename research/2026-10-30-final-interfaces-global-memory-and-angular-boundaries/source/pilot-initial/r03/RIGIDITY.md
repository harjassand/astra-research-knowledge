# Strict quasiconvexity from acoustic singular planes

For the accepted angular quartic

\[
 F_*(A)=|A|^4+\frac{3132}{301}(\det A)^2
                 +\frac{1196}{301}(\det A)X(A),
 \qquad X=a^2+c^2-b^2-d^2,
\]

the supplied non-strict quasiconvexity conclusion can be strengthened:

**Theorem.** On any bounded Lipschitz domain \(U\subset\mathbb R^2\), for
every matrix \(M\) and every \(\varphi\in W^{1,4}_0(U;\mathbb R^2)\) with
\(D\varphi\ne0\) on a set of positive measure,

\[
 \int_U F_*(M+D\varphi)>|U|F_*(M).                 \tag{1}
\]

Thus the affine map is the unique minimizer with its affine boundary
values, even though this energy is not polyconvex and lies on the curved
rank-one-convex boundary. The same conclusion holds for the other accepted
seed \(F_{11/13,28/13}\), and for every member of the already-certified arc
\(|\tau-1/30|<2^{-206}\). This does not enlarge that arc or classify any
additional quartic as quasiconvex.

The mechanism is a general rigidity criterion for heat certificates. Its
exceptional gradients occupy finitely many planes that contain no nonzero
rank-one matrix. Equality in the integrated heat inequality would force an
analytic periodic gradient into one of those planes, which is impossible
unless it is constant. No uniform positive pointwise margin is used.

## 1. The first attack fails at actual acoustic zeros

The inherited identity has the form

\[
 \sum_{j=1}^2F''(A)[B_j,B_j]+d\alpha_A(B_1,B_2)
       =h^T C_F(A)h\geq0,
\]

where \(B_1=(h_0,h_1,h_3,h_4)\) and
\(B_2=(h_1,h_2,h_4,h_5)\). A direct attempt to prove strictness by a
pointwise positive lower bound fails. At the acoustic points the actual
factorization has a nonzero null vector, rather than an inconveniently
small eigenvalue. The executable check verifies, in the exact quotient
algebra of \((w,g)\),

\[
 Ck=0,\qquad k_2=k_1^2,\quad k_4=k_1k_3,\quad k_5=k_1^2k_3,
 \quad k_0=1.                                   \tag{2}
\]

Consequently these null vectors are genuine compatible acoustic tensors
\(h^a_{ij}=v_a\xi_i\xi_j\), with \(v=(1,k_3)\), \(\xi=(1,k_1)\).

There is also a concrete finite-amplitude diagnostic. Let \(t>0\) be the
smaller positive root of

\[
 m(t)=2710t^4-83981t^2+2710=0.
\]

Put \(R=\left(\begin{smallmatrix}1&t\\0&0\end{smallmatrix}\right)\),
and let the entries of \(K\), in order \((a,b,c,d)\), be

\[
\begin{split}
 K_0&=-299(10+291t^2)(1+t^2),\\
 K_1&=299t(291+10t^2)(1+t^2),\\
 K_2&=89401t(1-t^2)-3010t(1+t^2)^2,\\
 K_3&=89401t^2(1-t^2)+3010(1+t^2)^2.
\end{split}
\]

This is an integer scaling of the governing arc construction at
\(\tau=1/30\). Exact division by \(m\) gives

\[
 F_*(K+sR)=F_*(K)+sDF_*(K):R+s^4(1+t^2)^2.        \tag{3}
\]

In particular the quadratic and cubic coefficients vanish identically at
this real acoustic root. On a periodic parallelogram having one reciprocal
lattice direction \(\xi=(1,t)\), set
\(\varphi(x)=\epsilon e_1\sin(\xi\cdot x)\). Averaging (3) gives

\[
 \fint [F_*(K+D\varphi)-F_*(K)]
       =\frac38\epsilon^4(1+t^2)^2>0.              \tag{4}
\]

The corresponding \(\fint|D\varphi|^2\) is
\(\epsilon^2(1+t^2)/2\). A positive quadratic strong-quasiconvexity
bound at this base is therefore impossible. The same obstruction applies
to a Dirichlet-test bound by taking many periods and cutting off in a
boundary layer whose relative volume tends to zero, before sending
\(\epsilon\) to zero. The wave nevertheless has a strict gap of quartic
order. The revised attack uses compatibility of a
gradient field with the singular gradient set, instead of replacing
the acoustic zeros by a positive pointwise margin.

## 2. A general finite-plane heat-rigidity principle

Let \(F\) be a quartic polynomial on \(\mathbb R^{2\times2}\). Suppose an
actual globally \(C^2\) one-form \(\alpha\) gives a continuous symmetric
compatible-Hessian matrix \(C_F(A)\) satisfying the identity above, with
\(C_F(A)\geq0\) for every \(A\). Assume its singular set is contained in
a finite union

\[
 \{A:C_F(A)\text{ is singular}\}\ \subset\bigcup_{\ell=1}^N L_\ell,       \tag{5}
\]

where each \(L_\ell\) is a real linear subspace of matrix space and

\[
 L_\ell\cap\{v\otimes\xi:v,\xi\in\mathbb R^2\}=\{0\}.               \tag{6}
\]

Then \(F\) satisfies (1). More precisely, on any periodic torus, for
nonconstant \(\varphi\in W^{1,4}\), its energy under componentwise heat
flow is strictly decreasing at every positive time.

**Proof.** Set
\(u_s(x)=Mx+e^{s\Delta}\varphi(x)\), and
\(E(s)=\int F(Du_s)\). For \(s>0\) this gradient is real analytic in
space. Integration by parts and Stokes give exactly

\[
 E'(s)=-\int h_s^TC_F(Du_s)h_s\leq0,             \tag{7}
\]

where \(h_s=D^2u_s\) is written in compatible coordinates. The integral
of the pullback of \(d\alpha\) is zero. This is the inherited heat/exact-form
criterion, with its actual primitive regularity; no pointwise choice of
a closed correction is substituted.

Suppose \(E'(s)=0\) at a positive time. The nonnegative continuous
integrand in (7) vanishes everywhere. If at any point \(Du_s\) were outside
the union in (5), \(C_F\) would be positive definite on a neighborhood
of that gradient. Consequently \(D^2u_s\) would vanish on a nonempty
open spatial set. Real analyticity on the connected torus would imply
\(D^2u_s=0\) everywhere. Hence, unless the heat-evolved map is affine,

\[
 Du_s(x)\in\bigcup_{\ell=1}^N L_\ell\quad\text{for all }x.             \tag{8}
\]

An analytic map into a finite union of linear subspaces lies in a single
one of them. Indeed, let
\(p_\ell(x)=\operatorname{dist}(Du_s(x),L_\ell)^2\). These are real
analytic. If none were identically zero, each zero set would have empty
interior; finitely many such closed sets cannot cover the torus. Thus
\(Du_s(x)\in L_\ell\) everywhere for some fixed \(\ell\).

Its mean \(M\) also lies in that plane, so \(D(e^{s\Delta}\varphi)\in L_\ell\).
For each nonzero real reciprocal-lattice vector \(k\), the Fourier
coefficient of this gradient is

\[
 i e^{-s|k|^2}\widehat\varphi(k)\otimes k\in L_\ell\otimes\mathbb C.
\]

Its real and imaginary parts are real rank-at-most-one matrices in
\(L_\ell\). By (6) both vanish. All nonconstant modes of \(\varphi\)
therefore vanish, since the heat multiplier is nonzero. This contradicts
nonconstancy. It follows that \(E'(s)<0\) for every \(s>0\) whenever the
initial periodic perturbation is nonconstant.

Heat approximation gives \(E(s)\to E(0)\) as \(s\downarrow0\) for
\(D\varphi\in L^4\); polynomial quartic growth suffices for this passage.
As \(s\to\infty\), \(E(s)\to |\mathbb T^2|F(M)\). Strict decrease at
positive times proves the strict periodic Jensen inequality. For
\(\varphi\in W^{1,4}_0(U)\), extend it by zero to a larger box and
periodize. The outside contribution is constant and cancels. This proves
(1). \(\square\)

The analytic step is essential to this proof. Condition (6) alone is not
being asserted to exclude gradient Young measures supported in a finite
union of planes, or arbitrary nonsmooth differential inclusions into
that union.

## 3. Checking the criterion for the acquired angular certificates

Use the case notation

\[
 T=|A|^2,\quad X=a^2+c^2-b^2-d^2,\quad
 Y=2(ab+cd),\quad Z=2\det A,
 \qquad T^2=X^2+Y^2+Z^2.
\]

The exact Bernstein certificate is stronger than a non-strict sign test:
on each ordinary leaf \(\widetilde C=T^2C_F\) is positive definite,
including the boundary of the leaf. On the local leaves

\[
 Q^T\widetilde C Q=D^TMD,\qquad M>0,\quad\det Q=1.
\]

The first column of \(D\) contains \(w,g\), and its other five columns
are independent coordinate vectors. Thus \(D\) is injective unless
\(w=g=0\). There is no additional possible singular set in the canonical
disk. On \(A=(\begin{smallmatrix}1&b\\0&d\end{smallmatrix})\), exact
reduction by \((w,g)\) gives

\[
 X=\kappa Z,\qquad Z^2=\sigma T^2.               \tag{9}
\]

The full orientation and matrix-cover argument in the governing proof
transports positive definiteness by invertible Hessian congruences.
Left output rotation preserves \(X,Y,Z\); column swap changes the signs
of both \(X,Z\); the other admitted reflection changes only the sign
of \(Y\). Therefore (9) also contains the full nonzero singular set.
The origin belongs to the same eventual union of planes. We only need
containment here, not a converse assertion that every point of (9) is
singular.

Write \(n=(X,Y,Z)/T\). Put
\(s=\sqrt\sigma\), \(e=\sqrt{1-(1+\kappa^2)\sigma}\). For the two seeds
the exact values are

| Seed | \(\kappa\) | \(\sigma\) | \(e^2\) |
| --- | --- | --- | --- |
| \(F_{11/13,28/13}\) | \(4/11\) | \(65/81\) | \(896/9801\) |
| \(F_{299/301,1084/301}\) | \(20/299\) | \(78561/78961\) | \(4336000/7059192361\) |

In particular \(s,e>0\). The possible normalized triples are exactly the
four points

\[
 n=(\kappa\varepsilon s,\delta e,\varepsilon s),
 \qquad \varepsilon,\delta\in\{-1,1\}.           \tag{10}
\]

Identify the columns of \(A\) with complex numbers \(z_1=a+ic\),
\(z_2=b+id\). Since
\(\overline z_1z_2=(Y+iZ)/2\) and \(|z_1|^2=(T+X)/2\), each fibre in
(10) is the real-linear plane

\[
 L_{\varepsilon\delta}:
 z_2=\rho_{\varepsilon\delta}z_1,\qquad
 \rho_{\varepsilon\delta}
 =\frac{\delta e+i\varepsilon s}{1+\kappa\varepsilon s}.               \tag{11}
\]

The denominator is positive because \(|\kappa s|<1\). For every nonzero
member of this plane,

\[
 \det A=\operatorname{Im}\rho_{\varepsilon\delta}|z_1|^2\ne0,
 \qquad \frac{|\det A|}{|A|^2}=\frac{\sqrt\sigma}{2}.                  \tag{12}
\]

Hence each plane contains no nonzero rank-one matrix. Equations (5)--(6)
hold, and the general principle proves the theorem at both seeds.

The internal replays in `verify_rigidity.py` reconstruct the actual
primitives, factorization and orientation identities, and check all 7,840
strict positive-definite Bernstein coefficient matrices across the two
source certificates. The separate exact remainder computations verify
(2), (3), and (9). Replaying an accepted source is not represented as an
independent scientific review.

## 4. The already-certified boundary arc

The governing continuation proof supplies a positive lifted matrix on
the same cover for \(|\tau-1/30|<2^{-206}\), with

\[
 \kappa=\frac{2\tau}{1-3\tau^2},\qquad
 \sigma=
 \frac{(\tau-1)(3\tau-1)(1+3\tau^2)}{(3\tau^2-2\tau+1)^2}.
\]

An exact identity gives

\[
 1-(1+\kappa^2)\sigma
 =\frac{16\tau^3(3\tau^2-3\tau+1)}
 {(3\tau^2-1)^2(3\tau^2-2\tau+1)^2}>0
 \quad (0<\tau<1/3),                            \tag{13}
\]

and \(\sigma>0\) on that interval. The accepted radius lies within this
interval. Consequently its singular set is contained in the same kind
of four rank-one-free planes, and the rigidity theorem applies to each
energy on the accepted arc. Positivity of (13) outside that arc is only
a geometric fact; it does not produce a heat certificate or establish
quasiconvexity there.

## 5. Comparison and the remaining central obligation

Ordinary convexity or polyconvexity cannot explain the theorem for
\(F_*\): the inherited unrestricted minor-support contradiction excludes
polyconvexity. The published Bruno--Pasqualotto classification requires
both left and right rotation invariance, whereas this energy has an
anisotropic \(qX\) term. Their heat/exact-form theorem supplies a valid
ordinary competitor, but its non-strict monotonicity conclusion alone
does not settle equality at the acoustic zeros. The additional finite-plane
rigidity argument uses the actual strictly positive lift already present
in the source, and requires no new primitive acquisition or selection
oracle.

The result rules out any nontrivial exact energy-neutral Sobolev
perturbation of an affine gradient. It does not yet rule out sequences
of oscillations whose normalized gaps tend to zero. In particular, no
constant \(c>0\) has been established such that, uniformly in \(M,U\),

\[
 \int_U[F_*(M+D\varphi)-F_*(M)]
       \geq c\int_U|D\varphi|^4.                \tag{14}
\]

Quantitative rigidity of approximate minimizers remains unresolved; (14)
is a concrete sufficient target. Possible nontrivial equality gradient
Young measures also remain unclassified. These are not asserted to be
exhaustive opposite alternatives: failure of a uniform estimate could
involve varying or unbounded base matrices. The wave (4) rules out a
quadratic modulus; it does not rule out (14).
Neither the finite-plane theorem nor its application settles general
rank-one-convex versus quasiconvex equivalence, the full curved boundary,
or completeness of closed-form heat certificates. Historical priority
of this rigidity observation has not been established.

## Governing material and executable artifact

- Supplied case `PROOF.txt`, Sections 2--6: acquired primitive regularity,
  acoustic-zero identity, strict finite Bernstein certificate, global
  orientation argument, and unrestricted non-polyconvexity of \(F_*\).
- Supplied `ARC_PROOF.txt`, Sections 1--4: the actual continuing family
  and the already-certified radius. The strictness extension inherits
  exactly that interval.
- Supplied literal data: `seed_11_13.json` and `seed_299_301.json`.
- Giuseppe Bruno and Federico Pasqualotto,
  [Quasiconvexity for the Dacorogna--Marcellini Energy](https://arxiv.org/html/2608.06367v1),
  Section 2 and Theorem 2 / Appendix A: governing heat/exact-form method
  and precise rotational-invariance scope. Read as a primary source.

Run `python3 verify_rigidity.py` in this research directory. It uses SymPy
for exact polynomial identities and the unchanged standard-library source
receiver for both seed replays. Its only new output is
`rigidity_results.json` in this directory. The real-analytic and Fourier
arguments are mathematical proofs above, not conclusions inferred from
finite numerical sampling.
