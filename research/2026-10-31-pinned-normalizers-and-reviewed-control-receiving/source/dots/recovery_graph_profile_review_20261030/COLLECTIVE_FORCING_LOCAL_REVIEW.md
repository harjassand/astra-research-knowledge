# Independent collective bounded-noise forcing review

30 October 2026. Source: `COLLECTIVE_BOUNDED_NOISE_FORCING.md`, SHA256 3930d300b696f964ed2467ea235b3fd0f84c4531a8d1e0bd2acf74853f814a75; frozen copy in `token_sources/`. This is a separate local abstract receipt, not an enlargement of prior raw-network conclusions.

**Verdict: accept the stated deterministic-time concentration and retention theorem**, conditional on the exact generator contract and nonexplosion/localization assumptions. No independence of realized label paths is required. No load-bearing gap was found.

For u=T-s, phi_r(u)=exp(-bu)P(Pois(qu)>=r) is decreasing in rank. The backward time derivative cancels a one-step progress generator, leaving b phi_r, including r=0. Larger progress drops help. Thus the progress/time contribution to S is at least bS. Every adverse event loses at most the current phi mass on its touched labels; the per-label participation bound implies its summed drift is at least -bS. This argument uses actual predictable intensities, not averaged bounds.

For F=exp(-xi S), retain safe events exactly: since they increase S, their entire F generator contribution is nonpositive. They need not have bounded rates or bounded jump sizes for this sign estimate. For progress/adverse events, |Delta S|<=max(k,1) and Taylor's inequality gives a remainder bounded by (xi^2/2)exp(xi k)(Delta S)^2 after replacing k by max(k,1). Progress contributes at most qn to the squared-jump rate. If an adverse event touches m<=k labels, (Delta S)^2<=m^2<=km. Summing event rates yields at most kbn. Correlation among the touched labels does not alter this calculation.

Consequently (partial_s+L)F<=C0 xi^2 n F. A stopped exponential supermartingale/Dynkin argument and the stated localization limit give E exp(-xi A_T)<=exp(-xi S_0+C0 xi^2 nT). Safe-event intensity is not smuggled into a variance bound. For nonexplosive paths, bounded F supplies the necessary limiting domination; mere finite-state localization without a justified limit would not itself be sufficient.

For every initial rank configuration, S_0>=nd(T), where d(T)=exp(-bT)P(Pois(qT)>=L). On 0<T<=1, d(T)>=exp(-b-q)q^L T^L/L!, and d(T)<=qT. Choosing C1>=max(C0,qk/4) makes xi=d(T)/(4C1T)<=1/k. Exponential Markov at nd(T)/2 gives exponent at most -nd(T)^2/(16C1T), as claimed. One common smaller positive constant gives both threshold and tail constant in the theorem. Random initial ranks also satisfy the estimate conditionally and hence unconditionally.

For an initially rank-zero cohort, S_0=n exp(-bT). A fixed sufficiently short T0 and fixed small xi yield the displayed exp(-cn) retention bound. Restricting to the cohort preserves the per-label participation bound and batch-size bound, even if events also touch other labels.

With T=n^-delta and 0<delta<1/(2L-1), both 1-(2L-1)delta and 1-Ldelta are positive. Splitting on the good-count event proves the stated inverse-grade expectation for each fixed s>0. This is a deterministic-time count bound; stopped-episode reset, integrated occupation and time ratios do not follow without additional arguments. The weaker exponent is not automatically compatible with prior advertised parameter ordering.

Scope exclusions remain essential: persistent fixed labels; genuine single-label baseline progress in the same clock; fixed adverse batch size; uniform conditional per-label adverse participation bound; no births/deletions unless separately paid. A simultaneous population-wide adverse reset violates fixed k. A holding/ingress bound alone does not establish participation intensity. No raw acquisition algorithm, chemical example, whole signed-cycle transfer, physical holding-cost bound or recurrence conclusion is certified here.
