# Physical conditional preparation without learning the hidden law

29 October 2026. Root synthesis and construction. Conditional resampling and
heat-bath methods are established. The result here specifies a physical
supplier and retained-record theorem, not a new Gibbs-sampling identity.

## 1. What a preparation supplier must add

The bounded counter changes an invariant law using unknown native dynamics.
It need not convert the currently held specimen to that law. Visible stopping
can choose the right observed label yet leave a biased hidden conditional
state. The four-state obstruction shows that even common rapid microscopic
mixing does not supply a universally exact visible stopping rule of finite mean.

Two constructive escapes are actual recognition of a chosen full state, or an
operation restoring the required conditional law uniformly over unresolved
states and retained records. The latter can avoid learning the hidden dynamics.
It is stronger than an invariant-law promise: it must actually remove the
relevant selection-induced memory at the promised tolerance.

## 2. One conditional operation for a whole target family

Let X be a standard measurable physical state space and Y:X->{1,...,k} an
actual noninvasive label. A warranted baseline mu has positive label masses
pi_y and conditional laws mu_y. These conditional laws need not be explicitly
known or represented by a finite predictive model. For any desired label
distribution q, define the full microscopic target

    nu_q = sum_y q_y mu_y.                                  (1)

For visible weights w, q_y=pi_y w_y / sum_z pi_z w_z. Alternatively q can be
specified directly without knowing pi. Knowing q does not supply a physical
way to set a state distributed as the unknown conditional law mu_y.

The ideal conditional replacement kernel

    E(x,dx') = mu_{Y(x)}(dx')                               (2)

fixes the label, obeys E²=E, and preserves every target (1). It is initially
only a mathematical comparison object. A real supplier must implement or
approximate it with an actual information and timing interface.

### The actual instrument premise

For each y, suppose an executable operation J_y keeps that label and returns
an actual endpoint X' and its complete retained apparatus record A. Write
J_y^A(x,da) for its actual record marginal. Require the joint bound

    sup_{x:Y(x)=y} TV(J_y(x,da,dx'),
                     J_y^A(x,da) mu_y(dx')) <= epsilon_y.   (3)

With deterministic duration and no exposed internal noise record, (3) reduces
to a usual uniform state-mixing bound. If bath kicks, timing data, or further
information are emitted, they belong in A and (3) is stronger than marginal
mixing. Any apparatus state affecting later operations also belongs in the
controlled state/reference model.

This conditional Markov instrument must remain valid after conditioning on
the actual preceding history. An average kernel is insufficient if unmodeled
state or an advance randomization key changes it after that conditioning.

## 3. Compiler and complete-record theorem

Let D be any retained initial record, including calibration and device choice.
There is no baseline assumption on the conditional initial physical state.

1. Draw a desired label L from the specified q, conditional on D if the task
   intentionally chooses q=q(D).
2. Use actual available dynamics and observations until the specimen has Y=L.
   This stage must actually terminate; all its information and time are charged.
3. Apply the supplied conditional operation J_L.

Let R contain D, L and all preparation observations, selectors, counts,
timestamps and other records before J_L. The incoming physical state has
label L but may otherwise have any conditional law. Let A contain every
additional retained record emitted by J_L.

**Theorem.** The actual joint law after this protocol is within

    epsilon_bar = E epsilon_L

of the positive reference

    Law(R,A)(dr,da) mu_{L(r)}(dx').                         (4)

The reference keeps exactly the actual joint preparation record. Its physical
state marginal conditional on D=d is nu_{q(d)}. Any complete later record from
an adaptive physical program using the retained preparation record has the
same TV bound, independent of its observation depth.

**Proof.** Condition on the actual pre-operation history and input state.
Apply (3) to that state, then integrate over its conditional distribution.
The resulting signed-measure bound is at most epsilon_L. Integrating over
the actual records proves (4). No independence of the initial state from D
or R is used. Summing mu_L with L|D=q(D) gives the target marginal. Apply
the same physical continuation kernel on joint record and state to both
experiments. TV contracts, including adaptive policies written as a kernel
on that joint space. QED.

This does not make the physical state independent of the retained label L.
It restores the conditional law given that label. The reference is a
comparison law, not a free physical initializer.

### Calibration-selected devices

If the conditional laws are mu_{theta,y} for an unknown device parameter
theta, condition throughout on (D,theta), retain its actual joint law in (4),
and use mu_{theta,L}. A uniform instrument bound over the promised device
class gives the same theorem. Calibration may select the device and correlate
its state with the old record. Its actual conditional device distribution
cannot be replaced by its pre-calibration prior. A finite-data confidence
event for the supplier retains its acquisition cost and failure probability.

## 4. Costs and the operational consequence

If actual target-label reachability has uniform expected call bound C_y and
J_y has supplied duration t_y, then

    E native calls <= sum_y q_y C_y,
    E conditional-operation time = sum_y q_y t_y.           (5)

Drawing L, sensing, changing modes and processing records cost additional
resources. Almost sure reachability does not imply a finite mean or a deadline.
A structural per-call hit probability p_y>0 supplies the ordinary geometric
bound C_y<=1/p_y for mandatory-call hitting. Stationary weights alone give
none of these bounds.

If epsilon_y(t)<=C exp(-gamma t) uniformly in y, a supplied time
log(C/epsilon)/gamma suffices for the conditional stage. The operation can
be globally nonmixing: it deliberately preserves Y. It removes the unresolved
conditional physical memory. Thus the whole target family (1) can share one
conditional supplier without reconstructing a hidden kinetic model.

An equally equipped conventional controller can use this same operation.
The change in attainable preparations comes from the physical supplier and
its joint-record guarantee, not an algorithmic advantage over ordinary
target-and-hit followed by relaxation.

## 5. More economical repair in the continuous receiver

The baker construction in SELECTIVE_MEMORY_THERMALIZATION.md needs less than
a full implementation of (2). Its selector already supplies the correct
joint law of the complete record R and accepted coordinate u: conditional on
R, unread digits of u remain fair while its current digit is the retained
target label. Only the stored-past coordinate v is wrong. Circle diffusion
acting on v repairs exactly that conditional burden, with a uniform bound
and logarithmic physical-time cost.

More generally, if a selector has supplied a required joint law Lambda(dR,du)
and the desired completion is Lambda(dR,du) kappa_u(dv), an actual instrument
fixing u and uniformly preparing kappa_u jointly with its emitted records
gives the same argument as Section 3. No reset of u is needed. The readiness
of (R,u) is a separate proved premise, not supplied by the thermalizer.

An invariant-law calculation obscures these two burdens: the selector must
put retained and ready coordinates into their required law, and the conditional
operation must remove the remaining physical memory. Acquired information can
guide which operation to build; it does not replace either physical action.

## 6. Failed shortcuts retained

Invariance of mu_y under J_y does not prove (3) from a history-biased input.
A spectral gap without a usable initial-density or uniform smoothing bound
need not give a uniform input guarantee. Clamping a label may change its
conditional equilibrium and cannot be assumed to preserve mu_y. A native
proposal leaving the label cannot be silently rejected by restoring a copied
pre-proposal physical state.

Keeping a bath displacement record can destroy (3) even with an exactly
uniform marginal endpoint. With known input v, a retained uniform displacement
A makes v_out=v+A deterministic conditional on A. Likewise, a correct visible
target does not suffice if hidden selection memory changes later responses.
These are witnessed failures, not hypothetical apparatus warnings.

The result is a supplier criterion and a composable physical construction.
This round supplies an idealized continuous selective-diffusion receiver for
the reduced-memory version, as well as finite-state sensing alternatives.
It does not supply a universal clamp for arbitrary interacting matter.
