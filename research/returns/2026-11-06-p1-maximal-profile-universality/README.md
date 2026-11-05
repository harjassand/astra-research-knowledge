# P1 maximal-profile universality: a universal extension with paid recovery

P1 reports an **unreviewed mathematical construction** for the following question: what operational content follows when a channel preserves the input's entire maximal-information profile, across every finite reference system and tensor power, and what does exact recovery cost? The claimed result combines a universal extension, finite structural criterion, optimal recovery program and sharp dimension/probability bounds. The visible return contains the argument and reports a completed compiler and checks; the named manuscript, code, certificates and source manifest have not been delivered here.

For every finite channel `N: M_a → M_b` and `0<ε<1`, the response constructs one extension `Lε: M_a → M_b⊗M_F` and fixed auxiliary state `σ_F` satisfying all of the following with the same parameters:

| Property | Claimed contract |
|---|---|
| Exact original marginal | `Tr_F Lε = N`, including reference-entangled inputs |
| Uniform operational approximation | `½‖Lε − (N⊗σ_F)‖diamond ≤ ε`, including observers who inspect the auxiliary output |
| Perfect complete maximal profile | Every maximal quantum f-divergence for an operator-convex generator is preserved, for every finite reference, tensor power and state pair, under the stated support/extended-value conventions; RLD Fisher information is also preserved |
| Heralded exact recovery | A completely positive trace-nonincreasing success operation obeys `Rsucc∘Lε = p_succ id`, with input-independent `p_succ ≥ ε/(2−ε) ≥ ε/2` |

These maximal divergences are a particular family of quantum information measures. Preservation does not identify them with Umegaki relative entropy, SLD information, trace distance or every operational measure, and does not imply deterministic reversibility.

With at most `Q` adaptive calls, the half-diamond approximation changes an event probability or bounded loss by at most `Qε` under the response's convention. Taking `ε=η/Q` gives a recovery guarantee at least `η/(2Q)`. Independent repeat preparations then cost at most `2Q/η` specimens on average per successful sample. **An unknown single quantum input cannot be replayed after a failed recovery.** New specimens and preparation costs remain charged.

| Read | Contents |
|---|---|
| [Complete visible response, actual prompt and available explanation excerpts](P1_MAXIMAL_PROFILE_UNIVERSALITY_20261106_RETURN.txt) | Byte-exact native prefix plus labeled rendered ending, including source formatting artifacts and overlap |
| [Structure and optimal recovery](structure-and-recovery.md) | Rank criterion, Kraus-Gram SDP, exact reversal price and sharp erasure/dimension deductions |
| [Construction, costs, comparators and retained failure](construction-costs-and-prior-art.md) | Environment synthesis, rational compiler interface, reported checks and false uniform-SLD route |
| [Publication receipt](SOURCES.json) | Capture provenance, unreviewed status and held attachment boundaries |
| [Preserved joint rounding result](../2026-11-06-p1-hard-discrepancy-covariance/README.md) | Earlier common-law guarantee, paid oracle and large rational extraction costs |

The claimed broad consequence is that one perfect maximal-profile class contains a continuous embedded copy of the entire finite-channel space at each fixed original input/output dimension, while exact recovery probabilities can approach zero. This does not establish a general computational speedup, an ordinary-capacity evaluator, a practical quantum technology or the P=NP-scale endpoint. World priority is unestablished.

The ZIP `maximal_profile_universality_bundle.zip` was selected once; the browser download timed out and no exact local file was available. The original remains on transfer hold, with no alternate export, PDF acquisition or retry. The visible manuscript link is preserved as source data, without claiming that manuscript was downloaded. Capital publishes the available response and guides without a new scientific review, code execution, producer contact or full corpus build. Generated retrieval remains unchanged.
