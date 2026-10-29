# Finite Box–Muller local sampler and common-design compiler
2026-10-29. Root-originated finite-sampler improvement; author proof/check draft, not yet independently accepted. Supersedes the Gaussian-grid proposal as the preferred route, without invalidating that slower fallback.

## Public local parameters and finite input
For rational0<nu<=1/2, set u0=nu/128, a=nu/16. Choose b by exact rational comparisons so h=2^-b<=nu*a*u0²/512. Draw16 independent pairs of b-bit integers and use their midpoint uniforms u,v in(0,1). Produce each complex entry
 z=sqrt(-log u)*(cos(2pi v)+i sin(2pi v)),
with each real component rounded to a rational at absolute error at mostnu*a/512. This is the complex Gaussian convention E|z|²=1. All constants and transcendental evaluations are known scalar computations, never operations on unknown data.

Let Ghat be this rational4×4 matrix. Compute a certified lower bound l on sigma_min(Ghat) with 0<=sigma_min(Ghat)-l<=a/16. If l<a/2, return the identity local gate. Otherwise compute the unitary polar factor Qhat=Ghat(Ghat†Ghat)^(-1/2) and synthesize it as a known two-qubit circuit to operator error at mostnu/4. All branches have a public bounded arithmetic/synthesis budget; no adaptive precision until success is assumed.

## Coupling to exact Haar U(4)
Couple each midpoint uniform to an exact uniform in its cell, so each coordinate error is at most h/2. The probability at least one of16 exact radial uniforms lies outside[u0,1-u0] is at most32u0=nu/4. On the complementary event, the interval between exact and rounded uniforms stays in[u0/2,1-u0/2] because h<=u0. The derivatives of both real Box–Muller components with respect to either uniform are bounded by10/u0² there. Indeed the radial derivative is 1/(2u sqrt(-log u)), bounded by2/u0² on that interval; the angular derivative is at most2pi sqrt(log(2/u0))<10/u0². Consequently uniform rounding gives Frobenius matrix error at most60h/u0². Arithmetic rounding of32 real components adds at most6nu*a/512. With the declared h, the total is less than nu*a/4.

For the exact complex Gaussian G, P[sigma_min(G)<=a]<=16a². Proof: a unit right singular vector has a coordinate of modulus at least1/2, so some column has distance at most2a to the span of the other columns. Conditional on those columns, its residual in their one-complex-dimensional orthogonal complement is a standard circular Gaussian; probability of norm<=2a is <=4a². Union over four columns proves the claim (dependent-column events have probability zero).

On the joint good event sigma_min(G)>a and all radial uniforms are interior, sigma_min(Ghat)>=a-nu*a/4>=7a/8. Therefore the finite lower bound l>=13a/16 exceeds a/2: every good case passes the acceptance check. The bad-event probability is at mostnu/4+16a²<=9nu/32<nu/2.

The polar map is stable here without requiring eigenvector stability. If G=QH and H>=aI, Procrustes optimality gives, for any unitary V,
 ReTr(Q†G)-ReTr(V†G)>=a||V-Q||F²/2.
Apply this to the polar maximizer Qhat of Ghat=G+E, and use its optimality for Ghat, to obtain ||Qhat-Q||F<=2||E||F/a<nu/2. Including known circuit synthesis, the implemented unitary differs from Q by at most3nu/4<nu in operator norm on the good event. The exact polar Q of G is Haar distributed by left/right invariance.

For any integer t>=1, telescoping tensor products gives unitary-channel diamond distance at most2t*nu on the good event and at most2 on the bad event. Thus the average t-copy conjugation channel differs from its exact Haar local-gate version by at most2(t+1)nu. No total-variation approximation between a discrete unitary measure and Haar measure is claimed.

## Bounded classical arithmetic
b=O(log(1/nu)). Midpoint radial uniforms lie between2^(-b-1) and1-2^(-b-1); log, square root, sin and cos on these explicit finite ranges can be evaluated by rational interval series/range reduction to O(log(1/nu)) accuracy bits with polynomial bit cost. The extra digits required near the endpoints are O(b), so no numerical-real oracle is used. For Ghat†Ghat (a4×4 rational Hermitian matrix), fixed-degree polynomial root isolation gives certified eigenvalue bounds; an additive a/16 singular-value interval suffices. This is a fixed-dimensional algebraic computation with polynomial coefficient/precision bit cost. On accepted inputs the inverse square root is conditioned by sigma_min>=a/2. Known fixed-size unitary synthesis uses additional O(log(1/nu)) precision bits. Exact-zero/degenerate algebraic branches can be resolved symbolically or safely rejected if the certified lower bound fails. These are theoretical bounded algorithms, not a claim that the diagnostic implementation below uses certified interval libraries.

## Common-design composition
Use Brandao–Harrow–Horodecki arXiv1208.0692v4 Corollary6 and Lemma3: https://arxiv.org/pdf/1208.0692v4 . For q>=2 system qubits, t copies and target diamond error0<epsilon<1, let ell=ceil(log2(4t)) and c=ceil(log2(8/epsilon)). A conservative exact integer circuit length is
 L=170000*q*ell²*t^10*(2*q*t+c).
It exceeds their Haar-two-qubit local circuit bound at design error epsilon/8, because local dimension2 and5+3.1/log(2)<10. The ideal common twirl is then within epsilon/4 in diamond norm. At each gate use the finite sampler with nu<=epsilon/[16L(t+1)]. Local hybrid errors sum to at mostepsilon/8. Uniform neighboring-location sampling uses bounded integer rejection with aggregate failure probability<=epsilon/16, charged as epsilon/8 channel error; identity fallback is permitted. The same sampled gate and location act on ALL t copies. Remaining error budget covers declared Schur/control synthesis.

## Small-irrep preparation
After large-D multiplicity extraction, prepare a single known highest-weight state in the small U(d)_lambda register, inverse small-d Schur, and apply this common design. Haar averaging replaces the irrep by its maximally mixed state while leaving multiplicity/reference correlations intact. The approximate design changes the full preparation channel by its diamond budget. Pad the small target dimension to a power of two at least4 with factor at most4; if D is too small for that embedding, D=O(d) and the direct small-dimensional branch suffices.

Together with the corrected full Schur compiler, this supplies uniform polynomial gate and classical bit-cost bounds in t,d,logD,log(1/epsilon), instead of only fixed-d GT enumeration. BHH constants and polynomial exponents are enormous. This is not an executed full design/decoder, practical speed claim, or historical novelty claim. The fixed-d compiler and earlier finite-grid construction remain fallbacks.
