# Retain certified experimental relations without retaining numerical sources

The exact path compiler has closed a computational join for the KNOWN old
program tuple. Its ACTUAL old-source semantics are still uncertified. The
next acquisition question is whether that semantics must be bought by
learning numerical old source programs at all. It need not: one can guard
an acquired conditional experiment while each source is still live, retain
only an equality/invariance certificate, and reuse it on arbitrary current
targets after every old source expires. This first construction is a
prospective operation, not an invented historical guard on the six caches.

## 1. Programs, native law and observation timing

Fix a finite native domain X with an explicitly paid sampler for nu. An
actually synthesized closed program h:X->Y and a closed native kernel K0
are frozen before the old guard episodes. Its known-code certificate proves

    X~nu; X'~K0(X,.)  has nu marginal on BOTH endpoints,
    K0(x,.)=nu(.|h=h(x)).                                 (1)

All h extraction, candidate search, native input construction, exact
conditional preparation, randomness, memory and verification costs are
paid. Neither useful h nor K0 is a supplied latent oracle. Earlier acquired
slice/group/path constructions supply examples of how(1) can be compiled
from closed code under their exact contracts, with explicit failures/caps.
Exhaustive native enumeration is another finite but potentially prohibitive
implementation. This theorem does not turn it into a polynomial procedure.

Old source i is a fixed scalar function F_i during its own actual query
episode. The guard needs only the genuine equality answer

    1{F_i(x)!=F_i(x')}.                                   (2)

Exact numerical values supply(2), but are unnecessary. A TRUE three-way
comparison also supplies it; the binary comparison oracle that may break
ties arbitrarily does NOT automatically supply it. Equality precision or a
conditional comparison-error budget is a real observation contract. No
numeric model, degree, alphabet size, unknown calibration or extension of
F_i is assumed. In particular F_i may be an arbitrary increasing transform
of a latent score, whose numerical values no comparison history determines.

The old sources need not coexist. K0 must remain the SAME frozen procedure
while their guards are bought, and every guard is completed while that
source is live. If h/K0 is synthesized only after a source expires, this
certificate cannot be acquired retroactively from unrelated old grids.
This is exactly the gap still present in the actual retained-six example.

## 2. A sequential aggregate guard needs no numerical source model

For each of r old sources buy m fresh ideal pairs from(1), and record
Z_i,t from(2). Conditional on the complete history before the live source
episode, let

    rho_i=Pr_(nu K0)[F_i(X)!=F_i(X')].                     (3)

The source may have been selected from earlier history, but is fixed for
this episode; K0/native randomness is genuinely fresh. Set C=sum_i,t Z_i,t
and R=sum_i rho_i. All failed proposed kernels/guards have their own finite
attempt and confidence allocation. Accept the current frozen kernel when

    C<=m eta/2,    m>=12 ln(1/delta)/eta.                  (4)

There is a JOINT soundness guarantee

    Pr[accept AND R>eta]<=delta.                          (5)

There is also a joint power guarantee

    Pr[reject AND R<=eta/4]<=delta.                       (6)

Thus model error need not be zero for coverage; no statement conditions on
an arbitrarily rare return event. The actual complete-procedure return
probability additionally pays native preparation/bit caps.

Proof with adaptive source selection: for a Bernoulli variable Z of
conditional mean p, E[exp(-Z+(1-e^-1)p)|past]<=1. Multiplying through
the rm actual observations yields a mean-at-most-one supermartingale.
The final predictable mean sum is mR. On(5)'s event the exponent is at
least m eta[(1-e^-1)-1/2]>m eta/8. Markov gives exp(-m eta/8).
For(6), use E[exp((ln2)Z-p)|past]<=1. Its exponent on that event is at
least m eta[(ln2)/2-1/4]>m eta/12. These bounds prove(5)--(6) with(4).
The cost is rm actual old equality comparisons (or2rm numerical values),
not an uncharged simultaneous-cohort query and not r separately tightened
eta/r tests. If actual pair preparations have finite caps, couple to these
ideal trials and abort on any failure; charge the abort probability and
ALL attempted known-code/bit work separately.

## 3. What survives after expiry: an unknown map, not a missing obligation

Let F=(F_1,...,F_r) denote the realized old tuple. Under(1), its full
within-h collision disagreement is

    d_F=sum_y p_y[1-sum_a Pr(F=a|h=y)^2] <=sum_i rho_i=R.  (7)

Every fibre has a finite conditional mode. Choose a mathematical mode map
phi(y) for the ACTUAL tuple and put E={F!=phi(h)}. The elementary
mode/collision inequality gives

    nu(E)=inf_phi nu{F!=phi(h)}<=d_F<=eta                  (8)

on the accepted good event. The algorithm does not need to observe, fit,
evaluate or store phi. It is a witness for the retained SEMANTIC relation.
This omission is legitimate because no step later calls phi as an oracle.

For EVERY deterministic composition psi of the actual old tuple, the SAME
E gives

    psi(F)=psi(phi(h)) outside E.                         (9)

This is a simultaneous family guarantee, not a claim that future tasks
will be chosen from that family. In particular, the earlier guarded
dictionary/prediction operations can be applied to a related future
f=psi(F) using h alone: they require only existence of a close h-composition,
not the numerical old programs. Their actual label support K, captured
mass/tail, dictionary construction, current answers, guards, preparation
and evaluation costs remain unchanged and paid. A small representation
language or good future coverage is not inferred from(8). Taking h=x
always makes(8) trivial but can make later table acquisition as costly as
the entire native domain.

Numerical old sources really can remain unidentifiable. Arbitrary strictly
increasing recalibrations preserve ALL comparison/equality answers while
changing old numerical values. Thus this is not a claim that an unbuilt
scalar decoder secretly resides in the retained comparison cache. The
acquired object is an executable native experiment plus a guarded relation
that later procedures can use without any old numerical evaluation.

## 4. Later experiments can be compiled after expiry

Consider ANY later chosen closed kernel K satisfying known-code checks

    nu K=nu,          h(X')=h(X) with probability1.        (10)

It can depend on later target history and need not sample full h-fibres,
mix rapidly, or have a density bounded relative to K0. Equations(8),(10)
give uniformly for the same realized old tuple

    Pr_(nu K)[F(X)!=F(X')]<=Pr[X in E]+Pr[X' in E]<=2eta.  (11)

The semantic certificate therefore extends to ALL such later compiled
experiments, even after source access expires. It is not necessary to
replay K0 or ask an old source to approve each new intervention. This is
why full conditional validation at acquisition time is stronger than
validating one arbitrary feature-preserving move: it certifies the hidden
pointwise relation(8), without learning its numerical map.

For a fixed arbitrary current finite-alphabet f, let
b_F=inf_psi nu{f!=psi(F)}. A known stationary relation kernel K gives

    d_K(f)=Pr[f(X)!=f(X')]<=2eta+2b_F,                    (12)

because a best old composition differs from f at at most b_F at either
native-marginal endpoint. Hence q independently prepared current pairs,
with q>=ln(2/delta_now)/(2u^2), provide the source-independent lower bound

    b_F>=max(0,(d_hat_K-u)/2-eta).                        (13)

It uses2q current values, no old values, and no assumption that the new
target is polynomial or related. A positive bound means the FULL actual
old algebra is insufficient at that distance. A zero bound is inconclusive:
identity/local/frozen kernels can have zero power. One must not assert
full-fibre coverage or a spectral gap for(10) merely from stationarity.
If a stronger quantitative coverage certificate is later acquired from
known code, it can justify an upper distance bound; none is granted here.

Examples of cheap known-code kernels include native block heat baths:
choose a block BEFORE the fresh native X, enumerate its assignments with
all h values fixed, then sample its exact finite conditional. Their matrices
are symmetric under uniform native input, so they preserve nu, at paid
p^|block| code work. Checking h invariance literally avoids a useful-block
label oracle. Fixed mixtures and certified translations are other permitted
procedures. No global-conditional sampler is inherited from their local
tractability; the preceding RP=NP construction still applies.

## 5. Source-acquisition coverage and strongest comparator

An actual ordinal primitive compiler can propose h before its initial
source episode ends, under its explicitly bounded inner language. That
cost and finite confidence remain paid. Guard(4) then supplies soundness
even if that true-inner-polynomial/shear promise is wrong, because it tests
the actual native equality relation rather than a guessed source model.
Coverage still requires a successful candidate and affordable native
preparation. For a rational action one must also supply/construct a finite
native law that it actually preserves; an action on Q^n does not preserve
an arbitrary old finite grid. One can define a NEW finite chart law by
sampling(y,z) and mapping to x=Uz+[y-h(Uz)]v when D_vh=1, but all old
guards/future risk then concern THAT paid, explicitly changed law. No
claim about the old evaluation law follows without a domination contract.

Ordinary sufficient-statistic, functional-dependency, invariance-testing
and code-aware retaining methods get the SAME native kernels, equality
access and full history, and can adopt this operation. The supermartingale
and conditional-mode ingredients are already conventional. The scoped
interface change is learning/guarding an executable relation instead of
requiring an acquired numerical model of every old source. Exact equality,
guard timing, native preparation, language construction, total arithmetic
and actual future coverage remain load-bearing. No new observations,
fixture or historical old guard is executed for this first construction.
