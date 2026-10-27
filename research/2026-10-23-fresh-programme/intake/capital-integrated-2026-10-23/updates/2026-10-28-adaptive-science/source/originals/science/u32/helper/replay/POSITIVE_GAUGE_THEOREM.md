# Count-certified positive predictive gauges

This is a sufficient observable confidence certificate, constructed and tested
here. Its ingredients are positive realizations, interval linear algebra and
coupling of finite-state kernels. Historical novelty and an advantage over an
equally informed positive HMM learner are not established. It does not solve
the general unknown-CP-instrument acquisition problem.

## 1. Supplied interface and exact coordinates

Use S7's finite legal action/outcome library, stationary CP instruments,
repeatable whole-process starts, and supplied architectural upper bound r on
the minimal observable rank. There is no latent state, Kraus, physical gauge,
or exact expectation oracle. Choose r normalized legal preparations p_j by
discarding their outcomes; p_1 is the empty preparation rho_0. Choose r legal
future event tests including trace. Let H contain their joint probabilities,
and H_z their shifted joint probabilities for z=(a,o). All confidence events
cover the entire candidate pool before any data-dependent choice.

On the simultaneous count-confidence event suppose H is nonsingular. The
rank upper bound certifies that its preparations span the observable quotient
V. In preparation coefficients c, the exact instrument is

    C_z = H^{-1} H_z.

This follows by testing the r physical core states, then extending by linearity.
The trace functional is 1^T because all core preparations are normalized.
The actual initial state has coefficient e_1 exactly, not an estimated mean.

Choose an invertible real matrix S with 1^T S=1^T. Its columns specify virtual
states in preparation coordinates; negative entries are allowed. Put

    W_z = S^{-1} H^{-1} H_z S,       c_0 = S^{-1} e_1.

If c_0>=0 and every W_z>=0 entrywise, this is an exact positive realization
of the entire legal process. Indeed sum_o 1^T W_(a,o)=1^T by true causality.
Starting at c_0, products have nonnegative coordinates and exactly the true
word probabilities. After every positive-probability legal history the
normalized coordinate is in the simplex. Induction also covers feedback:
both processes choose the same action at the same observed prefix.

The virtual vertices need not be positive physical density matrices. A finite
positive *predictive* realization is enough to give the correct classical
process from the certified initial state. No claim of a physical CP map from
virtual classical labels is made. Every actual reachable history from rho_0
is covered, but additional externally supplied states or controls are not.
For subnormalized core preps, replace 1^T S=1^T by m^T S=1^T throughout.

## 2. Computable interval certificate

Let hats denote rational count estimates, and let nonnegative matrices D_H,
D_z satisfy the simultaneous entrywise bounds

    |Hhat-H|<=D_H,       |Hhat_z-H_z|<=D_z.

Known trace/all-outcome probabilities have zero width. Define

    Vhat = Hhat S,       D_V = D_H |S|,
    U = Vhat^{-1},       A = |U| D_V.

If rho(A)<1, the entrywise inverse bound is

    |(H S)^{-1}| <= M := (I-A)^{-1}|U|.                 (2.1)

Proof: H S=Vhat+E with |E|<=D_V. Expand
(I+U E)^{-1} U as a Neumann series, take absolute values termwise and
sum the nonnegative series. This also proves true nonsingularity. The
stronger, simpler sufficient check ||A||_infinity<1 is used by the rational
replay; no floating eigenvalue decision is a proof premise there.

For raw fitted maps What_z=U Hhat_z S, the exact residual identity gives

    |What_z-W_z| <= E_z
      := M [D_z |S| + D_V |What_z|].                   (2.2)

The identity is (HS)(What-W)=(Hhat_z-H_z)S
 +(HS-Hhat S)What. It is exact, with no commuting matrices or hidden
replacement of a product norm. For any separately repaired fit What, add
|Vhat What-Hhat_z S| inside the brackets. This charges the actual repair.

Thus What_z-E_z>=0 certifies the *true* positive gauge. Fitted nonnegative
maps with exact branch-summed column sums one give a valid causal simulator.
All checks use counts, selected S and finite matrix arithmetic. Selecting S
after the simultaneous confidence event needs no additional statistical
selection penalty. Failure of the check returns UNKNOWN; it is not evidence
that no other positive or quantum realization exists.

The certificate still pays inverse-core information costs through M and the
transformed widths. It avoids the additional physical quotient-norm conversion
because contraction is now proved directly in a certified positive coordinate
cone. It does not erase an ill-conditioned core or unseen modes.

## 3. Sharp local uncertainty in a simplex

For each action a and current virtual state j, concatenate the fitted vectors
What_(a,o)[:,j] over outcomes into a probability vector p. The true vector q
lies in the box [l,u], obtained from (2.2), and in the probability simplex.
Its maximum TV distance from p is exactly

    t_(a,j) = max_(B subset of coordinates)
       { min(sum_(i in B) u_i, 1-sum_(i not in B) l_i)
                               - sum_(i in B) p_i }.  (3.1)

Proof: TV(p,q)=max_B(q(B)-p(B)). For fixed B, the maximum feasible q(B)
is min(u(B),1-l(B^c)); feasibility of the box-simplex intersection ensures
that this mass can be distributed inside the individual bounds. Interchange
the two finite maxima. This avoids summing incompatible separate deviations.
For large alphabets the elementary bound t<=one-half sum_i max(|p_i-l_i|,
|p_i-u_i|) avoids subset enumeration. Our four-coordinate replay enumerates
all sixteen subsets exactly. Correlations between uncertain entries can
only shrink the feasible set, so the box outer approximation is sound.

Put t=max_(a,j)t_(a,j), clipped at one. The true and fitted models, started
at the same simplex state, admit a stepwise coupling: while their virtual
labels and observable histories agree, choose the same action and maximally
couple the joint (outcome,next-label) kernels. A mismatch has probability
at most t. The models remain positive and normalized on all branches.

For H native steps, the complete classical transcript therefore satisfies

    TV <= 1-(1-t)^H <= H t.                            (3.2)

This is a full-law result, not moment matching. It is uniform over feedback
policies selected after the data and over initial simplex states shared by
the two models. It does not imply uniform normalized posterior accuracy at
every rare history: conditioning still pays inverse event probability.

## 4. Clocked operations and memory-retaining reuse

Before every native attempt force an independent known abort coin delta,
gamma=1-delta, retaining physical memory on abort as in S7. For an arbitrary
finite classical controller, native success can only shorten execution.
While the coupled models agree, termination before their first mismatch has
probability at least

    delta sum_(n>=0) [gamma(1-t)]^n
      = delta/(delta+gamma t).

Hence the entire terminal classical transcript, including all intermediate
outcomes and terminal labels, obeys

    b = gamma t/(delta+gamma t).                       (4.1)

Unlike the signed-resolvent estimate, no smallness condition gamma e<delta
is needed: both acquired models are valid positive processes. A one-state
source always producing zero, compared with a one-state model producing one
with probability t, attains (4.1). The mismatch is the observable occurrence
of at least one one before the shared abort.

For M sequential adaptive invocations, carrying the same retained memory
and allowing each controller to depend on the entire previous record,

    TV(joint complete transcripts) <= 1-(1-b)^M.        (4.2)

Condition on agreement so far and apply the same lower bound 1-b to the next
invocation; multiply. No independence of physical macro outputs is asserted.
If native terminations occur, they only improve the bound. There are at most
gamma/delta expected native calls per invocation and tail gamma^n after n
attempts. Starts, actuation, reads, count processing and fit arithmetic remain
charged separately.

This also couples the final abstract HMM labels. It does not certify the
trace distance of actual physical quantum memories, an external coherent
reference, or arbitrary newly introduced interventions. Every subsequent
legal classical continuation is included by extending the transcript. For
an event A of true mass p>0, conditional predictions require their own
normalization bound; joint error b alone is not a bound independent of p.

## 5. Nonvacuous regime and actual experiment

The class is open whenever a finite positive realization has a strict branch
margin and the chosen core is nonsingular. Count widths go to zero, so (2.2)
eventually proves positivity with finite counts. This is stronger than
empirically observing positive fitted entries: uncertainty is subtracted
before accepting a cone. For fixed r and margin m, the sufficient Hoeffding
shot count scales quadratically with the transformed inverse sensitivity
divided by m and logarithmically with the declared confidence-pool size.
The ordinary positive HMM learner can use exactly this construction.

The executed fixture is a rank-two, diagonal, stationary CP instrument, not
laboratory data. generate_counts.py samples full reset episodes into integer
tables; learner.py and exact_certificate.py import no plant. There are seven
legal action settings, one million shots each, totaling 7,000,000 resets and
14,000,000 native interventions. The 18 declared joint-event probabilities
have rational width 21/10000, giving simultaneous failure probability at most

    36 exp(-441/50) = approximately 0.00531894097.

The selected S has diagonal 5/4 and off-diagonal -1/4. Exact rational replay
finds positive lower margin 30002740030003/1430111088800000, approximately
0.0209793, and local TV t=4121523/210355000, approximately 0.0195932. With
delta=2/5, one whole operation has b=12364569/433074569, approximately
0.0285507; two adaptive retained-memory invocations have joint bound
10556678214535761/187553582314535761, approximately 0.0562862.

The S7 quotient-norm calculation on these same counts gives joint primitive
error e approximately 0.590707. With gamma=0.6 and delta=0.4 its signed
resolvent bound is approximately 7.80 and therefore vacuous as TV. This is
a comparison of sufficient certificates on this fixture, not a comparison
against an optimized conventional learner. Positive HMM fitting can reproduce
the new certificate exactly; no statistical or computational separation is
proved. The fixture is different from S8's original qubit experiment, so its
shot totals do not establish an acquisition-cost advantage over that fixture.

Post-acquisition scoring, separately importing the private plant, evaluates
the complete finite transcript tree with a Bellman recursion maximizing over
every feedback action at each prefix. At ten total native calls, the worst
clocked one-macro transcript TV is approximately 0.0008181. This is a numerical
full-law diagnostic of that finite fixture, not the confidence proof. The
proof is the exact interval certificate plus (4.1). Floating scoring does not
replace the rational count-only proof or certify arbitrary CP processes.

The original frozen rank-four qubit counts were also re-read at their exact
pinned commit. A declared uniform-expansion family of simplex gauges fails
raw positivity and therefore returns UNKNOWN. This finite search does not
prove that the fixture has no positive realization. The coherent obstruction
in COHERENT_OBSTRUCTION.md shows why this architecture cannot be universal,
even with infinite exact observations. A general quantum observable confidence
geometry, or a different acquired representation, remains necessary.
