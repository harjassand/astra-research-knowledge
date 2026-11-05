# Direct boundary experiments for a rare-event intervention decision

**Completed construction supplied to the root selection, 5 November 2026.** This note concerns only the newly selected intervention mechanism. The separate quantum construction in this directory and all earlier originals are preserved.

At fixed accuracy and sufficiently large N in the uniformly biased singleton family, a direct boundary-flux experiment needs no simulated trajectory, learned transition table, or numerical failure probability. A stopped-return experiment remains useful when the explicitly bounded clump correction is too large to ignore.

The direct branch also avoids constructing an experimental fixed-lag Markov kernel. Its proof uniformizes the **true operating generator** mathematically; its physical experiments use finite holds only to bound one scalar escape intensity. Coarse bounded timing errors can be handled at the decision level, without requiring a stationary experimental kernel or accumulating per-update clock error.

## 1. True model and the decision

For menu item u, let the true operating generator on {0,1}^N be

\[
Q^u=\sum_{i=1}^N Q_i^u,
\qquad Q_i^u=r_i^u(s)(H_i-I).
\tag{1}
\]

The declared context s excludes the focal bit i. The heat-bath kernel H_i replaces bit i by a Bernoulli variable with probability q_i(s) of 1. The operating clock r_i^u(s) is the same for both starting values of bit i. Assume the q_i are compatible with a strictly positive law pi. Thus every item u is reversible for the **same** pi. Suppose

\[
0<q_i(s)\le\bar q<1/2,
\qquad 0<r_{\min}\le r_i^u(s)\le r_{\max},
\tag{2}
\]

and a common continuous-time spectral-gap lower bound gamma>0 is supplied or validly acquired. These bounds concern the actual operating settings. Artificial-bias clocks are not substituted for them.

Let b=(1,...,1), A={0,1}^N minus {b}, p=pi(b), and let M_u be the mean first hitting time of b from pi conditioned on A. The task is to choose a budget-feasible u with M_u within a prescribed multiplicative factor of the largest M_u. Known deployment costs can define the feasible menu. An additive objective combining M_u with a monetary quantity of unrelated, unknown scale is a different task.

The common invariant law is a structural property of reciprocal intervention mechanics (1). Failure to detect differences between estimated q_i^u does not establish it. If interventions change q_i, the cancellation below need not hold; small local changes can accumulate in p.

## 2. An analytical kernel that is never simulated

Put

\[
R=Nr_{\max},\quad P_u=I+Q^u/R,\quad g=\gamma/R.
\tag{3}
\]

Each -Q_i^u is self-adjoint and positive semidefinite in L^2(pi). On a fixed-neighbor two-state block its eigenvalues are 0 and r_i^u(s). Hence

\[
0\preceq-Q^u\preceq Nr_{\max}I.
\]

P_u is a reversible stochastic positive-semidefinite kernel. Its nonconstant eigenvalues lie in [0,1-g]. A valid smaller g can be used. Define

\[
S_u=\sum_{t=0}^{\infty}(P_u^t(b,b)-p),\quad
q_{0,u}=1-P_u(b,b),\quad
\lambda_u=-Q^u(b,b)=R q_{0,u}.
\tag{4}
\]

The standard singleton Green identity is

\[
\boxed{M_u={S_u\over R p(1-p)}
={B_u\over\lambda_u p(1-p)},\qquad B_u=q_{0,u}S_u.}
\tag{5}
\]

The numerical value of p is unnecessary for ranking the M_u: it is common. The direct procedure bounds B_u and measures lambda_u. P_u and S_u are only analytical objects; no matrix, trajectory, uniformization clock, or return simulation is constructed.

## 3. A finite interval for the clump factor

Let w(x) be the number of zeros and let a=qbar/(1-qbar)<1. Sequential conditioning and single-bit weight ratios give

\[
p\le p_+:=\bar q^N,\qquad
{\pi(b)\over\pi(x)}\le a^{w(x)}.
\tag{6}
\]

A conditional probability given only some bits is an average of the full conditional, so it remains at most qbar. Turning the zero bits of x into ones multiplies its weight by conditional odds at most a. No independence is assumed.

### 3.1 Resolvent lower bound

Let f=1_b-p. On the mean-zero space,

\[
\langle f,f\rangle_\pi=p(1-p),\quad
\langle f,(I-P)f\rangle_\pi=pq_0,\quad
\langle f,(I-P)^{-1}f\rangle_\pi=pS.
\]

Cauchy–Schwarz gives

\[
\boxed{B=q_0S\ge(1-p)^2\ge(1-p_+)^2.}
\tag{7}
\]

This is exact, with no rare-event approximation.

### 3.2 Superharmonic escape construction

Fix 2<=k<N. At a state with 1<=w<k,

\[
P(w\to w+1)\ge{N-w\over N}A_0,
\quad A_0={r_{\min}\over r_{\max}}(1-\bar q),
\]

\[
P(w\to w-1)\le{w\over N}D_0,
\quad D_0=\bar q.
\tag{8}
\]

Set C=D_0/A_0 and

\[
R_0=1,\quad
R_j=\prod_{\ell=1}^{j}{C\ell\over N-\ell},
\quad
F(w)={\sum_{j=w}^{k-1}R_j\over\sum_{j=0}^{k-1}R_j}.
\tag{9}
\]

Then F is decreasing, F(0)=1, F(k)=0, and

\[
{N-w\over N}A_0[F(w+1)-F(w)]
+{w\over N}D_0[F(w-1)-F(w)]=0.
\]

The larger actual upward probability and smaller actual downward probability make F(w(X_t)) a supermartingale until hitting {0,k}. The chain need not be lumpable by w. Bounded optional stopping proves

\[
\Pr_x(\tau_b<\tau_k)\le F(1)
={\sum_{j=1}^{k-1}R_j\over1+\sum_{j=1}^{k-1}R_j},
\qquad w(x)=1.
\tag{10}
\]

If rho=Ck/(N-k)<1, then R_1=C/(N-1) and R_j<=R_1 rho^{j-1}. Thus, after the first departure from b, the probability alpha of returning before layer k obeys

\[
\boxed{\alpha\le\zeta:={C\over(N-1)(1-\rho)}.}
\tag{11}
\]

The sharper finite sum F(1) can replace zeta. Its uniformity over neighbors of b removes any need to know the departure distribution. A bound below one is required.

### 3.3 The visit-count identity and spectral remainder

Starting at b, count all visits to b before tau_k, including time zero and holding steps. A consecutive holding block at b has mean length 1/q0; each departure returns before layer k with probability alpha. Strong Markov regeneration therefore yields

\[
\mathbb E_b\sum_{t<\tau_k}1_{\{X_t=b\}}
={1\over q_0(1-\alpha)}
\le{1\over q_0(1-\zeta)}.
\tag{12}
\]

This identity is used only in the proof; these visits are not experimentally simulated.

Reversibility gives P^t(x,b)=(pi(b)/pi(x))P^t(b,x)<=a^k at layer k. By strong Markov, visits after tau_k and before an integer L have expected count at most L a^k. Therefore

\[
\sum_{t=0}^{L-1}P^t(b,b)
\le{1\over q_0(1-\zeta)}+La^k.
\tag{13}
\]

Positive semidefiniteness and gap g give

\[
0\le\sum_{t=L}^{\infty}(P^t(b,b)-p)
\le{e^{-gL}\over g}.
\tag{14}
\]

Subtract Lp, discard this nonpositive term, and use q0<=1. The result, uniform across interventions, is

\[
\boxed{b_-\le B_u\le b_+,\quad
b_-=(1-p_+)^2,\quad
b_+={1\over1-\zeta}+La^k+{e^{-gL}\over g}.}
\tag{15}
\]

The sharper upper bound keeps q0 multiplying the last two terms. Every term in (15) comes from coarse certificates, without estimating p.

### 3.4 Finite acceptance schedule

For v>0 choose

\[
L=\max\{1,\lceil g^{-1}\log(1/(vg))\rceil\},
\quad
k=\max\{2,\lceil\log(L/v)/\log(1/a)\rceil\}.
\tag{16}
\]

Check k<N, rho<1 and zeta<1, then evaluate b_+/b_-. A stronger easy sufficient check is

\[
p_+\le v,\qquad\zeta\le v.
\tag{17}
\]

The two remaining terms in b_+ are then at most v by construction. At fixed gamma, qbar, rate contrast and v, g=Theta(1/N), L=O(N log N), k=O(log N), and zeta=O(1/N). Thus the certificate succeeds for all sufficiently large N. L and k are certificate arithmetic, not experiment lengths.

If this interval is too broad, the branch must return unresolved or invoke the separately proved stopped-return procedure. Accuracy much smaller than 1/N can need that correction. Small symmetric cases may have better exact solvers.

## 4. Direct finite local experiment

For item u, choose i uniformly from {1,...,N}. On a faithful local copy under the actual operating setting u, pin its declared neighbors to 1, initialize focal bit i to 1, release the focal bit, and read it at a time T in [h_-,h_+], where h_-=h(1-omega), h_+=h(1+omega). Output Y=1 if it is zero. Only the bounded local context is prepared, not the full N-bit state b.

For the fixed context, let

\[
\lambda_{1,i}=r_i^u(s_b)(1-q_i(s_b)),\quad
\lambda_{0,i}=r_i^u(s_b)q_i(s_b).
\]

The true local process remains this two-state CTMC throughout the hold. The observation service must not alter its operating generator before the endpoint in an unmodeled way.

### 4.1 A bound that even permits within-trial adaptive timing

If Y=1, at least one jump out of 1 occurred by h_+. Hence

\[
\Pr(Y=1\mid i)\le\lambda_{1,i}h_+.
\]

On the event that the first jump occurs by h_- and there is no second jump until h_+, the state is zero at **every** possible read time T in the allowed interval. This event has probability

\[
\int_0^{h_-}\lambda_{1,i}e^{-\lambda_{1,i}s}
e^{-\lambda_{0,i}(h_+-s)}ds
\ge\lambda_{1,i}h_-e^{-r_{\max}h_+}.
\tag{18}
\]

Therefore these bounds hold even when the read time adapts to the current focal path, provided it stays in the stated interval and does not change the path law. No stopping-time identity or semigroup evaluated at an endogenous random time is used.

Define

\[
\theta_u={h\over N}\lambda_u,
\quad\theta_{\min}=h r_{\min}(1-\bar q),
\quad
\kappa_-=(1-\omega)e^{-r_{\max}h(1+\omega)},
\quad\kappa_+=1+\omega.
\tag{19}
\]

Uniform random coordinate selection and (18) give, conditional on every prior history,

\[
\boxed{\kappa_-\theta_u\le
\mathbb E[Y\mid\mathrm{past}]
\le\kappa_+\theta_u.}
\tag{20}
\]

For exogenous holding times independent of this trial's jump noise, the exact endpoint formula is
\((1-q_i)(1-e^{-r_iT})\). In that narrower case one may sharpen kappa_- to
\((1-\omega)\phi(r_{\max}h(1+\omega))\), with \(\phi(x)=(1-e^{-x})/x\). That semigroup formula must not be asserted for adaptive read times; (18) covers them with the weaker constant.

No experimental P_h or symmetry of holding times between source bits is needed. Only the true operating Q has to satisfy the common-invariant structure. No artificial-bias clock is transported.

### 4.2 Conditional service errors

If the combined per-trial pin, initialization, detector and random-address error changes the conditional mean by at most beta, then

\[
\kappa_-\theta_u-\beta\le
\mathbb E[Y\mid\mathrm{past}]
\le\kappa_+\theta_u+\beta.
\tag{21}
\]

Repeated cells and errors may be dependent. The envelope must hold after every history; a marginal one-shot calibration error does not establish it. A random-coordinate distribution at conditional TV distance beta_sel from uniform contributes at most beta_sel to beta. Focal/neighbor pin failure probabilities and detector bias similarly add.

If endpoint uncertainty or a finite read gate can change the answer only when a jump occurs in an additional time interval of total length d_gate, its contribution is at most r_max*d_gate. Any invasive read interaction or read-before-pin race needs its own service envelope. A clock counter alone does not certify the actual physical interval. All calibration and service costs remain payable.

## 5. Finite confidence without per-call union accuracy

Choose 0<eta<=1/4 and require

\[
\beta\le\eta\kappa_-\theta_{\min}.
\tag{22}
\]

Then the conditional means lie between
\(m_-=(1-\eta)\kappa_-\theta_u\) and
\(m_+=(1+\eta)\kappa_+\theta_u\). Take, for each of K items,

\[
\boxed{m\ge{3\over\eta^2\kappa_-\theta_{\min}}
\log{2K\over\delta}.}
\tag{23}
\]

With probability at least 1-delta, simultaneously for every item,

\[
\boxed{(1-\eta)^2\kappa_-\theta_u
\le\overline Y_u\le
(1+\eta)^2\kappa_+\theta_u.}
\tag{24}
\]

**Concentration proof.** For any 0<=Y<=1,
\(\mathbb E[e^{tY}\mid\mathcal F]\le1+\mathbb E[Y\mid\mathcal F](e^t-1)\).
For t>0 insert the upper mean m_+; for t<0 insert the lower mean m_-. Iterate this inequality. It gives the ordinary Bernoulli/Poisson upper Chernoff exponent at least m*eta^2*m_+/3, and the lower exponent at least m*eta^2*m_-/2. The former is at least log(2K/delta) by (23). The latter is at least (3/2)(1-eta)log(2K/delta), also sufficient for eta<=1/4. A union bound gives (24). Conditional dependence is permitted throughout. QED.

The two powers of (1+-eta) in (24) are intentional: one pays the decision-level service bias, the other the statistical fluctuation. Dropping a power while retaining (22)–(23) would overstate the confidence interval.

Beta is set by decision tolerance, not delta divided by the number of future uses. There is no requirement of per-use total-variation accuracy inversely proportional to a path length or number of experiments. The physical device must nevertheless earn its uniform conditional-mean envelope, with actual calibration exposure and confidence.

## 6. Decision and exact regret factor

Let \(F_0=h/[Np(1-p)]\), an unknown common constant. Combining (5), (15) and (24),

\[
{b_-(1-\eta)^2\kappa_-\over\overline Y_u}
\le{M_u\over F_0}
\le{b_+(1+\eta)^2\kappa_+\over\overline Y_u}.
\tag{25}
\]

On the confidence event the empirical means are positive. A zero empirical mean can instead yield an unresolved report; it is not evidence of infinite lifetime.

Choose an item \(\widehat u\) with smallest empirical mean. Then

\[
\boxed{M_{\widehat u}\ge{1\over\mathcal R}\max_u M_u,
\quad\mathcal R={b_+\over b_-}
\left({1+\eta\over1-\eta}\right)^2
{\kappa_+\over\kappa_-}.}
\tag{26}
\]

No p, partition function, or absolute rare-event time is needed by the decision.

For a simple explicit allocation let 0<epsilon<=1/2 and set
\(v=\eta=\omega=\epsilon/32\), \(h=v/r_{\max}\). Use (16) and require (17). Since v<=1/64,

\[
\kappa_-=(1-v)e^{-v(1+v)}\ge1-2v,
\quad\kappa_+/\kappa_-\le1+4v,
\]

\[
b_+/b_-\le1+8v,
\quad(1+\eta)/(1-\eta)\le1+3v.
\]

Consequently

\[
\mathcal R\le(1+8v)(1+4v)(1+3v)^2
=1+18v+113v^2+300v^3+288v^4
\le1+20v<1+\epsilon.
\tag{27}
\]

The exact computable ratio (26) is less conservative.

If actual preparation gives \(e^{-\xi_u}\le d\nu_u/d\pi_A\le e^{\xi_u}\), then the deployed mean is between \(e^{-\xi_u}M_u\) and \(e^{\xi_u}M_u\). With common xi, (26) becomes a factor \(e^{2\xi}\mathcal R\) against the best similarly prepared deployment. Total variation alone does not control this unbounded mean. Preparation failure, abort, initialization and deployment retain their actual costs and meanings; an abort is not assigned an infinite lifetime. The safe mass is at least 1-qbar^N>1/2, but achieving a density envelope still costs real preparation.

## 7. Full resource interpretation

At fixed qbar, rate contrast, physical gap, accuracy, menu size and confidence, the number of post-certificate local endpoint experiments is independent of N. Site addressing still uses O(log N) bits, and actual routing/propagation has its own physical cost. L and k are certificate arithmetic only.

With the explicit allocation, the experiment count is

\[
O\left(K{r_{\max}\over r_{\min}(1-\bar q)}
\epsilon^{-3}\log(K/\delta)\right),
\tag{28}
\]

and total focal hold exposure is

\[
O\left(K{1\over r_{\min}(1-\bar q)}
\epsilon^{-2}\log(K/\delta)\right).
\tag{29}
\]

Pin/read/reset service is additional and is multiplied by the actual trial count. Per-trial conditional mean error in (22) is of order epsilon^2*r_min/r_max, independent of N and the total number of future calls. A bounded-degree context needs at most a fixed number of neighbor pin channels per hold. A random-site generator with a finite cap can charge its conditional distribution error directly in beta.

Not removed: declared model closure; faithful local copies; actual operating intervention access; acquisition of common coarse qbar/r_min/r_max/gamma certificates; calibrated acquisition fields; uniform repeated-use pin/read guarantees; local gate/timing error; site addressing and propagation; installation of the intervention; and safe preparation. At fixed degree there are O(NK) local contexts to certify, but simultaneous confidence normally adds a log(NK/delta) factor to their sampling/exposure. O(N) contexts must not be mislabeled as exactly O(N) finite-confidence observations.

An N-address physical bank can have growing fabrication and communication cost. Constant post-certificate **local experiment count** is not constant end-to-end wall time or hardware. All comparators receive the same faithful-context, actuation, readout and preparation access.

## 8. Strong applicable primary approaches

The Green identity, clump correction, reversible capacities and target-local simulation are established machinery. The ordinary comparator cannot be restricted to waiting for catastrophe or reconstructing a complete marked-path law.

**Jackson Loper, Guangyao Zhou and Stuart Geman, “Capacities and efficient computation of first-passage probabilities,” Physical Review E 102, 023304 (2020), published 10 August 2020, DOI 10.1103/PhysRevE.102.023304.** Full primary author PDF read:
https://stanniszhou.github.io/papers/diffusion_manuscript.pdf
Publisher PDF read:
https://journals.aps.org/pre/pdf/10.1103/PhysRevE.102.023304
Earlier preprint, titled *Capacities and the Free Passage of Entropic Barriers*:
https://arxiv.org/abs/1811.00205

They estimate rare-target splitting probabilities from simulations confined to target neighborhoods, with finite error controlled by an epsilon-flatness condition. Their paper explicitly eliminates the temporal process and does not recover the overall first-passage-time scale (published page 023304-3, introductory discussion before Section II). The relevant new interface here is that exactly common invariant weights make that unknown scale cancel between kinetic interventions, while (15) and actual local operating experiments earn a finite multiplicative mean-lifetime decision. Local rare-event inference itself is not new.

**Aldous and Fill, *Reversible Markov Chains and Random Walks on Graphs*, Chapter 3.7:**
https://www.stat.berkeley.edu/~aldous/RWG/Book_Ralph/Ch3.S7.html
The excursion/capacity and extremal mean-hitting identities are established there. No novelty is claimed for them.

**Russo, Copperman, Zuckerman, Aristoff and Simpson, *Unbiased estimation of equilibrium, rates, and committors from Markov state model analysis* (2021):**
https://www.math.colostate.edu/~aristoff/unbiased_MSM.pdf
This primary full text discusses the importance of correct source-sink/absorbing boundaries and initialization for first-passage estimates. The direct branch here does not coarse-grain a trajectory or learn a lagged transition matrix. It should not imply that all Markov-state or milestoning methods require lifetime-sized trajectories.

The direct branch is stronger than the proposed polylog-N return probe at fixed accuracy in this uniformly biased singleton family. The return branch remains an accuracy refinement when (15) is unresolved. The earned consequence is a fully scoped acquired relative intervention decision without absolute-rarity learning, trajectory generation, or tiny per-call timing errors. No historical-priority or optimal same-access lower-bound claim is established by this note.

## 9. Additional cautions for the return fallback

- A visit-count formula A(A-1)^{j-1} is for E[binom(V,j)]; a falling factorial moment needs j!. Lower-tail concentration requires a separate argument.
- A cap exp[-(nu*J-k)^2/(2J)] requires nu*J>=k, or a positive-part exponent. The denominator uses the centered increments' range length two.
- The experimental-kernel fallback needs fixed context-specific holding times or a repeatable conditional holding-time law shared by the two focal bits, apart from explicitly coupled service errors. Bounded arbitrary history dependence alone does not define one homogeneous reversible P_h. The direct branch avoids that requirement.
- The singleton, uniform conditional bias, reciprocal mechanics and gap promises are substantive. This is not a theorem for arbitrary network disconnection sets, field interventions, hidden catastrophes, cascades or unknown state spaces.

This note is a completed analytical construction. No physical trials or new numerical simulations are claimed.
