# Primary-literature comparison: Laplace-positive convolution regularization

## Candidate and scope

The candidate concerns a compactly supported finite-order Hermitian matrix distribution $T$ on $\mathbb R^m$, normalized by $T(1)=I$. It asks whether strict positivity of its real Laplace transform

$$L_T(g)=\langle T,e^{g\cdot y}\rangle\succ0\quad(g\in\mathbb R^m)$$

is equivalent to existence of a smooth radial strictly log-concave probability density $p$, with every exponential moment, for which $p*T$ is pointwise positive definite. The proposed sufficiency permits arbitrarily small positive eigenvalue margins and chooses an adaptively slow unbounded radial log-slope. This is an overlap map, not a novelty finding.

## Decisive scalar predecessor: Diamond–Essén

H. G. Diamond and M. Essén, “Functions with non-negative convolutions,” *Journal of Mathematical Analysis and Applications* **63** (1978), no. 2, 463–489, [DOI 10.1016/0022-247X(78)90091-4](https://doi.org/10.1016/0022-247X(78)90091-4), is the closest scalar predecessor located. Katkova–Vishnyakova (below, p. 2) expressly describe it as investigating conditions on an input function $u$ that ensure existence of a nonnegative Borel measure $\mu$ with $u*\mu\ge0$. This is directly about scalar convolution positivity and is therefore priority-critical.

I could not verify Diamond–Essén’s theorem statement from the original paper. The ScienceDirect record labels it “Open archive,” but the publisher page and PDF route returned Cloudflare verification/403; Elsevier’s unkeyed text-mining endpoint returned minimized metadata only. No claim is made here about whether their criterion is exactly $L_u(x)>0$, whether it requires endpoint or quantitative margin conditions, or whether the result covers measures/distributions rather than functions. The proposed $L=BQ$ small-margin example therefore remains unclassified against Diamond–Essén. See [source receipts](SOURCE_RECEIPTS.md) for the access record. Reading the paper’s exact theorem is necessary before making a scalar priority claim.

## Exact continuous scalar overlap: Katkova–Vishnyakova

A. Katkova and A. Vishnyakova, “A Continual Analogue of a Theorem by M. Fekete and G. Pólya,” *Positivity* **5** (2001), 1–11, [DOI 10.1023/A:1009847605313](https://doi.org/10.1023/A:1009847605313), Theorems 1–2, give an exact scalar existence result. Their compact-support Theorem 2 assumes a real continuous function $u$ on $[a,b]$, with $u(a)>0$, $u(b)>0$, and bilateral Laplace transform $L_u(x)>0$ for every real $x$. Then there is $\varepsilon_0>0$ such that for each $0<\varepsilon\le\varepsilon_0$ there is $\lambda_\varepsilon>0$ for which, for every $\lambda\ge\lambda_\varepsilon$,

$$L_u(x)e^{\lambda e^{\varepsilon x}}$$

is the Laplace transform of a nonnegative function. The multiplier is the Laplace transform of the one-sided atomic measure $\mu_{\lambda,\varepsilon}$ on $\varepsilon\mathbb N$, with $\mu_{\lambda,\varepsilon}(\{\varepsilon k\})=\lambda^k/k!$; thus $u*\mu_{\lambda,\varepsilon}\ge0$. The hypothesis is pointwise strict transform positivity and includes no quantitative lower bound on $L_u$ at infinity. The proof handles tails through the positive endpoint values and uses compact-set positivity in the middle. So a global transform margin is not required within this endpoint class.

This does not settle the candidate. A smooth compactly supported density extended by zero has zero endpoint values at the boundary of its support, so Theorem 2 does not apply directly. Its output is nonnegative and obtained with a one-sided atomic, $u$-dependent choice of $\lambda$ and small $\varepsilon$; it is not a single smooth radial probability kernel and does not assert pointwise strict positivity on all of $\mathbb R^m$. The paper’s Theorem 1 extends the input to a continuous half-line function with integrable exponential tails, nonnegative outside a bounded interval, positive at some point on each tail, and $L_u(x)>0$ for all real $x$. It still uses the same atomic multiplier.

The authors explicitly distinguish their “standard” multiplier, whose form is independent of $u$, from Diamond–Essén’s more general existence question; they also give an example showing their fixed lattice multiplier need not work for a signed measure even when its bilateral Laplace transform is positive and the measure is positive near its support endpoints (Remark, pp. 10–11). That example refutes universal applicability of their particular multiplier, not existence of an arbitrary positive convolution measure.

## Poincaré–Pólya and Handelman: finite-support coefficient positivity

Katkova–Vishnyakova state the Fekete–Pólya theorem: if a real polynomial $f(u)$ is strictly positive for $u\ge0$, then for all sufficiently large $\lambda$, $e^{\lambda u}f(u)$ has nonnegative Taylor coefficients. Interpreting $f(u)=\sum_k a_k u^k$ as the Laplace transform of a finitely supported signed measure on $\mathbb N$ identifies this with a discrete convolution/coefficient result. It has finite support and a discrete Poisson-type multiplier, rather than a smooth radial kernel on Euclidean space.

For multivariate finite support, D. Handelman, “Deciding eventual positivity of polynomials,” *Ergodic Theory and Dynamical Systems* **6** (1986), 57–79, [DOI 10.1017/S0143385700003291](https://doi.org/10.1017/S0143385700003291), gives the sharp lattice comparison. In the easier multiplier problem in §I (pp. 57–58), a Laurent polynomial $f$ admits a Laurent polynomial $Q$ with nonnegative coefficients and $Qf$ coefficientwise nonnegative iff every face polynomial $f_F$ of its Newton polytope, including $f$ itself, is strictly positive on the positive orthant. The eventual-power Theorem A combines strict positivity for dominant strata of the full support of $f$ with recursive proper-face coefficient conditions; Theorem B gives a criterion through strict positivity on the appropriate dominant strata for the relative faces of $\operatorname{supp}P$. These are finite lattice/coefficient criteria, not all-real-parameter Laplace criteria or convolution by a smooth density. Handelman’s introduction records the historical scope: Poincaré handled one variable; Meissner and Pólya treated cases with standard hypercube/simplex Newton polyhedra.

D. Handelman, “Representing polynomials by positive linear functions on compact convex polyhedra,” *Pacific Journal of Mathematics* **132** (1988), 35–62, [DOI 10.2140/pjm.1988.132.35](https://doi.org/10.2140/pjm.1988.132.35), Theorem 1.3 (p. 39), proves that a polynomial strictly positive on a compact full-dimensional polyhedron defined by affine inequalities $\beta_i\ge0$ is a finite linear combination, with nonnegative coefficients, of products of the defining $\beta_i$. This is a compact-domain algebraic positivity certificate, not a Laplace-transform or convolution theorem.

## Matrix and operator polynomial analogues

Lê and Dư, “Handelman’s Positivstellensatz for polynomial matrices positive definite on polyhedra,” *Positivity* **22** (2018), 449–460, [DOI 10.1007/s11117-017-0520-y](https://doi.org/10.1007/s11117-017-0520-y), Theorems 2.1 and 3.1, prove a matrix-polynomial extension on compact polyhedra. On a simplex, if a symmetric polynomial matrix $F$ has degree $d>0$ and a uniform margin $F\succeq\lambda I$ there, their Bernstein–Bézier coefficient bound gives positive-definite constant matrix coefficients in the Handelman representation for integers

$$N>\frac{d(d-1)}{2}\frac{C}{\lambda}-d,$$

where $C$ is the stated coefficient norm of the homogeneous lift. The polyhedron theorem reduces to a lifted simplex and also assumes a positive margin on that compact simplex. This gives a finite-dimensional matrix positivity analogue, but its explicit bound depends on a uniform compact-domain margin; it does not concern matrix distributions, Laplace multipliers, or a radial kernel.

J. Cimprič and A. Zalar, “Moment problems for operator polynomials,” *Journal of Mathematical Analysis and Applications* **401** (2013), 307–316, [DOI 10.1016/j.jmaa.2012.12.027](https://doi.org/10.1016/j.jmaa.2012.12.027), Theorems 3–5, extend Haviland-type representing-measure results to operator-polynomial maps and give compact archimedean/Schmüdgen-type results. For operator-valued output on a general closed set, their Theorem 4 assumes complete positivity; for compact sets, their Remark 6 says positivity suffices. Their §5 example shows that the archimedeanity and strict-positivity certificate assertions of the finite-dimensional matrix Theorem 6 fail for operator polynomials; they leave the corresponding representing-measure assertion open. These are moment representation and semialgebraic positivity results; they do not give a convolution regularizer or Laplace-positive-distribution criterion.

## Comparison and priority limit

The necessary implication for the candidate is elementary whenever the transforms exist: $L_{p*T}(g)=L_p(g)L_T(g)$, and $L_p(g)>0$ for a probability density $p>0$. Hence $p*T\succ0$ implies $L_T(g)\succ0$.

The accessible sources establish close scalar overlap with no global transform-margin hypothesis for inputs positive at their support endpoints, and extensive finite-support scalar, matrix, and operator polynomial analogues. They do not state the full proposed combination of arbitrary compactly supported finite-order Hermitian matrix distributions on $\mathbb R^m$, pointwise positive transform with margins allowed to decay arbitrarily, and one smooth radial strictly log-concave probability kernel giving pointwise strict output. Diamond–Essén is the decisive scalar source, and its exact theorem remains unread here. Therefore this comparison supports neither a novelty claim nor a claim that the scalar full criterion is preexisting.
