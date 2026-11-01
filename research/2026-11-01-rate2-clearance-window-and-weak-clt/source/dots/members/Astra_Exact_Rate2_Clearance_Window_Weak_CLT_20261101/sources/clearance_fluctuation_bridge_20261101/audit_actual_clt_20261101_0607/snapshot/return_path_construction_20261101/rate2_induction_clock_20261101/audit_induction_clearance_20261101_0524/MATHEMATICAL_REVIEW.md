# Independent review: corrected finite-level clock and actual clearance continuation

## 0. Verdict, inputs, and separation of boundaries

**Both mathematical components PASS, without correction to either author source.** The accepted exact sources are:

- `FINITE_LEVEL_CORRECTED_CLOCK.md`, SHA256 `e0700bad37717a38976f295049a8d2cb1120aeb155c343783780d6b201f20c9d`;
- `ACTUAL_CLEARANCE_WINDOW_AND_OCCUPATION.md`, SHA256 `0eeb311064eaaad654d69ada711e22d26b4e8622b38d15e3a3998bcfbae1bd4d`.

The first source earns a full-process finite-level hitting window and genuine dyadic entrance, by a paid coupling to a six-channel retained chain. The second source separately earns the actual 15/16 clearance window, the two occupation outputs, and the first-passage LLN. The second result is an ANALYTICAL finite-N certificate with the interior constants c(epsilon), n0(epsilon) still unevaluated. It is not an executable numerical admission, a practical bound, or a point-mass approximation in CDF/KS/total-variation distance.

N is an integer because the literal initial state is `(0,N,1,1,0)`. Its true initial total is N+2. Reference N stays fixed in F, all dyadic bands, and every error expression. K may be a real admitted threshold; integer count crossings retain their +1 overshoots. The symbol S0=3 in the finite-level proof is a TIME-HORIZON CONSTANT, not the initial population N+2 used by the continuation.

Exact dependency gates were read and bound: the conditional dyadic source `0ddcfb78...8775e0a2`, its independent receipt `b96a909e...487dd0`, review `46e2267d...40272`, and receiving addendum `f312ac1f...2222f5`; the interior source `a8e0bd38...a1cf` and independent receipt `3f03ed19...333f`; and the deterministic scalar proof `6de845b2...7b237` with independent receipt `cd479dd4...af723`. Full hashes are in INPUT_BINDINGS.json. The 18-payload dyadic audit, eight-file scalar freeze, 18-file scalar receipt bindings, and three interior receipt payloads were hash-read back. The scalar numerical solve was not redundantly rerun: no numerical value of s_* is needed for this join.

## 1. Actual model, retained invariants, and omitted-channel coupling

All twelve actual directed channels use falling factorial A(A-1), not A^2/2. Only CD->AE has coefficient two. The six retained channels are immigration, AB->CD, CD->AB, CD->AE, AE->CD, AE->2A. The omitted set is exactly A death, the three 2A exits, and AC/AD->2A. Nothing is silently omitted from its price.

Let I count immigration, R_ct count AE->2A, and S_ct count AE->CD in the retained chain. Direct marks of each retained reaction give

`C-D=0`, `L=A+C=A+D=1+I+R_ct`,

`B=N-I-2R_ct+A-E`.

The retained L has only 0 or +1 jumps. Start at A=0, C=D=1, E=0. Put T=N^(1/5), p=K+1, q=2sqrt(K+1)+1, H=p+q+1. Stop at 3T, first L>=KT, or first E>=2sqrt(K+1)T^3, with an L hit taking priority over a simultaneous E hit. The pre-stop region AND one-jump targets satisfy A,C,D<=pT and E<=qT^3. The invariant bounds I+2R_ct<=2L give

`B>=N-2pT-qT^3>=N/2`.

For example T^2>=16H, T>=1 imply 2p/T^4+q/T^2<=3/16<1/2. B is not held fixed; this is a received lower bound on its actual retained value.

Summing all retained A marks gives `L_ret A=1+3CD-AB=1+3C^2-AB`. The omitted actual intensity is

`q_rem=A+3A(A-1)+A(C+D)<=(1+5pT)A`.

Stopped Dynkin, A(0)=0, and nonnegative terminal A imply

`E int AB <=3T+9p^2T^3<=12p^2T^3`.

Since B>=N/2, this yields `E int A<=24p^2/T^2=:h0`; also `E int AE<=qT^3 h0=24p^2qT=:g0`. The expected omitted hazard is at most `(1+5pT)h0<=144p^3/T`. These are stopped expectations; they do not control unrestricted full-process occupation.

A common-clock construction couples the literal full and retained chains until the first omitted mark. Along the stopped retained trajectory, its conditional occurrence probability is at most its integrated omitted intensity, so the unconditional failure price is at most 144p^3/T. On its complement the same actual path has no A death, no other omitted mark, and C-D=0 up to the retained stop. Rates after coupling failure are irrelevant to the claim. Both chains are nonexplosive: total is bounded by N+2 plus the constant-rate immigration count on every finite horizon.

## 2. Corrected F: exact retained identity and all residual prices

Use the SAME global `F=L-3E^2/(4N)+AE/N`. Its six retained marks are:

| Channel | delta F |
|---|---|
| immigration | 1+E/N |
| AB->CD | -E/N |
| CD->AB | E/N |
| CD->AE | (A-E/2+1/4)/N |
| AE->CD | (E/2-A+1/4)/N |
| AE->2A | 1+(5E/2-A-7/4)/N |

Their literal rate-weighted sum is

`L_ret F=1+E/N+CD/(2N)+2ACD/N + AE[1+(3E-2A-3/2-B)/N]`.

The cancellation is exact and uses actual B, not a fast-A equilibrium. The invariant gives

`N-B+3E-2A-3/2=I+2R_ct+4E-3A-3/2`,

whose absolute value is at most `5HT^3` on the stopped pre/target domain. The four drift-error classes, after division by T, have expectations bounded respectively by

`3q/T^2`, `3p^2/(2T^3)`, `48p^4/T^6`, `120Hp^2q/T^2`.

Weakening the second and third denominators to T^2 and expanding the positive polynomial envelope gives

`E[(1/T)int |L_ret F-1|] <=300H^4/T^2`.

The initial F/T is exactly 1/T. It is not dropped.

The immigration and AE->2A marks have absolute value <=2. Each of the other four marks is at most H/T^2. The admitted T^2>=16H bounds E/N and A/N, with room for all one-jump constants. The expected compensators for AB, the two CD exits, and AE->CD are at most `12p^2T^3`, `9p^2T^3`, and g0. Thus

`E<M_F> <=12T+4g0+(H^2/T^4)(21p^2T^3+g0) <=192H^5T`.

The last inequality follows coefficientwise from

`64H^5 >=4+32p^2q+7H^2p^2+8H^2p^2q`.

The bracket is order T after normalization of the frequent small marks; bounding every fast-event mark by order one would not earn this result.

For the stopped martingale, the L2 maximal inequality gives E sup|M_F|^2<=4E<M_F>. At tolerance aT/8 its probability cost is `49152H^5/(a^2T)`. Markov on the NONNEGATIVE initial-plus-absolute-drift error at a/8 costs `8/(aT)+2400H^4/(aT^2)`. Consequently the source's bound for `sup|F(sT)/T-s|>a/4`, with supremum only up to the stopped time, is valid. All stopping jumps are included in the bracket and terminal domain bounds.

## 3. E-counter residual, with actual E losses paid

Let J count CD->AE. Exactly `E=J-R_ct-S_ct`, and J has compensator `2 int C^2`. Define `e_N=E(sT)/T^3`, `l_N=L(sT)/T`, and `w(s)=2 int_0^s l_N(u)^2 du`. Then

`eta_N=e_N-w=M_J/T^3+(2/T^3)int(C^2-L^2)-(R_ct+S_ct)/T^3`.

Here C=L-A and `0<=L^2-C^2<=2pT A`. The expected absolute integral replacement error is therefore at most `96p^3/T^4`; the expected E-loss counter contribution is at most `48p^2q/T^2`. The martingale maximal second moment is at most `24p^2/T^3`.

At epsilon=a^3/12, splitting the tolerance into epsilon/2 for the martingale and epsilon/2 for the nonnegative remaining error gives

`P(sup|eta_N|>epsilon) <=13824p^2/(a^6T^3)+3456H^3/(a^3T^2)`.

The sign of the losses is not used to pretend they vanish: their full expected count is charged. Combining omitted hazard, F errors, and E errors, using H>=1, a<=1, T>=1, the total coefficient against `H^6/(a^6T)` is

`144+49152+8+2400+13824+3456=68984<100000`.

This proves the stated B_clock. It is an upper bound, not an assertion that the bound is small at every admitted N.

## 4. Pathwise scalar comparison and the level window

The accepted ordinary scalar solution satisfies `l=s+3e^2/4`, because the derivative of l-3e^2/4 is one. Hence `e'=2(s+3e^2/4)^2`. It is nonnegative, increasing, and `e(s)>=2s^3/3`. If it exists to 1, then e(1)>=2/3 and e'>=(9/8)e^4 force divergence by 2; otherwise it already diverges earlier. Every finite level l=K is crossed at a unique s_K<2. This mathematical fact, not the optional numerical enclosure, is what the proof uses.

On the two residual good events, the admitted `T^2>=4pq/a` gives `0<=AE/(NT)<=a/4`. Therefore

`l_N=s+3e_N^2/4+xi_N`, `|xi_N|<=d=a/2`,

`e_N=w+eta_N`, `|eta_N|<=epsilon=a^3/12`.

Both l_N and e_N are nonnegative. The coordinate e_N may decrease; the proof correctly uses the absolutely continuous, nondecreasing w instead.

For the upper comparison, z=w+epsilon is nonnegative and >=e_N. Almost everywhere,

`z'<=2[s+d+3z^2/4]^2`, `z(0)=epsilon`.

The shifted scalar y(s)=e(s+a) starts above epsilon because e(a)>=2a^3/3, and its drift is at least the displayed right side since a>=d. Scalar comparison on every interval where e(s+a) exists gives e_N(s)<=e(s+a). Using the l identity then gives l_N(s)<=l(s+a).

For the lower comparison,

`w'>=2[(s-d)+3 max(w-epsilon,0)^2/4]_+^2`.

If the retained path persists to s=a, integration of the weaker derivative `2(s-d)_+^2` gives `w(a)>=(2/3)(a-d)^3=epsilon`. For s>=a within the stopped path, z=w-epsilon is nonnegative and

`z'>=2[s-d+3z^2/4]^2>=2[(s-a)+3z^2/4]^2`.

Since z(a)>=0=e(0), scalar comparison gives e_N(s)>=z(s)>=e(s-a), and then l_N(s)>=l(s-a). Before a the required lower bound is simply l_N>=0=l(0). If the path stops before a, the lower comparison after a is not invoked. These are standard absolutely continuous scalar differential inequalities; no finite variation of eta_N or monotonicity of e_N is assumed.

An E-cap exit without an L hit is impossible on the good event. At that exit `3e_N^2/4>=3(K+1)`, but the corrected identity, l_N<K, `F/T>=s-a/4`, and `AE/(NT)<=a/4` give `3e_N^2/4<=K+a/2`. L takes priority if both boundaries occur together. The target and all residuals include the stopping jump.

An L hit before s_K-a would contradict the upper comparison at an argument strictly below s_K. If no L hit has occurred by s_K+a, the lower comparison there gives l_N>=l(s_K)=K, a contradiction. This time is less than 3. Thus `(s_K-a)T<=t_K<=(s_K+a)T`, with a negative lower endpoint replaced by zero. Crucially the last argument uses e(s-a), not e(s+a) after blow-up. No compact approximation is extended through the scalar explosion.

## 5. Fast-A cap and genuine actual dyadic entrance

The retained A upward and downward intensities are `1+3C^2+AE` and `AB+AE`. Using exp(1)-1<2 and 1-exp(-1)>1/2,

`L_ret exp(A)/exp(A) <=2+6p^2T^2+A(2qT^3-N/4)`.

T^2>=16H implies 2qT^3<=N/8. T^3>=64p^2 implies `N/8>=8p^2T^2>=2+6p^2T^2`. Hence this exponential drift is nonpositive for every integer A>=1 on the common stopped domain.

A starts at zero. Each actual excursion from 0 to 1, stopped at return to zero, cap ceil(KT/64), or the common stop, reaches the cap with conditional probability at most exp(1-KT/64), by optional stopping of exp(A). The count of such entries is bounded by the full actual upward count, whose expected compensator is at most

`3T+9p^2T^3+g0 <=36H^3T^3`.

Conditional expectation over the actual entrance stopping times, without independence between excursions, yields exactly B_A. This pays the A supremum through the random L hit, including a terminal cap jump; it is not a fixed-time sample or stationary-fiber estimate.

On the combined good event the literal full process coincides with the retained process until its actual t_K. Thus there has been no A death or other omitted channel, C-D=0, and KT<=L_full(t_K)<=KT+1. The cap gives A<ceil(KT/64), stronger than A<=KT/32+1. The F residual and t_K/T<2+a imply |F|<=4T<=KT/8.

For the E bounds, solve the corrected identity:

`E^2/(NKT)=(4/3)[L/(KT)+AE/(NKT)-F/(KT)]`.

The lower bound is `(4/3)(1-4/K)`. For the upper bound one must use the stronger available `F/T>=s-a/4>=-a/4`, not merely |F|<=4T. With L<=KT+1 and AE/(NT)<=a/4 this gives an upper bound `(4/3)[1+(1/T+a/2)/K]<=(4/3)(1+2/K)`. For K>=32 these lie in `[1,(13/10)^2]`. Every non-mass dyadic entrance hypothesis is therefore actually earned. The reference N and actual entrance are unchanged.

## 6. Continuation: original headroom and extracted pathwise occupation

Now use delta=10^-100, Cstar=3*10^12, epsilon_int=delta/4, `h_delta=40000 sqrt(delta)`, and `D_K=32T/K^(3/2)`. Admit KT<=delta N and `(1-delta)N>=n0(epsilon_int)` in addition to all finite-level conditions.

On the finite-level good event, t_K<3T and no A death has occurred. The true total is therefore `S(t_K)=N+2+I(t_K)>=N+2`. The clearance target `15(N+2)/16` has not yet been reached. Use ONE original rate-one immigration counter over the deterministic horizon [0,4T+5]. The event

`I(4T+5)<=delta N/2-2`

implies `S(t)<=N+2+I(t)<=(1+delta/2)N` throughout that horizon, regardless of deaths. It gives starting headroom and excludes every upper dyadic band exit. Its complement is exactly B_imm as stated. Conditional stage/interior estimates are never conditioned on this future event; it is intersected after applying their past-measurable admissible-entrance bounds.

The dyadic source's headline conclusion alone would NOT supply an occupation clock. The proof, however, stops the common process at `H_j=int_stage A dt=Hbar_j=10^4 sqrt(m_j/N)` and bounds that clock exit using the A martingale. Its SAME joint good event excludes this clock exit, excludes the other auxiliary exits, controls the terminal jump, and forces an L hit or actual band exit by the deadline. The sum of all failures is the same <16 exp(-m_j/Cstar), not an additional unpriced event. The independently reviewed derivation explicitly retains this construction. Thus the stronger proof-level assertion `int_stage A dt<=Hbar_j` is legitimately received here.

At actual continuing entrances m_j=2^j KT, apply the conditional estimate; no state or reference N resets. Band exit takes priority over simultaneous L success. Only an in-band success supplies the next entrance. Stop the entire composition at the FIRST actual L>=delta N, a band exit, or an exceptional stage; a final partial stage may be obtained by truncating the same good-event estimates. The deadline sum is

`sum 16sqrt(N m_j)/m_j^2 <32sqrt(N)/(KT)^(3/2)=D_K`.

The conditional failure sum is at most `32 exp(-KT/Cstar)=B_stage`; KT/Cstar>=1 on the stated admission range, so the geometric exponential bound is valid. For all active stages m_j<delta N, the pathwise occupation sum is

`10^4 sum sqrt(m_j/N) <=10^4 sqrt(delta)/(1-2^(-1/2)) <h_delta`.

The occupation statement includes any last partial stage and the actual terminal jump of the stopped process. It is not inferred from the success OR-event or an unconditioned average.

## 7. Tiny lower-band exit: actual death pricing, not false clearance

The lower band is `(1-delta)N`, NOT .75N. It is in fact above `15(N+2)/16` at the admitted N. A lower-band exit does not itself earn the clearance target.

Since the mesoscopic entrance has total at least N+2, a later actual `S<(1-delta)N` requires more than delta N+2 deaths after that entrance, even before adding later immigration. In particular it requires at least ceil(delta N) actual A-death events.

Conditionally on an admitted actual entrance history, the strong Markov random-time-change construction represents the future death count as `Y_D(int A dt)` for a unit-rate Poisson clock. This restarts driving-noise representation only, not state, rates, or reference N. On the event that all stage clocks are good, the compensator through the terminal outcome is <=h_delta. Thus a lower-band exit on that event implies `Y_D(h_delta)>=ceil(delta N)` by pathwise monotonicity. The random compensator may depend on Y_D; no independence between them is asserted or needed. Consequently this entire adverse event is charged by

`B_band=P(Poisson(h_delta)>=ceil(delta N))`.

No optional random-mean Poisson distribution is claimed. The equivalent counting-process exponential argument gives the same tail domination. This explicitly closes the lower-band loophole instead of promoting a tiny delta loss to 15/16 clearance.

## 8. First macro crossing, actual-total interior admission, and clearance

Outside the charged events the first L>=delta N occurs by t_K+D_K, with actual total in the original band. For a last active stage m_j<delta N, its post-jump bounds give

`A<=m_j/16+1`, `|C-D|<=m_j/16+1`, `|F|<=5m_j/32`.

Because this is a first crossing from below, `delta N<=L<=delta N+1`. Therefore

`C,D >=L-A-|C-D|/2 >=(29/32)delta N-3/2 >=delta N/2`.

From `3E^2/(4N)=L+AE/N-F` and AE>=0, one gets `E>=sqrt(delta)N/2` with substantial slack. The stage tube, including its post-jump allowance, gives `E<=2sqrt(delta)N+1`. Also `A+C+D=2L-A<=2delta N+2`. The lower total band then yields

`B>=(1-3delta-2sqrt(delta))N-3>=N/2`.

These are first-actual-crossing bounds, not assertions for an arbitrary already-macro starting state. In fact the admitted finite-level conditions force `KT<=sqrt(N)/8<=delta N/8` for N>=10^200, so KT+1<delta N here; the source's optional initially-macro branch is unnecessary on this admission domain. Even that branch is not used to smuggle an arbitrary initial-state overshoot bound.

Let n be the ACTUAL total at the macro entrance. Then `(1-delta)N<=n<=(1+delta)N`, and the four displayed fractions imply B,C,D,E>=epsilon_int n. A may be zero, as the interior theorem permits. The admitted `(1-delta)N>=n0(epsilon_int)` receives the exact size threshold.

Apply the accepted interior theorem conditionally at this genuine stopping entrance. It returns `S(u_macro+5)<=7n/8` except with probability at most `exp[-c(epsilon_int)n]<=B_int`. No future immigration event is used to condition this estimate. Since

`(7/8)(1+delta)N <15(N+2)/16`,

this endpoint inequality ensures the actual target has been hit by then. The process may continue afterward; no unused-time monotonicity is assumed. The deadline is at most `(s_K+a)T+D_K+5`, and is within 4T+5 because t_K<3T and D_K<T.

The lower hitting-time endpoint is received separately: no death before t_K means no clearance before t_K. Thus the actual clearance window holds except on the sum

`B_total=B_clock+B_A+B_imm+B_stage+B_band+B_int`.

These are union costs for dependent actual events, not factors from independence. Clip the resulting probability lower bound at zero. The statement is valid analytically even if its displayed error is vacuous.

## 9. Separate occupation outputs

The early retained estimate `E int A<=24p^2/T^2`, stopped at its common stop, gives by Markov a cost `B_occ_early=24p^2/T` for exceeding 1/T. On the already coupled finite-level good event this is the actual integral up to t_K. No expectation of the unrestricted full process is inferred. Together with all good stage clocks it gives

`int_0^u_macro A dt<=1/T+h_delta`.

Conversely, at actual clearance from initial total N+2, at least `ceil((N+2)/16)` A deaths have occurred, because immigration only increases total. If the actual death compensator up to a finite clearance time were <=(N+2)/32, pathwise monotonicity of the ORIGINAL death clock would imply

`Y_D((N+2)/32)>=ceil((N+2)/16)`.

Therefore the undesired event has probability at most B_occ_late as stated. With theta=log2, the ordinary Poisson upper-tail bound is

`B_occ_late<=exp[-(2log2-1)(N+2)/32]`.

This bound does not need a deterministic or independent compensator. Combining the window, macro-entry upper occupation, and strict clearance lower occupation costs at most `B_total+B_occ_early+B_occ_late`. Neither occupation assertion is an unrestricted expectation theorem.

## 10. Order of limits and the actual first-passage LLN

At s_K, `e(s_K)^2=(4/3)(K-s_K)>=(4/3)(K-2)`. Since e'>=(9/8)e^4, the remaining deterministic time is at most

`8/[27 e(s_K)^3] <=sqrt(3)/[9(K-2)^(3/2)]=beta_K`.

This proves `0<s_*-s_K<=beta_K`. The identity is about the deterministic scalar only; its independently certified decimal enclosure may be attached separately but is not necessary here.

For each FIXED K>=10^40 and FIXED 0<a<=1/4, all algebraic admission conditions eventually hold as N grows. The unevaluated but finite n0(epsilon_int) is also eventually exceeded. B_clock tends to zero as T^-1; B_A has an exponentially decaying KT term dominating its polynomial prefactor; B_stage tends to zero; the original immigration mean is O(T) while its threshold is order N; the band-death Poisson mean h_delta is fixed while its threshold tends to infinity; and B_int tends to zero because its supplied c(epsilon_int)>0. The ordinary Poisson tail limits can be seen directly from their Chernoff bounds. Thus B_total->0 for each fixed K,a.

Divide the accepted window by T. Its lower endpoint is at least `s_*-beta_K-a`; its upper endpoint is at most `s_*+a+32/K^(3/2)+5/T`. For any desired error choose a large but FIXED K so beta_K and 32/K^(3/2) are small, then choose a>0, then take N sufficiently large. This is the iterated order 'N first at fixed K, then K', not a hidden diagonal K(N) use of an unquantified limit. It proves

`tau_clear/N^(1/5) -> s_* in probability`.

It does not assert no deaths after scalar blow-up, approximation of a continuous finite-N CDF by a point mass, a CLT, relative tail control, or a compressed conditional exit kernel. The actual first-passage target and process have remained the same throughout.

## 11. Numerical/cost gates and audit evidence

The constants K>=10^40 and delta=10^-100 are retained literally. The probability prefactor is polynomial in K and a^-1 but can be enormous; admission alone does not make B_total<1. Finite numerical evaluation requires certified algebraic roots, exponentials/Poisson tails, any desired scalar numerical certificate, and acquired interior c(epsilon_int), n0(epsilon_int). Those last two numerical constants remain UNEVALUATED. Their existing theorem supplies existence, which suffices for the mathematical LLN, not a ready numerical validator or claimed runtime. No practical clock or physical acquisition claim is accepted.

The independent checker separately enters the full twelve and retained six literal increments, computes exact retained identities, verifies all retained invariants, polynomial drift/bracket/count envelopes, scalar comparison constants, fast-A margins, reference-population and death rounding, and rational outward geometric sums. It imports no author code. The final run passed 21,570 exact assertions, with 3,904 enabled retained-jump cases, four large exact admitted parameter cases, and 1,132 received geometric stages. Finite checks support, rather than replace, the stochastic and comparison proof above.

Both frozen author scripts were actually replayed in an isolated copied sibling layout; both reports matched byte-for-byte. The original sources and earlier gates were not edited. The first independent diagnostic script had an audit-only Python integer true-division overflow on a 400-digit test; the failed bytes/logs are preserved in check_history_v0, and both such comparisons were corrected to Fraction before the complete successful rerun. No author theorem defect was found or concealed. No new external source was retrieved.
