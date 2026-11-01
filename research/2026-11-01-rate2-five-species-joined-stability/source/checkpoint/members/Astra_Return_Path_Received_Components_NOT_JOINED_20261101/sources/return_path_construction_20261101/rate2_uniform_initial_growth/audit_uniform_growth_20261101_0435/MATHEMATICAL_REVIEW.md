# Independent review: uniform full-generator initial growth

## Verdict and exact boundary

PASS for the pointwise generator inequality and the stated first-hit/exit law, at the exact author theorem SHA256 `90a80f12bfc045350b5254a4c8d731f506da5520ee161ccd9e7cbb11df82329e`. No source correction or constant change is required. This is a mathematical component acceptance, not an executable receiving contract and not an activation, population-removal, recurrence, or stationary-moment theorem.

The full state is a finite vector `(A,B,C,D,E)` of nonnegative integers. The integer reference `N` is fixed throughout a run; it is not the current total population and need not equal the initial population. The theorem applies uniformly to every such state satisfying `B>=N/2` and `M<m`, with integers `N,m>=1` and `N>=10^8(m+1)^2`. In particular, it imposes no upper bound on B, R, or current total. That unbounded-state feature was checked in the proof, not inferred from finite tests.

Define `M=A+min(C,D)`, `R=C+D+E`, `u=M+1`, `phi=clip_[0,1]((96-R/u)/48)`, `h=1+16 A^2 phi/N`, and `V=2^(-M)h`. The same V, without killing or resetting, is evaluated at every enabled transition target.

## 1. Exact actual channels, including all corners of min

The propensities below use falling factorials. The three 2A propensities are `A(A-1)`, with no factor 1/2. CD->AE has rate 2CD; no other channel receives that factor.

| Channel | Rate | delta A | delta R | delta M |
|---|---:|---:|---:|---|
| 0 -> A | 1 | +1 | 0 | +1 |
| A -> 0 | A | -1 | 0 | -1 |
| 2A -> AC | A(A-1) | -1 | +1 | 0 if C<D; otherwise -1 |
| AC -> 2A | AC | +1 | -1 | 0 if C<=D; otherwise +1 |
| 2A -> AD | A(A-1) | -1 | +1 | 0 if D<C; otherwise -1 |
| AD -> 2A | AD | +1 | -1 | 0 if D<=C; otherwise +1 |
| 2A -> AE | A(A-1) | -1 | +1 | -1 |
| AE -> 2A | AE | +1 | -1 | +1 |
| AE -> CD | AE | -1 | +1 | 0 |
| CD -> AE | 2CD | +1 | -1 | 0 |
| CD -> AB | CD | +1 | -2 | 0 |
| AB -> CD | AB | -1 | +2 | 0 |

These are finite differences at integer states, not derivatives of min. At C=D both outward C/D arms decrease M and both arm returns preserve it; at adjacent unequal counts the displayed weak/strict conditions give the correct transition to equality. Every enabled target remains a nonnegative count state.

The negative-M rate is therefore

`q_- = A+3A(A-1)` when C=D, and `q_-=A+2A(A-1)` otherwise.

For integer A>=0, `A^2<=q_-<=3A^2`. The lower bound uses integrality: for A>=1, `2A^2-A>=A^2`; at A=0 everything is zero. This is not an assertion for arbitrary real A in (0,1).

## 2. One-jump h bounds and negative/positive M marks

On the open domain, integer M satisfies M<=m-1 and A<=M. Every actual jump changes A by at most one and M by at most one. Thus, both before a jump and at its enabled target, `0<=A<=m`, and

`1<=h<=1+16m^2/N < 1+16/10^8 < 101/100`.

A negative-M jump has A'=A-1, R'>=R, M'=M-1. It necessarily starts with M>=1, so `R'/(M'+1)>=R/(M+1)`. Clipping is monotone, hence phi'<=phi and `(A-1)^2 phi'<=A^2 phi`. Therefore h'<=h even if the jump crosses either cutoff corner.

Normalize each generator summand by the strictly positive `2^(-M)` at the source. A negative-M jump has mark `2h'-h<=h<=101/100`. A positive-M jump has mark `h'/2-h<=101/200-1=-99/200`. These bounds are for the full target, including targets outside the domain. In particular the positive jump bound pays for immigration and includes any adverse change of cutoff caused by increasing M.

For zero-M jumps, all channels with A decreasing and R increasing have nonpositive h change. Thus AB->CD and AE->CD are favorable; the zero-M outward C/D arms are also favorable. The only potentially positive zero-M contributions are CD->AB, CD->AE, and whichever C/D returns preserve M.

## 3. Full positive zero-M phase cost, including clipping transitions

For one of the remaining zero-M jumps, A'=A+1 and R'=R-j with j in {1,2}. M is fixed. The clipped affine function of R is globally Lipschitz with constant `1/[48(M+1)]`, including both corners. Let phi' be its target value. Then

`(A+1)^2 phi' - A^2 phi = (2A+1)phi' + A^2(phi'-phi)`

`<=2A+1+A^2/[24(M+1)] <=3A+1`.

The identity uses phi' on the first term, so no extra `(2A+1)(phi'-phi)` term is lost. The last inequality follows from A<=M and also holds at A=0.

If this phase change is positive, then phi'>0. Consequently `R-j<96(M+1)` and hence `R<=98(M+1)`. For such a source, `CD<=(C+D)^2/4<=2401(M+1)^2`. The two CD-return rates sum to 3CD, not 2CD; both C/D arm-return rates together are at most `A(C+D)<=98A(M+1)`. Thus the total relevant rate is at most

`7203u^2+98Au`, where u=M+1.

This statement does not erroneously impose an R bound on all states: if no phase change is positive, its positive contribution is zero. If any is positive, the bound holds at the common source and prices all such channels.

For integer A>=0, `3A+1<=2(A^2+1)` and `A(3A+1)<=4A^2`. Therefore the total positive zero-M contribution, normalized by `2^(-M)`, is at most

`16/N [14406u^2(A^2+1)+392u A^2]`

`<=236768u^2(A^2+1)/N`

`<=240000(m+1)^2(A^2+1)/N`

`<=0.0024(A^2+1) <=(A^2+1)/100`.

Here u>=1 and u<=m; using m+1 only weakens the bound. The 240000 coefficient therefore has slack, and the source's final 1/100 allowance is even weaker than the direct consequence 3/1250. This pays all cutoff-crossing and reverse-arm contributions, rather than asserting they have a favorable sign.

## 4. Uniform core and outer payments

### Core: R<=48(M+1)

Here phi=1. AB->CD preserves M, decreases A, and does not increase phi. Its normalized phase mark is at most `-16(2A-1)/N`. For A>=1, its actual rate AB and B>=N/2 yield

`AB[-16(2A-1)/N] <=-8A(2A-1)<=-8A^2`.

For A=0 the rate and reserve are both zero. This is a true channel payment even if the target crosses out of the core; no favorable-side differentiability is assumed. Discarding other negative contributions but retaining immigration, all negative-M jumps, and the full positive zero-M allowance gives

`LV/2^(-M) <=-99/200-8A^2+(101/100)3A^2+(A^2+1)/100`

`=-97/200-(124/25)A^2 <=-97/200<-12/25`.

### Outer region: R>48(M+1)

At least one satellite C,D,E is strictly greater than `16(M+1)`. If E is chosen, AE->2A is a positive-M channel. If C (respectively D) is chosen instead, C>D (respectively D>C), because the smaller of C,D is at most M and could not equal this maximum. Its actual C/D arm return is therefore a positive-M channel. Ties involving E may simply choose E.

The selected rate is `A max(C,D,E)`. For A>=1 it is greater than `16A(M+1)>=16A(A+1)>12A^2>=4q_-`; for A=0 the required non-strict inequality is 0>=0. This selected rate is separate from immigration. Using both payments and the full phase allowance,

`LV/2^(-M) <=-99/200-[4(99/200)-101/100]q_-+(A^2+1)/100`

`<=-97/200-(24/25)A^2 <=-97/200<-12/25`.

This is uniform even for arbitrarily large R or B. There is no averaging, stationary fast-A fiber, frozen B reservoir, or independent-attempt assumption.

Finally `h/4<=101/400<12/25`; hence both cases imply `LV<=-V/4`. The claimed inequality is substantially weaker than the earned normalized estimate. The denominator N remains the same reference integer in every source and target evaluation.

## 5. Nonexplosion, actual stopping, and the exponential moment

Let `S=A+B+C+D+E` be the actual total. Every internal channel conserves S; immigration increases S by one at constant rate 1 and A death decreases it by one. In a standard Poisson-clock construction, until any proposed explosion time, `S_t<=S_0+P_t` for a unit-rate Poisson immigration clock. On a finite horizon P has finitely many jumps. On a finite population set there are finitely many states and the sum of the 12 polynomial propensities is bounded. Infinite jumps cannot then accumulate. This establishes finite-horizon nonexplosion separately for every finite initial state, without an upper bound involving reference N.

Define the actual stopping time

`sigma=inf{t>=0: M_t>=m or B_t<N/2}`.

Only AB->CD decreases B; it decreases B by one and preserves M. A positive-M jump has size exactly one. Since the process starts with integer M<m, before sigma M<=m-1 and at sigma M<=m. This also holds when N is odd, where the first B exit is from ceil(N/2) to ceil(N/2)-1. Both events are legitimate outputs of this theorem. A target hitting a real output and an auxiliary localization boundary simultaneously is retained as that output, never suppressed or reset.

Thus, at every `t wedge sigma`, including the actual terminal target,

`V(X_{t wedge sigma})=2^(-M)h >=2^(-m)`.

This is the essential lower bound, with the correct sign. It does not rely on sigma already being finite. It also remains true at localizations stopped before sigma.

For completeness, localize the nonexplosive chain on finite population sets, stopping at exit times tau_n. On each fixed time interval, Dynkin applied to the integrating factor and the full V gives

`E[e^((t wedge sigma wedge tau_n)/4) V(X_{t wedge sigma wedge tau_n})] <= V(x)`.

Before the stopping time the drift of `e^(t/4)V` is nonpositive. The factor is stopped too; no drift inequality is asserted after a domain exit. Each localized expression is integrable because time and the pre/one-jump-target state region are bounded. Nonexplosion gives tau_n->infinity; nonnegativity and Fatou give the same inequality with t wedge sigma. The pathwise lower bound then yields

`E[e^((t wedge sigma)/4)] <=2^m V(x)`.

As t increases, the left side increases to `E[e^(sigma/4)]`, interpreted as infinity on {sigma=infinity}. Monotone convergence proves both sigma<infinity almost surely and

`E[e^(sigma/4)] <=2^m V(x) <=(101/100)2^m`.

Markov's inequality gives

`P(sigma>t) <=(101/100) exp(m log 2-t/4)`.

At t=8m, log 2<1 implies the advertised weaker bound `(101/100)exp(-m)`. No exact numerical evaluation of an exponential is required by this mathematical assertion. The finite tests are not evidence of the unbounded-time optional-stopping step; the localization argument above supplies it.

## 6. Scales and interfaces not received

For fixed positive K, `m=ceil(K N^(1/5))` satisfies the condition for sufficiently large N. An explicit sufficient real threshold is `N>=[10^8(K+2)^2]^(5/3)` with N>=1: then `m+1<=K N^(1/5)+2<=(K+2)N^(1/5)` and the size condition follows. Integer rounding N upward is harmless. This is only a sufficient threshold, not an optimized or unit-cost input operation.

For `N>=4*10^8`, let `s=sqrt(N)>=20000` and `m=floor(s/20000)`. Then m>=1 and `m+1<=s/20000+1<=s/10000`, so `10^8(m+1)^2<=N`. The optional slower scale is therefore valid at its stated endpoint as well.

There is NO total-population-band stop in this theorem. The process may cross a proposed upper or lower total band before sigma and must continue until its stated output unless a later consumer separately stops and accounts for that exit. Conversely, the B-half output is internal redistribution; AB->CD conserves total, so this is not a total-population decrease certificate.

At the M output, A can still occupy a large fraction of M and E or C-D can be arbitrarily unbalanced. Neither the balanced dyadic entrance nor post-entry occupation/removal conditions are supplied. The earlier conditional dyadic-stage acceptance remains separate; multiplying or composing these theorems without a newly proved interface would be unjustified. No recurrence, invariant law, stationary moment, arbitrary-state removal law, physical implementation, or experimentally acquired intensity is accepted.

V is an explicit rational-valued expression on integer inputs. Expanding the denominator 2^M requires order-M bits in addition to ordinary input arithmetic. The author file is a finite check script, not a hardened runtime receiver or a universal arithmetic/work budget. This acceptance does not assert such an API exists, nor certify floating-point probabilities.

## 7. Independent exact checks and clean author replay

`independent_initial_growth_checks.py` imports no author code. It enters the 12 actual increments and propensities independently, checks every enabled jump, all sign groups and scalar inequalities, full normalized generator bounds, integer terminal targets, both cutoff corners and the nonsmooth min surface. It also checks odd/even reference N, arbitrarily large-scale representative B/R values, 91-digit seed coordinates, and the optional square-root scale with integer square roots.

The run passed 658,415 exact assertions over 7,360 states, including 59,532 enabled jumps and 18,394 terminal-jump checks. These are finite diagnostics, explicitly not a substitute for the uniform proof above. Fractions and integers are exact; no float, numerical fluid approximation, stochastic simulation, or author generator import was used.

The exact frozen author checker was also run only in `author_replay/`, copied from the immutable inputs. Its 6,675-state/58,680-enabled-jump report was byte-identical to the supplied report. These author counts are separate from the independent counts. All four original component files and their frozen hashes are read back by the audit verifier. No author source was modified, and no external source was retrieved or relied on.
