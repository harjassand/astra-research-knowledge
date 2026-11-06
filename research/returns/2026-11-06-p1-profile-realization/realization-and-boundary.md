# Realization requires more than positivity

These are the [complete return's unreviewed claims](P1_PROFILE_REALIZATION_20261106_COMPLETE_RETURN.txt), with the [supplied manuscript](package/maximal_profile_geometry_and_realization.pdf) now archived. Capital performed no new proof check. Supplied channels `Φ_j: M_a→M_(b_j)` have explicit rational-complex Choi matrices, and rational signed coefficients obey `Σc_j=1`.

On the effective output support, set `Ω_j=Φ_j(I_a)` and `T_j(X)=Ω_j^(−1/2)Φ_j(X)Ω_j^(−1/2)`. The generated algebra is `A=C*(⊕_j T_j(M_a))`, with state functionals `τ_j(A)=Tr[Ω_j π_j(A)]/a` and `ell_c=Σc_j τ_j`. These are generally **nontracial**: ordered real and imaginary moments must be preserved.

The claimed criterion is `ell_c≥0` and `N_c={A:ell_c(A* A)=0}` a **two-sided ideal**. Equivalently, the density `Z_c` for `ell_c(A)=Tr(Z_c A)/a` is positive and its actual support projection is central. Replacing actual support by its central carrier would erase the relevant obstruction.

Two finite negative certificates are distinguished. A negative norm `ell_c(P*P)<0` defeats positivity. A null-ideal failure has `ell_c(P*P)=0` but `ell_c[(P T(H))*P T(H)]>0`. A hypothetical normalized channel has a state faithful on its actual output support, forcing a zero represented operator to stay zero under multiplication. This yields the claimed contradiction in **every finite output dimension**, rather than failure of one selected parametrization. A positive GNS construction alone is insufficient.

When positivity and central support hold, the conceptual channel `Γ(X)=Z_c^(1/2)T(X)Z_c^(1/2)` on that support reproduces ordered moments and the target profile. Standard finite-algebra/faithfulness machinery is credited, rather than invented anew. The executable construction removes conceptual irrational roots.

## Rational coordinates and compiler output

The implementation uses `barΦ=⊕Φ_j`, `barΩ=⊕Ω_j` and the rational product `B star C=B barΩ⁺ C`. Algebra closure, Gram positivity, null-space and right-ideal tests use exact arithmetic. It constructs positive rational `K` and a rectangular rational factor `C* C=K`, then returns `Γ(X)=C barΦ(X)C*`.

Binary decomposition of a positive rational pivot into rational squares gives polynomially many factor rows in its bit length, without a factoring or irrational-root oracle. A square rational Cholesky factor is not required. Floating-point inputs are rejected. Polynomial bit complexity in dense explicit Choi input can still mean exponential cost in qubit count and substantial intermediate rational heights. The earlier bounded-environment four-square compiler and corrected N1698 binary-square/canonical compiler have their own contracts; no earlier missing witness-generation bound is silently imported.

## Three-way qubit example

For the source's `κ=1/4` normalized map and two rational channels `Γ_0, Γ_(3/5)`, the formal profile coefficients are `1−5s/3, 5s/3`:

| Parameter | Exact source-reported outcome |
|---|---|
| `s=4/5`, coefficients `−1/3,4/3` | Physical signed extrapolation exists |
| `s=1`, coefficients `−2/3,5/3` | Positive functional, noncentral support: no finite-dimensional realizing channel |
| `s=6/5`, coefficients `−1,2` | Negative-norm obstruction |

Every channel in the open family has the same reference-free maximal profile for every operator-convex generator, while complete profiles differ in an ordered imaginary moment exposed by a reference. This is an example-specific separation, not an assertion that reference-free tests always fail.

As `s→1`, the actual channels approach a pure-output replacer, which exists. Their **formal affine endpoint profile** is the nonphysical object. The source's displayed quadratic-divergence query tends to `1/64`, while that query's replacer value is `0`. A replacer retains the untouched reference's information, so its complete profile is not generally zero. No historical-priority claim for maximal-divergence discontinuity is made.

Within the fixed supplied affine span, physical profiles are convex and need not be closed; the closure is the positive-functional slice in finite moment/query coordinates, with pointwise convergence for each fixed query, not uniform convergence over all queries. Commutative algebras remove this noncentral-support obstruction. Minimum complex dimension is the sum of active simple-component sizes, using prior N1698 machinery; rational compilation may enlarge output. The example's automatic rational output is dimension 14 while an explicit dimension-two realization exists. No polynomial minimum-rational-dimension guarantee is added.

[Witness/query and implementation costs](witnesses-queries-and-costs.md) · [Overview](README.md)
