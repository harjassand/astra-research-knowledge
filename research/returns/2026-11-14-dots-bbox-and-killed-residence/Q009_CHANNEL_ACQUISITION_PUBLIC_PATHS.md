# Executed original-scale four-corner channel acquisition

This fills an implementation gap in the delivered exp(52) archive: it had a computable partition law but no R200 channel sample or complete native path run. It does not solve the user's general rare-transition objective.

## Law and arithmetic
At R200, d132, q=exp(-1/25), each corner partition has law q^area/Z(d,d). Z(i,j)=Z(i-1,j)+q^i Z(i,j-1). Exact rational alternating Taylor bounds enclose q. Positive DP with Decimal ROUND_FLOOR/ROUND_CEILING encloses all Z. Each sequential branch uses a fresh lazy OS-random bit interval and compares it against outward branch-probability bounds. Ambiguity causes more bits and, if necessary, higher arithmetic precision; no fixed precision cutoff substitutes a chosen answer. The four corner laws and torus translation are independent.

Correctness is conditional on Python Decimal's documented directed arithmetic and genuine uniform secrets.randbits. It is not a proof-assistant certificate. Usual computable-real exact-sampling caveats apply to zero-probability exact threshold equality.

## Executed
One actual four-corner draw used 56,512 random bits, 80 decimal digits, no refinement and0.039 seconds including DP. Corner areas1356,811,671,935. The four-corner energy normalizer is acquired, not assumed.

The sampled channel then generated a translated native monotone path on the1600x1600 torus:1,280,000 additions in2.40 seconds. All additions were to absent spins, core additions had1 or2 physical occupied nearest neighbors, merge additions had at least2, every macro endpoint area/perimeter matched, and full endpoint shapes were independently compared at spaced checkpoints. The final addition was the first majority hit. A path hash and complete counters are recorded. Code emits no enormous path file.

The computation time is the time to CONSTRUCT a path, not the stochastic heatbath traversal time. This does not sample a physical trajectory, a full cut-energy edge, or the actual capacity. It does not validate the general overlap proof. It does not acquire the original thermal-source law (the flow injects through its valid all-minus reservoir edge, whose cost remains paid by the existing theorem).

## Reproduction
`python channel_sampler.py` generates a fresh exact-weight channel.
`python channel_path.py` uses that saved draw to construct/check the complete path.
`python check_partition.py` independently verifies rational normalizers by exhaustive partitions throughd5 and checks precision nesting.

The later exp(37)/exp(36) refinements described in inherited context were not available in this workspace. This run uses the delivered construction unchanged; no unlocated code has been relabeled as executed.

## Randomized central-interval refinement
A second implementation, `channel_random_interval_path.py`, uses the flow researcher's reconstructed law: choose a uniform first site in the central interval of m sites; for an occupied interval of j sites starting at i, extend left with probability i/(m-j), right otherwise. Integer rejection sampling via `secrets.randbelow` implements these probabilities without floating point. Each length-j interval is uniform: incoming contributions to start i sum to [(m-j-i)+(i+1)]/[(m-j+1)(m-j)] = 1/(m-j). `check_interval.py` also checks this by exact fractions for every m=1..64.

The complete randomized R200 path ran: 1,280,000 actual additions in 2.60 seconds, same endpoint/physical-neighbor checks and energy maxima as the deterministic-order path, translation [755,83]. SHA256 a20ec7396b788d2be390fa7960e42caac539218ea1c81fc6a8e74c2540bad335. This establishes an executable randomized path law, NOT a native stochastic trajectory or independent verification of the general flow-energy overlap bound.
