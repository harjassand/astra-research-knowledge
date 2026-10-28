# Extension of the completed convex-polynomial-lift classification

The general theorem is a completed input, not a discovery of this branch:
`quartic_alternative/POLYCONVEX_PROOF.md` section2.1, using Proposition2.4
of the pinned primary arXiv:2604.11124v1, proves that a homogeneous planar
quartic H has a convex polynomial lift of any degree if and only if
H-lambda*det² is convex for some lambda>=0. The peer applied it to F16.

Here is an extension to every tau in
\[
F_\tau=u^2+v^2+3w^2+\tau q^2+4q(u-v).
\]
At A=I, half the Hessian of F_tau-lambda*q² on the two diagonal
increment coordinates is, with sigma=tau-lambda,
\[
M_\sigma=\begin{pmatrix}\sigma+18&2\sigma\\2\sigma&\sigma-6\end{pmatrix},
\qquad
\det M_\sigma=-3[(\sigma-2)^2+32]<0.
\]
Thus **no member of this line admits a convex polynomial lift of any
degree**, including every tau in the now accepted PC range. Wherever PC
holds, its finite convex lift necessarily is nonpolynomial.

The smaller eigenvalue obeys the uniform bound
\[
\lambda_{\min}(M_\sigma)=\sigma+6-2\sqrt{\sigma^2+36}
\leq6-6\sqrt3<0.
\]
The inequality is Cauchy–Schwarz applied to
(sigma,6) and (1/2,sqrt3/2). If H is perturbed by an arbitrary homogeneous
quartic in the ordinary35 entry monomials, coefficient-sup error epsilon
changes this restricted half-Hessian at I by operator norm at most
15epsilon (diagonal bounds10epsilon, off-diagonal bound5epsilon).
Therefore the convex-polynomial-lift obstruction persists uniformly in tau
whenever
\[
\epsilon<\frac{2(\sqrt3-1)}5.
\]
This radius certifies only the lift obstruction. It gives no ROC or PC
claim for the whole large box, and does not exclude polynomial *support
selectors*. The accepted fixed-line PC certificates do use quadratic
selectors; a polynomial selector and a convex polynomial lift are
different requirements. The stronger selector obstruction belongs to the
different exact target in `PROOF.md`.
