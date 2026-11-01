# Raw-corner entrance and actual A/Z gates, stopped at the first other failure

**Author construction; not independently received.** This is an actual-chain gate
component, not an upper-ratio survival theorem or a clearance predictor. It uses
all twelve exact rate-2 reactions. No stationary A fiber, independent attempt
law, added source, reset, or CD-pulse simulation is used.

## Result and interface

Take integer N>=10^20, T=N^(1/5), raw initial state (0,N,1,1,0), and

    L=A+(C+D)/2, Z=C-D, R=E^2/(NL), m0=400.

Receive the accepted original count-band event through the first macro cap
`E>=ceil(N/100) or L>=N/5000`, or ORIGINAL time 4T. Its failure charge is

    delta_count=exp(-N/6200)+exp(-T)+exp(-5T).

It supplies B>=.9N without assuming A/Z/R gates. In the proofs below, B<.9N
is an explicit stopping boundary; **never condition on the favorable count event**.
Only at the end is its already-proved probability charge added.

The construction first reaches **actual L=400 by time 800**, with A<=2 and
Z=0, except for the startup failures priced below. From that entrance onward,
until the FIRST of a macro cap, original time 4T, R>2, or another stated gate
failure, it earns

    L>=200,     A/L<=1/100,     |Z|/L<=1/100.

The sum of its own first-exit-type costs, INCLUDING startup but EXCLUDING the
separately priced count band and the UNPRICED upper-R exit, is less than:

| N | own-gate failure upper bound |
|---:|---:|
| 10^20 | 3.548262743e-9 |
| 10^21 | 3.524124525e-10 |
| 10^22 | 3.521718027e-11 |
| 10^23 | 3.521477450e-12 |
| 10^24 | 3.521453393e-13 |
| 10^25 | 3.521450988e-14 |

These are outward-rounded numerical evaluations of the literal finite sums
below, not simulations. The dominant term is deliberately conservative startup
protection against every nonzero imbalance mark and every L-decreasing mark.
They establish useful gates in this N range, **not** that R<=2 survives or that clearance occurs. A first upper-R failure kills every later
stage; none of the estimates below assumes upper-R survival.

## 1. Exact identities and physical stop

The literal rates give

    lambda_A_up=1+A(C+D)+AE+3CD,
    lambda_A_down=A+3A(A-1)+AE+AB,
    GA=1-A-3A(A-1)+A(C+D)+3CD-AB,
    GL=1+A+AL-3A^2+AE,
    q_LL=1-A/2+A^2+AL/2+AE,
    GZ=-AZ,                 q_Z=2A(L-1).

Every A jump and every nonzero Z jump has magnitude one. E-upward marks have
rate `A(A-1)+2CD<=2L^2`, with no A-cap premise. All states and all rates used
are actual pre-stop states; terminal jumps are retained.

Adverse boundaries are assigned failure even when simultaneous with a stage
or macro target. At a jump to another gate failure the relevant martingales
are still evaluated at that actual endpoint. At original time 4T, unfinished
progress is a declared output, not a gate failure or successful clearance.

## 2. Raw-corner startup, without an independent fiber

Write m=400, mu=.9N and set

    d0=2m, r0=1+3m^2, e0_bar=8m^3, b0=e0_bar+2m,
    H0=2m r0/(mu-2m).

Stop at the first L>=m, time 2m, B<.9N, A>=3, any L-decreasing reaction,
any nonzero Z reaction, or the original E-birth counter reaching e0_bar.
Before this stop, A<=2, L<m, and

    GA<=r0-(mu-2m)A.

Nonnegative terminal A and stopped Dynkin imply `E int A dt<=H0`.
This is an unconditional expectation for the stopped actual process.

On A>=1, the up/down rate ratio is at most

    rho0=(r0+b0)/mu<1.

The exponential birth/death barrier used in Section 5 therefore bounds an
actual excursion from A=1 to A=3 before A=0 by rho0^2. Every such excursion
starts with a 0->1 upcrossing, of rate at most r0. Hence its opportunity
compensator gives, without independent attempts,

    delta_start_A <= 2m r0 rho0^2.                      (S1)

At A<=2 the total rate of L-decreasing marks is `A+3A(A-1)<=4A`, and the total
rate of nonzero Z marks is `2A(L-1)<=2mA`. Thus

    delta_start_marks <= (4+2m)H0.                      (S2)

The original E-birth counter has compensator at most `2m^2(2m)=4m^3`.
The exponential counting martingale at theta=log 2 therefore gives

    delta_start_E <= exp[-(8 log 2-4)m^3].              (S3)

This is not a claim of conditional Poisson independence. The ordinary unit-rate
immigration counter I does have Poisson law. If no earlier adverse stop occurs,
L never decreases and L>=1+I. Therefore a startup timeout implies I(2m)<m,
and its probability is at most

    delta_start_time <= exp[-(1-log 2)m].               (S4)

At entrance, L is exactly m: with the charged marks absent and A<=2, every
remaining L-changing mark is +1. Also A<=2, Z=0 and E<8m^3. Before entrance
L>=1; hence `R<64m^6/N<2` for N>=10^20. Likewise the macro caps cannot occur
there. Thus no unpriced upper-R or macro escape is hidden in startup.

For N=10^20, (S1) is below 1.245095e-14 and (S2) is below 3.430408e-9.
The same formulas apply for every declared N; no asymptotic replacement is used.

## 3. Dyadic stages and an earned floor/time scaffold

For j=0,1,... with m_j=400*2^j<N/5000, set

    m=m_j, h=m/400 (an integer), U=min(2m,N/5000),
    d=min(4m,4T).

A stage starts at its actual first L>=m after the previous successful stage.
Its entrance satisfies `m<=L<m+1`, `|Z|<=h`, and `A<=a_j`, where
`a_0=2` and `a_j=h` for j>=1. The only exception to A<=h is thus the first
stage; startup supplies A<=2,Z=0, already inside its A<=2h cap. The stage
ends at the first of:

* L>=2m, or either macro cap, or original time 4T;
* R>2, B<.9N, L<m/2, A>=2h+1, or |Z|>=2h+1;
* elapsed physical time 4m, or either auxiliary source/birth-budget exit below.

A simultaneous adverse gate exit is a failure, not a successful target.
Before these stops, A<=2h=m/200 and L>=m/2 imply A/L<=1/100; the same
calculation gives |Z|/L<=1/100. A successful doubling supplies the next entrance
A,|Z|<=2h=h_next. This induction concerns the actual states, not typical ones.

Let theta=log 2 and c=2 log 2-1>0. Since `q_LL<=GL` and `GL>=1` on these
pre-stop states, the finite-jump bound, for |u|<=1,

    exp(-theta u)-1+theta u <=(exp(theta)-1-theta)u^2

shows `G exp(-theta L)<=-c exp(-theta L)`. Consequently both
`exp(-theta L)` and `exp(-theta L+ct)` are stopped supermartingales. They give

    delta_floor,j <= exp(-theta m/2),
    delta_time,j  <= exp[theta(m+1)-4cm].                (D1)

The +1 in the second bound is harmless padding; theta*m alone suffices.
The timeout bound concerns a stage still alive at elapsed 4m; an earlier
original-time-4T stop is not a timeout failure. No positive-drift heuristic or
independent Gamma law is needed.

On successful prior time stages, the start time is at most
`2m0+4 sum_{i<j}m_i=4m-2m0`, and this stage is over by absolute time 8m.
Throughout that history before the current target/failure, L<2m.

## 4. Original E-birth boxes and same-stop A occupation

Let J_E be the ORIGINAL E-upward reaction counter from raw time zero. Before
the history just described stops, its compensator is at most

    2(2m)^2(8m)=64m^3.

Thus the event J_E reaching 128m^3 first has probability at most

    delta_birth,j <= exp[-(128 log 2-64)m^3].             (D2)

This is an original-counter stopped counting-martingale bound, not a restart
with an invented small E initial state. Since E(0)=0, E<=J_E pathwise.
Before the other gates, R<=2 and L<U also imply E<sqrt(2NU)<=2sqrt(Nm).
The macro E gate implies E<ceil(N/100). A deterministic integer ceiling is
therefore

    Ebar=ceil(min(128m^3, 2sqrt(Nm), N/100)).              (D3)

For the N values in the table N/100 is integer. For arbitrary integer N, the
ceiling still bounds each integer pre-cap E, and Ebar<=N/100+1.

Use the accepted unweighted storage, with its actual one-jump endpoints,

    W=A+2(Ebar+1-E), Q=int[(AB/2)+CD]dt,
    D=a_j+2(Ebar+1)+d, Qbar=2D.

At actual stage entrance W<=a_j+2(Ebar+1). The required source conditions hold:
`A<=L<=N/5000<B`, and

    C+D+4E <= N/2500+4(N/100+1) < B/2.

The accepted source-storage proof now gives

    delta_source,j <= exp(-D/124),
    int_stage A dt <= Hbar=4D/(.9N)                    (D4)

until the same physical stops, except for that charged first Q-budget hit.
No independence of A, E, Q, or stage entrances is used. The deterministic
initial-storage ceiling, not a claimed mean entrance storage, is what appears
in D. Since q_Z<=2UA, the same stop supplies the bracket budget

    v_Z=2U Hbar=8UD/(.9N).                              (D5)

## 5. Actual A excursions and their opportunity count

Throughout the stage,

    lambda_up <= r+bA, lambda_down >=mu A,
    r=1+3U^2, b=Ebar+2U, mu=.9N.

Define

    rho=(r/h+b)/mu <1.

Indeed `3U^2/h<=.48N` for ALL stages: use U=2m when m<=N/10000 and
U=N/5000 otherwise. Also `b<=.0104N+1`, `1/h<=1`, so for N>=10^20,

    rho <=(.4904N+2)/(.9N) <.545.                       (A1)

On h<=A<=2h, `rho^(-A)` is a supermartingale, by the literal birth/death
rates. An excursion beginning at A=h can hit 2h+1 before A=h-1 or another
physical stop with probability at most rho^(h+1). Each later excursion must
start with an actual upcrossing h-1 to h. Its predictable rate is at most
`r+b(h-1)`. Include one possible initial entrance excursion. The compensator
bound and conditional optional stopping, NOT independence of excursions, give

    delta_A,j <= [1+d(r+b(h-1))] rho^(h+1), j>=1.        (A2)

At j=0, the actual entrance may instead have A=2. Its initial excursion to
3 costs at most rho, whereas subsequent upcrossings 0->1 cost rho^2 each.
Thus the first stage uses the explicit replacement

    delta_A,0 <= rho+d r rho^2.                         (A3)

The source initial-storage ceiling in Section 4 also uses a_0=2; it does not
silently keep the one-particle initial charge from the other stages.

The physically capped U is crucial. Replacing it by 2m even when 2m>N/5000
would spoil the useful uniform rho bound near the macro cap.

## 6. Imbalance via its exact inward drift, without a damping-factor loss

For any eta>0, exact +/-1 marks give

    G cosh(eta Z)
      = -AZ sinh(eta Z)sinh(eta)
        +(cosh(eta)-1)q_Z cosh(eta Z)
      <=(cosh(eta)-1)q_Z cosh(eta Z).

Therefore `exp[-(cosh(eta)-1) int q_Z] cosh(eta Z)` is a positive stopped
supermartingale. The actual entrance has |Z|<=h, and a cap failure has
|Z|>=2h+1. On the source-budget event (D5),

    P(Z cap first) <=cosh(eta h)/cosh(eta(2h+1))
                      *exp[(cosh(eta)-1)v_Z]
                  <=2 exp[-eta(h+1)+(cosh(eta)-1)v_Z].

Choose eta=asinh((h+1)/v_Z). This yields the explicit bound

    delta_Z,j <=2 exp[-(h+1)asinh((h+1)/v_Z)
                        +sqrt(v_Z^2+(h+1)^2)-v_Z].      (Z1)

If v_Z=0 the noise is zero and the cost is zero. This exact cosh barrier
retains the inward drift GZ=-AZ. It avoids the unnecessary factor two from
bounding Z by twice the supremum of its driving martingale. In particular it
is nonvacuous even in the earliest stages where the bracket is tiny and the
integer cap is only two.

## 7. Literal finite sum, refusals, and stopping semantics

Put

    delta_gates = sum_{k in {A,marks,E,time}} delta_start_k
      +sum_{j:m_j<N/5000} (delta_floor,j+delta_time,j+delta_birth,j
                          +delta_source,j+delta_A,j+delta_Z,j). (F)

The startup estimates concern the process stopped also at the B floor; they
do not condition on survival of that floor. Stage A/Z/source/floor/time bounds
apply conditionally on each ACTUAL admitted entrance sigma-field and stop at
FIRST other failures. The original-counter birth boxes (D2), by contrast, are
unconditional bounds on the stopped original history, not fresh conditional
Poisson laws at stage entrance. Sequential optional stopping and a union bound
give (F) for
own first-exit types. Adding delta_count removes the auxiliary B boundary.
This DOES NOT bound the probability of an R>2 first exit. That separate
receiver must supply delta_R before a consumer can claim probability at least
`1-delta_count-delta_gates-delta_R` of surviving all gates to macro cap or 4T.
There is no conditioning on an upper-R survival event anywhere in this proof.

Refuse a numerical admission claim if N<10^20 for this version, if the raw
corner or the original time origin is changed, if a required count-band proof
is absent, if a computed rho is >=1, or if the final summed probability is
nonpositive. A claimed macro target after original time 4T needs a new received
count horizon; this component does not provide one. The construction does not
supply a lower R bound, a final clock-error bound, or the physical removal time.

`check_actual_gates.py` independently reconstructs the reaction identities and
evaluates (F) using high-precision decimal arithmetic, with a strictly positive
upper replacement for tiny exponential terms. Its output is evidence for the
algebra and numbers, not independent mathematical receipt of this author note.
