# A spectral decision envelope learned from imperfect experiments

## Status and scope

This is a proved synthesis / research direction, not a claim that eigenvalue cutting planes or convex approximation are new. The candidate contribution is a *uniformly certified, reusable computational quotient* for an entire class of future decisions, together with an adaptive acquisition rule whose failure produces the next useful experiment. It avoids operator-algebra recovery entirely. Its explicit limitation is low control dimension; it does not solve general switching or nonconvex planning.

## Consequential capability

An unknown fixed Hermitian pencil is

\[
H(u)=H_0+\sum_{i=1}^d u_iH_i,\qquad u\in D\subset\mathbb R^d,
\]

where the compact polytope D and bounds on the coefficient norms are known. The physical meaning can be a tunable symmetric dissipative system
\(\dot x=-H(u)x\). If \(f(u):=\lambda_{\min}H(u)\ge\gamma\), then
\(\|x(t)\|\le e^{-\gamma t}\|x(0)\|\) for every initial condition. Thus choosing a static design with high f is a genuine worst-case stability task.

After acquisition, an unbounded number of new linear prices c and new polytopal resource constraints \(S\subseteq D\) may arrive. The intended reusable capability is to solve

\[
\max_{u\in S}\{f(u)-c^Tu\}
\]

within a certified tolerance, or find a design with a specified decay margin, without further physical experiments or n-dimensional linear algebra. Future inverse queries, arbitrarily long switching schedules, and nonconvex control constraints are outside this capability.

## The experimental interface

For any chosen vector v, coefficient i returns

\[
\mathcal O_i(v)=H_iv+e_i(v),\qquad \|e_i(v)\|\le\eta_i\|v\|.
\]

The errors may depend on previous queries. This is a strong full-vector interface, explicitly charged as one n-vector experiment. A known norm/range bound is needed to certify unseen spectral modes. Such a bound cannot be inferred deterministically from a proper subspace of vector queries.

Let \(|u_i|\le R_i\) on D and
\(\mu=\eta_0+\sum_iR_i\eta_i\). For a unit vector v record
\(a_i=\operatorname{Re}\langle v,\mathcal O_i(v)\rangle\). The affine function

\[
q_v(u)=a_0+\sum_i u_i a_i+\mu
\]

is a certified upper bound on \(v^*H(u)v\), hence on f(u), throughout D. It overestimates that Rayleigh quotient by at most \(2\mu\). Finite arithmetic error can be included in the \(\eta_i\) budget.

An acquisition eigensolver must earn, rather than assume, a unit vector satisfying
\(v^*H(z)v\le f(z)+\tau\). Define

\[
\ell_z=a_0+\sum_i z_i a_i-\eta_0-\sum_i |z_i|\eta_i-\tau.
\]

Then
\[
f(z)-\kappa\le\ell_z\le f(z),\qquad
f(u)\le q_v(u)\ \forall u\in D,\qquad
q_v(z)\le f(z)+\kappa,
\]

with \(\kappa=\tau+2\mu\). Also \(q_v(z)-\ell_z\le\kappa\). An ordinary eigenpair residual alone does **not** establish the approximate minimum property; it can belong to the wrong eigenvalue. A randomized gap-free spectral procedure or a full reconstruction fallback is required. A constructive noisy polynomial-filter procedure is given below.

Let f have Lipschitz constant L on D, for example
\(L\le(\sum_{i=1}^d\|H_i\|^2)^{1/2}\). The stored q functions have Lipschitz constant at most
\(M=L+(\sum_{i=1}^d\eta_i^2)^{1/2}\).

## Acquisition algorithm

1. Obtain a witness q at any point of D. Set \(F(u)=\min_{j\le r}q_j(u)\).
2. Form the active cells
   \[
   C_j=\{u\in D:q_j(u)\le q_k(u)\ \forall k\}.
   \]
   These are explicit polytopes; enumerate their vertices, merging duplicates.
3. At each current cell vertex z, obtain a valid lower spectral bound \(\ell_z\). If
   \(F(z)-\ell_z>\varepsilon\), add its accompanying witness q and restart the cell check.
4. If every current cell vertex satisfies \(F(z)-\ell_z\le\varepsilon\), return the affine bank and the vertex certificates. Previously acquired lower bounds may be cached.

All representation choices are learned. No invariant subspace, block decomposition, low-rank algebra, or supplied reduced model enters the algorithm.

## Theorem: termination and reusable decision sufficiency

Assume every acquisition oracle call has the properties above, \(2\kappa<\varepsilon\), D lies in a Euclidean ball of radius R, and all cell vertices are enumerated. Then:

1. The algorithm terminates after at most
   \[
   N\le\left(1+\frac{2R(M+L)}{\varepsilon-2\kappa}\right)^d
   \]
   witness additions (up to taking an integer ceiling).
2. Its returned envelope satisfies the uniform certificate
   \[
   0\le F(u)-f(u)\le\varepsilon\qquad\forall u\in D.
   \]
3. For any later polytope \(S\subseteq D\) and linear price c, solve the explicit LP
   \[
   \max_{u,t}\ t-c^Tu\quad
   \text{s.t. }u\in S,\quad t\le q_j(u)\quad(j=1,\ldots,r).
   \]
   Its returned control is \(\varepsilon\)-optimal for the true objective. If the returned control is feasible and the LP has a certified primal-dual objective gap \(\delta_{LP}\), the true gap is at most \(\varepsilon+\delta_{LP}\).
4. If that LP returns value V, the true optimum is in \([V-\varepsilon,V]\), before accounting for LP numerical tolerance.
5. A candidate u with \(F(u)\ge\gamma+\varepsilon\) has true worst-case decay margin at least \(\gamma\). Its safety certificate applies to every n-dimensional initial condition.

### Proof of the uniform certificate

Every q is an upper bound on f, so \(F\ge f\). On cell \(C_j\), \(F=q_j\) is affine. The minimum eigenvalue of an affine Hermitian pencil is concave, since
\[
f(u)=\inf_{\|v\|=1}v^*H(u)v
\]

is an infimum of affine functions. Thus \(q_j-f\) is convex on \(C_j\). For any point u expressed as a convex combination of the vertices \(z_k\) of \(C_j\),
\[
F(u)-f(u)\le\sum_k\alpha_k[F(z_k)-f(z_k)]
\le\sum_k\alpha_k[F(z_k)-\ell_{z_k}]\le\varepsilon.
\]

This is the crucial certificate: an unseen spectral mode cannot create a violation solely in the interior of a current cell while passing all of that cell's vertices.

### Proof of termination

Let z be a newly violating vertex, and let y be any earlier witness-addition point. The old envelope obeys
\(F(y)-f(y)\le\kappa\), because the witness acquired at y is still present. At z,
\(F(z)-f(z)>\varepsilon-\kappa\), since \(f(z)-\ell_z\le\kappa\). The function \(F-f\) is \((M+L)\)-Lipschitz. Therefore
\[
\|z-y\|>\frac{\varepsilon-2\kappa}{M+L}=:s.
\]

The witness-addition points are s-separated. Disjoint radius-s/2 balls around them lie inside a ball of radius R+s/2, proving the displayed packing bound. Each finite witness bank has finitely many cells and vertices, so finitely many experiments occur between additions.

### Proof of decision quality

For every u, \(f(u)-c^Tu\le F(u)-c^Tu\). If \(\widehat u\) maximizes the envelope objective,
\[
f(\widehat u)-c^T\widehat u
\ge F(\widehat u)-c^T\widehat u-\varepsilon
\ge\max_{u\in S}[f(u)-c^Tu]-\varepsilon.
\]

The claimed objective interval and margin test follow from the same sandwich.

The downstream computation is explicit, rather than an assumed planning oracle. Writing \(S=\{u:Cu\le h\}\), \(q_j(u)=b_j+a_j^Tu\), its LP dual is
\[
\min_{\lambda,\beta\ge0}\sum_j\lambda_jb_j+\beta^Th,
\qquad \sum_j\lambda_j=1,\quad C^T\beta=\sum_j\lambda_ja_j-c.
\]

A feasible primal design and feasible dual weights certify their gap using only the learned coefficients and the new task description. Rational LP algorithms have polynomial bit complexity; in numerical work, residuals and any dual-feasibility repair must be budgeted explicitly. The state dimension n does not enter this subsequent certificate check.


## Noise, confidence, and finite precision

The geometric theorem is deterministic conditional on correct spectral intervals. Fresh randomized spectral probes can make each interval correct conditionally on the entire previous transcript, with failure probability \(\delta_j\). Taking \(\sum_j\delta_j\le\delta\) gives one simultaneous \(1-\delta\) certificate, even with adaptive acquisition. It is essential to account for *all* vertex tests, not just witness additions.

A known total call bound follows from the packing bound and a crude fixed-dimension cell-vertex bound. With r planes and s domain inequalities, there are at most
\(r\binom{r-1+s}{d}\) cell vertices before duplicate removal. Rechecking from scratch after every addition is polynomial in N for fixed d, but can be very expensive. This is an honest computational restriction, not a dimension-free claim.

### A constructive, deliberately conservative noisy spectral oracle

This supplies a proof of availability without treating an exact low-dimensional solver as given. It is not the recommended practical eigenvalue implementation. In the next formulas n denotes the physical vector dimension and d the number of controls.

Assume \(\|H\|\le B\), request Rayleigh suboptimality \(\tau\le B\), and set \(h=\tau/8\). For a trial threshold \(\theta\in[-B,B]\), scale
\(t_\theta(x)=1/2+(\theta-x)/(4B)\in[0,1]\). For odd k use the binomial-majority polynomial
\[
p_{\theta,k}(x)=\Pr\{\operatorname{Binomial}(k,t_\theta(x))\ge(k+1)/2\}.
\]

Hoeffding's inequality gives, with \(\zeta=\exp[-k h^2/(8B^2)]\),
\[
p(x)\ge1-\zeta\ (x\le\theta-h),\qquad
p(x)\le\zeta\ (x\ge\theta+h),\qquad
0\le p(x)\le1\ (|x|\le B).
\]

Set \(a=1/(2\sqrt n)\), \(\zeta_*=\rho=a\sqrt{h/B}/16\), and choose the smallest odd
\[
k\ge (8B^2/h^2)\log(1/\zeta_*).
\]

Compute its degree-k Chebyshev coefficients on [-B,B], then apply the polynomial by the three-term recurrence using vector experiments. A bounded polynomial has Chebyshev coefficients of magnitude at most 2. Write \(\nu=\overline\eta/B\), where \(\overline\eta\) bounds the error of a *combined pencil* action, not one coefficient action. With exact digital recurrence arithmetic, if \(\nu k^2\le1/2\), the jth noisy Chebyshev vector differs from its true value by at most \(2\nu j^2\). Summing the coefficient-weighted errors gives at most \(4\nu k^3\). Thus
\[
\nu\le\rho/(8k^3)
\]

leaves at most rho/2 polynomial error for action noise and rho/2 for coefficient evaluation and digital arithmetic. Arbitrarily accurate coefficient computation is an ordinary polynomial-size digital calculation; k+1 Chebyshev nodes and a discrete cosine transform recover this degree-k polynomial. The recurrence accuracy bound can equally include its local arithmetic errors. No hidden representation is supplied.

For a random unit vector g and any fixed unit eigenvector w,
\(\Pr\{|w^*g|\ge a\}\ge3/16\), by Paley-Zygmund and the sphere's second and fourth moments (the same conservative constant works over the complex sphere). With
\[
r=\left\lceil\frac{\log(1/\delta_j)}{\log(16/13)}\right\rceil
\]

independent starts, at least one has this overlap with probability at least \(1-\delta_j\). For all thresholds simultaneously:

* If \(\lambda_{\min}H\le\theta-h\), at least one filtered vector has norm greater than a/2 on that overlap event.
* If \(\lambda_{\min}H\ge\theta+h\), every filtered vector has norm at most a/4.

Maintain an interval [l,u] initially [-B,B]. At midpoint theta, classify the test as high exactly when the maximum computed filtered-vector norm over the r starts is greater than a/2; classify it as low otherwise. Norm-evaluation error must be included in the stated numerical error budget, or enclosed explicitly before making this comparison. A high test permits \(u\leftarrow\min(u,\theta+h)\); a low test permits \(l\leftarrow\max(l,\theta-h)\). After \(T=\lceil\log_2(B/h)\rceil+1\) tests the interval has width at most 4h. For a final threshold \(\theta=u+h\), the minimum mode is in the pass band and all modes above \(\lambda_{\min}+6h\) are in the stop band. Choose the largest-norm filtered vector and normalize it. Its norm before normalization is at least \(a(1-\zeta_*)-\rho\), and its tail beyond \(\lambda_{\min}+6h\) has norm at most \(\zeta_*+\rho\). The tail's Rayleigh contribution is less than h/8, so the resulting Rayleigh quotient is below \(\lambda_{\min}+\tau\). If u+h>B, the lower bracket is already within 5h of B and any unit vector has Rayleigh error at most 5h; no out-of-range filter is needed.

#### Exact original action accounting

For one fixed pencil H(z), all threshold filters use the same \(T_j(H(z)/B)g_s\), for j=0,...,k and s=1,...,r. Store these vectors once; changing theta only changes scalar coefficients. Each Chebyshev step calls every needed coefficient operator exactly once, so the worst-case number of original coefficient-vector experiments for a spectral call is
\[
\boxed{(d+1)(rk+1).}
\]

The final +1 is the coefficient expectation measurement of the selected unit witness. No bisection factor is hidden in the physical action count. If working memory is restricted and the vectors are recomputed, a factor at most T+1 appears explicitly instead. The straightforward stored implementation uses \(O(nrk)\) working scalars, \(O(nrkT)\) vector arithmetic plus coefficient construction, and emits only d+1 witness coefficients and one lower bound. The entire acquisition uses at most \(J(d+1)(rk+1)\) original actions when J is a valid bound on *all* cell-vertex spectral calls and delta_j is chosen uniformly using J. Adaptive anytime confidence schedules can instead sum the individual costs.

The asymptotic conditions are
\[
k=O((B/\tau)^2\log(nB/\tau)),\qquad
\boxed{\overline\eta/B\le c\frac{\sqrt{\tau/B}}{\sqrt n\,k^3}}.
\]

Thus at fixed relative task resolution the action noise must fall essentially as \(n^{-1/2}\), up to logarithms. These conservative epsilon exponents are a proof device, not an attractive practical noise tolerance. Stable Lanczos and modern noisy power methods are the important ordinary comparators. At a larger arbitrary-query noise floor the acquisition must report that it cannot earn the requested interval; it cannot relabel an eigenpair residual as a global certificate.

### Simpler full-column fallback and its information cost

For each coefficient, query every coordinate vector once. Let Y_i contain the n noisy returned columns and set \(\widehat H_i=(Y_i+Y_i^*)/2\). Then
\[
\|\widehat H_i-H_i\|\le\sqrt n\,\eta_i,
\]

because the column-error matrix has Frobenius norm at most \(\sqrt n\eta_i\). This uses exactly n(d+1) original full-vector actions, O((d+1)n^2) output/storage, and ordinary finite-precision dense eigenvalue computations thereafter. It is a serious baseline, and for moderate n can beat repeated spectral acquisition in physical query count. It earns an operator-norm reconstruction at the required resolution when
\(\sqrt n(\eta_0+\sum R_i\eta_i)\ll\varepsilon\). The adaptive spectral bank is attractive when n is sufficiently large, matrix actions are cheap relative to reconstructing all columns, and many future tasks amortize acquisition; it is not automatically more experiment-efficient.

### Why the square-root dimension factor cannot simply be dropped

Consider H=0 versus \(H=-\alpha ww^*\), with w uniform on the unit sphere and fixed before the algorithm's random seed. Both obey \(\|H\|\le\alpha\). Under the second hypothesis an adversarial action error can return the same zero vector as the first whenever \(\alpha|w^*v|\le\eta\|v\|\). For an adaptive algorithm receiving the all-zero transcript, its normalized query vectors depend on its own random seed but not on w. Sphere concentration and a union bound imply
\[
\Pr\left\{\max_{j\le q}|w^*v_j|>\eta/\alpha\right\}
\le 2q\exp\left[-\frac{(n-2)\eta^2}{2\alpha^2}\right].
\]

Consequently, when
\[
q\le\tfrac18\exp[(n-2)\eta^2/(2\alpha^2)],
\]

the two transcript distributions can be coupled to coincide with probability at least 3/4. Their minimum eigenvalues differ by alpha. No estimator can uniformly identify that margin to error less than alpha/2 with failure probability below 3/8 under equal prior probabilities. The error rule is norm bounded and can simply stop cancelling when the inequality fails; it does not require changing the fixed operator. This is the relevant contrast with coherent calibration error \(H+E\): coherent error perturbs the entire spectrum by at most \(\|E\|\), whereas independently bounded query errors can conceal a rare direction.

Adding a known identity matrix to both hypotheses gives I versus I−αww*, so for α≤1/2 the same obstruction holds with condition number at most two. It is not an inverse singularity effect.

In particular, for polynomially many queries a uniform worst-case margin certificate generally needs \(\eta/\alpha\lesssim\sqrt{\log q/n}\). A compact decision envelope does not evade the experimental distinguishability limit.

## What is learned

The operational object is a finite list of d+1 scalar expectations per worst-case witness, plus validation points and lower bounds. Vectors in the physical n-dimensional state space can be discarded after their coefficient expectations are recorded. The representation is a task envelope, not a recovered environment. Algebraic dimension can be n^2 and every matrix can have generic perturbations; the certificate remains meaningful.

For pencils H and H' with
\(\sup_{u\in D}\|H(u)-H'(u)\|\le\rho\), Weyl's inequality gives
\(\sup_D|f-f'|\le\rho\). If the stored envelope LP has exact optimum V for a future task, the corresponding optimum for H' lies in \([V-\varepsilon-\rho,V+\rho]\). The design selected by that envelope has regret at most \(\varepsilon+2\rho\) for H'; add the separately certified LP gap if present. Value perturbation by rho and decision regret are distinct statements. The matrix algebra can change discontinuously while this operational object changes continuously.

This stability does not establish *a priori* small bank size. The explicit worst-case upper bound is exponential in d. An envelope that is almost polyhedral may require a small practical bank, but acquisition must actually certify that fact.

## A stronger decision-level indistinguishability statement

For optimal values, two pencils are epsilon-equivalent over every stated future task exactly when their minimum-eigenvalue functions differ by at most epsilon on D. Sufficiency follows because taking a maximum changes values by at most the uniform function difference. Necessity follows because the task family permits singleton polytopes S={u}; the reported optimum then is f(u), up to a known linear offset. A design optimized for one pencil has regret at most twice that function difference for the other; equivalence of values and transfer of decisions use different constants. Thus the quotient is tied to the entire stated decision class, rather than chosen from a convenient matrix norm.

If only large resource regions and a narrower menu of costs are permitted, this metric is stronger than necessary. Learning the weaker decision-specific metric, without making its verification computationally intractable, is an open improvement.

## Obstacles and useful failures

* Residual-only certification is false: a perfectly converged eigenpair can miss a lower unseen eigenvalue.
* Learning the envelope from an arbitrary finite sample without a cell-vertex certificate is false: a new affine spectral mode can change a region between samples.
* The full-vector noise floor can hide a rank-one direction whose overlap with all test vectors is tiny. No amount of geometric certification repairs an unearned eigenvalue oracle.
* The dimension-free dream is false for broad task families: a nearly spherical joint numerical range needs many supporting witnesses at fine resolution. Curvature, not algebra dimension, controls that cost.
* New nonlinear constraints or time-dependent switching policies do not automatically reduce to LPs. This proof buys exactly the listed future tasks.
* The algorithm is a uniform, reusable version of established spectral cutting-plane ideas. The closest geometric comparators are the Sandwich algorithms of Rote and the Sandwich/Benson-type methods for convex multiobjective approximation; their vertex-based inner/outer certificates are closely related. The claimed contribution here is only the explicit experimental-noise/decision-compilation synthesis and its stated guarantees, not historical priority for the geometric algorithm.

## Primary sources and positioning

1. J. E. Kelley, “The Cutting-Plane Method for Solving Convex Programs,” 1960, DOI 10.1137/0108053. https://epubs.siam.org/doi/10.1137/0108053 . The basic cutting-plane idea is old.
2. C. Helmberg and F. Rendl, “A Spectral Bundle Method for Semidefinite Programming,” SIAM J. Optimization 10(3), 2000, DOI 10.1137/S1052623497328987. https://epubs.siam.org/doi/10.1137/S1052623497328987 . An important stronger ordinary solver for a single spectral optimization problem; its model is semidefinite rather than the simple polyhedral bank here.
3. S. Boyd and L. El Ghaoui, “Method of centers for minimizing generalized eigenvalues,” Linear Algebra and its Applications 188–189, 1993. https://www.web.stanford.edu/~boyd/papers/gevc.html . Establishes the consequential control-design setting and convex/quasiconvex optimization context.
4. J. Kuczynski and H. Wozniakowski, “Estimating the Largest Eigenvalue by the Power and Lanczos Algorithms with a Random Start,” SIAM J. Matrix Analysis and Applications 13(4), 1992, DOI 10.1137/0613066. https://doi.org/10.1137/0613066 . Random starts give global extremal-eigenvalue guarantees; deterministic Krylov starts can miss eigenmodes.
5. C. Musco, C. Musco, and A. Sidford, “Stability of the Lanczos Method for Matrix Function Approximation,” SODA 2018. https://groups.csail.mit.edu/tds/papers/Musco/SODA18.pdf . Finite precision must be handled explicitly; their matrix-action accuracy model includes approximate products beyond rounding.
6. M. Hardt and E. Price, “The Noisy Power Method: A Meta Algorithm with Applications,” NeurIPS 2014. https://www.mit.edu/~ecprice/papers/npm.pdf . A stronger practical/theoretical noisy-eigenvector baseline.
7. M.-F. Balcan, S. S. Du, Y. Wang, A. W. Yu, “An Improved Gap-Dependency Analysis of the Noisy Power Method,” COLT 2016. https://proceedings.mlr.press/v49/balcan16a.html . Improved gap and noise dependencies, including gap-independent approximation results.
8. S. Har-Peled and M. Jones, “A Proof of Dudley's Convex Approximation,” 2019. https://sarielhp.org/p/17/dudley_approx/ . Convex-body approximation provides stronger geometric existence bounds and a necessary comparator; it does not by itself give the present noisy experimental certificate.

9. G. Rote, “The convergence rate of the Sandwich algorithm for approximating convex functions,” Computing 48, 337–361, 1992. https://page.mi.fu-berlin.de/rote/Papers/abstract/The%2Bconvergence%2Brate%2Bof%2Bthe%2BSandwich%2Balgorithm%2Bfor%2Bapproximating%2Bconvex%2Bfunctions.html . A direct comparator: supporting tangents and connecting chords certify uniform approximation, with optimal O(1/n^2) convergence in one dimension.
10. I. Lammel and K.-H. Küfer, “The convergence rate of the Sandwiching algorithm for convex bounded multiobjective optimization,” primary preprint, December 18, 2023. https://optimization-online.org/wp-content/uploads/2023/12/convergence_rate_sandwiching_preprint.pdf . A direct modern comparator for polyhedral inner/outer approximation and error certificates, also called Benson-type algorithms. These methods apply related ideas to convex functions and sets.

11. C. W. Royer, M. O’Neill, and S. J. Wright, “A Newton-CG Algorithm with Complexity Guarantees for Smooth Unconstrained Optimization,” primary manuscript, 2018/2019. https://optimization-online.org/wp-content/uploads/2018/03/6513.pdf . Lemma 2 gives the explicit randomized Lanczos minimum-eigenvalue step count used by the numerical prototype.
