# Independent local review: native dark-source count lemma

31 October 2026. Verdict: PASS for the specified bounded, acquired dark-jump generator and its actual counting unraveling. No complete coherent simulator is inferred.

Full source read and bound: `NATIVE_SOURCE_COUNT_LEMMA_CANDIDATE.md`, SHA-256 `e2230beee7a7b2ba87f5aa9fe234cc9265724d36b8d4bd03327bd1c3afda0653`.

## 1. Tilted energy calculation

Write H=(1/2)sum L_a†L_a, gQ<=H<=hQ, and G†H<=-kappa H. For u=exp(theta)-1 in (0,min(1,kappa/(16h))], a=4u/kappa and W=I+aH obey I<=W<=5I/4. The tilted adjoint is

G_theta†W=aG†H+u sum L_a†W L_a.

Since H<=hI, the recycling energy is at most h sum L_a†L_a=2hH. Its total coefficient is therefore -4u+2u+8u²h/kappa<=-3u/2. Discarding slack gives G_theta†W<=-(a kappa/4)H, exactly as used later.

## 2. Complete Hamiltonian bound and constants

Extend source operators by identity to system and reference. H_sys acts only on those latter factors and commutes with W. For any normalized positive joint state rho, q=Tr(Qrho), the QQ part of the commutator expectation is bounded by 2hbq. Positivity gives ||P rho Q||_1<=sqrt(q(1-q)), so the two offdiagonal terms contribute at most 2hb sqrt(q(1-q))<=2hb sqrt(q). These bounds require only ||K||<=b and do not require centering.

The source negative drift is at most -a kappa lambda g q/4. Under sqrt(lambda)>=16hb/(kappa g), the QQ contribution 2ahb sqrt(lambda)q consumes at most a kappa lambda g q/8. The remaining scalar maximum is

sup_(q>=0) {-a kappa lambda g q/8+2ahb sqrt(lambda)sqrt(q)}
=8a h²b²/(kappa g)=32u h²b²/(kappa²g).

Using q>=0 rather than q<=1 only enlarges this valid bound. Since it holds on every normalized joint positive state, it proves the operator inequality L_theta†W<=cI<=cW, with the displayed c. This step is complete/reference-uniform. It is not an application of Jensen to a nonnormalized tilted state.

## 3. Positive tilted propagation, controls, and tail cap

The tilted evolution is positive (indeed completely positive, but not trace preserving). Applying the operator inequality to it gives weighted expectation growth at most exp(cT). W>=I bounds the ordinary counting moment by that weighted expectation; arbitrary initial states cost at most two because W<=2I.

A prescribed arbitrary common CPTP instrument, with its outcome register retained, satisfies I_inst†(W)<=2I<=2W. Thus p such slots multiply the bound by at most 2^p. Trace-preserving recorded feedback or reference retention does not require a separate scalar-state argument. The stated factor 2^(p+1), exponential coefficient and Chernoff count cap follow. The instruments' own implementation events are not silently included in the chosen source-jump count.

For a fixed permitted u, theta=log(1+u) is comparable to u. Consequently the simplified cap scaling has a max(1,h/kappa) multiplier on the control/failure logarithms and the displayed h²b²T/(kappa²g) activity scale. The exact displayed cap remains authoritative.

## 4. Low branch and degeneracies

The conditional physical source intensity is lambda Tr(sum L†L rho_cond)<=2h lambda. Predictable-intensity domination by a Poisson process is valid without assuming independent physical jumps. Below the high-rate threshold, 2h lambda T<=512 h³b²T/(kappa²g²). This gives a low-branch count bound, not an acquired waiting-time sampler or simulation algorithm.

At lambda=0 there are no counted source jumps. At b=0 every positive lambda lies in the high branch, and the weighted estimate gives a time-uniform count MGF from finite initial source energy. The allowed system-only Hamiltonian does not invalidate this statement. No analogous conclusion is asserted for an uncharged source Hamiltonian that fails to commute with H.

## 5. Scope

This receipt concerns a well-defined bounded finite-source generator (or an independently justified bounded-generator setting); it is not an unbounded-domain theorem. N is tied to the exact supplied dark-jump representation. Changing the unraveling changes N, and it is not automatically a laboratory detector statistic.

The lemma receives arbitrary initial source/system/reference states and the prescribed joint CPTP slots stated in the source. It does not by itself acquire a complete first-event isometry, a positive coherent clock, source jump access, fast no-jump contractions, their finite-bit implementation, or a retained full simulator. Nor does absence of centering in this count proof remove an actual sqrt(lambda) coherent mean from the dynamics or its implementation cost.

The separately reviewed direction-merged local-energy source supplies a compatible native H/g/kappa certificate under its own hypotheses. That conjunction establishes this activity estimate for that representation, not equivalence to the threshold collision lift. No novelty, optimality, or practical advantage is concluded.
