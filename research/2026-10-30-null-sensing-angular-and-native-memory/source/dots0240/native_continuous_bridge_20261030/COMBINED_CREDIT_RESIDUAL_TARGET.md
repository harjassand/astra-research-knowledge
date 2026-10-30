# Combined exact native credits: the remaining positive term
2026-10-30. Composition note for the independently scoped committed credit and dirty-history credit. Use the accepted slow-acquisition/cleanup instance; the separately reviewed fast-cleanup extension, if accepted, changes only rate accounting.

Let T_G,h be the good committed credit and T_B,h the bad-history erasure credit. Their nontrivial source sectors are orthogonal, and the erasure output Q0 activates neither. They commute as full CP channels, not only on V. All owner credits commute with one another and with exterior nominal generator terms by the proved ownership/private-register algebra. Set

    T_h=T_G,h T_B,h,    T=product_h T_h,    F=T(V).

At a fixed owner h, the observable is exactly piecewise

    good C:  Phi_h^* V_0 + S_G,h (V_0-Phi_h^*V_0),
    bad:     V_0 + S_B,h (V_1-V_0),
    good A/Q: V_0,

where V_0/V_1 set only h's actual flag to zero/one. Dirty commitment targets the first line, which is no larger than V_0, so it can only improve the bad-sector killed calculation. No dirty-source d_h is substituted for a cleared-target decrement.

With D_h the actual good committed projector and Delta_h=V_1-V_0, the accepted source calculations give constants gamma_G,gamma_B>0 and

    L_native^* F <= -gamma sum_h T_(not h)(D_h d_h+B_h Delta_h),
    gamma=min(gamma_G,gamma_B),

plus additional negative endpoint and clean-commitment terms. Both local target observables satisfy

    T_h(D_h d_h)<=D_h d_h,
    T_h(B_h Delta_h)<=B_h Delta_h,

because their credited jump branch exits the target subspace and the survival coefficient is <=I. Hence

    L_native^*F <= -gamma T(sum_h D_h d_h+B_h Delta_h).       (1)

This is an exact generator inequality with no effective jump process or accumulated simulation error.

The augmented full-animal argument gives

    W <= C_cov [sum_h d_h + sum_h B_h Delta_h]+C_vac N.

Local completion by all h tokens gives B_h d_h<=C_loc B_h Delta_h. Define the UNPAID clean uncommitted demand

    U=sum_h (I-B_h-D_h) d_h.

Since D_h<=I-B_h and all these source factors commute with d_h, U>=0. Adjusting constants,

    W <= C [sum_h D_h d_h+B_h Delta_h+U]+C' N.

Applying T and combining with (1) yields the precise residual inequality

    L_native^*F <= -(gamma/C) T(W)+gamma T(U)+bN.             (2)

The generic local/common-bath noise transfer is N^*F<=eta C_noise T(W). The CP circuit, raw-basin commutation, two-weight lower barrier, and fixed encoded initialization therefore already have the correct form. What remains is to absorb **T(U)** by a genuine native clean-acquisition/cleanup service mechanism. Setting U=0, replacing it by an average reset rate, or using a fixed-horizon average would be an unjustified promotion.

Equation (2) is a reduction of the remaining proof obligation, not the missing theorem. U includes consistent A/Q clocks and clean partial ownership, so no existing bad-history token charge applies to it. The separate weak-initiation branch is attempting a revised apparatus that handles this term.
