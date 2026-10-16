# Prior art and theorem dependencies

Novelty remains unresolved. The packet does not claim the first autonomous quantum memory, the first stabilizer twirl, or the first treatment of non-Markovian bath noise.

## Noise tailoring

- Wallman–Emerson, randomized compiling: https://arxiv.org/abs/1512.01098
- Cai–Benjamin, stabilizer-based twirling: https://arxiv.org/abs/1807.04973
- Beale–Wallman, stabilizer randomization and compilation: https://arxiv.org/abs/2306.13752
- Winick et al., Concepts and conditions for error suppression through randomized compiling: https://arxiv.org/abs/2212.07500v1 . Section III.2 treats persistent ancillary systems; Section III.3 treats gate-dependent/non-Markovian limitations including leaked frame information. These ideas are not claimed new here.

The present packet retains a joint-input instrument proof: a reduced-system Pauli-channel formula cannot in general describe arbitrary initially correlated system–bath inputs. See the exact correlated-input example in the theorem's final section.

## Autonomous memory comparison

- Drechsler–Oreg–Aharonov, https://arxiv.org/html/2610.05589v1 : synchronous channels and periodic Lindbladian constructions; the fully time-independent bounded-resource local memory gap is identified in Section 1.4.1. Randomly ordered local corrections require a separate continuous-time stability argument.
- Current 2D construction, https://arxiv.org/html/2601.20818v3 : discrete-time hierarchical QCA threshold; the continuous-time realization is an outline in the main text and Supplement VII, where its formal threshold proof is deferred.
- Pastawski–Clemente–Cirac, https://arxiv.org/html/1010.2901v2 : Section III.2 proves a nonlocal concatenated dissipative construction with growing block support; Section IV's static local 4D Toom proposal is supported numerically. The sweep rule here is different.
- Kubica–Preskill, https://arxiv.org/abs/1809.10145 : sweep operation and decoder-threshold predecessor. The local update geometry is prior art.
- Lake, https://arxiv.org/html/2510.08056v3 : rigorous asynchronous decoding with bounded waits and polylogarithmic noiseless control; Poissonian desynchronization is numerical.

Conditional significance: if independently verified, the stated sweep theorem gives a concrete fixed-local-resource, time-independent nonthermal memory under its specified noise model. The coherent extension concerns separately completed and randomized proposals. No exhaustive priority conclusion follows from this comparison.

## Probability imports

- Hartarsky–Toninelli, Corollary 9.5: https://arxiv.org/abs/2212.08437v2
- Swart–Szabó–Toninelli, Theorem 7 and Lemmas 13–14: https://arxiv.org/abs/2202.10999

Primary sources are linked rather than redistributed. Their complete theories are not reproduced by the finite checkers.
