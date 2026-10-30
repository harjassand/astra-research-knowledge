# Record-conditioned learning and the complete execution cycle

30 October 2026. Root supplement to
`REACHABLE_ENSEMBLE_ECHO_AND_UNSEEN_CONTINUATIONS.md`. Working version.

## 1. A marginal preparation is not its retained-record preparation

The main theorem starts from an actual density f relative to a warranted
baseline mu. If f is prepared by rejection using f(Y)/B, the accepted
specimen has this density marginally. A stored accepted label changes the
conditional input law. It must be included in the receiver, not treated as
a free erased bit.

A particularly clean supplied input family is

    f_a(x)=1{Y(x)=a}/mu{Y=a},   mu{Y=a}>0.             (1)

Reject independent baseline specimens until label a is obtained. The accepted
label is fixed. For genuine independent baseline preparations, the rejected
specimens, their labels, and the trial count are independent of the accepted
hidden state conditional on a. Thus the actual accepted state has law f_a mu
even given that retained history. The mean number of preparations is
1/mu{Y=a}; their preparation, sensing, rejected-material treatment and timing
must all be charged. Reusing one unequilibrated specimen does not supply this
independence. A fluctuating fabrication parameter shared by specimens also
requires a per-device or conditional analysis.

A general bounded f can be treated by keeping the accepted label a and
certifying its actual conditional input separately, or by supplying a real
record-isolation/reset operation. The main marginal identity remains true,
but it is not a complete-record statement merely because the acceptance
probability is known.

## 2. The correct joint distance has no gratuitous alphabet factor

Let R be an actual retained classical context with known sampling law p.
Conditionally on R=r, suppose the input f_r mu and the candidate/reference
words u_r,v_r are supplied. Assume 0<=f_r<=B uniformly. The same R is attached
to both compared output laws. Write

    rho_r=P_(u_r)^* f_r,       tau_r=P_(v_r)^* f_r,
    D_joint=E_R ||rho_R-tau_R||_2^2.                  (2)

Then, for every common causal receiver allowed to use both R and the entire
modeled physical state,

    TV(law(R,later record)_u, law(R,later record)_v)
       <= (1/2) E_R ||rho_R-tau_R||_1
       <= (1/2) sqrt(D_joint).                       (3)

The first displayed inequality is equality before applying a later receiver.
The second is Cauchy--Schwarz. No cardinality of R is needed. This is an
average over the *actual* context distribution, not a worst-case conditional
guarantee for an arbitrarily rare r. For a changed context law q with
dq/dp<=L, its squared-distance budget is at most L D_joint.

Crucially, (2) is acquired with actual calls: independently sample R from p,
prepare mu, execute the chosen echo, and report f_R(Y_0)f_R(Y_end). Three
echo types estimate the three expectations in (2). Each report is in
[0,B^2], regardless of the number of possible contexts. This does not need
two copies of the same hidden state or two native outcomes conditional on
one state. R can be sampled afresh for every echo type.

This input contract is substantive. An arbitrary old native trajectory does
not give a known f_r or an inexpensive sampler of its conditional hidden
state. If R arose from a controlled instrument A_r on a prior f mu, then

    f_r=A_r^* f / p_r,       p_r=mu(A_r^*f).           (4)

The normalization, its acquisition, and its conditional preparation are
real costs. Merely observing r once supplies none of them.

For unnormalized instrument densities a_r,b_r one instead has

    TV(joint laws)<= (1/2) sqrt(M sum_r ||a_r-b_r||_2^2)
                                                            (5)

when there are M transcript values and the same baseline measure is used.
This factor cannot just be removed from that unweighted objective. For
R uniform on M labels and a hidden uniform bit, let each conditional
candidate bit be a declared deterministic sign s_r while the reference bit
is uniform. Joint TV is 1/2; the sum of squared errors of the unnormalized
densities is 1/M. The correctly normalized quantity (2) equals 1.

## 3. A retained mixture key defeats cancellation

Take one binary state x=+1 or -1, baseline uniform, and an actual initial
preparation x=+1. Identity and a deterministic sign flip are reversible
fixed-call kernels for that baseline. A fresh fair selection bit J chooses
identity or flip. Marginal output is exactly uniform, so its marginal
distance to a uniform target is zero.

Retain J. The output is x=(-1)^J, whereas the reference with the same J
and an independent uniform state has joint TV 1/2. After m independent
uses, retaining all keys gives joint TV 1-2^(-m). This is the same exposed-
key mechanism preserved in the earlier accepted preparation corrections;
it is not a new impossibility theorem.

For a real mixture of reachable densities rho_i with key probabilities w_i,
the two relevant objectives are

    D_marg=||sum_i w_i rho_i-tau||_2^2,
    D_key =sum_i w_i ||rho_i-tau||_2^2.              (6)

The second controls the joint state/key record. Their exact difference is

    D_key-D_marg
       =sum_i w_i ||rho_i-sum_j w_j rho_j||_2^2.     (7)

Thus the apparent benefit of cancellation is exactly residual preparation
information carried by the key in this Hilbert norm. A generic marginal
Gram/QP learner does not pay that term. A competent ordinary learner can
use D_key when the key remains accessible; this is a linear mixture
objective, and does not gain fidelity below the best component by averaging.
A physical key-isolation/reset operation can change the useful interface,
but its work, side records and possible later return must be supplied.

## 4. Calibration selection and a deterministic learning receiver

For each fixed complete calibration history C, the actual next deployment
input must have the declared conditional law. The selected word w(C) is
fixed before this input is prepared. Reference deployment receives the same
C and the reference output law. On a simultaneous calibration event G,
suppose D(w(C),t)<=d. Then

    TV(law(C,later record)_actual,
       law(C,later record)_reference)
        <= Pr(G^c)+(1/2)sqrt(d).                    (8)

This follows by integrating the conditional TV bound, paying at most one on
the bad histories. It holds even if the future policy is chosen using all
of C. It does not condition a previously correlated specimen into a fresh
baseline state.

One exact receiver is ordinary selection among a fixed finite library:

1. Acquire or pilot-select candidate words and their actual resource costs.
2. Validate either all candidates simultaneously or one selected candidate
   on fresh conditional baseline trials, using the three echo entries.
3. Execute the least-cost candidate whose upper bound D^+ is at most
   4 epsilon^2, or retain the reference if none qualifies.

For uniform entry radius r, D^+_w=D_hat_w+4r. Every accepted candidate has
the stated all-future conditional TV bound. Every candidate with true
D_w<=4 epsilon^2-8r is accepted on the same event. Therefore the selected
cost is no larger than the cheapest candidate with that sufficient margin,
assuming exact optimization and correctly supplied costs. A conservative
failure to accept is not evidence that no useful replacement exists.

The library can be generated by a conventional search, a physical-learning
method or a scientist. The theorem does not bound the search complexity or
promise the existence of a cheaper word. Hidden-state dimension is absent
from the validation bound because the actual echo operation supplies a
specific inner product; it has not been paid away by an algorithmic slogan.

## 5. Precision and drift

The kernels acquired and deployed must be the same actual conditional
operations. Sharing an equilibrium measure does not establish that fact.
For a binary reversible kernel with flip probability p, a forward call at p
and a purported reverse call at q have centered correlation
(1-2p)(1-2q), whereas the required self-overlap is (1-2p)^2.
Unknown fixed rates are allowed; uncontrolled drift between calls is not.

Suppose a calibration echo has an initial total-variation error beta and
each executed call differs from its intended actual kernel by a uniformly
bounded conditional TV error eta_l. A coupled telescoping argument gives
record-law error at most beta+sum_l eta_l. For its [0,B^2] report, expectation
error is at most B^2(beta+sum_l eta_l). Add this bias to the corresponding
statistical entry radius. Every sensing, weighting and product-noise bias
needs its actual joint bound as well.

A deployed word with input error beta_dep and call errors eta_dep,l adds
at most beta_dep+sum_l eta_dep,l to the later TV budget. A reference with
its own mismatch pays the analogous term. These are sufficient uniform
budgets, not necessary hardware tolerances. If a useful receiver admits a
weaker error geometry, use its actual one instead of these worst-case sums.

For rejection with ideal acceptance f/B and an implemented probability
within eta of it pointwise, eta<1/B, the accepted-state TV error is at most

    B eta/(1-B eta).                               (9)

Proof: normalize the perturbed acceptance measure; its total mass is at
least 1/B-eta, and its unnormalized L1 discrepancy and normalization error
are each at most eta. This is a marginal bound. The retained accepted label
still belongs in the conditional preparation analysis above.

## 6. The full physical cycle is part of the comparison

Each echo trial consumes an actual baseline preparation, two complete word
segments (one in reversed order), two endpoint readings, required clock and
switch events, fresh physical randomness and a reported sample. The specimen
and apparatus then have to be restored or replaced before another claimed
independent trial. Restoration, retired reservoirs and failed rejection
specimens are not free because the final digital report is one number.

If a trial's complete qualified cycle costs c_echo and duration tau_echo,
and n trials are used for each of 2M+1 entries, the corresponding budget is
n(2M+1)c_echo and n(2M+1)tau_echo before any parallelization actually supplied.
For selected-word validation it is 3n cycles plus the full pilot budget.
Each c_echo must include its actual word-dependent lengths and restoration;
the notation is shorthand for summing unequal costs when necessary.

After training, a claimed amortized resource advantage over J deployments
requires

    C_calibration + J C_replacement < J C_reference. (10)

The C quantities must refer to the same complete-cycle resource, including
initialization, clocks, sensing, communication, control records, reset and
reliability. The norm theorem does not estimate them. Unknown-rate robustness
is not robustness to unmeasured apparatus work or conditional drift.

The present contribution is a mathematical and executable acquisition/
qualification principle at existing reversible-operation interfaces. It
does not establish an efficient instrument, autonomous hardware learner,
universal state initializer or a total-resource speedup. Ordinary optimizers
using the same physical correlations are equally entitled to its receiver.
