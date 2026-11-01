# Arm-backbone stability with arbitrary amplification-only detours

**Recovered proof version; fresh independent whole review required.** Workspace
replacement destroyed the pending source after its author replay and partial
independent review. This text reconstructs the complete argument, with a NEW
hash. The old c6061f53 manifest is historical, not a binding of these bytes.
No general weak-reversibility, arbitrary one-port, novelty or source-process
clearance claim is made. All work is mathematical and non-operational.

## 1. Raw acquisition and claim

There is one species A with the sole nonconservative pair 0 <-> A, rates
lambda,mu>0. All internal reactions are reversible binary hub/active pairs.
A hub is a square-free pair of satellite species. Every hub H has 2A <-> H;
every other internal edge is A+X <-> H; every satellite X has at least one arm.
All rates are positive. These are raw-list tests, not supplied decomposition data.

Acquire B as exactly the hubs having at least one A+X arm. Acquire D as the
remaining hubs, each having ONLY its 2A amplification pair. Every satellite
retains an arm in B. Vertices absent from B's edge graph are free; all others
are rare. The B graph on its rare vertices must contain neither an induced
triangle plus an isolated vertex nor an induced P4 plus an isolated vertex.
All D edges are unrestricted: rare/rare, rare/free, free/free and arbitrary
mutual overlaps are permitted. In particular, an omitted free/free hub may
have activity of order F² and is not assumed inactive.

The assertion for this class is nonexplosion, full-orthant irreducibility,
positive recurrence and every finite exponential stationary total-count moment.
For each real t>1 we construct an explicit bounded positive multiplier h with
W=t^N h and an acquired finite Foster head. Exact code uses rational rates/t.
Qualitative raw recognition needs no enormous quantitative head materialization.

The canonical B test is sufficient, not complete. It is NOT monotone over all
old full-graph successes: deleting amplification-only edges can destroy that
older graph condition. Earlier accepted routes remain alternatives. No failed
recognition or quantitative budget refusal means instability.

## 2. Retained ordinary primitives and notation

The accepted aggregate package is retained byte-identically under
frozen_aggregate/. It includes full core profile/cover proofs and separate
independent receiving, rather than an assumed favorable Lyapunov oracle.
For completeness, the quantities used here are stated explicitly.

Let a0=sum_{B} rates(2A->H), aD=sum_{D} rates(2A->H),
BD=sum_{D} rates(H->2A), E=number of B edges, d=number of rare species,
b=min_B rates(H->2A), s=max_B(total reverse rate),
b0=min_B(total reverse rate+amplification reverse rate),
S=sum of ALL internal rate constants. For each satellite let k_X be its total
forward arm rate. Let k_- and k_+ be rare minima/maxima. When the free set is
nonempty let k=min_free k_X and ell=max_B(sum of reverse free-arm rates).
Set F_all=2(a0+aD)+max_X k_X. All are finite raw scans.

Write F=total free count, U=A+total rare count, N=F+U,
J=U+A, R=A+tau_B, where tau_B is the minimum count-weighted B vertex cover.
Thus R<=U<=J<=2U. The accepted graph test acquires tau_B without exhaustive
cover enumeration: for each anchor v its anti-neighborhood is a disjoint union
of complete bipartite components and isolates. Add the anchor weight, isolated
weights and larger shore weight in each component; maximize over anchors to
obtain MWIS. Then tau_B=rare total-MWIS. This is ordinary max-plus graph
optimization, explicitly acquired rather than provided as an oracle.

Retained cover facts are: inserting a B edge raises tau by1 or2; deletion lowers
it by1 or2; a two-drop edge has an optimal cover containing both endpoints;
Q_B=sum_B x_i x_j>=tau_B²/(4E); and in the low-inventory heavy-rare branch the
bad/good comparison is Q_bad<=2E*du*Q_good when R<=du U and heavy rare mass is
at least U/2. The exact previous proof bounds bad endpoints by R and uses the
forbidden-pattern condition. No such graph claim is made about the full graph D+B.

For a chosen beta>0 set L=lambda(t-1),
 eps=min(1,(lambda+beta)/2), c0=4(L+eps)/beta,
 K0=max(2,ceil(2c0)), g_r=1+c0/r for r>=K0,
 g_r=(lambda*t+beta*r²)/(lambda+beta*r²-eps)*g_(r+1)
       for r=K0-1,...,1; g_0=2t g_1.
All denominators are positive. With d_r=g_r-g_(r+1), the acquired profile obeys
lambda(tg_(r+1)-g_r)-beta*r²*d_r<=-eps*g_r for r>=1. Acquire finite scans
 dlow=min(c0,min_{1<=r<K0}(r+1)²d_r),
 Gratio=max(3,max_{1<=r<=K0}d_(r-1)/d_r),
 D1=max(4c0,max_{1<=r<=K0}(r+1)²d_(r-1)),
 D2=max(8c0,max_{1<=r<=K0+1}(r+1)²[g_max(0,r-2)-g_r]).
The rational tails prove the displayed bounds outside those scans. All finite
loops, arithmetic and serialization are costs, not a claimed efficient oracle.

## 3. Exact new detour channels

For a D edge with v free endpoints, v=0,1,2, its forward 2A->H changes
 A by-2, F by+v, U by-v, J by-(2+v), and R by an integer in[-2,0].
The reverse changes R by0,1,2 and J by2+v. Every reverse is nondecreasing in
both inventories. If a reverse is R-neutral, deleting its endpoints lowers
tau_B by2; an optimal cover therefore contains both endpoints at the source.
They must be rare and their count sum is<=tau_B. Its activity is<=R² (indeed
<=tau_B²/4). Thus no hidden free bulk multiplies a positive neutral phase cost.

For f_R=A/(R+1)², a reverse positive increment is<=2/(R+1)², and every forward
absolute increment is<=20/(R+1)². The forward is enabled only for A>=2, R>=A.
A reverse increasing R has profile decrease>=dlow/(R+1)², paying its phase if
rho0<=dlow/4. A neutral reverse costs at most2rho0 times its rate constant.
A forward profile costs aD*A*R*(g_max(0,R-2)-g_R); its global profile ceiling
is aD*D2. Its phase ceiling is20rho0*aD. These are not one-step approximations.

For f_J=A/(J+1)² a reverse positive increment is<=2/(J+1)²; every forward
absolute increment is<=40/(J+1)². An enabled forward has J>=2A>=4 and loses
up to4 in J. Subtraction bounds its positive numerator by2J² with denominator
at least(J-3)²; small endpoints and the negative decrement give the safe40.
This phase CAN increase: it is not dropped as favorable.

## 4. Reacquired core energy

Use beta=b/(16E) in the profile above. Put D=mu(1-1/t), Kf=a0+d*k_+, and
 rho0=min(1,b*dlow/(88s),eps/[4(11(Kf+lambda*t)+20aD+2BD)]),
 e=min(1/4,D/[4(F_all+D)],eps/(4mu)), C_A=L+11mu,
 J0=max(K0+2,4,ceil(8c0(mu+Kf+2aD+beta)/D)),
 E_r=mu(g_(r-1)/t-g_r)+Kf*r*(g_(r-1)-g_r)
       +aD*r*(g_max(0,r-2)-g_r)+2beta*r*d_r,
 Qhead=max_{1<=r<J0}(r+1)² max(E_r+e(F_all+D),0).
The added aD term follows from A(A-1)<=AR. For r>=J0, r>=4 and r>=K0+2,
 r*d_(r-1)<=2c0/r, r*(g_(r-2)-g_r)<=4c0/r,
 mu(g_(r-1)/t-g_r)<=-D+2mu*c0/r, 2beta*r*d_r<=2beta*c0/r.
Hence E_r<=-3D/4 and E_r+e(F_all+D)<=-D/2. No tail law is inferred from tests.

Set h0=g_R+rho0*A/(R+1)²-e*A/(N+1), H0=g_0+rho0/4. Then3/4<=h0<=H0.
A global scaled generator ceiling is
 C0=1+L*g_0+(Kf+sE)D1+mu*D1/4
       +11rho0(Kf+sE+lambda*t)+rho0*C_A/4+e*mu
       +aD*D2+20rho0*aD+2rho0*BD.
Here D_t h=t^(-N)L(t^N h). The old B-channel ceiling applies by its actual
channel facts: a decreasing-R rare forward consumes a species count<=R;
free captures insert a B edge and cannot lower R; bad B products are<=R²;
good amplification pays reverse phases. New increasing-R reverses pay their
own phases since rho0<=dlow/88. Neutral reverses and forward detours have the
explicit ceilings in Section3. The angular positive forward term uses FULL
F_all, including2aD; all auxiliary reverse angular contributions are favorable.

Let
 du=min(1/[2(d+1)],1/(2E),b/[8Es*Gratio]),
 zeta0=min(eps,lambda)/4,
 U0=ceil max(1,4C_A/k_-,4Qhead/(rho0*k_-)).
Then U>=U0, R<=du U implies D_t h0<=-zeta0 h0, independently of F/N.
To verify the join, heavy rare mass is>=U-(d+1)R>=U/2. The B bad/good comparison
pays bad profiles, retaining -beta(R-A)²d_R and heavy phase
-rho0*k_-*A*Hheavy/(R+1)². Split that phase to pay C_A and Qhead using U0.
The new forward profile is exactly in E_r; the constants20rho0*aD and2rho0*BD
are in rho0's acquisition. Together with11rho0(Kf+lambda*t) they are<=eps/4;
e*mu<=eps/4. The recurrence gives<=-eps*g_R/2<=-eps*h0/4, as h0<=5g_R/4.

At R=0, A=0 and B channels are inactive. Auxiliary reverses may be active,
but cannot be R-neutral (both optimal-cover endpoint counts would be zero).
Their negative profiles pay their phases. Immigration gives
lambda[t(g_1+rho0/4)-g_0]<=-lambda*g_0/4, and the angular term improves it.
Thus no new latent R=0 source is incorrectly declared absent.

For any fixed0<gamma<=1, let delta=gamma*du,
 Cint=2L+2mu+(4c0+20rho0)S/delta²+rho0(11lambda*t+C_A),
 kap=min(D*delta/4,e*b0*delta²/(32E)),
 N0(gamma)=ceil max(1,max(K0+2,4)/delta,
    4C_A/(k_-gamma),4Qhead/(rho0*k_-gamma),(Cint+1)/kap).
The SAME h0 obeys D_t h0<=-zeta0*h0 when U>=gamma N and N>=N0(gamma).
For R<=delta N the preceding heavy proof applies with heavy mass>=gamma N/2.
Otherwise all profiles are in their rational tail. Two-step profile changes are
<=4c0/R² and phase changes<=20/(R+1)². Summing ALL internal rates gives Cint,
while true death and angular amplification retain
 D_t h0<=Cint-(D/2)A-e*b0*Q_B/(N+1).
If A>=delta N/2 use death; otherwise tau_B>delta N/2 and packing gives kap*N.
Thus drift<=-1 beyond N0. In this branch h0<=7/4 and zeta0<=1/4, so this
constant bound really implies the claimed multiplicative margin. If no free
vertices exist, U=N and this is already a complete core-only Foster proof.

## 5. Acquired aggregate correction and all finite head layers

Assume free vertices exist. Set c=1 and
 rho=min(1,bc/(4s))<=c/4,
 Bbirth=2Lc+rho*L/2+rho*lambda*t,
 m=min(bc*du²/(288E),rho*k*du/36), cfree=min(lambda/2,m/2),
 eta=(C0+1)/cfree,
 K=ceil max(2,2t/(t-1),4Bbirth/m,2U0,8eta*Bbirth/zeta0).
These constants precede the head height, so there is no circular acquisition.
Let q=4t, Q=ceil(q), dgeom=q(rho+c)/(q-1), C=1+c/K+dgeom, Bhead=Q^K.
Use gJ_j=q^(K-j)C-dgeom for j<K, and1+c/j for j>=K. It is decreasing and
 gJ_j-gJ_(j+1)>=c/(j+1)²,
 2t(gJ_(j+2)+rho)<=gJ_j for j<K.
Define Z=gJ_J-1+rho*A/(J+1)²>=0. Safe bounds are
 D2mass=9C*Bhead, D4mass=25C*Bhead,
 Cfor=(a0+k_+)*D2mass+aD*(D4mass+40rho),
 Cdeath=9mu*C*Bhead/t+4rho*mu,
 CZ=C*Bhead+2c+rho/2, with Z<=CZ/(J+1).

For the four-step bound, for j>=4 through the join use
(j+1)²q^(4-j)<=25; j<4 is bounded separately by16C*Bhead. For j>=K+4 the
rational tail gives4c(j+1)²/[j(j-4)]<=32c<=25C*Bhead. All steps of size1..4
are covered. Enabled forward detours themselves have J>=4.

All B reverse phases are paid by half their amplification reserve, leaving
-bc Q_B/[2(J+1)²]. Each auxiliary reverse separately has J increase2..4,
profile loss>=c/(J+1)² and positive phase<=2rho/(J+1)². As rho<=c/4 its
remaining contribution is negative, even at J=0 and with O(F²) free/free rate.
Existing B forward phases decrease. New forward phases need not, and their40rho
cost is retained. Adverse forwards total at most Cfor*A*U/(J+1)², since
A(A-1)<=AU. Free captures are exactly J-neutral and give
-rho*A*sum_free k_X x_X/(J+1)²<=-rho*k*A*F/(J+1)².

Actual death has J decrease2. Its head and both join layers are covered by
Cdeath; its tail profile contribution is nonpositive for J>=K+2 by
K>=2t/(t-1). Its phase positive increment is<=4/(J+1)². Immigration contributes
<=-lambda/2 when J<K (the head inequality pays the tilted baseline as well),
and<=Bbirth/(J+1) when J>=K.

Acquire
 db=min(1/4,rho*k/[4(C*(9(a0+k_++mu/t)+25aD)+40rho*aD+4rho*mu+1)]),
 deltaF=db/Bhead.
Then deltaF<=rho*k/[4(Cfor+Cdeath+1)]. On U+1<=deltaF*F all positive other
forward/death costs are paid, leaving
 D_t Z<=B_J-bc Q_B/[2(J+1)²]-rho*k*A*F/[2(J+1)²],
 B_J=-lambda/2 for J<K, Bbirth/(J+1) otherwise.
If J<K this is<=-cfree. If J>=K and R>du U, either A>=du U/2 or
tau_B>du U/2. Since J+1<=3U and F>=U, capture or packing gives negative
m, while Bbirth/(J+1)<=m/4; again D_t Z<=-cfree.
Otherwise U>=J/2>=K/2>=U0 and the low-R core margin applies. In particular,
wherever D_t Z>0 in the free cone, eta D_t Z<=zeta0/4. Since h0>=3/4,
 D_t(h0+eta Z)<=-nu, nu=min(1,zeta0/2).
This complementary argument does not require Z alone to have negative drift
on all inactive rare compositions.

## 6. Exact cutoff and new cross terms

For integer z>=1 define ell_d(z)=k+(z-2^k)/2^k, k=floor(log2 z), evaluated by
bit_length and rationals. It satisfies log2 z-1<=ell_d(z)<=log2 z and step
bound2|z'-z|/min(z,z'). Set
 L0=ceil(log2(4/db))+K*ceil(log2 Q),
 Jcoef=max(1,ceil(8eta(ell*E+mu+8aD)(C+2c+rho/2)/nu)),
 Jcut=Jcoef*Bhead,
 phi=clamp((ell_d(F+1)-ell_d(U+1)-L0)/Jcut,0,1).
Then phi>0 implies the free cone. The exact product-rule cross remainder is
sum rate*t^(Delta N)*Z(destination)*Delta phi. Nonpositive increments are
safe to drop because Z>=0. Only reverse free arms, true death and forward
auxiliary detours can raise phi.

Reverse free arms have Delta F=1, Delta U=-1, Delta J=0. Their positive cutoff
step is<=4/(Jcut U), including crossings from zero; rate<=ell*E*U² and
Z(destination)<=CZ/(J+1)<=CZ/U. Their cost is<=4CZ*ell*E/Jcut.
For death, J'=J-2 and J'+1=U+A-1>=U when A>=1. Its step is<=2/(Jcut U),
so actual rate mu*A and factor1/t<=1 cost<=2CZ*mu/Jcut, conservatively4.
This includes last-copy death; the incorrect pair-profile denominator at J=2
is not used.

A forward auxiliary with v>0 has A>=2,U>=2, Delta F=v, Delta U=-v. If phi
rises, F+1>=U: otherwise the destination ratio is at most3, incompatible
with positive dyadic numerator and L0>=4. Therefore its step is<=16/(Jcut U).
At the destination J'+1=U+A-1-v>=U-1>=U/2, so Z'<=2CZ/U. Its rate is<=k_H U²,
giving cost<=32CZ*k_H/Jcut. This covers v=2,U=2 and zero/one crossings.
Reverse auxiliary detours lower the cutoff and are not adverse fast clocks.
Thus total cross<=4CZ(ell*E+mu+8aD)/Jcut and eta times this is<=nu/2.

Let ku=min(D*du/4,e*b0*du²/(32E)) and
 A1=max(1,max(K0+2,4)/du,4C_A/k_-,4Qhead/(rho0*k_-)),
 A2=[2L+2mu+rho0(11lambda*t+C_A)+1]/ku,
 A4=(4c0+20rho0)S/(du²*ku),
 Ucut=2*(2^(L0+Jcoef*Q^K+1)+1),
 Nstar=ceil(A1*Ucut+A2*Ucut²+A4*Ucut⁴+1).
This dominates Ucut and N0(1/Ucut). When phi=1 the free-cone join gives
D_t h<=-nu/2 for h=h0+eta*phi*Z. When phi<1 and N>=Nstar, dyadic comparison
implies U>=N/Ucut. The core margin applies; discard a nonpositive D_t Z, or
use eta D_t Z<=zeta0/4 if positive. Before cross cost this is<=-zeta0/2<=-nu;
after cross it is<=-nu/2. Both boundary crossings were already charged.

## 7. Receiving the stochastic conclusion

For free vertices set H=H0+eta*rho/4+eta*C*Q^K, zeta=nu/(2H).
For the core-only branch set H=H0, Nstar=N0(1), zeta=zeta0. In either case
3/4<=h<=H and L W<=-zeta W outside N<Nstar. An explicit factored finite-head
constant is CF=(zeta+lambda+mu*Nstar+S*Nstar²)*H*t^(Nstar+1).
This bounds LW+zeta W on the head, since rates are at mostlambda+mu*Nstar+
S*Nstar² and every jump changes total mass by at most1.

Internal channels conserve N; the sole increasing channel is a constant-rate
immigration. Thus N(s)<=N(0)+Poisson(lambda*s) on the standard immigration clock.
Finite-time paths stay in finite sublevels with bounded propensities, proving
nonexplosion and finite-time integrability needed for stopped Dynkin. Every
satellite has a retained B arm; 0->A->2A->H->A+X->X is a reversible singleton
path. Nonnegative translations preserve enabling, so every count state connects
to zero. Full-orthant irreducibility is earned, not inferred from diagram WR.

Localized integrating-factor Dynkin and Fatou give
E_x W(X_s)<=exp(-zeta*s)W(x)+CF/zeta. Normlikeness gives tight occupation
averages, a stationary probability and positive recurrence by irreducibility.
Fatou on these averages yields pi(W)<=CF/zeta, hence
pi(t^N)<=4CF/(3zeta)<=2CF/zeta. No stationary-generator integrability identity
is assumed. Repeat for every finite t>1; uniqueness gives the same invariant law.

## 8. Acquisition, actual arithmetic and limits

The constructor obtains the canonical B/D split, free set, max-plus inventory,
finite core profile, all constants and both factored Foster routes. Same-author
canonical receiving is NOT an independent implementation. A requested loop
budget can return UNKNOWN_CORE_PROFILE_BUDGET with qualitative admission intact.
Raw failure only excludes this sufficient finder. Finite loop budgets do not
bound all scans, rational arithmetic or serialization.

Scaled pointwise evaluation skips the mass head whenever the exact cutoff is
zero. If positive, K*ceil(log2 Q)+1 is bounded by the supplied free-count bit
length, paying all required powers relative to that explicit input. It never
expands t^N. The head reader uses capped exponentiation to compare Q^K with a
bound of order bit_length(N); it either rejects the far-tail claim immediately,
or evaluates powers whose bit lengths are bounded by the actual count input.
The executable 50-node rational DAG separately represents H,Nstar,zeta,CF and
the moment bound. Its requested power-intermediate budget may refuse expansion
while preserving the exact expression. Standard DAG, bounded-power, Foster and
max-plus methods are credited, including the prior independent aggregate reader.
Compact expressions do not imply practical tails or small numeric moment bounds.

All-unit fixtures remain ordinary detailed-balance wins. The perturbed one-hub
production control forces a²=bc, ab=bc, ac=2bc, hence b=a,c=2a and an impossible
bc=2a²=a² for positive a: not merely a hidden complex-balanced case. This does
not rule out other ordinary recurrence methods. Previous tier, Foster, queueing,
product-form, fluid and piecewise/regenerative methods receive the same raw data.
The disclosed prior denied-source alternate read remains quarantined in retained
capital; mathematical review is not source-process or historical-novelty clearance.
The general arm-carrying-detour and weak-reversibility questions remain open here.
