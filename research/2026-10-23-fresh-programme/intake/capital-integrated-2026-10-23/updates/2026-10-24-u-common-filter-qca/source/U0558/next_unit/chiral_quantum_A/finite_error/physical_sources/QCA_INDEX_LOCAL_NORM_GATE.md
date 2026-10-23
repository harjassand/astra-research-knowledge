# Finite-error source gate: what would certify a trivial QCA index?

**Bounded result.** I did not locate a primary theorem turning computational-basis input/output records alone into a quantitative GNVW-index-triviality certificate. The closest directly usable theorem is Ranard, Walter & Witteveen, “A Converse to Lieb–Robinson Bounds in One Dimension Using Index Theory,” *Annales Henri Poincaré* 23, 3905–3979 (2022), [DOI 10.1007/s00023-022-01193-x](https://doi.org/10.1007/s00023-022-01193-x), [author-version primary text, §§4.3, Props. 4.10 and 4.12](https://arxiv.org/abs/2012.00741).

## Explicit local-norm theorem

Proposition 4.10 states: if `α₁` and `α₂` are nearest-neighbor QCAs on the same one-dimensional quasi-local algebra and, for one adjacent two-site block `{2n, 2n+1}`,

`||(α₁ − α₂)|_{A_{ {2n,2n+1} }}|| ≤ ε ≤ 1/192`,

then their GNVW indices are equal. The same proposition gives a local support-algebra conjugacy implemented by a unitary `u` on the neighboring block `{2n−1,2n}` with `||u−I|| ≤ 36ε`. Taking `α₁` to be the identity QCA gives an explicit sufficient statement for triviality: full local operator-norm closeness to identity at this scale forces unit index (logarithmic index zero). Blocking converts a radius-`R` QCA to nearest-neighbor form. Proposition 4.12 gives the corresponding direct form: if a radius-`R` QCA obeys `||α(x)−x|| ≤ ε||x||`, `ε ≤ 1/192`, for every local `x` supported on at most `2R` sites, it factors into two block-partitioned layers of `2R`-site unitaries.

The norm here bounds the automorphism difference on **all** operators in the indicated local algebra (the operator norm of the restricted linear map). The proposition is dimension-independent, but it assumes exact QCA automorphisms with the stated locality. It is not a theorem about finite-shot probabilities, noisy channels, or records from a subset of inputs/observables.

## Why basis records do not instantiate that hypothesis

Computational-basis populations constrain transition probabilities, not the full action on local off-diagonal operators. Therefore basis-record agreement for a restricted set of preparations and readouts does not by itself provide the local operator-norm bound required by Proposition 4.10. To use the theorem one would need a validated bound on the full local map (or a rigorous reconstruction/error conversion to it), plus the QCA locality premise. This source does not supply such a conversion from classical records; for the opening’s boundary records plus untagged stationary bulk state, the direct criterion remains **UNKNOWN / NOT FOUND**. The central team separately derives a candidate conversion from local tags to the operator-norm hypothesis; that derivation is not part of this source.

This is a sufficient stability certificate, not a lower bound on how much experimentally acquired data are necessary. It does not say that the specific counter-conveyor is invisible to every classical record protocol.
