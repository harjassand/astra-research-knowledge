# A preparation hierarchy under rapid microscopic mixing

29 October 2026. Astra P1 root construction. This combines the independently
developed four-state obstruction with two explicit changes of information or
precision. The hard-deadline argument is a new application of the preserved
signed-continuation control principle, not a claim to have invented polynomial
continuation. The finite-mean escape is ordinary target-and-hit feedback.

## 1. The physical service and its interface

The entire microscopic state of this mathematical receiver is
`X=(Y,H) in {-1,+1}^2`. The warranted baseline is uniform, `mu(x)=1/4`.
One actual native call has kernel

\[
 P_{\delta,\lambda}=(1-\delta)P_{0,\lambda}+\delta S,
 \qquad
 P_{0,\lambda}((y,h),(y',h'))={1+\lambda hh'\over4},
 \qquad S(y,h)=(h,y),
\]

where `0 <= delta <= 1/4` and `0 < lambda < 1/2`. The controller does not know
these parameters. It cannot select the mixture component, inspect the native
random seed, reset the specimen, or retain a physical copy. Every call is the
same combined operation. Native call count is the cost unit; a physical-time
claim additionally needs actual durations and sensing/control costs.

All these kernels are symmetric and preserve `mu`. Every entry is at least
`c=3/32`, so every one has the common minorization

\[
 P_{\delta,\lambda}(x,\cdot)\ \ge {3\over8}\mu(\cdot).
\]

This is a uniformly rapidly mixing, irreducible finite-state family. No frozen
sector or arbitrarily small spectral gap supplies the obstruction below.
The full microscopic model and this minorization are structural promises of
the receiver; a finite label trace does not establish them.

The desired preparation is the actual endpoint distribution

\[
 \nu(y,h)={1+ay\over4},\qquad 0<|a|<1.
\]

A weaker observable service, sufficient for both impossibility results, asks
only for

\[
 \mathbb E Y_\tau=a,\qquad
 \mathbb E Y_{\tau+1}=0,                                      \tag{1}
\]

where the second label follows one fresh native call after completion. Indeed
`P Y=delta H`, and `nu H=0`. The second native call is a real possible future
experiment. The controller is not asked to prepare an independent copy of its
own retained history.

Randomized controllers use a parameter-independent seed. They may process
their entire allowed record and include adaptive calibration in their actual
stopping rule. A seed supplied with exact hidden-parameter information is a
different information interface. Likewise, informative timing marks or extra
apparatus outputs must be included among the observations rather than silently
treated as free.

## 2. Visible-only universal exact preparation has infinite mean

With only `Y` observable, any one almost surely terminating stopping rule that
satisfies (1) for the whole family must have infinite expected native-call
count at `delta=0`. At these sources the visible record is iid fair signs,
independently of the hidden correlation parameter `lambda`.

The proof is in
`record_geometry/FOUR_STATE_UNIVERSAL_PREPARATION_OBSTRUCTION.md`, independently
developed by the existing record-geometry role and received by root. Its main
steps are worth stating because they identify the missing information.
Assuming `E tau < infinity`, the first rare swap transfers an earlier observed
sign into the hidden coordinate. Its later influence is attenuated by
`lambda` at each native step. Coupling to an iid visible record until the
second swap gives the first-order response

\[
 \left.{d\over d\delta}\mathbb E H_\tau\right|_{0+}
 = A(\lambda)=\sum_{\ell\ge0}c_\ell\lambda^\ell,
 \qquad
 c_\ell=\mathbb E[1_{\{\tau\ge\ell+1\}}Y_{\tau-\ell-1}].       \tag{2}
\]

The coefficients are absolutely summable because `sum |c_l| <= E tau`.
The probability of two swaps before the reference stop is `o(delta)` under
this first moment alone; no second moment is used. Exactness for all positive
`delta` forces (2) to vanish throughout `0 < lambda < 1/2`. Power-series
uniqueness gives every `c_l=0`. But optional sampling for the iid visible
signs gives

\[
 \sum_{\ell\ge0}c_\ell
 =\mathbb E\sum_{j<\tau}Y_j=-\mathbb E Y_\tau=-a,
\]

a contradiction. The universality quantifier and the absence of hidden-state
sensing are both essential. This is not a lower bound for every calibrated,
known individual kernel.

## 3. Full state recognition still cannot supply a universal exact deadline

**Theorem.** Even with noninvasive observations of both `Y` and `H`, no
parameter-independent controller using at most `L < infinity` native calls
can satisfy (1) throughout the family.

**Proof.** Fix any `lambda` in `(0,1/2)`. For a controller stopped by `L`,
define

\[
 m_0(\delta)=\mathbb E_{\delta,\lambda}Y_\tau,
 \qquad m_1(\delta)=\mathbb E_{\delta,\lambda}Y_{\tau+1}.
\]

For each finite state history, its probability is a product of transition
entries affine in `delta`. Integrating the controller's seed assigns fixed
nonnegative coefficients to these finitely many histories. Therefore `m_0`
and `m_1` are polynomials in `delta`, of degree at most `L` and `L+1`.
If (1) holds on `[0,1/4]`, their polynomial identities extend to `delta=1`.

At `delta=1`, the native operation is the deterministic swap `S`. Every
possible trajectory, including one stopped using the complete state, preserves
`Y+H` pathwise. The uniform initial law has mean zero of this conserved sum.
One later swap reads the terminal hidden coordinate as its new visible label.
Consequently

\[
 m_0(1)+m_1(1)=\mathbb E(Y_\tau+H_\tau)
 =\mathbb E(Y_0+H_0)=0.
\]

The continued target identities instead require this sum to equal `a`, a
contradiction. QED.

The swap at `delta=1` is an algebraic comparison point outside the warranted
rapidly mixing family. It is not an extra operation supplied to the controller.
All physically promised sources remain uniformly positive. This reuses the
preserved signed-continuation logic at a different endpoint-preparation
question. Variable unbounded stopping times do not give finite-degree
polynomials, so the proof does not prohibit the next construction.

Any calibration included in the same bounded history is covered. Exact
parameter-dependent advice, an additional state-changing operation, an
initializer, or unbounded calibration changes the premises. No assertion about
all such alternatives follows from this theorem.

## 4. One extra actual sensor gives an exact finite-mean operation

Supply a noninvasive sensor for the hidden coordinate `H`. No transition
probability is learned and no new state-changing actuator is introduced.

1. Independently draw a target full state `R` with distribution `nu`.
2. Execute at least one native call.
3. Read `(Y,H)` and stop if the current full state equals `R`; otherwise repeat.

Conditional on every past history and on `R`, each next call reaches `R` with
probability at least `c=3/32`. Thus, with `tau >= 1`,

\[
 \mathbb P(\tau>n\mid R,\hbox{initial information})
 \le (29/32)^n,
 \qquad \mathbb E\tau\le32/3.                              \tag{3}
\]

At completion the actual specimen equals `R`, exactly. Hence its law is
`nu`. The construction works from any initial state or distribution, with any
pre-existing record, provided `R` is freshly drawn from the stated target and
the native conditional transition law remains in the promised family. It is
ordinary target-and-hit feedback enabled by full state recognition; it is not
a new perfect-sampling algorithm.

For the concrete common comparison `a=1/3`, the target masses are
`(1/6,1/6,1/3,1/3)`. An exact fair-bit implementation draws two-bit integers
until one lies in `{0,1,2}`, uses two of these three values for `Y=+1`, and
draws one independent fair bit for `H`. Its expected random-bit cost is
`2*(4/3)+1=11/3`, with no hard bit-count cap. These bits, all full-state reads,
and the call durations are charged. A different warranted exact target
randomizer can also supply `R`.

The added sensing resource is the ability to identify the actual four-state
microscopic state. Merely retaining another bit of controller memory does not
supply that sensor, and an unmodeled physical bath is not claimed to be fully
observed by reading two symbols.

After stopping, the retained record includes `R`, so the physical state is
known given that record. A correct reference for any future adaptive service
keeps the same record and the same state `R`, then applies the same actual
future kernels. It would be incorrect to declare the terminal state independent
of a record explicitly containing it. Equation (3) has a geometric tail; the
universal exact hard cap ruled out in Section 3 remains unavailable.

## 5. Visible-only bounded finite-tolerance preparation is easy in this family

Keep only the `Y` sensor and set `a=1/3`. The preserved bounded stationary
compiler with integer weights `w(-)=1`, `w(+)=2` gives a kernel `K` with
`nu K=nu` and at most two native calls per completed macro-operation.
Its literal implementation, including its one fair phase bit, is specified
and checked in the four-state companion. Every entry obeys

\[
 K(x,x')\ge2(3/32)^2={9\over512}.
\]

Thus `K(x,.) >= (9/128) mu(.)`. The resulting Dobrushin contraction is
uniform over the entire promised family. Starting from any law `rho`, after
exactly `n` completed macros,

\[
 \operatorname{TV}(\rho K^n,\nu)
 \le (119/128)^n.                                           \tag{4}
\]

In particular `n = ceil(log(1/epsilon)/(-log(119/128)))` suffices, with
at most `2n` native calls. The elementary minorization is conservative; no
optimization of this constant is the scientific objective. This finite-error
route is much stronger than the exactness obstruction might initially suggest:
its call deadline is logarithmic in the requested inverse tolerance.

The compiled operation preserves the target, whereas repetition plus the
additional uniform mixing promise prepares it. The preceding snapshot supplied
the first achievement without this second premise. Completion count is not
fixed elapsed physical time, and the time-weighted occupation law is a separate
question. No exponential rate is inferred from equilibrium weights alone.

### Conditional information and later programs

Let `D` be an arbitrary retained pre-existing record. Suppose that, conditional
on `D=d`, the actual specimen may have any initial law `rho_d` and the actual
native kernel is one fixed member of this family. The member may depend on `d`
and may be unknown. Fresh operation randomness and valid conditional Markov
transitions must still be supplied. The uniform form of (4) gives

\[
 \operatorname{TV}\bigl(\mathcal L(D,X_{\rm out}),
                  \mathcal L(D)\otimes\nu\bigr)
 \le (119/128)^n.                                           \tag{5}
\]

The same conclusion holds if the fixed member is a further latent variable,
possibly correlated with `D` and the initial state: condition on that variable
as well and retain its actual joint law in the reference. This is the correct
form for a calibration-selected device. It does not require `mu` initially,
but it does require the whole conditional model to lie in the same promised
class. Calibration may establish such a class only with its actual confidence
and acquisition costs, not by reusing an unconditional estimate after selection.

Data processing transfers (5) to any complete later record generated by an
adaptive physical program based on `D` and later observations, with the same
device parameters in the reference. The bound does not grow with future depth.
This is a comparison to a mathematically initialized `nu` reference, not a
claim that a free exact initializer was constructed.

The *new preparation record* includes intermediate labels, phase bits, the
number of native calls in each macro, and possibly timestamps. Such records
may be correlated with the terminal state. They cannot simply be appended to
`D` in (5), because they were generated during the operation being analyzed.
If deployment uses them, a joint instrument bound is needed. The separate
selective-memory thermalization construction in this round supplies one such
bound for its own different receiver and its stated record interface.

## 6. What changes between the four achievements

| Interface and objective | Result | Essential resource or restriction |
|---|---|---|
| Visible-only, one universal exact stopping rule | Infinite mean at the iid-visible source | Unknown hidden response; no hidden-state sensor |
| Even full state sensing, universal exact hard deadline | Impossible for every finite deadline | Polynomial continuation to conserved-sum witness |
| Full state sensor, exact finite-mean endpoint | Mean native calls at most `32/3` | Actual recognition of the chosen full state; exact target randomizer |
| Visible-only, finite full-state TV tolerance | At most `2 ceil(log(1/epsilon)/(-log(119/128)))` calls | Structural common minorization and the bounded invariant-law compiler |

The contribution of this hierarchy is the separation of exact preparation,
finite-error preparation, measurement access, and deadlines within one uniformly
mixing unknown family. It is not evidence that all useful preparation is slow.
Nor does it establish a physical implementation or a practical speedup over
an equally informed conventional controller.

## 7. Primary predecessors and receiving status

Lovasz and Winkler, *Exact Mixing in an Unknown Markov Chain* (1995), give
finite-mean exact stationary stopping when the states of an unknown finite
chain can be identified. That full-state interface is an important constructive
predecessor, consistent with Section 4 and absent in Section 2:
https://www.combinatorics.org/ojs/index.php/eljc/article/download/v2i1r15/pdf

The older bounded compiler and signed-continuation proof remain preserved in
`continuation3_20261029` and `continuation2_20261029`; their accepted validation
is not reopened here. The four-state proof and its exact rational checks were
read and rerun by root. The additional deadline and sensor constructions in
this file were sent to the existing record-geometry role for a focused
challenge. Actual receiving notes, final hashes, and any corrections are saved
separately. Historical priority of the new four-state separation is unresolved.
