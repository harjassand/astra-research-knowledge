# A minimum-weight receiver for a nonfactorizing local fault expansion

29 October 2026. Derived extension of the ESTABLISHED Han et al.
arXiv2609.20537v1 AppendixC receiver argument. Independent challenge
pending. No generic qLDPC coherent threshold novelty is claimed.

## Exact assumptions

Let V be finite fault labels, each with declared source support X_v of
size<=q. Each physical source qubit belongs to at most D such supports.
Here D is the TOTAL incidence in this experiment, not incidence per unit
time. The stabilizer code has n qubits, distance d, and check-connectivity
graph Gamma of maximum degree Delta. Two qubits in one check are adjacent.

Let E encode into the code sector. Let G_M be maps from logical input to
the final physical source, with sum_M G_M an actual CPTP noise process,
and suppose

    ||sum_(M superset R) G_M||_diamond <= epsilon^|R|.     (1)

Assume an ENCODED-SUPPORT property: with S_M=union_(v in M) X_v,

    G_M(X) = sum_(P,Q supported on S_M) c_(P,Q,M)
                                  P E(X) Q^dagger.        (2)

The scalar coefficients can be signed/complex, correlated across M,
and need not come from independent local environments. No CP property of
G_M is required. Environment outputs have been traced out. This assumption
does not follow from (1) alone. Interleaved nominal Pauli correction which
spreads the common error is not granted by (2).

After this noise, perform PERFECT complete syndrome measurement and a
fixed minimum-weight Pauli correction C_s for each valid syndrome s,
then decode. Denote the resulting actual logical channel Lambda. The
decoder and extraction implementation costs and faults are not included.

## Forced/forbidden resummation replaces a product-channel premise

Write R_s for the CP trace-nonincreasing syndrome-s corrected decoder,
and R_Omega=sum_(s in Omega)R_s; ||R_Omega||_diamond<=1 for ANY syndrome
subset Omega. For each M,s consider the components of

    Gamma[S_M union support(C_s)].

The exact Pauli/minimum-weight argument in Han AppendixC.2 gives:

* If all components have size<d, R_s G_M is scalar times identity.
* If R_s G_M is nonzero, each component K has
  |K intersect S_M|>=|K|/2.

For completeness, expand (2) in Pauli pairs P,Q of syndrome s. On any
component K, C_s^dagger P has zero syndrome separately because no check
meets two components. If |K|<d this restriction is a stabilizer. On a
general K, replacing C_s on K by P preserves the syndrome; minimum weight
then gives wt(C_s restricted K)<=wt(P restricted K). Since K is covered
by S_M and C_s, the density inequality follows. Terms with no surviving
Pauli pair vanish. This reasoning uses declared S_M, so it also holds
when the map actually has smaller support.

Let Jset={K_1,...,K_r} be a nonempty family of connected subsets of Gamma,
each size>=d, pairwise disjoint and nonadjacent. Put J=union K_i, and
let boundary(J) be its external neighboring vertices. Define W_Jset to
be the sum of R_s G_M over terms for which EVERY K_i is a component of
Gamma[S_M union support(C_s)]. Other large components are allowed.

For a physical subset A let V_A={v:X_v meets A}. Set

    T = M intersect V_J,
    Z(T,J) = V_(J union boundary(J)) minus T.

Allowed T are subsets of V_J minus V_boundary(J). Fix such T. The needed
syndromes are the subset Omega_J(T) for which C_s covers J minus S_T and
avoids boundary(J). These conditions do NOT consult the outside faults.
Exactly as a finite rearrangement of maps,

    W_Jset = sum_T R_(Omega_J(T)) H(T,Z(T,J)),             (3)
    H(T,Z) = sum_(M:T subset M, M intersect Z=empty) G_M.

No commutation of disjoint error maps is used. The identity in PROOF.md
Section1, applied to (1), gives

    ||H(T,Z)|| <= epsilon^|T| (1+epsilon)^|Z|.            (4)

Whenever the corresponding term is nonzero, the density inequality and
q|T|>=|J intersect S_T| imply |T|>=|J|/(2q). Also

    |V_J|<=D|J|,
    |Z|<=D(1+Delta)|J|.

For 0<=epsilon<=1, there are at most2^(D|J|) choices of T, hence

    ||W_Jset|| <= L^|J|,
    L=2^D (1+epsilon)^[D(1+Delta)] epsilon^[1/(2q)].       (5)

This is the price for retaining ONLY an inclusive coherent norm
condition. Han's local-product channel model has stronger hybrid bounds
and therefore avoids this extra forbidden-boundary factor. That established
incumbent is strictly better when its input model applies.

## Logical error, without fictitious probabilities

Let C_d be all connected qubit sets of size>=d, and

    Xi = sum_(K in C_d) L^|K|.

For each M,s apply ordinary finite inclusion-exclusion to the event that
there is at least one large component. After summing maps,

    Lambda - c id =
      sum_(nonempty compatible Jset) (-1)^(|Jset|+1) W_Jset

for a scalar c, because the complementary small terms are scalar identity.
Thus (5) and dropping compatibility give

    ||Lambda-c id||_diamond
       <= product_(K in C_d)(1+L^|K|)-1 <= exp(Xi)-1.

Since Lambda is trace preserving, |1-c|<=exp(Xi)-1, and therefore

    ||Lambda-id||_diamond <= 2[exp(Xi)-1].                (6)

As usual cap the right side at2. This is a correctness bound, unlike the
Pauliization-only theorem in PROOF.md. It concerns a PERFECT final global
minimum-weight decoder under (1),(2), not an autonomous decoder.

Using the ordinary connected-set counting bound and the rational overpay
chi=max{1,3Delta}, if chi L<1 then

    Xi <= (n/chi) (chi L)^d/(1-chi L).                   (7)

For fixed q,D,Delta, a sufficiently small CONSTANT epsilon gives
exponential suppression in distance once d>=c log n and chi L<exp(-1/c).
Nothing in this statement makes D independent of an arbitrarily long
unrecovered history. Replacing D by its instantaneous value would be false.

## Physical Gaussian-noise specialization: a finite storage window

Here is a concrete sufficient model for the inputs, not a Davies or
Markov approximation. On a chosen finite interval [0,T], let the nominal
joint source/clock/environment Hamiltonian be

    H_0(t)=sum_s Pi_s tensor H_s(t),

where source checks Pi_s are those of this code, and the entire nominal
environment acts as identity on the logical algebra. The initial source
is E(X), with a fixed environment state independent of X. Add noise

    alpha sum_j A_j(t) tensor B_j(t).

Each Hermitian bounded A_j has norm<=1 and is supported on a FIXED source
set X_j of size<=q (it may also act on clocks); at most D sets meet any
source qubit. Noise baths j are independent centered Gaussian baths,
factorized from the initial source/nominal environment. Their bounded
finite-square correlations C_j(t,s) obey Wick. Joint dynamics and its
Wick expansion must be well defined, as in the frozen Gaussian packet.

Use ONE slot per seed j over this entire storage window. Phi[K] is the
PHYSICAL experiment with only couplings j in K turned on, with identical
nominal dynamics. Define G_M by Mobius inversion of Phi[K] and trace out
the full environment. Then sum G_M=Phi[V]. All source Pauli labels in a
term of G_M come from seeds in M. Evolution under H_0 preserves these
labels, merely adding syndrome-dependent environment coefficients. On
the initial code sector these coefficients are independent of the logical
input. Expanding and tracing therefore proves (2). It does not assume
that A_j(t) in the full interaction picture remains spatially local.

For the inclusive sum B(R), expand around the physical process with noise
baths j in R fully disconnected. The Gaussian correlation-variation
resummation of the frozen b_conventional/clock_memory packet retains all
other bath/nominal evolution as exact joint unitaries of norm1. Inclusion-
exclusion cancels every selected pair family failing to touch all seeds
in R. Crucially a Wick pair belongs to ONE bath j, and here a whole j is
ONE slot, so covering r=|R| marked seeds requires at least r selected
pairs, rather than ceil(r/2) for multiple time slots of a common bath.

With the deliberately loose constant8 put

    eta=8alpha^2 sup_j integral_[0,T]^2 |C_j(t,s)| dt ds.

The total selected-pair mass incident on r marked seeds is at most r eta.
All reference propagators and endpoint operators have norm<=1, uniformly
with inert references. For eta<=1, the same exponential-series argument
but with k>=r gives

    ||B(R)||_diamond <= sum_(k>=r) (r eta)^k/k!
                       <= (e eta)^r.                    (8)

Indeed multiply by z^(k-r), z=1/eta>=1, and sum exp(r eta z)z^-r.
Thus take epsilon=e eta<=1 in (1). For stationary C_j with
M_0=sup_j integral_R |C_j(u)|du finite,

    eta<=8alpha^2 T M_0.

Equations(6)--(8) give an explicit code-capacity receiver bound for this
non-Markovian physical storage window. They do not require positive
data-fault flags, a newly Gaussian conditional bath each round, spectral
resolution of a many-body Hamiltonian, or bath resets DURING this one
window. If correlations are only bounded on the finite square, use that
actual double integral instead of claiming M_0 exists.

The environmental state AFTER a window may be correlated with data.
Therefore applying this factorized-initial-bath specialization anew to
successive windows is NOT justified. A multi-time admission for faulty
extraction, recovery and bath reuse is still required. This is not yet a
fixed-noise arbitrary-time physical memory, a useful-rate device, or a
bounded-density3D apparatus.

## Comparison and provenance

The static component, syndrome-selector and MW density arguments are
adopted from Han et al. https://arxiv.org/html/2609.20537v1 AppendixC.
Their actual input is a bounded-depth local unitary/CPTP circuit. Formula
(4) states the explicit extra cost for replacing that product/hybrid
model by a consistent inclusive norm alone. The Gaussian resummation input
is Liu--Lu https://arxiv.org/html/2408.04009v3 Lemma1; non-Markovian Gaussian
noise FT is established prior (Ng--Preskill arXiv0810.4953). No priority
claim is made for combining these methods. The scientific contribution
claimed here is the displayed derivation at its exact assumptions, pending
independent challenge, not a claim to have discovered coherent FT itself.
