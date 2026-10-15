# Internal deductions supporting branch decisions

These deductions were reconstructed for the capital/method audit from the pinned source statements. They are mathematical review, not a scientific-script replay, physical measurement, or external proof certification. Path/revision/hash receipts are in `READ_REVISION_RECEIPT.json`.

## 1. A stopped-clock RMS bound can certify an absolute deadline interval

Suppose the incoming finite-chain coupling is valid and

\[
\mathbb E(T-\widehat T)^2=V.
\]

For every deadline t and h>0, the elementary event inclusions give

\[
\Pr(\widehat T>t+h)-\frac{V}{h^2}
\le \Pr(T>t)
\le \Pr(\widehat T>t-h)+\frac{V}{h^2}.
\]

Indeed, if T>t but \(\widehat T\le t-h\), the coupling error exceeds h. The analogous lower inclusion uses \(\widehat T>t+h\). Markov's inequality applied to the squared difference bounds either exceptional event by V/h². Clip the lower and upper endpoints to [0,1]. This requires no density or spectral regularity.

If the reduced survival function is certified Lipschitz in time with constant L near the deadline, then

\[
|\Pr(T>t)-\Pr(\widehat T>t)|\le Lh+V/h^2.
\]

For L,V>0, minimizing the right side at \(h=(2V/L)^{1/3}\) gives

\[
|S(t)-\widehat S(t)|\le 3\,2^{-2/3}L^{2/3}V^{1/3}.
\]

The local interval restriction on L must contain the chosen h. L must itself be acquired or bounded with numerical error accounted for. This is an **absolute** probability bound. Relative error needs an additional positive lower bound on the target survival probability; division by an arbitrarily small unknown tail is not justified.

The source's trap example shows why. With independent \(X\sim\mathrm{Exp}(1)\), \(J\sim\mathrm{Bernoulli}(M^{-3})\), and Y exponential of mean M, let T=X+JY and \(\widehat T=(1+M^{-2})X\). Then V=2/M tends to zero, but at t=M,

\[
S(M)\sim M^{-3}/e,\qquad
\widehat S(M)=\exp[-M/(1+M^{-2})].
\]

Thus the normalized relative underestimation tends to one. This disproves a proposed transfer to general relative rare-tail accuracy, not the RMS identity or an absolute deadline certificate.

The same coupling also gives, for any L-Lipschitz scalar utility F,

\[
|\mathbb EF(T)-\mathbb EF(\widehat T)|\le L\sqrt V.
\]

That is a natural task matched to this certificate. Indicator utilities require the smoothing or anti-concentration step above.

## 2. The retained G cannot have the strict FR premise

The exact FT proof gives

\[
G(I+t e_{12})=-1/24+3t^4.
\]

Since \(|I+t e_{12}|^2=2+t^2\), for epsilon>0,

\[
(G-\epsilon|A|^4)(I+t e_{12})
=-1/24-4\epsilon-4\epsilon t^2+(3-\epsilon)t^4.
\]

Its second derivative at zero is \(-8\epsilon<0\). This is a rank-one line. Therefore `G−epsilon|A|^4` is not rank-one convex, hence cannot be quasiconvex. FR's strict critical-trace/coercivity theorem explicitly assumes that strict subtraction is quasiconvex. No epsilon can satisfy that premise for G.

This calculation does not refute G's exact anisotropic heat certificate. It separates its quasiconvexity from a strictly stronger quantitative hypothesis.

## 3. The fixed-direction FS premise nevertheless holds for G

Writing \(u=|\mathrm{column}_1 A|^2\), \(v=|\mathrm{column}_2 A|^2\), and j=det A, the retained polynomial is

\[
G(A)=3(u+v-2j)^2+(35/24)u^2+j^2-(5/2)ju.
\]

For rank-one A, j=0, so

\[
G(A)=3|A|^4+(35/24)u^2.
\]

On the unit rank-one set this is at least 3, with equality when the first column is zero and the second is a unit vector. Consequently

\[
\mu=\min_{\operatorname{rank}A=1,\ |A|=1}G(A)=3.
\]

This is positivity of rank-one **values**, not positive curvature at every affine background. It is compatible with the zero second derivative in the previous calculation.

At the internally proved quasiconvexity scope, G is rank-one convex. Thus FS's fixed-direction amplitude theorem applies for a fixed unit n in W^(1,infinity), connected planar domain or connected torus, admissible nonnegative trace, and positive fourth mass. Its attainment, interior positivity, and uniqueness arguments require only these hypotheses. An attained unweighted weak-flux dual additionally requires a torus or strictly positive continuous boundary trace, ensuring a global positive amplitude lower bound.

Nothing here supplies a uniform inequality over all direction fields or an inexpensive method for discovering the unknown optimal amplitude/flux. FS's independent phase example for the convex energy |A|⁴ already prevents an inference of joint convexity.

## 4. Why the diagonal operator example is not regularizable by one all-exponential law

For the incoming normalized compact signed measures,

\[
T_n=\frac{\delta_2/16+\delta_{-2}+(-1/2+1/n)\delta_0}{9/16+1/n},
\]

the real Laplace entries are exactly

\[
H_n(g)=\frac{e^{2g}/16+e^{-2g}-1/2+1/n}{9/16+1/n}
=\frac{\sinh^2(g-\log 2)+1/n}{9/16+1/n}.
\]

They are strictly positive for each finite n and g. On ell², the diagonal operator H(g) therefore has strictly positive quadratic form on every nonzero vector. At g=log2, however,

\[
H_n(\log2)=\frac{16}{9n+16}\longrightarrow0.
\]

Thus H(log2) is not boundedly invertible and is outside the interior of the positive cone of B(ell²). The compact signed operator measure itself is norm bounded, because its three diagonal coefficient sequences are uniformly bounded, and T(1)=I.

Under PR94's norm-valued distribution theorem, one common all-exponential scalar regularizer would force H(g) to be interior positive for every g. Hence no such common regularizer exists. Each finite compression has positive minimum eigenvalue and may have its own regularizer. Exchanging “for every finite compression there exists noise” with “there exists noise for the whole direct sum” fails.

## 5. Model ambiguity can be harmless for the exact allowed decisions

PR94's scalar-response form is

\[
f_H(u)=f_0-a^TD(I+HD)^{-1}\mathbf1,\qquad D=\operatorname{diag}u.
\]

For invertible R=diag(a), put \(H^*=R^{-1}H^TR\). Diagonal R commutes with D. Transposing the scalar expression and using

\[
(I+DH)^{-1}D=D(I+HD)^{-1}
\]

gives \(f_{H^*}(u)=f_H(u)\) wherever the relevant inverse exists. The hidden directed models need not be uniquely identified to predict the fixed scalar response under diagonal controls. Changed source, detector, or coupled control can break this equivalence and requires new information.

This is a concrete reason to define epistemic sufficiency relative to a declared decision. It establishes neither robust finite-noise acquisition nor correctness of the apparatus assumptions.
