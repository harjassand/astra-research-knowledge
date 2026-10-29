# Code-dependent marginal refinement (established random-code mechanism)
2026-10-29. Additive calculation, not a new random-coding claim.

Keep a,b,D,k,T from MOMENT_AND_PRIOR.md and write P=sum_i|e_i><e_i|. Let tau_E=T(P/k) and Delta'=J_RE-(I_k/k) tensor tau_E. Then ||Delta'||2²=TrJ_RE²-(1/k)Trtau_E². The diagonal-column tensor moment is as before. The distinct diagonal-column moment is E[|e_i><e_i| tensor |e_j><e_j|]=(I-F/D)/(D²-1), so
 ETrtau_E²=(a+b)/(kD(D+1))+(k-1)(a-b/D)/(k(D²-1)).
Combining with ETrJ_RE² gives
 E||Delta'||2²=(k²-1)/(k²(D²-1))*(b-a/D).
Because k<=D, its prefactor is at most1/D². Therefore E||Delta'||1<=sqrt(kr*b)/D<=r sqrt(k/D), which yields the established Klesse-type average code fidelity bound. For k=1 the centered moment vanishes exactly, as it should. Uhlmann can use this per-code marginal; there is no requirement that the optimal-existence decoder share a fixed environmental target across seeds. The later physical learned decoder still needs its separate forward-query construction.
