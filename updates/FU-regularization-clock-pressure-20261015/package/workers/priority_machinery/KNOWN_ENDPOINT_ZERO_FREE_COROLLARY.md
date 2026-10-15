# A stronger consequence of the inspected continuous scalar predecessor

Status: elementary corollary of the acquired Katkova-Vishnyakova 2001 theorem, not an originality claim. It removes two superficial differences from an earlier comparison. It does not remove the theorem's endpoint-sign assumptions, one-dimensional scope, or the new draft's strict log-concavity requirement.

Let \(T\) be a real compactly supported integrable function of mass one satisfying the endpoint-sign and continuity assumptions of Katkova-Vishnyakova Theorem 1 after translation to the positive half-line, and suppose its bilateral Laplace transform is strictly positive on the real axis. Their conclusion, after normalization, supplies \(\varepsilon,\lambda>0\) such that

\[
T*\nu\ge0,\qquad
\nu=\operatorname{Law}(\varepsilon N),\quad N\sim\operatorname{Poisson}(\lambda).
\]

Let \(\widetilde\nu\) be the reflected law and \(G_\sigma\) a centered nondegenerate Gaussian. Then

\[
p=\nu*\widetilde\nu*G_\sigma
\]

is a symmetric (hence one-dimensional radial), smooth, strictly positive probability density, with all exponential moments and exponentially weighted integrability of all absolute derivatives. Positivity is preserved by further convolution:

\[
T*p=(T*\nu)*\widetilde\nu*G_\sigma>0
\quad\text{everywhere}.
\]

Strict output positivity follows because the nonzero positive measure \(T*\nu\) is convolved with a strictly positive Gaussian. Derivative integrability follows from the Gaussian derivative bounds and the all-exponential moments of the Poisson laws.

Moreover,

\[
\widehat p(t)=\exp\!\left[-\frac{\sigma^2t^2}{2}
 +2\lambda(\cos(\varepsilon t)-1)\right]>0
\quad(t\in\mathbb R).
\]

Thus a zero-free characteristic function is available in this known scalar endpoint class. Its reciprocal still grows at least as fast as the inverse Gaussian factor, so this gives no stable finite-sample inversion guarantee.

Consequently, describing the original predecessor's multiplier as one-sided, atomic, or nonradial does not by itself distinguish an existential one-dimensional theorem asking only for smooth radial all-exponential regularization. Reflection and Gaussian postconvolution remove those features. Strict log-concavity and the general compact-distribution/operator-valued scope remain substantive differences; they are not established by this corollary.

Primary source: [O. M. Katkova and A. M. Vishnyakova, Positivity 5 (2001), 1-11](https://doi.org/10.1023/A:1009847605313). Acquired institutional PDF: [source](sources/katkova_vishnyakova_2001.pdf), SHA-256 `f24e4260a54627f5ad68e0bfdba4c13bdf82e2d327453222a8cede43999b8925`; Theorem 1, PDF pp. 1-2; convolution interpretation, PDF p. 2.
