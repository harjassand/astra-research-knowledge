# Two rotation programs to FOUR spinor programs

Additive strengthening, separate from the frozen two-output v1. Independent receiving review requested.

Let R(q) be the nine homogeneous quadratic rotation polynomials in quaternion coordinates, and let z4(q) list all35 degree-four monomials. Construct the exact35×81 coefficient matrix M satisfying vec(R(q))^tensor2=M^T z4(q). Exact rank is35. Therefore
 B=(MM^T)^(-1)M
is a rational left inverse: BM^T=I35. Let J map z4(q) to the256 ordered tensor entries of q^tensor4 by repeating each monomial in its appropriate tensor positions. Define T=JB, an explicitly specified known256×81 rational operator. Then
 T vec(R(q))^tensor2=q^tensor4
as an exact homogeneous polynomial identity for all q, not merely a floating fit on unit quaternions.

The multiplicity of monomial alpha is4!/prod_i alpha_i!, so F=T^dagger T=B^T diag(multiplicities) B. Exact rational computation yields its full spectrum:
 0 (multiplicity46), 1/16 (25), 1/8 (1), 3/16 (9).
Consequently K=(4/sqrt(3))T is a valid Kraus contraction. On two normalized rotation programs c=vec(R)/sqrt(3),
 K(c tensor c) = 4/(3sqrt(3)) q^tensor4.
The exact success probability is16/27, producing FOUR pure quaternion programs, each usable through the known Bell-basis conversion. The SU(2) sign ambiguity disappears in q^tensor4. A purely rational, more conservative Kraus operator2T succeeds with probability4/9.

The complete matrix is determined by the exact B matrix, exponent list and multiplicity list in certificate.json; J is the explicit ordered-tensor monomial repetition rule. No optimization oracle, source inverse or arbitrary SDP rounding is assumed. As in v1, physical realization uses a known finite-dimensional Stinespring dilation of this contraction, with all preparation/control/finite-precision costs paid. This is not a native-hardware demonstration.

This strictly improves the number of available spinor programs and conditional success of the simple v1 map. It does NOT improve the often-vanishing or tiny exterior-program acquisition probability. It does not prove optimality among all programmable processors. Each standard single-outcome gate-teleportation use still pays its own success1/4, unless a separately proved multi-program retrieval construction is supplied. Failed gate attempts are not freely reversible and may damage an unknown input.

The exact full-memory support and pure-program decoupling assumptions are inherited from v1 with its support-wording erratum. No iid assumption, robust approximate symmetry, positive occupation gap, or practical yield is added. This is a finite linear-algebraic program conversion, not a claim that classical environment tomography has been avoided without paying quantum-record/coherence resources.
