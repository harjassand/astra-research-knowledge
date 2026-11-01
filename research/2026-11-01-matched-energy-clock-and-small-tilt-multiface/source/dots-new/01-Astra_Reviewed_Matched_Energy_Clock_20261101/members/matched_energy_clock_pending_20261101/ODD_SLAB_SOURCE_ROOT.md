# Root explicit odd-slab inverse-form source for the energy-sensitive trial

Status: NEW lemma candidate, independent review pending. This closes a source construction, not the complete matched trial/current algorithm.

Let b=1/2, v_b=1+9kappa/16 and v*=1+kappa. For any bounded r(y,z) supported in S=(-b,b) that is odd in y, nonnegative for y<0 and |r|<=1, use w=exp(-beta v(y)U(z))/Z_U and define

 j_y(y,z)=int_-b^y w(t,z)r(t,z)dt in S, zero outside;
 j_z=0.

Oddness of r and evenness of v imply integral_-b^b wr dy=0 for each z, so normal flux vanishes at BOTH boundaries. Distributional divergence is wr globally. The primitive is nonnegative; evaluating it either from the left or backwards from the right shows

 |j_y| <= b exp(-beta v_b U)/Z_U.

Unit longitudinal mobility gives full current energy

 beta int_S int j_y^2/w dz dy
 <=2 beta b^3 * [2v_b-v*]^(-alpha)
 = beta/4 * (1+kappa/8)^(-alpha).

The unknown partition cancels by homogeneity; 2v_b-v*=1+kappa/8>0. No transverse derivative, angular mixing, or source sampler is used. Finite energy and zero full mean admit the global inverse-form bound by the same current duality used in the accepted global odd construction. Compact-core/exhaustion is still the formal receiving framework, not an assumed pointwise vanishing flux at infinity.

The energy-sensitive trial h_u has h_u(-y)=1-h_u(y), so r=(2h_u-1)-(1_A-1_B) meets these conditions. Thus its changed residual source need not inherit the earlier scalar-only residual current. The bound is coarse but its price divided by the leading whole-well inverse scale M^2 beta R is exponentially small at fixed kappa as alpha grows. That relative asymptotic still requires the already received M,R estimates; this note itself is the explicit finite formula.

No claim is made here that the shifted barrier-flux well current, complete primal transverse price or final numerical error target has already been received.
