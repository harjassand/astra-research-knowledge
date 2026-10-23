# PRO3 continuation seed — 22 October 2026

This is the latest owned scientific state in this return. It supersedes the
tentative future-question paragraph of SAFE_LOCAL_THEOREM.md Section 8 while
preserving that already reviewed file byte for byte. Ownership remains with
Astra PRO3; Max integrates and the evaluator assesses research-system evidence.

## Current question

Determine the sharp proposal-start forward-KL mixing coefficient for the fixed
tempered local/global family when

    0 < eta <= theta_K := 1-alpha exp(-K)/2.

Is it K for every positive eta, or can a valid positive-eta family force a larger
coefficient or a scale for which epsilon log T is unbounded? The current
theta_K is a sufficient threshold of the proof, not an established transition.

## Exact active contract

Finite labelled space; strictly positive equivalent probabilities pi,q; its
size may grow across the supremum. A fixed symmetric stochastic Q is public
and target independent. It may have zeros and need not be irreducible.
K>0, alpha in (0,1) and eta in (0,1] are fixed over the relevant class.
The supplied population certificate is D(pi||q)<=K, not an empirical estimate.
G is ordinary independence MH from q. With beta=1-alpha,

    C_eta=(I+alpha G+beta L_eta)/2,       X_0~q,

and L_eta proposes from Q and accepts with

    min(1,(q(y)/q(x))^eta)
      * min(1,(pi(y)/pi(x))*(q(x)/q(y))^eta).

Both q and local proposals are sampleable, q ratios and the unnormalized target
are evaluable. The target normalizer is unknown and cancels. The sampler is
invariant to common raw-target rescaling. Every target query and local proposal
is counted. Cached values may be reused. Eta, Q and mixture probabilities never
change after observations. The construction is ordinary factorized/delayed
acceptance, not a newly invented acceptance algorithm.

Define R_eta(n)=sup TV(q C_eta^n,pi) and T_eta(epsilon) as the corresponding
worst-case first deterministic sufficient time. All upper estimates must be
uniform over this precise class. Individual finite-chain convergence is weaker.

## Established this checkpoint

1. Both received candidate-only optional-prefix impossibility proofs are
   accepted once, within their complete public-q/Q, unknown-normalizer,
   same-positive-K null-family, bounded-fallback contract. That endpoint is
   closed. Richer access is not universally ruled out.
2. On arbitrary measurable spaces, fixed pi-reversible L with a common
   finite measure bound qL<=Lambda q satisfies
   log(n) sup TV(qC^n,pi)->K and epsilon log T(epsilon)->K.
   A q-reversible proposal corrected to pi gives Lambda=2. No reverse KL or
   specially scheduled global prefix is needed.
3. In the above finite tempered family, every fixed eta>0 has zero uniform
   floor and finite uniform time at every positive error.
4. For eta>theta_K, the sharp coefficient is K. At K=1,alpha=1/2 this means
   eta>0.9080301397; eta=0.95 is a legitimate weaker fixed screen.
5. For any eta in (0,1), writing kappa=-log theta_K and ell=-log eta, every
   0<zeta<min(1,kappa/ell) has the sufficient bounds
   R_eta(n)=O(log(n)^(-zeta)) and
   T_eta(epsilon)<=exp(O(epsilon^(-1/zeta))).
   This is not a matching lower rate or the sharp unresolved coefficient.
6. Pure IMH already has coefficient K. The finite trap repair is not a
   practical speedup over it, and exact memoized counterexamples rule out
   universal finite-time hybrid dominance.

## Proof capital to reuse

SAFE_LOCAL_THEOREM.md contains the first-state-hitting submeasure construction,
the general initial-law anchored bound for mu<=Aq, uniform growing-time choices,
positive two-state lower family, and explicit inversion. The accepted binomial
pointwise near-harmonicity lemma is reused from the prior owner source.

TEMPERED_SCREEN.md proves qL_eta(A)<=q(A)+q(A)^eta. The layer-cake/Jensen
transport lemma gives qC_eta^j(A)<=D_j q(A)^(eta^j), where
D_j<=(3/2)^(1/(1-eta)). It propagates unconditioned first-hit submeasures against
pi. A bounded-density comparison retains both its truncation error and its
extra low-set mass. None of these proof measures is sampled by the algorithm.

For the sharp interval the current proof chooses s=ceil(v log log n),
1/kappa<v<1/ell, h=log(n)^(-2), V=exp(log(n)^z), with
v ell<z<1. The conflict between those inequalities is the present bottleneck.
It could be an artifact of repeatedly applying a coarse setwise bound.

## Invalidated shortcuts and comparison obligations

- qL^t<=(t+1)q is false even for a three-state q-reversible-proposal MH kernel.
  The exact counterexample is in reviews/safeguarded_mechanism_checks.json.
- For every eta<1 a two-state admitted family has unbounded qL_eta(A)/q(A).
  This defeats fixed linear domination, not the tempered sampler: zero floor
  was proved by the weaker power method.
- A worse sufficient estimate is not a lower bound. Do not call theta_K sharp.
- Do not insert a random stopping time or expected global count into a
  deterministic-prefix result.
- Off-diagonal/stationary comparisons do not imply finite-time TV ordering.
- Pure IMH, ordinary local MH, full caching, q evaluations and all proposals
  remain legitimate comparators/costs. Full disclosure of a finite target table
  permits direct discrete sampling and would change the information contract.

## Precise next action selected by the owner

Try to control cumulative transport after the first high state without losing
the power exponent eta at every deterministic step. A useful revised upper
proof must preserve all return paths and uniformity as support grows.
In parallel only where useful, seek a fixed symmetric-Q multiscale lower
construction whose capture and retention survive BOTH acceptance factors.
A two-state divergence in qL/q alone is already known and is insufficient.
The first decisive bound or valid adverse family should determine continuation.

Do not restart the closed J>K search, fixed-prefix theorem, or uniform-null
fraction question. No new application search or favorable galaxy selection
follows from this checkpoint. Closed R3/anMC, B3, GUIDE and other protected
operations remain in their scopes.

## Source and status

Main proof: SAFE_LOCAL_THEOREM.md, SHA256
ad80cb6a4ec919585182ff0fc5210da6643bd9a3378264dace262b6715e9d3da.
Extension: TEMPERED_SCREEN.md, SHA256
fa0d12398f3b2bbcaa417a591ab70b8ea33e76c4a940b6976c76018fe833f06c.
Both have independent actual-source bindings in reviews/. These are internal
correctness checks, not historical priority or external mathematical acceptance.
The full original owner ZIP and received prefix sources are included unchanged.
Read README.md for verification/replay and PRESERVATION.md for older source.

The mission continues after this substantive handoff. There is no background
job or unreported ongoing empirical computation.
