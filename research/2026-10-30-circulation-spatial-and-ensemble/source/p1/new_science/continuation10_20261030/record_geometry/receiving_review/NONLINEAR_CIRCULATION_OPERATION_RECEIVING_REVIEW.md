# Receiving review: nonlinear physical circulation operation

**Actual input.** `continuation10_20261030/NONLINEAR_CIRCULATION_OPERATION_AND_PATH_LAW.md`, SHA256 `53db4609d6b9a127c2898988a2f50684f4de7643d05c2156af516c19802a0c20`. Exact bytes are preserved in `NONLINEAR_CIRCULATION_OPERATION_AND_PATH_LAW_REVIEWED_53db4609d6b9.md` beside this review. Scope requested: Sections 2--7. The input was not edited.

**Verdict.** The main theorem in Sections 2--7 is accepted at the stated actual operation, conditional-noise, evaluator, clock and detector interfaces, with globally bounded derivatives. I reconstructed the nonlinear disturbance, both supplier connections, the spatial conservation estimate and the path-space map. No load-bearing counterexample was found. Two wording qualifications below prevent stronger claims from being inferred: the optional derivative localization needs its explicit stopping argument, and retention of the macroscopic auxiliary current is not retention of every fine controller log. Neither requires changing the central construction.

## 1. Nonlinear target and hidden native dynamics

Write `z_N(s,B)=N²[phi(s/N²,B/N²)−B/N²]`. Its time derivative is `partial_t phi`; the scaling cancels exactly. Its first spatial derivative is `D_h phi−I`, and its second derivative is `D_h² phi/N²`. Thus for any native jump v of bounded size,

\[
\Delta Z=(D_h\phi-I)v+R_N(v),\qquad
|R_N(v)|\leq C|v|^2/N^2.
\]

Compensate the complete target jumps. Native bounded drift contributes `(D_h phi−I)b`, the time term is bounded, and the compensator of the remainder is at most `C N/N²=O(1/N)`. Target jumps remain uniformly bounded and occur only at native jump times. Its martingale exponential bound therefore has the same `O(N)` coefficient. No assumption that native observations form a Markov state is needed. A finite-dimensional unknown generator is not being inferred.

The reasoning requires the native drift and jump-intensity bounds in the actual joint experiment, after permitted history conditioning. Merely knowing separate unconditional marginal statistics would not suffice. The draft explicitly states the actual deployment interface and isolation; I receive it at that scope.

The separate native and auxiliary counters are real operations. A detector reading only total composite current would not automatically supply the target. The evaluator qualification in Section 3 correctly excludes treating an arbitrary noncomputable smooth function as a supplied operation. Its rational nonlinear examples have bounded first and second derivatives and admit the stated finite arithmetic implementation on the polynomial counter range.

## 2. Queue interface and actual carrier suppliers

For bounded-rate carriers the opposing force gives a drift of magnitude between `2c_-R sinh(a/2)` and `2c_+R sinh(a/2)`. The actual total activity is `O(R)`, so combining it with the compensated target gives the queue's `O(N)` noise bound. The same outgoing prefactor is essential; generic spatially reciprocal conductances are properly excluded. Hidden causal clock variation within the stated bounds is harmless.

For the mechanical supplier, use the true measured error `E=A−Z` and the mathematical corrected error `X=E+(P−P0)/g`. The exact period cell gives inward drift `R beta²a/2` and fresh Gaussian innovation `−beta Y`, in addition to the target increment. The decision filtration excludes that unread incoming source. Revealing it to select the force would invalidate the martingale assertion. Endpoints and within-period motion are controlled by the explicit supplier formulas, not silently omitted from physical current.

Different lanes can have different gains, noise levels and periods. Apply the scalar theorem at each lane's own period boundaries and use the bounded-jump/explicit within-period estimates. No equal-mobility or noise-cancellation premise remains. The finite-duration readout note's extra relative-energy envelope is correctly acknowledged; force conservation alone would not bound staggered local measurements of arbitrarily energetic relative motion.

The delay/capacity conditions suffice: `K_N→infinity`, `K_N d_N=o(N²)` and `eta_N=o(N²)` permit an inward exponential supermartingale after short-window excursions are excluded. The queue stops at the first observation or window failure, rather than conditioning on a future success event. The two resulting exponents have orders `N⁴/[N d_N+N²]` and `K_N N`; both divided by N diverge in the stated regime. Whole-horizon failure probabilities must be superexponential, as the draft states.

## 3. Complete spatial current and topology

For the discrete embedding, the derivative of the piecewise constant `J_i/N` has atom `(J_i−J_(i−1))/N` at site i. Discrete conservation makes it exactly minus the density change. Its mean is `sum_i J_i/N²`, as required. There is no missing factor of N.

For mechanical carriers, differentiating a periodic test function along actual particle motion gives

\[
\langle\nu(t)-\nu(0),\psi\rangle
=N^{-2}\sum_l\int_0^{N^2t}\psi'(X_l(s)/N)dX_l(s)
=\langle Y(t),\psi'\rangle.
\]

The same conservation law therefore holds for the actual continuous displacement. The total added density is deterministically `R/N`, whatever the initial positions or later windings. For a mean-zero test f, its periodic primitive psi bounds the centered current by `2(R/N)||psi||_infinity`. The H^(-s) estimate for `s>3/2` follows immediately and holds simultaneously for every time and every realization.

The stronger total-variation fact needed when comparing weak measure topologies is also available: in one dimension the periodic primitive of a signed zero-mass measure is a bounded-variation function; after subtracting its mean, its sup norm is bounded by the variation of that measure. Here the bound is `2R/N`. The native version is bounded by a fixed constant when native empirical mass is at most one. Consequently all relevant current total variations are bounded by their mean magnitudes plus these deterministic constants. In the phrase “on bounded sets,” the appropriate boundedness is total variation, not merely a negative-Sobolev norm.

Use the joint J1 space over the product of the negative-Sobolev coordinate spaces, rather than a product with unrelated time changes. The mean is a continuous linear functional. Along a common Skorokhod time change, bounded spatial derivatives and the time derivative of phi control the change in (19); thus the time-dependent map is continuous. Uniform-in-time spatial discrepancies from density, centered current and servo error dominate the joint J1 metric. This establishes exponential equivalence of the full tuple in (20), not merely its endpoints.

The edge-atomic/current-step replacement is also sound. Pairing against an H^s test with `s>3/2` costs at most `C_s(1+sup|h_N|)/N`. The native bounded-drift/intensity assumption makes `sup|h_N|>cN` superexponentially rare: the required martingale excursion is of order N³, with quadratic compensator O(N³), and the bounded-jump exponential inequality has an exponent of order N³. This is sufficient for any fixed metric threshold.

## 4. Non-Gaussian contraction and conditional records

Once a good native LDP in the compatible geometry is genuinely supplied, the continuous mapping theorem and exponential equivalence yield (21). Nothing in bounded aggregate drift/intensity alone supplies that native LDP. The draft says so explicitly.

Density-rate preservation follows exactly: the operation leaves the density coordinate fixed, and every native current has an output. Thus minimizing over all outputs gives the same infimum over native currents as before. The joint output-plus-auxiliary-current map retains the original macroscopic native current because `W_native=W_out−Y`. This is an actual counted-current distinction from a passive native-current constraint.

Uniform conditional tracking estimates survive mixtures. An LDP for one fixed hidden native clock is not automatically the LDP of an arbitrary clock mixture, and a conditional calibration guarantee is not a posterior guarantee for every selected record. The draft retains these qualifications. It also correctly declines to claim total-variation closeness of all fine detector logs to an artificial projected apparatus.

For maximal precision, replace the broad sentence “no controller information or dissipation is erased” by “the macroscopic native-current information is recoverable when the auxiliary current is retained; the marginal contraction does not price the controller's dissipation.” The existing following paragraph already excludes fine logs, so this is a wording clarification, not a mathematical counterexample to (20)--(21).

## 5. Concrete completion of the optional derivative localization

The theorem is proved as written with globally bounded derivatives. Its optional sentence about an exponentially tight domain should use the following argument rather than simply adding one exponentially small failure probability to a superexponential claim.

Stop at `tau_L=inf{t:|h_N(t)|>L}`. On the compact range `|h|<=L+1`, the fixed smooth map has derivative bounds C_L; the target and queue proof apply until this stopping time. For every fixed L, their remaining error is superexponential in N. The native martingale estimate gives

\[
\lim_{L\to\infty}\limsup_{N\to\infty}
N^{-1}\log\Pr\{\tau_L\leq T\}=-\infty.
\]

First take the N-limit with L fixed, then let L grow. This recovers exponential equivalence. Evaluation and sensing guarantees must similarly be available on each fixed compact range, uniformly in N; their failure enters the same stopped argument. If only one compact domain with an `exp(−cN)` exit bound is warranted, the superexponential conclusion does not follow. The displayed native interface itself supplies the increasing-domain estimate above, so the repair is available without a new physical actuator.

## 6. Boundary of this review

Sections 2--7 pass at the stated interfaces. No fresh numerical fixture was needed for the stopping-time, conservation or continuous-map arguments. The root's Section 8 fluctuation/force-limit statements are separate receiving claims. In particular, the large-deviation tracking bound `E=o(N²)` does not by itself imply `E=o(N^(3/2))` at a central-limit scale. A leading covariance `Q M Q` for a specific always-active linear governor needs its finer tracking proof. The draft's companion force-limit construction is the proper place to establish or restrict that statement.

The whole theorem remains an active composite-conductor operation with additional actual carriers, detection, storage, clocking, communication, power and source preparation. It is not a same-port passive theorem or an apparatus-cost certificate. No novelty claim is received.
