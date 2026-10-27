# The actual first cosine-law root is a globally Lipschitz graph

25 October 2026. This is an exact geometric statement about the first root law, not a generic replacement measure and not a claim about all later residuals.

## Result

Let

\[
M(u,v,w)=\begin{pmatrix}1&u&v\\u&1&w\\v&w&1\end{pmatrix},
\quad K=\{z:M(z)\succeq0\},\quad F=\det M,
\quad d=(-1,2,2),\quad P=I-\frac{d\otimes d}{9},\quad \Omega=PK.
\]

For the actual correlated cosine law \(\mu=\mathcal L(\cos x,\cos y,\cos(x+y))\), let \(\nu_1\) be its full conditional-barycenter contraction along \(d\). As verified in `../morrey_nonlinear_chord_contraction_20261025/INDEPENDENT_CHECK.md`, it has the representation

\[
\nu_1=(h\mapsto h+m(h)d)_\#\lambda,\qquad \lambda=P_\#\mu,
\]

where, on generic fibers,

\[
F(h+td)=-8(t-c)(t-a)(t-b),\quad c<a<b,
\qquad m(h)=\frac{2ab-c(a+b)}{a+b-2c}.
\]

The continuous extension of \(m\) to the compact convex domain \(\Omega\) is globally Lipschitz. Consequently an open cone of directions around \(d\) has injective projection on the entire support of \(\nu_1\). This cone contains an open arc of null directions for

\[
q(u,v,w)=uv+uw+vw.
\]

In particular, there exist three linearly independent null directions, one equal to \(d\), along each of which \(\nu_1\) has zero contraction activity. Starting from the actual \(\mu\), applying \(d\) first and then cycling through these three spanning directions produces \(\nu_1\) forever. This disproves the assertion that a recurrent finite spanning null-direction set necessarily collapses this actual law to \(\delta_0\).

## 1. Exceptional geometry and absence of triple roots

Write

\[
H=D_dM=\begin{pmatrix}0&-1&2\\-1&0&2\\2&2&0\end{pmatrix},\qquad \det H=-8.
\]

A positive-length section of \(K\) along \(d\) contains a positive-definite matrix: otherwise its determinant vanishes on an interval, impossible because its cubic leading coefficient is \(-8\). Thus boundary points of \(\Omega\) have singleton physical fibers, with \(a=b\). Interior points of \(\Omega\) have positive-length fibers, by the usual relative-interior property of linear images of convex bodies.

There is no triple root at any point of \(K\). To see the rank-two case directly, use orthogonal coordinates in which

\[
M_0=\begin{pmatrix}A&0\\0&0\end{pmatrix},\quad A\succ0,
\qquad H=\begin{pmatrix}B&b\\b^T&h\end{pmatrix}.
\]

At tangency, the first determinant coefficient is \(\det(A)h=0\). The second is then \(-\det(A)b^TA^{-1}b\), which can vanish only if \(b=0\). But \(h=0=b\) makes \(H\) singular, a contradiction. This also shows that a rank-two double-root point cannot be an endpoint of a positive-length physical fiber: its Schur complement is negative on both sufficiently small nonzero sides.

The rank-one points are the four vertices \((1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)\). At these points

\[
F(V+sd)=s^2(\beta(V)-8s),\qquad \beta(z)=-9+8u-4v-4w,
\]

and the respective values of \(\beta\) are \(-9,7,-17,-17\), all nonzero. Only

\[
V=(1,-1,-1)
\]

can lie on a positive-length physical fiber: at the other vertices the determinant is negative on both sufficiently small nonzero sides. Convexity excludes an interior point farther along such a line if no interior point exists near its vertex. The calculation below proves that \(d\) enters \(\operatorname{int}K\) at \(V\).

Thus the only interior-projection collision is

\[
h_* = PV=(4/9,1/9,1/9),\qquad a=c=-5/9,\qquad b=23/72,
\]

corresponding to the endpoints \(V\) and \(W=(1/8,3/4,3/4)\). Everywhere else in \(\operatorname{int}\Omega\), all three roots are distinct and \(m\) is analytic.

## 2. Projected boundary: the apparent square-root singularity cancels

At every \(h_0\in\partial\Omega\), the physical roots satisfy \(a=b\), and the exterior root \(c<a\) is simple. The implicit-function theorem therefore gives an analytic continuation of \(c(h)\) to a full neighborhood of \(h_0\) in \(d^\perp\).

Put \(s=a+b\) and \(p=ab\). Both are analytic there because they are symmetric functions of the other two roots after removing the analytic simple root \(c\). Explicitly, if

\[
F(h+td)=-8t^3+\beta(h)t^2+C(h)t+F(h),
\]

then

\[
s=\beta/8-c,\qquad p=-C/8-cs.
\]

The root graph is

\[
m=\frac{2p-cs}{s-2c},
\]

whose denominator at \(h_0\) is \(2(a-c)>0\). It therefore extends analytically across every projected boundary point, including the three projected rank-one vertices. No differentiation of the individually nonsmooth roots \(a,b\) is needed.

## 3. The exceptional interior point: definite compression gives Lipschitz roots

Let

\[
n_1=\frac{(1,-1,0)}{\sqrt2},\qquad
n_2=\frac{(1,1,2)}{\sqrt6},\qquad
e_0=\frac{(1,1,-1)}{\sqrt3}.
\]

The first two vectors span \(\ker M(V)\), and \(M(V)=3e_0e_0^T\). In this orthonormal basis,

\[
H=\begin{pmatrix}
1&0&0\\
0&7/3&\sqrt2/3\\
0&\sqrt2/3&-10/3
\end{pmatrix}.
\]

In particular,

\[
H|_{\ker M(V)}=\operatorname{diag}(1,7/3)\succ0.
\]

This verifies, rather than assumes, the key definiteness.

Write \(h=h_*+\eta\), \(t=-5/9+s\), so

\[
M(h+td)=M(V)+M_0(\eta)+sH,
\]

where \(M_0\) is the linear zero-diagonal off-diagonal map. Its operator norm obeys

\[
\|M_0(\eta)\|\le\sqrt2|\eta|.
\]

In the displayed orthogonal decomposition write the matrix as

\[
\begin{pmatrix}A(\eta,s)&B(\eta,s)\\B(\eta,s)^T&C(\eta,s)\end{pmatrix}
\]

and use the symmetric Schur complement

\[
S(\eta,s)=A-BC^{-1}B^T.
\]

At the origin,

\[
S(0,0)=0,\qquad \partial_sS(0,0)=\operatorname{diag}(1,7/3).
\]

Here are explicit neighborhood bounds, so the local claim does not merely invoke unspecified root regularity. On

\[
|\eta|\le1/16,\qquad |s|\le1/16,
\]

one has

\[
C\ge2,\quad |B|\le1/8,\quad |\partial_sB|=\sqrt2/3<1/2,
\quad |\partial_sC|=10/3<4.
\]

Consequently

\[
\left\|\partial_sS-\operatorname{diag}(1,7/3)\right\|
\le\frac{2(1/2)(1/8)}2+\frac{4(1/8)^2}{2^2}
=\frac5{64},
\]

so, conservatively,

\[
\partial_sS\succeq\tfrac12I.
\]

For a unit direction in \(\eta\), the derivatives of \(A,B,C\) are each bounded by \(\sqrt2<2\). Hence

\[
\|\partial_\eta S\|
\le2+\frac{2(1/8)2}{2}+\frac{(1/8)^2 2}{2^2}<3.
\]

For every \(|\eta|\le1/192\), these bounds imply

\[
S(\eta,-1/16)\prec0,\qquad S(\eta,1/16)\succ0,
\]

since the signed margin at \(\eta=0\) is at least \(1/32\), and the perturbation is at most \(3/192=1/64\). In particular, the point with \(s=1/16\) is positive definite, proving that this entire \(\eta\)-ball is in \(\operatorname{int}\Omega\).

Let \(\ell_1(\eta,s)\le\ell_2(\eta,s)\) be the ordered eigenvalues of \(S\). Loewner monotonicity and the eigenvalue perturbation inequality give

\[
\ell_i(\eta,s_2)-\ell_i(\eta,s_1)\ge\tfrac12(s_2-s_1)
\quad(s_2\ge s_1),
\]

\[
|\ell_i(\eta,s)-\ell_i(\eta',s)|\le3|\eta-\eta'|.
\]

Each \(\ell_i\) has a unique zero in \((-1/16,1/16)\). Comparing the zeros using the two inequalities proves that each zero is \(6\)-Lipschitz in \(\eta\). These two zeros are exactly \(c+5/9\) and \(a+5/9\): \(\ell_2\) crosses first, then \(\ell_1\). The third root remains separated near \(b=23/72\).

Thus

\[
\operatorname{Lip}(a),\operatorname{Lip}(c)\le6
\quad\text{on }B(h_*,1/192).
\]

The root sum is

\[
a+b+c=-9/8+h_u-h_v/2-h_w/2.
\]

On \(d^\perp\), its derivative has norm \(1/\sqrt2<1\). Hence \(\operatorname{Lip}(b)\le13\). Throughout this ball, all three roots have absolute value less than one, and

\[
T=a+b-2c\ge\frac78-\frac{31}{192}=\frac{137}{192}>\frac12.
\]

For \(N=2ab-c(a+b)\), the product rule gives \(\operatorname{Lip}(N)\le69\), whereas \(\operatorname{Lip}(T)\le31\). Since \(m=N/T\in[a,b]\subset[-1,1]\), the identity

\[
m(h)-m(h')=\frac{N(h)-N(h')-m(h')[T(h)-T(h')]}{T(h)}
\]

gives the explicit local estimate

\[
\boxed{\operatorname{Lip}_{B(h_*,1/192)}m\le200.}
\]

The value 200 is deliberately crude; finiteness, not its optimization, is the relevant fact.

## 4. From local regularity to a global Lipschitz bound

Every point of \(\Omega\) now has a relative neighborhood on which \(m\) is Lipschitz: the preceding ball handles \(h_*\), interior simple-root points are analytic, and Section 2 gives analytic extensions at all boundary points.

Compactness gives a finite cover by smaller such neighborhoods, with finite constants \(L_1,\ldots,L_N\). Set

\[
L=\max(1,200,L_1,\ldots,L_N)<\infty.
\]

Given \(h,k\in\Omega\), their straight segment remains in \(\Omega\), by convexity. Subdivide the segment into finitely many pieces subordinate to the cover (a Lebesgue number suffices). Sum the local estimates over those pieces. Their lengths add to \(|h-k|\), so

\[
\boxed{|m(h)-m(k)|\le L|h-k|\qquad(h,k\in\Omega).}
\]

This is an existential finite global bound with an explicit bound at the only nonanalytic interior point. No numerical regularity inference is used.

## 5. The global excluded cone and three spanning null directions

Let \(e=d/3\). For two support points

\[
z=h+m(h)d,\qquad z'=k+m(k)d,
\]

their chord \(v=z-z'\) obeys

\[
Pv=h-k,\qquad |v\cdot e|=3|m(h)-m(k)|\le3L|Pv|.
\]

Therefore no nonzero support chord belongs to the open double cone

\[
\mathcal C=\{v\ne0:|v\cdot e|>3L|Pv|\}.
\]

This cone contains \(d\) and \(-d\). For every \(n\in\mathcal C\), orthogonal projection onto \(n^\perp\) is injective on the entire compact graph \(\Gamma=\{h+m(h)d:h\in\Omega\}\).

An explicit null-direction parametrization is

\[
d(r)=(1-r,r^2-r,r),\qquad q(d(r))=0,\qquad d(2)=d.
\]

Indeed its physical matrix is

\[
\begin{pmatrix}u+w&w\\w&v+w\end{pmatrix}
=\begin{pmatrix}1&r\\r&r^2\end{pmatrix}
=(1,r)\otimes(1,r).
\]

Continuity puts an open interval of \(r\)'s around 2 in \(\mathcal C\). More quantitatively, for \(|s|\le1/4\),

\[
|Pd(2+s)|\le|d(2+s)-d(2)|<4|s|,
\qquad d(2+s)\cdot e=3+3s+2s^2/3\ge9/4.
\]

Thus, for example, choosing

\[
0<\varepsilon=\frac1{16(1+L)}
\]

puts \(d(2),d(2+\varepsilon),d(2-\varepsilon)\) in \(\mathcal C\). They span \(\mathbb R^3\), because the exact determinant is

\[
\boxed{\det[d(2),d(2+\varepsilon),d(2-\varepsilon)]=-2\varepsilon^3\ne0.}
\]

## 6. Actual-law stationarity and the precise limitation proved

The density of \(\lambda\) is strictly positive on generic interior fibers, so its support is \(\Omega\), and \(\operatorname{supp}\nu_1=\Gamma\). In fact only containment in \(\Gamma\) is needed for stationarity.

For any \(n\in\mathcal C\), the continuous projection \(\Gamma\to P_n\Gamma\) is a bijection between compact and Hausdorff spaces, hence has a continuous inverse. A \(\nu_1\)-distributed point is therefore a measurable function of its \(n^\perp\)-projection. Its conditional law on almost every \(n\)-fiber is a Dirac mass. The full conditional-mean contraction along \(n\) is exactly the identity on \(\nu_1\); its null stress and variance loss are zero. The same chord exclusion also rules out positive partial two-point mixing along those directions.

The measure \(\nu_1\) is genuinely nontrivial. The original law has mean zero and covariance \(I/2\), and the first contraction preserves \(PZ\). Hence

\[
\int |Pz|^2\,d\nu_1(z)=\int|Pz|^2\,d\mu(z)=1.
\]

In particular, \(\nu_1\ne\delta_0\), without relying on any numerical activity estimate.

Take the fixed spanning finite direction set

\[
\mathcal D=\{d(2),d(2+\varepsilon),d(2-\varepsilon)\}.
\]

The cyclic schedule starting with \(d(2)\) takes the actual correlated cosine law to \(\nu_1\) on its first step and remains there on every subsequent step, although each of the three linearly independent directions is revisited infinitely often.

This establishes an actual-law obstruction to “finite spanning plus fair/recurrent scheduling implies collapse.” It does not assert that every finite spanning set fails, that useful directions outside this cone do not exist, or that full null-direction/adaptive contraction cannot collapse. In particular, it is fully consistent with the rigorously positive second contraction along the \(u\)-axis in the independent audit: that axis is necessarily outside the excluded cone.

## Exact checks performed

SymPy exact arithmetic independently verified the displayed orthogonal compression of \(H\), \(\det(M(V)+sH)=s^2(7-8s)\), \(q(d(r))=0\), and the determinant \(-2\varepsilon^3\). The Lipschitz and cone arguments above are analytic estimates, not sampling-based evidence.
