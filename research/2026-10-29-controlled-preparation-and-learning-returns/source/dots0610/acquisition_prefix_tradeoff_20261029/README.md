# Acquisition-prefix versus guarded-operation cost
2026-10-29. New executed source-model comparison; independent receiving review pending.

## What changed
The same original one-million-call no-reset training trajectory was replayed once, saving only copy snapshots of the actual classical counters and actual conditional bath at the predeclared prefixes100,1000,10000,100000,1000000. Each candidate uses only its own prefix counters. No true rotation, bath state or future channel enters the learner. Bath state and source generator enter only the mathematical evaluator.

After each prefix, deployment switches to fixed source unitaryU0, as in the reviewed v8/v9 fixture, retaining the actual bath. The preceding training source rule had depended on the latest output parity; this is an explicit stage-rule change, not a claim that future noise was inferred from past records. No bath reset occurs.

Each policy is fixed at155 service calls,35 output logical qubits, t=6, zero permitted test failures, and R=1. Six-state tests use C=1.5, service probability.4; matching survival uses C=2, service probability1/3. Both have the existing accepted-subnormalized error bound1/128 at ideal trusted control boundaries. This guarantee is distinct from a conditional-on-accept fidelity statement. Primitive gates/storage and calibration error budgets are not included in source-call throughput.

## Results including calibration
For one guarded attempt, the100000-call prefix gives six-state acceptance0.28982 and221.17 expected guard calls, compared with0.92902 and373.49 after one million. Including training, accepted output qubits per full-array source call are approximately0.0001012 versus0.0000325: a factor3.1 in this finite comparison despite lower acceptance. Divide by4 for physical-qubit exposures.

The100/1000 prefixes effectively always abort. The10000 prefix has onlyabout0.001 six-state acceptance. More training is helpful, but highest per-attempt acceptance is not automatically best end-to-end cost.

Amortization is evaluated by propagating the ACTUAL terminal bath channel between repeated guarded attempts, not resetting it or reusing the original pure bath. At1000 attempts the100k prefix yields0.0316309 accepted logical qubits per total full-array call versus0.0236755 for1m. The1m prefix overtakes100k at2032 attempts under these exact fixed policies and fixed futureU0. At10000 attempts their rates are0.0686759 versus0.0439256. These are conditional-on-one-training-history model results, not a guaranteed future-noise lifetime or an oracle-free rule selecting the best training budget.

The conventional six-state test outperforms matching here at every relevant prefix. No total hardware advantage is inferred for either.

## Exact memory computation and finite caps
For test mapsTpass,Tfail and total service mapTs, write G=(I-(1-s)Tpass)^-1, S=s Ts G, F=(1-s)Tfail G. For b=0 and J required services, accepted memory map is A=S^J, terminal memory map is End=S^J+F sum_(j=0)^(J-1) S^j, and expected-call row is Tr G sum S^j. This sums all repeated passed-test strings before the next service or failure. The inversion is valid since (1-s)Tpass has trace-norm spectral radius at most1-s. End is CPTP and preserves retained bath chronology.

The calculation uses floating4x4 bath maps from a declared known source generator; it is not a dense simulation of35 logical qubits or a hardware measurement. All maps pass Choi positivity/trace checks, one-million counters/bath reproduce the earlier bank exactly, and one-million deployment maps reproduce the reviewed comparator.

Displayed rates use the uncapped model as a convenient exact resolvent calculation. A finite capN=ceil((2J+256)/s) per attempt has abort-before-completion coupling probability at most exp(-Ns/8), by private service-coin Chernoff domination. Across A attempts the entire finite/uncapped path coupling error is at most A exp(-Ns/8); total accepted-count expectation differs by at most A² exp(-Ns/8). Thus finite caps approximate the displayed accepted counts to negligible explicit error here. The uncapped expected-call rates are not silently relabelled exact finite-cap rates; their source-call denominator requires its own truncation/coupling accounting if used for a formal finite-rate bound.

## Reproduction
Run replay_prefixes.py with the original check_retained_memory_bank_v4.py path as its optional first argument. That source needs its original check_exact_nonunital_v1.npz sibling; these are unchanged dependencies in the02:09 source package. The wrapper makes one copy-only snapshot insertion and records the source SHA. Run build_prefix_maps.py, then evaluate_prefix_tradeoff.py. Supplied prefix_bank.npz and prefix_maps.npz permit quick replay of the latter two stages without the training rerun. check_prefix_outputs.py performs retained-path consistency and the exact2032-attempt crossover calculation; its additional comparisons reference the earlier confidence and comparator fixtures in the shared research tree.

No source originals were overwritten. No historical novelty or unrestricted unknown-noise acquisition claim. Independent review remains pending.

## Workload-dependence cross-check
The separate policy worker evaluated its already-frozen large-block policies on these same prefix maps without reoptimization (governing data: guard_policy_optimization_20261029/frozen_policy_prefixes.json). At22517 services, the100k six-state candidate accepts onlyabout2.13e-6 versus0.988128 for1m. Thus the early-stopping benefit for the35-qubit workload does NOT transfer to that larger workload. Long protected operations can justify considerably more calibration. This is a required qualification, not a contradictory result; the controller, code size and permitted failure budget differ.
