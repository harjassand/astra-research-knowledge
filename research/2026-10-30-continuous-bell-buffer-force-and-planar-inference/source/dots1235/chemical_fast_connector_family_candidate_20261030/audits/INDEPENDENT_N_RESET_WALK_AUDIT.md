# Independent audit: N-directed fresh-section reset walk

Reviewed 2026-10-30. Source: `N_DIRECTED_RESET_WALK_CANDIDATE.md`.

## Initial verdict

The exact residual, active output-moment estimate, phase-dependent reset-walk escape exponent, fresh-B0 conditioning argument, and downward hazard opportunity check out. Two proof issues were identified:

1. A drift estimate conditioned on the fully observed reset phase/composition cannot use an averaged inverse-moment bound. Replace that step by the joint-kernel proof below.
2. Declaring every fast immigration “bad” safely upper-bounds up-exit probability, but a bad immigration can be r-neutral. A bound on time to that artificial stop is NOT yet a bound on time to the actual first nonzero r exit. Actual continuation from bad states must be proved or the time claim weakened.

The second point prevents clean acceptance of the actual mean-time assertion in the initial source. A repair route is recorded below but must not be silently treated as already present.

## 1. Residual and active episode estimates

The displayed H gives H(B+q-1)-H(B)=m-1 whenever activation is enabled. Immigration changes r by h only at positive B divisible by q-1. Clearing B=q->0 is neutral; at larger B it changes r by -h precisely at B congruent 1 modulo q-1. All other enabled connector changes are neutral. H(B)>=0, so N>=r during a neutral excursion.

The strict clearing mean yields the stated separate immigration and activation first-event bounds. For the output moment, the clearing compensator gives

    E[(1+A_after)^-m; clear before birth]
      =E integral_0^{tau_clear wedge tau_birth}
          k_D(B)_q (A)_m/(1+A-m)^m dt.

The ratio is uniformly bounded for A>=m. Thus the joint moment is <=Cp(r). Since a clearing occurs before any birth with probability 1-o(1), its conditional output moment is also <=Cp(r), uniformly in the incoming composition.

Starting at B=b+q-1, an episode without immigration has at most q-1 clearings before low return or a down exit. Additional activations preserve the residue class and have uniformly o(1) probability per clearing race, so their stage count is geometrically bounded. A neutral low return cannot wrap upward in phase: wrapping at residue one either produces the down exit or is the special q->0 clearing. Hence its terminal phase is indeed <=b-1. The first clearing before any birth directly returns to b-1, making the total low-return probability 1-o(1). Summing joint output moments over stages and then normalizing by this high-probability return proves the episode-level moment claim.

## 2. A correlation-safe reset-walk proof

Let K be the actual substochastic reset kernel from a fully specified fast-episode entrance to a low phase and composition, stopping on down or bad events. Its joint bound is K[(1+A)^-m]<=Cp and K1<=1. Holder therefore gives K[(1+A)^-ell]<=C beta^ell for 0<=ell<=m, beta=p^(1/m). No conditioning on a particular low output phase is justified or needed.

For a fixed sequence of immigration-run lengths, the probability factors can be bounded by backward iteration of these positive kernels. Each run contributes at most C(1+A)^-ell before the next reset; the next reset bound is uniform in its entire entrance state. This gives C^n beta^(sum ell_i) for runs shorter than m, even when phase and A are correlated.

Expected run count can be proved without the source's problematic post-reset conditional drift. Index the substochastic transition at fast-episode ENTRANCES, where its input composition and launch phase are known. The probability of any intervening immigration before the next activation is O(beta), averaged over the joint reset kernel and uniformly in that entrance state. If q successive transitions contain no immigration, the launch phase strictly decreases until absorption. Hence the q-step substochastic kernel has row mass at most qC beta<1/2 for small beta. Kernel iteration gives uniformly bounded expected run count. The first run from the supplied fresh law has the same averaged moment bound.

A run of length at least m has probability O(beta^m), and the bounded expected run count bounds the probability of ever seeing one by O(p). Otherwise an escaping n-run path from phase b needs at least q-b+n-1 immigrations. Summing the at most m^n length strings gives O(beta^(q-b)); together these give O(p^{min(q-b,m)/m}). Bad-episode probabilities are O(p) per run and fit the same estimate. Thus the phase-dependent exponent is correct; only B0 followed by compulsory immigration to phase 1 earns O(p), since q-1>=m.

## 3. Fresh B0 conditioning and the down opportunity

A B0 section return always comes from an actual q->0 clearing. At each entry into the final B=q attempt, conditional on its full preceding history, clearing before a competing birth has probability 1-o(1) and has the normalized output inverse moment <=Cp. Disintegrate successful section returns over their final attempt entrances. This preserves the same conditional moment for the mixture even if the overall section-return event is rare. It is essential not to condition further on the newly observed A or on a post-output selection event. The source's coarse-history warning is therefore substantive and correct.

After compulsory immigration at B0, A>=1. Activation from B1 has a uniform positive chance against immigration and enters B=q with N=r+m. Pointwise there,

    lambda_T>=c r^{-(m-1)} lambda_D,

including states where the clearing rate is zero. Integrating competing hazards until the first event proves P(T first)>=c r^{-(m-1)}P(D first), and P(D first)=1-o(1). The subsequent B=2q-1 state has downward clearing residue; extra activations preserve that residue, and immigration risk is o(1). Thus the cycle has a genuine c r^{-(m-1)} down opportunity, uniformly in its input composition.

## 4. Artificial bad stop versus actual exit

Fresh cycles have artificial upward/bad probability O(p), down probability >=c r^{-(m-1)}, and bounded mean duration. Iterating until the artificial stop therefore gives an O(r^-epsilon) upper bound on the probability of encountering up/bad before down. This safely upper-bounds eventual actual up probability: if no bad event occurs, the artificial and actual classifications agree. However it only bounds the mean time to the artificial stop. A neutral bad immigration can leave the actual process running in an active high-B state, so the claimed actual exit-time bound needs another argument.

A possible repair uses only the existing estimates. From an arbitrary active high-B state, repeat no-immigration fast episodes after neutral immigrations. Before each such interruption, at most q-1 clearings lead to down or low phase; the interruption probability is O(p), so this high-phase resolution has bounded mean and joint low-output moment O(p). Feed that subprobability output law into the worst-phase reset estimate O(beta). If a further bad immigration occurs, restart the high-phase repair. Its restart probability is O(beta), so geometric closure should yield bounded expected time to a fresh B0 section or an actual r exit. The final B0 moment uses the same last-attempt disintegration. Adding that written repair to fresh cycles would establish the desired actual mean without proving a global N-directed value.

This outline is not a license to replace an actual neutral event by an absorbing boundary. The current candidate must either include the repair or explicitly restrict its time claim to the artificial stopping rule.

## Reviewed initial source hash
0d5fdeed8ec717e47e349647c10fbb114dceb5ea5af6e451597f654abe9f3424  chemical_joint_shell_20261030/N_DIRECTED_RESET_WALK_CANDIDATE.md

### V2 receipt

Reviewed `N_DIRECTED_RESET_WALK_V2.md`. It replaces the post-output drift assertion by the q-step substochastic entrance-kernel proof and explicitly restricts the old time estimate to the artificial stopping rule. It does not claim the unproved actual mean from that argument. These corrections resolve the reset-walk file's two scope/proof issues. The actual continuation and value are separately audited in `INDEPENDENT_UNCAPPED_N_VALUE_AUDIT.md`.

Corrected reset source hash:
7d462ffb21e2ab248bbd7c95024efae6a995b2e8d8eb70bcaac920fbd9e09483  chemical_joint_shell_20261030/N_DIRECTED_RESET_WALK_V2.md
