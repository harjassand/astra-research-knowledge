# A sharp correction threshold before local–global Monte Carlo

## Scientific decision

I accept the received completion of the joint-KL theorem and close the
previous J>K question. Its exact coefficient is max(K,(1-alpha)J) under
the original fixed lazy reversible mixture contract. The supplied proof
and review are preserved unchanged; the source recovered from the packet
is byte-identical to my previous archive.

I then pursued a distinct consequence: how much ordinary independence-MH
correction must precede local updates to protect the proposal initialization?
This checkpoint establishes a full threshold theorem. It identifies the
precise uniform error that can remain after a fixed prefix, determines
the minimum prefix allowing any finite uniform guarantee, and shows that
a prefix within one candidate of that minimum restores the ordinary
independence sampler's sharp exponential coefficient.

This is foundational sampling knowledge. It is not a new sampler,
application adoption, finite-time speedup or claim of historical priority.

## Exact operation and information

The target pi and proposal q are equivalent, W=dpi/dq, G is ordinary
independence MH, and L is any fixed pi-reversible kernel. Alpha is fixed
strictly between zero and one, beta=1-alpha, and
C=(I+alpha G+beta L)/2.

The whole algorithm starts with one q draw, makes N-1 global MH
transitions, and then t fixed lazy-mixture steps. Its law is
q G^(N-1) C^t. N counts all prefix proposal candidates, including
initialization. The prefix uses unnormalized target/proposal ratios;
no unknown normalizer must be evaluated.

The first new theorem assumes only the certified population forward
budget D(pi||q)<=K. This is an explicitly different contract from the
accepted theorem with both budgets. Reversibility, fixed alpha, fixed L,
laziness and the initial q draw remain. The second consequence restores
the reverse budget D(q||pi)<=J and needs only one preliminary G transition.

## Main new result

Write b_K=1-exp(-K), lambda_K=-log b_K, and
gamma=(1-alpha)/(1-alpha b_K). For every fixed positive integer N,
the supremum of TV error at time t over the forward-KL class has limit

    F_N = gamma b_K^N.

This is a worst-case uniform floor. Individual admitted finite chains
can converge; their convergence times are not uniformly controlled below
the floor. The theorem gives the exact existence criterion:

    a finite uniform post-prefix mixing time exists iff epsilon > F_N.

Equality fails too. For every finite t, an admitted positive three-state
chain can remain strictly above F_N. The proof uses nearby strict parameters,
not an inadmissible reducible endpoint.

Therefore the smallest candidate count permitting a finite uniform time is

    N_crit(epsilon)
      = max(1, floor(log(gamma/epsilon)/lambda_K)+1).

The safe rule

    N_safe(epsilon)
      = max(1, ceil(log(gamma/epsilon)/lambda_K)+1)

uses at most one additional candidate and gives F_N <= b_K epsilon.
For this rule the worst-case subsequent time satisfies

    lim epsilon log T_safe(epsilon) = K.

The leading prefix length is consequently
log(1/epsilon)/[-log(1-exp(-K))]. At large fixed K this coefficient
grows like exp(K); the logarithmic dependence on accuracy does not make
initialization cheap uniformly in K.

## Why the proof works

The received near-harmonicity lemma controls every bounded evolved
observable g=C^t 1_F pointwise, including where the starting density is
unbounded. The new construction uses an exact equation on
D={W<1/B}: a global proposal leaves D precisely when the proposal itself
lies outside D. Its total stay probability is b=q(D).

The resulting low-set equation can be solved in sup/inf bounds. Its
oscillation relative to the fixed anchor contracts by
beta/(1-alpha b). This denominator retains repeated global redraws into
the low-weight set, which give repeated chances for local capture.
Treating those events as an O(b^2) error loses the exact forward-only floor.

The prefix law has another exact decomposition: on the event that a
candidate first exceeds a weight threshold h, it is accepted certainly.
That first accepted high candidate has density at most 1/h relative to
pi, and subsequent invariant transitions preserve the bound. The event
that all N candidates lie below h has probability b_h^N. This proves

    mu_N(W<1/B)
      <= b_h^N + [pi(W<1/B)/h] sum(j=0,...,N-2) b_h^j.

Forward KL bounds b_h by an explicit envelope tending to 1-exp(-K).
The prefix output is also one of N iid candidates, so mu_N<=Nq.
That fact supplies a controlled core multiplier for the anchored
Dirichlet argument.

The full finite-time inequality keeps the maximum of the dangerous
low-tail contribution and the target's high-weight tail, with explicit
small errors. It does not assume that the prefixed signed density has
the same signs as the original q-pi.

The matching lower family has a low-weight entrance, a rare high-weight
trap and a bulk state. Its exact prefix entrance mass approaches b^N.
The limiting local/global competition captures a fraction
beta rho/(1-alpha b), yielding the same floor as b approaches its
entropy endpoint and rho approaches one. All admitted approximating
chains remain positive and reversible. A separate two-state L=I family
retains the lower exponent K after every subexponential prefix.

These arguments, their hypotheses, constants, endpoint order and
uniformity are fully written in PREFIX_THEOREM.md.

## Joint KL consequence and the strongest ordinary comparator

Under a fixed reverse-KL budget, the probability of very low weights
already vanishes at order 1/log t. One preliminary global MH transition
squares the remaining dangerous prefix event, making it lower order.
Hence every fixed N>=2 has sharp coefficient K.

For K=1, J=4 and alpha=1/2:

| Operation | Leading epsilon log worst-case time |
| --- | ---: |
| Pure proposal-start independence MH | 1 |
| Original q-start lazy hybrid | 2 |
| One global update, then the same lazy hybrid | 1 |

For general parameters the original hybrid coefficient is max(K,beta J),
while the prefixed coefficient is K. Thus the improvement is strict at
the exponential scale only when beta J>K.

Pure IMH remains the strongest ordinary baseline used here. Existing
finite-support theory also establishes its same-budget dominance over
ordinary SIR in every convex f-divergence. This work does not replace
that comparator with a weaker initializer.

The full operation uses N prefix candidates and, at fixed t, an expected
alpha t/2 further global proposals and beta t/2 local transitions.
It adds local work while matching pure IMH's exponent. No inequality
asserts finite-time dominance or a wall-clock advantage. A rule stopping
after an exact number of global proposals would have a different random
time law; it is not obtained by substituting an expected count.

## Actual calculations

At K=1 and alpha=1/2, the computed constants are
b_K approximately 0.632120559, gamma approximately 0.731058579, and
1/lambda_K approximately 2.180192256.

| Requested epsilon | Minimal N for any finite guarantee | N in safe rule | Prefix MH updates in safe rule | Uniform floor after safe prefix |
| ---: | ---: | ---: | ---: | ---: |
| 0.1 | 5 | 6 | 5 | 0.0466392620 |
| 0.03 | 7 | 8 | 7 | 0.0186359485 |
| 0.01 | 10 | 11 | 10 | 0.00470707639 |
| 0.003 | 12 | 13 | 12 | 0.00188083664 |
| 0.001 | 15 | 16 | 15 | 0.000475062581 |

These prefix counts establish eligibility for a subsequent mixing
guarantee. They do not say that the prefix alone reaches the requested TV.

The principal also evaluated the explicit finite-time certificate and
the ordinary pure-IMH coupling certificate, each targeting a bound at
most 0.95 epsilon. The chosen integer log budgets x mean
t=ceil(exp(x)); these times were not executed:

| epsilon | Safe-prefix hybrid certificate x | Pure-IMH certificate x |
| ---: | ---: | ---: |
| 0.1 | 34 | 18 |
| 0.03 | 76 | 44 |
| 0.01 | 166 | 116 |
| 0.003 | 439 | 364 |
| 0.001 | 1171 | 1068 |

These are conservative sufficient bounds, evaluated with rounding.
They are not actual mixing times or a performance ratio. They demonstrate
why equality of asymptotic exponents should not be sold as practical
acceleration. In every evaluated case the hybrid certificate is worse.

Independent exact-rational checks covered 1,200 first-high decomposition
and tail cases on 30 positive chains; 75 repeated-competition cases
with 240 exact comparisons; and 15 integer-boundary cases. The principal
computed the scalar tables at 80 decimal digits, then checked 120 digits.
All integer counts and selected log budgets agreed; 127 numerical values
had maximum absolute difference about 2.38e-74.

The scientific proofs carry the universal conclusions. Finite diagnostics
test implementation and constants, not mathematical universality.
There is no empirical holdout claim: no fitted model or scientific dataset
was selected or evaluated in this mathematical continuation.

## Observed resources and limits

Original new execution receipts report:

| Calculation | Wall seconds | CPU seconds | Peak RSS KiB |
| --- | ---: | ---: | ---: |
| Exact prefix decomposition and tails | 0.205299 | 0.205293 | 9344 |
| Exact repeated-competition formula | 0.016808 | 0.016806 | 8960 |
| Exact integer-boundary checks | about 0.00848 | about 0.00848 | 8832 |
| Principal 80-digit scalar evaluations | 0.047749 | 0.047751 | 11136 |
| Principal 120-digit consistency check | 0.062977 | 0.062978 | 11136 |

The separate relocated replay receipt records its own additional cost.
Peak RSS values are process observations, not additive memory totals.
Model reasoning, full interaction cost and monetary charges were not
measured. No hardware purchase, accelerator job, installation, outreach,
or empirical campaign was initiated.

The mathematical transitions are ideal-real kernels. The scalar
calculations are rounded Decimal evaluations, not formal interval
certificates and not validation of a floating-point sampler's exact law.
Certified population KL remains an input assumption.

## Review, failures and continuation

Distinct contributors checked the exact prefix decomposition and new
low-set equation, supplied the matching lower floor including equality,
and verified the changing-N asymptotic bridge. The final upper review
is bound to the exact principal source hash. Historical novelty and
external mathematical acceptance remain unestablished.

The important failures are preserved: a naive single downward-crossing
argument is invalid; first-step capture misses repeated competition;
the actual low-tail mass is not its worst-case envelope; and a
fixed-N limit does not automatically apply to growing N. The exact
minimal-prefix boundary with vanishing slack is not given a sharp
cost theorem; the safe rule explicitly avoids it.

The next chosen question is whether observed proposal weights can
support a shorter *stopped global prefix* on easy instances while
retaining the same worst-case guarantee. The first step is a lower
bound with the certified K retained and the information contract made
explicit. The existing rollout-only certification barrier is a real
obstacle, not a new discovery to reproduce. No adaptive guarantee
has been claimed.

B3's pISO correction and failed full-halo inference remain intact;
the other metadata case and R3/anMC rejection stay closed. This
checkpoint does not reopen those operations or any other owner's
construction. Max retains integration ownership, and the same exact
source is supplied privately to Max and the evaluator.
