# Independent receipt of weighted all-p sharpening

27 October 2026, 02:50 UTC. PASS for exact_erasure_weighted_all_p_lower_bound.md.

The padded-source Choi reference has exactly the stated main and extra blocks and trace one. The centered perturbation is supported on the main block and has zero trace. Direct expansion with the inverse on support gives1+8p t; zero-weight extra blocks atpD=1 are correctly removed. The same source-independent common Weyl simulator works, with identity correction on the extra erasure sector.

The weighted trace Cauchy-Schwarz argument is valid without assuming that the averaged source commutes with its reference. For HermitianX supported there, factor Tr(signX X)=Tr[(B^1/2 signX)(X B^-1/2)] and bound the two Hilbert-Schmidt norms. The second squared norm is cyclically equal toTr(X B^-1 X); the first is at mostTrB. This verifies the half-distance inequality used for the two averaged hypotheses.

The extra datum retains the exactDt Haar factor. Expanding the finite binomial and using(D+1)...(D+k)>=(D+1)^k yields the claimedx=8pn/(D+1), a valid sharpening of the earlierD denominator. Thus the inverse lower bound is(D+1)/(8p) times the bracket. Sincefloor(1/p)+1>1/p, its stated non-strict uniform consequence1/(8p^2) times the bracket, and1/(40p^2) at error<=1/4, are valid. The branchx>=1 is automatic. No expected-query bound follows.

The separately received complete-noisy-recovery transfer permits replacing1-zeta bys=alpha-17delta/(8p)>0 with no other change. This strengthens constants and covers all smallp, but does not enlarge the task to accepted-only recovery, fixed absolute error, supplied flags, fixed output dimension, unbounded stopping times or free Stinespring/coherent oracle access.
