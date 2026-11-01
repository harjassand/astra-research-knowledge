# Independent exact receipt: original-source narrow count band and cone consequence

Frozen inputs:

- `../ACTUAL_NARROW_COUNT_BAND.md`, SHA-256 `c60f158a40e54a6b6864cec9b4fe8705ce432e809f3581647328f3b5235588bc`.
- `../COUNT_BAND_CONE_CONSEQUENCE.md`, SHA-256 `9e0bea69f21a7cdab972ee731d21fa643ac00d0b76aee98568160696760b4e7f`.

**PASS in their original-clock/stopped-domain scope.** The original immigration/death ledgers, temporary-floor elimination, literal constants, one-step cap overshoots and deterministic cone consequences are correct. No ratio/imbalance admission or later extension beyond the received clock is included.

## 1. Non-circular stopped construction

Use the fixed initial state `(0,N,1,1,0)`, integer `N>=10^5`, and `T=N^(1/5)>=10`. Temporarily stop at the first of the actual E/L cap, actual `B<.9N` exit, the continuous Q-budget hit, and original deterministic time `4T`. The storage and death-count estimates are first proved for this actual stopped process, not conditioned on a future count event or on future survival of the B floor.

Before the E cap, integrality is important: `E<ceil(N/100)` implies `E<=ceil(N/100)-1<N/100`. Before the L cap, `L<N/5000`. Therefore `A<=L<B` and `C+D+4E<.0404N<B/2` whenever the temporary floor `B>=.9N` holds. This is exactly a domain on which the previously accepted source-storage calculation applies; no separate small-A or imbalance assumption is inserted.

Initially `W_0=2(ceil(N/100)+1)`. For `S_0=W_0+4T`, `Qbar=2S_0`, the accepted exact storage theorem gives the budget-exit bound `exp(-S_0/124)`. Since `S_0>=N/50`, this is at most `exp(-N/6200)`.

At the same stop, the death compensator is at most `4S_0/(.9N)`. Since `W_0<=N/50+4`,

`4S_0/(.9N)<= (.08N+16+16T)/(.9N)<=1<=T`.

This holds for all `T>=10`. In fact, the displayed ratio is at most `511/5625<1`, by bounding `T^-5` and `T^-4` at ten. These are unconditional stopped-process compensator bounds; the later good event does not create them.

## 2. Original counters and literal tails

All internal reactions conserve total population; consequently the actual identity is

`S_t=N+2+I_t-D_ct,t`,

where `D_ct` denotes the true-death counter, not species D. The immigration process has its original unit-rate Poisson law, and the stopped death counter has its actual compensator `integral A dt`. No count is replaced by a conditional independent Poisson variable.

At `theta=log 2`, the original immigration tail is

`P(I_{4T}>=10T)<=exp[(4-10 log 2)T]<=exp(-T)`.

Real thresholds need no rounding adjustment: the event is the integer counter reaching or exceeding that real threshold. On its complement, monotonicity gives `2+I_t<=12T` for every original time `t<=4T`.

For the stopped death counter, `theta=1/2`, `exp(1/2)-1<1`, and the same-stop compensator ceiling give

`P(D_ct reaches 12T by that stop)<=exp(a-6T)<=exp(-5T)`.

Here `a<=1<=T`. The receiving event is interpreted for the stopped counter including its terminal jump, not after deleting an adverse final jump. On the complements of the budget, immigration and stopped-death failures, both counter bounds hold through the temporary stop, hence `|S_t-N|<=12T` there.

## 3. Elimination of the temporary B floor

The exact state identity is `B=S+A-2L-E`. If the temporary B floor were the first remaining stop, the just-proved count bounds and cap bounds would imply

`B>=N-12T-N/2500-N/100>=.9884N>.9N`,

because `12T/N=12/T^4<=.0012`. This contradicts the actual first floor exit. The Q stop is also excluded on the same good event. Therefore the temporary stop equals the actual cap or original time `4T`; no circular conditioning is used to extend the count event.

For completeness, the cap's terminal jump can increase L by at most one and E by at most one. Thus replacing both strict pre-cap bounds by terminal bounds costs at most `2*1+1=3` in `S+A-2L-E`. Even the conservative lower bound `.9884N-3` is above `.9N` for every `N>=10^5`. Count changes on the terminal jump are included in the original counters. This proves the asserted B-floor and count bounds including the actual cap jump.

The final failure charge is the ordinary union bound

`exp(-N/6200)+exp(-T)+exp(-5T)`.

It applies to the original interval `[0,tau_cap wedge 4T]`, with the original source budget and its occupation ceiling. It neither restarts at a later entrance nor continues beyond original time `4T` without an additional result.

## 4. Deterministic consequence for later states within the received event

At any state for which the original count bound is actually available and `E>=e0 T³`,

`|S-N|N/E² <=12T*T^5/(e0² T^6)=12/e0²`.

The special constants follow exactly:

- `e0=2` gives `|S-N|N<=3E²`;
- `e0=20` gives coefficient `3/100<1/25`;
- combining `|S-N|N<=E²/25` with `R=E²/(NL)<=2` gives `|S-N|<=2L/25`.

The word “later” does not extend the count theorem's time domain: if it is used by inheritance from this count event, the later state must still lie at or before `tau_cap wedge 4T`, or its count bound must be supplied separately. No new preparation, observation or independent probability event is created by the algebraic consequence. Existing counterexamples outside these gates remain unaffected.

No repair was needed in these two frozen sources. The separate buffered handoff sentence required an explicit original-clock guard; that receiving issue and its accepted repair are recorded in its own receipt.
