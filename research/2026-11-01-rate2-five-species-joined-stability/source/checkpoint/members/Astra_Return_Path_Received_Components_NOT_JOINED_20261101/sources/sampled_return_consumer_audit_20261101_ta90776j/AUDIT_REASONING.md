# Conditional consumer — independent proof receipt

**The conditional probability argument passes under its explicit statewise hypotheses.** The controlling source revision and acceptance are recorded in `FINAL_BINDINGS.json`. This is not a network theorem, not a runtime certificate, and not verification of (H) for the rate2 network.

Interpret population as nonnegative integer-valued, D as finite, and Poisson domination as holding under every P_x with the same finite rate λ. The block constants/duration cap and (H) must be uniform over all sufficiently large starting states. The repaired time-homogeneous, nonexplosive, finite-exit-rate CTMC assumptions are appropriate.

1. **All block costs are paid.** For failure B, Cauchy–Schwarz gives

   E_x[e^{θ n(X_d)}1_B] <= e^{θ n} [E e^{2θ I_d}]^(1/2) P_x(B)^(1/2).

   Since d=d(x) is deterministic given x, the Poisson MGF is exactly exp[λd(e^{2θ}−1)]. No independence between B and I, or stationarity inside the block, is used. The relative drift bound is

   e^{−θδn} + sqrt(p) exp[λD(e^{2θ}−1)/2 − κ n^a],

   where κ=[c−λD(e^{2θ}−1)]/2>0. It tends to zero uniformly. The remaining finite head has finite QV by the same domination.

2. **Sampled recurrence and integrability are justified, not assumed.** Q^kV<=ρ^kV+b/(1−ρ). Finite population sublevels make V normlike. Cesàro laws are tight; a convergent subsequence on the countable space converges in total variation. The telescoping invariance error tends to zero, giving νQ=ν. Fatou gives ν(V)<=b/(1−ρ). This avoids subtracting infinite stationary expectations. Every finite positive-rate CTMC path can be completed before any positive d(x), with a positive holding probability afterwards, so Q is irreducible. The deterministic state-dependent block schedule also has no sampling accumulation because d>=d0.

3. **Occupation transfer is exact.** h=ν(d) is finite and at least d0. For bounded f let g_s(y)=E_y∫_0^s f(X_u)du. Direct Markov/Fubini calculation gives

   h[π(P_s f)−π(f)] = ν(Qg_s−g_s)=0.

   The interval identity remains valid when s>d(x). The endpoint Markov step can be conditioned on each starting x, where d(x) is deterministic. Boundedness of f and finite h justify all interchanges. Thus π is an invariant probability of the actual CTMC, not merely of Q.

4. **The entire holding interval has a moment bound.** For 0<η<θ its occupation reward is bounded by

   D(1+n^a) exp[ηn+λD(e^η−1)(1+n^a)] <= K_η e^{θn}.

   The supremum defining K_η is finite because a<1. Consequently π(e^{ηn})<=K_η ν(V)/h<∞. The argument guarantees η<θ, not automatically the same θ at both sampling and physical time. Irreducibility supplies uniqueness and positive recurrence of the CTMC.

**Scope correction:** v1's general-looking pointwise-drift impossibility assertion was too broad; `V1_SCOPE_FINDING.md` gives an immigration–death counterexample to that wording. The revised text limits the obstruction to a separately established specific-network result. That external obstruction is not a premise independently established by this audit. The polynomial-failure comment is a worst-case n^a-time cost comparison, not a claim that polynomial failure could never suffice for bounded or shorter blocks.

No counterexample to the conditional consumer was found under these hypotheses. Its substantive outstanding premise for the investigation remains the uniform physical block statement (H), including actual removal, continuing immigration and all adverse channels.
