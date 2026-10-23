# Symmetry check: helicity contrast misses an axisymmetric poloidal flow

**Verdict: the proposed zero-helicity-contrast witness is valid under its stated symmetry assumptions.** The decisive reflection is a meridional plane reflection `φ→−φ`, not a reflection that reverses the vessel's `z` profile. Treating magnetic induction `B` as an axial vector makes the motional term `u×B` transform correctly. The result only removes the antisymmetric circular contrast; it does not make the common impedance flow-independent or imply that a real EMS flow is poloidal.

## Port symmetry

Let the bounded vessel, scalar `σ(r,z)` and `μ(r,z)`, outer conditions, and frozen velocity

`u(r,z)=ur(r,z) er + uz(r,z) ez`, `uφ=0`,

be invariant under rotations about `z` and reflection in any plane containing `z`. Require the two source modes and the two work-conjugate readout modes to be an identical covariant transverse doublet; otherwise the terminal reduction below need not hold. The full linear induction/Maxwell equations are covariant: under an improper orthogonal map `R`, electric field, current, and velocity are polar (`v→Rv`), while magnetic induction is axial (`B→det(R)RB`). Since `(Ra)×(det(R)RB)=R(a×B)`, `u×B` is polar. Scalar material coefficients and covariantly transformed boundary/source data preserve the symmetry.

The induced 2×2 complex terminal matrix therefore commutes with the transverse rotation representation. For a continuous `SO(2)` doublet this forces `Z=aI+bJ`, `J=[[0,−1],[1,0]]`; for a real irreducible `D3` doublet, commuting with the 120° rotation gives the same commutant. A meridional reflection is represented on the transverse doublet by a matrix conjugate to `S=diag(1,−1)`; if the magnetic-pattern convention adds an overall minus sign, conjugation is unchanged. Because `SJS⁻¹=−J`, reflection invariance forces `b=0`. Thus `Z=aI` on the doublet and

`e+† Z e+ − e−† Z e− = i(Z12−Z21)=0`.

This holds for an arbitrary invariant `ur,uz`, including nonzero poloidal circulation and strain. It does **not** assert `a` equals its no-flow value: the common/trace impedance can depend on the flow. Nor does a zero contrast prove no flow; it only says this odd-under-reflection witness is blind to the symmetric poloidal class. Other port observables may still respond.

## Smooth finite-power kinematic witness

On a cylinder `0≤r≤R0`, `0≤z≤H`, choose

`ψ(r,z)=A r²(R0²−r²)² z²(H−z)²`,

and set

`ur=−(∂zψ)/r`, `uz=(∂rψ)/r`, `uφ=0`.

Axisymmetric cylindrical divergence is exactly zero:

`(1/r)∂r(r ur)+∂z uz = −(1/r)ψrz +(1/r)ψrz = 0`.

The double factors at `r=R0` and `z=0,H` make both velocity components zero on the vessel wall and endcaps. At `r=0`, `ψ=r² f(r²)g(z)` makes `ur=O(r)` and `uz` smooth in `r²`, so the Cartesian vector field is regular on the axis. For `A≠0` it is nonzero in the interior; it cannot be a rigid motion because it vanishes at the boundary, so its symmetric strain rate is nonzero. For positive Newtonian viscosity `η`, its dissipation `2η∫D:D dV` is finite and strictly positive. This is a frozen kinematic symmetry witness; no claim is made that a particular electromagnetic drive generates or sustains this exact field without finite forcing/work.

The scope consequence is only an identifiability warning: circular nonreciprocity alone cannot certify general flow or fragmentation without a prior excluding reflection-symmetric poloidal states. This does not establish that a rotating EMS lacks swirl, and it does not rule out sensitivity through common-mode impedance or other measurements.
