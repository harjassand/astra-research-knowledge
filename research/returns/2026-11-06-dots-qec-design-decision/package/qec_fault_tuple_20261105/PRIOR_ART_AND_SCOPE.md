# Closest prior methods and limits of the present comparison

## What is actually added here

The acquired operation is an exact rational, killed, score-folded proposal for ordered oriented faulty-edge tuples on an acquired weighted circuit detector graph. It collapses clean-route multiplicity, retains all error weights rather than only minimum faults, and samples the full background edge noise before evaluating the fixed decoder. A finite integer certificate turns a numerically proposed table into an exact normalizer and an IID Bernoulli acceptance law. The current measured comparison is to our earlier path-cover implementation on the same d13/d21 inputs. This is not a claim of a new general rare-event principle or of beating the strongest published methods.

## Closest fault-set counting prior

Regev, Dilley and Bennink, *Closed form logical error rate approximations for surface codes*, arXiv:2605.03054v3 (11 September2026), explicitly identifies overcounting when multiple minimum logical paths contain the same physical error locations. It counts minimum-weight error configurations using their geometric transitions and derives an idealized surface-code approximation with an additional measurement-error treatment. This is a close conceptual predecessor to collapsing clean-route multiplicity. It does not, as stated, provide the same all-weight fixed-decoder interval for the acquired weighted circuit graph. We have not executed its software on a matched target and do not claim a speed advantage over it.

Primary source: https://arxiv.org/html/2605.03054v3

## Rare-event union and fault-subset methods

Karp-Luby-style union estimators and ALOE already turn overlapping rare-event covers into unbiased estimators; canonicalization is not itself a new statistical principle. ALOE also makes clear that efficient proposal sampling and overlap handling must be paid for. The present gain is a concrete circuit-specific cover and exact finite table, not the existence of importance sampling.

Owen, Maximov and Chertkov, *Importance sampling the union of rare events with an application to power systems analysis*, arXiv:1710.06965: https://arxiv.org/abs/1710.06965

Fault-subset/malignant-set sampling is established in quantum-error-correction reliability work. Such methods must be compared at their actual fault-set acquisition/enumeration cost, remaining-weight bias, and sampling uncertainty; they cannot be dismissed by comparing only to naive direct rejection. Nor should our finite cover be called the first IID rare-failure method.

## Splitting and MCMC

Mayer et al., *Rare Event Simulation of Quantum Error-Correcting Circuits*, Quantum 10, 2237 (2026), arXiv:2509.13678v4, is the directly relevant circuit-noise splitting incumbent. It extends Bravyi-Vargo splitting to circuit-level noise and reports logical failure rates below 10^-20, with additional leakage and post-selection treatment. Thus accessing extremely rare full-circuit failures is already established; the current operation must be assessed for its particular IID confidence contract, scope and full resource cost, not as the first access to that regime. Primary source: https://arxiv.org/abs/2509.13678 ; journal: https://doi.org/10.22331/q-2026-10-15-2237 .


Bravyi and Vargo, *Simulation of rare events in quantum error correction*, arXiv:1308.6270, is the central splitting/MCMC baseline: https://arxiv.org/abs/1308.6270 . Modern implementations, including Haruna and Murakami arXiv:2610.35498 and their mcmc4qec code, are relevant practical comparators. A same-input circuit experiment is a separate obligation: matching only code distance while changing noise, decoder, observable or uncertainty target is not a controlled comparison.

Splitting can use correlated samples and still be practically superior. We distinguish an exact IID fixed-shot coverage theorem from empirical error bars requiring mixing assessment, without treating the latter distinction as a blanket runtime victory. The current packet does not establish an independently calibrated hardware-noise model or superiority over optimized splitting.

## Limits that remain even after the finite gain

1. The repetition-line theorem in THEOREM.md proves exponential acceptance loss at fixed p, despite exact distances and unique clean routes. The tuple relaxation still does not condition omitted clean edges.
2. Fixed internal distance cap64 can lose geometric distance suppression on larger instances. Increasing it raises preprocessing/kernel costs. No distance-uniform polynomial result is established.
3. The measured distance matrices and shell kernels are largely dense. Small H-table size alone is not the full memory or setup cost.
4. A smaller exact normalizer guarantees larger acceptance probability per trial on the same target law. It does not guarantee smaller runtime per trial, total wall time, or superiority to another method.
5. The circuit projection retains one detector basis plus one original logical observable. It is not a simulation of the full joint Pauli logical channel.
6. The confidence result is conditional on ideal independent random bits. The actual reproducible Python PRNG run is not proof of physical randomness. The fixed noise model is not a hardware reliability certificate.

## Terminal matched-comparator result

The independently implemented published subregion heat-bath/BAR challenger used the same nonuniform d21 graph probabilities and fixed integer-cost decoder, with a predeclared 31-rung odds-tilt ladder, 16 chains, 2,000 burn-in and 2,000 retained steps per rung. It hit its fixed 1,200-second process cap after 13 of 31 rungs, so it produced no complete target probability or uncertainty interval. The process used 239,500 KiB peak RSS; its independent high-noise anchor was also charged. Partial traces and all sources are preserved in ../qec_fault_tuple_comparison_20261105/.

This is one executed, fixed-budget challenger, not a proof that splitting is slower or less accurate, an optimized time-to-accuracy measurement, or a result for every prior method. The subsequently canceled Zanella run was not executed. No partial ladder was extrapolated to the target and no favorable post-result schedule was substituted. Superiority over the strongest published circuit splitting/subset methods remains unresolved. The tuple result remains a verified finite cover/decision improvement over its own earlier path-cover implementation, not a general rare-event breakthrough.
