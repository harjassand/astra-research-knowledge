# Review: calibrated observable program and patched signed-clock theorem

29 October2026. Actual internal mathematical review by the complementary
record-geometry researcher. No external peer review, formal verification,
apparatus test, or historical-priority determination is implied.

Reviewed robust-program proof SHA256:
`70c6946997e53e49a114a85ba4050db1b260c550d6f4329c434fc14c29cf4ec5`.
Reviewed patched signed-continuation proof SHA256:
`658fc39e1a991ab34669cd702b37b8cf93216b2ca7fa35d2fd52d54d2cbafb2a`.
Both exact snapshots are retained in this directory.

## Verdict

ACCEPT the robust receiver, its same-device calibration supplier, probability
rounding, and stated ideal-model costs. ACCEPT the patched signed-continuation
proof and its stronger common-joint-clock-law wording. No load-bearing error
was found. One explicit initial-distance clause is recommended for the joint
old-record extension; it makes the intended conditional coupling unambiguous
without changing either displayed consumer bound.

The root executable was still under construction when this mathematical
review was performed; it was NOT rerun or accepted by this receipt. The
independent analytic numerical check is a separate small JSON in this folder.

## 1. Column-sum contraction and normalization

Let D be the current unnormalized Hamming disagreement. Conditional on the
coupled configurations x,y, a common uniform selected site gives ideal
expected disagreement

    D - (s/d) sum_j 1_{x_j!=y_j}
      + (s/d) sum_j [sum_i c_ij] 1_{x_j!=y_j}
    <=[1-s(1-alpha)/d]D.

Thus the COLUMN sum in the governing premise is the correct one for the
unweighted Hamming metric. It is not silently replaced by the more familiar
row-sum convention. Adding a maximal coupling between the actual endpoint
row and the ideal row at x contributes delta_i at site i, hence delta_bar
after averaging the site. Dividing by d gives the normalized recursion

    w_(t+1)<=rho w_t+delta_bar/d.

Its geometric sum is precisely equation(2), since
1-rho=s(1-alpha)/d. There is no missing factor d in its error floor.

The coupling can depend on the complete actual hidden history, provided the
actual row premise holds conditional on that history at the macrostep start,
BEFORE its new selector randomness. The ideal chain still has the correct
marginal transition kernel because each coupling has that fixed ideal
marginal. Evolving hidden memory is therefore allowed by the abstract
receiver, while its experimental supplier correctly assumes static H.

Fixed independent uniform site selection is essential. Arbitrary
history-selected sites, stopping times, target changes or feedback using
new key records do not inherit this contraction. The draft excludes them.
The theorem bounds marginal laws at deterministic macrostep t, not one
simultaneous accurate-trajectory event or complete transcript TV.

## 2. Ising constants and observables

Each neighbour influence is1/8 and every column has two neighbours, so
alpha=1/4. With s=9/20 the contraction is1-27/(80d), and the normalized
Wasserstein floor is(80/27)delta_bar.

For spins S_i=2X_i-1, conditional refresh mean is
(S_(i-1)+S_(i+1))/8. This gives the mean-spin recursion and Fourier eigenvalues
in equations(4)--(5) exactly. The zero Fourier mode has the same contraction
factor as the Hamming argument.

A single-site change moves normalized magnetization by2/d and normalized
bond correlation by at most4/d, proving Lipschitz constants2 and4. Equations
(6) follow. Both observables have oscillation at most2, so the failure-event
contribution can be bounded by2 beta for each, instead of the looser L beta.

The stationary/preparation claim follows by comparing to an ideal pi start,
using initial normalized distance<=1. A stationary actual endpoint law, when
it exists under the row premise, inherits the same good-event floor by
letting deterministic t tend to infinity. This does not assert hidden mixing.

## 3. Old records, initial couplings, and postselection

The uniform pointwise calibration event is sufficient even if the retained
history and hidden H are strongly correlated. Conditional on(H,D,Z), the
actual rows on the good event are uniformly close at every visible state.
After integrating, the frequentist failure probability contributes at most
beta in a metric of diameter1. Data-dependent tests f(D,Z,x) are legitimate
when their Lipschitz constants in x are uniform and the two laws retain the
same(D,Z) marginal. No cardinality bound on D or Z is needed.

Recommended explicit clause: for a general joint-record version of equation(2),
its initial term is the AVERAGE CONDITIONAL initial Wasserstein distance,
not merely W(Law(X0),Law(Y0)) after discarding D,Z. One can condition on all
retained records and use

    E_(D,Z) W_norm(Law(X0|D,Z),Law(Y0|D,Z)),

or the corresponding stronger conditioning used in the proof. The displayed
same-initial-state observable bound has initial distance0 under the declared
common coupling; the displayed preparation bound uses the universally valid
initial upper bound1. Both are already correct.

Why the clause matters: let Z be fair, actual X0=(Z,...,Z), and reference
Y0=(R,...,R) for independent fair R. Their marginal visible laws are identical,
so marginal Wasserstein distance is0. Yet the1-Lipschitz test
f(Z,x)=d^-1 sum_i1_{x_i=Z} has expectations1 and1/2. The conditional initial
distance is1/2. This is a counterexample only to reading the joint extension
as retaining the UNCONDITIONAL initial-distance term; it does not challenge
the conditional-coupling proof or either intended consumer.

Coverage is joint frequentist over calibration, not coverage conditional on
every rare realized D. Retaining D is allowed; selecting a subpopulation by
a rare D event is a new conditioning step. If such postselection is used,
its probability and resulting failure inflation must be charged (a simple
bound is beta divided by the selection probability). The draft's explicit
rare-D limitation is correct. Old Z used to formulate the conditional sampling
premise must not covertly encode future calibration innovations.

New primitive keys and intermediate paths may physically remain exposed,
but are not included in the observable metric or allowed to change the fixed
program. Endpoint-row closeness averages the NEW selector at each macrostep;
it does not give closeness conditional on a particular realized new key.
The draft correctly avoids that stronger marked-record claim. Random wall-
time sampling is also correctly separated from macrostep completion.

## 4. Same-device calibration and the actual words

Conditional on the fixed H vector and admissible pre-calibration record,
binary-symmetric source-B increments have the asserted fixed Bernoulli
probabilities independently across calls. The current bit does not affect
the flip probability. Thus repeated calls estimate each deployment site's
actual p0 and p3 without a hidden reset or independent new specimens.
Correlations between different sites' H values do not impair the union bound.

Each of2d scalar means has two-sided Hoeffding failure probability at most
2 exp(-2N eta^2). With eta from equation(8), the total is beta. Clipping to
an interval containing the true parameter cannot increase error.

The high word has actual flip probability r=2p3(1-p3), since its two fresh
increments are independent conditional on H. On[1/4,9/20], r ranges from
3/8 to99/200 and its derivative2-4p3 lies in[1/5,1]. Its estimated error is
therefore<=eta. The low interval ends at3/20, so the fitted bracketing gap
is at least3/8-3/20=9/40. All three required target probabilities lie strictly
inside the common low/high bracket.

For the fitted low weight w, the true endpoint error is
w(p0-p0hat)+(1-w)(r-rhat), of magnitude<=eta. There is no inverse-gap error
amplification in this identity. The gap warrants feasible stable mixing; it
is not used to replace a needed hidden-pointwise bound.

Dyadic rounding with |w_rounded-w|<=2^-b adds at most2^-b to row TV, since
|r-p0|<=1. A fixed b-bit uniform integer and an integer threshold implement
the rounded mixture exactly. The numerator can be computed from rational
count estimates without floating ambiguity. Any endpoint implementation error
must cover the WHOLE one/two-call word and boundary evolution; a per-native-
call error cannot be reused as a whole-word error without composition.

## 5. Costs and independently evaluated finite certificate

Calibration uses exactly2dN native calls. Sharing adjacent endpoint reads on
each site gives d(2N+1) reads. Persistent specimen count is d, with their
actual initial preparation still required. Each later macro uses one or two
native calls, b fresh selector bits, actual site selection and its physical
duration. Other sites must remain isolated throughout those calls and boundary
control. None of these costs are paid by the retained bit count.

For d=4,N=100000,beta=0.01,b=16, independently evaluating the ANALYTIC bounds
gives:

* eta=0.006073614619083051;
* ideal-model row delta=0.006088873408145551;
* good-event normalized Wasserstein floor0.018041106394505336;
* unconditional floor including beta0.028041106394505334;
* good-event magnetization error0.03608221278901067;
* magnetization bound including oscillation2 failure cost0.05608221278901067;
* good-event bond error0.07216442557802134;
* bond bound including oscillation2 failure cost0.09216442557802135.

The calibration counts are800000 calls and800004 endpoint reads. These are
ordinary displayed floating evaluations, not outward-rounded numerical or
metrology certificates. Physical delta_impl is unknown; zero is legitimate
only inside the declared ideal simulation. The bounds are nonvacuous for this
observable objective and uniform over deterministic service horizon.

## 6. Patched signed-continuation proof

The stopping functional is now explicitly capped on ALL reference paths.
The endpoint polynomial section explicitly retains its fixed-duration,
endpoint-only scope. Calibration D now includes retained controller state and
reused seeds, or future randomness is fresh. Boundary-control latency/evolution
is an explicit physical implementation requirement. These changes address the
previous review's requested clarifications.

The patched common-joint-clock-law statement is correct and now uses the
cleanest argument. A common joint law with positive opposite output probability
and almost-sure finite completion would give a positive constant
P_h(tau<=T and O) for some finite T. The bounded stopped-likelihood lemma
makes this event probability holomorphic, and its witness continuation is
negative. The identity theorem gives a contradiction. This does not require a
nondegenerate conditional outcome in every deadline slice, nor a claim that
every conditional dependence pattern changes with h.

## Final scope

The finite-data result now has an appropriate stable receiving objective.
It does not deny that small transition errors remain statistically detectable
in complete long records, and it does not turn an equilibrium L2 certificate
into pointwise control. The supplier actually estimates the persistent
specimens, implements available bracketing words, and keeps its physical and
statistical premises explicit. The mathematics is accepted at that scope.
