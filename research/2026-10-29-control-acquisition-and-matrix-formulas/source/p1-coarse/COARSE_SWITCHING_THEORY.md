# Certified composition from coarse survival observations

29 October 2026, Brisbane. This construction preserves hidden source memory,
uses fresh common preparations and live/absorbed reports, and certifies every
fixed switching word. Its executed source has countably infinitely many
states, norm one and infinite mean lifetime. A two-state approximation is
certified without assuming finite hidden rank.

The ingredients are established: positive-operator domination, weak Poincare
inequalities, energy estimates, confidence intervals, prefix trees and moment
realization. The useful contract joins finite native lifetime acquisition,
simultaneous switching-tail control, paid mixed-word observations, and finite
verification of a model's every-word output. Historical priority and generic
efficient learning are not established.

## Common preparation and the observable energy inequality

Let A_i be positivity-preserving selfadjoint contractions sharing a positive
unit vector v with A_i v<=v. On countable coordinates, mu_j=v_j^2 is a
probability distribution and P_i(j,k)=A_i(j,k)v_k/v_j is a substochastic
kernel reversible for mu. Prepare mu and report only live/absorbed. The
survival of a chronological word is f(w)=<v,A_wv>. Reversal preserves this
scalar. Every reachable x=A_wv satisfies 0<=x<=v.

The common reversible preparation is a structural access premise. Selfdual
readout alone does not establish the order condition. No boundary identity,
hidden dimension, strict source norm cap or uncensored lifetime bound is
supplied. A surviving coarse label never silently resets the actual source.

For any integer m>=1, the spectral inequality
1-lambda^(2m)<=m(1-lambda^2), |lambda|<=1, and order domination imply

    ||x||^2 <= m E_i(x)+f(i^(2m))||x/v||_infinity^2,
    E_i(x)=||x||^2-||A_i x||^2.                         (1)

Indeed, |A_i^m x|<=||x/v||_infinity A_i^m v. Equality at x=v proves

    sup_(|x|<=v) ||A_i^m x||^2 = ||A_i^m v||^2=f(i^(2m)).

Thus one accessible scalar supplies a uniform coefficient on the relevant
order interval. If simultaneous observations give s>=max_i f(i^(2m)),
then every switched state of length h satisfies

    ||A_wv||^2 <= z_h=s+(1-1/m)^h(1-s).                 (2)

Apply (1) at the selected action and iterate. Splitting a word into lengths
a,b and using reversal and Cauchy-Schwarz gives f(w)<=sqrt(z_a z_b).
Every length-2h word therefore has survival <=z_h. Absorption extends this
to all greater lengths. The limiting floor is s, rather than sqrt(s).

One acquired scale is a defective/one-scale weak-Poincare inequality. If
individual lifetime survivals tend to zero, finite q permits arbitrarily
small s at some finite m. Individual eventual absorption then implies uniform
eventual absorption over switching words in this common-preparation class.
There is no source-independent bound on m. Finite censoring is still needed
when uncensored mean lifetimes are infinite.

The energy mechanism is established weak-Poincare theory. The precise primary
comparison is branches/physical/CURRENT_WEAK_POINCARE_COMPARISON.md. The
ordinary proof, stronger multiscale recursion and structural counterexamples
are in branches/scalar/COARSE_SURVIVAL_FORMS_AND_SWITCHING.md. Positivity
preserving is essential; positive semidefiniteness alone is insufficient.

## What lifetime marginals leave unidentified

Take uniform preparation and total-live readout with

    A=[[10,2],[2,2]]/16,
    B_plus=[[8,1],[1,2]]/16,
    B_minus=[[2,1],[1,8]]/16.

A hidden swap conjugates the B matrices while fixing the preparation and
readout. All individual-action survival laws agree at every length. Yet AB
survival is 15/64 versus 9/64, and AAB-minus-ABA is -1/256 versus 5/256.
Even exact infinite marginal data leave mixed responses and preferred order
unidentified. See branches/physical/COARSE_SINGLE_ACTION_SWITCHING_OBSTRUCTION.md.

## Finite prefix coverage and compact model certification

Acquire simultaneous intervals on a finite prefix tree. A node is terminal
when its survival upper is <=epsilon; all extensions then have survival
<=epsilon. Every nonterminal node must have every action child represented,
and an interval half-width <=epsilon. Predict its midpoint at a nonterminal
word and zero at or after a terminal prefix. The empty word is exactly one.
If every branch closes, these finite checks certify every word.

Data-dependent pruning is valid when confidence covers every potential
interval. The cover argument itself needs absorption monotonicity, not rank
or reversibility. The lifetime theorem gives a finite cutoff for its source
class. Generic exhaustive acquisition to that cutoff may be exponential.
Prefix estimation is familiar; it is not claimed as a new learning algorithm.

A fitted positive substochastic model can use the same cover. At a branch,
bound its error by its maximum distance to the interval endpoints. At a
terminal prefix, bound both actual and model survival. Each decreases under
all suffixes, so every extension error is at most the larger prefix upper.
All passing models, including ones selected from the same data, are covered
by the single confidence event. No model-dimension premise is transferred to
the hidden source. Conditional normalized states and lifetime moments are
not controlled by uniform absolute survival accuracy.

## A countable source where centered inverse forms diverge

The fast block uses C_0=A and C_1=B_plus above, with preparation weight
1023/1024. For each n>=0 add a two-state block with

    p_n=2^(-n-1)/1024,
    A_i^(n)=(1-e_n)I+e_n C_i, e_n=2^(-n-4).

Prepare uniformly within each block. Every state has positive preparation
probability and killing probability. Slow diagonal expectations approach
one, proving the full contraction norm is exactly one. Each individual
operation eventually absorbs, but even the waiting time to first activation
has infinite mean: sum_n p_n/e_n=sum_n 1/128=infinity.

For every scalar t<1, the inverse-dissipation form of (A_i-tI)v is infinite:
on sufficiently slow blocks its numerator stays bounded below, while inverse
dissipation grows as 1/e_n. The scalar branch proves the stronger statement
for finite word features and strictly stable computational maps. The new
cover succeeds outside that certificate's finite-form premises. This is not
a failure theorem for all reduction methods; unweighted certificates remain
available at their own accuracy and conditioning cost.

The source backend uses integer transition draws and an untruncated geometric
bit sampler. No hidden state label or tail parameter reaches inference.
Every live update and report is charged. There is no unobserved-duration
shortcut and no physical equipment operation.

## Executed acquisition

First acquire 8,192 fresh trajectories per primitive, each censored at 32.
Simultaneous KL upper bounds cover the 32 even-time probabilities inspected.
The chosen scale is m=4 and s=.039498905686. Equation (2) after 13 energy
steps gives z_13<1/16. Thus every word of length at least 26 has survival
below 1/16, without a supplied strict source cap.

Next assign 512 fresh preparations to every binary control tape of length
10, totaling 524,288. Report after every executed step. Absorbed trajectories
stop and count as zero at all later assigned prefixes. A length-h prefix has
524,288/2^h preassigned trials, including those zeros; its survival count is
binomial for the unconditional prefix response. Future assigned controls
cannot affect that law. Overlapping prefix estimates need not be independent.

The resulting complete cover has 84 nodes: 41 branches and 43 terminals,
maximum length 7. It certifies absolute error 1/16 for every switching word.
The complete acquisition, INCLUDING the pure-curve phase, costs

    1,086,180 primitive applications,
    1,086,180 live/absorbed observations,
      540,672 fresh preparations.

All preparations are paid. The pure phase is retained in this cost even
though the observed cover closes before its conservative cutoff of 26.
The joint failure bound is

    32 exp(-12)+4092 exp(-18)<.001.

This allocates over all 2,046 possible prefixes before pruning. Floating
point proposes interval endpoints; exact rational logarithm enclosures accept
them. The dynamics branch independently replayed the ledgers, 168 selected
node endpoints, all 32 pure endpoints, completeness and inference isolation.

## The certified two-state approximation

An ordinary two-dimensional moment realization uses the same early counts
to propose, then rationally round,

    T0=[[.632329,.119580],[.119580,.131730]],
    T1=[[.497697,.070398],[.070398,.112506]].

Start uniformly and read total survival. Exact checks establish nonnegative
entries, symmetry and substochasticity. The 84 finite cover checks give

    every-word absolute error <= .062335817204,
    retained-branch error <= .016765342629.

There are no new source queries. The dynamics branch separately checked this
new use of the accepted cover. It certifies a two-state approximation to an
infinite source, not a two-state physical realization. A finite-mean candidate
and an infinite-mean source can agree to this absolute probability accuracy.

The candidate uses two matrices, while the validation artifact retains the
cover. A length-h matrix-product prediction costs O(h) fixed-dimensional
arithmetic, including its numerical-precision cost. The tree often answers
after seven controls, so compression here is not a demonstrated runtime gain.

## Strong existing routes and the remaining cost

DKW survival estimation already handles all repetition lengths of one action;
SURVIVAL_BASELINE.md gives its executed costs. The exact two-state ambiguity
explains why mixed-word data remain necessary. Positive realization and
prefix probability estimation are also established methods used here.

On the identical mixed-word counts, the retained scalar-echo compiler was
tested with three short dictionaries and exact common-metric checks. Its best
boxed-interval all-word bound was 9.69646, vacuous beyond the physical output
range. This is a failure of that specified conservative certificate at these
counts, not a lower bound against optimized moment-SDP or residual methods.

The strongest adopted comparator is the positive two-state realization:
ordinary fitting becomes certified through the acquired cover. Existing
methods using the same certificate preserve the observable addition. No
universal superiority or historical priority claim follows.

Acquisition complexity is the remaining obstruction. A cover can require
exponentially many mixed contexts. A broadly efficient method needs an
experimentally checkable reason that a small context set closes, or a
physical operation exposing the missing joint information. Fitting a small
candidate alone supplies neither.

## The next cost attack: a conditional upper and a generic lower

The conditional adaptive method was then executed on the identical source
with independent data. It required 458,449 applications/reports and 255,220
fresh preparations, giving a 38-node cover of depth five at the same 1/16
all-word absolute survival accuracy. It selects new words predictably,
uses fresh fixed batches, and predicts half the small upper at terminal
prefixes. No old receipts or lifetime pilot are used. Thus it is a stronger
executed route for this scalar task than the balanced acquisition. Its
terminal-floor representation does not automatically certify the earlier
two-state matrix model; see ADAPTIVE_COARSE_COMPARISON.md.

This remaining obstacle has now been tested. Let C_eta be the size of the
smallest complete prefix tree stopping only at true survival <=eta. Its
canonical form stops at the first such prefix. A fresh-batch adaptive learner
with radius epsilon/4 and node-j confidence expenditure delta/[j(j+1)]
visits no more than C_(epsilon/2) nodes on its simultaneous confidence event.
With C=C_(epsilon/2) and maximum depth H, its complete resource bounds are

    preparations O(C epsilon^-2 log(C/delta)),
    applications/reports O(H C epsilon^-2 log(C/delta)).

The proof controls rare overshoot too: if B counts confidence failures,
E exp(theta B)<=exp(delta(exp(theta)-1)), the actual node count is at most
C+qB, and depth is at most H+B. It therefore terminates almost surely and
has the same unconditional expected cost orders whenever C is finite.
The sharper source bound charges the comparison tree's sum of depths.
Allowing a nonzero midpoint prediction at terminal nodes instead of zero
improves the comparison to C_epsilon at the same absolute accuracy.

This is a conditional resource theorem for familiar active prefix estimation,
not a claim that C is a universal minimum sample count. It uses fresh batches
and cannot be retrofitted to data-dependent selections from the already
inspected balanced tapes. Its proof is in
branches/scalar/ADAPTIVE_PREFIX_COVER_COST_REVIEW.md.

Conversely, COARSE_INTERFACE_LIMIT.md constructs a four-control source family
with a KNOWN strict norm cap 1-1/(20d), identical individual-action lifetimes,
and short mixed responses hiding one of 2^d-1 possibilities. Uniform error
1/16 for all words of length <=3d+2 at success >=2/3 requires at least
(2^d-1)/6 expected informative preparations and primitive applications.
Arbitrary adaptive experiments are covered. A fully family-informed
comparison route matches the exponential scale up to polynomial/log factors.
Thus a generic polynomial bound cannot replace the context resource merely
by improving the representation or the numerical solver.

Code: core/coarse_switching_cover.py, core/coarse_compressed_model.py and
core/coarse_echo_comparison.py. Exact receipts and logs are under results;
scoped reviews are under branches. Preparation and sensor warranties are
premises of these executed software experiments, not newly calibrated devices.
