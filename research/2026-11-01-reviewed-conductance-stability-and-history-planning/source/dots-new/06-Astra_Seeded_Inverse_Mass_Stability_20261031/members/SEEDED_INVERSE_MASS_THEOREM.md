# Acquired inverse mass across an extinguishable common seed

**Status:** ordinary mathematical proof and exact rational implementation; frozen-source
independent review is recorded separately. No claim about arbitrary weakly reversible
networks, priority, or operational chemistry. Existing accepted packages are unchanged.

## 1. Result and the genuinely different obstruction

For every choice of positive rates, consider the count-process network

```
0 <-> A                                  lambda, mu
2A+B <-> A+B+C                            alpha1, beta1
2A+C <-> A+2B                             alpha2, beta2
A+B+C <-> A+2C                            alpha3, beta3.
```

Mass-action propensities use falling factorials, with no factorial divisors absorbed
implicitly. Only the first pair changes total count `N=A+B+C`. Every cubic complex
contains A. Thus its homogeneous leading vector field vanishes on the entire A-zero
face: the preceding leading-support criterion cannot apply, at any polynomial degree.
This is an obstruction to that criterion, not to recurrence.

**Theorem A.** Every closed communicating class of this CTMC is positive recurrent.
Every stationary distribution has every finite exponential total-count moment. For
positive rational rate input and each rational `t>1`, the exact rational halving algorithm below acquires a normlike
function `W` and finite constants `zeta,C_F>0` with

    L W <= -zeta W + C_F.

The algorithm requires neither a stationary fiber law nor a successful seed lifetime
nor a good weight as input. A raw structural receiver obtains the qualitative theorem
without materializing numerical Foster constants. Explicit numerical acquisition is
separate and can be expensive.

**Theorem B (representation obstruction).** On one closed communicating class with
positive satellite count, no positive normlike function of only `(A,N)` satisfies any
geometric Foster inequality `L F <= -epsilon F+C`. This excludes arbitrary such
functions, not just exponential products. The independent proof and exact enabled
connecting paths are in `SEEDED_MEDIATED_AGGREGATE_NO_GO.md` in the copied audit
mechanism directory. A proof is also summarized in Section 9 below.

The successful correction is `W=t^N(1+c/(A+eta B))` on A>=1, patched separately on
A=0. It retains the mediator B discarded by `(A,N)`. At pure C with one A, internal
events first create B without changing `(A,N)`; only subsequently is more A created.
This is why neither a stationary projected law nor an instantaneous service assumption
is used. At A=1 the actual death of the last A, at rate mu, is fully included.

## 2. Generic sufficient profile class and strict input scope

The more general rational finder accepts n>=2 species, one coordinate A, and:

* exactly the nonconservative channels `0->A` and `A->0`, with rates lambda,mu>0;
* conservative nonnull internal channels whose source and target both contain A,
  and whose common total molecularity is 2 or 3;
* a weakly reversible full raw complex graph.

Duplicates are aggregated after checking positive exact rational rates, null channels
discarded after validation, and A acquired from the raw nonconservative reactions.
Every internal channel, after stripping one A from both complexes, is a unary or
binary conservative channel `u->v` of a network Q. For A>=1, put

    r=A-1, y=(r,B_1,...,B_m), M=r+sum B_j.

The falling-factorial identity `(A)_(u_A+1)=A(A-1)_(u_A)` proves the **exact**, not
asymptotic, internal-generator identity `L_int=A Q` on this shifted lattice. At A=0
all internal rates vanish. Internals preserve the seeded region A>=1. Immigration and
death are not included in that time change and must be treated separately.

A proposed profile consists of rational weights `0<=w_j<=1`; the finder, not the
caller, searches them. Define

    R=A+sum w_j B_j,     R>=A>=1.

For each stripped channel with stoichiometric jump nu define

    d=nu_A+sum w_j nu_j,
    ell=1+max_channels |d|,
    rho(d)=d/ell if d>=0, and ell*d if d<0,
    Psi(y)=sum_channels kappa rho(d) (y)_u.

Aggregate Psi by its stripped source u, with coefficients gamma_u. The profile must
have `u_j:=gamma_(2B_j)>0` for every satellite, and all mixed satellite coefficients
`gamma_(B_j+B_k)>=0`. These are exact finite rational inequalities. They are sufficient,
not necessary for stability. Define

    K1=max(0, max_unary_sources -gamma_u),
    K2=max(0, max_binary_sources_containing_r -gamma_u),
    K0=K1+K2,
    K=K0+sum_j (u_j+K0)^2/(2u_j).

Here K>0 since m=n-1>=1 and all u_j>0. Missing sources have coefficient zero.

## 3. The exact inverse-mass inequality

For `0<c<=1`, put `h=1+c/R` on A>=1. Every enabled internal target is still seeded,
so `R'=R+d>=1`. Since both R,R'>=1 and |d|<=ell-1,

    R/ell <= R' <= ell R.

The exact increment is `h'-h=-cd/(RR')`. If d>=0 this is at most
`-c(d/ell)/R^2`; if d<0 it is at most `-c(ell d)/R^2`. Consequently

    L_int h <= -c A Psi(y)/R^2.                         (1)

All signs matter in (1): replacing all denominators by R^2 without separating the
signs would not be valid. After discarding nonnegative terms,

    Psi >= sum u_j (B_j)_2 - K2 rM - K1 M
         >= sum u_j B_j^2 - K0 A^2 - A sum (u_j+K0)B_j
         >= (1/2)sum u_j B_j^2 - K A^2.               (2)

For the second line use r<=A, A>=1, M<=A+sum B_j. For the last line complete each
square using `(u_j+K0) A B_j <= (u_j/2)B_j^2+(u_j+K0)^2 A^2/(2u_j)`.
Write `Q=sum u_j B_j^2`. Since 1<=h<=1+c and R>=A, (1)-(2) give

    L_int h/h <= c K A - c A Q/[2(1+c)R^2].            (3)

This is a joint composition/probability correction, not a finite-state protected
token. It works on an unbounded fiber and never integrates against an assumed law.

## 4. Paying the last-copy death and immigration explicitly

Fix rational t>1 and define

    D=mu(1-1/t),
    c=min(1,D/(4K)),
    C=lambda(t-1)+3mu+D,
    zeta=min(lambda/4,D/4,1),
    h0=2t(1+c).

Set `h=h0` on the entire A=0 face and `W=t^N h` everywhere.

* At A=0, only immigration changes W. Its target has h<=1+c, so
  `LW/W=lambda(t h(1,B)/h0-1)<=-lambda/2`. This treats arbitrary satellite counts.
* At A>=1 immigration increases R by one, decreases h, and contributes at most
  `lambda(t-1)` to LW/W.
* At A>=2 death changes R to R-1. Its contribution is at most
  `-D A+mu c A/[t R(R-1)h]<=-D A+mu`, using R>=A>=2 and c<=1.
* At A=1 the actual jump is to the patched A=0 face. Its contribution is exactly
  `mu(2(1+c)/h(1,B)-1)<=mu(1+2c)<=3mu`.

Thus the uniform death bound on A>=1 is `-DA+3mu+D`. Combining with (3) proves

    LW/W <= C-(3D/4)A-c A Q/[2(1+c)R^2], A>=1.        (4)

No service-free interval, infinite-lived seed, or suppressed death was inserted.
In particular, the unfavorable `lambda(t-1)` remains in C; it grows with t.

## 5. Acquired finite-head compatibility and the finite exception box

Define

    S=sum_j w_j^2/u_j.

If S>0 require the additional exact rational inequality

    c/[4(1+c)S] >= C+zeta.                            (5)

If S=0 there is no head-compatibility requirement. All weights then vanish and R=A.
Let

    A_cut=max(2,ceil[4(C+zeta)/(3D)]).

For A>=A_cut the linear term in (4) suffices. Restrict henceforth to 1<=A<A_cut.

If S>0, put `T_tail=9 A_cut^2/S`. Cauchy-Schwarz gives
`sum w_j B_j<=sqrt(SQ)`. If Q>=T_tail, then sqrt(SQ)>=3A_cut>=3A and

    R <= (4/3)sqrt(SQ),       Q/R^2 >=9/(16S)>=1/(2S).

By (5) the last term of (4) has magnitude at least A(C+zeta)>=C+zeta.

If S=0, put `T_tail=2(1+c)(C+zeta) A_cut^2/c`. When Q>=T_tail, the last term of
(4) is `cQ/[2(1+c)A]>=C+zeta`, since A<=A_cut^2. This deliberately generous bound
avoids a separate sharp optimization and is finite.

For either case choose exact integers

    B_cut,j=max(1,ceil_sqrt(T_tail/u_j)).

If any B_j>=B_cut,j then Q>=T_tail. Thus `LW/W<=-zeta` outside the finite box

    E={1<=A<A_cut; 0<=B_j<B_cut,j for all j}.

The entire infinite face A=0 is already handled, not enumerated. Set

    |E|=(A_cut-1) product B_cut,j,
    N_max=A_cut-1+sum(B_cut,j-1),
    C_F=(C+zeta)h0 t^N_max.                           (6)

On E, (4) gives LW/W<=C and W<=h0 t^N_max, so globally

    L W <= -zeta W + C_F.                            (7)

Both |E| and C_F may be enormous. The implementation computes |E| as an integer but
does not enumerate E. It stores C_F as an exact prefactor/base/exponent expression,
with conservative bit bounds, not an expanded rational. A low profile count is not a
claim that explicit tail bounds are small or efficient.

## 6. Stochastic consequences without circular stationary assumptions

Only constant-rate immigration can increase N, hence pathwise
`N(s)<=N(0)+Pois(lambda s)` under the ordinary immigration-clock construction.
On every finite time interval this is finite. Each fixed count sublevel contains
finitely many states and bounded finite rates. Thus there is no explosion.

For every finite time T, the same Poisson domination gives integrability of the
supremum of W and of a polynomial in N times W on [0,T]. The generator has degree at
most three, so stopped Dynkin identities pass to the limit with these dominating
variables. Integrating (7), or applying the integrating-factor version, yields

    E_x W(X_t) <= e^(-zeta t)W(x)+(C_F/zeta)(1-e^(-zeta t)).

Since W>=t^N is normlike, empirical occupation measures are tight. The standard
countable nonexplosive CTMC invariant-measure argument yields a stationary law on
each closed irreducible class, hence positive recurrence. Fatou applied to its
construction gives its W moment at most C_F/zeta. Equivalently one may use the
ordinary continuous-time Foster theorem; the preceding domination also verifies its
integrability requirements rather than presupposing a stationary moment.

Weak reversibility makes every enabled jump belong to a directed return path on the
state lattice: traverse a complex-graph return path while retaining the unchanged
nonnegative surplus `x-source`. Thus communicating classes are closed. There may be
distinct A-only and positive-satellite classes; they are not silently identified.
The global constants apply to every class. Because each closed class must intersect
one fixed finite sublevel with W<=2C_F/zeta, only finitely many closed classes are
possible, and stationary mixtures retain the same moment bound.

**Moment scope:** one accepted generic profile at one requested t proves that t^N
moment, positive recurrence, and every smaller exponential moment. It does not by
itself prove every exponential moment. All-t acquisition is separately proved in
Section 7 for the mediated skeleton, and is automatic for a valid S=0 profile since
(5) is absent for every t>1. For every real theta>0 choose a rational t>exp(theta).

## 7. No supplied good pivot: all-rate finite halving for the mediated lift

From the raw reaction list enumerate the at most two satellite orderings and match
the exact six internal directed channels of Theorem A, including positive rates.
Choose

    eta0=min(1/4,beta1/(4alpha3)),  w_B=eta, w_C=0,
    eta=eta0/2^k,                 k=0,1,2,... .

Each jump of R=A+eta B has increment among `+/-1`, `+/-(1-2eta)`, `+/-eta`; hence
ell=2. The exact aggregate coefficients required by the generic construction are

    u_B=beta2(1-2eta)/2,
    u_C=beta3 eta/2,
    gamma_BC=beta1/2-2alpha3 eta>=0,
    K1=0,
    K2=max(2alpha1,2alpha2(1-2eta)).

Thus all source-sign conditions hold from the first trial. Put

    Kmax=2 max(alpha1,alpha2),
    umin=beta2/4, umax=beta2/2, v0=beta3/2,
    Kbar=eta0[Kmax+(umax+Kmax)^2/(2umin)]
          +Kmax^2/(2v0)+Kmax eta0+v0 eta0^2/2.

Because umin<=u_B<=umax and u_C=v0 eta, direct expansion of K proves

    eta K <= Kbar.

With `c0=min(1,D/(4Kbar))`, therefore `c>=c0 eta` (eta<=1). Since S=eta^2/u_B,

    c/[4(1+c)S] >= c0 umin/(8eta).

All trials with

    eta <= eta_required := c0 umin/[8(C+zeta)]          (8)

pass (5). Halving terminates, and the number of required trials is explicitly bounded
by the first k+1 for which eta0/2^k<=eta_required. The code obtains that integer by
exact rational repeated halving and charges this separate bound-computation work.
Alternatively one could directly choose a smaller rational eta from (8); the search
often obtains materially smaller tail boxes than the coarse termination bound.

This proof holds for all positive real rates; the executable exact API accepts only
integers and Fractions, rejects bool/float rates and malformed complexes, and handles
positive rational rates. It is not an interval-real oracle.

**Executed main case:** all eight rates one except alpha3=2, t=2. The generic bound
acquires eta=1/2048 after nine profile evaluations (eleven trials are the proved upper
bound), with

    c=1047552/68738298881,
    A_cut=13, B_cut=79872, C_cut=3612829,
    |E|=3462766534656, N_max=3692711.

The 3.46-trillion-state box was not enumerated. The Foster constant was not expanded.
Independent mechanism-level estimates use different safe constants and can give a
different eta/box; numerical equality between those bounds is not expected.

## 8. Receivers, acquisition costs, and UNKNOWN semantics

`generic_search` enumerates all common denominators q=1,2,... and all vectors
`(k_1/q,...,k_m/q)` with 0<=k_j<=q. Duplicated rational profiles are charged again.
Every rational profile is eventually tested. It is complete only for this rational
profile certificate family: an accepted rational profile will eventually be found.
Without one, it need not terminate. A finite profile cap yields UNKNOWN, not a
stability-negative answer or a certificate-nonexistence theorem.

For Q denoting a reached denominator (not the quadratic energy), the raw enumeration
performs at most `sum_(q=1)^Q (q+1)^m` trials; each uses O(number of reactions times n
plus n^2) rational source/weight work, exact rational comparisons, and, on acceptance,
integer square roots. The graph check explicitly traverses return reachability for
every edge; its elementary bound is O(E(V+E)). These are arithmetic-operation bounds,
not bit-complexity or memory guarantees. Fraction bit sizes, rational products,
big-integer square roots, and output integers cost real work.

`hard_search` recognizes the raw skeleton and executes halving; its actual trial
list, source-term evaluation count, sufficient trial bound, graph work, and largest
retained rational-record bit size are recorded. The retained-record peak is **not**
a bound on every transient multiplication operand. Profile caps do not cap input
validation, termination-bound acquisition, graph work, integer bit work, or memory.

`receive(raw,t,weights,certificate)` independently of the mutable working record
revalidates raw input and re-derives all mathematical certificate fields; it demands
exact equality, including finite-box and factored-constant fields. It is a semantic
receiving routine, **not** an independent audit of search-accounting history. The
independent review/receiver states exactly which additional transcript checks it ran.

`hard_structural(raw)` performs only raw recognition and skeleton matching, then
returns qualitative all-exponential recurrence from the proved all-rate termination
theorem. It does not compute t, eta, Kbar, scalar tail constants, or any profile. Its
matching failure means UNKNOWN. `receive_structural` rechecks exact equality against
fresh raw recognition. A capped quantitative halving run can therefore be UNKNOWN
while the separate qualitative result is CERTIFIED. This spends reusable theorem
proof capital, not a hidden per-instance polynomial or stationary-law oracle.

## 9. Exact three-layer obstruction for every normlike F(A,N)

Assume a positive normlike F on the positive-satellite closed class and
`LF<=-epsilon F+C`. Enlarge C>=0 and reduce epsilon if needed so
`0<epsilon<=lambda^2/[4(lambda+mu)]`. Define

    u_n=F(0,n), v_n=F(1,n), w_n=F(2,n),
    r0=1-epsilon/lambda,
    s=(lambda+mu-epsilon-mu/r0)/lambda.

Elementary algebra gives 0<s<r0<1. At pure-C states, all composition-only internal
events vanish when applied to F. At `(0,0,n-1)`, the drift inequality implies

    u_(n-1)>=(v_n-C/lambda)/r0.

At `(1,0,n-1)`, it implies

    w_(n+1)<=s v_n+B0,
    B0=(C/lambda)(1+mu/(lambda r0)).

At `(2,0,n-2)`, the only A-changing internal channel has rate `2alpha2(n-2)` and
goes to A=1 at the same N. Dropping the positive immigration and death destination
terms yields

    v_n<=[1+q/(n-2)]w_n+C/[2alpha2(n-2)],
    q=(lambda+2mu-epsilon)/(2alpha2)>0.

Combine the last two inequalities. Their multiplicative factor tends to s<1, so
eventually `v_n<=rho v_(n-1)+B` for some fixed rho<1 and B<infinity. This bounds
v_n, contradicting normlikeness along the pure-C ray. No fast-limit stationary law
or interchange of limits is used. The independent proof supplies finite enabled
reversible paths joining these rays within one closed class; A-only states need not
belong to it. This does not exclude sampled-time, excursion, history-dependent,
composition-sensitive, or other conventional Lyapunov proofs.

## 10. Strong ordinary comparators and remaining obstruction

The simpler seeded star `0<->A;2A+B_j<->A+2B_j`, with internal A-neutral satellite
conversions, already admits `h=1+c/A`: exact cancellations give

    L_int h=c sum alpha_j B_j-c sum beta_j(B_j)_2/(A+1)

on A>=2, with the positive term absent at A=1. The independent baseline proof pays
the same actual extinction/immigration costs and proves all exponential moments.
It can admit arbitrary-order A-neutral channels because they are exactly invisible.
The generic unary/binary-stripped parser is narrower; parser rejection of such a
channel is not failure of the ordinary baseline. The two-species star is also a
deficiency-zero product-form control, not the difficult result.

The hard three-species example with alpha3=2 and all other rates one is not complex
balanced: the core forces a=1; the leaf 2A+B forces c=1; the leaf A+2C forces
c=2b; and the separate pair 2A+C<->A+2B forces ac=b^2. These equations contradict.
Thus the standard complex-balanced Poisson product theorem does not settle this
example. This does not rule out every imaginable conditional/product representation.

Conventional Foster theory, mass conservation, exact generator algebra, finite-state
graph reachability and inverse Lyapunov corrections are ordinary tools. The claimed
earned consequence here is their explicit seeded, mediator-sensitive certificate
acquisition, the representation no-go, exact all-count receiver, and paid constants.
We make no priority claim. Existing fluid, tier, excursion, decomposition and queueing
methods are not denied information about the raw network; failure of our previous
certificate is not evidence that all those methods fail.

A sharp next obstruction remains. For the common-A lift of

    2B <-> B+C <-> 2C,     B+C <-> r+B,

the pure-B effective coefficient has the sign of w_C-w_B and the pure-C coefficient
has the opposite sign. No real linear weight profile makes both strictly positive.
This is a complete obstruction to this particular inverse-linear profile family,
not to stability. A nonsmooth or polynomial composition mass, or an acquired
excursion correction, may resolve it, but none is assumed in Theorem A or B. In
particular we have **not** proved that every seeded lift of a support-accessible
stripped network is stable, and have not solved general weak reversibility.

## 11. Primary-literature scope retained

The local prior packages contain the task-first governing-source recovery and exact
primary-source receipts. Relevant conventional baselines include:

* Anderson, Craciun and Kurtz, complex-balanced product-form stationary distributions
  (the classical theorem applies only with its equilibrium hypotheses).
* Anderson, Cappelletti and Kim, J. Applied Probability 2020,
  <https://doi.org/10.1017/jpr.2020.28>: accessible publisher abstract inspected;
  its described binary/single-linkage and pure-complex hypotheses do not directly
  certify this cubic multiple-linkage fixture. No unavailable full proof was assumed.
* Bibbona, Kim and Wiuf, <https://pmc.ncbi.nlm.nih.gov/articles/PMC7423442/>:
  the inspected Theorem 4.1 includes positive inflow/outflow of every species;
  satellites here have neither. This is not a survey-completeness assertion.
* Dai and Meyn, <https://people.orie.cornell.edu/jdai/publications/daiMeyn95.pdf>:
  ordinary fluid/Foster queueing stability and moment machinery; not a theorem that
  generic fluid stability supplies the present all-exponential conclusion.
* Angeli, De Leenheer and Sontag,
  <https://www.sontaglab.org/FTPDIR/angeli_leenheer_sontag_math_biosciences_MBS-D-06-00188R1.pdf>:
  ordinary support/siphon invariant-face geometry. It explains the leading face
  obstruction but is not itself a stochastic seeded-boundary proof.

The ConStRAINeD project page <https://constrained.polito.it/publications/> announced
all two-species weakly reversible positive recurrence as work **in preparation** at
inspection; the manuscript was not available there or inspected. No general
arbitrary-dimensional conclusion or proof details are inferred from that announcement.
Historically denied/gated full texts were not retried or accessed by alternate routes.
