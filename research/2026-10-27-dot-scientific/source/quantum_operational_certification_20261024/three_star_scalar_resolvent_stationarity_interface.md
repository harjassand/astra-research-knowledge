# Scalar constrained resolvent form for the remaining pure-success three-block source

This is an exact source-compatible interface, not a positivity theorem. It follows from the dual blocks in `three_block_pure_success_dual_star_interface.md`. All x_i,c_i,p are interior, d=p/3, b_i=x_i/3, and

u_i(s)=d-c_i^2/[3(b_i+s)], U(s)=sum_i u_i(s).

Thus 0<u_i(s)<=d, u_i increases with s, and u_i(0)=d(1-r_i). Define

G_s(u;d)=-3 sum_i log[(u_i+3s)/(d+3s)]
          -log[(sum_i u_i+s)/(3d+s)]
          +2 sum_{i<j} log[(u_i+u_j+2s)/(2d+2s)].

Then the actual homogeneous deficit is exactly

Delta=integral_0^infinity G_s(u(s);d) ds.                  (1)

Proof: factor the input 2x2, reference arrowhead and output 3x3 determinants using their scalar central Schur complements. Subtract the zero-deficit c=0 source. The overlap entropy formula is minus the integrated logarithmic determinant ratio. In each input integral substitute its original resolvent parameter by 3s. This supplies the coefficient -3 in (1); the reference and normalized WH pair terms remain at s. No relation between the logical Gram phases is needed: the actual source spectrum has already eliminated them.

Differentiation gives the exact overlap stationarity equations

(1/(2c_i)) partial_{c_i} Delta = integral_0^infinity [1/(b_i+s)]
 {1/(u_i+3s)+1/[3(U+s)]-(2/3)sum_{j!=i}1/(u_i+u_j+2s)} ds.       (2)

At fixed d,c, the weight derivatives are

partial_{b_i} Delta=(c_i^2/3) integral_0^infinity [partial_{u_i}G_s]/(b_i+s)^2 ds.    (3)

The physical constraint is sum_i b_i=q/3, so an interior minimum at fixed p must satisfy all three equations (2)=0 and equality of the three expressions (3). Formula (3) is in b_i coordinates, not x_i; their derivatives differ by factor three.

One must retain the Möbius constraints on u_i(s). Treating u_i as freely variable at each s loses the actual source. In particular G_s is not pointwise nonnegative: when u_i=u<d<s, its equal-coordinate derivative is positive, so G_s(u,u,u;d)<0. Consequently (1) needs an integrated compensating argument, not pointwise scalar positivity. The already-received uniform-weight balancing theorem is consistent with this obstruction.

Together with `three_block_pure_success_boundary_stationarity_reduction.md`, these equations describe every possible negative minimum at fixed p. No global stationary exclusion is asserted here.
