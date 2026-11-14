# Signed-area extension of the two-sided clean-completion obstruction

This geometric extension is coordinated with GKP's thermal failed-both-completion bound. It does NOT prove that every unavailable native path is in the stated failure class.

## Pure embedded annulus, allowing overhangs
Take two disjoint embedded axial physical phase boundaries in a proper horizontal lift of the torus cylinder. They bound a pure plus annulus Omega, of area W (number of unit spin cells) and total physical perimeter Pw. Call the left and right curves f,g, without assuming they are row graphs.

For each curve define its mean horizontal position by signed area relative to a vertical reference, equivalently the oriented integral of x dy divided by L. Write these means fbar,gbar. Because a simple essential curve separates its cylinder into left and right sides, its area mean lies between its minimum and maximum horizontal coordinates. With consistent orientation,

    W=L(gbar-fbar).

This is Green's theorem on a periodic strip. The physical square-dual contour bounds the union of spin unit cells, so its area is exactly W; zero-edge resolutions at checkerboard vertices have zero area.

Put

    A=max(f)-min(f), B=max(g)-min(g),
    a=fbar-min(f), b=max(g)-gbar.

Every essential curve has vertical variation at least L and horizontal variation at least twice its transverse span. Hence

    Pw >= 2L+2(A+B).

If the pure annulus has NO full vertical plus column, then max(f)>=min(g): otherwise every column strictly between them is contained in Omega. Therefore

    A+B >= max(g)-min(f) = a+b+W/L.

No row-convexity was used. A dual-column/spin-column half-unit convention may be absorbed in the explicit padding below, rather than suppressed.

## Two ideal clean completions
Completing to the straight periodic limit on one side has ideal area n-La, and on the other side n-Lb. Retaining a pin-safety padding of c columns subtracts at most cL from each guaranteed completed area.

For the PURE annulus, if both conservative guaranteed areas are below n/2, then

    a,b > L/2-c,
    Pw > 4L-4c+2W/L.

This describes failure of THESE conservative clean-completion area guarantees. It must not be called failure of all native paths or all possible completions.

## Thermal bookkeeping, checked against GKP's derivation
Let the actual state be the pure annulus with h interior minus-hole sites and k exterior plus-island sites, so actual plus count V=W-h+k. A conservative completion may lose at most h of its ideal plus sites. If both padded ideal areas minus h remain below majority, then

    a,b > L/2-c-h/L,
    Pw > 4L-4c+2V/L-2(h+k)/L.

If every contractible filled-wall area is at most R^2, then planar isoperimetry A_gamma<=P_gamma^2/16 gives

    h+k <= sum_gamma A_gamma <= (R/4) Pcontract.

Nested full walls only overcount this defect area, which is safe. At phi=theta/R and L=8R, the original relative weight obeys

    w(x)/w_minus
       <= exp[6 theta Pw-32 theta L+32 theta c]
          *exp[-(3/2)theta Pcontract].

Thus ordinary contractible-loop pressure has activity q=3exp[-(3/2)theta], while the two actual essential interfaces retain their explicit 3^Pw counting. GKP owns the finite receipts and full source-family statement for this application.

## Necessary limits
- The premise is absence of a full **pure-phase** column. Absence of a full actual column is weaker because holes can destroy it.
- The failure criterion uses conservative completion area minus h. It does not characterize every dynamical obstruction.
- Large contractible defects exceeding R^2 are not controlled by this pressure argument.
- The proper embedded axial annulus is essential. Multiple essential bands, other homologies and torus-spanning non-annular phase regions need separate treatment.
- Neither the physical Hamiltonian, original core nor native clock changes in this geometric comparison.
