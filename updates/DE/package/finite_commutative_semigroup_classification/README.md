# Finite commutative semigroup product classification

The exact 569-line user-supplied report is preserved in [RESEARCH_REPORT.md](RESEARCH_REPORT.md). The standalone theorem route is [N674](../../../../frontier/dossiers/N674.txt).

For a finite commutative semigroup S, let e_x be the idempotent power of x, and define x R z iff e_x z = z. For a full-support input law μ, the report defines T(μ) as the output laws of R-supported transports from μ. It claims every law in T(μ) is exactly realizable for every n ≥ max(3, ceil(1/α)), where α = min_x μ(x) > 0, by an exchangeable coupling with n−1 identical entries and one uniformly positioned exception. At most |S|² mixture atoms are needed.

Conversely, every attainable output law at size n is within c(S)/n in total variation of T(μ), where c(S) = min{|S|−1, Σ_x(t_x−1)} and t_x = min{r ≥ 1 : e_x x^r = x^r}. The report gives a three-element example with distance 1/[2(n−1)], so the order cannot generally be improved to o(1/n). Its construction chooses φ_n(x,z) = x^r z using the multiplication-orbit period, then balances the individual marginals with a finite stochastic-kernel fixed point.

The report limits the criterion to full-support laws and commutative multiplication, and supplies counterexamples to dropping either assumption. Its separate rational linear-program formulation has O(|S|² log n) variables for finite-n feasibility, so avoiding an exponentially large joint table is not claimed as new computational power. The classification and diagnostics remain source-derived and unreviewed; no independent reconstruction or priority review was performed.

The source report contains the proof narrative, sharpness examples, computational contract, and limitations. Its separately linked research ZIP, longer research note, and constructor script were unavailable locally at intake and were not recreated; see the source manifest.
