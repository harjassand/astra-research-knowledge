# Actual bounded-controller three-role diagnostic

## Executed scope
The frozen bounded SOS/congruence-repair controller was run for 120 actual simulated source calls, not merely on old queries. A retained two-dimensional bath, four-spin carrier and adaptive predeclared source policy were propagated by finite matrices. The source choice is fixed before fresh private perturbation, role and probe choices, and ignores CPU time by construction. Roles have probabilities learn 1/3, matching validation 4/9, averaged service 2/9. Seeded random generators provide reproducibility, not a physical private randomness implementation.

There is NO outer error-correcting code, unknown payload transmission, acceptance instrument, verified physical clock, or claimed readiness/yield guarantee. Services propagate the averaged orbit interface. Validation failures do not stop this diagnostic. Candidate clock privacy is a mathematical simulation assumption, not a hardware conclusion.

## Results
120 calls: 38 learning, 59 validation, 23 service; 25 matching failures. Mean selected sum of three star losses is 0.5783052346218412; mean service bad weight is 0.33621227800062525. The early protection is poor and essentially unchanged from the preceding certified-oracle diagnostic. The new fixed-work solver gives tiny certified objective gaps, not a physical protection breakthrough. Solver time was 212.51 seconds; total 214.56 seconds, slower than the earlier approximately 73-second run. Timings are descriptive, not worst-case hardware bounds.

Each of 360 online classical queries and three final retrospective queries returns a rational feasible quaternion and independently checkable lower certificate. No target-gap failure abort is allowed. The legacy `requested_gap` field is a comparison target only. Final retrospective queries use no additional source calls.

## Machine-readable interface
`bounded_live_three_role_result.json` is the unchanged actual-run record.
- `feedback_exponents`: ordered 35 degree-four exponents in four quaternion coordinates.
- `final_feedback`: three arrays of 35 exact rational strings G_i,T.
- `observed_squared_feedback_per_edge`: exact sums of squared coefficient l1 norms, respectively 136057644, 140315004, 143064792.
- `shared_probe_count`: 38.
- `reported_gap_counters`: three upward dyadic counter reports, denominator 2^39 and PUBLIC cap 340050. Concentration must use this cap, not the smaller unrounded analytical bound 337890.
- `retrospective_candidates`: three sound solver outputs for the polynomial G_i,T/2. Their quaternions are hindsight candidates, not future guarantees.
- `retrospective_empirical_score`: exact value 3*m*Nprobe/(4p) + sum_i (G_i,T/2).phi(q_i), m=3.
- `T=120`, `p=1/3`, `perturbation_radius=2310`, midpoint count M=2^(perturbation_bits_per_coordinate); d=35.
- `oracle_calls`: current query coefficients and certificates, grouped by call then edge.
- `calls`: actual role, source index and diagnostic physical losses/outcomes.
- `verified_outer_code_deployed=false`, `unknown_payload_transmitted=false` are substantive scope boundaries.

The exact dyadic sums are 14311680399/549755813888, 7038314449/274877906944 and 14118609337/549755813888. Small observed sums do not themselves bound conditional expected solver gaps; use the separately reviewed concentration theorem, with its full penalties.

## Probe replay
`replay_bounded_live_probes.py` reuses all stored candidates/certificates (no optimizer work), repeats seeded source/role/probe propagation and adds raw probe axes/signs/outcome and three exact current-candidate delta estimators. Its output `bounded_live_probe_replay.json` retains `calls[].probe_raw` and `calls[].selected_probe_estimates` on learning rounds. It asserts exact equality of original final feedback, squared-feedback counters, role counts, failure counts, dyadic counters and numerical physical summaries. These are the actual prequential probes, not retrospectively selected test measurements.

Dependencies are the frozen bounded kernel and dyadic addendum, plus `quaternion_oracle_controller_20261029/quartic_sos_oracle.py` (polynomial convention) and the initialization prefix of `capture_one_axis.py` before `T=60000;` (physical source construction). The full latter file is hash-bound conservatively although its long original experiment is not executed here.

## Comparison and interpretation
Ordinary numerical optimization produces the same retained candidates. Exponential Hedge can store the same 35 cumulative counters and stream a finite net. The contribution assessed here is bounded-work proposal plus exact always-valid objective gap reporting, not exclusive storage, optimization quality or speed. Formal observable-loss bounds remain extremely conservative at this horizon; a numerical record must not be reclassified as a successful acquisition-only or two-role protocol.
