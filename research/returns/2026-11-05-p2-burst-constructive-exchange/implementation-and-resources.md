# Encoding, physical readout, implementation and resources

The [main statement](README.md) and [gadget/noise proof](forced-output-and-noise.md) give a scheduled classical circuit under arbitrary unflagged burst corruption. This page retains the complete endpoint and cost claims from the [original return](P2_CONSTRUCTIVE_EXCHANGE_20261105_RETURN.txt).

## One physical seed through noisy encoding and decoding

Only cell 0 initially knows the bit. A finite lifting circuit resets unused child cells and uses protected COPY, SWAP and included idles to populate the next level's designated children. If every child operation is good, validity lifts one level. The lift does not claim `D`-fault tolerance: its failure is bounded by `M p_(k-1)` for a fixed bound `M` on child calls, including idles. Summing over ascent levels costs at most `M C_p lambda_1/(1-theta)`.

At level `m`, repeat protected identity for `ceil(T/A^m)` cycles. Its failure is at most `(T/A^m+1)p_m`. Descent copies a valid parent's designated children into protected workspace, computes their monotone majority and transfers the forced result into child 0, recursively down to physical cell 0. Its union bound is the same as ascent's; it does not independently correct `D` bad child calls. Include a final physical clock interval for terminal reading.

Choose `m` minimally so `B^m >= T^(1/(a-1))`. Then

\[
\begin{aligned}
P_{\rm error}
&\le\frac{2M C_p\lambda_1}{1-\theta}
 +(T/A^m+1)C_p\lambda_1\theta^m+c\lambda_1\\
&\le\lambda_1\left[\frac{2M C_p}{1-\theta}+2C_p+c\right].
\end{aligned}
\]

Sufficiently small fixed positive intensity makes this at most `1/4`, uniformly over requested horizons. Encoding expansion and final local decoding are actual operations under noise. Neither is hidden in an initial horizon-growing input-dependent seed or an error-free terminal oracle.

## Paid resources

For explicit Pareto parameters and a fixed `1 < kappa < alpha-d`, the supplied bounds are:

| Resource | Bound |
|---|---|
| Initial input-dependent state | One physical bit |
| Mutable data and work cells along the wire | `O(T^(1/(alpha-d)))` |
| Noisy encoding and local decoding duration | `O(T^(kappa/(alpha-d)))` |
| Time from seed arrival to delivered output | `T + O(T^(kappa/(alpha-d)))` |
| Local physical operations, including idles across installed hardware | `O(T^(1+1/(alpha-d)))` |
| Explicit schedule generation/materialization | `O(G polylog T)` work/description bound, with `G` the physical operation count |

Pre-input hardware, adjacent connections and schedule manufacture are charged. The displayed delivery time starts at seed arrival; it does not erase pre-input preparation time. All installed hardware's idles count during encoding and decoding too. Architectural constants can be extremely large. A certified smaller Pareto exponent can replace the supplied one conservatively; a finite unrestricted empirical sample alone does not certify the tail assumption.

The source example `d=2, alpha=3.5, kappa=1.25` gives cells `T^(2/3)`, encoding/readout overhead `T^(5/6)` and physical operations `T^(5/3)`.

For any device contained in a cube of half-side `L`, the complete-device reset rate is

\[
q_L=\lambda 2^d\frac{\Gamma(d+1)\Gamma(\alpha-d)}{\Gamma(\alpha)}L^{d-\alpha}.
\]

Its worst-input bit error obeys `(1-exp(-q_L t))/2` as a lower bound. Fixed nontrivial accuracy therefore requires `L=Omega((lambda t)^(1/(alpha-d)))`. At fixed intensity the construction attains this radius exponent. This is not a universal hardware-volume lower bound or a practical hardware demonstration.

For a quantum register, complete replacement of all accessible input-bearing state has Bell overlap at most `1/4`, giving

\[
\tfrac12\|\mathcal N_t-\mathrm{id}\|_\diamond
\ge\tfrac34(1-e^{-q_Lt}).
\]

This negative comparison prevents transferring an exponential Davies-memory lifetime into the burst class without an earned bridge. The positive construction here stores a classical bit.

## Original code and source-reported checks

[burst_gadget.py](original/burst_gadget.py) is the original 19,071-byte loose attachment downloaded from the producer chat. Its bytes and hash are recorded in [SOURCES.json](SOURCES.json). It includes adjacent routing, partial-input three-valued semantics, fresh-output gadgets, recursive expansion of protected idles, ascent/descent and operation counters. Capital did not run or modify it.

The producer reports a smaller finite test instance `D=1, n=9, t=2, B=52`: 396 ordered routing cases, clean truth-table and partial-input checks, 194 injected-fault traces, two full seed-to-output runs with only cell 0 initially known, and descent from malformed children. The theorem's fault-separation argument instead uses `D=11`. The reported one-level example has 52 physical cells, 53,881 clock ticks and 2,798,049 local operations including encoding, rounded holding, descent and terminal window.

These are source-reported execution results and an original implementation artifact. No separate machine-readable test log, external formal certificate or new Capital execution is supplied here. Finite cases do not establish the asymptotic probability theorem by experiment. The full argument is preserved in the return, with in-session semantic checks/activity at their actual scope.

## Strong existing comparisons and remaining scope

The return credits [Gács's finite-space computation theorem](https://arxiv.org/abs/math/0003117): finite input independent of computation size and local output are established endpoint capabilities. The close [rigorous reconstruction of Tsirelson's hierarchy](https://quantum-journal.org/papers/q-2026-06-02-2125/pdf/) permits an immune schedule and credits local output reliability. Its ordinary local-stochastic condition bounds each specified set of `N` faults by `p^N`. In the burst law, one large mark reaches `N` consecutive wire locations during a unit interval with probability at least `c lambda N^(d-alpha)`, which exceeds `p^N` at large `N`. Small intensity alone does not supply that existing noise hypothesis.

[Poisson-hail stability](https://arxiv.org/abs/2102.07406) supplies related workload and moment machinery. Workload tightness does not itself specify how arbitrary corrupted data and decoder records preserve the unknown bit. The supplied contribution is the forced-output semantic gadget and its transfer to separated truncated Poisson sources, followed by charged encoding/readout. Hierarchical redundancy and local readout themselves are not claimed new; exhaustive priority remains unestablished.

P1's complete source-conditional loader remains credited, including the bath, commuting-coupling, cooling and control premises. Applicability of Code Swendsen-Wang or regular-matroid sampling to the full BDL family remains unresolved. P2's thermal replacement bound remains an actual thermal operation at its own scope, rather than an implemented burst-memory decoder. The general non-Pareto finite-moment sufficiency endpoint, laboratory realization, autonomous construction and practical advantage remain separate from the proved strict-Pareto circuit result.
