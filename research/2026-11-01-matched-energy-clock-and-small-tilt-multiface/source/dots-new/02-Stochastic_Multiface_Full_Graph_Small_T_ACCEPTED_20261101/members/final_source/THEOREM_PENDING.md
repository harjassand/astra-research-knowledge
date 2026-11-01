# Pending complete small-tilt multiface Foster construction

**Author construction, not independently accepted.** Pure mathematical count chains.
This aims to prove positive recurrence and one acquired nonzero exponential total-
count moment for the FULL square-free reversible binary one-port hub architecture,
with no graph restriction. It does **not** claim every exponential moment, arbitrary
weak reversibility, historical novelty, or source-process clearance. Ordinary source
aggregation, completely monotone profiles, finite subset elimination, an inactive-
state correction and Foster receiving are the components.

## 1. Raw data and finite acquisition

Species are A and n>=2 satellites. The sole nonconservative pair is 0<->A,
rates lambda,mu>0. Every square-free satellite hub e={i,j} has 2A<->i+j;
all other internal reactions are reversible A+i<->e. Each satellite has at
least one forward arm. All rates are positive rational. Every internal reaction
conserves total count N. Let E>=1 be the number of distinct hubs, Q=sum_e x_i x_j,
a=sum amplification-forward rates, k_i=sum forward A+i arm rates,
kmin=min_i k_i, kmax=max_i k_i, b=min amplification-reverse rate,
s=max_e(sum of ALL reverse outgoing rates at e).

Enumerate the nonempty independent satellite sets I, at most 2^n-1 masks.
All operations below are finite exact rational/integer arithmetic; no polynomial
complexity is claimed. Repeated channels are first combined by identical source
and destination. Define

 M=max(2,ceil(12s/b)), q=1+1/M, aW=2M, W=2M+2, s0=M.

(This is the general local source lemma with fixed L=2.)
For I, let Near(I) be its neighbors, Far(I) the remaining satellites, and put

 U_I=A+sum_{outside I}x_i, F_I=sum_I x_i,
 J_I=2M A+(2M+2) NearMass+(M+1) FarMass.

Then U_I<=J_I<=W U_I. At each A+i source with i in I every arm increases J_I
by at least 2. A hub with exactly one I endpoint, or with both endpoints Far,
has source weight 2M+2. Its amplification raises J_I by 2M-2>=M, while only
reverse arms to I can lower J_I, and then only by 2. Its source gap at q
is at least b/4: q^M>=2 makes the amplification contribution at least b/2,
while s(q^2-1)<=5s/(2M)<=5b/24<b/4 bounds all adverse reverse arms.
Set

 g=kmin*(1-q^-2)/(q-1), h=b/[4(q-1)],
 Cstep=(4M+4)*3^6,
 CA=Cstep*(a+kmax)+18mu M, CH=Cstep*s.

For j>=0 define the HEAD-FREE rational tail and its difference

 Z_j=(1-q^(-(j+s0)))/(j+s0), D_j=Z_j-Z_(j+1).

Its integral representation is Z_j=integral_[1/q,1] z^(j+s0-1) dz. The source-
group convexity argument gives selected-source drift at most -g D_j for each
unit A*F_I, and -h D_j for each unit selected-hub product. All jumps have
|Delta J_I|<=4M+4; the bound |z^Delta-1|<=Cstep(1-z) on [1/q,1]
charges every unselected reaction. True death, including last-copy death, costs
at most 18mu M A D_j, since q^(2M)<9. For every 1<t<=2,

 D_t Z_I <=lambda(t-1)Z_I-r_I
           +CA A(U_I+1)D_I+CH Qbad_I D_I,                    (1)
 r_I=[g A F_I+h(Qcross_I+Qfar_I)]D_I.

Here D_t f=t^-N L(t^N f), Qcross contains I--Near hubs, Qfar Far--Far hubs,
and Qbad is exactly the remaining hub set: outside I with at least one Near
endpoint. The negative physical-death baseline was safely discarded. The
immigration bound uses Z_(J+aW)<=Z_J, not a favorable birth head.

Useful uniform bounds, proved by the same integral, are

 0<Z_j<=1/(j+1),
 1/[8(j+s0+1)^2]<=D_j<=1/(j+1)^2.

The lower bound follows by integrating [1-1/(j+s0+1),1], a subset of [1/q,1],
and using z^(j+s0-1)>=1/4. Therefore with

 d=1/[8(W+s0+1)^2],
 d/(U_I+1)^2<=D_I<=1/(U_I+1)^2.                           (2)

## 2. Global subset elimination: no cutoff, no max of profiles

Acquire the integer T and constants

 T=max(1,ceil(4CA/g),ceil(4CH E/h)),
 B=1+nT, R=(B+1)^2/d,
 K=max(2,ceil(4*2^n*CH*R/h)),
 w_I=K^(n-|I|), P=sum_I w_I, Psi=sum_I w_I Z_(J_I).

Thus 0<Psi<=P. At a state, define I_large={i in I:x_i>=T(U_I+1)}.
This is an analysis partition; the actual function Psi has NO state-dependent
weights, selectors or cutoffs.

If I_large is nonempty, AF_I>=T A(U_I+1), paying the CA term with <=g AF_I/4.
A bad hub having an endpoint v neighboring I_large can be charged to one
cross hub {i,v}, i in I_large: its product is at most x_v U_I<=x_i x_v/T.
At most E bad hubs charge any chosen cross hub, so these costs consume at most
h Qcross_I/4. Every remaining bad hub has both endpoints Far(I_large), and is
therefore a selected far/far hub for I_large. Such a remainder is empty when
I_large=I. If J=I_large is a proper nonempty subset, then

 U_J<=U_I+nT(U_I+1)<=B(U_I+1), hence D_I<=R D_J.

Consequently (1) is bounded by its birth term minus 3r_I/4 plus
CH R Qfar_J D_J. This transfer is to a STRICTLY smaller independent set.

If I_large is empty, N<=B(U_I+1), so the adverse remainder in (1) is at most

 CA(B+1) A/(N+1)+CH(B+1)^2 Q/(N+1)^2,

while retaining at least 3r_I/4. This is the terminal case, not a discarded face.
For each receiving J, there are at most 2^n strict supersets, each with
w_I<=w_J/K. Thus all transfers into J cost at most w_J r_J/4. Summing proves

 D_t Psi <=lambda(t-1)Psi -S/2
           +RA A/(N+1)+RQ Q/(N+1)^2,                     (3)
 S=sum_I w_I r_I, RA=P CA(B+1), RQ=P CH(B+1)^2.

Equation (3) is a SINGLE GLOBAL generator inequality on actual states. Inactive
Far populations and arbitrarily separated bulk scales have not been dropped.
No max/min generator rule or stationary fiber law occurs.

## 3. Acquired activation cover, and the deliberately SMALL tilt

The separately proved finite prefix-gap selector applies to every graph. Take

 delta=1/4, eta=delta/(4n), hh=eta^(n-1)/(2n),
 epsC=min(1/4,hh^2/2,hh/8), gamma=delta*hh/8.

At any N>0 it returns either A>gamma N, an edge with both endpoints>gamma N,
or an independent I with U_I=0 or

 A F_I+Qcross_I+Qfar_I >=epsC U_I^2.

For completeness: sort satellite counts and stop at the first ratio gap <=eta;
its minimum is >=hh N if A<=gamma N. An edge in this prefix is the second
alternative. Otherwise it is independent and U<=delta min_I. If activation
fails, A+Near<epsC delta U, so FarMass>U/2. Apply the same prefix-gap operation
to Far. Its minimum is >=hh U, and epsC<hh^2 forbids an edge in that prefix.
Adding it to I preserves independence and U'<=3delta min_new/8. Each failure
adds a vertex, so <=n stages terminate. This is a charged selector, not an oracle.

Define the inactive set Z0={A=0,Q=0}. If the state is active and the selector
returns a face, U_I cannot be zero. Since counts are integers, U_I>=1; (2) gives

 S>=sstar, sstar=min(g,h)*d*epsC/4>0.                       (4)

No uniform bound is asserted for any fixed chosen face. All faces occur in Psi.

Choose, only AFTER P and sstar are acquired,

 Cbirth=lambda(1+P)+mu^2/4,
 eps=min(1,sstar/(16 Cbirth)), t=1+eps,
 D=mu*(1-1/t), F=2a+kmax,
 e=min(1/4,D/[4(F+1)]), H=1+eps(1+P).

This is why no enormous birth head is needed: the tilt is acquired small enough
rather than taking arbitrary prescribed t. All constants preceding eps are
independent of eps. This construction does not yet give all finite t moments.

## 4. Baseline and the inactive-state correction

Let B0=1-e A/(N+1). Then 3/4<=B0<=1. Sourcewise calculation yields

 D_t B0<=lambda eps+e mu -(D/2)A-2eb Q/(N+1).              (5)

Indeed tilted death's negative baseline is at least -(1-e)DA; the positive
last-copy angular change is <=e mu. Internal A-decreasing channels cost at most
e F A, while each reverse amplification gives -2eb x_i x_j/(N+1).
Immigration's angular increment is nonpositive. The chosen e leaves >=D/2.
Also e mu<=mu^2 eps/4.

Set the bounded positive multiplier

 h(x)=B0(x)+Psi(x)+H 1_Z0(x),  3/4<=h<=1+P+H.

An INTERNAL transition can never enter Z0: its target is either 2A, A+i, or a
hub, all active. No internal transition leaves Z0 because all its binary sources
are disabled. Immigration always leaves Z0. Its drift there is

 D_t h <=lambda[eps(1+P)-H]=-lambda.

The only adverse entrance to Z0 is a true death from A=1 with independent
satellite support. At that state, take I to be the support of all positive
satellites (nonempty for N>=2). Then J_I=aW, AF_I=N-1, and

 S>=g(N-1)D_(aW).

Thus the indicator's entire tilted cost mu H/t is paid by S/4 once
N>=1+4mu H/[g D_(aW)]. This explicitly pays the last-copy event, not a seed-only
excursion argument.

Choose an integer Nstar>=2 satisfying

 Nstar>=4RA/D,
 Nstar>=RQ/(eb),
 Nstar>=1+4mu H/[g dA], where dA=1/[8(aW+s0+1)^2]<=D_(aW),
 Nstar>=4(Cbirth*eps+1)/(D gamma),
 Nstar>=2(Cbirth*eps+1)/(eb gamma^2).

For N>=Nstar, combining (3)--(5), absorbing residuals and the indicator entrance,
gives on active states

 D_t h<=eps Cbirth -(D/4)A-eb Q/(N+1)-S/4.                 (6)

In the face alternative this is <=-3sstar/16. In either interior alternative,
the corresponding negative term is >=eps Cbirth+1. On inactive states the
drift is <=-lambda. Hence, with nu=min(lambda,1,sstar/8)>0,

 D_t h<=-nu, N>=Nstar.                                  (7)

All finite counts, waiting, deaths, reverse redistributions and boundary states
are included pointwise. There is no assumed fast clock or ignored failed search.

## 5. Stochastic receiving and finite representation cost

Put Htot=1+P+H, Wfun=t^N h, zeta=nu/Htot. Then LWfun<=-zeta Wfun outside
the finite head N<Nstar. If Srate is the sum of all internal rate constants,
a safe explicit head constant is

 CF=(zeta+lambda+mu Nstar+Srate Nstar^2)*Htot*t^(Nstar+1).

Internal channels conserve N, and the only upward-N channel is constant-rate
immigration. Thus N(s)<=N(0)+Poisson(lambda s); finite-time paths remain in finite
sublevels with bounded rates. This proves nonexplosion and finite-time moment
bounds for stopped Dynkin. Every satellite i has a reversible singleton path
0->A->2A->hub->A+i->i. Nonnegative translations preserve enabling; all count
states communicate with zero. Irreducibility is therefore acquired explicitly.

Localized integrating-factor Dynkin and Fatou give
E_x Wfun(X_s)<=exp(-zeta s)Wfun(x)+CF/zeta. Normlikeness gives tight occupation
averages and an invariant probability; irreducibility gives positive recurrence
and uniqueness. Fatou on occupation averages yields pi(Wfun)<=CF/zeta, hence
pi(t^N)<=4CF/(3zeta). This is one explicit nonzero exponential moment.

A requested power/bit budget may refuse expansion without disproving the theorem.
2^n subset enumeration, graph scans, rational operations, K^(n-|I|), the finite
head integer, and t^(Nstar+1) all have real costs. Factored integer-power DAGs
represent the final constants exactly; compact representation is not practical
numerical size. A budget refusal is UNKNOWN_COMPUTATION, never instability.
