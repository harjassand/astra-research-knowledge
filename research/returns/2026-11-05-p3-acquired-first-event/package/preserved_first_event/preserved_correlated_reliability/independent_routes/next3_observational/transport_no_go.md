# Finite observation cannot universally certify macroscopic equilibrium transport

## Status and original endpoint

The chosen question was whether finite equilibrium current observations can certify a material's macroscopic Green–Kubo transport coefficient, including the contribution of unobserved slow modes, without a separately supplied relaxation bound. The intended consequence was reliable transport prediction for materials and energy systems from finite simulation or measurement records.

The indispensable operation is **an upper certificate for the unobserved correlation tail**. This route refutes a universal version of that operation under passive current-only access. It does not deliver a new universal transport predictor. The result below is an exact two-dimensional, stable, passive, reversible counterexample, followed by a finite-observation and adaptive-stopping impossibility theorem. Historical novelty is not established.

The empirical motivation is the persistent sensitivity of computed transport to trajectory duration and long wavelength modes. Xu et al. measured length-dependent thermal conductivity in suspended graphene and reported logarithmic growth over their tested lengths [1]. This does not establish divergence at all lengths, and the model below is not asserted to explain graphene. It isolates a logically distinct obstacle: a small, unresolved slow mode can carry a large integrated transport contribution.

## 1. Exact mathematical and access premises

We work in dimensionless units with thermal energy and a reference fast relaxation rate set to one. Consider a stationary two-dimensional Ornstein–Uhlenbeck process

\[
dZ_t=-Q_\lambda\Sigma_\rho^{-1}Z_t\,dt+\sqrt{2Q_\lambda}\,dW_t,
\qquad Z_0\sim N(0,\Sigma_\rho),
\]

where

\[
\Sigma_\rho=\begin{pmatrix}1&\rho\\\rho&1\end{pmatrix},
\qquad Q_\lambda=\operatorname{diag}(1,\lambda),
\qquad 0<\lambda\le1,\quad |\rho|<1.
\]

The observer sees only the scalar stationary current \(J_t=Z_{t,1}\). We grant noiseless continuous observation, arbitrarily accurate arithmetic, unlimited postprocessing, and any fixed finite number \(m\) of independent exact equilibrium starts. Let the sum of the observed run lengths be \(B\). The observer does not receive the hidden coordinate, the generator parameters, or an independently certified lower bound on the slow relaxation rate.

The target is

\[
K=\int_0^\infty C(t)\,dt,
\qquad C(t)=E[J_tJ_0].
\]

A physical Green–Kubo prefactor can be restored afterward. Its presence does not change the statistical argument.

These are explicit access restrictions. If the exact generator is known, the two-dimensional target can be calculated by a matrix inverse. Many molecular simulations have a known microscopic generator; the theorem therefore applies directly to passive postprocessing of a finite current record, not to every computational method available to someone who knows the entire molecular model.

## 2. The process is passive, reversible, stable, and ergodic

Set \(A=Q_\lambda\Sigma_\rho^{-1}\). The matrix \(\Sigma_\rho\) is positive definite and \(Q_\lambda\) is positive definite. Also

\[
A\Sigma_\rho=Q_\lambda=\Sigma_\rho A^T.
\]

Consequently \(N(0,\Sigma_\rho)\) is invariant and the process satisfies detailed balance. Stability follows because \(A\) is similar to the symmetric positive definite matrix \(Q_\lambda^{1/2}\Sigma_\rho^{-1}Q_\lambda^{1/2}\). All its eigenvalues are strictly positive.

The energy is \(H(z)=\tfrac12z^T\Sigma_\rho^{-1}z\), the mobility is \(Q_\lambda\), and the noise obeys fluctuation–dissipation. The deterministic drift dissipates energy:

\[
\frac{dH}{dt}=-(\nabla H)^TQ_\lambda\nabla H\le0.
\]

No active gain, negative damping, nonstationarity, or truly nonergodic mode is used. Every member has a finite transport coefficient.

The observed equal-time variance and quadratic variation are identical throughout the family:

\[
E[J_t^2]=1,\qquad [J]_t=2t,\qquad C'(0+)=-1.
\]

Fixing the quadratic variation matters: otherwise perfect continuous observations could distinguish different noise amplitudes immediately.

## 3. An arbitrarily large coefficient hidden in an arbitrarily small correlation component

For \(t\ge0\),

\[
C(t)=e_1^Te^{-At}\Sigma_\rho e_1.
\]

Integrating the matrix exponential gives the exact identity

\[
\begin{aligned}
K&=e_1^TA^{-1}\Sigma_\rho e_1\\
 &=e_1^T\Sigma_\rho Q_\lambda^{-1}\Sigma_\rho e_1\\
 &=1+\frac{\rho^2}{\lambda}.
\end{aligned}                                                   \tag{1}
\]

At \(\rho=0\), the observed process is the unit OU process, with \(C_0(t)=e^{-|t|}\) and \(K_0=1\), independently of the unobserved \(\lambda\).

For any prescribed \(M>1\), choose

\[
\lambda=\frac{\rho^2}{M-1}.
\]

Taking \(\rho\) sufficiently small ensures \(\lambda\le1\), while (1) gives \(K=M\).

The two decay rates are

\[
r_\pm=\frac{1+\lambda\pm\sqrt{(1-\lambda)^2+4\lambda\rho^2}}
                  {2(1-\rho^2)}.
\]

For nonzero \(\rho\), \(0<r_-<1<r_+\). The correlation is the positive mixture

\[
C(t)=w_+e^{-r_+t}+w_-e^{-r_-t},
\quad
w_- =\frac{r_+-1}{r_+-r_-},\quad w_+=1-w_-.
\]

The weights obey \(w_++w_-=1\) and \(w_+r_++w_-r_-=1\). As \(\lambda\to0\) at small fixed \(\rho\), the slow weight is approximately \(\rho^2\), its rate approximately \(\lambda\), and its integral approximately \(\rho^2/\lambda\). The issue is the unresolved area under a narrow low-frequency component, not an unusually large instantaneous variance.

## 4. Complete finite-time trajectories can be statistically indistinguishable

Write \(u=\rho^2\). Compare the full two-coordinate path law of \((\rho,\lambda)\) with that of \((0,\lambda)\), using the same diffusion matrix. Their stationary initial distributions have relative entropy

\[
D_{\rm KL}\big(N(0,\Sigma_\rho)\,\|\,N(0,I)\big)
=-\tfrac12\log(1-u).
\]

For the dynamic part, the same-diffusion Gaussian change-of-drift formula gives

\[
\frac14\int_0^T E\!
\left[(b_\rho(Z_t)-b_0(Z_t))^TQ_\lambda^{-1}
(b_\rho(Z_t)-b_0(Z_t))\right]dt.
\]

Here \(b_\rho-b_0=-Q_\lambda(\Sigma_\rho^{-1}-I)z\). Stationarity and a trace calculation yield

\[
\begin{aligned}
E[(b_\rho-b_0)^TQ_\lambda^{-1}(b_\rho-b_0)]
 &=\operatorname{tr}\{Q_\lambda(\Sigma_\rho^{-1}-2I+\Sigma_\rho)\}\\
 &=\frac{(1+\lambda)u}{1-u}.
\end{aligned}
\]

Nondegenerate linear diffusions with these same diffusion coefficients have equivalent finite-horizon path laws; the formula can be justified by localized change of drift and the Gaussian linear-process likelihood. It does not require assuming an unverified global Novikov condition for an arbitrarily long time interval.

For \(m\) independent runs with total length \(B\), entropy adds:

\[
D_{\rm KL}^{\rm full}
=-\frac m2\log(1-u)+\frac{B(1+\lambda)u}{4(1-u)}.       \tag{2}
\]

Projection onto the current cannot increase relative entropy. Pinsker's inequality therefore gives

\[
\|P_{\rho,\lambda}^{J}-P_0^{J}\|_{\rm TV}
\le\sqrt{\frac12D_{\rm KL}^{\rm full}}.                \tag{3}
\]

When \(u\le1/2\) and \(\lambda\le1\), a convenient coarse bound is

\[
D_{\rm KL}^{\rm full}\le(m+B)u.
\]

The scalar reference law \(P_0^J\) does not depend on \(\lambda\). Thus, for every finite observation design, every target \(M>1\), and every \(\eta>0\), a strictly ergodic alternative with \(K=M\) lies within \(\eta\) TV of the same unit-OU reference observation law.

A common measurement-noise channel, finite sampling rate, lossy recording, randomized estimator, or finite memory can only decrease distinguishability. Equations (2)–(3) already grant the strongest passive observation in this scalar interface.

## 5. Uniform upper-confidence bounds must be infinite

**Theorem 1.** Let \(U\in[0,\infty]\) be any function of a fixed finite set of current trajectories and independent algorithm randomness. Suppose, uniformly over the class above,

\[
P_\theta(K_\theta\le U)\ge1-\alpha.
\]

Then under the unit-OU observed reference law,

\[
P_0(U=\infty)\ge1-\alpha.                              \tag{4}
\]

**Proof.** For any \(M>1\) and \(\eta>0\), choose an alternative with \(K=M\) whose observed law is within \(\eta\) TV of \(P_0\). Coverage implies

\[
P_0(U\ge M)\ge P_\theta(U\ge M)-\eta\ge1-\alpha-\eta.
\]

The alternative can depend on \(M,\eta\), but the reference scalar law remains fixed. Taking \(M\to\infty\), then \(\eta\downarrow0\), proves (4). \(\square\)

This is a uniform finite-sample statement. It does not contradict consistency as trajectory length tends to infinity for each fixed, sufficiently mixing process. A method can perform well on a useful restricted material class while failing the universal guarantee ruled out here.

For estimation rather than upper certification, the same construction gives a two-point lower bound. If two transport values have disjoint desired accuracy intervals, any estimator meeting those intervals would define a test. The maximum of the two test errors is at least \((1-\mathrm{TV})/2\). Arbitrarily large coefficient separation and arbitrarily poor finite-time discrimination coexist.

## 6. Adaptive stopping cannot create a missing relaxation certificate

**Theorem 2.** Let \(\tau\) be a stopping time for one continuously observed current trajectory and independent algorithm randomness. At a finite stopping time the method announces \(U_\tau\in[0,\infty]\). Assume uniformly

\[
P_\theta(\tau<\infty,\ U_\tau<K_\theta)\le\alpha.
\]

Then

\[
P_0(\tau<\infty,\ U_\tau<\infty)\le\alpha.             \tag{5}
\]

**Proof.** If the left-hand probability were greater than \(\alpha\), continuity from below would provide finite \(T,M\) and \(\eta>0\) such that

\[
P_0(\tau\le T,\ U_\tau<M)>\alpha+\eta.
\]

This event is measurable using only the finite observed path up to \(T\). Choose an alternative with \(K=M\) and path-TV distance less than \(\eta\). Under that alternative, the event has probability greater than \(\alpha\), but on it the announced bound is too small. This contradicts the assumed guarantee. \(\square\)

The theorem covers termination rules based on apparent plateaus, fitted correlation times, spectral residuals, cross-validation, or confidence stabilization whenever the only data are the passive current trajectory. It does not forbid stopping with infinite bounds, nonuniform guarantees, or external model constraints.

## 7. The coefficient is a genuine equilibrium diffusion and response coefficient

The integral need not be viewed as an abstract correlation functional. Define momentum \(p=\Sigma_\rho^{-1}z\), kinetic energy \(H(p)=\tfrac12p^T\Sigma_\rho p\), and positive definite friction

\[
\Gamma=\Sigma_\rho^{-1}Q_\lambda\Sigma_\rho^{-1}.
\]

Consider the passive Langevin free-particle system

\[
dp=-\Gamma\Sigma_\rho p\,dt+\sqrt{2\Gamma}\,dW,
\qquad dq=\Sigma_\rho p\,dt.
\]

The velocity \(z=\Sigma_\rho p\) has precisely the OU law above, since its noise covariance is \(2Q_\lambda\). Position may be taken on a torus to have a stationary uniform position distribution; transport uses its unwrapped displacement.

For the first coordinate,

\[
\operatorname{Var}(q_1(t)-q_1(0))
=2\int_0^t(t-s)C(s)\,ds,
\]

so its long-time diffusion coefficient is \(K\). Adding a constant force \(F e_1\) in the momentum equation gives steady mean current \(E[J]=FK\). The hidden slow component therefore controls both equilibrium diffusion and zero-frequency mobility.

This realization uses a thermal bath and a coupled kinetic energy. We have not embedded it into an isolated energy-conserving local many-body Hamiltonian with fixed material parameters. That stronger physical claim would require an additional construction.

## 8. A conditional tail certificate, and the premise it requires

Suppose independently that the relevant generator is reversible and self-adjoint, and the spectral measure \(\mu\) for the centered observable is supported on \([g,\infty)\), with a certified \(g>0\). Then

\[
C(t)=\int_g^\infty e^{-rt}\,\mu(dr),\qquad
R_T=\int_0^T C(t)\,dt.
\]

With \(C(T)>0\) and finite \(-C'(T)\),

\[
\boxed{
\frac{C(T)^2}{-C'(T)}\le K-R_T\le\frac{C(T)}g.
}                                                               \tag{6}
\]

To prove the upper bound, use \(1/r\le1/g\) in
\(K-R_T=\int e^{-rT}\mu(dr)/r\). For the lower bound, apply Cauchy–Schwarz to \(r^{-1/2}\) and \(r^{1/2}\) under the tilted measure \(e^{-rT}\mu(dr)\). A single remaining relaxation rate makes both bounds sharp when that rate equals \(g\). If the residual correlation measure is zero, the tail is zero; the ratio in (6) is then interpreted separately rather than as \(0/0\).

If jointly valid estimates give an upper bound for \(R_T\) and for \(C(T)\), the right side yields a computable confidence bound. The gap is an external premise. Theorems 1–2 show why its positive universal value cannot itself be certified from the same finite passive data over the unrestricted OU class.

Equation (6) assumes a positive exponential spectral representation. It is not automatically valid for an oscillatory current correlation generated by an arbitrary non-self-adjoint, inertial, or Hamiltonian evolution. It is a restricted conditional result, not a replacement endpoint.

## 9. Actual numerical witness and resource bills

The script `verify_transport.py` checks the covariance, stability, diffusion coefficient, path KL formula, finite sampled-path Gaussian KL, and conditional tail inequality by matrix calculations. No Monte Carlo success is being substituted for a proof.

Use \(\rho=0.01\), \(\lambda=10^{-4}/999\), one run of length \(T=100\). Then:

| Quantity | Value |
|---|---:|
| Reference transport | 1 |
| Alternative transport | 1000 |
| Both observed variances | 1 |
| Both observed quadratic-variation rates | 2 |
| Slow correlation weight | approximately 0.00010000002 |
| Slow relaxation time | approximately 9,990,000 |
| Largest covariance difference over the tested interval | below 0.0001000000 |
| Full two-coordinate finite-path KL | 0.00255025 |
| Scalar continuous-path TV upper bound | 0.0357089 |
| Lower bound on maximum testing error | 0.482146 |
| Scalar 101-sample Gaussian KL | 0.00000532291 |
| Correlation integral through time 100 | 1.00979996 |
| Remaining true correlation integral | 998.99020004 |

The exact stationary starts were granted for free in the theorem. Ordinary physical equilibration of the slow mode may itself require a time of order \(1/\lambda\). Granting equilibrium initialization therefore strengthens the obstruction. The family uses tiny coupling and a very slow hidden relaxation, not large state dimension. If rates are rationally specified, making \(\lambda\) exponentially small in its bit length costs only polynomial description length but requires exponentially long physical observation.

There is no finite passive observation bill that guarantees a useful universal upper certificate. Additional memory, computation, and lower sensor noise cannot repair the information deficit. Full generator access, a proved relaxation gap, or a controlled perturbation that exposes the slow variable changes the experiment and must be priced separately.

## 10. Primary comparators and what the theorem does to them

**Cepstral spectral estimation.** Ercole, Marcolongo, and Baroni [2] estimate the zero-frequency spectrum from equilibrium current records and report accurate transport estimates on several simulated liquids and solids. Their construction uses smoothness of the log spectrum to truncate its cepstral representation. This is a strong same-access comparator. Our arbitrarily narrow low-frequency component makes a uniform finite-sample smoothness or truncation guarantee unavailable without a class constraint. It does not refute their pointwise consistency or empirical accuracy.

**STACIE.** Toraman, Fauconnier, and Verstraelen [3] use low-frequency spectral fitting, locally weighted Bayesian regression, and automatic frequency-window selection, with uncertainty estimates and extensive synthetic benchmarks. Their paper explicitly identifies the need to capture slow modes and the difficulty of determining an adequate trajectory length. This is the most directly relevant modern same-access comparator inspected. Our theorem strengthens that caveat into an exact uniform impossibility statement for a passive reversible class. STACIE does not claim the universal guarantee being refuted.

**Transient subtraction.** Monmarché, Spacek, and Stoltz [4] construct transport control variates using perturbed initial ensembles and synchronously coupled trajectories. That is stronger access than a fixed passive current record. Our theorem does not lower-bound that entire method. Its comparison is useful precisely because intervention and coupling are ways to change the information interface, while remaining relaxation assumptions and computational costs still matter.

These comparisons do not establish historical priority for the mathematical obstruction. A literature search for prior general impossibility theorems would be needed before any novelty claim. Nor do they establish that the counterexample describes a particular real material.

## Conclusion for route selection

The original universal finite-observation transport-certification endpoint is invalid under the stated access. The earned result is a compact physical counterexample, exact finite-time information bound, fixed-window and adaptive-stopping confidence impossibility, and a sharp conditional tail bracket when a genuine spectral floor is supplied. This is a useful boundary theorem. It should not be presented as a civilization-changing constructive prediction capability.

## Sources

1. X. Xu et al., *Length-dependent thermal conductivity in suspended single-layer graphene*, Nature Communications **5**, 3689 (2014). https://doi.org/10.1038/ncomms4689 . Primary experimental and simulation observation; its measured range is not extrapolated into an infinite-length claim.
2. L. Ercole, A. Marcolongo, and S. Baroni, *Accurate thermal conductivities from optimally short molecular dynamics simulations*, Scientific Reports **7**, 15835 (2017). https://doi.org/10.1038/s41598-017-15843-2 ; https://arxiv.org/abs/1706.01381 .
3. Toraman, Fauconnier, and Verstraelen, *STACIE: STable AutoCorrelation Integral Estimator: Robust and Accurate Transport Properties from Molecular Dynamics Simulations*, Journal of Chemical Information and Modeling **65**, 10445–10464 (2025). https://doi.org/10.1021/acs.jcim.5c01475 ; https://pmc.ncbi.nlm.nih.gov/articles/PMC12529779/ . Full primary article inspected.
4. P. Monmarché, M. Spacek, and G. Stoltz, *Transient subtraction: A control variate method for computing transport coefficients* (2024 preprint). https://arxiv.org/abs/2410.00212 ; https://arxiv.org/html/2410.00212v2 . Full primary preprint inspected.

## Reproduction

From the workspace root, run `python next3_observational/verify_transport.py`. The generated JSON contains the numerical checks; the PNG and PDF show the correlation and integrated transport contrast. Floating-point agreement illustrates the exact formulas and is not a substitute for them.
