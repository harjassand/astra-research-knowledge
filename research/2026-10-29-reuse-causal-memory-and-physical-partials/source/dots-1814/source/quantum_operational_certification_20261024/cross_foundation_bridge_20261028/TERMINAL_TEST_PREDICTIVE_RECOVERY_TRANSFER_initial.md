# From an acquired classical transcript law to retained-memory quantum recovery

2026-10-28. Conditional construction, not yet independently received. This is a task interface lemma for the separate quantum-predictive certificate. It does not assert a new average-fidelity identity or that classical records determine an arbitrary physical quantum process.

## 1. Contract and chronology

A stationary source has an unknown hidden memory. Before the future datum is used, the learner has acquired a predictive model from repeatable whole-process episodes. A fresh whole-process start initializes deployment to the same process state used by the certificate. During deployment the hidden memory is **not reset between interventions**. Each permitted nonterminal action is a fixed physical CP instrument, with declared classical outcome. Action choices depend on preceding classical outcomes and permitted private randomness.

The future d-dimensional datum Q may be entangled with an untouched reference R but is initially independent of the source memory, acquisition records, and runtime controller randomness. It is held without coupling to those systems until the terminal action. Trusted storage and its duration/errors count. This is not a result for preexisting datum–environment correlations, or for an unresettable continuation from the acquisition run.

A finite terminal library A_term consists of actually implemented encoder/source/recovery circuits with output type Q. Every terminal circuit is a total CPTP map on datum plus current memory. Heralded branches are completed by declared replacements and flags are handled consistently. A terminal circuit may have its own fixed finite sequence of source uses and internal adaptive syndrome operations, all charged. It is not a supplied noise inverse or an ideal optimized decoder.

For each terminal action a, the legal acquisition/test library contains the following **ordinary test instrument**: prepare an independent uniform exact state 2-design psi on Q; execute the same terminal circuit a; measure {psi,I-psi} on its decoded Q output; record mismatch y. Input-state randomization and final readout are trusted and paid. The test label is not given to the source or used to choose the decoder/recovery action; it controls only the prescribed input preparation and final projector. No entangled source input is required for this test. For many qubits, a global Clifford/stabilizer design and its actual global readout are needed; product single-qubit tests do not substitute for global Bell fidelity.

Let Pi_H be any declared finite-horizon class of such classical feedback policies with at most H nonterminal native steps followed by exactly one terminal action. Safe abort branches are assigned a total replacement terminal action. Policies are fixed after acquisition but may adapt to subsequent runtime outcomes.

Assume the acquired predictive model satisfies, on a simultaneous count-confidence event,

    sup_{pi in Pi_H} TV(P_pi^test, Phat_pi^test) <= eta,

where the law includes the complete runtime history and final mismatch bit. Crucially the certificate must include the terminal test instruments, not merely preceding gates or unconditioned measurements. The same bound must hold for policies selected using the acquired model. Finite-library observable-rank or CP/gauge assumptions are those of the certificate provider; this lemma does not discharge them.

## 2. Exact counterfactual test identity

Fix a policy pi and a runtime history h preceding the terminal datum. Let p_h be its probability and xi_h its subnormalized hidden-memory state, with trace p_h. Since the datum has not interacted with the process, the terminal circuit selected at h induces a CP map L_h from Q to Q with Tr L_h(rho)=p_h Tr rho. The physical averaged payload channel is

    Lambda_pi = sum_h L_h.

There is no division by a rare history. The final memory and all classical calibration records are discarded in the claimed output convention. Summing over private randomness is included in h or in L_h.

For any CP map L with constant trace p and any exact state 2-design,

    E_psi Tr[psi L(psi)] = [p+d f(L)]/(d+1),
    f(L)=<Phi_d|(id tensor L)(Phi_d)|Phi_d>.

Derivation: the second-moment identity is E(psi tensor psi^T)=(I+d Phi_d)/(d(d+1)). Expanding the channel pairing gives [Tr L(I)+d^2 f(L)]/[d(d+1)]; Tr L(I)=dp. This holds for subnormalized maps and does not assume a unital source.

Therefore the unconditional terminal mismatch probability obeys

    q_pi = Pr_pi^test(y=1)
          = [d/(d+1)] [1-F_e(Lambda_pi)].              (1)

This is an equality between an ordinary hypothetical test execution and the actual future-payload channel. One does not test or destroy the actual unknown datum. The hidden memory may remain coherent, noncommuting and correlated with previous outputs throughout the runtime history. Only the declared initial independence and identical terminal operation are needed. The predictive model need not reconstruct xi_h or possess a channel to the physical source memory.

## 3. Selection theorem

Write c_d=(d+1)/d<=2. Let qhat_pi be the model's terminal mismatch probability. Full-law TV implies |q_pi-qhat_pi|<=eta simultaneously for every policy in Pi_H. Suppose the actual planning algorithm returns pi_hat with certified model optimization slack zeta:

    qhat_pi_hat <= inf_{pi in Pi_H} qhat_pi + zeta.

Then

    1-F_e(Lambda_pi_hat)
      <= inf_{pi in Pi_H} [1-F_e(Lambda_pi)]
                                      +c_d(2eta+zeta). (2)

Proof: apply the uniform reward error at pi_hat and at each comparator policy, use the planner inequality, then (1). No normalized posterior-error bound is used. A model-zero-probability history may receive any safe action; the same full-law certificate still accounts for its actual probability.

If the acquisition event fails with probability beta, actual Bell loss is bounded by one, so the record-averaged bound adds at most beta. A separately quantified complete implementation discrepancy adds its stated task-error debit once. The exact uniform event must be established for the final chosen model/gauge before this expectation conversion; a good fitted likelihood is insufficient.

This is an additive finite-policy Bell-risk guarantee. It is not the main branch's relative fast-accuracy theorem, and it does not give dimension-free diamond distance for the original untwirled channel. Standard Bell-to-complete-error conversions or a separately implemented private whole-logical Pauli twirl retain their actual dimensions/resources and record boundary.

## 4. Acquisition, computation and limitations

The terminal test actions must be included when acquiring the finite core matrices and shifted instrument probabilities. Every repeatable-start episode, intervening operation, rejected branch, global test state, known readout, classical random bit and memory hold counts. The provider's inverse-core sensitivity and any Choi-positivity margin remain real acquisition costs. Repeated whole-process starts during acquisition and one fresh deployment start are indispensable assumptions here; only within-episode independent reset is removed.

A literal finite planner can enumerate all outcome histories and use backward recursion on the known predictive state. This is finite, but generally exponential in H and the action/outcome alphabet. The theorem does not assume polynomial-horizon POMDP planning, solve arbitrary coherent-control optimization, or add terminal encoders/decoders outside the acquired library. Finite numerical planning may use interval values and charge zeta; exact real arithmetic is not required. The same equally informed conventional positive HMM or HQMM planner can use (1)-(2).

The useful bridge is precise: an acquired uniform classical law can guide retention of an unknown quantum datum when the desired fidelity functional itself is a declared terminal ordinary instrument. It does not certify arbitrary new coherent interventions or the state of physical memory. A predictive model based only on deterministic gates, lacking retained measurement outcomes or the terminal tests, does not meet the hypothesis.

## Sources and status

The starting acquired positive predictive framework is Astra's `POSITIVE_GAUGE_THEOREM.md`, SHA256 `8f3e50d85cc58803f29cda029e22c535d20fd2affc2779bf65bc8ad9b681fbef`, fetched through the Astra Research plugin at revision `fb960ac7b07b766d5703c43efbee8cd9d4492718` (2026-10-28 13:40 UTC), retained in imports with its governing scope. It covers its certified classical virtual-state regime. The new CP-predictive provider is separately under construction/review and is not established by this transfer. Ordinary global-state testing is also used, at its reset-source scope, in the already received joint local recovery manuscripts; no reset assumption from those manuscripts is silently waived.

No new acquisition simulation or hardware result is claimed by this derivation. An independent check must verify the subnormalized-history and finite-library chronology before promotion.
