# Independent review: uniform occupation bound
31 October 2026. Reviewer: independent internal mathematical review.

## Source and verdict
PASS, with no additional mathematical correction required. I read the complete actual source:
graded_reservoir_opening_20261031/UNIFORM_OCCUPATION_BOUND_CANDIDATE.md
3,340 bytes, SHA-256 136e1cf32b06eac6dbfba53f1e7c4a91783c607233779f2cf7ce55fa234509dd.
Its byte count and hash were independently checked. This is a separate local bound and cutoff improvement, not a whole graded-reservoir compiler acceptance.

## Weighted-square constant
On each finite total-number cutoff, R R^dagger<=g^2 N and [N,R]=R remain valid without using an infinite canonical commutator. With F=z^N, the transformed damping term is -4lambda(z-1)N/z. The transformed interaction is, up to sign, i c(R-R^dagger), c=(z-1)/sqrt(z).

The quadratic-form Cauchy–Schwarz/Young estimate gives
+/- i c(R-R^dagger)<=eta N+c^2 g^2/eta.
At eta=2lambda(z-1)/z, half the damping remains. The constant is exactly Gamma(z-1)/2, Gamma=g^2/lambda. Thus the source's differential inequality
M_z'<=Gamma(z-1)M_z/2-2lambda(z-1)Q_z/z
has the stated constants. The number-preserving free Hamiltonian contributes zero irrespective of its norm.

## Normalized convexity and solution
For a normalized positive joint state, f(s)=log Tr(exp(sN)rho) is convex and f(0)=0. Therefore f'(s)>=f(s)/s at positive s, which is exactly Q_z/M_z>=log(M_z)/log(z).

Writing u=log M_z gives u'<=a-bu with the displayed a and b. Vacuum has u(0)=0. Integration yields
u(t)<=g^2 z log(z)/(4lambda^2) * (1-exp[-2lambda(z-1)t/(z log(z))]).
This estimate is cutoff-uniform. Trace-preserving system instruments, including their retained records, preserve the total averaged number moment, so the differential comparison composes across prescribed controls. No normalization on an individual selected outcome is permitted.

At z=2 and mu=g^2/(4lambda^2), the formula is M_2(t)<=2^{2mu(1-exp[-lambda t/log 2])}<=2^{2mu}. The tail bound 2^{2mu-L} is correct.

## Cutoff consequence and domains
Under compatible self-adjoint number-preserving H_f sector restrictions, free evolution and lowering loss terms agree on embedded smaller-cutoff states. The only outgoing Hamiltonian block has B_L^dagger B_L<=g^2(L+1)Pi_L. The positive-state trace commutator estimate followed by Duhamel gives the source's conservative trace-norm bound
2Tg sqrt(L+1) 2^{mu-L/2}.
It is also a valid upper bound if trace distance is defined with an extra factor one half.

The smaller of this uniform-time prefactor and the previously proved exp(Gamma T/8) prefactor may be used. In particular L of order mu+log(2+Tg)+log(1/epsilon), with a fixed enlargement absorbing log(L+1), suffices. No H_f implementation cost is reduced by this argument.

Finite models first establish the estimates. Compatible cutoff maps are then Cauchy on the stated vacuum/control experiment, with the canonical extension justified by the already reviewed finite-particle density/contractivity construction. The source properly requires a self-adjoint direct sum rather than unrelated cutoff Hamiltonians, and does not claim uniqueness of every formal unbounded GKSL extension.

## Scope
The normalized-state assumption is essential: the jump-count tilted state has variable trace. Applying the same log-convexity argument to that state without carrying its log trace would be invalid. No time-uniform emission-count bound follows.

This local result improves occupation truncation, not accumulated activity, source preparation, complete first-event assembly, private-time error composition or the actual supplied H_f evolution cost. The full graded-sector compiler remains separately pending. No implementation, novelty or practical-efficiency claim is included.
