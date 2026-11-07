# Independent constructor initial report — 7 November 2026

Status: **proved conditional mathematical construction; no new foundational mechanism or physical advantage established**. This file is frozen before reading the other initial reports. Supporting follow-ups belong in `../constructor/`, not by rewriting this file.

## Independence boundary

Before receiving any principal-result description I had formulated the construction below: acquire a bounded Lipschitz pair force from repeated noisy short two-particle releases, retain the force table and a one-body probability field, derive its nonlinear McKean–Vlasov evolution by synchronous coupling, and use an explicit finite-grid nonlinear Markov update to compute it for every new preparation and prescribed bounded Lipschitz drive. My pre-exchange investigation also independently located the nonlinear gradient-exclusion route and Funaki–Gu–Wang's quantitative nongradient hydrodynamics.

The principal sent a short description of its own construction before this report was written to disk, then immediately identified the exposure. I have not read that report and have not used the description in the construction here. Thus the mathematical formulation was independent, but there was no frozen written initial report before that brief exposure. Do not describe the team as having four strictly sealed written reports. The text below was written after that message.

## 1. Strongest completed construction

This is a genuine infinite-dimensional nonlinear collective description with explicit acquisition, preparation, finite-N, drive, horizon and computation errors. It works for a specified soft-particle Kac/mean-field physical class, not generic short-range matter. It is a constructive composition of familiar force learning, propagation of chaos and nonlinear Fokker–Planck evolution. Existing literature already studies learned interaction kernels, trajectory prediction and transfer in system size. Its value here is that there is no uncomputed force functional, hidden discarded-bulk gap or assumption of observation-law transfer to a new preparation.

### Physical class and interfaces

There are N overdamped particles on the unit d-torus. With continuously tracked lifts over a short calibration interval,

\[
dX_i=[u(t,X_i)+N^{-1}\sum_jK(X_i-X_j)+r_i(t)]dt+\sqrt{2D}\,dB_i.
\tag{1}
\]

The independent Brownian motions and diffusion D>0 are calibrated. The unknown odd pair force K is the negative gradient of a smooth periodic potential, with known bounds |K|<=B and Lip(K)<=L. The Kac factor 1/N is part of the physical class, not an inferred property of ordinary dense matter. The new prescribed drive u is supplied after acquisition and has |u|<=U, spatial Lipschitz constant L_u and temporal Lipschitz constant L_t. Residual implementation forces obey |r_i|<=nu. No feedback from the future specimen is included. The same acquired force is required in calibration and use.

The paid calibration interface can prepare fresh isolated two-particle cells governed by the same K with the known coefficient 1/2, place their initial separation at z up to 2zeta, switch u off, release for h, and observe the first particle's unwrapped displacement. Each coordinate has independent fresh zero-mean sub-Gaussian readout noise with proxy sigma_m^2 at each endpoint. Detector offsets, timing error and preparation error must be separately calibrated; repetition cannot remove an unknown offset. Isolation/coupling normalization is an explicit experimental operation and must not be silently supplied by the theorem.

A reset costs c_R(zeta), a displacement readout c_M, a calibrated interaction-cell unit-time c_I, and work/heat w_R,w_M,w_I. These are actual apparatus costs to be reported, not proven polynomial services. Counts below make the total cost explicit. This is an idealized stochastic-physics theorem until those services are implemented and compared.

### Acquisition lemma

For an exact pair preparation at separation z, put Z=X_1-X_2. Then

\[
dZ=K(Z)dt+\sqrt{4D}\,dW,
\qquad
2\mathbb E[X_1(h)-X_1(0)]/h=h^{-1}\int_0^h\mathbb E K(Z_s)ds.
\]

Consequently the force-estimator bias is at most

\[
b_h=L\{Bh/2+(4/3)\sqrt{Dd h}\}+2L\zeta+b_{\rm sys}.
\tag{2}
\]

Here b_sys is the remaining warranted drift bias after timing/background/offset calibration. If an endpoint mean offset is only bounded by b_x, add 4 b_x/h in Euclidean norm with the appropriate coordinate factor. The Brownian term in (2) is derived, not an assumed short-memory approximation.

Take a separation mesh of radius r and Q<=C_d r^{-d} points. At every point use M independent releases and average 2 times the measured displacement divided by h. A union bound over Qd coordinates, Hoeffding on the bounded drift integrals and Gaussian/sub-Gaussian bounds on Brownian and readout means gives a numerical constant C_d such that, with probability at least 1-delta_A,

\[
\max_z|\widehat K(z)-K(z)|
\le b_h+C_d\sqrt{[B^2+D/h+\sigma_m^2/h^2]\log(6Qd/\delta_A)/M}.
\tag{3}
\]

Multilinear interpolation, norm clipping and odd symmetrization produce a finite retained force table satisfying a uniform error alpha whenever the right side of (3) plus Lr is <=alpha (replace Lr by the exact mesh covering factor). Clipping is Euclidean projection onto the B-ball and does not increase distance from the true K. Odd symmetrization likewise does not increase uniform error. No smoothness of the learned interpolant is needed below.

At fixed B,L,D,d and attainable b_sys,zeta small enough, r=Theta(alpha), h=Theta(alpha^2), and

\[
Q=O(\alpha^{-d}),\quad
M=O([\alpha^{-4}+\sigma_m^2\alpha^{-6}]\log(Qd/\delta_A)).
\tag{4}
\]

The deliberately elementary estimator is not statistically optimal. Total acquisition counts are QM resets, QM releases of duration h and 2QM endpoint observations. Thus

\[
C_A=QM[c_R(\zeta)+c_I h+2c_M]+C_{\rm calibration}+C_{\rm table},
\tag{5}
\]

and work/heat have the same multiplicities. Store O(Qd log(1/alpha)) numerical bits after the raw records have been processed; retaining raw evidence costs O(QMd) readings at their actual precision. Calibration of all promised biases is an additional paid task, not free information.

### Reusable nonlinear collective law

The retained macroscopic state is a probability measure mu_t on the torus, not finitely many fixed moments:

\[
\partial_t\mu=D\Delta\mu-\nabla\cdot\{[u(t,\cdot)+K*\mu]\mu\}.
\tag{6}
\]

With bounded Lipschitz K,u this equation has a unique law-valued solution, constructible by Picard iteration of its McKean–Vlasov SDE. The proof is the usual synchronous-coupling contraction over short intervals, iterated; it does not assume an orthogonal-dynamics gap. Replacing K by the acquired force table changes the law by a controlled amount below. The nonlinearity survives at every spatial resolution.

### Finite-size and source theorem, without an iid source promise

Fix any deterministic initial microscopic configuration x_1,...,x_N. Let mu_0^N=N^{-1}sum delta_(x_i), and let mu_t solve (6) from mu_0^N. Define independent nonlinear processes Y_i with initial Y_i(0)=x_i, common deterministic drift u+K*mu_t and the same Brownian path as X_i. Their individual laws need not coincide; their average is mu_t, and the Y_i are independent. Conditional on Y_i, the interaction summands indexed by j!=i are independent, each bounded by B. The empirical-force residual has mean size <=B/N and root variance <=B/sqrt(N). Thus, writing C=L_u+2L,

\[
N^{-1}\sum_i\mathbb E|X_i(t)-Y_i(t)|
\le e^{Ct}\{2Bt/\sqrt N+t\nu\}.
\tag{7}
\]

For a 1-Lipschitz macro readout phi with |phi|<=1,

\[
\mathbb E\left|N^{-1}\sum_i\phi(X_i(t))-\int\phi\,d\mu_t\right|
\le [2Bt e^{Ct}+1]/\sqrt N+t e^{Ct}\nu.
\tag{8}
\]

The extra 1/sqrt(N) is the independent-Y empirical-readout variance. Equation (7) follows from dE/dt<=CE+2B/sqrt(N)+nu and Gronwall. Equation (8) is the triangle inequality and Var(N^{-1}sum phi(Y_i))<=1/N. One may work with torus distances by choosing coupled lifts and use periodic Lipschitz coefficients. No particle independence was asserted for X_i.

If a future preparation has its realized empirical measure within W_1 distance zeta_0 of the supplied mu_0, apply the same synchronous argument to (6): the added error is <=e^{Ct}zeta_0. The new particles may have arbitrary initial correlations conditional on that empirical-measure guarantee. If that guarantee holds with probability 1-delta_P, add delta_P as a source failure probability. Local-marginal closeness alone is insufficient and is never used. An explicit preparation is grid placement with rounded particle counts: mesh radius r_0 and M_0 sites give W_1 error <=r_0+diam(T^d)M_0/N plus physical placement error, at O(N) loading operations. Supplying an arbitrary computable mu_0 still requires charging its integration/input precision and description length.

### Fully computable field evolution

For timestep Delta and a spatial grid with covering radius s, let nu_k be a grid probability vector and perform

\[
\nu_{k+1}={\cal R}_s\,\operatorname{Law}[Y+\{u(k\Delta,Y)+\widehat K*\nu_k(Y)\}\Delta+\sqrt{2D\Delta}\,G],
\quad Y\sim\nu_k,\ G\sim N(0,I_d),
\tag{9}
\]

where R_s rounds to the nearest grid point. This is a finite nonlinear Markov update; each transition probability is a Gaussian box integral with a rigorously bounded wraparound tail. It can be computed to any certified rational error. Computing the learned convolution and all transition entries costs O(M_s^2) per step, M_s=O(s^{-d}), before bit-complexity factors. There is no many-body matrix or unknown continuum functional in (9).

Let e_k=W_1(mu_(kDelta),nu_k), and let kappa_k bound the Wasserstein error from Gaussian integration/arithmetic at step k. Put V=U+B and

\[
C=L_u+2L,\qquad
C_0=C[V+\sqrt{2Dd}]+L_t
\]

for Delta<=1. A synchronous one-step coupling gives

\[
e_{k+1}\le(1+C\Delta)e_k+\alpha\Delta+C_0\Delta^{3/2}+s+\kappa_k.
\tag{10}
\]

To see the Delta^(3/2) term, over an interval of length q the true particle moves in expected distance <=Vq+sqrt(2Ddq); the law moves by no more. Integrate the resulting drift error, plus L_t q, and enlarge constants as above. The learned-force error is bounded uniformly by alpha, so regularity of Khat is unnecessary. Rounding costs at most s. Therefore for t=KDelta<=T,

\[
W_1(\mu_t,\nu_K)\le e^{CT}\{e_0+T\alpha+TC_0\sqrt\Delta+Ts/\Delta+\sum_{k<K}\kappa_k\}.
\tag{11}
\]

This proof of computability uses the derived dynamics of the eliminated correlations through (7), rather than presupposing a computable closure. Gaussian-box integration can be done using certified normal-CDF approximations and a finite tail sum. Normalization/positivity can be preserved by interval-certified probability rows. Its bit cost is polynomial in inverse requested row accuracy, mesh input precision and the number of rows; sharper algorithms are ordinary improvements.

### Combined acquisition-to-reuse statement

On the one acquisition event sup|K-Khat|<=alpha, for every future specified mu_0, every prescribed u in the above class, every N, every t on the chosen grid up to T, and every admissible phi,

\[
\begin{split}
\mathbb E\left|N^{-1}\sum_i\phi(X_i(t))-\langle\phi,\nu_K\rangle\right|
\le{}&[2BT e^{CT}+1]/\sqrt N\\
&+e^{CT}\{\zeta_0+T\nu+e_0+T\alpha+TC_0\sqrt\Delta+Ts/\Delta+\sum_k\kappa_k\}.
\end{split}\tag{12}
\]

Here zeta_0 and e_0 must not double-count the same initial discretization. A clean implementation sets nu_0 to the supplied preparation vector, uses e_0=0 and puts all realized source mismatch into zeta_0. A non-grid final time uses a shortened last step. Markov's inequality converts (12) to an individual-specimen failure probability; finite lists of queries can be union-bounded. The deterministic predicted means share a uniform acquisition event, but infinitely many future independent noisy physical runs do not share a single pointwise sample guarantee.

For target mean-absolute accuracy epsilon, fixed physical parameters and fixed T, choose all bracket contributions O(epsilon e^(-CT)), N=O(e^(2CT)(1+BT)^2 epsilon^(-2)), Delta=O(epsilon^2 e^(-2CT)/(1+TC_0)^2), s=O(epsilon Delta e^(-CT)/(1+T)). This gives polynomial acquisition and numerical-query costs in epsilon^(-1) in fixed d,T, independent of the physical N after preparation is specified. The simple proof is exponential in T; it earns no polynomial long-horizon or critical/metastable claim. Physical use for a new specimen costs O(N) loading plus its actual N-particle runtime, controls, readout, heat/work and reset. Prediction avoids propagating those N microscopic coordinates but must be compared with the same-information mean-field incumbent, which has this same mechanism.

The consequence is nonlinear driven collective density/transport prediction in a physically specified long-range soft-particle class, for genuinely new macroscopic profiles and extensive new drives. Threshold decisions are certified only when their margins exceed the explicit error. Rare-event rates, nucleation, phase-selection times, arbitrary short-range matter and hardware advantage are not implied.

## 2. Simpler local nonlinear mechanism and stronger existing machinery

For a 1D exclusion lattice gas with exchange rate

\[
c_{x,x+1}(\eta)=\lambda[1+a(\eta_{x-1}+\eta_{x+2})],\qquad a>-1/2,
\]

the microscopic current is exactly a gradient: with

\[
h_x=\eta_x+a(\eta_{x-1}\eta_x+\eta_x\eta_{x+1}-\eta_{x-1}\eta_{x+1}),
\]

one has c_(x,x+1)(eta)(eta_x-eta_(x+1))=lambda(h_x-h_(x+1)). Bernoulli-density averaging gives Phi(rho)=rho+a rho^2, hence the known nonlinear hydrodynamic equation partial_t rho=lambda partial_xx(rho+a rho^2). This is a genuine short-range interacting model, and rates can be learned by constant-size occupation-pattern preparation and jump counting. But I have not completed a quantitative theorem uniform over new inhomogeneous drives and noisy preparations for this model. The gradient identity alone does not prove local equilibrium or a finite-N error.

A substantially stronger existing predecessor is Funaki–Gu–Wang, arXiv:2404.12234v2 (23 May 2024), [primary full text](https://arxiv.org/html/2404.12234v2). Under their Hypothesis 1.1 (known finite range, translation invariance, uniform positive exchange rates, and rates independent of the two exchanged occupations), Theorem 1.4 gives algebraic convergence of finite-cell conductivity variational problems; Theorem 1.2 constructs density-uniform local correctors; Theorem 1.3 gives a polynomial quantitative hydrodynamic error from the stated entropy-close smooth initial data. Thus a useful nonlinear constitutive law is not generically an unevaluable oracle even for nongradient exclusion. Directly importing arbitrary drives or claiming polynomial-in-accuracy cell computation would be false: the finite-cell state space is exponential in cell volume, the theorem is stated for the unforced model, and its constants/exponents must be extracted before a numeric certificate is promised.

A constructive next attack is learn the finite local rate table, use the variational monotonicity c_hat in (1+-eta)c => conductivity_hat in (1+-eta)conductivity, compute finite-cell coefficient intervals, then propagate them with a stable nonlinear diffusion solver. In 1D, if A'=D>=d_* and sup|A-Ahat|<=delta, equal-mass solutions of partial_t rho=partial_xx A(rho) satisfy

\[
\|\rho_t-\widehat\rho_t\|_{H^{-1}}^2\le\|\rho_0-\widehat\rho_0\|_{H^{-1}}^2+T\delta^2/d_*.
\]

Proof: test the difference equation with (-Delta)^(-1)(rho-rhohat), use monotonicity of A and Young's inequality. This gives directly computable weak-observable error without differentiating a learned diffusion function. The remaining decisive operation is a verified driven/finite-noise preparation extension with extracted constants, not another fitted PDE demonstration.

## 3. Literature and novelty accounting

Primary predecessors already make a historic-discovery claim untenable for the completed mean-field construction:

- Lu–Zhong–Tang–Maggioni, PNAS 2019, [full primary text](https://pmc.ncbi.nlm.nih.gov/articles/PMC6642354/), learn nonparametric pair interaction laws and explicitly discuss transfer to larger particle numbers. Their learning metric is the trajectory-dependent occupancy law; uniform all-preparation force acquisition is a stronger paid interface here, not a free deduction from their theorem.
- Lu–Maggioni–Tang, JMLR 22 (2021), [primary paper](https://www.jmlr.org/papers/volume22/19-861/19-861.pdf), provides learning and trajectory-error theorems for heterogeneous agents. Exact theorem/hypothesis checking remains to be completed before using any theorem as a dependency. None is needed for the elementary proofs above.
- Yao–Chen–Yang, COLT 2022, [primary paper](https://proceedings.mlr.press/v178/yao22a/yao22a.pdf), estimate McKean–Vlasov drift from continuous trajectories; the access model here pays for discrete noisy interventions and avoids relying on its continuous-observation likelihood theorem. It already establishes the substantive field's existence.
- The supplied Mori–Zwanzig papers retain their actual projection/noiseless-data or hypocoercivity hypotheses. The constructor route does not use them. Formal exactness of power-functional and adiabatic variational descriptions is not an acquisition algorithm.
- The exact supplied arXiv:2609.37392v1 [record](https://arxiv.org/abs/2609.37392v1) reports that v2 was withdrawn on 2 October 2026. Preserve that current status rather than using its v1 as an unqualified validated result.

**Novelty status:** the self-contained end-to-end error accounting in (12) is a newly written derivation in this session; its building blocks and principal physical consequence are established mathematics. Historical novelty, practical superiority and a general new collective-physics principle are NOT_ESTABLISHED. The local nongradient route may be stronger in physical scope but remains an incomplete attack here.

## 4. Obstruction tests and exact limitations

1. **Initial local observations do not become dynamical source control.** Equation (12) requires empirical W_1 source control, not static local reduced-state accuracy; arbitrary hidden correlations outside that contract are not covered.
2. **Unbounded future force/drive classes defeat finite acquisition.** A finite set of noisy local probes cannot certify uniform predictions at arbitrarily fine unprobed spatial/drive scales without a known regularity or finite dictionary. Narrow changes to a constitutive law can be made undetectable on the acquired query distribution and revealed by a new targeted preparation. The Lipschitz/B bounds and the paid covering mesh are essential, not conclusions of the data.
3. **No dense-short-range leap.** Kac-normalized interactions mean the mean field is physically exact as N grows. An ordinary fixed-strength local fluid does not satisfy (7); replacing it by (6) is an uncontrolled closure unless a separate hydrodynamic/kinetic theorem is proved.
4. **No indefinite-horizon leap.** The explicit exponential-T bound exposes the instability/accumulation problem rather than hiding it. Convexity or a verified contractive physical mechanism could improve it, but this initial report does not assume a gap for discarded variables.
5. **No acquisition-free savings.** Pair isolation, same-kernel transfer, controllable normalization, preparation, tracking, bias calibration and resetting are paid structural interfaces. If the specimen lacks them the theorem does not apply. An equal-information incumbent can retain the same learned K and solve the same equation.

This report supplies an actual collective construction and a stronger local constructive attack. It does not close the user's broad strongest foundational objective.
