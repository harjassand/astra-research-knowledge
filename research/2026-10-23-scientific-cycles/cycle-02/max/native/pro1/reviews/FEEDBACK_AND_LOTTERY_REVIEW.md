# Focused incorporation and lottery review

Reviewer: `/root/feedback_incorporation`  
Date: 21 October 2026  
Scope: the new classical-transcript lemma, its measurable-instrument repair, and the proposed variable-cost achievability. This is not a repeat of the original recurrence or tree-capacity audit. Original owner and frozen trial files were not modified.

## Verdict

The fixed-horizon transcript argument is valid under the stated causal resource model, with the two incorporation corrections already identified by the supplied review. I find no surviving steering or normalization gap. The invariant is the Schmidt number of the **whole block channel's Choi operator**, equivalently the minimum possible maximal individual Kraus-operator rank. It is not the number of Kraus operators.

The variable-cost lottery is also valid. Two small qualifications should appear in its statement: the receiver uses a **Bernoulli(p)** coin, which is not generally fair; and the exact displayed probability formula requires `K >= 2` and `f >= K^(-2)`. For any fixed target `f > 0`, this holds for all sufficiently large K. If the requirement is fidelity at least f and `f <= K^(-2)`, the zero-use replacer already suffices.

These are internal mathematical assessments, not external certification or a historical-priority conclusion. The transcript lemma is the supplied trial's contribution. The tree walk-rank certificate and Dyck code belong to the unchanged owner source.

## 1. Correct fixed-horizon statement

Let a fixed causal n-slot device have finite-dimensional input ports `X_i` and output ports `Y_i`, initialized independently of the logical input, its reference, and the local laboratories. Let `N_n: X_1...X_n -> Y_1...Y_n` denote the ordinary block channel obtained by providing all inputs independently of its outputs, while keeping the device interactions in their original time order. Suppose `N_n` has a Kraus decomposition `{C_z}` with every `rank(C_z) <= M`.

Consider a physical n-slot protocol with independent initial laboratory states, arbitrary local ancillas and normal local operations, and only classical communication from the receiver Bob to the sender Alice. Controls are measurable functions of the previously received transcript; normal instruments may have standard Borel outcomes. No backward quantum wire or prior shared entanglement is supplied. Every outcome branch participates in the final deterministic logical channel `Lambda: L -> Lhat`, where both logical dimensions equal K.

Then the normalized logical Choi state has Schmidt number at most M, and

`F_e(Lambda) <= min{1, M/K}`.

Taking M to be the block Choi Schmidt number gives the representation-independent form. The causal-device premise is needed for the rearrangement. A bare noncausal input-output map would not supply a legal chronological protocol to which this argument applies.

## 2. Why fixing a transcript is legitimate

First use discrete outcomes. Fix a complete receiver transcript t and never divide its branch by its probability. Every Alice control is now a fixed label. Her later map acts on her retained local memory and its future emitted input; an earlier device interaction acts on the earlier emitted input and the device memory. These supports are disjoint. Bob's operations act on his own memory and completed output ports, also disjoint from Alice's retained systems.

Consequently one can commute Alice's maps to the beginning, preserving their internal order, and commute Bob's fixed branch maps to the end, preserving their internal order. The device interactions retain their original order. Tracing Alice's final private systems produces a transcript-specific CPTP map `E_t`, while Bob's selected branch and final decoder produce a CP trace-nonincreasing map `D_t`. The identity is

`Lambda_t = D_t o N_n o E_t`.

It holds as an unnormalized CP-map identity, including after tensoring with an arbitrary reference. `E_t` genuinely depends on the whole t. It is a mathematical encoder with frozen parameters, not a claim that Alice knew future outcomes in the original experiment, nor that the normalized physically conditioned Alice state equals `E_t` by itself.

Remote steering does not invalidate the identity: two fixed linear operators on disjoint tensor factors commute on entangled as well as product states. The argument would fail if one normalized intermediate branches, coherently combined alternative transcripts, or forced every branch to use the same E. None of those moves is used here.

Private Alice measurements do not introduce a missing branch dependence: they can be retained inside Alice's memory and then summed within her CPTP `E_t`. Entanglement created through earlier device slots is also already included in the circuit; no intermediate separability assumption is needed.

## 3. Why the branch sum has no alphabet penalty

For Kraus operators of the three factors, each logical branch operator is

`F_(t,b,z,a) = D_(t,b) C_z E_(t,a)`.

It has rank at most M. The physical protocol is deterministic, so summing all classical branches and all Kraus indices gives `sum F*F = I_K`. This equality comes from the completeness of the original chronological instruments; it does not require `sum_t E_t` to be trace preserving.

With a normalized maximally entangled logical input,

`F_e = K^(-2) sum |Tr F|^2 <= M K^(-2) sum Tr(F*F) = M/K`.

The inequality is the singular-value Cauchy-Schwarz bound `|Tr F|^2 <= rank(F) Tr(F*F)`. Input-dependent outcome probabilities are already present in these unnormalized operators. Retaining the transcript for decoding is allowed; unused records may be traced only after their permitted use. No success-only weighting is introduced.

## 4. Continuous outcomes and normality

Bob's full receiver strategy, viewed as acting on all finite-dimensional Y ports at once, defines a CP instrument with final quantum output Lhat and classical transcript t. Its finite-dimensional Choi-valued measure has a CP Radon-Nikodym density `D_t` relative to a finite positive scalar dominating measure `mu`. Standard Borel outcome spaces and measurable controls ensure that the frozen `E_t` and the composed integrand are measurable. The rearrangement gives

`Lambda = integral D_t o N_n o E_t dmu(t)`.

The density `D_t` need not be trace-nonincreasing for an arbitrary choice of dominating measure. For example, the density `D_t = 2t id` on `[0,1]` with Lebesgue measure integrates to the identity channel but increases trace when `t > 1/2`. Only the integrated physical normalization is required.

Each integrand's positive Choi operator lies in the cone of Schmidt number at most M. On a finite-dimensional trace-one slice that set is the convex hull of a compact set of pure states, hence compact and closed. Positive integrals remain in the same cone. Therefore the fidelity inequality survives without a cardinality factor or a pointwise trace-nonincreasing premise. Well-defined operational limits also inherit the bound by continuity of the final finite-dimensional logical channel. Nonmeasurable controls or infinite local procedures without a defined normal instrument are not included.

## 5. Coherent reservoir correction

For an arbitrary fixed normal initializer tau, the permitted cutoff is explicitly

`P_F = sum_(v in F) |v><v|`, `r = |F|`, `q = Tr(P_F tau) > 0`,

where F is a **finite set of vertex coordinates**. Put `tau_F = P_F tau P_F/q`. Every vector in its support contains at most r vertex-basis components. Its device Kraus matrices are therefore sums of at most r vertex-conditioned matrices, giving individual ranks at most `r M_n`.

Projecting a purification and normalizing gives `D(tau,tau_F) <= sqrt(1-q)`, where D is half trace norm. For the same fixed protocol, the final decoded state is a CPTP function of the initial reservoir, so

`F_e(tau) <= min{1, r M_n/K + sqrt(1-q)}`.

An arbitrary rank-r projection does not provide finite vertex support and cannot justify that finite-sum rank argument. Fix F before the horizon limit; enlarge it afterward. This establishes no common exponential rate for arbitrary coherent tails.

## 6. Exact lottery achievability under expected forward cost

Let `K >= 2` and let m be the smallest integer with

`D_m = Catalan_m * 2^m >= K`.

The owner source proves on the full reservoir Hilbert space that the `2m`-slot device restricted to the colored-Dyck code equals `V_m tensor I_E`. Restrict to any K-dimensional subspace, encode isometrically, and invert its output isometry. This is an exact identity logical channel, preserving arbitrary external entanglement and returning the bath together with any inert purifier at the block boundary.

Bob first samples a local Bernoulli(p) variable, retains it, and sends its one-bit value to Alice on the permitted backward classical channel. Conditional on success they run this exact `2m`-slot code. Conditional on failure they make zero forward calls; Bob outputs a fixed state sigma of dimension K and Alice retains or discards the unused logical input locally. The unconditional decoded channel is

`Lambda_p(rho) = p rho + (1-p) Tr(rho) sigma`.

It is CPTP, includes both branches, and has entanglement fidelity

`F_e(Lambda_p) = p + (1-p)/K^2`.

The abort term is exactly `1/K^2`, because the reference-output state on that branch is `I_R/K tensor sigma`. Thus for `f in [K^(-2),1]`, choose

`p = (f-K^(-2))/(1-K^(-2))`.

Then `F_e = f` exactly. The random call count is N=2m with probability p and N=0 otherwise. Its law is independent of the logical input, so both the maximally mixed mean and the supremum over all logical inputs equal `2mp`. There is no success-only credit: the abort contribution and its error are retained in the channel and its fidelity. No initially shared entanglement, bath access, bath replacement or backward quantum communication appears. The one classical coin message is an explicit resource, available under the unlimited backward-classical contract.

On each branch the bath operation is exactly the identity at the terminal boundary. This assertion is stronger than mere bath marginal return and follows from the inherited code identity, not from a new recurrence argument. The bath may move during the successful code block; all-use return is not claimed.

## 7. Code length and significance of the lottery

The Catalan estimate gives `D_m = 8^m / (sqrt(pi) m^(3/2)) (1+O(1/m))`. For the minimal m above,

`2m = (2/3) log2 K + O(log log K)`.

For fixed f>0, `p -> f`, hence the worst-input expected forward cost obeys

`E N / log2 K -> (2/3) f`.

Thus the construction proves the proposed upper bound on minimum expected cost. It also supplies the standard rare-long-block mechanism for failure of a fixed-horizon-style strong converse when rate is divided only by mean call count. That failure already occurs for a two-point stopping distribution; actual unbounded support is not necessary. This is a change of operational cost contract, not a contradiction of the fixed-n theorem.

I did not assess the converse for general stopping protocols; that is assigned to the distinct stopping-converse reviewer and remains a separate obligation. I do not claim exact optimal finite-K cost or a novelty result for the lottery mechanism.

## Sources and work record

Read completely:

- `experiments/feedback/stage1_frozen/RESULT.txt`.
- `experiments/feedback/ACCEPTED_SCOPE.txt`.
- `evidence/FEEDBACK_TRIAL_SCIENTIFIC_REVIEW.txt`.

Read the owner's exact tree/Dyck definitions and proof in `deliverables/Astra_Restore_PRO1_20261021/RECURRENT_RESERVOIRS.tex`, lines 233-302, plus targeted statement locations. No full recurrence audit was repeated. No frozen diagnostic or old replay was rerun: the question here is the operator identity and exact coding calculation, not another finite sample.

No external search, paid computation, hardware, outreach, sharing change or subdelegation was used. The write is a scratch review for inclusion in the owner's private packet. Model time and energy were not metered; no inferred resource total is claimed.
