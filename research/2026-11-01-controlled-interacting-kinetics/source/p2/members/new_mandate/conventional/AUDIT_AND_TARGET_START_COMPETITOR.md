# Independent audit and stronger conventional competitor

## Decision

The Gaussian reference, parity convention, normalization, spectral gap and first quartic Wick insertion pass the independent checks below. However, rarity-independent computation of the demonstrated equilibrium-source mean is already supplied by ordinary target-start relaxation trajectories when the same stationary target weight and gap bound are available. That is a successful whole-function competitor, not merely an objection to a scaling headline.

The remaining possible distinction is controlled computation through large **kinetic stiffness**, with a compact interacting Gaussian reference and local non-Gaussian perturbation. This audit does not establish a new complexity separation or priority for that distinction. Conventional averaging, exact local elimination and low-rank methods must be judged on the same acquired information.

## Independent physical audit

`audit_gaussian_reference.py` derives the reference generator from physical spin energy differences,

\[
H(\sigma)=-\sum_iJ_i\sigma_i\sigma_{i+1},\qquad
w_j(\sigma)=\frac{\nu_{j-1}}{1+\exp[H(\sigma^j)-H(\sigma)]},
\]

then quotients by global spin reversal to domain walls. It does **not** call the root's dense generator. The target is the no-wall configuration: both globally aligned spin configurations in the unquotiented system. It is not one chosen spin orientation.

Four cases include antiferromagnetic couplings, mixed signs, unequal attempt rates and a target weight \(3.5287\times10^{-11}\). Against the independently formed generator:

- Maximum mean relative error after the complementary-rate repair and rerun: \(2.47\times10^{-14}\).
- Maximum gap relative error: \(8.40\times10^{-14}\).
- Every Nambu two-operator contraction also agrees with explicit full Fock matrices at four unequal time pairs, maximum absolute error \(7.89\times10^{-15}\) in the rerun.
- The first non-Gaussian insertion integral for the four-site antiferromagnetic example is \(0.0127716403278992\) by the dense inverse. Gaussian quadrature gives relative error \(3.04\times10^{-7}\) at 32×8 nodes and \(9.07\times10^{-11}\) at 64×16 nodes.

For the demonstrated uniform \(J=-0.4\) reference, the Bogoliubov chart condition numbers at 128 and 256 sites are 181.3 and 362.7. The logarithmic Gaussian-versus-Gibbs normalization discrepancies are both \(5.69\times10^{-14}\) or smaller in the complementary-rate rerun. The determinant representation tends to the analytically supplied stationary weight at long time without evaluating growing exponentials. Earlier numerical values are retained in the investigation's intermediate records.

These are floating-point checks. They do not establish interval bounds, generic chart conditioning, uniform bit complexity, arbitrary Fock preparations, competing targets or a completed finite-reactive-boundary solver. The high-order inverse expansion in the root code is verified densely at small size; its full compact all-order implementation is a separate construction.

## Conventional target-start occupation estimator

Let a finite irreducible reversible continuous-time chain have stationary target weight \(\pi=\pi_b\), and let \(0<g\le\lambda_j\le\Lambda\) bound its nonzero relaxation spectrum. These are acquired model quantities here: the bounded spectator perturbation preserves the known one-dimensional Gibbs law and dominates the reference Dirichlet form.

Write

\[
R(t)=P_b(X_t=b),\qquad
W=\int_0^\infty[R(t)-\pi]dt.
\]

The existing return-kernel identity gives the exact equilibrium-outside mean

\[
\mathbb E_{\pi(\cdot\mid\neg b)}\tau_b
=\frac{W}{\pi(1-\pi)}.
\]

Positive spectral weights imply

\[
\frac{1-\pi}{\Lambda}\le W\le\frac{1-\pi}{g},\qquad
0\le W-W_T\le\frac{1-\pi}{g}e^{-gT}.
\]

Start an ordinary microscopic trajectory **at the target**, run it only to \(T\), and record

\[
L_T=\int_0^T\mathbf1_{\{X_t=b\}}dt.
\]

Then \(\mathbb E L_T=W_T+\pi T\). Nothing in this procedure waits for the equilibrium rare arrival.

The Markov property gives a useful variance bound directly:

\[
\mathbb E L_T^2
=2\int_{u,v\ge0;\ u+v\le T}R(u)R(v)\,du\,dv
\le2(\mathbb E L_T)^2,
\]

so \(\operatorname{Var}L_T\le(\mathbb E L_T)^2\). For \(N\) independent paths, define \(\widehat W=N^{-1}\sum L_T-\pi T\), and set

\[
r_{\max}=\frac{\pi T\Lambda}{1-\pi},\qquad
b_T=\frac{\Lambda}{g}e^{-gT},\qquad
e_N=\frac{1+r_{\max}}{\sqrt{N\alpha}}+b_T.
\]

Chebyshev's inequality and the tail bound prove

\[
\Pr\{|\widehat W-W|\le e_N W\}\ge1-\alpha.
\]

If \(e_N<1\), this yields the directly computable confidence interval

\[
\frac{\widehat W}{(1+e_N)\pi(1-\pi)}
\le\mathbb E_{\pi\mid\neg b}\tau_b
\le\frac{\widehat W}{(1-e_N)\pi(1-\pi)}.
\]

In the rare-target regime \(r_{\max}\ll1\), the sample count for fixed relative precision and confidence is independent of \(1/\pi\). Median-of-means can improve confidence dependence from \(1/\alpha\) to \(\log(1/\alpha)\). The conventional cost still contains the number of physical transitions through a mixing-scale horizon, generally \(\Lambda/g\) up to logarithms.

## Executed nonintegrable competitor

`target_start_occupation.py` performs exact uniformization on the root's actual spectator-dependent rate model with multiplier \(1+0.7n_{i+2}\). It uses no Gaussian propagation to sample the paths. The only supplied analytic quantities are the shared stationary target weight and reference gap lower bound.

At 256 sites, 1,024 paths of duration 19.9114 used 8,873,513 microscopic proposals and 4.76 seconds in this environment. The target weight is \(1.25538\times10^{-130}\). The estimated equilibrium-outside mean is \(3.65980\times10^{127}\), with the stated 95% confidence interval

\[
[3.20542,4.26428]\times10^{127}.
\]

The exact confidence derivation above is separate from the floating-point evaluation of its parameters; this is not an interval-arithmetic certificate. The example nevertheless demonstrates the complete conventional estimation service for the actual nonintegrable dynamics and its resource count. It is stronger than comparing only against equilibrium rare-event waiting or brute-force full-state diagonalization.

## Stiffness and stronger conventional alternatives

The current homogeneous even-wall reference is not exponentially stiff in system size or coupling. Its gap is

\[
g=2\nu[1-|\tanh(2J)|\cos(\pi/n)]
\ge2\nu[1-\cos(\pi/n)],
\]

so \(\Lambda/g=O(n^3)\). Removing global spin orientation removed the exponentially slow spin-reversal mode. These examples demonstrate compact rare-target arithmetic but do not establish a stiffness separation.

For explicit slow/fast local attempt rates, an equally informed competitor first writes \(Q=Q_{\rm fast}+\varepsilon Q_{\rm slow}\), conditions on the slow spins, and averages slow transition rates over the exact conditional Ising Gibbs law. One-dimensional transfer matrices supply those stationary conditional weights. Fast-block gaps control averaging error. Target occupation needs both the initial fast layer and slow conditional-target occupancy; simply replacing the whole target by a coarse state would be wrong. This offers a constructive conventional route for simple separated instances, though not a complete uniform algorithm for every admitted reference and perturbation.

Existing exact graph transformation avoids dynamical stiffness once the relevant network is represented, but its state/fill cost is not automatically polynomial in physical sites. Tensor-train/MPS solvers likewise address stiffness and inverse problems, but their cost depends on retained tensor ranks. No tensor-rank lower bound has been demonstrated for the root's class, so this audit makes no assertion that those methods fail.

Primary governing sources for those comparisons:

- Novotny, *Monte Carlo with Absorbing Markov Chains: Fast Local Algorithms for Slow Dynamics* (1994), https://arxiv.org/abs/cond-mat/9411081 — exact recurring-local-state elimination, extending the n-fold way.
- Bobbio and Trivedi, *Aggregation Technique for the Transient Analysis of Stiff Markov Chains* (1986), https://scholars.duke.edu/publication/687944 — explicit fast recurrent/transient subsets and conditions for asymptotic accuracy.
- Yin and Zhang, *Continuous-Time Markov Chains and Applications: A Singular Perturbation Approach*, https://doi.org/10.1007/978-1-4612-0627-9 — fast-group averaging, expansions and error conditions.
- *Low-rank tensor methods for Markov chains with applications to tumor progression models*, https://doi.org/10.1007/s00285-022-01846-9 — Neumann/uniformization tensor algorithms; low-rank structure is an explicit condition, not an automatic consequence of local rates.
- Sharpe and Wales, https://doi.org/10.1103/PhysRevE.104.015301 — exact stable graph transformation for finite represented networks.

The return-kernel and finite-defect prior is preserved separately in `RETURN_KERNEL_COMPETITOR.md` and `GAUSSIAN_RECORD_ROUTE.md`. No priority or civilisation-scale consequence follows from this audit alone.
