# Weighted operations, attainable normalization and repeat scope

30 October 2026. Root supplement. The original common-equilibrium theorem
and this extension have different acquisition costs.

## 1. Actual operations with different equilibria

Retain the actual fixed-call interface from `ACTUAL_OPERATION_ALGEBRA.md`.
Operation P_j is reversible for mu(x) w_j(Y(x)), where each w_j is known,
strictly positive and bounded above and below. Its kinetic prefactor may
differ arbitrarily from every other operation. No relation among the unknown
rates is inferred from the equilibrium weights. Put

    R_j = sup w_j / inf w_j,
    W_w = product_(j in word w) R_j.

The adjoint on L2(mu) is exactly

    P_j^* = M_(w_j) P_j M_(1/w_j).                    (1)

For an adjoint call starting at x and ending at x', execute the same forward
physical operation and multiply the report by w_j(Y(x))/w_j(Y(x')). For a
word, execute these calls in reversed order and multiply all such visible
ratios. They are positive and the product is at most W_w. This is numerical
weighting of a real experiment. It does not physically implement a Markov
kernel equal to P_w^*, nor prepare its invariant law.

Starting from actual input f mu, 0<=f<=B, the output density remains

    rho_w=P_w^* f,   0<=rho_w<=B W_w.                (2)

The acquired overlap is still

    K(u,v)=<f,P_u P_v^* f>,                          (3)

but its report now lies in [0,B^2 W_v]. Symmetry allows choosing the
orientation with the smaller adjoint weight range for a cross entry. The
self entries retain their own range. All endpoint-weight sensing and joint
product errors must be included. The universal bound can grow exponentially
with word length; common equilibrium removes that particular growth.

If every operation in a word has the same weight w, its ratios telescope
and W_w can be replaced by sup w/inf w. Sharper actual telescoping or known
path restrictions may likewise improve the range. A loose product bound is
not an impossibility theorem about the experiment.

The exact full-density distance, arbitrary-common-receiver TV bound, and
absence of a finite predictive closure remain unchanged. Use the actual
bounded report ranges in each confidence radius. With a common worst range
B^2 W, the elementary sample bound is O(B^4 W^2 epsilon^(-4) log(M/alpha)).
Clock, preparation and word duration are still additional costs.

## 2. A literal witness still exists, at its actual gain

Let C=B max(W_u,W_v). On the u branch of the main witness, run the weighted
adjoint experiment and form its nonnegative path report F_u, bounded by C.
Return 1 with probability F_u/C. On the v branch return 1 with probability
1-F_v/C. The conditional expectation of F_w is rho_w(x), although P_w^*
is not a Markov kernel. Therefore the complete randomized test has

    phi(x)=1/2+(rho_u(x)-rho_v(x))/(2C),
    Pr_u{1}-Pr_v{1}=D(u,v)/(2C).                    (4)

Every multiplication, randomization and possible finite-precision error is
an actual operation. Exact arithmetic on arbitrary real weights is not a
physical supplier; a finite tolerance can use specified rational evaluation
and a charged bias bound. The common-equilibrium binary-label witness needs
only a fair branch bit and its literal endpoint label. If the implemented
conditional test probability differs from the ideal by at most zeta, its
distinguishing gap is at least D/(2C)-2zeta. An acquired positive lower
bound on D thus gives a finite required probability-synthesis precision.

Hence exact operational completeness on reachable ensembles survives the
weighted interface, but its distinguishability and acquisition cost may be
poor. No all-horizon efficiency follows from this extension.

## 3. Unknown visible normalization can be acquired

A known bounded raw preparation function 0<=g(Y)<=G with Z=mu g>0 is enough.
Accept independent baseline preparations with probability g/G; the marginal
accepted law has density f=g/Z. Its expected baseline preparation count is
G/Z. For a shared input in both words define the raw echo overlap

    L(u,v)=<g,P_u P_v^* g>.

Then the exact normalized distance is

    D(u,v)=[L(u,u)+L(v,v)-2L(u,v)]/Z^2.             (5)

Acquire Z using actual baseline readings of g, and acquire the three raw
echo entries. On a joint confidence event with Z>=Z_->0 and raw numerator
upper bound N^+, the valid distance bound is

    D^+ = max{0,N^+}/Z_-^2.                         (6)

The confidence allocation includes the normalization experiment. A failed
positive lower bound on Z calls for more data or a weaker conclusion; it is
not silently replaced by an exact equilibrium label probability.

For a fixed-label input g=1{Y=a}, the rejection and retained-record supplier
in the record supplement applies. The main witness can also be executed
without knowing Z: use raw adjoint reports bounded by G max(W_u,W_v).
Its expectation difference is Z D/[2G max(W_u,W_v)]. Bounds on Z convert
the observed response to the corresponding normalized statement.

Distinct raw input functions need their separate normalization intervals
and the resulting conservative interval for the three scaled entries.
No full hidden normalization constant or potential has to be reconstructed.

## 4. What a finite input family does and does not qualify

Suppose input labels a have actual conditional densities f_a, and two
preparation words u,v have certified distances D_a. For any declared mixture
of inputs, retaining the input label, joint TV after every common receiver
is at most (1/2)sqrt(sum_a p_a D_a). In particular max_a sqrt(D_a)/2 controls
all label mixtures with no mixture-key omission. This is a useful classical-
input preparation interface, not a channel norm over arbitrary hidden inputs.

The distinction is sharp. A frozen hidden bit initially uniform can be
flipped or left alone with identical output ensemble, while the two maps
act differently on a nonuniform hidden-bit input or a bit correlated with
an old record. No supplied probe that never creates such input correlations
qualifies those maps on them. The theorem does not infer a diamond-norm or
uniform Markov-kernel distance from one input's output-density distance.

For J fresh qualified executions, a hybrid coupling gives joint later-record
TV at most the sum of the J conditional preparation errors, plus the single
calibration-failure allowance if one simultaneous event covers them all.
It is not necessary to pay that same calibration failure J times.
Each execution still pays its actual conditional preparation and apparatus
cycle. Reusing one specimen without that supplier is outside this corollary.

If a replacement is to be used recursively inside a larger computation,
every actual intermediate input must lie in the qualified input family or
receive another warranted error bound. The one-preparation all-future result
does not permit replacing later operations in only one of the two compared
future controllers. Those would no longer be a common receiver.

## 5. Physical scope

The baseline, controlled calls and visible weights are inherited actual
interfaces. Their full reversible hidden state and switching map must be
correct. A finite-data visible fit alone cannot verify microscopic detailed
balance or exclude a hidden apparatus memory channel. The current theorem
uses no new preparation, microstate-copy, inverse-noise or time-reversal-mirror
oracle beyond these declared operations. It also does not build a new
detector or show that an arbitrary unknown material exposes this interface.

The foundational consequence is precise: on the physically reachable
family, actual adjoint-word experiments furnish a complete hidden-ensemble
metric, a constructive falsifier, and a finite-data receiver for every later
common intervention. The remaining apparatus costs and the family restriction
are part of that consequence, not evidence of a universal control capability.
