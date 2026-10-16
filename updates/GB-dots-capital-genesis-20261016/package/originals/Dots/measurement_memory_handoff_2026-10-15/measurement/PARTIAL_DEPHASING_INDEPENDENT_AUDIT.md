# Independent audit: finite partial unread dephasing boundaries

Date: 2026-10-15. Verdict: PASS under the precise channel, independence, and reservation assumptions below.

## 1. Scalar skipped-full-pinching model

Take M equal weak-noise cells of duration delta=tau/M, exact initial and final full G pinchings, and M-1 internal channels

    T = r Id + (1-r) D_G,    0 <= r <= 1.

Each channel acts as this exact map on the full retained memory-plus-bath system, with identity action on the bath. Fresh independent reservoirs realize the composition; no discarded reservoir reinteracts. Boundary channels, durations, and supports are fixed independently of the input, perturbation parameters, and endogenous outcomes.

Choose the canonical latent-mixture dilation: an input-independent classical bit chooses Id with probability r or D_G with probability 1-r. Keep these bits and the successful full-pinching labels only as mathematical inaccessible environment coordinates.

Condition a whole latent success pattern. Merge adjacent weak cells whenever their shared full-pinching boundary was skipped. Let L_b be the total weak duration of merged block b. Every block begins and ends with a full G-sector copy. Deleting all of its assigned weak terms leaves a sector-preserving baseline, hence its endpoint mismatch projector Q_b obeys

    Q_b U_(z_b=0) W = 0

for every joint input and every setting of other interpolation parameters. The detector lemma gives product block-action-squared effects. Union over at least one bad block in each selected parent gives, conditional on all latent patterns,

    F_R(patterns) <= product_(i in R) c_i(pattern_i) I,
    c_i(pattern_i) = min{1, sum_(b in parent i) a_b^2}.

If ||V_i|| <= J_i, then a_b <= J_i L_b.

For one parent, two cells at separation k lie in the same block exactly when their k separating boundaries all skipped. Thus

    E sum_b L_b^2
      = delta^2 [M + 2 sum_(k=1)^(M-1) (M-k) r^k].

The resulting valid parent budget is

    p = min{1, J^2 tau^2/M^2
                  [M + 2 sum_(k=1)^(M-1) (M-k) r^k]}.

It interpolates between min{1,J^2 tau^2/M} at r=0 and min{1,J^2 tau^2} at r=1. The formula also handles M=1 with an empty sum. For r<1 the bracket equals

    M(1+r)/(1-r) - 2r(1-r^M)/(1-r)^2.

## 2. Cross-parent products and shared baths

The conditional detector estimate is uniform over the shared bath and all fixed other latent patterns. The bath need not factorize, reset, or commute between parent interactions.

If the entire latent boundary-pattern tuples are independent across parents, averaging their product costs factorizes:

    E_patterns product_i c_i(pattern_i)
       = product_i E c_i(pattern_i)
       <= product_i p_i.

Consequently F_R <= product_(i in R) p_i I, even with arbitrary shared-bath memory. Independence of physical syndrome outcomes is neither assumed nor inferred. Input-independent latent mixture probabilities and independent boundary-channel composition are what matter.

If parent patterns are correlated, replacing the joint cost moment by a product of its marginal means is unjustified. One must retain E product_i c_i or supply a separate correlation bound. Conditioning on an exogenous geometric schedule is allowed only when the stipulated conditional pattern independence and channel bounds still hold.

## 3. Generator-specific partial pinchings

For commuting stabilizer generators S_a let

    D_(S_a) = (Id + Ad(S_a))/2,
    T = product_a [r_a Id + (1-r_a) D_(S_a)].

The product is composition of exact joint channels. Its canonical independent mixture expands as

    T = sum_(H subset {1,...,m}) w_H D_H,
    D_H = product_(a in H) D_(S_a),
    w_H = product_(a in H)(1-r_a) product_(a notin H) r_a.

The all-generators component is D_G, so with q=product_a(1-r_a),

    T = q D_G + (1-q) R,

where R is the normalized convex mixture of the other D_H. At q=1 the remainder is irrelevant. Generator dependencies cause no difficulty; some proper H may already generate G, so this q may be conservative.

R can safely be treated as a skipped FULL boundary for the merged-block proof, with effective skip probability r=1-q. Crucially, R remains physically present in the common dilation. It cannot be replaced by Id.

Every D_H has Kraus projectors that are functions of G. Therefore its dilation preserves each entering full G sector. A merged block with all its weak terms deleted still has identical entering and exiting full labels even with any number of R channels in its interior. The all-input deletion-null identity survives unchanged.

For completion support, retain the partial-pinching outcomes as additional mathematical Kraus labels. Their projectors are scalar or zero on each encoded Pauli-error orbit, independent of the logical state. Removing them termwise leaves the same net block Pauli, supported on the weak-error footprint, with syndrome equal to the full endpoint difference. Equivalently, use the shifted-projector identity P_v E = E P_(v xor syn(E)). One must not simply commute an arbitrary Pauli through an intermediate partial projector.

The existing full-footprint condition

    Pauli(A) intersect Centralizer(G) subset phases times S_code

then makes every zero-mismatch block support-free in the established common-decoder sense. Bad parents can be charged on the original full reservation. Shared-bath coefficients remain in their original chronological order.

Sector preservation alone would suffice for deletion nullness but NOT for support: a skipped channel containing an undetected logical unitary is an immediate obstruction. The particular R here is safe because it is a mixture of pinchings by code stabilizers, with the termwise scalar/zero property.

## 4. Relaxing initial and final full pinchings

Suppose the endpoint channels independently have canonical mixtures

    T_in  = q_in  D_G + (1-q_in) R_in,
    T_out = q_out D_G + (1-q_out) R_out.

Mark a parent bad whenever either endpoint selector fails to choose its full D_G component. This failure event has probability

    e = 1 - q_in q_out.

On the both-success branch, use the internal-boundary budget p_int above. Treat the failed-endpoint branch as an arbitrary operation on the full bounded parent reservation. The same conditioning-and-product argument gives the valid combined budget

    p_parent = e + (1-e) p_int
             = 1-q_in q_out + q_in q_out p_int.

Equivalently, with an uncapped internal cost C_int, use min{1,e+(1-e)C_int}. This is at least as sharp as the looser e+p_int bound. Across selected parents the product follows when their endpoint/internal selector tuples are mutually independent and the conditional quantum estimate is uniform.

If endpoint selectors are correlated, replace q_in q_out by their actual joint both-success probability, and require whatever cross-parent pattern independence is used for factorization. Failed endpoints cannot be dropped or treated as harmless while still using the sector-difference deletion argument.

The exact initial correction-controller requirements are unchanged. If a genuine trusted correction record already guarantees the initial G sector, an additional full initial pinching is unnecessary for the first-block identity; charging its latent failure would merely be conservative. This refinement must not be used to replace an exact syndrome-controlled correction by a partial/noisy one without a separate qualification.

## 5. Exact conditions and obstructions

- Full reservations, clean disjoint concurrent memory resources, fixed timing, common parameter-independent dilation, norm bounds, and full-footprint detection/no-local-logical assumptions remain those of the deterministic cell corollary.
- All extra selector and pinching labels are inaccessible environment coordinates. Neither the controller nor the final decoder may depend on them unless separately physically available and authorized by the model. The good CP decomposition only requires one common decoder.
- Equality with T must hold on the joint retained memory-bath channel. A correct reduced-memory marginal with a reused or correlated reservoir is insufficient.
- For a pure stabilizer dephasing semigroup exp[t gamma(Ad S-Id)], the exact single-generator coefficient is r=exp(-2 gamma t). However, a finite interval of simultaneous unknown Hamiltonian coupling plus dephasing does NOT automatically equal the sequential boundary channel T followed or preceded by the weak cell. One must supply that exact interface or separately analyze/charge the intervening coupling.
- Boundary duration, resets, and enlarged total reservation time remain real geometric costs. Holding total boundary time fixed while increasing M generally changes q, so the fixed-q 1/M improvement is not a free infinite-rate limit.
- The product statement is a joint subset effect bound, not a small normalized conditional probability along arbitrary partial histories.

## Conclusion

The scalar partial-boundary formula, cross-parent product, generator-specific remainder treatment, and conservative endpoint-failure extension all pass. The crucial distinction is that partial pinchings may be ignored as FULL sector boundaries, but not erased from the physical channel. Their exact sector-preserving and Pauli-orbit-scalar structure is what preserves both deletion nullness and completion support.
