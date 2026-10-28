# Positive return events acquire a rank-one residual certificate

28 October 2026. Classical killed reversible Markov sources, one
distinguished reset state, and an accurate nonintrusive membership predicate.
The source norm cap is an external premise. Hidden-state identities and
hidden dimension are not given to the learner.

## Exact event and renewal identities

Use the common reversible similarity transform to write the self-adjoint
contraction A in boundary/hidden coordinates as

\[
A=\begin{pmatrix}t&d^T\\d&B\end{pmatrix},\quad b=e_0,\quad
D=(A-t)b=(0,d)^T,\quad \|A\|\le a<1.
\]

Similarity factors telescope along return paths, even for nonuniform
reversible weights. Thus f(n)=<b,A^nb> is the ordinary return probability.
For every k>=0,

\[
g_k=D^TA^{2k}D
=\Pr_b(X_{2k+2}=b,\ X_1\ne b,\ X_{2k+1}\ne b).
\]

This follows by deleting the b coordinate from the first and last
intermediate states in the path sum. At k=0 the first and penultimate
states coincide; the identity remains g_0=f(2)-t^2. In general
g_k=f(2k+2)-2t f(2k+1)+t^2 f(2k).
The positive event measures this quantity without subtracting noisy moments.

Let r_l be the probability of a first return at time l>=2 after an initial
departure. Then r_l=d^TB^(l-2)d. Define

\[
r=\sum_{l\ge2}r_l,\quad
s=\sum_{l\ge2}(-1)^l r_l,\quad
r_{\rm even}=(r+s)/2.
\]

Crucially, s=d^T(I+B)^-1d>=0, because I+B is positive definite.
It is valid to square an acquired nonnegative upper bound for s.
The block inverse formulas at +1 and -1 give

\[
\boxed{
Q=D^T(I-A^2)^{-1}D
=r_{\rm even}
+\frac{r^2}{2(1-t-r)}
+\frac{s^2}{2(1+t-s)}.}
\]

Both denominators are positive and at least 1-a. For example
1/(1-t-r)=<b,(I-A)^-1b><=1/(1-a).
This is a rank-one Schur-complement/renewal identity, not a hidden-rank
assumption. It estimates Q exactly from first-return parity probabilities.

## Finite censoring and confidence

If first-return observation stops at physical time H, the missed total
return mass satisfies

\[
0\le r-r_{\le H}
\le \frac{a^{H-1}\|d\|^2}{1-a}.
\]

A separate two-step pilot acquires ||d||^2 as the positive first-departure,
immediate-return event. Its upper confidence bound selects H. A fresh
main batch then estimates total/even/odd first-return events at this
fixed conditional horizon. Stop at the time-1 self-loop or the first
return. A silent cemetery cannot be recognized: censored trials are
charged through H, even when the software backend skips absorbed updates.

For X successes in N independent trials and ell>0, the one-sided mean
envelopes used are

\[
\mu_U=X+\ell+\sqrt{\ell^2+2\ell X},\qquad
\mu_L=\max(0,X-\sqrt{2\ell X}).
\]

Each excluded tail has probability at most exp(-ell). The pilot-dependent
horizon is legitimate because the main batch is fresh. All first-step
bits can be pooled for model calibration: the total sample count is fixed,
and each first step is an independent reset trial regardless of its later
stopping rule. Estimate the rare departure probability q=1-t, rather than
applying a variance-blind bound to the abundant self-loop indicator.

The implementation uses six one-sided bounds per primitive: pilot upper,
departure lower/upper, main total upper, even upper, and odd lower.
For two primitives and ell=10, joint failure is at most 12 exp(-10)<0.001.
Shared missed-tail mass is added once to each relevant event bound.

For the estimated coefficient t_hat, the weighted residual obeys

\[
\sqrt{Q_{\hat t}}\le\sqrt{Q_t}
+|\hat t-t|/\sqrt{1-a^2}.
\]

The root's dissipation certificate uses theta_i^2<=Q_(t_hat,i)/(1-t_hat_i^2).
Its all-word correction-noise term is at most
max_i delta_t,i/(1-t_hat_i^2). Thus the reported final upper bound is
2 max_i theta_i^2 plus this correction-noise envelope.

## Executed receipts and complete costs

The private fixtures are P0=[[1-g,g],[g,1/4]] and
P1=[[1-2g,g],[g,1/3]], with a=1-g/2 supplied as a source premise.
Only counts, membership flags and return times enter the learner.
renewal_acquisition.py executed integer-random trajectories.

At g=1/20, 20,000 pilot and 100,000 main return trials per primitive,
with two million pooled first steps per primitive, selected horizons
298 and 301. The final all-word bound is 0.0935512330. The complete charge
is four million logical trials, at most 299,190 physical preparations, and
8,192,273 primitive steps and predicate readings.

At g=1/100, 100,000 pilot and 500,000 main return trials per primitive,
with the same two million pooled first steps per primitive, selected
horizons 1881 and 1891. The final bound is 0.0493141119. The charge is
four million logical trials, at most 60,242 physical preparations, and
32,037,095 primitive steps and predicate readings.

An independent Fraction replay, replay_renewal_exact.py, recomputes pilot
radii, exact rational horizon tails, return envelopes, model radii and final
certificates using enclosing rational square roots. Every displayed
Decimal envelope dominates its exact replay. The exact certificates are
preserved in RENEWAL_EXACT_REPLAY.json; the finite receipt does not rely
on an unproved floating-point slack allowance.

compare_renewal_flags.py executes or replays the root's randomized residual
flags with the same variance-aware departure calibration.

| g | Method | All-word upper | Logical trials | Preparation upper | Primitive steps | Predicate readings |
|---|---|---:|---:|---:|---:|---:|
| .05 | Short residual flags | .09190317 | 4,000,000 | 299,681 | 6,452,016 | 4,587,663 |
| .05 | Censored renewal | .09355123 | 4,000,000 | 299,190 | 8,192,273 | 8,192,273 |
| .01 | Short residual flags | .04263276 | 24,000,000 | 359,737 | 27,168,692 | 24,716,036 |
| .01 | Censored renewal | .04931411 | 4,000,000 | 60,242 | 32,037,095 | 32,037,095 |

A known b endpoint starts the next trial without physical preparation.
The strong Markov property preserves the trial law. For renewal the
preparation charge, including terminal restoration, is
1+departures-first_returns per source, with the analogous pilot and
one-step terms. For fixed flags the saved data guarantee only the upper
1+departures-positive_flags: additional failed flags may also end at b.
The first version of this ledger incorrectly called every logical trial
a physical reset. That overstatement has been corrected in code and data.

At g=.05 the fixed flags use fewer transitions and readings at a slightly
better error bound, with comparable preparation upper bounds. At g=.01,
both meet error .05. Renewal adds 4,868,403 primitive steps and 7,321,059
predicate readings while reducing the recorded preparation upper bound
by 299,495. Comparing these upper ledgers gives a crossover
R>16.2554 A+24.4447 M, where R,A,M are preparation, transition and reading
costs. This is not a proved hardware-cost victory: the flag preparation
upper may be conservative. No unconditional dominance is established.

The residual event probabilities are Theta(g^2), so renewal residual
acquisition needs O(g^-2 log(1/delta)) trials. With a finite norm-based
horizon and early rejection, its primitive cost is
O(g^-2 log(1/g) log(1/delta)). But an O(g) complete all-word error also
requires delta_t=O(g^2), because correction noise is delta_t/(1-t^2).
Variance-aware first-step calibration then costs O(g^-3 log(1/delta)).
The full pipeline therefore does not inherit a g^-2 sample-rate claim.
With known-b continuation, actual preparation demands scale as
q times these trial counts, so the model-calibration preparation count
can be O(g^-2) even though its transitions and logical records cost O(g^-3).

## Antecedent and actual scope

Aldous and Fill, Reversible Markov Chains and Random Walks on Graphs,
Section 2.5.2, Lemma 2.25, records the first-hit/Green-function generating
identity and its renewal proof:
https://www.stat.berkeley.edu/~aldous/RWG/Book_Ralph/Ch2.S5.html .
The parity formula above is ordinary renewal/Schur-complement algebra.
The scoped addition is its use to acquire the particular physical
inverse-dissipation residual needed by the switching certificate.

Accurate nonintrusive membership is stronger access than endpoint-only
scalar reads. Its calibration and the common norm cap are not acquired
by this experiment. The result does not create positive flags for arbitrary
signed dictionaries, and does not justify inserting measurements into an
unknown quantum evolution. No physical hardware was operated.
