# Exact finite-temperature rod expansion for the dressed clock model

2026-11-01. Independent mathematical derivation, incorporating the parent's excursion representation and checking it against a primary continuum cluster theorem. This proves the ancillary free-energy lemma for the EXACT signed-clock Hamiltonian described below. It does not establish the native model's complete memory/dynamics theorem or replace the actual-code binding.

## 0. Result

Let a finite set of seven-state clocks have overlap graph of degree at most D and physical edge length at most R. The Hamiltonian is the exact dressing of the constructor's Pauli-clock Hamiltonian: each clock has energy Delta at levels 1,...,6 and zero at level 0; nearest-neighbor hopping around its seven-cycle has magnitude t; hopping matrix elements have the pairwise Pauli gauge signs derived in Section 1 and wrapping edges additionally carry an external sign s_g. All clocks, including their real thermal excitations, are traced. Put B=beta Delta and epsilon=t/Delta>=0.

For every fixed desired physical locality weight mu, there are explicitly selectable constants rho>0 and B0<infinity depending only on D,R,mu, such that, for 0<=epsilon<=rho and B>=B0,

    F_beta(s) := -beta^(-1) log Tr exp[-beta H_a(s)]
      = c_beta - J0 sum_g s_g + sum_(nonempty A) r_A(beta,t) product_(g in A) s_g,
    J0 = 2 Delta epsilon^7,

with an absolutely convergent, volume- and flux-uniform potential and

    sup_g sum_(A contains g) |r_A| exp[mu diam(A)]
      <= M0 Delta (epsilon/rho)^9
         + J0 exp(-B)[P5(B)+6+12D],                 (T)
    P5(B)=sum_(j=0)^5 B^j/j!.

M0 is a fixed constant, for example the coarse choice in Section 4. Thus the relative error is O(epsilon^2)+O(poly(B)e^-B), with constants depending on the fixed graph/locality parameters. A weaker O(Delta(C epsilon)^8)+(C/beta)e^-cB bound follows as well. If desired, choose B large enough that the thermal term is at most epsilon^2 J0. There is no upper bound on beta t and no assumption that all clocks are in their vacuum.

The same result holds on finite subgraphs with ordinary free/open or periodic boundaries, with the same degree/range bounds. It does NOT claim that arbitrarily pinned excited boundary clocks leave the uniform leading coupling unchanged; such pins can reverse a neighboring loop sign.

The more precise order-seven coefficient is site-dependent only through thermally excited spectators:

    J_g,7(beta,t)=J0 * [1-e^-B P5(B)]/[1+6e^-B]
                        * product_(h neighbor g) f_gh(B),
    f_gh(B)=[1+e^-B sum_(q=1)^6 chi_gh(q)]/[1+6e^-B],

where chi_gh(q) is the commutation sign of S_g and the clock-h Pauli prefix F_h(q). One can use these coefficients in place of J0 and remove the explicit second term of (T).

## 1. Exact gauge signs are pairwise; no assumption of commuting hops

Order gadgets as in the bounded-color dressing and write its data word at clock configuration q as D(q)=A F_g(q_g) C, where A contains earlier prefixes and C later prefixes. For a g-hop with Pauli P_gi and new q'_g,

    D(q')^dagger P_gi D(q)
      = C^dagger F_g(q'_g)^dagger A^dagger P_gi A F_g(q_g) C.

Conjugation by each earlier prefix in A contributes its scalar Pauli commutation sign with P_gi. The middle g product is identity on a nonwrapping edge and S_g on a wrapping edge. Conjugating the latter by each later prefix in C contributes its commutation sign with S_g. Consequently every transformed hop is its one-clock transition times (possibly s_g) times a PRODUCT of signs, one per overlapping other clock. These signs depend on the two clock labels/transition only and are one whenever the spectator clock is at q_h=0. There are no higher-body irreducible gauge phases; higher support of a transformed term comes from multiplying these pair factors.

In a worldline configuration, multiply those signs over hops. Assign each factor to the unique pair of excursions/thermal worldlines active at that hop. Two rods on different clocks acquire a symmetric pair factor h(gamma,gamma') in {+1,-1}; it equals one unless their clocks overlap and their temporal supports intersect. Symmetry here means that h is a function of an UNORDERED pair: include all hop factors between those two trajectories, regardless of which clock hopped. Same-clock overlapping rods have h=0; otherwise same-clock h=1. In all cases

    |h|<=1,   f:=h-1,   |f|<=2.

These factors do not depend on the external s variables. Each ordinary winding excursion contributes its own s_g. This derives the pair gas directly from the local dressed matrix elements and remains valid across the imaginary-time cut.

## 2. Exact periodic worldline-to-rod representation

Use the ordinary continuous-time Duhamel expansion of the finite-dimensional trace. Since H=Delta sum Q_exc -t times signed hops, each hop contributes t times its sign; a path contributes exp[-Delta times total excited occupation time]. Paths are periodic on the time circle of circumference beta.

At each clock, a path that visits zero decomposes uniquely into maximal excursions away from zero. An excursion gamma has a clock g, a departure time u on the circle, duration 0<ell<beta, an initial step 0->1 or 0->6, a nearest-neighbor path inside the chain {1,...,6}, and a final step to zero. The two boundary hops are included. Ordinary rods on the same clock have disjoint temporal interiors. An excursion can cross the chosen time cut without ambiguity: its departure from zero is its unique marked origin. Simultaneous events have measure zero.

A periodic path never visiting zero is one thermal wrap rod at its clock. It has duration beta, an initial excited label at the FIXED time cut, and a periodic path in the chain {1,...,6}. It excludes every other rod on its clock. No cyclic symmetry divisor is used for wrap rods, since the initial cut and trace label are fixed. A clock identically at zero has no rod.

This is a bijection, up to null coincidence events, between Duhamel paths and compatible rod collections. The usual unordered-collection factor 1/n! restores labelled rod counting. The full partition function is therefore exactly

    Z_a(s)=sum_(n>=0) 1/n! integral product_i dmu_s(gamma_i)
                                  product_(i<j) h(gamma_i,gamma_j).

The measure for each concrete trajectory contains its hopping monomial t^k, positive Boltzmann/time measure, and s_g^w for an ordinary rod's winding parity w. A first-return excursion has w=0 or 1: removing level zero leaves a chain; opposite entry/exit endpoints wind once, identical endpoints do not. Thermal wrap rods have no flux monomial because their paths never cross a wrapping edge incident to zero. All nontrivial signs beyond this monomial are in h.

Absolute activities are bounded by summing internal paths. The chain adjacency matrix has norm at most two. For ordinary rods this yields

    d|mu|_(ordinary, summed paths) <= 2 |t|^2 exp[-(Delta-2|t|)ell] du dell.       (1)

Indeed the boundary vector has squared norm two, and its chain propagator is exp(|t| A_chain ell). For wrap rods,

    |mu|_(wrap, summed paths at one clock)
        <= 6 exp[-beta(Delta-2|t|)].                                         (2)

The same bounds hold for complex t when both hopping orientations are analytically continued using the same t. These are estimates of the EXACT finite-temperature trace, not a vacuum projection. Rods of order t^0 are precisely the six no-hop thermally excited wrap trajectories.

## 3. Explicit uniform continuum KP estimate

Use the continuum theorem of Daniel Ueltschi, *Cluster expansions & correlation functions*, math-ph/0304003v3, Theorem 1. Its hypotheses are precisely |1+f|<=1 and

    integral d|mu|(gamma') |f(gamma,gamma')| exp[a(gamma')] <= a(gamma).

It permits a complex measure and general pair factors; positivity of hopping histories is not required. The conclusion is an absolutely convergent logarithmic cluster expansion with its rooted bound. This is the applicable primary theorem, rather than a ground-state analyticity result or a translation-invariant phase-diagram theorem.

Here is one deliberately loose choice of constants. Let d=D+1, nu=mu R+1, and a(gamma)=1+Delta ell(gamma)/4, also for wrap rods ell=beta. Apply the theorem to the ENLARGED absolute majorant measure carrying a factor exp(nu) per rod. Choose

    rho <= 1/8,
    rho^2 <= [64 d exp(nu+1)]^(-1),
    12 d exp(nu+1) exp(-B0/2) <= 1/4.

For |t|<=rho Delta, the ordinary weighted density from (1) is at most

    2 exp(nu+1) rho^2 Delta^2 exp(-Delta ell'/2) du' dell'.

For a test rod of duration ell, start times of another ordinary rod of duration ell' whose supports intersect have measure at most ell+ell', even on the circle. Include at most d same/neighbor clock choices and |f|<=2. Their contribution is bounded by

    8 d exp(nu+1) rho^2 Delta ell
      +16 d exp(nu+1) rho^2.

All potentially interacting wrap rods contribute at most

    12 d exp(nu+1) exp(-B/2).

The chosen constants make the total at most (Delta ell)/8+1/2, strictly below a(gamma). For a wrap test rod the same estimate is valid using ell=beta (the true start-time overlap is only beta). Integrability is finite at every finite volume and beta. Thus the cluster expansion converges with slack, uniformly in volume, flux and arbitrarily large beta.

This estimate is what prevents the extensive beta t^2/Delta vacuum-energy shift from ruining convergence: a long test rod is allowed a cost proportional to its duration, while the integrated neighboring-excursion intensity per unit time is O(t^2/Delta). It is not a high-temperature requirement beta t<<1.

## 4. Spatial potential, local coefficient norm, and analyticity

Each connected Mayer cluster projects to a connected clock set Y in the overlap graph. Its flux dependence is one monomial product_(g in A) s_g, where A is the set of clocks with an odd number of winding rods. A can be disconnected but lies in Y. Every nonempty A containing g entails at least one rod at g. If the cluster has n rods, diam(A)<=R(n-1), so exp[mu diam(A)] is bounded by the product exp(nu) already paid per rod.

Group cluster integrals by A, retain their time/physical support labels if desired, and put all empty-A terms into c_beta. The rooted cluster bound and (1),(2) give, at the majorant hopping radius t0=rho Delta,

    sup_g sum_(clusters with a rod at g) |cluster integral| exp[mu diam(Y)] / beta
      <= 4 exp(nu+1) rho^2 Delta
            + (6/beta) exp(nu+1) exp(-B/2)
      <= M0 Delta,

where M0=4exp(nu+1)rho^2+6exp(nu+1)/B0 is a safe choice. Counting a cluster once for each possible marked rod only enlarges this upper bound. The beta integral over ordinary rod origins has cancelled the division by beta; no volume factor remains.

For complete rigor concerning powers of t, do not differentiate a norm bound. Keep the concrete trajectories in the polymer measure. Each contributes an EXACT hopping monomial t^k; pair factors are t-independent. The absolute cluster sum at t0 therefore majorizes the absolute sum of all hopping-order coefficients, including arbitrarily many zero-hop thermal wrap rods. Absolute convergence allows grouping by hopping degree and flux monomial. This gives Banach-space analyticity of the weighted-local potential and bounds its high-order tail by M0 Delta (|t|/t0)^m0 once all retained terms have degree at least m0.

The logarithmic branch agrees with the real physical log Z for real t: at t=0 the trace is positive, and the convergent cluster formula is an exponential throughout the disk. Stabilizer dependencies cause no problem; the expansion is first defined for independent external signs and then restricted to physically allowed syndromes.

## 5. Winding selection and exact finite-beta degree-seven coefficient

Any ordinary winding rod requires at least seven hops. Nonwinding excursions require at least two hops. A thermal wrap path in the open chain has even hopping degree, including zero. A winding first-return path has seven plus an even number of hops. Consequently every nonempty-flux term below degree seven vanishes. At degree seven only ONE minimal winding rod occurs, with any number of zero-hop thermal wrap rods. Degree eight is impossible. All remaining flux-dependent coefficients have degree at least nine. Section 4 supplies their first term in (T).

It remains to compute degree seven without discarding thermal spectators. Fix g and set all other hopping variables to zero. Every other clock is then a static label q_h with independent onsite probability proportional to 1 for q_h=0 and e^-B otherwise. The product of dressed edge signs around g is

    s_g product_h chi_gh(q_h).

A one-clock gauge change puts that product on a single edge. The exact trace therefore depends on its loop product exactly as for an isolated clock. Its degree-seven term has two orientations. Mark the unique transition entering zero and integrate the six excited dwell times v_1,...,v_6; their sum is at most beta, and the remaining dwell is vacuum time. For each orientation the contribution is

    beta t^7 integral_(v_i>=0, sum v_i<=beta) exp[-Delta sum v_i] dv_1...dv_6
      = beta t^7 Delta^(-6)[1-e^-B P5(B)].

Division by beta and the unperturbed one-clock partition 1+6e^-B gives the isolated free-energy coupling stated in Section 0. There is no lower flux term in log Z, so no lower-order logarithmic cross-term modifies this coefficient. Averaging the static spectators multiplies it by product_h f_gh(B). In particular

    |1-product_h f_gh(B)| <= 12D e^-B,

using chi_gh(0)=1 and |f_gh|<=1. Also

    0 <= 1-[1-e^-B P5(B)]/[1+6e^-B]
       <= e^-B[P5(B)+6].

These inequalities prove the second term of (T). They include the real thermal occupations that a ground-state SW calculation would miss.

## 6. Parameter compatibility and boundary of the conclusion

For any desired sufficiently small relative remainder, first fix graph/locality constants and shrink epsilon so the degree-nine tail divided by J0 is small. Then increase B to suppress the explicit thermal factor. One can simultaneously impose beta J0=2B epsilon^7 above any fixed target low-temperature threshold. These are fixed constants independent of volume, albeit potentially extreme ones. There is no conflicting requirement beta t small.

The lemma applies to arbitrary flux patterns, not only typical ones, and its local potential permits cancellation of all far-away free energy in a witness ratio. For a flipped syndrome set T, the residual free-energy difference is at most 2|T| times the unweighted local remainder norm. Actual witness transfer must still check its precise syndrome-change set and use the resulting positive tension. Dynamical assumptions, dressed local-bath support, and logical lifetime remain separate gates.

No adversarial excited boundary conditioning is asserted. If a clock is pinned to an excited prefix that anticommutes with S_g, the neighboring leading loop coupling can change sign at order seven. Ordinary deleted-edge/free finite volumes are covered by the same proof and smaller degree; arbitrary external pins require explicit boundary terms instead.

## 7. Primary-source/provenance notes

The continuum signed-gas convergence step uses [Ueltschi, math-ph/0304003v3](https://arxiv.org/pdf/math-ph/0304003), Theorem 1, including its rooted bound and complex-measure hypothesis. The exact rods, clock winding selection, uniform physical potential, and coefficient computation above are the present derivation. No theorem concerning only a ground band is substituted for the finite-temperature trace.

Borgs–Kotecky–Ueltschi's low-temperature quantum contour work was inspected as a relevant primary precedent; its blocked-time method explains why beta t need not be small. The present proof does not invoke its translation-invariant phase-diagram conclusion for arbitrary inhomogeneous flux. It instead verifies the continuum gas hypotheses directly.

The argument assumes the exact full-Hilbert-space Pauli-clock dressing and bounded-overlap model algebra stated in the constructor, and rederives the pair-sign property needed by the gas. It is not an independent all-level construction of the recursive memory or a proof of a native lifetime theorem. No stopped source or external account was accessed or mutated.

## 8. Cross-audit and exact snapshot binding

At 23:50 UTC the separate scalar-return auditor read this rod derivation end-to-end and found no gap in the fixed-radius KP constants, exact-trajectory coefficient majorant, degree-eight exclusion, or finite-temperature spectator normalization. I independently checked that auditor's real-parameter marked-winding proof: its inequality (*) and explicit detour/multirod constants are valid. Its locality weight is in the overlap-graph metric; for physical edge bound R use mu R. These are complementary proofs of the same exact-model local free-energy gate, not numerical evidence for the full memory theorem.

- `independent_constructor.md`: `5c8200818c8cc3c1612fc0628c8181ad6ce99a0450af17e961f27008b01f4be1`.

- `ROOT_EXCURSION_PROOF_TARGET.md`: `b97a54e94ad715c0927252a6af10570f67c449ded3b7de9ad3793a6d327604c4`.

- `root_rod_audit.md`: `43b847eddc40ed237bb31313e7623504413ddd60a369504cf612e24e7dafbf6f`.
