# Independent direct-decision and preparation-uncertainty constructions

The package preserves two completed alternatives to the [local thermal trial](README.md). Their purpose is to expose when a structured task can avoid generic preparation, and when a simple forced response can conceal a large preparation-uncertainty space. They do not extend the main nonlinear trial theorem to arbitrary interfaces.

## Ordered causal experiments and a direct compliance decision

Read the [decision overview](package/decision/README.md), [complete theorem](package/decision/theorem.md), [executed record](package/decision/execution.json), and [weighted-score corollary](package/decision/weighted_score_corollary.md).

For two known zero-state LTI plants with a nonnegative difference impulse response and a pointwise input envelope, the maximal nonnegative envelope input Blackwell-dominates every causal adaptive or randomized input. With Gaussian white position readout the whole decision problem reduces exactly to one scalar Gaussian experiment, including bounded stopping before a declared deadline. Nonnegative contrast and a pointwise envelope matter; this is not a universal solution for arbitrary model-discrimination or energy-constrained input design.

A frozen-versus-Maxwell internal strain pair has long-run compliances `1/(mu+B)` and `1/mu`. Its optimal information has successive regimes proportional to `lambda^2 H^7`, `lambda^2 H^3`, and H, with constants and parameter ranges in the proof. At fixed force, sensor noise and confidence, the small-rate decision time is order `lambda^(-2/3)`, compared with relaxation time order `lambda^(-1)`. It is not a rate-independent deadline for classifying infinite-time behavior.

Smooth finite ramps and finitely integrated readings retain the scaling. In the known binary pair, a fourth-order differential annihilator removes both models' complete unknown initial-state output spaces. A bipolar force and polynomial readout weight attain the same rate without passive equilibration or private timing. This pays known two-state structure, exact/controlled model coefficients, bounded initial energy, finite dynamic range, calibration and metrology. The proof does not turn unknown-model nuisance elimination into a free oracle.

Known-model matched Gaussian testing and initial-state elimination are strong equally informed ordinary comparators. No historical priority or replacement of ordinary experimental design is established. The separate finite private-weight-cache construction retains its bias and next-round entropy ledger; a newly measured fine preparation record is never relabeled as an independent old reference.

## Exact maximum preparation kernel from a forced response

Read the [completion receipt](package/uncertainty/COMPLETION_RECEIPT.md), [maximum-kernel theorem](package/uncertainty/MAXIMAL_PREPARATION_KERNEL_THEOREM.md), [first-principles derivation](package/uncertainty/FIRST_PRINCIPLES_DERIVATION.md), and [acquired finite-box record](package/uncertainty/acquired_box_kernel_results.json).

The declared collocated contraction-bath class has known positive M, Gamma and mu:

```text
x'=v,
M v'=-mu x-Gamma v-<b,z>+f,
z'=A z+b v,
E=(mu x^2+M v^2+||z||^2)/2,     E'<=f v-Gamma v^2.
```

A generates a contraction semigroup and b is bounded; no hidden-dimension cap is assumed. Collocation, physical energy norm, known visible mechanics, a retained plant and an acquired response certificate are premises. This is narrower than passivity alone.

For zero-state displacement step response S, the maximum preparation kernel is

```text
Cmax(t,s)=1/mu-S(|t-s|)
 -2 Gamma integral_0^min(t,s) S'(t-u)S'(s-u)du.
```

The union of visible free paths over all admissible realizations with this S and initial energy <=E is exactly the radius-sqrt(2E) RKHS ball for Cmax. One conservative-bath completion attains the entire set while preserving the supplied local damper. It determines maximum uncertainty across the model class rather than the actual hidden realization or actual readiness.

For exact finite observations with Gram matrix G, target cross-vector c and target squared norm d, feasibility requires `y in range(G)` and `y^T G^dagger y<=2E`. The exact scalar minimax center is `c^T G^dagger y`, with radius

```text
sqrt[(2E-y^T G^dagger y)(d-c^T G^dagger c)].
```

Both scalar endpoints are physically attained in the completion. This does not make a singular acquired pseudoinverse robust by assumption, nor assert one state attaining every pointwise path extremum simultaneously. Finite position-box formulas use response values and differences rather than a free derivative/velocity oracle.

The actual inherited response error 0.0562185 is too coarse for the demonstrated robust Gram inflation on width-0.1 boxes: its bound is 4.8732 against the elementary energy radius 1.0. The operational choice is to retain the elementary bound. Improvement requires a newly paid smaller response-error certificate. Floating completion diagnostics and the exact rational finite-box calculation were supplied as executed; Capital did not rerun them.

A third-order rational forced response can have an infinite-rank maximum preparation kernel. This exact-rank fact does not imply infinite cost at finite accuracy; it prevents inferring a small exact preparation state from low forced-response order alone. Conservative realization, de Branges-Rovnyak models and Hilbert optimal recovery are established comparators, and earlier Astra N997 already compares retained histories with equally informed optimal recovery. No major novelty or practical advantage over them is claimed.
