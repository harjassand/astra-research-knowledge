# Independent adversarial audit

## Outcome

**PASS at the proved algebraic scope.** The core raw-vector-field construction is sound: manufacture `q=-div(f)/(n+1)`, acquire the smallest polynomial module containing the original coordinate seeds under `T_m=D+m q`, and reconstruct the original state by ratios of a constant-matrix exponential. No hidden conjugacy is needed by the acquisition algorithm.

This is not a novelty certification, a generic nonlinear solver, an efficiency claim in raw description length alone, or a physical/scientific application validation. Projective density representations, quasi-exactly-solvable first-order operators, Darboux methods, and Krylov closure are substantive classical ancestors.

## Mathematical checks

1. **Correct sign and decoder.** If `T_m phi=A phi`, then multiplying `phi(x(t))` by `exp(m integral q)` gives `z'=Az`. Since the first seed is one, dividing the coordinate-seed entries by the first entry recovers each original coordinate. The denominator equals a nonzero exponential on every finite actual real trajectory. The proof correctly restricts the ratio formula to its connected nonsingular interval and does not assert cost-free numerical evaluation.
2. **Correct polynomial-automorphism covariance.** A polynomial automorphism has constant nonzero Jacobian determinant because its determinant and the composed determinant of its polynomial inverse multiply to one in a polynomial ring. The extra divergence-transform term vanishes. This does not invoke or assume the Jacobian conjecture.
3. **Correct hidden-class guarantee.** For a projective vector field `a+B y-(c^T y)y`, the only degree-raising term on a homogeneous degree-`j` polynomial is `(m-j)(c^T y)p_j`. Consequently the degree-at-most-`m` space is invariant. Pulling back raw coordinate seeds through an unknown polynomial automorphism of degree at most `m` places them in this space. The finite-dimensional guarantee follows without supplying the automorphism to acquisition.
4. **Correct fixed-weight minimality.** Exact span closure from seeds produces the unique smallest invariant polynomial span. An appended pivot is an exact independence witness. This is not minimality among other gauges or arbitrary nonlinear decoders.
5. **Correct separation.** In the test, the second original coordinate pulls back to a polynomial with top homogeneous term `v^4`. For `m<4`, repeated application has nonzero top terms of strictly increasing degree, proportional to `u^k v^4`. Thus all four lower-weight modules are infinite, not merely larger than the tested budget. Ordinary state-containing finite Koopman closure really is impossible on this example.
6. **Correct weighted formal jets.** The auxiliary ODE `W'=m q(X) W` gives derivatives of `W p(X)` equal to powers of `T_m p`. Circuit convolution can evaluate these jets without multivariate coefficient expansion.

## Independent executable checks

`independent_replay.py` uses fresh SymPy polynomial arithmetic; it does not import the producer's sparse operations. It verifies:

- all **13** output module identities exactly;
- exact coefficient-matrix rank **13** of the output basis;
- both hidden pushforward identities;
- the raw divergence-derived identity `q=x-(y-x^2)^2-8/3`;
- divergence covariance under the supplied test-only hidden map.

`independent_results.json` records source hashes for this replay. `jet_replay.py` checks **72** weighted circuit-jet values against independently differentiated symbolic polynomials, for weights 0, 1, and 4 and orders 0 through 7. `circuit_jet_checks.json` records the checks. `exact_spectrum.json` records 13 distinct rational eigenvalues of the acquired sparse matrix, confirming diagonalizability for this example only.

## Issues found and resolution status

- **Fixed:** the initial implementation appeared generic in `n` but hard-coded the two-variable seed basis. The producer added explicit two-variable validation and scoped the proof's implementation statement accordingly.
- **Fixed:** a rank budget below the original seed dimension could previously return closure above budget. The early exact lower-bound guard now handles this; independently checked on zero dynamics with budget two.
- **Fixed in the proof:** sampled rank loss needed an explicit inconclusive/rejected branch rather than silently implying every training sketch succeeds. The revised Section 4 separates successful-discovery rank-minor probability from false-acceptance PIT probability.
- **Fixed and independently replayed:** the first circuit-route success result returned only residuals/metadata, discarding its acquired basis, operator rows, and seed-reconstruction rows. The revised output serializes all three. `circuit_output_replay.py` independently verifies all **13** serialized module identities and **3** seed reconstruction identities by fresh SymPy coefficient arithmetic. `circuit_output_replay.json` records the result and source hashes. The producer also tested this circuit-derived decoder at 180 decimal digits; that numerical check is supplemental, not the identity certificate.
- **Reporting caveat:** `peak_jet_bits` is only a jet-value metric, not the potentially larger elimination-coefficient height. The proof retains all actual bit costs, which is correct.
- **Reporting caveat:** original `seconds` values exclude parsing, manufacture of `q`, and some outputs. They are core timings, not end-to-end benchmarks.
- **Randomness caveat:** the experiment uses a fixed seeded pseudorandom generator for reproducibility. The information-theoretic Schwartz--Zippel statement applies to independently uniformly sampled values in the mathematical algorithm. The example's later deterministic coefficient replay removes this issue for its accepted identities; do not treat a seeded, adversarially known sketch alone as a universal probabilistic certificate.

## Strong conventional comparators

**Chèze--Combot, Symbolic computations of first integrals for polynomial vector fields (2017)** already uses formal flow series at random initial conditions and linear algebra to acquire bounded-degree rational, Darbouxian, Liouvillian, and Riccati first integrals. Theorem 4 explicitly allows an `I don't know` outcome at bad initial values, and Section 5's introductory strategy explains the jet acquisition. Their output is not the same full original-state time decoder, but this is materially closer than comparison only to generic EDMD or monomial Carleman truncation. Primary source: https://www.math.univ-toulouse.fr/~cheze/cheze_combot_symb_first_int.pdf .

**Turbiner, Lie-algebras and linear operators with invariant subspaces (1994; arXiv revision 1998)** treats polynomial finite-dimensional invariant spaces of differential operators through finite-dimensional Lie representations and quasi-exact solvability. The present `T_m` belongs directly to this classical family of first-order operators. Primary source: https://arxiv.org/abs/funct-an/9301001 .

There is also a direct Darboux interpretation: a left eigenvector of the acquired matrix gives a polynomial `p` satisfying `Dp=(lambda-mq)p`. Thus the eigenfunctions have a common nonconstant cofactor part; Jordan blocks give the corresponding generalized chains. The divergence prescription removes cofactor search only for this selected route. This interpretation prevents presenting the construction as a wholly new representation theory.

## Final scope

The accepted contribution is a concrete, checked acquisition construction with a nontrivial admission theorem beyond ordinary finite state-containing Koopman closure. The audit found no gap in that theorem. Historical priority, superiority over strong symbolic integration algorithms, practical scientific scaling, and a foundational civilization-level breakthrough remain **unestablished**.

## Added audit: acquired small chart and its inverse

The later `acquired_projective_chart.py` changes the seed to **one alone** and uses `T_1`. Its success path requires a closed `(n+1)`-dimensional cyclic span, takes the nonconstant basis functions as a candidate chart, and actually constructs and verifies its global polynomial inverse. The two inverse compositions are checked exactly; a nonzero Jacobian is not substituted for invertibility.

The sufficient hidden-class theorem needs an extra, visible **cyclicity/observability condition**: the projective denominator coordinate must be cyclic for the hidden `(n+1)`-dimensional linear representation. Then `T_1^k 1` spans all hidden affine functions. The acquired chart is an invertible affine transform of `h^{-1}`, and its inverse exists polynomially. Without this cyclicity, the one-seed route may miss coordinates, even though the earlier weighted original-state route succeeds. It is not a complete solver for all projectively conjugate systems.

Independent checks in `chart_replay.json` verify all **3** acquired operator identities and **4** global inverse component identities. Two adversarial controls were run:

- `f=(x-x^2,(2-4x)y)` has a closed rank-three cyclic-one module consisting of functions of `x` alone. It is **not** a two-coordinate chart. The code correctly rejects it as `SINGULAR_BASEPOINT`.
- `C=(x+x^2,y)` has identity Jacobian at zero but no polynomial inverse. Degree-one, -two, and -four formal inverse candidates all fail the exact global identities, and the code reports `INVERSE_NOT_ACQUIRED`.

**Fixed:** the initial doubling loop did not test a non-power-of-two final cap such as three. The producer changed the last stage to test the exact final cap. The regression `C=(x+y^3,y)`, `max_degree=3`, now tests stages 1, 2, 3 and acquires the degree-three inverse. This was a completeness-of-budget edge, not an unsound positive result.

**Resource comparison:** under cyclicity, the linear evolution dimension drops from the possible `binomial(n+m,m)` symmetric-power module to `n+1`. But this shifts work into chart inversion, whose degree, support, composition expansions, coefficients, and verification costs remain payable. The current inverse routine explicitly expands multivariate polynomials. The old 13-dimensional result and new 3-dimensional chart result use different raw vector fields and are not a matched numerical comparison. A same-input comparison must use `chart_results.json` for both routes; `same_input_dimension_comparison.json` records that check. Timing fields are not end-to-end matched and should not be used as a speed ratio.

An optional classical finite search ceiling is `deg(C^{-1}) <= deg(C)^(n-1)` **if C is a polynomial automorphism**. This can bound a complete inverse-recognition search but can be enormous and is not a certificate that C is invertible. Primary source: *Degree bounds of minimal polynomials and polynomial automorphisms*, JPAA 92 (1994), https://www.sciencedirect.com/science/article/pii/0022404994900256 .

## Added audit: asymptotic representation separation

The separation in `ACQUIRED_CHART_THEOREM.md` is **accepted as stated**, not extrapolated from the numerical examples.

Let `b=e+1`, `lambda_j=b^(j-1)`, and use the displayed upper-triangular homogeneous matrix with top row `(0,1,...,1)`. Its eigenlinear forms are `ell_0=Z_0-sum Z_j/lambda_j` and `ell_j=Z_j`. Thus `Z_0=ell_0+sum ell_j/lambda_j` has nonzero components on all `n+1` distinct eigenspaces. The cyclic-one chart has dimension `n+1`.

For the displayed degree-`e` shear, the top homogeneous part of `h_n` is nonzero of degree `e`. At every weight `m<e`, each application of `T_m` raises its degree by one with nonzero coefficient. No finite original-state-containing module can exist.

At `m=e`, homogenizing the seed one gives `Z_0^e`, whose expansion has a nonzero coefficient at every degree-`e` eigenform monomial. Their eigenvalues `sum alpha_j (e+1)^(j-1)` are distinct by uniqueness of base-`e+1` digits in `0,...,e`. A vector supported on `K` distinct eigenspaces has cyclic dimension `K` by the Vandermonde determinant, giving exactly `K=binomial(n+e,e)`.

At `m>e`, pad any exponent tuple from degree `e` only in its `ell_0` exponent. This embeds the former eigenvalue support into the new support. Collisions elsewhere cannot cancel it because every coefficient in the `Z_0^m` eigenform expansion is positive. Hence all finite original-state integer-density lifts have dimension at least the degree-`e` value. The proof uses no unproved assumption about spectral genericity.

The raw shear pushforward admits a circuit polynomial in `n` and `log e`; its maximum degree is at most `2e`, and the coefficients `lambda_j` have polynomial binary length in `n log(e+1)`. For `e=n`, the density-module dimension is `binomial(2n,n)` whereas the projective linear coordinate count is `n+1`. Polynomial-size circuit formal inversion to degree `e` is a valid proof-level construction using shared truncated-series DAGs; coefficient expansion is not needed for that circuit-size statement. It remains distinct from the current expanded-polynomial inverse implementation, and deterministic circuit identity testing is not assumed.

The result is a genuine exponential **representation-class** separation. It does not prove an exponential algorithmic advantage over classical projective recognition, Darboux integration, or any algorithm permitted to use a nonlinear decoder. The hidden sufficient class and cyclicity are checked or certified through actual acquired identities on accepted inputs; they do not turn arbitrary nonlinear systems into members of the class.
