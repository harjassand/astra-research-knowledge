# Paid UV refinement diagnostics

The exact texture-degree construction does not itself earn Wilson occupied-charge matching. Current numerical evidence:

* Complete smooth-mass tests: failed charge matching, as recorded in MICROSCOPIC_RECONNECTION_TEST.md.
* Piecewise barycentric mass, aligned refinement r=1 and r=2, N=3r, normal thickness L=5: occupied axial charge is zero at both endpoints for M=.5,2,8. Aligned r<=2 sampling hits only vertex/edge barycentric values and misses off-diagonal cores, so these tests are underresolved.
* Shifted UV grid offset (.173,.389,.617) in UV units, r=2: Q_A=0 at both endpoints for M=.5,1,2. This samples w cores but remains rough; it is not a test of the asymptotically refined regime.

Exact charge reduction used:

H_0=diag(h,h,-h,-h), H=H_0+B V B†,
V=M[[0,U],[U†,0]] on the boundary, G=B†H_0^{-1}B.

A Schur-complement congruence gives

    n_-(H)=n_-(H_0)+n_-(-V^{-1}-G)-n_-(-V^{-1}).

G is obtained from the full finite Wilson slab using tangential Fourier modes and exact inversion of the 4L-dimensional normal-direction matrix at every momentum. No normal modes are discarded. Thus the boundary inertia calculation pays the complete occupied-orbital count. Antiperiodic x boundary conditions make H_0 invertible. The boundary matrix dimension is 16(3r)^3; r=3 already gives 11664, while r=4 gives 27648.

Max neighboring operator-norm differences ||U_x-U_y|| on shifted UV grids:

 r       endpoint a        endpoint b       mean(a)
 1       1.99622           1.99622           1.27749
 2       1.94472           1.94472            .88783
 3       1.78332           1.78330            .67530
 4       1.55443           1.55443            .54535
 6       1.47374           1.47374            .39349
 8       1.25570           1.25570            .30834

These are far from a small-gradient admissibility regime relative to an O(1) UV/bulk gap. An r=3 dense inertia run was therefore NOT launched merely to collect another underresolved point. The uniform spatial derivative estimate for the constructed texture has a finite but significant geometric constant from the barycentric subdivision. Increasing M past the bulk hopping is not a substitute for refinement: the separate full-normal-orbital test explicitly shows mirror relocation.

Resource observations: this execution machine had roughly 4 GB available when checked. A dense r=4 complex128 boundary matrix alone requires about 12.2 GB, before factorization work arrays. A root-suggested packed LAPACK Hermitian factorization could reduce copies for r=3; it cannot make that mesh scientifically sufficient. Sparse no-pivot Hermitian LU can in principle provide inertia when identical row/column permutations and U=D L† are verified; only a small random-matrix consistency test was performed, not a large production factorization.

This is a computational/resource limitation for a particular decisive test, not an impossibility claim for the physical construction. No charged lattice index theorem is supplied here. The sign convention of any eventual nonzero induced charge must also be matched to the chosen Wilson slab's boundary orientation; all current zero-versus-unit mismatches are insensitive to that convention.

## Subsequent orientation calibration

Independent source-worker analysis (reported through root) calibrated the current code's w=0 boundary: T†psi=0 selects i Gamma_5 Gamma_4=X⊗I=+1, so tangential kinetic matrices reduce to +sigma_i. This is the opposite boundary chirality from the earlier continuum patch example. The continuum induced-charge calculation for this orientation predicts Q=+s, rather than the compensating Q=-s. To test the actual compensating interface, flip the normal root orientation (Gamma_4→−Gamma_4) or use the opposite face/root, with consistent target orientation. Current numerical zeros fail either unit-sign target, so the coarse failure results remain unchanged. No later nonzero result should be compared to a sign convention that has not been calibrated.
