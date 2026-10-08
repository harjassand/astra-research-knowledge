# Astra 2026-10-08: far-from-equilibrium near-unit global entanglement

**Status:** New self-contained ideal-model mathematical derivation, cross-checked against exact sector dynamics and the repository's N131 witness; *no independent expert/priority review*. This addendum builds on `state/2026-10-08-finite-temperature-Maxwell-hydrodynamics.md` and `state/2026-10-08-full-proofs-and-audits.md`. No experimental demonstration, no independent research-agent pool, no claim of a field-breaking result.

## Main theorem: an asymptotically perfect entanglement test before thermal mixing

Fix a finite bath occupation `nu >= 0`. Prepare `N` qubits in `rho_N(0)=I/2^N`. Evolve with the exact **unnormalized**, uniform collective GKSL generator

`d rho/ds=(nu+1)D[J_-](rho)+nu D[J_+](rho)`, where `D[L](rho)=Lrho L† - {L†L,rho}/2`, and `J_a=(1/2) sum_i sigma_a^(i)`, `s=Gamma*t`.

For **any** deterministic sequence `c_N -> infinity`, `c_N=o(log N)`, set `s_N=c_N/sqrt N`. With `SEP_N` the full N-party separable convex set and `rho_N(infty)` the stationary state selected by `I/2^N`, as `N->infinity`,

`(A) dist_T(rho_N(s_N), SEP_N) -> 1`, and simultaneously

`(B) dist_T(rho_N(s_N),rho_N(infty)) -> 1`.

`dist_T` means HALF trace norm. These are mathematically maximal asymptotic distances. The first assertion has a constructive **single-copy local-product measurement with shared classical randomness and one classical postprocessing step**; no entangling quantum measurement is needed. Assertion B follows from the universal Maxwell crossover and the subcritical `s_N=o(log N/sqrt N)` limit, not simply from expectation values.

Quantifiers: fixed `nu`, `N->infinity` first; `c_N` grows slower than `log N`. No claim for `nu=nu(N)`, non-collective noise, inhomogeneous couplings, all initial states, GME/depth>2, distillability, or fixed laboratory `N`. `J_±/sqrt N` physical jump normalization multiplies all times by `N`, i.e. here `t_N=c_N sqrt N/Gamma`.

## Proof I: transverse-spin variance tends to zero in units of N

Spin length j=M/2 is conserved by the ideal dissipator. The exact total-spin distribution under maximally mixed input is

`w_{N,M} = [(M+1)^2/(N/2+M/2+1)]*binom(N,(N-M)/2)/2^N`, `M ≡ N (mod 2)`, `0<=M<=N`.

The law of `X_N=M/sqrtN` tends to Maxwell density `f(x)=sqrt(2/pi)x^2 exp(-x^2/2)`, `x>0`. Moreover `E[X_N^2]=3 -2 E[M]/N <=3` and `E[X_N^2]->3=E_f[x²]`, since `E[J²]=3N/4`; thus `{X_N²}` is uniformly integrable.

Conditional on sector M, write k=0,...,M for excitation above bottom weight m=-M/2, with uniform initial law. The exact jump rates are

`lambda_k=nu(M-k)(k+1)`, `mu_k=(nu+1)k(M-k+1)`.

In macroscopic clock c= s sqrtN and `y=k/M`, generator drift is exactly

`b_{N,M}(y)=-(M/sqrtN)y(1-y) + [nu-(2nu+1)y]/sqrtN`, while quadratic variation rate is <= `C_nu/sqrtN`, uniformly all M>=1 and k. For any fixed compact a<=M/sqrtN<=R, with a>0 and R finite, compare the stochastic process on `[0,c_N]` with the logistic ODE `dot z=-x z(1-z)`, `x=M/sqrtN`, solution

`z_x(c;u)=u/[u+(1-u)e^(xc)]`, `u=k(0)/M`.

Doob + Lipschitz Gronwall (|F'_x|<=R) bounds the expected maximal error by

`E sup_{c<=c_N}|y(c)-z_x(c;y(0))| <= e^(R c_N) [C_nu c_N/sqrtN + C_nu sqrt(c_N/sqrtN)]`.

Since `c_N=o(log N)`, the right side tends to zero for every fixed compact `[a,R]`. Initial k uniform means y(0) asymptotically uniform on [0,1]. For all x>=a and u<1, `z_x(c_N;u)->0`, so `E[y(c_N) | M] ->0` uniformly for `a sqrtN <=M<=R sqrtN`. The endpoint u=1 has negligible mass 1/(M+1). Using the Maxwell-law uniform integrability of X_N², extend to all M:

`E_{M,k}[ (M²/N) y(c_N)] ->0`.

The state remains axially invariant so `E J_x=E J_y=0`. In each sector,

`J_x²+J_y²= j(j+1)-m²=M/2 + M²y(1-y) <= M/2+M²y`.

Consequently, with `v_N=Var J_x+Var J_y`,

`0<=v_N/N<=E[M]/(2N) + E[(M²/N)y(c_N)] ->0`.

**Check independent fixed-c limit:** At any fixed c, `v_N/N -> V(c)=integral_0^infinity f(x)x² g(cx) dx`, with `g(z)=integral_0^1 z_x(z;u)(1-z_x(z;u))du=-mu'(z)` and `mu(z)=[ze^z-(e^z-1)]/(e^z-1)^2` (`mu(0)=1/2`). The sequential tail is

`V(c) ~ K c^(-5)` as `c->infinity`, `K=sqrt(2/pi)*(4pi^4/5)=62.176967854...`.

To see this, substitute t=cx and use `f(x)~sqrt(2/pi)x²`: `c^5 V(c) -> sqrt(2/pi) int_0^infinity t^4[-mu'(t)]dt`. Integrating by parts gives 4 int t³ mu(t)dt. Expand `mu(t)=sum_{n>=1}(n t-1)e^(-nt)`; then int t³ mu(t)dt=18 zeta(4)=pi^4/5. These are **sequential** N then c limits; this note does NOT yet assert the uniform joint asymptotic `v_N/N~K c_N^-5` for every growing c_N, which would require sharper uniform estimates. It is not needed for the theorem.

## Proof II: a one-copy LOCC-compatible distinguisher for the entire fully separable set

On each prepared N-qubit state draw `theta` uniformly on `[0,2pi)` **after preparation**, broadcast it as classical randomness, and independently measure each qubit in the sigma_theta=cos theta sigma_x+sin theta sigma_y basis. Denote sum (eigenvalues ±1/2) by `J_theta`. Accept `|J_theta|<=w_N`. This one-copy test does not require prior knowledge of which separable state the adversary supplies.

For the target, `E[J_theta]=0` by phase covariance, and average over uniform theta of `Var[J_theta]` is `v_N/2`. Therefore Chebyshev gives

`Pr_target[accept]>=1 - v_N/(2 w_N²)`.

For **any product** `sigma_1 tensor ... tensor sigma_N`, write planar Bloch components of sigma_i as r_i∈R² with ||r_i||<=1. Conditional on theta, the independent ±1/2 outcomes have variance

`V_theta= [N - sum_i (r_i·n_theta)^2]/4`.

Choose theta0 along the largest eigenvector of the 2x2 Gram matrix `S=sum_i r_i r_i^T`, whose trace <=N. From lambda_max(S)+lambda_min(S)<=N, one obtains `V_theta >=(N/8) sin²(theta-theta0)` (indeed the minimum over S at each angle satisfies this; direct proof by splitting lambda_max<=N/2 vs >N/2). An independent-Poisson-binomial Fourier bound gives for any lattice atom

`sup_m Pr[J_theta=m] <= C /sqrt(max{V_theta,1})`.

Any interval `|J_theta|<=w_N` contains at most `2w_N+2` lattice values. Thus

`Pr_product[accept|theta] <= min{1,C'(w_N+1)/(sqrtN |sin(theta-theta0)|)}`.

Integrating theta gives uniform upper bound

`q_N := sup_{sigma in SEP_N} Pr_sigma[accept] <= C'' a_N [1+log(1/a_N)]` when `0<a_N:=(w_N+1)/sqrtN<1/2`.

This extends to **all** fully separable states by convexity and uniformity in the product constituents. The source repository's N131 contains an explicit sharpened form `q<=B(a)=(2/pi)[arcsin a+a ln((1+sqrt(1-a²))/a)]` with `a=2sqrt(pi)(w+1)/sqrtN`; the self-contained argument above only needs the weaker bound and does not assume the N131 constant independently proved.

Set `eps_N=v_N/N->0`, and choose `w_N=sqrtN eps_N^(1/4)` (if eps_N=0 choose instead N^1/4; add integer rounding as necessary). Then `v_N/(2w_N²) <=.5 sqrt(eps_N)->0` and `a_N->0`, so `p_N:=Pr_target[accept]->1`, `q_N->0`. By data processing for trace distance,

`inf_{sigma in SEP_N} .5||rho_N(s_N)-sigma||_1 >= p_N-q_N ->1`.

Even a single chosen random local measurement setting distinguishes the target from the ENTIRE convex SEP set with vanishing (target error + uniform separable false positive). All N local single-spin measurement outcomes must be collected/classically summed; detector axis error and calibration are not automatically free. For an actual finite-N certificate, evaluate explicit measured v_N and choose a certified w_N and q_N; no rate-uniform useful finite-N performance is claimed.

**Stronger information-theoretic consequence.** This same two-outcome **one-copy LOCC** measurement yields, by classical data processing,

`inf_{sigma in SEP_N} D(rho_N(s_N)||sigma) >= p_N log(1/q_N)-h(p_N) -> infinity`, where D is quantum relative entropy, h binary entropy.

It also bounds the regularized relative entropy of full multipartite entanglement `E_R^infty` from below by this binary KL asymptotically, **provided** each of m copies is tested sequentially with fresh theta and each lab holds one register per copy. For any m-copy competitor fully separable across N laboratories (but arbitrary entanglement *within* each laboratory across its m copies), conditional on previous measurement outcomes the untested N-register state remains fullSEP across labs. Thus its conditional pass probability <=q_N; the true m-copy target produces iid Bernoulli(p_N). The chain rule and classical data processing show `D(rho_N^{tensor m}||sigma_m)>=m*d(p_N||q_N)`. After minimization and regularization, `E_R^infty(rho_N) >= d(p_N||q_N) ->infinity`. The quantity diverges without a claimed universal explicit rate in N on the growing-c_N window.

## Proof III: still maximally far from thermal equilibrium

From the already proved full positive-temperature Maxwell mixing profile, for every fixed nu>=0 and any `s_N=o(logN/sqrtN)`, the sector TV distance to its own selected stationary state approaches 1. In particular `s_N=c_N/sqrtN`, `c_N=o(logN)` satisfies this, independently of Proof II. Therefore both distances in the Main theorem simultaneously tend to 1. Note stationary global fullSEP distance also tends to1, but that alone does not imply the transient lower bound; the actual early-time transverse-variance argument is necessary.

## Mechanism and practical costs

- Separation of emergence of detectable entanglement (c=O(1) in s=c/sqrtN), near-unit global entanglement and unbounded E_R^infty (c_N->infinity), and mixing to the selected stationary state (s~logN/sqrtN). This is a genuine *intermediate pre-equilibrium information-theoretic state* in the ideal model.
- Test uses one N-qubit preparation plus N local spin readouts and one uniform common setting; no entangling measurement. To estimate real success probabilities p/q with confidence, replicate, using O(eps^-2 log(1/delta)) preparations for additive confidence eps, but actual p and q approach 1 and 0 only asymptotically. Calibration of θ and detector counts requires precision proportional to chosen width w_N, and finite coherence time/collective coupling still need engineering.
- If each local spin is independently depolarized after preparation by fixed lambda<1, transverse variance generically acquires an O((1-lambda²)N) term; this **specific near-unit SEP-distance test no longer works**. The N135 stationary witness can still detect entanglement at fixed lambda but does not restore this theorem. Joint full noise robustness remains open. o(1) trace-error of the entire N-qubit state preserves a near-unit bound by triangle inequality.
- No extension to GME, positive distillation rate, computational advantage, Hamiltonian ground-state preparation, macroscopic Bell nonlocality, or state distance from 2-producible states: Astra N120 claims all-time 2-producibility for this ideal trajectory.

## Literature contrasts, novelty and skeptical audit

Prior works: Li-Xu2005 for related small-system common-bath effects; Bassler2025 PRA *Absence of entanglement growth in Dicke superradiance* (doi:10.1103/qxx1-xr44), which instead starts from a fully excited permutation-symmetric **product** state and proves separability preservation; Rosario et al 2025 PRL (doi:10.1103/xcxr-sm9c) same initial state and CSS mixture; Malz-Trivedi-Cirac2022 PRA large-N superradiance (doi:10.1103/PhysRevA.106.013716); Mathé et al 2026 Quantum *Estimating the best separable approximation of non-pure spin-squeezed states* (doi:10.22331/q-2026-04-21-2078), general distance-to-SEP methods on collective states; Mok et al *Nature Physics* Sept 25 2026 collective decay-rate scaling, a distinct quantity (doi:10.1038/s41567-026-03448-4). These are not priority clearance. Our **different starting condition** is maximally mixed on the full N-qubit Hilbert space, containing all Schur sectors, not a fully inverted product or symmetric-only preparation. No field-breaking/unpublished priority declaration until complete expert literature audit and independent proof review.

Independent formal check obligations: simplify the product-Gram angular bound and lattice point Fourier constant; replay variance ODE-Gronwall on short growing windows; verify conditional fully separable structure after adaptive classical measurement when laboratories hold multiple copies; find prior art for optimal local randomized fullSEP discrimination and transient almost-unit distance.

## Experiments and archived evidence

`transverse_variance_check.py` numerically integrated the fixed-c limiting variance, obtaining V(0)=.5, V(2)≈.13217579, V(5)≈.00942969, V(10)≈.00049939, V(20)≈.00001834; c^5V(c) approaches K≈62.17697. Exact sector matrix-exponential finite-N examples at N<=96 show very large finite-size corrections for c=5 (e.g. nu=.2,N=96), so the asymptotic measurement guarantee is **not** a near-term hardware performance claim. Existing archived checker `check_polarization_finiteN.py` separately verifies the first moment of the same dynamics and `verify_hitting_moments.py` checks sector hitting moments. Exact N3 NPT certificate is at `certify_thermal_npt.py` and is logically separate from this asymptotic result.

The finite-temperature hydrodynamic proof and all previous failures remain preserved; append this document rather than overwriting history.