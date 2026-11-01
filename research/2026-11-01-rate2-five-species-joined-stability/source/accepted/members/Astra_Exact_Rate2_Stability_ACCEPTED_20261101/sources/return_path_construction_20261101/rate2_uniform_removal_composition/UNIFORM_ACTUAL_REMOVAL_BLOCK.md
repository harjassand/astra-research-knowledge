# Uniform actual population-removal block for the rate-2 return tree

**Author composition candidate, pending independent review of its new interfaces.**
This source joins actual continuing-state stopping constructions and explicitly
pays the deterministic block's unused time. It does not itself assert an accepted
recurrence or stationary-moment theorem.

## 1. Model, precise conclusion and sources

The actual model is unit-rate 0<->A, 2A<->AC, 2A<->AD, 2A<->AE,
AE<->CD and CD<->AB, with only CD->AE changed to coefficient two; binary sources
use falling factorials. Let S=A+B+C+D+E, R=C+D+E and M=A+min(C,D).
For every initial state with total N define the DETERMINISTIC physical block

    d_N=1+10^8 sqrt(N).

There is a finite explicitly specified-by-component-constants N_* such that,
uniformly over EVERY initial composition with N>=N_*,

    P_x[S(d_N)>15N/16] <=32 exp[-sqrt(N)/10^6].          (H)

The reference N is never reset. No state reset, intervention or assumed attempt
independence occurs at the analysis phase boundaries. Failed events are charged
and the process continues for the entire deterministic block.

The exact sources used are:

- `../rate2_uniform_initial_growth/UNIFORM_FULL_GENERATOR_INITIAL_GROWTH.md`,
  SHA256 90a80f12bfc045350b5254a4c8d731f506da5520ee161ccd9e7cbb11df82329e,
  independently received at `audit_uniform_growth_20261101_0435/SOURCE_BOUND_ACCEPTANCE.md`
  SHA256 a1eb22f7376fb8cfd138908629f7242edc164dc721476be0999dde4716de67e8.
- `../rate2_uniform_activation/UNIFORM_ACTIVATION_OR_REMOVAL.md`, SHA256
  c1d2ed0820d4f92ea236dcb27eab1cd29e27665f9b1a2e826617cc34e3c3fda8:
  use its exact U drift/bracket and stopped charging argument, not an unsupported
  seed claim at its already-activated time-zero output.
- `../rate2_activated_macro_interface/ACTIVATED_TO_MACRO_AND_POSITIVE_FRACTIONS.md`,
  SHA256 e527fafdfe790fa753b4584fca338bf9e4aa37179643a1f1596e39b140cb99a0.
- `../rate2_paid_interior_removal/PAID_INTERIOR_REMOVAL.md`, SHA256
  a8e0bd383b053021f72e8197986581c87878046cdeaa7570536e44f5cf71a1cf:
  for fixed epsilon>0,
  an actual entry total n with B,C,D,E>=epsilon n has
  P[S(5)>7n/8]<=exp[-c(epsilon)n] for n>=n0(epsilon).
  Its separate independent receipt, not this source, controls its accepted scope.

The initial-growth source alone does not grant the new global-domain extension
below. That extension is proved here, not silently attached to its receipt.

## 2. A globally received seed before activation

Set m=floor(sqrt(N)/(2*10^4)), k=floor(m/2), and first assume N>=10^40.
Use the source function

    G_N=2^(-M)[1+(16/N)phi(M,R)A^2],
    phi=clip_[0,1]((96-R/(M+1))/48).

**Global-domain extension.** On M<m and S>3N/4, its actual full drift satisfies
`LG_N<=-G_N/4`, without a separate B assumption. To check this precisely:

- In the core R<=48(M+1),
  B=S-A-R>3N/4-49m-48>=N/2. Hence the accepted core calculation applies.
- Outside the core, the accepted outer calculation uses no lower bound on B.
  The positive-M group has rate at least A max(C,D,E)>=4q_minus; immigration
  supplies its fixed reserve. The entire positive zero-M cutoff expense is
  <=(A^2+1)/100 using N>=10^8(m+1)^2. AB->CD is nonadverse and can be dropped
  whatever B is. Thus the same bound `LG_N/2^(-M)<=-12/25` applies there.

All targets use the same function and A<=m at those targets, so h<=101/100.
Stop at M>=m, S<=3N/4 or S>2N, with mass outcomes taking priority over a
simultaneous seed jump. If M>=m initially there is no seed wait. Otherwise the
same t-wedge-stop integrating-factor/Fatou argument gives

    P(seed/main stop takes longer than 8m)<=(101/100)e^(-m).  (2)

This step also handles inactive states which were already activated at time zero;
there is no assumption that an R-threshold hit has supplied a seed.

## 3. Actual activation while preserving the seed

After the seed, take a removal output immediately if S<=3N/4. Upper S>2N remains
adverse. If already M>=delta N with delta=10^-12, go straight to Section 5.
If already R>=B/100, no activation wait is needed. Otherwise run the actual
charging phase from the cited activation source for at most T0=10^12, stopping
on a mass outcome, R>=B/100, M>=delta N or M<=k. Main/macro outcomes have first
priority; an activated exit on a simultaneous lower-seed mark retains M>=k.

The activation source's exact coordinate U=E-A/10 has

    LU>=M^2/4+(2/25)AB-3/5,
    Gamma_U<=4LU+241/100,
    L exp(-U/10)<=-[M^2/100]exp(-U/10) when M>=4,

throughout R<=B/100. Its stopped exponential argument bounds a charging
non-exit by exp(-N). Lower-seed excursions are paid by the G_N potential:
each actual crossing m->m-1 starts a strip k<M<m, and the global-domain
extension just proved receives its drift. The probability to reach k during
one excursion is at most (202/100)2^(-m/2). Before S>2N the expected number of
such crossings in T0 is <=32N^2 T0; hence their total cost is <=exp(-m/4).
No independent excursions or discarded AE losses are used. Therefore this phase
fails to give activation/macro/removal within its budget with probability at most

    exp(-m/4)+exp(-N).                                   (3)

At a continuing activated output M>=k. If M<delta N, then A<=M<delta N and

    R>=(S-A)/101>(3/4-delta)N/101>=4rN,  r=1/1000.      (4)

Thus the exact activated-macro interface is now actually received.

## 4. Uniform macroscopic entry or genuine removal

The activated interface, conditional on each actual state just obtained, gives
macro M>=delta N or a main mass stop within 256N/k, with failure at most

    8exp(-k/3)+exp(-N/100000).                           (5)

Its entire R-retention event is paid once by exp[-(R+2A+4M)/100]. Its finite
dyadic stages use 2^(-M)(1-A/(4N)) and retain all competing marks, including
neutral fast AB<->CD, CD startup, AE losses, 2A events and last deaths.
The mass stopping bounds are relative to this same original N. The lower stop
is a genuine reduction of that initial population; the upper stop is not service.

The inequalities m>=sqrt(N)/40000 and k>=m/4 imply

    8m+T0+256N/k+1/N+5 <1+10^8 sqrt(N)=d_N.             (6)

Thus the full optional composition fits inside the deterministic clock. Skipped
stages use no time, and all successful analysis phases continue from the actual
post-jump state rather than resetting anything.

## 5. Interior entrance and removal at a random paid time

Put eta=delta^4/(1000*3^40), epsilon=eta/4,

    rho=eta exp(-100)/4,
    c_win=rho^2/[2(32+rho/3)].

The macro interface supplies, over physical 1/N, an actual full-chain window with
probability of error at most 10exp(-c_win N). On its good event all five counts
are >=eta N/2. Treat any prior S<=3N/4 hit as removal instead. Otherwise the
interior entrance total n is >3N/4; provided no upper mass exit has occurred,
n<=2N and B,C,D,E>=epsilon n.

For N>=4 n0(epsilon)/3, the separately received interior theorem applies at this
actual stopping-time entrance by the strong Markov property. After a further
physical time 5 its conditional failure probability is at most

    exp[-(3/4)c(epsilon)N].                              (7)

It gives actual total <=7n/8 at that time. A lower mass hit at any earlier
construction phase was already removal. Neither outcome alone is treated as
an assertion at d_N; the unused continuing time is paid next.

## 6. One immigration charge for every phase AND unused time

Let I be the actual unit-rate immigration Poisson counter over the whole fixed
interval [0,d_N]. At every time S(t)<=N+I(t). Define the single event

    G_imm={I(d_N)<=N/64}.

For N>=10^40, d_N<=N/256. Chernoff with parameter log2 and log2>=2/3 gives

    P(G_imm^c)<=exp[d_N-(N/64)log2]<=exp(-N/256).        (8)

On G_imm no S>2N outcome can occur anywhere; this prices all upper exits
simultaneously. If a lower mass stop occurred, then at the FINAL block time

    S(d_N)<=3N/4+N/64=49N/64<15N/16.

If instead the interior theorem succeeded from entry n, then n<=65N/64 and
at the final block time

    S(d_N)<=7n/8+N/64<=463N/512<15N/16.                (9)

This pays all post-service waiting. It does not condition on G_imm when invoking
any phase estimate or assume immigration independent of success: all errors are
combined by a union bound in the actual joint construction.

## 7. Threshold, full failure bound and precise scope

Choose N_* to be any integer at least the maximum of

    10^40,
    28exp(100)/eta,
    4n0(epsilon)/3,
    [1/(10^6 c_win)]^2,
    [4/(3*10^6 c(epsilon))]^2.

The last two ensure the ordinary exp(-cN) window/interior errors are no larger
than their stated prefactors times exp[-sqrt(N)/10^6]. All values are finite;
n0 and c are exactly the constants supplied by the received interior theorem,
not an assumed stochastic mixing oracle. Thresholds may be enlarged without
changing the argument. No practical computation of these enormous constants is
claimed. The finite-cover/validated-ODE acquisition described by the interior
source remains its own explicitly identified ordinary cost.

Combine (2), (3), (5), the 10exp(-c_win N) window error, (7) and (8).
Since k>=sqrt(N)/160000, the weakest mesoscopic term has exponent at least
sqrt(N)/480000, stronger than sqrt(N)/10^6. The sum of all displayed prefactors
is less than 32. This proves (H).

This is a full uniform actual-block candidate for THIS non-complex-balanced
rate-2 tree, not arbitrary connected binary complex graphs. Its permitted
consumer parameters are a=1/2, delta_remove=1/16, p=32, c=10^-6,
D=100000001 and d0=1. The root sampled-return consumer may receive these only
after this composition and its new interfaces are independently checked.
In particular the source does not replace the continuous-time generator by the
complex-balanced competitor, and it does not produce a geometric Foster function
uniformly comparable to exp(theta S). That forbidden bounded-profile geometry
is bypassed by state-dependent real-time blocks and their occupation measure.
