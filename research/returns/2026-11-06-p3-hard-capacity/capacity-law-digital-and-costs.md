# Bulk capacity law, regional admission and finite digital costs

For translation-invariant rational finite-range data on regular geometric systems with the stated primitive interface, the [complete return](P3_HARD_CAPACITY_20261106_RETURN.txt) reports the bulk limit `v(ρ)=lim_n J_n(floor(ρn))/n`, `0≤ρ≤1`. It is nondecreasing, concave, Lipschitz and computably enclosed by finite-patch LPs. This concerns optimal sustained performance, not all invariant laws, differentiability, rare failures or relaxation times.

For patch side`L` in dimension`d`, with mean-capacity value`g_L(ρ)` and computable boundary constant`C₀`, compatible large tori satisfy

`g_L(ρ)−C₀/L−(C/4)√(L^d/n)−C/n ≤ J_n(floor(ρn))/n ≤ g_L(ρ)+C₀/L`.

Consequently `|v(ρ)−g_L(ρ)|≤C₀/L`. If `ψ(λ)` is the unconstrained bulk optimum charging each enabled HIGH primitive price`λ`, the result is

`v(ρ)=min_(0≤λ≤Cfull)[ψ(λ)+λρ]`.

Finite-patch LP duality alone supplies a bound; constructive hard-capacity admission and uniform-in-price boundary error justify equality in the limit. `Cfull` is the full reward's disagreement/suppression sensitivity. The finite-system sensitivity is `0≤J_n(M₂)−J_n(M₁)≤Cfull(M₂−M₁)`. This price is a reward-unit multiplier, not an acquired energy price.

Global online admission can be replaced by separately capped regions`G`, assigning`M_G=floor(μ_G)` for regional mean demand. Caps sum to≤`M`; unused whole units can be redistributed. Loss includes fluctuation plus integer-allocation terms. With regional size between`s/2` and`s`, the intensive allowance is `(C/4)√(2k/s)+2C/s`. Nested geometric partitions can use `k=O(ε^(−d))`, `s=O(ε^(−(d+2)))` and diameter `O(ε^(−(1+2/d)))`. Offline allocation and finite-delay physical communication remain paid. The finite-region result is not zero-latency free global coordination.

Several supplied fixed **nonnegative** HIGH-resource weights are also handled by sequentially deleting largest-weight requests. Constants depend on actual densities/weight bounds. State-dependent or signed resources and mandatory-action equalities are outside that argument.

The digital controller observes actual plant snapshots at interval`Δ`, holds commands between readings, and conditionally updates references from observed endpoints. Held rate`q` gives parity-change probability`p_q=(1−exp(−2qΔ))/2`. Conditional reference probabilities such as `(p_c−p_d)/(1−p_d)` or`p_c/(1−p_d)` have denominators≥`1/2`; they do not require rare-event division or hidden noise-channel access.

Sample-and-hold changes reward and mean demand by `ΔA_r,ΔA_c`, with finite patch Poisson constants computed and charged. For `|r|≤nR₀`, total finite-horizon sampling error`δ`, `JΔ=T`, intensive regret is bounded by

`D∂/n+CΓ_P/n+Δ(A_r+CA_c)/n+[S+K_x E D₀/(2a)]/(nT)+2R₀δ`.

Using `ceil(log₂(4nJ/δ))` random bits per conditional draw with sufficiently accurate probability evaluation/initialization supplies the reported allowance. Internal stationary distributions are finite matrix computations with paid conditioning/precision, not physical equilibration. Rounded request sampling still passes through an exact feasible integer selector; faulty physical enforcement is a separate obligation.

| Resource | Constructive cost or unresolved input |
|---|---|
| Occupation LP | `O(Σ_B4^k_B)` state/action variables |
| Offline arithmetic | Rational LP, stationary/Poisson solves and certificate bit lengths |
| Plant reads / command writes | `n(J+1)` reads, at most that many writes |
| Online random bits | `O(nJ log(nJ/δ))` plus initialization |
| Controller memory | Reference states, policy labels/tables, counters |
| One-cap selector | `O(n)` elementary operations per interval |
| Physical execution | Actual read/write/compute/communication/clock costs and feasible latency |

Compilation remains exponential in accuracy-dependent patch volume. Small observation intervals can make online execution expensive. For commissioning duration`Tc`, reward lower`−nRcTc`, one-time costs`Cinit`, operating rate`Lop` and online cost`conline`, whole-campaign net performance is bounded below by

`[(Lop−conline)T−RcTc−Cinit/n]/(Tc+T)`.

No physical break-even time follows without actual source and cost inputs. The earlier synthetic/noisy two-primitive commissioning construction does not silently supply arbitrary apparatus acquisition or safe faulty actuation here.

The source credits Hong–Xie–Chen–Wang's NeurIPS2023 Follow-the-Virtual-Advice foundation, including continuous-time O(1/√N) optimality without UGAP under its unichain premise. Goldsztajn–Avrachenkov2406.04751v3's weakly coupled multiple-action/constraint methods are substantive alternatives; their discrete-time synchronization counterexample is a different setting, not a refutation of this positive-baseline coupling. Zhang–Hong–Wang2502.06072v6's heterogeneous `O(N^(−1/2))` results mean a square-root rate alone is not novel. Historical priority of the stated spatial/coupling/digital/regional/bulk combination remains unestablished. Primary links remain in the exact source; Capital has not performed another literature audit.

The new four-component example uses`a=1,b=3,M=1`, two-pair rewards plus weak crossings. Source-reported exact checks cover256 joint states,2,048 marginal equalities, disagreement and capacity in every state, reference balance/relaxation,12 sampled-coordinate cases,52,488 weighted-resource deletions and Poisson constants. Numerical potential discovery followed exact rational residual recomputation. Delivered/optimal total rates are enclosed by `[1.27012283236,1.27012283238]` and `[1.40714285714,1.40714285715]`, gap≤`0.13702002479` total or about`0.03425500620` per component. This is finite model evidence, not practical superiority or independent review.

The original report/code/certificates remain in the held ZIP; Capital ran none. The next consequential gap is actual **state-dependent joint rate/cost interfaces with feasible finite latency and reliable enforcement**, not a missing permission to assume them. Unknown apparatus, rare-catastrophe protection, economical deployment and unrestricted SAT remain outside the returned construction.
