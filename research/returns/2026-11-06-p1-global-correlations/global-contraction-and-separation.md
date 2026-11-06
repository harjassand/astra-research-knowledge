# Exact global contraction, SAT-preserving compilation and finite-ring separation

The [full return](P1_GLOBAL_CORRELATIONS_20261106_RETURN.txt) and [research note](package/RESEARCH_NOTE.txt) supply an exact operation, not the missing unrestricted polynomial SAT algorithm.

For integer wire parameters`t_i`, use `K_t=[[1,1−t],[0,t]]`, rows indexed by`y`, columns by`x`. The network sums explicit local tables`A_v(y_v)`, `B_w(x_w)` against`∏K_t(y_i,x_i)`. Working modulo`2^p`, let`δ_i=v₂(t_i)`. Transform each B-side table by

`B̃_w(y_w)=Σ_(x_w⊇y_w) B_w(x_w)∏_(i∈x_w\y_w)(1−t_i)`.

A degree-`d` table costs`d2^(d−1)` modular updates, polynomial in its **explicit table length**. No exponentially large table is supplied by a free short evaluator. The exact global result is the sum of transformed terms with`Σδ_i y_i<p`, each weighted by`∏_(y_i=1)t_i`. Omitted terms are individually divisible by`2^p`; no approximate cancellation claim is used.

Define `r(p;δ)=#{S⊆[E]:Σ_(i∈S)δ_i<p}`. For full explicit input length`I`, the reported conservative bit bound is

`O((I+1)³(p+1)²+r(p;δ)(E+1)²(p+1)²)`.

Retained subsets have polynomial-delay/space enumeration, and working space is polynomial in`I+E+p`. Precision costs`p` bits, not merely the binary encoding length of`p`. This has no hidden conditional-counting oracle, but it is not polynomial when`r` is superpolynomial.

The weak-wire representation retains arbitrary CNF SAT. A constant gadget uses `K=[[1,−1],[0,2]]`, `J=[[2,1],[0,1]]`, `H=JJᵀ=[[5,1],[1,1]]`, with `KJ=2I` and`KHKᵀ=4I`. Both`K,H` have rank1 modulo2, yet the gadget carries a scaled equality at higher precision.

A uniform compiler uses clause tables of width≤3, deterministic OR chains for wide clauses, and degree≤3 equality trees for repeated signals. Every original assignment has a unique consistent auxiliary extension. Empty clauses/conjunctions and variable renaming retain their source encoding semantics. Replacing`m` ordinary wires by the gadget gives `E=2m` and `Zweak=4^m #F=2^E #F`.

For binary CNF length`N` and occurring-variable count`n`, the source bounds `E≤12N`, network bits`O(N log(N+1))`, construction`O((N+1)³)` and precision `p=E+n+1≤13N+1`. This residue recovers the exact count by shifting`E` bits. A polynomial exact contractor for this family would solve SAT, but none is constructed. The local transform sends`H` to `UHUᵀ=diag(4,1)` with `U=[[1,−1],[0,1]]`; extracted wire weights restore four times equality. All`δ_i=1`, and`p>E`, so **every subset survives: `r=2^E`**. That explains this algorithm's remaining cost, not why every algorithm must enumerate those states.

For a given boundary of`b` wires, the minimum number of terms in a full-kernel representation `Kboundary(y,x)=Σ_(j≤r)f_j(y)g_j(x)` over`R=Z/(2^p)` is exactly

`r=#{S⊆[b]:Σ_(i∈S)v₂(t_i)<p}`.

For common positive valuation`δ`, it is `Σ_(j=0)^min(b,ceil(p/δ)−1) binom(b,j)`. In particular,`t_i=2,p=b+1` needs`2^b` terms. This is finite-ring separation dimension, not ordinary rank of the matrix reduced modulo2.

Invertible wire operations diagonalise the kernel with diagonal entries`∏_(i∈S)t_i`. Nonzero entries modulo`2^p` give the stated count. The source's lower bound uses the image module: nonzero diagonal entries`2^a`, `a<p`, each contribute a generator to `imD/2imD`. Submodules of`R^k` need at most`k` generators over this chain ring, so factoring through fewer coordinates cannot suffice. Writing each nonzero diagonal entry separately attains it. The full proof, including nonunits, remains in the supplied original; Capital ran no module calculation.

An unweighted binary-clause family realizes the same conditional-count matrices: for each boundary pair use selector`s_i`, `δ_i` auxiliary bits, clauses `(¬s_i∨x_i)`, `(¬s_i∨y_i)` and`(s_i∨¬a_ij)`. Its one-pair count matrix is `[[1,1],[1,1+2^δ_i]]`, equivalent by invertible integer operations to`diag(1,2^δ_i)`. At`δ_i=1`, it has`4b` variables,`3b` binary clauses and`O(b log(b+1))` description; precision`b+1` needs`2^b` separated terms. **These disjoint formulas themselves are easy to satisfy/count**, and product-boundary contractions can be easy. A full-boundary representation requirement exceeds the original SAT search/decision output requirement; it is not a general algorithm lower bound.
