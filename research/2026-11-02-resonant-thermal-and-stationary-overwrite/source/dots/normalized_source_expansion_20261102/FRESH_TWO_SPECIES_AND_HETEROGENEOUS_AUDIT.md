# Fresh adversarial audit: normalized contact/events and heterogeneous clocks

2026-11-02. Reviewed `ROOT_TWO_SPECIES_CONSTRUCTION.md`, `CONTACT_EVENT_INDEPENDENT_AUDIT.md`, the independent `TWO_LEVEL_CONTACT_GAS_AUDIT.md`, the earned `EXACT_MIXED_SOURCE_ROD_FACTORIZATION.md`, and the heterogeneous corollary appended to `resonant_rod_bound.md`. The finite Poisson numerical identity is not a premise.

**Verdict: no fatal gap found.** The normalized contact/event construction and its explicit scalar KP admission are valid under the earned full-column dictionary, physical locality/dimension/filling assumptions, and the strengthened inflated native KP conditions. The consumer must use local scalar FUNCTIONS, not insist that dressed sources remain single characters. Neither a polynomial-in-K total robustness theorem nor the counterterm family follows.

## A. Exactness, including possible failure points

1. The used-label component graph and compatibility graph must both use intersections of full contacts: N1 of owned clock columns plus actual data/bath supports. Enlarging only the component graph or only compatibility would fail. As written, they agree. Owned columns remain their original union, not the entire contact neighborhood.
2. This deterministic regrouping preserves the Dyson-history bijection and repetition/time-order factors. Distinct components retain disjoint affected checks and data supports; syndrome closure holds separately. Merging disconnected owned clock sets does not interfere with this argument.
3. Compatible source columns cannot be adjacent, since adjacent owned columns force intersecting N1 contacts. Thus direct native source/source signs are one. Each background rod can see at most one source, including owned-column exclusion. This proves the singleton identity exactly, trajectory by trajectory.
4. Pinning changes rod activities by modulus-at-most-one factors and leaves their mutual pair factors unchanged. The native convergent log series can therefore be used for each fixed compatible source family. Finite-volume normalization is exact; local KP bounds, not an infinite extensive exponent, justify uniform limits.
5. Residual events are native connected Mayer terms with at least TWO rods. Their complex measure includes its original Ursell/factorial convention. Event/event factor must be one, including coincident or overlapping events. The independent complex-Poisson sum then reconstructs precisely the exponential of the residual log intensity. Adding event exclusions, including singleton events again, or omitting the event-only denominator would invalidate the claimed normalization. None occurs in the specified construction.

## B. Exact cancellation and source norm

Let c be the owned clock count and T the clock contact set. For a uniform K clock, the raw all-level transfer bound is K^c exp(beta M0 c), M0=KJ. It also holds with any number of prescribed norm-one matrix-unit insertions: the intervening time intervals sum to beta, and a single trace dimension factor suffices.

Owned nonwinding singleton deletion contributes exp[-beta(M0-J-delta_nv)c]. Owned winding deletion costs at most exp(beta J c); unowned winding response at most exp[2 beta J(|T|-c)]. Nonwinding and wrap responses on unowned contacts have modulus at most one; owned wraps can also be dropped in an upper bound. Multiplication gives exactly the safe envelope

`K^c exp[2 beta J |T| + beta delta_nv c]`.

Thus the compact root expression is correct. The less tightly combined expression in section 2 of the independent contact audit is merely a looser upper bound; section 3 of the two-level audit correctly performs the cancellation without charging owned winding twice.

The tail estimate follows by a c0=t/K² tilt of the unmarked spectral measure: M0(c0)<=4M0/3 and hence `delta_nv <= (4/3)M0 exp(-beta c0)`. Positivity needed here is available for nonwinding ordinary rods; signed winding rods were explicitly separated.

Including the already charged dictionary, insertion and bath norms gives

`q_norm = M^b_c d_B^b_B exp[2 beta J b_T + beta delta_nv,max b_c] (exp(beta v_dict)-1)`.

This removes exp(beta J K) self-pressure before absolute source majorization. It does not eliminate K-dependence of b_c, b_T, the dictionary coefficient norm, elementary-label degree/count, or contact degree.

## C. Event pressure and constants

For native activities inflated by exp(gamma), marking a rod on a fixed clock overcounts, never undercounts, events meeting that clock. The rooted cluster estimate gives

`P_gamma <= exp(gamma){beta[exp(a0_gamma)M0(b_gamma)-M0] + exp(a0_gamma)W(b_gamma)}`.

The subtraction really is INSIDE exp(gamma). Integrating ordinary-root `exp(a)-1` to infinity gives this difference; the retained wrap expression conservatively drops a nonnegative subtraction. This does not charge singleton pressure again.

For the uniform-length model, `exp(a0)-1<=2a0`, `exp(a0)<=2`, and

`M0(b)-M0 <= b M1/(1-b/mu) <=2b M1`

give

`p_gamma/J <=128 x_gamma+64 x_gamma=192 x_gamma`.

The bound therefore checks, with `x_gamma=D exp(gamma) eta²` (and any independently intended spatial weight included consistently). The uninflated thermal/KP point alone is insufficient; require the inflated x bound and inflated wrap condition explicitly.

## D. Second KP and consumers

The source-animal sum touching one full-support node is bounded by

`G(Q)=ell_full Q/(1-C_contact Q)`.

Connected-set counting may replace C^(m-1) by C^m conservatively; no extra repeated-insertion count is missing because that count is already in q_norm. With `A=1+4b_T P_gamma`, `Q=q_norm exp(A+alpha)` and alpha>=0, the explicit conditions

`Q<=min{1/(2C_contact), gamma/(8ell_full), 1/(4b_full ell_full)}`

imply `G<=min(gamma/4,1/(2b_full))`. Event roots cost at most `2nG<=gamma n/2`. Source roots cost at most `2b_T m P_gamma+b_full mG<=Am/2`. This gives actual slack, including for exceptional source test roots of EVERY size. No matrix-valued cluster theorem is invoked.

After singleton dressing the dependence support of a source is its original stabilizer-filling footprint plus its contacts. Fixed-trajectory pair factors remain syndrome independent. A telescoping product can change only through a source footprint or an event flux footprint. Using `|z(s)-z(s')|<=2 envelope` avoids any exponential Fourier expansion of a filling neighborhood.

Choose positive spare alpha to pay the actual polynomial filling/anchor-count overhead. This step presupposes the earned physical geometry/volume growth and polynomial filling statement; bounded contact degree alone does not prove it. The resulting anchored source integral S_* is finite uniformly in memory and bath volume. At v/v0=eta<=1 every source-containing connected term gains eta, since each source contains at least one perturbation insertion and its singleton dressing is v-independent. Marking sources and event roots then yields the displayed bound

`|Xi(s)-Xi(s')| <=2 eta |T| (S_*+P_gamma)`.

Event-only terms cancel before this argument. The bound applies to real logarithmic magnitudes if the truncated scalar gas is complex; positivity of that truncation is not assumed.

Every large memory-touching source remains exceptional even if its word happens to be scalar. Distance still forces the conservative cutoff m>=d/b_D. Its logical word has norm one, its singleton dressing is scalar, and all interactions with the small-source/event gas are scalar modulus-at-most-one pins. The same source-root KP bound holds at arbitrary m, earning exp(A m) per exceptional pin. Compatible exceptional words commute by disjoint actual data supports; in any case the operator norm product bound suffices.

The resulting exceptional activity sum is anchored at native data OR clock labels, O(n), with bath extensions counted inside connected animals. Remote pure-bath contributions cancel. Summing multiple exceptional roots gives r_n<=exp(R_n)-1. For r_n<=1/2 the comparison with actual positive projected Gibbs traces yields the claimed two-syndrome correction at most 4r_n. This is a relative ratio error, not an additive Gibbs bad-event floor.

## E. Independently checked heterogeneous corollary

With K_a>=3, M=max K_a, `t_a=J M² K_a/(2eta²)` and `g_a=eta t_a/M`, every J_a is exactly J. The moment identities give `M0,a=JK_a`, `M1,a=eta²(K_a-1)/M²`; mu_a>=2JM/eta². With common `a0=64Dbar eta²/M` and `b=16Dbar JM`, b/mu_a<=8x. The displayed species-uniform KP integral `8Dbar JM l+20Dbar eta²/M` is correct and fits the charges.

The marked logarithmic tilt is at most `(32/3)x K_a/M`; adding a0 gives at most32x because M>=3. The species tail tilt `t_a/K_a²>=JM/(2eta²)` gives exactly the stated common finite-beta tail. Thus (T_het) and (R_het) check for arbitrary neighboring species lengths; equal lengths were not silently assumed.

The same normalized-event estimates extend: with inflated x_gamma and the corresponding common charges,

`exp(a0)-1` times `M0,a` contributes at most128 x_gamma J;
`exp(a0)[M0,a(b)-M0,a]` contributes at most64 x_gamma J.

Hence the same192 bound applies. Also

`delta_nv,a <=(4/3)JM exp[-beta JM/(2eta²)]`.

These provide explicit heterogeneous versions of the q_norm and P_gamma inputs rather than requiring a fictitious padding to M states.

Actual clock dimension sum and edge count are both sum K_a. Each cycle has K_a-2 internal t_a edges and two g_a edges, so the displayed exact edge-strength sum proportional to `sum K_a(K_a-2+2eta/M)` is correct and involves sum K_a². The sum of 2t_a coefficients is `2 sum t_a` if each excited-sector projector Q_a is treated as one onsite operator; the stated `sum 2t_a(K_a-1)` instead counts its rank-one projector decomposition. These are different resource conventions, both mathematically legitimate, and should be labeled rather than conflated. Peak onsite coefficient is 2t_max, while peak internal edge coefficient is t_max.

## Scope

This replaces the earlier raw-source obstruction by a valid normalized connected construction. It is meaningful new analytic progress, not merely an isolated-mediator calculation. A whole native phase/lifetime join still must substitute the actual physical dictionary and code constants, retained witness threshold, logical endpoint and environment assumptions. No blanket polynomial-K imperfection tolerance, practical K=180 device, cheap preparation, historical novelty, or g proportional to K^-1/2 counterterm family is certified here.
