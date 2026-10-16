# Causal tester embedding for arbitrary staggered parity refresh

Date: 2026-10-16. Complete proof; internally reviewed for the tester interface, causal tensorization, and unchanged-action limit. This is an original reduction using a classical quantum-strategy theorem; no historical novelty claim is made. No numerical search or acquired code was used. No hardware implementation claim follows.

## Claim

Under exactly the finite-dimensional broad parity contract in `joint_refresh_bernstein/PROOF.md`, arbitrary fixed own-coordinate pinch schedules satisfy

    P_s W* P_all-terminal-flipped W P_s <= (product_i Q_i) P_s,
    Q_i = 1 - product_k cos²(min(a_ik, pi/2)).

Here W includes the actual prescribed pinches and no additional pinch on a physical parity is inserted. In particular the minimal staggered two-coordinate case has the sharp bound Q1 Q2. The argument applies to any finite number of coordinates. Existing independent sink witnesses give sharpness over the arbitrary-finite-bath uncertainty class. All auxiliary communication and fine rotations below are a mathematical comparison process, not additional permitted physical interventions.

### Fixed-schedule boundary

The schedules and action envelopes are fixed/exogenous and satisfy the original sign-independence contract. This proof does not cover state-dependent, prover-selected, or outcome-adaptive refresh times: those choices may destroy the independent-tester factorization. Conditioning on an externally chosen clock is legitimate only when, under that conditioning, the schedules and control contract are fixed and the required sign independence remains intact; any resulting bound must then be averaged over that external randomness. No unconditioned product of averaged Q factors is asserted.

## 1. Finite independent testers

First consider a finite circuit built from:

- arbitrary joint-parity-diagonal unitaries D on parity qubits A_1,...,A_d and a common bath B;
- fixed rotations exp(-i theta X_i) on one parity qubit at a time, with theta >= 0;
- prescribed private computational-basis measurements of A_i at that coordinate's own refresh nodes, with the outcomes retained and inaccessible to the controls;
- computational-basis measurements of all A_i at the endpoint.

Each initial A_i is |0>; relabeling handles other specified initial sectors. A reference is included in B. The own-gap rotation action a_ik is the sum of the theta values in that gap.

We embed this circuit in d independent interactive testers, one per A_i, with a single unrestricted joint prover. Tester i keeps A_i PRIVATE. At every control round it:

1. prepares a fresh message qubit M_i in |0>;
2. applies CNOT with A_i as control and M_i as target;
3. sends M_i to the prover and receives a qubit of the same message space back;
4. applies the same CNOT and discards M_i (or keeps it forever as inaccessible garbage).

Between these rounds tester i applies its fixed X rotations and its prescribed own pinches. If it has no rotation or pinch at a given global step it does nothing. Thus all testers have a common finite sequence of message rounds, but their PRIVATE refresh schedules need not coincide. Each tester accepts precisely when its endpoint parity is 1. Initial tester states, tester operations and terminal accept measurements are all tensor products across i. The joint prover has arbitrary shared memory, including B, and may act on all message qubits together.

### 1.1 Every parity-diagonal bath unitary is implemented exactly

Write D = sum_s |s><s|_A tensor D_s, where s is a joint parity bit string and each D_s is unitary on B. The prover applies

    sum_s |s><s|_M tensor D_s

to the message register and B, returning M unchanged. The local CNOT uncomputations reset every message qubit to |0>. On A and B the resulting operation is exactly D, even on coherent superpositions and with arbitrary entanglement with a reference. No measurement, dephasing, conditioning, or discarded success probability occurs.

Therefore every finite circuit above is a legal joint prover strategy against these INDEPENDENT testers. The common bath is on the prover side, not a shared initial tester resource.

### 1.2 Every unrestricted prover preserves each private parity between rotations

For a single tester, purify the prover operation to an isometry U on M and its memory E. The complete copy/prover/uncompute operation has the form

    sum_a |a><a|_A tensor L_a,

where L_a maps E to the returned-message/updated-memory space. Explicitly its action on |a>_A|psi>_E is

    |a>_A tensor (X_M^a tensor I) U(|a>_M tensor |psi>_E).

Each L_a is an isometry. After discarding the message, every induced Kraus operator is block diagonal in A. In particular the prover cannot flip private A, even if it returns an arbitrary message, keeps coherent copies, uses measurements, or correlates its actions across rounds. Purifying all its garbage gives fixed parity-preserving isometries between the charged rotations.

This statement needs no postselected validation test. Granting free normalized filters would be a different model and is not used.

## 2. Single-tester value is at most Q

Fix ANY prover strategy against one tester, with arbitrary initial memory/reference state. For an own gap, condition only on the actual previous own-parity record. The private parity starts in a definite sector; the other memory can be arbitrary and entangled.

Scale all fixed X rotations in this gap by the same complex z. Retain every prover and tester garbage register in a dilation. Project the output onto the opposite parity. The resulting rectangular amplitude F(z):

- is entire of type at most a = sum theta in the gap;
- has norm at most one for every real z, since all rotations are unitary and other maps are isometries;
- obeys F(0)=0, since every map left when rotations are removed preserves the private parity.

The scalar-to-operator sine lemma already proved in `joint_refresh_bernstein/PROOF.md` gives

    F(1)* F(1) <= sin²(min(a,pi/2)) I

on the entering parity sector. The fixed prover strategy is not allowed to depend on z; its optimality at z=1 is irrelevant to the uniform real-axis bound.

Let s_k be this gap bound. For the event of any recorded mismatch, each surviving past history has conditional next-mismatch probability at most s_k. Thus the probability of no mismatch throughout all gaps is at least product_k(1-s_k). Endpoint parity 1 entails some mismatch, so every prover strategy has acceptance probability at most

    Q = 1 - product_k(1-s_k).

The proof permits any number of parity-preserving rounds inside each gap. It never conditions on another tester's future outcome. Arbitrarily large prover memory causes no difficulty: each fixed finite tester has the standard finite-dimensional strategy representation, and its upper bound is uniform in all finite memories.

## 3. Positive causal domination tensors

Primary source: G. Gutoski and J. Watrous, *Toward a General Theory of Quantum Games*, June 22, 2007, Theorem 9, printed p. 13, and its co-strategy version:

https://cs.uwaterloo.ca/~watrous/Papers/GeneralTheoryQuantumGames.pdf

The theorem identifies a tester outcome's maximum forcing probability p with the least scalar admitting domination of its positive outcome operator by p times a normalized non-measuring strategy of the same type. This includes multiple rounds and permits one-dimensional dummy message spaces.

For tester i let T_i be its positive accept operator and p_i its maximum acceptance probability. There is a normalized causal operator R_i of the same tester type with

    0 <= T_i <= p_i R_i.

Because the testers are independent and share a common ordering of rounds, tensoring their normalized causal operators gives a normalized causal operator of the combined tester type. Positivity gives

    tensor_i T_i <= (product_i p_i) tensor_i R_i.

Pair with ANY compatible joint prover strategy S. Normalization implies pairing(tensor_i R_i, S)=1, while positivity preserves the inequality. Therefore

    Pr(all testers accept) <= product_i p_i <= product_i Q_i.

For completeness, use the strategy orientation by giving each tester an initial one-dimensional input and a final one-dimensional output. If there are r message exchanges, there are n=r+1 tester turns: send the first copy, then receive/finish a round and send the next copy, and finally receive/finish the last round and output only its private decision. The normalized positive operators R_i admit positive prefixes R_i,k satisfying the ordinary comb constraints

    Tr_{Y_i,k} R_i,k = I_{X_i,k} tensor R_i,k-1,
    R_i,0 = 1,   k=1,...,n,

with tensor factors reordered consistently and X_i,1 and Y_i,n one-dimensional. For the combined tester set R_k = tensor_i R_i,k, with the canonical regrouping by round. Taking the partial trace over all current outputs gives

    Tr_{tensor_i Y_i,k} R_k
      = tensor_i [I_{X_i,k} tensor R_i,k-1]
      = I_{tensor_i X_i,k} tensor R_{k-1}.

Thus the product is explicitly dual-feasible, with no extra premise about simultaneity of private pinches. Every coordinate has a copy-message round at each global control opportunity; rotations of angle zero and no-op private steps pad its local schedule. The initial state of any common bath or reference belongs to the joint prover co-strategy. It is not a shared initial tester state. The accept-outcome operator is tensor_i T_i because all tester initializations, channels and outcome projectors are local tensor factors.

This is the exact causal inequality needed here. It handles arbitrary coherent joint prover memory. It does not assume independent prover actions or independent measurement outcomes. The private pinches occur at different local rounds without disrupting the tensor product of testers.

For two factors the Loewner step can be seen directly by writing

    p1 p2 R1 tensor R2 - T1 tensor T2
      = (p1 R1-T1) tensor (p2 R2) + T1 tensor (p2 R2-T2),

a sum of positive operators.

This argument is about maximizing an all-pass outcome. Quantum hedging examples concern different objectives and do not invalidate this positive domination argument. See Molina and Watrous, *Hedging bets with correlated quantum strategies*, https://arxiv.org/abs/1104.1140, for that distinction; the multiround result actually invoked here is the Gutoski–Watrous theorem above.

## 4. Embedding every admissible finite-dimensional Hamiltonian

It remains to show that the finite circuits of Section 1 approximate every allowed physical evolution, without increasing the own-gap action budgets. This is essential: causality alone or an analogy with tests would not prove the result.

### 4.1 Equalize sector dimensions and remove the baseline

Decompose the original Hilbert space into its joint parity sectors. Choose a common dimension d at least as large as every sector, isometrically embed each sector into a copy of C^d, and pad all operators by zero on the orthogonal complements. The enlarged space is

    (C²)^{tensor number_of_coordinates} tensor C^d.

The original embedded space is invariant under the padded Hamiltonian and pinches. Norms and all observed probabilities are unchanged. Unequal original sector dimensions therefore pose no obstruction.

Pass to the interaction picture of H0. Its propagator commutes with every parity and hence with all prescribed pinches and endpoint effects. The transformed V_i remain own-odd, other-even, and satisfy the same norm envelopes. We may consequently assume H0=0. Alternatively its parity-diagonal propagators are free D gates in Section 1.

### 4.2 A norm-bounded odd Hamiltonian is an average of conjugated X gates

For one coordinate i, write an own-odd, other-even Hermitian contraction B in the two blocks of its own parity:

    B = [ 0  K ; K*  0 ],  ||K|| <= 1.

Here K is block diagonal in all OTHER parity labels. Work separately in each such block, whose dimensions are equal after padding. A square contraction has a polar decomposition K=W P with P>=0, P<=I, and W extendable to a unitary on the full equal-dimensional space. Put

    U_plus  = W (P + i sqrt(I-P²)),
    U_minus = W (P - i sqrt(I-P²)).

Both are unitary and K=(U_plus+U_minus)/2. Choose the constructions separately by other-parity block, so U_plus and U_minus preserve all those labels. Define

    D_plus  = diag(U_plus,I),
    D_minus = diag(U_minus,I).

These are JOINT-parity-diagonal unitaries, and

    B = (D_plus X_i D_plus* + D_minus X_i D_minus*)/2.

Therefore for a nonnegative action theta,

    exp(-i theta B)
      = lim_{m->infinity}
        [ D_plus exp(-i theta X_i/(2m)) D_plus*
          D_minus exp(-i theta X_i/(2m)) D_minus* ]^m.

Each approximating circuit uses only legal D gates and fixed private X rotations with total own action EXACTLY theta. No negative time, postselection, uncontrolled extra rotation, or access to private records is used.

### 4.3 General time dependence and simultaneous coordinates

Take a finite time partition containing EVERY prescribed pinch node. On each cell I define

    A_i,I = integral_I V_i(t) dt,
    theta_i,I = integral_I j_i(t) dt.

Then ||A_i,I|| <= theta_i,I. If theta_i,I=0, A_i,I=0. Otherwise B_i,I=A_i,I/theta_i,I has the contraction form in Section 4.2. The cell approximation exp(-i sum_i A_i,I) can be Lie–Trotter split into the coordinate exponentials, each approximated as in Section 4.2. Total action charged to coordinate i in cell I remains theta_i,I exactly. At the prescribed nodes apply only the original own pinches.

These averaged-cell propagators converge to the actual time-ordered propagator as the mesh is refined in integrated total action. One direct estimate is available without regularity assumptions on V_i: if b_I=integral_I sum_i j_i(t)dt, both the time-ordered propagator and exp(-i integral_I sum_i V_i) equal I-i integral_I sum_i V_i plus a remainder of norm at most exp(b_I)-1-b_I. The discrepancy on a cell is at most twice this quantity. Since sum_I b_I is fixed and max_I b_I tends to zero, the sum of these errors tends to zero. For real Hermitian evolution all exact and approximate cell propagators are unitary, so the telescoping error is bounded by the sum of local errors. The finite pinch channels or their isometric dilations are contractions and preserve this convergence.

For each finite partition choose finite Trotter orders large enough to make the total additional approximation error arbitrarily small. Thus there is a sequence of finite circuits of Section 1 converging in operator/dilated-channel norm to the actual prescribed-record process, with EVERY own-gap action exactly its original a_ik. The number of tester rounds increases along the sequence; the scalar bound product_i Q_i is independent of that number.

## 5. Passage to the target effect and sharpness

Fix any initial unit vector in the specified joint parity sector, including arbitrary bath/reference entanglement. Each approximating circuit is a joint prover strategy for independent testers with singleton bounds Q_i, so its endpoint all-flipped probability is at most product_i Q_i. Norm convergence passes this bound to the original evolution. Since the initial vector was arbitrary, the asserted operator-effect inequality follows. Mixed states follow by linearity. If any own-gap action is zero, the simulator simply has no corresponding rotations. If Q_i=0 for any coordinate, it has no charged rotation in any gap and its private parity cannot flip, so the product-zero case holds directly as well.

For each coordinate, use its established finite fresh-sink construction separately on its actual own schedule, and take the tensor product across coordinates. The coordinate evolutions commute and their baths are independent. Their individual endpoint probabilities are exactly Q_i and their joint probability is the product. Distinct refresh times do not affect this factorization. Therefore the fixed-schedule worst case over arbitrary finite baths is exactly product_i Q_i, not merely bounded above by it.

### Stronger recorded-event version

The same argument bounds the event that every selected coordinate has at least one mismatch between successive own records. Replace each tester's accept condition by its private permanent first-mismatch flag. Section 2 already bounds exactly that acceptance probability by Q_i; tester independence and all subsequent steps are unchanged. The simulating prover still never sees these records. This stronger event includes all endpoint parities flipped and has the same independent-sink equality witness.

## 6. Audit checklist and limits

- The actual process is embedded in a LARGER prover class, so its upper bound is valid; no claim that every enlarged prover belongs to the original Hamiltonian class is needed.
- The enlarged class cannot flip the tester-private parity except through its budgeted rotations. Its universal singleton Q bound is proved explicitly, rather than assumed from a norm constraint on an unrestricted channel.
- Coherent-copy messages are uncomputed for the simulating strategy; hence no unwanted physical pinch is inserted.
- Arbitrary strategies can leave garbage, but this preserves private parity and is already covered by the singleton proof.
- All-pass tensorization is invoked only AFTER establishing independent testers and the exact unchanged-action simulation.
- No normalized postselection, future-success conditioning, private-record feedback, or extra parity-flipping resource occurs in the simulator.
- The finite-dimensional sector padding and all approximation stages are explicit. The argument is uniform in finite bath dimension.
- The earlier functional counterexamples remain correct. They lack this causal independent-tester realization with the stated singleton value.
- The original factorized virtual-seed subclass is included because the proved claim is for the broader parity contract.
- The outcome is an ideal-model mathematical bound. It makes no finite-width controller, scalable hardware, or physical-fault interpretation claim.

## Internal mathematical review

A separate internal reviewer read the complete proof and found no substantive gap. Their requested clarifications about one-dimensional dummy messages, strategy orientation, and round-wise tensor regrouping are incorporated above. This was an internal mathematical check, not external validation or peer review. The review separately checked the arbitrary-prover diagonal interface, the exact-budget approximation for merely integrable envelopes, and the primary Theorem 9 attribution.

## Appendix A. Analytic input and explicit equality construction

### Scalar-to-operator sine lemma

If F is an entire operator-valued function of exponential type at most a, ||F(x)||<=M for real x, and F(0)=0, then

    ||F(1)|| <= M sin(min(a,pi/2)).

For fixed unit vectors u,v choose a phase so that the scalar f(1)=exp(-i phi)<u,F(1)v> is real nonnegative. The entire real-on-real function g(z)=[f(z)+conjugate(f(conjugate(z)))]/2 has type at most a, satisfies |g(x)|<=M on the real axis, and g(0)=0. The sharp real Bernstein inequality g'(x)^2+a²g(x)^2<=a²M² bounds the derivative of arcsin(g/(M+epsilon)) by a. Integrating from zero to one and letting epsilon decrease to zero proves the sine bound when a<=pi/2; otherwise use ||F(1)||<=M. Take the supremum over u,v. Zero M or a follows by continuity or constancy.

Primary reference for the sharp real Bernstein inequality: R. M. Redheffer, *On a theorem of Plancherel and Pólya*, Pacific Journal of Mathematics 3 (1953), 823–835, Theorem 11, printed pp. 832–833, https://msp.org/pjm/1953/3-4/pjm-v3-n4-p11-s.pdf . Its prior verification is documented in the input proof. In the present finite tester, exponential type follows directly from ||exp(-iz theta X)||<=exp(theta |Im z|) and the norm-one intervening isometries.

### Fresh-sink equality for arbitrary fixed schedules

For coordinate i with m_i own gaps use basis |0>,|1>,...,|m_i>, with parity + on |0> and - on all |k>, k>=1. In gap k drive only the two-level transition |0><k|+|k><0|, with envelope j_i until accumulated angle min(a_ik,pi/2), then stop. Every previous sink is untouched by every subsequent own-gap drive. The prescribed pinch at the end of each internal gap makes the remaining |0> survival branch incoherent with newly occupied |k>. Endpoint measurement supplies the final record. Starting in |0>, survival probability after all gaps is exactly product_k cos²(min(a_ik,pi/2)); every other branch ends in odd parity. This uses m_i+1 levels and norm no greater than j_i at all times. Tensor these coordinate constructions and their actual distinct pinch schedules. Every generator is own-odd and other-even, and the joint terminal-flip probability is exactly product_i Q_i. This construction establishes broad-contract sharpness without requiring a common clock.
