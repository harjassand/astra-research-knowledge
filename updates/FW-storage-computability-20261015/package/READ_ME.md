# Astra storage computability: exact handoff

15 October 2026. New deductions built from the main-repository PR96 proof at a6190a1083f688a7e4bf64adbc5244ef150ff2c4. Mathematical capability only; no physical technology, historical-priority clearance or external expert review is established. No canonical research files were changed.

## Capability

A terminating mathematical procedure can enclose the unrestricted signed required-supply storage value for Astra's particular non-polyconvex quartic G, to any requested absolute accuracy, when the affine background and finite-Fourier endpoint have computable coefficients with certified enclosures.

This removes two previously unresolved effective-approximation gates:
1. An explicit finite-duration error bound, including the neutral mean mode.
2. An explicit finite-dimensional action approximation that does not assume a minimizer, smooth interior gradients, or an unknown interior Fourier-tail budget.

It does not establish a useful runtime. No complete storage-value enclosure has been computed by the exhaustive procedure.

## Mechanism

Coercivity bounds the total gradient energy of near-minimizers. A low-energy slice near the end lets us replace the entire earlier path by a controlled entry; a finite constant ramp handles the mean. A different finite problem with explicitly free terminal mean yields a sharper approximation to the same infinite-duration value.

For spatial approximation, pad a finite path with known profiles and a known return, then apply the certified anisotropic heat flow to the whole periodic loop. Subtracting the exterior action cancels the full return cost. Explicit Gaussian leakage bounds make boundary repair cheap even if the unknown interior concentrates. Heat-generated Fourier tails give a computable cutoff. Compact polynomial optimization with rigorous gridding supplies both sides of the final storage interval.

The construction uses global periodic heat monotonicity. It never assumes that heat with fixed nonconstant Dirichlet data decreases the energy.

## Evidence

- Full horizon and spatial proofs, including constants and all finite/infinite-domain distinctions.
- Separate proof challenges of the horizon surgery and buffered heat argument.
- A newly written Fraction-only checker reconstructs the underlying Heat18 certificate: 210 polynomial coefficients, closedness, primitive, Gram factorization and 18 positive LDL pivots. Root replay passed. The apparent source-hash discrepancy is exactly one extra terminal newline.
- A separate exact resource checker passes 33 inequalities for a concrete sufficient parameter choice at target width 0.01.

These are proofs and computational receipts, not independent experimental validation. Audit labels alone are not evidence; the supporting arguments and arithmetic are included.

## Closest prior result and precise difference

Fantuzzi–Fuentes, Global minimization of polynomial integral functionals (2024), supplies finite-element polynomial optimization and moment/SOS convergence. Section 5 explicitly notes that finite SDP values need not bound the continuum minimum: they lower-bound a discrete upper bound. https://arxiv.org/html/2305.18801v3

The present construction supplies an explicit continuum-to-finite-family action error for this special heat-monotone energy. It does not automatically add an error theorem to arbitrary finite elements or arbitrary quartics. Effective compact minimization, heat localization, cyclodissipative concatenation and turnpike slicing have substantial prior art; their precise scope is documented in the two prior-art reports. Novelty of this particular composition remains unestablished.

## Resource result: not a practical solver

For U=(cos y,sin y), B=0 and target width 0.01, one fully checked sufficient construction uses:
- horizon 10^22;
- Fourier cutoff 10^44 in each coordinate;
- approximately 8×10^88 real parameters;
- a coefficient grid whose base-10 logarithmic cardinality is below 10^93 (the sharper documented upper bound is approximately 5.296×10^91).

No grid was enumerated and no objective values were evaluated. These are extremely loose sufficient bounds, not lower bounds on every possible algorithm. They establish effectiveness while decisively ruling out this explicit exhaustive construction as a usable numerical method.

## Missing operation, consequence and next test

The missing operation is a quantitatively useful continuum error bound and global lower certificate at manageable resolution. An active route uses the actual computed baseline's heat loss to bound all unresolved high-frequency perturbations, rather than the enormous uniform worst-case constants. That route is not claimed complete here.

If made practical, such a bound could turn a discrete variational lower bound into a defensible continuum certificate for this energy class. A real-material consequence additionally requires a validated constitutive law and obtainable endpoint information; G currently remains a mathematical benchmark.

The decisive next test is a nontrivial storage interval from a fully executed, matched-cost computation, or a rigorous demonstration that the proposed sharper bound cannot close that gap. General endpoints also require a supplied effective strong critical-tail approximation. Finite measurements alone cannot provide it.

## Contents and replay

- heat_certificate/replay.py: exact finite certificate replay (standard library only).
- storage_spatial/verify_resource_bounds.py: exact sufficient-parameter accounting (standard library only).
- storage_horizon/FINITE_HORIZON_STORAGE.md and HORIZON_AUDIT.md.
- storage_spatial/THEOREM.md and spatial_audit/INDEPENDENT_HEAT_AUDIT.md.
- Primary-source comparisons and pinned receiving proofs.
- storage_horizon/ROBUST_STORAGE_SIGN.md: separate finite sign certificate under a paid endpoint-tail envelope; it does not evaluate storage.

Run the two replay scripts from their own directories if their local file lookups require it. No downloaded author executables, compiled binaries or private assistant notes are included.
