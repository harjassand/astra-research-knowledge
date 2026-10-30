# Adversarial child review: multifacet obstruction and killed shells

Reviewer: finite_phase_drift_challenge, 2026-10-29. Internal mathematical review only; no external priority claim. Reviewed THREE_SPECIES_INTEGRABILITY_OBSTRUCTION.md, KILLED_FACE_RESOLVENT.md, and RESOLVENT_POINTWISE_OBSTRUCTION.md.

## Verdict

All three restricted claims pass this review. They establish representation and information-loss obstructions, plus a polynomial killed-shell absorption bound; none establishes or disproves general recurrence. One exposition repair is needed in the first proof: actual reaction shifts imply lattice coordinate shifts, not immediately unit shifts. The repair below closes this gap. Avoid the unqualified word “equivalently” between fixed-shift and gradient premises: the latter with appropriate Taylor control is sufficient, and necessity here is proved within the special angular ansatz.

## Fixed shifts really force triangularity

Write y0=(1,3,0), y1=(3,0,0), y2=(0,3,3). Every ±yi is an actual immigration/emigration displacement. Their integer combinations give

    3e_A=y1,
    9e_B=3y0−y1,
    9e_C=3y2−3y0+y1.

At points tending to infinity in a compact interior angular cone, every finite intermediate shift is enabled and stays in that cone. Telescope the assumed reaction-shift differences. Smoothness gives U(x+s)−U(x)=o(1) for each fixed intermediate shift s, so the premise holds for these three coordinate lattice shifts as well.

Fix 0<v<u<1 and send A→∞ with B~A^u, C~A^v. For the 9e_C difference, divide by 9A/[C log A], which diverges. By first-order differentiability, the limit is ∂v U_A; contributions from U_B and U_C have respectively B/A and C/A relative factors, while the stipulated bounded difference becomes zero after division. Thus ∂v U_A=0 everywhere. U_A is consequently exactly independent of v. Repeat the same argument dividing the C difference by 9B/[C log A] to obtain ∂v U_B=0. Finally divide the 9e_B difference by 9A/[B log A] to obtain ∂u U_A=0. This uses only local C1 control on compact angular sets, not a false implication from arbitrary fixed differences to derivatives. Hence U_A is constant and U_B depends only on u.

## Prefactors, coefficients, and one class

For A~alpha t^3, B~beta t^2, C~gamma t^s, fixed positive alpha,beta,gamma change angular coordinates by O(1/log t); continuity therefore gives the same limiting U for all such prefactors. Local incoming factors converge by the assumed shift premise. At s<1 or s>1 the off-face monomials are smaller by a fixed power of t and their coefficients remain bounded. The two exposed monomial ratios are respectively alpha^2/beta^3 and the same ratio with a common gamma^3 canceled. Varying this arbitrary positive ratio forces both individual exposed coefficients nonpositive. The immigration contributions are strictly positive and finite, so rho>50 on the first face and rho<1/50 on the second. Triangularity makes rho identical; contradiction.

The claimed class is exact. With A in 3Z, B,C in 9Z and B≥C, A≥(B−C)/3, the integers n2=C/3, n0=(B−C)/3, n1=(A−n0)/3 are nonnegative. The prescribed immigration births sum to (A,B,C), and their reverse order gives enabled emigrations to zero. Rays with 0<s<2 satisfy both inequalities eventually; rounding each coordinate into these lattices preserves all asymptotics. These are not rays in different disconnected classes.

## Killed-shell estimate

The path argument is valid even on boundary states: if x=z+y with z≥0, following a graph path y→...→y_exit keeps the same nonnegative residual z. Before the exit, every source remains face-active and w·x=N. A shortest path has bounded length L independent of N. Total retained-and-killing rate is at most C(1+N)^D; each prescribed enabled edge has rate at least kappa_min. The probability of absorption within L embedded jumps is therefore at least p_N as stated. Iterating at block endpoints gives E[J]≤L/p_N. Every active holding rate is at least kappa_min, so E[T]≤L/(kappa_min p_N). The finite resolvent row-sum norm equals maximal expected absorption time; transpose dual l1 estimate follows directly. No shell irreducibility or spectral-gap assumption is hidden. Remove null reactions when defining the embedded jump chain, and take N with nonempty active shell. Inactive states and entire neutral linkage classes remain genuinely excluded, as stated.

## Pointwise obstruction

The one-particle inverse is (-Q)^−1=[[2,1],[1,1]], so lifetime from A is 3, from B is 2, and expected B occupation from A is 1. Stopping n independent particles at first death gives the stated shell process and inverse norm≤3 for n≥1. The displayed p_B(t) is correct, and p_B(t)≤1/sqrt(5). Independence gives the all-B occupation integral exactly. Initial all-A holding time is 1/n. Thus v_n(allB)/v_n(allA)≤n(1/sqrt(5))^(n−1), proving the asserted lack of polynomial coordinatewise comparability from an inverse norm alone. Strictly positive forcing can preserve the separation by choosing its additional mass sufficiently small for each n; this is not a statement for uniformly comparable forcing, nor an obstruction specifically to carefully designed adjacent-shell factorial ratios.

## Scope preserved

The angular no-go requires bounded smooth, radial-size-independent angular coefficients and their local-fugacity fixed-shift premise. It does not exclude rapidly narrowing boundary layers, general integrable potentials, or all positive dual measures. The absorption and pointwise results do not by themselves determine inter-shell feedback or recurrence. Those remain the exact assembly blockers.

## Final artifact pin after author repair

Re-read the repaired angular-premise and lattice-shift paragraphs; the repair is accepted. SHA-256 of reviewed versions:

- THREE_SPECIES_INTEGRABILITY_OBSTRUCTION.md: `27f81a2fb9308adc4f10a06841205cf30322289f8bf8cd64ddf0c5bf2c048a9e`
- KILLED_FACE_RESOLVENT.md: `85af6cf1bc510bac0e5304a5ca3f175782083c0e84c43de50bb6f55432dd32ea`
- RESOLVENT_POINTWISE_OBSTRUCTION.md: `e3a8dc3bff2376c46120f1e0a9f74af35449fbdad309584cc7a57ba772db5229`
