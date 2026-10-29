# Consistent empirical teacher with a support-safe escape

30 October 2026. Root's new construction, **PROPOSED pending whole challenge**.
This is the capital-first pair's next operation, building on the accepted
asymmetric compiler while challenging its central input suppliers. No new source,
model, solver or benchmark instance has been run. All frozen inputs stay intact.

## 1. Strong ordinary mechanism and the remaining interface

Liu--Moitra, arXiv:2411.07536v1, Section4.1, Claim4.1 and Lemma4.6, already
construct a consistent lazy empirical teacher supplying exact PDF/sample access
from conditional samples. I read that complete subsection from the cached primary
source. Its tree, empirical categorical rows and positivity mechanism are ordinary
prior machinery, not discoveries here. The substantive additional interface is
that our original Q can have zero-probability prefixes, and its conditional service
is permitted only at positive-Q prefixes. Simply adding local floors and querying
their new descendants would violate that contract.

The construction below repairs that interface. A small global uniform component
pays the remaining logarithmic cost. It removes the original VALUE supplier if
the full composition survives review. It does not make real resets or conditional
sampling physically free.

## 2. A conceptual tree, implemented only where needed

Fix rational 0<rho<=1/(10O), 0<alpha<=1/4 and failure probability beta. At every
positive-Q prefix h assign, conceptually and independently, m iid draws from the
next-token Q distribution. Let e_h(o) be the empirical fractions. Choose

    m >= [T log O + log(2T O/beta)]/(2 rho^2)

with a larger fixed constant if needed. A union bound over at most T O^T token
events makes ALL |e_h(o)-Q(o|h)|<=rho with probability>=1-beta. This conceptual
tree is never materialized; a visited active node draws its batch once and caches
the rational row. Conditional-on-past concentration, or equivalently independent
preassigned batches, justifies lazy adaptive visits.

Define a full-support distribution Qbar as follows. Initially its path is active.
At an active node h its token probabilities are

    qbar(o|h) = (e_h(o)+rho)/(1+O rho).

If e_h(o)=0 and that edge is followed, the path becomes permanently inactive;
all remaining tokens are uniform and no further original-Q call occurs. If the
edge count is positive, its prefix is known positive-Q from an actual observed
sample. Thus every original-Q query is authorized by support, even when Q has
zeros. The active/inactive status of a specified prefix is determined by its
ancestors in this fixed cached tree. No new random row is substituted on revisits.

At inactive nodes there is no empirical batch. At unvisited active nodes generate
the batch when first needed. Every sample or value query visits <=T active nodes.
Rational products have O(T[log m + bits(rho)+log O]) bits. The exact row and prefix
probabilities of Qbar are therefore available with polynomial sample/arithmetic
work per lazily visited node. This exactness concerns the acquired empirical law,
not the unknown Q probabilities.

Let G be the full strings whose Qbar path never takes a zero-count edge. On the
global accuracy event, at every active node

    e_h(o)+rho >= Q(o|h).

Consequently, for x in G,

    Qbar(x) >= Q(x)/(1+O rho)^T.                         (2.1)

Also Q(G^c)<=T O rho: conditional on reaching an active node under Q, every
zero-count edge has true probability<=rho, and union over T steps. This is a
bound on the union of those edges, not an assumed uniform conditional-P guarantee.

## 3. Add one global, rather than recursively queried, uniform component

Put U=Uniform([O]^T) and

    R = (1-alpha) Qbar + alpha U.

For any prefix h, its prefix likelihood is an exact rational combination of
Qbar(h) and O^(-|h|). Its next-token row is computed by ratios of those positive
prefix likelihoods. A conditional R sample can use those exact rational rows.
Alternatively draw the latent mixture component from its prefix posterior.
Either implementation touches only cached Qbar rows, and hence only positive-Q
original service nodes. R has full support, exact rational VALUE access and
conditional sample access. Its bit complexity is polynomial. It can be supplied
to the accepted asymmetric compiler without pretending it is low rank.

Let d=D(P||Q)<infinity, not assumed known. Pinsker gives

    P(G^c) <= T O rho + sqrt(d/2).

For x in G, log[Q(x)/R(x)] <= T log(1+O rho)-log(1-alpha)
<=T O rho+2alpha. For all x, since Q(x)<=1 and R(x)>=alpha O^(-T),

    log[Q(x)/R(x)] <= B0 := T log O + log(1/alpha).

Thus the proposed complete interface bound is

    D(P||R) <= d + T O rho + 2alpha
                 +(T O rho + sqrt(d/2)) B0.             (3.1)

Negative log ratios need no lower bound: these are upper bounds inside an exact
KL identity. The escape law need not resemble Q after a zero-count edge; its
Q mass and then P mass are charged explicitly. This avoids an invalid query of
Q at a floor-created prefix and avoids assuming multiplicative approximation on
every original Q edge.

## 4. Fixed-tau consequence and polynomial cost

Run the accepted compiler at fixed tau, with x=A/tau and its resource schedule.
Use rho=alpha=x^(-10000), allowing rational downward dyadic rounding by at most
two. Then m is a fixed polynomial in x and T,log O,log(1/beta). Each VALUE or
sampling call of the accepted compiler costs a polynomial number of original
conditional samples and bits. Although the exponents are enormous, there is no
exponential-in-T sample precision hidden here. A demanded exact empirical VALUE
has a rational representation rather than a fresh estimation to the demanded
absolute error.

The accepted theorem's clean acquisition condition is D(P||R)<=x^(-4096).
For x sufficiently large (as its A>=1000 ensures), d<=x^(-10000) suffices for
(3.1): B0 <=10001 x^2, so d+2TO rho+2alpha+sqrt(d/2)B0 is well below x^(-4096).
Constants and dyadic rounding will be checked during challenge, not hidden as a
practical noise range. With that promise, the accepted fixed-tau compiler yields
D(P||P_hat)<=D(P||R)+40T(B+1)tau, for the accepted clipping bound B.

For nonzero d, choosing a tau on the scale A d^(1/10000) would give a weaker but
horizon-independent Holder guarantee. No supplied d is needed if the candidate
selection below works. Rank(P)<=r remains a promise. Source and conditional-Q
acquisition, including every returned future string, remain paid real inputs.

## 5. Removing a supplied KL upper bound by ordinary candidate selection

This is a proposed further composition, not a new model-selection principle.
Choose a dyadic tau grid from tau_min (a polynomially small function of epsilon/A)
up to tau_max=1/(100A). At every grid point run the fixed-tau operation with its
own empirical teacher and fixed known work caps. On any detectable invalid
geometry/algorithmic failure return a uniform candidate. Every candidate is an
actual rational teacher-free autoregressive law even when its approximation
promise fails. Work bounds do not assume that a small-tau candidate is accurate.

After freezing all K candidates, draw an independent P holdout. For each pair
define the Yatracos set A_ij={x:p_i(x)>p_j(x)}, using exact products of the finite
models' rational output token probabilities. Estimate P(A_ij) from the holdout
and p_k(A_ij) from independent samples of each candidate. With
O(epsilon^(-2) log(K^3/beta)) samples per law, Hoeffding uniformly pays those
finitely many set probabilities. Let candidate k minimize

    score(k)=max_(i,j) |P_emp(A_ij)-p_k_emp(A_ij)|.

If all empirical errors are<=e and k* has minimum TV error v*, then
score(k*)<=v*+2e. For the selected k, the exact discrepancy on A_(k,k*) is
<=score(k)+2e<=v*+4e. Since A_(k,k*) realizes TV(p_k,p_k*),

    TV(P,p_k) <= 3 v* + 4e.                            (5.1)

Indeed p_k*-versus-P on that set costs v*, and triangle adds another v*.
All density evaluations and candidate samples are teacher-free; their actual
solver, rational sampling and evaluation work is charged. The finite score
selection uses no unknown entropy, P likelihood, exact TV oracle or KL bound.

The best grid point satisfying d<=x^(-10000), if one exists, can then be chosen
up to a constant TV factor. If no point can qualify, a stated global Holder
bound must be made vacuous at that endpoint; deriving its explicit constants and
confidence-adjusted A is a remaining task. This note does not yet assert the
Delta-oblivious theorem as accepted.

## 6. Distinct root alternative preserved

Before reading the full ordinary PDF primitive, root derived a changing-floor
operation. It remains a potentially useful alternative, not the preferred first
supplier: outgoing clip=max(z,theta mu_t), theta=a tau; incoming child reference
max(w,theta mu_parent(o,.)/pi_o,theta mu_child). This dominates parentclip/pi,
preserves token KL, and has mass<=1+v+Ob+(v+theta)/a+theta. Relative-density
conditional-sample estimates after rare-transition cutoffs and high-ratio
feature masking could then replace absolute precision. That more complicated
route needs whole challenge and might reduce the smoothing loss; it is not used
to promote (3.1) or hide the stronger ordinary lazy-tree construction.

## Status

The central new claim being tested is the support-safe empirical-teacher/KL
interface and its full composition, not the existing empirical tree or Scheffe
selection. T and A independently challenge it. No usable moderate-noise learner,
large model distillation result, physical reset capability, practical improvement
or historical priority is claimed. The original value-oracle theorem remains
accepted at its original exact contract; this note does not retroactively change it.
