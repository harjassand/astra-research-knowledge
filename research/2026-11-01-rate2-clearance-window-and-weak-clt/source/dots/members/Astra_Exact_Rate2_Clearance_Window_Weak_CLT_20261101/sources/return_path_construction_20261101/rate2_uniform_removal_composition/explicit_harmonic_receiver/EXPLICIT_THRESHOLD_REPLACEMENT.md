# Actual all-start block with a literal threshold and no interior-attraction supplier

**Author replacement candidate, pending review of the new harmonic theorem and
this join.** The accepted original composition and all its receipts stay unchanged.

Use the exact rate-2 count tree, total S, and the deterministic schedule
`d_N=1+10^8 sqrt(N)`. For EVERY initial composition of total N>=10^40, the proposed
replacement retains exactly

    P[S(d_N)>15N/16]<=32exp[-sqrt(N)/10^6],               (1)

but its threshold is now the literal 10^40, rather than an expression involving
unevaluated interior n0(epsilon),c(epsilon) and an extremely small positivity
window. It uses only actual full-generator and count-martingale arguments.

## 1. Exact received prefix, not an invocation of the old large-head conclusion

The original composition source
`../UNIFORM_ACTUAL_REMOVAL_BLOCK.md`, SHA256
 a0e09b39c50c28365a1ed5a0fe04c71b003b9c5556ffe9b94202441f9ee4cb21,
and its independent review at `../independent_review_20261101_0454/` provide the
already checked Sections 2-4: global seed, actual activation with seed persistence,
and activated macro M entry. These particular inequalities require only N>=10^40;
they do not use the old N_* terms introduced by its Sections 5-7. We receive that
prefix only, not its full conclusion at a threshold where it was not asserted.

Set m=floor(sqrt(N)/20000), k=floor(m/2), M=A+min(C,D). With all original mass
stops and priorities retained, the actual prefix reaches S<=3N/4 or

    M>=10^-12 N, 3N/4<S<=2N

by time at most `8m+10^12+256N/k`, except on errors

    (101/100)e^-m +e^(-m/4)+e^-N
        +8e^(-k/3)+e^(-N/100000).                       (2)

Upper mass stops are still adverse, not service. The original state and reference
N are never reset. No independence of stages or excursions is asserted.

## 2. New explicit actual receiver

The replacement receiver is
`../../rate2_explicit_macro_removal/EXPLICIT_HARMONIC_PERSISTENCE_AND_REMOVAL.md`,
SHA256 4d1ad7a929f7e3c6d81d06222bd8217eb96e06eb183e6f0cfe3f5dbca6ca16ca.
Take its parameters

    m0=10^-12, h=400/m0^2=4*10^26.

The size requirement N>=32h is automatic at N>=10^40. At a continuing macro
entry, apply it only if S<=5N/4; otherwise declare an adverse upper-entry output.
The original-episode headroom event below excludes that output, rather than
assuming the stronger upper entrance in every possible state. The M condition
is exactly the prefix's actual output.

The harmonic theorem gives S after h physical units <=13N/16, apart from

    32N^2h exp(-N/10^15)
      +exp[-200N^2/(32h+20/3)]+e^(-N/2)+e^(-N/96).       (3)

Each term of (3) is <=exp[-sqrt(N)/10^6] for N>=10^40.
For the only non-immediate comparison, put u=sqrt(N)>=10^20. Since 32h<e^100
and log u<=sqrt(u),

    log(32N^2h)<=100+4sqrt(u)<=5sqrt(u).

Also u^2/10^15-u/10^6>=u^2/(2*10^15)>=5sqrt(u) in this range.
The first error comparison follows. For the second, N>=32h and N>=7 give
`32h+20/3<=2N`, so its exponent is at least 100N. The last two comparisons
are elementary. Thus all four receiver errors are received at the common scale.

## 3. Deterministic deadline and original-episode headroom

Since k>=sqrt(N)/160000, the prefix time is bounded by
`40960000sqrt(N)+8m+10^12`. Also h<=4000000sqrt(N) for N>=10^40.
The entire successful construction therefore fits strictly inside

    (44960002)sqrt(N)<1+10^8sqrt(N)=d_N.                 (4)

Use the ORIGINAL unit immigration count I on [0,d_N]. Exactly as in the original
composition, `P[I(d_N)>N/64]<=exp(-N/256)`. On its complement, S(t)<=65N/64
for every time, excluding all upper stops and supplying S<=5N/4 at the harmonic
entrance. No phase estimate was conditioned on this future event.
If a lower mass stop occurred, then S(d_N)<=49N/64. Otherwise the successful
harmonic endpoint, followed by all unused continuing time, gives

    S(d_N)<=13N/16+N/64=53N/64<15N/16.                  (5)

The local harmonic immigration error is conservatively retained even though the
same original headroom already excludes it; no fresh independence is required.

The prefactors in (2), the four terms of (3), and the original immigration bound
sum to 1701/100<32. All exponents dominate sqrt(N)/10^6 at N>=10^40. This proves
(1) with a literal head and the original consumer parameters
`a=1/2, delta_remove=1/16, p=32, c=10^-6, D=100000001, d0=1`.

## 4. Scope and actual improvement

This replaces only the ordinary interior supplier, not the model or initial
rates. The same accepted sampled consumer would consequently receive
positive recurrence and a stationary exp(5*10^-17 S) moment once the new
harmonic source/join is independently accepted. Existing accepted proofs already
earn those conclusions by their original routes; this candidate does not revoke
or retroactively edit them.
The improvement is fully acquired finite constants and removal of a deterministic
global-attraction prerequisite, not a practical threshold or new-network claim.
N>=10^40 and the time coefficient remain enormous. No changing-rate theorem,
external-source novelty claim or operational interpretation is supplied.
