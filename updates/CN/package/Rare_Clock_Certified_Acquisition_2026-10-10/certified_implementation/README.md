# Certified rare-clock implementation gate

Completed bounded n=4 acquisition, with compression genuinely active.

- Exact integer/rational implementation and proof: CERTIFICATE.md, certified_clock.py
- ε=1/4, requested δ=1/20; proved conservative failure bound 59429/5242880 <0.011336
- Same-tape continuous-H enclosure proves the recorded moderate-instance relative error <0.001653
- q=2^-200 scale check: all four strata compressed, 29,401 exponential cells, about 0.9 seconds
- Seventeen regression tests and separate code/mathematics audit pass

One fresh OS-backed moderate draw is also preserved as OS_ACQUISITION_RESULTS.json plus the 189,440-byte OS_PREFIX. Its exact replay matches; no reselection or extra full Cox reference was used.

Read the probability/source distinction in CERTIFICATE.md: the algorithm theorem assumes independent unbiased input bits. Recorded SHA256 tapes are deterministic reproducibility fixtures, not certified random-source samples. The metric is multiplicative coupling/CDF, not relative rare-tail accuracy or continuous total variation. This is internal verification, not external novelty certification.

Run:

    python certified_clock.py --budget-only
    python certified_clock.py --reference
    python -m unittest -v test_certified_clock.py
    python certified_clock.py --replay-recorded OS_PREFIX

PREFLIGHT_BUDGET.json and EXTREME_RARITY_PREFLIGHT.json specify exact inputs and prior work bounds. REPLAY_RESULTS.json and EXTREME_RARITY_RESULTS.json contain exact outputs, counts, and fingerprints. PROVENANCE.json records source hashes; the original proofs and prototypes are unchanged.
