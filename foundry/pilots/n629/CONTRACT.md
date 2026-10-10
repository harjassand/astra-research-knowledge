# Exact mathematical and algorithmic contract

All arithmetic is over F_2. Let `m,w >= 0`. The supplied maps
`L_i : F_2^m -> F_2^{r_i}` are represented by lists of `r_i` binary row masks
with `0 <= mask < 2^m`. Zero rows, empty blocks, repeated/dependent rows,
repeated maps, and arbitrary common kernels are legal. Block codomains may have
any finite binary dimension. This pilot uses least-significant coordinate first.

For each ordered pair `(u,v)`, form the image span
`{0, L_i(u), L_i(v), L_i(u)+L_i(v)}`. It must have size 1 or 4 in every block.
Equivalently `rank(L_i | span(u,v))` is 0 or 2, never 1. Let `C` be the set of
these pairs. This definition admits `(0,0)` and admits other dependent pairs
when the joint kernel is nonzero. The complete input support is the whole
binary vector space; a caller cannot silently restrict it to an arbitrary subset.

The source `Sampler(m,blocks)` exposes exact integer `total=|C|`, `count(prefix)`,
`unrank(index)` and `draw(rng)`. Prefix bits describe `u` then `v`, each from least
to most significant bit. A legal index is an integer in `[0,|C|)`; a legal prefix
is a list of 0/1 bits of length at most `2m`. `count` is the number of completions,
including zero for inconsistent prefixes. `unrank` is intended to be a bijection
onto `C`, not numeric order on packed pairs. `draw` calls `rng.randrange(total)`
once, then un-ranks. It does not sample the independent translation `a` itself.
Malformed dimensions, masks, prefixes, ranks, arbitrary nonlinear maps and
nonuniform latent distributions are excluded from this source API contract.
Source assertions are not a hardened input validator; do not use Python `-O`.

Given an ideal uniform integer rank, `draw` has exact mass `1/|C|` at every pair.
The finite suite checks this implied distribution by enumerating every rank,
not by interpreting sampled frequencies as proof. Seeded `random.Random` is used
only for reproducibility and finite validity tests. Its finite pseudorandom state
does not itself prove ideal random bits or cryptographic randomness. Uniform
integer generation from unbiased bits can use rejection: expected O(m+1) bits,
with no finite worst-case bit bound. Choose `a` independently uniformly in F_2^m
and output `(a,a+u,a+v)` to obtain the coupling. Each latent row is uniform;
every block is all equal or all distinct. The latent law is uniform on
`2^m |C|` triples, and its exact KL divergence from three independent uniform
latent rows is `log(4^m/|C|)` (natural logarithm). Observed codeword divergence
is at most this by data processing.

The source claims `|C| >= 4^(m-2w)` for arbitrary maps, hence
`D_KL <= 2w log 4`. With common-kernel dimension `h`, there are `4^h` pairs
that give identical observed rows, and their probability is `4^h/|C|`.
The latent diagonal `(0,0)` has probability `1/|C|`. For joint kernel zero,
`|C|=1+6G`, where `G` is the number of good two-planes. If `w>=1,m>=2w`, the
source's theorem guarantees `G>=1`, so conditioning away `(0,0)` gives three
distinct latent and observed rows. **The provided `draw` does not do this
conditioning** and always has positive diagonal mass. At `m=w` coordinate
rank-one maps can have `C={(0,0)}`. No distinctness promise applies there.

The claimed deterministic work for construction, exact counts and unranking is
`5^w poly(S)`, where `S` counts `m`, `w`, all explicitly supplied binary rows,
and output length. This is exponential in `w`. Even with no rows, an output
has `2m` bits, so `poly(input)` cannot mean polynomial in a compressed `log m`
description of the ambient dimension. Python integer masks are a convenient
encoding; their JSON byte count is reported separately from dense matrix bits.
There are at most `5^w` signed systems, each in `2m` variables. Their coefficient
absolute-sum bound is `7^w`, so counts/intermediate sums need O(m+w) bits.
Gaussian elimination and O(m) prefix counts contribute polynomial factors.
The supplied implementation stores merged bases and uses `5^w poly(S)` memory
in the worst case; a polynomial-memory streaming implementation is only a
source-described possibility and is not implemented or benchmarked here.

Simple rejection proposes independent uniform `(u,v)` and accepts exactly `C`.
Its exact expected proposals per output are `4^m/|C|`, at most `16^w` conditional
on the support-size theorem. Proposal validation costs polynomial explicit-input
time. Its runtime and random bits have no finite worst-case bound. Brute force
visits `4^m` pairs and stores accepted pairs in this pilot; its setup is included.

The broader sunflower problem supplies an arbitrary family of sets, without
binary coordinates, full linear support, translation invariance or efficient
kernel membership. Here each observed row is a transversal with one symbol in
each of `w` disjoint blocks, the maps and basis are already supplied, binary
addition preserves support, and the uniform full-space law gives all three
marginals for free. The theorem allows diagonal mass and exponential dependence
on width. It does not acquire a large additive subfamily, learn its maps, handle
arbitrary biased source laws, find sunflowers in arbitrary set families, prove
the sharper `m>w` conjecture, or establish historical originality.
