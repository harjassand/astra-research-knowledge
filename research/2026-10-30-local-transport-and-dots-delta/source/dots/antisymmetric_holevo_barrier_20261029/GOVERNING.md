# Antisymmetric data-hiding reservoirs have an actual-Holevo-loss barrier

2026-10-29. Scoped analytic negative result for a proposed mechanism; not an N371 counterexample or general theorem. No historical novelty assertion. This branch is stopped after this note; no reservoir refinements are claimed.

## Precise result
Let S be a Haar-random r-dimensional subspace of C^d, with 1<=r<d. For 1<=k<=r define

 rho_(S,k)=P_(wedge^k S)/binom(r,k), on wedge^k C^d.

The ensemble is genuinely mixed unless k=r. Its average is I/binom(d,k), by unitary invariance and irreducibility of the exterior-power representation. All conditional states have entropy log binom(r,k), so the ACTUAL ensemble Holevo information is

 chi_k = log[binom(d,k)/binom(r,k)].                         (1)

For even k, canonical antisymmetric splitting into two k/2-particle groups is an isometric full-domain channel whose two marginals on these letters both equal rho_(S,k/2). Its actual loss is

 delta_k=chi_k-chi_(k/2) >= chi_k/2.                       (2)

Indeed chi_0=0 and

 chi_(j+1)-chi_j=log[(d-j)/(r-j)]

is nondecreasing in j: its ratio to the previous increment's argument is >1 when d>r. Thus chi_k is convex on the integers and chi_(k/2)<=chi_k/2.

Replacement by the ensemble mean is one EB channel. In fact its trace error is exactly

 T(rho_(S,k),I/binom(d,k))
 =1-binom(r,k)/binom(d,k)=1-exp(-chi_k)
 <=chi_k<=2 delta_k.                                    (3)

Pinsker also gives the familiar e<=sqrt(delta_k), but (3) is stronger for small loss. Thus this whole exterior-power covariance mechanism cannot exhibit delta->0 with EB trace error bounded away from zero.

## Arbitrary weighted transient reservoirs
Take distinct EVEN copy counts k_j<=r with orthogonal input sectors wedge^(k_j) C^d and label-independent weights p_j. Include the distinct output sectors wedge^(k_j/2) C^d in the ambient direct sum. Every letter is the block mixture

 rho_S=direct_sum_j p_j rho_(S,k_j).

Dephase the sector flag and apply the splitting isometry in each block. Define arbitrary fixed outputs on unused input sectors to obtain a full-domain channel. Swap acts by a scalar sign on each isometry's image, so the two marginals agree on every input, not only on the promise family. The channel is self-compatible.

Because j->k_j/2 is injective and the weights do not depend on S, the input and output flag entropy cancels exactly:

 chi_in=sum_j p_j chi_(k_j),
 chi_out=sum_j p_j chi_(k_j/2),
 delta>=chi_in/2.

The ONE constant EB channel replacing its input by bar_rho has exact error

 e=sum_j p_j[1-exp(-chi_(k_j))] <=chi_in<=2delta.

No stationarity, bounded dimension, independent output copies, or replacement-mixture decomposition of the physical channel is assumed. Uniform dyadic flags can still make raw broadcasting disturbance small by a boundary shift; the actual Holevo deficit prevents this from being an N371 counterexample. This is specifically a label-independent orthogonal-sector theorem. Label-dependent sector laws or noninjective flag maps are not silently covered.

## Splitting isometry, not a cloning oracle
For an occupation basis vector |I> with |I|=k, set

 V_k|I> = binom(k,k/2)^(-1/2)
           sum_(J subset I, |J|=k/2) sign(J,I\J)|J> tensor |I\J>.

Different I have disjoint supports and each image has norm one. Thus V_k is an isometry. Its two partial traces on the normalized exterior projector for S are the normalized exterior projector of degree k/2 for S, either by direct occupation counting or U(r)-covariance. Swapping its output groups multiplies V_k by (-1)^((k/2)^2), so its density outputs and two marginals are symmetric.

## Classical label is retained, including the usual approximate-Markov temptation
The codimension-one case r=d-1 is obtained by measuring one particle A of the normalized (k+1)-particle antisymmetric state with the covariant rank-one POVM d|psi><psi| dpsi. The outcome psi is CLASSICAL, and the conditional remaining state is

 rho_(psi-perp,k)=P_(wedge^k psi-perp)/binom(d-1,k).

Its actual Holevo information is chi_k=log[d/(d-k)]. Equal-receiver splitting loses log[(d-k/2)/(d-k)], at least chi_k/2. Therefore importing the small-CMI antisymmetric Markov examples does not produce the desired small-deficit equal-receiver classical-label counterexample by this construction. A fixed orthonormal-basis measurement is even less useful: all resulting conditional exterior projectors commute.

The Haar prior may be replaced by a finite exact weighted orbit design. Apply finite-dimensional convexity to the joint tuple of the finitely many exterior projector moments required by the reservoir; the Haar tuple lies in the convex hull, so a finite weighted ensemble reproduces every mean used above exactly. No efficiency claim is made for that finite design.

## Scope and source discipline
The governing N371 entropy-tree and exponent-obstruction sources, N61 copy-ladder proof, and N553 research proof in `producer-workspace/sources` were read. They explicitly do not permit replacing actual Holevo loss by raw broadcasting error. The result here is a decisive failed premise for one natural higher-dimensional extendible/data-hiding mechanism, not a general obstruction to N371, an unrestricted dimension-free residual theorem, or a quantum-reference counterexample disguised as classical X. No LOCC restriction is imposed on the EB comparator.
