# Independent review of the recurrent bath rank consequence

Reviewer: `recurrent_bath_rank`. Date: 21 October 2026.

## Disposition

**The proposed rank and asymptotic separation argument is correct, conditional on the stated spectral intertwining lemma.** No finite reservoir entropy is needed. The complete-process conclusion is stronger than a statement about individual output marginals. The rank constant is sharp in the general unitary model.

This review independently checks the consequence of the intertwining identity. The proof that recurrence implies that identity is assigned to a different reviewer. There was no numerical replay, no external certification, and no historical-priority determination in this review.

## Exact assumptions

Let S be a Hilbert space of finite dimension d, with the same input and output dimension. Let E be a separable Hilbert space, let U be a fixed unitary on S tensor E, and let tau be a normal density operator on E. All retained degrees of freedom belong to E; repeated interactions use no additional discarded or replenished ancilla.

Write tau_t for the reservoir reference orbit. Assume that, for every nonnegative integer t,

    U (I_S tensor tau_t) U* = I_S tensor tau_(t+1).                 (1)

The intended derivation of (1) uses recurrence under maximally mixed reference inputs. The argument below uses (1) itself and therefore does not add an entropy or stationary-state hypothesis.

Choose a threshold c>0 such that

    P_0 = 1_[c,infinity)(tau),
    q = Tr(P_0 tau) > 0,
    eta = 1-q,
    r = rank(P_0) < infinity.

The projections must contain complete eigenspaces. An arbitrary truncation through the middle of a degenerate eigenspace is not justified by (1). Taking smaller thresholds supplies q arbitrarily close to one, because tau is positive trace-class.

Set P_t = 1_[c,infinity)(tau_t). Bounded Borel functional calculus applied to (1) gives

    U (I_S tensor P_t) U* = I_S tensor P_(t+1).                    (2)

Thus every P_t has rank r. Equation (2) holds as an operator identity and controls arbitrary input states, including states entangled with references or earlier outputs.

## Uniform Choi rank approximation

Let b_d be the normalized maximally entangled state between an input S_i and a reference R_i. In n uses, supply n independent b_d states and retain every output and reference. Let Omega_n^rho be the resulting state on (O R)^n when the initial reservoir is rho.

The global unitary is W_n = U_(S_n E) ... U_(S_1 E), with identities on all other systems and references understood. Equation (2) implies

    W_n [S_1 tensor ... tensor S_n tensor ran(P_0)]
       = S_1 tensor ... tensor S_n tensor ran(P_n).

Define sigma = P_0 tau P_0/q. Since P_0 commutes with tau, the exact decomposition is

    tau = q sigma + eta chi,

where chi is a normalized positive state on the complementary spectral subspace if eta>0. Therefore, for every n,

    Omega_n^tau = q Omega_n^sigma + eta Omega_n^chi,               (3)

and

    ||Omega_n^tau - Omega_n^sigma||_1 <= 2 eta.                    (4)

The initial global state b_d^(tensor n) tensor sigma has rank at most r. Unitary evolution preserves rank. Its final reservoir support lies inside ran(P_n), which also has dimension r. A state of rank at most r on H tensor C^r has a marginal on H of rank at most r^2: decompose it into r pure states, each of whose reduced states has rank at most r, and take the span of those supports. Consequently,

    rank(Omega_n^sigma) <= r^2                                  (5)

for every n. Both r and eta were chosen before the horizon.

Equation (4) also follows for every complete causal tester, since the full experiment is a channel acting on its initializer. Thus full strategy distance between the two induced processes is at most 2 eta, uniformly over finite horizons. The rank statement (5) specifically concerns the normalized Choi tester used here.

### Interpretation caveat

The projections P_t can move through infinitely many directions in E. Choosing a basis in each ran(P_t) produces an r-dimensional model with time-dependent unitary interactions. This does not automatically construct one fixed finite-dimensional simulator or a finite clock. No such claim is needed for (3)--(5), and no compactness of the entire reference orbit is being assumed.

## Separation from targets with spreading spectra

For a normalized target state Xi_n on the same finite output/reference space, let kappa_m(Xi_n) be the sum of its m largest eigenvalues, with kappa_m=1 if m exceeds its dimension. Let Q_n be the support projection of Omega_n^sigma. Equations (3) and (5) give

    Tr(Q_n Omega_n^tau) >= q,
    rank(Q_n) <= r^2,
    Tr(Q_n Xi_n) <= kappa_(r^2)(Xi_n).

The variational characterization of half trace distance yields

    (1/2)||Omega_n^tau-Xi_n||_1
       >= [1-eta-kappa_(r^2)(Xi_n)]_+                            (6)
       >= [1-eta-r^2 ||Xi_n||_infinity]_+.

This is a direct support-measurement bound; no sign or factor of two is lost through a triangle inequality.

If ||Xi_n||_infinity tends to zero, then for every fixed eta>0, the liminf of the half trace distance is at least 1-eta. Sending eta to zero proves

    (1/2)||Omega_n^tau-Xi_n||_1 -> 1.                            (7)

The equivalent general condition is that every fixed-rank Ky Fan mass tends to zero. It is exactly divergence of the target min-entropy. A mere positive von Neumann entropy rate does not suffice for this generalization: one-half of a pure state plus one-half of the maximally mixed state on a growing space has positive entropy rate, but retains an eigenvalue approaching 1/2.

## Memoryless channel target

For a fixed channel N:S->S, let J_N=(N tensor identity)(b_d) be its normalized Choi state. Exact independent use has target Xi_n=J_N^(tensor n), and

    ||Xi_n||_infinity = lambda_max(J_N)^n.

A square trace-preserving channel has pure Choi state precisely when it has one Kraus operator K with K* K=I; in equal finite dimensions this K is unitary. Therefore every nonunitary N has lambda=lambda_max(J_N)<1. Equation (6) proves the candidate estimate

    (1/2)||Omega_n^tau-J_N^(tensor n)||_1
       >= [1-eta-r^2 lambda^n]_+.                              (8)

It follows that the half trace distance tends to one for every nonunitary N. The Choi experiment is an admissible finite causal tester. Full strategy distance is at least this full trace distance and is at most two; hence full strategy distance tends to two as well.

This establishes that a process satisfying (1) cannot equal a fixed nonunitary memoryless channel at all horizons. It does not claim that one-use channels, each output marginal, or all classical-input tests already distinguish the process. Retained reference systems and complete output records matter.

## Zero Choi entropy rate without finite reservoir entropy

The same finite-rank mixture gives a useful corollary. All entropies below are finite for each n because the output/reference dimension is d^(2n). The mixture entropy upper bound and (5) give

    S(Omega_n^tau)
       <= h_2(eta) + q S(Omega_n^sigma) + eta S(Omega_n^chi)
       <= h_2(eta) + 2q ln r + 2 eta n ln d.

Dividing by n and taking n to infinity yields limsup S(Omega_n^tau)/n <= 2 eta ln d. Since eta can be arbitrarily small,

    S(Omega_n^tau)/n -> 0.                                     (9)

No subtraction of infinite entropies occurs. Equation (9) concerns the complete Choi state; individual outputs can still have entropy proportional to n. For iid N, S(J_N^(tensor n))/n=S(J_N)>0 whenever N is nonunitary, but (8) is the stronger metric statement.

## Exact sharpness example: repeated SWAP

Take d=r, E=C^d, tau=I/d, and U=SWAP. The reference reservoir state is stationary. Under the Choi tester, for n uses the output/reference state is

    (I_(O_1)/d) tensor
    [tensor_(i=1)^(n-1) b_d(R_i,O_(i+1))] tensor
    (I_(R_n)/d),

with the empty middle product at n=1. It has rank exactly d^2, with every nonzero eigenvalue equal to 1/d^2. This attains the rank bound (5).

The one-use channel is completely depolarizing, whose iid Choi target is I/d^(2n). Direct comparison of these flat spectra gives

    (1/2)||Omega_n - (I/d^2)^(tensor n)||_1
       = 1-d^(2-2n).

This is equality in (8) with eta=0, r=d and lambda=1/d^2. The sharpness example also shows why examining the one-use map alone misses retained correlations.

## No reservoir-independent distinguishing horizon

Fix S=C^2. For each L>=1, let the reservoir consist of L classical bits in the maximally mixed state I/2^L. Apply a controlled-Z to S using the first reservoir bit and cyclically shift the reservoir bits after each interaction. This is one unitary on S tensor E_L. Its maximally mixed reservoir is stationary under maximally mixed reference inputs.

The first L uses employ independent uniformly distributed control bits, so their complete process is exactly L independent uses of the complete dephasing channel. Thereafter the bits repeat. For n>=L, the Choi state is the uniform mixture of 2^L distinct periodic Bell-phase words, whereas the iid dephasing target is uniform on all 2^n phase words. Consequently,

    half trace distance = 0,              n<=L,
                        = 1-2^(L-n),     n>=L.

The two formulas agree at n=L. This proves that no bound on the distinguishing horizon can depend only on d and the target channel, while ignoring the reservoir state.

Even the unitary device can be fixed across this delay family: take E to be the Hilbert direct sum of the finite E_L and U the direct sum of the corresponding controlled-Z/shift unitaries. Each initial state supported on one L sector is normal and stationary. The deterministic sector label is included in E.

More generally, tau = direct-sum_L p_L I/2^L is a normal stationary density operator. For n calls, the reservoir sectors L>=n form an exact iid dephasing component of weight w_n=sum_(L>=n) p_L. Thus

    half trace distance to iid dephasing <= 1-w_n.

Any decreasing tail w_n with w_1=1 and w_n->0 can be realized by p_L=w_L-w_(L+1). Hence the approach to maximal separation can be arbitrarily slow. This matches the need for a quantitative spectral-tail profile in the finite-horizon estimate and remains compatible with the pointwise asymptotic theorem for every fixed normal initializer.

## Limits to retain

- The upstream intertwining lemma must be proved in the complete closed unitary model; arbitrary CPTP devices with a fresh discarded environment can generate independent noise.
- Equal finite input/output dimensions are used in identifying pure Choi channels with unitaries.
- Full process equality and discrimination include references and correlations. Marginal stationarity or a fixed one-use channel is insufficient.
- Finite spectral cutoffs include entire degenerate eigenspaces.
- The proof has no finite reservoir entropy hypothesis.
- The spectral-tail profile and lambda give a quantitative bound, but recurrence alone supplies no reservoir-independent finite horizon or universal rate.
- A moving finite-rank subspace is not a fixed finite-dimensional autonomous implementation.
- The separating Choi tester prepares n maximally entangled d-dimensional input/reference pairs and retains all 2n output/reference registers. Its support measurement depends on the reservoir model and is not proved efficiently synthesizable. The structural strategy-norm conclusion is not an efficient detector or a measured experimental advantage.
- For general correlated targets, diverging min-entropy is sufficient; positive von Neumann entropy rate alone is not the asserted criterion.
- These internal proofs and explicit examples do not establish historical novelty or external certification.

---

# Appendix: independent challenge of faithful-reference recurrence separation

## Disposition and difference from the preceding argument

**The faithful-reference separation theorem is correct.** It does not require the spectral intertwining identity (1), a maximally mixed input reference, finite reservoir entropy, or return of a reservoir purification. It uses recurrence of the reservoir marginal, an invariant marginal on a mathematical purifying system, and prefix consistency of the complete external experiment.

This appendix checks that theorem independently. It does not infer the preceding uniform finite-rank initializer approximation or the entropy-rate statement from the more general hypotheses. The relevant finite-rank concentration is proved at recurrence times; all-horizon metric separation then follows from monotonicity of discrimination under retaining a longer output record.

## Hypotheses and experiment

Let S have finite dimension d, with equal input and output dimension. Let eta be a faithful density operator on S. Let E be separable, let tau be a normal density operator on E, and let U_j be unitaries on S tensor E. A fixed U_j=U is a special case. The sequence U_j is fixed consistently across horizons. There is no discarded or replenished ancillary reservoir outside E.

For independent reference inputs eta, define

    tau_0 = tau,
    tau_j = Tr_S[U_j (eta tensor tau_(j-1)) U_j*].              (A1)

Assume there is a strictly increasing sequence n_k tending to infinity such that

    delta_(n_k) = (1/2)||tau_(n_k)-tau||_1 -> 0.                (A2)

For any n, use the same nonadaptive tester: prepare n independent pure purifications |psi_eta>_(S_j A_j) of eta, pass the S_j systems through the sequential device, and retain every output O_j and reference A_j. Write X_n=(O A)^n and let Gamma_n be the resulting state on X_n. This is a physically allowed tester; it never accesses a purification of the reservoir.

For the proof only, purify tau by |psi_tau>_(E R), with inert R. After all n interactions the state |Psi_n> on X_n tensor E tensor R is pure. Define

    omega_n = Tr_(X_n)|Psi_n><Psi_n|.

Its E marginal is exactly tau_n, because tracing the independent input purifiers recovers the reference inputs in (A1). Its R marginal remains tau_R=Tr_E|psi_tau><psi_tau|, because every interaction acts trivially on R. No assertion is made about the joint ER state returning to its initial pure state.

## Marginal tightness supplies joint finite-rank concentration

Use a Schmidt decomposition

    |psi_tau> = sum_i sqrt(t_i) |e_i>_E |r_i>_R,

where t_i are the eigenvalues of tau in decreasing order. For any epsilon>0 choose finite r so that sum_(i<=r) t_i >= 1-epsilon. Let P and Q project onto the corresponding first r Schmidt vectors in E and R. Thus

    Tr(P tau) >= 1-epsilon,
    Tr(Q tau_R) >= 1-epsilon.

Unlike the spectral-intertwining argument above, this proof does not transport these projections. A cutoff within a degenerate eigenspace is harmless here: only the two tail bounds are used.

At any time n, the variational characterization of half trace distance gives

    Tr[(P tensor I_R) omega_n]
        = Tr(P tau_n) >= 1-epsilon-delta_n,

where delta_n=(1/2)||tau_n-tau||_1. Meanwhile,

    Tr[(I_E tensor Q) omega_n] = Tr(Q tau_R) >= 1-epsilon.

The commuting projections satisfy

    I_(ER) - P tensor Q
       <= (I_E-P) tensor I_R + I_E tensor (I_R-Q).

Consequently

    Tr[(P tensor Q) omega_n] >= 1-2epsilon-delta_n.             (A3)

This is a union bound for two marginal tails. It does not assume E and R are uncorrelated, even approximately. Arbitrary correlations between the reservoir, its purifier, and all earlier outputs are allowed.

The projector P tensor Q has rank r^2. The Ky Fan variational principle therefore yields

    kappa_(r^2)(omega_n) >= 1-2epsilon-delta_n,                 (A4)

where kappa_m denotes the sum of the m largest eigenvalues, capped at one if appropriate. Since the global state is pure, Gamma_n and omega_n have the same nonzero eigenvalues. This statement remains exact for infinite-dimensional ER: the other side X_n has finite dimension d^(2n), so the Schmidt decomposition is finite. Thus

    kappa_(r^2)(Gamma_n) >= 1-2epsilon-delta_n.                 (A5)

The reduced external state Gamma_n need not itself be pure. Purity is used only for the global state across the bipartition X_n : ER.

## Separation from an iid nonunitary target

Let N:S->S be a finite-dimensional CPTP channel and put

    theta_eta = (N tensor identity_A)(|psi_eta><psi_eta|),
    lambda = ||theta_eta||_infinity.

For n independent uses of N under the same tester, the external state is theta_eta^(tensor n). Let T_n be a leading spectral projector of Gamma_n of rank min(r^2,d^(2n)). Equations (A5) and the spectral norm bound imply

    Tr(T_n Gamma_n) >= 1-2epsilon-delta_n,
    Tr[T_n theta_eta^(tensor n)] <= r^2 lambda^n.

The two-outcome measurement {T_n,I-T_n} therefore proves

    (1/2)||Gamma_n-theta_eta^(tensor n)||_1
       >= [1-2epsilon-delta_n-r^2 lambda^n]_+.                 (A6)

All norm conventions are explicit: delta_n is the half-trace return error. If the supplied return error is e_n=||tau_n-tau||_1, replace delta_n by e_n/2. In full trace norm (A6) becomes

    ||Gamma_n-theta_eta^(tensor n)||_1
       >= 2[1-2epsilon-e_n/2-r^2 lambda^n]_+.

Faithfulness of eta is exactly what makes lambda<1 for every nonunitary square channel. To see this without relying on a name for the weighted Choi construction, take Kraus operators K_a of N and write |psi_eta> as the vectorization of sqrt(eta) in its eigenbasis. Then

    theta_eta = sum_a |K_a sqrt(eta)>><<K_a sqrt(eta)|.

If theta_eta is pure, all nonzero vectors K_a sqrt(eta) are collinear. Since sqrt(eta) is invertible, all K_a are collinear. The channel therefore has a single effective Kraus operator K. Trace preservation says K* K=I, and equal finite input/output dimensions make K unitary. Conversely, a unitary channel produces a pure theta_eta. A nonunitary N thus gives a mixed normalized theta_eta and lambda<1.

This is the only use of faithfulness in the separation proof. For a specified comparator N, the theorem also holds for a nonfaithful reference eta whenever theta_eta is mixed. Faithfulness supplies a uniform sufficient condition over every nonunitary square channel.

For each fixed epsilon and its finite r, (A2) and (A6) yield

    liminf_k (1/2)||Gamma_(n_k)-theta_eta^(tensor n_k)||_1
        >= 1-2epsilon.

Taking epsilon to zero after the subsequence limit proves convergence to one along the recurrence subsequence. There is no interchange requiring a uniform spectral-tail estimate in r or a rate for the recurrence times.

## Why subsequence separation extends to every horizon

For m<=n, causality and the fixed independent input preparation give

    Tr_(X_n\X_m) Gamma_n = Gamma_m,
    Tr_(X_n\X_m) theta_eta^(tensor n) = theta_eta^(tensor m).

After output O_m has been retained, all subsequent device interactions act on its complement. They cannot change its joint marginal with the retained earlier references and outputs. Tracing the later input purifiers and outputs gives precisely the same prefix experiment. This remains true in the presence of arbitrary earlier-output/reservoir correlations.

Trace-distance contractivity under this partial trace implies that

    D_n = (1/2)||Gamma_n-theta_eta^(tensor n)||_1

is nondecreasing in n. Since D_n<=1 and D_(n_k)->1,

    D_n -> 1 as n->infinity.                                 (A7)

This monotonicity is not a claim that the leading projectors T_n form a compatible sequence or that Gamma_n has uniformly bounded smooth rank at every n. Only the two families of states have to be prefix consistent. Operationally, a later tester can always discard its additional outputs and perform the earlier discrimination test.

The nonadaptive reference-input tester is one admissible complete causal tester. The full strategy distance is at least its full trace distance and at most two. Therefore complete-process full strategy distance also converges to two, or to one under a convention that divides that distance by two. Adaptive testers are not needed for this lower bound. The proof does not assert that every adaptive input sequence has recurrent reservoir marginal or satisfies (A3).

## Faithfulness boundary: explicit stationary counterexample without it

If the reference is nonfaithful, even exact stationary return of a normal reservoir does not prohibit an exactly memoryless nonunitary channel. The following example shows that faithfulness is an operational assumption, not only a convenience in the proof of lambda<1.

Take a qubit system and eta=|0><0|. Let E have an orthonormal basis indexed by finite subsets F of the integers; equivalently it is the Hilbert space of an infinite two-sided qubit tape with finitely many excitations above the all-zero vacuum. This is separable. Denote the normal pure vacuum state by tau=|empty><empty|.

Let X_0 toggle membership of 0 in a finite subset. Let V shift every tape site one position to the left, V|F>=|F-1>. Both are unitaries. Define the fixed interaction

    U = (I_S tensor V)
        [|0><0|_S tensor I_E + |1><1|_S tensor X_0].

Thus the system controls a CNOT into the tape head at site 0, after which the tape shifts left. At the beginning of every call, site 0 is a fresh pure |0> factor: all previous records lie at negative sites, and all initially positive sites were vacuum. Every record remains inside E and is counted.

The system channel is exactly complete dephasing at each use, independently at every horizon, including for inputs entangled with references or chosen adaptively. Indeed, each call uses a fresh |0> tape qubit as the Stinespring record, and no recorded qubit ever interacts with the system again. The shift only relabels the retained records.

Under the specified reference input |0>, no excitation is ever written, and the vacuum is shift invariant. Hence tau_n=tau for every n: the reservoir reference return error is exactly zero. Nevertheless the complete process is the iid nonunitary dephasing channel.

For a faithful qubit reference, p=<1|eta|1> lies strictly between zero and one. The same reservoir acquires n independent Bernoulli-p records, and its vacuum probability is (1-p)^n. Its half-trace distance from the vacuum is exactly 1-(1-p)^n, so recurrence fails. The counterexample therefore respects and illustrates the precise faithfulness boundary of the theorem.

## Limitations and verdict

- The recurrence times must tend to infinity, and recurrence concerns the unconditional reference orbit in (A1). Conditional return on selected outcomes is a different hypothesis.
- Normality supplies a countable Schmidt purification and arbitrarily good finite-rank marginal cutoffs. No finite entropy of tau or its purifier is assumed.
- The mathematical purifier R is never accessed and need not return jointly with E. Its marginal is invariant simply because it is inert.
- The proof allows deterministic time-dependent U_j as well as a fixed U. It requires one consistent process across horizons and a closed unitary dilation with every environmental record included in E.
- Retained output/reference correlations are essential. The theorem is about complete processes, not about their one-use channels or unreferenced output marginals.
- No finite recurrence-time rate, universal distinguishing horizon, or efficient implementation of T_n is provided. The physical witness uses n preparations of a d-by-d purification of eta, retains all n output/reference pairs, and allows a collective final measurement dependent on the model.
- This appendix does not establish spectral intertwining, a single finite-rank initializer approximation uniform in n, zero Choi entropy rate at every horizon, or historical novelty under the faithful-reference assumptions.

**Independent verdict:** no counterexample to (A6)--(A7) exists within the stated hypotheses; the proof is valid. The nonfaithful stationary tape example is a counterexample to dropping faithfulness. Internal validation of this lemma is not external certification or a novelty determination.
