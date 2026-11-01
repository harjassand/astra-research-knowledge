# Independent exact receipt: finite clock endpoint receiver

Source: `../FINITE_CLOCK_ENDPOINT_RECEIVER.md`, SHA-256 `0018c24de9dfa6cf2757a42cbfd3d1b8cb7d37369f46cf2fa5e0f9fac9228919`.

**PASS as an explicitly conditional ordinary receiver. No repair required.** The inverse-clock bound, startup and cap geometry, corrector constants, two-sided Freedman inversion, original-clock non-hit contradiction, no-early-clearance argument, and conditional entropy-service join are correct. The residual, bracket and jump ceilings `r,v,j` remain unacquired. This receipt supplies no finite-N algorithm or economic/computational advantage.

## 1. Precise receiving scope

Use a successful actual startup stopping time `sigma<=800` from the raw corner, with the stated physical startup coordinates and gates. The actual Dynkin martingale is initialized at zero at sigma, as is its accumulated drift error. Take deterministic uniform nonnegative ceilings `r,v,j`, and `0<delta<1`. Their bounds must hold for the actual process stopped at the first macro cap, original time `4T`, or other admission failure, including actual terminal jumps. A budget maintained only after conditioning on future success is not received.

The aggregate `delta_adm` must cover all stated startup, original count-band, post-startup gate, target-gate and budget first failures, from original time zero. It is not merely a post-startup success-conditioned probability. This is the source's stated all-gates/all-first-failures accounting. Simultaneous adverse exits take priority, so target endpoint bounds are used only when the actual target also satisfies all their premises.

The entropy-five component is a separately received conditional future service at the actual cap state, with failure at most `delta_5`; this review checks its entrance geometry and interval join, not its internal proof. No pre-cap count event is extrapolated through that future service.

## 2. Inverse clock and corrector ceiling

The inverse flow has `L(w)>=l+3w²/4`, hence for `l>0,e>=0`,

`0<=b(l,e)<=integral_0^infinity [2(l+3w²/4)²]^-1 dw`
`             =pi/(4sqrt(3)l^(3/2))<l^-3/2`.

The coefficient and inequality are correct. On the admitted scaled state, `R=e²/l<=2` and `A<=Tl/100`, so

`AE|b_l|/(NT)`
` <=sqrt(2)/(100T²) l^(3/2) min(1,l^-5/2)`
` <=sqrt(2)/(100T²)<1/(70T²)`.

For `l<=1` the middle l-factor is at most `l^(3/2)<=1`; for `l>=1` it is `l^-1<=1`. The rational comparison is certified by `2*70²<100²`. The corrector is nonpositive because `b_l<=0`. Thus `q>=-1/(70T²)` everywhere on the admitted domain, without a lower ratio gate.

## 3. Actual startup enclosure

The startup data give `L=400`, `A<=2`, `Z=0`, and `E<=Ebar=512000000`. In particular `A/L<=1/200<1/100`. At `N>=10^20`, its upper ratio is automatically well below two: `Ebar²/(400*10^20)<2`. The source also explicitly retains the actual endpoint gates.

Join `(0,0)` to `(400/T,0)` horizontally and then to the actual `(400/T,E/T³)` vertically. The horizontal path uses the received smooth boundary extension and `-1<=b_l<=0`; no inverse division at l=0 is made. On the vertical path, `e²/l<=2<=3`, so `-6<=b_e<=0` applies throughout. Consequently

`s_*-400/T-6Ebar/T³-1/(70T²)<=q(X_sigma)<=s_*`.

Since `0<=sigma<=800`, the source's conservative quantity

`beta=800/T+6Ebar/T³+1/(70T²)`

indeed bounds `|sigma/T+q(X_sigma)-s_*|`. The actual random startup time and state remain in the identity; this calculation does not reset or replace them.

## 4. Actual cap endpoint

At an admitted L cap, `L>=N/5000`; at an admitted E cap, `E>=ceil(N/100)>=N/100` and `R<=2` imply `L>=N/20000`. Thus in either case

`l>=T^4/20000>1`.

The sharper corrector estimate in this regime is `sqrt(2)/(100T² l)`. Therefore

`|q(X_tau_cap)| <=[20000^(3/2)+200sqrt(2)]/T^6`
`                 <3*10^6/T^6=c_cap`.

The numerator equals `2000200sqrt(2)` and is strictly below three million. Every one-step cap overshoot is retained in these endpoint coordinates. Any simultaneous failure of A/L, R, imbalance, count or other needed target gate is instead an adverse admission event.

## 5. Freedman inversion and forced original-clock hit

Let `H=log(2/delta)`, `a=jH/3`, and `m=a+sqrt(2vH+a²)`. Exact algebra gives

`m²=2H(v+jm/3)`.

The one-sided bounded-jump Freedman bound applied to M and -M therefore gives total failure at most `2exp(-H)=delta`. The zero-bracket/zero-jump case is trivial and does not require dividing by a zero tail denominator. Conditional application at the actual entrance is valid with uniform ceilings; the tower rule gives the same unconditional failure charge on successful entrances, without independence or favorable future conditioning.

On successful admission and the martingale event, suppose the cap has not been reached by original time `4T`. The actual identity then yields

`4=sigma/T+q(X_sigma)-q(X_{4T})+D_{4T}+M_{4T}`
` <=s_*+beta+1/(70T²)+r+m`.

This contradicts the source's strict condition. Therefore the macro cap is reached by the original deadline; target reachability was not assumed in optional stopping. The cap-at-deadline case is allowed, and an adverse simultaneous exit is charged rather than silently accepted.

At the successful actual cap, the same identity and the two endpoint enclosures give

`|tau_cap/T-s_*|<=beta+r+m+c_cap`.

## 6. No early clearance and conditional entropy-five join

The original count-band event holds from time zero through the actual cap because the preceding argument forces that cap by original time `4T`. It gives `S>=N-12T` before and at the cap. For `T>=10^4`,

`N-12T>15(N+2)/16`,

equivalently `T^5>192T+30`. Hence the first downcrossing of the stated population threshold cannot occur before the cap. This needs the original count event, not merely a band observed after startup.

For the entropy entrance, the admitted actual target has

`M=A+min(C,D)=L-|Z|/2>=199L/200`.

Thus its seed is at least `199N/(4*10^6)>10^-6N`. The same count band gives `.75N<S<=17N/16` since `12T<=N/16`. These are the stated seed/mass entrance conditions at the same fixed reference N, without replacing the microscopic state or changing its distribution. Other entropy-service hypotheses and its numerical failure expression remain the separately received component's responsibility.

The received service reaches `S<=13N/16` by physical `tau_cap+5`; that endpoint is strictly below `15(N+2)/16`. Therefore the first threshold downcrossing is no later than `tau_cap+5`, regardless of whether the population later rises again. Only this upper first-hitting-time consequence is used.

Combining this with the no-early-clearance result gives exactly

`tau_clear/T in [s_*-epsilon, s_*+epsilon+5/T]`,
`epsilon=beta+r+m+c_cap`,

with union-bound failure at most `delta_adm+delta+delta_5`. Conditional service failure contributes at most `delta_5` by the tower rule at the actual cap; no independence is needed. If the probability expression is vacuous, it is not promoted to nonvacuous admission.

## Conclusion and non-acceptances

No repair was required. The receiver is consistent with actual stopping, terminal jumps, original-horizon limits and conditional future service. It acquires none of `r,v,j`, startup/admission probabilities, or entropy service itself. Executable reporting still needs outward rational enclosures and acquisition/precision costs for s_*. Neither a Gaussian/CDF approximation nor an advantage over retained ordinary computation follows from this receiver alone.
