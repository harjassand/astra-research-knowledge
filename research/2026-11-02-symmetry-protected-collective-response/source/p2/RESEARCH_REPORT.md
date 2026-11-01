# Astra — A symmetry-protected route to collective dynamical response

**Scientific decision:** concentrate on *orbit-averaged Green–Kubo response* for reversible, strongly cooperative, kinetically heterogeneous systems. This replaces interaction-word enumeration by a physical symmetry quotient plus a nonperturbative quadratic error bound. It is an earned conditional computational regime, not a general solution of interacting dynamics, experimental demonstration, or historical-priority finding.

## Why this question matters

Material and chemical networks often contain many exchangeable subunits but heterogeneous local activity. Their stationary thermodynamics can be simple while relaxation and fluctuation response is not: the heterogeneity destroys exact collective Markov closure. Full configurations require exponentially many states, and at phase coexistence ordinary trajectory simulation must wait through long metastable periods. The desired object is the **actual integrated equilibrium correlation** of a collective observable, not the wait for a rare target that can already be addressed by target-start methods.

The question is whether a **small number of collective coordinates can acquire the response of every actual microstate** with a rigorous error and work budget, without a slow-manifold or tensor-rank premise.

## The central construction

Given a reversible Markov generator `K`, average it over a **physical** permutation symmetry of its equilibrium law to obtain `K0`. If the original and averaged generators differ by at most a relative Dirichlet-form contrast `rho<1`, all centered, symmetry-invariant observables satisfy

```
chi(K0) <= chi(K) <= chi(K0)/(1-rho**2)
```

The lower bound and the quadratic upper bound are proved in `THEOREM_AND_PROOF.md`, including all exponentially many microscopic modes. The proof explicitly uses `P(K-K0)P=0` and the scalar spectral measure of the normalized inverse. It does not approximate `K` by a low-order perturbation. The constant is sharp: two independent unequal-rate sites exactly saturate the upper ratio.

For an assembly of `n` binary sites in `r` genuinely interacting modules, supply **any** complete integer Gibbs table `H(k1,...,kr)` and per-site positive reversible clock multipliers. The averaged generator is exactly lumpable to `D=prod(n_g+1)` count states. For `r` fixed this is polynomial in population size despite `2**n` microscopic states. The response of *actual* heterogeneous clocks is enclosed by the computed quotient response and the acquired clock contrast.

Nested splitting of kinetic classes creates monotone all-order lower bounds; each upper bound uses the residual within-class contrast. This is not a low-order moment or an assumption that a population average is Markov.

## Executable discriminating tests

All results below are mathematical-model quantities; no experimental clock or energy parameters were inferred.

### 1,024 distinct-clock, strongly cooperative population

- `n=1024`, Gibbs weight per microstate `2**H_k`, with `H_k=2*floor((2*k-n)**2/n)`. This forms an explicitly specified two-well collective energy landscape.
- Every site has a distinct rational clock `nu_i=1+(2*i-(n-1))/(20*(n-1))`, so the **mean clock is exactly one** and the largest relative deviation is `rho=1/20`.
- The full model has `2**1024` configurations and its total occupancy is **not Markov**.
- Positive birth–death currents plus directed integer divisions acquire the mean-clock response as an exact rational decimal interval with `p=30`; the disorder theorem then gives

```
3.7146990963296473e316 <= chi_M <= 3.7240091191274660e316
relative interval width: 0.002506265664160401 (0.2506266%)
```

The complete integer bounds, without decimal truncation, appear in `tests.json`. The prototype recorded about 0.05 seconds of integer-arithmetic kernel time in this container; this is a test observation, not a cross-platform performance claim. Input construction, Python launch and source verification are outside that kernel timing.

The **consequential operation** is the gap-independent, relative response interval under extensive kinetic disorder. The enormous time scale is only a numerical stress test.

### Full microscopic comparisons

| Case | True microstate response | Symmetrized response | Theorem upper | Outcome |
|---|---:|---:|---:|---|
| 8 binary sites, collective magnetization, 20% rate deviation | 415.468007 | 408.425602 | 425.443336 | contains actual |
| 10 sites, squared magnetization source, 20% rate deviation | 2938.795718 | 2899.861345 | 3020.688901 | contains actual |
| 8 sites in two interacting modules, collective difference, max 21.05% deviation | 3348.270742 | 3280.727298 | 3432.876970 | contains actual |

All microstate values use independently built full reversible generators and sparse Poisson solves. They are floating-point checks; the general theorem supplies the rigorous bound.

### Progressive, all-order rate refinement

With 12 sites and 12 distinct rates from 0.5 to 1.5, refine from one group to 2, 4 and 6 groups. The exact full model has 4096 states and response `1483.16925946`.

| Kinetic groups | Quotient states | All-order lower | All-order upper |
|---|---:|---:|---:|
| 1 | 13 | 1330.5462 | 1774.0616 |
| 2 | 49 | 1432.8104 | 1587.8765 |
| 4 | 256 | 1470.0951 | 1505.7338 |
| 6 | 729 | 1478.1145 | 1488.4509 |

This is not a truncated series: each quotient includes every kinetic process consistent with its group symmetry. The clock-heterogeneous full process lies within each interval. The lower bounds improve monotonically under nested refinements.

### Finite-bit work and a numerical failure

For one group the exact solution is a **sum of positive integer-rational edge-current terms**, using `n` divisions. No floating-point eigenvalue or condition-number assumption is needed. For multiple groups, the code builds a rational *a posteriori* certificate from a proposed Poisson potential, its exact residual, and a spanning-tree Poincare constant acquired from the reduced graph. The 8-site two-module test achieved a rational relative certificate width around `7.16e-27` for the quotient; the full-heterogeneity interval is much wider because of the actual rates.

An instructive failure: for a 40-site stronger two-well test, a standard double-precision augmented Poisson solve gave a relative error `-5.27e-6` against the directed integer formula, even though its residual norm was about `0.0109`. A small **unscaled** residual is not a useful inverse-error guarantee when the slow eigenvalue is extremely small. The exact 1D algorithm and the rational graph certificate are separate remedies for their respective admitted sizes.

### Temporal response, rather than only zero frequency

`laplace_response.py` uses rational tridiagonal elimination to calculate

```
chi_f(s)=integral_0^infty exp(-s*t)*Cov(f(0),f(t)) dt
```

at any supplied positive rational `s`. The same quadratic disorder inequality holds at **every** `s>=0`. Direct 6-, 10- and 16-site checks agree with numerical quotient resolvents. This supplies scalar long-time response at multiple observation windows; it does **not** imply pointwise all-time covariance bounds.

## Strongest existing approaches and what changes

- **Exact Markov lumping** already handles equal clocks within each class. It supplies the economical reference `K0`; it does not by itself control *arbitrary within-class kinetic differences* at the same output accuracy.
- **Reversible variational Poisson solvers and Dirichlet comparison** already provide mean-centered lower trials and a first-order bound from `nu_min,nu_max`. The present zero first-order compression plus Kantorovich argument improves the rate error from `O(rho)` to a sharp `O(rho²)` for invariant observables and a shared equilibrium.
- **Exact full-state sparse solves, tensor methods, coupling, and stochastic trajectory estimators** remain valid and can outperform this construction outside the symmetry-rich regime. Coupled-chain unbiased Poisson estimation has strong 2026 primary literature, and quantitative nongradient exclusion homogenization already solves important transport tasks by local functions. These do not become invalid because a different restricted response is available.
- **Existing Astra passage, source-current and clock comparisons** remain accepted at their actual scoped models. Their prerequisites, especially actual law versus nominal law and finite-bit costs, are respected. No transfer of their results to this cooperative network is asserted.

## Where this is genuinely broader, and where it stops

The mathematical theorem applies to *any* finite reversible group-averagable Markov system with an acquired relative form contrast and group-invariant source. The executable physics compiler covers arbitrary cooperative energy functions of counts in several modules, not only one-dimensional Ising rings, and can have strong interactions, phase coexistence, antagonistic modules, nonzero fields and individually distinct rate multipliers. The quotient state count is polynomial at a fixed number of modules, and the one-class scalar backend is exact integer arithmetic.

It **does not** handle general symmetry-poor lattices economically, site-specific equilibrium energies, nonequilibrium driving, arbitrary complex time-frequency response, or observables that break the selected symmetry. If the number of module classes grows with `n`, the quotient can again be exponential. All energies, rate bounds, output observables and module assignments must be acquired as inputs; this is not a learned Hamiltonian or a measurement instrument.

## The scientific decision

**Advance earned:** an all-order, sharp, symmetry-protected *relative* Green–Kubo response theory with a count-level algorithm and computational-work/error accounting. It can enclose the actual slow collective response of an extensively heterogeneous, interacting population without microscopic-state storage or long-time event following, when its equilibrium symmetry and kinetic-rate contrast are known.

**Next hard opening:** replace global permutation symmetry with *certifiably approximate local symmetry* and construct the relevant invariant-sector projection and its work cost from a genuine spatial generator. This would connect the result to disordered solids, locally interacting reactive materials, and nonlinear transport without assuming their slow-mode representation. No such spatial extension has been earned in this run.

**Novelty:** group lumping, Dirichlet forms, operator convexity, and Kantorovich inequalities are established mathematics; independent historical priority for the combined response construction remains unresolved. This is not yet a civilisation-changing general theory, working device, or experimentally validated material prediction.

## Preservation

The previous complete all-order construction and its nested earlier P2 archive remain **unchanged** at the original Library path. This new bundle is a separate branch; it does **not** claim to have copied or reverified the original archive bytes. See `PRESERVATION.md`.
