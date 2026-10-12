# Acquisition-aware capacity enclosure for a layered rare-transition model

**Status, 12 October 2026:** a proved, model-conditional two-sided relative certificate for an exponentially wide reversible network. The Schur-complement and variational principles are established tools; this note makes no novelty or advantage claim. The result is useful as a concrete boundary case: a rare capacity is certifiable without enumerating exponentially many microstates when an exact layer aggregate and a strong transverse gap are part of the acquired model contract.

## Exact model and admission gate

Fix integers `d >= 1` and `n >= 2`. The state space is the layered hypercube

\[
V=\{0,1,\ldots,n\}\times\{0,1\}^d,
\qquad m=2^d.
\]

The terminal sets are the complete end layers `A={0} x {0,1}^d` and `B={n} x {0,1}^d`. Between levels `k` and `k+1`, for `0 <= k < n`, the conductance of the edge at microstate `i` is

\[
c_{k,i}=g_k(1+\delta_{k,i}),\qquad g_k>0.
\]

Within each internal level `1 <= k < n`, connect every hypercube-neighbor pair `i,i xor e_j` with conductance `kappa/d`, where `kappa>0`. There are no other edges. Set

\[
j_k=1+(k\bmod d),\qquad \sigma_k=k\bmod 2,
\qquad \delta_{k,i}=\rho(-1)^{i_{j_k}+\sigma_k},\qquad 0\leq\rho<1.
\]

Thus half the longitudinal edges in every layer have conductance `g_k(1+rho)` and half have `g_k(1-rho)`, and the layer sum is exactly `m g_k`. The perturbation formula is a compact input certificate: it covers all `2^d` edges without inspecting them. The hypercube and its gap are also implicit in `d`, not supplied as an edge list.

This is a finite reversible continuous-time Markov chain: take uniform stationary measure `pi(x)=1/|V|` and rates `q(x,y)=c_xy/pi(x)` on each undirected edge. The quantity certified below is the network capacity between the two end layers. Interpreting its inverse as a mean transition time additionally needs the usual metastable-set assumptions; this note does not assert that approximation.

**Admission gate.** The source must provide (and the verifier must check) `d,n,rho,kappa`, the exact hypercube/perturbation rule above, and one certified log-conductance interval for every base rate `g_k`. Let `C_model` be the charged cost to acquire and validate that compact descriptor, and `c_g` the cost of one certified base-rate query. Querying all `n` base rates and scanning their intervals costs `C_model+n c_g+O(n)`. The explicit graph has `(n+1)2^d` states and `n2^d+(n-1)d2^{d-1}` edges, so this bound depends on the compact source contract. A local-transition oracle that does not certify the full state-space rule, the exact zero-mean sums, and the transverse gap does not pass this gate.

Write

\[
G=\max_{0\leq k<n}g_k,
\qquad R=\sum_{k=0}^{n-1}g_k^{-1},
\qquad C_0=\frac{m}{R}.
\]

For target relative width `1+epsilon`, with `0<epsilon<1`, set

\[
t=\frac{\epsilon}{2+\epsilon},\qquad \gamma=\frac{2\kappa}{d}.
\]

The exact-arithmetic gate is

\[
4\rho^2G\leq t\gamma.
\tag{G}
\]

Under (G), capacity lies in `[(1-t) C_0, C_0]`. The interval ratio is at most `1/(1-t)=1+epsilon/2`. If every acquired `log(g_k)` is only known in an interval and the resulting interval for `R` has ratio at most `1+t`, the reported capacity interval still has ratio at most `1+epsilon`.

In particular, if `g_k=s a_k` with a common rare scale `s=exp(-beta Delta)` and positive `a_k`, then `C_0=s m/(sum 1/a_k)` and the cost remains `O(n)` rate acquisitions. When `kappa` is fixed, (G) becomes easier as `s` decreases. Computation should retain `log(g_k)` and use log-sum-exp, so the work and interval do not depend on representing `exp(beta Delta)` as an ordinary floating-point number.

## Theorem and proof

Let `cap(A,B)` be the Dirichlet capacity, the minimum of

\[
\mathcal E(u)=\sum_{\{x,y\}}c_{xy}(u_x-u_y)^2
\]

over `u=0` on `A` and `u=1` on `B`. Then

\[
(1-t)\frac{2^d}{\sum_k g_k^{-1}}
\;\leq\;\operatorname{cap}(A,B)
\;\leq\;\frac{2^d}{\sum_k g_k^{-1}}.
\tag{1}
\]

Here is the explicit low/high decomposition behind the certificate. Let `P` replace a function by its arithmetic mean on every layer; write `u_{k,i}=x_k+y_{k,i}`, where `sum_i y_{k,i}=0` on every internal layer and `y_0=y_n=0`. The coarse energy is

\[
A(x)=m\sum_{k=0}^{n-1}g_k(x_{k+1}-x_k)^2.
\]

Let `D` be the hidden-fluctuation block of the conductance Laplacian and `B x` the hidden component of the Laplacian applied to the layer-constant profile `x`. The hypercube Laplacian with edge conductance `kappa/d` has first nonzero eigenvalue `gamma=2 kappa/d`. The longitudinal part of `D` is nonnegative, so

\[
D\succeq\gamma I.
\tag{2}
\]

The coupling includes both boundary-adjacent layers. At internal level `k`, after projecting away the layer mean,

\[
(Bx)_{k,i}
=g_{k-1}\delta_{k-1,i}(x_k-x_{k-1})
 +g_k\delta_{k,i}(x_k-x_{k+1}).
\]

Using `|delta|<=rho`, `||a+b||^2<=2||a||^2+2||b||^2`, and `g_k<=G`,

\[
\begin{aligned}
\|Bx\|_2^2
&\leq 4\rho^2m\sum_k g_k^2(x_{k+1}-x_k)^2\\
&\leq 4\rho^2G\,A(x).
\end{aligned}
\tag{3}
\]

In matrix language, `Gamma=B^*B <= 4 rho^2 G A`. Under (G), `Gamma <= t gamma A`. Eliminating the hidden fluctuations gives the exact Schur complement `S=A-B^*D^{-1}B`; (2) and (3) imply

\[
(1-t)A\preceq S\preceq A.
\tag{4}
\]

The capacity is the minimum of the reduced form over coarse profiles with `x_0=0,x_n=1`. By Cauchy-Schwarz,

\[
1=\left(\sum_k(x_{k+1}-x_k)\right)^2
\leq\left(\sum_k g_k(x_{k+1}-x_k)^2\right)
      \left(\sum_k g_k^{-1}\right),
\]

with equality when `x_{k+1}-x_k` is proportional to `1/g_k`. Hence `min A=C_0`, and (4) gives (1).

The proof covers the entire transverse state space through two verifiable certificates: exact zero-mean conductance perturbations and a global hypercube spectral gap. It does not estimate a rare event by observing successful transitions. There is no omitted tail in this finite model. The longitudinal coordinate is fully scanned; the exponential cross section is covered by the algebraic aggregate and gap.

### Finite-precision output

Suppose acquisition returns `ell_k^- <= log(g_k) <= ell_k^+`, with every width at most `log(1+t)`. Define

\[
R_- =\sum_k e^{-\ell_k^+},\qquad
R_+ =\sum_k e^{-\ell_k^-},\qquad
G_+=\max_k e^{\ell_k^+}.
\]

Then `R_- <= R <= R_+`, `R_+/R_- <= 1+t`, and `G<=G_+`. Check the gate using `G_+`; if it passes, return

\[
\left[(1-t)\frac{2^d}{R_+},\;\frac{2^d}{R_-}\right].
\tag{5}
\]

Its lower endpoint is positive and its endpoint ratio is at most

\[
\frac{1+t}{1-t}=1+\epsilon.
\]

This is a deterministic certificate conditional on the source intervals and model description being valid. Its total cost is `C_model+n c_g+O(n)`; it does not cost `2^d` edge acquisitions. The precision required of each log-rate interval is `log(1+t)`; for an Arrhenius input `g_k=g_* exp(-beta E_k)`, an energy oracle must therefore certify `E_k` to width at most `log(1+t)/beta` (after accounting for prefactor uncertainty). This per-query precision cost is part of acquisition. If the gap gate fails, the uniform-lane Thomson flow still gives the wider interval `[(1-rho^2)2^d/R_+, 2^d/R_-]`, whose ratio is at most `(1+t)/(1-rho^2)`; the narrow-width theorem makes no promise.

## Diagnostic showing why the gap gate matters

Take `d=1,n=2,g_0=g_1=1`, with opposite perturbation signs in the two longitudinal layers: `delta_0=(rho,-rho)`, `delta_1=(-rho,rho)`. Let the one transverse edge between the two internal states have conductance `kappa`. Both layer totals equal `2`, so the coarse capacity is `C_0=1`. Solving the two harmonic equations gives

\[
\operatorname{cap}(A,B)=1-\frac{\rho^2}{1+\kappa}.
\tag{6}
\]

At `kappa=0`, the capacity is `1-rho^2`, which can be arbitrarily smaller than the coarse answer even though every edge is listed and every layer sum is known exactly. As `kappa` grows, transverse equilibration removes the discrepancy. This is also a boundary-term check: heterogeneity on the two edges incident to the fixed terminal layers drives the hidden internal mode. An internal-only Laplacian block can have a zero low/high off-diagonal while the boundary forcing still produces the correction in (6). The coupling map in (3) therefore retains both adjacent longitudinal slices.

In the hidden unit vector proportional to `(1,-1)`, `D` has eigenvalue `2(1+kappa)`. For the layer-constant profile with endpoints `0,1`, the internal coupling vector is `(rho,-rho)`, so its Schur energy subtraction is `||Bx||^2/D=2rho^2/[2(1+kappa)]=rho^2/(1+kappa)`, exactly the deficit in (6). This small case checks that a transfer condition must include the boundary-adjacent response, even when the interior block alone reports no coupling.

## Acquisition and failure boundary

The compact representation is doing essential work. The verifier can establish `sum_i delta_{k,i}=0`, `|delta_{k,i}|=rho`, and the hypercube gap without enumerating states because the model names the exact bit rule. It still acquires all `n` base barriers or rates. If a physical source only offers named local probes and does not provide an auditable full-support rule, the hidden-channel obstruction in `HIDDEN_CHANNEL_BOUND.txt` remains applicable: an unqueried high-conductance edge can invalidate the assumed layer sum. This theorem is not a way to infer the compact representation from a few observations.

The absolute rare scale is also conditional on the transverse rate. The useful regime is either a common small scale on all `g_k` with transverse transitions not scaled down as fast, or a checked inequality (G). If both `g_k` and `kappa` are multiplied by the same small factor, (G) is scale invariant, so the certificate can still pass; if transverse mixing is weakened relative to the active vertical coupling, the relative bracket can widen. If `rho` is close to one and the transverse gap is absent, (6) shows that exact layer aggregates alone are insufficient.

## Strongest comparator checked

The primary source by den Hollander and Jansen was retrieved as full HTML; its relevant theorem statements and comparison were inspected. Theorem 1.1 gives the Berman-Konsowa path principle for finite oriented self-avoiding paths, with edge-use measure absolutely continuous with respect to conductance. Theorem 1.4 gives the equivalent unit-flow form. Equation (1.15) is Thomson's principle, and (1.16) proves by Jensen that a Berman-Konsowa path lower bound is at least the Thomson lower bound for the same flow. These identities already make the capacity the supremum of path/flow lower bounds; no new variational principle is claimed here.

For a concrete matched baseline, send a unit flow `1/m` along each fixed-microstate vertical lane. Since every layer has half `+rho` and half `-rho`, its Thomson resistance is

\[
R_{\rm lane}=\sum_{k,i}\frac{(1/m)^2}{c_{k,i}}
=\frac{R}{m(1-\rho^2)},
\]

so Thomson certifies `cap >= (1-rho^2) C_0` at the same `O(n)` base-rate acquisition cost. Berman-Konsowa on this flow samples a uniform lane `I` and uses

\[
Z_I=\frac{m}{\sum_k [g_k(1+\delta_{k,I})]^{-1}}.
\]

It can improve this particular Thomson bound; a path sample is bounded between `(1-rho)C_0` and `(1+rho)C_0`, and repeated samples can estimate its expectation with ordinary bounded-variable concentration. However, this fixed-lane law does not exploit `kappa`; in (6), its lower bound remains `1-rho^2` as `kappa` tends to infinity. Other path laws, especially one close to the harmonic flow, can be stronger. The Berman-Konsowa supremum equals capacity, so the present result is an acquisition-aware structural certificate against a chosen coarse model, not an advantage over the optimal variational comparator.

The Schur complement itself is also established Kron reduction. Dörfler and Bullo explicitly define the reduced Laplacian as `Q_aa-Q_ab Q_bb^{-1} Q_ba` and discuss effective resistance. The specific estimate here is the explicit active-Gram bound (3) for this layered input contract. Whether that specialization is independently useful or already subsumed by a direct known coarse-graining theorem remains unresolved; no priority claim is made.

Primary sources and read depth:

- den Hollander and Jansen, *Berman-Konsowa principle for reversible Markov jump processes*, [arXiv:1309.1305](https://arxiv.org/html/1309.1305), full HTML retrieved; Theorems 1.1 and 1.4, equations (1.15) and (1.16), and path admissibility inspected.
- Dörfler and Bullo, *Kron Reduction of Graphs with Applications to Electrical Networks*, [arXiv:1102.2950](https://arxiv.org/abs/1102.2950), arXiv source retrieved; the exact Schur-complement reduction statement and its effective-resistance context inspected.

## Route change and outcome

The first attack was a one-dimensional birth-death chain with conductances `c_k`. Its capacity is exactly `(sum_k 1/c_k)^-1`. More generally, if `r(x)=1/c(x)` and `log r` is globally `L_0`-Lipschitz on a complete interval of length `ell`, a block of diameter `h` anchored at `x_j` has `r(x_j)e^{-L_0h}<=r(x)<=r(x_j)e^{L_0h}`. Summing these bounds gives an integral enclosure with ratio at most `e^{2L_0h}`; choosing `h<=log(1+epsilon)/(2L_0)` uses `O(L_0 ell/log(1+epsilon))` acquisitions, independent of the absolute barrier offset. This is a sound global-coverage result, but the serial capacity identity is already exact and lies inside classical Thomson/Berman-Konsowa theory. It does not exercise hidden transverse states or improve the strongest variational comparator, so I stopped that direction rather than presenting quadrature as a rare-event discovery.

The changed attack keeps the slow reaction coordinate but gives each level `2^d` hidden configurations and adds a certifiable transverse mixer. The hidden fluctuation block now matters. An exact aggregate plus the active-Gram/spectral-gap gate proves a `1+epsilon` interval using `O(n)` acquired rates, with all exponential-width states covered. The result survives as a bounded, conditional capability for this synthetic model. It does not establish a general molecular rate algorithm, a sample-only global-coverage method, or novelty over Kron reduction or Berman-Konsowa.

## Input-path note

The requested `research/2026-10-12-frontier/root/rare_event_opening/PRIOR_ART_AND_OPENING.md` was not present in this checkout at inspection time. `CROSS_FLUX_SAMPLER.txt` and `HIDDEN_CHANNEL_BOUND.txt` were present and read. The comparator check above was performed directly from the primary arXiv sources, so the missing local opening did not block this bounded investigation.
