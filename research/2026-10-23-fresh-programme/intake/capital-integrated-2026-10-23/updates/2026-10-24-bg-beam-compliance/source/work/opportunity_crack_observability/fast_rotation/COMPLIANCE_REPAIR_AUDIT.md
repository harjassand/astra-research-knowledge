# Audit: compliance monotonicity repairs the aperture-only observability gap

**Verdict: the proposed repair is valid under the force-controlled, traction-free, linear-elastic assumptions, with two precision fixes.** First, the variational comparison requires the *same exterior load functional* on both material domains, homogeneous fixed supports eliminating rigid motion, and no body-force contribution from material that is removed. Second, the lower bound must use a certified `Ymin` over every intermediate crack half-length `x ∈ (0,a]`, not merely a value at the endpoint. With those conditions, a finite ellipse containing a slit has compliance at least that of the slit, so the elastic compliance gap does not vanish as ellipse aperture `b → 0`.

## Variational comparison

Let `Ω` be a bounded linearly elastic body, with a fixed homogeneous displacement condition on `ΓD` and a shared scalar outer load pattern `ℓ` on the remaining loaded boundary. For defect `D`, write the material domain as `ΩD = Ω \ closure(D)` and define

`aD(u,v) = ∫ΩD ε(u):C:ε(v) dx`,

where `C` is positive-definite elasticity. Let `VD` be the finite-energy displacement space with `u=0` on `ΓD`, with no imposed displacement on the traction-free defect boundary. Supports make `aD` coercive; assume the body remains well-posed. For a *unit* load pattern, define the scalar compliance

`c(D) = sup_{u∈VD} { 2ℓ(u) − aD(u,u) }`.

The maximizer `uD` solves `aD(uD,v)=ℓ(v)`, and `c(D)=ℓ(uD)` is the work-conjugate displacement per unit force. The actual load `Fℓ` produces displacement `F uD` and complementary-work value `F² c(D)`.

Let `Γa` be a zero-width central slit of half-length `a`, and let the closed elliptical void `closure(Db)` contain `Γa`. An admissible finite-energy slit field `u∈VΓ` restricts to `ub=u|Ω\closure(Db) ∈ VDb`: the new ellipse boundary is free, so no new trace constraint is imposed. The exterior trace and hence `ℓ` are unchanged. Since `closure(Db)` removes material and the strain-energy density is nonnegative,

`aDb(ub,ub) ≤ aΓ( u,u)`.

Therefore `2ℓ(ub)−aDb(ub,ub) ≥ 2ℓ(u)−aΓ(u,u)`. Taking the supremum over `VDb` on the left and over `VΓ` on the right proves

`c(Db) ≥ c(Γa)`.

This is a compliance monotonicity statement, not a general displacement-field pointwise ordering. It uses force control; prescribed nonzero exterior displacements, crack-face contact/friction, cohesive tractions, surface energy, body loads changed by excision, or nonlinear material response are outside this comparison as written. Finite-energy crack-tip fields are admissible; restriction to the smoother subdomain removes the tip singular points from its interior.

## Factor and integrated gap

Use `c(a)=δ/F` for the scalar compliance of a centrally cracked through-thickness plate of thickness `t`; `a` is the *half*-crack length, so increasing `a` by `da` extends both tips and adds projected crack area `dAcr=2t da`. Under force control, the potential energy is `−F²c(a)/2`; consequently

`G = −dΠ/dAcr = F² c'(a)/(4t)`.

The factor `4t` is correct for the two advancing tips of a center crack when `G` is per unit projected crack-plane area. If a different crack-length variable or one-tip geometry is used, this factor changes.

For isotropic LEFM, `G=KI²/E'`, with `E'=E` in plane stress and `E'=E/(1−ν²)` in plane strain. Put `σ=F/A` for gross-section area `A` and `KI=Y(x)σ√(πx)`. Equating the two expressions gives

`c'(x) = 4πt x Y(x)² / (A² E')`.

Thus, in the ideal continuum LEFM family, if constants `Ymin>0` and `Emax` are certified so that `Y(x)≥Ymin` and `E'≤Emax` for *all* `x∈(0,a]`,

`c(Γa)−c(∅) = ∫₀ᵃ c'(x)dx ≥ 2πt Ymin² a² / (A² Emax)`.

By the domain comparison, the same lower bound applies to `c(Db)−c(∅)` for every aperture `b>0` whose void contains `Γa`. For a minimum crack half-length `a0`, replace `a` by `a0` to obtain a uniform separation. Without a positive minimum crack length, this lower bound tends to zero as `a²`; there is no uniform all-sizes detector threshold.

For physical use of LEFM, integrating all the way from `x=0` may cross sizes below its validated small-scale-yielding / continuum range. If LEFM is certified only for `x∈[a*,a]` with `a*>0`, the justified increment is instead

`c(Γa)−c(Γa*) ≥ 2πt Ymin² (a²−a*²) / (A² Emax)`.

Force-control domain monotonicity also gives `c(Γa*)≥c(∅)`, so this is still a lower bound relative to pristine compliance. It is positive only when `a>a*`; the physical minimum size used by this argument must exceed the LEFM validity threshold.

## Measurement scope

For known intact geometry and supports, a calibrated work-conjugate displacement measurement under a known small force can distinguish the cracked/void case whenever its compliance resolution is finer than the bound. The signal in displacement is `F Δc`. This is a genuine conventional mechanical observable independent of attenuation contrast and closes the idealized `b→0` gap conditionally. It does not guarantee identification in an unknown structure: other damage, support slip, temperature, residual stress, geometry error, or sensor noise can also alter compliance. A spatial strain/opening sensor would require its own response and resolution bound.

“Small” or “safe” cannot be inferred from the compliance inequality. A probe's reversible, nondamaging force range must be licensed separately for the actual material, geometry, environment, and cycling history. A bound on `KI` alone is not a proof against subcritical growth or fatigue, and this calculation supplies no lifetime estimate. The ideal result assumes a known baseline, an open traction-free crack, quasi-static linear elasticity, and a valid LEFM energy relation on the crack-length interval used in the integration.
