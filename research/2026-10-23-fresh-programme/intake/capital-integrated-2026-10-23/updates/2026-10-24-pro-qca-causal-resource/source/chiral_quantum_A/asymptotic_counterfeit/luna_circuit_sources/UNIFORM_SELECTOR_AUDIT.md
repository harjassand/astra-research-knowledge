# Uniform-source selector construction: exact mismatch and scope

Date: 2026-10-24

## Construction and exact count

Take blocks of length `L=M+k`, with `M=2^k` payload bits and `k` header bits. Interpret each header string as a selector `J_b` in `{1,...,M}`. Designate payload slot 1 as the logical bit `q`. The reversible encoder `P` controlled by the unchanged header swaps slot 1 with slot `J_b`; when `J_b=1` it does nothing. Thus the encoded logical bit is the selected input bit `q_b=x_{b,J_b}`. All other payload values, together with the header, are the syndrome. This is a bijection on the same `L` bits.

Let `C_left` replace `q_b` by `q_{b+1}` (indices modulo the number of coarse blocks) and leave all other encoded registers fixed, and set `F=P^{-1} C_left P`. Decoding block `b` gives

```text
header:       h_b (unchanged)
payload i:    x_{b,i},                         i != J_b
payload J_b:  x_{b+1,J_{b+1}}.
```

So, relative to the blockwise identity, only the selected payload bit can change. For iid uniform input bits and at least two independent coarse blocks, conditional on either block's header the two selected bits are independent fair bits. Therefore

```text
P(F(x)_{b,i} != x_{b,i}) = P(J_b=i) P(x_{b+1,J_{b+1}} != x_{b,J_b})
                         = (1/M)(1/2) = 1/(2M)
```

for every payload slot `i`; each header slot has mismatch probability zero. There are no extra data/workspace registers: `P` is just a permutation of the `M+k` bits, with the selector stored in the header. The one-coarse-block periodic degeneracy is excluded, since then `C_left` is the identity and the mismatch is zero.

The full index-cancelled operation in the opening is `Omega = sigma_right F`. Its natural comparison is the pure fine shift `sigma_right`, not pointwise identity. Since a shift permutes coordinates, the Hamming mismatch count between `Omega(x)` and `sigma_right(x)` equals that between `F(x)` and `x`. The exact `1/(2M)`-on-payload and zero-on-header profile above is in the source/block-relative frame before that final shift, or equivalently when error bits are labelled by the input registers that the fine shift transports.

There is a fixed-coordinate caveat if “header” and “payload” instead mean output slots in the original block partition after `sigma_right`. For a right shift by one fine site, the mismatch profile rotates one site: with order `[k headers, M payloads]`, output slot 0 receives the old last payload's error probability `1/(2M)`, while output payload slot `k` receives the old last header's zero probability. Thus the final-shift profile is not literally zero on every fixed output header and exactly `1/(2M)` on every fixed output payload. The period-averaged rate remains `1/(2L)`. This is a coordinate convention issue, not an error in the reversible selector map.

An exhaustive tiny replay confirms both frames: for `k=1, M=2, L=3`, two coarse blocks and all 64 binary inputs, residual mismatch counts in fixed `[header,payload1,payload2]` coordinates were `[0,16,16]` out of 64. After the fine right shift, compared with the pure right-shift baseline, fixed output-coordinate counts were `[16,0,16]`. This also demonstrates why the frame must be stated.

## Matching lower bound in the stated code class

Let any reversible block encoder be a bijection

```text
E: {0,1}^L -> {0,1}_q x {0,1}^{L-1}_s,
```

with one distinguished binary logical register `q` and an arbitrary syndrome `s`. Under a uniform physical block, `(q,s)` is uniform, so `q` is fair and independent of `s`. For independent neighboring uniform blocks, a single coarse countershift replaces `q_b` by an independent fair `q_{b+1}` and leaves `s_b` fixed. The decoded block equals its original value if the two q values agree; if they disagree, it must be a different length-`L` bit string because `E` is injective. Hence the probability that the decoded block differs is exactly `1/2`, and its Hamming distance from the original is at least one on that event. Consequently

```text
expected mismatches per decoded block >= 1/2,
mean mismatch probability per physical site >= 1/(2L).
```

The selector construction attains this bound: the changed block has exactly one flipped/replaced site whenever the selected bits disagree, so its expected Hamming distance is `1/2`. More generally, for a distinguished uniform `d`-level logical register, the block-change probability is `1-1/d`; translating that to a per-site lower bound requires an error metric that counts at least one changed physical symbol for any changed decoded block.

This is a lower bound only for blockwise reversible encoding into one logical register plus syndrome, one independent-neighbor logical countershift, and blockwise decoding, under the uniform product source and the stated mismatch metric. It does not lower-bound arbitrary QCAs: it says nothing about overlapping/multiblock codes, several logical registers, non-product sources, different error metrics, or general quantum-channel approximation. It also does not establish a universal asymptotic obstruction for all index-one local circuits.

## Reversible circuit costs

At the permutation level, the selector encoder needs no additional workspace bits. It can be specified as the mutually exclusive family of header-controlled swaps between slot 1 and slot `j`; the header is never measured or consumed. This does not make the control free. The controls have `k` header bits, the naive family has up to `M-1` nontrivial conditional swaps per encoder, and the coarse `q` movement spans blocks of physical length `L`. A hardware synthesis must charge gate count, control fan-in/decomposition, routing/range, depth, and clock time. An implementation that uses temporary ancillas must count them; an ancilla-free decomposition may instead cost more gates/depth. The exact no-extra-workspace statement is about the reversible block permutation and its register count, not a constant-cost or constant-depth actuator.
