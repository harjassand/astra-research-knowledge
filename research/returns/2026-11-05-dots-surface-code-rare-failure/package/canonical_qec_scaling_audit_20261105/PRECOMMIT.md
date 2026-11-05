# Independent scaling audit, fixed diagnostic grid

2026-11-05, before executing this grid.

Use the unchanged canonical_qec_witness_20261105/sampler.py Model and Proposal. Test distances13,25,41,61 and p=1/10000,1/1000,1/200, 2000 trials per cell; length cap=max(55,3d), seed2026110500+100j+i (j enumerates p, i distance). Report all rejection categories, normalizer/tail, setup and sampling time. These are exploratory acceptance diagnostics, not rare-failure confidence claims or a proof of square-code asymptotics. No adaptation to observed acceptance.

Separately prove and exhaustively check the serial-diamond IID counterexample. Its Z-error distance is2m; a CSS realization has dual X-distance2, so it is not a balanced distance2m surface-code family.
