# Ordinary optimal fixed-point factories for internal selected means

Status: separate candidate option, not part of a frozen resource ledger. It strengthens the explicit polynomial implementation option in LAST_REFRESH_WHOLE_BRIDGE_AND_ENDPOINT_RACES.md; the latter's conservative polynomial remains sufficient.

## Primary component

Yoder, Low and Chuang, *Fixed-point quantum search with an optimal number of queries*, arXiv:1409.3305v2, equations (1), (14), (19): https://arxiv.org/html/1409.3305v2 . Their odd-length sequence L=2l+1 has failure probability

    delta^2 T_L(cosh(arccosh(1/delta)/L)*sqrt(1-p))^2.

Thus p>=pmin suffices for failure<=delta^2 if

    L>=arccosh(1/delta)/arccosh(1/sqrt(1-pmin)).

The known phases are alpha_j=-beta_(l-j+1)
=2 arccot(tan(2*pi*j/L)*sqrt(1-gamma^2)), with
 gamma=1/cosh(arccosh(1/delta)/L).
The accepted target can have a p-dependent phase. The theorem is an ordinary search/amplitude-amplification component, not a new normalization result here.

## Acquired controlled implementation and its actual scope

For a retained classical control label z (which can be coherent), let U_z prepare the factory proposal, and let the explicitly computed success flag define its target subspace. Reflections about the initialized work registers are implemented by U_z, the zero-register phase, and U_z dagger. Reflections about success are flag-controlled phases. A sequence of l generalized iterations plus the initial preparation uses exactly L proposal-unitary or inverse calls. All labels z and all seeds are retained; there is no unknown-state reflection oracle. Direct sums over z have the same uniform bound. The two-dimensional invariant space is the span of normalized success and failure projections, regardless of how many seeds they contain.

For the event-sector race use pmin=1/4. For the no-refresh race and conditional last-gap clock use pmin=1/2. These floors also hold for the ideal finite-grid circuit under the structural complement convention below. Choose delta=sqrt(xi), where xi is the desired FAILED PROBABILITY, and round L upward to an odd integer satisfying the displayed inequality. A certified upper rounding avoids exact transcendental comparisons.

In PREP dagger SELECT PREP, SELECT is diagonal in preserved history/control labels and is zero on any failure flag. Within each label the success vector is unchanged up to its common scalar amplitude and phase; the phase cancels. Consequently this factory changes the selected contraction mean by at most xi, even though its public-state isometry error need only be O(sqrt(xi)). For a sequence of at most three factories, whose probabilities depend on earlier retained outcomes, deleting their failed branches changes the final selected mean by at most 3xi. Orthogonality of retained seeds makes this an ordinary conditional probability union bound, with no cross-label interference. This statement does not apply to revealing the source state, uncomputing labels before SELECT, or the complete physical first-event instrument's outer amplification.

The primary phases are acquired classically. Evaluate arccot via quadrant-correct atan2 of sin/cos and sqrt(1-gamma^2), rather than a potentially huge tangent. Since L is odd, the sampled cosine is not zero; its separation is inverse-polynomial in L. All quantities have polynomial bit complexity in L and log(1/xi). There is no table over coherent durations. Approximate all L proposal calls and O(L) phase/reflection operations to total FULL-CIRCUIT operator error zeta by telescoping, for example each to zeta/[100(L+1)]. The selected-mean perturbation is then at most 2zeta, independently of the ideal failed probability xi. Actual controlled rotations, zero-register reflections, arithmetic and inverse circuits are charged.

This option removes generic phase-factorization preprocessing for these particular constant-gap factories and gives an explicit ordinary degree constant. It does not demonstrate a practical gate advantage. A proposal call still contains its fixed-rate clock bit rotations and comparisons; the three-call alternative instead pays its real scalar acceptance computation. Both must be compared on the same input, accuracy and retained-record convention.

## Finite-grid receiving clarification for both normalization options

The following implementation convention binds both this option and the polar option of frozen whole-bridge source8a9d53b8. Prepare one known coin with probability f approximating c/(c+s), and obtain its complementary coefficient as 1-f, not a separately rounded value. Prepare the a0 and pi coins with probabilities in[0,1]. Use interval-event flags of one clock, not subtraction of two separately rounded survival probabilities. Where the same survival probability x occurs in two branches, use identically prepared clock distributions (independent seeds are permitted). Then the late event-race weight sum is EXACTLY1+x*(1-f*a0)>=1 for the ideal rounded circuit. Early wQ>=1 structurally. The high atom race sums to x+1-pi*x>=1; the low atom race contains an always-accept branch. The finite conditional geometric clock has success>=1/2 by its exact decreasing-bin identity. Therefore the exact floors1/4 and1/2 survive clock/parameter discretization without relying on a tiny-error gap argument. Rounding changes the target law by the separately priced error, not the normalization floor.

Only subsequent actual gate/phase synthesis may violate these exact identities slightly; compare it to the ideal rounded circuit in FULL operator norm by the allocated telescoping bound. No approximate-gate success-floor assumption is needed. This is a finite-grid receiving precision qualification, not a changed physical source, virtual overflow cap or numerical ledger. As an optional less structured fallback, certify raw-law perturbation<1/8 and use smaller floors1/8 and1/4 with correspondingly longer degrees; no such fallback constants are silently substituted into the present option.
