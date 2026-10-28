# A causal extension of random dimension reduction, with persistent receiver memory

27 October 2026. New construction candidate; independent receiving required. This addresses the root's precise causal-completion question, not the full R^2 acquisition target. The construction supplies **existence and a finite generic implementation**, not a polynomial-in-N,log(s) circuit. It uses only receiver processing of ordinary source outputs and retains quantum memory. No coherent encoder/control register bypasses the source.

## 1. Target and the missing global condition

Fix `1<=k<=s`. For each n we seek a CPTP channel

`T_n : L((C^s)^tensor n) -> L((C^k)^tensor n)`

such that for every unknown isometry W:C^k->C^s and EVERY operator X on `(C^k)^tensor n`,

`T_n(W^tensor n X W*^tensor n) = integral U^tensor n X U*^tensor n dU`,       (1)

and, crucially, the global causal consistency relation holds on arbitrary physical input operators:

`Tr_output_n T_n(X) = T_(n-1)(Tr_input_n X)`.                                (2)

Consistency only on promised common-support inputs would be insufficient to infer a physical online dilation. The construction below proves (2) on the full operator space.

## 2. The standard reduction on allowed Schur sectors

Schur–Weyl decompose the physical tensor power as

`(C^s)^tensor n = direct_sum_(lambda partitions n, rows(lambda)<=s) Q_lambda^s tensor P_lambda`.

The corresponding k-dimensional tensor power contains exactly the diagrams with at most k rows. Let P_n be the physical central projector onto those allowed diagrams, and Q_n=I-P_n. (Here Q_n denotes a projector, not the Schur irreducible register Q_lambda^s.)

Define the CP trace-nonincreasing map S_n by discarding cross-diagram blocks and, on each allowed diagonal block, tracing out `Q_lambda^s` and replacing it by `I_(Q_lambda^k)/dim(Q_lambda^k)`, preserving the symmetric-group multiplicity register P_lambda. Forbidden diagrams map to zero. Thus

`Tr S_n(X)=Tr(P_n X)`.

This is the usual exact random-dimension-reduction operation on its promised sector. It has three elementary properties:

1. `S_n(Ad_(W^tensor n) X)` equals the Haar twirl in (1), by naturality of Schur modules under isometries and the Haar block decomposition.
2. Its output commutes with every `U^tensor n`, U in U(k).
3. For every permutation pi in S_n and X supported on P_n,

`Tr[Pi_k(pi) S_n(X)] = Tr[Pi_s(pi) X]`.                                     (3)

The reason for (3) is that permutations act only on the preserved P_lambda register. These identities apply to arbitrary non-Hermitian operators as well; no iid assumption is used.

## 3. Recursive TP completion

Set `T_1(X)=Tr(X) I_k/k`. For n>=2 define

`T_n(X) = S_n(P_n X P_n)
        + T_(n-1)(Tr_input_n[Q_n X Q_n]) tensor I_k/k`.                      (4)

S_n already kills forbidden/cross blocks, so its displayed P_n sandwiches can be omitted. Both summands are CP; their traces sum to Tr X. Hence T_n is CPTP. Every promised W^tensor n input lies in P_n, so (1) is preserved EXACTLY.

By induction, T_n is invariant under conjugation of ALL physical inputs by `V^tensor n`, V in U(s), and its output is invariant under `U^tensor n`, U in U(k). The replacement completion is order-specific; output permutation covariance is deliberately NOT asserted.

## 4. Proof of full prefix causality

We prove (2) by induction, splitting X into its P_n/Q_n diagonal blocks and cross blocks.

### Allowed block

Let X=P_n X P_n. Restriction of an allowed S_n irrep to the prefix subgroup S_(n-1) has at most k rows, by the Young branching rule. Therefore

`Tr_input_n X = P_(n-1) (Tr_input_n X) P_(n-1)`.

This statement for arbitrary X follows from the subspace inclusion `range(P_n) subset range(P_(n-1) tensor I_s)`.

Both `Tr_output_n S_n(X)` and `S_(n-1)(Tr_input_n X)` are U(k)^(tensor(n-1))-invariant. For every prefix permutation pi, property (3) shows that their expectation against Pi_k(pi) is the SAME physical expectation against `Pi_s(pi) tensor I_s`.

The span of prefix permutation operators is the whole commutant of U(k)^(tensor(n-1)). Two operators in this commutant with equal Hilbert–Schmidt pairings against that span are equal (take linear combinations and adjoints). Hence

`Tr_output_n S_n(X)=S_(n-1)(Tr_input_n X)
                     =T_(n-1)(Tr_input_n X)`.                              (5)

### Forbidden block

For X=Q_n X Q_n, (2) follows immediately from the second summand of (4) and `Tr(I_k/k)=1`.

### Cross blocks — the essential global extension check

Let X=P_n X Q_n or Q_n X P_n. Formula (4) sends it to zero. To prove the right side of (2) is also zero, let B be ANY operator on the preceding output registers. Input-U(s) invariance of T_(n-1) implies

`T_(n-1)^*(B) in Comm{V^tensor(n-1):V in U(s)}
                 =span{Pi_s(pi):pi in S_(n-1)}`.

Consequently `T_(n-1)^*(B) tensor I_s` commutes with the CENTRAL S_n projector P_n. Its pairing against a P_n/Q_n cross block is zero. By duality,

`T_(n-1)(Tr_input_n X)=0`.

This proves (2) on every matrix block, hence on the FULL input operator space. Complete/reference-preserving equality follows because it is an equality of linear maps.

## 5. Online physical realization and resource contract

The Choi matrices of the T_n satisfy the deterministic-comb trace constraints by (2). [Chiribella–D'Ariano–Perinotti, *A theoretical framework for quantum networks*, Theorem 3, equations (25)–(32)](https://arxiv.org/html/0904.4483) explicitly realizes any such positive normalized family by sequential known isometries. Each step receives one physical s-output and the retained receiver memory, emits one k-output immediately, and updates the memory. Their Section III.3.3 bounds memory dimension by the maximum Choi rank of a prefix. For this construction a coarse bound is

`dim(memory after n) <= rank Choi(T_n) <= (sk)^n`.

Thus O(n log(sk)) memory QUBITS suffice at this existence level, but a generic matrix/isometry construction has exponentially large descriptions and gates. A finite known-channel Choi calculation, Stinespring factorization and dense unitary synthesis supplies a finite implementation for each predetermined horizon N. It does not supply `poly(N,k,log s)` gates. Matrix-conditioning, precision and total comb/strategy error must be paid; an ordinary noninteractive channel-error statement must not automatically be substituted for the interactive transcript error.

No source query is used to synthesize T_n. Its matrices depend only on s,k,n and known representation data. The persistent memory may retain earlier physical outputs and their relational information. It is NOT a protected logical/control register prepared before the unknown source, nor an unknown-source inverse/environment. There is no assertion that the emitted outputs alone carry a reusable classical frame, or that the memory can be reset without losing alignment.

For any fixed W, the ENTIRE restricted N-slot channel equals the common-U Haar channel in (1). Both are causal channels. Linking arbitrary adaptive ordinary preparations/measurements into their slots therefore gives identical interactive transcript/reference laws. Conditional on the mathematical common U, each new ordinary source output is in the SAME U-coordinate system. Future input controls may be classical functions of earlier outcomes without requiring coherent control of the unknown source. U need never be observed or sampled physically.

The horizon must include all planned validation and payload slots. One may continue the consistent family with its quantum memory; a finite compiled circuit cap/horizon is still required for a deterministic implementation/resource claim. A physical payload after the horizon cannot be decoded using an old compressed-space classical D alone.

## 6. The antisymmetric boundary is resolved by order, not ignored

For k=2, s>=3, n=3, a physical fully antisymmetric state is forbidden. Its first two particles are supported on the antisymmetric physical sector, so their required T_2 output is the qubit singlet. Equation (4) maps the three-particle forbidden state to

`|singlet><singlet|_(outputs1,2) tensor I_2/2`.

The first pair is correct and the channel is causal. It is not invariant under permutations exchanging the third output with earlier outputs. Requiring full output permutation covariance would indeed conflict with the pure-singlet marginal. Causality does not require that extra symmetry, and (4) does not impose it.

## 7. What this unlocks, and what it does not

The common output support of the supplied quaternion source family has dimension at most 8R: each of the four basis encoders contributes at most 2R dimensions. This is a valid common-support bound without supplying its basis. Taking `k=min(s,8R)` makes the online construction applicable to all ordinary adaptively chosen controls and the final payload.

As an EXISTENCE/resource-expensive corollary, it repairs the alignment premise in `ordinary_adaptive_nonnegative_design_bridge_20261027.md`: run that weighted action-design method on the emitted k-registers while preserving the receiver memory. The statistical source cap becomes `O_tilde(k^4/(gamma epsilon))=O_tilde(R^4/(gamma epsilon))`, with no physical geometric grid factor and no coherent encoder bypass. The scalar empirical-risk proof holds for each mathematical U with the same uniform constants; averaging U preserves its failure bound. The selected compressed-space decoder must be used on the later ONLINE-compressed payload in the same ongoing memory process. It is not a bare physical-space reusable decoder.

This improves the ordinary statistical construction beyond ambient s^4, but still pays R^4 rather than R^2 and does not have efficient processing. A collective quantum active-design learner and an efficient causal-RDR implementation remain separate proof obligations. No lower bound against either is proved. The conventional comparator with identical receiver memory and controls can use this same construction.

## 8. Check and blocker state

`causal_random_dimension_reduction_extension_check.py/.json` constructs small standard reductions from permutation Gram matrices, tests complete positivity/TP and full prefix causality on ALL matrix units at s=3,k=2,n<=3, and tests the common-support identity plus forbidden-boundary behavior. These are finite checks supporting, not replacing, the induction.

Status: explicit causal TP-extension candidate with full arbitrary-input proof; independent receiving pending. Blocker for efficient target: compile its sequential dilation with polynomial known processing, then replace scalar d-log(M) action regression by a collective rank-squared decision-risk learner. No tool permission denial/retry occurred.

### Confidence/deployment refinement for the acquisition corollary

The latent-frame event `f_selected(U,record)<=B` is not automatically a quality statement conditioned on every exposed physical record. There are two legitimate uses:

1. **Clean fresh-bank route.** Retain only the selected encoder x, not its compressed decoder. Pointwise, `ell_opt(x)<=f_selected(U,record)`. Therefore the global-good-encoder event `ell_opt(x_selected)<=B` depends only on the actual selected index and the fixed source, not on latent U, and has failure at most the scalar learner's beta. Discard discovery memory. Train a NEW received direct-Bures decoder for x jointly with each later payload. Configure that learner with multiplicative slack gamma/8 and additive slack epsilon/4. Since the selector's factor is at most 1+gamma/2 and its finite-net/statistical additive cost is at most epsilon/4, the second factor satisfies `(1+gamma/8)(1+gamma/2)<=1+11gamma/16<1+gamma`, and total additive cost is below epsilon. Discovery costs `O_tilde(R^4/(gamma epsilon))`; each later payload additionally costs `O_tilde(R^2/(gamma epsilon))` fresh calibration calls and its one transmission. This is the same averaged-fresh-bank deployment contract as the received direct-Bures encoder theorem, now without the physical epsilon^-3/2 grid factor.
2. **Retained-frame route.** Continue the SAME online quantum memory through payload slots and apply the selected compressed decoder there. The interactive identity justifies this physical channel, but an averaged loss statement pays the bad latent-event probability beta. One can set beta=O(epsilon) and budget it; a stronger exposed-record confidence claim needs separate posterior/Markov or validation accounting. It is not implied for free.

Approximate online implementations require an interactive/strategy or per-step diamond telescoping budget for the complete adaptive transcript; a parallel-channel diamond bound alone is not a proved substitute. The source precision and memory horizon remain charged.
