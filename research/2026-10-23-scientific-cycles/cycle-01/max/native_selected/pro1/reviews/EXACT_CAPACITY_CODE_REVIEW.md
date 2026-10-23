# Independent constructive review: colored Dyck code for the tree reservoir

Date: 2026-10-21. Reviewer: `/root/recurrent_bath_literature`.

## Status and scope

The colored Dyck construction is correct. It supplies a zero-error code of dimension

`K_m = Catalan_m (d-1)^m`

in `2m` uses, with exact restoration of the entire bath after each code block. Its asymptotic rate is

`ln(2sqrt(d-1))` nats per use.

This review independently proves the construction and its growth rate. The matching converse through the ranks of vertex-conditioned Kraus operators is independently handled by the rank reviewer. Combining that converse with this construction determines the ordinary unassisted block capacity for the specified diagonal initial bath. Section 7 additionally supplies a finite-vertex compression argument extending the capacity conclusion to every fixed normal coherent initial bath. No efficient implementation, feedback-assisted capacity, entanglement-assisted capacity, or historical novelty is asserted.

The earlier pair-code lower bound and spectral-decay upper bound in `TREE_BOUNDARY_REVIEW.md` remain valid intermediate results, but the capacity gap between them is superseded by this matching construction and converse.

## 1. Device and code alphabet

Let `d>=3`, and put `b=d-1`. The bath Hilbert space is `ell²(V)` for the rooted infinite `d`-regular tree. At every nonroot vertex, port `0` points to its parent and ports `1,...,b` point to its children. At the root, ports `0,...,b` all point to children. The device maps a port/vertex basis state to the reverse directed edge:

`U|a,v>=|a',w>`.

Here `w` is the neighbor selected by port `a` at `v`, and `a'` is the port at `w` pointing back to `v`. This is the fixed involutive permutation already checked in `TREE_BOUNDARY_REVIEW.md`.

The code deliberately uses only ports `1,...,b` for forward moves. These ports always point to children, including at the root. Port `0` is used only to reverse a move made inside the same code word; it is never used to leave the starting vertex toward its parent or its exceptional root child.

## 2. Colored Dyck words

A code word `w=(w_1,...,w_(2m))` has symbols in `{0,1,...,b}`. Its height after `j` symbols is

`H_j = #{i<=j:w_i!=0} - #{i<=j:w_i=0}`.

Require

`H_j>=0` for every prefix and `H_(2m)=0`.

Every nonzero symbol is a push labelled by that color. Every zero is a pop. The ordinary last-in-first-out matching associates each pop with its most recent unmatched push. There are exactly `m` pushes and `m` pops.

Define the output word `F(w)` by

- placing `0` at every push position;
- placing the matched push color at every pop position.

For example,

`(a,b,0,0) -> (0,0,b,a)` and `(a,0,b,0) -> (0,a,0,b)`.

The parenthesis pattern, as well as the colors, carries logical information. The earlier two-use code used only the special pattern consisting of successive push/pop pairs.

## 3. Bath-independence proof

Fix any starting vertex `v`. Consider a prefix of the word and the stack of its unmatched push colors, `(a_1,...,a_h)`. The following invariant holds:

1. The current bath vertex is obtained by starting at `v` and following the child ports `a_1,...,a_h`.
2. At every completed push position the emitted symbol was `0`.
3. At every completed pop position the emitted symbol was its matched push color.

Initially the stack is empty and the bath is `v`, so the invariant holds. On a push `a`, child port `a>=1` leads to a child whose reverse port is `0`; the bath descends one level, the output is `0`, and `a` is appended to the stack. On a pop, nonnegative prefix height ensures that the stack was nonempty. The bath is therefore at a child entered earlier in this block. Its port `0` returns to that child's parent, emitting the stored child-port color at the parent and removing the top stack entry.

The pop never passes above the starting vertex. Thus neither its parent port nor the root's exceptional port-zero behavior is encountered at an empty stack. At the end of the balanced word the stack is empty and the bath is exactly `v`.

Writing `U_(2m)` for the sequential device on all `2m` input registers, the invariant proves the exact vector identity

`U_(2m)(|w>⊗|v>) = |F(w)>⊗|v>`

for every code word and every bath basis vertex. The output word is independent of `v`.

## 4. Injectivity and coherent correctness

The map `F` is injective. From an output word in its image, mark zero positions as pushes and positive positions as pops. This recovers the Dyck parenthesis pattern. Scan these positions with a stack; at each positive output symbol, assign its color to the matched earlier zero position. Assign input symbol `0` at the current pop position. This reconstructs the original word uniquely.

Consequently the map

`V_m|w>=|F(w)>`

is an isometry from the code subspace `C_m`, spanned by code-word basis vectors, to the output code subspace. The basis identity extends by linearity and continuity to the operator identity

`U_(2m)|_(C_m⊗E) = V_m⊗I_E`.

It therefore holds for arbitrary coherent bath superpositions and for any normal bath density, not only a diagonal one. Tensoring with the identity on any external reference proves correctness for entangled logical messages and bath purifications. Even initial code/bath correlations are preserved up to `V_m` on the code register.

An encoder identifies a `K_m`-dimensional logical space with `C_m`; the decoder applies the inverse isometry on its output image, with any CPTP completion outside that image. The resulting logical channel is exactly the identity. The bath returns exactly after the whole block and can be used for the next block without reset, access, or knowledge of its state.

This is terminal block return. It makes no claim that the bath returns at every intermediate use within a Dyck excursion.

## 5. Exact code count and asymptotic growth

The number of uncolored Dyck patterns with `m` pushes and `m` pops is

`Catalan_m = [1/(m+1)] binom(2m,m)`.

For completeness, among all `binom(2m,m)` balanced binary paths, reflect the prefix through the first visit to height `-1` of each invalid path. This bijects invalid paths with paths having `m+1` pushes and `m-1` pops, of which there are `binom(2m,m-1)`. Subtracting yields the Catalan formula. Each push independently admits `b` colors, while pop symbols are fixed at zero. Hence

`K_m = [b^m/(m+1)] binom(2m,m)`.

No asymptotic enumeration theorem is needed to establish the rate. The central binomial coefficient is the largest term in `(1+1)^(2m)`, so

`4^m/(2m+1) <= binom(2m,m) <= 4^m`.

It follows that

`(4b)^m/[(m+1)(2m+1)] <= K_m <= (4b)^m/(m+1)`.

Taking logarithms and dividing by `2m` gives

`lim_(m->infinity) [ln K_m/(2m)] = (1/2)ln(4b) = ln(2sqrt b)`.

Thus the rate loss at block length `2m` is only `O(log m/m)`. For odd total horizons, use the even-length code on the first `2m` ports and an arbitrary final input; discard its output. Future bath evolution cannot change the already emitted logical outputs.

The achievable rate is one bit per use higher than the earlier repeated-pair construction:

`log_2(2sqrt b) = 1+(1/2)log_2 b`.

## 6. Interface with the matching upper bound

For the diagonal initial bath `tau=sum_v pi(v)|v><v|`, the block channel has Kraus operators

`A_(w,v)=sqrt(pi(v)) <w|U_n|v>`.

For fixed initial and final vertices, distinct input words that reach the final vertex have distinct emitted words, because the full device is a permutation. Thus the associated operator is a scaled partial permutation whose rank is the number of length-`n` walks between those vertices. The separately checked tree adjacency-norm bound gives

`rank(A_(w,v)) <= (2sqrt b)^n`.

The rank reviewer supplies the matching coding inequality: a channel admitting a Kraus representation with each Kraus rank at most `M` has entanglement transmission fidelity at most `M/K` for every unassisted CPTP encoder and decoder of logical dimension `K`. Applying it here makes rates above `ln(2sqrt b)` impossible, with fidelity tending to zero exponentially at any strictly larger fixed rate.

Combining this converse with the code proved above gives

`Q_unassisted = ln(2sqrt(d-1))` nats per use,

or

`Q_unassisted = log_2(2sqrt(d-1))` qubits per use.

The zero-error block code achieves the same asymptotic rate. Since `2sqrt(d-1)<d` for `d>=3`, the rate is strictly below the full port rate. Its value is independent of the stationary-reference parameter `p` within the specified family.

Important assumption distinction: the **lower bound** is uniform over all coherent bath states. The displayed **upper-bound Kraus decomposition** uses a vertex-diagonal initial bath. It must not be silently generalized to coherent initial densities; summing vertex-conditioned partial permutations can increase operator rank. The following separate approximation argument handles that increase explicitly.

## 7. Extension to every fixed normal coherent initial bath

Let `tau` now be any fixed normal density on the same bath Hilbert space. Choose an increasing sequence of finite vertex sets `F_r` with union `V`, with corresponding projections `P_r`. Normalize the compressed state:

`tau^(r) = P_r tau P_r / Tr(P_r tau)`.

For all sufficiently large `r` the denominator is nonzero, and normality gives

`delta_r := (1/2)||tau-tau^(r)||_1 -> 0`.

Write `s_r=|F_r|`. A spectral decomposition of `tau^(r)` has eigenvectors supported on these `s_r` vertices. Its channel Kraus operators are linear combinations of at most `s_r` vertex-conditioned partial permutations. Rank subadditivity therefore gives

`rank(A_(w,j)^(r)) <= s_r (2sqrt b)^n`.

Apply the same coding-rank inequality as above. For every logical dimension `K_n` and every CPTP encoder/decoder pair,

`f_n(tau^(r)) <= s_r (2sqrt b)^n/K_n`.

The complete coded experiment is a single CPTP map of the initial bath density. Trace-distance contraction and the final entanglement-fidelity measurement give

`|f_n(tau)-f_n(tau^(r))| <= delta_r`,

uniformly in block length and in the encoder/decoder. Thus

`f_n(tau) <= s_r (2sqrt b)^n/K_n + delta_r`.

If the code rate is strictly greater than `ln(2sqrt b)`, first keep `r` fixed and take `n->infinity`. The first term vanishes. Then let `r->infinity`, proving `f_n(tau)->0`. Combined with the bath-independent Dyck code, this establishes the same exact capacity for every **fixed normal** initial bath state, including coherent ones.

This extension proves a strong converse without a state-independent exponential convergence rate: arbitrary normal states can have arbitrarily slow vertex-projection tails. It also depends on one fixed initializer across horizons. It does not authorize a sequence of increasingly delocalized coherent initializers chosen separately for each block length. The direct diagonal-state converse, by contrast, already has its explicit exponential bound without finite-support approximation.

This extension is an independently derived proof obligation supplied to the parent; it should receive the same independent check as the rank converse before being incorporated as a central theorem.

## 8. Bounded primary-source comparison

One search-service call made exactly these three narrow searches:

1. `"quantum channel" "Dyck" capacity`
2. `"quantum capacity" "regular tree"`
3. `"quantum channel" "stack" "Catalan"`

The returned results did not identify a primary paper proving this specific tree-device communication capacity. They included unrelated quantum streaming/Dyck-language work, random-unitary-channel work, and network terminology matches. No further broad novelty search was conducted, and no result was used as support for a priority claim.

The report's mathematical conclusions rest on the explicit construction, counting argument, and separately reviewed converse. Failure to locate the exact construction in this bounded search is not evidence of historical novelty or external certification.

## 9. Conclusion for continuation

The colored Dyck code closes the previous operation asking whether collective codes beat the repeated-pair rate: they do, by exactly one asymptotic bit per use, and the matching rank converse fixes the optimum for the specified diagonal bath model.

The capacity problem stated in this report is complete. Further activity should require a distinct operation or changed hypothesis. There is no mathematical reason to keep this exact-capacity operation open by chasing its polynomial block overhead or a spectral-cutoff constant.
