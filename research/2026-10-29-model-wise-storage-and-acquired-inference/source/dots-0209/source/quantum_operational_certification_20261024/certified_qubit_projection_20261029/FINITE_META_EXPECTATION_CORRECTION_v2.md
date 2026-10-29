# Expected arithmetic guarantee versus realized ledger; randomness accounting

2026-10-29 UTC. Substantive independent-review correction to FINITE_META_ARITHMETIC_v1.md. The frozen v1 proof/data remain intact. This addendum governs the stochastic expectation scope and corrects overbroad wording about total private bits.

## Expected guarantee

The exact potential inequality contains the RANDOM pathwise ledger sum_t rho_t. Accordingly, after taking conditional/total expectation in the service theorem, the extra average-regret term is

2 E[sum_t rho_t]/(eta N),

not the realized ledger of a selected simulated trajectory. The recorded values661/73786976294838206464 etc are correct realized algebraic ledgers; they are not themselves unconditional performance guarantees.

A deterministic universal envelope is available for the implemented64-bit kernel. Put D=2^64. The dyadic argument bracket lies in[0,2/3+1/D], of width at most1/D. The lower odd Taylor polynomial at the upper endpoint exceeds1/2 (a direct rational inequality checked below). Alternating-series remainder magnitudes for the even32 and odd33 polynomials are at most1/33! each since the argument is<1. The exponential is1-Lipschitz on[0,1]. Thus upper-lower<=1/D+2/33!, and downward rounding of the lower bound adds less than1/D. The pre-rounded relative deficit is therefore

rho_raw<4/D+4/33!.

Because4D<33!, rounding rho_raw UP to the next multiple of1/D gives rho_t<=5/D. There are at most N nonzero-loss updates. The unconditional average-regret debit is consequently bounded by

40 sqrt(N)/2^64.

At N1024 this is1280/2^64≈6.939e-17. This universal debit, not the smaller observed ledger, can be inserted without additional assumptions into the expected baseline/learner regret statement. Add the separate safe regret coupling debit2N*2^-128 for capped expert coins. The actual kernel permits other bit counts, but this stated numerical envelope is proved only for its implemented64-bit setting; other settings require recomputing the inequalities.

## Randomness accounting

The output field `private_random_bits` counts only expert-selection rejection-sampler bits. It does NOT count all private control randomness. The executable additionally consumes exactly2N Python private bits for role selection. For the implemented power-of-two horizon, ideal discrete terminal-time selection needs log2 N bits, and each shadow-basis choice needs2 bits. The fixture delegates those latter choices to NumPy; its machine-word consumption is not measured by the expert bit counter. Quantum Born outcomes and source-state sampling in the simulator are not private control choices of the experimental learner. Therefore11.21--12.43million is an expert-sampling cost, not a fully instrumented total-controller bit count. Any finite pruning/default-label selection adds its separately reported bit/debit ledger. Hardware randomness generation/preparation is not demonstrated by seeded PRNG execution.
