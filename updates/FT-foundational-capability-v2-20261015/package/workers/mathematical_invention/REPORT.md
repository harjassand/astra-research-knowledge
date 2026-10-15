# Mathematical invention worker report

Date: 2026-10-15. Discovery was independent of sibling files. The supplied attachment was read fully. Parent messages provided literature leads and proof stress tests; indispensable statements were reconstructed here.

## Strongest exact result

Let \(T\) be a compactly supported Hermitian matrix distribution on \(\mathbb R^m\), normalized by \(T(1)=I_d\). The following are equivalent:

1. \(T(e^{g\cdot y})\succ0\) for every real \(g\).
2. Some scalar probability measure with every exponential moment makes its convolution with \(T\) a positive matrix distribution.
3. A smooth radial strictly log-concave scalar probability density \(p\), with every derivative integrable against every exponential weight, makes \(T*p\succ0\) at every point.

There is no quantitative lower-bound assumption on the least Laplace eigenvalue. A stronger ordered-space version holds for real Banach values in a proper closed convex cone with nonempty interior and normalized interior mass. Pointedness is unnecessary; the full-space cone is excluded.

For every \(0<\varepsilon<1\), the construction supplies
\[
(1-\varepsilon)p(x)\mathcal L_T(\nabla V(x))
\preceq (T*p)(x)
\preceq(1+\varepsilon)p(x)\mathcal L_T(\nabla V(x)).
\]

Full proof: [PROOF.md](PROOF.md).

## Mathematical operation and hard step

Retain the exact positive real exponential transform. Expand only the nonlinear remainder of the log density. The difficult part is making that remainder uniformly smaller than an arbitrarily deteriorating positivity margin.

Let \(\mu(t)\) be the minimum interior margin of \(\mathcal L_T\) on \(|g|\le t\), and absorb the distribution's order and support radius into
\[
G(t)=\max\{1,e^{R_1t}(1+t)^{N+1}/\mu(t)\}.
\]
Using a fixed smooth step, choose explicit thresholds
\[
S_n\ge2n,\qquad S_{n+1}\ge S_n+2,\qquad
S_n\ge2\log G(n+1),
\]
and set \(q(s)=1+\sum_n\theta(s-S_n)\).
Then \(q\to\infty\), every positive-order derivative is uniformly bounded, and
\(G(q(s))e^{-s}\le C e^{-s/2}\).

The radial potential
\[
V_L(x)=L\int_1^{\sqrt{1+|x/L|^2}}q(\log u)\,du
\]
is smooth and strictly convex even where \(q\) is constant. Its \(k\)-th derivative has the required bound
\(O(L^{1-k}q(\log\rho)\rho^{1-k})\). This turns the local logarithmic error into a global relative error \(O(L^{-1})\), while \(q\to\infty\) ensures every exponential moment.

Necessity uses growing compact cutoffs and moves all derivatives onto the exponential/cutoff test function. Thus it needs no smoothness or derivative integrability of the original noise measure.

## A witness beyond exponential margins

The proof constructs a real \(t\in C_c^\infty([-A,A])\), \(A=\pi^2/6\), with \(\int t=1\) and \(\mathcal L_t(s)>0\) for every real \(s\), but
\[
\mathcal L_t(r_n)\le\exp[-\exp(r_n^2)],
\qquad r_n=2^{2^n}.
\]
It uses
\[
B(z)=\prod_{j\ge1}\frac{\sinh(z/j^2)}{z/j^2},\qquad
Q(z)=\prod_{n\ge1}
\frac{(z-r_n)^2+\delta_n^2}{r_n^2+\delta_n^2},
\qquad \delta_n=\exp[-\exp(r_n^2)].
\]
The full complex bound
\[
|B(z)Q(z)|\le C_k(1+|z|)^{-k}e^{A|\operatorname{Re}z|}
\]
for every \(k\) invokes the smooth Paley–Wiener theorem and yields the compact smooth input.

Every positive scalar-noise regularization of this \(t\) must have cumulants
\[
K_\nu(r_n)\ge \exp(r_n^2)-O(r_n).
\]
Therefore no density obeying \(p(x)\le C e^{-c|x|\log|x|}\) in both tails, for any \(c>0\), can regularize it. The adaptive theorem nevertheless supplies an even smooth strictly log-concave regularizer with all exponential moments. This establishes that the removed margin hypothesis and variable tail profile add actual mathematical scope.

## Exact singular matrix boundary

For an unnormalized finite matrix distribution, positive regularization exists exactly when every real Laplace transform is positive semidefinite and its kernel is independent of \(g\). Compress to the common kernel's orthogonal complement and normalize there. The zero distribution is included.

Merely semidefinite Laplace positivity fails: the transform
\(\left(\begin{smallmatrix}1&g\\g&g^2\end{smallmatrix}\right)\) has varying kernel and comes from
\(\left(\begin{smallmatrix}\delta&-\delta'\\-\delta'&\delta''\end{smallmatrix}\right)\). A positive convolution would force \(p''\ge0\) with zero integral, which is incompatible with a probability density.

## Concrete consequence

Every Hermitian matrix polynomial \(P(g)\succ0\) on all of \(\mathbb R^m\) admits a radial strictly log-concave \(p\) with all exponential derivative moments and
\[
P(-\partial)p(x)\succ0\quad\text{at every }x.
\]
This is a representation theorem, not a polynomial-positivity decision algorithm.

A common regularizer exists for a family of inputs with common compact support, common finite-order seminorm bound, and a positive uniform margin on each bounded real Laplace ball. The normalized quantum tuple class is one special family. A fixed density cannot handle all normalized Laplace-positive distributions without such controls: \(\delta+a\delta''\), \(a>0\), already rules that out.

## Predecessor boundary and status

Positive convolution multipliers are established mathematics. The closest verified primary predecessor is [Katkova–Vishnyakova (2001)](https://ekhnuir.karazin.ua/bitstreams/41e252c6-eba5-435f-bbbb-66a8582ace7e/download), Theorems 1–2: scalar one-dimensional inputs, positive bilateral Laplace transform, and positivity near support endpoints; their Poisson-lattice multiplier makes the convolution nonnegative. The earlier [Diamond–Essén (1978)](https://doi.org/10.1016/0022-247X(78)90091-4) requires direct comparison. The finite lattice version is related to Poincaré–Pólya–Handelman positivity multipliers and face conditions.

The internally derived candidate is the complete arbitrary-margin criterion with matrix/cone values and a scalar radial strictly log-concave regularizer, together with the deep-valley separation. Historical priority is UNKNOWN. No floating-point check substitutes for the all-point proof. The proof has been read and stress-tested inside this agent team; it has no external independent review or formal verification.

The operation does not supply an efficient compiler, optimized variance, stable inversion, demonstrated statistical advantage, or an exceptional physical capability. Its thresholds depend on full compact-ball positivity margins and can be enormous. Mathematical scope expanded; the user's exceptional-advance objective is not established.
