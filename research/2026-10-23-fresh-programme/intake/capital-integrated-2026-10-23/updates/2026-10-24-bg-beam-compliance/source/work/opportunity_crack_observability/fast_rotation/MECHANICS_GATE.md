# Mechanical gate: attenuation visibility versus crack driving force

**Result.** In the stated continuum model, a finite-resolution attenuation scan can lose all resolvable contrast as the aperture of a fixed-length slit tends to zero, while the limiting sharp crack retains nonzero mode-I driving force at fixed remote stress. This is an observability mismatch, not a fatigue-life prediction. A calibrated compliance or displacement measurement is a conventional possible escape; load amplification is only safe after a material- and geometry-specific margin is established.

## Exact idealization

Take a homogeneous, isotropic, linearly elastic, thin infinite plate in plane stress, with a through-thickness elliptical void extruded through thickness `t`. Its in-plane semi-axes are `a` along `x` and `b` along `y`, with `a` fixed and `b/a → 0`. Apply remote uniaxial tensile stress `σ∞` in the `y` direction, perpendicular to the major axis. The two ellipse ends at `(±a,0)` are therefore mode-I notch tips. For the radiographic statement, let the solid attenuation coefficient be `μs`, the void coefficient be zero, and use parallel-beam views followed by a fixed finite set of detector bins with bounded, normalized point-spread / bin kernels. This is an explicit finite-resolution observation model; it is not a claim about every scanner or reconstruction pipeline.

## Attenuation signal vanishes with aperture

The void volume is

`V(b) = π a b t`.

For any parallel-beam direction, the line-integral deficit on a detector coordinate `u` is `d(u) = μs ℓvoid(u)`. A detector bin with normalized nonnegative kernel `ψj(u)` returns `dj = ∫ ψj(u)d(u)du`. If `ψj` is bounded by `Cj`, Fubini's theorem gives

`0 ≤ dj ≤ μs Cj ∫ ℓvoid(u)du = μs Cj V(b) = O(b)`.

The equality uses the projection identity that integrating chord lengths over the detector plane gives the object's volume. Thus every fixed bin's contrast tends to zero with `b`; any fixed finite linear reconstruction also has contrast tending to zero because its operator norm is fixed. For any positive detection threshold or noise floor, sufficiently small `b` is operationally invisible in this model. It is not exactly invisible for every positive `b` in a noiseless ideal measurement.

Opening a closed crack changes the separation of the faces and may create a finite void aperture. It does not destroy mass. An attenuation difference between loaded and unloaded scans is possible only to the extent that this new gap changes the ray integrals and survives the instrument's spatial averaging and noise. It must not be assumed that a crack-opening event automatically appears as missing mass in an X-ray difference image.

## Elastic driving force does not vanish with aperture

For the ellipse, Inglis's infinite-plate solution gives the maximum tensile stress at either major-axis end as

`σtip = σ∞ (1 + 2a/b)`.

The local radius of curvature is `ρ = b²/a`, so equivalently `σtip = σ∞ (1 + 2√(a/ρ))`. At fixed `a` and `σ∞`, the classical elastic notch stress diverges as `b → 0`. That divergence is a warning about the sharp-notch limit of scale-free linear elasticity; it is not a prediction of an actual infinite material stress. Inglis's original paper explicitly treats the elliptic-hole solution and its fine-crack limit.

The limiting object is a central straight crack of total length `2a`. Irwin's Westergaard solution for a large/infinite plate gives

`KI = σ∞ √(πa)`.

For fixed `a` and nonzero `σ∞`, this is finite and nonzero even though the limiting aperture and void volume are zero. For a tensile cycle with stress range `Δσ`, the same idealization has `ΔKI = Δσ √(πa)`. The near-tip field is parameterized by `KI`; it does not require a finite-volume defect. The formulas are mutually consistent at the level relevant here: the finite-aperture elliptical tip stress grows without bound, while the sharp-crack field has a finite stress-intensity amplitude. Do not use the notch-tip divergence as a physical local stress or as a direct life estimate.

Primary sources: C. E. Inglis, “Stresses in a Plate Due to the Presence of Cracks and Sharp Corners,” *Transactions of the Institution of Naval Architects* 55 (1913), pp. 219–241 ([original paper scan](https://imechanica.org/sites/default/files/1913%20Inglis%20Stress%20in%20a%20plate%20due%20to%20the%20presence%20of%20cracks%20and%20sharp%20corners_0.pdf)); G. R. Irwin, “Analysis of Stresses and Strains Near the End of a Crack Traversing a Plate,” *Journal of Applied Mechanics* 24(3) (1957), 361–364 ([author paper scan](https://imechanica.org/sites/default/files/1957%20Irwin%20Analysis%20of%20stresses%20and%20strains%20near%20the%20end%20of%20a%20crack%20traversing%20a%20plate.pdf)). Irwin restricts the 2-D treatment to configurations where a generalized plane-stress or plane-strain description is appropriate and discusses corrections when crack length is no longer small relative to body dimensions.

## Is there a conventional measurement escape?

Yes, in principle. A crack changes the elastic displacement/strain field and the load–displacement compliance of a finite specimen, even when its zero-aperture idealization removes zero volume. A mechanically instrumented compliance, strain, or crack-opening measurement can therefore be a distinct observable from unloaded attenuation CT. Irwin's crack-opening field is load-dependent. Such a method still needs a specified fixture, boundary conditions, sensor resolution, and a demonstrated intact-versus-cracked signal margin; it is not a universal guarantee that every crack is detectable.

Increasing the applied load can increase `KI` and the displacement signal linearly in the elastic regime, but it is a safe proof-load only if an independently justified allowable `Kmax` (and yield / stability margin) is available for the material, geometry, environment, and loading rate. Otherwise amplification could extend the crack or trigger failure. In a finite body the appropriate form is `KI = Y(a/W, …) σ √(πa)` with geometry factor `Y`, rather than the infinite-plate `Y=1`. A fatigue-life statement would additionally require material-specific crack-growth data and treatment of load ratio, closure, residual stress, environment, and plasticity; none is inferred here.

The mechanical gate is therefore narrow: attenuation can be aperture/volume-limited while fracture mechanics is length/stress-field-limited; mechanical compliance is a plausible conventional alternative, but its detectability and safe operating window are device- and material-specific.
