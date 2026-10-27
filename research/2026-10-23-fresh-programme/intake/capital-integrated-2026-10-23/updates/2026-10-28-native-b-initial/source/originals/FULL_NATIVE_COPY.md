## Outcome

I obtained a **positive Gaussian-filling construction using at most three original field-value queries**, with exact preservation of the source conditional mean and a proved full-law total-variation bound. I also proved that the packet’s unrestricted pointwise Newton interface has an unbounded inverse—and, for some bounded smooth forcings arising from legal source perturbations, **no \(L^2\) solution at all**.

These results change the next scientific decision. The general polylogarithmic Gaussian-mean target remains open, but the unrestricted pointwise inverse should no longer be treated as a plausible missing lemma. A viable construction needs to control what reaches the output law, while retaining enough of the source coupling to support further corrections.

The independent attack on the predictive-process interface produced a second result: an exact full-law confidence geometry for a rank-two CP family, together with a matching-order information lower bound. It separates coordinate-conditioning losses from a real acquisition cost.

The complete main derivation is in POINTWISE_NEWTON_OBSTRUCTION.txt[POINTWISE_NEWTON_OBSTRUCTION.txt](sandbox:/workspace/scratch/23206e14a217/research/gaussian_mean/POINTWISE_NEWTON_OBSTRUCTION.txt), with executable implementation and checks in check_and_sample.py[check_and_sample.py](sandbox:/workspace/scratch/23206e14a217/research/gaussian_mean/check_and_sample.py). The supplied sources are unchanged.

## 1. Working backward from the consequential capability

The main target is a sampler for
\[
\mathcal N\!\left(\mathbb E g(G),\sigma^2I_d\right),
\qquad G\sim\mathcal N(0,I_d),
\]
using a deterministic bound of \(\operatorname{poly}(\log d,\log(1/\varepsilon))\) whole-vector evaluations of a globally Lipschitz conservative field \(g\), with polynomial surrounding arithmetic.

The packet already contains substantial machinery: finite secant actions, source-preserving rotations, formal Newton identities, and strong averaging comparators. Re-deriving an expectation identity would not address the remaining capability.

The essential missing step is an **acquired correction of the actual output law** that can be reused. Such a correction must jointly satisfy four demands:

- It must be a positive sampling program using the permitted values.
- Its error guarantee must concern the whole law.
- Its source correlations must remain available for subsequent corrections.
- Its complete query tree must satisfy the required bound on every execution.

I therefore attacked the pointwise Newton inverse in S3 at the simplest nontrivial Gaussian reference. That exposed a structural obstruction. I then constructed a correction that cancels the first-order discrepancy visible at the output, using paired source-dependent replicas and actual field values.

## 2. The acquired construction: three-query approximate Gaussian filling

### Declared source contract

This theorem uses an additional near-affine assumption:
\[
g(x)=\lambda x+h(x),\qquad 0<\lambda<1,
\]
where \(\lambda\) is known and \(h\) is globally \(\delta\)-Lipschitz. The algorithm evaluates \(g\); it does not require a separate \(h\) oracle.

Write
\[
a=\sqrt{1-\lambda^2},\qquad
\mu=\mathbb E g(G)=\mathbb E h(G).
\]
The mean \(\mu\) appears only in the theorem, never in the program.

Choose a finite cap \(N\ge0\) and a Gaussian reserve \(\tau>0\). The theorem is normalized so that the affine reference has covariance \(I_d\); its target covariance is \((1+\tau^2)I_d\). For the original fixed-\(\sigma\) problem, this reserve must fit inside the target variance budget.

### Executed algorithm

Draw independent standard Gaussian vectors \(G,Z,Z',V\), and form
\[
X=\lambda G+aZ,\qquad X'=\lambda G+aZ'.
\]

Choose an index with probabilities
\[
\Pr(J=j)=p_j=a^2\lambda^{2j},\quad 0\le j<N,
\qquad
\Pr(J=\mathrm{tail})=\lambda^{2N}.
\]

On the tail branch, set \(C=0\). On an active branch \(j\), draw one fresh standard Gaussian vector \(U\), and set
\[
r_j=\lambda^{2j+1},
\]
\[
A_j=r_jX+\sqrt{1-r_j^2}\,U,\qquad
B_j=r_jX'+\sqrt{1-r_j^2}\,U,
\]
\[
C=-\frac{g(A_j)-g(B_j)-\lambda(A_j-B_j)}{p_j}.
\]

Return
\[
\boxed{O=g(G)+aZ+C+\tau V.}
\]

This is an ordinary random vector. Its implementation uses no signed probabilities, derivative values, conditional sampler, or supplied mean.

### Exact conditional-mean preservation

The construction satisfies
\[
\boxed{\mathbb E[O\mid G]=g(G).}
\]

Conditional on \(G,J,U\), exchanging \(Z\) and \(Z'\) exchanges \(A_j\) and \(B_j\), reversing the correction’s sign. Consequently \(\mathbb E[C\mid G]=0\).

This property matters for reuse. It retains the original field as the conditional mean of the output, rather than merely producing an approximately correct marginal mean.

### Full-law theorem

Let
\[
\phi(1)=\frac{e^{-1/2}}{\sqrt{2\pi}}.
\]
For the actual program above,
\[
\boxed{
\begin{aligned}
d_{\mathrm{TV}}\!\left(
\mathcal L(O),
\mathcal N(\mu,(1+\tau^2)I_d)
\right)
\le {}&
\frac{\delta\sqrt d\,\lambda^{2N+1}}
     {\tau\sqrt{2\pi}}
\\
&+\frac{\phi(1)\delta^2d}{\tau^2}
\left[
1+\frac{2\lambda^2(1-\lambda^{2N})}{1-\lambda^2}
\right].
\end{aligned}}
\]

The first term is the explicit finite-cap error. The second is the full-law nonlinear remainder, including the randomness and correlations of the implemented correction.

### Why the proof works

Let \(P_r\) denote the Gaussian Ornstein–Uhlenbeck operator with correlation parameter \(r\). Since \(X,X'\) have correlation \(\lambda^2\),
\[
\mathbb E[h(G)\mid X]=P_\lambda h(X).
\]

For an active index,
\[
\mathbb E[h(A_j)-h(B_j)\mid X]
=
P_{r_j}h(X)-P_{\lambda^2r_j}h(X).
\]
The factor \(p_j\) cancels against the index probability. Summing the finite differences telescopes:
\[
\boxed{
\mathbb E[h(G)+C\mid X]
=
P_{\lambda^{2N+1}}h(X).
}
\]

This is an analysis identity for the executed program; the algorithm does not query that conditional expectation.

The shared \(U\) also gives the uniform pathwise bound
\[
\|C\|
\le
\frac{\delta\lambda}{a^2}\|X-X'\|.
\]
Combining this with conditional centering and Gaussian Poincaré yields
\[
\mathbb E\|h(G)+C-\mu\|^2
\le
\delta^2d
\left[
1+\frac{2\lambda^2(1-\lambda^{2N})}{a^2}
\right].
\]

Finally, the independent reserve gives a direct density argument. For any jointly distributed \(Y,D\), an independent standard Gaussian \(V\), and finite \(\mathbb E\|D\|^2\), the density of \(Y+tD+\tau V\) has a first-order expansion whose remainder satisfies
\[
\left\|
\mathcal L(Y+tD+\tau V)-P_0-tL
\right\|_{\mathrm{TV}}
\le
\frac{\phi(1)t^2}{\tau^2}\mathbb E\|D\|^2.
\]
Here \(L\) is the signed first variation of the density. The bound follows by integrating the absolute second directional derivative of a Gaussian density:
\[
\int\left|D^2\phi_\tau(x)[v,v]\right|\,dx
=
\frac{4\phi(1)}{\tau^2}\|v\|^2.
\]

Applying this to the actual perturbation \(h(G)+C-\mu\), and using the telescoping identity for its first variation, proves the displayed TV theorem. No finite collection of moments is used as a substitute for full-law control.

### Query and arithmetic costs

Every execution uses at most **three whole-vector \(g\)-queries**: \(g(G),g(A_j),g(B_j)\). The tail branch uses one.

The capped index can be generated with at most \(N\) Bernoulli trials. Those trials can themselves be generated from Gaussian seeds using the packet’s finite Gaussian-to-uniform construction. The surrounding cost is
\[
O(d+N)\ \text{real arithmetic and Gaussian draws},
\qquad O(d)\ \text{storage}.
\]

For fixed \(\lambda\) and \(N=O(\log(d/\varepsilon))\), the inverse probabilities \(1/p_j\) have polynomial size in \(d/\varepsilon\). A complete finite-bit implementation remains an obligation: it needs an explicit primitive-error budget and a common rounding convention for the output and target law. The current continuous-law theorem uses exact Gaussian seeds and real arithmetic.

## 3. The pointwise Newton obstruction

The obstruction is already present in one dimension at an exactly Gaussian affine channel:
\[
X=\lambda G+aZ,\qquad a=\sqrt{1-\lambda^2}.
\]

Let
\[
\delta_Z=Z-\partial_Z,\qquad N_Z=\delta_Z\partial_Z.
\]
The source-centered Newton representation in S3 writes
\[
u=\delta_ZJ.
\]
At the affine reference, its exact linearized equation becomes
\[
\boxed{
\bigl[a(N_Z+2)+\lambda\delta_Z\partial_G\bigr]J=-R.
}
\]

The \(+2\) includes both contributions from the Gaussian baseline. Omitting one changes the operator.

### Exact inverse on Hermite chaos

Let \(e_n=\mathrm{He}_n/\sqrt{n!}\) be the normalized Hermite polynomials. For the unit-norm forcing \(R=e_n(G)\), the unique solution in total chaos \(n\) is
\[
J=\sum_{j=0}^n c_j e_{n-j}(G)e_j(Z),
\]
with
\[
c_j=
\frac{(-1)^{j+1}}{a}
\left(\frac{\lambda}{a}\right)^j
\frac{\sqrt{\binom nj}}{(j+1)(j+2)}.
\]

Orthogonality gives the exact expression
\[
\|\partial_Zu\|_2^2
=
a^{-2}
\sum_{j=0}^n
\binom nj
\frac{(\lambda^2/a^2)^j}{(j+2)^2}.
\]
Consequently,
\[
\|\partial_Zu\|_2\ge\frac{a^{-n-1}}{n+2},
\]
and, more strongly for the existence of an \(L^2\) inverse,
\[
\|J\|_2
\ge
\frac{a^{-n-1}}{(n+1)(n+2)}.
\]

For every nonzero \(\lambda\), these grow exponentially with degree. Other chaos degrees cannot cancel this amplification: the operator preserves total chaos, and its restriction to each finite block is invertible. Testing a weak \(L^2\) solution against finite Hermite products forces the same coefficients.

Thus this is a failure of the inverse itself, beyond failure of a particular Neumann-series estimate.

### Some bounded smooth forcings have no \(L^2\) solution

For
\[
0<\beta<\frac{\lambda^2}{2a^2},
\]
consider
\[
R_\beta(G)=
\sum_{m\ge1}e^{-\beta m^2}\cos(mG).
\]
This function is bounded, has bounded derivatives of every order, and is entire.

The inverse of \(\cos(kG)\) has norm growing at least as
\[
\frac{\exp\!\bigl(\lambda^2k^2/(2a^2)\bigr)}
     {\operatorname{poly}(k)}.
\]
Within each even Hermite degree, all the cosine summands have the same coefficient sign. Their inverse contributions therefore cannot cancel. The weighted inverse norms diverge, proving that \(R_\beta\) has no weak \(L^2\) solution.

Smoothness—even analyticity by itself—is insufficient for this interface.

### The bad forcing arises from legal source perturbations

Take
\[
g_{\eta,k}(x)
=
\lambda x+\eta\frac{\sin(kx)}{k}
=
F_{\eta,k}'(x),
\]
where
\[
F_{\eta,k}(x)
=
\frac{\lambda x^2}{2}
-\frac{\eta\cos(kx)}{k^2}.
\]
These are smooth conservative sources, uniformly \((\lambda+|\eta|)\)-Lipschitz in \(k\). For \(|\eta|<\lambda\), the potentials are even strongly convex.

Writing \(f_k=\sin(kx)/k\), the actual first-order Stein residual of
\[
g_{\eta,k}(G)+aZ
\]
is
\[
R_1=\lambda(f_k'+K_{f_k}),
\qquad
K_{f_k}=\int_0^1P_t f_k'\,dt.
\]
In Hermite degree \(n\), its coefficients equal those of \(\cos(kG)\), multiplied by
\[
\lambda\left(1+\frac1{n+1}\right).
\]
The unstable components survive.

At the same time, a direct conditional-Gaussian comparison gives
\[
d_{\mathrm{TV}}\!\left(
\mathcal L(g_{\eta,k}(G)+aZ),\mathcal N(0,1)
\right)
\le
\frac{|\eta|}{ka\sqrt{2\pi}}.
\]

The output law approaches its target as the pointwise inverse becomes exponentially worse. The pointwise equation is demanding correction of source detail that the output largely suppresses.

This disproves a uniformly \(L^2\)-controlled differentiable pointwise Newton construction over the allowed source class. It does **not** lower-bound the original sampling problem or exclude a smaller, appropriately smoothed residual class.

### A sharp restricted repair

For source-only forcing \(P_\rho R(G)\), the same calculation gives
\[
\rho\le a
\quad\Longrightarrow\quad
\|\partial_Zu\|_2\le\frac{\|R\|_2}{2a}.
\]
For \(\rho>a\), no bounded inverse exists on this source-only subspace.

That is a sharp smoothing threshold for this specified interface. It does not extend automatically to arbitrary residuals depending jointly on \(G,Z\).

## 4. Why controlling the output law is analytically better—and still not a free oracle

There is a useful general structure behind the paired construction. Let
\[
Y=h(G)+sZ,\qquad Y'=h(G)+sZ',
\]
where \(h\) is \(L\)-Lipschitz, and define the analysis operator
\[
Tw(y)=\mathbb E[w(Y')\mid Y=y].
\]
On centered \(L^2(\mathcal L(Y))\),
\[
0\le T\le\frac{L^2}{L^2+s^2}I.
\]
Hence \(I-T\) has a gap of at least \(s^2/(L^2+s^2)\).

This contraction is known mathematics: it is a specialization of Klartag–Ordentlich’s strong data-processing bound under Gaussian heat flow, using the Poincaré constant of a Lipschitz Gaussian image. I do not claim it as a new theorem. [arxiv.org](https://arxiv.org/html/2406.03427v1?utm_source=chatgpt.com)

For an available centered direction \(v\), the abstract solution
\[
w=(I-T)^{-1}v
\]
produces
\[
D=w(Y)-w(Y'),
\]
with
\[
\mathbb E[D\mid G]=0,\qquad
\mathbb E[D\mid Y]=v(Y),
\]
and
\[
\mathbb E\|D\|^2
\le
\frac{2(L^2+s^2)}{s^2}\|v\|_2^2.
\]

The important acquisition boundary is that **\(w\) is not supplied by this theorem**. For nonlinear \(h\), applying \(T\) involves the posterior \(G\mid Y=y\). Repeatedly generating replicas from the same latent \(G\) does not implement repeated applications of \(T\).

At the affine reference, the relevant conditional Gaussian operations are explicit. That is what makes the finite telescoping construction in Section 2 possible.

The helper also derived a separate bounded projected inverse with an unbiased implementation using **one residual-value evaluation** and finite second moment; its full formula is in PROJECTED_AFFINE_RESOLVENT.txt[PROJECTED_AFFINE_RESOLVENT.txt](sandbox:/workspace/scratch/23206e14a217/research/predictive_interface/PROJECTED_AFFINE_RESOLVENT.txt). A residual-value oracle is not automatically an original \(g\)-value oracle. The three-query construction above closes that distinction for its declared first-order operation.

## 5. Decisive failures of immediate completion

I tested whether the acquired correction could already be promoted to arbitrary accuracy. Two explicit failures prevent that conclusion.

### Increasing the cap leaves an actual variance defect

Take \(h(x)=\eta x\). As \(N\to\infty\), the output becomes exactly Gaussian, with variance
\[
v_1=
1+\tau^2+
\eta^2\left(1+\frac{2\lambda^2}{a^2}\right)
\]
per coordinate, instead of
\[
v_0=1+\tau^2.
\]

Thus the quadratic remainder represents a real law defect. Increasing the cap removes the first-order truncation error but leaves the wrong covariance.

For \(\lambda=\tfrac12,\eta=0.1,\tau=1\), the exact TV distance between these two \(d\)-dimensional Gaussians is:

| Dimension \(d\) | TV distance after the cap tends to infinity |
|---:|---:|
| 1 | 0.00200806 |
| 100 | 0.0233682 |
| 10,000 | 0.230785 |
| 1,000,000 | 0.996654 |

These values use the exact radial-density crossing formula, recorded in CHECK_RESULTS.txt[CHECK_RESULTS.txt](sandbox:/workspace/scratch/23206e14a217/research/gaussian_mean/CHECK_RESULTS.txt).

For a known affine field, ordinary Gaussian covariance completion removes this defect exactly. The example establishes the need for a genuine next correction in the proposed mechanism.

### Bounded correction size does not preserve source regularity

For the uniformly 1-Lipschitz functions
\[
f_k(x)=\frac{\sin(kx)}k,
\]
the derivative of the active correction with respect to its shared Gaussian seed \(U\) can reach
\[
\frac{2\sqrt{1-r_j^2}}{p_j}.
\]
This grows like \(\lambda^{-2j}\).

The correction has controlled amplitude and second moment, yet the complete randomized program can develop a large seed derivative. It also introduces additional seeds and a discrete branch. Its output is therefore not automatically another source in the original conservative Lipschitz class.

Any recursive theorem must accommodate this explicitly. Feeding the corrected output back into the same theorem would currently be unjustified.

## 6. Checks and conventional alternatives

The implementation and proof checks include:

- Exact rational verification of 81 Hermite-chaos blocks, the inverse lower bounds, and the smoothing upper bound.
- Independent cosine-integral and Hermite-series calculations, agreeing to a maximum relative residual of \(2.43\times10^{-14}\).
- Direct nonlinear quadrature of the telescoping conditional identity, with maximum discrepancy \(3.33\times10^{-16}\).
- 1,200 executions of the actual capped factory across several dimensions and caps, with a maximum of three original \(g\)-queries.
- Integration of complete one-dimensional output densities for affine and nonlinear examples.

For the nonlinear fixture
\[
f(x)=0.35+\frac{\sin(1.3x)}{1.3}
+\frac{0.4\cos(0.7x)}{0.7},
\qquad h=\eta f,
\]
using \(\lambda=\tfrac12,\tau=1,N=6\), the results were:

| \(\eta\) | Integrated-density TV diagnostic | Proved analytic TV upper bound |
|---:|---:|---:|
| 0.04 | 0.000119897 | 0.00126730 |
| 0.08 | 0.000480515 | 0.00506376 |
| 0.16 | 0.00193346 | 0.0202441 |

The numerical density calculations diagnose the implementation. The analytic theorem supplies the full-law guarantee; the quadrature is not being represented as a rigorous numerical TV certificate.

### The strongest simple comparator is already strong

Under the same known near-affine decomposition, if only the Gaussian mean marginal is required, the one-query program
\[
h(G)+\sqrt{1+\tau^2}\,V
\]
benefits from S5’s averaging argument. In the small-residual regime its error is
\[
O\!\left(\frac{\delta^2\sqrt d}{1+\tau^2}\right),
\]
often better than the \(O(\delta^2d/\tau^2)\) bound proved here.

The acquired capability added by the paired construction is its exact conditional mean \(g(G)\), combined with a finite correction of the first-order output discrepancy. That could support source-dependent reuse, but no practical superiority has been established.

The wider primary literature also already contains positive Gaussian-cloud corrections and high-accuracy stochastic-query sampling mechanisms. Their actual oracle assumptions and parameter dependence remain the appropriate comparison; positivity or a formal high-accuracy correction is not itself new. [arxiv.org](https://arxiv.org/html/2609.38710v1?utm_source=chatgpt.com)

Historical novelty and practical advantage remain separate, unestablished claims.

## 7. Independent acquisition result: exact predictive-law geometry

The helper attacked N952 through a legal stationary CP subfamily with one hidden classical bit, represented as a qubit.

Each fresh episode starts in state \(0\). There are two actions:

- **Charge \(C\):** state \(0\) changes to \(1\) with unknown probability \(p\); state \(1\) remains \(1\). The visible outcome is constant.
- **Read \(R\):** report the bit nondestructively.

These are explicit CP instruments. For \(p>0\), the predictive rank is two.

The family structure is supplied for the upper theorem. Finite observed counts do not establish that an arbitrary unknown process belongs to this family.

### Exact distance between all future policy laws

Within one retained-memory episode, draw
\[
W_p\sim\operatorname{Geom}(p),
\]
the index of the first successful charge. Every subsequent transcript under any causal policy is a common function of \(W_p\) and the policy’s own randomness.

For \(0\le p\le q\le1\), define
\[
d_H(p,q)
=
\max_{0\le k\le H}
\left[(1-p)^k-(1-q)^k\right].
\]

Then
\[
\boxed{
\sup_\pi
d_{\mathrm{TV}}(P_p^\pi,P_q^\pi)
=
d_H(p,q),
}
\]
where policies may use feedback, arbitrary reads, and retained-memory macros, with at most \(H\) charges.

The proof uses the single sign change in the likelihood ratio of the two censored geometric laws. A single experiment \(C^kR\), for a maximizing \(k\), attains the supremum.

Thus adaptive-policy complexity disappears from the exact operational metric in this family.

### Acquiring a positive predictor from legal counts

Run \(C^hR\) in \(N\) independent calibration episodes and record \(x\) successes. The count is binomial with parameter
\[
q_h(p)=1-(1-p)^h.
\]

An exact binomial confidence interval \([L,U]\) transforms to
\[
[\ell,u]
=
\left[
1-(1-L)^{1/h},
\;
1-(1-U)^{1/h}
\right].
\]

Choose \(\hat p\in[\ell,u]\), and implement the positive two-state model at \(\hat p\), retaining its state across macros. On the same confidence event, simultaneously for every future policy within the episode,
\[
d_{\mathrm{TV}}(P_p^\pi,P_{\hat p}^\pi)
\le
\max\{d_H(\ell,\hat p),d_H(\hat p,u)\}.
\]

This is a full-law result because the declared process family has the geometric path representation. It does not infer unrestricted law accuracy from finite moments.

Calibration pays for \(N\) fresh starts, \(Nh\) charge calls, and \(N\) reads. A data-dependent choice of \(h\) requires a paid pilot or valid simultaneous/sequential inference.

The future-policy theorem concerns **one retained-memory episode**. Several independent future starts require a separate composition bound. If \(\ell=0<u\), the unrestricted-horizon confidence diameter is one.

### A genuine information cost remains

For any adaptive acquisition strategy using at most \(B\) charge calls,
\[
\mathrm{KL}(\mathcal D_p\|\mathcal D_q)
\le
B\,\mathrm{kl}(\operatorname{Ber}(p)\|
                    \operatorname{Ber}(q)).
\]

Taking \(q=(1+\eta)p\) and a future horizon of order \(1/p\) yields the lower bound
\[
\boxed{
B=\Omega\!\left(
\frac{1}{p\varepsilon^2}\log\frac1\alpha
\right)
}
\]
for learning the future laws to error \(\varepsilon\) with confidence \(1-\alpha\), in the stated small-error regime.

This scaling is achievable in the family by appropriate binomial calibration. Ordinary likelihood-based estimation can realize it; no superiority over that conventional alternative is claimed.

The lower bound also survives adding a known action that sets the bit to \(1\). That action allows a predictive core with inverse norm independent of \(p\), while providing no information about the rare transition. Consequently the information obstruction persists after the short-core conditioning problem is removed.

The proof, acquisition method, and costs are in OBSERVABLE_HAZARD_GEOMETRY.txt[OBSERVABLE_HAZARD_GEOMETRY.txt](sandbox:/workspace/scratch/23206e14a217/research/predictive_interface/OBSERVABLE_HAZARD_GEOMETRY.txt). Its checks include 1,000 complete censored-law comparisons and 1,000 adaptive transcript comparisons. This resolves a discriminating subfamily, not acquisition of arbitrary rank-\(r\) quantum instruments.

## 8. The exact next scientific obligation

For the main target, the next construction must produce a **reusable representation of the output-law residual** of the three-query update, together with a positive correction acquired from original values.

A sufficient next theorem would establish a discrepancy \(\mathcal E\), controlling the final TV error after budgeted smoothing, and a legal correction \(K\) satisfying
\[
\mathcal E(KS)\le C\,\mathcal E(S)^2
\]
on a specified source-state class. The theorem must include:

1. **Acquisition:** the corrective direction is obtained from \(g\)-values, with all subsidiary calls counted.
2. **Closure:** the class tolerates the demonstrated growth in seed derivatives, the extra Gaussian seeds, and the discrete branch.
3. **Dimension control:** the quadratic error avoids the present \(d\delta^2\) obstruction strongly enough to support the target.
4. **Complete execution cost:** fixed branching through \(O(\log\log(1/\varepsilon))\) correction depth, or a proved alternative tail bound, with polynomial arithmetic.
5. **Entrance and variance budget:** a legal path from a general allowed source into the class, using only the fixed target noise budget.

The source-smoothing threshold provides another precise possibility: prove that an acquired compiler generates residuals inside a space satisfying the required smoothing budget. Analyticity alone cannot establish that, because the bounded entire counterexample already defeats the unrestricted inverse.

The scientific decision supported by this work is to pursue an acquired, recursively closed correction of the output law. The pointwise \(L^2\) inverse has now failed at a legal smooth perturbation; the finite paired construction identifies a replacement operation and exposes the specific obligations that remain.

### Proofs, code, and data

| Material | Files |
|---|---|
| Main obstruction, three-query construction, TV proof, costs, and recursion failures | POINTWISE_NEWTON_OBSTRUCTION.txt[POINTWISE_NEWTON_OBSTRUCTION.txt](sandbox:/workspace/scratch/23206e14a217/research/gaussian_mean/POINTWISE_NEWTON_OBSTRUCTION.txt) |
| Executable sampler and main checks | check_and_sample.py[check_and_sample.py](sandbox:/workspace/scratch/23206e14a217/research/gaussian_mean/check_and_sample.py), CHECK_RESULTS.txt[CHECK_RESULTS.txt](sandbox:/workspace/scratch/23206e14a217/research/gaussian_mean/CHECK_RESULTS.txt) |
| Numerical data | INVERSE_AMPLIFICATION.csv[INVERSE_AMPLIFICATION.csv](sandbox:/workspace/scratch/23206e14a217/research/gaussian_mean/INVERSE_AMPLIFICATION.csv), NONLINEAR_DENSITY_CHECK.csv[NONLINEAR_DENSITY_CHECK.csv](sandbox:/workspace/scratch/23206e14a217/research/gaussian_mean/NONLINEAR_DENSITY_CHECK.csv) |
| Independent inverse audit and projected construction | AFFINE_NEWTON_INVERSE_AUDIT.txt[AFFINE_NEWTON_INVERSE_AUDIT.txt](sandbox:/workspace/scratch/23206e14a217/research/predictive_interface/AFFINE_NEWTON_INVERSE_AUDIT.txt), PROJECTED_AFFINE_RESOLVENT.txt[PROJECTED_AFFINE_RESOLVENT.txt](sandbox:/workspace/scratch/23206e14a217/research/predictive_interface/PROJECTED_AFFINE_RESOLVENT.txt) |
| Predictive-process theorem and reproducible checks | OBSERVABLE_HAZARD_GEOMETRY.txt[OBSERVABLE_HAZARD_GEOMETRY.txt](sandbox:/workspace/scratch/23206e14a217/research/predictive_interface/OBSERVABLE_HAZARD_GEOMETRY.txt), check_hazard_geometry.py[check_hazard_geometry.py](sandbox:/workspace/scratch/23206e14a217/research/predictive_interface/check_hazard_geometry.py), SYNTHETIC_COUNTS.csv[SYNTHETIC_COUNTS.csv](sandbox:/workspace/scratch/23206e14a217/research/predictive_interface/SYNTHETIC_COUNTS.csv) |