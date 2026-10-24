# Scientific checkpoint: an acquired local preparation island

24 October 2026. The literal assignment/principal brief are preserved once in `FIRST_CONSTRUCTION.md`; the root's retained-trajectory refinement is preserved in `RETAINED_CONTEXT_ACQUISITION.md`. Prior rank-two, permutation and predictive files are unchanged.

The consequential obstruction chosen was the supplied global rank/completeness promise. The new operation admits arbitrary hidden exterior memory rather than trying to rule it out from a finite minor. It learns a contracting local guard from paid noisy observations, then makes a finite-horizon local experiment reproducible while the exterior remains uncontrolled. A second substantive change is that **even acquisition uses one retained trajectory and no full initializer**. The supplied replacement structure is a finite local causal/clock/sensor interface; finite data do not certify that structure against omitted local influences.

## The acquired operation and proof

`ISLAND_THEOREM.md` proves the complete statement. The physical contract supplies clocked native bits, known bounded parent sets, stationary conditional local response, synchronous site-selective updates with fresh conditional noise, and QND readouts with a full-history conditional error ceiling. Bits are held during paid repeated reads. No true context, transition table, contracting mode, context sampler, global dimension or reset is supplied.

The learner explores a finite collar using a fixed public alternating-mode schedule. It reconstructs each local context/response from repeated noisy reads, retains the first m visits at every context/mode/site row, and returns UNKNOWN at a finite cap if any row remains incomplete. Predictable selection before update noise makes the first-m table confidence valid without stationarity or a context-visitation floor. All-correct-sensing probability is separately paid. The guarantee is a bound on **return AND an invalid assertion**, not conditional-on-return confidence or a promise of fast successful coverage.

Simultaneous table intervals yield full local parent-influence bounds Cbar. The chosen per-site modes are deterministic and public. With A=Cbar_BB and b=Cbar_B,Bc*1, the sharper executed certificate is

    v_0=1; v_(t+1)=min(1,A*v_t+b),
    future-TV diameter <=sum_(i in backward future cone) v_k(i).

Every boundary-parent weight is included. The scalar theorem bounds v_k(i) by q^k+q^distance; its no-1/(1-q) spatial factor follows from disjoint first-boundary-hit probabilities of a substochastic dependency walk. The theorem requires only local sufficiency at the guard/future cone; an exterior of arbitrary hidden dimension/history can feed arbitrary predictable boundary trajectories. It is a finite-H local statement, not an unbounded-horizon global reset.

The control word and preparation completion time are visible. There is no sampled-controller-word key, selection entropy or key-erasure claim. The legal preparation emits no state/bath readout. Its microscopic stochastic noise remains unmonitored as an explicit physical channel contract. Acquisition's observations/completion time are public calibration information; they are not themselves called a reset. Continuation policies read only the declared support and frozen calibration information. A private PRNG fixture does not validate physical bath independence, QND sensing, clock gating or absence of hidden local inputs.

`GLOBAL_RANK_AND_REFERENCE_SCOPE.md` gives an exponential global-Hankel-rank witness for the native-bit family and fixes target semantics. This is operational reproducibility with a small local diameter, not a learner-known exact target law. The actual initial field is a private scorer anchor, never an initial-state sampler given to the learner.

## Actual observation and later acquisition

Prospective settings were guard B=[-7,7] (15 sites), exploration collar [-8,8] (17 sites), three parents per site, two candidate preparation modes, 2^3 contexts, m=2,500 first responses/row, w=0.05, 81 noisy QND reads per bit with conditional error ceiling 0.1, and a 100,000-round exploration cap. Preparation depth was fixed at 12; future visible support is the center, with one future update round. Geometry is a one-dimensional nearest-neighbor array; bounded degree alone would not imply this polynomial guard volume.

The source is a designer-selected 1,001-cell clocked stochastic fixture, with site-dependent unknown modes. The learner receives no response-rule formula, source seed, native bit, exact context or probability. `island_learner.py` uses only actual noisy read-count and legal update capabilities during exploration. A separate process produces the certificate from `learner_input.json`. The future mode c was not among the response-table controls; its new local effect and a feedback protocol were measured only after the guard was acquired.

Acquisition completed at **64,903 parallel rounds**, with all **240 context/mode/site rows** filled. It retained 600,000 response majorities out of 973,545 observed local response opportunities. Individual row exposure ranged from 2,500 to 6,537. Every surplus visit, collar pulse, raw read and hold tick was charged:

| Cost | Acquisition | Later 10,000 trials | Total |
| --- | ---: | ---: | ---: |
| Full initializer calls | 0 | 0 | 0 |
| Native site-update pulses | 1,103,351 | 1,810,000 | 2,913,351 |
| Synchronous update rounds | 64,903 | 130,000 | 194,903 |
| Raw sensor reads / hold-read ticks | 168,228,576 | 15,000 | 168,243,576 |
| Controller word-selection bits | 0 | 0 | 0 |

The device begins in an existing zero field in this replay fixture; this fact is not disclosed to the learner and is not a repeatedly supplied preparation. No initializer method is exposed to the acquisition controller. The proof handles any permissible incoming field. Sensor counts are simulated with the exact binomial count distribution of the stated read-noise model, charging all represented raw reads; the learner never receives its native true bit. Python runtime is about 3 seconds for acquisition and 1 second for later execution, and is not a physical latency/resource measurement.

The acquired maximum influence row sum is **q=0.5248**. The scalar future bound is 0.03420039695. The sharper finite-matrix certificate is **epsilon=0.000294420934**. Post-execution private evaluation confirms the selected modes' true row sum is 0.12; that source fact was not used in the learner's decision.

Two later event programs each ran 5,000 trials, with the full field retained between trials and 12 public guard rounds before each:

| Previously unmeasured program | Observed ones | Private anchor-reference probability | Absolute error |
| --- | ---: | ---: | ---: |
| Apply c at center, read its noisy output | 2,486 | 0.4994002724 | 0.0022002724 |
| Read center; choose c/a from that bit; read again | 1,657 | 0.3350086334 | 0.0036086334 |

The observed event is a raw noisy sensor output; its noise is part of the target law. A bounded-bias martingale proof gives an error allowance epsilon+0.04=**0.040294420934**. The unconditional probability of returning an invalid certificate or violating either later bound is at most

    480 exp(-12.5) + 3,200,000 exp(-25.92) + 4 exp(-16)
      < 0.001806954416.

The saved rational upper bound uses a finite positive 96-term Taylor sum for exp, not an exact-real exponential oracle. The earlier valid but looser 0.00325109 arithmetic bound is preserved in the summary. There were no extra observations in tightening the arithmetic. No iid future-trial or independent joint-law assertion is made.

## Strong comparisons and limits

The same-data ordinary local-table/controller implementation selects **identical public modes and certificate**. This remains the strongest fixed-target comparison and is an exact tie. `PRIMARY_COMPARISON.md` identifies the established Dobrushin/PCA coupling and factored-MDP/UCRL confidence machinery, including the explicit no-reset extension of UCRL-Factored. The construction is a paid interface composition, not a new generic mixing or local system-ID algorithm.

Root's stronger public schedule check is preserved in `operation_checks.json`: uniform all-a/all-b have certificate 1, but simple deterministic alternation already yields diameter **0.02608289** (a,b) or **0.02947888** (b,a) after 12 rounds. Both pass the requested 0.05 preparation tolerance. Thus selecting each site's preferred mode is not necessary for every successful preparation on these data. It tightens the bound by about 89 times relative to a,b, not the measured physical error by that factor.

At the same numerical error/confidence allowance, the 12-round alternation bounds need 39,611/68,391 sufficient trials versus 5,000 for selected modes. A search over depths 1..100 improves those arithmetic pulse budgets: a,b at depth 18 needs 5,574 trials and 1,510,554 pulses per program; selected modes at depth 9 need 5,712 trials and 776,832 pulses. The executed depth-12 selected schedule is not cost-optimal even under that pulse-only objective. These alternatives were **not executed**. Their own reference laws can differ, so these numbers are reproducibility/certified-cost calculations and not a fixed-target advantage. The same-data conventional learner may adopt the selected schedule and tie it. Read latency, sensor cost and control parallelism are additional physical resource coefficients.

A separately supplied exact initializer followed by the identical selected guard has the same fixed target. It needs only **4,928** trials per program for the reported error/confidence allowance, compared with 5,000 under the acquired guard bias. Without measured initializer/update/readout costs, the experiment establishes neither end-to-end savings nor superiority to stateful prediction. The new concrete capability is that no initializer is needed to acquire or use this preparation within the local physical contract.

Exact checks pass all 240 source-table intervals, 180 matrix/first-exit inequalities, missing-context and boundary-copy countermodels (UNKNOWN), byte-identical offline certificate replay, equal-mode conventional comparison, exact eight-context scoring independent of the event-polynomial evaluator, and all cost identities. These checks make no new observation calls. Source moment closure is used only by the private post-execution scorer; neither it nor a latent model is supplied to learning.

The remaining substantive gaps are physical justification/acquisition of the local causal/sensor/hold interface, high sensing cost, rare-context noncompletion, finite spatial/horizon coverage and reference-law matching for a prescribed task. Hardware validation, historical novelty, general learning advantage and civilisation-level consequence remain unestablished.

## Replay

From the workspace root, a new run is:

```sh
python3 work/portfolio_20261024/deep_continuation/learning/run_island.py --out-dir work/portfolio_20261024/deep_continuation/learning/replay_retained --seed 202610241
```

The output directory must not already exist. The supplied observed run is `run_retained_202610241/`. Recheck its certificate and exact arithmetic without new source observations:

```sh
python3 work/portfolio_20261024/deep_continuation/learning/check_island.py
python3 work/portfolio_20261024/deep_continuation/learning/island_learner.py work/portfolio_20261024/deep_continuation/learning/run_retained_202610241/learner_input.json --out work/portfolio_20261024/deep_continuation/learning/replayed_certificate.json
```

Replay seeds/source parameters remain outside learner input. The replay is a statistical model experiment; the physical assumptions still require their own implementation evidence.
