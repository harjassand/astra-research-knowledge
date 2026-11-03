# Independent compiler audit: tensor quadrature and moving walls

2026-11-03. Read `POLYNOMIAL_QUANTUM_TERM_COMPILER.md`; delegated an independent Sections4–8 check to the thermal-source auditor (see `AUDIT_QUANTUM_COMPILER_SECTIONS4_8.md`). The initial Section3 spectator variation estimate was incorrect, but its polynomial repair is now incorporated.

Continuous and S-point Fourier compression are unital completely positive maps when S>2L'. Their complete operator norms are one. The one-coordinate block-row estimate therefore costs d=2L'+1, not the full tensor dimension. To telescope coordinates, apply the differing coordinate map FIRST to the raw function at fixed spectator angles, use its uniform slice bound, then apply all other continuous/discrete contraction maps. The maps commute because they integrate separate scalar Fourier variables. This ordering avoids confusing slice variation with variation in a spectator L-infinity norm.

The active reset compression is CC dagger with ||C||<=1. Its quadrature error is bounded by sqrt(d)(V_A+2pi L')/S, and the resulting projector error by twice that. The discrete C_S is also a contraction, since the grid Fourier columns are exactly orthonormal.

The original assertion Var_j(CC dagger)<=2 Var_j(A) was NOT justified for moving floor walls. A unitary step whose wall moves in the active angle can have finite variation on every fixed-angle slice but infinite variation as an L-infinity(active-angle)-valued function. Contraction alone cannot be used on that stronger norm.

The corrected bound is valid. Write C as the integral of the Fourier vector v(theta), of norm sqrt(d), tensored with A(theta). For any spectator partition, move its finite variation sum under the active integral and use the uniform slice variation. This gives Var_j(C)<=sqrt(d)V_A, and hence Var_j(CC dagger)<=2sqrt(d)V_A. The same argument holds for C_S. Therefore

  E_grid <=[2sqrt(d)(V_A+2pi L')
            +(p-1)d(2sqrt(d)V_A+4pi L')]/S.

The enlarged grid choice remains polynomial in p,d,V_A and inverse error, with no d^p factor. This was a real estimate correction, not merely a wording change.

For pointwise choices at simultaneous rounding walls, budget both one-sided jumps if the chosen value is not one of the two slice limits; a safe contribution is four times the unitary norm per isolated wall rather than two. This changes only a polynomial constant. Exact grid ties must use the already-declared texture wall convention so that the uniform normalization bound remains valid.

The rest of the compiler's structural claims are consistent with this correction: one active reset survives pulling the integer shear outside; complete code isometries prevent padded states from leaking into the physical block; synthesized unitaries with exact reversed gate lists preserve Hermiticity; the final integer-charge equality construction pinches the accepted block EXACTLY. Local axial cyclic averaging must use the integer cochain representative sum m cup dm and normalized integer pair projectors, rather than a fractional local density differing only after global coboundary cancellation.

Grouped polynomial evaluation has polynomial derivative/roundoff control without eigenvector conditioning. A finite-patch quadratic generator can be implemented by deliberately inefficient polynomially many pair rotations. The norm of the grouped partial sign polynomial is <=1 even for a gapless patch. Thus no hidden exponentially large one-body generator is introduced by expanding a bounded polynomial incorrectly.

The resulting ideal logical quantum block-encoding claim is polynomial at fixed microscopic parameters, after the explicit code, Hermiticity and variation repairs. It is not a polynomial classical table of the Hamiltonian, an efficient practical implementation, or a ground-preparation theorem. Ground preparation and any exposed-surface/coercive-regulator interface require their separate contracts.
