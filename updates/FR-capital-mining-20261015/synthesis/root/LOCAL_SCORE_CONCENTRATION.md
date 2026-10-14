# An unconditional concentration bound for condition-matched local exchange scores

Root derivation, 15 October 2026. The independent quantum-information worker
derived the pair/triple compiler and conditional component bound; the root
supplied the random-label bounded-difference step below. Both reconstructed the
combined argument. This is same-team analytic work, not external validation.

## Exact scope

Each arm prepares B independent batches of N iid labeled modules. Conditional
on the full label vector, modules are independent and their joint RSE state
depends only on their observed condition c. All gate components, continuation
channels and readouts act locally to their declared components and introduce
no shared noise. Each endpoint score is in [0,1]. The bath-safe joint routing,
reference tracking, matched continuation and readout assumptions of the source
remain required. None is inferred from this sampling proof.

Within a condition class of size k>=2, use disjoint swaps for even k and one
3-cycle plus disjoint swaps for odd k. Singletons remain untouched. Every
non-singleton moves and has exactly the source's conditional product marginal.
For each condition, denote the native and routed local score means by o_c,d_c
in [0,1]. These values need not be known to use the bound.

The tested target is the actual unconditional *finite-batch* routing score,
not the ideal infinite-reservoir score. Systematic errors and any inference
from finite batch to ideal decorrelation are separate from sampling error.

## Conditional measurement fluctuations

For fixed labels the disjoint components are independent. A component of size
g in {1,2,3} has total score in [0,g], even when its endpoints are correlated.
Write S for the score averaged over all BN endpoints. Hoeffding's exponential
bound, conditional on the labels, gives

    E[exp(lambda (S-E[S|labels])) | labels]
      <= exp(lambda^2 sum_components g^2 / (8 B^2 N^2))
      <= exp(3 lambda^2/(8BN)).

The second inequality uses g^2<=3g and sum g=BN. Independent endpoints are
never assumed. More precise realized component counts improve this term.

## Random-label fluctuations

For one batch the conditional mean is

    mu(labels)= (1/N) sum_c h_c(k_c),
    h_c(0)=0, h_c(1)=o_c, h_c(k)=k d_c for k>=2.

Its increment on adding one member to a class is

    h_c(1)-h_c(0)=o_c in [0,1],
    h_c(2)-h_c(1)=2d_c-o_c in [-1,2],
    h_c(k+1)-h_c(k)=d_c in [0,1] for k>=2.

Changing one label removes one member from a class and adds one to another.
Therefore it changes the conditional batch mean by at most 3/N. This constant
is attainable with two classes initially of sizes2 and1: take native/routed
means (1,0) and (0,1), and move one member from the former to the latter.

The B-batch conditional mean, as a function of BN independent labels, has
bounded differences 3/(BN). The Doob-martingale exponential bound gives

    E[exp(lambda(E[S|labels]-E S))] <= exp(9 lambda^2/(8BN)).

For completeness, both exponential bounds use only the elementary bounded
variable lemma log E exp(lambda(Z-E Z)) <=lambda^2(b-a)^2/8 for Z in[a,b].
To prove it, twice differentiate the log moment-generating function; its
second derivative is the variance under exponential tilting, at most
(b-a)^2/4. Integrate twice from zero. The label bound applies that lemma to
Doob increments, each of whose conditional range is at most the corresponding
bounded difference. Thus no unexplained concentration theorem is a premise.

## Combined result

Condition first on labels and then average the two exponential bounds:

    E exp(lambda(S-E S)) <= exp(12 lambda^2/(8BN)).

Chernoff optimization for both signs yields

    Pr(|S-E S|>=r) <= 2 exp(-BN r^2/6).

For four predeclared arms, a union bound gives the simultaneous per-arm radius

    r4 = sqrt(6 log(8/delta)/(BN)).

Each two-arm contrast has radius2r4. One can use the smaller of this and the
source's independent-batch radius sqrt(log(8/delta)/(2B)); the new bound is
smaller when N>12. With B=4000,N=32,delta=.05, the new per-arm radius is about
0.015424 versus .025187 for the batch-only bound. This is a sufficient analytic
bound under stronger explicit local-component assumptions. It is neither a
measured shot requirement nor a demonstrated advantage over other assays.

The number of transpositions per class is ceil(k/2), minimal among
derangements: a permutation with no fixed points has at most floor(k/2)
cycles, and its minimum transposition count is k minus its cycle count.
This reduces gate count relative to one long cycle without changing the
source's tagged mean. Bath action, parallel hardware, resets, reference
storage and acquisition costs remain charged.

## Limits and falsifiers

A joint cross-component continuation, common detector or gate noise, dependent
source preparations, unmodeled adaptive policy selection, or nonlocal score
can invalidate this factorization. Treat independent whole batches as the
sampling units until the stronger locality/independence contract is justified.
The actual tested score includes reference assignment and can change purely
because reference partners changed; the separate reference-pairing
counterexample must accompany any causal interpretation.
