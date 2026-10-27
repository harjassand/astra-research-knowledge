# Exact observation replacement with charged classical raw access

## Contract and result

Let K be an m-by-n and L a k-by-n column-stochastic rational matrix. A source
already holds a **classical** symbol X in {0,...,n-1}. In one round, the module
receives a fresh private record Z~L(.|X). It may request the current raw X once,
at unit charged cost, before producing Y. The source's internal use of X to
produce Z is part of the L service, not a free raw disclosure to the module.
Reading or transferring X to the module is the charged operation.

The caller/controller receives Y. It receives neither Z nor raw-read flags,
raw values, private randomness, nor simulator memory. A controller may have an
arbitrary finite quantum reference, prepare the next **classical** X adaptively,
and update its reference between rounds. The L noise is fresh conditional on X;
a reference correlated with that same internal noise is outside this contract.
The module has no access to the controller's quantum reference. Measuring a
coherent input to manufacture X would be a different, additional operation.

A locally exact module must implement K for **every possible current x**, at
each full private history immediately before the new Z is generated. This
counterfactual correctness requirement is the modular interface. It is stronger
than correctness merely averaged over hidden internal states or over a promised
input source. The history includes all previous read flags, observations,
outputs and retained raw values; it excludes the fresh random bits used in this
round. A module can change its rule with that history.

The construction below has three separate conclusions:

1. A rational LP gives the exact one-step minimax raw-read probability q*.
2. For T rounds, the compiled module is exactly K under arbitrary admissible
   feedback, including finite quantum side references, and its raw-read count
   N_T is stochastically dominated by Bin(T,q*). Among the locally exact modules
   just defined, the worst-case count tail has the exact minimax value
   Pr[Bin(T,q*)>B].
3. Stopping before raw read B+1 produces an experiment within that binomial
   tail of the ideal record in total variation, or half trace norm with a
   quantum reference. This is an **upper error bound**, not an optimization of
   hard-budget simulation error. A useful fallback or globally approximate
   simulator can improve the actual error.

## One-step construction and completeness

Let U be an m-by-k nonnegative matrix. Put s_z=sum_y U_yz and require

    s_z <= 1,             U L <= K entrywise.                         (1)

Define r_z=1-s_z, D=K-U L and

    q_x = 1-sum_z L_zx s_z = sum_y D_yx.                              (2)

Given z, choose outcome y without a raw read with probability U_yz for each y;
with the remaining probability r_z, request X. If the raw value is x, choose y
with probability D_yx/q_x. Ignore z on this queried branch. If q_x=0, the
queried branch has zero probability for that x; choose its unused rule
arbitrarily. This uses valid distributions because D>=0 and (2) holds.
For each x,y, its total output probability is exactly

    sum_z L_zx U_yz + sum_z L_zx r_z D_yx/q_x
       = (UL)_yx + D_yx = K_yx.                                     (3)

The no-read/query decision is made without knowing X. The code's raw callback
is only invoked on a query branch.

Conversely, fix a private pre-round history of any permitted one-step protocol.
Before its first raw request, it has only Z and X-independent private
randomness. Therefore

    U_yz = Pr[no raw request and output y | record z]

is independent of x. Its columns have mass at most one. The probability of
output y on the no-read branch at input x is (UL)_yx; exactness forces this to
be at most K_yx. Its raw-read probability is exactly (2). Its post-query output
rule can depend on x and z, but (3) replaces it with a rule depending only on x,
without changing either the output channel or raw-read probabilities. Repeated
reads of the same current classical symbol can be cached. Thus (1) describes
all one-step possibilities in the declared resource contract.

Consequently the exact acquisition problem is the rational LP

    minimize q
    U>=0, q>=0,
    sum_y U_yz <= 1                              for each z,
    sum_z U_yz L_zx <= K_yx                      for each y,x,
    1-sum_z L_zx sum_y U_yz <= q                 for each x.          (P)

U=0,q=1 is feasible, so 0<=q*<=1. U is in a compact product of substochastic
simplices; restricting q to [0,1] changes no optimum. A rational optimum exists.

q*=0 exactly when K is a stochastic postprocessing of L. Indeed D>=0 and
zero column masses force D=0. Every record z reachable at some x then has
s_z=1; unused z columns can be completed arbitrarily to a stochastic matrix.
Conversely a stochastic A with K=AL is a q=0 solution. This includes singular,
rectangular, and zero-entry channels; positivity/invertibility are unnecessary
for this new compiler.

## Exact dual and a least-favorable fresh input

For nonnegative numbers beta_z, alpha_yx and pi_x, consider

    sum_x pi_x <= 1,
    beta_z + sum_x alpha_yx L_zx >= sum_x pi_x L_zx   for each y,z.    (4)

They give the lower bound

    ell = sum_x pi_x - sum_z beta_z - sum_yx alpha_yx K_yx <= q*.    (5)

This is the ordinary LP dual of (P). The independent certificate checker
verifies (1), (2), (4), and equality ell=q by exact rational arithmetic.
When q*>0, complementary slackness gives sum pi=1 in an optimum: q is a
strictly positive primal variable. Write this probability vector as pi*.

For every feasible U, not just the minimax solution, (4) yields

    sum_x pi*_x q_x(U)
      >= 1-sum_z beta_z-sum_yx alpha_yx K_yx = q*.                  (6)

To see the direction directly, replace beta_z by beta_z s_z and alpha_yx K_yx
by alpha_yx(UL)_yx; both replacements can only increase the right side of (5).
Then apply (4), multiplied by U_yz and summed over y,z. At a minimax optimum,
q_x<=q* for all x, so equality holds in (6); every x in pi*'s support has
q_x=q*. If q*=0, no lower-bound witness is needed because every count tail is
nonnegative and the zero-query compiler attains zero.

pi* is a dual adversary, not a promised restriction of the raw alphabet. A
module promised that X only lies in some subset can legitimately use the
restricted channel problem instead, with potentially smaller cost. That is
not the universal local interface (P).

## Adaptive exactness and complete side-reference semantics

At a fixed private history h, (3) is an identity of classical channels for
each input basis state. Hence it remains exact on an arbitrary cq state

    rho_XR = sum_x |x><x| tensor rho_R^x

with positive, possibly noncommuting and subnormalized rho_R^x. Both ideal
and simulated Y,R outputs have y block sum_x K_yx rho_R^x. No dimension,
commutativity, entropy approximation or asymptotic limit is used here.

The stationary compiled U* satisfies this identity at every history. Summing
out private histories, then composing with the next controller operation,
proves exact equality of the entire Y record and final reference by induction.
The controller can be quantum and the next classical X can be correlated,
persistent, or chosen from past outputs. Its input distribution need not be
known to the compiler. Reading an already classical X has no additional
conditional disturbance of R; this statement supplies no coherent-input
measurement capability.

This is not equality of the joint law of (Y,Z,read flags,X). Those internal
variables can carry additional information. Exposing them to the controller,
using the same internal L noise in an external reference, or promising to
preserve an ideal independently generated (Y,Z) pair changes the experiment.

## Exact minimax count tail at the local-module scope

Let B_t be the indicator of a raw read at round t. Under U*, even conditional
on the complete private pre-round history and any current classical input,

    Pr[B_t=1 | history, X_t=x] = q_x(U*) <= q*.                     (7)

Averaging over any cq input distribution preserves (7). A Bernoulli sequence
with conditional success probabilities at most q* is stochastically dominated
by independent Bernoulli(q*) variables: use fresh independent uniform V_t to
realize B_t=1{V_t<=p_t(history)} and compare to 1{V_t<=q*}. This couples the
count to a pathwise larger binomial count. Thus

    Pr[N_T>B] <= b(T,q*,B) := sum_{j=B+1}^T C(T,j)(q*)^j(1-q*)^(T-j). (8)

For the lower bound, let the source choose fresh independent X_t~pi*, with no
correlation to the simulator's initial private state or randomness. This is
one admissible controller/source. Conditional on every full private history,
its current X is still pi*. Local exactness and (6) imply

    Pr[B_t=1 | full private history] >= q*.                         (9)

The reverse uniform coupling shows that its count stochastically dominates
Bin(T,q*), even when its module changes rule with its history. For U*, the
conditional probability is exactly q* under this adversary, so equality is
attained. Therefore, for each integer budget B,

    inf_(locally exact causal modules) sup_(admissible sources/controllers)
               Pr[N_T>B] = b(T,q*,B).                              (10)

The same stationary U* simultaneously attains every count-tail minimum. The
lower bound already uses a classical source; quantum side-reference access
by the controller cannot invalidate it. This theorem does not optimize over
simulators that are correct only after averaging private states, over delayed
block-output algorithms, or over all globally approximate simulations.

For a *known* persistent raw X, an ordinary implementation may pay once and
cache X for all later rounds. Equation (8) remains a valid upper bound for
our compiler in that context, but (10) is not a context-specific optimality
claim there. Its worst case permits fresh inputs. Known reachability or
source restrictions must be supplied equally to competing methods and can
change the local alphabet/interface.

## Hard budget and approximation error

Run the exact compiler until it would request read B+1. Stop before that
access, emit a distinguished abort record, and apply any fixed admissible
continuation/fallback to the retained reference if a fixed final time is
required. Couple this with the full exact execution using the same private
randomness until abort. The abort event is exactly N_T>B in the full process.

For classical records, the two executions coincide off this event, so total
variation is at most (8). For a quantum reference, private random/read paths
are classical CP branches. The ideal and truncated final states have a common
positive subnormalized part G from nonaborting paths. Their remaining positive
parts each have trace p=Pr[abort]. Therefore

    (1/2)||rho_ideal-rho_truncated||_1 <= p <= b(T,q*,B).             (11)

No square root is needed. The truncated output space includes the abort flag;
the ideal is embedded with no abort. A different physical protocol or a
controller that observes private cost information is not covered by (11).

Equation (10) proves minimax optimality of the **exact execution's count**.
It does not prove that the best B-read approximate simulator has error (8).
The fallback may remain partly correct on budget exhaustion. Conditioning on
no abort can bias the record; its conditional law is not generally K's
unconditional law. An always-read strategy gives an exact budget of T; no
fixed smaller all-horizon exact budget follows from this theorem.

## Acquisition, precision and resource costs

(P) has mk+1 variables and k+mn+n inequalities, apart from nonnegativity.
It is an ordinary rational LP with polynomial-size rational optimal
certificates. Standard polynomial-time rational LP algorithms may be used;
this is existing optimization capability, not a new complexity result.
The implementation instead uses exact Fraction simplex with Bland's rule.
Set v=1-q, maximize v, and transform every inequality a_U U+a_q q<=b into
 a_U U-a_q v<=b-a_q, adding v<=1. All RHS are nonnegative, so U=0,v=0 supplies
an initial feasible slack basis, including at zero entries. Bland's rule
terminates on bounded LPs. The returned exact primal and dual are checked
separately. The pivot count can be exponential; no polynomial runtime or
conditioning-independent performance guarantee is claimed for this backend.

Each rational basis/tableau value has a determinant-size encoding bounded by
polynomials in the LP dimension and input encoding. Verification is polynomial
in the explicit certificate size and uses no solver. The code reports actual
pivot counts and largest tableau numerator/denominator bit lengths for these
runs. Complete fresh-process replay times include reading, startup, checking
and serialization; they exclude prior research, failed construction, source
calibration and operating-system setup, which are separately identified.

The runtime stores rational tables for no-read choices at each z and queried
choices at each x. Integer rejection samples a table with denominator d from
ceil(log2 d) fair bits per attempt, acceptance above 1/2 (or one at powers of
two). This is exact with finite expected random-bit/runtime cost, not a fixed
worst-case time or a floating approximation. Counts charge raw disclosures;
they do not equate a disclosure with one physical bit. One L-service call,
its calibration/representation, output storage and all arithmetic are extra.
Archiving queried X values costs up to N_T ceil(log2 n) bits plus indexing;
read flags/positions also cost bits and may leak information. Neither the
output archive nor simulator bookkeeping is free or automatically compressed.

For q=a/b rational, (8) is a rational with denominator dividing b^T. The code
computes it with exact integer binomial recurrence. It needs O(B+1) arithmetic
steps for the lower CDF (or at most O(T)), on integers with O(T log b+log T)
bits. Writing the exact answer already has up to O(T log b) bits. There is no
polynomial-in-log(T) exact-tail claim. Rational quantile search returns the
smallest budget certified by (8), not the globally optimal hard-budget error.

Input matrices are supplied exact finite data. Their physical acquisition,
validation and drift are not solved by this compiler. If actual channels are
only approximate versions of those matrices, additional channel-error
composition is required; the exact claims are not calibration guarantees.
