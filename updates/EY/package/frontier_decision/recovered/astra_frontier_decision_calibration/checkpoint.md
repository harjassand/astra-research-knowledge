# ASTRA checkpoint — 13 October 2026

## Actual new capability

A freshly compiled measurement-to-control policy covers unknown U in [3.9,4.1] and original physical d in [1.9,2.1], at t=1 and control V in [0,3], for the same infinite tracial range-two interacting quantum chain. No U,d point estimate or online many-body solve is needed.

One six-site-preparation/logical-Ramsey measurement setting, tau=1/2, has mean exp(-d/2) cos((U-4)/2+psi), with cos psi=32/257 and sin psi=-255/257. Its phase is independent of V because the prepared neighbour pattern makes the single-hop detuning exactly U.

Control command: clip and round to grid1/2048 of
V0 + (14340421443/4294967296) sample_mean -13/85,
V0=1109/512. Extra calibrated actuator error <=1/4096 is allowed; combined quantization/actuation <=1/2048. Mean bias <=1e-4 is charged.

Uniform, >99%-confidence model-wise global regret:
- N=262144: <8.780360455e-5; native time131072.
- N=1048576: <4.342742581e-5; native time524288.
Additional preparation, reset, freezing, readout and calibration costs are not zero. No physical assay was executed.

Every model in the uncertainty box is certified to have exactly one global optimum in (2,2.5). Root-containing policy tube has certified curvature <=-0.07592003516. All bounds separately hold for finite periodic D_n at n>=41.

## Strict information separation

For a=+-0.01, define U=4+a and d=2+2log(cos(a/2)+(255/32)sin(a/2)). Both models have exactly the same fine-assay Bernoulli law. Their D(V0) intervals are disjoint by >0.0203442744. Thus repeated use of this contrast cannot identify absolute D to error <.0101721 uniformly, while the policy remains good. Other measurements can distinguish them; the statement is not about an unrestricted experiment interface.

Every deterministic control selected from only the common parameter box, without observations, has worst-case regret >=0.00012390875. Both policy guarantees improve on this comparator. No claim against the strongest active Hamiltonian learner is made.

## New mathematical/compiler elements

- General decision object is a common near-optimal action on a (thickened) observation fibre, not a reconstructed parameter vector or output surface.
- C=-F_uu^-1 F_ueta proposes a low-dimensional compensation direction. This implicit-function/cross-Hessian idea has prior art. Its usefulness and curvature must be checked, not assumed.
- Fixed-reference normalization S(2)+lambda I permits uncertain physical d while retaining affine operator dependence. Re T>=beta=min(1,d/2); perturbation norms w=(1,1,1/2) in axes[V,U,d].
- Exact corrected-output error is <r,R T^-1r>. Multi-index derivative bound is 4 sum_(a+b+c=alpha) alpha!|c|!/(a!b!c!) beta^(-|c|-1) w^c q_a q_b.
- Twenty mixed trial derivatives through total order3, all35 residual derivatives through order4, exact rational Grams and polynomial pullbacks certify the full nonlinear sensor policy over the entire nuisance box.
- The actual measurement direction is selected by a finite rational/Pythagorean search from the corrected Hessian, then verified globally. It is also the one-copy locally unbiased minimum-variance measurement for the selected scalar at fixed tau, a specialization of established quantum semiparametric principles.

## Construction and evidence

Fresh span8 dictionary acquisition179.8333s; mixed solves46.4836s; exact packet13.0620s; six fresh anchors9.0969s (two unused but charged); policy check3.6676s. Sum252.1435s; peak1.88GiB, oneBLASthread. Code/enrichment settings reused, not prior response coefficients; exploratory development and physical acquisition excluded. Separate all-packet reconstruction16.9518s.

Finite checks: exact error identity with uncertain noise;240 mixed derivative bounds;20 integer-limb products;9 direct physical polynomial scalar checks; corrupted population defect rejected;9 detuning identities;40 Lindbladian Ramsey checks; exact interval tests;10 synthetic decision trials.

Optional coarse calibration: two quadratures at tau1/8,2^20 shots each, starts from U[0,8],d[1,4]. It returns the required box only if its whole interval fits, otherwise inconclusive. Mean bias1e-4 charged. Joint probability of accepting then giving a bad decision <.009. This is not a conditional-on-acceptance guarantee. No acceptance probability is promised. Raw coarse measurements would add information beyond the one-contrast nonidentifiability example.

## Remaining scientific question

Generalize construction of conservation-safe decision residuals and a realizable low-dimensional sensor across broader physical classes with useful total cost. A low-rank decision Jacobian alone gives no generic global optimizer, inverse-rank bound, cheap sensor or compact dictionary. This is a concrete restricted uniform uncertainty-family success, not a civilisation-level result, physical experiment, low-temperature claim, closed-system result or generic polynomial solver.

## Priority/provenance

Prior full response-error note read; finite compiler reused with recorded changes. Astra revision74c2843bd224c2975c6e46735b30ae7c927f948b inspected; no external writes. Targeted openai/math decision/regret/sensitivity search yielded no applicable result. Tan-Frazier2022 already gives cross-Hessian regret with quartic nuisance remainder; goal-oriented reduced models, goal-driven BOED and semiparametric quantum estimation explicitly credited. Combined quantum sensor-policy novelty, independent proof review and formal verification remain unknown/unperformed.
