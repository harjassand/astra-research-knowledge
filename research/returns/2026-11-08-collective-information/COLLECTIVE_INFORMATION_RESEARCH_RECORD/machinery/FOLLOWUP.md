# Cross-challenge and interacting-shell repair

7 November 2026. The independent initial remains frozen at `bcf64b92220176b0062cb04eb1c27da8dd13b9a0f5e24fe10cc8facbbe91fce6`. This follow-up reads the principal's `RELATIVE_ENERGY_CONSTRUCTION.md`, subsequent `MASS_METRIC_REPAIR.md`, and the auditor's frozen initial; no constructor work was read.

## 1. Principal mathematics checked

The relative-form Duhamel estimate checks in finite dimension with a fixed common Hilbert metric. For h_t=U_A(T,t)^*g, h'_t=A_t h_t, so its A-energy integral is (||g||²-||h_0||²)/2; the forward C-energy integral is at most ||f||²/2. Relative form control and A>=(1-d)C give d/[2 sqrt(1-d)]. Arbitrary time-dependent kinetic multipliers preserving the same pi are covered. Changing thermodynamic U generally changes pi and requires the separate finite-horizon argument.

The uniform count-shell variance calculation checks: the complete-graph rate-one exclusion gap is m; at most k(m-k) unordered swaps change a configuration; its Dirichlet form is at most k(m-k)L_s²/2. The two signs cost the stated factor two, and independent conditional blocks let their variances add. This yields C_c=4V_0, independent of the macroscopic gap. The killed Schur comparison also checks when the target is a union of count fibers. It controls the equilibrium-conditioned **mean** lifetime, not the exit distribution or all initial states.

The mass-metric repair checks as well. Put H=M^(-1/2) C M^(-1/2). In the polar decomposition M^(-1/2) C^(1/2)=H^(1/2)V, ||V||<=1. For z outside the angle pi/3 sector this proves

\[
 \|(zM-C)^{-1}C^{1/2}\|\le[(1-d)|z|]^{-1/2}.
\]

Since C>=(1-d)A, Douglas factorization permits replacement by A^(1/2) at another factor (1-d)^(-1/2). The resolvent identity

\[
 (z-B)^{-1}-(z-A)^{-1}
 =(zM-C)^{-1}[(C-A)-(M-I)A](z-A)^{-1}
\]

is correct for B=M^(-1)C; it includes the otherwise easily missed mass factor. The two terms are at most d/[(1-d)|z|] and 4d/[3(1-d)|z|]. The contour's left arc encloses zero, costs at most 2e d/(1-d), and its rays cost less than 3d/[pi(1-d)]. Thus the stated constant 8 is safe. No inverse gap appears. Applying M=diag(pihat/pi), C=M Bhat is valid when both frozen chains are reversible in their own measures. This repairs empirical stationary weights for **frozen** control. Arbitrary switched metric/form evolution is not proved by that autonomous contour argument.

No material algebraic error was found in these central statements. This is an internal mathematical check, not physical validation or historical priority.

## 2. Exact published overlap

**Hilder–Sharma, arXiv:2201.10256v2.** Theorem 3.1 assumes a finite irreducible L and uniform conditional LSI H(nu|rho_y)<=R_{L^y}(nu|rho_y)/alpha. Its stationary-conditional effective generator N satisfies

\[
 H(\widehat\mu_t|\eta_t)\le H(\widehat\mu_0|\eta_0)
 +C(L,N,\rho)\alpha^{-1/2}
 [H(\mu_0|\rho)-H(\mu_t|\rho)]^{1/2}.
\]

Uniform-time coarse-graining is therefore established prior machinery. Lemma 3.8 / Remark 3.9 disclose the effective-relaxation dependence of its time-uniform constant. Proposition 4.11 assumes reversible slow-fast chains, conditional LSI and uniformly positive coarse initial data; its improved entropy bound is proportional to epsilon T/alpha on finite [0,T]. The principal estimate is a special reversible, gap-independent alternative, not the invention of quantitative coarse-graining. Their LSI uses the paper's jump-process Fisher-information convention. [Primary text](https://arxiv.org/html/2201.10256v2); cache `source/2201.10256v2.{html,txt}`.

**Blassel, arXiv:2610.36078v1.** Definition 3 uses conditional laws of the **full microscopic QSD**. Theorem 5 assumes orthogonal decay C_zeta exp(-zeta t), zeta>2(lambda^X+gamma^X), and matching initial coarse laws. Bias is ||A^X||/zeta times C exp(-gamma^X T)+C'T exp[-min(gamma^X,gamma^Z)T]; constants use QSD eigenfunctions and the initial law. Theorem 7 / Corollary 8 establish O(epsilon) all-time adiabatic bounds with fixed positive reduced relaxation constants. The exit statement is **Proposition 11**, not Theorem 11: it bounds exit-event bias after surrogate decorrelation. It is not a relative mean-lifetime result independent of a reduced rare gap. The paper explicitly notes that constructing the canonical surrogate is generally impractical. [Primary text](https://arxiv.org/html/2610.36078v1); cache `source/2610.36078v1.{html,txt}`.

The principal combines established stochastic averaging, a useful elementary relative-form lemma, a size-uniform variance calculation, and reversible-network/Schur algebra. The distinguishing candidate is useful control even with an exponentially slow coarse killing scale and local acquisition precision. A deeper priority search in form perturbation of semigroups, singular perturbation, capacities and potential-theoretic metastability is still necessary. Novelty remains **UNKNOWN**.

## 3. Residual microscopic interactions: full conditional-variance extension

Take

\[
 E_t(x)=U_t(k(x))+\sum_r W_r(x_{V_r}).\tag{F1}
\]

Each W_r is fixed, known, finite range and bounded locally. Its one-spin and exchange increments are bounded by J_W,J_sw. Beta is fixed. There are no residual microscopic interactions across blocks; U_t may couple counts arbitrarily within its declared increment/evaluation budget. Changing W, beta or block size requires new conditional compilation/acquisition.

The exact conditional law is nu_{r,k}(x)=Z_{r,k}^{-1} exp[-beta W_r(x)] 1_{|x|=k}, independent of every future U_t. Hence P is fixed. Fast stirring MUST use W-reversible Kawasaki rates kappa exp[-beta Delta_swap W/2], not uniform swaps. Slow flips have rate

\[
 b_i(x_{N_i})a_i(x_{N_i},t)
 e^{-\beta\Delta_iW_r/2}e^{-\beta\Delta_rU_t/2},\tag{F2}
\]

with b,a excluding the central spin so they agree on a flip and its reverse.

**Exact import:** Boudou–Caputo–Dai Pra–Posta, arXiv:math/0505533v2, Theorem 3.1 uses normalized complete-graph rates m^{-1}exp(-beta Delta W/2). Its norm assumption is sup_i sum_{A containing i}|A|sup|Phi_A|<infinity. At sufficiently small beta it gives a gap lambda_*>0 uniformly in volume, density and boundary conditions. For finite-range potentials Corollary 3.3 gives the nearest-neighbor gap c_beta/diam(V_r)². Choose standard lattice blocks or verify the comparison-path geometry; finite diameter alone does not cover arbitrary disconnected regions. Multiplication by kappa scales the gap. Constants must be extracted with the actual potential/rate normalization; a spectral gap is not automatically a uniform LSI. [Primary text](https://arxiv.org/html/math/0505533v2); cache `source/0505533v2.{html,txt}`.

Put w_min=b_min a_min exp(-beta J_W/2), w_max=b_max a_max exp(beta J_W/2), K_sw=exp(beta J_sw/2). If a spin affects at most s local slow summands, swapping a pair changes each S_r^+/- by at most L_s=2s w_max. The normalized complete-graph W-Kawasaki Poincare inequality gives

\[
 \operatorname{Var}_{\nu_k}(S_r^+)
 \le\frac{K_{sw}L_s^2}{2\lambda_*m}k(m-k)
 \le\frac{K_{sw}L_s^2}{2\lambda_*}(m-k),
\]

and the minus bound uses k. Means are at least w_min(m-k) and w_min k. Therefore the principal proof extends with

\[
 V_W=\frac{e^{\beta J_U/2}K_{sw}L_s^2}{2\lambda_*w_{min}},\quad
 C_c=4V_W,\quad
 \gamma_F\ge\kappa\min_r c_\beta/\operatorname{diam}(V_r)^2.\tag{F3}
\]

Conditional blocks remain independent. This is a real nonuniform interacting-shell extension with d²=C_c/gamma_F and no macroscopic gap.

## 4. Conditional acquisition: actual mixing, measurement and calibration costs

At fixed m,W,beta, acquire all conditional local pattern probabilities needed by Delta_i W and b,a, for every count k. Let s now bound the required support size and chi be the calibrated single-site detector inverse norm. Corrected local-pattern scores have absolute value <=chi^s. For absolute pattern error delta_p,

\[
 M=O(\chi^{2s}\delta_p^{-2}\log(m^2 2^s/\delta))\tag{F4}
\]

fresh shell samples suffice. To give every forward and reverse total rate relative error eta, uniformly over all allowed positive local kinetic weights, it suffices conservatively to use delta_p=O(eta w_min/[m 2^s w_max]). Near-empty/full counts are why an m factor appears. Include positivity-projection factors, b calibration and systematic bias. The finite support and a_min>0,a_max<infinity are essential. Passive noisy count inversion is not assumed.

Prepare a known configuration of exact count k, pause slow flips, and run W-Kawasaki. Bounded local W gives nu_min>=2^{-m}exp[-beta osc W], with osc W=O(m). Reversibility and the spectral gap give the stronger relative mixing estimate

\[
 |P_t(x,y)/\nu_k(y)-1|
 \le e^{-\gamma_Ft}/\sqrt{\nu_k(x)\nu_k(y)}
 \le e^{-\gamma_Ft}/\nu_{min}.\tag{F5}
\]

Thus TV OR pointwise-relative conditional accuracy epsilon_mix is obtained in O(gamma_F^{-1}[m+log(1/epsilon_mix)]) time. Fresh reset/mix/readout trials are independent; a spaced single trajectory needs a conditional-freshness/martingale argument. Each record pays O(m) reset/readout operations and expected swap count

\[
 O\!\left(\frac{|E|\operatorname{diam}(V)^2}{c_\beta}
 e^{\beta J_{sw}/2}[m+\log(1/\epsilon_{mix})]\right).
\]

Kappa cancels from this event count. There are m+1 shells and M records per shell; all actual bath/work/control costs multiply these counts. No practical advantage has yet been shown.

The residual W changes the two-state calibration. Clamp its required neighbors and pause stirring. Starting at zero, with known Delta W,

\[
 p_b(h)=\frac{1-e^{-2b\cosh(\beta\Delta W/2)h}}{1+e^{\beta\Delta W}}.\tag{F6}
\]

Choose h=[4b_max cosh(beta J_W/2)]^{-1}. Then dp/db>=h exp(-beta J_W/2-1/2), so inverse Lipschitz constant is at most exp(beta J_W/2+1/2)/h. The principal's corrected binary Hoeffding acquisition applies with this constant, detector contrast and warranted systematic bias. The symmetric U=0 calibration formula is wrong if W remains present.

## 5. Frozen-control all-time repair with empirical conditional rates

The principal's recursive-ratio construction is operational after (F4)–(F6). For one block let the positive acquired bare rates a_hat,k^+/- have uniform relative error eta<=1/2. Define z_hat,0=1 and z_hat,k+1/z_hat,k=a_hat,k^+/a_hat,k+1^-. True detailed balance gives the same recursion for Z_k/Z_0. Every log-ratio error is <=4eta. Over all blocks with N total spins,

\[
 |\log(\widehat\pi_U/\pi_U)|\le8N\eta
\]

after normalization, uniformly over every new U. Learned driven rates a_hat,k^+/- exp(-beta Delta U/2) are exactly reversible in pi_hat,U. Put d_m=exp(8Neta)-1, d_q=eta and d=max(d_m,d_m+d_q+d_m d_q). The verified mass-metric lemma gives the learned-vs-exact-coarse observable error <=W 8d/(1-d), for d<1. Add the principal's microscopic averaging term W D(sqrt(C_c/gamma_F)), initial-source error and numerical error.

Hence eta=O(epsilon/[WN]) suffices for **frozen U and frozen kinetic control** at all horizons; acquisition is polynomial in N and inverse error, with the explicit conditional mixing/noise costs above. This closes the empirical-stationary-weight problem without pretending empirical rates preserve the true Gibbs measure. It does not justify arbitrary switching from a finite list of separately symmetrized kinetic tables whose inferred stationary measures differ.

For a fixed number of blocks, the full coarse state count is polynomial in N and a frozen semigroup may be evaluated with polynomial log(T) arithmetic/bit precision. A growing block count has an exponentially large count grid. Ordinary coarse trajectories cost O(T) jumps. These different computational contracts must stay separate.

## 6. Exact offline conditional compilation as an alternative

For a finite-range one-dimensional W, compute Z(z)=sum_x exp(-beta W(x))z^{|x|} with a position/last-r-bits/count dynamic program. All Z_k cost O(m²2^r) arithmetic. Constrain each needed local pattern and repeat; conservative total O(m³2^{O(r+s)}) arithmetic and O(m²2^{O(s)}) retained coefficients give every conditional pattern probability. Future U only multiplies these stored rates, so no conditional microscopic solve is repeated.

The learned b table can then remain inside exact conditional expectations, preserving the true pi_U and the principal's stronger common-pi time-dependent kinetic-drive certificate. General dimensions pay exponential elimination width; this is not a general efficient partition solver. Rational local Boltzmann and half-Boltzmann factors, or factors in one fixed-degree common algebraic field, give exact coefficients with polynomial bit length at fixed range. Unrestricted collections of algebraic numbers need additional degree accounting. General computable-real W needs interval compilation to the declared numerical workload; arbitrary rounded rows must not inherit an ideal infinite-horizon theorem silently. New block sizes need new conditional compilation.

## 8. Positive partition-ratio acquisition and relative lifetime repair

An independent way to obtain one kinetic-control-independent Z_hat table uses the positive insertion identity

\[
 s_k=E_{\nu_k}\left[(m-k)^{-1}\sum_{i:x_i=0}e^{-\beta\Delta_iW}\right],
 \qquad Z_{k+1}/Z_k=\frac{m-k}{k+1}s_k.\tag{F7}
\]

To prove it, multiply the unnormalized shell-k weight by the insertion factor; each shell-(k+1) state appears k+1 times. The positive observable lies between exp(-beta J_W) and exp(beta J_W). Z_0=exp[-beta W(0)] is known. Estimate each log s_k to eps_z/m; accumulated partition error then satisfies |log(Z_hat,k/Z_k)|<=eps_z. The finer 1/m precision is paid.

With local noisy detectors, the corrected insertion score has absolute bound at most m chi^s exp(beta J_W), including k=m-1. A conservative sufficient per-shell sample count is

\[
 M=O(\chi^{2s}e^{4\beta J_W}m^4\varepsilon_z^{-2}
       \log(m^2 2^s/\delta)).\tag{F8}
\]

Conditional mixing and residual detector bias must meet the corresponding absolute mean-error budget. More repetitions do not remove systematic bias. This is a safe polynomial bound, not an optimal or small practical cost. The conditional mixing/readout operations are exactly those already charged above.

Let a_k^+(a) be the conditional forward mobility total. Edge reversal gives M_k(a)=Z_k a_k^+(a)=Z_{k+1}a_{k+1}^-(a), because b and a agree on each microscopic flip and its reverse. Use positive estimates a_hat,k^+(a), uniformly log-relative eps_a accurate over allowed local weights a. Define

\[
 \widehat w_k=\widehat Z_k e^{-\beta U(k)},\quad
 \widehat c_k=\widehat Z_k\widehat a_k^+(a)
 e^{-\beta[U(k)+U(k+1)]/2},\quad
 \widehat q_{k,k+1}=\widehat c_k/\widehat w_k,\quad
 \widehat q_{k+1,k}=\widehat c_k/\widehat w_{k+1}.\tag{F9}
\]

This shared-flux construction is reversible in hat w for every future U and every frozen future a. Its stationary weights do not depend on a. True and learned unnormalized weights differ by exp(plus/minus eps_z), edge conductances by exp(plus/minus(eps_z+eps_a)), and rates by exp(plus/minus(2eps_z+eps_a)). The mass lemma supplies the same frozen-control all-time repair, with no unknown exact partition ratio left over. It does not prove arbitrary switched semigroups even though the learned mass is now fixed.

There is also a direct relative mean-lifetime comparison requiring no semigroup contour. For a transient count set C and killed unnormalized conductance Laplacian K,

\[
 \tau=\frac{w_C^T K^{-1}w_C}{w(C)}.\tag{F10}
\]

If pointwise hat w/w is within exp(plus/minus eps_z) and each conductance ratio is within exp(plus/minus eps_c), quadratic form comparison gives exp(-eps_c)K<=K_hat<=exp(eps_c)K. Its inverse is entrywise nonnegative, as a killed-chain Green matrix. The two positive weight vectors cost exp(plus/minus 2eps_z), inverse comparison costs exp(plus/minus eps_c), and normalization costs exp(plus/minus eps_z). Hence

\[
 e^{-(3\varepsilon_z+\varepsilon_c)}\tau
 \le\widehat\tau\le e^{3\varepsilon_z+\varepsilon_c}\tau.\tag{F11}
\]

For (F9), eps_c=eps_z+eps_a. Combining with the principal's Schur bound yields

\[
 e^{-(4\varepsilon_z+\varepsilon_a)}
 \le\tau_{micro}/\widehat\tau
 \le e^{4\varepsilon_z+\varepsilon_a}/(1-d^2).\tag{F12}
\]

No exponentially small killing gap appears even if tau grows exponentially in m. This compares equilibrium-conditioned mean lifetimes, not arbitrary sources or an exit-time law.

An operational source can be prepared by drawing counts from hat w conditioned on C, loading a known configuration at that count, and running W-Kawasaki to pointwise log-relative error eps_mix using (F5). Its density relative to the true equilibrium-conditioned source lies within exp(plus/minus[2eps_z+eps_mix]). Since hitting times are nonnegative, their actual mean differs by those same multiplicative factors; add 2eps_z+eps_mix to the exponents in (F12). A TV-only preparation promise would not establish such relative control for an unbounded hitting observable. A one-block birth/death positive-sum formula evaluates the learned mean in polynomial arithmetic/bit precision in m, input lengths and log tau. Increasing the number of blocks reintroduces the large coarse-state problem, and blockwise log errors add.

## 9. Supplementary finite check and extra predecessor

`check_residual_shell.py` exhaustively constructs a six-site model with nonuniform nearest-neighbor residual W, count-dependent nonconvex U, local neighbor-dependent mobilities and W-reversible nearest-neighbor swaps. It checks the count transfer polynomial, insertion identity, exact edge-flux identity, conditional coupling/gap certificate, killed mean-lifetime comparison and changed-mass semigroup bound across 121 times. `RESIDUAL_SHELL_CHECK.json` records residuals below 6e-14, microscopic/coarse lifetime ratio 1.00003612 below 1.00017214, and measured operator error 0.00201438 below 0.01866941. These are finite algebra diagnostics; they do not prove the general theorems, demonstrate physical advantage or establish priority.

Artur Stephan, *Coarse-graining and reconstruction for Markov matrices*, Z. Anal. Anwend. 44 (2025), 251–275, [DOI 10.4171/ZAA/1796](https://ems.press/content/serial-article-files/51411), is another directly inspected primary predecessor. Theorem 2.6 constructs the stationary-measure conditional reduction and preserves reversibility; Section 2.5 / Proposition 2.8 control error using the reduced spectral relaxation rate, with an analogous continuous-time statement. Its discrete-time exposition needs the usual spectral/aperiodicity qualifications; I do not import a claim that an arbitrary unique-invariant discrete Markov matrix converges at the real part of its second eigenvalue. The positive reversible heat-semigroup specialization is the relevant comparator. Full PDF/text are cached as `source/Stephan2025.{pdf,txt}`.

A further numerical-incumbent lead is Kannan–Sharpe–Swinburne–Wales, *Optimal dimensionality reduction of Markov chains using graph transformation*, J. Chem. Phys. 153 (2020), 244108, DOI 10.1063/5.0025174. Its supplied-network exact MFPT/graph-reduction approach should be compared when the full transition network is already known. Only its primary abstract/open manuscript landing result was inspected here; no detailed theorem from it is imported. It does not by itself acquire an exponentially large microscopic network from local experiments. Form-perturbation literature (Mugnolo–Nittka–Post, arXiv:1007.3932v2; Post–Simmer quasi-unitary equivalence) remains a primary priority-search lead, not a verified claim of an exact earlier identical bound.

## 7. Scientific status

The high-temperature conditional gap, fluctuation extension, finite noisy conditional acquisition and frozen-control mass repair collectively provide a substantive extension beyond exchangeable uniform shells. They use known count coordinates, known residual W, calibrated local controls and fast physical stirring. They do not discover a generic collective state or model an arbitrary fluid/solid.

The exact transfer-matrix alternative and the empirical-ratio construction overlap strongly with established conditional Monte Carlo, stochastic averaging, histogram/reweighting and reversible network theory. Novelty and practical advantage remain **UNKNOWN / NOT ESTABLISHED**. Source-specific mathematical gaps were not filled by a polished abstract.

The auditor checked that Han–Zhao–Li arXiv:2609.37392 has a withdrawn later v2. The frozen initial inspected v1 but omitted this current status; a consolidated dossier should record it without inferring that the mathematics is false. This researcher obtained the full Zenodo 22722557 PDF and checked its fixed-block N Q^{tau-1}P elimination, which the auditor had not yet retrieved at freeze.
