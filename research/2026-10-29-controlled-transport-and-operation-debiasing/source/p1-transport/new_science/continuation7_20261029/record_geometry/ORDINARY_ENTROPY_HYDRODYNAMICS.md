# Ordinary entropy route to controlled hydrodynamic trajectories

**Role:** complementary constructive comparator for Astra P1, continuation 7.  
**Date:** 2026-10-29.  
**Status:** proved below at the stated model interface. This is an application of established entropy, Feynman–Kac, and martingale methods; it is not a priority claim for a new hydrodynamic principle. It does not prove the stronger fluctuation-field or dynamical large-deviation results being developed separately by the root role.

## 1. Conclusion and the exact interface that supplies it

An autonomous, independently driven phase coordinate on each bond can remove bounded hidden kinetic modulation from the empirical-density trajectory on every fixed macroscopic time interval. In the model below, it is enough that the physical phase rate `kappa_N` tend to infinity, however slowly. No lower bound on the visible spectral gap, no locality of the modulation's dependence on the visible configuration, and no statistical law for frozen disorder are needed.

The averaged process is already the gradient symmetric exclusion process. This fact is decisive: after the phase-dependent drift has been removed, the empirical density equation closes without an occupation one-block or two-block theorem. Consequently, this mean-density result is a relatively ordinary analytical comparator for the more demanding density/current path-action question.

The required interface is substantial. The baseline jump rate has an exactly known common mean, the modulation is invariant under its own bond swap, and independent phase Brownian motions are actual available operations. Arbitrary unknown rates with a small acquired equilibrium error do not automatically have this structure.

## 2. Model and reference measure

Fix a spatial dimension `d`. On the discrete torus

\[
\Lambda_N=(\mathbb Z/N\mathbb Z)^d,\qquad V=N^d,
\]

let `eta_x` be an exclusion occupation in `{0,1}`. Represent each unoriented nearest-neighbor bond once, as `b=(x,x+e_j)`; there are `d V` bonds. Let `eta^b` denote the swapped configuration. A phase `theta_b` on the circle is attached to each bond. A frozen parameter `z` can contain arbitrarily much hidden information.

For constants `s>0` and `0<=a_0<=1`, assume

\[
|\alpha_b(\eta,z)|\le a_0,\qquad
\alpha_b(\eta^b,z)=\alpha_b(\eta,z).
\tag{1}
\]

The amplitudes may depend on the entire visible configuration and on `N`; they need not be translation covariant. They are independent of all phases. Define

\[
c_b(\eta,\theta,z)
=\frac{s}{2}\bigl[1+\alpha_b(\eta,z)\cos\theta_b\bigr].
\tag{2}
\]

The physical generator and its diffusive acceleration are

\[
\mathcal L_N f
=\sum_b c_b(f(\eta^b,\theta)-f(\eta,\theta))
 +\kappa_N\sum_b\partial_{\theta_b}^2f,
\qquad L_N=N^2\mathcal L_N.
\tag{3}
\]

Native jumps leave every phase and `z` unchanged. The phase process has independent Brownian increments and is autonomous even while the native dynamics is running. The convention in (3) gives a circle spectral gap of one before multiplication by `kappa_N`.

For each fixed `z`, take as a mathematical reference measure

\[
\mu_N=\operatorname{Ber}(1/2)^{\otimes V}
       \otimes\operatorname{Haar}^{\otimes dV}.
\tag{4}
\]

It need not be a physically supplied initial preparation. Its mixture over conserved particle sectors causes no difficulty. Assumption (1) makes the visible jump part reversible for (4), at every fixed phase configuration. The phase bath is also reversible for (4). With

\[
D_{\rm vis}(f)=\frac12\sum_b\int c_b|f^b-f|^2\,d\mu_N,
\qquad
D_\theta(f)=\sum_b\int|\partial_{\theta_b}f|^2\,d\mu_N,
\tag{5}
\]

the Dirichlet identity is

\[
-\langle f,L_N f\rangle
=N^2D_{\rm vis}(f)+N^2\kappa_ND_\theta(f).
\tag{6}
\]

All estimates below are uniform in the frozen value `z` and the allowed amplitudes. The finite visible state space, compact phase space, bounded jump coefficients, and elliptic phase diffusion provide the ordinary Markov and closed-form constructions used below.

## 3. Exact drift and the phase-energy estimate

For a smooth real test function `G` on the continuous torus, write

\[
\pi^N(G)=\frac1V\sum_xG(x/N)\eta_x.
\]

Let `Delta_N` be the usual discrete Laplacian including its factor `N^2`. Summation by parts gives the exact identity

\[
L_N\pi^N(G)=\frac{s}{2}\pi^N(\Delta_NG)+F_N^G,
\tag{7}
\]

where

\[
F_N^G=\sum_bu_b(\eta,z)\cos\theta_b,
\]

\[
u_{(x,x+e_j)}=
\frac{sN^2}{2V}[G((x+e_j)/N)-G(x/N)]
(\eta_x-\eta_{x+e_j})\alpha_b(\eta,z).
\tag{8}
\]

Define

\[
C_G=\frac{s^2a_0^2}{4}\sum_{j=1}^d\|\partial_jG\|_\infty^2,
\qquad
L_G=\frac{sa_0}{2}\sum_{j=1}^d\|\partial_jG\|_\infty.
\tag{9}
\]

The following are deterministic, pointwise bounds:

\[
\sum_bu_b^2\le C_G\frac{N^2}{V},
\qquad
\|F_N^G\|_\infty\le L_GN.
\tag{10}
\]

For a real normalized form-domain function `f`, integration by parts in the phase coordinates gives

\[
\langle F_N^G,f^2\rangle
=-2\sum_b\int u_b\sin\theta_b\,f\partial_{\theta_b}f\,d\mu_N.
\tag{11}
\]

There is no derivative of `alpha_b`: the integration is in `theta_b`, while `u_b` depends only on `eta,z`. Cauchy–Schwarz and (10) imply

\[
|\langle F_N^G,f^2\rangle|
\le 2\sqrt{C_G}\frac{N}{\sqrt V}\sqrt{D_\theta(f)}.
\tag{12}
\]

For every real `gamma`, completing the square in `sqrt(D_theta)` yields

\[
\sup_{\|f\|_2=1}
\{\gamma V\langle F_N^G,f^2\rangle+\langle f,L_Nf\rangle\}
\le \frac{\gamma^2C_GV}{\kappa_N}.
\tag{13}
\]

The visible Dirichlet form was merely discarded in this estimate. In particular, no positive lower bound on it was needed, and the endpoint case `a_0=1` is permitted here.

The ordinary Feynman–Kac variational estimate therefore gives

\[
\mathbb E_{\mu_N}
\exp\left\{\gamma V\int_0^tF_N^G(X_u)\,du\right\}
\le \exp\left\{\frac{\gamma^2C_GVt}{\kappa_N}\right\}.
\tag{14}
\]

This calculation is the useful constructive core. It avoids differentiating the potentially nonlocal visible dependence of the modulation.

## 4. Uniform replacement on a fixed macroscopic interval

Put `A_t^G=int_0^t F_N^G(X_u)du`, and fix `T<infinity` and `epsilon>0`. When `C_G>0`, Chernoff's inequality applied to (14) gives, for `t<=T`,

\[
\mathbb P_{\mu_N}(|A_t^G|\ge\epsilon)
\le 2\exp\left\{-\frac{\kappa_NV\epsilon^2}{4C_GT}\right\}.
\tag{15}
\]

Use a deterministic time grid of mesh at most `epsilon/(2 L_G N)`. Since (10) controls the variation between grid points, with

\[
K_N=2+\left\lceil\frac{2L_GNT}{\epsilon}\right\rceil
\]

one obtains

\[
\mathbb P_{\mu_N}
\left(\sup_{0\le t\le T}|A_t^G|\ge\epsilon\right)
\le 2K_N\exp\left\{-\frac{\kappa_NV\epsilon^2}{16C_GT}\right\}.
\tag{16}
\]

If `C_G=0`, then `F_N^G=0`, so all replacement assertions hold exactly and no division by `C_G` is used.

### 4.1 Relative-entropy initial data

Suppose an initial law `nu_N` satisfies

\[
H(\nu_N\mid\mu_N)\le hV.
\tag{17}
\]

The corresponding path laws have the same relative entropy: the transition mechanism is unchanged. For any event `E`, binary relative entropy implies

\[
\mathbb P_{\nu_N}(E)
\le\frac{H(\nu_N\mid\mu_N)+\log2}
{\log(1/\mathbb P_{\mu_N}(E))}.
\tag{18}
\]

Applying (16) gives

\[
\mathbb P_{\nu_N}
\left(\sup_{t\le T}|A_t^G|\ge\epsilon\right)
\le
\frac{hV+\log2}
{\kappa_NV\epsilon^2/(16C_GT)-\log(2K_N)},
\tag{19}
\]

whenever the denominator is positive. Thus `kappa_N -> infinity` suffices, with no required rate relative to `N`.

### 4.2 A density ceiling is stronger for rare events

If instead

\[
\frac{d\nu_N}{d\mu_N}\le e^{hV},
\tag{20}
\]

then every path event probability is at most `exp(hV)` times its reference probability. Consequently (16) implies

\[
\limsup_{N\to\infty}\frac1V
\log\mathbb P_{\nu_N}
\left(\sup_{t\le T}|A_t^G|\ge\epsilon\right)=-\infty
\tag{21}
\]

when `kappa_N -> infinity`. This is a superexponential phase-replacement statement at speed volume. It is not, by itself, a full large-deviation theorem for density or current.

## 5. Empirical-density path theorem

Dynkin's formula gives

\[
\pi_t^N(G)=\pi_0^N(G)
+\frac{s}{2}\int_0^t\pi_u^N(\Delta_NG)\,du
+A_t^G+M_t^G.
\tag{22}
\]

Let `c_max=s(1+a_0)/2`. A visible jump on bond `(x,x+e_j)` changes `pi^N(G)` by at most `||partial_j G||_infinity/(N V)`. Therefore

\[
\frac{d}{dt}\langle M^G\rangle_t
\le\frac{c_{\max}}{V}
\sum_j\|\partial_jG\|_\infty^2,
\tag{23}
\]

and Doob's inequality gives

\[
\mathbb E\sup_{t\le T}|M_t^G|^2
\le\frac{4Tc_{\max}}{V}
\sum_j\|\partial_jG\|_\infty^2.
\tag{24}
\]

**Theorem.** Assume (1)–(3), `kappa_N -> infinity`, and either (17) with a uniform `h`, or the initialization supplied in Section 6. Assume also that the initial empirical measures converge in probability, in the weak topology, to `rho_0(u)du`. Then on every fixed `0<=t<=T`, the entire empirical-density path converges in probability, uniformly in time in a metric for weak convergence, to the unique heat evolution

\[
\partial_t\rho=\frac{s}{2}\Delta\rho,
\qquad \rho(0,\cdot)=\rho_0.
\tag{25}
\]

The estimates controlling the dynamical error are uniform in the allowed amplitudes and frozen disorder. The initial-profile convergence is still a genuine assumption; no mixing claim prepares that profile automatically.

**Proof.** For a smooth test `G`, (22), (19), and (24) show that the test trajectory differs in probability, uniformly on `[0,T]`, from a trajectory with uniformly bounded drift. The empirical measures have total mass at most one, and a countable dense family of smooth tests supplies tightness in the weak-measure path space. Every limit has continuous paths. Since `Delta_N G -> Delta G` uniformly, the martingale equation passes to the limit. Its limit is the weak heat equation. Empirical exclusion measures have limit densities between zero and one. Uniqueness of the weak heat equation identifies every subsequential limit; the deterministic initial-profile assumption upgrades this to convergence in probability. This proves the claim. The same proof gives joint convergence in distribution with a random initial profile to that profile and its deterministic heat evolution, if the initial profiles converge in distribution. It does not assert convergence in probability to a random object on an unspecified common probability space. ∎

This theorem concerns empirical-density paths. It neither identifies the full microscopic record law nor gives a total-variation approximation of that law. It also does not identify density fluctuations or a dynamical rate function.

## 6. Arbitrary initial correlations: active phase regularization

The entropy premise need not require an equilibrium preparation or a label-isolating hold. Fix `u>0`, let `p_u` be the heat kernel on the circle for generator `partial_theta^2`, measured relative to normalized Haar measure, and write

\[
K_u=\|p_u\|_\infty<\infty.
\]

Run the **actual native dynamics and phase bath together** for physical time

\[
\tau_N=\frac{u}{\kappa_N},
\qquad
\delta_N=\frac{u}{\kappa_NN^2}
\tag{26}
\]

in macroscopic time. Starting from any joint law of visible configuration and phases, the autonomy of the phases gives a phase marginal density at time `tau_N` bounded by `K_u^(dV)`. Conditional on a phase configuration, the probability assigned to any of the `2^V` visible configurations is at most one. Hence the full joint law `nu'_N` satisfies

\[
\frac{d\nu'_N}{d\mu_N}
\le 2^VK_u^{dV}
=\exp\{V(\log2+d\log K_u)\}.
\tag{27}
\]

This is a joint density ceiling. It does **not** claim that the visible configuration and the phases become independent. The visible process can have acquired extensive information about the phases during this layer.

The expected visible test displacement during the layer is bounded by total jump variation:

\[
\mathbb E\sup_{0\le t\le\delta_N}
|\pi_t^N(G)-\pi_0^N(G)|
\le\frac{c_{\max}u}{\kappa_NN}
\sum_j\|\partial_jG\|_\infty.
\tag{28}
\]

The omitted initial part of the phase drift has the deterministic bound

\[
\left|\int_0^{\delta_N}F_N^G(X_t)\,dt\right|
\le\frac{L_Gu}{\kappa_NN}.
\tag{29}
\]

Applying (20)–(21) and the theorem after this layer, and then using (28)–(29), proves the same empirical-density limit from arbitrary initial phase distributions and visible-phase correlations. There is no supplied baseline reset in this argument. The added phase operation, its rates, and the short elapsed time remain actual resources.

### Retained records and frozen sectors

The same calculation can be made conditional on any pre-existing record `D` and any frozen value `z`, even when the record has arbitrarily many values or determines the initial microscopic state. It requires that, conditional on this past, the complete future native-and-bath process retains the declared generator law, including its native jump innovations as well as fresh Brownian bath increments. The stated uniform structural bounds must remain true. Fresh bath noise alone is insufficient if the record exposes future native innovations. The conditional initial empirical-profile assumption must be stated at the strength used by the intended conclusion. Averaging uniform dynamical error bounds over `D,z` is valid and does not incur a record-cardinality factor.

This observation does not supply a posterior validity guarantee after arbitrary data selection. If an acquired model is only known to satisfy the structural bounds on a confidence event, the theorem applies on that event at its warranted interface. It also does not include newly generated preparation logs in a reference joint law unless those logs are explicitly modeled.

## 7. Why a path theorem over all times is false

Even the unmodulated symmetric exclusion process rules out an infinite-time path assertion of this kind. Consider an even one-dimensional ring with `N/2` particles and `alpha_b=0`. From any configuration in that sector, the finite irreducible process almost surely visits the configuration with the first half of the ring occupied and the second half empty. For `G(u)=sin(2 pi u)`, the test value at that configuration tends to

\[
\int_0^{1/2}\sin(2\pi u)\,du=\frac1\pi.
\]

Start with the uniform half-filled canonical equilibrium. Its initial empirical profile converges to `1/2`, whose heat evolution has zero `G`-moment. Nevertheless, for each fixed `0<epsilon<1/pi`, and all sufficiently large `N`,

\[
\mathbb P\left(\sup_{t\ge0}|\pi_t^N(G)|>\epsilon\right)=1.
\tag{30}
\]

Fixed macroscopic time windows are therefore essential. A uniform bound on individual-time compressed operators is not a uniform approximation of an infinite observed path.

## 8. Predecessors and the narrow value of this construction

The analytic route is established. A particularly direct inspected template is Avena–Franco–Jara–Völlering, *Symmetric exclusion as a random environment: Hydrodynamic limits* (2015), whose proof uses an initial path-entropy bound, exponential entropy inequality, Feynman–Kac/Dirichlet estimates, and martingale tightness. Their physical model is different: a random walker observes an autonomous exclusion environment. See the proof of Theorem 2.1 and Section 2.2 in the [primary article](https://www.numdam.org/article/AIHPB_2015__51_3_901_0.pdf).

Redig–Saada–Sau, *Symmetric simple exclusion process in dynamic environment: hydrodynamics* (2020), prove empirical-density path hydrodynamics in dynamic conductances through self-duality and a one-particle invariance principle. Their configuration-independent conductances permit one-particle closure; the amplitudes in (1) may destroy that closure. The phase-energy calculation above supplies a different sufficient replacement estimate, rather than extending their theorem by assertion. See Theorem 3.2 and Remark 3.3 in the [primary preprint](https://arxiv.org/pdf/1811.01366).

For the stronger target, Bertini–De Sole–Gabrielli–Jona-Lasinio–Landim's current large-deviation theorem already specifies the classical density/current action of symmetric exclusion and its weakly tilted hydrodynamic construction. The present mean-density theorem does not reproduce their full result for the modulated system. See Theorem 2.2 and Section 3 in [Large deviations of the empirical current in interacting particle systems](https://arxiv.org/pdf/math/0512394).

The constructive addition recorded here is therefore a sharply stated supplier: actual independent phase agitation, exact common phase mean, and swap-invariant bounded modulation give the explicit estimate (13), including nonlocal visible dependence and arbitrary frozen sectors. Its novelty relative to the full fast-environment literature remains unresolved; no historical priority is claimed.

## 9. Read source versions

This note extends the interface of the following predecessor proofs without changing them:

| Source | SHA-256 read |
|---|---|
| `continuation5_20261029/GAP_FREE_SELECTIVE_AVERAGING.md` | `9df1e444eefdf5223a97e48cbbe5145339d4b00ae6521bd7f9208482e7b5eeae` |
| `continuation5_20261029/SELECTIVE_KINETIC_ANNEALING.md` | `53b1a25cc73ba0802085ab82bca8e7560a0854dd71184b4be33b1cab1eb39350` |
| `continuation5_20261029/RELATIVE_COLLECTIVE_RESPONSE.md` | `03df6fe085c502bd27e2e425fc5a9ea17633b33d5a5cefd6e7732e83b490bd79` |

