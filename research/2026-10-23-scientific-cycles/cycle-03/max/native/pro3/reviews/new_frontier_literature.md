# Proposal-compatible local kernels after the candidate-only stopping obstruction

Contributor: `/root/prefix_literature`. First observed clock: **2026-10-21 16:08:35 UTC**. The parent names this the Cycle 2 allocation dated 20261022; the observed runtime clock is retained rather than altered to match that label.

This note investigates two mechanisms. It does not review or rerun the received optional-prefix impossibility. The owner retains the principal construction and the decision about which question to pursue. Neither mechanism below is claimed to be new, or to improve an actual application.

## Recommendation

The most direct structural continuation is to distinguish **a local proposal reversible for q, subsequently Metropolized to pi**, from the old class of arbitrary pi-reversible local kernels. That distinction is operational, needs no target normalizer, and constrains precisely the proposal-mass transport that caused the old obstruction. It is a plausible place to seek a forward-KL proposal-start theorem without a long prefix. The theorem is **not established by this literature note**.

The alternative is an honest geometric certificate from off-proposal target queries and a known regularity bound. This can make early certification possible, but it also enables strong ordinary rejection sampling. A prefix-only comparison would be too weak in that access model.

### Consolidation after the owner's new construction

During this investigation the owner reported a stronger candidate theorem: for fixed K>0, alpha in (0,1), and a **fixed common Lambda>=1**, restrict the supremum to pi-reversible L satisfying the measure inequality `qL<=Lambda q`. Under only `D(pi||q)<=K`, the candidate conclusion is

`lim_(n->infinity) log(n) sup ||q C^n-pi||_TV = K`,

and the corresponding sharp proposal-start mixing coefficient is K. The owner retains the full constructive proof, including initial escape from very low W and subsequent anchored smoothing. This note does **not** certify that proof. The question now is the precise literature boundary for this condition, rather than whether reference-compatible proposals are a new algorithm.

The word **common** is essential. On any fixed positive finite-state instance, arbitrary L has some finite q-domination constant. Merely assuming instancewise finiteness while permitting that constant to be unbounded in the supremum would restore the original obstructed class. The fixed-Lambda theorem and a q-invariant-proposal construction with universal Lambda=2 avoid that error. The result would concern uniform robustness, not a speedup over ordinary IMH, whose leading coefficient is already K.

## Mechanism A: local proposals compatible with the reference law

### Exact operation and access

Let R be a fixed q-reversible Markov proposal, supplied independently of the target. Define its pi-Metropolis correction by

`L_R(x,dy)=R(x,dy) min(1,W(y)/W(x))` off the diagonal, with rejection on the diagonal.

Then `alpha G+(1-alpha)L_R` is the Metropolis correction of the q-reversible proposal `alpha q+(1-alpha)R`. Its acceptance test needs only the ratio of unnormalized importance weights. The same laziness can be retained.

On a labelled finite or countable space, an ordinary way to build R from public q and target-independent Q is to Metropolize Q to q first. If Q is symmetric, this gives the local acceptance product

`min(1,q(y)/q(x)) min(1,tilde_W(y)/tilde_W(x))`.

Thus the complete local move is a conventional delayed-acceptance MH step for pi, using q as the first-stage surrogate. Every local proposal and every new target evaluation must be counted. An early q-stage rejection need not evaluate the expensive target at y; a passing first stage does.

For Gaussian q, another standard example is a pCN proposal `Y=sqrt(1-rho^2) X+rho Xi`, `Xi~q`, followed by the W-ratio acceptance. Here one q-distributed Gaussian noise draw is consumed by each local proposal. It is therefore not a free alternative to a global q draw under a primitive-draw cost model.

### Why this is a distinct mathematical restriction

For any measurable sets A,B, q-reversibility gives

`integral_B q(dx) R(x,A)=integral_A q(dy) R(y,B)<=q(A)`.

Consequently an initially q-distributed reservoir cannot send a constant fraction of its mass into a q-rare trap in one such proposal. This is an elementary flow constraint, not a proof that the whole MH evolution mixes safely. After MH updates the current law need not be q, and multiple-step transport still needs analysis. In particular, neither reversibility nor this one-step identity proves the desired forward-KL asymptotic coefficient.

This frontier changes the local-kernel class. It must not be described as a consequence for the original arbitrary pi-reversible L. A meaningful claim would state the exact q-compatible proposal hypothesis, derive a uniform q-start bound, and compare it to ordinary IMH at matched target evaluations and proposal costs.

There is an elementary broader bridge to the owner's condition. Any accept/reject kernel L built from proposal R with rejection staying at the current point satisfies, for every measurable A,

`qL(A) <= qR(A)+q(A)`.

Hence **q-invariance** of R already implies `qL<=2q`; q-reversibility is not needed for this domination calculation. It is useful for the scale-free W-ratio acceptance above and for proving pi-reversibility conveniently. More generally, `qR<=lambda_R q` gives `qL<=(lambda_R+1)q`. These one-step inequalities follow by discarding acceptance indicators and bounding rejection probabilities by one; they are not claimed as novel. The nontrivial claim is their combination with a population forward-KL budget to control the full cold-start evolution sharply.

### Closest primary results and limits

**Hairer, Stuart and Vollmer (2014),** *Spectral gaps for a Metropolis–Hastings algorithm in infinite dimensions*, Annals of Applied Probability 24(6), arXiv:1112.1392v4. Primary full text: <https://arxiv.org/html/1112.1392v4>.

Algorithm 1 uses the Gaussian-reference-reversible pCN proposal and likelihood-ratio acceptance. Theorems 2.12 and 2.14 establish dimension-independent Wasserstein contraction, with consequences for L2 and sample-path estimates, under acceptance/drift and global or local log-Lipschitz hypotheses. These are substantial controls beyond a population KL budget. The paper does not provide the proposed KL-only q-start conclusion. Reference-reversible proposals and their dimension-robust usefulness are therefore established; their entropy-only robustness here remains a separate question.

**Banterle, Grazian, Lee and Robert (2015 preprint; 2019 journal),** *Accelerating Metropolis–Hastings algorithms by Delayed Acceptance*, arXiv:1503.00996v2. Primary full text: <https://arxiv.org/html/1503.00996v2>; journal: <https://www.aimsciences.org/article/doi/10.3934/fods.2019005>.

Lemmas 1–2 prove invariance for a product of reciprocal acceptance factors. Remark 1 shows this acceptance is no greater than ordinary MH with the same proposal. Proposition 1 transfers spectral-gap and asymptotic-variance control under a uniform factor condition. Proposition 3 demonstrates loss of geometric ergodicity for a poorly chosen Gaussian surrogate. Thus delayed acceptance alone is no safety theorem. Its ordinary benefit is avoiding expensive later factors after a cheap rejection; fair comparisons must include that cost as well as the reduced movement.

### Strong ordinary comparator

Use pure IMH with the same q, the same target evaluations, and its known proposal-start TV theory. Also compare the q-screened local step to unscreened pi-MH on the same Q when evaluating practical cost. The screened step has smaller off-diagonal probabilities, so a claim of faster transitions solely from introducing the screen would be unsupported. A new uniform theorem could justify safety of composition even when it does not imply speedup.

### Peskun, Tierney and weak-Poincare comparison do not close this initial-law step

**Peskun (1973),** *Optimum Monte-Carlo sampling using Markov chains*, Biometrika 60(3):607–612, DOI <https://doi.org/10.1093/biomet/60.3.607>, gives the classical finite-state efficiency ordering. **Tierney (1998),** *A note on Metropolis–Hastings kernels for general state spaces*, Annals of Applied Probability 8(1):1–9, DOI <https://doi.org/10.1214/aoap/1027961031>, extends it. Primary full text inspected: <https://www2.stat.duke.edu/~scs/Courses/Stat376/Papers/TransdimMCMC/TierneyAAP1998.pdf>.

Tierney Theorem 4 compares asymptotic variances for stationary reversible chains. Proposition 5 says maximal MH for a mixture proposal dominates the mixture of the corresponding maximal MH kernels off diagonal. The following paragraph explicitly warns that evaluating all component proposal densities may cost more than evaluating the selected component alone. Neither is a finite-time proposal-start TV ordering. In the q-reversible construction above all component acceptance ratios agree, so equality of the mixture constructions is immediate; it is not a new stronger Peskun theorem.

**Andrieu, Lee, Power and Wang (2022),** *Comparison of Markov chains via weak Poincare inequalities with application to pseudo-marginal MCMC*, Annals of Statistics 50(6):3592–3618; arXiv:2112.05605v2, 9 August 2022. Primary full text: <https://arxiv.org/html/2112.05605v2>. Theorem 8 bounds L2 convergence through an initial functional Phi(f); Section 2.3 treats IMH. Applying that route directly to initial density `dq/dpi=1/W` can fail because forward KL does not bound its L2 norm or the needed initial functional. The owner's proposed first-hit/density-domination step addresses this missing initial-law control; it is not justified by Dirichlet comparison alone.

Focused searches and these primary sections did not identify the exact forward-KL, q-start, fixed-q-domination theorem or its sharp coefficient K. This is a bounded literature result, **not a historical novelty claim**. Reference-reversible proposals, delayed acceptance, invariant mixtures and their stationary comparisons are prior art. A later novelty assessment must distinguish those operations from the claimed entropy-only uniform cold-start theorem.

### Exact comparison with Kurennoy et al. Theorem 6

**Kurennoy, Yarullin and Reid (2026),** *Metropolis–Hastings Dominates Importance Resampling for Policy Composition*, arXiv:2610.03480v1, 2 October 2026. Primary full text: <https://arxiv.org/html/2610.03480v1>, Appendix B.5, Theorem 6 and its known-proposal/support paragraph.

For an instance-uniform remaining-TV certifier U using N iid proposal responses and recorded weights only, no off-candidate evaluations, the theorem gives

`Pr(U>=v_s)>=(1-s)^N-delta`,
`v_s=s/[s+(1-s)Z]-1+(1-s)^M`,

where M is the fixed IMH candidate budget and delta the confidence failure probability. It can force a nonzero reported error on a constant-weight instance where IMH is exact. The following construction preserves known q and support while altering an unobserved branch's weights.

This theorem does not assume a supplied population KL cap K and does not analyze local kernels satisfying `qL<=Lambda q`. The owner's new construction restricts dynamics and can query local proposals; it does not infer a small remaining error from a benign finite iid pool. The two claims concern different information and guarantees. The separate received stopping obstruction remains closed; it was not rederived or re-reviewed here.

## State-dependent safeguards: a valid tool, not an automatic resolution

**Maire and Vandekerkhove (2022 version),** *Markov Kernels Local Aggregation for Noise Vanishing Distribution Sampling*, arXiv:1806.09000v2. Primary full text: <https://arxiv.org/html/1806.09000v2>.

Algorithm 1 chooses a pi-reversible component P_i with state-dependent probability omega_i(x), runs its proposal, and accepts that move with `min(1,omega_i(y)/omega_i(x))`. Proposition 1 proves reversibility. The effective edge multiplier is `min(omega_i(x),omega_i(y))`. Algorithm 2 folds component selection into the ordinary MH ratio. The paper also exhibits failure of uncorrected state-dependent mixing. These provide legitimate constructions, not a generic finite-time TV improvement theorem.

A local gate that becomes small on very low W could suppress the dangerous initial transport. However, choosing that gate using normalized W silently requires information absent from the old unknown-normalizer contract. A threshold on raw unnormalized weights is not scale-invariant. A data-selected reference scale would create a random, observation-dependent kernel and a correlated initial state; its actual stopped/conditioned law would require a new proof. These costs cannot be removed by citing the reversible construction.

## Mechanism B: certified geometric bounds from real target queries

### A concrete richer access model

Suppose the state space is a known compact metric space, q is evaluable and sampleable, and the unnormalized logweight `f=log tilde_W` has a supplied, valid Lipschitz constant L. Permit counted evaluations of f at a deterministic h-net `z_1,...,z_m`. These are genuine off-proposal target queries, not observations conjured from a q-prefix.

Let `f_min` and `f_max` be the smallest and largest observed values. The covering guarantee yields

`exp(f_min-Lh) <= tilde_W(x) <= exp(f_max+Lh)` for every x.

These inequalities and their ratio are invariant under a common rescaling of the weights. The target normalizer need not be known. The normalized importance weights satisfy the certified bound

`W(x) <= M_cert := exp(f_max-f_min+2Lh)`.

An h-net is the actual extra information that rules out unseen narrow exceptions. It is not implied by a small empirical loss or by having many repeated q candidates.

### The strongest comparator already solves sampling directly

Using `bar_w=exp(f_max+Lh)`, ordinary rejection sampling accepts an iid q draw y with probability `tilde_W(y)/bar_w`. Its accepted output is exactly pi; its expected number of attempts is `bar_w/Z<=M_cert`. This does not require evaluation of Z. Each attempted candidate and any uncached target evaluation is counted, in addition to the m pilot queries and construction of the cover.

On the null pi=q, all observed logweights are constant and `M_cert=exp(2Lh)`. For fixed h this is independent of epsilon; the pilot cost, however, is a covering number and can grow exponentially with dimension. The same information also gives ordinary IMH and a fixed lazy mixture a global minorization bound. Therefore a claim that geometric certification improves only the hybrid prefix misses the stronger ordinary exact sampler available under the same access.

These elementary deductions are not offered as a new rejection-sampling method. They identify a real richer model and its cost boundary. For an unbounded domain, a global Lipschitz bound alone does not provide a finite cover or envelope; a tail bound or separate envelope is additional input.

### Closest primary adaptive method

**Achddou, Lam-Weil, Carpentier and Blanchard (2019),** *A minimax near-optimal algorithm for adaptive rejection sampling*, ALT, PMLR 98:94–126. Primary proceedings: <https://proceedings.mlr.press/v98/achddou19a.html>; full preprint: <https://arxiv.org/html/1810.09390v1>.

NNARS uses exact target evaluations, known Holder regularity on a compact cube, and a positive density lower bound. It constructs computable piecewise-constant proposal envelopes from prior evaluations. Theorem 6 supplies exact sampling and an expected rejection-loss bound near order `n^(1-s/d)` up to logarithms; a matching-order minimax lower result is also developed. This is a stronger ordinary comparator than a fixed global envelope when geometric evaluation information is available. Its assumptions concern regularity of the density, not the logweight formulation above; they should not be interchanged without checking the conversion and constants.

## What would change the research decision

For mechanism A, the decisive step is completion and independent challenge of the owner's q-domination theorem, with fixed common Lambda and full initial-law control. A stationary spectral comparison is insufficient. If valid, the theorem supplies a safe local-kernel design rule without proving any computational advantage. If it fails, the failure should identify the specific uncontrolled transport or smoothing step rather than discard the already valid accept/reject construction.

For mechanism B, there is already a constructive route, so the substantive question would be whether a specified scientific model supplies usable, inexpensive geometric certificates and whether a new operation beats ordinary rejection/NNARS using exactly the same information. Without that concrete input and comparison, there is no reason to open an application campaign.

## Work record and limits

Read the Cycle 2 PRO3 prompt and prefix access contract to preserve the resolved boundary, without reading the optional-prefix proofs. Read the primary sections specified above; investigated reference-reversible proposals, corrected state-dependent mixtures, delayed acceptance and geometric adaptive rejection. Both web search engines were used. Some exact-string searches returned unrelated material and were discarded. An initially guessed PMLR path used `achdou` rather than the proceedings spelling `achddou`; the authoritative path was recovered. A Kamatani HTML request was disabled and no claim depends on it.

No scientific simulation, old proof review, old sampler suite, application search, installation, spending, or outreach was performed. This is a literature and mechanism note, not an executed algorithmic improvement. The companion resource receipt records observed clocks and tool counts; it is not a claim about total model/research cost.
