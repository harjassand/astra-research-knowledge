# Acquired productive repair: attained resource boundary and physical limitations

Working companion construction, 2026-11-05. This is a mathematical result for a declared finite-source repair contract. It is not a new physical apparatus or a priority claim for machine-repair models, monotone coupling, or birth–death exit asymptotics.

## 1. Operational question and contract

There are `N` continuously productive modules. If `K_t=k` are unavailable, the remaining modules deliver genuine useful flow at rate `r(k)=nu(N-k)` with `nu>0`: for example delivered pumping capacity or another continuously measurable output. A backlog or physical demand is present, and delivered flow is retained if a later module fails. Define service failure at

\[
\tau_m=\inf\{t:K_t=m\},\qquad 1\le m<N,
\]

and useful work `W=integral_0^tau r(K_t)dt`. Before failure, useful flow is at least `nu(N-m+1)`. This explicitly excludes increasing lifetime by stopping useful operation.

The homogeneous Markov service contract is:

* Each healthy module fails at hazard `lambda`; hence total upward jump rate at count `k` is `b_k=lambda(N-k)`.
* There are `c_N` installed repair channels. Each busy channel repairs one failed module at completion hazard `mu`. One module may occupy at most one channel. Repair returns it to a healthy state with the original characteristics.
* A causal policy may allocate or idle the channels, depending on the whole past. Its total repair intensity is at most `d_k=mu min(k,c_N)`.
* Only single-module jumps occur. No unpriced common catastrophe, degraded repair, latent output corruption, repair-induced failure, time-dependent ageing, or unavailable replacement stock is included in this base model.
* A work-conserving assignment realizes `d_k` at every count. Exponential service and immediate dispatch are part of this particular contract. A deterministic setup/detection dead time cannot be folded into `mu` without a proof. Autonomous local repair with `c_N=N` avoids pooled dispatch, but its measured conditional rates still require a physical justification.

The intervention is the repair capacity or local repair drive. It changes the invariant distribution. No identical-invariant-law assumption is used.

## 2. Full allocation optimum for fixed installed capacity

**Theorem 1.** Work-conserving allocation stochastically maximizes both the service-failure time and useful work before failure among every causal randomized repair-allocation policy satisfying the contract.

**Proof.** Couple the optimal count `K*` and any other count `K^pi`, initially equal. Whenever the counts agree, couple all upward jumps and all downward jumps of the other process; assign additional repair jumps only to `K*`. At equal counts its downward intensity is at least that of the other process. At unequal ordered counts, unit jumps cannot cross them. Standard Poisson thinning gives a construction with `K*_t<=K^pi_t` at all times up to absorption. Consequently `tau*>=tau^pi`. On the common time interval the decreasing reward satisfies `r(K*)>=r(K^pi)`; the additional interval contributes nonnegative work. Thus `W*>=W^pi` under the coupling. This proves stochastic, and hence mean, optimality. Labels or priorities are immaterial only because components and repair channels have identical characteristics.

This is an honest direct-method optimum: ordinary monotone comparison and finite-source queueing already supply this operation. It does not beat an equally informed direct queueing decision method.

### Robust conditional-intensity extension

If an operating system has history-dependent single-unit failure intensity at most `lambda(N-k)` and a realizable repair operation with conditional completion intensity at least `mu min(k,c_N)`, the same coupling places its damage count below the homogeneous envelope. Hence every lower survival/work guarantee for that envelope remains valid without stationarity, independence, reversibility, or a Markov assumption for the actual system. These must be pointwise conditional-intensity bounds, not merely average rates. Finite homogeneous-rate assay data alone cannot certify them for arbitrary future histories. The envelope itself belongs to this class and attains the worst case, so the envelope guarantee cannot be uniformly improved within the stated class.

## 3. Exact finite-N answer, including every safe start

Let

\[
w_0=1,\qquad
w_k=\prod_{j=1}^{k}\frac{\lambda(N-j+1)}{\mu\min(j,c_N)}.
\]

These are the unnormalized stationary weights for the corresponding unabsorbed repair chain on `0,...,N`. For every safe initial state `i<m`,

\[
H_i=\mathbb E_i\tau_m
=\sum_{k=i}^{m-1}\frac{\sum_{j=0}^{k}w_j}{b_k w_k},
\tag{1}
\]

\[
G_i=\mathbb E_i W
=\sum_{k=i}^{m-1}\frac{\sum_{j=0}^{k}w_j\nu(N-j)}{b_k w_k}.
\tag{2}
\]

**Derivation.** The reward equation is `b_k(G_k-G_{k+1})-d_k(G_{k-1}-G_k)=r(k)` with `G_m=0`. Multiplication by `w_k` and detailed balance `w_k d_k=w_{k-1}b_{k-1}` telescopes to

\[
b_k w_k(G_k-G_{k+1})=\sum_{j=0}^k w_j r(j).
\]

Summing yields (2); set `r=1` for (1). Log weights, log prefix sums, and one reverse cumulative sum evaluate every initial-state mean in `O(N)` arithmetic and `O(N)` memory (or one chosen mean with streaming memory). Relative precision and transcendental evaluation are a separate numerical specification.

Let `i*` be any mode of `w_0,...,w_(m-1)` and

\[
R_N=w_{i_*}/w_{m-1},\qquad b_{m-1}=\lambda(N-m+1).
\]

The weights are unimodal because successive weight ratios decrease. For **every** safe `i`,

\[
\frac{R_N}{b_{m-1}}\le H_i\le
\frac{m(m+1)}{2}\frac{R_N}{b_{m-1}}.
\tag{3}
\]

For the lower bound retain the final term of (1), whose numerator contains the modal weight. Before the mode, each prefix weight is at most its final weight; after it, every numerator is at most `(k+1)w_i*` and `w_k>=w_(m-1)`. Sum `(k+1)R_N/b_(m-1)`. Also

\[
\nu(N-m+1)H_i\le G_i\le\nu N H_i.
\tag{4}
\]

These establish the same exponential mean scale from every safe start. They do **not** assert a small immediate failure probability from a start adjacent to failure.

### Finite-horizon survival from an acquired all-healthy start

Normalize `pi_k=w_k/sum_j w_j` on `0,...,N`. Couple a chain started at zero below a stationary version. If the stationary version reaches `m` by time `T`, it either started at/above `m` or made an upward crossing from `m-1`. The expected number of such crossings is `T pi_(m-1)b_(m-1)`. Therefore

\[
\Pr_0(\tau_m\le T)\le
\pi([m,N])+T\pi_{m-1}b_{m-1}.
\tag{5}
\]

This uses stationarity only as an analytical comparison; the operating plant starts healthy and never requires equilibrium preparation. If

\[
q_N=b_{m-1}/d_m<1,
\]

decreasing weight ratios and normalization by at least the modal weight give the simpler explicit certificate

\[
\Pr_0(\tau_m\le T)\le
R_N^{-1}\left[\frac{q_N}{1-q_N}+b_{m-1}T\right].
\tag{6}
\]

It is valid for the history-dependent envelope system as well, under its stated conditional-intensity contract. On the no-failure event, delivered work by time `T` is at least `nu(N-m+1)T`.

## 4. Sharp repair-capacity boundary and exponent

Let `m/N -> b in (0,1)` and `c_N/N -> s>0`, keeping positive finite `lambda,mu,nu` fixed. Put `rho=1-b`, the required healthy fraction. The fluid drift is

\[
f(x)=\lambda(1-x)-\mu\min(x,s).
\]

It has a unique zero

\[
x_*=\begin{cases}
\lambda/(\lambda+\mu),&s\ge\lambda/(\lambda+\mu),\\
1-\mu s/\lambda,&s<\lambda/(\lambda+\mu).
\end{cases}
\]

For every safe starting sequence,

\[
\lim_{N\to\infty}\frac1N\log H_i
=\lim_{N\to\infty}\frac1N\log G_i
=V(b,s),
\]

where

\[
V(b,s)=\begin{cases}
\displaystyle\int_{x_*}^{b}\log\frac{\mu\min(x,s)}{\lambda(1-x)}\,dx,&b>x_*,\\
0,&b\le x_*.
\end{cases}
\tag{7}
\]

This follows directly from (3), product weights, and Riemann sums; no unproved diffusion replacement is needed. For fixed parameters with an interior modal point, `log R_N=NV+O(1)` under integer rounding, while (3) leaves only `O(log N)` uncertainty in log mean.

**Positive exponential service scale is feasible iff both**

\[
\mu b>\lambda\rho,
\qquad
\mu s>\lambda\rho.
\tag{8}
\]

The first is the individual-channel repair-speed requirement; the second is the total installed-capacity requirement. More channels cannot overcome an inadequate per-module repair rate. If the boundary drift is positive by `delta>0`, then it is at least `N delta+O(1)` throughout the safe region, and Dynkin's formula gives

\[
\mathbb E_0\tau_m\le\frac{b+o(1)}{\delta}.
\tag{9}
\]

At equality the exponent is zero; a claim of a fixed exponential service guarantee at criticality is false. In the saturated regime `x*>=s` relevant to the root's phase diagram, writing `c=mu s` gives

\[
V=\frac{c}{\lambda}-\rho-\rho\log\frac{c}{\lambda\rho}.
\tag{10}
\]

For relative slack `Delta=c/(lambda rho)-1`,

\[
V=\rho\bigl(\Delta-\log(1+\Delta)\bigr)
=\frac{\rho\Delta^2}{2}+O(\Delta^3).
\]

This expansion alone does not justify extrapolating fixed-slack mean asymptotics uniformly into a critical window; the exact finite-N expressions remain available there.

For autonomous independent repair (`s>=b` on all safe states), `q=lambda/(lambda+mu)` and `V=D(b||q)` when `b>q`, the binary relative entropy. The maximal possible exponent at this repair speed is attained once `s>=b`; installing more channels does not alter any safe-state dynamics.

## 5. Useful-work clock, energy, parts, and physical support

In useful-work time `w=nu integral(N-K_t)dt`, failure events have constant intensity `lambda/nu`; repair events have intensity `mu min(k,c_N)/(nu(N-k))`. The repair decision cannot acquire a fictitious benefit by dilating the wall clock.

Let `F_T` and `R_T` be the numbers of failures and completed repairs by a stopping time. Pathwise

\[
K_T-k_0=F_T-R_T.
\]

Under the homogeneous failure contract, compensators give

\[
\mathbb E F_T=(\lambda/\nu)\mathbb E W_T,
\]

so

\[
\boxed{\mathbb E W_T=(\nu/\lambda)
[\mathbb E R_T+\mathbb E K_T-k_0].}
\tag{11}
\]

At service failure `K_T=m`, this becomes an exact energy/material account. If each completed repair consumes energy `e>0`, then

\[
\mathbb E E_{repair}=
(e\lambda/\nu)\mathbb E W-e(m-k_0).
\tag{12}
\]

Equivalently, if each busy repair channel dissipates power `p_r` and completes at rate `mu`, the same **expected** identity holds with `e=p_r/mu`. A positive universal reset energy is not assumed: (12) applies only where this is the actual physical repair cost. No unsupported Landauer lower bound is asserted.

If at most `B` repairs can be supplied before resources are exhausted and operation continues until failure, **every** allocation policy obeys

\[
\mathbb E W\le(\nu/\lambda)(B+m-k_0).
\tag{13}
\]

Thus a finite stock of repair parts, or energy sufficient for only `B` positive-cost repairs, limits useful work linearly in that stock. Exponential mean useful work requires exponential expected total repair throughput/resources, even though instantaneous hardware and power scale only linearly in `N`. A reusable repair mechanism still needs its actual operating energy and lifetime accounted; it does not automatically consume one material part per event.

If background operation, sensors, dispatch, and standby repair channels consume total power `P_bg`, then

\[
\mathbb E E_{total}\le E_{init}+
\left[\frac{P_{bg}}{\nu(N-m+1)}+\frac{e\lambda}{\nu}\right]\mathbb E W
-e(m-k_0),
\tag{14}
\]

when these are the complete costs. Linear instantaneous background power yields a finite energy cost per useful unit at fixed healthy fraction. This says nothing about the cost or reliability of supplying that energy for an exponentially long interval.

For a net expected utility `W-price*E_repair`, (12) gives

\[
\mathbb E[W-price E_{repair}]
=(1-price\,e\lambda/\nu)\mathbb E W+price\,e(m-k_0).
\]

Hence the same work-conserving optimum applies when the coefficient of useful work is positive, for the specified repair-energy cost and fixed installed capacity. Standby cost and a finite fuel budget can change the full design optimization and must be supplied separately.

### Protection is part of the operation

Suppose shared power, cooling, dispatcher, load routing, or other indispensable support has an independent failure time `sigma~Exp(kappa)`. Actual service ends no later than `min(tau_m,sigma)`, giving

\[
\mathbb E\tau_{physical}\le1/\kappa,
\qquad
\mathbb E W_{physical}\le\nu N/\kappa.
\tag{15}
\]

A constant common-support hazard eliminates the exponential-in-N lifetime claim. If `kappa_N=exp(-N gamma+o(N))`, adequate repair resources are supplied, and the internal chain is in the strict stable regime, (3), (6), and independence yield actual mean lifetime exponent `min(V,gamma)`: the upper bound is immediate; for the lower bound use a horizon below both exponents and the survival certificate. Protection therefore needs its own error budget and hardware/energy model. It is not supplied by the internal repair theorem.

## 6. Acquisition, preparation, metrology, deployment, reuse

The all-healthy state is acquired by inspecting/resetting all modules, with initialization latency and energy charged. It is not a Gibbs or other equilibrium preparation. Reliable state detection, valid output in healthy mode, and the unchanged repair characteristics are prerequisites to be demonstrated for a particular platform.

For genuinely homogeneous constant rates, an alternating single-module assay gives independent healthy dwell times `Exp(lambda)` and repair dwell times `Exp(mu)`. `K=O(eta^-2 log(1/delta))` paired intervals estimate the rate ratio to relative error `eta`, using expected physical exposure `K(1/lambda+1/mu)` and `2K` observed transitions. Ordinary operation can also supply cumulative healthy and busy-repair exposures. Individual failures need not be rare on the collective service-failure scale. If individual `lambda` is very small, its waiting bill still remains, and parallelism buys wall time with extra test hardware. A matched test module is not proof of transfer to the operating population.

For a fixed positive slack in (8), this local parameter evidence is independent of the collective failure threshold `N`. If rates are heterogeneous and only per-unit worst-case bounds are available, every relevant unit/type needs coverage, potentially linear in `N` or worse. Empirical averages cannot establish arbitrary history-uniform intensity bounds.

The instrument/control bill is at least module status sensors and repair resources, with `O(N)` status/queue memory and `O(N)` event throughput per unit wall time at fixed rates in a pooled implementation. Physical dispatch distance, detection latency, transport, and setup time must satisfy the actual completion-hazard contract; if not, add those stages to the state and recompute. Autonomous per-site channels remove the global scheduling dependency at the expense of more installed channels.

Systematic clock, missed-event, and exposure errors must fit inside the slack budget; repeated samples do not eliminate them. A common clock scale cancels in a rate ratio, but separate-clock calibration does not. Repair-rate load dependence and workload-dependent failure rates require measurement at the deployed conditions.

Reuse of one calibration is valid only for the declared constant-rate lifetime or a proved future envelope. With bounded drift, shrink the safety margin and set a recalibration interval before the envelope expires. Arbitrary unobserved drift cannot be controlled by an initial finite assay. If separate confidence statements are used over many epochs, their total failure probability must be budgeted over all epochs. Maintaining an exponential-duration service claim may itself require an exponential number of ordinary recalibration/maintenance cycles.

## 7. Strongest comparison and provenance

This construction is an exact attained reliability/resource boundary for the stated class, plus a physical accounting framework. It has no established priority or civilization-level claim. The finite-source machine repair process is classical. Direct local-rate assessment, work-conserving repair, birth–death formulas, and drift certificates are the strongest ordinary same-decision methods here; they obtain the same decision without reconstructing a rare absolute lifetime. Any evidence separation from absolute prediction must be stated as a separation of different statistical targets, not a victory over these direct methods.

Primary literature checked:

1. P. Naor (1956), **On Machine Interference**, JRSS B 18(2), 280–287, DOI 10.1111/j.2517-6161.1956.tb00235.x. Explicit state probabilities and diminished productivity for several repairmen servicing machines. https://academic.oup.com/jrsssb/article/18/2/280/7027272
2. P. Naor (1957), **Normal Approximation to Machine Interference with Many Repairmen**, JRSS B 19(2), 334–341, DOI 10.1111/j.2517-6161.1957.tb00269.x. https://academic.oup.com/jrsssb/article/19/2/334/7026756
3. R. N. Salia and M. A. Shashiashvili (1985), **On Palm's Model with a Large Number of Machines and Repairmen**, JRSS B 47(2), 316–322, DOI 10.1111/j.2517-6161.1985.tb01359.x. Large-population stationary approximation and asymptotically optimal repair staffing under production costs. https://academic.oup.com/jrsssb/article/47/2/316/7035726
4. D. Gross and J. F. Ince (1981), **The Machine Repair Problem with Heterogeneous Populations**, Operations Research 29(3), 532–549, DOI 10.1287/opre.29.3.532. Explicitly identifies identical failure/repair characteristics as the classic model and develops heterogeneous extensions. https://pubsonline.informs.org/doi/pdf/10.1287/opre.29.3.532
5. **Monotone matrices and monotone Markov processes** (1977), Stochastic Processes and their Applications, DOI corresponding to 0304414977900333. Search result states the established monotonicity of birth–death processes; full publisher page was blocked. https://www.sciencedirect.com/science/article/pii/0304414977900333
6. **Large deviations and quasi-stationarity for density-dependent birth–death processes**, ANZIAM Journal (2009 online entry). Relevant established large-deviation machinery; current theorem instead derives the exponent directly from exact weights and (3). https://www.cambridge.org/core/journals/anziam-journal/article/large-deviations-and-quasistationarity-for-densitydependent-birthdeath-processes/90398B27C94418A53A0E39562D10A95E
7. M. Jain, C. Shekhar, S. Shukla (2016), **N-policy for a repairable redundant machining system with controlled rates**, RAIRO Operations Research 50(4–5), 891–907, DOI 10.1051/ro/2015032. Controlled/interdependent rates, extra repairmen, mixed standbys and degraded production are already studied; this prevents claiming these physical features as novel. https://www.numdam.org/articles/10.1051/ro/2015032/

## 8. Executed verification

`physical_repair_companion.py` checks the exact Green-sum means against direct finite-generator linear solves; exhaustively checks all 54 stationary staffing choices for a seven-module/five-failure/two-channel example; checks the stationary-coupling finite-horizon bound against matrix-exponential survival; and computes log-scale means across capacities below, at, and above the threshold for `N=100,...,1600`. All checks passed. These checks verify finite algebra and illustrate convergence; they do not validate the physical contract, establish novelty, or replace the proofs above.
