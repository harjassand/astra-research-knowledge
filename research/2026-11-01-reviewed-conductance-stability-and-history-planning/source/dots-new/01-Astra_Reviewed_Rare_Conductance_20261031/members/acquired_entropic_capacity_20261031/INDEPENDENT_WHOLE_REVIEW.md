# Independent whole review: acquired entropic capacity

31 October 2026. **Scoped mathematical and executable PASS** on the final v3 source set below. This is abstract diffusion mathematics and exact declared-input computation only. No physical model calibration, sampling oracle, first-passage prediction, historical novelty or practical superiority is certified. Author originals and saved reports were preserved; execution used copied files in a temporary directory.

## 1. Exact bindings and execution

Entire current proof, implementation, verifier, tests, costs and scope sources were read. Principal bindings:

- `PROOF.md`: `9de2b84db7b432a346605b0b0f04b8737ea8424c47346c2fbb58b2684af4f291`.
- `capacity.py`: `8ff7aeebe56217463b7976b389d9931c3952a5f4e51f1f3b55d8f54e27652131`.
- `verify.py`: `7e0e57a4e2b2db4acb9d367a486c5a6f50a3ea55ea04b082c4f40b7778902843`.
- `check.py`: `07f8fed1521a9da0b1416bb99d6823af46e8f34684ed0e6950195177e001b5a7`.
- `COSTS_AND_COMPARISONS.md`: `4412569ac382a27ae2260f494a355faa8c7351f2a5a5c2ed01c347cd06bbcdaf`.
- `SOURCES_AND_SCOPE.md`: `86d33735f6bea548af030b0e6bda7336981058e6a8af6a9af4d8561056007533`.
- `README.md`: `bb72e1db7935bc74cdfe28a1a72f2d6dee5a27fcab3f0ce0c12e4bb50b003955`.

Copied final author tests passed **3,558 assertions**, including exact re-verification of all five saved scaling certificates. A separately constructed suite passed **243 checks**. Its code is `check_independent_review.py` (SHA256 `ea9692e8c8ee27383a8f040de2e3a2c8b7ea0c4e71d5a3f8b4fc8e80481a419e`), result `independent_review_checks.json` (`01a84290c5fd96b7a542029dbab9fc00c03a0876b370a0e0a84fe52e6255eff7`), and copied author replay `independent_author_replay.json` (`4fc8c21476e025189a7d2e62e77b93e73f81f6730dfd0f645de6b56a6292eec9`). The independent suite takes the source directory as its command-line argument; it does not rewrite author reports.

## 2. Actual process and observable

The SDE has locally Lipschitz polynomial drift and constant nondegenerate noise. In acquired orthogonal coordinates,

    x.grad F = sum_i [1+kappa_i(3y^4-4y²+1)] z_i².

The scalar polynomial has minimum -1/3 on y²>=0, so the generator of 1+|x|² is bounded above by a constant times 1+|x|². The stopped Lyapunov argument therefore gives nonexplosion. Integrating the Gaussian fibers gives a constant times q(y)=det(I+v(y)H)^(-1/2). Its tail is integrable; the displayed bound is valid for m>=1, and the actual parser restricts to m>=2. The smooth divergence-form diffusion is reversible with this finite Gibbs measure. Equivalently, its symmetric Dirichlet-form construction is conservative and agrees with the unique nonexplosive SDE. Uniform ellipticity/irreducibility gives the usual unique invariant component. There is no artificial reflecting wall.

The requested output is cap_mu(A,B)/mu(A), for the ACQUIRED full-fiber half-space basins. The executable does not return arbitrary-start mean hitting times, a first-hit distribution, a finite-deadline success probability, a spectral gap, or a separate normalized capacity. The field `observable` and basin/direction/beta bindings are checked by the receiving verifier. The conditional projected coordinate is generally not Markov: its generator contains z^T H z. No fast fiber-equilibration replacement is used in the proof.

## 3. Variational sandwich and actual current

For rho_y with continuity velocity w, differentiation of the conditional mean gives E[h_y+w.grad_z h]. Cauchy--Schwarz against the vector (1,w) gives the factor 1+E|w|² exactly. On full-fiber boundary sets the conditional mean has the required boundary values. The one-dimensional minimization with conductivity p/(1+K) yields the lower bound; restricting the original trial functions to h(y) yields the upper bound. These directions are correct.

The same lower bound is a legitimate finite-energy unit current: j=(rho_y,rho_y w_y) is divergence-free in the open slab, has total unit normal flux at its two faces, and resistance beta*integral(1+K)/p. The Gaussian current decays in z; it does not introduce a hidden flux at fiber infinity. Smooth truncation/Dirichlet-domain density justifies the weak identities. One may first truncate admissible h into [0,1], which does not raise its energy, before the integration-by-parts approximation.

For this family C=beta^-1(I+vH)^-1, all matrices commute. The given linear velocity satisfies C'=w_linear*C+C*w_linear^T and hence the Gaussian continuity equation. Its quadratic cost is precisely v'²/(4beta) Tr[H²(I+vH)^-3]. The root-derived Hessian acquisition supplies H and the physical projector; this current is constructed analytically, not assumed as an optimal-current oracle. The implementation need not simulate paths of that current to certify its resistance.

With p=q/Zbar, capacity bounds contain 1/(beta*Zbar*R), while mu(A)=MA/Zbar by reflection symmetry. Thus Zbar cancels, giving the displayed ratio bounds without an uncomputed normalization constant. Noise amplitude sqrt(2/beta) agrees with the beta^-1 Dirichlet-form convention.

## 4. Dimension-free estimate

Let w=1/q and S1=sum kappa/(1+kappa v). On [0,b], -w'=2y(1-y²)S1*w. The pointwise comparison

    sum kappa²/(1+kappa v)^3 <= c*S1,
    c<=1/(4(1-b²)^2)

follows from t/(1+t)^2<=1/4. Consequently K*w<=(2c/beta)y(1-y²)(-w'). Integration by parts gives the stated NEGATIVE boundary term -b(1-b²)w(b); discarding it is in the safe direction. Also 1-3y²<=1, even when it is negative on part of a larger interval. Reflection doubles numerator and denominator alike. This proves R1/R0<=1+1/[2beta(1-b²)^2], hence 1+8/(9beta) at b=1/2, for every positive heterogeneous spectrum. No dimension or stiffness maximum was silently inserted into this factor.

This is a multiplicative full-diffusion capacity certificate. At fixed positive compact fiber bounds, q(0) is exponentially small in m. The stated polynomial-width neighborhoods provide the exponential-order lower estimates for resistance and basin mass, while elementary upper estimates control the remaining logarithmic factors. The theorem does not claim the same acquisition/runtime behavior for arbitrarily ill-conditioned coefficients or arbitrary nonlinear fibers.

## 5. Raw polynomial acquisition

The current route uses the actual quadratic Hessian Q=P+H. Its one-dimensional nullspace identifies the physical direction. Normalizing the rational nullvector by its first nonzero component is harmless; the projector uu^T/(u^Tu) is exact rational and the unit direction may involve one square root. A nonsquare norm is not rejected. The full polynomial identity is then checked, not merely its Hessian or top degree. Positive LDL pivots of H+Pi establish strict positivity on the fiber. The determinant polynomial is derived from the characteristic polynomial and checked against a direct exact determinant, eliminating an ordering/normalization assumption. No eigenbasis or spectral oracle is supplied.

The sparse route checks the entire exact monomial dictionary against its claimed aligned model. Thus it is not a fast path that silently ignores lower-degree terms. Dense rotations and irrational normalized directions/positive fiber eigenvalues were independently tested. Added odd linear/cubic/quintic terms, coefficient corruption and altered external tasks were rejected. The abandoned gcd route is not a dependency or a necessary cost.

This is a sound incomplete exact-input recognizer. UNKNOWN does not prove the underlying physical problem lacks useful structure. Basins are generated by the recognized grammar, not arbitrary externally supplied basin shapes. Raw coefficient size and dense expansion/nullspace/LDL/determinant costs remain paid.

## 6. Exact interval backend and receiving

At every rational grid point, the determinant is evaluated exactly by products or rational Horner arithmetic. Integer square root of the scaled rational gives outward dyadic bounds; the floor-of-rational preprocessing does not change the floor of its square root. Endpoint Darboux sums are valid on each interval because v, q and 1/q have known monotonicity and the code splits at y=1. Reflection is used only for the resistance. The analytic mass-tail bound uses det_+(H), y²-1>=y²(1-1/T²), and the exact integral of y^-2m. Its leading coefficient is correctly acquired in both routes.

The product of positive lower/upper mass and resistance intervals gives the safe reciprocal free-rate interval; multiplying only the lower endpoint by the universal loss factor receives the full capacity ratio. The external requested quadrature ratio is checked independently by `receiving_verify`. It reacquires the raw model, direction, determinant and all integral bounds. Exact rational fields, dimension, physical basin meaning, beta, grid/precision/cutoff and loss factor are bound. Floating displays, timings and operation proxies are intentionally not evidence; their tampering cannot change the accepted exact interval.

Independent checks include exactly integrable resistance for equal two-fiber constants, rational pointwise q/w enclosures, six non-coordinate rational-projector models with unequal spectra, whole-polynomial corruption, certificate type aliases, external NaN/infinity/bool budget arguments, unresolved seed mass, and tiny-beta exact output with unavailable binary64 display.

## 7. Defects found, repaired, and preserved

The initial frozen v1 executable had three genuine boundary defects, none a wrong accepted rational interval:

1. For valid very large kappas, fixed precision could make the seed lower bound zero. The tail loop then never terminated. The repaired code explicitly rejects unresolved seed mass and caps cutoff, initial/refined grids, total points and precision.
2. A NaN `max_quad_ratio` could bypass the external tolerance comparison. The receiver now requires a positive exact task ratio at least one and strict positive integer budgets before work; the producer similarly validates its external arguments.
3. Tiny valid beta could overflow a diagnostic float conversion despite valid rational bounds. Non-proof displays now return null/status outside binary64 range; exact rationals remain. Explicit decimal serialization limits produce UNKNOWN.

The intermediate v2 Horner precheck omitted the c.numerator contribution in the bound for D*v+c. This affected a claimed intermediate-bit precheck, not exact interval validity. Final v3 includes all three numerator/denominator terms before the multiplication, with a targeted regression. v1/v2 copies are retained by the author; they do not inherit this final receipt.

`max_integer_bits` remains a determinant-product/Horner size proxy, not total peak storage or every integral/output integer. The product-bit budget likewise does not pretend to cap all symbolic acquisition or final arithmetic. Those ordinary costs are still real. Capped/fixed-precision computation can return UNKNOWN on a valid model; no universal completion or polynomial-in-bit-length guarantee for arbitrary stiffness is inferred.

## 8. Costs and ordinary alternatives

All five saved exact intervals were independently reconstructed by the receiver, including the 129-dimensional aligned sparse case near [2.2773e-18,4.3298e-18]. Its exponential rarity is not an exponential trajectory-sampling bill here. This is not a claim that generic dense 129-dimensional polynomial acquisition is equally cheap. The sparse JSON itself uses full exponent vectors, so its representation is quadratic in dimension; the proof properly pays that cost. Grid/product counts and reported timings are implementation evidence, not sampler acquisition or physical times.

Dirichlet/Thomson principles, conditional Gaussian integration, Gaussian transport/Sylvester geometry and exact rational interval arithmetic are ordinary components. Giving an ordinary comparator the newly constructed current and dimension-free estimate lets it reproduce this result; that does not establish that an existing cited paper already contains the whole new conjunction. Conversely, no bounded search establishes novelty or superiority.

I independently opened the mathematical primary body of Petersen--Lichtinger--Covino, arXiv:2608.02536v1, particularly equations3--14. Its exact flux-fidelity variational upper bound and explicit approximation replacing boundary-flux fidelity by basin averages support the author's stated comparison. This is a strong reusable-data comparator, not an automatic exact two-sided certificate for this polynomial family. No biological application was pursued. Other source-ledger primary readings are the author's scoped attributions, not all independently re-audited here.

## 9. Final scope

The accepted result is a full-diffusion equilibrium capacity/mass certificate from exact raw polynomial data, with acquired physical coordinate/metric, explicit lower current, dimension-free finite-rate loss, and a repaired exact receiving implementation. It does not supply an arbitrary-start kinetic law, a projected Markov model, a general rare-event solver, physical measurement of coefficients, experimental access, historical priority or demonstrated advantage over the strongest equally informed ordinary construction.

No further correction is required for this bound source set. Newly added `full_pde_diagnostic.py` and its floating output are explicitly OUTSIDE this receipt; they were not needed for the proof or exact receiver acceptance.
