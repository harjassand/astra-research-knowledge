# Astra 2026-10-08 upgrade: positive-temperature Maxwell profile and fast entanglement-witness onset

**This addendum supersedes only the explicit OPEN gate in Section E of RESEARCH_STATE_2026-10-08.md: the positive-temperature Maxwell crossover is now proved under the same ideal collective-jump model.** The exact N3 rational PPT/NPT counterexample and the Formanek obstruction in that record are unchanged. Research derivation and independent numerical/algebraic cross-checks; novelty/prior art and expert correctness review still open. Times `s=Gamma*t` assume unnormalized collective jumps `J_±`; if jump operators are `J_±/sqrt(N)` with fixed Gamma, multiply all physical times by N.

## New Theorem 1: universal **positive-temperature** Maxwell crossover

Let `N` spin-half qubits start from `I/2^N` and evolve by

`d rho/ds=(nu+1)D[J_-](rho)+nu D[J_+](rho)`, for ANY **fixed finite nu>=0**, with `D[L](rho)=Lrho L† - {L†L,rho}/2`. Let `rho_N(infty)` be the selected sector-preserving stationary state for that initial condition, and `D_N(s)=||rho_N(s)-rho_N(infty)||_1/2`. For ANY fixed `c>0`,

\[
\boxed{\lim_{N\to\infty}D_N\bigl(c\log N/\sqrt N\bigr) = F_{\rm Maxwell}\left(\frac{1}{2c}\right)}
\]

\[
F_{\rm Maxwell}(z)=\int_0^z\sqrt{\frac2\pi}\,x^2e^{-x^2/2}\,dx
=\operatorname{erf}(z/\sqrt2)-\sqrt{2/\pi}\,z e^{-z^2/2}.
\]

Both parity subsequences share the same limit, and, surprisingly, it is **independent of the fixed bath occupation nu**, including zero temperature. This is a macroscopic nontrivial crossover, **not** a sharp mixing cutoff in the conventional ratio-one sense. The earlier document proved this only for nu=0 and established the scale for nu>0; the following variance calculation closes that gap.

### Proof: exact passage-time second moments

The exact Schur-weighted TV formula and spin-sector birth-death rates are as in Section D of the original report. Write `M=2j`, `k=0,...,M`, `q=nu/(nu+1)` (so `q=0` for nu=0), `lambda_k=nu(M-k)(k+1)` and `mu_k=(nu+1)k(M-k+1)`. For `1<=k<=M` define `xi_k` as the first hitting time of `k-1` when starting from `k`. By the strong Markov property and the nearest-neighbor structure, the successive passage times `xi_x,...,xi_1` encountered on the way from `x` to `0` are **independent**, and `tau_0 = SUM_{k=1}^x xi_k` in distribution.

Detailed balance with `pi_k ∝ q^k` gives exactly

\[
a_k:=\mathbb E\xi_k = \frac{1-q^{M-k+1}}{k(M-k+1)}.
\]

For a function `h_x=E_x tau_0`, `g_x=E_x tau_0^2`, the killed-chain Poisson equations `(-Q)h=1`, `(-Q)g=2h` (acting on functions) yield

\[
g_k-g_{k-1} = \frac{2}{\mu_k\pi_k}\sum_{i=k}^M\pi_i h_i.
\]

Since `tau_k = xi_k + tau_{k-1}'` with independent terms, `g_k-g_{k-1}=E xi_k^2+2a_k h_{k-1}`. Substitute `h_i-h_{k-1}=a_k+SUM_{\ell=k+1}^i a_\ell` and use geometric pi. The **exact identity** is

\[
\boxed{\operatorname{Var}(\xi_k)=a_k^2+
\frac{2}{k(M-k+1)}\sum_{\ell=k+1}^M
q^{\ell-k}\bigl(1-q^{M-\ell+1}\bigr)a_\ell.}
\]

At `nu=0` this reduces to the exponential holding-time identity `Var xi_k=a_k^2`.

Fix `delta in (0,1/2)` and all `x in [delta M,(1-delta)M]`. Since `a_k <=1/[k(M-k+1)]` and `M-k+1>=delta M` for `k<=x`, the sum `SUM_{k<=x}a_k^2<=pi^2/(6 delta^2 M^2)`. For the extra variance term split the inner sum into `ell<=k+delta M/2` and `ell>k+delta M/2`. In the first range `a_ell<=2/(delta M k)` and `SUM_{ell>k}q^(ell-k)<=q/(1-q)=nu`, so contribution from all k is at most `4nu pi²/(6 delta² M²)`. In the far range `q^(ell-k)<=q^(delta M/2)` (for fixed nu>0) and `a_ell<=1`; summing geometric tails and the outer k gives an exponentially small `o(M^-2)` remainder. Therefore, UNIFORMLY in all typical starting levels,

\[
\operatorname{Var}_x(\tau_0)=\sum_{k=1}^x\operatorname{Var}(\xi_k)
=O_{\nu,\delta}(M^{-2}).
\]

Also the exact means satisfy

\[
\begin{aligned}
\mathbb E_x\tau_0&=\sum_{k=1}^x \frac{1-q^{M-k+1}}{k(M-k+1)}\\
&=\frac{H_x+H_M-H_{M-x}}{M+1}+O_{\nu,\delta}(q^{\delta M}\log M/M)\\
&=\frac{\log M+O_\delta(1)}{M},\qquad \delta M\le x\le(1-\delta)M.
\end{aligned}
\]

For nu=0 the geometric correction is exactly zero. Chebyshev and then `delta->0` imply

\[
\frac{M\tau_0}{\log M}\xrightarrow{\mathbb P}1
\]

under the **uniform initial distribution** on levels `0,...,M`. The same result holds for the first hitting time `tau_K` of any fixed level `K>=0`, since the discarded sum `SUM_{k=1}^K xi_k` has mean `O_{K,nu}(1/M)`.

For `s=alpha log M/M` with `alpha<1`, `Pr_u(tau_K>s)->1`. Thus the actual state has vanishing mass on levels `<=K` (one must first hit K to enter), while its geometric stationary distribution has mass at least `1-q^(K+1)`. Make K arbitrarily large to obtain `d_M(s)->1`.

For `alpha>1`, choose `eta>0` with `1+eta<alpha`. With probability `1-o(1)`, the chain hits 0 by `(1+eta)logM/M`. After this, the remaining interval has length at least `(alpha-1-eta)logM/M`; the sector spectral gap lower bound `c_nu M` and the chi-square bound `chi²(delta_0||pi)<=nu` from the original report make the remaining TV `O(M^{-c_nu(alpha-1-eta)})`, so `d_M(s)->0`. At nu=0, level0 absorbs, giving the same conclusion. Therefore, for **every** fixed nu>=0:

\[
\lim_{M\to\infty}d_M(\alpha\log M/M)
=\begin{cases}1,&\alpha<1,\\0,&\alpha>1.\end{cases}
\]

At `M=x sqrt N`, `s_N=c log N/sqrt N` has `M s_N / log M -> 2cx`. The exact Schur-weight measures for `x=M/sqrtN` converge (by local central-binomial CLT) to Maxwell density `sqrt(2/pi)x²e^-x²/2`; exceptional equality `x=1/(2c)` has zero limiting measure. Bounded sector TV plus tightness give the claimed integral. **QED.**

### Mechanism and verified finite checks

The surprising independence of nu comes from two ingredients that survive at any fixed finite temperature: (1) in high-spin typical sectors, the downward *net drift* of excited occupation is `-k(M-k)+O_nu(M)`, whose leading bulk part does not depend on nu, and (2) typical passage time to the low-energy boundary is `(logM)/M` with variance only `O(M^-2)`, while final local thermal equilibration occurs in `O(logM/M)` with any spare multiplicative constant. Temperature affects finite-size corrections, not the leading Maxwell critical surface.

`verify_hitting_moments.py` independently inverts killed generators for 5 nu values (including zero) and 8 sector sizes and matches the exact mean and variance recurrences: 40 finite tests **PASSED**. It also prints `M*SD(tau0)` bounded on M=100,300,1000,3000 with fixed nu, confirming the order but not replacing the proof. `check_positive_maxwell.py` numerically computes full sector sums at N16/32/64/96 for positive nu=.2,1 and c=.2/.5/1/2: finite-size progress towards the common Maxwell limit is slow and can come from either side. No large-N numerical claim is based on only these sizes.

## New Theorem 2: a faster, temperature-independent macroscopic polarization law

Retain the same ideal model and fix ANY finite nu>=0. Let `s_N=c/sqrt N` for a fixed `c>=0`. Then

\[
-\frac{\langle J_z\rangle_{s_N}}{\sqrt N}\to
P(c)=\int_0^\infty\sqrt{\frac2\pi}\,x^3e^{-x^2/2}
\left[\frac12-\mu(cx)\right]dx
\]

with

\[
\mu(z)=\int_0^1\frac{u}{u+(1-u)e^z}\,du
=\frac{ze^z-(e^z-1)}{(e^z-1)^2},\quad\mu(0)=1/2.
\]

This polarization law is also independent of nu at fixed temperature, and `P(c)` strictly increases from `0` to `sqrt(2/pi)`.

**Proof via the rescaled generator and martingale:** Condition on spin length `M=x sqrtN` with x in a compact positive interval, and define `y=k/M`. In rescaled time `c=s sqrt N`, its drift is *exactly*

\[
\frac{\lambda_k-\mu_k}{M\sqrt N}
=-\frac{M}{\sqrt N}y(1-y)
+\frac{\nu-(2\nu+1)y}{\sqrt N},
\]

and its quadratic-variation rate is `(lambda_k+mu_k)/(M² sqrtN)=O_nu(N^-1/2)` uniformly. Doob's martingale inequality and Lipschitz Gronwall imply uniform-in-compact-time convergence in probability to the ODE `dy/dc=-x y(1-y)` with initial `y(0)=u`, where the uniform initial levels give `u~Uniform[0,1]`. The deterministic solution is `y(c)=u/[u+(1-u)e^(xc)]`. Spin magnetization in that sector is `m=M(y-1/2)`. Average over the Maxwell limiting spin distribution, using uniform integrability of `M/sqrt N` from conserved `E[J²]=3N/4`, to get the formula. Strict monotonicity follows because y(c) is strictly decreasing in c for 0<u<1, x>0. QED.

## New Corollary: faster collective-spin entanglement certificate

The exact Casimir `J²` is conserved by the collective jump Lindbladian and has `E[J²]=3N/4` initially and at all times. Every FULLY separable N-qubit state obeys the spin-squeezing inequality `Var J_x+Var J_y+Var J_z >= N/2`, hence for this axially symmetric trajectory, **M_N(s):=-E[J_z](s) > sqrtN/2 suffices for entanglement**: its spin-variance sum is `3N/4-M_N(s)² <N/2`.

Define the universal constant `c_*` as the unique solution to `P(c_*)=1/2`; numerical deterministic quadrature gives

\[
\boxed{c_*\approx 1.22681373253.}
\]

For **every fixed finite nu>=0 and every c>c_***, the maximally mixed initial state evolved to time `s_N=c/sqrtN` is **provably non-fully-separable for all sufficiently large N** (in this ideal model). For c<c_*, this particular variance witness does not detect entanglement asymptotically; it is **not** a proof of separability or of an exact intrinsic entanglement-onset threshold.

The model therefore has *two parametrically separated dynamical scales*: collective-spin detectable entanglement arises at `s=Theta(1/sqrtN)`, whereas full selected-stationary-state trace-distance relaxation has a Maxwell crossover at `s=Theta(logN/sqrtN)`. For normalized collective jump operators `J_±/sqrtN`, both physical times are multiplied by N, becoming respectively `Theta(sqrtN/Gamma)` and `Theta(sqrtN logN/Gamma)`: **no energy-normalization-free speedup is claimed**.

**Measurement interface:** measure `J_z` and the three collective second moments `J_a²` on separately prepared states (a different collective axis per batch), test `sum_a Var J_a<N/2`. Because `J²` is conserved and `E[(J²)²]=O(N²)` for maximally mixed spin-half input, both `J_z/sqrtN` and `J_a²/N` have bounded variances, so a constant witness margin can be resolved with `O(eps^-2 log(1/delta))` ideal independent preparations and `O(N eps^-2 log(1/delta))` elementary spin readouts if global axis measurements are available. Real collective dissipator calibration, finite-size corrections (nonuniform when nu grows with N), J² conservation under noise, detector precision and wall-clock collective coupling resource are charged, not presumed. For large enough N, single-qubit Bloch magnetization is only `O(N^-1/2)`; two-qubit pair correlations (from collective second moments and permutation invariance) are also `O(N^-1)` even while this global witness detects entanglement. This is global multipartite entanglement, not proven genuine N-party depth nor quantum advantage.

**Verification:** `macroscopic_polarization.py` integrates P(c) and solves `c_*=1.2268137325306523`, returning P(2)=0.65007540794, P(infinity)=sqrt(2/pi)=0.7978845608. Independent finite-N exact sector matrix exponentials in `check_polarization_finiteN.py` show approaches toward universal P(c) for nu .2, 1, 10; ν10 convergence is much slower at N<=96, consistent with fixed-nu-before-N quantifier. These checks are illustrations, not proofs.

## New high-upside directions and proof status

1. **Physical design target**: engineer global collective thermalization with precisely calibrated J± couplings; measure temperature-independent macroscopic spin polarization onset; compare fixed-ν finite-size corrections. Assess power/bath cost with actual scaling of Γ and jump normalization before claims of practical advantage.
2. **New research question**: characterize the full entanglement phase diagram on c/sqrtN, beyond spin-variance witness. The c_* above marks only a *witness threshold*. Fully separable vs biseparable vs genuine multipartite entanglement and distillation remain independent questions.
3. **Universality challenge**: determine which perturbations preserve Maxwell crossover and polarization laws—nonuniform coupling, local dephasing, ν=ν(N), prepared nonuniform Schur weights. The proofs show exactly which assumptions are critical: conserved spin sectors and Haar/Maxwell j distribution, quadratic birth/death rates, and fixed finite ν.
4. **Prior art is not cleared**. These are new self-contained candidate research results from this run, not verified field-breaking or publication-ready novelty. Specialist scrutiny is required, and older papers may already imply variants. No independent proof assistant used. False routes and parameter caveats above are retained.