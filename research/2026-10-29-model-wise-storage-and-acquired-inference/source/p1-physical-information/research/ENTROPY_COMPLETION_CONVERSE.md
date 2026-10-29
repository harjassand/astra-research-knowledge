# The entropy floor of a regenerative event record

29 October 2026, Brisbane. Root construction. This is a variational
characterization in an explicit record topology, not an exact-record
optimizer or a physical thermal device.

## 1. Record and physical scope

B is a finite set of resolved singleton microscopic ports, all fixed
by physical reversal. K_ij(t) is the stationary FLUX density of a hidden
excursion from port i to its next port j, with positive interior duration
t. Native initial port holds are separate. Direct flux d_ij, i!=j, is
also separate; d_ii=0. Let F_ij=integral K_ij and rho_i=sum_j(F_ij+d_ij).
Assume port row and column flux sums agree and the trace is irreducible.
Assume R>0 whenever using per-departure or mean-cycle quantities; the
event-free singleton case has E=J=V=0 and is treated separately.
Supplied positive port weights w_i fix native holding rates rho_i/w_i.
Let V=sum_ij integral t K_ij(t)dt be finite, W=sum_i w_i+V, R=sum_i rho_i.

The observed event-flux reversal divergence is

    J(K,d)=sum_ij integral K_ij(t)log[K_ij(t)/K_ji(t)]dt
                      +sum_i!=j d_ij log(d_ij/d_ji).       (1)

Assume J is finite. Supports are therefore reciprocal up to null sets.
For a finite hidden CTMC with stationary weights w and involution Theta
fixing B, define its intrinsic stationary reversal-divergence rate by

    E=sum_x w_x [sum_y!=x q_xy log(q_xy/q_Theta(y),Theta(x))
                            +lambda_Theta(x)-lambda_x], (2)

where lambda_x=-q_xx. Then sigma=E/W is the long-horizon path KL rate.
The fixed-horizon stationary path KL also has boundary D(pi||pi Theta).
Here pi need not be Theta-invariant. Thermodynamic interpretation requires
faithful physical reversal and local detailed balance. The prior all-even
and midpoint-operation theorems keep their own assumptions unchanged.

Microscopic excursion-flux KL equals E: port-weight endpoint terms cancel
by balanced port traffic, jump terms average to stationary edge fluxes,
and holding terms average to occupation. Because ports are fixed renewal
states, no hidden initial-preparation boundary survives this regenerative
identity. Data processing gives E>=J. This lower bound is established
Markovian-event machinery; the new target is a matching converse.

## 2. Finite paired channels

Take a common finite duration partition I_k and define

    a_ij,k=integral_(I_k) K_ij(t)dt,
    nu_k=sum_ij a_ij,k,
    c_k=[sum_ij integral_(I_k) t K_ij(t)dt]/nu_k.

Delete zero-mass bins. For each positive cell (i,j,k), place n directed
hidden phases between i and j, each with rate lambda_k=n/c_k. Entrance
rate from i is a_ij,k/w_i; each phase has weight a_ij,k/lambda_k.
Keep direct port rates d_ij/w_i. All rows and stationary flows balance.
The chain is finite and irreducible. It preserves EXACTLY w_B, d, F,
every port holding rate, total hidden mass V and mean cycle duration W/R.

If g_(n,c) is the Erlang density of shape n and mean c, its return law is

    K^(n)_ij(t)=sum_k a_ij,k g_(n,c_k)(t).                 (3)

Theta fixes ports and pairs phase l of (i,j,k) with phase n+1-l of
(j,i,k). Self-return chains reverse internally. Finiteness of J ensures
every positive channel has a reverse partner. Paired escape rates agree,
so holding terms in (2) vanish. Along one channel the rate-ratio sum is
log(a_ij,k/a_ji,k)+log(w_j/w_i). The port-gradient term cancels globally.
Thus the exact microscopic cost is

    E_(n,partition)=sum_ij,k a_ij,k log(a_ij,k/a_ji,k)
                         +sum_i!=j d_ij log(d_ij/d_ji).  (4)

Shape n changes clocks and state count, but not (4). Overlapping Erlang
components hide k, so the OBSERVED duration divergence of (3) may be
strictly smaller than (4). A common-Erlang-mixture representation is an
exact realization of that mixture, not automatically its exact entropy
minimum. The matching result below is in closure.

## 3. Approximation in probability AND duration

Narrowing Erlang kernels on a fixed histogram produces spikes and fails
L1 convergence. Refine the bins faster than the kernel width.

Use nested logarithmic bins on [exp(-m),exp(m)] with width delta_m=2^-m,
plus two tail bins; take shape n_m=2^m. Then sqrt(n_m)delta_m ->0.
Use the aggregate conditional means c_k even on the tails.

For Z_n~Gamma(n,rate n), the continuous common-kernel mixture is the
law of T Z_n. Its density operator A_n f(t)=integral f(s)g_(n,s)(t)ds
preserves mass and first moment and contracts L1 with weight 1+t.
Multiplicative dilation is strongly continuous in this space. Since
Z_n->1 in L2 and E Z_n=1, approximation first by continuous compactly
supported densities away from zero, then contraction, proves
A_n f->f in L1(1+t). This uses only a finite first moment.

For s,c in one interior log bin,

    D(g_(n,s)||g_(n,c))=n[s/c-1-log(s/c)].                 (5)

Pinsker bounds the L1 difference by O(sqrt(n)delta_m). For the weighted
part use t g_(n,s)=s times the Gamma(n+1,rate n/s) density; its difference
is O((1+s)(sqrt(n+1)delta_m+delta_m)). Integrating makes the interior
quantization error vanish. On the two tail bins, summed over endpoints,
the error is bounded by twice the aggregate tail mass plus twice its
first moment, because nu_k c_k equals the actual tail first moment.
It also vanishes. Therefore

    sum_ij integral (1+t)|K^(m)_ij(t)-K_ij(t)|dt ->0.      (6)

Total mean is exactly preserved while the stronger weighted error tends
to zero. Mere finite first moment supplies no source-uniform convergence
rate or finite-data acquisition guarantee.

## 4. Variational characterization

Consider all sequences of finite CTMC explanations with arbitrary hidden
parity fixing B, the same w_B,d,F, native port clocks and total V, whose
records converge as in (6). Then

    inf_(such sequences) liminf_m E_m = J(K,d).           (7)

For the lower bound, every E_m dominates its observed event divergence;
relative entropy is lower-semicontinuous when the event measures and
their reversals converge in total variation. For the upper bound, (4)
is the common finite-partition KL, bounded above by J. Nested generating
partitions increase this KL to J. Construction (3) supplies the required
convergence. Dividing by the UNCHANGED W or R gives the analogous exact
infimum for entropy per native time or per departure.

Consequently no universally valid lower bound on E that is lower-
semicontinuous in this record topology can exceed J in this unrestricted
parity/state/rate class. Additional physical or resource information can
support stronger bounds. All-even inference excludes the new channels
and is not contradicted. Exact matching to a fixed nonreciprocal record
is a different problem; a sharp obstruction is developed below.

## 5. State, clock, preparation and acquisition costs

The construction uses n times the number of positive ordered endpoint/bin
cells, at most |B|^2 K n hidden states. Its maximum hidden rate is
max_k n/c_k. Both may diverge with accuracy. A fixed clock or state ceiling
therefore defines a different problem. Real coefficient existence does
not supply instrument or arithmetic precision. A finite-precision version
needs certificates for its bin integrals and rate errors.

Stationary preparation has parity divergence

    D(pi||pi Theta)=W^-1 sum_ij,k a_ij,k c_k
                                      log(a_ij,k/a_ji,k). (8)

This is finite at every finite construction; a uniform free bound has
not been assumed. Ordinary memory storage, stationary preparation time,
reset work and physical implementation are additional resources. The
source law is not identified. Bin masses and aggregate bin means are
the decisive supplied/acquired inputs; the old finite assay does not
already provide all of them.

This is a foundational completion theorem. Conventional hidden-network
optimization remains the strongest equally informed comparator when
physical topology, all-even parity or finite resources are known. No
sample or computational speedup is asserted.

## 6. Exact matching can have infinite cost while the closure floor is finite

Finite microscopic reversal divergence requires every positive directed
edge to have its physical reversed edge. Theta bijects positive hidden
itineraries between a port pair at each jump length. The leading
small-time order of K_ij is the least number of hidden states visited,
minus one. Positive path weights cannot cancel the leading coefficient.
Finite E therefore requires equal leading powers of K_ij and K_ji.

Take two unit-weight ports, no direct jumps, and

    K_12(t)=exp(-t),       K_21(t)=t exp(-t).              (9)

Both integrated fluxes and native port rates are one; V=3 and W=5.
The observed divergence is exactly

    J=integral exp(-t)(1-t)(-log t)dt=1.                 (10)

Gamma derivatives at 1 and 2 verify this, with Euler constants cancelling.
The record has a five-state directed-cycle realization: one hidden phase
from port 1 to port 2, two on the return, all phase rates one.

EVERY exact finite completion fixing the ports under physical reversal
has E=infinity. K_12(0)>0 forces a path 1->x->2. Finite E would force
2->Theta(x)->1 and hence K_21(0)>0, a contradiction. Yet (7) gives finite
approximations with E->1, preserving port clocks, endpoint fluxes and total
mean. Their normalized rate tends to 1/5.

This separates exact structural information from finite-precision event
information. It does not mean a physical laboratory source dissipates
infinite heat: the infinity is microscopic path-support failure in an
ideal finite jump-model class. Exact short-path zeros are not acquired
merely by collecting finitely many duration observations.

A further necessary condition for exact finite equality E=J follows
from the equality case of data processing. On a fixed itinerary the
microscopic likelihood ratio is C exp(sum_l delta_l s_l), where delta_l
is the reversed escape-rate difference and s_l are positive dwell times.
Conditional on their total t, the dwell simplex has full support; a
ratio depending only on t forces all delta_l to coincide. Every positive
finite itinerary has positive density at every t>0, so every itinerary
for the same pair must give the same function. Necessarily

    K_ij(t)/K_ji(t)=C_ij exp(delta_ij t).                 (11)

For a finite phase-type record this condition is also sufficient, as
established by the next construction. Non-exponential ratios still rule
out exact finite saturation even where finite E is possible.

## 7. Exact finite attainment: a complete criterion

Assume each nonzero K_ij, after normalization, is a finite phase-type
duration density. Every record produced by a finite CTMC has this
property: condition its killed hidden chain on eventual exit at j by
the absorption-probability h-transform, and trim inaccessible phases.

Then an exact finite completion attains E=J IF AND ONLY IF every
off-diagonal directional ratio has form (11). The criterion concerns
attainment by one finite model. It does not evaluate the infimum among
exactly matching models when attainment fails.

Here is the sufficiency construction. For an unordered pair, write

    K_ij(t)=beta exp(Tt) r,    r=-T1,    beta 1=a=F_ij.

Trim phases so the occupation vector z=beta(-T)^-1 is strictly positive.
With D_z=diag(z), the reversed-path channel has

    T_left=D_z^-1 T^T D_z,
    beta_left=z elementwise-times r,
    r_left=beta^T elementwise-divided-by z.

The entrance vector beta_left has total flux a, and this channel has
the same duration density as the forward channel. For constants C,delta
from (11), define

    h=(-T_left+delta I)^-1 r_left,
    T_minus=D_h^-1 (T_left-delta I) D_h,
    r_minus=D_h^-1 r_left,
    beta_minus=(beta_left elementwise-times h)/C.         (12)

The target reverse density has finite total mass. Reachability of every
retained phase makes h finite and positive; T_left-delta I is transient.
The equation (T_left-delta I)h=-r_left verifies that (12) is a proper
transient channel. It realizes exactly

    beta_minus exp(T_minus t) r_minus
                  =K_ij(t)exp(-delta t)/C=K_ji(t).

Pair forward and reverse phase labels under Theta. Their escape-rate
difference is delta. Entrance, internal and exit factors telescope, so
every microscopic excursion-flux likelihood ratio is exactly C exp(delta
t), already a function of the observed endpoints and duration. Equality
in data processing follows. The actual reverse stationary weights are
beta_minus(-T_minus)^-1; they are generally NOT z times h/C.

For a self-return density, use its channel and reversed-path copy with
half the flux each and swap the copies. Their combined law is unchanged
and their entropy is zero. Keep reciprocal direct rates d_ij/w_i. Pairwise
assembly and port-flux balance then give an irreducible finite CTMC with
the exact complete native record, port weights, clocks and total mean.

The independent derivation and exact six-state rational control are in
entropy_completion_review/EXACT_ATTAINMENT_CLASSIFICATION.md. The control
has E=J=89/418; the stationary jump-log contribution cancels and the
holding-asymmetry contribution supplies all of E. This checks a term
that is absent from the equal-clock approximation but essential in the
general physical-reversal formula. Phase-type reversal and exponential
tilting are standard ingredients; historical priority of this combined
attainment classification has not been established.

## 8. Equal reversed clocks define a distinct physical class

Suppose the admitted class additionally requires

    lambda_Theta(x)=lambda_x for every microscopic state x.

Then the dwell-simplex necessity has delta=0. Exact finite attainment
therefore occurs if and only if each K_ij(t)/K_ji(t) is constant in t.
Sufficiency follows from (12) with delta=0: h=1 and the reversed PH
channel has exactly the original diagonal escape rates. The paired
Erlang approximations already have this property, so the closure floor
J in (7) is UNCHANGED by this equal-clock requirement. Exact attainment
and robust approximation again have different information boundaries.

An arbitrary involution is a mathematical reversal contract; it does
not establish which reversal is physically available for a given
experiment. Equal reversed escape rates, stationary parity symmetry,
an all-even state model, and local detailed balance are different
constraints. None is silently inferred from the observed event law.
The main rate is path-reversal divergence under the declared contract.
A heat or total physical entropy interpretation additionally requires
the appropriate thermodynamic dynamics and reversal of any odd external
parameters. No apparatus, parity pulse or microscopic control is
provided by this realization theorem.
