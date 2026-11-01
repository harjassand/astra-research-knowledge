# Independent skeptical receipt: decoder-trace polymer lemma

1 November2026. **PASS-CONDITIONAL for the abstract explicit-circuit theorem and ideal sampler.** The actual RX/RZ circuit binding is NOT supplied by this receipt. No physical or noncommuting thermal loader is established.

Frozen audited root `ROOT_DECODER_TRACE_POLYMER_LEMMA.md`: SHA256 `3a724349a408548f8d86b012c05638109c27a5613a16674648e8b775fc4cf81c`.

## 1. Splitting is valid under literal full-input marking

Use a wire as its unique circuit wire identifier, not just its value. An input object is the nonzero external input wire. A marked gate includes EVERY incident input/output wire, including wires carrying zero. The circuit description and gate rules are fixed and deterministic, with a distinguished zero value at every alphabet.

For any accepting execution, take one stencil-connected component. Replay exactly its nonzero external input bits and zero all others. Induct in topological order. At any gate originally active in the selected component, a nonzero incoming wire's driver/input object must belong to that component because the wire lies in both stencils. Every originally zero input remains zero: its driver is either reproduced with the same output, or becomes inactive on all-zero input. A different originally active gate cannot receive a retained nonzero input, since its full input stencil would connect it to the selected component. An originally inactive gate receives only zeros. Thus the selected component is reproduced exactly and all other objects vanish. Rejecting outputs remain zero.

This proof includes gates with nonzero inputs and zero outputs. Omitting them invalidates it: an XOR rejection gate accepts11 but each isolated nonzero input10/01 rejects. Keeping cancellation gates but omitting their input wires from the stencil has the same failure. These are necessary negative controls, not counterexamples to the root as written.

## 2. Recombination and uniqueness

For individually accepting connected traces with disjoint COMPLETE stencils, nonzero external inputs are disjoint. Topological replay of their union reproduces each trace. If a gate could receive nonzero input from either trace, that trace's isolated execution already marks the gate and contains all its incident input wires. If a second trace contributed another nonzero input, its producing object would overlap that marked stencil. Hence no newly active or differently evaluated merging gate can arise in a compatible union.

The resulting trace is exactly the union, with no overlap edges between its components, and remains accepting. Conversely every accepting input has a unique deterministic execution and unique connected-component partition. A connected trace is not an arbitrary certificate or witness; it must be the exact complete execution of its own input restriction. This yields the bijection, including the empty valid input/empty polymer collection. Nonzero connected components necessarily contain at least one nonzero external input, because the circuit is finite acyclic and zero-preserving.

The root therefore does not suffer from a many-to-one witness cover. But a later implementation must deduplicate canonical traces and validate them by replay; counting arbitrary consistent-looking local witness fragments would not inherit this result.

## 3. Counting and truncation

Let N=O(n) be the actual supplied object universe. Fixed gate fan-in/output/stencil sizes, wire fanout and alphabets give a bounded-degree stencil-overlap graph and a fixed bound on local value labels. Object identifiers are counted in the connected-animal enumeration; they are not extra unconstrained labels from an n-sized alphabet.

The isolated component is accepting, so the assumed valid-execution bound applies to it: m<=A|x_gamma|. Thus w_gamma<=exp(-beta J_min m/A). With rooted count at most K^m, write q=K exp(-beta J_min/A)<1. The total omitted activity above L is bounded by N q^(L+1)/(1-q), up to the fixed counting convention. The positive gas has inclusion probability <=w_gamma because its excluded partition is a sub-sum of the full positive partition. The truncated gas is exactly the full gas conditioned to contain no omitted polymer. Its total-variation difference is therefore at most this tail. No assumption of independent polymer occupations is used.

Enumerating all connected labeled candidates of size<=L and replaying each on the full explicit circuit is sufficient. O(N) replay per candidate remains polynomial when L=O(log(N/epsilon)) and the local constants are fixed. This does not require an unproved local recognition shortcut. Supplied additive energies/weights must have polynomial-time precision access, with input encoding costs charged.

## 4. Birth–death coupling and finite implementation

For neighboring legal configurations differing by gamma, use common birth clocks of rates w_eta and death clocks of rate1. Gamma's death removes distance |gamma| at rate1. A birth allowed only in the configuration without gamma must be incompatible with gamma; its increase is at most|eta|. Birth of gamma can instead coalesce and can safely be ignored in an upper bound. All other common events do not increase distance. The assumed rooted weighted activity bound gives drift <=-(1-theta)|gamma|.

Weighted symmetric difference is exactly the legal single-polymer-update path metric: remove the differing polymers first, then add the target's differing polymers. Both intermediate phases remain compatible. Every nonzero distance is at least1. Compatible traces use at most N marked objects per configuration, so diameter<=2N. Finite-state path coupling therefore yields the stated Wasserstein and total-variation mixing estimates. The low-temperature rooted sum can make theta<1 uniformly in n; no Peierls-to-mixing leap is being made.

The displayed uniformization gives the right rates and R<=2K_dictionary. Without an event cap it has expected-polynomial, not deterministic worst-case, event count. The parent's subsequent proposed cap is valid: for N_Pois~Poisson(Rt), Markov's inequality applied to2^N gives

 P(N_Pois>M)<=exp(Rt-M log2).

M=ceil[2Rt+2log(1/epsilon_cap)] makes this <=epsilon_cap. Return a default output on that event and add its TV budget. Approximate event probabilities to total error <=epsilon_prob/M per step; also charge numerical Poisson sampling/mean error and weight preparation. A fixed-rate2K_dictionary implementation is an equivalent way to avoid an uncertain normalization rate. With polynomial-time computable weight precision, these costs remain polynomial. This cap is a verified implementation clarification communicated after the frozen root, not a preexisting statement silently attributed to it.

## 5. What actual RX/RZ binding must prove

The abstract theorem does not follow merely from the published decoder's polynomial runtime or Peierls witnesses. Required actual evidence:

1. A fully specified deterministic finite DAG on ALL input syndrome strings, with zero-preserving gates and exact acceptance iff the syndrome is allowed. Promise-only correctness on already valid inputs is insufficient. All local solve/tie rules and terminal-seed validity checks must be specified.
2. Bounded-size local gadget implementations at fixed microscopic parameters, bounded fanout/stencil degree, and total gate/input universe O(n). Finite gadget sizes may be enormous constants; they must not grow with hierarchy depth.
3. For EVERY valid input, a bound on ALL marked gates including cancellation gates, nonzero reconstruction witnesses, tests and branch logic: total<=A|x| with fixed A. A contraction bound on syndrome counts alone does not price a circuit that globally expands correction histories. A validator using local per-level reconstruction identities may avoid that expansion, but this must be shown.
4. The actual final validity relation, including redundant check constraints and both CSS sectors, must match constant-degeneracy commuting Gibbs sectors. Any auxiliary choices must be deterministic or summed with a separately proved unique representation; unpriced existential witnesses are not covered.
5. A gate-level trace replay and canonical extraction algorithm with polynomial encoded arithmetic cost. The abstract graph need not be a geometrically local physical device, so this sampler does not by itself provide low-noise hardware loading.

Once these hold, enumeration and the explicit sampler are earned ideal classical algorithms for the known COMMUTING syndrome Gibbs distribution. They do not prepare generic noncommuting interacting equilibrium, provide raw logical encoding, apply physical corrections fault-tolerantly, or implement noisy routing.

## 6. Independent exact diagnostics

Saved `test_abstract_trace_bijection.py` beside this receipt. It generated200 deterministic zero-preserving binary DAGs with5 inputs and7 two-input gates, checking all32 inputs each. Across3049 accepting executions it verified isolated-component validity, exact compatible-family recombination, uniqueness, equality of the full input set and polymer-family set, and exact rational partition equality at fugacity1/7. All pass. This is an abstract stress test, not an actual RX/RZ binding or a proof replacing the induction.

No counterexample to the frozen abstract lemma was found under its stated literal circuit hypotheses. The principal remaining gate is actual construction-level binding, not a missing abstract split/recombination principle.
