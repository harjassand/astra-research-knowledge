# Independent review: explicit harmonic persistence and actual endpoint service

## 0. Verdict and exact statement

**PASS, no correction to the author theorem or constants required.** Accepted source: `EXPLICIT_HARMONIC_PERSISTENCE_AND_REMOVAL.md`, SHA256 `4d1ad7a929f7e3c6d81d06222bd8217eb96e06eb183e6f0cfe3f5dbca6ca16ca` (8,831 bytes).

For the literal full twelve-channel rate-2 count process, fix an integer reference N and rational `0<m0<=10^-6`. Set `h=400/m0^2` and require `N>=32h`. From EVERY count state with `3N/4<S(0)<=5N/4` and `M(0)=A+min(C,D)>=m0N`, the source earns

`P[S(h)>13N/16] <=32N^2h exp(-m0N/1000)`

`+exp[-200N^2/(32h+20/3)]+exp(-N/2)+exp(-N/96)`.

This is the displayed fixed-reference ENDPOINT service. It is not a fixed fractional decrease from every allowed starting total: an admissible S(0) just above .75N can already be below .8125N. N is never replaced by the moving total. Any later join must receive the literal entrance mass, M threshold, N>=12800/m0^2, elapsed h, and reference-based endpoint. Replacement joins are outside this receipt.

The proof is self-contained at the actual-generator boundary. It uses no deterministic attraction supplier, unknown interior c/n0, stationary fiber, stochastic mixing, or favorable next-event path. It does not implement a hardened numerical receiver or certify practical computation/physical acquisition.

## 1. Exact actual marks and harmonic geometry

Write `c=A+C`, `d=A+D`, `s=c+d`, `H=2cd/s` for s>0 and H=0 for s=0. Then `M=min(c,d)`, so `M<=H<=2M`, `A<=M`, and `s>=2H`. For nonnegative count states H<=S as well.

The twelve channels have the following (delta A, delta c, delta d) marks:

| Channel | Rate | delta A | delta c,d |
|---|---:|---:|---|
| immigration | 1 | +1 | (+1,+1) |
| A death | A | -1 | (-1,-1) |
| 2A->AC | A(A-1) | -1 | (0,-1) |
| AC->2A | AC | +1 | (0,+1) |
| 2A->AD | A(A-1) | -1 | (-1,0) |
| AD->2A | AD | +1 | (+1,0) |
| 2A->AE | A(A-1) | -1 | (-1,-1) |
| AE->2A | AE | +1 | (+1,+1) |
| AE->CD | AE | -1 | (0,0) |
| CD->AE | 2CD | +1 | (0,0) |
| CD->AB | CD | +1 | (0,0) |
| AB->CD | AB | -1 | (0,0) |

All enabled targets are nonnegative. The falling factorial convention and coefficient two are retained literally. In particular all four AB/CD and AE/CD phase directions are harmonic-neutral, including the two different CD exits.

On s>0,

`H_c=2d^2/s^2`, `H_d=2c^2/s^2`, `1<=H_c+H_d<=2`,

`Hess H=-(4/s^3)(d,-c)^T(d,-c)`.

The Hessian is negative semidefinite, rank one, with operator norm `4(c^2+d^2)/s^3<=4/s`. Every nonzero c,d mark has entries in {-1,0,1} and squared length <=2. For a source with H>=1000, the entire line segment to an enabled one-jump target has denominator at least s-2>=2H-2>0. Taylor's integral remainder is therefore at least

`-(1/2)[4/(s-2)]*2=-4/(s-2)>=-4/H`.

Thus there is no unpriced finite-jump curvature or singular denominator. The endpoint is never replaced by a derivative evaluation. On the entire nonnegative quadrant each actual harmonic mark has absolute size <=2: single-coordinate marks use a partial derivative <=2, and same-sign double marks use H_c+H_d<=2. At the origin the continuous extension gives the same bound directly. No enabled mark has opposite-sign nonzero c,d components.

## 2. Full harmonic and falling-factorial generators

The exact full coordinate drifts are

`Gc=1+A+A(d+E)-3A^2`, `Gd=1+A+A(c+E)-3A^2`.

The exact H-changing intensity is

`q_H=1+A+3A(A-1)+A(C+D+E)`.

Let V=max(C,D), X=V+E. Linearizing H only for the purpose of the separately paid remainder gives a drift lower bound

`1+A+AV/2+AE-6A^2`.

Indeed the positive constant/A/AE part uses H_c+H_d>=1; the negative -3A^2 part uses H_c+H_d<=2; and

`H_c d+H_d c=2(c^3+d^3)/s^2>=max(c,d)/2>=V/2`.

Multiplying the full remainder price by q_H and weakening A(A-1) to A^2 gives exactly the source's lower bound (7).

Let f(A)=A(A-1). Direct summation of the twelve actual marks gives

`Gf=-6A^3+10A^2-2A+2A^2(C+D)+2AE+6ACD-2A(A-1)B`.

For an upward A mark, delta f=2A; for a downward enabled mark, delta f=-2(A-1). Thus every enabled phase mark has absolute value <=2A. At A=0, every enabled upward phase mark is ZERO. At A=1, downward phase marks are zero. These integer endpoint facts are essential; substituting A^2 for the falling factorial would lose the zero-cost CD startup at A=0.

Set `W=H-100f(A)/N`, and let delta0=10^-6. In the source region `3N/4<S<=2N`, `1000<=H<=delta0 N`, `N>=200000`, use A<=H, CD<=HV, C+D<=2V. The V coefficient in GW is at least

`1/2-8/H-1000H/N>=491/1000`.

Here the 1000H/N pays both `200A^2(C+D)/N` and `600ACD/N`. The E coefficient is at least

`1-4/H-200/N>=995/1000`.

The constant is >=996/1000. The remaining linear-A losses, after retaining the initial +A, are bounded by

`[12-1+4/1000+1000delta0]A=11.005A<12A`.

The favorable terms 600A^3/N and 200A/N may be discarded. This yields the literal uniform bound

`GW>=99/100+(49/100)AX-6A^2-12A+(200/N)A(A-1)B`.

All one-jump target values used in G are the same globally defined W; no event is killed.

## 3. Both B cases, including A=0 and A=1

If B>=N/4, the last term is at least 50A(A-1), giving

`GW>=.99+.49AX+44A^2-62A`.

For integer A>=2, `44A^2-62A>=10A^2`. At A=0 the positive constant suffices. At A=1, use H<=2M to obtain `min(C,D)=M-1>=H/2-1>=499`, so X>=499. This pays the otherwise negative A=1 polynomial: `.99+.49X-18 >=(2+X)/4`. Therefore in every integer case

`GW>=(1+AX+A^2)/4`.

If B<N/4, set rho=1/4-delta0/2. Because S>3N/4 and A<=delta0 N,

`X>=R/2=(S-A-B)/2>rho N`.

For N>=200000, the exact rational inequality

`6delta0+12/N <=(24/100)rho`

holds. Hence `6A^2+12A<=.24AX`; also A(A-1)B>=0 on integer states. The same drift bound gives

`GW>=.99+AX/4`.

Both cases prove strict positivity uniformly in imbalance and all absent coordinates. They use no hypothesis that A is equilibrated or that C,D,E individually have fixed positive fractions.

## 4. Full squared-mark bound and exponential barrier

The full actual rate is

`q_all=1+A+3A(A-1)+A(C+D)+2AE+3CD+AB`.

On the small-H source region, A<=delta0 N, CD<=2NH, and C+D+2E+B<=2S<=4N. A direct conservative bound is

`q_all/N^2 <=1/N^2+delta0/N+3delta0^2+10delta0 <=13delta0`.

The last inequality already holds at N=200000 and improves afterward. It is independent of balance and includes immigration and every death/return.

Since |delta H|<=2 and |delta f|<=2A,

`|delta W|<=2+200A/N<=2+200delta0<3`.

Using (u+v)^2<=2u^2+2v^2 and summing every channel,

`Gamma_W<=8q_H+(80000A^2/N^2)q_all`.

The integer inequality A<=A^2 gives `8q_H<=8+32A^2+16AX`; the phase cost adds at most 1.04A^2. Thus

`Gamma_W<=8+34A^2+16AX`.

For B>=N/4 this is bounded by `50(1+AX+A^2)<=200GW`. For B<N/4, `A/X<=delta0/rho<=5delta0` when A>0 (A=0 is immediate), so `A^2<=5delta0 AX`. Then `8+(16+170delta0)AX<=198+50AX<=200GW`. Hence Gamma_W<=200GW everywhere in the claimed region.

For Q=exp(-W/400), use the entire finite mark z=delta W, not a differential approximation. Since |z|<=3, Taylor's integral remainder and `exp(3/400)<=1/(1-3/400)<2` give

`exp(-z/400)-1<=-z/400+z^2/160000`.

Summing the literal generator yields

`GQ/Q<=-GW/400+Gamma_W/160000<=-GW/800<0`.

In this region W itself has positive storage: `W>=H-100H^2/N>=(9999/10000)H`. Globally W can be negative at large A; the proof does not assume global positivity or global supermartingale drift. It applies Q only during the admitted excursions, evaluates actual stop targets globally, and uses nonnegativity of Q at other outcomes.

## 5. Actual lower-H excursions, overshoots, and the event count

Put r=m0N. The service assumptions imply

`N>=12800/m0^2>=200000`, `r/2>=6400/m0>=1000`, and r/2>2.

Start with H>=M>=r. A first hit H<=r/2 must occur in an excursion that enters H<r by an actual downward crossing. Because the H mark is at most two, the entrance H is at least r-2 and strictly above r/2. Main lower/upper mass outcomes take priority if they occur on the same jump. Stop each admitted excursion at return to H>=r, a lower H hit, a main mass outcome, or its remaining deadline. Its entire pre-stop region is exactly covered by the drift/barrier theorem: r/2<H<r<=delta0 N and 3N/4<S<=2N.

At entrance, A<=H<r, so

`W_entry>=r-2-100r^2/N=r-2-100m0^2N`.

At a lower hit, the integer falling factorial is nonnegative even at A=0,1, hence `W_exit<=H_exit<=r/2`. The positive storage gap is at least

`r/2-2-100m0^2N >=(2/5)r`.

Indeed `(1/10-100m0)r>=2` follows immediately from m0<=10^-6 and N>=12800/m0^2. The +2 entrance overshoot is explicitly paid. No unsupported zero-overshoot or fluid boundary assumption occurs.

Optional stopping of the nonnegative Q, conditionally on each actual entrance history, therefore bounds that excursion's lower-hit probability by

`exp[-(W_entry-r/2)/400]<=exp(-r/1000)`.

Stopping values at return or a mass boundary need only be nonnegative. An upper-H return target can exceed the source strip; the generator inequality is not asserted after that stop. Since the total tube and its one-jump targets form a finite state set for fixed N and the horizon is finite, integrability can be justified directly or by ordinary localization.

Globally before the upper mass stop, the coefficientwise identity bound `q_all<=3S^2+1` implies `q_all<=12N^2+1<=13N^2<32N^2`. This is valid even outside the small-H strip, where Q drift need not hold. The expected total actual event count before the global stops and time h is therefore at most 32N^2h. Downward entrance crossings are a subset of these genuine events.

Index entrance times as stopping times. Conditional optional stopping at each, followed by the tower property and Tonelli over the number of actual entrances, gives

`P(lower H hit before main mass stop and h) <= E[# entrances] exp(-r/1000)`

`<=32N^2h exp(-m0N/1000)=B_pers`.

No attempt independence, deterministic number of attempts, stationary law, or hidden reset is used. Outside this error, before any main stop H>r/2 and therefore M>=H/2>m0N/4.

## 6. Acquired actual A occupation

The exact A drift is

`GA=1-A-3A(A-1)+A(C+D)+3CD-AB`.

Let x=min(C,D), y=x+t=max(C,D), t>=0, and M=A+x. Exact subtraction gives

`GA-[3M^2-A(1+6M+B)] =1+3A+2Ax+At+3xt>=0`.

Thus the displayed global lower bound (14) is correct. Since M+B<=S<=2N and N>=1, `1+6M+B<=13N`. Before the persistence/main stops, M>m0N/4, so

`GA>=(3m0^2/16)N^2-13NA`.

Stop additionally when the continuous actual occupation clock Lambda_A=int A dt hits 4N. On the event that no mass/persistence boundary occurs by h and the clock has not hit, the stopped A martingale at h obeys

`M_A(h)=A(h)-A(0)-int GA`

`<=2N-(3m0^2/16)N^2h+13N(4N)`

`=2N-75N^2+52N^2<=-20N^2`.

Here A(0)>=0 is discarded in the favorable direction. The endpoint A(h)<=2N is used only on the no-mass-exit event. Outputs at the deadline count as outputs; they are not included in this no-output event.

Every actual A jump has absolute size one. For the COMMON stopped martingale, its predictable bracket is at most 32N^2h, because rates are bounded before the upper mass stop. No future immigration or persistence-good event is used to condition a martingale inequality.

For a compensated bounded-jump martingale with jump bound b and deterministic stopped bracket v, the exponential-compensator inequality

`exp(theta z)-1-theta z <=theta^2 z^2/[2(1-theta b/3)]`

and optional stopping give `P(inf M<=-x)<=exp[-x^2/(2(v+bx/3))]`, applying the same argument to -M. Use b=1, v=32N^2h, x=20N^2. The exponent is EXACTLY

`-200N^2/(32h+20/3)`.

This proves B_A. It acquires an actual accumulated A clock; it does not assume positive A occupation from an equilibrium or deterministic ratio. The negative tail implication only applies when no other favorable/adverse stop already occurred, which is the event needed by the final decomposition.

## 7. Original immigration, actual death clock, and unused time

Internal reactions conserve S, A death decreases S by one, and immigration increases S at constant rate one. Hence along the SAME continuing process

`S(t)=S(0)+I(t)-D(t)<=S(0)+I(t)`.

This also proves nonexplosion: on any finite horizon I is finite almost surely; population then lies in a finite state set with bounded rates.

The original immigrant count over the WHOLE deterministic interval [0,h] has law Poisson(h). At theta=log2, with h<=N/32 and log2>=2/3,

`P[I(h)>N/16]<=exp[h-(N/16)log2]<=exp(-N/96)=B_I`.

The lower bound log2>=2/3 follows by integrating the tangent `1/x>=4/3-4x/9` on [1,2]. No new or independent phase immigration clock is substituted. On this event's complement, `S(t)<=5N/4+N/16=21N/16<2N` for the entire interval, excluding every upper mass exit.

If the process hits S<=3N/4 at any earlier time sigma<=h, then on the SAME immigration event its CONTINUING endpoint satisfies

`S(h)<=S(sigma)+I(h)-I(sigma)<=3N/4+N/16=13N/16`.

This pays unused physical time. It does not freeze the state at removal or assume the total cannot rise afterward. A separately admitted initial S<=3N/4 can be handled by this same endpoint calculation, with immigration paid, without requiring the M condition.

Otherwise there has been no lower mass hit. Outside B_I there is no upper mass hit. Outside B_pers there is no lower H hit before h. Outside B_A the actual continuous clock int A dt must therefore reach 4N by h. Let theta_A be its first such hit. The exact random-time-change representation is

`D(theta_A)=Y_D(4N)`

for the original unit-rate Poisson death clock. This does NOT assert a Poisson law conditional on a random occupation path. Pathwise identity at the deterministic internal-clock value 4N is enough. Survival at theta_A and I(h)<=N/16 require

`D(theta_A)=S(0)+I(theta_A)-S(theta_A)<5N/4+N/16-3N/4=9N/16<2N`.

Thus the remaining bad event is contained in `{Y_D(4N)<2N}`, regardless of correlations between the death process and its compensator. Chernoff at log2 gives

`P[Poisson(4N)<2N]<=exp[-2N(1-log2)]<=exp(-N/2)=B_D`.

The last inequality uses log2<3/4, certified for example by `exp(3/4)>1+3/4+(3/4)^2/2+(3/4)^3/6>2`.

Consequently any bad endpoint S(h)>13N/16 requires at least one of the four explicitly priced events B_pers, B_A, B_D, B_I. This proves the stated service. Conditional entrance bounds, martingale bounds, and the original future immigration event are only intersected after their valid unconditional/past-conditioned estimates; no illegal future-event conditioning is used.

## 8. Scope, explicit replacement potential, and costs

All constants of THIS service are explicit. In particular, m0=delta/2 gives h=1600 delta^-2 and N>=51200 delta^-2 exactly. The result no longer needs an interior ODE attraction constant or an unevaluated c(epsilon), n0(epsilon). That statement is about the present service only; replacing an earlier consumer still requires its own exact composition proof, including original reference N, entrance mass <=5N/4, M>=m0N, time h, numerical errors, and any unused time.

A mere sqrt(N)-scale seed generally cannot be inserted as an N-dependent m0 proportional to N^-1/2 while retaining N>=12800/m0^2; that condition must be checked literally. The allowed endpoint is relative to N, not necessarily a fractional decrease relative to S(0). These are receiving boundaries, not defects in the source theorem.

The proof uses finite rational geometry, explicit exponential/Poisson inequalities, and exact count martingales. It is not a production parser, numerical probability enclosure API, or unit-cost exponential algorithm. Ordinary numerical evaluation still needs precision/work budgets. The h and N constants can be enormous; no practical speed, physical preparation/calibration, changed-rate operation, arbitrary-network theorem, or publication claim is acquired.

## 9. Independent diagnostics and immutable replay

The independent script separately enters all twelve literal increments and rates and imports no author code. It verifies the full polynomial identities, Hessian rank/norm formula, global origin/axis and A=0/1 phase marks, actual one-jump rational curvature, both B cases, exact GW/variance inequalities, and service-scale/clock/endpoint constants. On selected states it also directly encloses the full GQ using outward rational Taylor exponentials, rather than merely testing the derived quadratic envelope.

The final complete run passed 553,035 exact assertions: 243 origin/small states, 11,840 source-region states, 127,538 enabled region marks, 320 direct outward exponential-generator cases, and four exact service parameter choices, including the intended tiny-delta substitution. These are finite supporting checks, NOT proofs of optional stopping, global event counting, or the endpoint decomposition; those arguments are supplied above.

The exact author checker was replayed only in `author_replay/` and its report matched the frozen report byte-for-byte (3,287 states, 33,906 marks). All four original files are read back unchanged. The initial independent harness used integer true division in one exponent comparison; the resulting failed run is preserved under check_history_v0. Replacing it with Fraction and rerunning the whole suite produced the accepted exact result. No source theorem defect was found or hidden, and no author/previous accepted source was edited. No new external source, installation, or retrieval was used.
