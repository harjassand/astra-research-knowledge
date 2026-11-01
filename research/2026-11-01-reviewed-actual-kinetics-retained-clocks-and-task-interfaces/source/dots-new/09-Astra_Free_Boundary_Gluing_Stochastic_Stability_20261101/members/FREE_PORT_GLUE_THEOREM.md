# Dyadic gluing across a free-port extinction boundary

**Author-verified ordinary proof candidate; independent review pending.** This is
separate from the finite-layer lemma and every previously accepted archive. The
implementation and exact component checks are retained, but no independent
acceptance, general-WR, or historical-novelty conclusion is being claimed.

## Target raw class

One open species A has0<->A. Internal channels are the reversible binary hub/2A/arm
architecture. There is a satellite F absent from every hub, with EXACTLY ONE arm
A+F<->H0, where H0=B+C. Remove F from the hub graph; the remaining graph satisfies
the accepted dominating-cover condition. All its satellites have arms, every hub
has amplification, and all rates are arbitrary positive. F is acquired by trying
the finitely many isolated satellites and checking its unique arm/core graph; no
good F or hub is supplied as an oracle.

Notation: M=sum of all rare (non-A, non-F) counts, U=A+M, N=F+U. Let d be the number
of rare species, E>=1 the core hub count, a the sum of 2A->hub rates, k_- and k_+
the minimum/maximum forward arm totals on rare satellites, k_F the sole forward
F-arm rate and ell_F its reverse rate. Let b_-=min hub->2A rates, s_+=max total
reverse hub rates, b0=min_h(s_h+b_h), S=sum internal constants, and
F_all=2a+max(k_+,k_F). The core weighted-cover inventory is R=A+tau_Grare.
The protected capture-pair inventory is P=A+min(B,C). Always P<=R<=U.

The constructed global function is

    W=t^N [h0 + eta phi Z],
    h0=g0_R+rho0 A/(R+1)^2-e A/(N+1),
    Z=gF_P-1+rhoF A/(P+1)^2 >=0.

The two profiles are acquired finite backward heads with rational tails. A dyadic
logarithmic cutoff phi is compiled below. It is not a stationary fiber law.

## A. Common one-dimensional profile constructor

For a specified beta>0 and requested t>1 define L=lambda(t-1),

    eps=min(1,(lambda+beta)/2), c=4(L+eps)/beta,
    K=max(2,ceil(2c)),
    g_r=1+c/r for r>=K,
    g_r=(lambda*t+beta*r^2)/(lambda+beta*r^2-eps)*g_(r+1)
       backwards for r=K-1,...,1; g_0=2t g_1.

Let d_r=g_r-g_(r+1)>0. The accepted elementary recurrence proof gives

    lambda(tg_(r+1)-g_r)-beta r^2 d_r <= -eps g_r, r>=1.

Acquire the following finite constants, with displayed tail bounds:

    dlow=min(c,min_(1<=r<K)(r+1)^2 d_r),
    Gratio=max(3,max_(1<=r<=K)d_(r-1)/d_r),
    D1=max(4c,max_(1<=r<=K)(r+1)^2 d_(r-1)),
    D2=max(8c,max_(1<=r<=K+1)(r+1)^2[g_max(0,r-2)-g_r]).

Thus d_r>=dlow/(r+1)^2; d_(r-1)<=D1/(r+1)^2 and the worst two-step profile
decrease is <=D2/(r+1)^2. The D2 tail uses
2c(r+1)^2/[r(r-2)]<=8c for r>=K+2>=4. All scans and rational bit growth cost work.

## B. A core energy with a global ceiling and a uniform away-cone margin

Construct g0 with beta0=b_-/(16E). Put Kf=a+d k_+, D=mu(1-1/t), and

    rho0=min(1,b_- dlow0/(88s_+),eps0/[44(Kf+lambda*t)]),
    e=min(1/4,D/[4(F_all+D)],eps0/(4mu)),
    C_A=L+11mu,
    J0=max(K0+1,2,ceil(4c0(mu+Kf+beta0)/D)),
    Er=mu(g0_(r-1)/t-g0_r)+Kf r d0_(r-1)+2beta0 r d0_r,
    Qhead=max_(1<=r<J0)(r+1)^2 max(Er+e(F_all+D),0).

For f=A/(R+1)^2, every internal |Delta f|<=11/(R+1)^2. A nondecreasing-R
forward arm decreases f. F is in no core cover, so A+F->H0 cannot decrease R;
its f drift is negative and may be dropped in the partial-cone argument.
R-decreasing rare forward rates are <=Kf A R. Bad hub products are bounded
GLOBALLY by E R^2, because both endpoints of any optimal-cover witness have count
<=tau<=R. Good hub amplification is negative; rho0 absorbs its positive phase
cost globally. This yields a finite GLOBAL ceiling

    t^(-N)L(t^N h0)<=C0,

where a safe explicit choice is1 plus

    L*g0_0 +(Kf+s_+E)D1_0 +mu D1_0/4
       +11rho0(Kf+s_+E+lambda*t)+rho0 C_A/4+e mu.             (B1)

The physical death term -D A is retained to pay e(F_all+D)A. At R=0 all internal
sources vanish and the exact birth computation is negative, so (B1) still holds.
Always3/4<=h0<=H0=g0_0+rho0/4.

For EVERY fixed rational0<gamma<=1, the SAME h0 has a Foster margin whenever
U>=gamma N and N is sufficiently large. Its function does not depend on gamma.
Acquire

    delta_gamma=min(gamma/[2(d+1)],gamma/(2E),
                    gamma b_-/[8E s_+ Gratio0]).

If1<=R<=delta_gamma N, heavy R-exceeding rare vertices have total
H>=U-(d+1)R>=gamma N/2. Core graph domination gives
Q_bad<=2E delta_gamma Q_good/gamma. One quarter of good amplification pays bad
profile drift; one quarter pays reverse phase drift. The remaining half gives
-beta0(R-A)^2 d_R. Heavy rare captures give
-rho0 k_- A H/(R+1)^2. Their half pays the positive phase-core A term once
N>=4C_A/(k_-gamma), and their remainder pays the finite Er head once
N>=4Qhead/(rho0 k_-gamma). The tail Er+e(F_all+D)<=-D/4 needs no oracle.
The two constant costs11rho0(Kf+lambda*t) and e mu are each<=eps0/4. Hence
scaled drift<=-eps0 g0_R/2 and thus L(t^Nh0)<=-eps0 t^Nh0/4.

If R>delta_gamma N and N>=K0/delta_gamma, the rational tail gives

    t^(-N)L(t^Nh0)
       <=Cint_gamma -(D/2)A-e b0 Q/(N+1),
    Cint_gamma=2L+2mu+(2c0+11rho0)S/delta_gamma^2
                         +rho0(11lambda*t+C_A).

The elementary packing bound Q>=tau^2/(4E) gives linear restoration with

    kap_gamma=min(D delta_gamma/4,e b0 delta_gamma^2/(32E)).

The exact R=0 birth bound gives -lambda g0_0/4. Therefore with

    zeta0=min(eps0,lambda)/4,
    N0(gamma)=ceil max(1,K0/delta_gamma,
       4C_A/(k_-gamma),4Qhead/(rho0 k_-gamma),
       (Cint_gamma+1)/kap_gamma),                              (B2)

one has L(t^Nh0)<=-zeta0 t^Nh0 on U>=gamma N, N>=N0(gamma).
The crucial feature is zeta0 independent of gamma. Costs may be huge as gamma
shrinks, but every inequality is acquired and finite.

## C. An earned negative correction in the free-F cone

Every hub reverse amplification raises P by1 or2. Every reverse arm preserves or
increases P; A+F->H0 preserves P exactly. Other forwards decrease P by at most2.
At P=0, A=0; any enabled hub reverse creates positive P. Unlike R=0, P=0 need NOT
freeze all internals, but those extra reverse channels improve the profile.

Construct gF with betaF=b_(H0->2A)/2. Choose

    rhoF=min(1,b_- dlowF/(4s_+),epsF/(44lambda*t)).

For fP=A/(P+1)^2 every reverse has positive increment at most2/(P+1)^2.
Every forward increment in absolute value is <=20/(P+1)^2: for P>=3 direct
subtraction gives a bound17, and P<=2 is checked from0<=fP<=1/4. Thus reverse
phase cost is absorbed by half of all amplification. The surviving H0 term is
at least betaF min(B,C)^2 d_P. Other forward rate is <=(a+k_+) A U and its
profile-plus-phase cost is <=Cfor A U/(P+1)^2, where

    Cfor=(a+k_+)(D2_F+20rhoF).

Capture A+F has exact phase drift -rhoF k_F A F/(P+1)^2. Define

    Tr=max(cF mu+2betaF cF,
       max_(1<=r<=KF)(r+1) max(
          mu(gF_(r-1)/t-gF_r)+2betaF r dF_r+D,0)),
    T=Tr+rhoF C_A,
    deltaF=min(1/4,rhoF k_F/(4Cfor),rhoF k_F/(4T)).           (C1)

The tail bound for Tr drops -D(gF_r-1) and uses
(r+1)mu d_(r-1)<=mu cF and (r+1)2betaF r d_r=2betaF cF.
If U+1<=deltaF F, half the negative capture drift pays both Cfor A U/(P+1)^2
and T A/(P+1). The physical core drift of Z equals the core drift of hF minus
lambda(t-1)-D A. The displayed Tr explicitly pays the resulting +D A; it is
NOT incorrectly discarded. The remaining phase birth constant is<=epsF/4.
Consequently for P>=1,

    t^(-N)L(t^N Z)<=-3epsF/4-L.

At P=0, every enabled reverse has negative g decrement at least d0 and phase
increase at most rhoF/4. Birth gives at most -lambda gF_0/4-L. Hence a uniform
negative correction is acquired throughout the free-F cone:

    t^(-N)L(t^N Z)<=-c_free,
    c_free=min(epsF/2,lambda gF_0/4)>0.                       (C2)

Also acquire C_Z so0<=Z<=C_Z/(P+1), for example

    C_Z=max(2cF+rhoF,
      max_(0<=r<KF)(r+1)[gF_r-1+rhoF r/(r+1)^2]).           (C3)

No infinite-fiber stationary distribution or recurrence premise entered.

## D. Exact dyadic cutoff and its paid cross-generator error

For real z>=1 define k=floor(log2 z) and

    ell(z)=k+(z-2^k)/2^k.

For integer z it is exact rational arithmetic using bit_length, not a numerical
log oracle. It is continuous, monotone, and satisfies
log2 z-1<=ell(z)<=log2 z. Its increment over an integer step is <=2/min(z,z').

Choose integer L0>=ceil(log2(4/deltaF)), and integer Jcut>=1. Set

    phi=clamp((ell(F+1)-ell(U+1)-L0)/Jcut,0,1).              (D1)

If phi>0 then U+1<=deltaF F, so (C2) applies. Only two types of jumps can raise
phi: H0->A+F, and actual A death. Every other internal leaves F,U fixed except
A+F capture, which decreases phi; immigration also decreases it.

For the exact product-rule remainder

    R_cross=sum_y rate(x,y)t^(N_y-N) Z(y)[phi(y)-phi(x)],

drop nonpositive terms. On H0->A+F, P is EXACTLY unchanged, U decreases1 and
F increases1. If the cutoff actually rises, its increment is <=4/(Jcut U);
this follows directly from the dyadic step bound and the support threshold
(the transition crossing from zero is included). Q_H0=B C<=P U, and
Z(y)<=C_Z/(P+1). This contributes at most4 C_Z ell_F/Jcut.
For A death, P decreases1 and Z(y)<=2C_Z/(P+1); the cutoff increment is
<=2/(Jcut U). Since A<=U, its contribution is at most4 C_Z mu/Jcut.
Thus, including true last-copy death,

    R_cross<=Ccross/Jcut,
    Ccross=4C_Z(ell_F+mu).                                  (D2)

This is the paid compatibility step. It uses the actual unique capture-hub flux
and a tunably slow dyadic cutoff, not an assumed favorable partition of unity.

## E. Global join and formal finite head

Choose

    eta=(C0+1)/c_free,
    Jcut=max(1,ceil(4eta Ccross/zeta0)),
    Bcut=2^(L0+Jcut+1), gamma=1/[2(Bcut+1)],
    Nstar=max(ceil(2(Bcut+1)),N0(gamma)).                     (E1)

If phi=1, (B1),(C2),(D2) give scaled drift <=-1+zeta0/4.
If phi<1 and N>=2(Bcut+1), the dyadic bounds imply
F+1<Bcut(U+1), hence U>=gamma N. Apply (B2); wherever phi>0 its own correction
term is nonpositive, and (D2) costs at most zeta0/4. Since h0>=3/4, scaled drift
is at most -zeta0/2. Both regions therefore satisfy that same conservative bound.

Let Htot=H0+eta(gF_0-1+rhoF/4). The combined h lies in[3/4,Htot]. With
zeta=zeta0/(2Htot), obtain LW<=-zeta W outside N<Nstar. The ordinary factored
finite-head bound is

    CF=(zeta+lambda+mu Nstar+S Nstar^2)Htot t^(Nstar+1).

For completeness, internal channels conserve N and the sole increasing core
channel has constant rate lambda, so N(s)<=N(0)+Poisson(lambda s). Finite-time
paths stay in finite count sublevels with bounded rates, proving nonexplosion.
Every satellite X, including F, has a reversible singleton path
0->A->2A->H->A+X->X. Nonnegative translations preserve enabling, so concatenation
constructs/removes every state and proves full-orthant irreducibility.

Stopping in finite sublevels, integrating-factor Dynkin and Fatou give
E_x W(X_s)<=exp(-zeta s)W(x)+CF/zeta. No invariant-generator integrability is
assumed. The Poisson bound and W<=Htot t^N also provide finite-time integrability,
including polynomial propensities. Normlikeness makes occupation averages tight;
the standard countable-state localization argument gives a unique invariant
probability and positive recurrence. Fatou on occupation averages yields
pi(W)<=CF/zeta. Since h>=3/4, pi(t^N)<=2CF/zeta is conservative and valid.
Repeating the construction for each finite t>1 proves all finite exponential
stationary total-count moments. Finite test values of t are not that proof.

### An explicitly factored head, and exact receiving without expanding it

The implementation replaces the max in(E1) by a conservative polynomial head.
Let delta_unit=delta_gamma/gamma and

    kap_unit=min(D delta_unit/4,e b0 delta_unit^2/(32E)).

Since0<gamma<=1, kap_gamma>=kap_unit gamma^2. Put Ucut=1/gamma=2(2^e_cut+1),
e_cut=L0+Jcut+1, and acquire rational coefficients

    A1=max(1,K0/delta_unit,4C_A/k_-,4Qhead/(rho0 k_-)),
    A2=[2L+2mu+rho0(11lambda*t+C_A)+1]/kap_unit,
    A4=(2c0+11rho0)S/(delta_unit^2 kap_unit).

Then the integer expression

    Nstar=ceil(A1 Ucut+A2 Ucut^2+A4 Ucut^4+1)

is at least both2(Bcut+1) and N0(gamma). This is an exact symbolic bound, not an
expanded binary integer or an estimated magnitude. The Foster coefficient remains
a symbolic expression using this integer and t^(Nstar+1). Fully expanding either
integer or power must pay the actual output bits.

An exact pointwise test N>=Nstar does not secretly expand an infeasible head:
Nstar>=Ucut>2^(e_cut+1), so bit_length(N)<=e_cut+1 immediately proves N<Nstar.
Otherwise e_cut is bounded by the supplied state's bit length, and expanding the
power2^e_cut and evaluating this fixed-degree polynomial costs polynomial work in
that state/certificate representation. Evaluating W's rational factor and LW/t^N
also needs only dyadic bit_length, rational arithmetic and the two finite profiles.
Actual W or a numerical stationary-moment bound remains a different output task.

The optional expansion budget caps only the intermediate power's bit count,
e_cut+1. It is not a bound on total head output, rational arithmetic or wall time;
refusal retains the explicit W and symbolic Foster formula. No complete numerical
polynomial guarantee is inferred from the compact algebraic representation.

## F. Costs, exact executions, and independent-review boundary

Raw recognition, both finite profile heads/scans, eta, Jcut and the exact dyadic
pointwise W are constructively acquired. Bcut, gamma and Nstar can be enormous.
An explicit numeric expansion must pay those bits; a retained expression such as
2^(L0+Jcut+1) is not an expanded numerical constant. A structural qualitative receiver uses this ordinary theorem as retained proof
capital; this author branch remains pending independent acceptance.
No complete numerical-polynomial or practical-tail claim is proposed.

The author executed1167 exact states and8663 enabled internal jumps,105 free-cone
negative-correction checks,135 explicit-gamma partial-core and full-negative
checks,1080 generic cutoff-bound tests with synthetic finite widths, and182 exact
factored-head receiving comparisons. Both triangle+free F and non-complex-balanced
P4+free F were used. The actual global head and actual phi=1 global-tail states
were NOT expanded/executed; the ordinary proof supplies that unbounded join.
Synthetic widths test the cutoff lemma only, not complete Foster certificates.

The main t=2 construction performs16894 profile/head loops (additional explicitly
listed finite slope scans are separate work), retains6673-bit scalars, and has
Jcut=50564677892798. Its power-of-two head intermediate requires50564677892823 bits;
a100000-power-bit expansion request is refused. This is a compact exact expression
and a pointwise W circuit, not a small numerical bound. Complete numerical
acquisition is not claimed polynomial in binary rates; profiles can already be
large, before any exponential head materialization.

Important independent-review joins are every P/R switching case, the global
ceiling(B1), the same h0 independent of gamma, the +D A correction in(C1), cutoff
crossing from phi=0, exact receiving semantics, and all actual costs. The finite-
layer lemma does not certify this construction. No accepted package or source
has been edited, and this candidate is not included in any delivery ZIP.

## G. Scope and ordinary comparisons

This is a sufficient raw family: an acquired dominating-cover core plus one
isolated satellite whose only arm returns to one acquired hub. Multiple target
hubs for that F are not covered by this proof. General one-port conservative
stability and general weak reversibility remain separate open targets here.
At unit rates ordinary detailed balance/product form may already solve instances;
those wins are not hidden by a new parser. The diagnostic triangle-plus-F rates
are all1 except CD->AD at2. Its internal complex graph is a tree, so amplification
balances imply B=C=D=A, contradicting the AD leaf equation a*d=2c*d. Thus that
fixture is not complex-balanced. The P4-plus-F fixture inherits the already
checked incompatible leaf balances from its P4 core.

The new graph has an induced forbidden core pattern plus the free F, so the
previous dominating-cover near-cone comparison genuinely fails. The proof repairs
that representation boundary using a local pair correction and an acquired
flux-compatible logarithmic cutoff. Ordinary phase correctors, Foster arguments,
finite profile recurrences, graph optimization and smooth/piecewise gluing are
components, not novel principles asserted without literature comparison. No
exhaustive prior-art or historical novelty conclusion is made.

No new source retrieval occurred. Prior source-access failures remain disclosed
and quarantined, not retroactively cleared. No publication, outreach, upload,
laboratory instruction or process design is part of this mathematical work.

### Organising stochastic-boundary interpretation (not a burst-time theorem)

At a pure-F state, all internal propensities vanish and the first actual event is
immigration with exponential waiting rate lambda. The proof does not replace it
by a uniformly fast boundary clock. Its finite cost is retained in gF_0=2t*gF_1,
the free-cone margin, and all physical generator terms. A conservative leading
population-normalized ODE started exactly on that face has no A or hub seed and
remains inactive; vanishing scaled constant immigration cannot supply one in that
direct limit. This explains why simply invoking that fluid trajectory would miss
the boundary layer. It is not a claim that strong fluid-plus-regeneration or
averaging methods, given the same raw seed information, are incapable of treating it.

The acquired bounded tilted correction pays the stochastic low-count layer before
the core's draining region controls the tail. A quantitative macroscopic recovery-
burst distribution is NOT proved here. The separate finite latent-layer sample-
clock note is unreviewed and is not used as a premise of this full pointwise proof.
