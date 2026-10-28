# Positive residual events from nonintrusive boundary observations

28 October 2026. This construction changes the experimental interface in a
specific, useful classical source class. It does not turn endpoint-only
observations into a positive residual oracle by postprocessing.

## 1. Source and additional observable

Let P_i be killed reversible Markov transitions with a common reversible
measure. In its symmetrized Hilbert representation each A_i is self-adjoint
and contractive. A fixed physical state b can be reset reproducibly. The
additional observation is an accurate, nonintrusive predicate: is the
current state b? The observer receives no identity for another live state
and cannot distinguish an unobserved live state from the cemetery.

Return probabilities are f_i(k)=<b,A_i^k b>. Reversible similarity factors
cancel on a return path, so the construction does not require every hidden
stationary weight to be known. All source-norm and sensor premises remain
explicit. A quantum intermediate measurement generally changes the process
and does not automatically provide this classical interface.

Use the one-column dictionary V=b and the true Galerkin coefficient
p_i=P_i(b,b). Set D_i=(A_i-p_i)b.

## 2. The positive event identity

For k>=0,

    g_(i,k)=D_i* A_i^(2k) D_i
      =f_i(2k+2)-2p_i f_i(2k+1)+p_i^2 f_i(2k).

The same quantity is the probability, conditional on X_0=b, of

    X_1 != b, X_(2k+1) != b, X_(2k+2) = b.

Inclusion-exclusion proves the identity. Removing paths with X_1=b gives
p_i f_i(2k+1); removing those with X_(2k+1)=b gives the same term; the
intersection contributes p_i^2 f_i(2k). For k=0 the first and penultimate
observations coincide, and the formula still gives f_i(2)-p_i^2.

Consequently a genuinely positive residual event is observable. At exact
closure its probability is exactly zero under the ideal sensor contract.
The full-support endpoint-only impossibility does not apply because the
intermediate predicate distinguishes events absent from that observation
law. False-negative or false-positive sensor errors can destroy this null
property and must be included as a probability-error floor.

## 3. Acquire the weighted source form with finite trials

Given a warranted ||A_i||<=a_i<1, write M_i=1/(1-a_i^2). For depth K,

    Q_i=D_i*(I-A_i^2)^(-1)D_i
       <= sum_(k<K) g_(i,k) + M_i g_(i,K).

Choose a random k with weights 1,...,1,M_i and observe the event above.
With Z_i=K+M_i, its success probability is the displayed finite upper
form divided by Z_i. This is a finite Bernoulli experiment. It has no
subtraction of large measured means.

If the first predicate reports X_1=b, the event is already false and the
trial stops immediately. The first predicates from every trial also estimate
p_i; no separate model-calibration batch is necessary. Reusing these data
introduces dependence between estimates, which is harmless to the union
bound on their confidence events.

For X successes in N independent trials and ell>0, one-sided Chernoff
inversion gives the upper mean bound

    p <= [X+ell+sqrt(ell^2+2 ell X)]/N

except with probability exp(-ell). The companion lower bound is
max(0,[X-sqrt(2 ell X)]/N), with the same one-sided failure probability.
The code evaluates square roots outward with rational arithmetic. For
estimating a self-loop near one, it applies these bounds to the rare
departure count, not to the abundant self-loop count.

Let t_i be the observed self-loop frequency and let delta_i bound its
error. For D'_i=(A_i-t_i)b, the triangle inequality in the inverse-source
dissipation norm gives

    Q'_i <= [sqrt(Qupper_i)+delta_i/sqrt(1-a_i^2)]^2.

Define R_i=1-t_i^2 and accept only R_i>0. Then theta_i^2=Q'upper_i/R_i
satisfies the source premise of the dissipation theorem. The uncertain
weak defect p_i-t_i contributes at most zeta_i=delta_i/R_i after the
two coefficient-energy telescopes. Thus the central predictor formed
from the t_i satisfies, simultaneously for every future finite word,

    |f(w)-prediction(w)| <= 2 max_i theta_i^2 + max_i zeta_i.

The learned scalar maps commute in this rank-one specialization. The
certificate asserts that any order effects omitted by this representation
are inside the bound. The several-boundary-state extension retains
noncommuting maps and is a separate construction.

## 4. Executed sampling and complete charges

The simulator's two live-state matrices are

    P_0=[[1-g,g],[g,1/4]], P_1=[[1-2g,g],[g,1/3]], g=1/20,

with row deficits sent to an absorbing cemetery. A supplied a=1-g/2 is
verified against the hidden matrices by the checker. The learner receives
only counts, the predicate interface and this norm warranty; it receives
neither the matrices nor a hidden-rank promise.

At K=4, two million flag trials per primitive, and ell=10, the run has
227 and 218 positive flags. It charges 6,452,016 primitive applications,
four million resets and 4,587,663 predicate observations. All random
transitions are generated with integer denominators; the learner does not
receive an expected-count oracle. No physical equipment was operated.

The four million figure is the original conservative fresh-reset ledger,
equal to the number of logical trials. Under the exact Markov and
nonintrusive-predicate premises, a trial known to end at b can start the
next trial without a physical preparation. The same receipts therefore
give a valid required-preparation upper bound of 299,681. The strong Markov
property preserves the trial law. This reuse would be invalid if the
predicate merely identified a coarse label concealing an unreset state.

`core/markov_residual_events.py` initially uses a Hoeffding model interval
and obtains bound .1115663505. `core/markov_departure_refinement.py`
reuses the same departure counts with variance-aware intervals and obtains
the exact rational upper bound whose decimal is .0919031664. It performs
zero new source queries. Two two-sided model bounds and two one-sided flag
bounds have joint failure at most 6 exp(-10)<.001. This is a bound on the
probability of emitting a false guarantee, not posterior confidence
conditional on a particular emitted transcript.

The checker verifies 73 switched and constant-mode tasks, maximum observed
error .023569. The all-word conclusion follows from the proved certificate,
not from that finite test set. It concerns separately reset unconditional
programs, not policies conditioned on hidden intermediate trajectories.

## 5. Strong comparator and the remaining precision charge

The same predicate permits first-return/renewal acquisition, an established
strong alternative. Let r_even and r_odd denote nontrivial first-return
probabilities by parity, r=r_even+r_odd and s=r_even-r_odd. Renewal algebra
gives the exact identity

    Q=r_even+r^2/[2(1-p-r)]+s^2/[2(1+p-s)].

For a reversible source s>=0 by the positive resolvent of the hidden
compression. Censoring, missed-return tails and all unobserved cemetery
steps must still be paid. The dynamics branch implements this alternative
and replays its confidence bounds exactly.

At g=.05 the refined fixed-flag run gives .09191 using 6.452 million steps;
the renewal run gives .09356 using 8.192 million steps, both with four
million logical trials. Known-boundary reuse gives preparation counts or
upper bounds 299,681 for flags and 299,190 for renewal. Renewal has not
earned a clear complete-cost advantage at this point.
At g=.01, runs meeting .05 accuracy trade 27.169 million steps and 24
million logical trials (flags) against 32.037 million steps and four
million logical trials (renewal). The corresponding preparation upper
bound/count is 359,737 versus 60,242. Preparation and observation costs
change the preferable strategy. Because some failed flags also end at b,
the flag upper bound cannot establish a hardware-cost crossover by itself.

Rare-event acquisition can improve the residual-estimation exponent, but
the complete target also requires accurate retained transition rates.
To deliver O(g) output error over the slow scale 1/g, the weak-defect
allowance requires model error O(g^2). Estimating a departure probability
of order g to that accuracy costs order g^-3 samples at fixed confidence.
The complete-cost theorem and matching elementary calibration lower bound
are developed separately; a residual-only sampling improvement must not
be advertised as an end-to-end improvement.
