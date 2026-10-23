# P2 finite-sleeve return — 24 October 2026

This is an append-only addition under the existing [P2 sliding-ring finite-contour coverage update](../../README.md). Its earlier README, source manifest and producer return remain unchanged. The [manifest](source_manifest.json) pins the exact supplied return capture. That single JSON preserves the complete captured `text`, the equation-bearing `html` (including its math-source annotations and rendered markup), and the original `links` references together. No code or data attachment was supplied.

## Contact geometry and retained order

The return reports a single-passage and retained-ring-order construction for a specific rod-and-sleeve model. The axle has diameter `d`, retains its circular thickness, and has local bend radius at least `d/2`; this is an explicit constitutive assumption, not something inferred from bead diameter or persistence length. The example sleeve has bore diameter `1.5d`, length `1.2d`, outer diameter `3.5d`, and terminal stopper diameter `2d`.

For axle radius `ρ`, bore radius `H`, clearance `c=H−ρ`, and minimum bend radius `q`, the reported sufficient condition is `0 < c < q` and

`L > 2[ρ + q(1 − sqrt(1 − (c/q)^2))]`.

For the selected dimensions this requires `L > 1.133975d`. Under the stated thickness and bend-radius assumptions, the source argues that a second central-plane passage forces a lateral excursion too wide for the bore; the solid-torus contact geometry is also used to rule out two collars exchanging crossing order. Every initially threaded collar then has one trackable contour coordinate, with spectators retained between consecutive active collars. This is a source-reported model result, not a molecular realization.

The same model has outward handles on active collars and no binding sites on spectators. At reported center separation `5.6d`, two facing handles can connect outside both bores while either locally straight axle translates through its sleeve without stretching the exterior connection. The selective interaction and its chemical implementation remain unestablished. Threading before installing the final stopper supplies the model's assembly path; no internal axle join or imposed threading-sector predicate is used in the described motion.

## Separate elastic-energy floor

With the curvature constraint softened while retaining the same finite-sleeve contact geometry, the return reports a local floor for the first additional central-plane passage:

`E_b,gate ≥ 0.81343 K/d`.

This is an absolute local elastic-energy floor relative to a straight segment. It is not a thermal activation free-energy barrier or a retention-time estimate. Existing strain, applied work, entropy, changes in bending stiffness, and cross-section deformation may change a practical barrier. Keep this claim separate from the hard single-passage result above.

## Ideal statistical claims and counterexample

The reported statistical statements use a three-dimensional Gaussian-span model with contour allocation and positional displacement as described in the preserved return. In that ideal setting, one spectator per interval retains the special cancellation after contour allocations are integrated out. Two spectators per interval give joint log-concavity of the contour-and-displacement weight; the stated extension requires jointly convex additional energies, affine contour constraints, products, and integration over convex domains.

The return reports a converged three-span counterexample in which the convex diagnostic penalty `100(n₁−n₂)²` defeats the one-spectator positional-convexity result, while the two-spectator case retains the stronger guarantee. That penalty is a mathematical diagnostic, not a proposed chemical interaction. In the coincident-endpoint ideal model, one spectator gives a divergent inverse-contour moment; with two, the reported equal-occupancy identity is `⟨1/nᵢ⟩=(3k−2)/N`. Higher derivatives can require higher moments, so this does not establish universal robustness to finite contacts. The suggested `BB−A−BB−A−BB` sequence is a theoretical target, not a demonstrated molecular architecture.

For the ideal uniform-spectator interface, a unique crossing is insufficient: the physical weight must include the angular Jacobian `|n̂·t(s)| ds d²q` and sleeve, axle, handle, and neighboring-ring interactions. The ideal `nᵐ/m!` factor requires that combined weight to be constant over ordered contour positions. The return identifies sleeve straightening and handle-dependent tangent selection as possible deviations; the uniform-spectator/Gaussian interface remains unacquired.

For a Gaussian off-axle linker, the return gives a correlated attachment criterion in dimensionless units. With axle stiffness `P`, handle-position covariance `V`, axle-force/handle-position cross-covariance `G`, and linker covariance `Σ`, all from the same loaded ensemble, it requires `Σ−V ≻ 0` and

`P − G(Σ−V)⁻¹Gᵀ ⪰ 0`.

The source relates this criterion to established Gaussian smoothing mathematics; it preserves the correlations instead of assuming that a soft linker removes the response.

## Molecular interface and evidence boundary

CB7/PEG is retained as a chemical lead. The referenced aqueous pumping and exterior crosslinking results are separate; their required intersection—ordered functionalized/native rings that retain sliding after selective connection—has not been established. The captured return records a `5.4 Å` CB7 portal, `7.3 Å` equatorial cavity, and `9.1 Å` height, and a PEG persistence length around `3.7–3.8 Å`; statistical stiffness is not a hard minimum bend radius. Molecular realization and the uniform-spectator/Gaussian interface remain unacquired.

The earlier residence pilot remains neither equilibrium evidence nor sliding-speed evidence. The source capture labels itself as producer return only, not scientific validation. The supplied review read the complete return and checked selected primary-source boundaries; it is source-exposed programme judgment, not independent proof or computational replay. No new scientific run, replay, code or data attachment is part of this integration. Producer claims, established mechanics and unestablished novelty or physical capability remain distinct.

The complete set of original source references, with their captured labels and URLs, is preserved in `producer_return.json` under `links`.
