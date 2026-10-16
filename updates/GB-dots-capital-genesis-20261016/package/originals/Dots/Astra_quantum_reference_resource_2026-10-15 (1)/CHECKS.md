# Exact reproducibility checks

## Strictly positive ternary certificate

Let E be ternary erasure with reveal q=3/10 and F=T_(1/2), where T_lambda=lambda I+(1-lambda)J/3. Precompose both with N=(99/100)I+J/300. The actual compared channels in this certificate are EN and FN. The ordinary order E >= F is preserved by this common preprocessing. All entries of EN and FN are strictly positive, so every measurement effect is positive definite.

Take the rational rank-one frame

B0=[[1,2],[2,4]]/9,
B1=[[4,2],[2,1]]/9,
B2=[[4,-4],[-4,4]]/9.

These sum to I_2. Set R_i=B_i+I_2/100, H=(B0,-B1,0), and tau=103/50. Then beta=direct_sum R_i/tau and alpha=direct_sum(R_i+H_i)/tau are faithful normalized states. They are classical-quantum and separable. Their reference marginals differ. The exact source-minus-target quadratic gap is -5193535897517/393527734190500; direct Q2 evaluation gives -5193535897517/810667132432430. The negative sign disproves reference-assisted dominance despite ordinary dominance.

checks/clean_ternary_certificate.py checks all channel entries, each state’s Hermiticity and positive leading principal minors, both traces, the exact quadratic identity, and the direct Q2 gap. Every matrix and exact fraction is in checks/clean_ternary_certificate.json. The script reconstructs them and compares the full result with the fixture.

## Exact global ordinary-order certificate

For a faithful scalar input distribution r=(x,y,z)>0, x+y+z=1, and h=(h0,h1,h2) with sum h=0, source scalar RLD information is (3/10)sum h_i^2/r_i; erasure tangent vanishes. Target information is (1/2)sum h_i^2/(r_i+1/3). The difference is sum a(r_i)h_i^2 where

a(t)=(1-2t)/[10t(t+1/3)].

Restrict h2=-h0-h1. The resulting 2-by-2 matrix has diagonal a(x)+a(z), a(y)+a(z), and off-diagonal a(z).

For any x,z>0 with t=x+z<1, w=xz<=t^2/4, the numerator of a(x)+a(z), over positive denominator 10xz(x+1/3)(z+1/3), is

t^2+t/3-(10/3+2t)w >= t(1-t)(3t+2)/6 >0.

The determinant a(x)a(y)+a(x)a(z)+a(y)a(z), over the positive denominator 300xyz(x+1/3)(y+1/3)(z+1/3), has numerator

4-16(xy+xz+yz)+42xyz
=4 [sum x^3 +3xyz -sum_sym x^2 y] +6xyz >=6xyz>0.

The bracket is Schur's degree-three inequality on nonnegative x,y,z, using x+y+z=1. For completeness, sorting x>=y>=z proves Schur by

sum x(x-y)(x-z) = (x-y)[x(x-z)-y(y-z)] + z(z-x)(z-y) >=0,

where each term is nonnegative. Therefore the 2-by-2 restricted Fisher matrix is positive definite for every faithful scalar baseline. Gauge shifts h->h-c r handle arbitrary trace tangents; faithful state pairs satisfy the exact quadratic identity. Since both channels ignore input off-diagonals, this proves ordinary Petz D2 dominance for arbitrary faithful qutrit states, not merely a numerical simplex grid.


The preceding identities are checked by checks/exact_scalar_order_certificate.py. The positivity implication is the mathematical argument above, rather than an exhaustive numerical search.

## Finite reference sharpness check

checks/check_finite_reference.py verifies the projection lemma’s scalar identity and reconstructs a regularized trine example with m=4, r=2 and lambda=1/2. Its reference baseline sums to I and its total tangent trace vanishes. Exact symbolic evaluation yields

input excess = 2(13 epsilon+2)/[3(3 epsilon+2)],
target excess = 8(52 epsilon²+12 epsilon+1)/[3(8 epsilon+1)(24 epsilon+11)].

The ratio tends to 4/11 as epsilon decreases to zero. The positive regularizer makes every baseline block faithful. The general upper bound and normalized physical-state construction are in THEOREM.md. This single symbolic example is not a proof of the all-m, all-r theorem.

## Integrity

SHA256SUMS binds the handoff, theorem, audit, scripts, and fixtures. verify_all.py verifies every listed file before running the scripts. Exact computations require SymPy; the runtime version used for the packaged verification is recorded in VERIFICATION.txt. No numerical search, external data retrieval, or binary assets are required.
