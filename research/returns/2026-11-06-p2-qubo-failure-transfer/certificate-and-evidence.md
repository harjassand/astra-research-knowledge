# Three-bit certificate gap, accepted spectral scope and finite evidence

The supplied [full report](package/RESEARCH_REPORT.txt) retains

`E=−31x₁−30x₂−28x₃+32(x₁x₂+x₁x₃+x₂x₃)`.

Its unique minimum is`−31` at`(1,0,0)`; the eight values in source order are`0,−31,−30,−29,−28,−27,−26,7`. Coefficients have gcd1.

The rational first Boolean moment matrix, indexed by`(1,x₁,x₂,x₃)`, has first-row/column entries`(1,1/2,1/2,1/2)`, data diagonals`1/2` and off-diagonals`1/8`. It satisfies Boolean moment equalities. The Schur complement is`(3/8)I−(1/8)J`, with eigenvalues`0,3/8,3/8`, so it is PSD. Each pair has a valid local distribution`(Pr00,Pr01,Pr10,Pr11)=(1/8,3/8,3/8,1/8)`.

The moment functional gives objective`−65/2=−32.5`. Thus the minimisation relaxation's optimum is at most`−32.5`, whose ceiling is at most`−32`, still below the true minimum`−31`. Greater numerical accuracy cannot remove this structural gap. Equivalently, affine-square/degree-two certificates `E−ℓ=Σp_j²+Σλ_i(x_i²−x_i)` require`ℓ≤−32.5`. Adding nonnegative individual-pair functions does not remove the witness because its pair distributions are valid. This excludes that certificate class, **not higher-order/global inequalities or arbitrary algorithms**.

P2 reports inspecting the governing Astra scalar spectral-certificate source at pinned revision`78ec80fd5a68f769b6a222e114f1b167fd41d6f8`. That accepted source requires a separately constructed candidate and actual tractable consumer; its spectral certificate is sufficient and may be `INCONCLUSIVE` even for an optimal candidate. Physical acquisition also has separate source/noise/precision/cost assumptions. Here coefficients are already explicit, but a general candidate constructor and universally successful certificate remain missing. The three-bit gap respects the accepted limitation and does not invalidate the stronger strategy of retaining an optimised tractable core and certifying a residual. Capital does not reprove or retract that prior result.

The source credits Lucas for standard SAT/Ising translations, Boros–Gruber for pseudo-Boolean quadratization identities, min-plus/Barvinok rank to established tropical linear algebra, and standard submodular optimisation/partial-minimisation facts. No literature priority or universal superiority is established. Governing links and derivations are preserved in the full report/return; Capital has not performed another source audit.

| Producer-reported exact finite checks | Scope |
|---|---:|
| Star identities/multilinear coefficients | `k=2,…,12` |
| Weighted-square variable splits | 872 |
| Balanced cuts of a`4×4` grid | 12,870 |
| Oriented middle-layer contact inequalities | 139,586 |
| Three-bit energy table/PSD/value | Exact rational witness`−65/2` |
| Signed-binary object fixture serialization | Supplied round-trip record |

The [exact checker](package/verify_research.py), [recorded run](package/audit_results.json) and [fixture record](package/fixture_roundtrip_results.json) are delivered unchanged. `audit_results.json` is the producer's finite-check record, not a new Capital audit or external scientific review. The reference optimiser uses exponential enumeration. Finite passing tests supplement general proofs and check arithmetic/implementation; they do not prove general correctness or polynomial complexity of an unrestricted solver.

The [packet index](package/PACKET_INDEX.txt) says no peer transmission occurred. [FAILURE_OBJECTS_ONLY.json](package/FAILURE_OBJECTS_ONLY.json) retains explicit families, signed-binary coefficient fixtures, exact failed claims and scopes without preferred repairs or proof narratives. The coordinator owns any first exchange. Public retrieval/Personal Context remain allowed by the nonblind experiment; neither publication nor retention establishes delivery, use, feedback benefit or a causal policy win. No research code, optimiser or proof replay was run during publication.
