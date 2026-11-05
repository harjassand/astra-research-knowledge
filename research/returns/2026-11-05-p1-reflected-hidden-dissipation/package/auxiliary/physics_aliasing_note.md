# Exact thermodynamic ambiguity of a fixed sampled law

Internal research note for the parent research thread, 2026-11-05.

## Status and significance

This note contains a completed mathematical construction. The broad phenomenon of equilibrium/nonequilibrium aliasing under regular time sampling is **known**. The extension established here is an explicit, fixed, three-state transition matrix with a continuum of strictly bidirectional generator realizations, uniformly bounded jump rates, and unbounded entropy production. A literature search did not find this exact statement, but that does not establish priority. This is a useful obstruction and a possible short mathematical result, **not a civilization-changing discovery**.

## Theorem

For every observation interval \(\Delta>0\), there exists a strictly positive stochastic matrix \(P\) on three fully observed states such that:

1. \(P=e^{\Delta Q_{\rm eq}}\) for an irreducible equilibrium generator with uniform stationary law and zero entropy production.
2. There is a continuum \(Q_x\) of irreducible generators with every off-diagonal entry strictly positive, uniform stationary law, and \(e^{\Delta Q_x}=P\).
3. All exit rates of all generators in this family are bounded by the same finite constant.
4. The stationary entropy production of \(Q_x\) is unbounded over the family.

Consequently, even perfect observation of every state at arbitrarily many integer multiples of \(\Delta\) does not place a finite upper bound on dissipation in this model class. This remains true under adaptive choices of integer-multiple waiting times and arbitrary known state preparations at the observation times, as long as only state records are observed and the generator between observation times is unchanged.

## Explicit construction

Use row-vector generator convention. Define

\[
\omega=2\pi/\Delta,\qquad a>\sqrt3\,\omega,
\qquad J=\tfrac13\mathbf1\mathbf1^T,
\qquad P=J+e^{-a\Delta}(I-J).
\]

The equilibrium realization is \(Q_{\rm eq}=-a(I-J)\), with rate \(a/3\) on each directed edge.

Set

\[
x_0=-a+\frac2{\sqrt3}\sqrt{a^2+\omega^2}.
\]

The assumption on \(a\) implies \(0<x_0<a/3\). For \(x\in(x_0,a/3]\), define

\[
y=(a-x)/2,
\qquad c=\sqrt{\frac{\omega^2+(3x-a)^2/4}{3}}.
\]

Then define

\[
Q_x=\begin{pmatrix}
-(x+y)&x+c&y-c\\
x-c&-(x+y)&y+c\\
y+c&y-c&-2y
\end{pmatrix}.
\]

Every row and column sum is zero, so the stationary distribution is uniform. The clockwise edge pairs have rates \(x\pm c,y\pm c,y\pm c\).

### Positivity and rate bounds

Directly,

\[
12(x^2-c^2)=3x^2+6ax-a^2-4\omega^2.
\]

The positive root of the right side is exactly \(x_0\). Therefore \(x>c>0\) when \(x>x_0\). Since \(x\le a/3\), \(y\ge x>c\). Every directed edge rate is strictly positive. The maximum escape rate is

\[
\max(x+y,2y)=a-x<a.
\]

The equilibrium generator also has escape rate \(2a/3<a\). In particular, the divergence below is not obtained by making the jump activity arbitrarily fast.

### Same propagator

For a doubly stochastic three-state generator parameterized by symmetric edge rates \(x,y,z\) and common circulation \(c\), the two nonzero eigenvalues are

\[
-(x+y+z)\pm\sqrt{x^2+y^2+z^2-xy-yz-zx-3c^2}.
\]

Here \(z=y\), \(x+2y=a\), and the definition of \(c\) makes the square root \(i\omega\). Thus

\[
\operatorname{spec}(Q_x)=\{0,-a+i\omega,-a-i\omega\}.
\]

The plane orthogonal to \(\mathbf1\) is invariant. Its generator has minimal polynomial \((\lambda+a)^2+\omega^2\), so its exponential is

\[
e^{tQ_x}=J+e^{-at}\cos(\omega t)(I-J)
+e^{-at}\frac{\sin(\omega t)}\omega[Q_x+a(I-J)].
\]

At \(t=\Delta\), \(\omega\Delta=2\pi\), so \(e^{\Delta Q_x}=P\), independently of \(x\). The same holds at every integer multiple of \(\Delta\).

### Unbounded dissipation

For a stationary continuous-time chain, use dimensionless entropy production (Boltzmann constant set to one):

\[
\sigma(Q)=\sum_{i\ne j}\pi_iq_{ij}\log\frac{\pi_iq_{ij}}{\pi_jq_{ji}}.
\]

For the family,

\[
\sigma(Q_x)=\frac{2c}{3}\left[
\log\frac{x+c}{x-c}+2\log\frac{y+c}{y-c}\right].
\]

As \(x\downarrow x_0\), \(c\to x_0>0\), \(x-c\to0^+\), while \(y-c\to(a-3x_0)/2>0\). Therefore the first logarithm diverges and \(\sigma(Q_x)\to\infty\). Each individual family member has finite entropy production and strictly positive reverse rates.

### Why adaptive passive experiments do not help

All family members have the same kernel \(P^m\) for every allowed waiting time \(m\Delta\). Condition on any observed history. An adaptive experiment chooses the same distribution over its next state preparation, measurement and integer \(m\) under every model because the history law is the same. The next observed-state kernel is also the same. Induction gives equality of the entire experimental record law, including stopping rules and randomized adaptive schedules supported on the grid. This is an information-theoretic indistinguishability result, not a statement about a specific estimator.

## What physical resource causes the divergence?

Under local detailed balance, the edge affinity \(\log[(x+c)/(x-c)]\) diverges. A physical realization thus requires unbounded thermodynamic driving/work per relevant cycle. The theorem does **not** assert unbounded dissipation at bounded drive or bounded available energy. It establishes that a state-only stroboscopic record and an upper jump-rate bound do not determine that drive. A known bound on affinities or an independently calibrated calorimetric measurement changes the inference problem.

The family is also deliberately spectrally degenerate at the sampling interval: the two nontrivial eigenvalues of \(P\) coincide. This is not a generic identifiability theorem for arbitrary propagators. Finite measurement uncertainty nevertheless prevents experimental data alone from reliably excluding nearby degeneracies without conditioning assumptions.

## Known constructive remedy and its costs

If intervals are independent exponentials \(T\sim\mathrm{Exp}(\lambda)\), the pooled transition kernel is the resolvent

\[
R_\lambda=\mathbb E[e^{TQ}]=\lambda(\lambda I-Q)^{-1},
\qquad Q=\lambda(I-R_\lambda^{-1}).
\]

This standard identity eliminates matrix-logarithm branch ambiguity at every positive average sampling rate \(\lambda\). It is not a new result of this note. A complete practical claim must include the fact that an exponential clock permits arbitrarily short intervals; a fixed minimum sensor dead time is a different experiment. If state-reset samples are used, their preparation cost must be paid. If samples are harvested from one long stationary trajectory, rare-state visitation and correlation must be paid instead.

For the induced infinity norm and a known escape-rate bound \(r\),

\[
\|R_\lambda^{-1}\|_\infty\le1+2r/\lambda=:\kappa.
\]

If an estimate satisfies \(\|\widehat R-R\|_\infty\le\delta<1/\kappa\), inverse perturbation yields

\[
\|\widehat Q-Q\|_\infty
\le\frac{\lambda\kappa^2\delta}{1-\kappa\delta}.
\]

Thus no aliasing does not imply cheap inference. Moreover entropy production is not uniformly continuous as a reverse rate tends to zero, so a finite generator norm error alone does not certify a finite upper entropy-production error without a lower bound on positive rates or affinities.

## Numerical verification executed

For \(\Delta=1,\omega=2\pi,a=12\), \(x_0\approx3.640904390064641\). A NumPy/SciPy calculation gave:

| \(x-x_0\) | Smallest directed rate | Maximum exit rate | Entropy production | Maximum entrywise \(|e^Q-P|\) |
|---:|---:|---:|---:|---:|
| \(10^{-1}\) | 0.1063727234 | 8.2590956099 | 23.6106609732 | \(4.44\times10^{-16}\) |
| \(10^{-3}\) | 0.0010738689 | 8.3580956099 | 34.4041923595 | \(2.78\times10^{-16}\) |
| \(10^{-6}\) | \(1.0739710\times10^{-6}\) | 8.3590946099 | 51.1678521213 | \(2.22\times10^{-16}\) |
| \(10^{-9}\) | \(1.0739751\times10^{-9}\) | 8.3590956089 | 67.9348243892 | \(3.89\times10^{-16}\) |

The proof, rather than these numerical values, establishes exact equality and divergence.

## Primary literature and novelty boundary

1. Malena T. Bauer, Udo Seifert, Jann van der Meer, *Stroboscopic measurements in Markov networks: Exact generator reconstruction vs. thermodynamic inference*, J. Phys. A 58, 125001 (2025), [arXiv:2412.15642](https://arxiv.org/abs/2412.15642), [full text](https://arxiv.org/html/2412.15642v2). Section 3.2.2 explicitly gives an equilibrium and a driven three-state generator with the same sampled law; Section 3.3 discusses uncountably many logarithms for degenerate propagators but restricts its complete entropy bounds to the generic finite-candidate case. The construction in this note must not be described as the first discovery of thermodynamic aliasing.
2. J. Blanchet, P. W. Glynn, K. Leder, *On Lyapunov Inequalities and Subsolutions for Efficient Importance Sampling*, ACM TOMACS 22(3), Article 13 (2012), [author page](https://web.stanford.edu/~glynn/papers/2012/BlanchetGLeder12.html). This already establishes local Lyapunov verification of relative-variance guarantees; a proposed residual-certificate rare-event breakthrough was rejected as largely a rediscovery.
3. Xiaoou Cheng, Jonathan Weare, *The surprising efficiency of temporal difference learning for rare event prediction*, NeurIPS 2024, [proceedings](https://proceedings.neurips.cc/paper_files/paper/2024/hash/94205e76ba4a5077ad0fac02b17bd46f-Abstract-Conference.html), [arXiv:2405.17638](https://arxiv.org/abs/2405.17638). This already proves polynomial observed-transition cost for relative accuracy on some exponentially rare finite-state events from short trajectories. The cost of physically obtaining the starting states is a separate access premise, but unknown-kernel rare-event prediction itself is not a new opening without further work.
4. Carsten Hartmann, Annika Jöster, *Risk-neutral limit of adaptive importance sampling of random stopping times* (2024), [arXiv:2402.08476](https://arxiv.org/abs/2402.08476), and Hartmann et al., *Importance sampling of unbounded random stopping times: computing committor functions and exit rates without reweighting* (2026), [arXiv:2601.01489](https://arxiv.org/abs/2601.01489). These directly warn that variance minimization can hide infinitely long trajectories and pursue joint variance/duration control.

