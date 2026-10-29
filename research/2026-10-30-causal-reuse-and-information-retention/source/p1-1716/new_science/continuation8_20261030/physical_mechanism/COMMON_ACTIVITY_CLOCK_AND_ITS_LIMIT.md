# A common activity clock programs rare transport, but cannot suppress it at fixed mean speed

30 October 2026. Existing Astra P1 physical-mechanism role. This is a constructive ordinary comparator for programming a macroscopic transport law without identifying hidden kinetic amplitudes. It is deliberately different from the event-updated shared-sign mechanism under development by root. Stationary thinning, stochastic time change, occupation large deviations and switching-diffusivity tails are established methods; no priority claim is made for them.

## 1. Outcome and decisive limitation

Suppose a real actuator can multiply the **entire supplied physical generator** by one of two known positive factors g_0<g_1. Drive that actuator by an independent two-state clock whose physical transition rates are Q/N while the specimen is observed for physical time N^2 T. This operation has a precise macroscopic consequence: it adds a controllable global activity cost to the inherited density/current action.

Write D=s/2, chi(rho)=rho(1-rho), and let the base action be

\[
I_U^0(\rho,j)=\frac1{2s}\int_0^U\!\int_{\mathbb T}
\frac{[j+D\rho_x]^2}{\chi(\rho)}\,dx\,du,
\qquad \rho_u+j_x=0,\quad\rho(0)=m.                 \tag{1}
\]

The new full action is

\[
\boxed{I_T^{\rm gate}(\rho,j)=
\inf_{a:[0,T]\to[g_0,g_1]}
\int_0^T\left\{
\frac1{2s}\int_{\mathbb T}
\frac{[j+a(t)D\rho_x]^2}{a(t)\chi(\rho)}\,dx
+\ell_Q(a(t))\right\}dt.}                           \tag{2}
\]

The infimum uses measurable a. The standard finite-energy and continuity interpretation of (1) is retained. The variable a(t) is global in space, so eliminating it produces a nonlocal rare-history action without identifying the hidden native amplitudes.

For Q with transition rates r from state 0 to 1 and l from state 1 to 0, put

\[
x(a)=\frac{a-g_0}{g_1-g_0},\qquad
\ell_Q(a)=\bigl[\sqrt{r(1-x(a))}-\sqrt{l x(a)}\bigr]^2. \tag{3}
\]

The stationary mean speed is
\(\bar g=(l g_0+r g_1)/(r+l)\).
For total circulation q and v=s chi(m), the endpoint rate and scaled cumulant generating function are exactly

\[
I_T^{\rm gate}(q)=\min_{a\in[g_0,g_1]}
\left\{\frac{q^2}{2vTa}+T\ell_Q(a)\right\},          \tag{4}
\]

\[
\Lambda_T^{\rm gate}(\lambda)
=T\lambda_{\max}\!\left(Q+\frac{v\lambda^2}{2}
\operatorname{diag}(g_0,g_1)\right).                 \tag{5}
\]

This is a working controller with a complete receiving formula, not an appeal to unknown favorable mobility. But it has a sharp limitation. At fixed mean speed bar g=1,

\[
I_T^{\rm gate}(q)\le\frac{q^2}{2vT},\qquad
\Lambda_T^{\rm gate}(\lambda)\ge\frac{vT\lambda^2}{2}. \tag{6}
\]

Thus autonomous positive common speed modulation can broaden rare circulation tails. It cannot reproduce a suppression of equilibrium circulation at unchanged mean diffusion. Its SCGF curvature at zero is unchanged. Section 8 proves an actual stationary current CLT separately; that conclusion is not inferred by differentiating an LDP.

## 2. Actual operation, hidden information and physical time

Let X_N^0(u) denote the **entire** supplied base Markov state in physical time u, including occupancy eta, actuated phase/sign coordinates, and any frozen z. Its physical generator is B_N. A valid inherited supplier is

\[
B_N=\sum_i\frac{s}{2}[1+\beta_i(\eta,z)\sigma_i](T_i-I)
+\gamma_N\sum_i(F_i-I),                              \tag{7}
\]

where |beta_i|<=1, beta_i is invariant under its own exchange, F_i reverses its own sign, and the independent sign strength gamma_N tends to infinity. The circle-diffusion supplier is equally admissible when its entire generator is multiplied. The unknown beta_i may depend on all occupancies and arbitrary frozen data. The base action (1) and its moment bounds are supplied by the accepted continuation7 proof, including its zero-gate extension.

**Additional port.** In gate state k, the actual generator must be g_k B_N. In particular, the native transition intensities and the already supplied phase/sign clock must all receive the same multiplier. If an unactuated hidden process continues at a different clock, the exact time-change identity below is not supplied by this assumption. The frozen z of (7) causes no difficulty.

This port is substantial. Knowing equilibrium weights, having a phase diffusion kernel, being able to select endpoint calls, or logging a random seed does not establish it. A model-level supplier can consist of Arrhenius native rates whose transition-state energies all acquire the same added barrier Delta B_k while well energies and attempt factors remain fixed: the factor is then g_k=exp(-beta Delta B_k). That is an explicit rate-model premise, not a claim that an actual material's prefactors remain fixed when its barriers are moved. The phase/sign apparatus must separately be commanded to the corresponding strength g_k gamma_N or g_k kappa_N. No apparatus for this uniform barrier change is constructed here.

Both g_k are strictly positive. Therefore the construction does not assume a perfect hold, protected storage or microscopic reset. Gate switching is assumed not to move particles or change the frozen data. Its timing and switching transients are part of the required port specification, not free omissions.

The gate G_N(tau) is an actual independent two-state continuous-time chain in physical wall time tau, with generator Q/N. On physical horizon N^2 T it makes order-N transitions. Its innovations must be independent of the base execution innovations conditional on the retained past. Its initial state may be fixed and recorded.

At gate stationarity the expected transition count is exactly 2rlNT/(r+l); a fixed initial gate adds only O(1). Each transition may require a command delivered to all N bonds and to the phase apparatus. The independent-sign base still executes gamma_N N^3 A_N(T) sign flips in conditional expectation, and native opportunities remain order N^3 on the full horizon. The extra gate's slow clock does not remove these base costs. Preparing the initial occupancy profile, maintaining the known common mean, sensing the desired current, controlling the uniform multiplier and keeping records are also actual resources. A rate multiplier alone supplies no energy/work estimate.

## 3. Exact time change of a persistent specimen

Define the operational time

\[
C_N(\tau)=\int_0^\tau g_{G_N(u)}\,du,
\qquad A_N(t)=N^{-2}C_N(N^2t).                         \tag{8}
\]

Take an independent base process X_N^0 and set X_N(tau)=X_N^0(C_N(tau)). Conditional on a gate path, this process has the prescribed generator g_{G_N(tau)} B_N. Together with the autonomous gate its generator is

\[
\mathcal B_N f(x,k)=g_k B_N f(\cdot,k)(x)
+N^{-1}\sum_{k'}Q_{kk'}f(x,k').                       \tag{9}
\]

This proves equality in law with the actual gated execution. It is a representation of one persistent specimen's dynamics. The apparatus does not sample counterfactual futures, copy hidden states or run the base process separately.

The gate clock in macroscopic time has generator NQ. Every A_N lies in the compact set

\[
\mathcal A=\{A\in C[0,T]:A(0)=0,\quad
g_0(t-u)\le A(t)-A(u)\le g_1(t-u)\},                 \tag{10}
\]

so clocks are uniformly Lipschitz and have uniformly Lipschitz inverses on their ranges. The native integrated-current record is time changed by exactly the same A_N; no extra current is assigned to the gate events.

The initial visible sequence and frozen-sector scope are those of the inherited base theorem: for the full action stated here, each deterministic visible initial sequence approaches the fixed flat profile m. The gate does not create that initial preparation. The stationary CLT variant later has a different, explicitly specified initialization.

## 4. The clock has an explicit path cost

The integrated occupation of a finite-state chain with generator NQ has a speed-N path LDP. Here its contraction to A is

\[
J_T(A)=\int_0^T\ell_Q(A'(t))\,dt\quad(A\in\mathcal A), \tag{11}
\]

and infinity otherwise. The initial gate state contributes no exponential-volume cost. This standard path occupation result is stated, for example, as Corollary 3.3 following Theorem 3.1 in Huang--Mandjes--Spreij, *Large deviations for Markov-modulated diffusion processes with rapid switching*, [primary manuscript](https://arxiv.org/pdf/1501.03020), [published DOI](https://doi.org/10.1016/j.spa.2015.12.005). Its model, occupation metric, rate definition (5), Theorem 3.1 and Corollary 3.3 were read.

For clarity, the rate used here is not an unexplained eigenvalue approximation. At occupation fractions (1-x,x), the two-state variational expression is

\[
\begin{aligned}
\ell(x)
&=-\inf_{z>0}\{(1-x)r(z-1)+xl(z^{-1}-1)\}\\
&=r(1-x)+lx-2\sqrt{rlx(1-x)}.
\end{aligned}                                       \tag{12}
\]

This proves (3), including the endpoint costs ell(g_0)=r and ell(g_1)=l. The boundary lower costs also follow from staying in the chosen gate state; if necessary, enter it during an initial interval tending to zero. Thus a strictly interior occupation approximation does not accidentally discard the endpoint costs. The zero-cost speed is bar g. Convexity follows either from (12) or from the occupation variational formula. Compactness of (10) supplies clock exponential tightness.

Equivalently, for any real h,

\[
\lim_N\frac1N\log\mathbb E e^{Nh A_N(T)}
=T k_Q(h),\qquad
k_Q(h)=\lambda_{\max}(Q+h\operatorname{diag}(g_0,g_1)), \tag{13}
\]

because the exact finite-N moment is an entry of
\(\exp[NT(Q+h\operatorname{diag}g)]\mathbf1\).
The positive two-state eigenvector gives the large-N limit for either initial state. Explicitly,

\[
k_Q(h)=\frac{h(g_0+g_1)-r-l+
\sqrt{[h(g_0-g_1)-r+l]^2+4rl}}{2}.                    \tag{14}
\]

The established switching-diffusion predecessor is particularly close: Gueneau--Majumdar--Schehr, *Large Deviations in Switching Diffusion: From Free Cumulants to Dynamical Transitions*, [primary paper and supplement](https://arxiv.org/pdf/2501.13754), [DOI](https://doi.org/10.1103/rqsn-bzr6). Its supplement Sections IV and V derives the two-diffusivity SCGF and equivalent two-state switching process. Formula (14) and the scalar tail mechanism below are not new discoveries relative to that literature.

## 5. Full density/current receiver by continuous time change

Fix U=g_1 T. Use the continuous interpolated version of the accepted base density/current path on [0,U], with its good speed-N action (1). The interpolation discrepancy is bounded by one native jump and is deterministically exponentially negligible. Its path space is the continuous version of H^-3 density/current paths used in the inherited theorem.

The independently constructed pair (base path,A_N) has the product LDP with rate I_U^0+J_T. The composition map

\[
(\rho^0,W^0,A)\mapsto(\rho^0\circ A,W^0\circ A,A)     \tag{15}
\]

is continuous in the uniform path topology: the base-path error is bounded by its uniform error plus the limiting path's modulus of continuity at the clock error. This avoids inferring a path theorem from endpoint moments. It also avoids a spurious Markov claim for the coarse visible process.

On a finite-action path write a=A'. The inverse clock is bi-Lipschitz since g_0>0. If j denotes physical-macroscopic current, then

\[
\rho(t,x)=\rho^0(A(t),x),\qquad
j(t,x)=a(t)j^0(A(t),x).                              \tag{16}
\]

The continuity equation is preserved distributionally. Changing variables du=a(t)dt in the finite-energy action gives

\[
I_{A(T)}^0
=\frac1{2s}\int_0^T\!\int
\frac{[j+aD\rho_x]^2}{a\chi(\rho)}\,dx\,dt.          \tag{17}
\]

The portion of the independent base path after operational time A(T) is unobserved. Its minimum additional cost is zero: extend the terminal density by ordinary heat evolution and choose j^0=-D rho_x^0. Such a weak heat extension exists for every bounded terminal density and preserves the finite-energy interpretation. Conversely every finite-action preimage restricts to (17), so no cost is lost by this minimization.

The contraction principle therefore gives the **joint** rate for the retained macroscopic clock and visible path,

\[
I_T^{\rm joint}(\rho,j,A)
=\frac1{2s}\int_0^T\!\int
\frac{[j+A'D\rho_x]^2}{A'\chi(\rho)}\,dx\,dt+J_T(A). \tag{18}
\]

Eliminating A proves (2). Goodness follows from the good product rate and the continuous map, rather than being asserted from the integral alone. The clock bounds ensure equivalent finite-energy control before and after the change of variable.

If the recorded actual clock paths converge uniformly to a fixed A, the base-path contraction for these deterministic clocks gives the conditional rate (17), **without** J_T(A). The occupation cost is paid only when averaging over the fresh random clock. Thus retaining the clock is allowed, but conditioning on a rare clock record changes the relevant action in an explicitly known way.

## 6. Scalar transport and the fixed-mean obstruction

For a given A, the inherited scalar circulation rate at operational duration A(T) is q^2/[2vA(T)]. It can also be checked directly from (1): spatial Cauchy--Schwarz, the vanishing integral of rho_x and concavity of chi bound the cost below by the quadratic circulation cost, and rho=m with constant spatial current attains it. For an assigned total operational time Ta, convexity in (11) makes the least clock cost T ell_Q(a), achieved by the constant occupation speed a. This proves (4).

The inherited base proof also supplies quadratic exponential tail bounds for the supremum of circulation on a fixed time interval. Since the gated current is a base current observed before U=g_1T, these bounds transfer. They justify the unbounded linear Laplace principle for circulation; the SCGF is not inferred from a bare LDP without its moment condition. Taking the dual of (4), or first optimizing q at fixed a, gives

\[
\sup_q\{\lambda q-I_T^{\rm gate}(q)\}
=T\sup_a\{v\lambda^2 a/2-\ell_Q(a)\}
=T k_Q(v\lambda^2/2),                               \tag{19}
\]

which is (5).

Taking a=bar g in (4) proves the rate inequality
\(I_T^{\rm gate}(q)\le q^2/(2vT\bar g)\).
Equivalently, k_Q is convex, k_Q(0)=0 and k_Q'(0)=bar g, so
\(k_Q(h)\ge\bar g h\).
These are exact variational/Jensen obstructions, not perturbation theory. At bar g=1, no autonomous positive activity clock of this type can suppress equilibrium circulation relative to the unchanged mean-speed base process. The conclusion also holds for any independent positive clock with a zero-cost mean operational time and the stated joint LDP; it is not peculiar to two states.

For the symmetric choice r=l=b and g_0=1-d, g_1=1+d with 0<d<1,

\[
k_Q(h)=h-b+\sqrt{b^2+d^2h^2},
\]

\[
\Lambda_T^{\rm gate}(\lambda)
=T\left[\frac{v\lambda^2}{2}-b+
\sqrt{b^2+\frac{d^2v^2\lambda^4}{4}}\right].          \tag{20}
\]

Its small-lambda expansion is

\[
\Lambda_T^{\rm gate}(\lambda)
=\frac{vT\lambda^2}{2}+
\frac{Td^2v^2\lambda^4}{8b}+O(\lambda^8).             \tag{21}
\]

The SCGF curvature is unchanged; higher tails broaden. Large circulation preferentially uses the faster gate state. In particular, I(q) is asymptotic to q^2/(2vTg_1)+Tl up to a vanishing correction as |q| tends to infinity. This interpretation is the familiar switching-diffusivity mechanism, now connected by an exact operation to the unknown-kinetics base receiver.

## 7. A matched-ports ordinary deterministic comparator

The same two speed levels can be driven deterministically with the stationary duty fractions l/(r+l) and r/(r+l). Choose, for example, a physical cycle period proportional to N. There are order-N cycles on physical horizon N^2T, just as there are order-N stochastic gate transitions in the critical random program. The integrated operational clock differs from bar g t by at most O(1/N) on macroscopic time.

The same base path contraction then yields the deterministic speed-bar-g action and scalar rate q^2/(2vT bar g). No direct intermediate speed port is needed. Thus a competent ordinary controller with the same speed-level ports can choose whether to introduce broad rare tails or eliminate that extra source. Randomization does not beat deterministic scheduling at the goal of suppressing circulation at fixed mean activity.

These clock-event counts are not identical energy budgets. Both programs still require the uniform speed port, phase-strength synchronization and its actual switching fidelity. The deterministic result does not inherit any ability to pause the specimen.

## 8. An actual stationary CLT, supplied separately from the LDP

Here take the finite-state independent-sign base (7), a fixed particle count M_N/N->m, and the specified stationary law: uniform canonical occupancy times independent fair signs, for each fixed frozen z. This is an additional initial-law premise for this section, not a preparation inferred from the path LDP.

Let H_N be the physical total-current drift,

\[
H_N=c\sum_i\beta_i\delta_i\sigma_i,\qquad c=s/2.
\]

It is centered in the stationary law. Sign integration by parts for a linear test f gives

\[
|\langle H_N,f\rangle|
\le c\sqrt{N/2}\sqrt{D_{\rm sign}(f)}
\le c\sqrt{N/(2\gamma_N)}\sqrt{D_{B_N}(f)}.
\]

Therefore the inverse-energy norm satisfies

\[
\langle H_N,(-B_N)^{-1}H_N\rangle
\le c^2N/(2\gamma_N).                               \tag{22}
\]

The ordinary stationary forward/backward martingale inequality, also proved in the previous continuation's rotation note, bounds the expected squared supremum of its integral up to physical N^2U by 20N^2U times (22). After current-CLT scaling N^-3 this is O(1/gamma_N), tending to zero. This does not require a large visible spectral gap.

The compensated native total current is a martingale with bracket int sum_i r_i delta_i^2. The phase-dependent part of this bracket is treated by the same inverse-energy estimate. The remaining activity A=sum delta_i^2 has canonical mean 2M_N(N-M_N)/(N-1) and variance O(N). Stationarity and Jensen, without a temporal mixing estimate, show

\[
N^{-3}\int_0^{N^2t}\sum_i r_i\delta_i^2du
\longrightarrow s\chi(m)t
\]

uniformly in probability on a bounded interval. Native martingale jumps after scaling are bounded by N^-3/2. The martingale functional CLT, followed by the negligible drift integral, proves

\[
N^{-3/2}J^0(N^2t)\Rightarrow\sqrt v B_t.             \tag{23}
\]

The gate clock satisfies A_N->bar g t uniformly in probability. Continuous random time change of (23) therefore gives

\[
N^{-3/2}J(N^2t)\Rightarrow\sqrt{v\bar g}\,B_t.       \tag{24}
\]

The inverse-energy bound is uniform in the terminal time on [0,U], and the martingale second moments are uniformly bounded there. Conditioning on the independent A_N also gives convergence of the terminal variances to v bar g t. Thus at bar g=1 the actual stationary leading circulation variance is unchanged, even though the speed-N rare tails are different.

This CLT requires fresh future native and controller noise and the stated stationary initial joint law. An arbitrary exposed initial microscopic record is not silently substituted for it.

## 9. Genuine joint-correlation programming with identical marginal controllers

For a direct correlation comparison, take two physically separate specimens, each with its own inherited base process and its own unknown frozen amplitudes. They are actual separate systems with independent execution innovations, not microscopic copies of one hidden state. Let v_a=s_a chi(m_a), a=1,2.

Drive their speed ports either with the same common gate or with independent copies of the same gate law. Each specimen has exactly the same marginal controller and marginal native execution law in the two programs. At the same speed N,

\[
\Lambda_{\rm shared}(\lambda_1,\lambda_2)
=T k_Q\!\left((v_1\lambda_1^2+v_2\lambda_2^2)/2\right), \tag{25}
\]

whereas

\[
\Lambda_{\rm independent}(\lambda_1,\lambda_2)
=T k_Q(v_1\lambda_1^2/2)+T k_Q(v_2\lambda_2^2/2).    \tag{26}
\]

This follows from the product base actions and the common occupation contraction. The means and leading Gaussian cross-covariance remain zero. The mixed fourth derivative of (25), however, is

\[
\partial_{\lambda_1}^2\partial_{\lambda_2}^2
\Lambda_{\rm shared}(0,0)
=T k_Q''(0)v_1v_2
=\frac{2T\operatorname{Var}_{\pi_Q}(g)}{r+l}v_1v_2>0, \tag{27}
\]

while it vanishes in (26). Shared activity creates correlated rare transport bursts despite identical individual controller laws and without learning either specimen's hidden kinetic amplitudes. A finite multistate controller with a known speed vector per state similarly gives a finite matrix eigenvalue for a programmable collection of joint tails.

The hardware and synchronization cost of controlling two specimens is real. A shared source and two independent sources do not have equal wiring, randomness or switching-resource budgets automatically. The joint action with the coarse clock retained is supplied by (18); an LDP for every fine switching timestamp is not asserted.

## 10. Bandwidth regimes explain why this does not imitate a fast shared-sign gate

If the physical gate generator is epsilon_N Q instead of Q/N, its macroscopic rate is N^2 epsilon_N Q. Relative to speed N, the governing parameter is

\[
b_N=N\epsilon_N.                                    \tag{28}
\]

When b_N tends to a finite positive b, replace ell_Q by b ell_Q and k_Q(h) by the largest eigenvalue of bQ+h diag(g). The preceding proof is unchanged.

When b_N tends to infinity, the occupation clock is superexponentially concentrated at bar g t on speed N. Product contraction then yields precisely the deterministic mean-speed action. In particular a gate whose physical rate stays positive, or diverges, loses this rare-tail programming effect in the large-volume limit. A common clock becoming physically fast does not by itself recreate the root mechanism's suppression.

When b_N tends to zero but N b_N tends to infinity, the gate still makes many macroscopic transitions and its typical clock tends to bar g t. However its occupation deviations cost subexponentially in N. The speed-N scalar rate becomes q^2/(2vTg_1). This is an even stronger broadening at the same typical mean speed. The many-transition premise prevents confusing this regime with a random nonaveraged initial gate; no statement is made about exponentially tiny transition rates without a separate initial-law analysis.

These claims follow directly from the clock occupation estimate, or by taking the appropriate finite-matrix variational limit. They separate physical bandwidth, macroscopic bandwidth and the large-deviation speed.

## 11. Stronger feedback can suppress current, with extra ports and different behavior

The no-suppression statement is for an **autonomous clock independent of the base execution**. It does not exclude ordinary feedback supplied with extra operations.

For example, if a perfect global hold g=0 and continuous signed-current sensing really exist, choose an integer threshold h_N and stop all native evolution at the first time |J| reaches h_N. Since each native current jump is plus or minus one, the actual protocol obeys |J(t)|<=h_N at every later time. Taking h_N=o(N^2) suppresses every fixed nonzero macroscopic circulation without identifying hidden rates.

Under the stationary base used in Section 8, choose h_N=N^(3/2+e) rounded to an integer, with 0<e<1/2. The proved maximal second-moment bound is O(N^3), so the chance of activating the hold before physical N^2T is O(N^(-2e)). Typical trajectories are consequently unaltered with probability tending to one, while the rare current tail is clipped. This is a valid strong conventional comparator when its hold and sensing ports are supplied.

It has materially different physical and path consequences. It observes or accumulates signed native events at an order-N physical event rate, rather than using only an autonomous order-1/N gate clock. A counter needs order log h_N bits and a timely global stop. Once triggered it arrests the entire density evolution, rather than only a chosen circulation mode. Therefore it does not establish the desired unchanged full density/current action with only a rank-one fluctuation subtraction. Finite sensing/actuation latency also removes the literal finite-N bound unless its overshoot is separately controlled. Neither a hold nor native-event sensing is inferred from the positive speed port or the inherited phase bath.

## 12. Interpretation and primary comparison

The useful completed unit is an exact operation-to-action bridge: an actual common speed port plus a known finite-state controller transforms the inherited hidden-kinetics-free action into (2), with a finite spectral formula for terminal circulation and joint rare bursts. Its implementation and selection can be performed by an ordinary controller. The construction gives no new general theory of time change or switching diffusion.

Kraaij--Schlottke, *A large deviation principle for Markovian slow-fast systems*, [primary manuscript](https://arxiv.org/pdf/2011.05686), explicitly treats the competition of slow-variable deviations and fast occupation costs through a variational Lagrangian and principal eigenvalue. Its introduction and the two representations were read. That established framework is the conceptual incumbent; the present proof uses an exact time-change contraction rather than claiming its broad mechanism as new.

There are also close predecessors to the separate root idea of pairing opposite currents. Hexner--Levine, *Noise, diffusion, and hyperuniformity*, [primary manuscript](https://arxiv.org/pdf/1611.02386), [DOI](https://doi.org/10.1103/PhysRevLett.118.020601), studies center-of-mass-conserving equal/opposite kicks with ordinary mean diffusion but altered noise in a nonequilibrium setting. Morningstar--O'Dea--Richter, *Hydrodynamics in long-range interacting systems with center-of-mass conservation*, [primary manuscript](https://arxiv.org/pdf/2304.12354), [DOI](https://doi.org/10.1103/PhysRevB.108.L020304), explicitly uses separated equal/opposite pair currents, including diffusive regimes. Their physical models and conserved quantities differ from an exact reversible shared-sign compiler, but broad claims that pairing currents or engineering fluctuations through correlations are new would be untenable.

The present comparator changes selection in a precise way. Autonomous common activity randomness can program enhanced and correlated rare transport, but it cannot account for mode-specific suppression at unchanged mean diffusion. Ordinary threshold-and-hold feedback can suppress circulation but supplies a stronger hold/readout interface and changes the post-trigger density dynamics. Any proposed advantage for the event-updated gate must be stated against those actual alternatives, including their distinct timing, records and costs.
