# Independent aggregate-occupation flow review

Reviewed radical's n1722_aggregate_occupation_flow_20261113/RESULT.md and the prior fixed-fiber construction. This review is confined to the stated filled-D good class, not all M5 exits or residence.

## Exact linear identity
For a finite reversible graph with weights w and native conductances g, let B be grounded. For each source x choose a finite path ending at its FIRST B visit, and send mass w(x). Include sources already in B with zero path. Summing signed directed edge traffic gives divergence w(x) at every non-B source, zero at other non-B vertices, and negative terminal mass only in B. A path passing through another source does not invalidate this identity: its own transit divergence is zero.

Thus, for any function v vanishing on B,

    sum_sources_notB w(x)v(x)=sum_unoriented_edges F(e) grad(v)(e).

Cauchy gives its square <= E_g(F) E_g(v). With the ORIGINAL global soft-core voltage, native E_g(v)<=C_kappa, giving the claimed occupation bound. A voltage killed at the M6 boundary cannot replace it because the growth paths can leave M6. No entrance-current density is used or assumed Gibbs.

## Interior labels and contour collisions
Fix geometric D and its deterministic once-only outside order. An edge flips site i outside D. The position of i determines the prefix F_k. Its oriented pre-flip endpoint z reconstructs the unique source x=z XOR F_k. In particular x restricted to D is exactly z restricted to D: there is no independent interior-pattern label to enumerate. The reverse orientation gives at most one other source, contributing the opposite sign. Consequently (a-b)^2<=a²+b² pays both directions without a factor2 beyond the two endpoint resistances.

All interior patterns can therefore be pooled into one F_D. Inter-contour collisions remain real and are paid by M=#D, through (sum_D F_D(e))²<=M sum_D F_D(e)². Unique geometric-D reconstruction is neither true nor required. Native heatbath resistance1/g=1/w(z)+1/w(z^i) then gives E(F_D)<=2n e^(4theta) Z_D once the prefix moment is established.

Source disjointness holds because each source has exactly one actual outermost domain larger than5R² while every exterior companion is <=R². This requires D to mean an actual source domain and its full deterministic separating minus collar, not a freely chosen subdomain or marked support. General nonfilled merger supports with geometric holes are not covered by this counting statement.

## Prefix moment checked independently
For deterministic flipped outside set F,

    w(x)/w(x XOR F)
      = exp[2theta sum_cross(F) sigma_i sigma_j -2phi|F|+4phi N_F^+].

Every F–D crossing was an original source boundary edge with signs minus/plus. All remaining products are <=1. Therefore the cross term is bounded by2theta[P(D union F)-P(D)]. Conditional on each fixed interior pattern, the complete minus-collared exterior companion gas obeys the same previously proved density bound under all site fields tilted from phi through3phi. Integrating the log-MGF derivative gives E exp(4phi N_F^+)<=exp(4phi rho|F|). Averaging over interior patterns preserves the bound; no independent-spin approximation is involved.

The geometric two-neighbor fill never increases perimeter. Subsequently the shorter-side strip has length equal to the current longer side, exceeding sqrt5 R. Every partial strip increases perimeter by at most2, while a completed strip's exponent change is4theta-2phi(1-2rho)*length<0. Hence all prefixes cost at most e^(4theta). Torus wrap can only lower the comparison perimeter. The source must have positive M_D so complement flipping actually reaches B. Retained source boundary plus spins preserve an M5 violation all along the path.

This argument imports the proven uniform companion-gas density estimate and its pin-avoiding full-domain involution. It does not independently establish source coverage for configurations violating those hypotheses.

## Exponents and finite source-capacity gate
The supplied conservative bounds are consistent:

    M<=8n4^(13R),
    Z_good/ZA<=36nR² e^(-16.6536R)/[(1-q)(1-u6)],
    E(F)/ZA<=4608 n³R² e^16 e^(1.5464R)

at theta4,u6<3/4,q<1/2, using ln4<1.4. The positive1.5464 coefficient must remain; omitting contour collisions would falsely remove it.

Radical's proposed M1 trial-capacity bound has a separate sound scalar derivation CONDITIONAL on the existing joint-contour/topology lemma. Reserving .05 in each contour's geometric tail costs at most21; six roots per site give126n. Up to8 joined contours yield8(126n)^8. At theta4 the remaining exponent is(6-1.45)(4R-4)=18.2R-18.2. Target predecessors inside M1 require Nplus>=n/2-1; the same4phi tilt gives exp[-2phi(1-2rho)n+4phi]. Soft source states in A intersect B must contribute kappa*w(A intersect B). I did not independently reprove the inherited disjoint joined-domain/winding lemma or acquire final finite C_kappa/ZA numbers.

Converting N_good/ZA to N_good/N_total additionally needs an earned positive denominator1-U_C/kappa. A small current-weighted probability of visiting bad states does NOT bound their occupation. Neither limitation is removed by this result.

## Exact diagnostic
check.py uses96 dyadic-Ising source configurations across3 different contours, with varying internal spin and4 thermal exterior bits. It constructs2160 aggregate native edges and verifies with Fraction arithmetic: off-target divergence, one internal label per fixed-contour edge, integration by parts, Cauchy, and aggregate-energy multiplicity bound. Its arbitrary sorted paths and test voltage are deliberately NOT the large-R geometric construction or actual harmonic voltage. It checks the aggregate algebra only, not asymptotic density/contour hypotheses.

## Critical baseline correction: valid construction, no stronger occupation bound
After the preceding proof check, radical pointed out the decisive simpler baseline. Since0<=v<=1,

    N_good/ZA <= Z_good/ZA
               <=36nR² e^(-16.6536R)/[(1-q)(1-u6)].

This directly uses the SAME already-proved source-mass estimate and is stronger than the aggregate-flow estimate (approximately e^(-8.3R) after the proposed capacity exponent and before prefactors). The flow proof is valid, but its capped5–6R² occupation consequence supplies NO improvement over trivial voltage domination. The review above must not be interpreted as a major new occupation result. No ZIP or breakthrough claim is justified from it. An actually useful extension would have to cover a region whose Gibbs mass is not already exponentially small, while preserving geometric decoding, source laws and full occupation control; none has been proved here.
