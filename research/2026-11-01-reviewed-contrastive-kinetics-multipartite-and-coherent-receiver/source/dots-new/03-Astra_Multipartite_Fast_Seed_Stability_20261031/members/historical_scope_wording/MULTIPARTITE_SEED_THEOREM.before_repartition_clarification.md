# Fast boundary-seed amplification on complete multipartite hub graphs

**Candidate ordinary proof; independent review pending.** Pure mathematical CTMC
research. Earlier accepted files are unchanged. This theorem does not assume or
establish arbitrary one-port conservative stability or general weak reversibility.
No literature is fetched in this continuation. The preceding package's disclosed
source-access failure remains quarantined; no novelty or source-clearance claim is
imported from it.

## 1. Raw class and the new obstruction

There is one open species A and n-1 satellites, n>=3. The only count-changing pair
is 0<->A, with positive rates lambda,mu. All other nonnull channels are binary:

* 2A<->H for every A-free square-free hub H=X+Y;
* selected reversible A+X<->H arms, with every satellite X covered by an arm.

All rate constants are strictly positive. Hub edges form a COMPLETE MULTIPARTITE
simple graph on ALL satellites, with q>=2 nonempty independent parts. Thus every
cross-part pair is a hub and no within-part pair is a hub. There are no free isolated
satellites. The complement graph's connected components, checked to be cliques,
acquire these parts directly from the raw list. They are not a supplied grouping.

For q=2 this overlaps a one-component subfamily of the earlier biclique theorem.
For q>=3 it includes triangles and arbitrary cliques, where the maximum-matching
inventory has exact drop-two counterexamples. Disconnected latent components and
free passengers, covered in part by the earlier theorem, are NOT included here.
Neither sufficient family contains the other.

Write Z_j for the total satellite count in part j and N=A+sum_j Z_j. Define

    M=max_j Z_j,       R=N-M=A+sum_j Z_j-max_j Z_j.

Every internal product contains A or a hub, so R>=1 cannot become R=0 internally.
R=0 means A=0 with all satellites in a single part, and every internal source is
disabled. Unlike the earlier matching inventory, R counts a deficit from the largest
part; no universal one-Lipschitz matching premise is used.

## 2. Raw rate summaries and acquired weights

Let a be the sum of 2A->H rates, k_X the sum of A+X->H rates, b_h the H->2A rate,
and s_h the sum of all rates out of hub h (including b_h). Set

    k_-=min_X k_X, k_+=max_X k_X,
    b_-=min_h b_h, s_+=max_h s_h,
    b_0=min_h(s_h+b_h), S=sum of all internal rate constants,
    F_0=2a+k_+,
    eta=b_-/(16s_+),
    c_0=min(eta*k_-/3,b_-/4),     gamma=c_0/(1+eta).

All are acquired by finite raw sums/minima. Since s_+>=b_-, 0<eta<=1/16. Put

    P=(1+eta)R-eta A = R+eta(R-A).

For R>=1, R<=P<=(1+eta)R. The small latent excess weight ensures fast A-capture
improves the inverse profile, while potentially adverse cross-hub reverse arms are
charged against their own amplification rates.

## 3. All-count inverse bounds, including max ties

Each internal jump changes every part total by at most one, so |Delta R|<=1.
Direct enumeration of the 2A/hub and arm/hub forms gives |Delta P|<=1+2eta<2.
Both endpoint P values are at least one whenever R>=1. Therefore P/P'<=3 and

    |1/P'-1/P| <= 6/P^2.                                      (1)

This is an exact finite-count estimate, including switches and ties of maximizing
parts. The total internal rate is at most S N^2, so globally

    L_int(1/P) <= 6 S N^2/P^2.                                (2)

No smooth max derivative or continuum approximation is used.

### Sharper boundary-cone estimate

Suppose 1<=R<N/2. Then M=N-R>N/2 is a UNIQUE largest part, call it I. Its old part
remains a maximizer after each enabled internal jump, though the destination may
tie. Let U=R-A be the count outside I.

1. A+X->H with X in I changes P by eta (if H meets I) or 1+2eta (otherwise). Its
   inverse increment is at most -eta/(3P^2). The aggregate rate is at least k_- A M.
2. For a hub meeting I, H->2A changes P by 1-eta. Its inverse increment is at most
   -(1-eta)/(2P^2)<=-3/(8P^2).
3. For the same cross hub, H->A+X with X in I changes P by -eta, whose inverse
   increment is at most 2eta/P^2. Reverse arms returning X outside I change P by
   +1 and have nonpositive inverse drift.

The potentially adverse cross-hub term at hub h is thus at most 2eta s_h/P^2,
while amplification contributes at most -3b_h/(8P^2). The chosen eta gives
2eta s_h<=b_-/8<=b_h/8. At least b_h/(4P^2) negative drift remains. Complete
multipartiteness gives the exact cross-hub product sum M U. Together with capture,
these fast channels contribute at most

    -c_0 M(A+U)/P^2 <= -gamma M/P.

All other potentially positive inverse increments have a source made of two seed
particles: 2A, A+an outside satellite, or a hub entirely outside I. Each such rate
is at most its constant times R^2. Their total positive contribution is at most6S
by (1). Consequently

    L_int(1/P) <= -gamma (N-R)/P + 6S,    1<=R<N/2.             (3)

This is earned fast seed amplification. It makes no stationary-fiber, independent
lineage, success-coin, or uniform-mixing assumption.

## 4. An oppositely signed interior activation correction

The inverse profile is good near an inactive face, but need not have negative drift
in the interior. Fix any finite t>1 and define

    D=mu(1-1/t),       epsilon=min(1/2,D/(4F_0)).

For R>=1 set

    h=1+1/P-epsilon*A/(N+1),      W=t^N h.                     (4)

At R=0 set h=4t. Always 1/2<=h<=H:=4t, so W is normlike and comparable to t^N.
The negative A/(N+1) term rewards activation in the interior; its positive forward
capture contribution is paid by actual A-death. Its sign is deliberately opposite
the earlier latent-clock correction, where fast capture had to be rewarded instead.

Write Q=sum_h x_i x_j. The internal A drift is exactly

    L_int A = -2a A(A-1) - A sum_X k_X x_X + sum_h(s_h+b_h)x_i x_j.

Hence

    L_int[-epsilon A/(N+1)] <= epsilon F_0 A
                                 -epsilon b_0 Q/(N+1).        (5)

The negative second term becomes order N in the interior even when A=0. It replaces
an assumed physical activation clock by a direct joint generator estimate.

## 5. Physical immigration/death and the last seed

At core birth P increases exactly by one; at core death P decreases exactly by one.
For R>=1 decompose the core generator as

    t^(-N)L_core W = lambda(t-1)h - D A h
       +lambda*t(h_birth-h) +mu*A/t(h_death-h).

The inverse birth increment is nonpositive. The phase birth increment is also
nonpositive, because (A+1)/(N+2)>=A/(N+1). For a death with R>=2,

    (mu*A/t)[1/(P-1)-1/P] <= mu,

using A<=P and P>=2. The phase-death increment contributes at most epsilon*mu,
since [(A/(N+1))-(A-1)/N] <=1/N and A<=N. The sole inverse singularity is R=A=1,
P=1. Its destination uses the prescribed h_0=4t directly; the entire positive death
increment is at most (mu/t)h_0=4mu. This is a real seed-loss charge, not a protected
or deleted death channel.

Use h<=2 on R>=1, h>=1-epsilon>=1/2, and epsilon F_0<=D/4. Combining these facts
with (5), and enlarging the bounded core cost to

    B=2lambda(t-1)+5mu,

gives the global master estimate on R>=1:

    t^(-N)LW <= B+L_int(1/P)-D A/4-epsilon b_0 Q/(N+1).       (6)

At R=0 there are no internal moves or deaths. Birth produces A=R=P=1 and
h_birth=2-epsilon/(N+2), so exactly

    t^(-N)LW=lambda[t(2-epsilon/(N+2))-4t] <= -lambda h_0/2.   (7)

## 6. One finite geometric cover, with explicit constants

Acquire the rational cone width

    delta=min(1/4, gamma/[2(1+eta)(B+6S+1)]).                  (8)

If 1<=R<=delta N, then (3) applies. Since M/P >=1/[2(1+eta)delta], the negative
term in (3) is at least B+6S+1 in magnitude. Equation(6) therefore gives

    t^(-N)LW <= -1.                                          (9)

For the complementary region R>delta N, (2) gives L_int(1/P)<=6S/delta^2. If
A>=delta N/2, the death term in (6) is at least D delta N/8. Otherwise
A<delta N/2<=N/8, M>= (N-A)/q>=N/(2q), and U=R-A>delta N/2. Completeness again gives

    Q>=M U>=delta N^2/(4q).

For N>=1, N^2/(N+1)>=N/2. Thus the two negative terms together are at least kappa N,
where

    kappa=delta/8 * min(D,epsilon b_0/q),
    C_int=B+6S/delta^2,
    N_*=max(1,ceil((C_int+1)/kappa)).                           (10)

For R>delta N and N>=N_*, (6) is again at most -1. Since h<=2 on R>=1, (7)-(10)
prove

    LW<=-zeta W outside {N<N_*},   zeta=min(1,lambda)/2.       (11)

All joins use exact inequalities. Max-part ties occur only outside the small-seed
cone, where the global finite-jump bound is used. No compatibility of local Lyapunov
patches, undisclosed interpolation, or stopping-time occupation law is assumed.

## 7. Finite exception, recurrence and all moments

With H=4t retain the factored constant

    C_F=(zeta+lambda+mu N_*+S N_*^2) H t^(N_*+1).               (12)

The same raw rate and destination bounds used above give

    LW<=-zeta W+C_F 1_{N<N_*}.

No point in this potentially enormous count-space head is enumerated. Its size is
binomial(N_*+n-1,n). The power in (12) may remain factored.

Nonexplosion follows from N(t)<=N(0)+Poisson(lambda t). Full-orthant irreducibility
is earned by the reversible singleton paths 0->A->2A->H->A+X->X, choosing an acquired
arm for each X, and translating/concatenating these paths. Ordinary localized Dynkin
with an integrating factor gives

    E_x W(X_s)<=e^(-zeta s)W(x)+C_F(1-e^(-zeta s))/zeta.

Fatou/nonexplosion removes stopping, tight occupation averages give an invariant
probability, and irreducibility gives positive recurrence and uniqueness. Fatou on
those averages gives pi(W)<=C_F/zeta without first assuming invariant generator
domain membership. Since h>=1/2,

    pi(t^N)<=2 C_F/zeta.

Every construction terminates for any fixed finite t>1 and every strictly positive
rate vector. Thus every finite exponential stationary total-count moment exists.
The raw qualitative theorem receiver needs only finite graph/rate recognition;
materializing numerical constants is a separate operation.

## 8. Acquisition cost and exact boundary

For rational rates and rational t>1, the numerical construction consists of a fixed
number of positive rational arithmetic operations, comparisons and one ceiling,
after the finite graph and rate scans. There is no loop whose length depends on a
rate ratio, t-1, N_*, or a count-space cutoff. Under ordinary binary rational input,
these scalar outputs have polynomial bit length and can be acquired in polynomial
bit complexity; the factor t^(N_*+1) is NOT expanded. This is not a claim that the
bound is small, sharp, or useful as a numerical mixing estimate.

The complement-graph acquisition is a sufficient recognizer. It is not a complete
finder for arbitrary inventories or stable networks. A missing cross edge, a free
satellite, disconnected hub components, absent amplification, uncovered arm or
other internal channel is UNKNOWN, not instability. In particular unit-rate P4
hub networks are detailed balanced and stable by ordinary product form despite
failing this new recognizer. The earlier biclique theorem handles additional free
passenger/disconnected geometries that this fast-amplification proof does not.

Triangles are an actual new mechanism test relative to the accepted matching
inventory: its drop-two obstruction persists, yet the weighted largest-part deficit
plus an interior activation correction can succeed. All-unit triangles are already
ordinary detailed-balanced controls. An incompatible positive-rate triangle fixture
must be tested separately before attributing value; no historical novelty follows
from the old parser's rejection. General weak reversibility and arbitrary conservative
one-port dynamics remain unproved here.

## 9. Exact need for the interior energy in this template

For q>=3 put A=0 and give EVERY satellite part the same total n>=1 (one species
per part may hold that total). Every enabled hub reverse removes particles from
only two parts. At least one untouched part still has total n. Its product creates
A; an arm may also increase an untouched part. Therefore M never decreases,
Delta R<=0, and Delta P<0 on every enabled reverse jump. All internal increments
of 1/P are strictly positive. The core birth contribution for the radial-only
candidate W_rad=t^N(1+1/P) is

    lambda[(t-1)+t/(P+1)-1/P],

which is positive for all sufficiently large n. Consequently the radial-only
candidate fails a negative geometric Foster inequality along this ray for EVERY
positive rate vector and every t>1. The negative activation term in (4) contributes
order -N there and repairs this specific obstruction. This is a template statement,
not the nonexistence of all alternative Lyapunov functions or ordinary methods.

The polynomial-bit claim concerns compact rational constants and a symbolic base /
integer-exponent representation of the bound. Expanding C_F, evaluating t^N at a
binary-encoded huge N, or enumerating the finite exception is NOT polynomial-output
work in general and is not performed. Pointwise receiving can instead cancel t^N:
LW/t^N and h are rational with polynomial-size exact evaluation on binary states.
