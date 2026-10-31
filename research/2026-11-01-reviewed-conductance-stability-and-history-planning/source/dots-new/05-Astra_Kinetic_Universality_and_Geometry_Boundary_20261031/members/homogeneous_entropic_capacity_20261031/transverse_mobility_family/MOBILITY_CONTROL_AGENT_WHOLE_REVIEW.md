# Independent whole review: unidentified transverse mobility

## Verdict and immutable scope

**PASS** for the exact attainable-range theorem and the separately declared universal-family receiver. No defect requiring a source change was found. The result concerns the actual conservative reversible diffusion for every fixed finite constant SPD transverse matrix, with unit longitudinal mobility and zero cross mobility. It does not authenticate a particular physical process from its potential, numerically evaluate the exact lower endpoint, or construct a realizing matrix.

I read both full mathematical candidates, the complete receiver and author test source, README, costs, executed-result and dependency records. The underlying quartic and finite-Jensen proof/code interfaces were previously whole-reviewed and have been rehashed. Current bindings:

- `FROZEN_SHA256.txt`: `44bc44842a8c3c69f9145248603f68331308989434b464e304663ecfb5b3abed`.
- `EXACT_MOBILITY_RANGE_CANDIDATE.md`: `ff8b132c42a37567f832a397ee53b64e7a34b3aabad39fe55aa327181ccd52c9`.
- `MOBILITY_FAMILY_CANDIDATE.md`: `833c715329f6692d69bba7cbd0cc410f9c6903b17bfbce42121248fe941f01fe`.
- `receive_family.py`: `34b3769394667a1e2761e23cd975281f7de5196da4094be1e35a6d2200dd7d1f`.
- `check_family.py`: `fb59e4f53e6a29204ea5aca90f3ebce920e168b49c230799ed5501ea52db7e69`.
- `family_513D_certificate.json`: `fe8e5006fc794259aaa11fad5c1c7f4dfd1eb71f9aeef1a0b2436e8914f9ca3c`.
- `check_results.json`: `09225d856a1775dafb04d70c95a0f4bcb39e1606ecb8ea7b34c3252221d3b4fa`.
- `COSTS_AND_SCOPE.md`: `65928a37cfacb8b2d736deb9d7a5668df1b66f7007defa4d45341e76b28543f4`.
- `DEPENDENCIES.json`: `fff3743a4653e7a066f2c657f7b1b2dfab4f0c0098abf9d4043b3e30368adf56`.

All ten frozen source entries and nine dependency entries were verified unchanged. In particular the finite engine is430d5e82...b00769 with whole receipt02553441...7178af, and its raw engine45d75db5...03fbf and whole receipt04736659...97a6e are unchanged. Candidate/pending headers are immutable historical source text; this separate receipt records the later whole acceptance. Neither the cross-mobility team's construction nor other extensions are included by this review.

## 1. Global process for each member, not uniform dynamics identification

For every fixed finite SPD M, the block diffusion matrix diag(1,M) is uniformly positive as a constant matrix, though its constants may depend on M. The stated drift is exactly minus this matrix times grad F and the covariance is twice it divided by beta. This earns reversible Gibbs density independently of M. The known homogeneous scaling makes the density finite under4m>p.

The analytical Lyapunov function V_M=1+y^2+(1+kappa/p)z^T M^-1 z is coercive for each fixed M. Its generator is

    -2[yv'+(p+kappa)v]U + 2[1+(1+kappa/p)m]/beta.

The first bracket is at least p because yv'>=-kappa and v>=1. Thus the generator is bounded above by the displayed finite constant, and the stopped Lyapunov argument rules out explosion. Polynomial drift is locally Lipschitz. The same constant M in drift and noise gives the conservative symmetric Dirichlet form with invariant probability mu.

This proof does not use a uniform lower eigenvalue over the quantified family or compute M^-1. As matrices become nearly singular or large, equivalence of V_M to Euclidean norm may degenerate; no uniform finite-time relaxation estimate is inferred. Exactly singular, variable, cross-coupled or nonreversible mobility is outside this statement.

## 2. Global weighted H1 minimizer and boundary closure

The proposed global H1(mu) is a Hilbert space: smooth positive density bounds above and below on every compact set identify local weak derivatives with ordinary distributional derivatives, and their graph is closed. Its bounded constraint0<=h<=1 and the values1 on A,0 on B are closed convex L2 constraints. They therefore remain weakly closed in H1. A scalar smooth transition is a finite-energy competitor.

For fixed M, the energy controls all derivatives by a positive M-dependent constant. A bounded-energy minimizing sequence in the constrained class also has L2 norm<=1 since mu is a probability. Weak Hilbert subsequences exist; weak lower semicontinuity of the constant positive quadratic derivative form produces a minimizer. No compact Sobolev embedding or conditional spectral gap is being used.

The global H1 class supplies the matching boundary traces. On any compact transverse set, it is ordinary H1 near y=+/-1/2; being constant on the open basin side fixes the plane trace from the slab side. A discontinuous jump across that plane is not admitted. Almost-everywhere basin constraints and this local trace property give the usual Dirichlet condenser boundary condition. The standard smooth-core/weighted Sobolev Dirichlet realization is legitimate here: cutoffs and local smoothing apply to the smooth positive weight, and bounded basin-valued functions have finite L2 mass. There is no artificial transverse boundary at infinity.

For clarity in the later strictness argument: truncation to[0,1] does not increase the energy and preserves the basin values. Therefore the constrained minimizer is also a minimizer over the entire affine H1 class with those boundary values, not merely an obstacle-problem solution. Arbitrary compactly supported interior variations give its weak Euler–Lagrange equation. Local elliptic regularity then gives a smooth solution in the open slab. Strict convexity modulo constants, connectedness and the fixed boundary values yield uniqueness.

## 3. Low-mobility endpoint and finite trial energy

For any admissible h, dropping the nonnegative transverse quadratic energy and applying fiberwise weighted Cauchy proves cap_M>=cap_parallel. The scalar trial gives cap_M<=cap_free. These depend on the full-fiber boundary condition; they are not a statement that projected paths are Markov.

The proposed h_parallel is the normalized integral of exp(beta v(s)U(z)) from y to b. Differentiating in y gives its exact longitudinal energy cap_parallel. The normalization and reciprocal directions agree with the accepted parallel theorem.

Differentiating with respect to U gives beta times the covariance of a bounded interval indicator with v under that normalized interval law. Its absolute value is bounded by beta times the slab oscillation of v. Consequently its transverse derivative is bounded by that constant times the polynomial grad U. Coercivity and the slab's positive v_min make the squared derivative integrable under exp(-beta v_min U). Its longitudinal derivative has already been shown square-integrable by the finite parallel energy. The bounded function extends with values1/0 outside and matching traces, so it is indeed in global H1(mu).

For every fixed SPD shape B it follows that

    E_(gamma B)(h_parallel)=cap_parallel+gamma C_B,

with finite C_B. This proves convergence down to cap_parallel as gamma decreases to zero. C_B can depend on uncomputed angular moments and B. The proof is an existence/limit argument, not an acquired convergence modulus or a solver selecting gamma from a requested accuracy.

## 4. High-mobility endpoint without angular mixing

For gamma_n tending to infinity, the minimizers have longitudinal energy bounded by cap_free and transverse Euclidean gradient norm squared bounded by beta cap_free/[gamma_n lambda_min(B)]. For gamma_n>=1 they form a bounded global H1 sequence. A weak subsequential limit remains in the closed constrained class. The transverse gradients converge strongly to zero, hence the limit has zero transverse distributional derivative.

Because the weight is positive on compacts, vanishing weighted derivative implies vanishing ordinary local distributional derivative. Connected fibers R^m imply h(y,z)=g(y) almost everywhere. No mass-escape assertion or conditional Poincare inequality is needed: L2 boundedness, weak Hilbert compactness and closed basin constraints are sufficient. The limit inherits the basin values and has finite scalar weighted derivative energy.

Weak lower semicontinuity of the longitudinal part then bounds liminf cap_(gamma_n B) below by the scalar minimum cap_free. The reverse bound holds for every n. Applied to arbitrary divergent sequences (and a subsequence realizing any putative smaller liminf), this proves convergence to cap_free. It does not establish convergence of sample paths, a fast-equilibration timescale, or a finite-gamma approximation algorithm.

## 5. Strict endpoints, continuity and attainable set

A fiber-constant finite-M minimizer would be a smooth g(y) satisfying

    beta^-1 g''(y)-v'(y)U(z)g'(y)=0

throughout the open slab. At z=0, homogeneity gives U=0, hence g''=0. At a point with U>0 and y other than0, v' is nonzero, hence g'=0. Smoothness then contradicts the unit boundary drop. This argument uses the unconstrained interior Euler–Lagrange property justified above, not an unsupported variation through an active box constraint.

Thus every finite-M minimizer has strictly positive transverse energy. Its longitudinal energy is at least cap_parallel, so cap_M>cap_parallel. Equality with cap_free would make the scalar trial itself a minimizer, contradicting the same fact; hence cap_M<cap_free.

For gamma2>gamma1, using the gamma2 minimizer as a trial at gamma1 subtracts a strictly positive transverse-energy term. This proves strict monotonicity. The capacity is an infimum of affine functions of gamma, therefore concave; being finite on the open positive axis it is continuous there. Together with the two limits, every fixed shape path gamma B spans exactly the same open interval. All SPD matrices lie strictly between the endpoints, while any one shape path attains every interior rate. Dividing by common positive mu(A) gives the claimed exact family range.

The homogeneous pushforward and accepted parallel formula make both endpoints independent of angular U at fixed m,p,kappa,beta. This is not equality of rates at a particular M. For m>=2, nonproportional shapes can each be scaled to an interior rate, so a conductance value alone does not identify matrix shape. If U and B are both fixed, strict monotonicity instead gives a unique gamma. Neither claim computes that gamma. The family characterization is not a constructive inverse-mobility algorithm.

## 6. Exact family-scoped executable

At import the code hashes BOTH the frozen range proof and the finite-Jensen module; that module in turn hashes the raw arithmetic engine. The new source then actually reruns raw acquisition and the entire finite-Jensen computation from original coefficients and the external task.

It accepts only the exact string `all_fixed_transverse_SPD`. An actual M, cross covariance, changed longitudinal mobility, alternative family or control argument is not silently interpreted; unsupported arguments are rejected. Fresh nested family and range descriptors prevent a caller-mutated returned record from altering future expected semantics.

The new schema, method, observable, numerical-scope field and `uniform_rate_enclosure` explicitly differ from isotropic output. The exact open interval is characterized symbolically; flags state its lower endpoint was not numerically evaluated and no realizing matrix was constructed. The numerical answer is the SAME closed finite-Jensen OUTER enclosure, which contains every member; it is not the exact open range endpoints. Numerical values inside that outer enclosure need not all be attainable.

The verifier recomputes the result and recursively binds all family/range descriptors, exact proof/module hashes, task and requested total width, acquired raw model, basins, numerical cutoff/grid/precision/tail and all six interval endpoints. False versus0 and other bool/integer/float aliases are distinguished. Stale `full_rate` and `factor_upper` scope fields are rejected. Optional timing/display/work diagnostics and arbitrary extra prose are not authenticated by PASS; the actual physical membership exclusion remains explicitly bound.

No matrix entries, inversion or eigensolver are executed because the input is a quantified family task. For a specific physical system, verifying that its drift/noise really have this structure is an additional unearned task. All raw polynomial scanning, coercivity, full identity, unbounded-tail arithmetic, repeated quadrature and inherited unused radial-factor costs remain paid. A tight requested full width can still cause UNKNOWN due to finite resolution or intrinsic Jensen slack.

## 7. Independent executions and artifact preservation

All execution occurred in `producer-workspace/mobility_review_20261031` with copied theorem/module/dependency files. The full author suite passed **846 assertions**, including an ACTUAL fresh recomputation of the513D family certificate. The regenerated author result is byte-identical to the frozen report.

An additional **137 exact checks** passed:

- every family/range/task/acquisition leaf tampered, including nested integer/bool/float aliases;
- missing scope fields, all interval endpoints, stale isotropic/radial records;
- unsupported family, actual matrix/control/mobility arguments, external task and raw-model substitutions;
- fresh descriptor isolation, same enclosure but distinct raw acquisition records;
- fifteen exact off-diagonal, possibly ill-conditioned3D SPD Lyapunov/inverse cancellations;
- an actual proof-hash import rejection after changing ONLY the temporary copied proof, then restoring it.

Dedicated artifacts, with no reused earlier reviewer filenames:

- `audit_control_agent_20261031_1954/check_control_audit.py`: `4136c65ab84bb432fead01073796fbf8f82403d96bdaf3ff9e582131577fa601`;
- `audit_control_agent_20261031_1954/independent_control_results.json`: `edd1e90279434f2f013bc973e104c55887e7c8c142941717d27a0925ffad4f94`;
- `audit_control_agent_20261031_1954/author_replay_results.json`: `09225d856a1775dafb04d70c95a0f4bcb39e1606ecb8ea7b34c3252221d3b4fa`.

The independent test's proof-tamper operation asserts a `/tmp` path. Reproduce in a temporary copy with the documented sibling layout, not next to original proof files. Finite checks do not substitute for the infinite-dimensional minimizer/limit proof reviewed above.

## 8. Consequence and boundaries

The513D raw fixture retains its finite exact closed enclosure displaying approximately[2.369045057852262e-37,2.384988210037886e-37], ratio1.0067297800574877<1.01. It pays3,069 expanded monomial reads,131,074 scalar evaluations and real bigint/root work. The unchanged outer enclosure now has a separately earned universally quantified model-family meaning. It is not an improved numerical endpoint or a free matrix-identification service.

This supplies conditional information reduction: under the exact block/FDT model, hidden transverse shape, scale and condition number need not be reconstructed to bound this equilibrium full-fiber observable. A target outside the certified enclosure cannot be repaired by choosing another matrix in that family. It does not validate experimental data, establish arbitrary-start kinetics, recover source dynamics, or authenticate the physical interface from F alone.

Dirichlet/Rayleigh monotonicity, weak Hilbert compactness, local elliptic regularity, homogeneous scaling and concavity are ordinary tools. An ordinary implementation equipped with this proof obtains the same output. No historical-priority or broad practical superiority claim is accepted. Cross mobility, variable/singular matrices, altered longitudinal mobility, nonreversible drift, time-dependent controls, other basins and arbitrary nonhomogeneous potentials remain excluded. The separate cross-mobility construction is not duplicated or received here.

**Conclusion:** the exact open-range theorem, global-process premises and fully scoped numerical family receiving are coherent and source-bound. All original frozen files and dependencies remain unchanged.
