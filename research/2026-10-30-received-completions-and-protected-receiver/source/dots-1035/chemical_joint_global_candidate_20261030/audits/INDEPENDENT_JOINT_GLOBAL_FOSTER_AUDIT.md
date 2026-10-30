# Independent audit of the complete explicit-network Foster coupling

Reviewed 2026-10-30. **The candidate passes this child-level adversarial audit, conditional on the previously audited bulk and trace lemmas as stated.** I found no remaining circularity or unclosed region in the displayed construction for this particular network. This is not independent whole-project replication, a general weakly reversible recurrence theorem, or novelty clearance.

## 1. Stopped-cost values are earned, not assumed

Take integer residual thresholds sufficiently large. The factorial exit-ratio calculation remains valid after multiplying phi by (1+z)^12. Conditional contraction of this larger weight bounds the expected sum over all pre-threshold residual excursions. Since that weight has a positive lower bound on integer z above the threshold, the expected number of excursions is finite. Each excursion has the independently proved finite mean and no explosion. Thus only finitely many excursions occur before the threshold almost surely, each taking finite time, and the stopped process is well-defined without an assumption about global recurrence or unrestricted-process nonexplosion.

On a neutral excursion the cost phi(z) is constant; its conditional expected accumulated cost is at most C(1+z)^12 phi(z). Summing proves the asserted value upper bound, uniformly over hidden coordinates and, for r, over admissible controls. One does not need to replace an expected holding time by a pathwise bound.

For the actual s-value the usual first-jump decomposition is legitimate because the stopped path and its integrable cost have just been constructed. It gives LW_s=-phi_s. For the controlled r-value, hold an arbitrary admissible row until the first jump and concatenate epsilon-optimal policies separately at its finitely many targets. The supremum value is at least this policy's value; multiplying its first-jump inequality by the finite total rate gives L_row W_r<=-phi_r after epsilon tends to zero. Countable states and finitely many targets avoid a selection or regularity assumption. No optimal policy or invariance of the physical coefficient cone is required.

## 2. Actual generator domains and threshold defects

The h bounds are correct. On r>r0 one has B<=3N/2, and actual activation/clearing coefficients are uniformly positive and bounded on A>=epsilon1 N for N large. The first trace therefore supplies the claimed physical local generator inequality. All fast A/C moves leave (N,B), hence W_r, exactly unchanged, including moves that leave the comparison cone.

Outside that cone, finitely many connector channels, bounded residual jumps, the uniform value upper bound, and the factorial ratio phi(r+1)/phi(r)=e^-d1(r+1)^alpha give (LW_r)^+<=C N^D phi_r(r). This uses no smoothness of the value function. Below the integer threshold only immigration from r=r0 can enter the positive domain; it has rate one and uniformly bounded target value, so its defect is bounded independently of B.

For W_s the actual inequality holds at every composition above threshold. On its zero side only activation from s=s0 can reach the positive side. Its intensity is AB, and the target value at s0+1 is uniformly bounded over all N and compositions. Thus its positive defect is <=C NB. Fast conversion and clearing preserve s and produce no crossing defect. Bounds involving Gamma(r+1) or Gamma(s+1) should be read only above their respective positive thresholds; below them the corresponding value is defined as zero.

## 3. Uniform entropy comparison and large-N coverage

The earlier exact low-B function obeys F>=V0: its exit data increase under the enabled low-B immigration/activation moves, and the running cost is nonnegative. At B<4 its upper ratio to V0 is polynomial in N, so LF=-V0 has at least an inverse-polynomial-F margin. At B>=4 the extreme-composition estimate gives the stronger margin cN^3(B)_4 F, uniformly in B.

For balanced composition and B>=max(8,K_bulk), every target has B>=4 and F agrees exactly with V0 at source and targets. The primal bulk bound has a quantitative margin c F times the sum of source falling-factorial monomials. The stoichiometric span of this network is all of R^3 (the two connector increments span the A/B plane and fast conversion adds the C direction), so the bulk theorem's finite exceptional set is uniform here; there is no hidden sequence of class-dependent exceptional radii. This verifies both the uniform large-N coverage and the negative margins used later.

Only balanced composition with finitely many B remains potentially bad for F. There r=N-O(1), and uniform Stirling/fixed-shift estimates give the stated logarithmic ratio N[alpha H(t)-d1]+O(log N). Since H(t)>=H(epsilon0) there, the r-value's negative forcing overwhelms every polynomial-F positive drift.

On the uncovered C-dominant side A<epsilon1 N, its possible positive r-value drift is negligible uniformly in B. If B<=eta N, use r!<=N!, F>=V0, binomial entropy <=N H(epsilon1)+O(log N), and r>=N-2eta N/3-1; the chosen small eta gives a strictly negative linear exponent. If B>=eta N while r>r0, the product N!/r! contains a positive-linear-in-N number of factors comparable with N, giving a negative c_eta N log N exponent. The entropy term is only O(N), the exponential e^-d1r does not hurt, and B! in F helps. All generator prefactors are polynomial in N because B<=3N/2. These facts rigorously absorb the positive W_r terms against the established F margins.

If r<=r0 and N is large, B is a positive multiple of N. Bulk or extreme-sector negativity of F absorbs the bounded r-threshold defect. Hence F+W_r has negative drift for every sufficiently large N, uniformly in B, with precisely the quantitative margins claimed.

## 4. The s-value closes the remaining domain

For large N, W_s can add positive drift only on s=s0. There B=g_N+s0~4N/3. Bulk or extreme-sector F negativity applies; the preceding comparison leaves a factorially large negative margin, which absorbs C NB. There is no conflict with the r-value threshold or the C-dominant comparison.

For N in the remaining fixed finite range and B tending to infinity, W_r and every possible successor W_r vanish. The s-value gives exact forcing -phi_s. Here F=V0 at source and every target for sufficiently large B, and its drift is bounded in absolute value by polynomial(B) F. Since g_N is bounded on this cylinder, phi_s(B-g_N)/F is bounded below by exp(d2 B) times an inverse polynomial. This proves domination uniformly over the finitely many A/C choices. These two domains cover the entire complement of a finite set.

## 5. Foster and moment consequences

The constructed V is finite at every state and normlike because V>=F. Every state has finitely many finite-rate outgoing channels. The proven negative drift outside a finite set gives a global upper bound LV<=b. Stopping on finite V-sublevel sets and applying Dynkin proves nonexplosion without assuming it beforehand. The stronger LV<=-1 outside a finite set yields positive recurrence on each closed irreducible class.

Weak reversibility of the physical reaction graph ensures closure: a physical transition z+y to z+y' has the enabled return path z+y_i along its complex return cycle, with fixed nonnegative residual z. Thus this is not an unsupported inference from only a projected phase graph.

The quantitative negative margins indeed dominate exp(theta(N+B)) for each fixed theta: F provides factorial growth in all coordinates in bulk/extreme regions, phi_r does so where B is bounded, and phi_s does so where N is bounded. The subtracted competing terms have been absorbed with a fixed fractional margin. Regenerative stopped Dynkin bounds therefore yield finite stationary exponential moments on each class. This does not require assuming integrability of V under the stationary distribution: finite-set regeneration bounds the integrated forcing directly, and finitely many exit destinations have finite V.

## Verdict and scope

The two complementary infinite-background traces and their stopped-cost values genuinely close the previously open feedback for this explicit six-complex, one-linkage, rank-three network. The value functions are implicit but finite by proved estimates; they are not postulated Lyapunov barriers. No physical cone invariance, fast mixing, or prior stationary measure is used. The conclusion remains restricted to this network and dependencies actually proved; external novelty and a separate whole-proof review are not provided by this audit.
d2a7534d0d7cf9bd8555d677b8f5f5e732ace593d9b357c9caf4e75f42bf359f  chemical_joint_shell_20261030/JOINT_GLOBAL_FOSTER_CANDIDATE.md
