# Actual induction-to-clearance window and occupation receipt

**Author continuation candidate, pending independent review.** The finite-level
source is frozen separately; current global stability freezes are unchanged.
This is an actual first-passage confidence window, not approximation of a
continuous finite-N distribution by a point mass.

## 1. Exact target, references and finite admission conditions

Use the rate-2 model and x_N=(0,N,1,1,0) from
`FINITE_LEVEL_CORRECTED_CLOCK.md`, SHA256
 e0700bad37717a38976f295049a8d2cb1120aeb155c343783780d6b201f20c9d.
The true initial total is S0=N+2. Define

    tau_clear=inf{t:S(t)<=15(N+2)/16},  T=N^(1/5).

Fix K>=10^40, 0<a<=1/4, and retain all finite-level admission conditions and
its p,q,H,B_clock,B_A. Let

    delta=10^-100, Cstar=3*10^12, epsilon=delta/4,
    h_delta=4*10^4 sqrt(delta), D_K=32T/K^(3/2).

Require additionally

    KT<=delta N,
    (1-delta)N>=n0(epsilon).                              (1)

Here n0(epsilon) and c(epsilon)>0 are exactly the constants supplied by the
separately received actual interior theorem
`../rate2_paid_interior_removal/PAID_INTERIOR_REMOVAL.md`, SHA256
 a8e0bd383b053021f72e8197986581c87878046cdeaa7570536e44f5cf71a1cf.
Their mathematical existence is received, but no numerical values are claimed
acquired in this source. A numerical finite-N consumer must acquire them or
explicitly refuse the final interior admission; it cannot silently set them.

The dyadic source is
`../rate2_dyadic_continuation/EXACT_CORRECTOR_AND_STAGE_LEMMA.md`, SHA256
 0ddcfb78c068ae58c2e5ddae1da015ba70d76acae67a2b0e9104f7358775e0a2,
received with its source-bound audit and exact receiving addendum. In particular,
band exit takes priority over a simultaneous L hit, and only a first crossing
from below uses the terminal +1 bound. The lower band here is (1-delta)N,
NOT the .75N lower stop of the separate square-root construction.

## 2. Explicit total probability cost

Let P_mu denote a Poisson random variable of mean mu. Define

    B_imm=P(P_(4T+5)>delta N/2-2),
    B_stage=32 exp[-KT/Cstar],
    B_band=P(P_(h_delta)>=ceil(delta N)),
    B_int=exp[-c(epsilon)(1-delta)N],
    B_total=B_clock+B_A+B_imm+B_stage+B_band+B_int.        (2)

The actual finite-N statement is

    P{ (s_K-a)T <= tau_clear
          <= (s_K+a)T+D_K+5 } >=1-B_total.               (3)

A negative lower endpoint can be replaced by zero; probabilities are clipped
at zero/one as usual. Poisson tails in (2) are literal ordinary tails and may be
computed directly or replaced by certified Chernoff bounds. They are not claims
of independence between actual arrival, death and service events.

## 3. Mesoscopic entrance and original Poisson headroom

On the finite-level good event, t_K/T is within a of s_K, no A death or other
remaining bad event has occurred, and every non-mass entrance condition of the
dyadic theorem holds at t_K. Since s_K<2 and a<=1/4, t_K<3T. Before that hit,
S=N+2+I, so the clearance target cannot already have been reached.

Use ONE original unit immigration counter over the deterministic interval
[0,4T+5]. On I(4T+5)<=delta N/2-2, actual total is at most

    N+2+I <=(1+delta/2)N

throughout the construction. This gives literal starting headroom and excludes
EVERY upper dyadic mass-band exit. No local estimate is conditioned on this
future event; intersect it only after applying the uniform conditional estimates.
The error cost is exactly B_imm.

## 4. Receiving the stage's pathwise occupation budgets

The independently checked dyadic proof constructs, at each actual entrance
m_j=2^j KT, a good event of conditional probability at least
`1-16exp(-m_j/Cstar)`. On this event the continuing path reaches its next
in-band L target or a mass boundary before the stage deadline, all auxiliary
martingale/clock exits are excluded, and its actual occupation clock obeys

    int_stage A dt <=10^4 sqrt(m_j/N).                   (4)

This pathwise clock assertion is part of the proof's common stopped good event;
it is not inferred from the headline success disjunction alone. The receiving
argument here explicitly retains that event. Its failure is already included
in the same 16-term bound. Only analysis clocks restart; the state does not.

Stop at the FIRST actual L>=delta N, or a band exit or exceptional stage.
The geometric deadline sum is

    16 sqrt(N)/(KT)^(3/2)/(1-2^(-3/2)) < D_K.

The conditional failure sum is at most B_stage. On the good stage composition,
the accumulated actual A clock before this terminal outcome is at most

    10^4 sum_j sqrt(m_j/N)
      <=10^4 sqrt(delta)/(1-2^(-1/2)) < h_delta.           (5)

A final partial stage only decreases this bound. If initial L is already at the
macro threshold there is no stage and no upper-overshoot assertion is needed.

At the mesoscopic entrance S=N+2+I(t_K)>=N+2 because no A death has occurred.
A subsequent lower band exit S<(1-delta)N therefore requires at least
ceil(delta N) ACTUAL A deaths after t_K. Given the actual entrance state, realize
the future death counter by a fresh unit Poisson clock evaluated at int A dt.
On (5), its count is at most that same clock evaluated at h_delta. Thus

    P(lower band exit AND all stage clocks good | entrance)<=B_band. (6)

Equivalently one may use the counting-process exponential supermartingale.
The random compensator may depend on the death clock; pathwise monotonicity
on the event that it is <=h_delta suffices. No false independence is used.
This pays away the lower band exit instead of calling its tiny delta loss
15/16 clearance.

## 5. Actual positive-fraction entry and terminal clearance

On the remaining good paths, a first L>=delta N occurs by t_K+D_K, while total
stays in [(1-delta)N,(1+delta)N]. The accepted stage tube/corrector bounds give
at that actual entry

    B>=N/2, C,D>=delta N/2, E>=sqrt(delta)N/2.

For completeness, the last stage has m_j<delta N, post-jump
A<=m_j/16+1 and |C-D|<=m_j/16+1, while L>=delta N. Hence each of C,D is at
least delta N/2 at the admitted N. The identity defining F and its good bound
supply E>=sqrt(delta)N/2. The same identity gives E<=2sqrt(delta)N+1,
and A+C+D<=2delta N+2; together with the lower total band this gives B>=N/2.
These are first-crossing bounds, not the unsupported upper bound for an arbitrary
already-macro initial state. An initial KT=delta N entrance satisfies stronger
bounds directly from its received E/F/A conditions.

Let n be the ACTUAL entry total. It lies in the displayed band, so B,C,D,E are
all at least epsilon n. Condition (1) receives n>=n0(epsilon).
Strong Markov and the independently received interior theorem therefore give
actual S<=7n/8 after five further physical units, except on B_int. Since

    (7/8)(1+delta)N <15(N+2)/16,

this is a genuine hit of the stated clearance target. All times fit inside
4T+5 because t_K<3T and D_K<T for the admitted K. There is no unused-time
claim: the first-passage hit has occurred by the displayed deadline regardless
of what the continuing process does afterward. Combining these events proves (3).

## 6. Finite occupation outputs, with their separate error costs

The retained stopped estimate (4) of the finite-level source gives
`E int_0^tK A dt<=24p^2/T^2` before coupling failure or its outer stop.
Therefore imposing the additional event

    int_0^tK A dt<=1/T

costs at most

    B_occ_early=24p^2/T.                                 (7)

On that event and the good stage clocks, at the actual macro-positive entrance
u_macro,

    int_0^u_macro A dt <=1/T+h_delta.                    (8)

This is a stopped high-probability occupation guarantee, not an assertion about
the unrestricted expected A occupation. It prices all waiting before macro entry.

Conversely, actual clearance from S0=N+2 requires at least ceil(S0/16) A deaths,
since immigration only increases total. The unit death-clock representation gives

    P{tau_clear<infinity, int_0^tau_clear A dt<=S0/32}
       <=P(P_(S0/32)>=ceil(S0/16))=:B_occ_late.           (9)

For example Chernoff bounds this by exp[-(2log2-1)S0/32]. Thus (3), (8), and
`int_0^tau_clear A dt>S0/32` hold jointly except on probability at most
B_total+B_occ_early+B_occ_late. This is a finite physical-time/exit/occupation
packet, not merely a formal limiting trajectory.

## 7. Actual first-passage law of large numbers

From e'>=(9/8)e^4 and e(s_K)^2=(4/3)(K-s_K), s_K<=2, one has for K>2

    0<s_*-s_K <=sqrt(3)/[9(K-2)^(3/2)]=:beta_K.          (10)

For every FIXED K>=10^40 and a>0, all finite-N admission conditions eventually
hold and every term of (2) tends to zero as N tends to infinity. In particular,
no A death before the level hit is asserted only on this fixed-K stopped window;
there is no such claim beyond the deterministic blow-up time.
Given a desired temporal error, first choose K large enough to make beta_K and
32/K^(3/2) small, then choose a, then take N large enough. This uses the legitimate
order N then K, rather than diagonalizing an unquantified compact limit. It proves

    tau_clear/N^(1/5) -> s_* in probability.              (11)

A numerically certified interval for the ordinary scalar s_* may be inserted
from its separately reviewed solver; no numerical value is needed for this proof.
The useful finite-N output is the interval (3) and its complete error budget,
not zero CDF error to a deterministic point mass. A finite-N distribution kernel,
CLT, or conditional exit-law compression is not claimed.

## 8. Cost ledger and remaining numerical acquisition

The phase constants and every non-interior error in (2) are explicit algebraic,
exponential or Poisson-tail expressions. The finite-level prefactor is polynomial
in K and a^-1, not exp(CK^2), but is still extremely conservative. The accepted
K floor 10^40 and delta=10^-100 are unchanged and must not be hidden in a claimed
practical certificate. Scalar ODE computation and Poisson-tail evaluation have
their own ordinary numerical certification costs.

The final interior c(epsilon), n0(epsilon) remain separately supplied existence
constants until their ordinary validated acquisition is actually carried out.
Thus this source gives a finite-N ANALYTICAL certificate and an unconditional
mathematical LLN, but not a ready numerical finite-N evaluator with a claimed
running-time bound. The root computational consumer must retain/refuse that
acquisition gate. No novelty, arbitrary-network theorem, rate-changing operation,
publication, hardware action or operational chemistry is inferred.
