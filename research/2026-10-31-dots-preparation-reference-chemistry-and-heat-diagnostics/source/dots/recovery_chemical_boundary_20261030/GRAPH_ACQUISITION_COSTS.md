# Finite graph acquisition costs and comparison

30 October 2026. Companion to the unreviewed tagged-cohort/reset construction. No novelty or efficient uniform complexity claim.

For rational positive edge rates, choose rational Lambda>=max_i sum_j q_ij and one shortest path i->a of length ell_i<=L. Uniformization gives the explicit one-unit lower bound

    P_i(X_1=a) >= exp(-Lambda) product_{edges on path} q_edge / ell_i!.

For an initial a tag and u<=1, the no-jump bound is exp(-q_a). Thus a rational lower bound for the all-time occupancy constant p can be computed using

    exp(-Lambda) >= 2^(-ceil(2 Lambda)),

and the minimum prescribed-path product. Increase Lambda to at least 1 to avoid special zero-rate cases. The same paths supply the short-time u^L constants. No stationary distribution or unexplained mixing-time oracle is required.

The actual-episode absorption path uses H<=2L+3 jumps; a crude uniform operational j-th moment costs C_j n^(2Hj). Coarse moment exponents and the Chernoff constants therefore come from finite arithmetic and finite graph paths. For a finite requested set of s, one selects their logarithmic thresholds after these constants, then takes their maximum. The log-squared good set eventually dominates every one of them.

Computing shortest paths is polynomial graph work. This is NOT an assertion of polynomial certificate bit length or practical numerical conditioning: the path-rate products, rational exponential lower bound, inverse p, and final cutoff can be extremely large/small as graph size or rate ratios vary. The acquired population exponents deteriorate with L. These are real costs, not hidden uniform constants over arbitrary graphs.

The ordinary comparators are uniformization, independent-particle finite-chain concentration, finite event-path absorption, and multistep/stopped Foster construction. The reserve Poisson equation in the earlier compiler note is NOT needed for this tagged-cohort proof. Its failure to control the distinguished-A first-arrival clock remains a useful diagnostic, not an extra assumed lemma. The new construction's useful content is acquiring the joint local feedback certificate while changing to logarithmic good sets; it does not purport to replace conventional recurrence machinery at the final step.
