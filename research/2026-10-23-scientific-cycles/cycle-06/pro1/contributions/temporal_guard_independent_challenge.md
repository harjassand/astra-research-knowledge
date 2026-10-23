# Independent challenge of the guard–meander operator lower bound

Reviewer: the Cycle6 temporal-dual contributor, distinct from the constructive
proof author. This is a focused internal mathematical review, not external
certification or historical-priority evidence.

## Source inspected

Read `temporal_constructive_structure.md` in full, especially Sections 2–5.
Read its exact hypotheses against the Cycle5 bulk finite-prefix representation
and the independently derived closest-point duality in
`temporal_operator_dual.md`. No repeat of the old capacity audit was performed.

## Load-bearing points checked

1. **Physical coefficient and sign.** On a sufficiently deep core let
   `Z=W0* Ws`. Since `W0* Q W0=kI−Q`, the physical displacement is
   `G_s=2Q−kI+(Z*QZ−Q)`. Charge pinching gives the coefficient
   `G1=[C_−,C_+]`. The diagonal terms are `kI−2Q`; after removing these,
   the pair `(i,j)` acts on endpoint pattern `01` as
   `C_j C_i−C_i C_j`. This agrees with the constructive note. The deep
   computation transfers to every depth at least `k` through the inherited
   exact finite-prefix identity; it is not a physical bath restriction.

2. **Word cancellation.** With `g=i−1`, `E=U_(i−2)...U_0` and
   `M=U_(j−1)...U_(i+1)`, the two displayed identities in (6) follow
   by adjacent involution cancellations, without commuting distinct bath
   interactions. The exterior `E` cannot initially be discarded. It cancels
   only after proving that the inner bracket is input-only and bath-identity
   on a local charge sector preserved by `E`.

3. **Whole-bath local identity.** A nonnegative meander reduces to closed
   Dyck factors separated by unmatched pushes. A closed factor is an exact
   input-color permutation tensor the identity on every bath vector. Thus
   in `M* U_j M` its inverse cancels after the endpoint insertion, also for
   vacuum input. With unmatched colors `a1,...,ah`, the remaining operation
   shifts them to `a2,...,ah,z` and inserts `a1` atop the original bath;
   when `h=0`, this inserted color is `z`. The guard and zero endpoint then
   pop the guard color and this inserted color in opposite orders. Both
   branches restore the bath pointwise. No pop relies on an original bath
   color. The two output color maps consequently differ by exactly one
   transposition of distinct input color wires.

4. **Uniformity in the dual state.** The selected block is
   `P(I−SWAP) tensor I_E` as an operator identity, not an expectation in a
   diagonal or symmetric bath. Any coherent or entangled prefix density
   therefore contracts to the same input operator. A bath-state-dependent
   cancellation cannot remove this block. This is the crucial step that a
   uniform-prefix average by itself would not establish.

5. **Orthogonality and counting.** Different endpoint pairs flip different
   pairs of binary charge bits. Their matrix blocks are disjoint, so the
   weighted Hilbert–Schmidt squares add. Distinct full input charge patterns
   within one pair also add without cross terms. Under sigma, the guard and
   oriented endpoint event has probability `1/8`, the meander event has
   probability `p_r`, and the conditional uniform color square norm of
   `I−SWAP` is exactly `1`: the swap has normalized trace `1/2`. The
   Hermitian adjoint occupies a disjoint reverse domain of the same weight.
   Hence the per-pair contribution `p_r/4` has the correct factor of two.

6. **Uniform lower constant.** The meander count
   `p_r=2^(-r) binom(r,floor(r/2))` follows by telescoping reflected
   endpoint counts. Its stated elementary bound is valid for even and odd
   r; in particular `p_(2m+1)=p_(2m+2)`. Summing the retained pairs gives
   `v_tau >= (k−2)(k−1)/(8 sqrt(2k))`. For `k>=4`, this exceeds
   `k^(3/2)/32`. Thus the lower is uniform in k and tau, not a fixed-k
   remainder statement or evidence from a short numerical sweep.

## Omitted-premise challenge

Positive net middle height is insufficient, even if the guard is retained.
The charge word `100111`, endpoints `i=1,j=5`, guard `g=0`, has middle
`011`: final height `+1`, but its first step is negative. With distinct input
and bath tokens, the first bracket restores the initial bath, while the second
can replace its top token by the input color at port 3. More explicitly, if the
initial bath is `b0·tail`, the second bracket ends at `a3·tail` and emits `b0`
at the guard. This is a witness against substituting final height for the path
condition, not a converse saying every non-meander block is useless.

## Conclusion and remaining obligations

The all-length proof establishes the claimed uniform lower bound on the full
operator dual objective. Combining it with the closest-point theorem yields
`A_k/k >= (ln2/256) sqrt(k)` for `k>=4`, with an actual operator-feasible
variational optimizer. The review does not infer an exact quadratic growth
law. It does not by itself establish nonlinear input positivity, exact drift
at nonzero beta, overflow, an arbitrary-reference code, feedback capacity, or
efficient compilation. The principal investigator retains those distinct
obligations and the physical fixed-before-horizon rule.

Costs: this focused analytic review used the native proof and exact identities;
no new k sweep, finite bath cutoff, or external numerical service was used.
Discovery and review wall-clock totals are unmeasured. The separate k=4
rational replay has its own resource receipt and is not this all-length proof.
