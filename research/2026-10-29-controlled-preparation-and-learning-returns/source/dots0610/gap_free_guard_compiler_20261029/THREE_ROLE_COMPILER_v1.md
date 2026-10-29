# Gap-free three-role guarded encoder/recovery compiler
2026-10-29. New operational synthesis; independent review pending.

## 0. Claim and dependency boundary
This theorem compiles an actual-history expected-loss learner into finite guarded recovery. It does not assume a positive occupation gap, identify a unique frame, predict an independently chosen future channel, or acquire a complete environment. The model-free soundness and structured-family availability are separate claims. Controls, settings privacy, source-port isolation, retained-memory scope and record retirement remain the governing trusted boundary.

The new learner dependency is `gap_free_encoder_attack_20261029/GAP_FREE_ONLINE_THEOREM_v1.md` with `QUADRATIC_NET_AND_FINITE_ARITHMETIC_v2.md`, still requiring its own independent acceptance. Its exact structural promise: one fixed hidden product frame makes every current complete joint source operation commute with the corresponding swap algebra. The source may adapt to all allowed past history and retain arbitrary memory, but cannot choose its current channel after externally learning the fresh candidate frame, role or settings. Quantum response to supplied inputs is permitted. All results below are conditional on the stated learner theorem; this compiler does not silently re-prove or accept its Dirichlet transfer.

For horizon T, probe probability p, rational SO3 net with covering radius epsilon and M points, and rational0<eta<=p/2, its finite exact multiplicative-weights version supplies

 L_T=(9/2)epsilon² T+45[log(M)/eta+eta T/p],
 E sum_{r<=T} sum_{i>0} delta_ir(C_ir) <=(n-1)L_T.      (1)

The full-singlet transfer coefficient is A_n=2^n/Catalan(n/2)=O(n^(3/2)). Each current candidate gives raw full-P Bell loss p_raw,r<=A_n sum_i delta_ir. The independent matching first-moment argument gives q_r<=p_raw,r. These are current-channel quantities, not stationary forecasts. The v2 net can take epsilon=T^(-1/4), M=O(T^(3/4)); a dyadic eta within a factor two of min(p/2,sqrt(p logM/T)) gives L_T=O(sqrt(T logT/p)+logT/p). Finite arithmetic cost is polynomial but very large.

## 1. Actual finite protocol
Choose B=2^h>=32, n=4h, and encode each h-qubit outer symbol in h four-spin singlet blocks, K=B. Use the actual outer quantum code over GF(B) correcting arbitrary t=B/8 symbol errors, carrying h(B-4t) logical qubits in B symbols. The trusted Bell-label four-spin encoder/total reset decoder can be used; earlier matrix completion alone does not establish an elementary gate cost.

Set

 p=1/3, C=C_n=(n+2)/(n-1),
 s=(1-p)/(C+1), a=C s, T=9B,
 J=B, t=B/8, b=B/32.

Thus p+s+a=1, s>=2/9, and C s/a=1. At each ACTIVE round:

1. From only earlier LEARNING records, sample all star-edge experts privately and obtain one consistent product frame. Current candidate sampling precedes the role choice. The source's current operation cannot depend on these fresh private choices through an external control leak.
2. Independently choose LEARNING(p), SERVICE(s), or VALIDATION(a).
3. LEARNING: put a fresh independent product-Pauli probe through the physical source port and obtain the shared bank record. Update all edge experts with importance-weighted estimate1[learning] fhat/p. The unknown payload is NOT used for this call.
4. SERVICE: encode the next outer symbol, apply a fresh uniform physical permutation, apply the current learned local frames, call source, undo frame and permutation, and apply the canonical total reset decoder. Retire permutation keys under the governing interface. No expert loss update is made.
5. VALIDATION: use matching-singlet preparation/survival in the SAME current candidate frame and source port. Count a failure if its survival test fails. Do not feed this outcome into expert weights; it may affect stopping and, through actual retained memory/history, subsequent source behavior.
6. Reject upon failure b+1. Accept after J=B services, including if the Bth service occurs on call T; then apply the total outer decoder. Otherwise reject at call T. Sampling aborts reject. No more source calls occur after stopping.

Candidate changes are allowed between slots. The logical code coordinates are always the same h bare qubits. On each orbit good branch the actual encode/source/decode operation is identity on those coordinates tensor a memory map, even though its physical frame differs from prior slots. A source cannot revisit retired output carriers, reference storage, keys or endpoint trash.

## 2. Why outer-input/memory correlations do not invalidate learning transfer
At an actual observed history H, the unprocessed outer block can be entangled with the source memory M. Its marginal sigma_M nevertheless defines the current independent-probe channel used by a hypothetical learning/validation role. The orbit theorem gives the exact current service CP split

 S=id_symbol tensor B_good+S_bad,
 S_bad*(I)=I_symbol tensor H_bad,
 Tr_symbol S_bad(rho)=B_bad(Tr_symbol rho).

Therefore the virtual bad-service probability on the ACTUAL correlated symbol-memory state is precisely Tr(H_bad sigma_M)=p_raw of that probe-defined current channel. Validation failure has probability q for the same sigma_M. The fresh role/candidate coins and role indistinguishability at the physical port are essential. Matching and orbit service preparations have identical mean P/d at that port; the learning state differs, but the source operation must be a single nonanticipating channel rather than an externally role-selected operation.

The learner theorem is used on actual observed histories and their marginal memories, not on a fictitious iid bath. For expected virtual bad counts, linearity and the current input-independent bad effect suffice; no hidden faults are supplied to the learner. Interspersed learning and validation maps act on source memory and fresh sacrificial probes, not directly on unsent logical carriers. Their memory correlations are retained. On a virtual branch with at most t bad services, the total errors are supported on those t outer slots and the memory, so the existing arbitrary-error Knill-Laflamme correction applies. This is not a classical independent-Pauli fault model.

## 3. Explicit stopping extension
Let tau<=T be the actual stopping time. For analysis only, after tau define the source to be the identity channel with zero swap losses for EVERY candidate and zero test/bad indicators. Continue hypothetical independent role coins to T. This does not assert anything about a physical future source or produce additional data.

The potential inequality can use artificial unshifted feedback0 on all experts after tau; its conditional loss is0. For the shifted finite learner, artificial fhat=87/180 for all candidates produces the same common factor on a hypothetical learning round and leaves all normalized weights unchanged. Its conditional mean is exactly the shifted zero loss. Thus the same finite-horizon expected-regret proof applies to the stopped trajectory. No post-stop measurements or observable actual losses are inserted. A bound derived on the non-stopped actual process cannot be used without this predictable zero-loss extension.

## 4. Soundness for arbitrary noise
For every current state and candidate, the matching/orbit witness gives H_bad<=C E_fail. The three role probabilities therefore give service-bad hazard <= test-failure hazard because C s/a=1. Learning rounds are neutral for these two counters and may change the memory arbitrarily; the conditional inequality is re-established at the next round. Removing neutral times in the existing stopping supermartingale therefore preserves its negative-binomial bound.

With the stipulated coarse-memory interface and retired decoder trash,

 (1/2)||A_acc-id_payload tensor B_acc||diamond
 <=epsilon_B:=Pr[Bin(t+b+1,1/2)<=b]
 <=exp(-3B/128).                                           (2)

B_acc is the ACTUAL accepted coarse-memory map. The finite cap and sampler abort only discard possible accepted branches, never weaken this soundness. No learning accuracy, occupation gap, collective-model correctness or nonzero success probability is needed for(2). It does require the trusted matching/orbit control interface. Unmodelled local gate failures are not erased by this theorem.

## 5. Availability under the common-algebra promise
Let F be the number of validation failures before the stopped trajectory ends, and V its virtual bad service count. Equation(1), current conditional independence of the fresh role coin, and the raw-loss transfer give

 E F <= a A_n(n-1)L_T,
 E V <= s A_n(n-1)L_T.                                   (3)

These expectations are over the actual interleaved source/learner history. In particular they do not reuse an uninterrupted calibration bank or fixed future U0. Markov gives

 Pr[F>=b+1] <= a A_n(n-1)L_T/(b+1).                        (4)

Markov on V also bounds Pr[V>t] by s A_n(n-1)L_T/(t+1), but is NOT needed for availability and is weaker than the model-free accepted soundness bound. Acceptance only requires enough services without too many test failures.

The hypothetical role sequence has T s>=2B expected services, so Pr[fewer than B service coins by T]<=exp(-B/4). If there is no test/sampling abort and at least B service coins, the actual protocol accepts. Consequently

 Pr[accept]>=1-exp(-B/4)-a A_n(n-1)L_T/(b+1)-beta_sampler. (5)

A negative displayed lower bound means no quantitative guarantee at that finite size; do not clip it into a claimed useful rate. For n=4log2B and the rational net/learning rate above, its rejection term is O((logB)^(5/2) sqrt(logB/B)), up to explicit constants. It tends to zero without a source occupation gap. Meanwhile accepted subnormalized soundness decays exponentially in B. This is a gap-free actual-sequence availability theorem, not a frozen learned frame that predicts arbitrary future channels.

For independent fixed initial source memory, coarse-memory closure makes accepted probability independent of payload. Only then, and only if(5) is positive, dividing(2) by that success lower bound yields a normalized accepted logical-channel bound. For payload initially correlated with source memory keep the accepted-map/filter formulation; do not claim a scalar universal conditional fidelity.

## 6. Finite resources and qualified comparisons
This n=4log2B construction is a SCALABLE FAMILY OF SOURCE PORTS, not an asymptotic capacity theorem for one fixed-n physical port. There are at most9B physical n-qubit source calls, including all calibration; at least hB/2 output qubits are encoded. Conditional on acceptance the nominal payload/source-exposure ratio is at least1/72. The expected useful ratio includes Pr[accept]. This excludes local gates, exact expert arithmetic, source-independent storage and outer decoding; it is not an overall efficiency claim. Exact v2 arithmetic uses O(nM) experts and polynomial but enormous bit arithmetic. Physical rational rotation descriptions still require finite-accuracy gate synthesis.

Cap edge-weight sampling, permutation sampling, matching sampling and rational role-coin sampling separately with allocated abort probabilities summing beta_sampler. Uniform bounded-integer draws through binary rejection each fail with probability at most2^-r after r attempts; choose r for the actual total number of draws, including n-1 edge draws on every round. These aborts do not change model-free soundness. Compare to the ideal unlimited-sampler process by coupling; do not infer unbiased candidate distributions conditional on having survived earlier sampling failures. Any separately proved total endpoint/control channel error beta_ctrl can be added by compositional trace-distance coupling to soundness and availability; no particular hardware error budget is supplied here.

Strong comparator: a high-rate full-singlet Schur subcode of power-of-two dimension K>=d/2, with full-path two-MUB tests and bare endpoint Pauli twirling, can use the SAME learner. Generic Dirichlet transfer to that subcode costs D/K<=2D/d, so the same polynomial availability order is available, with constant-factor changes and paid Schur encoder/decoder. Thus there is no generic information-theoretic or asymptotic acquisition superiority over that equally informed alternative. Its endpoint/control complexity differs and must be compared explicitly. Matching tests avoid deploying the service encoder/decoder for each validation but do not certify their faults.

For the simple h-four-spin-block FIXED subcode without orbit, K=2^h but D=2^(4h), so generic transfer D/K=B^3 does not give the same useful T=Theta(B) availability estimate. The improved direct-block transfer under a positive identified frame gap in the previous structured packet does not automatically become a gap-free online loss transfer. No impossibility of a better direct-block learner or theorem is asserted. This gap-free comparison obligation remains open.

Resource-first deployment can instead generate outer encoded Bell resources before submitting an unknown payload, using the separately reviewed finite first-success compiler. It pays clean reference storage, Bell measurements/feedforward and finite retry soundness allocation; unlimited fixed-error retries are unsafe. That option does not make trusted local storage free or solve self-bootstrapping quantum memory.
