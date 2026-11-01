# Independent review: actual weak clearance-time CLT

## Finding, binding, and scope

**PASS for the stated actual-chain weak limit. No author source repair was required.**
The reviewed theorem is `ACTUAL_CLEARANCE_CLT.md`, SHA-256
`4b09204361aee3b35adceaa148fcbca560c1b07d53720c803f36f82f5d60138a`,
under author freeze `fd48100bccba41d7df3cc777fe96a717f74746bf0c52354aec0cba8dda11a022`.
The exact tail note is `c470d0c69266e8bf2ac1443474ea29608afb887d8c5c3d79584315bf4c315fdc`.
All seven frozen payloads and sixteen inherited source/review bindings match their
specified sizes and hashes. The manifest itself and all 23 bound files are
snapshotted here. Two further old interior-review files and twelve separately
scoped deterministic-parameter/receipt files are also snapshotted and bound.

This is an ordinary mathematical audit with exact algebraic corroboration, not a
proof-assistant certificate. The independent checker imports no author code.
It derives actual increments from twelve literal stoichiometric vectors, checks
polynomial identities, and proves the displayed positive-monomial bounds
universally on the stated domain using a different parameterization. Finite
small-state jump tests supplement these arguments; they do not prove asymptotics.

The accepted conclusion, as N tends to infinity through integer initial counts,
is

    [tau_clear - s_* N^(1/5)] / N^(1/10) ==> Normal(0,Sigma²),

for the actual rate-2 chain starting at `(0,N,1,1,0)` and the first actual total-count
hit `S<=15(N+2)/16`. Here

    Sigma² = integral_0^s_* b_l(l(s),e(s))²(1+3l(s)²e(s)) ds
           = integral_0^infinity b_l(l,e(l))² dl,

with the deterministic origin orbit and its remaining-time function b. No rate,
initial law, target, reference scale, or retained state is replaced. This earns
neither convergence of moments nor a finite-N approximation/error rate. The
proof controls actual hitting times on events of probability tending to one;
no finite-N bad-history duration or moment bound is asserted.

## 1. Actual model and all-channel cancellation

Fix N; it is not current population. Set T=N^(1/5),
`L=A+(C+D)/2`, `Z=C-D`, `n=A+B+C+D+E`, `h=AE`,
`a2=A(A-1)`, and `Q=L²-CD=2AL-A²+Z²/4`.

From the twelve species increments, the independent algebra recovers every
entry of the accepted jump table, including the coefficient **2** for CD→AE.
The drifts are exactly

    GL=1+A+AL+h-3A²,
    GE=a2-2h+2CD,
    Gh=-Nh+3EL²+r_h,
    r_h=E-3EQ+2ACD+A(A-1)²+2CD+h(N-B+2L+2-7A).

The last coefficient is `N-n+E+4L+2-8A`. Because 0<=A<=L,
its absolute value is at most `|n-N|+E+4L+2`; the negative A term is not
bounded by an additional unsigned 8A charge that would alter the formula.
The rate sums are exactly

    q_LL=1+A+(3/2)a2+A(C+D)/4+h,
    q_EE=a2+2h+2CD,  q_LE=-(a2+h),  sum lambda|uv|=a2+h,
    s_L=1+A+2a2+A(C+D)/2+h,
    q_hh=E²[1+A+2a2+A(C+D)+CD+AB]
          +a2(A-E-1)²+2h[(E-1)²+A²]+2CD(A+E+1)².

Only immigration/death change total, by +1/-1. With none of the stated omitted
marks before a stop, Z=0 and n-N=2+I exactly. The omitted set includes all
three 2A departures, both AC/AD returns, and death; their full actual intensity
is at most `(1+5L)A`. This is a counting-process admission cost, not a reduced
model definition. Changing CD→AE to rate CD leaves a nonzero source defect;
the checker explicitly verifies that counterfactual mismatch.

For any C² f and `q_f=f(z)+h f_l(z)/(NT)`, the exact product rule is

    Delta q_f=Delta f + Delta h f_l/(NT) + h' Delta f_l/(NT).

Consequently `G q_f=(V·Df)/T+R_f`, where `V=(1+3l²e,2l²)` and the
full R_f is the accepted formula. In particular, the `-Nh` drift cancels
`h f_l/T`, while `3EL²/(NT)=3l²e/T`. The AB/CD channels have zero slow
increment but nonzero corrected marks `+/-E f_l/(NT)`; their bracket
contribution is retained. No equilibrium or stationary fast-fiber law enters.

The source's envelope of |R_f| has, in order, charges

    |f_l|(A+2AL)/T,
    |f_e|(a2+2h+2Q)/T³,
    |f_l|H_h/(NT),
    f_ll q_LL/(2T²)+f_le sum lambda|uv|/T⁴+f_ee q_EE/(2T⁶),
    f_ll hplus s_L/(NT²)+f_le hplus q_EE/(NT⁴),

with absolute derivative envelopes, `hplus=(A+1)(E+1)`, and the stated H_h.
It requires only C², since Delta f_l is an integral of second derivatives.
The actual corrected bracket is bounded by

    2[a²q_LL+2ab sum lambda|uv|+b²q_EE]+2c²q_hh,

where `a=F10/T+hplus F20/(NT²)`, `b=F01/T³+hplus F11/(NT⁴)`,
`c=F10/(NT)`. These are the formulas used below, not a bracket of f alone.

## 2. Boundary smoothness and deterministic sensitivity

The received inverse-flow theorem gives b smooth in the positive interior,
`b_l=J_inf-1`, `|b_l|<=1`, and

    (1+3l²e)b_l+2l²b_e=-1.

The new forward-flow extension really supplies the previously missing initial
boundary domain. At every nonnegative starting point choose a sufficiently
small positive h before blow-up. Since l'>=1 and then e'>0, the image lies in
the positive interior. Smooth finite-time dependence gives a neighborhood on
which `h+b(flow_h z)` is C² and agrees with remaining time at nonnegative
points. On overlaps along the physical quadrant the functions and needed
one-sided derivatives agree, and one may choose a common small h over each
fixed compact neighborhood. Thus the physical jump segments, including segments
touching an axis, have bounded C² norms. No singular inverse formula is evaluated
at l=0. The PDE then implies b_l(0,0)=-1.

For `l>=g e²`, 0<g<=3/4, the inverse denominator along v>=e satisfies
`L(v)>=l+(3/4)(v²-e²)>=g v²`. Thus

    b(l,e)<=1/(6g²e³).

The received cone bounds are valid on whole segments with e>=1. At g=1/32,
after inserting the minimum segment e=sqrt(r)/3, their five coefficients are
exactly

    7962624/5, 41472, 6879707136/7,
    1177743753216/7, 1007952445734912/35.

Every one is strictly below D=10^14. The factor in b_ll is 3^8, not 3^7,
because its original numerator already includes 3. The final coefficient is
below 2.88*10^13. These are independently recomputed exact rationals.

## 3. Fixed-compact stopped process: occupation and admission

Fix K>=10^40 first. Every constant marked C_K is allowed to depend on this
fixed K; none is transported uniformly to a growing compact. Stop the actual
chain at L>=KT, the received E ceiling, time 3T, I>8T, the first omitted
mark, and the continuous occupation threshold Hbar=h_K/T²,
`h_K=100(K+1)²`. Include the stopping jump and its one-jump enlarged rectangle.

The stronger occupation threshold is genuinely paid. The received full-chain
A-clock estimate has drift `GA<=r-(N/4)A`, where `r=1+3K²T²`, when B>=N/2
and 2KT<=N/4. These hold eventually on the pre-omission compact state domain,
since n=N+2+I and E=O_K(T³), L=O_K(T). Its bracket cap is
`r*3T+C_A Hbar=O_K(T³)` with `C_A=N+O_K(T³)`; the positive threshold is

    N Hbar/4 - r*3T
      =[25(K+1)²-9K²]T³-3T >=16K²T³

for K>=1, T>=1. The exponential martingale bound therefore gives an
`exp(-c_K T³)` failure probability. An unamplified Markov estimate of E H
would not establish the claim, but that shortcut is not used here.

The full omitted intensity has integrated bound
`(1+5KT)h_K/T²=O_K(T^-1)`. At the first omitted mark, the stopped marked count
has expectation equal to its stopped compensator, so the mark probability is
at most this bound. Original immigration through 4T+5 is Poisson(4T+5); its
upper tail at 8T tends to zero exponentially. No proof conditions local
martingales on this future count event. The accepted finite-level theorem pays
the remaining entrance/tube failures. Hence the common stopped sigma_K equals
the actual first level hit on an event tending to one.

All pathwise polynomial estimates below are for the stopped process itself,
including a first adverse endpoint; they are not assertions conditional on
future success. At fixed K, the integrated rates satisfy

    int q_LL=O_K(T), int q_EE=O_K(T³), int q_hh=O_K(T^9),
    int |r_h|=O_K(T^4), sup h=O_K(T^4).

The full residual is O_K(T^-1), the corrected bracket O_K(T^-1), and each
corrected jump O_K(T^-1). The independent power ledger proves these exponents
with arbitrary fixed positive compact constants, retaining every product term.

## 4. Actual averaging and compact covariance identification

Integrate the exact Gh identity, with the stopped h-martingale M_h:

    (int h - int 3EL²/N)/T
      =[h(0)-h(t)+M_h(t)+int r_h]/(NT).

Since NT=T^6, the deterministic terms are O_K(T^-2). Doob's inequality and
the actual q_hh bound give a squared maximal martingale error O_K(T^-3).
Thus the primitive of h dt/T converges uniformly in probability to the
primitive of 3l_N²e_N ds. Total mass of h dt/T is itself bounded by the
E ceiling and the occupation cap. Step-function approximation of a deterministic
continuous weight, together with this mass bound and uniform convergence of
path weights, justifies replacing it inside the eventual b_l² integral.
No rapid-mixing assertion or fast stationary distribution is substituted.

The accepted compact corrector equations imply the integral equations for the
limiting ODE. Alternatively apply the exact f=l corrector, the E counter, and
the just-proved h averaging. On a fixed compact enlarged to K+1 the field is
Lipschitz, so stopped Gronwall gives path convergence. Work to a deterministic
time strictly between s_K and s_(K+1); l'>=1 yields transversality and hence
sigma_K/T→s_K and convergence of the actual crossing state. Paths can be frozen
at their crossing. Compact failures have vanishing probability and do not
change this convergence. No estimate here is applied with K=K(N).

For each literal reaction write
`kappa_r=Delta q-b_l u_r/T`. The E term costs O_K(T^-3) in integrated
squared rate, because `int q_EE/T^6=O_K(T^-3)`. The fast correction costs
`int q_hh/T^12=O_K(T^-3)`. A C² Taylor remainder squared is bounded by a
constant times `u²/T^4+v²/T^12`, since |u|,|v|<=1; its integrated rate is
O_K(T^-3). The post-jump product terms are smaller. Thus

    int sum lambda kappa²=O_K(T^-3),
    int sum lambda (b_l u/T)²=O_K(T^-1).

Cauchy–Schwarz bounds the integrated cross term by O_K(T^-2), so multiplying
by T still gives a vanishing error. The exact q_LL expression leaves only
1+h at leading order: its remaining integrated rates are O_K(T^-1), from
H=O_K(T^-2) and A,C+D=O_K(T). It follows that

    T<M_b>_(sigma_K) →
      Sigma_K²=int_0^s_K b_l(l,e)²(1+3l²e) ds.

This is an actual reaction covariance calculation, including all corrected
AB/CD marks. The scaled E bracket is O_K(T^-2), and its cross covariance
vanishes by Cauchy–Schwarz. The rank-one l-direction noise is earned, not
assumed as a linear-noise premise. In particular the averaging identity alone
would not have justified this conclusion without the kappa and q_hh estimates.

## 5. Compact martingale CLT is valid on the actual stopped clock

For Y=sqrt(T)M_b, the maximum jump is O_K(T^-1/2), its predictable bracket is
bounded deterministically by C_K, and its terminal bracket tends to Sigma_K².
All rates are finite on the bounded-count stopped domain, and the chain is
nonexplosive: total is bounded above by N+2 plus the original immigration count.
For the compensated-jump characteristic-function calculation,

    Z_t=exp(i theta Y_t+theta²<Y>_t/2),

has residual integrated expected drift at most
`exp(theta² C_K/2)|theta|³ j_N C_K/6`. This follows from the integral Taylor
remainder `|exp(ix)-1-ix+x²/2|<=|x|³/6`; the predictable bracket here is the
continuous integrated actual squared jump intensity. The bracket cutoff and
bounded complex exponential justify the expectation/localization. Since its
terminal bracket is bounded and converges in probability to a constant,
E exp(i theta Y_terminal) tends to exp(-theta² Sigma_K²/2).
This proves the compact normal limit. No moment convergence of tau is used.

## 6. Growing cutoff: admitted states, stopped events, and full tail ledger

For each fixed K and sufficiently large T, choose J least with
`m_J=2^J KT>=T^(3/2)`. Then m_J<2T^(3/2), and active stages have
`m=Tr`, `K<=r<sqrt(T)`, `w=sqrt(Nm)=T³sqrt(r)`. Start only at the actual
successful preceding entrance, with the original fixed reference N. Retain
all stage clocks, martingale/tube/mass exits and deadlines; add the omitted
mark and count stops. Invalid future entrance or simultaneous band/L exit is
adverse. After any failure freeze the construction. No arbitrary-state stage
entry is inferred from the headline level-disjunction alone.

The received good-event occupation assertion is explicitly consumed:
`int A<=10^4 w/N`; the stage duration is at most 16w/m². Before any adverse
mark Z=0 and |n-N|<=10T, which is much smaller than delta N. Every omitted
rate still enters the full generator and bracket. From the exact omitted
intensity, a stage costs at most `11m int A<=110000 T^-1 r^(3/2)`.
The increasing geometric sum is less than twice its last term, hence below
400000 T^-1/4. This compensator bound applies to the stopped counter before
all the stated stops, so it pays the probability of any first omitted mark.
It does not condition the martingale on a future no-mark event. Original
stage failures keep their conditional sum `32exp(-KT/(3*10^12))`.

For all actual connecting segments, including an adverse endpoint,
`L>=m/2-1>=m/3`, `w/2-1<=E<=2w+1`, so

    l>=r/3, sqrt(r)/3<=e<=3sqrt(r), l>=e²/32.

The last follows already from 1/3>=9/32; it is not just a prestate test.
With K>=10^40, e>=1 and m,w>=100 are automatic. The actual A cap supplies
both hplus<=3mw and post-jump h<=2mw. In particular a terminal +1 has not
been silently removed.

The accepted full rate formulas give the positive integrated envelopes

    U=d+H+(5/2)mH+2wH,
    W=mH+2wH,
    VE=mH+4wH+8m²d,
    VL=d+H+4mH+2wH,
    Qh=4w²[d+H+6mH+4m²d+2NH]
        +16w²mH+40w³H+128w²m²d,
    Rh=2wd+24mwH+9m²H+8m²d+2wH[10T+2w+8m+2],

where H=10000w/N and d=16w/m². These are independently reconstructed from
`Q<=4mA`, `a2<=mA`, `h<=2wA`, `A(A-1)²<=m²A`, `CD<=4m²`, and
`AB<=2NA`. For example, Qh contains the full `E²AB` cost via 2NH, and Rh
contains the full actual count term via 10T. These fast terms are not zero.
Since m<=w on the active domain, A+E+1<=4w and |E-1|<=3w are valid.

The independent symbolic implementation reparameterizes `T=t^4`, `r=u²`,
`1<=u<=t`. A positive monomial c t^p u^q is at most c when
`p+max(q,0)<=0`. This alternative universal calculation gives U,W,VL<=10^7m,
VE<=10^7w, Qh<=10^7w³, and the printed five-base Rh envelope. It is not
verification at a finite grid of N,K or a floating-point power comparison.

Substituting the exact derivative exponents into all five residual classes,
including h' Delta b_l, gives the independently reproduced coefficient sums

    non-Taylor residual: 131059200000000000000 * T^-2 r^-1,
    Taylor:             8257200000000000000 * T^-1 r^-5/2,
    full bracket:       71293440000000000000000000000000000/(T r^4),
    jump:               1200000000000000/(T r^(5/2)),
    endpoint correction:2*10^14 T^-2 r^-1.

Each is below its author's generous stated ceiling. In particular the full
bracket includes both slow/fast cross terms and the q_hh term. Summing the
decreasing dyadic powers from r=K yields

    int_tail |R_b| <= C[T^-1 K^-5/2+T^-2 K^-1],
    <M_tail> <= C/(T K^4),

with C independent of N,K. These bounds hold on the stopped process, not only
its future-success event. The total deadline from the fixed compact entrance
is at most 32T/K^(3/2), so the construction stays before 4T and the original
immigration horizon 4T+5 is sufficient even on stopped failure paths.

## 7. Actual terminal clock and macroscopic clearance

At the joint-good actual entrance t_J, `E>=sqrt(Nm_J)` and the cone is admitted.
Thus `b<=200(m_J/T)^(-3/2)` and
`sqrt(T)|q(t_J)|=O(T^-1/4)+o(1)`. The endpoint corrector uses the previous
stage scale r_J/2, which changes only a universal factor; its T power remains
smaller. No A death occurred before t_J on this event, so total remains
N+2+I and the actual clearance target has not already been hit.

The ORIGINAL all-channel stages then continue from this actual entrance to
the first L>=delta N, with delta=10^-100. The cutoff satisfies m_J<<delta N
eventually; the original stage requirement N>=10^200 is also eventual. No
omission restriction is used to change dynamics during this final continuation.
The remaining dyadic time is at most

    32sqrt(N)/m_J^(3/2) <=32T^(1/4).

The same original immigration count excludes the upper mass exit: 8T is
below delta N/2-2 for sufficiently large T. The tiny lower band remains
`(1-delta)N`, not the clearance boundary. At t_J total>=N+2. An adverse
lower exit requires at least ceil(delta N) subsequent actual A deaths.
The good-stage occupation sum is at most 40000sqrt(delta), so the actual
unit death-clock representation or its exponential compensator pays this
exit by the received Poisson tail. No independence of that clock and its
random occupation is assumed.

At the first macro crossing, the received tube/F bounds and +1 endpoint
conventions provide actual B,C,D,E fractions at least delta/4 of the actual
entry total n, with `(1-delta)N<=n<=(1+delta)N`. The bound on E and C,D
uses a first crossing from below, not an arbitrary already-macro state.
The old accepted interior theorem has fixed positive c(delta/4) and finite
n0(delta/4), so its five-unit physical service applies eventually. It yields
S<=7n/8, and `(7/8)(1+delta)N<15(N+2)/16` is the correct comparison to the
unchanged original target. Thus the actual hit occurs by t_J+32T^(1/4)+5
on events of probability tending to one.

This audit receives the old interior source a8e0bd38 and its separate receipt;
it does NOT silently replace it with the later explicit harmonic service or
replacement addenda. Numerical values of its c,n0 are not acquired here.
They are sufficient for this asymptotic conclusion and insufficient for a
ready finite-N numerical error evaluator. The lower band is never called
clearance, and the continuing physical waiting time is included.

## 8. Correct centering, martingale comparison, and order of limits

At time zero h=0, L=1, E=0; `|q(X0)-s_*|<=1/T` by |b_l|<=1. The identity
has the sign

    t/T = q(X0)-q(Xt)+int R_b+M_b(t).

The compact residual, summed tail residual, terminal q, and actual continuation
therefore show, for each fixed K,

    (tau-s_*T)/sqrt(T) - sqrt(T)M_b(sigma_N) ->0 in probability.

Failure probabilities tend to zero, including the paid O(T^-1/4) omission
price; uncontrolled failure durations are not multiplied by that probability.
This proves a weak transfer (equivalently normal CDF convergence at each finite
point), not an integrable error bound.

On a compact failure the tail is zero; on an admitted entrance it is an
adapted stopped martingale with bracket at most C/(TK^4). Hence

    E|sqrt(T)[M_b(sigma_N)-M_b(sigma_K)]|²<=C/K^4.

This isometry is legitimate on the stopped construction itself. It is NOT an
L² statement about tau. For bounded 1-Lipschitz test functions it costs at most
sqrt(C)/K². Take N to infinity at fixed K using the compact CLT, and only then
K to infinity. There is no unjustified diagonal use of a fixed-compact estimate.

The covariance limit is positive because b_l(0,0)=-1 and continuous. It is
finite: along the origin orbit l=s+(3/4)e² and s<=2, so for l>=4,
e²>=(2/3)l. The received `|b_l|<=64/(135e^5)` gives `b_l²<=C l^-5` and
variance tail O(K^-4). Since dl/ds=1+3l²e, the two displayed integrals for
Sigma² are identical. Thus Sigma_K²→Sigma², completing the normal limit.

Crucially, this reasoning does NOT discard the fixed-K deterministic duration
of size T/K^(3/2), which would diverge after division by sqrt(T). That entire
segment is transported by the corrected remaining clock. Only the noise tail
is made small as K grows. The duration discarded is the genuinely smaller
post-growing-cutoff O(T^(1/4))+5 contribution.

## 9. Exact checks, replay, and limitations

The sealed independent checker passes **144,878** exact assertions: 69 symbolic
full-chain identities/controls; 144,504 finite enabled-jump/domain checks;
126 universal tail-monomial checks; 10 geometry/clock checks; 161 fixed-compact
power checks; and 8 limit-exponent checks. A preliminary progress count included
19 redundant rational decay sanity checks; those were omitted from the final
checker and count. No failed author assertion or source repair is hidden by
that count cleanup.

A copied execution of the frozen author checker passes all 91 assertions and
reproduces `TAIL_CHECK_RESULTS.json` byte-for-byte. The read-only original
binding verifier passes all 23 specified byte/size pins. Separate readback
checks verify 63 bound files across the two earlier deterministic freezes and
their independent receipt manifests; their numerical solvers are not rerun
or newly accepted here. The exact parameter identity is detailed separately.

No blocking defect or counterexample to the frozen weak theorem was found.
The enormous K floor, delta, universal constants, and eventual interior
threshold are not practical computational costs. This is not an executable
finite-N distribution receiver, arbitrary-initial-state CLT, moment theorem,
variance convergence result, finite-noise Ito formula, or uniform finite-N
normal error bound. No claim about a point-mass CDF approximation, relative
extreme tails, exponential moments, measured physical model, or hardware follows.
No external source, helper, installation, simulation, or frozen-source edit
was used. New fraction-clock or other corollaries remain outside this receipt.
