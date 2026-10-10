# Sunflower alphabet surgery: exact operations and their limits

Date: 2026-10-10. Scope: the three-petal case of the general sunflower problem.

## Result and status

No exponential general sunflower bound is proved here. The logarithmic loss is not removed. This pass constructed an exact loss-accounted alphabet operation and tested the steps it would need:

1. **Lossless local folding is insufficient.** There are sunflower-free codes of rank `w` and size `exp(O(w))` whose alphabet product is `exp(Theta(w^2))`, and every single identification of two symbols either destroys injectivity or creates a sunflower.
2. **The same obstruction has an explicit simultaneous repair.** Delete one specified row per three-row witness, then fold every active alphabet to binary. More than two-thirds of the original rows survive. The total logarithmic loss is less than `log(3/2)`, independent of the number of folds.
3. **A prescribed coordinate cannot always be erased at constant loss.** Exact projection representations of linear three-uniform hypergraphs, combined with a probabilistic construction proved below, give sunflower-free codes for which the best injective sunflower-free subfamily after erasing that coordinate has relative size tending to zero.
4. **Even an adaptively chosen coordinate may cost a factor of three.** An explicit 12-row code of rank three has maximum safe retention four after deleting any coordinate. This is verified without relying on numerical optimization.

These are mechanism-level facts, not a claimed advance in the general sunflower bound. In particular, (1) does not give superexponentially large sunflower-free families; its large quantity is the ambient alphabet product. Statement (3) does not rule out adaptive choice of a different coordinate or a nonlocal operation. Novelty of the constructions has not been established against all prior literature.

## 1. Reduction and notation

Independently assign each ground-set element one of `w` colors. A given `w`-set is rainbow with probability `w!/w^w >= exp(-w)`. Thus every uniform family has a `w`-partite subfamily with at least this fraction of its members.

A partite family is a code `F` in `A_1 x ... x A_w`. A triple of distinct codewords is a sunflower exactly when, in every coordinate, its three symbols are either all equal or all distinct. The only forbidden coordinate pattern is exactly two equal symbols. All assertions below use this exact relation.

## 2. A genuinely executable fold-and-prune operation

For a coordinate map `f`, construct a conflict hypergraph on the original rows:

- Put a two-element edge on every pair that `f` maps to the same row.
- Put a three-element edge on every triple whose images are three distinct rows forming a sunflower.

Then a row subset `I` is independent in this hypergraph if and only if `f` is injective on `I` and `f(I)` is sunflower-free. This is an exact equivalence, and permits exhaustive or integer-programming implementation on modest inputs.

For a single identification `a ~ b` in coordinate `i`, the newly forbidden triple edges have an especially precise form: every other coordinate was already all-equal or all-distinct, and coordinate `i` originally had pattern `(a,a,b)` or `(a,b,b)`. They cannot be ignored. A triple originally all-distinct in that coordinate can instead acquire a new two-equal obstruction; that effect is beneficial, and is also captured by the exact image test.

For nonnegative row weights, choose a maximum-weight independent set and charge

`loss = log(total weight before / retained weight)`.

This is an accounting potential, not an established bound. For repeated coordinate erasures with uniform initial weights, the charges telescope. A rank-zero injective code has at most one row, so a universal `O(w)` total charge would prove the desired exponential estimate. Merely defining this charge proves no such estimate.

The algorithms in `test_erasure.py` implement the exact conflict constraints. No polynomial-time claim is made: selecting a maximum-weight independent set is an expensive operation in general.

## 3. Arbitrarily large locally irreducible alphabet boxes

Fix integers `t >= 2` and `q >= 3`. Put

`G = t * binom(q,2)`.

Choose the least positive integer `m` for which `2^m >= G + m + 1`. The code has `t` active coordinates, each with alphabet `{0,...,q-1}`, followed by `m` binary tag coordinates.

Reserve binary tags `0,e_1,...,e_m` for controls. Give each ordered gadget label `(i,{a,b})`, where `0 <= i < t` and `a < b`, a distinct remaining binary tag. In its active coordinates place the following three rows:

- coordinate `i`: `a,a,b`;
- coordinate `h(i)=(i+1) mod t`: `0,1,2`;
- all other active coordinates: `0`.

All three rows receive their gadget's tag. Each control tag receives one row with all active coordinates zero.

### Sunflower-freeness

A triple involving more than one binary tag has a tag coordinate with exactly two equal symbols. A triple contained in a single tag must be that gadget's entire three-row set, and its active coordinate `i` has exactly two equal symbols. Controls contribute no within-tag triple. Thus the code is sunflower-free.

### Every one-symbol-pair identification is blocked

For any active coordinate `i` and any pair `a < b`, its designated gadget becomes a sunflower if `a` and `b` are identified. Its three images remain distinct because the helper coordinate still takes `0,1,2`. For a binary tag coordinate, identifying `0` and `1` merges the control rows at tags `0` and `e_j`. Thus every possible single-coordinate symbol-pair fold is blocked.

### Parameters

There are `3G + m + 1` rows and rank `w=t+m`; the alphabet product is `q^t 2^m`. Taking `q=2^t` gives

- `m=2t+O(log t)`;
- `w=3t+O(log t)`;
- `log |F|=Theta(w)`;
- `log(product |A_i|)=Theta(w^2)`.

This separates alphabet complexity from family size and disproves a lossless-fold normal-form argument based only on ambient alphabet product.

## 4. Positive surgery on the irreducible examples

In each gadget, delete its third row, the row with main symbol `b` and helper symbol `2`. Retain every control row. Now apply the same binary map to every active coordinate:

`beta(0)=0`, and `beta(x)=1` for `x != 0`.

The two surviving rows of each gadget remain distinct because their helper symbols are `0` and `1`. Rows from different tags remain distinct. The image is an injective binary code, hence sunflower-free: any three distinct binary rows have a coordinate with exactly two equal symbols.

The retained fraction is

`(2G+m+1)/(3G+m+1) > 2/3`.

Consequently, this single simultaneous surgery has logarithmic charge less than `log(3/2)`, even when it reduces the logarithm of the alphabet product by `Theta(w^2)`. Counting merges, summing alphabet sizes, or charging each locally forbidden identification independently would dramatically overcharge this example.

The repair depends on the common tag structure. No argument here extracts such tags or an analogous shared deletion cover from an arbitrary sunflower-free family.

## 5. An exact factor-three erasure certificate

The following twelve rows in `{0,1,2,3}^3` are sunflower-free:

```
001 002 020 030
100 113 211 212
223 233 300 313
```

After erasing any coordinate, a safe injective image has at most four rows. Here is a proof independent of the optimizer: a rank-two code is the edge set of a simple bipartite graph. A three-petal sunflower is either a three-edge star or a three-edge matching. Thus a sunflower-free rank-two code has maximum degree at most two and matching number at most two. Every path or even cycle has at most twice as many edges as its maximum matching, so the entire graph has at most four edges.

The supplied verifier checks all triples of the twelve rows and finds a four-row safe projection in each direction. Thus the retention ratio is exactly `1/3` for every coordinate. Products of this code preserve sunflower-freeness and provide arbitrarily high ranks with the same first-erasure ratio in every coordinate. This establishes a lower bound on a one-step charge, not an unbounded total-budget obstruction.

## 6. A prescribed coordinate can have unbounded pruning cost

### 6.1 Exact projection representation

Let `H` be a linear three-uniform hypergraph on a vertex set `V` of size `N`. Suppose it has a coloring `c:V -> [q]` under which every edge has exactly two colors, with multiplicities two and one.

For every unordered pair `{x,y}`, let `B_xy` be the unique edge of `H` containing that pair if one exists, and otherwise let `B_xy={x,y}`. Make a coordinate whose partition has one non-singleton class `B_xy` and singleton classes for all other vertices. The row for `v` records its partition class. Append an identity coordinate with a different symbol for every vertex; this guarantees distinct projected rows and never creates a two-equal triple pattern.

The sunflower triples in these rows are **exactly** the edges of `H`:

- An edge `e` meets any other edge in at most one vertex. In a coordinate built from an edge, the three labels of `e` are all equal if the block is `e`, and all distinct otherwise. A block from an uncovered pair cannot contain two vertices of `e`.
- If `{x,y,z}` is not an edge, then the block `B_xy` contains `x,y` and does not contain `z`. That coordinate has exactly two equal labels.

Finally prepend the coordinate `c(v)`. Every triple that was a sunflower is now blocked by exactly two equal colors, so the full code is sunflower-free. Erasing the prepended coordinate recovers precisely the sunflower hypergraph `H`. The largest safe retained family has size `alpha(H)`.

The construction uses `binom(N,2)+2` coordinates. This large rank is important to its scope.

### 6.2 Such hypergraphs can have independence fraction tending to zero

Here is a self-contained existence argument; no general high-chromatic-hypergraph theorem is assumed.

Partition `N=q^2` vertices into `q` classes of size `q`. Let the eligible triples be exactly those with two vertices in one class and one in another. Select each eligible triple independently with probability

`p = q^(-11/4)`.

All selected edges already have the required exactly-two-color property. We will delete edges to make the hypergraph linear while keeping every sufficiently large vertex set non-independent.

Set `s=ceil(q^(23/12))`. For a set `S` of size `s`, let `n_j` be its class occupancies. For sufficiently large `q`, the number of eligible triples inside `S` satisfies

```
E(S) = sum_j binom(n_j,2) (s-n_j)
     >= (s-q) (s^2/q-s)/2
     >= s^3/(8q).
```

The first inequality uses `n_j <= q` and Cauchy-Schwarz. Hence the mean number of selected edges in `S` is at least `q^2/8`. A binomial lower-tail bound shows that the probability it contains fewer than `q^2/16` selected edges is at most `exp(-q^2/64)`.

There are at most `(eN/s)^s = exp(o(q^2))` choices of `S`. A union bound therefore shows that, with probability tending to one, every such `S` contains at least `q^2/16` selected edges.

Let `D` count unordered pairs of selected edges sharing a vertex pair. A within-class vertex pair has at most `q^2` eligible completions; a cross-class pair has at most `2q`. Therefore

```
E D <= p^2 [ (q^3/2)(q^4/2) + (q^4/2)(2q^2) ]
     <= q^(3/2)/4 + q^(1/2)
     < q^(3/2)
```

for sufficiently large `q`. Markov's inequality gives `D <= q^(7/4)` with probability tending to one. Delete at most one edge for each colliding edge pair. The resulting hypergraph is linear; at most `D` edges have been removed. For sufficiently large `q`, `q^(7/4) < q^2/16`, so every size-`s` set still contains an edge.

Thus some linear hypergraph `H_q` has

`alpha(H_q) < ceil(q^(23/12))`,

and consequently

`alpha(H_q)/|V(H_q)| <= q^(-1/12)+q^(-2) -> 0`.

Each of the `q` color classes is itself independent and has size `q`, so also `alpha(H_q)/N >= 1/q`. This is consistent with the upper bound: the number of colors is not fixed but scales as `q=sqrt(N)`. After the representation, the code rank is `Theta(N^2)=Theta(q^4)`.

Applying the representation gives a sunflower-free code for which erasing one specified coordinate has an optimal logarithmic loss tending to infinity. This remains true with uniform row weights, so passing to weighted independent sets or fractional coloring cannot supply a constant guarantee for an arbitrary prescribed coordinate.

### Precise limit of the negative result

The example does not force every coordinate to be expensive. Its rank is `Theta(N^2)`, much larger than `log N`. An adaptive operation could erase auxiliary coordinates first, exploit their redundancy, or make a simultaneous transformation. The proof does not refute that possibility and does not refute the sunflower conjecture.

## 7. What is actually missing

A valid full proof using this approach needs a nonlocal invariant that identifies a useful simultaneous fold or a useful coordinate, and bounds the **total** deleted mass logarithm by `O(w)`. Neither ambient alphabet product nor a universal weighted guarantee for a specified coordinate does that. The exact operation and its accounting are available; the indispensable global estimate is not.

**The prescribed/adaptive distinction is decisive.** Repeated constant-fraction retention under an adaptively chosen coordinate would immediately give an exponential bound, so it remains a major unproved obligation, not a solution obtained by changing vocabulary. No credible new adaptive potential survived this pass.

This is not being presented as a new equivalent conjecture or as an affirmative research result. Further computation of small cases alone would not establish the required estimate. This branch should not be promoted until a concrete new global invariant survives the constructions above.

## 8. Reproduction

From the repository root:

```
python independent_programme/combinatorial_primitive_20261010/check_folds.py
python independent_programme/combinatorial_primitive_20261010/check_projection_embedding.py
python independent_programme/combinatorial_primitive_20261010/verify_erasure_certificate.py
```

These verifiers require only the Python standard library. The exploratory optimization additionally requires NumPy/SciPy:

```
OPENBLAS_NUM_THREADS=1 python independent_programme/combinatorial_primitive_20261010/test_erasure.py
```

`erasure_results.json` records the optimizer status. In particular, the size-12 code found in the alphabet-five search was **not** proved maximal. No maximality claim for that case is used. The asymptotic random construction is justified analytically above; the small projection checks verify the representation, not an asymptotic estimate.
