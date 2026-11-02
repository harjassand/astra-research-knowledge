# Acquired bounded-buffer transport of the normal-cell reference deficit

This supplements the finite-conformal-generator transport already proved in POWER_BALANCE_AND_CONSERVATIVE_QUOTIENT.md. Here a simpler direct comparison is sufficient, because the normal-cell reference maximizers are proved interior. It is not a supplied neighboring-profile law.

Write tau_(i,j)=y_i+z_j and set the fixed vector

    zeta=(0,0,0,0,log(2)/4,log(2)/4), so zeta.w=log2.

The normal-cell weight has

    -log mu(i,j,k)=E_(i,j)(x)+zeta.rho,
    E_(i,j)(x)=sum log(x_l!)-zeta.x
                  +log(alpha_i beta_j)+zeta.tau_(i,j).

Thus its deficit relative to the cell maximum is exactly E_(i,j)(x)-min_cell E. The arbitrary choice of base rho and fiber index cancels.

At a neutral or repaying unexpected source the next actual anchors are again <=3. The new residual cell differs from the old one by one of the FIXED hidden buffers

    e_B-e_C, -e_B, -e_C,

or their peer analogues. Anchors of the residual remain zero. For bounded hidden-pair differences, the reference-barrier proof places every cell minimizer at hidden counts at least delta N for large N. Consequently adding any of those bounded buffers to a minimizing node, while keeping its phase, produces a valid node of the adjacent cell. The converse comparison uses the adjacent cell's minimizing node and the negative buffer. Every factorial increment in these comparisons is bounded by C log(N+15); the linear tilt changes by a constant. Therefore

    |min_cell' E-min_cell E|<=C log(N+15).

The actual enabled raw jump has bounded coordinate increments, so its factorial-energy change is also at most C log(N+15) in absolute value. There are finitely many phase coefficients. Combining the two estimates gives

    |deficit(actual output,new cell)-deficit(prejump,old cell)|
        <=C log(N+15).

This proves the receiving comparison used for a fixed number of central episodes. The constants and interior threshold are acquired from the fixed raw list and the admitted pair-difference bound. Nothing here asserts a uniform global transport bound when those differences grow without the stated interior control.
