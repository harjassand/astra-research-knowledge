# Inverse activity removes the weighted-current remainder

30 October 2026. Complementary constructive proof within Astra P1. The inverse-activity theorem below is proved at a uniformly elliptic reversible exclusion interface. Its application closes the weighted-corrector remainder for the shared-bit ring when `N gamma_N -> infinity` and `gamma_N/N -> 0`. It does **not** by itself prove the proposed nonlinear density/current large-deviation principle. In particular, the hydrodynamic receiver under the corrected spatial tilt remains a separate obligation.

The zero-external-clock version of the inverse-activity theorem is valid. The subsequent odd-in-the-bit corrector estimate uses an actual positive clock and does not establish the zero-clock weighted receiver.

## 1. A sufficiently general inverse-activity theorem

Let `eta` be an exclusion configuration on a periodic ring of `N` sites, with exactly `M_N` particles and `M_N/N -> m`, `0<m<1`. Write

\[
\delta_i=\eta_i-\eta_{i+1},\qquad a_i=\delta_i^2,
\qquad A(\eta)=\sum_i a_i.
\tag{1}
\]

Thus `A>=2` in every nontrivial particle sector. Work on physical time accelerated by `N^2`.

The complete finite-state process may contain an auxiliary state. Its reference law `mu_N` has uniform canonical visible marginal, and the full generator is reversible for `mu_N`. Each visible transition is a nearest-neighbor exchange, with physical rate between constants `q_*>0` and `q^*<infinity` on active bonds. The joint Dirichlet form dominates `q_* D_ex`, where the visible exchange form is evaluated at each fixed auxiliary state against the corresponding uniform visible conditional law. Auxiliary-only transitions do not change `eta`. Equivalently, it is enough to assume a product reference `mu_eta times mu_aux`, visible-only exchanges reversible in every fixed auxiliary state, and an additional reversible auxiliary generator. This last formulation directly covers the original `(eta,sigma)` shared-clock ring, including `gamma_N=0`.

Suppose the actual initial law satisfies

\[
\frac{d\nu_N}{d\mu_N}\le e^{hN+o(N)}
\tag{2}
\]

for one fixed finite `h`. On the finite ring, an arbitrary initial occupancy and one retained bit cost at most `2 binom(N,M_N)`, so (2) includes arbitrary initial laws in that sector. No initial flat spatial profile is needed.

**Theorem.** For every fixed `T<infinity` and `epsilon>0`,

\[
\limsup_{N\to\infty}\frac1N\log\mathbb P_{\nu_N}
\left(\int_0^T\frac{dt}{A(\eta_{N^2t})}>\epsilon\right)
=-\infty.
\tag{3}
\]

The same conclusion holds under any mathematical native-rate tilt `r_i -> r_i exp(q_i)` with predictable `|q_i|<=K/N`, for fixed `K`, and unchanged auxiliary dynamics. This is a likelihood transfer, not a supplied control operation.

The proof does not assume that `A/N` is bounded below pointwise, or that rare paths resemble the canonical equilibrium. It combines three explicit conventional inputs and then gives the compactness argument joining them.

## 2. Density-path exponential tightness from reversibility

Let `pi_t^N=N^{-1} sum_i eta_i(N^2t) delta_(i/N)`. For a smooth periodic `G`, every native jump of `pi^N(G)` has magnitude at most `||G'||_infinity/N^2`, and its forward Dynkin martingale has predictable bracket over an interval of length `delta` at most

\[
q^*\|G'\|_\infty^2\delta/N.
\tag{4}
\]

The auxiliary jumps do not contribute. Under the stationary reversible law, the reversed process on `[0,T]` has the same generator. Subtracting its Dynkin martingale from the forward one cancels both generator integrals and gives the exact forward/backward identity

\[
\pi_t^N(G)-\pi_s^N(G)
=\tfrac12(M_t^G-M_s^G)
-\tfrac12(\widehat M_{T-s}^G-\widehat M_{T-t}^G).
\tag{5}
\]

The bounded-jump martingale exponential inequality, applied forward and backward on a finite interval grid, gives

\[
\lim_{\delta\downarrow0}\limsup_N\frac1N\log
\mathbb P_{\mu_N}\left(
\sup_{|t-s|\le\delta}|\pi_t^N(G)-\pi_s^N(G)|>\epsilon
\right)=-\infty.
\tag{6}
\]

For example, at a fixed grid interval the exponent is bounded above by a constant times `-epsilon^2 N/(q^* ||G'||^2 delta+O(epsilon/N))`; the number of grid intervals is fixed before `N` grows. This is the elementary finite-chain instance of the classical Lyons–Zheng forward/backward method.

Interpolate each visible jump continuously between its neighboring states. The change in a weak density norm is deterministic `O(1/N)` (and `O_G(1/N^2)` on a fixed smooth test). Fourier truncation, the bound on total mass, and (6) give exponential tightness of these interpolated density paths in `C([0,T],H^{-3})`. All limits have densities `0<=rho<=1`, and conserved mass `m`. The usual countable-test diagonal construction supplies a compact set with any prescribed exponential escape cost. Multiplication by (2) transfers this assertion to the actual initializer. Irreducibility is unnecessary.

## 3. An exponential spatial energy estimate independent of the clock

Use the convention

\[
D_{\rm ex}(f)=\frac12\sum_i\int|f(\eta^i,z)-f(\eta,z)|^2d\mu_N.
\tag{7}
\]

For `||f||_2=1` and real coefficients `H_i`, invariance under each visible exchange gives

\[
\begin{aligned}
\left|\left\langle\sum_iH_i\delta_i,f^2\right\rangle\right|
&=\frac12\left|\sum_iH_i\langle\delta_i(f^2-(f^i)^2)\rangle\right|\\
&\le\sqrt{2\sum_iH_i^2}\sqrt{D_{\rm ex}(f)}.
\end{aligned}
\tag{8}
\]

Complete the square against `q_* N^2 D_ex`. The top Feynman–Kac eigenvalue for the potential `N sum_i H_i delta_i` is at most `(2q_*)^{-1} sum_i H_i^2`. This holds separately for every time of a smooth time-dependent field; the usual `L2` norm differential inequality integrates the bound.

Define the continuous path functional

\[
\mathcal E_H(\rho)=\int_0^T\!\int\rho\,\partial_xH\,dxdt
-\frac1{2q_*}\int_0^T\!\int H^2\,dxdt.
\tag{9}
\]

Discrete summation by parts and Riemann sums have `O_H(1/N)` error before multiplication by `N`. Therefore, for each fixed smooth `H`,

\[
\limsup_N\frac1N\log
\mathbb P_{\nu_N}(\mathcal E_H(\pi^N)>R)\le h-R.
\tag{10}
\]

Here and below the same functional on the empirical path means its Riemann-sum version; its limit is (9). Its difference from the interpolated path version vanishes for each fixed field.

Take a countable dense set of smooth fields, including rational multiples. Functional duality gives

\[
\mathcal E(\rho):=\sup_H\mathcal E_H(\rho)
=\frac{q_*}{2}\int_0^T\!\int|\partial_x\rho|^2dxdt,
\tag{11}
\]

with value infinity if there is no square-integrable weak spatial derivative. No assertion that a single finite-`N` atomic path has a finite value of the continuum supremum is made. We use only finitely many tests at a time and then a compactness argument in Section 5. This avoids an unjustified interchange of an infinite supremum and an exponential expectation.

The general energy-estimate method is established. For a primary treatment of its role in exclusion large deviations, see Bertini–Landim–Mourragui, Section 3.2 and Lemma 3.3 of [Dynamical large deviations for the boundary driven weakly asymmetric exclusion process](https://arxiv.org/pdf/0804.2458). Equations (8)–(11) give the simpler periodic reversible estimate actually used here, without importing that paper's different generator or boundary conditions.

## 4. Occupation replacement forces small activity toward pure profiles

For a block of `ell` sites let `rho_ell(x)` be its average occupancy, and let `p_ell(x)` be its `ell-1` internal adjacent products divided by `ell`. Set

\[
U_\ell(\eta)=\frac1N\sum_x|p_\ell(x)-\rho_\ell(x)^2|.
\tag{12}
\]

The explicit variational one/two-block estimate proved in the accepted round7 file
`record_geometry/TILTED_HYDRODYNAMIC_RECEIVER.md`, equations (7)–(13), says

\[
\lim_{a\downarrow0}\limsup_N\frac1N
\sup_{\|f\|_2=1}
\{bN\langle U_{\lfloor aN\rfloor},f^2\rangle
-q_*N^2D_{\rm ex}(f)\}=0
\tag{13}
\]

for every fixed `b>0`. Apply it at each auxiliary state and integrate. Thus, for each `delta>0`,

\[
\lim_{a\downarrow0}\limsup_N\frac1N\log
\mathbb P_{\nu_N}\left(\int_0^T U_{\lfloor aN\rfloor}(\eta_{N^2t})dt>\delta\right)
=-\infty.
\tag{14}
\]

This use of the predecessor requires only its visible variational estimate and form domination, not an independently randomized local phase bath or a hydrodynamic identification. Although that file displays the Bernoulli reference, its conditional-block proof is unchanged at a fixed global particle count: all conditional block laws remain uniform canonical, and every intermediate permutation in the moving-particle estimate preserves the global canonical measure.

Let `chi(v)=v(1-v)` and define

\[
C_{N,\ell}(\eta)=\frac1N\sum_x\chi(\rho_\ell(x)).
\]

Averaging the internal pair products gives the deterministic inequality

\[
C_{N,\ell}(\eta)\le \frac{A(\eta)}{2N}+U_\ell(\eta)+\frac1\ell.
\tag{15}
\]

Indeed the average block density equals `m_N`, the average internal pair product is `(ell-1)/ell` times the global adjacent pair average, and `A/N=2m_N-2N^{-1}sum_i eta_i eta_(i+1)`.

At fixed `a>0`, the limiting functional is

\[
C_a(\rho)=\int\chi(B_a\rho)(x)dx,
\tag{16}
\]

where `B_a` is the periodic box average of width `a`. It is continuous in the weak measure topology on `0<=rho<=1`. In particular, its quadratic term is a double integral against the continuous triangular autocorrelation kernel of the box. Consequently it is continuous along the uniformly weakly converging compact density paths supplied in Section 2. As `a` decreases to zero, `C_a(rho_t)` converges to `int chi(rho_t)` in time `L1` by the approximation-of-identity theorem and boundedness.

## 5. The finite-test compactness proof of (3)

Suppose `int_0^T 1/A dt > epsilon`. Choose one fixed `K>2T/epsilon` and put `b_N(t)=1{A(eta_(N^2t))<=K}`. Since `A>=2`,

\[
\int_0^T\frac{dt}{A}\le T/K+\tfrac12\int_0^T b_N(t)dt.
\tag{17}
\]

Thus the bad event forces `int b_N > epsilon` after decreasing `epsilon` harmlessly if necessary.

Here is the deterministic exclusion of such bad paths from every finite-energy limit. Take a sequence of paths in a fixed compact density-path set, and assume:

1. each fixed test from the countable dense energy family eventually satisfies `E_H<=R`, for one finite `R`;
2. for scales `a_j down to 0` and tolerances `delta_j down to 0`, each fixed `j` eventually satisfies `int U_floor(a_j N) <= delta_j`;
3. the bad event in (17) holds.

Pass to a density-path limit `rho`, and to a weak-star subsequential limit `b` of the bounded functions `b_N` in `L infinity([0,T])`. Then `0<=b<=1` and `int b>=epsilon`. For each fixed `j`, multiply (15) by `b_N` and integrate. Its limit gives

\[
\int_0^T b(t)C_{a_j}(\rho_t)dt\le\delta_j.
\tag{18}
\]

Let `j` grow. The approximation-of-identity limit in Section 4 yields

\[
\int_0^T b(t)\!\int\chi(\rho_t(x))dxdt=0.
\tag{19}
\]

The energy conditions and (11) place `rho_t` in spatial `H^1` for almost every `t`. At each such time, `0<=rho_t<=1` and its integral is `m in (0,1)`. A function in `H^1` on the connected circle that is `{0,1}`-valued almost everywhere is constant: for example its absolutely continuous representative is continuous, or apply the Sobolev chain rule to `rho^2=rho`. Hence

\[
\int\chi(\rho_t)>0\quad\text{for almost every }t.
\tag{20}
\]

Equations (19) and (20) force `b=0` almost everywhere, a contradiction.

For completeness, the probabilistic quantifiers are finite at every stage. Fix any desired exponential cost `L`. Choose a compact density-path set with escape cost greater than `L` by Section 2, and choose `R>h+L+1`. Choose `a_j down to 0`, `delta_j down to 0` so that each replacement failure in (14) has limsup exponent below `-L-1`. If for every finite number of energy and replacement tests there existed arbitrarily large `N` and a bad path in the compact set passing those tests, a diagonal selection would produce exactly the contradictory sequence above. Therefore some finite number of tests excludes all such paths for sufficiently large `N`. A finite union bound, (10), and (14) bound the bad-event exponent by `-L`. Since `L` is arbitrary, (3) follows.

This proof pays for low-activity paths through their dynamical energy. It does not replace a speed-`N` rare event by its typical equilibrium concentration.

## 6. Bounded weak tilts and retained records

For a predictable native tilt `|q_i|<=K/N`, let `Z_q` be its path likelihood against the base process over physical time `N^2T`. The exact jump likelihood identity is

\[
Z_q^2=Z_{2q}\exp\left\{\int_0^{N^2T}\sum_i r_i(e^{q_i}-1)^2dv\right\}.
\tag{21}
\]

The total native rate is at most `q^* N`, so the extra exponent is at most `C_K N T`. The bounded likelihood exponential is a true martingale on the finite horizon, giving `E Z_q^2<=exp(C_KNT)`. Cauchy–Schwarz transfers every speed-`N` superexponential assertion above. No invariant measure of the tilted process is assumed.

Conditional-on-record use requires (2) at the chosen conditioning interface and the **complete future native and auxiliary conditional generator law**. A record revealing future native innovations invalidates this law even if the external clock itself is fresh. The theorem supplies neither initial preparation nor calibration confidence. Fixed calibration failure probability cannot be discarded in a rare-event claim.

## 7. Exact algebra for the ring weighted corrector

Now specialize to the round7 ring with even `N`,

\[
r_i=c(1+\alpha u\delta_i),\quad c=s/2,\quad
u=\sigma p(\eta),\quad 0\le\alpha<1,
\tag{22}
\]

where the external bit `sigma` flips at physical rate `gamma_N`. Native exchanges flip `p` and therefore `u`. The actual native rates in coordinates `(eta,sigma)` are uniformly elliptic and reversible at every fixed `sigma`, so (3) applies even if `gamma_N=0`.

Write

\[
L_{\rm ex}=\sum_i(T_i-I),\qquad
\mathcal D=\sum_i\delta_i(T_i-I),\qquad
L_{\rm native}=cL_{\rm ex}+c\alpha u\mathcal D.
\tag{23}
\]

For a smooth deterministic spatial field `H`, set `A_H=sum_i H_i a_i` and `F_H=A_H/A`. Then `|F_H|<=||H||_infinity`. A swap changes only its two neighboring activities, so `|Delta_i A|<=2`, `|Delta_i A_H|<=2||H||`, and `A(eta^i)>=A(eta)/2` on active edges. Thus

\[
|\Delta_i F_H|\le 8\|H\|_\infty/A,
\qquad |L_{\rm ex}F_H|\le8\|H\|_\infty.
\tag{24}
\]

There is an exact local-divergence identity for the asymmetric operator. Put

\[
q_j=\eta_j+2\eta_{j+1}+\eta_{j+2}
-2(\eta_j\eta_{j+1}+\eta_j\eta_{j+2}+\eta_{j+1}\eta_{j+2})
+4\eta_j\eta_{j+1}\eta_{j+2}.
\]

Its eight binary values lie in `[0,2]`, and direct expansion gives

\[
\mathcal D a_j=q_{j-1}-q_j,
\quad \mathcal D A=0,
\quad |\mathcal D A_H|\le2\sum_j|H_{j+1}-H_j|.
\tag{25}
\]

The identity `D A=0` is **not** extended to nonlinear functions of `A`. Instead, the exact quotient expansion is

\[
\mathcal D F_H
=\frac{\mathcal D A_H}{A}
-\sum_{i:\,a_i=1}\frac{\delta_i\Delta_i A
      (\Delta_i A_H-F_H\Delta_i A)}{A\,A(\eta^i)}.
\tag{26}
\]

Consequently

\[
|\mathcal D F_H|\le
\frac{2\sum_j|H_{j+1}-H_j|+16\|H\|_\infty}{A}
\le C_H/A.
\tag{27}
\]

For smooth `H(t,x)`, the constant is uniform on the fixed time interval.

It follows that

\[
uL_{\rm native}F_H=c\,uL_{\rm ex}F_H+c\alpha\mathcal D F_H
\tag{28}
\]

splits into a uniformly bounded odd-in-`sigma` term and a term dominated by `C_H/A`. The latter has superexponentially vanishing time integral by (3), including under every bounded weak comparison tilt in Section 6.

## 8. The odd term, clock term, and a larger allowed clock window

For a bounded visible function `v(eta)` and `V= sigma v`, the fair-sign integration-by-parts inequality is

\[
|\langle V,f^2\rangle|\le\sqrt2\|v\|_\infty
\sqrt{D_\sigma(f)},\qquad \|f\|_2=1,
\]

where `D_sigma=(1/2) int(f(eta,-sigma)-f(eta,sigma))^2`. Against the macroscopic clock form `N^2 gamma_N D_sigma`, Feynman–Kac gives

\[
\log\mathbb E_{\mu_N}\exp\left(bN\int_0^T V_tdt\right)
\le b^2T\|v\|_\infty^2/(2\gamma_N).
\tag{29}
\]

Apply this to `u L_ex F_H=sigma[p L_ex F_H]` using (24). It is superexponentially negligible at speed `N` provided `N gamma_N -> infinity`. Apply it to `gamma_N u F_H`; its divided log-moment cost is `O(gamma_N/N)`. The associated compensated clock sum has the same divided log-moment cost. Therefore both are negligible if

\[
N\gamma_N\longrightarrow\infty,
\qquad \gamma_N/N\longrightarrow0.
\tag{30}
\]

The round7 hypothesis `gamma_N -> infinity`, `gamma_N/N -> 0` is a sufficient subcase. A fixed strictly positive clock, or a slowly vanishing clock satisfying the left condition, also suffices for this remainder estimate. No claim is made at `gamma_N=0` using (29).

Here is the complete path identity behind the receiving statement. Let

\[
K_H(t)=\sum_{\text{native events}\le t}
[H_i\delta_i-\alpha u_-F_H(\eta_-)]
-\int_0^t cS_H(\eta_v)dv,
\quad S_H=\sum_iH_i\delta_i.
\tag{31}
\]

The increment field is evaluated at the event's macroscopic time for time-dependent `H`. The total native rate is `cA`, and the two unwanted drifts cancel, so `K_H` is exactly a martingale. Applying the jump rule to `uF_H` gives, for time-independent `H`,

\[
\begin{aligned}
J_H(t)-K_H(t)-\int_0^t cS_Hdv
={}&\frac\alpha2[u_0F_H(\eta_0)-u_tF_H(\eta_t)]\\
&-\frac\alpha2 L_H(t)
-\frac\alpha2\int_0^t uL_{\rm native}F_Hdv\\
&-\alpha C_H^{\rm clock}(t)
-\alpha\gamma_N\int_0^t uF_Hdv,
\end{aligned}
\tag{32}
\]

where `L_H` is the compensated native sum of `u_- Delta_i F_H`, and `C_H^clock` is the compensated clock sum of `u_- F_H`. For smooth time-dependent `H`, add the deterministic time-derivative integral `alpha/(2N^2) int u partial_t F_H dv` to the right; after division by `N^2` it is `O(N^-2)`.

The native martingale `L_H` has bounded jumps and physical bracket rate at most `C_H/A<=C_H/2`, by (24). Its normalized accumulated contribution on time `N^2T`, divided by `N^2`, is superexponentially negligible at speed `N` by its bounded-jump exponential inequality. The boundary is `O(N^-2)`. Equations (3), (28)–(30) handle every remaining term. These estimates hold uniformly over terminal times: deterministic integral domination handles (27), while finite time grids or maximal martingale inequalities handle the bounded odd sources and martingales.

Thus the actual weighted current has the proved replacement

\[
\frac{J_H(N^2t)}{N^2}
\;\simeq_{\rm superexp,\,N}\;
\frac{K_H(N^2t)}{N^2}
+c\int_0^tS_H(\eta_{N^2v})dv
\tag{33}
\]

on every fixed horizon, under (30) and under all the bounded weak comparison tilts specified above. This removes the exact remainder identified in the round7 attack file. The martingale bracket there remains exact; the new work is the justified passage back to the **actual** current.

## 9. An actual unforced hydrodynamic consequence

Suppose, additionally, that the initial empirical density converges in probability to an actual profile `rho_0(x) dx`, with `0<=rho_0<=1` and interior total mass. It may be deterministic or random at the microscopic level, subject to (2). Under (22) and (30), the actual empirical density and spatial current converge on every fixed horizon to

\[
\partial_t\rho=c\partial_x^2\rho,\qquad \rho(0)=\rho_0,
\qquad j=-c\partial_x\rho.
\tag{34}
\]

To verify this corollary, apply (33) to `H_i=N(G_(i+1)-G_i)`. This family has uniformly bounded sup norm and discrete variation for each fixed smooth `G`. Exact continuity identifies the left side with the change in `pi^N(G)`, and the drift is `c pi^N(Delta_N G)`. The martingale in (31), divided by `N^2`, has bracket `O(1/N)` because its native jumps and rates are bounded. Hence every exponentially tight density subsequential limit satisfies the weak heat equation. Its bounded weak solution is unique.

For the current, first use `H=1` in (33); its drift is zero, so `Q_N` tends uniformly to zero. Exact ring continuity gives `||W_t^N||_TV<=|Q_N(t)|+1`. The same martingale estimate for each smooth `H` and (33) identifies `W_t(H)=c int_0^t int rho_v H_x`. Bounded total variation and dense tests then give continuous tightness and the full weak-current limit. This proves (34), including nonflat or initially phase-separated visible profiles. It does not determine rare histories under a corrected spatial tilt.

## 10. What is and is not closed

The denominator `A` need not be replaced by its equilibrium mean. The proof includes phase-separated initial configurations and uses only interior total mass, elliptic reciprocal rates, and the stated full future law. It supplies no finite-`N` quantitative convergence rate.

For `gamma_N=0`, the inverse-activity result and quotient estimate (27) still hold. The odd term `u L_ex F_H` is not controlled by the external-sign estimate, and an exact event-pair trace changes the physical time parameter. Neither gap is erased here.

For positive clocks in (30), a full nonlinear action still needs a rigorous receiving law under the spatial corrected-current tilts, its matching lower-bound construction, and the relevant action topology and approximation argument. A martingale covariance or (33) alone is not a large-deviation principle. Canonical equilibrium current fluctuations are a distinct, simpler possible receiver.

### Primary provenance and exact dependency

- Lyons and Zheng, [A crossing estimate for the canonical process on a Dirichlet space and a tightness result](https://www.numdam.org/item/AST_1988__157-158__249_0.pdf), 1988: classical forward/backward reversible decomposition. The finite-state identity and bracket estimate actually used are written in (4)–(6).
- Bertini, Landim and Mourragui, [Dynamical large deviations for the boundary driven weakly asymmetric exclusion process](https://arxiv.org/pdf/0804.2458), 2009, Section 3.2: energy-exclusion strategy. The periodic estimate and finite-test argument here are explicit.
- The accepted local occupation supplier is `new_science/continuation7_20261029/record_geometry/TILTED_HYDRODYNAMIC_RECEIVER.md` relative to `Astra_P1`, SHA-256 `ae8dbab399e9378a8ce8d2e8a87bac07a5f4b4c409db5329db50274e01f660f5`. Only its explicit visible variational proof, equations (7)–(13), is imported.

No priority claim is made for the generic exclusion estimates. The specific contribution is their assembly into (3), the exact quotient bound (27), and the resulting actual-current correction (33) for this controlled memory family.
