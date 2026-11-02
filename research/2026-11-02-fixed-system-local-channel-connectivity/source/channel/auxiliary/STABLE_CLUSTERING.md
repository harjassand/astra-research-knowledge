# Physical clustering: a constructive bridge and its exact missing gates

1 November 2026. Independent derivation. This note does NOT certify stable clustering for the weakly noncommuting actual family from scalar partition weights alone.

## 1. The demanding observable in the MKS hypothesis

Ma–Khemani–Sang, [2509.15204v3](https://arxiv.org/html/2509.15204v3), Definitions 1–2 and Theorem 1, use annulus covariance between norm-one operators on an inner simply connected region and the entire exterior, uniformly under small local interaction changes. For unrestricted quantum perturbations the algebra is the full local operator algebra. Bounds on individual local Pauli pairs do not suffice: expanding an arbitrary exterior operator loses an exponential factor. Their construction is an explicit local recovery-channel construction, not an efficient elementary-gate algorithm. Below, the derived stretched-exponential variant is an extension, not their literal theorem.

## 2. Exact dimension-free factorization of the reference code

Let omega0=P0/Tr(P0) be the maximally mixed ground code. Suppose no check meets both A and C, and |A|<d. Then

    omega0_AC = omega0_A tensor omega0_C.

Proof: it suffices to test P_A tensor P_C for Pauli operators. If their product is a stabilizer, each factor centralizes every check, since no check meets both supports. Distance forces P_A to be a stabilizer up to phase; then P_C is one too. Conversely two stabilizers have the expected product. If a factor has nonzero syndrome, the joint product also does, so the joint and the corresponding single expectation vanish. This proves all Pauli coefficients factor, hence the density operators factor. No expansion of an arbitrary exterior operator is charged.

Every sector omega_sigma=E_D(sigma) omega0 E_D(sigma)^dagger has the same A:C factorization, because E_D is a tensor product of onsite Paulis. In the exact commuting Gibbs mixture, therefore,

    Cov_rho(O_A,O_C) = Cov_mu(f_A,f_C),
    f_X(Gamma)=Tr[O_X omega_Gamma^X], |f_X|<=1.

If the decoder correction splits over trace components (phases irrelevant for conjugation), f_X depends only on polymers whose correction support meets X. This is stronger than a local-Pauli estimate and is valid for arbitrary norm-one O_C.

The restriction |A|<d is genuine. It includes every fixed-polylogarithmic ball asymptotically for polynomial distance. A theorem about all simply connected annuli would need stronger geometric correctability, not merely distance.

## 3. Physical-envelope lemma: sufficient hypotheses

For each trace polymer gamma of mass m, require a physical envelope D_gamma containing both its correction support and the locations of its dependency stencils, with:

1. diameter(D_gamma)<=C m^p, p>=1;
2. incompatible polymers have touching envelopes (or their union has diameter bounded by C(m_gamma+m_eta)^p);
3. rooted physical activity tails and total activity obey sum_{gamma:D_gamma touches x, |gamma|>=M} w_gamma <= C poly(M)e^{-cM}, and sum_gamma w_gamma<=CN;
4. the strengthened low-activity incompatibility bound sum_{eta incompatible gamma} w_eta |eta|<=theta |gamma|, theta<1.

Cardinality of a correction support is not enough for (1). A shortcut-host graph distance is not physical distance. Anchored radius and bounded physical multiplicity must be checked. The accepted actual trace gas supplies (4), and polynomial *physical* footprint geometry may supply (1)–(3), but this note has not independently rederived that actual geometry.

## 4. Conservative stretched-exponential clustering without a dubious clan moment

Under these hypotheses one can avoid assuming an exponential total-mass moment of an infinite ancestor clan. Truncate polymers at mass M. The omitted-polymer probability is at most CN poly(M)e^{-cM}. Run the truncated birth/death chain from the empty configuration for time t=aM. Weighted path coupling gives total-variation error at most CN exp[-(1-theta)t].

Use independent Poisson birth clocks of rate w_gamma and death clocks of rate 1. Acceptance of a birth consults only incompatible occupations. A dependence path running backward through births has successive incompatible labels. Deaths only erase dependence and need not enlarge such a path. For a retained gamma,

    sum_{eta incompatible gamma} w_eta <= theta |gamma| <= theta M.

The expected number of temporally ordered paths of length k, summed over all possible initiating births, is bounded by CN t (C M t)^k/k!, with harmless fixed constants. Stirling's inequality, t=aM, and k=K M^2 with sufficiently large fixed K give a global long-path probability bounded by poly(N,M)e^{-c' M^2}. Spatial displacement along k successive envelopes is O(k M^p), hence O(M^{p+2}).

Consequently the chain's outputs in sets separated by r can be coupled to functions of disjoint Poisson input collections, with error at most poly(N,M)e^{-cM}, by taking M=c_0 r^{1/(p+2)} and assigning disjoint buffered cones. Those functions are independent because the initial state is deterministic empty. For bounded f_A,f_C this gives

    |Cov_mu(f_A,f_C)| <= poly(N) exp[-c r^{1/(p+2)}].

Constants absorb small r and polynomial M factors. A fully formal proof should specify the cone truncation at the level of polymer-clock supports; the assumptions above ensure that an accepted/rejected birth and its consulted incompatibilities are contained in the union of those supports. The argument is constructive and does not equate rapid mixing on the shortcut graph with physical clustering.

Combined with Section 2 this proves the COMMUTING-reference covariance, for |A|<d, provided the stated physical-envelope hypotheses bind to the actual family. Uniform bounds persist under sufficiently small changes of the positive commuting check energies. It does NOT yet prove stability under generic noncommuting perturbations.

One might improve the exponent to 1/p using weighted cluster connectivity, but that stronger claim requires a genuine connected-weight/disagreement proof. Naively claiming an exponential total-mass ancestor-clan moment from first-moment contraction overlooks the common exponential lifetime of a large polymer.

## 5. Why scalar quantum weights do not finish the quantum claim

The existing expansion bounds Tr(P_sigma e^{-beta H}) and near-scalar logical Gram matrices. Those statements determine sector weights, not the joint density operator on A plus a macroscopic exterior. Off-diagonal sectors contribute to an arbitrary O_A O_C. An expansion with two arbitrary operator insertions must control its connected terms in operator norm/trace norm without an exp(|C|) factor; this has not been supplied by the scalar gas.

A promising alternative is a uniformly physical-quasilocal controlled spectral flow from every reference sector to its filtered sector, with syndrome dependence localized in the same causal cone. The gapped filtered parents make physical spectral flow possible because their interactions are physical-quasilocal even though the *gap proof* uses a shortcut graph. But one must prove locality of the controls in the branch labels and show that replacing sector weights by the weakly interacting trace gas preserves the physical dependence-path bounds. A polynomial adiabatic circuit does not establish this. Nor does a gap alone establish the required uniform branch-controlled implementation.

## 6. Stretched clustering still supports polylog-radius recovery channels

Assume, as an additional earned input, uniform covariance

    Cov(A,C)<=poly(N) exp[-c dist(A,C)^alpha], alpha>0,

for the balls encountered in the construction and all neighboring Hamiltonians along the path. In the MKS local-perturbation lemma choose l=r/2. Its bound becomes a polynomial prefactor times exp[-c'(r)^alpha], plus an ordinary Lieb–Robinson exponential. Thus the inner buffer can be r1=O(log(poly(N)/epsilon)^(1/alpha)). The approximate-Markov recovery error requires outer buffer r2=O(r1^D+log(poly(N)/epsilon)) at fixed beta. In D=3 these remain fixed powers of logarithms. The finite-dimensional colored covering uses finitely many geometric scales, so replacing each scale by a fixed polynomial of the preceding scale still yields polylog total range. Error allocation among polynomially many gates changes only the logarithm.

This establishes the analytic sufficiency of stretched-exponential *stable, exterior-uniform* clustering. It does not certify efficient gate synthesis of Petz maps on polylog-radius volumes: generic synthesis costs exp(polylog N), not necessarily poly(N). It also does not eliminate finite-size errors from logical components; if these contribute eta_N, allocate polynomial(N)*eta_N below the requested tolerance and retain an intrinsic floor otherwise.

## Verdict

A nontrivial positive bridge is available: exact stabilizer factorization reduces arbitrary-exterior reference covariance to classical footprint dependence, and a finite-time graphical construction gives conservative physical stretched-exponential decay. The actual quantum open-phase conclusion still requires the physical-envelope binding plus a quantum controlled-flow/operator-valued correlation theorem. The accepted scalar thermal encoder alone is insufficient. These are exact proof gates, not evidence of a no-go.

## 7. Stronger route once the direct local phase channel is earned

**Update after the parent construction:** The parent reports a direct actual-code extension of the XCW sampling/controlled-flow channel with deterministic polylog causal radius. That construction, if its physical controls and caps pass review, makes an independent quantum insertion expansion unnecessary for the following correlation theorem. The proof here is complete conditional on that precisely stated channel, and is not an independent audit of its construction.

Suppose for every admitted accuracy epsilon there is a circuit C_epsilon, using initially product local ancillas and no free shared global randomness, satisfying

    ||C_epsilon(omega0 tensor ancillas)-rho_H||_1 <= K epsilon + eta_N,
    causal radius(C_epsilon) <= C0 log^q(N/epsilon).

The channel can be spatially inhomogeneous; uniformity over a perturbation domain is enough. All randomness and adaptive branches must obey the same deterministic radius cap; a high-probability radius only suffices after explicitly aborting overlong branches and charging their probability to epsilon.

Let r=dist(A,C) and choose R with 2R<r and |A_R|<d. The output operators O_A and O_C pull back into disjoint backward cones A_R and C_R. Because the channel is a composition of gates with product local environments and the cones are disjoint, its adjoint on their product factors as

    C_epsilon^*(O_A O_C)=C_epsilon^*(O_A) C_epsilon^*(O_C)

when written on system plus its product Stinespring ancillas. These pulled-back operators have norm at most one. The reference reduced state on A_R and C_R factorizes by Section 2, after adding the initially product ancillas. Therefore the channel output has exactly zero A:C covariance. If tau is this output, trace-norm continuity gives

    |Cov_rho(O_A,O_C)-Cov_tau(O_A,O_C)|
       <= 3 ||rho-tau||_1 <= 3K epsilon+3 eta_N.

The three terms are the joint expectation and the two single-expectation differences. This is uniform in arbitrary norm-one exterior O_C, with no dimension factor.

For fixed or polylog-size A on a bounded-density 3D lattice, choose

    R = c min(r,d^(1/3)),
    epsilon = min(1, N exp[-(R/C0)^(1/q)]),

with c small enough to keep |A_R|<d and separated cones. Constants also require the radius of A itself to be o(d^(1/3)). In the nontrivial regime this yields

    Cov_rho(A,C) <= C N exp[-c min(r,d^(1/3))^(1/q)] + 3 eta_N.

If physical linear size is L, d>=c L^delta, and r<=O(L), then

    min(r,d^(1/3)) >= c' r^s,   s=min(1,delta/3),

up to fixed constants. Hence

    Cov_rho(A,C) <= poly(N) exp[-c r^(s/q)] + 3 eta_N.

For N polynomial in L and eta_N bounded by poly(N)exp[-c d^nu], eta_N can itself be absorbed in a weaker stretched exponential in r with exponent at most delta*nu, or retained explicitly. In either form this is physical, arbitrary-exterior clustering for small inner regions, uniform over any domain on which the direct local-channel construction has uniform constants.

### Accuracy domain and finite-size qualification

The chosen epsilon must be inside the proven channel accuracy regime. If linked clusters require log(N/epsilon)<c d, the above choice is admitted whenever R^(1/q)<c'd. For polylog R this always holds asymptotically. If extending to polynomial R, verify that inequality rather than extrapolating an inverse-polynomial-only theorem. One can always state the rigorous inverse-polynomial form: for each fixed k, physical separation at least C_k log^q N and |A_R|<d implies covariance <=N^(-k)+3 eta_N.

### What is and is not concluded

This is a useful observable consequence of direct local phase connectivity, independent of MKS and therefore noncircular. It verifies stable local-versus-exterior correlations for inner regions of fixed/polylog size (and the stated larger distance-limited sizes). It does not automatically establish MKS's full all-annulus definition if that includes inner balls whose physical volume exceeds distance; a separate geometric correctability or factorization argument would be needed there. Conversely the direct phase channel already establishes the desired two-way connectivity if the parent proves its reverse, whether or not that stronger covariance condition holds.
