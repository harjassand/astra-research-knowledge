# Bounded convex relaxation: exact planar control and rejected primitive claims

P1's recovery record supplies completed constructive mathematics for an ordinary classical planar diffusion model: exact linear-response reachability, minimum duration, simultaneous radial thermal-error optimality among fastest controls, and an explicit force schedule. Companion results give a sharp finite-stage resource law and prove that fastest need not minimize a combined time/noise/work objective when surplus contraction is available.

The proposed foundational primitives did not survive direct literature comparison. Gradient-flow holonomy, labelled transport and the relevant geometry already have direct treatments. The contribution retained here is the constructive optimization result within established geometry and Langevin dynamics. No new microscopic law, experimental demonstration or civilization-changing capability is established; priority of the combined deductions is not exhaustively settled.

**6 November quantum preparation allocation, complete visible response, original pending:** [P1 reports a separate permanent-factory/noisy-selector construction](../2026-11-06-p1-fixed-quantum-factories/README.md) using accepted mixed-block machinery and whole-inactive-state neutralization. It does not transfer this classical Gaussian theorem to quantum states. The complete visible response supplies the bounded-incidence scope and final comparisons; original report/checks remain pending. The source explicitly has no independent audit/peer review, and no total-resource advantage is established. These convex-relaxation proofs, prior materials/reflection and failed-novelty boundaries are unchanged.

## Governing source record

| Read | Contents |
|---|---|
| [Original ZIP](original/convex_relaxation_research_record.zip), [package guide](package/README.txt), [manifest](package/FILE_MANIFEST.json) | All 40 original members and 39 supplied member checksums |
| [Main proof and claim boundaries](package/invention_variation/proof_and_claim_boundary.txt) | General-target compiler, exact controls, covariance ordering and scope |
| [Finite-stage theorem](finite-stage-and-slower-controls.md) | Sharp factor count, contraction, time and condition number; slower-time tradeoff |
| [Thermal, work and physical limits](thermal-order-work-and-physical-scope.md) | Radial ordering, stored input energy, bandwidth, measured comparators and full limitations |
| [Independent audit](package/invention_holonomy_audit/audit.txt), [primitive log](package/invention_root/primitive_log.txt), [source audit](package/invention_root/source_audit.txt) | Proof corrections, rejected novelty and primary comparisons |
| [Executable compiler](package/invention_root/compile_planar_response.py), [example output](package/invention_root/example_rotation_operation.json) | Ideal model schedule, covariance and confidence radius; not a laboratory control program |
| [Recovery capture](P1_INTERRUPTED_RECOVERY_1C7E_20261105_RETURN.txt), [source map](SOURCES.json) | Exact original/recovery prompts, complete rendered answer, activity and capped native prefix |

All supplied bytes are unchanged. Recorded calculations and audits retain their actual scopes. Capital did not run the compiler, numerical suites, plots or a new scientific audit. The floating compiler is not an interval-certified solver for arbitrarily scaled inputs.

## Model and exact operation

```
dX_t = -A(t) X_t dt + sqrt(2D) dW_t
A(t) = A(t)^T,  0 <= A(t) <= Lambda I
X_T = F X_0 + eta.
```

The position and entire response matrix are two-dimensional. Diffusion is constant, isotropic and memoryless; controls are prescribed independently of the unknown input and bath trajectory. The same response holds for every bath-independent input point/distribution. It is stronger than matching one chosen final marginal, but that representational distinction is established prior literature.

For a real `2x2` target with positive determinant, define `s=-log(det F)/2`, `N=exp(s)F` and the established symmetric-traceless horizontal distance `d(N)` on `SL(2,R)`. The source evaluates this distance through explicit monotone scalar roots rather than assuming an optimization oracle. Exact reachability and minimum time are

```
F reachable iff s >= d(N)
T_min = (s+d(N))/Lambda.
```

Singular and negative-determinant targets are unreachable in finite bounded-control time. The construction traverses a shortest shape with maximum rank-one restoring force for `2d(N)/Lambda`, then applies maximum isotropic relaxation for `(s-d(N))/Lambda`. It implements the requested full matrix and computes the thermal covariance directly. Among all duration minimizers it minimizes every radial error tail. Optimal covariances can form an orthogonal-conjugacy orbit; a single matrix below every optimizer is not asserted.

For `F=exp(-s)R_theta`, principal `|theta|<=pi`, the distance is `L_theta=sqrt(theta^2+2pi|theta|)`. A 90-degree boundary rotation retains only about 2.983% of input amplitude. This is a severely attenuating operation, with preparation and readout costs not hidden by the mathematical control result.

Earlier [materials and completion-dose results](../2026-11-05-p1-timed-material-construction/README.md), the failed frozen-law specimen, selection and reflection records remain unchanged; the failed specimen was not refitted. This package contains preservation hashes rather than copies of those earlier ZIPs. The separately pending materials original is not delivered or resolved by this intake. The completed producer chat remains a predecessor; Capital created no fresh chat or researcher message.
