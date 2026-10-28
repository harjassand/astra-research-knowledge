# A finite capped two-way reference factory from an ordinary-learned Bell-fraction seed

28 October 2026. New composition candidate; independent receiving is pending. This is a resource-acquisition extension, not another strict-ordinary learner: only WARM discovery is ordinary. Subsequent Bell-pair generation sends locally entangled halves through the source, and recurrence/teleportation use explicitly supplied, paid bidirectional authenticated classical communication. No protected quantum link or shared entanglement is furnished. The same equally informed conventional protocol can perform the construction.

The established recurrence, teleportation and five-qubit code are not claimed as new. The new obligation here is a learned generic seed, deterministic raw cap, selected-pair conditional law, actual code-teleportation circuit and complete finite-history reference interface.

## 1. Source and resource contract

Use the stationary independently reset source, fixed four-real-coordinate calibrated isometric encoder family, valid uniform encoded Choi-rank bound R, common output dimension k<=min(s,8R), and received persistent causal receiver-frame compiler. The full CPTP decoder is acquired, not supplied. The frame is initialized for the ENTIRE public horizon and retained through warm discovery, pair generation and any later data/payload slots. Its exact arbitrary-operator law supplies one latent common U; neither U nor a classical support alignment is available physically.

Supply rational 0<g<=1/4 and the promise

    max_(x,D CPTP) F_e(D E_x)>=1/2+2g.                  (P)

The sender and receiver have trusted local quantum memory, known local gates, shared finite randomness, and a classical channel in BOTH directions with charged messages/latency. The classical communication is not secretly transmitted by an uncounted quantum link. Its reliability or authentication is an explicit resource assumption; hardware/security qualification is not inferred from source calibration. There is no initial remote entanglement.

For Q>=1 future reference qubits, budgets beta_t,beta_v,beta_r in(0,1), target code discrepancy delta_c in(0,1), and finite whole-process discrepancy nu, the construction below has a deterministic raw-call cap. It implements a total CPTP transfer from Q sender qubits to Q receiver qubits, allowing arbitrary correlations with untouched systems and later data. On abort it supplies fixed replacements, never normalized successful-branch promises. Its averaged unhalved complete error is at most

    2(beta_t+beta_v+beta_r)+delta_c+nu.                 (1)

All calibration/factory records are discarded in this tested-output convention. No quality is asserted for every revealed record.

## 2. Ordinary warm acquisition and fresh Bell-fraction certificate

Use the received ten-anchor inverse-square baseline with its accuracy parameter epsilon_0=2g, but with arbitrary joint confidence beta_t in its ten density banks instead of tying confidence to epsilon_0. Its good-event proof is unchanged. Set

    delta_a=g/512, m_a=delta_a^2/8,
    d=2k, r=min(d,3R), D_a=nextpow2(d r),
    n_a=ceil[(80 D_a/m_a) log(120 D_a/beta_t)].

There are ten actual ordinary loss-state banks, each of n_a source calls. Retain the baseline's exactly feasible positive-model fit, full-CPTP decoder SDPs, rational inward rounding, and encoder grid at epsilon_0. All its finite arithmetic tolerances are retained. On its simultaneous latent good event,

    ell_selected<=ell_star+epsilon_0/4=ell_star+g/2,
    F_selected>=1/2+3g/2.                              (2)

The frame and decoder are frozen, not rebuilt in a new gauge. The source coefficient fit is only a bounded physical prediction lift; no Choi-completion state is learned or prepared during warmup.

For a FRESH holdout, choose the six Pauli eigenstates uniformly, send/decode them with this fixed policy, and test return to the chosen state. Mismatch probability q obeys q=(2/3)(1-F_selected). With

    n_v=ceil[(18/g^2) log(2/beta_v)],
    Fhat=1-(3/2) qhat,

Hoeffding gives |Fhat-F_selected|<=g/4 with conditional failure at most beta_v, pointwise in U and the frozen training record. Accept iff

    Fhat>=1/2+5g/4.

On the two good events, acceptance occurs and F_selected>=1/2+g. Even without promise (P), false acceptance of a seed below this latter threshold has probability at most beta_v. This is not posterior certification after division by a small acceptance probability. Under (P), all warm aborts and bad accepted seeds together have probability at most beta_t+beta_v.

The deterministic warm cap is N_w=10n_a+n_v=O_tilde(kR/g^2), with log confidence and the explicitly paid polynomial classical/frame/control costs. The high-confidence branch is used here, not merely the predecessor's displayed averaged risk.

## 3. Actual raw Bell pairs and a finite recurrence depth

After warm acceptance the sender locally prepares a Bell pair, retains its first qubit, and sends the second through the frozen known seed encoder, the actual source, the next SAME frame step, and the learned decoder. This uses ONE raw call and creates the actual normalized two-qubit Choi state of the learned seed. Apply an independent bilateral Clifford twirl Ubar tensor U preserving Phi_2. After discarding its key, the pair is exactly

    sigma_F=F Phi_2+(1-F)(I_4-Phi_2)/3,
    F>=1/2+g,

conditional on U and the warm record. Separate raw calls produce tensor powers in that exact reference experiment, including the sender halves. The received arbitrary-operator common-frame identity, not a physical reset of the processor memory, justifies this statement.

One recurrence attempt uses two pairs. Both parties apply CNOT from their first qubit to their second, measure the second pair locally in Z, exchange the two bits and keep the first pair iff the bits agree. Discard the second pair in every case. Reapply the independent bilateral Clifford twirl after EVERY successful attempt. If a Bell label is (x,z), bilateral CNOT maps labels

    (x_1,z_1),(x_2,z_2) -> (x_1,z_1+z_2),(x_1+x_2,z_2),

with binary addition. Passing is exactly x_1=x_2. The accepted identity weight and passing probability are therefore

    P(F)=(8F^2-4F+5)/9>=5/9>1/2,
    R(F)=(10F^2-2F+1)/(8F^2-4F+5).                    (3)

The target fidelity after re-twirling is R(F). Fine measurement bits are uniform independently of the Bell labels of the retained pair; twirl keys and irrelevant fine records are discarded. For coarse pass/fail conditioning, each successful pair has the same sigma_(R(F)), independently across disjoint attempts. No arbitrary-input conditional channel is attributed to the recurrence itself: its input is the specified pair resource.

The derivative of R has positive numerator 6(-4F^2+14F-1) on[1/2,1]. Also, for t=F-1/2 in[0,1/4],

    R(F)-1/2=6t(1+t)/(5+4t+8t^2)>=(9/8)t.             (4)

Let K_1 be the least nonnegative integer satisfying (9/8)^(K_1)g>=1/4, and put K=K_1+9. Monotonicity, (4), and the exact rational check R^9(3/4)>39/40 imply

    R^K(1/2+g)>=39/40.                                (5)

Thus K=O(log(1/g)) is known before data. Exact iteration from the actual F is not required and F is not supplied. These bounds are deliberately conservative.

The recurrence is established prior art: Bennett, DiVincenzo, Smolin and Wootters, *Mixed State Entanglement and Quantum Error Correction*, Section3.2.1, equations42–43, https://arxiv.org/pdf/quant-ph/9604024 . The prior accepted source-specific note `../pure_success_reset_eb_and_assisted_entanglement_classification.md` also derives these conventions and insists on re-twirling each round; it supplies no finite raw cap or the learned generic factory below.

## 4. Deterministic reservoirs, not an expected stopping rule

First choose a concatenation level L and final number B of retained pairs as in Section5. Let

    t_cap=4 ceil(log_2(2(K+1)/beta_r)),
    N_K=B,
    m_j=4(N_j+t_cap), N_(j-1)=2m_j=8(N_j+t_cap)
        for j=K,K-1,...,1.                             (6)

Generate exactly N_0 raw pairs, or fewer on warm abort. At stage j there are N_(j-1) pairs. Partition them into m_j predetermined disjoint pairs of pairs, perform all recurrence attempts, and retain the FIRST N_j successful outputs after re-twirling. Discard every surplus. If there are fewer N_j successes, abort and later output replacements. There is no retry beyond the declared cap.

Inductively, conditional on the prior coarse pass history and successful previous stages, these inputs are iid sigma_(F_(j-1)). Each success flag is an independent Bernoulli with probability P(F_(j-1))>=1/2. Selecting the first fixed number of successes leaves iid sigma_(F_j), independently of the success pattern: this is the tensor instrument factorization for identical inputs, not an assumption that random selection generally preserves iid laws. This is also why the fine twirl keys are not conditioned on in the reference model.

Writing X_j for the success count, its mean is at least m_j/2 and N_j<=m_j/4. The elementary multiplicative Chernoff bound gives

    Pr(X_j<N_j | prior success,U,w)
      <=exp(-m_j/16)<=exp(-t_cap/4)<=beta_r/(K+1).

The union bound over K stages gives total shortage probability at most beta_r on each good warm history. The final B pairs, conditional on every retained coarse history, are iid sigma_(F_K) with 1-F_K<=1/40. Formula (6) gives the EXACT raw-pair cap

    N_0=8^K B+8 t_cap(8^K-1)/7.                        (7)

Both terms are real source costs; all discarded pairs and failed attempts count. On bad warm histories the same cap still applies. At fixed g the multiplier8^K is a constant, but can be enormous. More explicitly it is bounded by a constant times g^(-log(8)/log(9/8)), a large polynomial gap overhead, not a uniform useful throughput claim.

## 5. Actual code-teleportation circuit and complete reference error

A standard Bell measurement at the sender and the reported Pauli correction at the receiver, using one Bell-diagonal resource with label probabilities q_P, implements EXACTLY the Pauli channel sum_P q_P Ad_P. The four measurement outcomes are uniform and independent of the input and Bell label. This identity holds on every matrix unit, hence with arbitrary untouched references. Tensor-product resources give a tensor product of these channels, even when the transmitted carriers are entangled. This is ordinary teleportation with two paid classical bits per carrier, not a physical bypass furnished for free.

For each of the Q reference qubits, the sender applies the received level-L concatenated [[5,1,3]] encoder. Teleport each of its 5^L physical carriers using a distinct retained pair, send the two classical outcome bits, apply the Pauli correction, then apply the received deterministic concatenated syndrome recovery/decoder at the receiver. The original reference qubit is consumed in this encoding/teleportation process. No source query occurs during this teleportation phase: the source calls created the pair bank in Section4. Equivalently, applying this circuit to half of a fresh local Bell pair prepares one high-fidelity remote pair; this is an explicit LOCC realization, not an asserted bilateral stabilizer identity.

The already received five-qubit transfer proof exactly corrects every weight-zero or weight-one Pauli error and maps every other Pauli pattern to a logical Pauli. For independent carriers with nonidentity mass p_l,

    p_(l+1)<=10p_l^2,
    p_0<=1/40,
    p_L<=4^(-2^L)/10.                                 (8)

The local control faults are NOT inserted into p_l and squared; they are charged separately in nu. Choose the smallest integer L>=0 such that

    (Q/5) 4^(-2^L)<=delta_c,
    B=Q 5^L.                                          (9)

These are finite exact integer/rational tests. The complete error of all Q transferred references is at most 2Qp_L<=delta_c, including arbitrary correlations across references and with later/stored source data. Disjoint code blocks remain conditionally independent Pauli maps, but the hybrid bound would suffice. Shared warm history stays outside the product and is averaged only afterward.

For fixed g, B=O(Q[1+log(Q/delta_c)]^(log_2 5)). Known local coding/decoding circuits have polynomial cost in B. This uses the accepted exact five-qubit control/compiler and Pauli transfer receipts, not a presumed efficient arbitrary hashing decoder. The underlying code is standard: Laflamme et al., *Perfect Quantum Error Correction Code*, https://arxiv.org/abs/quant-ph/9602019 .

## 6. Full chronology, classical communication, and comparison

All warm acquisition and the whole reservoir factory occur BEFORE unknown references/payloads arrive. Initialize the common frame for the public worst-case horizon

    H=N_w+N_0+J_future,

where J_future counts every later source/data/payload slot in an application. The frame memory is retained through all recurrence, classical message delays, later teleportations, classical optimization and payload deployment. It is not reset after pair generation. Warm rejection or reservoir shortage causes a fixed replacement branch, with no conditional normalization or hidden retry.

Raw Bell-pair generation costs N_0 seed encodings, source calls, frame steps and learned decodings. Recurrence costs at most sum_j m_j bilateral CNOT/measurement attempts, two compared measurement bits per attempt, retention-index communication, bilateral-twirl keys, local gates and discarded systems. A conservative message/storage cap is polynomial in N_0,K,B and their bit lengths; all basis/key messages and both directions are included. Teleportation costs exactly2B sender-to-receiver outcome bits plus the explicitly known corrections. The ideal twirl may use a uniform24 Clifford label; a finite-bit modulo sampler within total variation O(nu/N_ops) suffices after the single complete-process error allocation, rather than an unbounded exact rejection loop.

Worst-case local quantum storage may hold O(N_0) sender/receiver qubits during factory preparation, plus the causal frame's polynomial-in-H memory and tomography workspace. It subsequently stores B retained pairs and the reference/data/code registers. These may wait through lengthy classical SDP calculations and communication latency. Trusted local storage time, not merely qubit count, is a paid assumption. No fault-tolerance threshold for arbitrary local noise is derived.

In the exact reference experiment, fix U and a good warm history. The reservoir failure costs at most2 beta_r at the COMPLETE channel level; on success, Section5 costs delta_c uniformly, including reference inputs chosen using the permitted coarse factory metadata. Warm bad mass costs at most2(beta_t+beta_v) ONCE for the entire future reference batch, not Q times. A globally CPTP ideal comparison can supply perfect references even on bad warm histories using dummy metadata; contractivity then gives (1).

Allocate a SINGLE worst-case unhalved interactive discrepancy nu to all actual finite controls: ordinary training, frame compilation, Bell preparation, seed controls, classical random sampling, bilateral gates/measurements, storage, teleportation, QEC, and any linked operations not otherwise paid. Use deterministic worst-case operation/horizon caps to distribute precision. Approximate physical hardware need not admit a literal U or conditional iid law; comparison to the exact reference is at the whole experiment level. Accepted statistical arithmetic tolerances are not charged twice.

For communication alone, directly code-teleporting the actual payload through this same factory is the stronger simple conventional baseline. Learning a near-optimal fixed one-use encoder/decoder is a different goal. No unassisted capacity, two-way optimal rate, general distillability detector, hardware execution or practical conservative-cap advantage is asserted.

## 7. Typed coherent-calibration substitution, not a new source-input oracle

The output of this factory is a PAID complete identity approximation on Q laboratory qubit wires. It can replace the reference-transport interface in an ALREADY RECEIVED typed coherent-calibration protocol. That protocol must separately supply its calibrated controlled-anchor/Gamma preparation, physical data-call cap, accepted rank bounds, frame typing, and finite controls. Real ordinary V_x access alone does NOT grant controlled selector access. A concatenation W=[V_i] is not presumed isometric; any admitted contraction/filter realization retains its own heralding/failure/preparation costs.

In the standard received controlled-anchor Gamma interface, Q=3n_Gamma references and n_Gamma data calls are explicitly paid. Use the factory before those data calls; then prepare each actual data sample by that interface and teleport its sender references using the reserved bank. The same frame persists. Perfect-reference replacement is solely a complete causal comparison, not physical deletion of the preceding factory/frame slots. The ideal bank then satisfies the received Gamma law; no iid or low-rank property is imposed on the actual contaminated bank.

For example, in the received finite-M relative wrapper, take e=epsilon/(8M), choose n_Gamma and optimizer/eigensolver precision from the accepted coherent theorem at this e, set beta_t=beta_v=beta_r=epsilon/64, delta_c=epsilon/4, and reserve total linked finite-process nu<=epsilon/4. Then the ideal learner costs at most epsilon/4 additive global error; warm/factory bad mass costs3epsilon/32; reference coding costs epsilon/4; finite implementation costs epsilon/4, leaving slack. With the ORIGINAL one-use, privately framed, predetermined encoder-list/full collective decoder comparator,

    ||Lambda_actual,M-id||_diamond
       <=min{2,(1+gamma)Delta_star_(family,frame,M)+epsilon}.

At fixed g, the total raw cap is

    N_w+N_0(3n_Gamma,epsilon/4,epsilon/64)+n_Gamma+M
       =O_tilde(k^2 M/(gamma epsilon))+M,              (10)

where the suppressed logarithms include the explicitly displayed code power and confidence logs; the large g-dependent factor8^K is NOT universal. If a different typed data preparation uses more source calls or references, substitute its ACTUAL ledger rather than (10). All typed-frame assumptions and any separate helper output type remain those of the received interface.

The source optimum in (P) has F>1/2, so it can include channels outside the previous one-use Pauli entropy seed promise H(q)<1. This does not supersede that older bootstrap where it applies: the old construction needs no two-way recurrence and can have a better reference source rate/control bill.

## 8. A nontrivial zero-unassisted-capacity fixture

Consider the qubit depolarizing source D(rho)=(1/2)rho+(1/2)I/2. Its identity encoder/decoder has Bell weights(5/8,1/8,1/8,1/8), so F=5/8>1/2 and H=3-(5/8)log_2 5>1. It meets (P), for instance with g=1/16, but its identity Pauli distribution does not meet the entropy-seed condition. In fact its unassisted quantum capacity is zero: Cubitt, Ruskai and Smith, *The structure of degradable quantum channels*, Appendix B.5, explicitly identifies depolarizing Bloch multipliers up to2/3 as antidegradable; https://arxiv.org/pdf/0802.1360 was directly inspected. Here the multiplier is1/2. This is an established assistance distinction, not a new capacity phenomenon.

For this qubit source the calibrated quaternion encoder can be any logical unitary family; decoding can undo it. A decoder cannot turn this antidegradable channel into a positive unassisted-capacity channel. In particular an H(q)<1 privately framed decoded seed would imply positive unassisted quantum communication by the already received entropy code, so no such seed exists. The two-way factory can still acquire reference entanglement. Direct two-way-assisted payload transfer is again a simpler competitor when learning is not the objective.

## Evidence and status

The companion exact/numerical checks must distinguish recurrence label algebra, finite caps and code/teleportation identities from actual acquisition or hardware execution. The inverse-square warm proof, finite Bures query, frame compiler and five-qubit transfer are accepted imports, not newly re-audited here. This candidate requires independent receiving of its new composition and all-history ledger before promotion.
