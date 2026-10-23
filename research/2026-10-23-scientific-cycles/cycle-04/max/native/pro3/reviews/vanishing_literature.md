# Vanishing screens: primary-literature and operational boundary

Prepared by the focused literature/operational contributor for Astra PRO3 Cycle3.
Host date: 2026-10-21 UTC; programme packet date: 2026-10-22.

## Decision and scope

The diagonal regime in which the screening exponent depends on the requested
horizon is a substantive uniformity question. It does not follow by substituting
an exponent into a theorem proved separately for every fixed positive exponent.
The parent investigator owns the constructive proof and its acceptance. This
note assesses the closest literature found, records an elementary nonuniformity
example, and derives accuracy consequences conditional on the parent's stated
uniform bounds.

The narrow literature search did not identify a theorem giving the proposed
KL-only, proposal-start, support-uniform diagonal threshold. This is not a
historical originality certificate. Standard delayed acceptance, tempered
surrogates, interpolation, first-hit decompositions, and general links between
mixing and hitting times all have substantial prior literature. The candidate
contribution must be the explicit minimax boundary with its matching admitted
family, not those ingredients individually.

The relevant class is finite labelled state spaces, positive probabilities
pi and q, fixed population bound D(pi||q)<=K, fixed alpha in (0,1),
beta=1-alpha, symmetric stochastic Q, and

    C_eta = (I + alpha G + beta L_eta)/2, initialized at q.

Here G is independence MH with proposal q, and the off-diagonal acceptance of
the Q proposal is

    a_eta(x,y) = min(1,(q(y)/q(x))^eta)
                min(1,(pi(y)/pi(x))(q(x)/q(y))^eta).

The exponent can depend on the predeclared horizon or tolerance, but remains
fixed throughout an individual run. The normalizer of the target is not
available. Neither a within-run adaptive chain nor a new initial distribution
is admitted by this note.

## Closest primary results and exact boundaries

### 1. Delayed-acceptance construction and stationary comparisons

Marco Banterle, Clara Grazian, Anthony Lee, Christian P. Robert,
*Accelerating Metropolis-Hastings algorithms by Delayed Acceptance*,
arXiv:1503.00996v2, journal publication 2019:
<https://arxiv.org/html/1503.00996v2>.

Sections 2.1-2.2 and Lemmas 1-2 validate products of reciprocal acceptance
factors. Section 2.3, Condition 1 and Proposition 1, give spectral-gap and
asymptotic-variance comparison when accepted-ratio factors have a common
positive lower bound. Section 2.4, Proposition 2, clips factors to obtain such
control. Section 2.6, Proposition 3, exhibits loss of geometric ergodicity with
an unsuitable surrogate. The introduction and Section 3 distinguish reduced
evaluation expense from reduced acceptance.

The present L_eta is a standard two-factor delayed-acceptance kernel.
The required common factor lower bound is absent when q ratios are unrestricted.
Stationary variance or spectral comparisons therefore do not supply the
proposal-start diagonal TV assertion. Claim neither the algorithmic factorization
nor the general warning about poor surrogates as new.

### 2. Variance-bounding inheritance can fail under a tempered surrogate

Chris Sherlock, Anthony Lee, *Variance Bounding of Delayed-Acceptance Kernels*,
Methodology and Computing in Applied Probability 24, 2237-2260 (2022):
<https://doi.org/10.1007/s11009-021-09914-1>;
author preprint arXiv:1706.02142v4:
<https://arxiv.org/pdf/1706.02142>.

Section 3, Lemma 1 and Theorem 1, transfer conductance under a regionwise
minorization and small excluded accepted-proposal mass. Section 4.2,
Corollary 2, uses bounded surrogate/target ratios. Corollary 3 and Theorem 3
weaken this under local-proposal and discrepancy/tail conditions.
Example 3 is particularly close in spirit: the independence proposal equals
an exponential target, while a different exponential surrogate destroys
variance bounding. Example 4 contrasts a random-walk proposal on that target.

These are qualitative properties of individual continuous-space kernels,
not a population-KL-only uniform q-start rate over finite spaces with a
separate unscreened global IMH component. They establish that surrogate
flattening and robustness are old concerns; they do not determine the proposed
eta log n threshold.

### 3. Recent tempered-surrogate mixing theorem: DART

Robert Kutri, Robert Scheichl, *Fast-Mixing Markov Chains without Gradients*,
arXiv:2606.27564v1:
<https://arxiv.org/html/2606.27564v1>.

Section 3, equations (3.1)-(3.6), constructs state-dependent surrogate
proposals with potential theta g(y)+gamma||y-x||^2/2 and an inner root chain.
Theorem 3.4 fixes theta=1/2 and assumes a warm start, strongly convex smooth
target and surrogate, gradient fidelity (3.12), localization (3.13), and
root-chain mixing (3.14). Its outer mixing bound is
O(kappa max(kappa,d) log(2 beta/delta)); the inner-chain length is additional
work. Section 4.3's multimodal evidence lies outside that theorem.

This is a primary precedent for mixing analysis of regularized and tempered
surrogates. Its state-dependent proposal, geometric hypotheses, warmness,
and fixed theta do not establish the current finite-space KL-only diagonal
result. It also prevents describing tempered-surrogate mixing guarantees
in general as a new area created by this project.

### 4. Weak Poincare comparison and the cold initial density

Christophe Andrieu, Anthony Lee, Sam Power, Andi Q. Wang,
*Comparison of Markov chains via weak Poincare inequalities with application
to pseudo-marginal MCMC*, arXiv:2112.05605v2:
<https://arxiv.org/html/2112.05605v2>.

Theorem 8 gives an L2 convergence estimate multiplied by an initial
functional Phi(f). Remark 12 converts it to TV for an initial density whose
corresponding Phi is finite. Section 2.3 treats independence MH; Section 3
develops comparison/chaining inequalities.

These are close general analytic tools. The proposed problem cannot simply
invoke the density version with a uniform initial constant: dq/dpi=1/W can
be arbitrarily large under D(pi||q)<=K. Finite support makes each individual
density square-integrable but does not bound its norm uniformly as support
and probabilities vary. A bounded-test argument can avoid that particular
density requirement, but still needs the proposed q-relative transport and
explicit eta dependence. The first-hit interpolation is the missing
problem-specific obligation rather than a new interpolation principle.

### 5. Mixing and hitting large sets

Yuval Peres, Perla Sousi, *Mixing times are hitting times of large sets*,
arXiv:1108.0133v3, Journal of Theoretical Probability 28, 488-519 (2015):
<https://arxiv.org/pdf/1108.0133>;
author copy <https://www.statslab.cam.ac.uk/~ps422/mix-hit.pdf>.

Theorem 1.1 compares lazy mixing time to the maximum expected hitting time
over all starting states and all sets with stationary mass at least a fixed
number below 1/2. Section 9 discusses robustness under conductance
perturbations.

The current first-hit decomposition concerns a specified q start and a
particular safe set. An unrestricted worst-start hitting maximum can be
dominated by a state of negligible pi and q mass. It is therefore too strong
to insert as a common finite constant in the KL-only class. This source
supplies perspective, not the desired sharp threshold.

## Why the new limit is not a parameter restatement

Let R_eta(n) be the supremum of the proposal-start TV error over the stated
class. The already accepted fixed-positive-eta theorem controls

    for each eta>0: lim_(n->infinity) log(n) R_eta(n)=K.

It does not provide a rate for how large n must be as eta shrinks. The
candidate diagonal theorem addresses R_{eta_n}(n), whose worst instance
may vary with n. The two quantifiers cannot be exchanged without an
explicit bound uniform in eta on the required range.

Even one-step kernel convergence to eta=0 is nonuniform within the admitted
class. Here is a direct illustration, independent of the parent's
long-horizon calculation.

Fix b in (0,1-exp(-K)). On states A,B,C, for sufficiently small eta>0 take

    q(A)=b exp(-1/eta), q(B)=b, q(C)=1-b-b exp(-1/eta),
    pi(A)=eta^2, pi(B)=eta^4, pi(C)=1-eta^2-eta^4.

Let Q swap A and B and fix C. All probabilities are positive. The A
contribution to D(pi||q) is eta+o(1), the B contribution is o(1), and the
C contribution tends to -log(1-b)<K. Thus the KL constraint holds eventually.
For B->A, the first stage is exp(-1), the second stage is one, whereas
ordinary MH (eta=0) accepts with probability one. Consequently

    TV(C_eta(B,.),C_0(B,.)) = beta(1-exp(-1))/2

for this row, independently of how small eta is.

For every single fixed positive finite pair the entries do converge as
eta->0. The failure is the uniform exchange over pairs with increasingly
extreme proposal ratios. This is exactly the type of issue a diagonal
theorem resolves. The example is an elementary witness, not a proof of the
candidate horizon threshold.

## Accuracy formulation: a consequence of the proposed uniform bounds

This section is conditional on the parent accepting its uniform upper
estimate and the independent three-state capture lower estimate. It should
not be promoted merely on the strength of this literature note.

Write T_eta(epsilon)=inf{n:R_eta(n)<=epsilon}. The screen eta(epsilon)
is selected before the run and stays fixed. Let

    d_epsilon = eta(epsilon)/(epsilon log(1/epsilon)).

The proposed upper transport threshold has constant

    Lambda_* = 1 + log(1+beta/2)/
                     [-log(1-alpha exp(-K)/2)].

Equivalently its interpolation exponent can approach
1/Lambda_* from below by choosing the fixed safe-set parameter sufficiently
small. To translate from horizon to accuracy, evaluate at

    n_epsilon = ceil(exp(A/epsilon)), A>0.

Then log n_epsilon ~ A/epsilon. The KL-tail term contributes
K epsilon/A to first order. If d_epsilon->d in (0,infinity), the upper
transport remainder is bounded by a constant times
epsilon^(a A d+o(1)), for every admissible fixed a<1/Lambda_*.
It is o(epsilon) whenever a A d>1. Taking A>K as well proves the candidate
upper conclusion

    limsup epsilon log T_{eta(epsilon)}(epsilon)
        <= max(K,Lambda_*/d).

The capture family uses target mass p=(log n)^(-m), m>2, so that its
target-mass subtraction is o(epsilon) at this horizon. Its retained
spurious mass is a positive constant times

    exp[-eta(epsilon) log n_epsilon (1+o(1))]
      = epsilon^(A d+o(1)).

If A d<1 this exceeds epsilon by an unbounded factor. Together with the
pure-IMH lower family, this gives

    max(K,1/d)
        <= liminf epsilon log T_{eta(epsilon)}(epsilon)
        <= limsup epsilon log T_{eta(epsilon)}(epsilon)
        <= max(K,Lambda_*/d).

The endpoints of this useful regime statement are:

* If d_epsilon->infinity, the coefficient is K.
* A finite limit d>Lambda_*/K also suffices for coefficient K.
* If 0<d<1/K, the hybrid has a strictly larger minimax exponential
  coefficient than K under this tuning, assuming the capture proof.
* If d_epsilon->0, every fixed A gives retained mass
  exp[-o(log(1/epsilon))] much greater than epsilon. Hence
  epsilon log T_{eta(epsilon)}(epsilon)->infinity.

The remaining interval between 1/K and Lambda_*/K is not resolved by these
bounds. Equality cases require separate treatment. Nor should a mere
zero-error limit be confused with reaching error epsilon: for example,
eta(epsilon)/epsilon->infinity can give convergence at horizons
exp(A/epsilon) while eta(epsilon)/(epsilon log(1/epsilon))->0 still
prevents epsilon accuracy at every finite A.

All statements here concern a diagonal family of fixed kernels. They say
nothing about changing eta along a trajectory, and do not substitute a
random stopping count into a deterministic-horizon formula.

## Matched comparator and actual cost boundary

The operational comparison must retain pure IMH with the same q, target
oracle, caching, precision and population-KL certificate. Its established
coefficient is already K. Thus the candidate result demonstrates a
robustness threshold and a possible penalty for an insufficient screen,
not an improvement over the strongest ordinary method in this class.

The local product acceptance is pointwise nonincreasing in eta>=0. To
check, put r=q(y)/q(x), s=pi(y)/pi(x). If r<=1 then
a_eta=min(r^eta,s); if r>=1 then a_eta=min(1,s r^(-eta)).
Both are nonincreasing. Decreasing eta therefore increases local
off-diagonal transitions towards ordinary MH. That stationary comparison
does not imply a proposal-start finite-time TV ordering. Indeed, the
candidate adverse family would quantify precisely why that inference fails.

The first screen also passes at least as often when eta is decreased.
Consequently weakening eta does not reduce the number of uncached target
evaluations for a fixed current state and proposed point. It may change
the subsequent state trajectory and reuse, so no total runtime ordering
follows either.

For an honest implementation, each run must count:

* initialization from q and its target evaluation;
* IID global proposals, local Q proposals, random branch choices and uniforms;
* q-value or log-q evaluation at all required points;
* target evaluations only after an accepted first local screen or for a
  required global acceptance test, except when cached;
* all cache lookups, cache misses, memory and preprocessing;
* log-ratio arithmetic and numerical decisions at both stages.

The expected number of branch proposals in n lazy steps is alpha n/2
global and beta n/2 local. Expensive target evaluations can be lower
because of repeated candidates and local first-stage rejection. These
counts alone do not determine wall time or estimator error. No CPU
benchmark was executed for this note.

If the complete finite target table is actually supplied or cheaply
enumerable, normalized direct discrete sampling is an ordinary comparator
and the oracle-only minimax model is not a practical restriction one may
impose on that recipient. If the target is genuinely expensive and available
only through evaluations, cache both methods fully. The target normalizer
cancels in every acceptance ratio; it must not be inferred from the
population-KL assumption or silently supplied by test code.

The proof is an ideal-real statement. Computing eta log(q(y)/q(x)) rather
than raising tiny probabilities is a sensible representation, but a
floating-point implementation still needs a numerical error contract.
No uniform precision cost over unbounded log-proposal ratios is established
by the mixing theorem. Target approximations, stochastic likelihoods,
empirical training loss, and within-run parameter adaptation need separate
assumptions and are outside this result.

## Search boundary and failed retrievals

The focused search used both engines, with primary-domain verification,
on delayed acceptance, tempered-surrogate mixing, variance-bounding
inheritance, vanishing parameters, relative entropy, and first-hit mixing.
It reopened the five primary sources summarized above. Recent searches
also surfaced adaptive multilevel/SMC and empirical subset-sampling work;
none was used to assert the current theorem or a speedup.

The 2021 Sherlock-Thiery-Golightly paper on delayed-acceptance RWM
efficiency was located, but its full-text Euclid endpoint returned only
an iframe and both arXiv and an author PDF route failed in this session.
No section-specific technical claim from it is made. Some unversioned
arXiv HTML routes also failed; working versioned HTML or PDF routes were
then used for the sources above. These are source-access limitations,
not counterevidence about their results.

The literature supports proceeding with the specific diagonal theorem.
It does not support claiming new delayed acceptance, universal superiority
of tempering, or any demonstrated practical acceleration. After the
parent's proof assessment, the sharp finite-d crossover coefficient is
a precise remaining question, if its resolution warrants further effort.
