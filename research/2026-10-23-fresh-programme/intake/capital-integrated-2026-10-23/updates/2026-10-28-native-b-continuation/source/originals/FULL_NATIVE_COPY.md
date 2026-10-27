I obtained a **positive, value-only fourth-order correction for every source in the original class**, with a complete query bound and a reusable conditional interface. The general polylogarithmic Gaussian-mean target remains open.

The main advance is the implemented correction and its full-law proof. I also pursued its two most plausible routes to recursion. Deterministic covariance-time quadrature removes a genuine shared-random-time defect. Replacing global source regularity with ordinary integrated Sobolev regularity fails, with explicit counterexamples. A more promising operation survives: **the acquired correction defines a stable joint law kernel that can retain its Gaussian input and Brownian anchors**.

The complete construction, proof, accounting, and precise remaining obligation are in ACQUIRED_COVARIANCE_AND_FOURTH_ORDER_SAMPLER.txt[ACQUIRED_COVARIANCE_AND_FOURTH_ORDER_SAMPLER.txt](sandbox:/workspace/scratch/23206e14a217/research/covariance_compiler/ACQUIRED_COVARIANCE_AND_FOURTH_ORDER_SAMPLER.txt).

## 1. The general construction

Let
\[
g=\nabla F:\mathbb R^d\to\mathbb R^d,\qquad F\in C^{1,1},
\]
with a supplied global Lipschitz bound \(L\). Convexity is unnecessary. Write
\[
\mu=\mathbb E g(G),\qquad C=\operatorname{Cov}(g(G)).
\]
These are analysis quantities; the algorithm receives neither.

I used the packet’s existing Clark–Ocone representation and two-value heat-Hessian action. Their composition supplies the covariance operation needed below. The added result is a positive program that uses this operation, together with a proof controlling its actual output law.

### A covariance action acquired with four values

The existing S4 action is
\[
J_s(c;v)
=
\|v\|\,
\frac{g(c+sZ_\perp+Ru)-g(c+sZ_\perp-Ru)}{2R},
\]
where \(u=v/\|v\|\), \(Z_\perp=(I-uu^\top)Z_0\), and \(R=s\chi_3\). It satisfies
\[
\mathbb E[J_s(c;v)\mid c,v]=H_s(c)v,
\qquad
\|J_s(c;v)\|\le L\|v\|,
\]
with \(H_s(c)=\mathbb E Dg(c+sG)\). No derivative is evaluated.

Draw \(T\sim U(0,1)\), \(W\sim N(0,I_d)\), and set
\[
c=\sqrt T\,W,\qquad s=\sqrt{1-T}.
\]
Apply two fresh actions at this **same** center and scale:
\[
\mathcal A_g(v)=J_s\!\left(c;J_s(c;v)\right).
\]

The Brownian covariance identity gives
\[
C=\int_0^1
\mathbb E\!\left[H_{\sqrt{1-t}}(\sqrt t\,W)^2\right]dt.
\]
Conservativity supplies the symmetry needed for the square. Consequently,
\[
\boxed{
\mathbb E[\mathcal A_g(v)\mid v]=Cv,
\qquad
\|\mathcal A_g(v)\|\le L^2\|v\|.
}
\]

This operation uses **at most four original whole-vector values**, with \(O(d)\) surrounding arithmetic and storage.

For a fresh Gaussian input \(Z\), averaging \(M\) independent actions conditional on that same \(Z\) gives
\[
\mathbb E\|\overline{\mathcal A}_M(Z)-CZ\|^2
\le \frac{L^4d}{M}.
\]

The dimension factor matters. The ordinary unbiased sample-covariance action
\[
\frac12\bigl(g(G)-g(G')\bigr)
\bigl(g(G)-g(G')\bigr)^\top Z
\]
has squared norm expectation \(L^4d(d+2)\) already for \(g(x)=Lx\). The acquired secant action has the operator-scale bound \(L^4d\). This improvement uses the source’s conservative geometry.

### A mean-preserving source with zero third tensor

Choose an integer \(m\ge2\), put \(n=m^3\), and use the exact rational coefficients
\[
a=\frac1{m^3-m},\qquad
b=-\frac1{m^2-1},\qquad
\kappa=\frac1{(m-1)^2(m+1)}.
\]
Generate
\[
U=a\sum_{i=1}^{n}g(G_i)+b\,g(G_{n+1}).
\]

The identities
\[
na+b=1,\qquad na^3+b^3=0,\qquad na^2+b^2=\kappa
\]
hold exactly. Therefore
\[
\mathbb EU=\mu,\qquad
\operatorname{Cov}(U)=\kappa C,\qquad
\mathbb E(U-\mu)^{\otimes3}=0.
\]
As a function of its Gaussian inputs, \(U\) is \(L\sqrt\kappa\)-Lipschitz.

Nothing is fitted. In particular, the third tensor is canceled algebraically without estimating the mean or any moment tensor. Negative vector coefficients do not create a signed probability law: \(U\) is an ordinary sampled random vector.

### The actual output

Allocate the Gaussian noise budget as
\[
\tau^2=\nu^2=\frac{\sigma^2}{2}.
\]
With all source replicas independent of the action seeds and the final Gaussian reserve, return
\[
\boxed{
O
=
U+\tau Z
-\frac{\kappa}{2\tau}\overline{\mathcal A}_M(Z)
+\nu W_0.
}
\]

Its mean is exactly \(\mu\). Its complete original-query cap is
\[
\boxed{Q=n+1+4M}
\]
on every execution.

For \(m=2\), the source sum uses eight coefficients \(1/6\) and one coefficient \(-1/3\). One covariance action then gives a 13-query correction. Larger parameters supply the accuracy guarantee.

## 2. The full-law theorem

Let \(\rho=L/\sigma\). If
\[
\kappa\rho^2\le\frac12,
\]
the implemented output satisfies
\[
\boxed{
\operatorname{TV}\!\left(\mathcal L(O),N(\mu,\sigma^2I_d)\right)
\le
\kappa^2\rho^4
\left[
\left(\sqrt6+\frac1{2\sqrt2}\right)\sqrt d
+\phi(1)\frac dM
\right],
}
\]
where
\[
\phi(1)=\frac{e^{-1/2}}{\sqrt{2\pi}}.
\]

The term \(d/M\) charges the randomness of the **actual acquired covariance action**. Replacing that action by its conditional expectation inside the output law would incorrectly remove this term.

The proof has three parts.

### The ideal fourth-order comparison

For any centered \(B\)-Lipschitz Gaussian image \(V\), with covariance \(K\) and zero full third tensor,
\[
\operatorname{TV}\!\left(
V+N(0,S^2I-K),\,N(0,S^2I)
\right)
\le
\frac{\sqrt{24}\,B^4\sqrt d}
{8(S^2-\|K\|_{\mathrm{op}})^2}.
\]

This permits singular \(K\) and source laws without densities.

The proof constructs a weak fourth-order Stein witness. Starting from the Gaussian-source Stein kernel, two Poincaré–Riesz steps give a symmetric tensor \(T_3\) such that
\[
\mathbb E\!\left[V\cdot\nabla f-K:D^2f\right]
=
\mathbb E[T_3:D^4f],
\qquad
\|T_3\|_{L^2,\mathrm{HS}}\le B^4\sqrt d.
\]
The zero third tensor is what permits the second step.

Interpolating between the Gaussian target and the covariance-completed source, then contracting against the fourth Gaussian Hermite tensor, controls every bounded measurable test. This establishes TV; finite moment matching is only one ingredient.

Higher-order Stein kernels and their construction from functional inequalities have established primary precedents in Fathi and Courtade–Fathi–Pananjady. The saved proof supplies the particular weak, anisotropic form used here, without making its analysis witnesses runtime oracles. [arxiv.org](https://arxiv.org/abs/1812.02703?utm_source=chatgpt.com)

### The acquired action’s randomization error

Replace \(\overline{\mathcal A}_M(Z)\) by \(CZ\) only in an analysis comparison.

Its error is centered conditional on \(U,Z\). Expanding the density of the independent \(\nu W_0\) reserve makes the first-order term vanish and bounds the complete remainder by
\[
\frac{\phi(1)\kappa^2L^4d}
{4\tau^2\nu^2M}.
\]

This step charges action variance through a full density estimate.

### The remaining deterministic covariance error

The comparison using \(CZ\) has Gaussian noise covariance
\[
Q_1=\sigma^2I-\kappa C+\frac{\kappa^2C^2}{4\tau^2}.
\]
The ideal covariance-completed comparison uses
\[
Q_0=\sigma^2I-\kappa C.
\]
A Gaussian KL/Pinsker bound controls their difference. Combining it with the previous two bounds gives the displayed theorem.

The residual is genuinely fourth order. For an affine scalar field, the implemented output is Gaussian with an explicit positive fourth-order variance excess. That verifies the correction’s limitation; affine sources themselves are easy because \(g(0)\) reveals their mean.

## 3. Complete query and arithmetic accounting

The following deterministic parameter rule suffices. Define
\[
A=\frac{128}{9}\phi(1)\rho^4\frac d\varepsilon,
\qquad
D=\frac{128}{9}
\left(\sqrt6+\frac1{2\sqrt2}\right)
\rho^4\frac{\sqrt d}{\varepsilon}.
\]
Choose the least integer \(m\ge2\) such that \(n=m^3\) obeys
\[
n\ge\frac{16}{3}\rho^2,\qquad n^2\ge D,\qquad n^3\ge8A,
\]
and set
\[
M=\max\{1,\lceil A/n^2\rceil\}.
\]
Then the TV bound is at most \(\varepsilon\), with
\[
\boxed{
Q=
O\!\left(
1+\rho^2+
\rho^{4/3}(d/\varepsilon)^{1/3}
+\rho^2d^{1/4}\varepsilon^{-1/2}
\right).
}
\]

The integer selection uses doubling and binary search; it does not assume an exact cube-root primitive. The source coefficients are rational.

The original-source implementation uses
\[
O(d(n+M)+\log(n+1))
\]
surrounding arithmetic and \(O(d)\) storage. Reading the vector answers is included. A literal implementation needs at most
\[
d(n+3+3M)+9M
\]
independent scalar Gaussian draws.

There is no source-dependent fitting phase. Heat smoothing is performed by the actual queried points. Both final Gaussian terms are charged to the fixed \(\sigma^2\) budget.

These bounds use the packet’s exact-real secant model. The numerical implementation is not a finite-bit TV theorem. Primitive-error budgets and comparison with a commonly rounded target remain necessary for that separate theorem.

## 4. What can already be reused

The covariance construction extends to an explicit conditional Gaussian value circuit
\[
H_x(W)
=
\sum_{i=1}^{q}
c_i\,g\!\left(b_i(x)+\sum_{\ell=1}^{r}\beta_{i\ell}W_\ell\right),
\]
where \(x\) is available state, the coefficients and centers come from the explicit program, and the Gaussian blocks are fresh.

I constructed both forward and transpose actions for its rectangular Clark matrix using original \(g\)-values. Their fresh composition acquires
\[
\operatorname{Cov}(H_x(W))z
\]
with **four original values per action**.

The relevant bound is
\[
B_{\mathrm{word}}
=
L\sum_i|c_i|\|\beta_i\|.
\]
A sharper source Lipschitz bound \(B_0\), when proved from the circuit, controls the ideal-law terms. \(B_{\mathrm{word}}\) controls action randomization. Without a sharper certificate, use \(B_0=B_{\mathrm{word}}\).

The conditional sampler costs
\[
q(n+1)+4M
\]
original values. Its direct arithmetic, coefficient storage, and center preparation are explicitly accounted for in the proof.

Because the theorem holds conditionally on available \(x\), it gives a joint guarantee with \(x\) retained. An adaptive outer program can reuse the actual outputs, charging conditional errors through a hybrid argument. This does not call a posterior or a current-law mean oracle.

The restriction is explicit: the circuit has scalar Gaussian blocks \(\beta_{i\ell}I_d\). The nonlinear, value-dependent query directions generated by the correction do not automatically remain in that circuit class.

### A further joint-law operation survives the regularity failures

For a fixed-center two-action word \(A_{c,s}\), common fresh seeds give
\[
\mathbb E\|A_{c,s}(v)-A_{c,s}(w)\|^2
\le144L^4\|v-w\|^2.
\]
Thus input errors propagate in mean square with a constant independent of dimension.

There is also a center-stability theorem for the **joint** kernel
\[
K_c=\mathcal L\bigl(V,\tau V+\alpha A_{c,s}(V)+\nu N\bigr).
\]
Writing \(c_1=\sqrt{2/\pi}\),
\[
\operatorname{TV}(K_c,K_{c'})
\le
\frac{
2c_1+(1+\sqrt{12})c_1^3|\alpha|L^2/\nu
}{2s}\,
\|c-c'\|.
\]

This follows by integrating perpendicular seed derivatives by parts; only the parallel pieces require direct derivative bounds. It controls arbitrary joint tests of the retained \(V\) and output.

For translated sources \(g(x+G)\), the Brownian anchors \((T,W)\) can also be retained. Since
\[
\mathbb E(1-T)^{-1/2}=2,
\]
the corresponding center-to-joint-law bound remains dimension independent after averaging over time.

The internal secant seeds and query endpoints are excluded from the retained state in this theorem. Exposing them to later tests would invalidate this particular integration-by-parts argument. The result is stability of implemented kernels, not conditional Gaussianity given their anchors.

## 5. A failed mechanism led to acquired deterministic time quadrature

One shared random time can produce a dimension-coherent fluctuation in the output law. I proved this for the implemented four-value action.

Take \(g_i(x)=\sin x_i\), use the actual rational replica weights, and choose dimensions along which \(\kappa=d^{-1/2}\). The expected covariance integrand is
\[
F(t)=e^{-1}\cosh(t)I_d.
\]
Its nonzero time variance
\[
v=\operatorname{Var}_{T\sim U(0,1)}(e^{-1}\cosh T)
\]
forces, for every fixed number \(M\) of shared-time actions,
\[
\liminf_{d\to\infty}
\operatorname{TV}\!\left(\mathcal L(O),N(0,I_d)\right)
\ge \frac{v^2}{640M^2}>0.
\]

This is a bounded-test law argument, obtained from an energy statistic and uniform fourth-moment tail control. It demonstrates why the action-randomization term cannot simply be discarded.

I then replaced time sampling with a constructed positive quadrature rule.

The Gaussian chaos decomposition gives
\[
F(t)=\sum_{j\ge1}A_jt^{j-1},
\qquad
A_j\succeq0,\qquad
\sum_jA_j\preceq L^2I.
\]
Consequently,
\[
0\preceq F^{(k)}(t)\preceq L^2k!(1-t)^{-k}I.
\]
This regularity belongs to the **expected matrix integrand**; it makes no analyticity claim about individual Brownian paths.

Using \(m\)-point Gauss–Legendre rules on \(J\) dyadic intervals, and certified rational node and weight approximations of tolerance \(\zeta\), gives
\[
\|C-\widetilde C_Q\|_{\mathrm{op}}\le L^2\xi,
\]
where
\[
\xi=2^{-J}+(2m+1)16^{-m}+2\zeta.
\]

The coefficients are actually acquired by code using rational Legendre recurrences, ranked-root bisection, and interval weight certificates. General Gauss roots are not assumed to be free primitives. Precomputation has a deterministic polynomial arithmetic and bit bound.

If \(S_2=\sum_iw_i^2\) is the exactly computed squared-weight sum, the complete sampler satisfies
\[
\operatorname{TV}
\le
\kappa^2\rho^4
\left[
\left(\sqrt6+\frac1{2\sqrt2}\right)\sqrt d
+\phi(1)dS_2
\right]
+
\frac{\kappa\rho^2\xi\sqrt d}{\sqrt{2\pi}}.
\]
Its source-query cap is \(n+1+4Jm\).

This removes the identified shared-time component and charges the remaining within-time action variance. Independent random-time averaging with a growing number of actions also removes the counterexample’s gap and can have a better worst-case variance per query. The quadrature result therefore establishes a controlled representation change, not a universal speedup.

## 6. The attempted Sobolev repair fails decisively

I pursued integrated regularity because global seed-Lipschitz regularity had failed. Squared first derivatives are integrable, and the dimension-free input-stability estimate above survives. The full source derivative norm has the wrong dimension scale.

For the smooth conservative sources
\[
g_k(x)_i=\frac{\sin(kx_i)}k,
\qquad \operatorname{Lip}(g_k)=1,
\]
the actual two-value action satisfies
\[
\lim_{k\to\infty}
\mathbb E|\partial_{c_i}J_i|^2
=\frac d{4s^2},
\]
and
\[
\lim_{k\to\infty}
\mathbb E\|D_{Z_\perp}J\|_{\mathrm{HS}}^2
=\frac{d(d-1)}4.
\]

Adding an affine background,
\[
g_k(x)=\lambda x+
\eta\bigl(\sin(kx_i)/k\bigr)_i,
\]
passes this obstruction through the second action:
\[
\liminf_{k\to\infty}
\mathbb E\|D_{Z_{\mathrm{inner}}}A\|_{\mathrm{HS}}^2
\ge
\frac{\lambda^2\eta^2}{4}d(d-1).
\]

Positive averaging of \(K\) independent words retains a factor \(\sum_iw_i^2\). Restoring an \(O(d)\) Gaussian Dirichlet bound **at the action’s own natural scale** requires \(K=\Omega(d)\). Thus ordinary normalized Gaussian source energy does not provide cheap recursive closure for this representation.

There is a sharper scalar failure. Let
\[
g(x)=\lambda x+\eta|x|,
\qquad \lambda>\eta>0,\quad \lambda+\eta\le1.
\]
This is the gradient of a \(C^{1,1}\) potential. With \(c=\sqrt t\,W\), \(R=s\chi_3\),
\[
J=V\left[\lambda+\eta\,\operatorname{clip}(c/R,-1,1)\right],
\]
so
\[
\partial_WJ=
\eta\sqrt t\,\frac VR\,\mathbf1_{\{|c|<R\}}.
\]
Its **fourth moment of the first seed derivative** is infinite:
\[
\mathbb E|\partial_WJ|^4=\infty.
\]
The center probability contributes \(R\), the radius density contributes \(R^2\), and the fourth power contributes \(R^{-4}\), leaving \(\int_0 dR/R\). The two-action word retains the divergence. Smooth approximations show that no uniform fourth-moment bound exists even over smooth sources.

These are failures of specified sampled representations and norms. They are not lower bounds for the Gaussian-mean target, and they do not rule out an intrinsic Poincaré inequality for the output law. Indeed, the dimension-free smoothed joint-kernel bounds demonstrate why a law-level approach can remain useful despite bad seed derivatives.

## 7. Evidence and comparison

The checks exercise the acquired operations, their general conditional interface, and their complete query caps:

- Exact rational mean, third-tensor, and variance identities passed for 19 integer cubes.
- Four-query covariance actions passed 120 unknown symmetric-affine checks, with maximum numerical residual \(2.71\times10^{-14}\).
- Nonlinear rotated-gradient and conditional-circuit covariance checks each used 20,000 diagnostic samples; the sampler received only the value callable.
- All 120 original sampler executions and 36 quadrature sampler executions respected their complete query caps.
- Rational quadrature passed certified root, positivity, total-weight, precision-cap, and replication-allocation checks.
- The integrated-regularity formulas agreed with independent circle quadrature to \(6.07\times10^{-16}\).

The TV certificates are the proofs above. The numerical checks do not infer a full law from finitely many moments.

For \(\rho=1\), conservative parameter choices give the following **analytic query-budget comparisons**, not runtime benchmarks:

| Dimension | Requested TV | New query cap | Proved new TV bound | Supplied S5 averaging cap |
|---:|---:|---:|---:|---:|
| \(1\) | \(0.1\) | 32 | 0.01190 | 4 |
| \(1{,}024\) | \(0.1\) | 138 | 0.01870 | 115 |
| \(1{,}024\) | \(0.01\) | 521 | 0.00110 | 1,132 |
| \(10^6\) | \(0.01\) | 2,486 | 0.00152 | 35,359 |

Averaging is not the strongest comparison in every regime.

**Stochastic FORS is equally informed here.** One original value gives the unbiased target-gradient estimate
\[
\frac{y-g(G)}{\sigma^2}.
\]
Its norm-tail scale is \(O(L\sqrt d/\sigma^2)\). The published bound therefore specializes to roughly
\[
\widetilde O\!\left((\sqrt d+\rho^2d)\operatorname{polylog}(1/\varepsilon)\right).
\]
One additional value \(g(0)\) supplies initialization:
\[
\log\!\left(1+\chi^2(N(g(0),\sigma^2I)\|N(\mu,\sigma^2I))\right)
\le \rho^2d.
\]
The FORS exponential call-count tails permit deterministic truncation with an allocated TV loss. Its accuracy dependence is stronger than this construction’s. [arxiv.org](https://arxiv.org/html/2602.14342v2?utm_source=chatgpt.com)

The supplied **S1 arbitrary-fixed-exponent candidate** also remains a stronger dimension-asymptotic comparator under its stated audit status. This result does not supersede it.

The published Gaussian-cloud \(d^{1/5}\) theorem uses exact target-potential gradient queries. For this Gaussian target, such a query would expose \(\mu\); its headline bound is therefore not directly an equally informed original-\(g\)-value theorem. [arxiv.org](https://arxiv.org/html/2609.38710v1?utm_source=chatgpt.com)

I am making no historical-priority claim or practical-performance claim. The preserved advance is the explicit positive correction, its full-law accounting, and the acquired conditional and joint-kernel operations.

## 8. The exact remaining scientific obligation

The next obligation can be stated more sharply than “find a regular representation.”

For an actual represented output \(X\), mean \(\mu\), and declared Gaussian variance \(a^2\), suppose an analysis witness \(D\) satisfies
\[
\mathbb E[(X-\mu)\cdot\nabla f-a^2\Delta f]
=
\mathbb E[D:D^2f].
\]
Define a proved normalized defect bound
\[
e\ge \frac{\|D\|_{L^2,\mathrm{HS}}}{a^2\sqrt d}.
\]
An independent final reserve gives
\[
\operatorname{TV}\!\left(
X+\nu G,\,
N(\mu,(a^2+\nu^2)I)
\right)
\le
\frac{\|D\|_{L^2,\mathrm{HS}}}{2\sqrt2\,\nu^2}.
\]
Thus a fixed relative reserve converts this defect into \(O(\sqrt d\,e)\) full-law error.

The missing construction is a **positive value-only update on an explicit represented class** that contains the original initialization, returns another member of that class, and proves
\[
e_{\mathrm{new}}\le C e^2
\]
uniformly in dimension and source.

Every conditional operation used by that update must be acquired from original values. The Stein witness may remain an analysis object; its existence cannot be promoted into a runtime oracle.

Such a contraction would need only \(O(\log\log(d/\varepsilon))\) depth. To obtain the requested query bound, however, source-query growth must be a fixed factor per depth or obey an actually proved subcritical-forest bound. Multiplying a generic polylogarithmic cost at every depth is insufficient. Gaussian reserves must also fit the fixed final noise budget.

The present construction does not establish that self-map. It supplies concrete operations for pursuing a law-kernel representation, while the counterexamples rule out two specific source-regularity routes. That is the remaining bridge.

### Preserved proof, code, and data files

The earlier constructions and obstructions remain in place. The new ordinary files include:

- check_covariance_compiler.py[check_covariance_compiler.py](sandbox:/workspace/scratch/23206e14a217/research/covariance_compiler/check_covariance_compiler.py), CHECK_RESULTS.txt[CHECK_RESULTS.txt](sandbox:/workspace/scratch/23206e14a217/research/covariance_compiler/CHECK_RESULTS.txt), and QUERY_COMPARISON.csv[QUERY_COMPARISON.csv](sandbox:/workspace/scratch/23206e14a217/research/covariance_compiler/QUERY_COMPARISON.csv)
- ACQUIRED_TIME_QUADRATURE_ALGORITHM.txt[ACQUIRED_TIME_QUADRATURE_ALGORITHM.txt](sandbox:/workspace/scratch/23206e14a217/research/covariance_compiler/ACQUIRED_TIME_QUADRATURE_ALGORITHM.txt) and acquire_time_quadrature.py[acquire_time_quadrature.py](sandbox:/workspace/scratch/23206e14a217/research/covariance_compiler/acquire_time_quadrature.py)
- :chatgpt-content-reference{index="10"}[SHARED_TIME_COVARIANCE_OBSTRUCTION.txt](sandbox:/workspace/scratch/23206e14a217/research/source_replica/SHARED_TIME_COVARIANCE_OBSTRUCTION.txt)
- :chatgpt-content-reference{index="11"}[INTEGRATED_ACTION_REGULARITY.txt](sandbox:/workspace/scratch/23206e14a217/research/source_replica/INTEGRATED_ACTION_REGULARITY.txt)
- :chatgpt-content-reference{index="12"}[SOBOLEV_CLOSURE_OBSTRUCTIONS.txt](sandbox:/workspace/scratch/23206e14a217/research/source_replica/SOBOLEV_CLOSURE_OBSTRUCTIONS.txt)

Automatic approval review rejected the optional Library upload because it could not establish authorization for that destination. No upload occurred; the ordinary local files above are preserved and available. Retrying that optional copy would require approval.