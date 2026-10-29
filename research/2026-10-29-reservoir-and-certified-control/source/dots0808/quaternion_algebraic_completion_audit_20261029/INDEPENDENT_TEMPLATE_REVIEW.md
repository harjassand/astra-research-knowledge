# Independent review: fixed-template perturbative quartic oracle
2026-10-29. Theoretical expected-bit construction; the large universal template is not implemented by this packet.

## Decision and exact scope
Accepted as a mathematical fixed-template algorithm for a rational quartic in four variables: almost surely return an exactly rational unit quaternion and a rational global lower bound within any requested positive rational additive tolerance, with expected bit cost polynomial in the input and accuracy bit lengths. The constants can be astronomical. The optional cap-plus-complete-grid composition is valid as a mathematical totalization rule once an actual worst-case grid bit-operation bound is supplied.

This is NOT acceptance of a generally fast implemented algebraic solver, a polynomial worst-case source-clock schedule, a generic success guarantee for the separate fixed-z Gröbner scripts, the running perturbed Choi–Lam experiment, an online quantum advantage, control-error tolerance, or a novelty claim. Expected computation time cannot be exchanged for metadata-hidden physical source time without the stated additional interface.

## Primary prerequisites actually read
I read the relevant primary passages, not only search summaries:
- Sodomaco, arXiv:1802.10173v2, https://arxiv.org/pdf/1802.10173 : Propositions2.1–2.2 (resultant existence/zero locus and multidegrees), Definition1.2, Theorem3.8, Proposition3.11, and the leading/isotropic discussion in Section4.
- Cartwright–Sturmfels, arXiv:1004.4953v2, https://arxiv.org/pdf/1004.4953 : Theorems1.2 and5.5 and their stated generic scope.

The needed established inputs are the homogeneous resultant property, its block multidegrees, generic40 distinct normalized eigenvalues for four-variable quartics, and coefficient degrees108−j of the restricted resultant. The new receiving derivations below do not assume a generic smooth-resultant criterion, reduced critical ideal, or a general Gröbner bit-complexity theorem.

## Nonzero bad polynomial and finite sampling
The universal resultant of four cubics has degree27 per independent coefficient block and total108. Restriction to `(partial_i F)/4−lambda Qq_i` has generic degree40. Since coefficients of higher powers vanish on a dense open family, they vanish identically on the quartic family. Generic distinctness makes `c40 Disc(R)` a nonzero polynomial.

The discriminant of degree40 has total coefficient degree78 and index-weighted degree1560. Substituting the homogeneous degree108−j of c_j therefore gives degree6864; adding c40 contributes68. The ternary boundary resultant of degrees3,4,4 has block degrees16,12,12, hence quartic-coefficient degree40. Its three-polynomial system is sufficient to contain every boundary eigenray; additional zeros merely cause conservative rejection.

I independently reran the concrete boundary nonzero witness with a different exact Gröbner method (Buchberger instead of f5b). Each of the three projective charts gives the unit ideal. Thus this boundary polynomial is not identically zero. Its witness need not also witness the other factors: an integral polynomial ring has no zero divisors. The product bad polynomial is nonzero and has degree at most6972.

Independent perturbations on the stated16384-point rational grid in all35 coefficients are an invertible affine substitution of that nonzero polynomial. Polynomial zero counting gives failure at most6972/16384<1/2 uniformly for every input. The perturbation l1 norm is at most epsilon/4; unit-sphere monomials have magnitude≤1, so the objective changes uniformly by no more than that amount. Each attempt uses exactly490 private random bits, not continuous randomness. Repeat-until-success is almost surely terminating with finite expectation, not terminating on every possible infinite random tape.

## Simple restricted roots identify unique projective rays: complete proof
Fix independent cubic coefficients a and a common projective root q. The linear coefficient subspace L_q consists of all four tuples of cubics vanishing at q. The universal resultant vanishes identically on L_q. Since the current coefficient tuple lies in L_q, its differential annihilates L_q. Therefore, in each coefficient block i, its gradient has the form beta_i(q) times the degree-three monomial evaluation vector at q.

At a simple lambda-root of the restricted resultant, the chain rule implies that the universal gradient is nonzero. Choose a nonzero coefficient block. If two distinct common rays q,r existed, that same block would be proportional to both monomial evaluation vectors. Choose a coordinate k with q_k nonzero. Its pure cube entry forces r_k nonzero, and ratios of the q_k²q_j entries to q_k³ recover every q_j/q_k. Hence the two rays coincide. This excludes positive-dimensional fibers as well as multiple distinct points; it does not assert scheme reducedness and does not need to.

There is no hidden isotropic common root. If Q(q)=0 and all restricted cubics vanish at one lambda, then gradient F(q)=0. The same q would be a common root for every lambda, forcing R identically zero, contrary to c40 nonzero. Thus all roots represented by R are nonisotropic. This argument avoids any additional smooth-quartic factor. Isotropic eigenrays with nonzero proportional gradient need not be discussed as global real-sphere candidates.

Boundary resultant nonzero ensures q0 is nonzero at every such root. With real coefficients and real lambda, conjugation preserves the unique projective ray; its q0=1 representative is consequently real. Conversely each real sphere stationary point supplies a real R root, and Euler's identity gives its objective equal to lambda. Therefore the smallest real root is the global sphere minimum of F. A real minimum exists by compactness, so the real-root list cannot be empty on a good trial.

## Constructive primitive coordinates
All derivatives must be taken with respect to the80 INDEPENDENT cubic coefficients of the universal resultant before restricting them to quartic-gradient coefficients. Derivatives only in the35 quartic directions would not supply the claimed evaluation blocks.

At a root, A_i (pure q0³ derivative) equals beta_i q0³ and B_ij (q0²q_j derivative) equals beta_i q0²q_j. Some A_i is nonzero. Therefore R,A_0,...,A_3 have no common root, and extended Euclid supplies rational polynomials b_i with sum b_i A_i=1 modulo R. The degree<40 polynomials `X_j=sum b_i B_ij mod R` evaluate to q_j/q0 at EVERY root. No root-dependent choice of a gradient block, fixed-z separation assumption, or critical-ideal radicality is required.

An independent executed binary quartic test builds the full two-cubic universal resultant, differentiates it before substitution, applies this multi-polynomial Bezout extraction, and verifies both original cubics vanish modulo R. It also verifies the normalized objective equals lambda. This tests the algebraic mechanism in a small exactly implemented case; it is not execution of the four-cubic quaternion template.

## Bit-cost justification without a generic Gröbner claim
The universal polynomial and its derivatives are fixed finite integer polynomials. A finite symbolic-elimination preprocessing algorithm can construct them independently of the eventual rational input; this is a fixed, potentially enormous overhead, not an optimizer oracle. Evaluating them and the boundary polynomial is a fixed finite collection of rational polynomial operations. After denominators are cleared, all coefficient bit heights are O(B+constant) for input/accuracy bit length B, with large fixed degree-dependent constants.

R has degree40; coefficient-derivative polynomials have degree at most107 in lambda. Polynomial reduction and extended Euclid are bounded-degree rational linear-algebra calculations, with polynomial bit heights. For a squarefree integer polynomial p of fixed degree D and coefficient height H, Cauchy's bound gives root magnitudes≤1+H. Since its nonzero integer discriminant has absolute value≥1,
`1 <= |leading(p)|^(2D−2) * delta² * [2(1+H)]^(D(D−1)−2)`
for its smallest pairwise root separation delta. Thus delta≥2^{-O(log H)} at fixed D. Exact Sturm isolation with adaptive subdivision therefore uses polynomially many bit operations, rather than a uniform exponentially fine grid. Rational roots/endpoints can be handled exactly.

The coordinate polynomials have fixed degree and polynomial-height coefficients. Their values and derivatives on bounded root intervals have at most exponential magnitude in B, so polynomially many precision bits suffice. Normalize `(1,X_1,X_2,X_3)` with its positive square root, then approximate its stereographic coordinates rationally. The normalized first coordinate is positive, so the stereographic denominator is at least1; no unbudgeted pole is present. A quartic with coefficient l1 norm A is4A-Lipschitz on the unit ball. Refinement to O(B+log(1/epsilon)) bits thus yields a rational unit quaternion with certified perturbed-objective error≤epsilon/2. Returning the perturbed lower bound minus the exact perturbation l1 bound gives the original-objective contract, with total gap≤epsilon.

## Termination, clock and implementation limits
Each retry has uniformly bounded polynomial bit cost and success probability>1/2, so the almost-sure algorithm has expected polynomial bit cost. A fixed retry cap alone can fail in a candidate-dependent way and is not a neutral guard abort. If failure invokes a complete deterministic grid fallback of known bit cost bound W_net, K≥ceil(log2 W_net) makes its expected extra work≤1. Since log W_net is polynomial in input/accuracy bit lengths, this composition is valid in principle. No concrete W_net, totalization implementation, or physical padding budget is supplied here.

Worst-case runtime can still include the very large grid, and expected runtime does not hide candidate-dependent elapsed time from an adaptive source. The source-clock/privacy requirement, physical control precision, and equally informed conventional comparator remain unchanged. The universal template and extractor are not implemented in four variables in this packet, so no empirical speed or quantum throughput claim follows from the theorem.
