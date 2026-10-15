# Preserved first route: sharp branchwise rank-collapse cutoff

15 October 2026. Exact mathematics independently reconstructed from the N636
exterior-power mechanism. This route was not selected as an exceptional
foundational result: exterior-power nilpotency and local-automaton delay are
established comparators. Historical novelty of the exact combined formulation
is unresolved.

Capital revision read: `25fc24509a59aabee340b36b588c9e59a144253d`.
Decisive source: N636, `updates/CT/package/work/COORDINATOR_CHANNEL_COMPRESSION.txt`,
lines 1–135, exact routed file
`frontier/proof_ranges/f545febb99796892bd63923e.txt`.
Its scoped branchwise rank-one test was read; its source-derived status was
not upgraded. No other campaign worker file was read for candidate selection.

## Exact all-parameter result

Let `1<=r<d`, put `q=r+1` and `D=binom(d,q)`, and let `K_1,...,K_m` be
arbitrary linear maps on a `d`-dimensional vector space over a field.
If there exists `L` such that every product of `L` generators has rank at most
`r`, then every product of length `D` has rank at most `r`.
The bound `D` is attained, including by finite trace-preserving instruments
over the complex numbers. The number of outcomes is allowed to grow with `D`.

Proof of the upper bound. On `E=Lambda^q V`, define `A_i=Lambda^q K_i` and
`V_0=E`, `V_(t+1)=sum_i A_i V_t`. Then `V_t` is exactly the span of the images
of length-`t` exterior products. Since `V_1 subset V_0`, monotonicity gives a
descending chain, and any equality persists forever. In dimension `D`, a
descending chain which eventually reaches zero must do so by time `D`.
Functoriality and `Lambda^q B=0 iff rank(B)<q` prove the claim.

Proof of sharpness. Enumerate the `q`-element subsets of `{1,...,d}` as
`S_1,...,S_D`, with their increasing wedge bases `e_(S_j)`. For `1<=j<D`,
let `B_j` map the ordered basis of `S_(j+1)` bijectively to the ordered basis
of `S_j` and annihilate the other coordinates. It has rank `q`, and

`Lambda^q B_j = e_(S_j) e_(S_(j+1))^*`.

These are matrix units on a directed chain. All products of length `D` are
zero in the exterior representation, while the product along the chain of
length `D-1` is nonzero. Therefore the original family has collapse index
exactly `D`.

To make a trace-preserving instrument, replace `B_j` by `c B_j` with, for
example, `c=1/(D+1)`. The matrix `sum_j (c B_j)^*(c B_j)` is diagonal and
strictly below the identity. Add one rank-one Kraus operator
`sqrt(1-c^2 h_a) |e_1><e_a|` for each coordinate `a`, where `h_a` is the
number of source subsets among `S_2,...,S_D` containing `a`. These fill the
diagonal exactly. Their `q`th exterior powers vanish because `q>=2`, so they
do not change the collapse index. All entries are explicit algebraic numbers.
If Gaussian-rational entries are required, express each integer
`(D+1)^2-h_a` as a sum of four integer squares and use up to four rank-one
fillers for coordinate `a`; the usual four-square theorem then supplies an
exact rational completion. This last existence observation is not a claim of
an optimized bit-complexity implementation. QED.

The supplied-generator interface is essential. It is not a
representation-independent entanglement-breaking criterion: a completely
depolarizing qubit channel has an invertible Pauli Kraus representation,
whose every branch product is invertible, while the channel itself is
entanglement breaking. The cutoff also concerns every word, not existence of
one low-rank word or almost-sure finite-time purification.

## Restricted binary search and falsified extrapolation

`search_partial_injections.py` exhaustively enumerates two partial injections
on `d` coordinates whose combined domains cover all coordinates. The induced
unordered-pair graph is acyclic exactly when every sufficiently long product
has rank at most one. Its longest-path vertex count is the collapse index.
Each family has an exact rational trace-preserving monomial realization:
for a coordinate appearing in both domains use nonzero weights `3/5` and
`4/5`, and for a coordinate appearing in only one domain use weight one.
The columns of either operator are orthogonal, so completeness holds.

The finite exhaustive results are:

| `d` | maps surviving necessary single-letter tests | unordered pairs tested after domain coverage | maximum index |
|---:|---:|---:|---:|
| 4 | 125 | 2,796 | 6 |
| 5 | 866 | 136,020 | 10 |
| 6 | 7,057 | 9,093,600 | 14 |

Thus the tempting conjecture that **binary partial-injection instruments
attain `binom(d,2)` for every `d`** fails already at `d=6` in this exact
restricted search. This does not imply a 14-step upper bound for arbitrary
two-outcome `6 by 6` Kraus matrices, nor a formula in untested dimensions.
The general sharpness proof above allows a growing number of generators.

Examples are recorded in `restricted_search_results.json`. Missing transitions
are encoded by `-1`, and coordinates are zero based. The exact search code
has no floating-point rank tests.

## Closest verified primary prior art

- M.-P. Beal and J. Senellart, On the bound of the synchronization delay of a
  local automaton (1998):
  https://www-igm.univ-mlv.fr/~beal/Recherche/Publications/echelle.pdf
  establishes quadratic synchronization-delay behavior even on two letters.
- M.-P. Beal, E. Czeizler, J. Kari and D. Perrin, Unambiguous automata:
  https://igm.univ-mlv.fr/~beal/Recherche/Publications/unambiguousAutomata.pdf
  distinguishes the linear complete-local case from quadratic general delay.
- Horodecki, Shor and Ruskai, General Entanglement Breaking Channels:
  https://arxiv.org/abs/quant-ph/0302031
  supplies the standard rank-one Kraus/measure-prepare equivalence.

Neither the finite search nor the sharp cutoff is reported as a major
foundational advance. The finite search was stopped after it killed the
proposed all-dimension binary extrapolation.
