# Frozen sampler implementation and fixed-run results

The independently reviewed sampler is `exact_sampler.py`, SHA-256
`229c5f08443090fb68e8525a1ec31ac7cc4fd16cd740671e34cfb410483074d1`.
`SAMPLER.md` states its exact integer law, floating-prefix enclosure proof,
resource accounting, and scope. No pre-existing frozen files were changed.

## Correctness checks before production

- 14,190 adversarial endpoint bucket checks and 3,949 exact prefix-enclosure
  checks passed; 10,970 deliberately ambiguous cases exercised exact fallback.
- Structural tests accept shared endpoints, reject a reversed repeat of the
  same underlying edge, and recover the ordered oriented faults from the fixed
  CircuitModel path while omitting clean edges.
- On each actual dataset, 256 deterministic same-seed trials gave identical
  outcomes and requested-bit counts with certified floating prefixes and with
  arbitrary-precision integer prefixes. These are correctness checks, not
  statistical or performance pilots.
- Independent review additionally checked 286,300 prefix enclosures and 1,573
  thresholds, including length 65,536 and zero vectors. The parent received
  independent arithmetic/certificate and sampler signoff before either run.

Local test artifacts: `test_sampler.py`, `sampler_unit_results.json`.

## Fixed d13 run

20,000 trials, seed 202611051913, exactly as precommitted.

- Accepted 1,578; repeated-edge rejection 4,089; fold rejection 878;
  non-failure 9,293; other canonical tuple 4,162. Null and negative-score counts 0.
- Rounded-model point estimate: 2.775464563103335e-8.
- Individual 99.9% interval, including conversion TV:
  [2.5595549148433986e-8, 3.002621635589656e-8].
- Decoder calls 15,033. All 163,264 endpoint draws were float-certified;
  no exact fallback was needed in this fixed run.
- Requested fair-bit count 5,928,265,458, including 5,854,451,520 noise bits
  and 56,192 thinning bits; 165,222 uniform-range rejection attempts.
- Setup 0.190 s, sampling 23.462 s, confidence 1.472 s;
  sampler total 25.124 s, full child-process wall time 27.656 s.
- Full-process peak RSS 138,940 KiB; listed static arrays 3,949,864 bytes.

The frozen earlier d13 path sampler used 100,000 trials and 48.688 s sampling
for 1,249 acceptances. This run's interval is about 10% narrower. That is a
specific observed comparison, not a claim of faster individual trials or an
end-to-end comparison that omits producer and independent verification costs.

Artifacts: `production_d13_20000.json`, `.log`,
`production_d13_20000_process_resources.json`, and launch hash-check log.

## Fixed d21 run

10,000 trials, seed 202611052921, exactly as precommitted.

- Accepted 55; repeated-edge rejection 4,987; fold rejection 2,808;
  non-failure 1,563; other canonical tuple 587. Null and negative-score counts 0.
- Rounded-model point estimate: 2.742784171599928e-12.
- Individual 99.9% interval, including conversion TV:
  [1.6876511444865811e-12, 4.18024741599281e-12].
- The lower endpoint exceeds the unchanged target 1e-12 per 21-round block.
  This is evidence against that target for the fixed modeled decoder, under
  the stated ideal-bit and model assumptions. The target was not changed.
- Decoder calls 2,205. All 149,272 endpoint draws were float-certified;
  no exact fallback was needed in this fixed run.
- Requested fair-bit count 3,795,606,393, including 3,734,176,320 noise bits
  and 179,712 thinning bits; 147,956 uniform-range rejection attempts.
- Setup 0.364 s, sampling 28.053 s, confidence 0.023 s;
  sampler total 28.440 s, full child-process wall time 30.156 s.
- Full-process peak RSS 226,492 KiB; listed static arrays 33,836,136 bytes.

Artifacts: `production_d21_10000.json`, `.log`,
`production_d21_10000_process_resources.json`, and launch hash-check log.

## Limits and accounting

The runs were sequential, in separate processes, and stayed within their
20-minute and 2-GiB resident-memory budgets. `run_capped.py` checks resident
memory every 25 ms and wall time, and obtains whole-child CPU and peak RSS from
Linux wait4. The RSS monitor is sampled, not a kernel hard memory cgroup.
`postrun_hashcheck.log` confirms the precommitted files remained unchanged.
`postrun_record_checks.json` checks count, bit, endpoint and resource consistency.

Each interval is individually 99.9%, not a simultaneous 99.9% claim for both.
The executable uses deterministic Python random.Random; mathematical IID and
coverage guarantees assume ideal independent fair bits. Requested bits are not
measured physical entropy. Both graphs, independent-edge model, costs and
CircuitModel are fixed; no hardware, arbitrary decoder or correlated-noise
reliability conclusion follows. Saved-table load time is not the whole
construction cost: floating table production, exact repair/certification and
independent verification must be charged separately by the overall report.
