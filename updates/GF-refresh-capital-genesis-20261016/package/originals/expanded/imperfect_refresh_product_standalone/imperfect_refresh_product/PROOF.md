# Imperfect local refresh: causal product and exact two-gap value

Date: 2026-10-16. This is a separate extension; the delivered ideal-pinch packet is unchanged. Results concern a stipulated mathematical channel contract, not experimentally established refresh quality or hardware availability. Internal mathematical review is not external validation or peer review.

## Main exact result

Keep the same finite-dimensional broad-parity Hamiltonian contract: commuting parities, arbitrary parity-preserving baseline/shared bath, and bounded interactions odd only in their own coordinate. Coordinate i now has one fixed local partial-dephasing channel at time t_i, with no requirement that the t_i coincide. The specified channel is

    D_eta_i(rho) = eta_i rho + (1-eta_i) Pinch_i(rho),  0<=eta_i<=1,
    Pinch_i(rho) = (rho+Z_i rho Z_i)/2.

This is a specified node channel. A finite-width interval with concurrent noncommuting Hamiltonian evolution is not identified with this channel without a separate full-process qualification. The channel acts on that coordinate's parity and as identity on the bath and other coordinates. Its discarded environment is not available to the Hamiltonian controls. Different coordinates' refresh environments are independent. Its coherence multiplier eta_i is fixed, known, and independent of the signs/controls. The own action budgets before and after its node are a_i,b_i.

Put

    p_i = sin²(min(a_i,pi/2)),  q_i = sin²(min(b_i,pi/2)),
    Q_i = p_i+q_i-p_i q_i.

Define F(p,q,eta) by the elementary one-variable optimization

    F = Q + max_{0<=c<=1} [-p q c² + 2 eta sqrt(p q (1-p)(1-q)) c].

Equivalently, for 0<p,q<1:

    if eta²(1-p)(1-q) <= p q:
        F = Q + eta²(1-p)(1-q);
    otherwise:
        F = p+q-2pq + 2 eta sqrt(pq(1-p)(1-q)).

The formulas agree on the boundary. If p=0, F=q; if q=0, F=p; if either p or q is 1, F=1.

**The endpoint all-flipped effect is at most product_i F(p_i,q_i,eta_i) times the specified initial-sector projector. This bound is sharp over arbitrary finite baths.** In particular the minimal two-coordinate staggered case has sharp value F_1 F_2. A shared bath does not enlarge it beyond the product of the exact local imperfect-refresh values.

No hidden ideal pinch is inserted at the partial-dephasing node. Acceptance is the endpoint parity, not a fictitious first-mismatch history there.

## 1. Exact singleton upper bound

Consider one coordinate. All parity-preserving controls or channels can be purified to parity-preserving isometries; retain their unused environment as bath. The first-gap final pure state can be written

    sqrt(1-w) |0,u> + sqrt(w) |1,v>,

with normalized parity-sector vectors u,v and 0<=w<=p. The last inequality is the established one-gap sine bound, uniform over all baths and parity-preserving interventions. Initial mixed states can be purified into a reference.

After D_eta, the diagonal blocks are unchanged and the cross term is multiplied by eta. Fix any second-gap strategy and purify it to an isometry U. For its even-output components set

    A=P_even U|0,u>, B=P_even U|1,v>,
    r=||A||², t=||B||².

Applying the one-gap sine bound to both entering parities gives r>=1-q and 0<=t<=q. Cauchy–Schwarz bounds the final even probability below by

    h_w(r,t) = (1-w)r + w t - 2 eta sqrt(w(1-w) r t).

We may minimize this over the relaxed rectangle r>=1-q, 0<=t<=q. This is a relaxation: no claim is made that every point in the rectangle is a physically valid unitary compression.

For 0<w<1 and fixed r, the minimizing t is

    t_star(r) = min(q, eta²(1-w)r/w).

When the second argument is <=q, the minimized h is (1-eta²)(1-w)r, a nondecreasing function of r. On the capped branch t=q, its derivative in r is

    (1-w) - eta sqrt(w(1-w)q/r).

At the branch boundary this equals (1-w)(1-eta²)>=0; it increases with r. Thus the minimum over r is attained at r=1-q. (The eta=0 case follows directly.) Substitution gives final odd probability at most F(w,q,eta), with F as stated above.

To replace w by its allowed maximum p, note that the minimized-survival construction is nonincreasing in q: increasing q enlarges the relaxed feasible rectangle. Therefore F(w,q,eta) is nondecreasing in q. The explicit expression is symmetric in w and q, so it is also nondecreasing in w. Consequently F(w,q,eta)<=F(p,q,eta). Cases w=0 or 1 follow directly or by continuity.

The proof permits arbitrary shared reference/bath state and arbitrary parity-preserving instruments inside each gap. It does not grant conditioned-on-success filters; all probabilities are unconditional.

## 2. Finite three-level equality witness

Use a positive-parity basis state |0> and two negative-parity states |e>,|s>. Choose c in [0,1] and write

    |v> = c |e> + sqrt(1-c²)|s>.

During the first gap drive only |0><v|+|v><0|, to angle alpha=min(a,pi/2). Apply the actual D_eta. During the second gap drive only |0><e|+|e><0|, to angle beta=min(b,pi/2), with the same phase convention. The remaining sink |s> is untouched in the second gap. Both generators are Hermitian, own-parity odd, and have norm one before multiplying by their allowed envelopes. Stop each drive after the desired angle.

Direct evaluation gives endpoint odd probability

    Q - p q c² + 2 eta sqrt(pq(1-p)(1-q)) c.

The maximizing c is min(1, eta sqrt((1-p)(1-q)/(pq))) for interior p,q. This attains the upper bound. Endpoints are attained by taking the appropriate uncoupled sink or single-gap drive. Tensor independent three-level witnesses across coordinates to attain the product for arbitrary distinct node times.

This witness is in the broad parity contract. Its generic three-level structure is not asserted to be a literal factorized virtual-seed interaction. The upper bound does apply to that subclass; equality for every more restricted subclass is not established here.

## 3. Why the causal product remains valid

Use the private-parity tester construction from the ideal packet, reproduced here in its necessary form. Each tester keeps its parity qubit private. At a control round it coherently copies that parity into a fresh message qubit, sends the message to a common prover, receives a message back, uncomputes the copy and discards the returned message. Every induced Kraus operator preserves the private parity. Any joint parity-diagonal bath unitary is implemented losslessly by the prover controlling a bath unitary on the copied joint parity string and returning the messages unchanged.

Between such rounds tester i applies its fixed budgeted X rotations and, at its own designated node, the ACTUAL channel D_eta_i. Its final test is endpoint odd parity. Independent local channels preserve tensor-product tester structure even when their times differ. Section 1 bounds every single-tester strategy by F_i.

Let T_i be its positive accept operator. The multiround strategy domination theorem gives a normalized positive causal operator R_i with T_i<=F_i R_i. Their product is normalized causal after regrouping factors by the common message rounds. Explicitly, prefix operators satisfy

    Tr_{Y_i,k} R_i,k = I_{X_i,k} tensor R_i,k-1,  R_i,0=1.

Taking tensor products preserves every equation. Positivity gives tensor_i T_i <= (product_i F_i) tensor_i R_i. Pairing with any compatible joint prover therefore bounds all-accept probability by product_i F_i.

The primary theorem is Gutoski–Watrous, *Toward a General Theory of Quantum Games* (2007), Theorem 9, printed p.13, with proof on p.14:
https://cs.uwaterloo.ca/~watrous/Papers/GeneralTheoryQuantumGames.pdf

The unchanged-action simulation from the ideal packet applies verbatim with the prescribed local channels retained at the partition nodes: equalize parity-sector dimensions by padding; remove H0 in its interaction picture; write each off-diagonal contraction K as the mean of two unitaries; represent the corresponding odd generator as the mean of two parity-diagonal conjugates of X; Lie–Trotter approximate at exactly the original own-gap action. Partial dephasing commutes with parity-diagonal H0, including bath-dependent H0, so the interaction-picture step leaves its specified form unchanged. Partitions include all actual channel nodes. Norm convergence passes the bound to every admissible evolution and every initial bath/reference vector, giving the operator-effect inequality. No access to private refresh records or discarded noise environments is needed by the simulator.

## 4. Exact obstruction to retaining the ideal Q

For every eta>0 and 0<p,q<1, F>Q. Thus any nonzero residual coherence can defeat the old ideal-pinch Q if arbitrary broad-contract baths are admitted. The excess is explicitly

    eta²(1-p)(1-q)                         when eta²(1-p)(1-q)<=pq,
    2 eta sqrt(pq(1-p)(1-q)) - pq          otherwise.

A particularly simple witness uses no sink admixture: a=b=pi/6, eta=1/2, c=1. Then p=q=1/4,

    ideal Q = 7/16,
    actual optimal F = 9/16,
    excess = 1/8.

An interior-optimizer rational example uses the same a=b=pi/6 but eta=1/4. The optimal overlap is c=3/4 and

    F=121/256,
    ideal Q=112/256,
    retained-pinch mixture bound=132/256.

Thus the exact optimization is strictly sharper than averaging the separately optimal ideal/no-pinch branches. It still charges the real increase over perfect dephasing.

At eta=0, F=Q. At eta=1, F=sin²(min(a+b,pi/2)), including the regime where optimally choosing c<1 removes backflow and achieves one. Thus the exact formula interpolates between complete refresh and no refresh, without assuming the old bound survives unchanged.

## 5. General independent local testers and limits

For ANY fixed finite collection of independent local testers, positive all-pass domination gives exact product of their individual optimal accept values: the upper bound is the tensor argument, and independent optimal prover strategies attain the product (or approach it when values are expressed as suprema). This statement allows private local memory, specified imperfect local channels, and arbitrary joint prover memory. It is an operational theorem about genuinely independent testers.

To apply it to a Hamiltonian/channel model one must still establish the unchanged-action tester embedding and bound or compute each single-tester value. For the one-node partial-dephasing contract above, both steps and sharp physical witnesses are explicit, so the original model's sharp product is established. No unspecified multiround single-coordinate optimum is being presented as a computed quantity.

The following are outside the claim unless separately reduced:

- correlated refresh environments or a shared untrusted refresh controller;
- access by the controls to discarded noise environments;
- bath-dependent dephasing channels that do not have the stipulated local form;
- state/prover-selected refresh times, or an external schedule correlated with the secret signs;
- observed coherence decay without a justified channel model or parameter bound.

Ordinary independent local noise channels that themselves change parity may still define independent testers, but their single-test value can be much larger, even one. The old action-only F or Q cannot be reused for them without a new singleton analysis.

## 6. Multiple nodes: inherited mixture method with the new finite-action bound

The latent retained-pinch decomposition is inherited, not new. The 2026-10-15 capital notes `measurement_randomizer_bridge/PARTIAL_DEPHASING_BOUNDARY_THEOREM.md` and `PARTIAL_DEPHASING_INDEPENDENT_AUDIT.md` already establish it under the requisite full-joint-channel, fresh-environment, independence, and reservation assumptions. Those notes concern a wider full-stabilizer-group/support-completion contract. This single-parity endpoint theorem does not replace that separate support/reservation machinery or extend to every multi-generator dephaser.

For a single parity with m fixed channels D_eta_k at times t_1,...,t_m, expand each independently as identity with probability eta_k or full pinch with probability 1-eta_k. For each retained-node pattern, merge action intervals across skipped nodes. The ideal fixed-schedule theorem gives

    Q_pattern = 1 - product_blocks cos²(min(block_action,pi/2)).

Thus a valid, generally nonsharp local bound is B=E Q_pattern. Independent coordinate pattern families give the joint bound product_i B_i. This replaces the older quadratic sum-over-merged-block certificate by the sharp finite-action Q for each fixed pattern. It is not an exact multi-node optimization: different latent patterns can demand incompatible controls. For one node at a=b=pi/6, eta=1/2, this bound is 19/32 while the exact optimum is 18/32.

It can be evaluated without enumerating 2^m patterns. Let t_0=0,t_(m+1)=T, A_ik be the total action from t_i to t_k, and c(x)=cos²(min(x,pi/2)). Define G_i as the expected product of block-survival factors from a retained start t_i to the endpoint. Then, backwards for i=m,...,0,

    G_i = [product_(j=i+1)^m eta_j] c(A_i,m+1)
          + sum_(k=i+1)^m [product_(j=i+1)^(k-1) eta_j]
              (1-eta_k) c(A_ik) G_k.

Empty products equal one. The answer is B=1-G_0. Prefix action sums and rolling skip products give O(m²) arithmetic; no division by eta is needed, so zero/one parameters are handled exactly. This is a computable certificate, not a generic exponentially large SDP.

## Channel qualification warning

The map D_eta must hold on the full modeled joint state as D_eta tensor identity on every persistent bath/reference degree of freedom, not only on a reduced-memory marginal. If the discarded dephasing environment later becomes accessible, a controlled quantum eraser can restore coherence, and the single-channel assumption used above no longer describes the process. Generic correlated measurement errors, arbitrary diamond-close instruments, or a measured coherence-decay number alone do not establish this contract.
