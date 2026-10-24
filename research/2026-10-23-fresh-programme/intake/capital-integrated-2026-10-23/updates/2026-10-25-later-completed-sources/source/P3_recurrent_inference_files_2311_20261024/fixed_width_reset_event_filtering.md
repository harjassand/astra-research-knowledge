# Fixed-width event filtering under a certified recurrent-gate approximation

New Pro3 theorem and targeted implementation review. The exact retained
approximation stays within a fixed-width positive product mixture under the
admitted identified-event workload. The true source posterior is enclosed
by a relative certificate; it is not asserted to have that same product
mixture rank.

The source and controller-bridge calculation are developed separately in
`fast_switching_event_kernel_proof.md` and implemented in
`fast_switching_event_kernel.py`. The closure theorem below needs a positive
product propagation operator and the stated mark/reset structure. Its
proof does not depend on a biological interpretation of the source.

## 1. Source-relative product propagation

A symmetric autonomous hidden controller takes values c in {-1,+1} and
switches at rate nu>0. Its silent switches do not change the leaves. Module
i has a finite controller-independent silent generator Q_i. The total
recorded-event hazard is

    V(c,x)=Vbar(x)+c h(x),       |h(x)|<=A,
    Vbar(x)=v0+sum_i dbar_i(x_i),

with v0>=0 and dbar_i>=0. The actual V is nonnegative. Individual marked
hazards may couple multiple components, and the graph of those couplings
may be connected. Additivity is required for Vbar, not for V in each phase.

The reference pre-event flow is the positive operator

    F_t=exp(-v0 t) P_C(t) tensor_i T_i(t),
    T_i(t)=exp((Q_i-diag(dbar_i))t).                     (1)

The true pre-event flow P_t has the same silent path support. Only its
survival weight differs. The controller-bridge theorem supplies

    a(t) F_t<=P_t<=b(t) F_t                             (2)

entrywise for every joint controller/leaf input and output. Its constants
do not require stationary local inputs, strictly positive initial laws or
positive marked hazards in every state.

For the fast-gate certificate, one may take

    a(t)=exp(-A tanh(nu t)/nu),
    b(t)=min(exp(At), 1+S(t)/(1-exp(-2nu t))),            (3)

where omega=sqrt(nu^2+A^2) and

    S(t)=(1+A/omega) exp((omega-nu)t)
          +(1-A/omega) exp(-(omega+nu)t)
          -1-exp(-2nu t).

The exact selected marked operator J_j is retained. Hence the true event
density K_j(t)=P_t J_j and reference query operator F_t J_j obey (2) with
the same constants. Exact zeros of J_j remain zeros.

## 2. Precise reset condition

Let an observed mark j determine a set S_j of active COMPONENTS and one
public output state z_ji for each i in S_j. All retained variables of those
components are reset, not merely one coordinate in a correlated component.
Allow the mark to have kernel

    J_j((c,x),(d,y))
      =h_j(c,x_(S_j),d)
         product_(i in S_j) 1_(y_i=z_ji)
         product_(i not in S_j) 1_(y_i=x_i),             (4)

where h_j>=0 combines hazard and controller reset. Its sum over d is the
mark hazard. This includes controller identity,

    h_j(c,x_S,d)=lambda_j(c,x_S) 1_(d=c),

but also allows the controller reset to depend on the active pre-event
values or on an unobserved guard branch. Those variables are integrated
out before the output controller row is normalized.

Every leaf variable on which h_j depends must be included in S_j. The leaf
reset state must be the same for all unobserved branches and independent
of the old or new hidden controller state. Public dependence on the
identified mark, known time or known protocol is permitted. A fixed public
product reset distribution can replace the point masses in (4).

An inactive component may also undergo a known product transition that
does not depend on the controller, active values or unobserved branch;
that can be absorbed into its output factor. The identity form in (4) is
the concrete implementation.

These are sufficient closure conditions, not a classification of every
mark that happens to preserve products. For example a fully factorized
hazard may preserve a product even without a full reset. The theorem makes
no necessity claim for each listed condition in isolation.

## 3. One-component update with all density factors retained

Start from one normalized product component

    pi_r(c) product_i mu_ri(x_i)

with mixture weight w_r. After reference propagation, keep raw rows

    p_r=pi_r P_C(t),     v_ri=mu_ri T_i(t),
    s_ri=v_ri 1.

For the observed mark define the raw controller row

    g_r(d)=sum_c p_r(c)
             sum_(x_S) h_j(c,x_S,d) product_(i in S) v_ri(x_i).
                                                               (5)

The output component has event-density mass

    ell_r=exp(-v0 t) (g_r 1) product_(i not in S) s_ri.   (6)

Its normalized factors are

    pi'_r=g_r/(g_r 1),
    mu'_ri=delta_(z_ji)                 if i in S,
    mu'_ri=v_ri/s_ri                    if i not in S.   (7)

Equations (5)-(7) follow by summing the reset input coordinates in (4).
The inactive rows factor out of that sum. Thus one input component gives
one output component, even when the hazard in (5) is strongly coupled.

Components with exactly zero ell_r can be dropped. A conditional posterior
is defined only if the total event density

    ell=sum_r w_r ell_r

is positive. The new mixture weight is w'_r=w_r ell_r/ell. Components are
not normalized before their event-density masses have been included.

The same formula works with unnormalized numerical lower rows p_r and
v_ri: their masses must be retained. In particular the lower controller
row need not sum to one. Normalizing it and dropping its mass would change
both the likelihood and the mixture weights. The implementation retains
this mass inside its hazard/controller contraction.

## 4. Fixed width through arbitrary identified-event sequences

### Theorem

Suppose the initial retained law is a nonnegative mixture of R product
components over controller and leaves. Every propagation interval has
product form (1), and every observed mark satisfies (4). Then after any
finite identified-event sequence the exactly updated reference law has at
most R product components. A final no-event interval also preserves this
width. Previously overlapping active scopes cause no extra branches.

**Proof.** Product propagation preserves each component. Equations (5)-(7)
show that every admitted mark maps it to one component or zero. Apply this
argument inductively, preserving its exact event-density mass. QED.

The mixture label r retains initial correlations and its likelihood weight
changes with the whole record. The physical controller posterior remains
inside each component. Neither controller observations nor resets between
successive events are required.

For finite local state spaces, propagation costs ordinary local row-matrix
products. If the active mark kernel has a supplied positive guard expansion

    h_j(c,x_S,d)=sum_(b=1)^B_j a_jb(c,d) product_(i in S) g_jbi(x_i),

then (5) is computed through local guard expectations and the small
controller rows. Its cost is polynomial in R, B_j, the controller size and
local state sizes. For m records the total cost is the sum of these m
local propagation and guard-contraction costs. No joint leaf-state table
or controller-switch trajectory is needed. Without such a compact guard
representation, contraction of an arbitrary h_j may itself be expensive;
the full reset does not make reading a huge hazard table free.

## 5. Branches, controller resets and historical labels

Coarse marks may sum different guard patterns without increasing R when
every branch has the same complete leaf reset in (4). Branches may have
different controller resets: their contributions simply add to g_r(d).
The implemented AND/OR edge mark is of this form.

If hidden branches reset leaves to different product states, one generally
obtains a mixture of those outputs. For example equal branches resetting
two leaves to 00 and 11 produce a correlated law from a single product
input. One product component cannot represent that law. Observing the
branch separately removes this particular ambiguity; silently merging
the two outputs does not preserve width.

Controller-dependent leaf resets can also introduce controller/leaf
correlation within a component. Controller resets depending on inactive
leaf variables have the same problem unless those variables are included
in the fully reset scope. Only dependence already integrated in (5) is
covered by the one-component result.

Failure to reset a hazard-dependent component can matter even for the
current AND/OR family. Let controller and two leaves initially be uniform
and independent. The mark hazard is AND in phase + and OR in phase -.
If only the first leaf is reset, the normalized joint table of controller
and the second leaf is, in phase order (+,-),

    [[0,1/4],[1/4,1/2]].

It has nonzero determinant and is not a product. Resetting both leaves to
00 removes that event-induced dependence while preserving the updated
controller row.

The full-reset condition applies to the state actually retained. An old
count label correlated with an active leaf is not erased merely because
the leaf's present bit is reset. A count tensor train retaining such labels
therefore does not automatically enjoy fixed R. Its certificate can still
be propagated by positive operations, but its representation may need
larger bonds or extra mixture branches. Coarse total counts and uncertain
event times likewise do not inherit the identified-record fixed-width
claim without a separate construction.

## 6. Conditional-state and record-likelihood certificates

For a particular record with interval lengths t_1,...,t_k, let

    alpha=product_l a(t_l),     beta=product_l b(t_l).

The final interval may be a no-event interval, in which case it has no J
factor. Positivity of every intervening mark/reset gives

    alpha nu F_(t_1) J_1 ... F_(t_k) J_k
      <= nu K_1 ... K_k
      <= beta nu F_(t_1) J_1 ... F_(t_k) J_k.            (8)

Omit J_k when appropriate. There is no division by the observed record's
probability or density in this bound.

If the entrance has projective spread R_0 and the numerical execution adds
spread C_num,l at interval l, the final conditional-state spread is at most

    R_0 (beta/alpha) product_l C_num,l.                 (9)

The TV bound is tanh(one quarter of the logarithm of (9)). The initial
entrance error is paid once. Every approximate propagation and every new
numerical rounding allowance is paid when applied. Fixed mixture width
does not mean approximation error remains fixed over an arbitrarily long
record.

Let ell_hat be the product of the exact retained update normalizers. It is
the approximate JOINT DENSITY of the observed event times and marks, not a
probability and not a product of independently normalized component rows.
For an exact normalized initial input its true value lies in

    [alpha ell_hat, beta ell_hat]

before numerical allowances. With only a projective initial certificate
R_0 and no separate entrance-mass calibration, the conservative interval is

    [alpha ell_hat/R_0, beta ell_hat R_0],

with numerical lower/upper factors included as certified. This conservative
likelihood calibration does not change the posterior spread R_0 in (9)
to R_0 squared. Tighter calibrated initial masses may improve the interval.

## 7. An explicit fast-controller envelope for whole records

The denominator in (3) matters at small t. The following algebra keeps it
and produces a simple uniform envelope. Put

    d=omega-nu,     c=A^2/(2nu)=d(1+d/(2nu)),
    D0=1-exp(-2nu t).

Split S into its even and odd parts. Exactly,

    S_even=(exp(dt)-1)(1-exp(-(2nu+d)t)),
    S_odd=(A/omega) exp(dt)(1-exp(-2omega t)).

For v>=u>0, (1-exp(-vt))/(1-exp(-ut))<=v/u. Therefore

    S_even/D0 <= (1+d/(2nu))(exp(dt)-1)
               <= exp(ct)-1,
    S_odd/D0 <= (A/nu) exp(dt) <= (A/nu) exp(ct).

The second step for S_even follows from
r(exp(x)-1)<=exp(rx)-1 for r>=1 and x>=0. Consequently

    b(t)<= (1+A/nu) exp(A^2 t/(2nu)).                  (10)

No approximation omega-nu<=A^2/(2nu) was applied to an uncontrolled cosh
difference. The endpoint denominator is accounted for by the displayed
ratios, including the t down to zero limit.

If k propagation intervals have total elapsed time T, (3) and (10) give

    log(beta/alpha)
      <= k[A/nu+log(1+A/nu)] + A^2 T/(2nu).            (11)

Thus one certificate covers every identified mark sequence and every
choice of positive gaps with those k,T, independently of record rarity.
The same bound with k<=M+1 covers all records of at most M events on a
fixed horizon T, including the final no-event gap. Add log R_0 and the
numerical log-spreads for the executed conditional law.

### Source-certified workload eligibility

Fix an admitted mark family satisfying the full-reset schema, an event
budget M, and a total elapsed-time budget T. Consider ALL records with at
most M identified events and positive gaps whose sum is at most T,
terminating immediately after the last identified event. The reference
filter has at most R components throughout, and its analytic log-spread is
uniformly at most

    rho=M[A/nu+log(1+A/nu)]+A^2 T/(2nu).              (12)

There is no minimum-lag premise in this ideal theorem. With initial spread
R_0 and an actually enforced total numerical log-spread budget Gamma_num,
a sufficient eligibility test for posterior-TV target epsilon is

    Delta=4 atanh(epsilon)-log R_0-Gamma_num > 0,
    nu >= (2 M A+A^2 T/2)/Delta.                       (13)

This follows from log(1+A/nu)<=A/nu. For A=0 the analytic allowance is zero
and the remaining initial/numerical budget is the only restriction. A
terminal survival interval uses M+1 in place of M. A nonpositive Delta
means that this declared error budget cannot establish the target.

The physical controller rate nu is supplied by the scientific source and
is not changed to make (13) pass. This is a source/application eligibility
test, not permission to modify the model. Near-zero observed gaps can
require extra numerical precision to meet Gamma_num; that obtaining cost
is still paid, and the concrete fixed-precision executor is not claimed to
handle every arbitrarily small gap.

A common policy may select subsequent certified query actions using public
record history. The relative-error argument still applies on each resulting
record when every selected source/action contract is satisfied and the same
uniform budgets hold. Fixed width additionally requires every chosen action
to preserve the product/reset family. A source-changing intervention needs
its own checked dynamics, killing, contrast and reset contracts; positivity
alone does not certify that the new physical source remains in this class.

## 8. All complete records: a bounded-potential measure envelope

There is a second useful bound without an event-count restriction. On a
complete marked path over a fixed horizon T, retain all true silent
transition and marked-jump factors, but replace survival exp(-integral V)
by exp(-integral Vbar). Call the resulting positive path measure Mhat_T.
The exact source measure M_T differs by

    dM_T/dMhat_T=exp(-integral_0^T C_s h(X_s) ds).

Hence, for the same normalized entrance,

    exp(-AT) Mhat_T <= M_T <= exp(AT) Mhat_T.           (14)

The finite source has bounded intensities and is nonexplosive; the marked
path space includes all finite event counts. Summing or integrating (14)
is legitimate and shows that Mhat_T has finite total mass between exp(-AT)
and exp(AT). Integrating out silent paths gives the product query operators
F_t J_j used above, including a final survival factor.

Equation (14) remains valid after any common measurable record selection
or coarsening. It gives relative spread exp(2AT), and therefore conditional
TV at most tanh(AT/2), for every nonzero selection of complete records.
For fixed k,T the sharper analytic spread can use

    log R_analytic <= min(2AT,
        k[A/nu+log(1+A/nu)]+A^2 T/(2nu)).               (15)

Initial projective error and numerical allowances are added separately.
The analytic complete-record envelope is mathematical; the concrete saved
interface evaluates a specified lag. It does not contain a precomputed
numerical table for every continuous event time or every possible record.

The surrogate Mhat_T is not automatically a probability measure or the
law of a conservative reduced CTMC. Keeping the actual J_j while replacing
their total killing by Vbar generally leaves a row-sum imbalance. A global
normalization of the entire finite-horizon positive measure yields a valid
probability measure with the same projective spread, but that is different
from asserting local Markov-generator conservation. The implementation
makes only the certified record-operator claim.

Coarsening records preserves (14) as a measure inequality; it need not
preserve the fixed-width representation of Sections 3-4. Those are separate
statements. Nor does (15) promise a vanishing fast-controller error uniformly
over an unrestricted number of events as nu tends to infinity: the
event-count-free envelope is 2AT, while the faster bound retains k.

## 9. Concrete executed specialization and targeted review

The available `fast_switching_event_kernel.py` obtains an interface from a
checked 146-rule source with 24 binary leaves and a recurrent controller.
Its full physical state space has 33,554,432 configurations. Each cycle
edge has AND hazard in phase 1 and OR hazard in phase 0, represented by
three disjoint OR guard patterns. Every branch of the same observed edge
mark resets both active leaves to 00 and retains the controller.

The exact Boolean-polynomial average is additive even though each phase's
hazard graph is one connected cycle. Local scope calculations give A=18;
the controller rate is nu=1,000,000. This is a declared new future kinetic
source applied to an already acquired correlated entrance, not an empirical
inference of those kinetics.

The retained interface is `fast_switching_record_interface_24sites.json`.
The executed record is edge_0, edge_1, edge_2, edge_0, with lag 1/10 between
successive events. The controller is unobserved and not reset between
events. All four updates preserve the original 256 mixture components.
The exact rational final controller/leaf mixture is retained in
`fast_switching_record_posterior_24sites.json`.

`fast_switching_event_kernel_results.json` reports the outward enclosures

    four-event record density in
    [0.0000099762810347, 0.0000099783643303],

    final joint controller/leaf posterior TV < 0.000052200302,

    final controller-on probability in
    [0.0552143956249, 0.0553187962282].

The interval endpoints above have been rounded outward for display. The
full output retains longer certified endpoints. Acquisition propagation
spread minus one is at most 2.05e-42; application arithmetic has separate
small factors. The analytic fast-controller allowance dominates the
reported error.

The implemented `workload_certificate` also checks the full-reset schema
for all 24 edge marks. With M=4 and total event-lag budget T=2/5, it obtains
the source-only analytic log-spread bound 261/1250000. Including the
inherited entrance certificate, the ideal exact averaged operators have
uniform posterior-TV bound less than 0.000052200463617 for EVERY admitted
mark sequence and positive choice of gaps in that workload. This
class-wide result is separate from the particular four-record numerical
execution. Its reported numerical spread budget is one, so future
numerical executions must add and enforce their own budget. A terminal
no-event tail is not included in that saved workload certificate.

The retained-interface loader checks the compact source, additive mean,
contrast, reset schema and rational operator dimensions without
reevaluating its exponentials. The posterior loader checks exact rational
mixture normalization and local probability ranges. These are reuse checks
on the scientific objects, not a replacement for the acquiring proof.

A targeted code review checked the common-reset schema, retention of raw
controller and local row masses, exact guard aggregation, rational mixture
normalization, and separate payment of acquisition and application numerical
spreads. In particular `fixed_reset_schema` checks the reset condition before
the fixed-width update. The all-input operator theorem itself applies to
positive marks beyond that narrower application schema.

The completed independent three-leaf comparison uses the full coupled
16-state killed generator, positive uniformization with 41 terms per scaled
step and 18 matrix squarings. It checks all 16 input rows, 64 positive event
entries and 192 structural zeros. All reference enclosures lie inside the
operator sandwich. The source acquisition and four-event computation were
not independently rerun by this proof review.

## 10. Interpretation and comparison

The fixed-width update is an algebraic consequence of summing every
hazard-dependent retained component before resetting it to the same public
product state. It is not an assumed-independence projection. It also is
not a whole-system renewal claim: inactive components retain their histories,
overlapping future marks can revisit them, and initial mixture correlations
remain in r.

Positive filtering, reset factorization, averaging and Feynman-Kac measure
comparison are established machinery. The controller-bridge source and
primary comparisons are in `fast_switching_event_kernel_proof.md`; the
projective all-record theorem is detailed in `conditioning_stable_entrance.md`.
The construction being developed is their source-checked composition:
coupled fast-gated hazards, a certified product pre-event operator, exact
active-guard/reset contraction, and a retained correlated filter with
explicit width, likelihood and all-record error contracts. Incumbents may
use the same algorithm, source inputs and retention mechanisms. No
historical priority, architecture necessity or unrestricted rank guarantee
is claimed.

## 11. A bounded nonadditive mean residual: exact cancellation is not essential

This is an additional proved obtaining extension. The current numerical
compiler and retained cycle calculation use exact additive mean killing;
they have not been extended or rerun for this section. It matters because
exact cancellation is a fragile binary admission condition, whereas an
explicit residual can be assigned part of the scientific error budget.

Allow the actual mean to have the decomposition

    Vbar(x)=v0+sum_i dbar_i(x_i)+r(x),
    r_minus<=r(x)<=r_plus,       W=r_plus-r_minus.

The reference additive killing v0+sum_i dbar_i must remain nonnegative,
with v0,dbar_i>=0. The residual bounds may have either sign. The actual
source hazards remain nonnegative, and the contrast |h(x)|<=A is the
contrast of the ORIGINAL phasewise hazards. Use the same positive product
reference flow F_t formed from the additive part and the exact original
mark/reset operators J_j.

### Residual comparison theorem

For every joint input and output coordinate,

    exp(-r_plus t) a(t) F_t J_j
      <= K_j(t)
      <= exp(-r_minus t) b(t) F_t J_j.                 (16)

**Proof.** Fix a silent leaf path. The controller bridge comparison remains
unchanged because r does not depend on the controller. The additional
positive survival factor lies between exp(-r_plus t) and exp(-r_minus t).
Multiply these two inequalities, integrate over leaf paths, and apply the
exact positive mark/reset. QED.

The analytic log-spread for k propagation intervals of total time T is
therefore at most

    W T + min(2AT,
        k[A/nu+log(1+A/nu)]+A^2 T/(2nu)).               (17)

The same full-reset proof preserves R reference mixture components. All
previous likelihood and numerical-accounting statements apply with the
multipliers in (16). A workload of at most M events, ending at its last
event, has the sufficient eligibility test

    Delta=4 atanh(epsilon)-log R_0-Gamma_num-WT > 0,
    nu >= (2MA+A^2T/2)/Delta.                           (18)

If r is a known constant, W=0: the constant changes likelihood calibration
but introduces no conditional-state error. Faster controller switching
cannot make an uncontrolled nonadditive mean disappear. The term WT is
the explicit remaining obstruction rather than a hidden approximation.

This is a uniform conditional-state statement for each specified record.
When records with different total durations are integrated or coarsened,
their duration-dependent scalar likelihood multipliers must also be
retained; a projective spread alone does not calibrate relative masses
between different records. On a common complete horizon, the constant
residual factor is common. This is the same reason that unnormalized
operators, rather than separately normalized rows, are the retained object.

### Obtaining a valid residual from the guarded Boolean source

The existing exact polynomial expansion obtains

    Vbar(x)=p_empty + sum_i p_i x_i
                   + sum_(|S|>=2) p_S product_(i in S) x_i.

Put b=p_empty+sum_i min(0,p_i), and define

    v0=max(0,b),
    dbar_i(0)=max(0,-p_i),   dbar_i(1)=max(0,p_i),
    r(x)=min(0,b)+sum_(|S|>=2) p_S product_(i in S) x_i.

This is an EXACT identity and gives nonnegative local reference killing
even when the affine part of the mean is negative somewhere. Obtain the
valid rational bounds

    r_minus=min(0,b)+sum_(|S|>=2) min(0,p_S),
    r_plus =min(0,b)+sum_(|S|>=2) max(0,p_S).            (19)

Every Boolean monomial is zero or one, so (19) requires no global
configuration search. Grouping monomials with common small support and
enumerating that support can sharpen the bounds; arbitrary overlap only
makes the sum of local bounds conservative. The original local-scope
contrast calculation still obtains A. All quantities are exact rational
source calculations. With bounded guard scope, the number of expanded
monomials is bounded by the sum of the per-rule guard expansions.

Thus the mathematical construction extends to controller-independent
silent modules with arbitrary compact bounded-scope marked hazards. The
desired accuracy is useful only when the obtained W, A, nu and workload
budgets satisfy (18); no claim is made that this happens for every source.
No minimization over all separable baselines or best residual bound is
claimed. This extension uses the familiar bounded-potential Feynman-Kac
comparison; the source-derived residual and its workload cost are the
additional constructive facts retained here.
