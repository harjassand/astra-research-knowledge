# Mechanical cell audit and reciprocal two-port example

## Algebra check

For anchored host stiffness `H ≻ 0`, cell coordinate `y`, and coupling pattern `a`, the potential

`E(u,y) = 1/2 uᵀ H u − fᵀu + V(y) − y aᵀu`

has host equilibrium `u(y)=H⁻¹(f+ya)` and reduced fixed-load potential

`Φ(y)=V(y)−1/2(f+ya)ᵀH⁻¹(f+ya)`.

Consequently `Φ′(y)=V′(y)−aᵀu`, `Φ″(y)=V″(y)−aᵀH⁻¹a`, and an increment `Δy` changes the trigger extension by `aᵀH⁻¹a Δy`. A different threatened extension `bᵀu` changes by `bᵀH⁻¹a Δy`. The host is reciprocal, so this cross response is a compliance and is not an independent sensor/actuator gain. It can have either sign; negative cross-compliance is the geometric requirement for shielding by a positive snap increment.

For deletion of a rank-one bond `k bbᵀ`, Sherman–Morrison gives

`C′−C = k(bᵀH⁻¹f)²/(1−k bᵀH⁻¹b)`, where `C=fᵀH⁻¹f` and the post-deletion matrix is positive definite exactly when the denominator is positive. At fixed force the minimized host potential is `−C/2`, so its change is `−(C′−C)/2`; this is the load-controlled potential change, not the strain-energy change alone. The expression in `FIRST_CONSTRUCTION.md` is correct under its stated stability condition. For several cells, eliminating `u` gives Hessian `D²V−AᵀH⁻¹A`; strict positive definiteness is a sufficient local branch-stability condition, with equality marking a loss of strict stability.

## Exact normalized reciprocal spring/snap cell

Take two node displacements `u=(x₁,x₂)`, each attached to ground by a unit spring. Add a unit threatened spring between them with extension `e_v=bᵀu`, `b=(-1,1)`. Thus `H=I+bbᵀ=[[2,−1],[−1,2]]`, `det H=3`, and `H⁻¹=(1/3)[[2,1],[1,2]]`. Attach a bistable snap coordinate `y` to node 1 through the reciprocal lever coupling `−yx₁` (`a=(1,0)`). This is a passive potential model: the same coupling that makes node-1 displacement act on the snap coordinate makes snap motion exert force on node 1.

The compliances are

`H⁻¹a=(2/3,1/3)ᵀ`, `aᵀH⁻¹a=2/3`, and `bᵀH⁻¹a=−1/3`.

So a positive trigger-driven snap increment increases its own trigger extension by `(2/3)Δy`, while it decreases the distinct threatened spring extension by `(1/3)Δy`. No nonreciprocal or externally commanded actuator is used.

For a bistable flexure normal form

`V(y)=(3/4)(y²−1)² +(1/3)y²`

and dead load `f=(0,2√3)ᵀ`, define `s=aᵀH⁻¹f=2/√3`. The `+(1/3)y²` term in `V` cancels the host relaxation term `−(aᵀH⁻¹a)y²/2`, giving, up to a constant,

`Φ(y)=(3/4)(y²−1)²−sy`.

As `s` is raised from below `2/√3`, the negative-y local minimum remains metastable until its spinodal at `y₋=−1/√3`: `Φ′(y₋)=0` and `Φ″(y₋)=0`. The other minimum is `y₊=2/√3`, with `Φ′(y₊)=0`, `Φ″(y₊)=9>0`. The snap has `Δy=√3`. The threatening spring extension is

`e_v(y)=(2√3−y)/3`,

which falls from `7/(3√3)` to `4/(3√3)`, a reduction of `1/√3`. The trigger extension `x₁(y)=(2y+2√3)/3` rises by `2/√3`, so the snap is positively self-activating at its trigger port.

The entire fixed-load energy ledger is included. The reduced potential drops by `Φ(y₊)−Φ(y₋)=−9/4` (normalized energy units). During the snap the dead load does work `fᵀΔu=2`; the host spring energy changes by `+7/3`, the flexure energy `V` by `+1/12`, and the reciprocal interaction energy `−yx₁` by `−8/3`. Thus the internal mechanical energy change is `−1/4`, and subtracting the load work gives `−1/4−2=−9/4`, exactly the reduced-potential change. This example therefore charges the preload/dead-load reservoir rather than claiming the flexure alone supplies all released energy. The metastable branch and coupling are the reserve; the fixed-load source contributes the stated work. At a real design’s comparison boundary, both must be charged, together with cell volume and reset/reuse costs.

For the same host, deleting the threatened spring has `q=bᵀH⁻¹b=2/3`. Under the displayed dead load with the cell held fixed at `y=0`, the pre-deletion extension is `e=bᵀH⁻¹f=2/√3`. Hence `ΔC=e²/(1−q)=4`, and the minimized host potential falls by `2`. The post-deletion matrix is `H−bbᵀ=I ≻0`; this directly checks the deletion identity and denominator in the construction.

## Scope

This is an exact small mechanical counterexample to a sign-based impossibility: a passive reciprocal cell can be triggered at one generalized strain and reduce a different threatened extension. It does not establish an advancing shield, fracture-arrest probability, superior work-to-failure, or an advantage over optimized static prestress/reinforcement or known transformation toughening. Its load contribution and internal reserve are explicit; any physical comparison must use the same fixed-load protocol and count both. The quartic potential is a reduced snap-through model, not an acquired material law.

Reproduce the checks with `python3 check_cell.py` in this directory. The algebraic spring identities use exact fractions; the spinodal and energy ledger use double precision only to evaluate the displayed radicals.
