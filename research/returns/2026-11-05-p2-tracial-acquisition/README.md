# Finite-action acquisition from fresh maximally mixed collision baths

This construction bounds what **all retained physical mixed-bath outputs** can acquire about an arbitrary unknown quantum input, then supplies an explicit output-only receiver matching the weak-action scaling. A source can forget its input on a quadratic collision clock while recovery from the emitted registers takes a quartic clock. Identical reduced source dynamics therefore do not determine physical output acquisition costs.

Read the complete [report](package/tracial_acquisition.pdf), [editable proof](package/tracial_acquisition.tex), [independent converse proof and audit supplement](package/theory_converse.txt), and [exact partial-SWAP theory](package/partial_swap_theory.txt). All operational errors on these pages are **half diamond distance**, `delta(C,D)=||C-D||_diamond/2`, in `[0,1]`. Recorded diagnostic fields explicitly labelled raw trace distance or full diamond retain their unhalved convention.

| Distinct result | Direct route |
|---|---|
| Adaptive finite-action converse for arbitrary receiver processing | This page |
| Exact partial-SWAP output-only receiver and two acquisition clocks | [Decoder, product modules and identical source dynamics](partial-swap-decoder.md) |
| Finite local register, routing, calibration and error bill | [Physical interface](finite-interface.md) |
| Independent thermodynamic companion | [Active-port nonidentifiability and sharp known-drift criterion](active-port-nonidentifiability.md) |
| Independent computational companion | [Local unit-rate dynamics, spectral obstruction and prediction hardness](local-rules-prediction.md) |
| Original material | [ZIP](original/tracial_acquisition_research_package.zip), [complete captured return](P2_TRACIAL_ACQUISITION_20261105_RETURN.txt), [provenance and hashes](SOURCES.json) |

A subsequent [fixed weak-stream memory study](../2026-11-05-p2-weak-stream-memory/README.md) preserves this complete package unchanged and develops a general prefix memory converse, a broader deterministic nonselective covariant one-qubit boundary, and distinct Schur/block/virtual-statistic limits. Retained-outcome feedback and general coherent receivers are not excluded by the one-qubit theorem; the optimal causal tradeoff remains unresolved.

## Actual physical access

The source has finite dimension `d>=2` and arbitrary input/reference state. Every encounter brings a fresh finite ancilla `E_j` in `I/e_j`, independent of the input, reference, previous outputs and receiver quantum memory, conditional on a genuinely classical history. Initial bath purifiers and operating preparation keys are unavailable. Incoming mixed marginals alone do not establish this freshness contract.

The receiver can retain every emitted register and all their quantum correlations, apply arbitrary channels/instruments, and choose later source unitaries and source/fresh-ancilla interactions by classical feedback. It cannot return an emitted register to the source, couple retained quantum memory coherently back to it, replace fresh inputs by purified/precorrelated states, or use an additional source measurement/reset port. The final source is discarded. There are finitely many rounds with a paid finite stopping bound; bounded adaptive stopping is padded with zero-action rounds.

Charge each **entire encounter**, after removing source-only and fresh-ancilla-only local interaction pictures, by `a_j >= integral ||H_j(t)||dt`, with `hbar=1`. Dividing one encounter into subintervals does not create a succession of independent fresh baths.

## Universal finite-action law

Put `q_j=min(1,4a_j^4)`, `b=product_j(1-q_j)`, `alpha=1-b`, `c=1-d^-2`. For the full acquired channel `C` and its constant-output baseline `sigma=C(I/d)`,

```text
delta(C,Tr(.)sigma) <= min(1,sqrt[(d^2-1)alpha]/2),
inf_R delta(R C,id) >= c(1-sqrt(alpha)) >= c b/2.
```

The infimum includes every CPTP final decoder, with no computational bound, any protected receiver memory and arbitrary input/reference. This is an acquired-channel theorem; reduced-source relaxation is not a premise or a recovery certificate.

For branch-dependent actions and bounded stopping, an **every-history path budget** `sum_j -log(1-q(a_j,h))<=C_*` yields the same bounds with `b=exp(-C_*)`. This is not an expected-action theorem or free conditional postselection. When every `4a^4<=q_*<1`, target `epsilon<c/2` requires a worst-path fourth-action budget at least `(1-q_*)log[c/(2epsilon)]/4`.

The proof keeps the maximally mixed baseline source product with receiver memory in every classical block. A weighted norm `Tr(X^dagger X omega^-1)` contracts under receiver channels. For a fresh tracial input, the source partial trace of the first interaction commutator vanishes. An exact Volterra bound makes exported amplitude at most `2a^2`; orthogonal accumulation of old and new exported components gives squared-norm transfer at most `4a^4`. The observable amplitude itself need not be fourth order. Blockwise integrated action handles genuine feedback; the integral of a maximum branch norm must not be replaced by the maximum integrated branch norm.

Arbitrary-reference normalization gives the displayed channel bound directly. A centered weighted Cauchy–Schwarz estimate for entanglement fidelity yields `F_R<=d^-2+c sqrt(alpha)` and the all-decoder lower bound. The supplied supplement explicitly credits and proves the relevant Barnum–Knill/Petz and sharper Renes recovery inequalities with their correct dimension conventions; those general recovery principles are not claimed as new.

## Matching operation, product modules and clocks

The [partial-SWAP result](partial-swap-decoder.md) retains every output, prepares an independent maximally mixed dummy source and reverses the known collision circuit entirely on receiver hardware. It does not access the discarded source or bath purifiers. Its exact recovered channel is depolarizing, with half-diamond error `c r` for `r=product_j(1-sin^4(theta_j))`; every decoder has error at least `c(1-sqrt(1-r))`. This receiver is within a factor two of the optimum.

For **product emission channels** across independent modules, arbitrary entangled input/reference and collective final decoding are allowed. Let `c_i=1-d_i^-2`, valid local residuals `b_i`, and `U=product_i(1-c_i b_i)`. Every collective decoder has error at least `1-sqrt(U)`; for total dimension `D` the sharper supplied bound is `1-D^-2-sqrt[(1-D^-2)(U-D^-2)]`. Shared active controls that destroy product emission are outside this statement. The matching fixed-dimensional weak partial-SWAP construction costs `Theta(theta^-4 log(m/epsilon))` encounters per module, total quartic action `Theta(m log(m/epsilon))`.

## Supplied audit and numerical evidence

The [independent proof supplement](package/theory_converse.txt) supplies a substantive audit verdict and full arguments for the weighted-norm transfer, normalization, recovery comparison, product-module qualification and pathwise strengthening. This completed mathematical checking is credited at its actual fresh-tracial, one-pass, classical-feedback scope. Capital adds no new scientific audit or replay.

The [original matrix program](package/check_hot_bath.py) and [recorded results](package/hot_bath_checks.json) cover 48 qubit partial-SWAP cases with `N<=6`, five `d=3/4` cases including entangled references, 80 generic-Hamiltonian transfer checks and twelve measured-output feedback chains. Reported maximum qubit decoder entry discrepancy is about `1.11e-15`, and qudit/reference discrepancy `5.56e-17`. These are finite floating-point diagnostics, not an SDP optimum, formal proof assistant or physical experiment. Large counts and [plots](package/figures/acquisition_clocks.png) evaluate proved finite formulas, not a simulation of huge baths. The [resource table](package/resource_counts.json) uses the stronger centered bound; earlier diagnostic necessary-count rows use a simpler valid bound and need not have identical lower counts.

The finite [register implementation](finite-interface.md) pays routing, peak source coupling and encounter windows, precision, calibration, protected memory, isolation and real wall time. One full source SWAP is simpler when the physical source port allows it. Pure coherent ports, bath preparation keys, returning particles, nontracial probes and coherent feedback supply different resources. No arbitrary finite-temperature bosonic-bath theorem, general noisy many-body hardware theorem, practical superiority or historical-priority finding is asserted.

The [earlier P2 rare-failure results](../2026-11-05-p2-unknown-local-ports/README.md) retain their operational backbone, declared port reach, starting-mass and precision costs. [Warm results](package/WARM_RESULTS.txt), [selection record](package/SELECTION_RECORD.txt), [prior-art comparison](package/prior_art_comparison.txt) and [pinned source ledger](package/sources.json) preserve the actual boundaries. No efficient weak-export pure-port decoder was completed in the screened-out route; its failure is a construction gap, not a general impossibility theorem. Generated current retrieval has not been rebuilt; these complete proofs and scientific entries are directly public on GitHub.
