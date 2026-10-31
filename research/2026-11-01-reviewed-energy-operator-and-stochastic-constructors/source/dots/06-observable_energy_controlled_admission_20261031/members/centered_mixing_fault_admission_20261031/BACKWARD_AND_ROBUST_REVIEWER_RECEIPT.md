# Independent whole review: backward-control admission and robust reference

## Binding and verdict

Read both entire source bodies, not merely the author receipts:

- `BACKWARD_CONTROLLED_OBSERVABLE_ADMISSION_CANDIDATE.md`, SHA-256 `f2d89255727d94d8a4e1a4af08c906e1e39c7fbff6149c40ee72b0f54b4d3a3c`.
- `ROBUST_BACKWARD_OBSERVABLE_COROLLARY.md`, SHA-256 `e2c7a9a80aad1bca93a50cfee8b29b2c3bb0d44679aa8675a0d0f8bdc10a5ad6`.

**Mathematical PASS for both within the stated finite-register, initialized-field, fixed local-patch and actual-generator scope.** No load-bearing correction found. The earlier derivative-budget proof and its receipt remain unchanged. The robust result is a separate derivation, not an automatic transfer of the earlier theorem. No code frontend, calibration, hardware threshold, priority or practical advantage is certified here.

## 1. Backward observable and source-blind controls

The ideal local evolution includes the actual constant source generator and the specified local data controls/instruments, while omitting the selected unwanted K. Source-only evolution commutes with every source-blind data superoperator, even on initially correlated states. Thus its adjoint action on K(s) can be factored from the data adjoints. The coefficientwise identity G*K(s)=-rK(s) gives the factor exp[-r(s-t)]. This is a complete operator statement; it is stronger than covariance decay in one input state.

Unital CP adjoints contract the operator norm of the Hermitian observable, including a retained local record and arbitrary references. Consequently B(t)=2 integral_t^b Phi* K(s) ds has norm at most 2c(1-exp[-r(b-t)])/r. Noncommuting data coefficients do not invalidate this step. Source-dependent controls would invalidate the superoperator commutation and are not admitted.

On continuous pieces differentiation gives partial_t B+G*B+i[H0,B]=-2K, with B(b)=0. At an instrument, the future integral is pulled back through its full record-retaining adjoint: B_before=C*B_after. This is an equality of effects across the whole instrument, not a contractivity claim for each normalized rare outcome.

Local adaptive policies are compatible when represented on the fixed data/record patch with uniform bounds: the policy defines a linear CP propagator on that enlarged space. Future record access outside the patch, or coherent control registers coupling active patches, is not implicitly covered. The final source explicitly confines such global changes to compatible weight-free boundaries.

B is an analysis observable. A mathematical certificate can use its existence without a physical backward-integration device or a numerical B oracle. Acquiring the generator identity and actual support conditions remains a separate obligation. Ideal-control gate count, synthesis and actual imperfections are not made free by the analysis.

## 2. Tilt, instruments, endpoint factors and constants

With V=I+yB, q=2Rc/r<=1/2 ensures positivity. The backward derivative cancels the tilted identity term +2yK exactly. The remainder is

    i y conjugate(z) K B - i y z B K.

It is Hermitian whether or not K and B commute, and has norm at most 2|y||z|c||B||<=4R²c²/r. Since I<=V/(1-q)<=2V, the squared-norm growth rate is at most 8R²c²/r. No hidden derivative of K or ideal gate Hamiltonian norm is needed.

At an interior ideal local instrument, C*V_after=V_before follows from unitality. For its initialized Stinespring map U this says U†(V_after tensor I_environment)U=V_before, exactly the weighted receiving relation needed. It does not disclose, condition on, or discard a private outcome to improve a bound.

The initial weight costs at most 1+q in squared norm. At the terminal boundary B(b)=0, so V(b)=I and there is no inverse-(1-q) exit penalty. A reused source can then enter another selected or unselected location in its actual state, including all previous correlations. The insertion is only an inequality, not a preparation or reset.

Taking square roots and applying inclusive Cauchy extraction gives eta=sqrt(1+2Rc/r) exp(4R²c²tau/r)/(R-1). The radius in equation (8) gives q<=1/2 and quadratic exponent<=1/2; R>=2 permits 1/(R-1)<=2/R. The displayed constant and maximum are correct. The zero-coupling case is correctly separated. If the candidate radius is below 2, the simplified sufficient admission is unavailable.

The short-time integral equals 2c[tau/r-(1-exp(-r tau))/r²]. For q<1 the squared-norm exponent is bounded by 2R²c/(1-q) times that integral. With the correspondingly smaller endpoint bound this recovers a c*tau scale, so the coarse c/r endpoint estimate is not a physical zero-time floor. No executable optimization is inferred from this optional formula.

## 3. Whole-product and common-dilation receiving

At any instant the actual source/data patches are disjoint. Therefore the current positive weights commute, and each source generator or local instrument acts on only one factor. Multiplying a single-factor Loewner inequality by the other positive factors is valid. This is not a general product rule for a Lindblad generator with cross-block jumps.

All real outside couplings remain present. They commute with each selected current weight because they occupy disjoint patches. Initially entangled sources do not spoil this algebra. Cross-patch hopping, shared spectators, a source that simultaneously serves distinct active patches, or an operation touching another active weight must satisfy a different explicitly proved bound; product initial states or marginal decay would not repair that missing premise.

For finite systems, finite horizon, bounded coefficients and finitely many instruments, use a common jump-history/record Stinespring space for all selected complex parameters. The no-jump factors and finite instrument compositions are entire. On a compact polydisc, the sum over jump sectors is uniformly norm convergent, for example using an exponential no-jump bound times sqrt((T sum_j sup||L_j||²)^k/k!). Hence the history map is operator-norm analytic. Its squared norm is controlled by the positive but non-trace-preserving tilted evolution, to which the weight estimates apply. There is no illicit normalization of this evolution.

Positive Taylor degree in every selected variable is exactly the inclusive alternating omission sum: the unwanted K is omitted at each selected location in the relevant branches, while intended controls, source evolution and every outside interaction are unchanged. Summing Cauchy bounds over positive degrees produces (R-1)^(-|S|). Interior instrument dilation histories are the same in all these branches. This proves an initialized-field amplitude premise, not independence of reduced errors, a local probability estimate, or a bound on an arbitrary incoming-field unitary.

The proof therefore receives repeated source use, arbitrary initial source/data/reference correlations, and local recorded instruments within its actual support restrictions. It does not automatically certify noisy preparation/measurement implementations or a code's full threshold hypotheses.

## 4. Robust reference: actual G, not a changed generator

The reference B0 uses only the data-control propagator and the scalar exponential kernel. Direct differentiation gives

    (partial_t+i ad_H0-r)B0=-2K.

The actual constant source generator commutes through the data adjoints and the future integral, so

    (G*+r)B0 = 2 integral_t^b exp[-r(s-t)] C* J(s) ds = F(t).

This identity is exact even though K is not an eigenoperator. Contractivity and Fubini give integral||F||<=2d_J/r. The actual weighted generator has the earlier quadratic remainder plus yF. Since V>=I/2, its extra integrated squared-norm exponent is at most 2R integral||F||<=4R d_J/r. The same exact instrument receiving, start factor and zero terminal factor remain valid. After the square root the additional exponent is 2R d_J/r, exactly as stated.

Constant G during the location is essential to this particular formula. A time-varying G_t cannot simply be moved through the future integral acting on K(s). Neither an empirical exponential fit nor an uncharged reference dynamics is being substituted for the actual device. Actual source-model/calibration error must enter the acquired J bound.

A source-independent bias has J=rK0 and is paid at its ordinary integrated interaction strength; raising the reference r cannot hide it. If ||J||<=epsilon*r*c, h=2epsilon*c*tau gives the isolated sufficient factor exp(hR)/(R-1). Its unconstrained minimum is h exp(1+h), attained at R=1+1/h. Radius constraints and the other factors can only worsen this sufficient optimization. This is not a universal physical lower bound on every mismatch; the source correctly distinguishes bias from harmless or differently suppressed detuning.

## 5. Strong ordinary comparisons and bounded conclusion

The primary comparisons from the immediately preceding review remain applicable: [Ng–Preskill](https://arxiv.org/html/0810.4953) already gives microscopic all-selected Gaussian-noise admission with a square-root correlation-integral scale; its Gaussian/free-field structure cannot be inferred merely from a finite-source eigenoperator identity. The present thermal one-axis fixture even has an ordinary exact telegraph representation. Neither its fast-noise scaling nor its single-cell solvability is a new capability.

[Preskill's collective Hamiltonian-noise criterion](https://arxiv.org/html/1207.6131) supplies strong general non-Markovian fault receiving and explicitly allows effective dressed interactions. Direct norm accounting pays the coupling strength, while any use of a transformed or averaged description must earn its locality and uniform all-selected error. That primary statement alone does not provide the particular actual-generator/backward-weight certificate audited here.

Backward equations, finite-horizon correctors, CP effect pullback, weighted tilted evolution and analytic coefficient bounds are ordinary methods. This review establishes the conjunction in these sources, not that no prior theorem contains it. In particular, an operator-specific mixing or microscopic-noise result with exactly these controlled initialized-dilation hypotheses could subsume the result; absence of such a match in a focused comparison is not a novelty proof.

The meaningful improvement over the previously checked derivative-budget certificate is mathematical: source-blind local ideal-control variation no longer incurs an artificial d bill, and interior local instruments are received exactly. It does not remove the cost of actual control hardware, source-model acquisition, initialized ports or imperfection certification. Fixed diffusion retains its nonvanishing leading noise, and no practical architecture advantage is proved.

## 6. Executed evidence

Read `check_backward_control.py` and executed a copied version under `producer-workspace/backward_observable_review`, preserving the author source and JSON. It checks 20 exact rational identities (stationary backward resolvent/tilt and noncommuting depolarizing example) and four floating common-dilation histories with an interior measurement, source reuse and outside interactions ON. The exact checks supplement the algebra review; the floating histories are diagnostics, not rigorous numerical certificates. Their stationary-resolvent checks are not mislabeled as direct numerical verification of every finite-horizon backward observable.
