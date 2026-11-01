# Pending aggregate-mass correction: arbitrary free-arm target overlap

This is a separate proof draft, not part of the frozen single-free-port theorem.
It uses no new external source or stationary fiber law. No recurrence claim has
received independent review. The earlier target-cover exclusion remains correct
for that resource but need not be an obstruction for this different construction.

## 1. Raw class and the retained core

Start with the binary hub/active architecture of the frozen free-port theorem:
0<->A; every square-free A-free hub H has 2A<->H; every other internal pair is
A+X<->H; each satellite has at least one arm; all rates are strictly positive.
Acquire a nonempty set of isolated hub-graph species F_i, remove their actual
arms and coordinates, and require the residual raw core to pass the admitted
dominating-cover graph test. A sufficient finder takes ALL isolated hub-graph
vertices, so it is not handed a favorable grouping. The remaining graph need
not be complete multipartite or a disjoint union of bicliques. Every F_i may
capture into arbitrary hubs; the union of targets may contain triangles/P4s.

Let F=sum_i F_i, M=total residual rare count, U=A+M, N=F+U. Let

    R=A+tau_core,       J=2A+M=U+A.

Thus U<=J<=2U and R<=U. Every free capture A+F_i->H, and its reverse, preserves
J EXACTLY. Every hub amplification H->2A raises J by2; every reverse rare arm
H->A+X raises J by1. Their forward counterparts lower J by2 or1. Immigration
raises J by2; actual A death lowers J by2. This linear resource counts inactive
rare bulk, so Q need not control J^2. That failure is handled by the core's
low-R/U cone, not denied or supplied as an activation oracle.

Use k=min_i sum_H k_(i,H)>0. Then actual free capture intensity is at least kAF.
Use ell=max_H sum_i ell_(H,i). Reverse free-arm activity is at most ell Q.
Use b=min_H b_H>0, s=max_H(total reverse rate), E=#core hub edges, and the actual
rare forward maximum k_+. All aggregate inequalities keep arbitrary positive
rate ratios; no equilibrium of the free composition is assumed.

## 2. What is reused, and the additional low-inventory observation

The frozen one-hub proof's Section B only used that free captures insert a core
edge and therefore cannot decrease R. Its estimates extend to the summed free
capture intensity, with F_all using the maximum of ALL species' forward totals,
and s,S including every actual channel. Let h0, C0,H0,zeta0, rho0, Qhead, C_A,
K0 and delta_unit be its explicitly acquired quantities. Then

    3/4<=h0<=H0,
    D_t h0:=t^(-N)L(t^N h0)<=C0.

The same h0 has the global away-free-cone Foster estimate at N>=N0(gamma),
U>=gamma N, with zeta0 independent of gamma. These are to be rechecked on the
new raw parser, not inherited from a successful call to the old one-hub parser.

The transfer of the core inequalities uses explicit channel facts, not recognition
by the old one-free parser. Every core cover hits an inserted hub edge, so each
free capture changes tau by1 or2, hence changes R by0 or1 and decreases the
positive A/(R+1)^2 phase. Every reverse free arm is already one of the all-hub
reverse rates charged in s and in the bad/good hub comparison; summing several
such arms adds no new jump type. A rare forward that lowers R must consume a
rare species whose count is<=R, retaining the Kf*A*R bound. Every heavy rare
capture is nondecreasing in R and supplies its same negative phase increment.
Finally the negative angular term uses F_all=2a+max_X k_X over ALL free and rare
species, so no additional free-forward angular cost has been omitted. These
facts are exactly the new raw-family checks needed to reuse Section B's estimates.

More importantly, define delta=delta_unit and

    U0=ceil max(1,4C_A/k_-,4Qhead/(rho0 k_-)).

The LOW-INVENTORY half of Section B proves directly

    U>=U0, R<=delta U  ==>  D_t h0<=-zeta0 h0.       (L)

Indeed the heavy rare mass is >=U-(d+1)R>=U/2; the bad/good hub comparison uses
R/U<=delta; heavy rare capture pays the two head costs once U>=U0. Neither the
argument nor its conclusion requires U/N bounded away from0. The R=0 birth
calculation is negative without the U threshold. This is not the full core
Foster theorem with gamma secretly set to the state-dependent U/N: it is the
explicit first branch of that proof, stated and checked separately.

## 3. Choose tail constants BEFORE choosing the finite profile

Fix any t>1, L=lambda(t-1), and c=1 (any fixed positive c also works). Choose

    rho=min(1, b*c/(4s)),
    B=2Lc+rho L/2+rho lambda t,
    m=min(b*c*delta^2/(288E), rho*k*delta/36),
    cfree=min(lambda/2,m/2),
    eta=(C0+1)/cfree.

These constants depend only on the acquired core constants and raw rates, not on
the still-unconstructed finite profile. Choose an integer K>=2 with

    K>=2t/(t-1),
    K>=4B/m,
    K>=2U0,
    K>=8eta B/zeta0.

This order is essential: no profile-head amplitude appears in the condition
that chooses its own length. Quantitative cost can still be enormous and must
be charged. A qualitative certificate need not materialize the profile.

For j>=K set g_j=1+c/j. For j=K-1,...,0 set

    g_j=max( 2t*(g_(j+2)+rho), g_(j+1)+c/(j+1)^2 ).       (P)

All values are obtained by a finite rational backward recurrence; g_(K+1) is
already a tail value. Then g is decreasing to1 and

    g_j-g_(j+1)>=c/(j+1)^2,
    g_j-g_(j+2)>=c/(j+1)^2                            (j>=0).

For tail j the first inequality is immediate from c/[j(j+1)]. At j=0 the finite
head inequality is literal; no tail formula is used at0. Define

    Z=g_J-1+rho A/(J+1)^2 >=0.

Acquire a finite C_Z with Z<=C_Z/(J+1), for example the maximum of2c+rho/2 and
(j+1)(g_j-1)+rho*j/[2(j+1)] over0<=j<K. The limiting baseline is exactly0.

## 4. Full physical-time channel bounds

Write f=A/(J+1)^2. Every reverse internal channel has positive Delta f at most
2/(J+1)^2. Amplification has negative g drift at least
-b_H x_u x_v c/(J+1)^2. Since rho<=bc/(4s), summing EVERY reverse channel leaves

    reverse contribution <=-bc Q/[2(J+1)^2].             (R)

This includes all reverse free arms; they preserve J and increase A by1. No
independent-packet or favorable target premise is used.

Every forward internal channel DECREASES f. For a rare capture (A,J)->(A-1,J-1),
the numerator of f_new-f is A(2J+1)-(J+1)^2<0 because2A<=J. For amplification
(A,J)->(A-2,J-2), the numerator is4AJ-2(J+1)^2<0. Free captures preserve J and
therefore contribute exactly -rho*A*sum_i k_i F_i/(J+1)^2, at most

    -rho k A F/(J+1)^2.                                 (F)

The other forward g cost is at most Cfor A U/(J+1)^2, where

    D2=max(8c, max_(1<=j<=K+1)(j+1)^2
                         [g_max(0,j-2)-g_j]),
    Cfor=(a+k_+)D2.

The finite scan includes the head/tail joins. For j>=K+2, the tail two-step
bound uses2c(j+1)^2/[j(j-2)]<=8c.

For immigration, when J<K, recurrence(P) gives the entire tilted Z increment
at most-lambda*g_J/2-L<=-lambda/2. Indeed the destination phase is<=rho, so
2t(g_(J+2)+rho)<=g_J pays it, and the subtracted baseline contributes1-t.
For J>=K, birth is at most

    B/(J+1),

using g_(J+2)<=g_J, c/J<=2c/(J+1), A<=J/2, and
f(A+1,J+2)<=f(A,J)+1/(J+1)^2.

Actual death has rate mu A and tilted g contribution

    mu A [ (g_(J-2)-1)/t - (g_J-1) ].

For J>=K+2 this is nonpositive by K>=2t/(t-1). For2<=J<=K+1 it is bounded by a
finite acquired coefficient. The phase increment is at most4/(J+1)^2, because
f(A-1,J-2)-f(A,J) has numerator4AJ-(J+1)^2<=J^2 and J>=2. Therefore set

    Cdeath=4rho mu + max_(2<=j<=K+1) mu(j+1)^2
                  max((g_(j-2)-1)/t-(g_j-1),0).

This pays real last-copy death and both head/tail join layers. Set

    deltaF=min(1/4,rho*k/[4(Cfor+Cdeath+1)]).

On U+1<=deltaF F, the other forwards and every positive death contribution
consume at most one quarter of the negative free-capture phase drift. Dropping
another quarter gives the convenient exact bound

    D_t Z <= B_J -bc Q/[2(J+1)^2]
                       -rho k A F/[2(J+1)^2],            (Z)

where B_J=-lambda/2 if J<K, and B/(J+1) otherwise. All rates, tilted baselines,
finite head values, and failed activation states are accounted for.

## 5. Complementary activation, not uniform activity

If R>delta U and J>=K, split on A. If A>=delta U/2, then J+1<=3U and F>=U imply
the surviving capture term in(Z) is at most-rho*k*delta/36. Otherwise

tau=R-A>delta U/2, and the ordinary cover packing bound gives
Q>=tau^2/(4E)>delta^2 U^2/(16E). The surviving reverse term is at most
-bc delta^2/(288E). Thus (Z) and K>=4B/m yield D_t Z<=-cfree.
For J<K, (Z) yields D_t Z<=-lambda/2<=-cfree regardless of R.

The only remaining case has J>=K and R<=delta U. Here U>=J/2>=K/2>=U0, so(L)
applies, while eta D_t Z<=eta B/(U+1)<=zeta0/4. Consequently throughout the
free cone, combining both energies gives

    D_t(h0+eta Z)<=-nu,
    nu=min(1,zeta0/2)>0.                                 (G)

The same argument also records a fact useful in a partial cutoff region:
wherever D_t Z>0 in the free cone, eta D_t Z<=zeta0/4.
This is why requiring Z alone to have uniform negative drift would have been
an unnecessary and costly oracle. Inactive rare mass is paid by the core, while
active rare mass is paid by the linear resource's amplification.

## 6. Exact cutoff and global join

Use the frozen exact dyadic ell and

    phi=clamp((ell(F+1)-ell(U+1)-L0)/Jcut,0,1),
    L0>=ceil(log2(4/deltaF)).

Then phi>0 implies U+1<=deltaF F. On any reverse free arm, J is unchanged,
U decreases1, and F increases1. Its positive cutoff increment is<=4/(Jcut U).
The total rate is<=ell Q<=ell E U^2, and the destination Z<=C_Z/(J+1)<=C_Z/U.
Thus its aggregate cross cost is<=4C_Z ell E/Jcut. Actual A death has J->J-2
and contributes<=4C_Z mu/Jcut. Every other cutoff increment is nonpositive or0.
Acquire

    Ccross=4C_Z(ell E+mu),
    Jcut=max(1,ceil(2eta Ccross/nu)),
    Bcut=2^(L0+Jcut+1), gamma=1/[2(Bcut+1)].

For phi=1, (G) and the cross bound give drift<=-nu/2. For phi<1 beyond the same
factored global head N>=max(2(Bcut+1),N0(gamma)), the full core away-cone bound
applies. A nonpositive D_t Z can be discarded. If D_t Z>0 and phi>0, the bound
eta D_t Z<=zeta0/4 leaves core-plus-correction drift<=-zeta0/2<=-nu. Thus the
cross bound again leaves<=-nu/2. This argument includes jumps across phi=0,1.

Since h=h0+eta phi Z is between3/4 and
H=H0+eta(g_0-1+rho/4), the formal Foster rate is nu/(2H). The same explicit
factored head, finite-head rate ceiling, Poisson nonexplosion argument, reversible
singleton paths, and localized Foster/Fatou receiver then yield recurrence and
all finite exponential stationary total-count moments FOR THIS RAW CLASS.
The derivation and generalized raw code still need independent checking.

## 7. Costs, ordinary comparators, and limitations

The raw graph/circuit acquisition is finite. The new backward mass head costs K
rational steps, followed by O(K) scans; its coefficient growth and full serialized
size are not hidden under a largest-scalar statistic. The later cutoff power may
have an enormous exponent and is kept factored, with a distinct expansion budget.
The order tail constants -> K -> finite head -> deltaF -> cutoff is acyclic.
No practical efficiency, general one-port theorem, general WR theorem, historical
novelty, macroscopic recovery-time law, or operational chemistry is established.
Ordinary Foster, piecewise Lyapunov, angular/resource and fluid-with-regeneration
methods receive the same raw information; no claim excludes them. Leading fluid
limits can erase finite seeding, but that observation is not a proof of their
inadequacy under stronger boundary analysis.

## 8. Closed geometric head instead of an impossible unrolled scan

For the first arbitrary-target triangle fixture at t=2, the actual acquired plan
has K=29,729,394,962,313,506,647. It is NOT materialized. The following alternative
has the same inequalities and makes head acquisition an explicit factored formula.
Set q=4t, d=q(rho+c)/(q-1), C=1+c/K+d. Replace(P) by

    g_j=q^(K-j) C-d              (0<=j<K),
    g_j=1+c/j                    (j>=K).

The head obeys g_j=q(g_(j+1)+rho+c), including j=K-1. Hence it satisfies both
inequalities in(P), with room to spare. Head powers remain factored unless their
requested expansion budget is actually paid. Let Q=ceil(q), and Bhead=Q^K.
The monotonic ratios (j+1)q^(-j)<=1 and
(j+1)^2 q^(2-j)<=9 for j>=2 prove the explicit scan replacements

    D2=9C Bhead,
    Cdeath=9mu C Bhead/t+4rho mu,
    C_Z=C Bhead+2c+rho/2.

Here c=1 and K>=2 ensure the D2 bound also dominates the rational tail8c.
For j=1 its separate two-step estimate is4C Bhead<=9C Bhead. No claim about a
finite head is being inferred solely from sample evaluation.

Set

    delta_base=min(1/4, rho*k /
              [4(9C(a+k_++mu/t)+4rho mu+1)]),
    deltaF=delta_base/Bhead,
    L0=ceil(log2(4/delta_base))+K ceil(log2 Q),
    Jcoef=max(1,ceil(8eta(ell E+mu)(C+2c+rho/2)/nu)),
    Jcut=Jcoef Bhead.

These factored quantities satisfy all earlier cone and cross inequalities.
Jcut is an integer without expanding Bhead. The outer cutoff exponent is now
L0+Jcoef Q^K+1, and the factored Nstar is a polynomial in2 times one plus2 to
that exponent. The representation is nested but finite, not a numerical tail
bound of polynomial bit length. A requested expanded power, profile value,
head or stationary-moment constant must pay its own output/arithmetic cost.
Pointwise phi=0 can be decided before evaluating any mass-head power whenever
its numerator is nonpositive. This shortcut is an exact expression simplification,
not an assertion that an enormous global-tail region has been tested.

## 9. Strictly beyond target-cover compatibility

A triangle core with every free species capturing into all three hub edges is
admitted by this aggregate construction but excluded by the uniform target-cover
single-deletion criterion. With all rates1 except one reverse A+X leaf rate2,
complex balance is impossible: leaf balance removes all rare-arm net flows;
the remaining symmetric connected graph on2A, the three hubs and free-arm
complexes has equal positive node monomials. Hub products then force all three
rare concentrations equal A, contradicting the perturbed leaf equation.
The all-unit version remains an ordinary detailed-balance control, not evidence
of a new stability result. No prior-method exclusion is inferred from the old
parser's refusal.
