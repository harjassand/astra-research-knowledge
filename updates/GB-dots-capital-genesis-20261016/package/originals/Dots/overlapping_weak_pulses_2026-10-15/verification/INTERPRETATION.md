# Certificate scope

## Exact symbolic certificates

- check_crossing_echo.py: rational crossing-pulse frame identity, Fourier Kraus completeness and genuine completion-syndrome probabilities. The conditional bad probability is 9801/10201, while the tested small pulse-action bounds are much smaller. Pair/subset smallness can still hold.
- check_crossing_independent.py: independent reconstruction of actual frame gates and causal measurement effects on every bath input. Intermediate syndrome recording is nondisturbing on the averaged encoded domain, including bath-reference coherences.
- check_three_pulse_moments.py: three interleaved noncommuting shared-bath pulses, exact normalization, all seven nonempty pulse subsets, and positive-semidefinite rational effect gaps. This is a finite example, not the general moment proof.
- check_memory_only_reorder.py: 16 correction/character operator identities and 64 initial-syndrome checks. Memory factors may be grouped at their completions while every bath factor retains chronological order. Joint pulse channels are not commuted.

## Floating-point stress test

check_subset_character_stress.py uses a fixed random seed, three Z3 coordinates, four time segments and four-dimensional full operators. Twelve instances produce 84 subset-effect checks with a 10^−12 numerical tolerance. The observed largest effect-to-bound ratio is approximately 0.278700619. These floating-point results corroborate examples only and are kept separate from exact certificates.

## Limits

No checker verifies the full asymptotic memory theorem, all allowed controllers or Hamiltonians, the published deterministic contour theory, hardware feasibility, a useful numerical threshold, or historical novelty. The universal result rests on the explicit proofs and their model assumptions. Source checkers are preserved byte-for-byte; generated outputs and manifests provide reproducibility and integrity evidence.
