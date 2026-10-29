# Nonunital and retained-memory physical encoder acquisition
2026-10-29. Independently accepted at the explicit conditional scope in `independent_acquisition_review/RECEIPT.json`.

The previous random-unitary pair-fixed-vector method is extended to a16×9 pair-adjoint defect. It learns unknown local conjugations of a common collective-noise algebra using ordinary independently randomized product-Pauli preparation and local readout. Nonunital collective damping is permitted. Training need not reset the bath or be stationary: one common randomized bank estimates the actual predictable occupation-average operator, with a martingale confidence bound and an observed singular-gap/abstention rule.

The structural common-algebra/excitation promise is a COMPLETENESS/YIELD assumption, not an experimentally certified noise model. A bad candidate can be guarded by the separate sequential model-free finite-operation construction. The occupation average is not a predicted future channel.

Files:
* `GOVERNING_v1.md`: full proof/interface/costs and retained conditions.
* `check_exact_nonunital_v1.py/.json/.npz`: exact collective-lowering Lindblad example, unknown local frames, nonunitality and full16×9 gap. The NPZ is a reproducible mathematical source model, not an acquired environment.
* `check_physical_probe_bank_v2.py/.json`:1m actual product-input/full-output sampled trials through that global nonunital channel.
* `check_retained_memory_bank_v3.py/.json`:200k no-reset probe trials with actual conditional bath updates and past-output-dependent source choices.
* `check_retained_memory_bank_v4.py/.json`: extends the same sequence to1m calls; v3 is a checked prefix, not additional physical sample cost.

Independent replay matched original JSON exactly and independently checked all1296 product input expectations. Observed1m frame errors are diagnostic: the conservative declared operator confidence radius at delta=.05 is about.556, exceeding the actual gap≈.354, so these simulations DO NOT claim that the formal stopping condition has fired. The sequential soundness guard does not require correct candidate identification; obtaining high yield is separate.

Ordinary noiseless-subsystem algebra, randomized tomography and martingale concentration are established methods. No historical novelty, laboratory demonstration, generic efficient learner for all unknown noise, or total-resource superiority is asserted. Preparation/readout calibration and current-setting privacy are actual costs.
