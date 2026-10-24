# A source-only reaction-event kernel with an all-input certificate

New Pro3 construction. The acquired object is a positive sum of local
operators representing an unnormalized first-event time-density kernel.
Its certificate is obtained from the scientific source before an initial
joint hidden-state law is chosen. The same object can subsequently act on
different supplied correlated entrances, including positive count-accumulator
tensor trains.

This is the main quantifier extension of
`nonstationary_opening_entrance_proof.md`. That file establishes the local
same-generator identities, reachable-support procedure and relative
quadrature bounds, and documents the deterministic-initialization executor.
Here the bounds hold entrywise for every local input state, turning a
certified fixed-input entrance into a certified scientific operator.

## 1. Source and operation

There are finite local state spaces E_i. During one preparation phase an
autonomous controller starts closed, opens once at rate gamma>0, and then
remains open until the observed first recorded event. The silent generator
of module i is the same Q_i before and after opening. Once open, total
recorded-event killing is D_i=diag(d_i)>=0 locally, and the global killing
is additive. Write A_i=Q_i-D_i.

For the selected recorded mark, the complete event/reset operator is supplied
as a finite positive sum

    J=sum_{b=1}^B beta_b tensor_i J_(b,i),   beta_b>=0.

Its row sums and the total recorded-event killing must be consistent with
the specified reaction source. Resets may be finitely branched, but an
arbitrary cross-module operator is not assumed to have such a compact
factorization. All needed physical output variables and public phase
information must be retained.

Fix an observed event lag t>0. Define local positive kernels

    H_i(u)=exp(Q_i(t-u)) exp(A_i u),      0<=u<=t.

The exact first-recorded-event kernel for the selected mark is

    K_t=integral_0^t gamma exp(-gamma(t-u))
                     (tensor_i H_i(u)) J du.             (1)

Its entry K_t(x,y) is the joint density, given initial configuration x, of
the first recorded event having the specified mark at lag t and leaving
post-reset state y. No particular initial law appears in (1).

## 2. Keep the event-density operator unnormalized

K_t is generally not a stochastic transition matrix. Its row sum

    f_x(t)=sum_y K_t(x,y)

is the selected event-time density from initial state x. It can vary strongly
with x. For an uncertain normalized entrance nu, the output is

    event density:      nu K_t 1,
    conditional state:  nu K_t / (nu K_t 1).              (2)

Normalizing each row K_t(x,.) first and then mixing those row laws with
unchanged weights nu(x) is incorrect. The correct posterior also reweights
the initial states by f_x(t). A reusable event kernel must retain its
input-dependent mass.

Positive terms, local matrix factors and their scalar weights likewise
cannot be individually normalized while discarding their normalization
factors. A known common scalar can be separated for numerical stability,
but its effect on event density must be retained. The operator's units are
those of a time density; its relative certificate is dimensionless.

## 3. Local entrywise identities and source-only support

For every pair of local input/output states,

    H_i'(u)=-exp(Q_i(t-u)) D_i exp(A_i u),
    -d_(i,max) H_i(u) <= H_i'(u) <= -d_(i,min) H_i(u),

and

    exp(-d_(i,max)u) exp(Q_i t)
      <= H_i(u) <= exp(-d_(i,min)u) exp(Q_i t).           (3)

These are entrywise matrix inequalities. Their proof is the derivative and
positive-semigroup argument of the companion file applied to every basis
initial row. No positivity or stationarity of a future input law is used.

For t>0, the positive entries of exp(Q_i t) are exactly the reachable local
state pairs, including diagonal pairs. Their support is obtained from the
positive-rate graph. For each reachable pair x,y, a positive path of length
at most |E_i|-1 supplies a strictly positive uniformization-series lower
bound. Thus

    q_(i,min)=min_{(x,y) reachable} exp(Q_i t)(x,y)>0

has a local positive lower certificate. Unreachable entries stay exactly
zero in every H_i(u). The minimum ranges over local transition pairs,
not over exponentially many global configurations or a chosen initial law.

After multiplication by a fixed positive reset branch, the output support
is the relational composition of reachability and reset support, again
independent of u. Different branches can have different supports; positive
summation takes their union.

## 4. Source-only relative quadrature

Put

    d_-=sum_i d_(i,min),  d_+=sum_i d_(i,max),
    L=max(|gamma-d_+|,|gamma-d_-|).

Any certified larger constant is also valid. In particular the numerical
executor may use the simpler gamma+d_+.

The integrand F(u) in (1) satisfies, entrywise on supported pairs,

    (gamma-d_+) F(u) <= F'(u) <= (gamma-d_-) F(u).         (4)

Positive reset branches and summation preserve these bounds. Therefore the
midpoint and exponentially weighted midpoint obtaining algorithms in
`nonstationary_opening_entrance_proof.md` apply to the kernel itself. The
integrated midpoint-envelope construction with N uniform cells has spread
at most exp(Lt/(2N)); the exponentially weighted construction has spread at
most exp((d_+-d_-)t/(2N)). These bounds hold for every matrix entry at once.

For completeness, the exponentially weighted construction is explicit.
Set c=gamma-(d_++d_-)/2, rho=(d_+-d_-)/2 and H(u)=exp(-cu)F(u).
Equation (4) gives |H'(u)|<=rho H(u) entrywise. For cell [s_j,v_j] with
midpoint u_j, use the positive scalar weight

    omega_j=integral_(s_j)^(v_j) exp(cu)du
           =(exp(c v_j)-exp(c s_j))/c       if c!=0,
           =v_j-s_j                        if c=0,

and construct

    G_weighted=sum_j omega_j exp(-c u_j) F(u_j).

For maximum cell width h, the pointwise log envelope proves

    exp(-rho h/2) G_weighted <= K_t
                               <= exp(rho h/2) G_weighted.

Thus for a target 0<epsilon<1, an exact uniform midpoint rule needs at most
the node count obtained by choosing

    N=max(1,ceil((d_+-d_-)t/(8 atanh(epsilon)))).

Its normalized output-TV guarantee is epsilon for EVERY input law with
nonzero output mass. The number of positive product-operator terms is at
most NB, counting reset branches. Node and scalar-weight evaluation errors
are separate relative spread factors. This explicit obtaining guarantee
does not contain silent-rate magnitudes or gamma; their local evaluation
and arithmetic costs have not been declared free.

For a sharper practical Gauss compiler, define local rational matrices

    C_(i,0)=I,
    C_(i,m+1)=-Q_i C_(i,m)+C_(i,m) A_i.

Then

    H_i^(m)(u)=exp(Q_i(t-u)) C_(i,m) exp(A_i u).

On every reachable pair one may use

    b_(i,0)=1,
    b_(i,1)=d_(i,max),
    b_(i,m)=||C_(i,m)||_infinity
             exp(d_(i,max)t)/q_(i,min),       m>=2.       (5)

Each row of the first semigroup is a probability row, the second semigroup
is substochastic, and (3) supplies the denominator. The bound is uniform
over all input rows. Certified upper/lower local enclosures make (5)
obtainable. It can depend substantially on silent rates; silent-rate
independence of scalar mesh size belongs to the midpoint alternatives,
not necessarily to the high-order bound.

The generalized product rule obtains a source-only B_8 with
|F^(8)(u)|<=B_8 F(u). Four-point Gauss quadrature of maximum cell width h
then has exact positive sum G satisfying

    |K_t-G|<=delta K_t,
    delta=(1/1778112000) h^8 B_8 exp(Lh),                 (6)

entrywise. If the implemented positive lower-node operator L_t satisfies

    L_t<=G<=C_num L_t,

and delta<1, the retained kernel certificate is

    a L_t<=K_t<=b L_t,
    a=1/(1+delta), b=C_num/(1-delta).                     (7)

The lower-node operator has the form

    L_t=sum_{ell=1}^Nop c_ell tensor_i T_(ell,i),
    c_ell>=0, T_(ell,i)>=0.                              (8)

For four-point Gauss with N cells and B reset branches, Nop<=4NB. Storing
the local kernels costs O(Nop sum_i |E_i||E'_i|) scalar entries, plus source
and certificate data. Finite support proofs and interval arithmetic must
handle structural zeros without inventing positive mass there.

All of (3)-(8) is obtained from local source generators, hazards, resets,
the selected mark and lag t. New source parameters, a new lag, or another
mark can require new acquisition. Reuse across input laws does not certify
one numerical table for every parameter or every continuous time.

## 5. The all-input theorem

### Theorem

Given (7), for every finite nonnegative initial joint law mu,

    a mu L_t <= mu K_t <= b mu L_t.                      (9)

If the output mass is positive and finite, the normalized output laws
have total-variation distance at most

    (sqrt(b/a)-1)/(sqrt(b/a)+1).                          (10)

For normalized exact mu, the event-time density belongs to

    [a mu L_t1, b mu L_t1].

The certificate is the same for every initial correlation pattern and every
supported initial state. It survives common exact later propagation,
observation, conditioning and reset operators.

**Proof.** Multiply (7) by a nonnegative row mu and sum input states.
Positivity preserves order. Apply the sharp projective-to-TV conversion in
`conditioning_stable_entrance.md`. Later positive operators preserve the
same order. QED.

This is a computational statement about supplied inputs. It does not infer
an unknown biological initial distribution. A compact kernel does not make
an arbitrary exponentially large input law cheap to read or contract;
execution cost depends on the input's available representation.

### Certified inputs compose with the kernel

If true unnormalized input M_0 and retained input L_0 obey

    a_0 L_0<=M_0<=b_0 L_0,

then

    a_0 a L_0 L_t<=M_0 K_t<=b_0 b L_0 L_t.

The output spread is at most (b_0/a_0)(b/a). Input normalization constants
cancel in the final conditional state. Event likelihoods from normalized
inputs require the mass calibration described in the companion proof.

The initial entrance error is inherited once. EVERY application of an
approximate kernel incurs that kernel's certified spread, even when the
same stored kernel is reused. Over m applications the general bound contains
the product of the m kernel spreads, or the sum of their log-spreads.
Source acquisition can be reused; approximation error is not waived by reuse.

## 6. Applying the kernel to a positive tensor entrance

For a component with nonnegative tensor-train cores U_i(x_i), one term of
(8) replaces each local core by

    U'_(ell,i)(y_i)=sum_{x_i} U_i(x_i) T_(ell,i)(x_i,y_i).

Only the physical state index changes. The bond dimensions remain the same.
The sum of Nop operator terms produces a positive mixture of at most Nop
such trains per input component. A positive product mixture is the bond-one
case. The transformed component's normalization is obtained by contracting
its cores and must be included in the new mixture weight. It depends on
both the input component and the operator term.

An implementation may retain an exact lazy sum of local maps rather than
materialize every output core. This avoids premature expansion; it does not
bound the cost of subsequent contraction. Repeated phases can multiply
mixture branches or bonds. Any compression needs an additional certificate.

## 7. Retaining physical historical labels jointly

For physical labels h, such as the unobserved per-site allocation of an
earlier total-count record, extend the kernel by

    K_tilde((h,x),(h',y))=1_{h'=h} K_t(x,y).

Its entrywise certificate is unchanged. For a count-accumulator train the
local physical index is (k_i,x_i). Applying T_(ell,i) to x_i while leaving
k_i fixed preserves the count increments and old carry boundaries. The
output certificate applies jointly to those historical physical counts
and the new hidden state. Artificial quadrature or mixture indices remain
representation labels, not identified physical history.

## 8. A permitted repeated-phase protocol

An input from an unresolved-count window may have its controller known
open. Reusing the one-opening source requires an explicit modeled reset of
ONLY that controller to closed. Leaf states and retained old count
allocations remain unchanged. The next phase then has one autonomous
irreversible opening, and one conditions on its first recorded mark at a
specified lag.

The known controller-only reset is a positive operation and does not imply
independence of the correlated leaves. Applying the kernel afterward is
exactly the operation of Sections 5-7. A hidden recurrent controller that
opens and closes without observation is a different source and is not
solved by this protocol.

The new opening time is marginalized. The output state, public phase and
known timestamps must suffice for later dynamics. Retrospective questions
about the unretained opening time are not supplied by a state-only output.
Old physical labels can be retained through the identity extension above.

## 9. Relation to prior machinery and implementation claims

Several close primary antecedents delimit the claim.

* Celikkaya and Shelton's [TTOP method, 2014](https://proceedings.mlr.press/v32/celikkaya14.pdf)
  already starts from the full matrix propagator in Equation 1. Section 2.2
  evaluates its structured products through local Kronecker factors, and
  Section 2.4 explicitly discusses a choice with nonnegative correction
  matrix B. Full-operator treatment, local product evaluation and positive
  decompositions are therefore established precedents; reuse across input
  laws is not by itself a historical novelty claim.
* Le Gland and Oudjane's [Hilbert-metric filtering analysis, 2004](https://scispace.com/pdf/stability-and-uniform-approximation-of-nonlinear-filters-5cqc16nut7.pdf)
  gives initial projective-error propagation in Theorem 4.1 (p.155),
  entrywise multiplicative kernel-ratio conditions in Remark 4.3 (p.157),
  and propagation of local projective errors in Theorem 4.4 (pp.157-158).
  Basic nonexpansion does not require mixing; mixing strengthens the
  long-record conclusions. The positive-order certificate in Sections 5-7
  uses this established structure.
* Beylkin and Monzon's [positive exponential-sum approximation, 2010](https://amath.colorado.edu/faculty/beylkin/papers/BEY-MON-2010.pdf)
  obtains relative approximations from integral quadratures and uses them
  in separated operator representations. Positive quadrature and relative
  separated approximation are also established ideas.

The candidate obtaining distinction here is narrower: same-Q local killing
provides an entrywise log-variation bound determined by the local hazard
ranges, with an explicit all-input node count and an obtainable local
support certificate. This produces the selected reaction-event density
operator directly from a checked compact source. Its relative certificate
is then composed with established positive filtering and tensor operations,
including a correlated entrance retaining old count allocations. The
mathematical comparisons above do not establish historical priority for
this specialized construction, and no comparative runtime superiority has
been demonstrated.

The acquired object retains input-dependent event-likelihood reweighting,
which a collection of separately normalized fixed-initial-state posteriors
would discard. Ordinary programmes can adopt the same construction and
reuse the same operator. No special architecture is necessary. Positive
tensor-map application and counter-automaton contraction are standard
algebra; additional tensor and cardinality references are given in
`unresolved_count_interface_proof.md`.

## 10. Executed binary specialization and retained exact laws

The following are new calculations represented by available code and data,
not claims recovered from an unavailable earlier runtime. The general
finite-local proof above is broader than the implemented binary adapter.
The executor checks positive binary switching rates, the unchanged silent
generator across opening, the one-opening controller contract, and the
specified local reaction/reset. Neither the general weighted-midpoint
alternative nor a generic arbitrary-tensor-network executor is claimed to
have been implemented.

### One acquisition, several different supplied inputs

`reaction_event_kernel.py` exposes
`acquire_from_source(source, event_mark, elapsed, tolerance)`.
The demonstration wrapper `acquire_kernel` supplies one compact family.
The completed 24-component, 73-rule calculation selected mark 0 and elapsed
time 1/10. It acquired 32 positive product operators from eight four-node
Gauss cells. The retained rational operator is in
`reaction_event_kernel_24sites.json`, with exact multipliers a,b and exact
spread b/a. Its certified output-TV upper bound for every supplied initial
joint law is less than 2.390081e-9.

The source derivative minimum is taken over all four local silent
transition entries, rather than over a chosen initial row. Local kernels
are evaluated in the order exp(Q(t-u)) exp(Au), followed by the marked reset.
Mark 0 gives an exactly zero active-state output column at its firing site.
The stored positive sum is never row-normalized during acquisition.

The same stored operator was applied without recomputing its quadrature to
the all-off and all-on product entrances. The exact rational event-density
normalizers and complete lazy conditional laws are retained in
`event_kernel_product_applications.json`. Approximate central values below
describe those retained laws; the intervals are conservative displayed
enclosures for the source-model quantities.

| Supplied input | Selected event-time density | Probability that all 23 nonfiring sites are active after the event |
|---|---:|---:|
| All off | [0.0050799554867, 0.0050799555353] | [4.75140354e-28, 4.75140365e-28] |
| All on | [0.0251566466963, 0.0251566469369] | [0.3657151703, 0.3657151748] |

These densities have units of inverse time and are not constrained to be
probabilities. The very small all-off guard probability is enclosed by the
relative certificate; it was not estimated from rare successful samples.
The table is a synthetic source-model calculation, not empirical biology.

### Reuse on a correlated count entrance and smoothing of old attribution

The third input is the already retained total-count posterior in
`unresolved_count_posterior_24sites.json`: 256 nonnegative counter-tensor
components, each with count bond 9 for the old total count 8. Its physical
indices retain both old local count allocation and current binary state.
The protocol explicitly resets only the known-open controller to closed,
retains all leaves and old counts, and observes the next first mark 0 at
lag 1/10.

The exact lazy result is `event_kernel_count_tt_application.json`. It
references the actual stored input tensor law and operator, specifies the
controller-only reset, and stores the exact rational output density
normalizer. There are 8192 implicit pairs of input component and operator
term. Each pair keeps count bond 9. The calculation contracts integer
coefficient polynomials; it neither materializes all pairwise tensor trains
nor converts the count law into a product-mixture expansion over allocations.

For clarity, the normalization actually used is the following. If input
component r has normalized law product_i a_(r,i,k_i,x_i)/C_r on sum_i k_i=8
and exact mixture weight alpha_r, its scalar is alpha_r/C_r. For kernel
term ell, all local matrix denominators are included in its scalar. The
local transformed factor is

    a'_(r,ell,i,k_i,y_i)
      =sum_(x_i) a_(r,i,k_i,x_i) M_(ell,i,x_i,y_i).

Exact coefficient extraction and summation over r,ell give the full density
normalizer. There is no missing input or kernel scalar, and old k_i are
unchanged. Normalization occurs once after this full weighted contraction.

The certified selected event-density interval is

    [0.0111931155328, 0.0111931156814].

The joint posterior certificate covers old physical count allocation and
new hidden state, with TV upper bound less than 2.853745e-9. It multiplies
the inherited count-entrance spread by the newly applied kernel spread;
the exact integer/rational contractions incur no further approximation.
The old attribution query changes as follows:

| Query | Certified source-model probability interval |
|---|---:|
| Old site 0 contributed at least one count, before the new observation | [0.0700916614584, 0.0700916617003] |
| The same historical event, after the new mark and lag are observed | [0.0426022383477, 0.0426022392789] |
| All 23 nonfiring sites active after the new event | [1.4152204644e-11, 1.4152204968e-11] |

The second row is smoothing of an earlier unresolved attribution by later
reaction evidence. It demonstrates why the historical count correlations
and the input-dependent event density must both be retained. The new
unobserved controller-opening time is still marginalized; this object does
not supply its retrospective distribution.

### Available code, certificate checks and finite reference comparison

`reaction_event_kernel_results.json` records the completed executions and
full outward-rounded enclosures. `load_kernel` reads the exact stored
operator, checks dimensions, positivity and marked reset support, and
checks the exact multiplier/spread algebra and conservative exported TV
bound. Its checks do not replace the mathematical quadrature proof or
independently reacquire the kernel. The lazy result files, their referenced
scientific objects, and the applying code together specify complete
conditional laws; the results JSON alone would not do so.

A separate three-leaf expanded calculation used a 16-state killed generator
and positive rational uniformization. It checked all eight input basis
rows, all 32 positive input/output entries and 32 structural zeros against
the acquired operator certificate. All reference entry enclosures lay
inside the operator sandwich. Forty-two uniformization terms left a tail
bound less than 2.879e-61. This finite reference check is evidence for the
implemented specialization; the all-input claim for 24 leaves rests on the
source-only proof and its implemented local bounds, not on enumeration of
the 24-leaf state space.

A targeted code and saved-data review checked propagator order, source-only
derivative denominators, exact retained-law normalization, identity action
on historical counts and multiplication of input/operator spreads. Exact
rational checks also confirmed that serialized TV bounds are conservative.
The review did not rerun the source acquisition, count filtering or full
applications, and no additional broad test suite is being represented.
