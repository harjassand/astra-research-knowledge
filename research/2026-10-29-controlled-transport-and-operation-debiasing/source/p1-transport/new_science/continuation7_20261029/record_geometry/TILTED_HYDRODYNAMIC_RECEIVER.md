# The weakly tilted density and current receiver

**Date:** 2026-10-29. **Status:** proved below at the stated interface. This supplies the dependency used in Section 5 of `RARE_TRANSPORT_WITHOUT_KINETIC_IDENTIFICATION.md` and Sections 2 and 5 of `CONTROLLED_MACROSCOPIC_ACTION.md`. It reconstructs ordinary exclusion arguments; no new hydrodynamic method or priority is claimed.

## 1. Exact statement

Use the one-dimensional ring model of the companion notes. The physical native rates are

\[
r_i=(s/2)[1+\alpha_i(\eta,z)\cos\theta_i],
\qquad |\alpha_i|\le a<1,
\qquad\alpha_i(\eta^i,z)=\alpha_i(\eta,z).
\tag{1}
\]

The amplitudes may depend on all of `eta`, position, `N`, and arbitrary frozen `z`. They are phase independent. Native jumps leave phases unchanged. The actual phase bath is autonomous with independent fresh Brownian increments, at physical rate `kappa_N -> infinity`. Work on macroscopic time, so the entire physical generator is multiplied by `N^2`.

Fix a smooth bounded deterministic comparison field `E(t,x)` on `[0,T]` times the unit circle. Change only the native jump rates to

\[
r_i^E=r_i\exp\{E(t,i/N)(\eta_i-\eta_{i+1})/N\}.
\tag{2}
\]

This is a mathematical comparison law. An actuator implementing (2) is not assumed. Initial occupations are deterministic and their empirical measures converge weakly to `m dx`, with `0<m<1`. Initial phases and their correlations with frozen information may be arbitrary.

Then the empirical density and integrated current converge in probability, on `[0,T]`, to

\[
\partial_t\rho=(s/2)\rho_{xx}-\partial_x[s\chi(\rho)E],
\qquad\rho(0,x)=m,\qquad\chi(\rho)=\rho(1-\rho),
\tag{3}
\]

\[
W_t(dx)=\left[\int_0^t j(u,x)du\right]dx,
\qquad j=-(s/2)\rho_x+s\chi(\rho)E.
\tag{4}
\]

Convergence is uniform in time in the weak-measure topology on bounded-total-variation sets, equivalently in `C([0,T],H^{-3} x H^{-3})` after the deterministic negligible interpolation of visible jumps. In Skorokhod space the original jump paths have the same limit.

All dynamical bounds are uniform over the admitted amplitudes and frozen sectors. The initial-profile convergence is an actual premise. The assertion can be made conditional on a fixed retained old record when the complete future native-and-actuator process retains the declared conditional generator law, including native jump innovations as well as fresh actuator inputs; it is not a posterior calibration assertion or a transfer after rare future conditioning.

For a constant field `E`, uniqueness gives `rho=m` and

\[
Q_N(t)=N^{-2}\sum_iJ_i(t)\longrightarrow s\chi(m)Et,
\qquad
\int_0^T\frac1N\sum_i(\eta_i-\eta_{i+1})^2dt
\longrightarrow 2\chi(m)T.
\tag{5}
\]

The same receiver holds for the separately supplied independent-sign-flip model, using its phase-replacement estimate and finite-state initial density ceiling.

## 2. The occupation variational input, explicitly reconstructed

Let `mu_eta=Ber(1/2)^N`, and set

\[
D_{\rm ex}(g)=\frac12\sum_i\int|g(\eta^i)-g(\eta)|^2d\mu_\eta.
\]

For a block of `L` sites starting at `x`, let `rho_L(x)` be its average occupancy and let `p_L(x)` be the sum of its `L-1` internal products `eta_i eta_{i+1}`, divided by `L`. Put

\[
U_L(\eta)=\frac1N\sum_x|p_L(x)-\rho_L(x)^2|.
\tag{6}
\]

For every fixed `b>0,c>0`,

\[
\lim_{\epsilon\downarrow0}\limsup_{N\to\infty}\frac1N
\sup_{\|g\|_2=1}
\{bN\langle U_{\lfloor\epsilon N\rfloor},|g|^2\rangle
       -cN^2D_{\rm ex}(g)\}=0.
\tag{7}
\]

Symmetric blocks, including the last adjacent product, give the same statement: endpoint errors are `O(1/L)`. This is the precise variational estimate needed by the receiving proof. Its derivation follows.

### 2.1 One fixed block

Under the uniform canonical law on `ell` sites with `k` particles, the mean of an internal product is `k(k-1)/[ell(ell-1)]`. Thus the canonical mean of `p_ell-rho_ell^2` is `-k/ell^2`, of magnitude at most `1/ell`. Its variance is at most `C/ell`, uniformly in `k`: only `O(ell)` edge pairs overlap, while disjoint edge-product covariances are `O(1/ell)` by the explicit hypergeometric moments `(k)_r/(ell)_r`, `r<=4`. Equivalently, couple sampling with and without replacement for four sites; their probability of a repeated draw is `O(1/ell)`. Therefore

\[
\mathbb E_{\ell,k}|p_\ell-\rho_\ell^2|\le C/\sqrt\ell.
\tag{8}
\]

The nearest-neighbor exchange chain on each nontrivial fixed-count block is finite and connected. Let `C_ell` be the maximum of its finite Poincare constants; trivial sectors have variance zero. Conditional on the exterior and block count, subtract the canonical mean of the observable. Writing `g^2-(E_B g)^2=(g-E_Bg)(g+E_Bg)` and applying Poincare and Cauchy–Schwarz gives

\[
\langle U_\ell,|g|^2\rangle
\le C/\sqrt\ell
 +C\sqrt{C_\ell\ell\,D_{\rm ex}(g)/N},
\quad \|g\|_2=1.
\tag{9}
\]

Indeed each nearest-neighbor edge belongs to `ell-1` translated blocks. This explains the factor `ell/N` after averaging their forms. Constants may be enlarged without dependence on `N` or the frozen context.

### 2.2 Two separated blocks and the moving-particle estimate

For two disjoint `ell`-site blocks at displacement `y>=ell`, their density difference has conditional canonical mean absolute value at most `C/sqrt(ell)` when their combined particle count is fixed. This follows directly from the hypergeometric variance of the count in one half.

Connect the two blocks by one exchange between a designated site in each block, in addition to their internal edges. This finite graph is connected; its canonical Poincare constants have a finite maximum `C'_ell` depending only on `ell`. The connecting exchange has displacement at most `y`. Its form satisfies

\[
D_{x,x+y}(g)\le4y\sum_{i=x}^{x+y-1}D_i(g).
\tag{10}
\]

To prove (10), realize the long transposition as at most `2y-1` adjacent transpositions, telescope `g`, use Cauchy–Schwarz, and use invariance of the Bernoulli reference under every intermediate permutation. No actual long-range actuator is assumed: (10) is solely an inequality between forms.

Let

\[
V_{\ell,M}(\eta)=\frac1{NM}\sum_x\sum_{y=\ell}^{M}
|\rho_\ell(x)-\rho_\ell(x+y)|,
\qquad M<N/4.
\]

The same conditional variance argument, now followed by (10), gives

\[
\langle V_{\ell,M},|g|^2\rangle
\le C/\sqrt\ell+
C\sqrt{C'_\ell(\ell+M^2)D_{\rm ex}(g)/N}.
\tag{11}
\]

For the long-edge term, summing over starting positions counts each nearest-neighbor edge `y` times; (10) contributes another factor `y`. Averaging `y<=M` therefore costs `O(M^2/N)D_ex`. The internal-block terms cost `O(ell/N)D_ex`.

### 2.3 Assembly and the order of limits

Discrete convolution, Jensen's inequality, and `|u^2-v^2|<=2|u-v|` on `[0,1]` give a deterministic bound of the form

\[
U_M\le U_\ell+C V_{\ell,2M}
       +C(\ell/M+1/\ell),
\tag{12}
\]

for `M>=2ell` and `2M<N/4`, after harmless changes of block origin. One way to verify (12) is to average the `ell`-block pair product inside an `M`-block, replace it by the square of its `ell`-block density, and compare that density with the average of all such densities in the large block. The first and last `ell` sites and the omitted internal endpoint product account for the displayed boundary terms. Pairs of overlapping small blocks contribute at most `C ell/M`. The remaining pairs are bounded by (11).

Apply (9) and (11) to (12), and complete the square against `cN^2 D_ex`. For fixed `ell` and `b,c`, this bounds the variational expression in (7), divided by `N`, by

\[
b(C/\sqrt\ell+C/\ell+C\ell/M)
+C_{b,c,\ell}(\ell+M^2)/N^2.
\tag{13}
\]

First let `N` grow with `M=floor(epsilon N)`, then let `epsilon` decrease, and finally let the fixed auxiliary `ell` grow. The limsup is at most zero. The constant trial function gives a nonnegative variational value, proving (7). No estimate on how fast `C_ell` grows is required for this order of limits.

This reconstructed argument is the usual one-block/two-block proof underlying the occupation estimate stated in Theorem 3.2 of [Bertini et al., Large deviations of the empirical current in interacting particle systems](https://arxiv.org/pdf/math/0512394). The source is a classical predecessor; equations (7)–(13) make the actual variational interface explicit rather than invoking its entire path theorem for a different generator.

## 3. Transfer to the joint process and its comparison tilt

For (1), `c_min=s(1-a)/2>0`, so the joint Dirichlet form dominates `c_min D_ex`. Apply the visible variational bound separately to `f(.,theta)` at each phase configuration and integrate its squared norm. Thus (7) bounds the top Feynman–Kac numerical range for the actual joint process, without assuming that its evolving law factorizes.

After an initial density ceiling `d nu_N/d mu_N<=exp(hN)`, exponential Markov and (7) yield, for every `delta>0`,

\[
\lim_{\epsilon\downarrow0}\limsup_N\frac1N
\log\mathbb P_{\nu_N}
\left(\int_0^T U_{\lfloor\epsilon N\rfloor}(\eta_t)dt>\delta\right)
=-\infty.
\tag{14}
\]

The fixed `h` is absorbed by sending the Chernoff multiplier to infinity after the block limits. The weak-tilt likelihood has `E Z_E^2<=exp(C_E N T)`, so Cauchy–Schwarz transfers (14) to (2).

Arbitrary initial phases require no reset: the active phase heat layer of physical duration `u/kappa_N` gives the joint ceiling `(2K_u)^N`. Its bounded occupation integral vanishes deterministically. Its empirical density and integrated current changes are superexponentially negligible in the weak topology, by the Poisson jump-count bound. The proof uses this ceiling only for (14), not to transfer a finite-action probability.

For smooth weights `F(t,x)`, convolution moves the block average from `eta_i eta_{i+1}` onto the weight with an `O(epsilon)` error. Also

\[
(\eta_i-\eta_{i+1})^2
=\eta_i+\eta_{i+1}-2\eta_i\eta_{i+1}.
\]

Consequently (14) replaces weighted pair activities by `2 chi` of the smoothed empirical density. At fixed block scale, this is a continuous functional of bounded empirical-density paths. After passage to a subsequential limit, the spatial approximation of the identity converges in space-time `L1`, since `0<=rho<=1`. Sending the block scale to zero identifies `2 chi(rho)`.

The companion lemma `PHASE_ENERGY_SUPPLIES_EXCHANGE_COERCIVITY.md` extends this occupation transfer to `|alpha_i|<=1`: for all sufficiently large `kappa_N`, the full native-plus-phase form still dominates `(s/4)D_ex`. The root receiving theorem currently retains `a<1`, so this endpoint extension is not needed for its acceptance.

## 4. Martingale identification under a smooth field

Write `delta_i=eta_i-eta_{i+1}` and `a_i=delta_i^2`. For a smooth spatial current test `H`, the exact current decomposition has martingale jumps bounded by `||H||_infinity/N^2` and bracket bounded by `C_{E,H}T/N`. Its drift is

\[
\sum_i H_i r_i e^{E_i\delta_i/N}\delta_i
=\frac{s}{2}\sum_iH_i\delta_i
+\frac{s}{2}\sum_iH_i\alpha_i\delta_i\cos\theta_i
+\frac{s}{2N}\sum_iH_iE_i a_i
+\frac{s}{2N}\sum_iH_iE_i\alpha_i a_i\cos\theta_i
+O_{E,H}(N^{-1}).
\tag{15}
\]

The Taylor remainder is uniformly bounded by `C/N` after summing all bonds. The two phase terms have superexponentially vanishing accumulated integrals under the comparison law, by `WEAK_TILT_PHASE_REPLACEMENT.md`. The first term is

\[
\frac{s}{2}\sum_i\eta_i(H_i-H_{i-1}),
\]

which converges to `(s/2) int rho H_x`. Occupation replacement turns the third term into `s int H E chi(rho)`.

For a density test `G`, use `H_i=N(G_{i+1}-G_i)`. The same decomposition gives the discrete heat term plus the flux term, the phase remainder, and a martingale of bracket `O(1/N)`. The heat drift and the weak-field drift are uniformly bounded on fixed test functions. Accumulated phase errors vanish uniformly in time. This gives tightness of the density test trajectories.

For the current, `H=1` first bounds the circulation in probability uniformly on `[0,T]`. Exact one-dimensional conservation implies

\[
\|W_t^N\|_{\rm TV}\le |Q_N(t)|+1.
\tag{16}
\]

Thus current compact containment follows. The same drift and martingale estimates for each smooth `H`, together with (16), give continuous tightness in `H^{-3}`. Limits satisfy (3) and, for every smooth `H`,

\[
\langle W_t,H\rangle
=\int_0^t\left[\frac{s}{2}\langle\rho_u,H_x\rangle
                  +s\langle\chi(\rho_u),E_uH\rangle\right]du.
\tag{17}
\]

This identifies the complete integrated spatial current; continuity of density alone would leave its spatially constant part undetermined.

## 5. Uniqueness, energy, and the flat receiver

The forcing `s chi(rho)E` is bounded for a bounded weak solution with `0<=rho<=1`. The weak heat-energy estimate therefore places `rho_x` in space-time `L2`, permitting the usual difference estimate. If `rho` and `rho'` have the same initial profile, write `v=rho-rho'`. Since `chi` is Lipschitz with constant one on `[0,1]`,

\[
\frac12\frac d{dt}\|v\|_2^2
\le-\frac{s}{4}\|v_x\|_2^2
     +s\|E\|_\infty^2\|v\|_2^2.
\tag{18}
\]

Gronwall proves uniqueness. Existence for smooth `E` and the constant interior initial profile is the ordinary uniformly parabolic construction; the maximum principle preserves `[0,1]`. The uniqueness argument also identifies every tight subsequential empirical limit, proving convergence in probability to (3)–(4).

For constant `E`, `rho=m` solves (3). Equations (14), (15), and (17) then give (5), with all factors of two fixed by the native swap rate `s/2` and the canonical activity `2 chi(m)`. This closes the particular lower-bound receiver used for the scalar circulation theorem.

## 6. Limits of this receiving result

The proof requires the supplied common mean and common reversible form, autonomous phase/sign operation, and fresh future randomness. Arbitrary nonlocal amplitudes cause no additional difficulty because no argument differentiates them in visible coordinates. A phase-dependent mean varying with frozen sector is not removed. Merely small acquired equilibrium errors do not establish the structural premises.

The weak field is deterministic and smooth in this proof. Arbitrary observation-selected feedback fields, full microscopic record laws, finite-N rates of hydrodynamic convergence, and a uniform-in-infinite-time path theorem are not asserted. Fixed-confidence calibration error remains separate from speed-volume rare-event confidence.

