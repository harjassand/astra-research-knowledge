# Fresh audit: prescribed dynamic flux and vacuum point pins

2026-11-02. Independently checked both lemmas against the exact ordered-prefix edge formula and the audited signed rod KP criterion. **PASS within the expressly scalar prescribed-history scope.** No finite numerical test is a premise.

## Dynamic algebra and positivity

The exact dressed edge is `sigma_(a,i)(q) S_a^c`, where sigma consists solely of Pauli commutation signs `chi(P,F_h)` and `chi(S_a,F_h)`. These are signs of fixed operators, not functions of syndrome eigenvalues. Replacing the closing-hop eigenvalue by s_a(t) therefore leaves every trajectory pair sign unchanged, even across flux jumps and shared X/Z clocks. This conclusion follows from the edge formula, not from static free-energy substitution. For an actual dressed data history, additional Pauli insertions belong to the data-history amplitude; the statement about its clock factor presupposes that they are data-only.

An ordinary first-return rod uses the closing edge zero, one, or two times, only at its endpoints. Thus the listed winding and backtrack multipliers are exact. Wraps cannot use that edge. Endpoint values at jump times do not matter in the continuous-time integrals.

The gas is real. Interpolating each whole-rod multiplier linearly between 1 and its dynamic value stays in [-1,1], so the same absolute KP majorant proves nonvanishing along the full interpolation. Its initial partition function is positive. Therefore the dynamic trace is positive and its real logarithm agrees with the cluster branch. The interpolation need not itself be a physical Hamiltonian; it is a legitimate interpolating gas. Positivity of arbitrary products of positive operators is neither used nor claimed.

## Rooted estimate and constants

Winding singletons contribute exactly `-2 sum_a J_(a,beta)L_a`: each endpoint orientation integrates over a full beta-circle start measure. For nonsingleton clusters, the telescoping product inequality and the rooted `exp(a)-1` bound give exactly `2 sum R_a L_a`.

A closing-link backtrack changes sign only if its circular interval crosses a flux jump. Its bad-start measure is at most ell N_a, with overlaps only overcounting. Including its singleton and using the rooted exp(a) bound gives `2 sum E_a N_a`. The backtrack subdensity is bounded by rho_a, so the stated conservative E_a is valid. Unmarked wraps, nonwinding rods and signful shared-clock interactions remain inside the rooted bound.

Consequently (DF) is correct with no missing factor beta or factor two. The homogeneous bound `E_a<=8g²(K-1)/t²` and heterogeneous bound `E_a<=8eta²/M` follow from the previously earned tilted M1 bound and exp(a0)<=2. The derived J_eff lower bound correctly subtracts both the finite-beta winding tail and the nonsingleton winding remainder.

## Vacuum pins in dynamic backgrounds

Inserting |0><0| at (a,t) deletes exactly the rods on a whose nonzero interval covers t and all wraps on a. The external multiplier is 0 or 1, so its absolute Mayer factor is 1, not 2. For several pins,

`|product pin multipliers -1| <= sum over rods/pins of the deletion indicator`.

Rooting the log-response on a deleted ordinary rod gives start measure exactly ell and hence E_a; rooting on a deleted wrap gives Wtilde_a. This directly proves

`|log Z_pin[s]-log Z[s]| <= sum_i(E_(a_i)+Wtilde_(a_i))`.

Dynamic flux multipliers have modulus one and do not enlarge the absolute activities. Deletion interpolation preserves the same KP majorant and real nonvanishing; starting from the positive dynamic partition function proves positivity of the pinned one as well. Thus exponentiation gives both claimed ratio bounds on arbitrary prescribed dynamic backgrounds. Multiple pins require only the displayed union bound, not temporal separation or statistical independence.

Under the heterogeneous cold condition the per-pin bound is indeed `8eta²/M+2eta²/M=10eta²/M`. E_a itself depends on its finite-beta integration limit, but has the stated beta-uniform upper bound; the wrap bound decreases in beta.

## Exact scope retained

These results control scalar clock traces with prescribed piecewise-constant flux and optional vacuum projectors. They do not justify adding such projectors to physical perturbations, replacing arbitrary clock matrix units by vacuum blocks, discarding complementary open/nonvacuum paths, or concluding normalized quantum-data contour stability. They provide no beta-uniform generic-noise theorem, Gibbs preparation theorem, or new logical-memory consumer by themselves. The remaining quantum history normalization and logical/operator summation gates stated in the lemmas are real, not technicalities already solved by this audit.
