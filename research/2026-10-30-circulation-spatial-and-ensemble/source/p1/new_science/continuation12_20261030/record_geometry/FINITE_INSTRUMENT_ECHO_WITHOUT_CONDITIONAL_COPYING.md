# Finite record instruments: joint echo qualification without conditional copying

30 October 2026. Constructive receiving extension by the existing
record-geometry role. It supplements root's ensemble-echo construction.
The independent sparse-load alternative remains unchanged.

## 1. Actual prefix and retained record

Use root's common-equilibrium interface: actual Markov calls P_j are
self-adjoint on L2(mu); a fresh baseline mu and a known bounded visible
input density f(Y), 0<=f<=B, integral f=1, are warranted.

A supplied finite causal prefix produces an actual finite record R.
Its branch operator A_r is positive and substochastic, with sum_r A_r1=1.
The prefix may choose later calls from earlier visible labels and retain
its actual random selector keys. For each complete record r, its known
branch factors are finite products of the actual calls and visible
nonnegative multiplication operators. Label checks are multiplication by
indicators; recorded random choices contribute their actual known
conditional selection probabilities.

This is not an arbitrary unknown measurement instrument. Each factor's
adjoint must be experimentally available. Invasive sensors, hidden-state
selectors, or extra accessible clock records need their own joint supplier.
Merely observing a transcript does not create its adjoint.

Set a_r=A_r^*f and p_r=integral a_r dmu. Real deployment starts from
f mu and runs the prefix, giving joint record/state measure a_r mu.
The conditional density a_r/p_r need not be a function of the current
visible label and is not assumed to be directly evaluable.

After record r, use candidate u_r or reference v_r. Their unnormalized
joint output densities and difference are

\[
b_r=P_{u_r}^*a_r,\qquad c_r=P_{v_r}^*a_r,\qquad
\Delta_r=b_r-c_r.                                         \tag{1}
\]

Both words are Markov, so their record marginals remain p_r. Let S
be the records on which replacement is attempted. On every other
record execute u_r=v_r exactly. Those branches have zero replacement
error, not an assumed conditional preparation.

## 2. Design weights replace unknown conditional probabilities

If S is empty, use the reference everywhere and the joint error is zero.
Otherwise choose any known positive q_r on S with sum_(r in S) q_r=1. These
are numerical design weights, not a claim about the physical context
law. Freeze them and the branch programs before fresh validation.
Define

\[
\mathcal D_q=\sum_{r\in S}\frac{\|\Delta_r\|_2^2}{q_r}.
                                                               \tag{2}
\]

The actual complete joint record/state law, and every later common
causal receiver using both r and the complete included physical state,
satisfy

\[
\operatorname{TV}({\cal L}_u,{\cal L}_v)
\le\frac12\sum_{r\in S}\|\Delta_r\|_1
\le\frac12\sqrt{\mathcal D_q}.                              \tag{3}
\]

The final step is Cauchy--Schwarz against the probability measure
q_r mu(dx). It does not require q=p. Before a later receiver, the
first inequality is equality.

If the actual p are known and all records are included, q=p recovers
root's normalized conditional objective sum_r p_r
||b_r/p_r-c_r/p_r||². That normalization is an optional specialization,
not a prerequisite for joint-law qualification.

The rare-context cost remains. Uniform q gives an alphabet-dependent
report range. Pilot-informed q can improve the range or objective,
but must be frozen before validation. A zero q is legitimate only
where the reference is executed unchanged.

For fixed nonzero branch errors the mathematical optimum is q_r
proportional to ||Delta_r||_2, with minimum (sum_r ||Delta_r||_2)².
If an included branch has zero error, this is the corresponding
infimum over strictly positive weights; assigning it zero weight
under the actual protocol still requires the unchanged-reference
rule. Learning useful weights requires actual pilot data and fresh
validation; the identity does not reveal unknown errors for free.

## 3. One actual chronological trajectory acquires each overlap

For each of three echo types start an independently warranted mu
specimen and read f(Y_0). Run the actual prefix and obtain its real r.
If r is outside S report zero. Otherwise a cross echo executes:

1. the candidate word u_r;
2. the reversed actual calls of v_r;
3. the adjoint branch A_r^*, by reversing its factors, reading the
   appropriate visible label checks, and multiplying its known
   branch probability coefficients;
4. the final visible value f(Y_end).

Report

\[
Z_{uv}=\frac{f(Y_0)f(Y_{\rm end})}{q_r}
 \times(\hbox{reversed branch checks and coefficients}).    \tag{4}
\]

Failed reversed checks give zero. They do not request a second future
from the original hidden state. The forward A_r probability is already
supplied by the actual observed prefix and is not multiplied again.
The reversed coefficients are needed because they belong to A_r^*.
For example, a recorded selector probability s appears once through
the real forward event and once in its reversed adjoint report.

Chronological conditional expectation gives

\[
E Z_{uv}
=\sum_{r\in S}\frac{
 \langle f,A_rP_{u_r}P_{v_r}^*A_r^*f\rangle}{q_r}
=\sum_{r\in S}\frac{\langle b_r,c_r\rangle}{q_r}.            \tag{5}
\]

The u,u and v,v types give the diagonals; their combination is (2).
The calibration prefix's unweighted r frequency is its mu-input
frequency, not generally deployment p_r. The actual initial factor
f(Y_0) in (4) supplies the correct forward a_r.

There is no conditional specimen sampler or externally simulated
context in this construction. In the common-mu case every reversed
branch multiplier is at most one, so

\[
0\le Z_{uv}\le B^2/q_{\min}.                               \tag{6}
\]

The adjoint branch is a substochastic operator represented by a
positive report, not a stochastic trajectory inverse. Prefix and
reverse-prefix duration, failed checks, restoration, sensing and
fresh sources are all actual costs.

## 4. Confidence, selection, and an optional p-normalized bound

With n independent trials per echo type, the simultaneous Hoeffding
entry radius

\[
r_n=\frac{B^2}{q_{\min}}
 \sqrt{\frac{\log(6/\alpha)}{2n}}
\]

gives, with probability at least 1-alpha,

\[
\mathcal D_q\le\max\{0,\widehat{\mathcal D}_q+4r_n\},\qquad
\operatorname{TV}_{\rm later}
\le\min\{1,\tfrac12\sqrt{\max\{0,\widehat{\mathcal D}_q+4r_n\}}\}.
                                                               \tag{7}
\]

Pilot data may select S, q and the entire branch policy. Conditional
on that pilot, these are fixed; fresh validation and an actual
conditional baseline supplier justify (7). A fixed finite library
can instead be covered simultaneously. Choosing q on the same
unprotected validation data and treating the report as predetermined
would be invalid.

For each complete calibration history C, the next deployment must
have the declared conditional input and future operation law. If a
simultaneous event of probability at least 1-alpha guarantees the
selected objective at most d, attaching that same C to both laws gives
joint later-record TV at most alpha+sqrt(d)/2, capped at one. No
conditioning of an already correlated specimen into a fresh source
is inferred. The record r from the actual deployment prefix remains
part of the joint output throughout.

If actual conditional probabilities are desired, acquire p_r from
real f-mu prefix trials or from baseline reports f(Y_0)1{R=r}.
An unweighted calibration-prefix frequency does not supply p_r.

Freeze independent positive lower confidence bounds p_-r on S.
The positive weighted objective

\[
\mathcal D_-=\sum_{r\in S}\|\Delta_r\|_2^2/p_{-r}
\]

dominates sum_(r in S) ||Delta_r||²/p_r on the normalization success
event. Its three entries can then be freshly validated. Positivity
of each per-record squared norm is essential: inconsistent interval
normalization of signed cross terms would not give this argument.

For joint TV alone, the design-weight theorem (2)--(7) avoids the
conditional-probability acquisition stage. It retains the precision
bill in q_min and the full physical trial cost.

## 5. A literal joint-record witness

Put C=B/q_min. Given an actual candidate state and retained r in S,
choose a fresh fair bit. On one branch execute the adjoint of
A_r P_(u_r): first reversed u_r, then the adjoint branch A_r^*.
Its nonnegative endpoint/branch report F_(r,u) is at most B and has
conditional expectation b_r(x). Return 1 with probability
F_(r,u)/(C q_r). On the other branch use v_r and return 1 with
probability 1-F_(r,v)/(C q_r). For r outside S return a fair bit.

Thus the conditional response is

\[
\phi(r,x)=\tfrac12+\frac{\Delta_r(x)}{2Cq_r}
\quad(r\in S),
\]

which lies in [0,1]. The actual joint response difference is

\[
\Pr_u\{1\}-\Pr_v\{1\}=\mathcal D_q/(2C).                   \tag{8}
\]

This tests the retained-record law. It does not discard the mixture
key. It uses fresh actual forward calls, visible checks and known
classical probability synthesis, with no hidden-state copy.

## 6. Unknown raw-input normalization and weighted calls

For known 0<=g<=G and unknown Z=mu g>0, replace f by g in all raw
echoes and let a_r=A_r^*g. The deployed joint densities are b_r/Z
and c_r/Z, so

\[
\operatorname{TV}_{\rm joint,later}
\le\frac{\sqrt{\mathcal D_q^{\rm raw}}}{2Z}.                \tag{9}
\]

Only one global normalization is needed. Acquire it from actual
baseline g readings and use Z_->0 on a joint confidence event.
Conditional record probabilities are not required. The actual
preparation g mu/Z and any accepted label or clock still need
their joint source contract; the algebra does not erase rejection
history.

The raw witness uses C=G/q_min and has joint response gap
\(\mathcal D_q^{\rm raw}/(2CZ)\). Exact Z need not be implemented in
that test.

For calls reversible with respect to mu w_j, insert their actual
endpoint ratios in the reversed u/v/prefix segments. Visible
multipliers remain self-adjoint. Identity (5) survives, while the
report and witness ranges acquire the actual adjoint weight
products. The forward prefix does not receive an invented weight.
Unknown kinetic prefactors remain allowed only for the same actual
acquired and deployed conditional operations.

More explicitly, let W_(A_r) bound the endpoint-weight product on
the reversed prefix branch and W_(w_r) the product on reversed word
w_r. Visible branch checks and selection factors still lie in [0,1].
A valid common witness constant and echo range are

\[
C=B\max_{r\in S}
 \frac{W_{A_r}\max\{W_{u_r},W_{v_r}\}}{q_r},
\qquad 0\le Z_{\rm echo}\le BC.                         \tag{10}
\]

The raw-normalization version replaces B by G. Known telescoping
can improve these bounds; no such improvement is assumed. Finite
precision in evaluating weights, q or endpoint probabilities must
have its actual report or conditional test-error budget.

## 7. Four-state test and physical limits

Let X=(Y,H) be two uniform baseline bits, and supply f=2 1{Y=0}.
The prefix swaps Y,H, then records r=Y. Consequently

\[
p_r=1/2,\qquad a_r=2\,1\{Y=r,H=0\}.
\]

Candidate identity and reference H-flip have joint TV one. The
conditional densities are 4 1{Y=r,H=0} and 4 1{Y=r,H=1}.
With q_r=1/2, \(\mathcal D_q=8\) and C=B/q_min=4. The TV upper bound
is capped at one, while the witness gap equals 8/(2*4)=1.
It distinguishes them exactly using the actual reverse prefix.

Replacing the true conditional input by its visible projection
2 1{Y=r} would instead give a false zero defect. The prefix echo
never makes that replacement.

Finite complete records, compatible adjoints, actual conditional
baselines, and known visible multipliers are substantive requirements.
An accessible continuous clock is not silently coarsened. A generic
old trajectory is not automatically an instrument of this form.
Calibration-history attachment and fresh-repeat composition use
root's conditional hybrid argument. Recursive reuse on unqualified
inputs does not follow from one preparation.

This is a constructive extension, not a conditional state copier,
universal sensor, free initializer or cheap rare-context sampler.
