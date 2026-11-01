# Acquiring service under arbitrary finite shared-port composition

1 November 2026. Solo construction and exact executable controls.

The central question remains whether a sole linear reservoir stabilizes every
conservative weakly reversible module. The result here is a compositional
principle, with a raw-list acquisition proof, rather than another isolated
network. It also identifies a precise obstruction to extending its scalar
representation to general coupled modules. Historical priority is not settled.

## Theorem

Let A be the reservoir species. Suppose a finite conservative mass-action module
is a union of weakly reversible submodules on disjoint dynamic species blocks
`B_1,...,B_k`, sharing A and any globally inert catalysts. Each submodule has
internal stoichiometric rank at most one. A channel may read A, its own block,
and the inert catalysts; it may not read another dynamic block. No bound on k,
reaction degree, linkage count or deficiency is imposed. All rates are fixed
positive rationals; propensities use falling factorials. Adjoin only

    0 -> A at rate lambda,       A -> 0 at rate mu A.

Then every communication class is nonexplosive and positive recurrent. Its
unique invariant probability has a nonzero exponential moment of actual total
count. The classwise tilt, finite head, generator bound and factored stationary
moment bound can be acquired by finite exact arithmetic from the raw reaction
list, rates and one initial state. No equilibrium, mixing law, stationary fiber,
conditional independence or occupation premise is input.

In particular this covers arbitrary conservative rank-one internal modules in
any species dimension. Finite bounded internal phases can be joined as described
below. The full reaction graph can have arbitrarily large internal rank through
the number of joined modules. This theorem does not include arbitrary coupled
rank-two submodules.

## 1. Acquire the decomposition and class coordinates

Ignore zero-change channels. A nonport species is dynamic if some internal
reaction changes it; the others are inert catalysts with their actual initial
counts. Join dynamic nonport species whenever one raw channel reads or writes
both. The connected components are the candidate blocks. Exact rational rank
tests on `(A,block)` and directed-graph tests acquire the stated rank-one and
weak-reversibility properties. The constructor checks these, rather than
inferring them from a model label. Rejection is not instability.
Every nonzero channel must be assigned to a block. An A-only stoichiometric
change is rejected even when another species catalyzes it: a positive conserved
weight cannot permit that change. The executable controls also reconstruct the
class norm's zero increment on every actually enabled internal channel.

For a nonzero rank-one block, divide a nonzero reaction vector by the gcd of its
entries to obtain a primitive integer vector v, and verify that all other
reaction vectors are integer multiples of it. Conservativity forces both signs
in v. A positive integer conservation vector is acquired explicitly: let P be
the sum of positive entries of v and R the absolute sum of negative entries;
give positive entries weight R, negative entries weight P, and zero entries
weight 1. Its scalar product with v is zero.
Positive block weights may be rescaled to give their shared A coordinate the
same weight; inert catalyst weights are arbitrary positive values. Thus the
conservation acquisition is compatible across all the joined blocks.

Nonport states in the block have the form `x_i=b_i+v_i q` on a classwise affine
lattice. If the nonport entries of v have both signs, nonnegativity gives a
finite integer interval for q. It and every outside population bound are
computed by integer divisions. These are bounded phases, not frozen fibers:
their actual generators and jumps will remain in all estimates.

Otherwise orient v so its nonport entries are nonnegative. Then `v_A=-r<0`.
Shift the minimum nonnegative lattice coordinate to q=0, giving

    x_i=b_i+v_i q,       q>=0,       a=x_A>=0.

The b_i are acquired nonnegative integers. Species with v_i=0 are fixed. A
linkage requiring more of such a fixed catalyst than the actual count is
permanently disabled and may be removed as a whole: that coordinate is constant
on every complex in the linkage. If every linkage in a block is disabled,
the block is frozen at its actual initial state.

For each unbounded ray block put `s=sum_(i != A) v_i>0`. The integer norm

    N_c=a+sum_ray r_i q_i
          +sum_bounded[-v_A,j q_j+max(v_A,j,0) Q_j]

is nonnegative, where a bounded coordinate has been shifted to `[0,Q_j]`.
Every internal jump preserves N_c; immigration increases it by one and true
death decreases it by one. Its sublevels in this classwise coordinate set are
finite. Thus

    N_c(X_t) <= N_c(X_0)+Poisson(lambda t)

proves nonexplosion. This also pays all finite-time polynomial/exponential
integrability needed for localized Dynkin below.

## 2. A source-order lemma acquired from weak reversibility

Fix a live linkage in a ray block. Since v_A is nonzero, its minimum-A complex
`y_0` is unique. Write its A exponent as m, and its total exponent on moving
nonport species as beta. Every other complex is

    y_j=y_0-k_j v,
    (y_j)_A=m+r k_j,
    sum_moving (y_j)_i=beta-s k_j,       k_j>=1.

Here k_j is an integer. Weak reversibility supplies an outgoing edge from y_0
with strictly positive A increment. Choose one, and let R_l(a,q) be its actual
propensity. In a nontrivial linkage beta>=s>0.

Let `A_*=a+sigma`, with sigma larger than every absolute A jump. There is an
acquired integer Q0 such that for q>=Q0 every moving falling-factorial factor
in the minimum source is at least `(q+1)/2`. For every adverse (A-decreasing)
channel from y_j, actual source division then gives

    lambda_j(a,q)/R_l(a,q)
       <= C_j A_*^(r k_j)/(q+1)^(s k_j),                 (1)

whenever a>=m. If a is below the larger source exponent, its propensity is zero.
The constants C_j are exact products of rate ratios, catalyst factors and
integer affine-population bounds. There is no conditional probability in (1).

## 3. One tail profile controls all unbounded modes simultaneously

Choose an integer p at least

    m_l+(r_i/s_i) beta_l

for every live ray linkage, and at least every A source exponent in the bounded
modes. Put `g(a)=(a+sigma)^(-p)`. For all enabled negative A jumps,

    0<=g(a+d)-g(a)<=B A_*^(-p-1),

with acquired rational B. A selected positive jump of size d gives

    g(a+d)-g(a)<=-d_l A_*^(-p-1),
    d_l=p d [sigma/(sigma+d)]^(p+1)>0.

Use (1). In the region `q+1>=K A_*^(r/s)`, a sufficiently large acquired integer
K makes all adverse channels of a linkage cost at most half its selected
negative term. In the complementary region, every source monomial has upper
bound a constant times

    A_*^[m+r k+(r/s)(beta-s k)] = A_*^[m+(r/s)beta] <= A_*^p.

After multiplying by the profile difference this is bounded. A positive term
requires a>=1, so it can be bounded by a constant times a. The same argument
charges the minimum source that is retained as a negative term in the estimate.
For q<Q0, explicit affine-count upper bounds give the same conclusion. At a=0
there is no adverse A-decreasing channel.

Bounded modes contribute at most C a using their acquired finite outside
population bounds. True death's positive profile increment is charged likewise;
immigration's increment is nonpositive. Summing all actual subgenerators proves
the single GLOBAL inequality

    Lg <= C a-T,
    T=sum_live_linkages c_l R_l(a,q_i)/(a+sigma)^(p+1)
                                      *1_{q_i>=Q0,i},    (2)

where c_l=d_l/2>0 and C is an acquired finite rational. The indicators in (2)
are only bounds in the proof; g itself has no population selector. The
implementation uses integer powers, explicit coefficient bounds and integer
doubling. No supremum over an unbounded population is supplied as an oracle.

Although the modes compete for the same A molecules, (2) is pointwise in the
joint state. Independence of their clocks or conditional histories is irrelevant.

## 4. Construct a dormant-head correction under arbitrary competition

For each ray block take the smallest minimum-source A exponent among its live
linkages; let M be the maximum of those block minima. Thus at a>=M every ray
has at least one active selected source for all sufficiently large q_i.

We now acquire H(a), supported on a<M, with

                         LH<=-1 on a<M                 (3)

for ALL simultaneous ray populations and bounded phases. This is the important
composition step: no bounded-rate assumption on the other ray populations is
made.

Write `H(a)=sum_(j=a)^(M-1) d_j` for a<M, and H=0 above it. Choose the positive
slopes d_a successively, from a=0 upward. At a fixed a, every A-decreasing
channel has positive H cost

    w_j(a)=sum_(h=a+Delta_A)^(a-1) d_h.

Its source enabling ensures a+Delta_A>=0, so this cost uses only slopes already
chosen. For a live linkage (1), with this fixed a and fixed w_j, explicitly
acquire a population threshold above which its whole adverse H cost is at most
R_l(a,q). Below the threshold, bound all affine counts by their threshold
values. This yields a finite rational D_(a,l) and, for EVERY q,

    adverse H cost in linkage l <= R_l(a,q)+D_(a,l).

Disabled linkages give zero. Bounded phases contribute an acquired finite bound
by their whole coordinate interval. Summing gives a finite D_a. Set

    d_a >= max(1, [1+mu a d_(a-1)+D_a]/lambda),          (4)

where d_(-1)=0. Each selected A-increasing jump reduces H by at least d_a,
even if it overshoots M. Therefore

 LH <= -lambda d_a+mu a d_(a-1)+D_a
                         +(1-d_a)sum_l R_l <=-1.

This proves (3). It is a forward finite recursion: thresholds in this step
depend only on earlier slopes, so there is no hidden fixed-point assumption
between an adverse-rate bound and its own head function.

## 5. Pay actual returns to the head

Outside a<M, a jump can enter the head only when

                         M<=a<M+L,

where L bounds the absolute A jump (and includes death's unit jump). Only
finitely many a values are involved. For any fixed positive epsilon and delta,
apply the same exact source division (1), now to the known costs H(a+Delta_A).
Choose thresholds so that delta times each large-q entry cost is at most its
share of epsilon T/2. Below those thresholds bound every source count explicitly.
True death contributes the actual finite entrance
`mu M H(M-1)`; bounded phases are charged on their entire ranges. This constructs
a finite rational E such that

    delta LH <= epsilon T/2+E 1_{M<=a<M+L},   a>=M.       (5)

All source returns, overshoots and last-copy deaths are included. E is acquired
after epsilon and delta; it is not required to be small.

## 6. Small tilt and complete actual-time Foster receiving

Choose eta>0 rational sufficiently small, set t=1+eta, and put

    D=mu(1-1/t),   epsilon=D/[2(C+1)],   delta=2lambda eta,
    h=1+epsilon g+delta H.

The previously acquired g,H,C are independent of eta, so choosing eta small
enough to give `1<=h<=3/2` is noncircular. Now acquire E by Section 5. Internal
jumps preserve N_c. Exact tilted algebra gives

 t^(-N_c) L(t^N_c h)
     =Lh+lambda eta h(x+e_A)-D a h(x-e_A).

At a<M use (2),(3), h>=1 and h<=3/2 to bound this by

    -D a/2-epsilon T-delta+(3/2)lambda eta
                                           <=-lambda eta/2.   (6)

At a>=M, (2),(5) bound it by

    -D a/2-epsilon T/2+E 1_{a<M+L}+(3/2)lambda eta.      (7)

Choose A_cut>=M+L and A_cut>=4lambda eta/D. Equation (7) is negative by at
least lambda eta/2 for a>=A_cut. For the remaining finite interval
`M<=a<A_cut`, each ray block has a selected source satisfying

    c_l R_l(a,q_i)/(a+sigma)^(p+1) >= c_i (q_i+1)^beta_i

for q_i>=Q0,i, with an acquired c_i>0. Minimum falling-factorial values over
this finite A interval and the outside lower bounds give c_i explicitly.
Acquire Q_cut,i so that its contribution epsilon T/2 exceeds E+2lambda eta.
Then (7) is negative by at least lambda eta/2 if ANY ray is above its cutoff.

Thus outside the acquired finite head

    a<A_cut,       every ray q_i<Q_cut,i,

the explicit normlike function `W=t^N_c h` obeys

    LW<=-zeta W,       zeta=lambda eta/3>0.              (8)

The head includes every bounded-mode phase; none has been frozen. A count
threshold N_star enclosing that head is obtained by summing r_i Q_cut,i and
the bounded norm spans. On its finite sublevel, bound raw propensities by the
corresponding integer count powers. This gives a finite rational Lambda_star
bounding total rates. A safe factored head constant is

    C_F=(3/2)(zeta+Lambda_star)t^(N_star+1).

No huge final power need be expanded. Localization, integrating-factor Dynkin
and Fatou give

    E_x W(X_s)<=exp(-zeta s)W(x)+C_F/zeta.

Tight occupation averages construct an invariant probability in each
communication class, and irreducibility there gives positive recurrence and
uniqueness. In a weakly reversible network every communication class is closed:
the reverse path of an enabled channel is the directed return path of its
complex, translated by the same nonnegative residual count. The stationary
moment obeys `pi(W)<=C_F/zeta`.

Actual total count is at most `C_0+B_0 N_c`, with acquired classwise integers:
bounded-phase and offset counts go into C_0, and take B_0 at least each
`s_i/r_i` and 1. Choose rational rho>1 with rho^B_0<=t, for example
`rho=1+eta/2^B_0` when eta<=1. Then

    pi(rho^total_count)<=rho^C_0 C_F/zeta <infinity.

If all nonport modes are bounded or frozen, no profiles are required: N_c=a
plus bounded terms, and `L(t^N_c)/t^N_c=lambda(t-1)-mu a(1-1/t)` directly gives
the result, including every prescribed t>1 at that scope.

## 7. A decisive obstruction beyond the compositional case

The earlier directed cubic module

    2A+B -> 2B+C -> A+2C -> A+B+C -> 2A+B

with rates 1,2,3,5 and the same reservoir has a coupled rank-two outside block.
It rules out EVERY scalar multiplier `W=t^(A+B+C) h(A)` with t>1 and positive
finite h(0),h(1),h(2),h(3) as a pointwise Foster function outside a finite head.
Boundedness of h at other A values is unnecessary for the obstruction.

At `(A,B,C)=(0,n,0)` all internal channels are disabled, so nonpositive tilted
drift for all large n requires `h(0)>=t h(1)`. At `(1,n,0)` they are still
disabled. Its drift is

    lambda[t h(2)-h(1)]+mu[h(0)/t-h(1)].

The second term is nonnegative, so nonpositive drift requires
`h(1)>=t h(2)`. Hence `h(0)>=t^2 h(2)>h(2)`.
Equivalently, if D0,D1 denote these two tilted drifts, the exact identity
`h(0)-t^2 h(2)=-(lambda+mu)D0/lambda^2-t D1/lambda`
is a positive-coefficient implication from D0,D1<=0.
But at `(2,n,0)` the first cubic channel is enabled at rate 2n, takes A to
zero, and every other internal channel is disabled. Its tilted drift is

 2n[h(0)-h(2)]+lambda[t h(3)-h(2)]+2mu[h(1)/t-h(2)],

which tends to positive infinity. Contradiction. The same argument excludes
an additive correction `A+B+C+f(A)` of arbitrary scalar shape: its first two
drift constraints force `f(0)-f(1)>=1` and `f(1)-f(2)>=1`, while the same
2n internal term then grows positively.

These states belong to the same closed communication class: from `(3,n,0)`,
the first and fourth internal edges give `(2,n+1,0)`; one immigration restores
A=3. Weak reversibility supplies translated return paths, and the reservoir
connects all finite A values. Thus choosing different constants for unrelated
classes does not remove this obstruction.

A sum of any number of A-only profiles is still A-only, so more scalar profiles
cannot repair it. The existing multivariable Foster construction for this very
prototype remains valid. The universal extension must carry nonport geometry
through the potential or a genuinely different representation. One cannot
freeze a higher-rank face, use a rank-one certificate there, and treat its
constants as uniform while the other coordinates move.

## 8. What has changed and what remains

The acquired shared head, especially recursion (4), proves that arbitrary
competition through one reservoir does not prevent stabilization of this whole
modular class. It is not an assumed service interface and is not justified by
enumerating cubic fixtures. The unresolved general step is handling a genuinely
coupled higher-rank block: acquire a multivariable source/face cover whose
outside parameters evolve, with all actual head entries paid. Section 7 proves
why the scalar construction cannot supply that universal bridge.

The strongest received Astra comparison remains N1612's completed small-tilt
binary multiface theorem at db0969a8586afaa38137a4371b3457c5576fadea. Its graph
scope and accepted audit are preserved. N1485's actual rank-monotone forcing
and raw-split proofs were also read: that rank is a finite label-progress rank
under restricted pooled binary contracts, not the stoichiometric rank here.
Its retained face, terminal and physical-clock hypotheses cannot be transferred
by similar terminology. No novelty or superiority claim follows from failure
of either source's structural guard. Product-form and ordinary Markov/Foster
machinery remain the reference comparators; our incompatible complex-balance
controls avoid presenting a product-Poisson instance as new capability.

The Bruno–Pasqualotto heat-flow correction was resolved separately. Its Theorem 1
closes the ADM counterexample route and Theorem 2 covers rotationally invariant
homogeneous quartics. The exact planar reductions and fixed-root obstruction
are retained; a general non-invariant planar construction remains a separate
question, with no transfer by analogy from this count-chain argument.

## Executable evidence and cost

`rank_one_modules.py` acquires coordinates, graph sources, tail order and
constants from the raw module. `shared_port_modules.py` acquires the joint head,
all entry bounds, tilt and finite cutoff. `check_shared_port.py` compares their
inequalities with the actual raw-channel generator using exact Fraction
arithmetic. The retained run covers 1,571 states across 16 raw inputs, including
unequal weighted degrees, multiple deficient modules, missing fixed catalysts,
bounded phase motion, competing large populations and last-copy entrances.
It also refuses the coupled rank-two prototype under this theorem's guard.
Finite checks supplement Sections 1–6, which establish the quantifiers.

Acquisition has real costs: graph and rank work, finite slope recursion, rational
arithmetic and coefficient/power bit lengths, integer searches for the heads,
and final power evaluation if requested. The largest acquired head in the
retained controls has 402 bits; that is a finite exact threshold, not practical
scale. Neither a polynomial bit-complexity nor practical numerical tail claim
is made. No stationary probability table or exponential head power is required
by the representation.

Run from this workspace with
`env PYTHONDONTWRITEBYTECODE=1 python3 work/capability_first_20261101/check_shared_port.py`.
`emit_shared_port_example.py` writes a concrete two-module certificate including
the exact head function, source data, tilt and factored actual-count moment
bound. `receive_shared_port_example.py` reads that file without importing either
constructor, reconstructs raw-channel norm conservation, the head rate and
factored bound, and checks 26 actual large-state generator values. This is
separate arithmetic receiving of that concrete artifact, not a whole independent
mathematical audit.
The source and controls use Python's standard library. No external action,
hardware claim, independent-audit claim or general weak-reversibility theorem
is implied by this solo proof.
