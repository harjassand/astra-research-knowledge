# Normalized source forests: exact identity and a useful endpoint reduction

Independent analytic audit, 2026-11-02.

## 1. Exact integration identity (not a pair-potential approximation)

For a fixed finite family of complete source histories indexed by I, let C_i be the owned clock columns. Encode both column deletion and native source–rod interactions by

`f_i(r)=0` if r occupies a column in C_i, and otherwise by the product of its pair factors with source history i.

Thus |f_i|<=1. For a background cluster Γ set F_i(Γ)=product_{r in Γ}f_i(r). With w(Γ) the original connected background cluster measure, strict KP gives the exact identity

`log[Xi(z product_i f_i)/Xi(z)] = sum_Γ w(Γ) [product_i F_i(Γ)-1]`.

This holds by absolute convergence also for f_i=0 and complex phases. There is no assumption of positivity. For each finite I, algebraically expanding the bracket gives effective hyperedges

`U_J = sum_Γ w(Γ) product_{i in J}[F_i(Γ)-1]`, J nonempty.

The logarithm contains ALL J, not only pairs. The sums defining each U_J are absolutely convergent for fixed I, since |F_i-1|<=2. Direct source–source factors remain outside this background ratio.

A nonwinding singleton on a source's own column contributes the negative deleted scalar pressure. It must be combined with its source-history measure BEFORE absolute values. For compatible disjoint owned columns the pure deleted singleton constant is additive in columns. Singleton interactions with other sources are not pure deleted constants and must not be discarded. This identity precisely identifies where a naive pairwise reduced source gas fails.

## 2. What a sufficient forest lemma must say

A sufficient, genuinely additional lemma is an exact connected interpolation/forest representation whose majorant has, for n source vertices, one endpoint weight per incident tree edge of the form

`P_i = c_0 m_i + c_1 sum_{intervals on C_i}(a0+b length)`

(possibly with a polynomial βJ0K and incidence factor in c_0,c_1), with spatial bridge kernel row sum L uniform in bath volume. Every normalized history measure in that majorant must retain its scalar pressure subtraction. It is NOT sufficient to assign each owned column the full-time weight a0+bβ.

One promising interpolation is h_s=1+s(h-1), s in [0,1]. It preserves |h_s|<=1 and the native KP bounds. However, this fact alone does not prove the required normalized forest identity: differentiating the normalized denominator produces extra terms, and deleted-column singleton cancellation must survive their reorganization. No such cancellation is claimed here without a proof.

## 3. Degree moments are affordable (proved reduction)

Suppose the endpoint forest lemma above is established, and reserve a fixed extra trajectory tilt δ>0 within strict native KP. The marked full-column transfer-matrix calculation can be repeated with charges (1+δ)a0,(1+δ)b. Its residual remains O(J0):

`exp[(1+δ)a0] M0((1+δ)b) - h_nv = J0 + O_δ(x J0)`

provided (1+δ)b<μ by a fixed margin. This follows from the same resolvent identity; it does not cost exp(βJ0K).

Consequently, after charging dictionary and support overheads, for d endpoint marks one has

`integral normalized_source_majorant * P_i^d <= B_i * d! * R_i^d`,

where B_i has the desired scale

`B_i <= [Q_dict * K^(b_c) * exp(C βJ0 b_c) * βv]^(m_i)`

and R_i can be chosen proportional to m_i plus polynomial bridge factors. Indeed y^d <= d! δ^(-d) exp(δy), and the extra exponential is absorbed into the spare trajectory tilt. Endpoint constants proportional to m_i can instead be absorbed by spare source-label charge; support growth must be explicit.

The factorial d! is not a fatal loss. For n>=2 the exact labeled-tree identity is

`sum_{T on [n]} product_i deg_T(i)! = (n-2)! * binom(3n-3,n-2)`.

Proof: Prüfer codes give multiplicity (n-2)!/product_i k_i! for degrees k_i+1, sum k_i=n-2. Multiplying by product_i(k_i+1)! leaves product_i(k_i+1); its generating function is (1-z)^(-2n). Extract z^(n-2).

Thus the tree sum is at most n! C^n for an absolute C (e.g. 8), compatible with the 1/n! in the connected source expansion. If the bridge row sum is L, the spatially summed n-source term is bounded geometrically in C B L, rather than suffering an extra factorial divergence. This closes a real combinatorial concern once the forest lemma is supplied.

## 4. Required geometry and exceptional-source bookkeeping

Q_dict includes actual local matrix-unit/Pauli and bath overhead. K^(b_c) is not polynomial in K if b_c grows with K. Likewise C_an, source incidence, row sum L, and native degree D must be retained; none is silently constant in a growing-support compiler.

If the forest theorem is proved for scalar short sources and pinned test roots with the same majorant, the old scalar/exception consumer applies: all memory-touching sources with m>=d/b_D remain exceptional, even accidentally scalar ones; arbitrary bath-only sources remain scalar. Test-root control is needed separately for the matrix-valued exceptional estimate. Scalar zero-freeness alone does not imply an operator-log expansion or a matrix pin bound.

## Status

The exact background hyperedge identity and factorial/extra-tilt reduction above are proved. They do not yet constitute the requested connected source expansion. The unresolved step is an exact pressure-preserving forest extraction with a bath-volume-uniform bridge row sum. Neither fixed-support moment bounds nor strict KP quoted without this reorganization establishes that step.

## 5. Positive-Poisson reformulation and its exact limitation

If the nonwinding singleton trajectory activity is positive, let P_a be its exact finite-β total mass on column a. Factor `exp(sum_a P_a)` from the native gas. This is an exact independent-Poisson normalization. Deleting C contributes `exp(-sum_{a in C}P_a)`; hence the large scalar cancellation is automatic at this stage. The residual native logarithm contains only winding/wrap singletons and nonsingleton connected clusters, whose local absolute mass is O(βJ0) by the audited bound. The finite-β difference from βh_nv is retained as the already quantified tail.

This identifies a useful backbone criterion: a background cluster touching two distinct deleted owned columns cannot be a one-column singleton. Its cost belongs to the small residual native pressure. A background singleton can, however, bridge multiple external source intervals on neighboring columns; its endpoint costs must be charged to actual intervals, not replaced by full-time columns.

Caution: geometric contact components of a Poisson configuration are not independently weighted after assigning each its own void-probability factor. Their exclusion neighborhoods may overlap. An exact component regrouping must retain the induced hard-core compatibility or a single global Poisson normalization. Otherwise it silently asserts precisely the source factorization that remains to be proved.
