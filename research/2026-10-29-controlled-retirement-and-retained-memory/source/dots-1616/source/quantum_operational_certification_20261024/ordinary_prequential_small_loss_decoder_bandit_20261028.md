# A positive-loss decoder bandit for finite non-reset terminal recovery

28 October 2026. **NEW PROOF CANDIDATE; independent receiving pending.** No sampled acquisition or hardware claim. The received slow prequential source remains immutable:
`ordinary_prequential_terminal_memory_recovery_20261028.md`, SHA20e59391aeab608e0fb76dbaee3fee6825d434991892a2c63fe5e57634316079, main receipt1173110f088c93a6854d3119a8f509ab6f61db1ada22dc678000aa1d99a591ed.

This changes the learning apparatus. Instead of measuring one physical Pauli word and constructing a signed full-information gradient, EVERY probe is passed through an actually synthesized exploratory CPTP decoder and yields a single ordinary return-mismatch bit. Its second moment is its loss. A finite log-det mirror-descent construction gives O(d^5 log(1/epsilon)/(gamma epsilon)) source calls for multiplicative-plus-additive terminal risk. The payment is a compiled general local decoder on every probe, not merely at the final payload. It retains one logical qubit, a fixed encoder, a known w-qubit output patch, and one private terminal payload time.

## 1. Exact interface and changed occupation law

Import the received source's complete causal retained-memory interface, full initial QR–source product premise, fresh private coins, private current decoder, same complete probe/payload port, padded timing, isolated terminal output, trusted payload holding, finite-cap samplers and one whole-process implementation allowance. No iid reset, environment reconstruction, gauge spectrum floor, or predictable future memory is supplied.

The all-probe reference process HERE uses the exploratory decoders and one-bit return instruments defined below. Its conditional memory states and occupation law generally differ from the old physical-Pauli tomography process. Write E_(t,h) for this NEW actual conditional CPTP channel and

    R_N(D)=(1/N)sum_t E_h[1−F_e(D E_(t,h))].              (1)

The comparison is inf_D R_N(D) for a FIXED terminal decoder, not a hindsight-per-path or counterfactual-policy oracle. The received CP-memory Pauli/gauge family with CP-order G_I>=G_alpha supplies a single fixed ideal decoder that is pointwise full-CPTP optimal for all these histories; its proof is unchanged. That family is a sufficient physical corollary, not required for the general occupation-law regret theorem.

## 2. One actual positive loss bit

Let d=2^w, k=2d, and use normalized output-first decoder Choi matrices C>=0, Tr_output C=I_d/d. Thus Tr C=1. After choosing and fixing the current decoder C, prepare a uniformly random ordinary six-state qubit |j,s>, apply the current source, apply the ACTUAL decoder, and measure sigma_j on its output. Record y=1 for mismatch and y=0 for match. All j,s choices are fresh and independent of the current source memory and private exploration coins. They are not leaked as classical labels through another port.

For each actual prior history h the mean is

    q_(t,h)(C)=d Tr(C T_(t,h))=(2/3)[1−F_e(D_C E_(t,h))],
    T_(t,h)=(1/6)sum_(j,s) Pi_(j,−s) tensor r_(j,s)^T>=0,
    r_(j,s)=E_(t,h)(|j,s><j,s|).                         (2)

In particular q(C) is LINEAR on the affine Choi set and lies in[0,1] for EVERY feasible decoder. T is an analytic positive effect, not a learned matrix or an oracle. The only acquired datum is the integer bit y. Current source dynamics may depend on the past, but not on fresh private current decoder/control labels. Physical quantum-input discrimination remains inside the same CPTP map.

## 3. Rational affine coordinates, barrier, and finite exploration

Take the D=3d^2 rational Hermitian basis matrices

    E_a=sigma_j tensor W, j=X,Y,Z, W a physical w-qubit Pauli.

They have zero output partial trace and Tr(E_a E_b)=k delta_ab. Every normalized TP Choi matrix is C(theta)=C0+sum_a theta_a E_a, with C0=I_k/k and real theta. The feasible coordinate set K is known. Its Euclidean diameter is at most sqrt(2/k)<=1. No arbitrary affine-frame acquisition is needed.

On its positive interior use R(theta)=−log det C(theta). At a rational center C_t, its gradient and Hessian are rational:

    [grad R]_a=−Tr(C_t^(-1)E_a),
    H_ab=Tr(C_t^(-1)E_a C_t^(-1)E_b).                   (3)

H is real symmetric positive definite. For a tangent matrix Delta=sum v_a E_a,

    ||v||_H^2=Tr(C_t^(-1)Delta C_t^(-1)Delta)
             =||C_t^(-1/2)Delta C_t^(-1/2)||_F^2.       (4)

Compute a rational invertible D×D matrix V satisfying the EXACT rational certificate

    (1/2)I <= V^T H V <= I.                              (5)

This is acquired from the KNOWN current Choi matrix. A finite Cholesky/inverse approximation, scaled by3/4, has a fixed slack about(9/16)I; §6 gives an explicit precision/bit cap. No unstable eigenbasis alignment is used. Let v_i=V e_i and u_i=V^(-T)e_i, with the inverse taken exactly over rationals.

Draw i uniformly from{1,...,D} and z uniformly from±1; fix the played decoder

    C_t^play=C_t+(z/2)sum_a (v_i)_a E_a.                 (6)

The normalized perturbation in(4) has norm at most1/2, so C_t^play>=C_t/2>0 and has exactly the same TP marginal. It is a physical rational decoder, not a floating eigenvector prescription. The mean played Choi is EXACTLY C_t. After its actual mismatch bit define the rational coordinate estimator

    ghat_t=2D y z u_i.                                  (7)

Let l_t be the unknown coordinate gradient of q_(t,h). Averaging over i,z and the ACTUAL return bit, linearity gives

    E[ghat_t|h]=sum_i u_i v_i^T l_t=l_t,
    E[y|h]=q_(t,h)(C_t),
    ||ghat_t||_(H^(-1))^2
       =4D^2 y [e_i^T(V^T H V)^(-1)e_i] <=8D^2 y.      (8)

Here y^2=y, not q^2. This is the load-bearing small-loss variance identity. It is valid for adaptive conditional memory and the physical noisy bit. No unbiased estimate of a nonexistent microscopic error is asserted.

## 4. Certified rational log-det mirror step

Fix rational 0<gamma,epsilon<=1 and

    eta=gamma/(64D^2), zeta=epsilon/16,
    delta=eta epsilon/64.                               (9)

Initialize C_1=C0. Given the actual rational ghat_t, return a rational TP center C_(t+1)>0 with coordinate theta_(t+1) satisfying BOTH exact certificates

    ||theta_(t+1)−theta_t||_(H_t)^2 <=1/4,
    ||eta ghat_t+grad R(theta_(t+1))−grad R(theta_t)||_2^2
                                                        <=delta^2. (10)

The first is a locality-of-update guard for the LEARNER, not physical spatial locality. The second is a finite tangent stationarity residual. All terms use rational inverses/traces. Section6 constructs a deterministic polynomial-cap known convex solve meeting these certificates on EVERY data history. On y=0 one may simply retain C_t, satisfying both exactly. A failed numerical certificate triggers a physical replacement but cannot be silently declared a valid optimization step or a fresh statistical event.

Here is a direct proof, avoiding a high-level ideal SCRiBLe oracle. Define the log-det Bregman divergence B(C,D)=R(C)−R(D)−<grad R(D),theta_C−theta_D>. It is nonnegative. For any fixed strictly positive comparator C_*, the residual and the coordinate diameter imply

    eta <ghat_t,theta_(t+1)−theta_*>
      <=B(C_*,C_t)−B(C_*,C_(t+1))−B(C_(t+1),C_t)+delta. (11)

Let r=||theta_(t+1)−theta_t||_(H_t)<=1/2 and
    a=eta ||ghat_t||_(H_t^(-1)).
The eigenvalues x_b of C_t^(-1/2)(C_(t+1)−C_t)C_t^(-1/2) lie in[−1/2,1/2]. The elementary inequality x−log(1+x)>=x^2/3 on this interval yields

    B(C_(t+1),C_t)>=r^2/3.

Adding eta<ghat_t,theta_t−theta_(t+1)> to(11), applying Cauchy–Schwarz and ar−r^2/3<=3a^2/4<=a^2, and summing gives the PATHWISE inequality

    sum_t <ghat_t,theta_t−theta_*>
       <=B(C_*,C0)/eta
          +eta sum_t ||ghat_t||_(H_t^(-1))^2+N delta/eta. (12)

Choose C_*=(1−zeta)C_D+zeta C0 for any fixed physical comparator D. It is strictly positive with

    B(C_*,C0)=−log det(k C_*)<=k log(1/zeta),
    q_t(C_*)<=(1−zeta)q_t(C_D)+zeta<=q_t(C_D)+zeta.       (13)

Taking conditional expectations in(12), using(8), and writing L=E sum_t y_t yields

    (1−8eta D^2)L
       <= E sum_t q_t(C_D)+zeta N
           +k log(1/zeta)/eta+N delta/eta.               (14)

No fixed-point/noise-stationarity argument appears. The comparator is fixed; the unknown loss functions can follow the ACTUAL retained-memory history. In particular the observed bit is not replaced by its expectation inside a nonlinear algorithm.

## 5. Actual private-terminal channel and finite source cap

Use the received private terminal-time protocol, but freeze the current sampled physical decoder C_t^play before its current source call. The hypothetical all-probe history includes all previous exploratory decoder labels and mismatch outcomes; current fresh i,z are averaged in its mixture. At the terminal call insert the stored unknown payload, apply this same frozen exploratory decoder, isolate the output and stop, WITHOUT observing y or updating.

The received exact prefix argument gives an actual CPTP payload channel whose Bell loss is(3/2)L/N. This is not a claim that the decoder's center C_t alone has been applied to the unknown payload: the physically sampled decoder is applied, and linearity makes their means agree. Full payload-reference entanglement is retained in the channel identity. The initial full QR product and complete-port/privacy assumptions remain essential.

Let L0=ceil log2(16/epsilon), and N be the least power of2 satisfying

    N >=512 D^2 k L0/(gamma epsilon).                   (15)

Since log(16/epsilon)<=L0, the three additive terms in(14), divided byN, are at mostepsilon/16, epsilon/8, epsilon/64. Also

    1/(1−gamma/8)<=1+gamma/7<=1+gamma.

Consequently the averaged terminal Bell loss obeys

    ell_terminal <=(1+gamma)inf_D R_N(D)+(39/112)epsilon (16)

under the ideal trusted controls. A single whole-process operational discrepancy nu<=epsilon/2 gives the advertised <=(1+gamma)inf_D R_N(D)+epsilon. The retained CP-memory dominance family replaces the infimum by its per-history all-CPTP oracle on THIS occupation law. No conditional input/reference independence is invented from data.

The actual protocol uses at mostN complete source calls INCLUDING its ONE payload, with

    N <1024 D^2 k L0/(gamma epsilon)
       =18432 d^5 L0/(gamma epsilon).                  (17)

The source exponent is not claimed optimal. This is an EXPECTED averaged terminal-service theorem, not a high-probability per-record certificate. No future decoder availability, growing selector, unknown patch, or repeated payload service follows automatically.

## 6. Finite known-matrix optimization and bit/control bill

The numerical requirements are constructed, not assumed as an uncharged optimization oracle.

**Known lower bound generated by the learner.** The first guard in(10) implies C_(t+1)>=C_t/2. Therefore every center, played decoder and one-step solve through N rounds has a usable conservative LEARNER-ONLY bound

    mu I <= C,     mu=2^(-(N+2))/k.                    (18)

This artificial exponentially small bound has O(N+log d) bits. It is not a source gauge/noise spectrum premise, and no inverse-mu arithmetic-iteration bound is claimed. The algorithms below have polynomial BIT complexity, not a claim that every spectral condition number is polynomial.

**Whitening.** In the rational coordinates(3), kI<=H<=k mu^(-2)I for centers. A Cholesky factor H=R^T R gives V0=R^(-1), so V0^T H V0=I. Approximate(3/4)V0 entrywise by rational dyadics to error at mostmu/(128kD); its H^(1/2)-weighted operator error is at most1/(128sqrt(k)). Thus its squared singular values lie strictly between1/2 and1. Check(5) by exact rational PSD arithmetic and use the resulting rational inverse V^(-T), not a separately rounded dual. Cholesky square roots can be approximated to the prescribed certified absolute/relative accuracy by bounded bisection with O(poly(N,D)) bits; exact degeneracy of H causes no eigenvector problem.

**Existence and a bounded solve for(10).** Consider the known convex proximal objective

    F(theta)=eta <ghat_t,theta>+B(C(theta),C_t)

over the affine spectrahedron C_t/2<=C(theta)<=3C_t/2. It has known rational interior center C_t. The unrestricted positive-TP minimizer exists and is unique. Indeed the barrier diverges at the boundary of the compact Choi set. If r_* is its H_t displacement, stationarity against theta_t and the eigenvalue identity give

    r_*^2/(1+r_*) <= eta ||ghat_t||_(H_t^(-1)) r_*.

Here a<=sqrt(8)eta D<=1/16, so r_*<=a/(1−a)<=1/15. Hence this same minimizer lies strictly inside the displayed matrix box, with a fixed relative margin. Adding the box does not change it.

On that box the coordinate Hessian of F is bounded below by kI and above by L I with L=4k/mu^2. A known-coefficient weak convex minimizer, with objective error

    tau_obj <= delta^2 mu^4/(4096k),                    (19)

has coordinate distance to the exact minimizer at mostsqrt(2tau_obj/k), by strong convexity. Its tangent gradient norm is at mostL times that distance, well belowdelta/4. Round its coordinate entries to a FIXED dyadic grid of mesh

    u <= min{delta mu^2/(128kD), mu/(64kD)}.              (20)

The gradient change is at mostL sqrt(D)u<=delta/32; its H_t displacement changes by at mostsqrt(kD)u/mu<1/64. Including the objective-distance displacement, the rounded point has r<1/2 and residual norm<delta. It is TP exactly by the Pauli affine coordinates, and positivity follows from the first guard. The exact rational checks(10) certify the returned result. There is no recursive denominator growth: all centers are returned on the prescribed grid; all inverses and traces have polynomially bounded rational bit size.

For completeness, this weak solve is a standard finite classical convex task with explicitly bounded size: use an ellipsoid/value-subgradient scheme on the known spectrahedral box with the center C_t and known inner ball determined bymu. PSD separation is obtained by rational LDL tests/negative vectors; the gradient uses rational matrix inverses. Log-determinant values can be obtained from the positive rational determinant and a bounded-precision scalar logarithm. The objective accuracy in(19) has O(N+log d+log(1/delta)) bits, as do the known inner radius and upper bounds. Thus weak convex optimization and subsequent rounding require a deterministic number of bit operations polynomial in N,D and the input precision, not polynomial in1/mu. No source queries are used by this solve. A production solver or its empirical runtime has not been executed; the statement is a finite classical algorithmic cap with certifiable output, not a favorable floating-point result.

**Actual quantum controls.** Every played rational positive TP Choi matrix is realized using the received exact algebraic Gram/Kraus and Stinespring construction: environment at most2d, known unitary embedding at most4d, at most two additional local reset qubits. Dense synthesis costs O(poly(w)4^w) gates before routing/precision overhead. Unlike the slow base, this is applied on EVERY probe, followed by a one-qubit return measurement. Each round's compilation/optimization duration is padded independently of whether it is the terminal role. Charge total polynomial(N,d,log(1/nu)) classical/control cost, with the precision bill including O(N) bits from(18). This is exponential in w and is not a scalable arbitrary-output-register claim. The retained payload's trusted idle storage lasts for the full paid sequence and its errors are included in nu.

**Fresh finite randomness.** T takes log2 N bits. Per possible round, i takes uniform-integer rejection from ceil log2 D bits, and j takes two-bit rejection for three axes; each succeeds with probability at least1/2. Cap each at R=ceil log2(4N/nu_rng) trials and abort to a physical replacement on exhaustion. At most2N draws give failure<=2N 2^(-R)<=nu_rng/2. The two independent signs z,s take two bits. Thus an explicit cap is log2 N+N[2+R(ceil log2 D+2)] fair bits, before any separately declared optional terminal twirl. All abort/compile/storage discrepancies fit ONE whole-process allowance nu; no acquisition confidence event is hidden in(14).

## 7. Conventional comparison and primary context

Positive-loss self-concordant bandit learning is established conventional machinery. [Rakhlin and Sridharan, *Online Learning with Predictable Sequences*, COLT2013](https://proceedings.mlr.press/v30/Rakhlin13.pdf), AppendixA Lemma10 (printed p15) and its proof (printed p25), explicitly give a multiplicative small-loss SCRiBLe bound. The primary PDF and these conditions were retrieved. We do not claim their fixed-loss-vector statement automatically covers this retained quantum-memory process or noisy bit feedback; equations(2),(5)–(14) prove the needed conditional-law and variance transfer directly. The mirror-descent variant and exact rational residual certificates are used instead of an ideal eigenvector/FTRL oracle.

The strongest equally informed conventional learner may use precisely this apparatus and solver. The contribution here is the fully paid ordinary quantum input/actual decoder-return realization and its finite non-reset terminal-channel composition, not a new abstract bandit phenomenon or a practical quantum advantage. The old separable-Pauli learner remains a lower-control competing architecture with the slower epsilon^(-2) source rate. No new sampled simulation is presented as acquisition evidence.
