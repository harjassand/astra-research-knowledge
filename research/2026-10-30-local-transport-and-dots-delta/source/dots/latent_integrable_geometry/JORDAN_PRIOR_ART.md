# Raw quadratic equations → rank-one Riccati geometry: audit and prior art

**Decision (2026-10-29): retain the tested recognition capability; reject this as a new algorithmic mechanism or a filtering speedup.** The quotient construction is sound. An independently implemented, equally informed Bernstein–Peirce construction acquires the same matrix geometry from the same raw coefficients using rational linear algebra, and then uses the same classical Riccati decoder. I did not locate a publication presenting the identical packaged quotient algorithm; that limited search result is not evidence of novelty.

## 1. What is already classical

* **Raw quadratic field → algebra.** Markus explicitly attached a commutative, generally nonassociative algebra to a quadratic differential system and related equivalence of systems to algebra isomorphism. Polarizing the Hessian is therefore not new discovery machinery. [Markus, *Quadratic Differential Equations and Non-Associative Algebras* (1960), original paper](https://rainbow.ldeo.columbia.edu/~alexeyk/QDS/Markus1960.pdf).
* **Jordan structure → Riccati equations.** Walcher's 1986 paper directly concerns regular Jordan pairs and Riccati equations. Its bibliographic existence is verified, but I did not retrieve its full primary text and do not attribute the present reconstruction algorithm to it. [Publisher DOI, Walcher (1986)](https://doi.org/10.1080/00927878608823405).
* **Constructive unital Jordan operations.** Jacobson's strong coordinatization theorem gives matrix coordinatization from appropriate idempotents and connectors, not an automatic supply of them. Orlitzky gives an arbitrary-basis rank/characteristic-polynomial algorithm for Euclidean Jordan algebras, not an end-to-end general raw-ODE matrix recognition theorem. These are stronger comparators than merely knowing the abstract classification. [Jacobson, *Lectures on Quadratic Jordan Algebras*, Chapter II (1969)](https://mathweb.tifr.res.in/Documents/Publications/Lectures/tifr45.pdf); [Orlitzky (2022), original manuscript](https://michael.orlitzky.com/documents/papers/rank_computation_in_euclidean_jordan_algebras.pdf).
* **The relevant nonunital ancestor is Bernstein algebra theory.** Walcher studied Bernstein algebras that are Jordan algebras. González–Martínez explicitly treat idempotents and Peirce decomposition in Bernstein algebras, which generally have no identity. Thus failure to find a unit does not defeat classical Peirce methods. [Walcher (1988), original paper](https://www.math.uci.edu/~brusso/walcherArchMath88.pdf); [González–Martínez (1990), original paper](https://www.math.uci.edu/~brusso/gonzalezmartinezJLMS90.pdf), [publisher record](https://doi.org/10.1112/jlms/s2-42.3.430). The primary scans were search-index accessible but direct fetching was unreliable; the exact specialization below is also independently derived and tested, not dependent on an unread theorem.
* **Nonlinear algebraic ODEs already have linear-algebraic solution methods.** Walcher (1992) solves the Bernstein-train equations and describes a matrix-function construction for more general Bernstein equations. This does not by itself solve an arbitrary affine drift, but it rules out treating Bernstein recognition followed by special-function evaluation as a new general principle. [Walcher, *On Bernstein algebras which are train algebras* (1992), §§2–3](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/7752B5532C2D338C636854CE7F578543/S0013091500005411a.pdf/on_bernstein_algebras_which_are_train_algebras.pdf).
* Svinolupov's Jordan correspondence concerns integrable many-field KdV systems; it is not the most direct comparator for this finite-dimensional reconstruction. Veronese recognition also has classical differential criteria, but these do not establish that the exact quotient-contraction algorithm below was previously packaged. [Svinolupov (1991), primary journal abstract](https://www.mathnet.ru/php/archive.phtml?jrnid=tmf&option_lang=eng&paperid=5498&wshow=paper); [Konnov (2000), original paper](https://www.mathnet.ru/links/6721f14ab852bc5b451e450f29511789/im303_eng.pdf).

## 2. Soundness and completeness of the quotient construction

Write the raw field as `f=c+Lx−q(x)`, with `q` homogeneous quadratic, on `V` of dimension `d=m(m+1)/2`. Its product is `a*b=(q(a+b)−q(a)−q(b))/2`. The **common** derivative kernel, not a kernel at a sampled point, is

`Ann = {a: a*b=0 for every b}`.

Suppose an unknown invertible linear map `S:Sym_m→V` satisfies

`q(SP)=S[(Pr)(Pr)^T]`, `r≠0`.

Then `Ann=S{P:Pr=0}`. One implication is immediate; for the other, if `Pr≠0`, choose symmetric `Q` with `Qr=Pr` and the polarized product is nonzero. Since `P↦Pr` is surjective, the quotient dimension is `m`.

Any acquired full-rank quotient `B:V→W` has `BS(P)=UPr` for invertible `U`. Factoring the quadratic coefficients gives

`q(x)=K[(Bx)(Bx)^T]`,

where `K:Sym_m→V` is invertible and, necessarily,

`K(X)=S(U^-1 X U^-T)`.

Consequently the acquired chart is `X=K^-1x=UPU^T`, and

`BK(X)=X r'`, where `r'=U^-T r`.

Thus the contraction test is a linear coefficient solve and is complete on this class. Its success plus invertibility and the factor identity proves `K^-1q(KX)=Xr'r'^TX`. Factoring through an `m`-dimensional quotient alone would **not** suffice. The separate linear test for `K^-1LK(X)=AX+XA^T`, with arbitrary symmetric transformed constant `Q`, proves the full identity

`X'=AX+XA^T+Q−Xr'r'^TX`.

Both `r'` and `A` are unique in this chart: contraction on all symmetric matrices identifies `r'`; if `DX+XD^T=0` for all symmetric `X`, first `X=I` makes `D` skew, then all diagonal `X` force `D=0`.

The implementation's off-diagonal coefficient convention is consistent with its `vec`/`sym` functions. Rational raw coefficients require only rational linear algebra, even if a physical factorization of the original rank-one matrix used square roots. Completeness is for the specified exact rank-one class, not generic quadratic fields or arbitrary measurement rank. An affine translation can also leave a Riccati field in this admitted form, but recovering the original physical covariance origin is not promised.

## 3. Concrete equally informed Bernstein–Peirce comparator

This section is an independently derived specialization of the classical operations, not a claim of a historically identical algorithm.

In the rank-one matrix model,

`P*Q=(Prr^TQ+Qrr^TP)/2`, `ω(P)=r^TPr`.

Direct multiplication gives `P^3=ω(P)P^2` and `(P^2)^2=ω(P)^2P^2`; `ω` is multiplicative. This is a Bernstein–Jordan algebra. For its left multiplication operator,

`trace L_P = (m+1)ω(P)/2`.

Indeed, after a congruence taking `r` to the first coordinate, the operator is triangular with diagonal eigenvalues `ω(P)` once, `ω(P)/2` repeated `m−1` times, and zero on the lower symmetric block. Trace invariance makes this weight formula usable directly in the raw basis.

1. Acquire `ω=2 trace L/(m+1)`; choose a raw coordinate basis vector `a` with `ω(a)≠0`.
2. Acquire the idempotent `e=a*a/ω(a)^2`; no root-finding or unit is needed.
3. Solve the rational nullspaces of `L_e−I`, `L_e−I/2`, and `L_e`. The promised dimensions are `1`, `m−1`, and `m(m−1)/2`.
4. Choose any basis `u_1,…,u_(m−1)` of the half-eigenspace. Define the matrix-chart columns by
   * `E_11 ↦ e`;
   * `E_1j+E_j1 ↦ u_(j−1)`;
   * `E_ii ↦ u_(i−1)^2` for `i>1`;
   * `E_ij+E_ji ↦ 2u_(i−1)*u_(j−1)` for `1<i<j`.
5. Check invertibility and the entire quadratic identity, then perform the same linear Lyapunov-drift solve and constant transformation as the quotient method.

Completeness follows by a simultaneous congruence taking the acquired `e` to `E_11` and the measurement vector to `e_1`. The half-eigenspace becomes precisely the first-row/column off-diagonal space; its products span the lower symmetric block. Hence these columns are independent and give the desired product table. No eigenvalue separation, algebraic extension, or nonlinear algebraic search is required: the three eigenvalues are known rational constants.

The decoder for either chart is the same conventional block flow:

`[U(t);V(t)] = exp(t H)[I;X0]`,

`H=[−A^T,R; Q,A]`, `R=rr^T`, `X(t)=V(t)U(t)^−1`, `x(t)=K vec(X(t))`,

where `U(t)` is invertible. Differentiation verifies the Riccati identity. Both recognition methods have polynomial exact-arithmetic implementations from explicit rational coefficient tables, with rational bit growth charged; neither has an established asymptotic advantage over the other. The matrix exponential/solve is not intrinsically numerically stable for long times.

## 4. Independent code receipt and limitations

`audit/bernstein_peirce_comparator.py` imports **no producer code**. It acquires the original three-variable field, its linearly mixed version, and a six-variable/matrix-size-three generic stress input using the preceding comparator. It rejects all three producer controls: wrong quadratic contraction, wrong linear drift, and unsupported rank-two measurement. It independently verifies all eight matrix-component polynomial identities in the two serialized producer records, their contraction identities, and block-generator signs. Its acquired decoder agrees with high-accuracy DOP853 at three short times for each anchor (maximum observed discrepancy `3.5e−13`). Numerical agreement is not a rigorous error enclosure.

The acquisition interface receives only raw scalar equations: no hidden chart, physical matrix, or measurement direction is imported. The scientific input is nevertheless a small, recognizable Riccati model; obscuring it by a linear coordinate change is a stress test, not a new scientific discovery. The six-variable comparator example is likewise only a completeness stress test.

**Anchor precision:** Berry–Harlim Eq. 2.1 supplies a continuous-observation slow-fast filtering model; Eq. 2.2 is its **steady-state algebraic** Riccati equation. Their Figure 1 uses discrete observations. The present transient ODE is derived using the standard continuous-observation Kalman–Bucy covariance equation, with their listed parameter values and the explicitly chosen `ε=0.1`; it does not reproduce that figure's experiment. [Berry–Harlim, original article, Eqs. 2.1–2.2 and Figure 1](https://pmc.ncbi.nlm.nih.gov/articles/PMC4032560/).

Admission proves a matrix Riccati form, not automatically a physical filter: general admitted `Q` and initial `X0` need not be positive semidefinite. Exact rank tests are not robust recognition guarantees for noisy coefficients; singular-value gaps, chart conditioning, and input precision must be charged. Dense raw coefficient input already has order `d^3` entries. Saved producer evaluation has `cond(U)≈2.38×10^9` and absolute discrepancy `3.75×10^-8` at `t=4`, despite a benign covariance trajectory. Conventional stabilized Riccati methods are the relevant long-time comparator, not a deliberately ill-conditioned single block exponential. Ordinary physical Kalman solvers are given the matrix model from the start and need no recognition overhead. [Kalman–Bucy (1961), original paper](https://eceweb1.rutgers.edu/~gajic/pdffiles/519KalmanFiltering/KalmanBucy1961.pdf); [Dieci (1992), differential Riccati numerical integration](https://epubs.siam.org/doi/abs/10.1137/0729049).

### Audited source hashes

```
rank_one_riccati.py
aff851123caee0acc9a67a04467e735a6891ac1eca72638cd39bd11d08e6c75e
rank_one_results.json
c9a43e19b03568d9362a36614cd7eeeed6df7cfdd16ead9747d71f3353c277ea
audit/bernstein_peirce_comparator.py
e8fffd1a56a4bdc7f3aa3a949bfe8d28b0efe751bec1f38fd703dc9f0a379a2f
audit/bernstein_peirce_comparator.json
8f89da933143b16e44148fc4f69462b2b9594be5a31cafae1471aed1c786045d
```

**Research disposition:** verified engineering capability, negative novelty/comparator result. No new algorithmic mechanism survives the concrete equally informed comparator. A publication claiming the identical quotient implementation was not found, so do not replace this conclusion with an unsupported historical priority claim.
