# Audit: covariance-only work-register representation repairs fixed-system phase locality

1 November 2026, 23:06 UTC. Independent audit of the replacement mechanism. **PASS, conditional on the previously audited deterministic physical-cone representation and uniform whole-state error bounds.** This does not promote the growing-work-register representation itself into a standard phase circuit.

## 1. Growing local work dimension is harmless for covariance

Suppose a mathematical representation T_epsilon maps omega0 tensor an input-independent product of local work states to a physical output tau, with ||tau-rho_H||_1<=K epsilon+eta_N. Suppose its full physical causal radius—including messages, event records, randomness, and adaptive branches—is deterministically at most R(epsilon). There is no restriction on the dimension of each *local* work factor for this claim.

For regions A,C with 2R+R_check<dist(A,C), their full backward cones are disjoint. The input physical code state factorizes on A_R:C_R when |A_R|<d. This follows from the Pauli argument in STABLE_CLUSTERING.md Section 2. The local work factors also factorize across those cones, irrespective of their dimensions. A product Stinespring dilation then proves exact factorization of the output expectations for arbitrary norm-one O_A,O_C. Trace-norm continuity yields

    Cov_rho_H(A,C)<=3K epsilon+3eta_N.

No dimension factor enters at any step. A globally shared seed, global accept/reject flag, unrecorded remote lookups, or uncontrolled long branch invalidates the premise. Locally aborting the rare excessive-event/path branches is allowed if their total error is charged. Merely an expected radius is insufficient.

Thus the stochastic/controlled representation can be retained as a proof of correlations even when it fails the standard bounded-physical-system phase-circuit definition. The conclusion concerns rho_H itself and no longer carries the work-register resource into the next construction.

For the spectral-flow part of this representation, large classical simulation records can be discarded after producing local syndrome controls. Only O(1) sign controls per bounded-incidence check/site need survive. The physical Lieb–Robinson estimate is then on bounded-density controls and physical spins. The large discarded record dimension does not appear in the generator's local interaction norm. Block-diagonal controls must be normed as block-diagonal operators, not summed as one independent interaction per branch.

## 2. Exactly the restricted covariance needed for microscopic-core LPPL

The full all-annulus MKS Definition 1 is unnecessary for the repaired construction. Use a single microscopic Hamiltonian term as the varied core A. Its diameter and number of spins are O(1). The MKS LPPL lemma invokes covariance of A_l versus the exterior, where l is the inner buffer. Taking l=polylog(N/epsilon) makes A_l a polylog-size ball. Its backward cone remains polylog-sized and therefore lies below polynomial code distance for sufficiently large N.

For any requested inverse-polynomial local error epsilon_M, choose the representation accuracy epsilon'=epsilon_M/poly(N), its radius R=polylog(N/epsilon_M), and a core-to-exterior separation at least 3R+O(1). This proves the needed covariance directly; no assertion about macroscopic inner regions is made. The logical intrinsic error must obey poly(N)eta_N<<epsilon_M. For stretched-exponentially small eta_N and inverse-polynomial targets this is automatic asymptotically.

Consequently LPPL has polylog inner-buffer range. The actual physical Gibbs approximate-Markov bound then yields an actual-data recovery channel on a larger buffer with

    r2 >= lambda [kappa+mu |A B1|+log(poly(N)/epsilon_M)].

In 3D, |A B1|=O(r1^3). At fixed inverse temperature this is O(r1^3+log(poly(N)/epsilon_M)); for inverse temperature O(log N), kappa,mu,lambda contribute additional fixed polylog powers. In both cases r2 is polylogarithmic.

This is the MKS local-recovery proof specialized to microscopic cores, rather than an invocation of their full stable-clustering theorem without checking its hypothesis. The source is [Ma–Khemani–Sang 2509.15204v3](https://arxiv.org/html/2509.15204v3), Lemmas 1–3 and Section III.1.

## 3. Standard fixed-system channel composition

Assign each microscopic interaction term a nearby physical root. Color roots so gates of radius r2 in a color have disjoint support. Bounded physical density gives O(r2^3) colors. For one small coefficient update, the sequential intermediate Hamiltonians can be defined term by term. Construct each Petz gate from the corresponding actual-data intermediate marginal. Gates with disjoint supports commute as maps, even though their specifications were defined in a sequential order, so one color can be executed as a layer. Telescoping error is bounded by the number of gates times epsilon_M.

Intermediate Hamiltonians need not be homogeneous. The proof therefore requires estimates uniform over the entire coefficient box swept by partial updates, not merely along a homogeneous one-parameter curve. For positive check energies bounded below and perturbations in a small local-norm ball, this is the natural admitted box; retaining a strict margin in both bounds handles each partial update.

These Petz gates are CPTP maps on blocks of the ORIGINAL bounded-density physical system. They do not retain the earlier per-site event histories. They fit the standard arbitrary-local-channel circuit model; one may use/discard a Stinespring environment inside a gate. This is not an efficient gate-synthesis theorem: a block of polylog-radius volume can have exp(polylog N) Hilbert dimension, and computing its true Gibbs marginal or densely synthesizing its channel may take still larger global time. The construction is explicit at the mathematical finite-system channel level. No polynomial elementary-gate cost follows.

## 4. Uniform commuting low-temperature extension

Write the dimensionless commuting Hamiltonian as

    H_b = sum_j b_j Q_j,  b_j>=b0>0,

with b0 chosen strictly inside the trace-gas low-activity window. The coefficients may vary arbitrarily from check to check. The actual trace factorization gives

    w_b(gamma)=exp[-sum_{j in sigma_gamma} b_j]
              <=exp[-b0 |sigma_gamma|]
              <=exp[-b0 |gamma|/A].

All rooted activity, contraction, dictionary-tail and dominating birth-clock bounds are therefore bounded by the same worst-case b0 constants. Raising any coefficient only improves these bounds. The physical trace envelope and reconstruction geometry do not depend on b_j. The finite-time sampler/physical-cone covariance representation is consequently uniform for every heterogeneous collection with b_j>=b0, in particular max_j b_j=O(log N). No extra low-temperature quantum expansion is needed in this commuting segment. Independent onsite bath Gibbs factors remain products and do not alter the code factorization.

For a homogeneous high endpoint b_j>=B, positivity gives

    Prob(any nonempty trace) <= sum_gamma w_B(gamma)
                            <= C N exp[-c B]

once B exceeds the fixed activity threshold. Thus B=C_k log N makes the commuting Gibbs state inverse-polynomially close to its normalized ground-code projector (tensor the selected independent bath reference if bath spins are handled separately). This supplies a finite endpoint for zero-temperature connectivity; one need not apply Petz maps at literally infinite inverse temperature. Contractivity transfers the finite-endpoint approximation through the constructed channels.

An onsite bath with degenerate ground space can be kept as a specified product mixed state or locally reset; its ground degeneracy must not be silently identified with a unique pure product ground state. At finite beta its onsite Gibbs factors are known product inputs.

## 5. Do not extend the generic quantum window to beta~log N

The available perturbative smallness behaves schematically as beta v exp(C beta J). A fixed nonzero v cannot be held in that sufficient window uniformly while beta grows like log N. Therefore the valid route is:

1. connect a weakly noncommuting finite-beta state to its commuting reference while beta remains in the fixed compact interval;
2. raise commuting check coefficients, including heterogeneous intermediate values, toward O(log N);
3. use the positive trace-tail estimate to connect the high-coefficient Gibbs state to the code projector within the requested accuracy.

The open quantum neighborhood exists at each admitted fixed finite beta, not uniformly to beta=infinity. Confusing these statements would invalidate the repair.

## Final verdict

The growing-register flaw does not infect the covariance premise. Its representation is a legitimate dimension-free proof of stable small-inner-region/exterior correlations. Microscopic-core LPPL plus actual-data Petz recovery can convert those correlations into standard fixed-system local phase channels, with polylog depth and radius, without importing the large persistent work registers. The gates' computational synthesis cost remains unearned. Uniformity of the commuting segment up to logarithmic coefficients is supported by monotonic domination at the fixed low-temperature threshold; uniform noncommuting extension to that endpoint is not.
