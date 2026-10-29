# Acquired divergence-compensated projective modules

**Status:** an exact constructive theorem and a small exact implementation, not a claim of historical novelty or a general nonlinear solver. The underlying density representations, projective linearization, and Krylov closure are classical. The investigated bridge is acquiring the compensating operator and the original-state reconstruction module from raw polynomial equations, without supplying a coordinate change or observable dictionary.

## Contract

Input: a rational polynomial vector field `f` in `n` original variables, a nonnegative integer weight `m`, and a rank budget `R`. The deterministic implementation currently supports **two variables** and takes exact sparse coefficients; the mathematical algorithm is general in `n`. It charges all generated monomials and rational bit sizes. A circuit route described below has polynomial arithmetic overhead in the raw circuit size and rank budget, with randomized identity testing and all intermediate rational bit costs retained.

Output: either an exact invariant module containing `1,x_1,...,x_n`, its operator matrix, and an original-coordinate ratio decoder; or a certified rank lower bound exceeding `R`. A budget failure is not nonexistence at other weights or larger ranks. Searching weights must pay every rejected candidate. No unknown coordinate transformation is an input.

## 1. The manufactured operator

Let `D = sum_i f_i partial_i`, and manufacture

    q = -div(f)/(n+1),       T_m p = Dp + m q p.

The factor `n+1` is not fitted. It comes from the divergence of the projective action in dimension `n`.

Suppose a column of polynomial functions `phi`, containing `1,x_1,...,x_n` as its first entries, satisfies the exact polynomial identity

    T_m phi = A phi

for a constant rational matrix `A`. Along any real solution on an interval containing zero, let

    w(t) = exp(m integral_0^t q(x(s)) ds).

Then `z(t)=w(t) phi(x(t))` obeys `z'=Az`, with `z(0)=phi(x(0))`. Consequently

    x_i(t) = (exp(t A) phi(x(0)))_i /
             (exp(t A) phi(x(0)))_0.

This is original-state reconstruction, not merely a predictor of selected observables. On an actual finite real trajectory the denominator is nonzero because it equals `w(t)`. Conversely the displayed ratios solve the original ODE near zero by the polynomial identity and uniqueness. Continue only on the connected nonsingular interval; denominator zeros and removable singularities require separate treatment. A matrix exponential expression is an exact representation, not a cost-free numerically accurate evaluation: precision, coefficient sizes, and denominator conditioning must be charged.

## 2. Guaranteed acquisition class, with no supplied conjugacy

Consider a projective linear vector field in hidden coordinates `y`:

    g(y) = a + B y - (c^T y)y.

Its divergence is

    div(g) = tr(B) - (n+1)c^T y.

Hence its manufactured `q_g` is `c^T y-tr(B)/(n+1)`. For a homogeneous polynomial `p_j` of degree `j`, the degree-`j+1` term of `T_m p_j` is

    (m-j)(c^T y)p_j.

It vanishes at `j=m`; all other terms have degree at most `j`. Therefore `T_m` preserves the complete polynomial space of degree at most `m`, of dimension `binomial(n+m,m)`.

Now let `x=h(y)` be **any polynomial automorphism**, and let `f=h_*g` be the raw polynomial vector field. We do not know or supply `h` or its inverse. A polynomial automorphism over characteristic zero has constant nonzero Jacobian determinant: the chain-rule determinant equation with its polynomial inverse says the determinant is a unit of the polynomial ring. The divergence transformation formula therefore gives

    div_x(f)(h(y)) = div_y(g)(y).

The extra derivative of `log det Dh` is zero. Thus the raw manufactured operators intertwine:

    (T_m^f p) composed with h = T_m^g(p composed with h).

For any `m >= deg(h)`, the original seed functions `1,x_i`, pulled into hidden coordinates, are `1,h_i(y)` of degree at most `m`. Their complete raw cyclic module is consequently finite, of dimension at most `binomial(n+m,m)`. The acquisition algorithm below therefore terminates for that weight with a large enough budget, **without finding h**.

This is a sufficient class, not a necessary characterization. The bound can be exponential in `n` or `m`. No practical general advantage is inferred from this bound. A hidden polynomial automorphism is used only in the proof that a class is admitted; acceptance for any particular raw input comes from the acquired identities, not from assuming this promise.

## 3. Exact raw acquisition and minimality at fixed weight

Start with `V_0=span{1,x_1,...,x_n}`. Repeatedly apply `T_m` to each current basis polynomial and perform exact rational coefficient elimination against the basis. Append every nonzero residual, normalized by one nonzero coefficient. Process newly appended basis elements as well.

Each appended element is independent, because a previously unused pivot monomial survives exact elimination. If the basis exceeds `R`, this is an exact lower bound on the dimension of any `T_m`-invariant polynomial space containing the original seeds. If the queue empties, all basis images lie in the span and produce the exact matrix `A`.

The completed span is the unique smallest such invariant space: any invariant space containing the seeds must contain every generated image and linear combination. This statement is about fixed manufactured weight and polynomial modules; it is not minimality among arbitrary nonlinear encodings or all possible scalar gauges.

The deterministic cost depends on every intermediate polynomial support and coefficient height. A small final dimension does not by itself prove efficient sparse discovery.

## 4. Circuit acquisition without monomial expansion

This section is a proved arithmetic-operation route, now separately implemented in `circuit_jets.py`; the initial exact experiment uses Section 3. Let the raw equations be division-free rational arithmetic circuits with a verified degree bound `d>=1`. Their divergence can be built by circuit automatic differentiation. For each rational sample point `a`, solve only the truncated **formal** initial-value problem

    X'=f(X), X(0)=a;       W'=m q(X)W, W(0)=1.

Using power-series coefficients, the order `k+1` state coefficient is the order `k` coefficient of the right hand side divided by `k+1`. At a multiplication gate, the order `k` coefficient is a convolution of length `k+1`. Thus all jets through order `R+1` use polynomially many rational arithmetic operations in circuit size and `R` (a direct incremental implementation uses quadratic convolution work per gate).

The values of `T_m^k 1(a)` and `T_m^k x_i(a)` are `k!` times the order-`k` coefficients of `W` and `W X_i`. No trajectory integration, numerical derivatives, hidden chart, or monomial expansion is required.

Run finite-dimensional elimination on these evaluation vectors, retaining each basis function as an explicit linear combination of these circuit jets. A nonzero evaluation minor proves actual polynomial independence, without probability. Every proposed closure identity is then checked at **independent fresh** rational points using the same jets. Its degree is at most `D=1+(R+1)(d-1)` when the processed Krylov orders are at most `R+1`. By Schwartz--Zippel, a fixed nonzero residual is zero at `k` independent uniform points from `S^n` with probability at most `(D/|S|)^k`. Condition on training randomness before applying this bound. For multiple adaptive attempts allocate a summable error budget or use a fixed bounded search and a union bound. Exact identity verification can instead be done by coefficient expansion, with that cost paid.

Rank-deficient training sketches can hide true directions. If the original independent seeds lose sampled rank, return INCONCLUSIVE (or retry with fresh points, paying the attempt). If a candidate fails fresh-point verification, return REJECTED, not an invariant module. For a successful-discovery probability bound, use `R+1` independent training points and note that a nonzero evaluation minor for any fixed independent set of at most `R+1` jet polynomials is a nonzero polynomial of total degree at most `(R+1)D` in all point coordinates. Schwartz--Zippel bounds loss of that rank by `(R+1)D/|S|`. A fixed bounded search can budget this separately from the false-acceptance probability. No Las Vegas termination or finite closure promise is presumed.

This is a Monte Carlo output guarantee unless the polynomial identities receive deterministic verification. General deterministic circuit identity testing is not silently assumed. Evaluation and elimination bit complexity is polynomial in the **actual intermediate bit lengths**, not asserted polynomial in circuit description alone: repeated squaring of constants is a simple obstruction to that stronger claim.

The experimental script uses a fixed seeded PRNG for reproducibility. That particular run is not an information-theoretic PIT guarantee against an input chosen after seeing the seed; its optional exact coefficient replay supplies deterministic admission. The stated probability theorem concerns independent random draws, not the pseudorandom implementation as an adversarial guarantee.

## 5. Exact separating example

The test generator starts from

    u'=u-u^2,       v'=7v-uv,

and applies the polynomial automorphism

    x=u+v^2,       y=v+(u+v^2)^2.

Its inverse is `v=y-x^2`, `u=x-(y-x^2)^2`, and its determinant is one. This hidden information is confined to input construction and independent validation; `acquire(raw_f,m,R)` receives only the raw coefficients and budgets.

The resulting raw field has degrees 8 and 9 and respectively 10 and 16 terms (see `results.json`). The compiler derives `q=x-(y-x^2)^2-8/3`. At `m=4` it constructs an exact 13-dimensional module and replays all 13 matrix identities coefficient by coefficient. Weights `0,1,2,3` each generate 17 independent polynomial functions before the test's rank cap; these are lower bounds, not by themselves proofs of infinitude.

For this particular family infinitude for every `m<4` has a separate proof. In hidden coordinates the second original coordinate has a nonzero degree-four homogeneous part `v^4`. For any polynomial of degree `j>m`, the leading-degree action is `(m-j)u p_j`, which is nonzero. Its successive images have strictly increasing degrees and are independent. In particular the ordinary `m=0` state-containing Koopman module is infinite. The weighted method is not simply a faster implementation of the same finite ordinary module.

Twelve independent forward-trajectory checks compare the acquired matrix-ratio formula with the hidden analytic projective flow. The measured maximum absolute difference was about `3.22e-13`. These floating checks are supplementary; algebraic closure was verified exactly.

## 6. Strong conventional alternatives and what is not new

* Carleman/Koopman finite invariant embeddings and Krylov span discovery are standard. Brunton et al., *Koopman Invariant Subspaces and Finite Linear Representations of Nonlinear Dynamical Systems for Control* (2016), explicitly discuss both exact finite closure and its limitations: https://pmc.ncbi.nlm.nih.gov/articles/PMC4769143/ .
* The operator `D+lambda div(f)` is the classical Lie derivative on scalar densities. Polynomial projective vector fields and their density-module representations are longstanding. Lecomte--Ovsienko, *Projectively equivariant symbol calculus* (1998): https://arxiv.org/abs/math/9809061 ; Michel, *Conformally Equivariant Quantization -- a Complete Classification* (2012), Section 3: https://sigma-journal.com/2012/022/sigma12-022.pdf . The present derivation does not claim to invent that representation.
* Darboux-polynomial and inverse-integrating-factor methods also discover exact linearizable structure and can be stronger on other classes. The primary implementation paper *Pegasus: sound continuous invariant generation* explains the nonlinear cofactor-discovery difficulty and existing algorithms: https://link.springer.com/article/10.1007/s10703-020-00355-z . The manufactured divergence cofactor removes that particular unknown only for the admitted projective-density route.
* The stronger acquisition comparator is Cheze--Combot, *Symbolic computations of first integrals for polynomial vector fields* (2017), Theorem 4 and the introduction's strategy: https://www.math.univ-toulouse.fr/~cheze/cheze_combot_symb_first_int.pdf . It already combines formal-flow series at random initial conditions with linear algebra to acquire bounded-degree rational, Darbouxian, Liouvillian, or Riccati first integrals. It includes an explicit inconclusive outcome. Consequently formal-jet discovery itself is not a new primitive here. Its output is a first integral, rather than the present full original-state time-evolution decoder; superiority over the full conventional pipeline is unestablished.
* First-order quasi-exactly-solvable differential operators preserving polynomial spaces are another close structural ancestor; see Turbiner, *Lie-algebras and linear operators with invariant subspaces*: https://arxiv.org/abs/funct-an/9301001 . Eigenvectors of the manufactured operator are Darboux polynomials with a shared nonconstant cofactor component.
* A conventional symbolic algebra system, supplied the same acquired module, can use the identical matrix-ratio solution. No same-input speed superiority over the strongest symbolic/projective-recognition solver has been established.

Historical priority of the complete raw-acquisition combination is **unknown**. Its substantive current result is a checked dictionary-free acquisition route strictly beyond ordinary finite state-containing Koopman closure, with an explicit class guaranteed by existing projective machinery. It is not yet the user's civilization-level foundational theory.

Recorded sparse timings are core queue/elimination timings after construction of q; circuit core timings start after construction of the raw/AD circuit and q. They are not end-to-end parsing-to-output benchmarks. The current compact example does not demonstrate a speed advantage: exact sparse discovery is faster than the circuit sketch, whose purpose is to remove the monomial-expansion requirement. Circuit output contains its own basis combinations, operator matrix and original-seed reconstruction map; those can be ill-conditioned numerically. Bit-size and high-precision decoding costs remain real.

## Astra source handling

Read `00_START_HERE.txt` and the computational-algebra/representation-acquisition route files at commit `95c99ce592a48d4505dd4bfcc0925d7ebad0efdd`. Read packets N1209, N1217, N1223 and the full governing native final for N1223 at `research/2026-10-29-memory-information-and-model-receivers/source/finals/P3_NATIVE_FINAL.md`. Those emphasize paid acquisition and intermediate representations. Their unavailable producer proof/code originals were not requested or imported. No Astra theorem is used as a mathematical premise of this construction.
