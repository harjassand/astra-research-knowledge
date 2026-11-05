# Independent audit of the P3 burst compiler

5 November 2026. Reviewer: the P1 comparator branch, after completing the actual-family Fano obstruction.

## Verdict

The two claimed semantic properties R (regular output from arbitrary input) and C (correct logical action from regular input) survive an independent adversarial review. They fix a real missing bridge between a globally nice-noise statement and an arbitrary raw fault field. The initial draft's three-round gadget was more redundant than necessary: one normalization round followed by the logical gate round already suffices. The revised `p3_construction.md` adopts that simplification.

The renormalization and finite-seed architecture are consistent with the declared immutable-schedule circuit model. The revised report now includes the explicit synchronization and footprint choices requested below, along with the stronger primary comparator. No counterexample was found. This is a mathematical circuit construction under a specified Poisson register-corruption contract; it is not a constructed physical device or a theorem for damaged processors or schedules.

A stronger primary comparator is required than the Gacs lecture alone. Published hardwired Tsirelson/exRec machinery already supplies arbitrary-input correction and localization of bad regions. The earned contribution should be the stated padded island implementation and its connection to the sharp strict-Pareto recoverability law, including finite-seed growth and physical readout. Generic fault-tolerant simulation and doubled correction should not be claimed as new principles.

## 1. Stronger existing method and its actual boundary

Primary source:

Shankar Balasubramanian, Margarita Davydova, Ethan Lake, *A local automaton for the 2D toric code*, Quantum 10, 2125 (2026), final arXiv:2412.19803v3.

Working final published PDF:

https://quantum-journal.org/papers/q-2026-06-02-2125/pdf/

Relevant anchors are §2, Theorem 2.2 / Corollary 2.1, and Appendix B. The source has immutable hardwiring, local binary gates, arbitrary bad-gadget outputs, and explicit extended-rectangle / star-decoder control of arbitrary incoming damage. Appendix C.1 also mentions doubled error correction as an alternative way to obtain the arbitrary-input correction property. Thus this is a closer comparator than full self-organizing cellular automata.

Its p-bounded probability theorem is not a direct theorem for the Pareto burst field. A macroscopic set of n adjacent physical cells can all fail from one burst with polynomially small probability, violating a bound p^n at every fixed p<1. The needed adaptation is geometric rather than merely replacing p by a one-point hit rate. The fixed Tsirelson substitution also has space factor 3 and time factor 6; approaching the causal boundary requires a padded family with time exponent tending to one, not simply citing that particular fixed substitution.

A readable extraction of the primary sections is saved in `sources/bdlake_2026_tsirelson_exrec.txt` (CC BY 4.0, attribution included). It is an extraction, not a substitute for the full paper.

## 2. One preceding normalization is sufficient

Let a clean three-pass round decode the five fixed Info copies of each input, apply a fixed-fanin Boolean function f, and write a perfect repetition of the result. This remains true for arbitrary initial Info words if the entire round is clean, because every pass sees the same word and all working storage is reset.

A two-round macrostep consists of a normalization round, a separating gap longer than the fault-island time width, and a logical-gate round.

- If the single island hits normalization, the subsequent gate round is clean. Whatever fixed Info words remain after normalization, all three passes of the gate round agree and produce perfect output.
- If it hits the gate round, normalization was clean and supplied perfect inputs. The existing regular-input proof gives regular correct output.
- If it hits the separating gap, it changes at most one Info position per macrocell; the subsequent clean gate round decodes correctly from the resulting regular inputs.

From regular initial inputs both rounds preserve the intended values except for the prescribed f. From arbitrary initial inputs the output is always regular. Faults at the final vote affect at most one output replica and preserve regularity.

An independent exact enumerator, `p3_two_round_check.py`, tests 491,520 adversarial identity-core cases. All passed. The generic fixed-fanin statement follows from the clean-round and regular-input arguments above, not from claiming that an identity test verifies every Boolean function.

The initial draft's two normalizations plus a gate remain a valid redundant variant; this simplification changes constants only. It shows that the number of pre-normalizations is not the foundational consequence.

## 3. Scheduling condition needed for the proof

The clean-pass argument assumes input Info is frozen while the logical layer is read. This must hold globally, not only per output macrocell.

A concrete valid schedule is:

1. Normalize all source macrocells, using a constant spatial coloring if needed.
2. For each temporal pass number, complete that pass for every color before beginning the next numbered pass.
3. Retain all computed outputs in Hold tracks. Do not commit new Info for any target until every pass of the logical layer has finished.
4. Perform the local three-Hold majority commits in a common final stage.

This is compatible with a fixed finite local gate basis and only changes the constant c_0 in U<=c_0 B before time padding. No mutable clock or protected data-dependent routing table is introduced. A constant-size flattening of tracks may move Info inside a bounded microcell; enlarge the island width by that fixed guard and choose replica separation larger again.

## 4. Arbitrary-E support projection

The draft's projection is sound at the semantic level. If I_t(i) marks an irregular incoming word and Bad(i,t) means that the fault support in the corresponding macrostep cannot fit inside one allowed island, then R gives

`I_(t+1)(i) <= Bad(i,t)`.

C gives the correct decoded logical action unless the current rectangle is bad or an input encoding was irregular. Thus all coarse errors lie in Bad together with its bounded next-step input-neighborhood expansion. This construction is monotone in the raw support and independent of adversarial error values.

That monotonicity is important: it permits comparison with the small-radius-thinned Poisson process without conditioning on successful data history. Correlations introduced by adversarial values do not invalidate independence of the support envelopes in disjoint marked-Poisson regions.

## 5. Explicit influence-box closure

A compact way to close the spatial and temporal support bookkeeping is the following. After accounting for the Bad-to-next-step expansion, let a,b be fixed constants such that one parent support test uses child grid points within spatial span aB and temporal span bU. For a level-k support event define a raw influence box with half-spans rho_k and eta_k. Up to a fixed base guard, the recursion can be bounded by

`rho_k <= a L_k + rho_(k-1)`,

`eta_k <= b tau_k + eta_(k-1)`,

where L_k=B^k and tau_k=U^k. Therefore

`rho_k/L_k <= a/(1-1/B)+O(B^-k)`,

`eta_k/tau_k <= b/(1-1/U)+O(U^-k)`.

Choose B,U>=2, bound these uniformly by constants C_x,C_t, and choose the allowed island width w larger than the resulting doubled support constants plus the small-radius cutoff guard. Then a non-nice parent window has two child support points separated enough in space or time that:

- temporal separation makes their raw Poisson time intervals disjoint;
- spatial separation makes their raw small-radius Poisson influence regions disjoint after removing bursts of radius >=cL_k.

There is no k-dependent footprint factor. Constants a,b include the initial/final macroperiod guard at conversions. This is the exact place where mere marginal probabilities would be insufficient; the draft uses disjoint support regions instead.

The local gate schedule and B can be chosen after fixing these constant guards. The relation U=ceil(B^z), z>1, eventually exceeds the O(B) implementation depth, so the choices are compatible.

## 6. Probability and execution costs checked

For cube bursts in R^d, restricting centers to those that hit a line multiplies the intensity by (2R)^(d-1). The draft includes this tilt, avoiding an incorrect one-dimensional tail exponent. The large-burst rate in a parent box is consequently O(lambda tau_(k+1) L_(k+1)^(d-alpha)), with constants depending on B and the cutoff.

With separated small-radius supports, the claimed recurrence

`p_(k+1) <= C p_k^2 + D lambda theta^(k+1)`

is consistent, where theta=U B^(d-alpha). The induction p_k<=A lambda theta^k is valid for A>=max(C_0,2D) and lambda<=theta/(2CA). Strict alpha>d+1 permits 1<z<alpha-d and hence theta<1 after choosing B sufficiently large.

Finite upward and downward conversions can be ordinary local circuits over the child bit lattice. On the event of no induced coarse fault in those circuits, their projected bit output is the exact encoded/decoded word. Resetting working registers and preserving waiting values must remain among those counted gates. Including the preceding-period support guard prevents conversion boundaries from silently discarding residual damage.

The sum over scale conversions is finite because M(B) is a family constant and sum p_k converges. A fixed commissioning circuit and fixed terminal detector have nonzero failure floors; choosing the low-intensity range small enough can budget them below the target. The output remains within the fault model until delivery. The O(T) delivery delay is material and is correctly charged.

## 7. Recommended statement after the above clarifications

At sufficiently small positive intensity, a uniform family of finite locally operated binary circuits with a horizon-independent finite input-dependent seed can return that bit with error at most 1/4 after every finite requested storage horizon under the strict Pareto law alpha>d+1. For alpha<=d+1, the accepted complete-cone erasure theorem prevents that operation. The positive hardware/time exponents may depend badly on the tail margin and the fixed gate/correction constants.

This is a sharp strict-Pareto classification under intact immutable gate laws and schedules, instantaneous Poisson bursts, and arbitrary register corruption. It is not the finite-(d+1)-moment endpoint for all tail laws, an autonomous self-repairing controller theorem, a passive quantum-memory theorem, or an experimentally delivered apparatus. These are scope limits, not additional requirements imposed on the approved target.
