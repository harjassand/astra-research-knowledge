# Passive repair under uncertain contact time — 24 October 2026

This focused addendum preserves a conditional hazard-scheduling bound and its separate creep consequence. The two source notes were copied byte-for-byte and checked against the retained receipt; see [source_manifest.json](source_manifest.json). No physical material model, experiment or repair operation was acquired here.

## Conditional bound

The source assumes damage at time zero, a preset nonnegative productive hazard `a(t)` independent of future face contact, contact time `tc ∈ [0,T]`, identical repair dwell `τ`, and required dose `∫[tc,tc+τ] a(t) dt ≥ H` for every contact time. Writing `T=mτ+r`, with `0≤r<τ`, and `J=∫[τ,∞)a(t)dt`, it derives the universal tail bound `J≥mH`.

If `a(t)≤A`, feasibility requires `H≤Aτ`. In the same mathematical class, the source gives the exact optimum `J_min=mH+max(0,H−A(τ−r))`, attained by a periodic rectangular schedule. These statements depend on the preset-hazard and all-contact-times contract; they are not a physical impossibility result or evidence that a material realizes the schedule.

## Consequence and changed premises

Under the stated no-parallel-load-path assumption, the source maps the bound to Maxwell-like creep `u=(ell σ/G) ξ J`. Contact sensing or mixing, permanent locking, waiting or unloading changes the premises and carries separate costs. Furan-maleimide healing and existing repair methods remain incumbents. No measured constitutive law, contact distribution, material lifetime or acquired repair operation is included.

## Evidence boundary

This is a source-reported conditional model derivation; no independent proof review, material experiment, practical comparison, novelty or advantage is claimed. The topology/sorption route and other polymer alternatives from the same snapshot are not selected by this update.
