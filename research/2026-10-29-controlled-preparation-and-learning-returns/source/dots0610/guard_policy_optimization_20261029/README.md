# Tolerant guard policies with actual retained-memory instruments
2026-10-29. Author: review_actual_logical_comparator. New finite computational construction pending independent review. This is a source-known benchmark of declared policies, not an acquired optimal controller or a physical performance claim.

## Question and outcome
The previous illustrative controller aborted on its first failed test. This construction permits b failed tests and prices the larger outer error-correction radius required by the same accepted-operation soundness target1/128. Actual CP instruments are retained, including their different quantum-memory backaction. The objective is expected accepted payload divided by expected source calls for ONE conditional operation. It is not automatically a long-run no-reset renewal throughput.

A716-policy expanded grid includes service-heavy policies through R=64, failure budgets b in{0,1,2,4,8}, and outer lengths B in{31,63,127,255,511,1023,2047}. All admissible candidates are reported. The original smaller grid is preserved as v1. Expansion was motivated by the structural fact that fixing R=1 is not an optimal or asymptotic restriction; it was not advertised as predeclared before seeing any earlier research. The expanded grid was fixed before its own run.

All four best policies occur at the largest tested B=2047. Therefore they are finite-grid optima, not global optima. Same source, same one-million-call acquired frame, same final retained bath, same fixed post-training sourceU0:

- Full six-state test: R8,b4,t99;18,161 payload qubits; acceptance0.9881280;26,676.60 expected native calls; score0.672702 logical qubits per call.
- Two complementary logical bases X/Z: R8,b4,t99;18,161 payload; acceptance0.9804750;28,035.81 calls; score0.635131.
- Weighted test with exact C3: R16,b2,t142;16,269 payload; acceptance0.8897474;25,862.26 calls; score0.559708.
- Matching test C2: R8,b8,t147;16,049 payload; acceptance0.9545582;27,951.17 calls; score0.548088.

Finite caps are explicitly specified below and their analytic corrections are negligible at the displayed precision, not zero. A native call uses the four-qubit source array, so these figures must be divided by4 for logical qubits per source-input physical qubit. Full conventional logical testing remains strongest in this metric. More tolerant policies can improve availability relative to the small b0 example, but their payload size, redundancy, latency and control costs differ.

## Exact soundness parameter choice
Write R=C s/(1-s). The accepted reviewed guard proof bounds accepting more than t service faults by the negative-binomial tail for failures before b+1 test failures. With R=r/q, the tail is exactly
sum_{j=0}^b binom(t+b+1,j) q^j r^(t+b+1-j)/(q+r)^(t+b+1).
The program evaluates this as an exact rational number and picks the smallest t for which it is at most1/128. No floating comparison sets the correction radius. For each retained candidate, B>=4t+1 and B=2^h-1. The inherited constructive CSS/GRS code is [[B,B-4t,2t+1]] over GF(2^h), with J=hB inner qubit services and h(B-4t) payload qubits. At most t inner faults affect at most t outer symbols. The reviewed total decoder and arbitrary-noise accepted-operation theorem are dependencies; no new fault-tolerance or calibration theorem is asserted.

The actual role controller needs only s, counters and test outcomes. It does not need the source generator or bath state. Source matrices are used to evaluate and select benchmark policies here, so optimal policy acquisition remains unclaimed.

## Efficient exact-memory policy evaluation
Let Tpass and Tfail be actual bath CP maps for test outcomes, and Svc the total bath map of the private-pad service. All are4x4 superoperators for a two-dimensional retained memory; these are evaluator objects. At a state with j completed services and f failed tests, arbitrary strings of passed tests can be summed with
G=[I-(1-s)Tpass]^-1, S=s Svc G, F=(1-s)Tfail G.
The inverse exists because Tpass is trace nonincreasing and1-s<1. G is the convergent CP series. The expected number of native calls before the next service or failed test is the positive functional trace G applied to the current unnormalized memory state.

The direct recursion preserves j,f and the entire bath matrix. A faster service-epoch transfer has blocks A[fout,fin]=S F^(fout-fin) for fout>=fin. This accounts for every allowed number of failed tests before the next service, with all CP maps in physical order. Paths crossing b failures lose trace and abort. The cost row for entering failure count f is trace G times sum_{r=0}^{b-f}F^r. Augment A with this cost row and a scalar accumulator, then raise the augmented matrix to J. The final bath trace is acceptance; the scalar is expected native calls. Runtime is logarithmic in J at fixed b, using matrices of dimension4(b+1)+1. No hidden reset, independent-event approximation or scalar failure rescaling is used.

Direct and fast recursions were compared on the four original-grid winning policies; discrepancies are below4e-11 expected calls and2e-14 acceptance. These are floating numerical results, not interval-certified probability bounds. The all-input soundness guarantee is supplied by the exact theorem and exact rational parameter selection, not numerical tiny-tail estimates.

## Finite cap and no-result accounting
Choose N=ceil((2J+256)/s). Every actual operation stops no later than obtaining J service roles, or earlier on b+1 test failures. Extending the private Bernoulli role coins beyond an abort for analysis only, the probability of remaining active at time r is at most P[Bin(r,s)<J]. For rs>=2J, Chernoff gives exp(-rs/8). Hence cap loss is at most exp(-Ns/8), and the difference between uncapped and capped expected calls is at most exp(-Ns/8)/(1-exp(-s/8)).

The program reports intervals obtained by subtracting these quantities from acceptance and expected calls as appropriate. For extremely small exponents it reports a conservative positive floating floor exp(-700), never claims exact zero failure, and retains the actual log bound. Test-failure abort probability is also reported. The cap changes no soundness proof: additional aborts cannot increase accepted bad mass. This cap argument is analytic; it does not rely on stationarity of source noise. Stationarity is needed only for the compact CP-matrix benchmark evaluation.

## New two-MUB conventional comparator
Prepare uniformly one of the four eigenstates of logical X or Z, execute the actual same E→N→D operation and measure survival. All decoder Kraus operators, including leakage resets, are included. After logical Pauli twirling, if pX,pY,pZ denote nonidentity weights, q=(pX+pZ)/2+pY while e=pX+pY+pZ, so e<=2q. Averaging opposite eigenstates removes affine/nonunital terms. The same relation lifts to bath effects because it holds for every bath state; 2F-W is the positive Y-branch effect. The actual effect and CP-map checks are in the programs/data. This conventional route uses only two mutually unbiased bases but still executes the full inner encoder/decoder on test calls. No claim that the identity is new.

## Calibration-prefix consequence
The two best large-block policies for six-state and matching were frozen using the1m fixture, then applied unchanged to earlier nested learning prefixes from the separate acquisition-prefix construction. No per-prefix policy optimization was performed. At100k calls, the frozen large six-state operation accepts only2.1346e-6; at1m it accepts0.988128. Matching at100k accepts6.10e-17, versus0.954558 at1m. Very early-prefix zeros can be numerical underflow, not a proof of zero probability.

Thus an earlier candidate can be useful for a small35-qubit operation yet fail almost every attempt on this much larger operation. Learning duration and guarded workload must be chosen together. The prefix source rule deliberately switches to U0 carrying its actual prefix bath; it is not a prediction of unchanged acquisition dynamics. These results are conditional on one sampled training history, not training-average performance.

## Physical and computational costs limit the interpretation
The largest code requires22,517 trusted buffer qubits at each relevant endpoint, with source latency up to the stated cap. The source-call score omits calibration time beyond the separately shown single-training metric, native gate duration, routing, outer circuits, temporary keys and storage noise. It is not a hardware utility or net communication-capacity score.

field_and_control_bounds.py supplies exact binary-polynomial irreducibility certificates for h5 through11. It also prices one sufficient dense inherited field-linear circuit: at most B(B-1) field additions, B field scales and B register swaps. Charging h² CNOTs per field addition,3h² per scale and3h per register swap gives h²B(B-1)+3h²B+3hB CNOTs per transform. At B2047,h11 this is507,578,214 CNOTs, before other outer operations. This is a sufficient upper bound, not a lower bound or executed large compilation; faster structured encoders could be better. The large optimum's dense encoder/decoder has NOT been compiled or run here. Existing exact construction and parameter guarantees are reused at their scope; this benchmark exposes the practical control obligation rather than silently resolving it.

Even an optimistic inner-control-only calculation is demanding: ignoring source duration, outer circuits and storage, and treating the six-state test's cost as one full inner E/D operation, the best matching policy beats its score only if a matching test costs below7.38% of that full operation. This is a simplified break-even, not a measured advantage. Service-heavy policies reduce the room for cheap tests to help; fixed-R comparisons cannot establish asymptotic test-overhead impossibility.

## Files and dependencies
- policy_grid_v1.json and policy_grid_v2.json: every valid policy and exact tail, plus finite-cap bounds; all_policies_v2.csv is a convenience copy.
- optimize_policies_grid_v1.py and optimize_policies_grid_v2.py; embedded_chain.py supplies reusable evaluation.
- fast_vs_direct_check.json; field_and_control_bounds.py/.json; control_break_even.json.
- frozen_policy_prefixes.py/.json depends on the separately hash-pinned acquisition prefix_maps.npz.
- reviewed_fixture_arrays.npz and matching_memory_maps.npz come from the reviewed previous comparison; their provenance remains the exact million-call source-generator replay, not new measurement data.

The source and proof dependencies remain intact. No publication, historical novelty, Capital integration or hardware performance is asserted.
