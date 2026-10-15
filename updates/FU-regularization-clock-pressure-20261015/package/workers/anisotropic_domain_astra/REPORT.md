# Arbitrary convex moment domains are attainable

The anisotropic extension holds for every open convex \(D\subset\mathbb R^m\) containing zero. No smoothness, strict convexity, boundedness, symmetry, or absence of lines is required of \(D\).

For a compact distribution \(T\) taking values in a real Banach space ordered by a proper closed cone \(C\) with nonempty interior, normalized by \(T(1)\in\operatorname{int}C\), the following are equivalent:

1. \(H_T(g)\in\operatorname{int}C\) for every \(g\in D\).
2. A scalar probability noise with finite moments throughout \(D\) makes \(T*\nu\) positive.
3. A scalar everywhere positive smooth strictly log-concave probability density \(p\), with **exact full finite-MGF domain \(D\)**, makes \(T*p\) positive.

The density can satisfy the arbitrary relative cone sandwich from PR94. Every derivative of the noise and output is integrable against \(e^{g\cdot x}\) for every \(g\in D\). Its potential has positive-definite Hessian everywhere and gradient range exactly \(D\).

The complete argument is in [PROOF.md](PROOF.md). Its central geometric lemma is stronger than the application: for any positive continuous tolerance \(\tau(g)\), any finite derivative order \(K\), and any fixed physical radius \(R\), one can arrange
\[
\max_{2\le|\alpha|\le K}\sup_{|y-x|\le R}|\partial^\alpha V(y)|
\le\tau(\nabla V(x)),
\quad \nabla V(\mathbb R^m)=D,
\quad \mathcal D(e^{-V})=D.
\]

The construction has four material parts.

- An integral over the compact polar, using its **relative dimension**, gives a smooth strongly convex exhaustion of \(D\). This handles corners, unbounded domains, and lineality.
- A convex increasing scalar composition makes the dual Hessian dominate any prescribed continuous lower bound. Conjugation then makes the primal Hessian as small as required in gradient coordinates.
- A globally Lipschitz positive minorant of \(\tau\) controls transport of the tolerance through a fixed physical neighborhood. Convolution of the **potential** with a fixed compact even mollifier transfers the small second derivative to every required higher derivative.
- The global Hessian cap makes this convolution a bounded perturbation of the potential. Exact moment-domain preservation follows, including divergence at every boundary point. A finite integral of an exponential of a finite convex function forces a linear coercivity bound; this rules out an inadvertently finite boundary moment.

Necessity uses the PR94 Banach-cone cutoff argument at \(g\), without using \(-g\). An explicit check is
\[
T=\delta-\delta',\qquad p(x)=e^{x-e^x},\qquad
\mathcal D(p)=(-1,\infty),\qquad T*p=e^xp>0.
\]
Thus the theorem includes genuinely one-sided domains even when the Laplace symbol becomes negative outside the chosen domain.

Status is **internally proved candidate**, not independently reviewed or formally verified. Classical convex-barrier and Legendre-function existence is prior work; the primary Borwein–Vanderwerff paper is saved and cited. Historical priority for the combined regularization theorem remains unknown. The proof is qualitative, requires the positivity-margin profile and domain geometry, and establishes no efficient sampler, variance optimum, or physical acquisition advantage.

Only this worker directory was written. The frozen PR94 proof was read and copied here; the worktree and GitHub were not modified.
