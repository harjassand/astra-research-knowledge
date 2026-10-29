# Costs, ordinary methods, and decision scope

The targeted capability was repeatable acquisition of small fast bilinear
algorithms from finite-field decompositions. A rank-47 rational 4-by-4 scheme
would be one possible output. It would not by itself beat the strongest
large-matrix exponent or optimized BLAS implementations. Addition count,
coefficient growth, recursion and floating-point error are separate costs.

The mechanism attempted here was exact obstruction-guided structural
rewriting. It was not an audit of the known native scheme: the actual
acquisition tested every one-plus expansion and every following flip,
including rank-48 intermediate decompositions, with unrestricted mod-4
corrections. All failed. General tangent-update algebra was constructed
and used to pay that finite search. No repaired characteristic-zero
algorithm, new rank bound, or practical speedup was obtained.

## Primary prior acquired before promotion

1. Fawzi et al., *Discovering faster matrix multiplication algorithms with
   reinforcement learning*, Nature 610 (2022), DOI
   [10.1038/s41586-022-05172-4](https://doi.org/10.1038/s41586-022-05172-4).
   Native factors and their cyclic output convention were acquired from
   [the official repository](https://github.com/google-deepmind/alphatensor).
   Factorizations are available information; their discovery cost is not
   claimed as ours. Nonsoftware materials are CC-BY 4.0; attribution retained.

2. Kauers and Moosbauer, *Flip Graphs for Matrix Multiplication*, ISSAC 2023,
   [arXiv:2212.01175v1](https://arxiv.org/html/2212.01175v1), §5. They already
   give flip-graph search and Hensel lifting, and report that over 100000
   4-by-4 rank-47 schemes failed lifting from Z2 to Z4. Thus the native
   fixed-point obstruction and the broad strategy are prior, not discoveries
   here. Their successful lifts in other formats show why simply assuming
   all modular improvements transfer would be an incorrect interface.

3. Dumas, Pernet and Sedoglavic, *A non-commutative algorithm for multiplying
   4×4 matrices using 48 non-complex multiplications*,
   [arXiv:2506.13242v7](https://arxiv.org/html/2506.13242v7), §§4–7.
   Their characteristic-zero rank-48 scheme is already rational, obtained
   by isotropy from AlphaEvolve's complex scheme, and they provide
   straight-line/basis variants. We do not rediscover rational descent,
   compare to Strassen49 as though48 were unavailable, or treat a successful
   hypothetical48 repair as a new rank record.

4. Khoruzhii, Gelss and Pokutta, *Faster Algorithms for Structured Matrix
   Multiplication via Flip Graph Search*,
   [arXiv:2511.10786v1](https://arxiv.org/html/2511.10786v1), §§4–6.
   Their modular-plus/flip/Hensel pipeline, alternative-field searches and
   complete public implementation are ordinary informed alternatives.
   Their actual source notes that F3 can recover inverse-of-two rational
   schemes and reports substantial multi-core search costs. We did not
   acquire F3 rank-47 inputs or duplicate that pipeline.

5. Perminov, [arXiv:2603.02398v1](https://arxiv.org/html/2603.02398v1),
   §§4.6,7.5, and
   [arXiv:2606.02480v1](https://arxiv.org/html/2606.02480v1), §5.3.
   Open implementations already perform constrained/unrestricted lifting,
   plus/flips, reconstruction and multiple-ring searches. The latter
   emphasizes sensitivity of lifting to modular structural moves.
   We claim no novelty for guided coefficient reconstruction or for
   generating alternative modular schemes.

Direct characteristic-zero nonlinear least-squares searches, SAT/SMT or
constraint searches, and broader plus/flip walks remain serious alternatives
for rank47. They have access to all the same native data and to the known48
construction. We did not execute or defeat them. In particular, replacing
one supplied F2 point by an optimally chosen characteristic-zero start is
an acquisition task, not a free input to our proposed repair.

Current Astra was checked selectively during hypothesis formation. Search
metadata and candidate titles are recorded in SOURCES.json. No preview was
imported as a theorem, no corpus search absence is a novelty argument, and
the potentially active field-acquisition branch was not read. No A/C/T
active designs or files were consulted.

## Measured and unpaid costs

All computation used the existing local Python environment and one process;
there were no new workers, solver services, packages, physical operations,
paid compute, external writes, or model runs.

| Acquired operation | Recorded time |
|---|---:|
| Fetch 16021 native binary bytes | 0.470136 s |
| Corrected 12-proposal pilot | 0.019025 s |
| All12972 ordered plus proposals | 15.156299 s |
| All27924 post-plus flips | 28.621422 s |
| Independent-row/full-system/lemma controls | 1.602288 s |

Compute timers start after Python imports. They are measured implementation
kernels, **not** the full elapsed research or engineering effort. Literature
intake, tool transport, coding, module startup, inspections and reasoning
are additional. No end-to-end speed claim is based on the sum. An initial
prototype hit a numpy-integer/Python-bit-vector type error before producing
a result; this was fixed by explicit Python integer exponent conversion.
The first 12-case pilot was rerun only for that repair, then the full scans
were executed once. The failed prototype was additional setup cost, not
silently successful acquisition.

The same 64 candidate plus states were tested with two methods:

| Exact method, same candidates | Kernel time |
|---|---:|
| Rebuild and solve whole Jacobian, ordinary Python control | 0.807201 s |
| Quotient compiler, excluding shared preprocessing | 0.023614 s |
| Shared base-image preprocessing for compiler | 0.002577 s |

Every answer and predicted rank agreed. Candidate materialization for the
ordinary arm was an additional0.001533s. This is an implementation control,
not a matched comparison with optimized published C++/M4RI solvers or their
incremental methods. It establishes that the compiler made our enumeration
payable; it does not establish a new best lifting algorithm or a practical
research multiplier.

No high-order lift or rational reconstruction was run: every proposal was
already exactly inconsistent at the first lift. No unobserved trajectories,
conditional inputs, pretraining, or physical measurements were assumed.
The complete scientific boundary is the specified finite binary rewrite
neighborhood and the general tangent-update lemmas. All characteristic-zero
global success, priority and practical-impact claims remain NOT_ACQUIRED.
