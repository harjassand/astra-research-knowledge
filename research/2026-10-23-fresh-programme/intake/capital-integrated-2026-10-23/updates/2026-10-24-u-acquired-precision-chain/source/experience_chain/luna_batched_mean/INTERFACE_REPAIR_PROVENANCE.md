# Interface repair provenance

Before the interface audit, the generator wrote latent/noise RNG seeds to `seed_manifest.json`, and the result JSON repeated the seed values in a top-level field. Those learner-facing names were superseded. The original manifest bytes were moved intact to `private_evaluator_seed_manifest_DO_NOT_PASS_TO_LEARNER.json`; the pre-repair result JSON was copied intact to `private_evaluator_results_pre_interface_repair_DO_NOT_PASS_TO_LEARNER.json`. Neither private file is a learner/control input. The regenerated public result omits seeds, and `public_manifest.json` contains only public model constants, paid observations, exposures, and acquisition order.

Original seed-manifest SHA-256 after move: `78319c44888ddbab1271c5d1149d5b924bc41d8c26daa6f7431f271ec77f9d73`.

Pre-repair result-copy SHA-256: `ae3f0e808e0bab91d421ea7a1723698135aa8dfbbfd5fead5cf1bf30c0010101`.

The pre-audit report also labeled the realized four-checkpoint source sum plus target sum `0.0373011224` as the union-bound budget. Because the stopping policy could inspect any of 12 scheduled source checkpoints, that realized-only sum is not a valid stopping-bound. It is retained in the regenerated report as a diagnostic; the valid scheduled union-bound sum is `0.0390199211` (at most `0.04`). The old report JSON is retained under the private pre-repair filename above.
