# Acquiring and cancelling the hidden response of physical operations

29 October 2026. Astra P1 root construction. This changes the actual execution
interface by compiling available operations into fresh randomized calls. It
does not assert that fitting a model makes original operations memoryless.

## 1. Question and consequence

Can acquired information remove hidden memory's influence on useful controlled
observations, rather than only predict it with a growing model or wait for
microscopic equilibration?

Chronological experiments acquire the relative directions of different controls'
hidden responses. A convex optimization finds a physical mixture cancelling
those directions, subject to useful-transition requirements. A measured
separating direction can instead exclude every allowed mixture. Exact population
cancellation gives a positive finite-state controlled process at all observation
depths, including feedback and retained old records. Strong lumpability,
covariance, convex separation and randomization are established. The candidate
addition is the physical acquisition/synthesis bridge. Historical originality,
an apparatus and practical advantage are not established.

The explicit source below has frozen continuous hidden memory. Each raw
operation has infinite observable linear rank; two compiled calls have an
exact two-state realization. Complete isolated-operation path laws cannot
determine whether cancellation is possible. A second source has identical
individual-operation laws but admits no cancelling mixture. Cross experiments
distinguish them.

## 2. Actual acquisition interface

Let X be a standard Borel hidden state, Y:X->{1,...,k} a finite noninvasive
visible label, and mu a warranted baseline calibration law. Put mu_a=mu(Y=a)>0.
Actual fixed calls T_1,...,T_s are reversible Markov kernels for mu in the main
version. Independent source preparations at mu, switching, specified durations
and fresh native randomness are actual premises.

Define

    f_jb=T_j 1_b,
    K_j(a,b)=E_mu[f_jb |Y=a],
    r_jab=1_a(f_jb-K_j(a,b)),
    H^a_ij=E_mu[sum_b r_iab r_jab |Y=a].                 (1)

H^a is PSD. Individual-outcome Grams H^{a,b} omit the sum over b. These are
squared conditional-mean residuals, not variances of one stochastic report.

In one trial record Y0, execute T_i, record Y1, execute T_j, and record Y2.
Reversibility gives

    L^a_ij=Pr_mu(Y1=a,Y0=Y2)/mu_a
          =E_mu[sum_b f_ib f_jb |Y=a],
    H^a_ij=L^a_ij-sum_b K_i(a,b)K_j(a,b).              (2)

Proof: the b contribution is
<1_b,T_i E_a T_j1_b>_mu=<T_i1_b,E_a T_j1_b>_mu.
One-call joint labels acquire K. Requiring Y0=Y2=b acquires H^{a,b}.
No hidden copying, same-state restart, force oracle or microscopic reversal
appears. At most s(s+1)/2 two-call settings and s one-call settings suffice;
each returns all labels. Source preparations, calls, sensing and precision
remain paid. No hidden-state count or ill-conditioned feature-Gram inverse
is needed for this positive readout space.

For calls reversible for mu_j proportional to w_j(Y)mu, with known positive
bounded weights, the same identity uses the visible return-loop weight

    L^a_ij=(1/mu_a) sum_b [w_i(b)/w_i(a)]
                           Pr_mu(Y0=b,Y1=a,Y2=b).        (3)

This follows from T_i^*=M_wi T_i M_wi^{-1}. Weight range enters statistical
cost. Equilibrium weights do not specify unmeasured kinetics. Nonreversible
calls still need actual adjoint access; stationarity alone does not suffice.

## 3. Compiled operation and exact certificate

For compiled action ell and label a choose probabilities p_{ell,a,j}. Draw a
fresh index J independently of hidden state conditional on the declared label
and outer history, execute T_J and read the endpoint. J is excluded from the
entire service record, including timing/apparatus side records. Durations must
be equal or actually padded when timing is exposed. The current label is
freshly read or warranted unchanged since its last read. The actual kernel is

    U_ell(x,dx')=sum_j p_{ell,Y(x),j}T_j(x,dx').

Its visible transition and residual are

    C_ell(a,b)=sum_j p_{ell,a,j}K_j(a,b),
    E_{ell,a}^2=p_{ell,a}^T H^a p_{ell,a}
       =E_mu[sum_b(U_ell1_b-C_ell(a,b))^2 |Y=a].        (4)

THEOREM. If every row residual vanishes, every allowed adaptive compiled
program's complete visible/action record equals the positive controlled Markov
law C. The initial hidden marginal may be any law absolutely continuous with
respect to mu. The joint old record Z may have arbitrary cardinality and
correlation. Both laws share initial (Z,Y0) and outer policy. A fresh initial
read is included. Equality at all finite depths extends to the countable
infinite record through cylinder laws.

Proof. (4) gives constant next-label rows outside a common mu-null set. Each
raw kernel preserves null sets because its reversible law is equivalent to mu.
Finitely many raw calls therefore preserve absolute continuity of the state
marginal under arbitrary history-dependent selection. No conditional density
given Z is assumed; Z may equal X0. Condition on full history and hidden state,
average the fresh J and obtain C_ell(a,b). Apply the probability chain rule.
Extra raw calls, intermediate native paths and exposed J are excluded.

For a continuum of exactly cancelling configurations, take a finite basis of
ker(H^a) for each label. Each basis residual vanishes outside a null set; their
finite union supplies ONE exceptional set for every zero-defect mixture. Thus
data selection among exact null mixtures does not require an uncountable union
of exceptional sets. The finite-error case has the distinct selection condition
in Section 6.

Synthesis with useful behavior is the convex quadratic problem

    minimize p^T H^a p over p>=0, 1^T p=1,
    subject to sum_j p_j K_j(a,.) in a convex target set,
               sum_j p_j cost_j <= a specified budget.   (5)

A zero residual without useful-transition constraints could give only a useless
replacer. The example retains two distinct actions. The theorem certifies the
compiled operation language, not the still available original raw language.

An acquired exclusion witness: choose z with v2=z^T H^a z>0 and
c=min_j(H^a z)_j>0. Every simplex mixture has E>=c/sqrt(v2), by
Cauchy--Schwarz on residual functions. Valid confidence lower bounds on c and
upper bounds on v2 preserve the exclusion. This excludes convex mixtures of
this menu, not sequential words or new controls.

## 4. Predictive preparation after exact compilation

A fixed compiled reset C_R with stationary pi_R and Dobrushin coefficient
theta=max_{a,a'}TV(C_R(a,.),C_R(a',.))<1 prepares every later compiled service
record, jointly with the same old Z and Z-selected policy, within theta^m
after m real reset calls. The reference starts Y~pi_R independently of Z.
Reset outcomes and raw keys are discarded. This is finite-state Markov
contraction and data processing; hidden memory need not decay.

If all raw calls share mu and mixture probabilities are label-independent,
the mixtures preserve mu. For an ergodic C_R, pi_R=mu_Y and the reference can
be the genuine original device at mu run under the same compiled service.
Row-dependent mixtures require separate stationarity/target checks. Different
data-selected configurations need not have a common limiting law.

## 5. Finite acquisition and execution

Finite data do not certify generic exact zero. Suppose one simultaneous valid
event bounds |H^a_ij-Hhat^a_ij|<=d_a and all mean errors. For any selected
simplex p, on the same event,

    E_{ell,a}^2 <= max(0,p^T Hhat^a p+d_a).               (6)

Use independent validation or simultaneous intervals for every entry used by
selection. Hhat may be indefinite: optimize using a PSD regularization or a
feasible PSD confidence set, then validate (6). An indefinite empirical
quadratic program is not convex.

For known mu_a, scalar frequency radius eta and clipped conditional mean
estimates, d_a=(1+2k)eta/mu_a suffices. Estimated mu_a needs its own positive
floor and ratio error. Independent bounded trials admit Hoeffding bounds.
Squared-defect precision O(N^{-1/2}) generally gives residual-norm precision
O(N^{-1/4}); small matrices do not remove this cost. Sensing, clocks, actuation,
conditioning and independent preparations keep their separate budgets.

If implemented selection probabilities differ from the design by at most zeta
in l1, an n-stage hybrid adds n*zeta/2. A uniform per-call implementation TV
error adds n times that error. Randomization, padding, switching and disposal
of key records cost resources. Endpoint mixtures are not generator mixtures:
sum p_j exp(tQ_j) generally differs from exp(t sum p_j Q_j).

## 6. Finite-error complete records for static hidden disorder

Here the stronger WARRANTED structure is X=(Y,H), with H unchanged by every
call. Conditional on H=h, Y is Markov with matrix P_j(h), including all native
randomness: no additional returning memory is omitted. Calibration is
pi(Y)nu(dh). Each P_j(h) is reversible for the same visible pi_j, possibly a
known reweighting of pi. Thus the loop acquisition applies. This structure
is not inferred from a coarse fit.

Freeze the compiled library and reference before applying this theorem. If
calibration data D select the configuration, condition on D and require
dLaw(H|D)/dnu<=B for deployment, uniformly over the used configurations.
Independent calibration specimens and independently drawn deployment H suffice
when its marginal ceiling is B. An unconditional pre-calibration H ceiling is
not enough when the chosen mixture and deployment H are correlated. Z below
may still be arbitrary within a fixed configuration. Simultaneous Gram confidence
alone does not supply this selection/deployment condition. Alternatively use a
fixed finite menu of all selectable configurations and pay its full row sum
in (7). The same qualification applies to (8).

Let P_ell(h) be the compiled rows and C_ell=E_nu P_ell. Choose explicit
positive stochastic reference matrices Ctilde with entries >=tau>0. Bound

    V_{ell,a} >= E_nu sum_b(P_ell(h)(a,b)-C_ell(a,b))^2,
    M_{ell,a} >= sum_b(C_ell(a,b)-Ctilde_ell(a,b))^2.

Variance/mean orthogonality bounds mean square error to Ctilde by V+M.
Suppose only that the actual INITIAL unconditional H marginal has density
<=B relative to nu. Allow arbitrary initial (H,Z,Y0), including perfectly
informative or infinite old Z and arbitrary feedback. With the same (Z,Y0)
law and outer policy on both sides, the complete record satisfies

    TV(actual, Ctilde reference)
      <= min(1,sqrt[n B/(2 tau) sum_{ell,a}(V_{ell,a}+M_{ell,a})]). (7)

Proof. Compare joint laws retaining H,Z,Y0 with the SAME initial joint law.
The KL chain rule sums row divergences. KL<=chi-square bounds a row by
sum_b(P_ell(h)(a,b)-Ctilde_ell(a,b))^2/Ctilde_ell(a,b).
Bound the selected nonnegative row function by its sum over ell,a. H's
unconditional marginal is unchanged, so expectation is <=B times its nu
average regardless of what the policy learned. Sum n stages, use Pinsker
and marginalize H. Matching exact zero support can replace a positive floor;
unproved zero columns cannot.

This removes old-record cardinality cost only in the static-disorder class.
If feedback moves H, even when every fixed call preserves a stationary H law,
the proof fails. The sum can be loose: a Gram alone does not supply a
pointwise maximum of residual row functions.

For m reset calls whose Ctilde_R has stationary pi_tilde and Dobrushin theta,
followed by n service calls, the positive-reference preparation bound is

    min(1, theta^m +
        sqrt[(m+n)B/(2tau) sum_{ell,a}(V_{ell,a}+M_{ell,a})]). (8)

This reference is the explicit positive Markov process, not automatically the
original device at mu. For two genuine physical preparations, bound each
against the same reference and add the errors. Exact cancellation restores
the physical-reference statement in Section 4.

## 7. Infinite-memory source and useful compiled controls

Let H be uniform on [-1,1] and frozen, and Y binary, initially uniform
independently. Raw operation j flips Y with p_j(h)=u_j+v_j h:

    j       u_j       v_j
    0       1/10      1/20
    1       3/10     -3/20
    2       1/4       1/10
    3       7/20     -1/10.

All p_j lie in [1/20,9/20]. A continuous-time realization is a symmetric
bit-flip generator of rate q_j(h)=-log(1-2p_j(h))/(2t), run for the same t.
Maximum rate is log(10)/(2t). This is a compatible mathematical physical model,
not a built apparatus. Baseline iid samples of nu require an independently
prepared ensemble or another justified source protocol. Waiting on one
frozen-H device does not supply those samples.

Here H^0=H^1=(2/3)vv^T. Two positive mixtures cancel the hidden response:

    A: (3/4,1/4,0,0),     flip probability 3/20,
    B: (0,0,1/2,1/2),     flip probability 3/10.

Each uses one raw call and a fresh dyadic key. They retain distinct visible
dynamics with centered contractions 7/10 and 2/5. Eight B calls yield binary
preparation error at most (1/2)(2/5)^8=0.00032768 for every subsequent compiled
adaptive record, regardless of length. H never changes.

Raw observable rank is infinite: f(y)=(-1)^y obeys
T_0^n f=(4/5-h/10)^n f. These functions are linearly independent under the
continuous full-support nu. Observable autocorrelation Hankel matrices are
Gram matrices of powers of lambda=4/5-h/10, positive definite at every size.
Thus no finite linear observable-operator model reproduces all raw records.
Compilation changes the operation language. The state space has a disconnected
visible factor, so the connected smoothing/sharp-readout obstruction is respected.

## 8. Complete isolated-operation knowledge is insufficient

In source B replace v by |v|. Every INDIVIDUAL raw operation has exactly the
same complete baseline visible path law in both sources, by h->-h for any
changed sign. This includes the whole continuous-time path under that one
generator, arbitrary durations and visible choices of waiting times. Static
visible equilibrium and diagonal residual norms also agree.

Cross-operation Grams differ. Source A has the cancelling mixtures above;
in source B every convex mixture has slope >=1/20, hence E_a^2>=1/600.
The separating witness z=e_0 attains that bound. This excludes convex mixtures,
not sequential words. The 0-then-1 return probability is
1-u0-u1+2u0u1+2v0v1/3, differing by exactly 1/100 between sources. Cross
experiments acquire relative hidden-response registration that arbitrarily
extensive isolated-operation characterization cannot supply.

## 9. Decisive boundaries and comparison

Retaining J defeats cancellation. For H=+1 versus H=-1 in source A, action A
has identical visible outcome law, but TV of (J,next label) is
sum_j p_j*2|v_j|=3/20. Reusing a private key can also create correlations.
Timing, randomizer memory and other accessible side records count as exposure.

Small mean-square residual is not pointwise control. Finite data require (6)
and a justified receiving premise such as Section 6. No arbitrary unseen
defect, rare postselection or cold-start stationary ensemble is supplied.

A positive mixture of injective self-adjoint operators that are positive
SEMIDEFINITE in the SAME L2 geometry remains injective. Positivity of kernel
entries alone is insufficient; a Markov operator can have negative spectrum.
When it also remains smoothing on a connected full-support source, the earlier
sharp-readout obstruction survives. Exact cancellation is not universal.

A fully informed conventional controller can solve the same convex program
and implement the same mixture. There is no computational advantage over a
competent same-information comparator. The two-source separation is a missing
cross-information result. Group averaging, randomized compiling and controlled
lumpability are close predecessors; see SOURCES_AND_PREDECESSORS.md.

The result supplies an experimentally specified synthesis problem, an infinite
rank example and a measurable exclusion witness. The unresolved physical task
is an available useful device/control menu with robust cancellable responses
at affordable calibration, timing and actuation cost. No practical speedup,
apparatus demonstration or civilisation-scale breakthrough is claimed.

## 10. Strengthening the failure: finite pulse words also cannot cancel source B

In source B every primitive centered multiplier
lambda_j(h)=1-2u_j-2|v_j|h is positive and strictly decreasing on [-1,1].
An open-loop word w has multiplier product_{j in w}lambda_j(h), because the
conditional binary matrices commute. Every nonempty finite word is therefore
strictly decreasing. A finite random mixture of such words remains strictly
decreasing whenever it places positive probability on a nonempty word. Adding
an empty identity branch cannot cancel the derivative. This also applies to
word probabilities chosen using only the initial visible label, separately
for each label. The same argument covers arbitrary positive durations in the
given generators: q_j(h) is strictly increasing and exp(-2tq_j(h)) decreases.

Consequently source B admits no EXACT nontrivial hidden-independent transition
from any finite open-loop word/randomization construction of this kind. This
does not exclude intermediate-observation feedback, per-specimen identification,
new controls or approximate long waiting. The two individually indistinguishable
sources differ in that stronger finite-word control capability.

A strong conventional approximate baseline is waiting plus an identity branch.
For repeated mode 0, lambda(h)^L lies in [(7/10)^L,(9/10)^L]. Let a_L be its
nu mean. To target centered multiplier c (0<c<1), choose identity probability
w=(c-a_L)/(1-a_L) when a_L<=c. The averaged target is c and the pointwise
multiplier error is at most (1-w)(9/10)^L. The one-step label TV error is
at most half this. Thus a full n-stage record is within
n(1-w)(9/10)^L/2 of its target Markov law, even with arbitrary old H information.
This pays L native pulse durations on the waiting branch; if its selection
must be hidden from timing, the identity branch also needs actual padding.
It supplies no exact finite-L cancellation, but is an honest powerful baseline.
The exact acquired mixture attains its constructed target in one fixed-duration
call; a competent conventional controller with the cross Gram uses it too.
