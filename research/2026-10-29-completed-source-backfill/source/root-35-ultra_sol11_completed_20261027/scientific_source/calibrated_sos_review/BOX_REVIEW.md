# Independent whole-box review: ACCEPTED

Whole-read inputs: `../smooth_conic_interface/PROOF.md`, including its
reusable strict-input contract and both Slater points; `EXPLICIT_BOX.md`;
and the full coefficient-bound and square-completion implementation in
`local_evaluator.py`. Parent already independently reconstructed the two
actual70 query certificates. This review does not repeat those queries.

`check_box_bounds.py` instead independently rebuilds the UNIFORM cube
calculation without importing producer code. It takes the literal frozen
quartic/p6 input, reconstructs H,pH,D and the six affine-in-query coefficient
polynomials of N, and uses direct binomial sums after A=a+Y. In a fixed
Y-monomial coefficient, the zero-anchor/zero-query N0 term is removed
EXACTLY before absolute bounds. Each remaining monomial contributes its
absolute coefficient times ra^(anchor degree), rb^(B degree), rs^(s degree).
This also bounds |ell_a(z)| by |N(a,z)|/sigma^2. The D-shift coefficient
bound multiplies that value bound. Thus no rational denominator is treated
as an exact constant away from zero.

The Gram right inverse is independently rebuilt from all490 monomials
of degrees2–8 and all69 feature pairs. For each monomial the pairs with
maximal d_i d_j are retained and share the correction equally. Diagonal
entries receive the full coefficient; symmetric off-diagonals receive half.
The scaled symmetric matrix's operator norm is at most its maximum
absolute row sum. The independent result is EXACTLY

    rho=69249540579711104218703/155675520000000000000000
       <9/20<1/2.

Combined with the separately exact base-block LDL bounds from the source,
this proves Q>(1/2)diag(d_i^2) throughout the declared coefficient cube.
The new review independently reconstructs rho and all bound weights; it
does not claim a second numerical replay of the source base blocks, already
independently consumed by parent.

The derivative bound is also correct. For k=pH/(T+sigma)^2, ordinary
coefficient-l1 degree-six estimates give

    |k|<=P r^6/sigma^2,
    |Dk|<=6P r^5/sigma^2+4P r^7/sigma^3,
    ||D2k||<=30P r^4/sigma^2+52P r^6/sigma^3
                                      +24P r^8/sigma^4.

The52 is48 from the two gradp/A product terms plus4 from the scalar
identity term. With R=s+q(a)-cofa:B, |R|<=rs+r^2/2+r*bnorm,
||DR||<=r+bnorm and ||D2R||=1. Differentiating ell gives exactly the
displayed source Hessian-deviation bound. Our independent reconstruction
matches its rational value and obtains approximately2.662348473e-6<e.

Root existence uses the Euclidean anchor ball r=1/4000, not the larger
coordinate cube. On that ball Hessell<=-eI, while gradell(0,z)=2eB.
The query cube implies ||B||<=2/32000=r/4. Consequently the outward
radial derivative on ||a||=r is at most2e||B||r-er^2<0; a maximum lies
strictly inside. Strict concavity gives one stationary maximizer in the
ball and ||a||<=2||B||<=r/2. IFT and uniqueness patch the analytic branch
throughout the open query box. Its PD69 certificate makes it the global
contact maximum and the finite SOS value. This is not an assumption that
a floating Newton iteration found every possible critical point.

Square completion is exact. The coefficient2l is-D(a)grad_A ell_a(z).
After reserving b|Y|^2 from Q, the square b|Y+l/b|^2 adds |l|^2/b.
The chosen eta=2|l|^2/(sigma^2 b) cancels this with the subtracted
eta sigma^2/2 term. D(a+Y)-sigma^2/2 is SOS whenever |a|^2<=sigma/4.
The full coefficient cube already implies this because4ra^2<=sigma/4.
Thus the evaluator does not trust Newton convergence or floating accuracy.

Both new Slater claims check. The rank69 graph Gram's full70 kernel is
span(v4(B)); distinct graph points have nonproportional evaluation vectors.
Their positive average gives a strictly PD primal Gram at their mean query.
Y=diag(1,s-detB) always supplies distinct points, including a rank-one Y
on the graph. A full Gaussian moment functional normalized by its positive
expectation of D has PD M4 and satisfies L(D)=1, so dual Slater also holds.

The explicit domain is accepted exactly as written:

    |B_i|<1/32000, i=0,...,3, and |s|<1/10000.

It is a full-dimensional open neighborhood of the origin, not a uniform
tube around the whole unit matrix ball. The general theorem separately
gives qualitative analytic neighborhoods of every graph point. No smoothness
outside their union or generic solver speed is inferred.

Independent uniform-bound replay took0.260178s including scientific imports
and literal input loading, excluding interpreter startup. No new SDP or
finite-query acquisition ran. Full exact output is in `BOX_REPLAY.json`.
