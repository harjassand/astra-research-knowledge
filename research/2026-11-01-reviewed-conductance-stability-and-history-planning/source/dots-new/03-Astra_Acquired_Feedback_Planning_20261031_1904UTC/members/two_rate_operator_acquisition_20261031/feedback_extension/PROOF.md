# Acquired-block Markov feedback: a separately paid planner

Exploratory extension, outside the accepted 18:24 freeze and its review.
The planner is ordinary finite-horizon coarse-MDP dynamic programming. The
question here is whether the acquired certificate actually covers its policy
class, with all additional acquisition paid. No new Bellman algorithm is claimed.

## 1. Exact task/interface

There are m unknown stochastic A_a on n explicitly named states, with the
same ordinary forward generative interface as the accepted source. The task
specifies a fixed initial probability ell and terminal reward b in [0,1]^n.
The acquired partition P=ZW must preserve both, exactly as before.

The output is an OFFLINE policy and value certificate for this explicit-state
simulator. A simulated rollout retains its current microscopic state label i;
querying (a,i) returns the next label. At each remaining horizon t the policy
looks up g=block(i) and a=pi_t(g). Actual deployment does not thereby acquire a
physical sensor, hidden-state estimator or authenticated block observation.
Those would be additional premises/costs, and are not constructed here.

The comparison class is all deterministic time-dependent Markov policies on
the acquired block labels. Randomized Markov block policies can also be
covered by convexity. Arbitrary microscopic feedback and arbitrary
history-dependent block feedback are NOT in this class. Small prediction rank
alone is not a claim that they have no advantage.

## 2. The extra operator family

Let D_g be the diagonal indicator of block g. P,Q commute with every D_g.
For a deterministic map pi:{1,...,r}->{1,...,m}, define

    A_pi = sum_g D_g A_(pi(g)),
    B_pi[g,:] = B_(pi(g))[g,:].

Both matrices are stochastic. A product of the A_pi operators represents a
time-dependent Markov block policy, with the usual backward-value ordering.
There are m^r one-step maps, not m^(rL), but m^r is still exponential in r.
The first historical construction explicitly acquired/checked ALL of them.
The current polynomial sufficient route instead uses the acquired block-norm
comparison in BLOCK_COMPARISON_PROOF.md; it does not claim an optimal norm planner.

Set D_a=sum_(g:pi(g)=a)D_g. These are disjoint orthogonal row selectors. For
any vector x,

    ||Q A_pi P x||_H²
       = sum_a ||D_a Q A_a P x||_H²
       <= sum_a e_in,a² ||x||_H².

Thus e_in,feedback=sqrt(sum_a e_in,a²), or the implemented sqrt(m)*max e_in,
is valid. Moreover row g of W A_pi Q equals row g of W A_(pi(g)) Q, so e_out
is unchanged. The coarse-action row error d is also unchanged.

The same argument only gives alpha_feedback<=sqrt(m)*max_a alpha_a,
which can destroy contraction. We do NOT assume the original alpha survives.
Instead use the original simultaneous spectral observation event for C_a:

    C_pi=sum_g D_g C_(pi(g)),
    ||A_pi−C_pi||_2<=sqrt(m)*t.

Fresh probes, chosen after all acquired data and this entire finite policy
family are fixed, certify ||Q C_pi Q|| for every pi with failure allocation
delta_norm/m^r. The resulting bound is

    alpha_feedback = max_pi certified_norm(Q C_pi Q) + sqrt(m)*t.

All probes and sparse integer products are paid. The initially acquired
per-action norm work becomes redundant here but remains in the ledger.
The observed C_pi is not stochastic and its count total need not equal the
original common denominator. The code normalizes by its actual count total
for the existing norm checker, then exactly rescales to the original count
denominator. No stochastic-normalization shortcut is applied to C_pi.

The original source sampling/pilot/leakage/fine events are retained with
their original allocations. The new family norm event REPLACES the old
per-action norm event in the proof, with the same delta/8 budget; it is not
silently added on top of an exhausted confidence budget. All other events
remain simultaneous over actions and fixed rounds, so reusing their records
does not introduce independent-evidence assumptions. The same mock-randomness
and authentic-iid provenance limitations remain explicit.

### If both norm alternatives are reported/selected

Using two independently delta/8-budgeted norm constructions and then choosing
the better one cannot simply reuse a single delta/8 union allocation. For the
ACTUAL finite six-round acquisition prototype there is a separate sufficient
accounting: the column lower-tail proof spends at most delta/16 (not its
reserved delta/8); coarse and covariance-pilot events each spend delta/8;
the two new norm families each spend delta/8; and each of the quadratic/fine
round families spends at most (delta/4)*(6/7). Their sum is

    delta [1/16+1/8+1/8+1/8+1/8+2*(1/4)*(6/7)]
      = (111/112) delta < delta.

A receiving implementation using this JOINT assertion must bind the actual
six-round cap and the original schedules, and must not require the old
per-action norm event as well. Old norm work remains paid; its correctness
is unnecessary to the new family proof. No posterior-on-PASS assertion is
made. Without this finite-cap refinement, use only a prespecified one of
the new norm events, or split their confidence budgets before acquisition.

### Compatible future task interface

The operator event itself does not depend on a future block-constant terminal
reward or block-uniform initial probability. Consequently the same proof
covers every b=Z b_bar with ||b_bar||infinity<=1 and every ell= W^T mu_bar
for a probability mu_bar, simultaneously and without another statistical
union. This is a restricted learned task language, not arbitrary future
microscopic observables. If a new reward/initial law is supplied as n-state
data, checking the stated compatibility and reading it costs O(n); if it is
supplied directly over the already acquired blocks, reading costs O(r).
The source partition was acquired before this task language is exposed.

Each new terminal reward still pays its ordinary O(L m r²) Bellman planning
and integer bit costs. An initial-state simulator may sample an indicated
block by rejection using the retained map (expected 1/pi_g trials), or pay
to store/acquire an inverse membership table. Neither a free rare-block
sampler nor a physical sensor is inferred. The numerical fixture first uses
the original source/target task; broader compatible task tests are separate.

## 3. Uniform finite-horizon policy-value certificate

Apply the accepted mixed-norm theorem to this new finite operator family.
For every sequence pi_1,...,pi_L, including a sequence selected after seeing
the learned model, the expected terminal value differs from its coarse value
by at most

    E = ||ell||1 ||b||infinity
        [L d + e_out sum_(j<L) t_j],
    t_0=0, t_(j+1)=min(1,alpha_feedback*t_j+e_in,feedback).

Each randomized one-step Markov block policy is a convex combination of the
deterministic one-step maps (choose each block's action independently).
Norm, row-error and leakage bounds are convex, so the same certificate
extends to randomized time-dependent Markov block policies if desired.

## 4. Paid dynamic programming and regret

Let v_0=Wb. Ordinary backward induction computes

    v_t(g)=max_a sum_h B_a[g,h] v_(t−1)(h)

and stores a maximizing action for every pair (t,g). This costs O(L m r²)
scalar products and Lr action choices, plus exact comparison arithmetic.
It gives the optimal coarse value for any initial coarse distribution and
for the above class. If pi_hat is its policy and pi_star any true policy in
that class, the uniform certificate gives

    value_true(pi_star) <= value_coarse(pi_star)+E
                       <= value_coarse(pi_hat)+E
                       <= value_true(pi_hat)+2E.

Thus E<=epsilon gives 2epsilon regret WITHIN THE STATED CLASS, not against
all microscopic or history-dependent policies. The planner actually has to
run; this conclusion does not follow from the prediction rank alone.

Here empirical B entries have known rational count denominators. Acquire
and pay their common denominator D (using an exact lcm). In the indicator
fixture, integer DP values at stage t can use denominator D^t and numerators
between 0 and D^t. Integer bit lengths grow as t log2(D), explicitly measured;
the acquired fine model is not treated as free exact-real arithmetic. No
numerical approximation to the Bellman maximizer is needed. If the reported
value is rounded, its output rounding is separately added to its interval,
not silently included in the exact-policy regret.

## 5. Complete receiving and execution costs

The retained partition map needs n*ceil(log2 r) packed bits (8192 bits for
n=4096,r=4), in addition to the coarse matrices, certificates and observations.
The policy table needs Lr*ceil(log2 m) bits (96 bits here). Initial-state and
terminal-reward interfaces, microscopic label registers and metadata are
additional. The 468-byte coarse hot model is NOT the complete policy machine.

A hypothetical simulated episode of L transitions pays one initial draw
from the explicitly provided ell interface, L forward-source calls, L block
lookups, L action lookups and L destination-label updates. Physical sensing,
actuation, hardware fault tolerance and any plant-model mismatch are outside
this offline simulator construction. No equipment is operated by this work.

The polynomial acquired residual comparison replaces exponential norm
enumeration in the current admission route; its entries, common norm and
fresh-probe arithmetic are actually paid, not premises. The historical
enumeration remains in the cumulative experimental cost ledger. This
sufficient comparison can fail conservatively; it is not optimal recognition. Ordinary reduced-
MDP, bisimulation and model-based planning methods get the same acquired
certificate, data and retained work. Prior matching and comparative utility
remain separate questions, not established by a Bellman calculation.

## 6. Current receiving boundary

`replay_polynomial_feedback.py` first receives the frozen open-word record
and counts under externally supplied task, horizon, tolerance, confidence
and action-count parameters. The exact source bytes/hash are also externally
bound. It then reconstructs all m r² local count matrices, corrects each
normalizer, replays the stored integer probes including their error budgets,
checks U and its exact PSD norm bound, recomputes E, and re-executes exact
Bellman DP. It checks the actual packed map, policy and task bytes. This is
a typed scientific receiving API with assertions enabled, not a hostile-JSON
security service or an authentication protocol.

The final receiver prespecifies the POLYNOMIAL route, using its slightly
larger E. It does not select the smaller enumeration bound. Accordingly it
does not need the optional joint 111/112 confidence refinement. The old
per-action norm arithmetic is replayed as part of the base record, but that
norm's statistical correctness is not used in the new family theorem. The
original simultaneous observation/leakage/fine events remain valid even if
an old heuristic norm affected the stopping round. No posterior-on-PASS
confidence claim is made. Fresh iid source samples, fixed-before-validation
support/sample schedules and independently fresh probes remain external
provenance premises. Mock seeded generation is not evidence of those premises.

The final output is exact rational. Decimal values are display diagnostics,
not extra rounded-value certificates. Received cost fields cover sparse
integer products separately from projection work, allocation, serialization,
big-integer comparisons, exact lcm/PSD work and source-oracle execution. The
logical billion-sample aggregate fixture does not execute billions of named
individual source queries.
