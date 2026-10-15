# Independent reconstruction before reading the new author proof

Date: 2026-10-15. Internal same-team audit. This note was written before any new author proof was available or read. It uses the candidate statement and supplied `sources/mathematics_pasted.txt`, principally lines 222-333. Supplied source claims are data, not established premises. The source checkout HEAD was independently checked as `a6190a1083f688a7e4bf64adbc5244ef150ff2c4`.

## Contract

Let H be the Hilbert direct sum of countably many C^2 blocks. Let a_n>0 tend to infinity, c_n be arbitrary real numbers, b_n be real and bounded, and

    A_n=c_n I+a_n sigma_z,  B_n=b_n sigma_x.

A is the self-adjoint Hilbert direct sum on its natural domain and B is bounded. Each real linear combination sA+tB is self-adjoint on D(A) when s is nonzero, by the bounded perturbation theorem; at s=0 it is bounded. A successful common scalar probability noise nu and normalized POVM M satisfy, at every real frequency,

    M_hat(s,t)=nu_hat(s,t) direct_sum_n exp(i(sA_n+tB_n)).

The natural POVM convention is weak or strong countable additivity, not operator-norm countable additivity. An MGF ball in this note means finiteness at every g with Euclidean norm strictly less than R. Finiteness on the boundary and exact equality of the full MGF domain to that ball are separate claims.

## Necessary threshold: analytically reconstructed

Compression to any block gives a normalized positive operator measure with the same nu. If the noise MGF m(s,t) is finite in an open neighborhood of (s,0), the compressed measure has genuine exponentially weighted moments there, and

    F_n(s,t)=m(s,t) exp(sA_n+tB_n).

This must be justified through the finite block's compact distribution and genuine moment transfer; merely substituting imaginary frequencies is insufficient. For example, local complex analyticity plus positivity of the characteristic function gives even moments by finite differences, and the Taylor bounds sum to exponential integrability on a smaller neighborhood. Analytic continuation then identifies the displayed transform. A direct proof of that lemma remains required in the final theorem if not cited to a fully proved dependency.

Positivity of the tilted measure gives the operator moment matrix

    [ F_n       (F_n)_t  ] >=0.
    [ (F_n)_t   (F_n)_tt ]

Let kappa=log m and u=s a_n>0. Removing kappa_t from the second row and column and taking the Schur complement gives

    kappa_tt(s,0) E + E_tt - E_t E^{-1} E_t >=0,

where E(t)=exp(u sigma_z+t b_n sigma_x) and E=E(0). Direct differentiation gives

    E=diag(exp(u),exp(-u)),
    E_t=b_n sinh(u)/u sigma_x,
    E_tt=b_n^2 [sinh(u)/u I
                      +(u cosh(u)-sinh(u))/u^2 sigma_z].

Conjugation by E^{-1/2} reduces the last two terms to diag(-C_n(s),C_n(s)), where

    C_n(s)=b_n^2 [sinh(2s a_n)-2s a_n]/(2s^2 a_n^2).

The scalar shift exp(s c_n) cancels. Therefore

    kappa_tt(s,0) >= sup_n C_n(s).

For fixed s>0 and a_n tending to infinity,

    C_n(s) ~ b_n^2 exp(2s a_n)/(4s^2 a_n^2).

Consequently a successful MGF ball of radius R>0 requires

    sup_n |b_n| exp(s a_n)/a_n < infinity  for every 0<s<R,

and hence

    R <= r_* := liminf_n (-log |b_n|)/a_n,

with -log 0=+infinity. Indeed, if s>r_* there is a subsequence with -log|b_n| <= (s-epsilon)a_n, making the displayed expression divergent. This proves the ceiling and shows that all-exponential noise requires r_*=infinity. It proves neither sufficiency nor a boundary requirement at s=R.

## Endpoint stress test and dependence

For 0<R<infinity, take a_n=n and b_n=exp(-Rn+sqrt(n)). Then r_*=R, while

    sup_n C_n(R)=infinity.

For every s<R the supremum is finite, but it diverges as s increases to R. An endpoint construction claiming finiteness only on the open ball may accommodate this through kappa_tt(s,0) tending to infinity. A proof cannot replace the endpoint by a uniform bound at R.

Independent coordinates do not suffice for this stress sequence when nu has an open MGF neighborhood: independence makes kappa_tt(s,0)=Var(Z_2), a finite constant. The inequalities for all s<R would then imply a finite upper bound at R by monotone limit, contradicting the example. Thus dependence is essential for some endpoint cases. An independent product-noise construction establishes only a narrower result unless it separately handles this failure.

## Plausible sufficiency, still unproved at this stage

For R<r_*, exponential decay with an exponent above R controls the tail blocks. A common finite-slope density could plausibly handle those blocks, followed by convolution with a regularizer for finitely many remaining bounded blocks. The proof must control all x and all tail blocks simultaneously and preserve the requested MGF domain.

For R=r_* or r_*=infinity, the plausible mechanism is dependent noise with a radial or otherwise slowly changing log-density. The allowed logarithmic gradient approaches the boundary of the tilt domain, and its curvature is selected small enough to compensate the finite but growing envelope sup_n C_n(s). The density's finite-radius tails must also dominate subexponential defects such as exp(sqrt(a_n)) in the endpoint example. A local approximation by a tilted exponential, without a uniform treatment of blocks whose a_n exceeds the local spatial scale, is not a proof.

An alternative countable-convolution construction would require actual summable exponential-moment costs of the individual regularizers. Existence for every finite truncation does not supply tightness, a common regularizer, or all-exponential moment control.

## Topology, normalization, and energy shifts

If positive normalized block POVMs M_n with one common nu are actually constructed, define

    M(E)=direct_sum_n M_n(E).

Each block effect is between 0 and I. This defines a bounded effect on H and gives normalization M(R^2)=I. For disjoint E_j, dominated convergence in the square-summable block coordinates proves strong countable additivity. Bounded integrals give the required transform blockwise and then on H. No norm convergence of infinite densities is needed. If a pointwise direct-sum density is claimed, boundedness of that density must be proved separately.

When A is unbounded, the characteristic function generally cannot be norm continuous at zero: nu_hat(s,0) is nonzero near zero, so norm continuity of nu_hat(s,0) exp(isA) would imply norm continuity of exp(isA), forcing A bounded. Strong continuity is the appropriate statement.

The shifts c_n translate the first report in each block and do not affect noise existence or the normalized transverse bounds. They can make A positive or give compact resolvent only under additional growth choices. They can greatly change physical energy costs. Neither the threshold nor exact representability implies a uniform finite-energy realization, a finite block cutoff, a measurement information gain, or a preparation/reset advantage.

## Preliminary status

The necessary threshold is reconstructed. The candidate endpoint and all-exponential sufficiency remain open pending a complete global common-noise proof. This note is not an endorsement of those directions and is not external verification.
