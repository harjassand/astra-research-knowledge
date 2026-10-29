# Sample-only teacher acquisition at fixed compiler tolerance

30 October 2026. Full proposed producer operation, pending independent whole
challenge. All accepted files in the parent t_predictive folder stay frozen.
This is not a new benchmark or an assertion of practical complexity.

## 1. Consequence, established machinery and exact input

The accepted compiler needs arbitrarily accurate probability VALUES of its
teacher. Estimating those original probabilities from samples at its requested
absolute precision can be exponential in horizon. The changed representation is
to acquire a RANDOM RATIONAL teacher and perform fine probability arithmetic on
that acquired law. Extra digits then consume internal arithmetic, not fresh
statistical information. Liu--Moitra2411.07536v1 §4.1 Claim4.1, Lemma4.6 and
Remark4.7 already construct consistent lazy empirical probability trees. This
operation is explicitly credited, not reinvented as a new principle.

The additional interfaces paid here are (i) queries to the original Q are allowed
ONLY at positive-Q prefixes, (ii) P is a different low-rank source, related by
global KL rather than uniform conditional accuracy, and (iii) full composition
must return a finite autonomous model without either oracle. The root's
SAMPLE_TEACHER.md independently identifies this same strongest ordinary route;
its model-selection extension is separate from this fixed-tolerance producer.

Inputs: O>=2,T>=1,r>=1; iid FULL P trajectories; independent conditional future
samples from Q at positive-Q prefixes. No probability VALUE service, P likelihood,
conditional-P sample, minimum nonzero Q probability or Q-rank promise is supplied.
The actual conditional-Q and P acquisition costs are multiplied in. Source
queries are independent across calls and independent of compiler/holdout random
bits. Predictive linear rank(P)<=r at every cut remains a promise.

Fix rational failure probability delta in(0,1/4) and rational

    A=ceil[1000(r+O+T+4/delta)],  0<tau<=1/(100A),  x=A/tau.

The algorithm builds a VALID finite teacher-free candidate for every P,Q. If
the actual (possibly unknown) d=D(P||Q) satisfies

    d<=x^(-10000),                                      (1)

then, with probability at least1-delta,

    D(P||P_hat)<=x^(-4096)+40T(B+1)tau,
    B=log[((r+1)8(r+1)/a+2)/(theta*a^T)],
    a=tau/(2O), theta=tau/[4(r+1)].                      (2)

No numeric bound d is an ALGORITHM input at fixed tau. Condition(1) is a sufficient
accuracy premise, not a test by the learner. Root separately constructs a grid/
Scheffe selector; no Delta-oblivious global theorem is claimed by this file alone.
The fixed-tau calls, rational arithmetic, stored bits and inference have fixed
polynomial bounds in x,r,O,T and encoded input length, relative to source sample
costs. The exponents are enormous and do not imply useful finite data budgets.

## 2. Independent conceptual empirical tapes

Put rho=alpha=x^(-8192), beta=delta/4. Conceptually assign to EVERY positive-Q
prefix h of length<T an independent tape of m conditional-Q future draws at h.
Only the first token of each draw is used to form counts c_h(o), fractions
e_h(o)=c_h(o)/m. Descendant fragments of those futures are NOT reused as another
node's conditional draws. The conceptual tapes are independent of P training/
holdout data and of all token/mixture-sampling uniforms.

Let

    L_m=ceil(log2(8/beta))+(T+1)ceil(log2 O)+1,
    m=ceil(L_m/rho^2).                                (3)

There are at most O^T non-leaf prefixes and at most O^(T+1) token events. Hoeffding
and a union bound give, with probability at least1-beta, the event

    E: |e_h(o)-Q(o|h)|<=rho
       for ALL positive-Q h and all o.                 (4)

The union pays the LOGARITHM of the number of conceptual nodes in m. It does not
materialize or query that tree. The algorithm reveals a node's independent tape
only on its first active visit, caches the count row, and never resamples it.
By deferred decisions this is statistically identical to the conceptual tree,
including arbitrary adaptive queries. Conditioning on the complete table makes
the acquired teacher a FIXED law before the compiler's feature draws are analyzed.

## 3. Support-safe floor: escape rather than query an invented prefix

Define a full-support law Qbar on length-T words. A root-to-word path initially
has an ACTIVE flag. At an active node h choose the next token with probabilities

    qbar_h(o)=(e_h(o)+rho)/(1+O rho).                    (5)

If the followed edge has c_h(o)=0, set the flag INACTIVE permanently; every later
token is uniform and no further original-Q query is allowed on that path. If
c_h(o)>0, then h o has positive Q mass, because it was observed in an actual draw
at the already verified positive-Q h. Thus every actual original-Q query is
support-valid, even outside E and even when d is infinite. Adding a floor without
this escape would not justify querying its new descendants.

For a specified prefix h the flag is a deterministic function of its ancestors
and the FIXED table: the first zero-count edge determines it. There is no
path-history ambiguity, no reactivation and no resampling on a repeated query.
The root is positive-Q. Induction proves support safety on every active path.
At an unvisited active node reveal its tape. Inactive suffixes need no tape.

Let G be the complete words whose path never takes a zero-count edge. On E,

    Qbar(w)>=Q(w)/(1+O rho)^T for w in G,
    Q(G^c)<=T O rho.                                  (6)

The first inequality multiplies e_h(o)+rho>=Q(o|h) along active paths. For the
second, under a Q trajectory, the first zero-count edge at an active node has
conditional probability at most O rho: every zero count implies Q(o|h)<=rho.
Union over at most T steps. This is a probability under Q, not a claimed uniform
conditional-P guarantee. Zero-Q words contribute zero to the first inequality.

## 4. One global uniform mixture supplies exact rational conditional values

Define

    R=(1-alpha)Qbar+alpha U,   U=Uniform([O]^T).         (7)

For a prefix h of length t, compute Qbar(h) by multiplying its rational rows,
including uniform factors after escape. Then

    R(h)=(1-alpha)Qbar(h)+alpha O^(-t)>0,
    R(o|h)=R(h o)/R(h),
    R(f|h)=R(h f)/R(h).                                (8)

These are exact RATIONAL values derived from finite counts, not estimates of
the original Q at fine precision. Any demanded extra value bits are ordinary
rational arithmetic. No original-Q VALUE is queried. A conditional R sample may
choose Qbar versus U from the exact prefix posterior, then use its active/escape
flag; equivalently sample the exact rows in(8). Even a uniform-component query
cannot cause an unsupported Q call: all Qbar evaluations obey the root-path flag.

A node row has O(log m+bits(rho)+log O) bits per integer/rational entry. A path
has at most T rows, so R prefix/conditional values have polynomial bit length
O(T[log m+bits(rho)+log O]+bits(alpha)). Products, sums and divisions in(8) do
not require knowing an unobserved original Q probability. Conditional R sampling
uses independent uniforms, separate from the empirical tapes. Rational categorical
sampling has expected polynomial fair-bit work; a fixed random-bit budget can
instead be given a separately paid approximation/failure allowance.

## 5. Global KL transfer, including the omitted mass

Work on E and assume d=D(P||Q)<infinity. Pinsker and(6) yield

    P(G^c)<=T O rho+sqrt(d/2).                          (9)

On G, R(w)>=(1-alpha)Q(w)/(1+O rho)^T, hence
log[Q(w)/R(w)]<=T O rho+2alpha. Everywhere on support(P),
log[Q(w)/R(w)]<=L=T log O+log(1/alpha), because R(w)>=alpha O^-T and Q(w)<=1.
The identity D(P||R)=d+E_P log(Q/R) therefore gives

    D(P||R)<=d+T O rho+2alpha
              +(T O rho+sqrt(d/2))L.                  (10)

There is no unproved pointwise original-Q multiplicative approximation on G^c.
Its P mass and logarithmic penalty are paid. Negative log ratios require no
lower bound for this upper estimate. Neither R nor Qbar is assumed low rank.

Here A>=20000, x>=100A^2, T O<=x^2 and
L=T log O+8192log x<=(A+8192)log x<=2x log x<=x^2.
Under(1), sqrt(d/2)<=x^-5000. With rho=alpha=x^-8192, (10) is at most

    x^-10000+x^-8190+2x^-8192+x^-8188+x^-4998
       <=6x^-4998 <=x^-4997 <=x^-4096.                 (11)

The constants are intentionally conservative. No epsilon-dependent log is
multiplied into a claimed uniform d-modulus here: rho and alpha are chosen from
the FIXED tau that also governs the compiler's accuracy/noise premise. Choosing
them solely from the requested final epsilon and then ignoring log(1/epsilon)
in the noise term would be an invalid transfer.

## 6. Complete compiler composition and all conditional-Q costs

Condition on a complete empirical table satisfying E. The acquired R is fixed,
full-support and supplies exactly the VALUE/conditional-sample interface needed
by the accepted t_predictive/PROOF Sections2--6. Give that fixed-tau construction
confidence delta/4 and the promised bound x^-4096. Its actual implementation
does not use or verify the original d; every resource schedule depends only on
tau,A,r,O,T,delta. By(11) its accuracy premises hold. P trajectories and compiler
sampling uniforms remain independent of the empirical table. The conditional
probability of its good acquisition/gradient events is at least1-delta/4.
Together with Pr(E)>=1-delta/4, this proves(2), leaving slack for explicit finite
random-bit adapters/rounding budgets. The original accepted finite-precision
proof is applicable; exact rational R also permits its teacher cache values to
be computed exactly before any paid rounding.

Let B_R be a deterministic polynomial cap on all R prefix/conditional-value/
future-sample calls in the fixed-tau compiler. Each such call exposes at most T
new active original-Q nodes. Consequently at most T B_R independent count rows
are acquired, costing at most

    m T B_R original conditional-Q FULL-FUTURE draws,
    m T^2 B_R returned source symbols.                 (12)

Unused descendant symbols are discarded, not reused as free conditional samples.
The actual time/precision/reset cost of each original conditional-Q draw is an
input service cost. Each acquired row and rational prefix product has the bit
bound in Section4. Since m is a fixed polynomial in x with exponent16384 and
only polynomial T/confidence factors, all composition costs are fixed polynomials.
There is no exponential-in-T probability-estimation precision bill. The conceptual
tree, despite exponentially many possible nodes, is never an output or memory
allocation. The final generator stores only the accepted compiler's finite cache
and deterministic inference algorithm; discard the empirical table and both
source handles when compilation ends.

## 7. Unconditionally valid bounded-work candidates

This is needed for root's separate unknown-d selection. The guarantee(2) is
conditional; existence of a valid model and known work cap must not be.

* If finite geometric retention cannot certify its known threshold gap, retains
  more than r directions, or exceeds its fixed work budget, return the uniform
  candidate. These fallbacks are invisible on the proved good geometry event.
* Every cached R token row is an exactly normalized rational probability vector.
  For any sum-alpha1, |alpha_i|<=C, all signed marginal l1 norms are<=SC. Thus
  the clipped token denominator is positive and bounded by SC+O b, even on bad
  candidates. If that denominator exceeds2, use a permanent uniform-suffix flag
  on this history rather than invoking a projection with pi<a. On good states
  it is<=1+v+O b<2, so this completion does not alter the accuracy proof.
* At each projection start from the known uniform feasible coefficients, not a
  warm start with inherited arithmetic size. Round the log gradient to a FIXED
  rational grid within the allocated first-order error; use an exact rational
  LP vertex with deterministic tie-breaking and a fixed rational FW step. Bounded
  curvature/objective gives a fixed polynomial number of steps. Cached rational
  constraints give a fixed vertex determinant bit bound. Coefficient bit sizes
  therefore have a fixed polynomial bound independent of parent denominators.
  If the prescribed cap cannot certify its gap, switch to a uniform suffix.
* Log approximation uses a warranted deterministic finite series followed by
  rational grid rounding. It never waits to decide whether a true logarithm is
  exactly a rounding-grid boundary. All categorical rounding/fallback conventions
  are fixed, making each completed candidate a deterministic autoregressive law
  once compilation randomness has been frozen.

These are scope-correct completions rather than new statistical promises. They
do not grant accuracy to a bad teacher or verify its KL bound. They permit
teacher-free likelihood comparison and sampling of every finished candidate.
Source queries all occur before these inference operations and remain capped.

## 8. Evidence and boundaries

This file is a constructive mathematical operation, not a finite-source success
claim. The accompanying generic adapter implements exact rational empirical-tree
prefix/conditional values and samples; no new scientific source, P/Q trajectory
instance, optimizer or kinetic/network fixture has been run for this packet.
Strong ordinary access is retained: the underlying consistent empirical-tree
primitive is Liu--Moitra prior, and the strongest short-horizon teacher trie and
EM controls from the frozen compiler still win their declared finite costs.

Practical sample counts, moderate misspecification, historical novelty, actual
scientific reset/conditional sampling, inference package validation and physical
world-model acquisition remain unacquired. The result uses original Q samples
only, but that conditional-sampling service remains a substantive supplied
capability. Root owns the separate unknown-KL grid/tournament and global error
constants; A owns independent whole challenge of this producer operation.
