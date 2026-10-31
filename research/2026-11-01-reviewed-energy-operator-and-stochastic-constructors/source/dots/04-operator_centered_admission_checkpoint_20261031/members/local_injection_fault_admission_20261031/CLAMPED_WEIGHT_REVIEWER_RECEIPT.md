# Independent review: clamped weights for source-creating local noise

31 October 2026. Reviewer: challenge_graph_profile_compiler.

## Verdict and source

**Mathematical PASS within the stated local model and initialized-field receiving interface.** I independently read the full root source and checked the local operator inequalities, all-selected-set construction, weight discontinuities, convolution estimates, common-dilation comparison and Cauchy extraction. This receipt is not a new threshold theorem, an executed acquisition/compiler, a hardware construction or a practical/novelty claim.

Source: `local_injection_fault_admission_20261031/CLAMPED_WEIGHT_INJECTION_CANDIDATE.md`, SHA-256 `b3589808a6b2e23b717cbd5012840c8f21300a30f94bda61ee2beb44bd64b0c8`.

I reread the final Section 1 clarification: positive loss, aggregate coupling norm, fixed common schedule/source sets across controlled branches, and uniform retained-control-register norms are now explicit. No mathematical constant changed.

The scope uses lambda>0. The constant c bounds the TOTAL unwanted Hermitian operator assigned to a given source cell at a given location, including all its declared contributions, not each of an unbounded number of separately bounded terms. Every such operator acts on that source cell, its declared system patch, and any admitted shared spectator; it does not secretly act on additional guard cells. Common support/incidence bounds must be paid under controlled implementations. These are the local interface underlying the proof.

Unlike the earlier transparent-charge theorem, this result allows K=[[0,C*],[C,D]] with a nonzero source-creating C, even invertible K such as X. It requires the exact PP compression to vanish. Arbitrary PP noise is not removed by a mean-subtraction convention. The distinction is scientifically substantive.

## 1. Real unselected creation

At one cell the commutator with diag(I,1+u) is off-diagonal, with norm u||C|| after factoring the positive commuting outside weight. For alpha=4c²/lambda, the claimed majorant after removing u is diagonal with entries alpha and alpha(1+u)+lambda/4. The product of those scalar bounds is at least alpha lambda/4=c². The operator-valued two-block Schur inequality therefore proves the displayed bound even when C acts nontrivially on system, reference or an admitted spectator. D contributes no charge-weight commutator.

Consequently each real unselected interaction spends lambda u Q/4 and pays activation alpha u V. This is local and independent of exterior system size. It does not require classical source trajectories or a factorized source state. The remaining local loss is 3lambda/4; the total scalar activation budget a_eff=a+4c²/lambda correctly includes all these unselected interactions. A bound on individual summands without first bounding their total would not justify this step.

## 2. Complex selected-site allocation

At u=1, the tilted Hamiltonian contribution is i conjugate(z) K V - i z V K. Its top-right block is i(2 conjugate(z)-z)C*, with norm at most 3Rc. Its QQ block is 4 Im(z)D, hence at most 4Rc Q in Loewner order.

For the off-diagonal part, s_R V+(lambda/4)Q with s_R=36R²c²/lambda is positive as a majorant: the PP scalar is s_R and the QQ scalar is 2s_R+lambda/4, whose product is at least 9R²c². The QQ contribution is at most lambda Q/4 when R<=lambda/(16c). These are operator inequalities, not scalar expectations requiring a normalized tilted state.

The existing edge inequality contributes at coordinate i the coefficient lambda[d_i u_i+sum_j B_ij u_j] Q_i V_rest. At a selected coordinate u_i=1 it is at most 2beta lambda Q_i V_rest, hence at most lambda Q_i V_rest/4. The full selected-site loss is -lambda Q_i V_rest. Thus after the two complex allocations and hopping, the remaining occupation coefficient is at most

    -lambda + lambda/4 + lambda/4 + 2beta lambda <= -lambda/4.

It can safely be dropped. No weight derivative is needed at a clamped coordinate. Including a_eff rather than just a in its scalar activation cost is conservative, not a second unpriced loss subtraction.

## 3. Free coordinates, impulses and the volume estimates

At free coordinates, the real-creation allocation and the hopping inequality produce precisely

    M=lambda[-3I/4+diag(d)+B].

Its off-diagonal entries are nonnegative and both row and column sums are at most -lambda gamma0, with gamma0=3/4-2beta>=1/2. Starting from zero at the final physical time and working backward, a free coordinate cannot leave [0,1]: at a first value one, its derivative is at most -lambda gamma0. Selected active coordinates are set to one.

Each backward entry into a selected interval requires a nonnegative jump of size at most one per participating cell. Repeated use of a cell is counted with multiplicity. Over k selected locations there are at most gk such impulses. Adjacent/overlapping selected intervals can only reduce the number of actual jumps relative to this bound.

Between jumps, write u'=Mu+f. On a selected coordinate,

    f_i=-(Mu)_i=lambda(3/4-d_i-sum_j B_ij u_j),

so 0<=f_i<=3lambda/4. It vanishes on free coordinates. The fixed finite schedule gives

    sup_s ||f(s)||_1 <= (3lambda/4)gk,
    integral ||f(s)||_1 ds <= (3lambda/4)gk tau.

The first bound uses the total number of selected incidences, not all device cells; the second uses their total space-time volume. No independence is involved. The positive mild solution with these impulses and forcing, together with ||exp(Ms)||_1<=exp(-lambda gamma0 s), gives

    sum u(initial) <= gk + 3gk/(4gamma0),
    integral sum u <= gk/(lambda gamma0)+3gk tau/(4gamma0).

This proves both bounds in the source, uniformly over exterior computation duration, gaps between selected intervals, and total source size. The construction depends on the selected set only as an analysis weight; the physical device need not monitor that set or solve this equation.

## 4. Discontinuous weight comparison

The direction of the weight jumps is correct. A backward upward clamp corresponds to a forward downward jump of V. For positive tilted density rho_z, such a jump decreases Tr(V rho_z). There is no adverse multiplicative boundary cost. The terminal comparison uses V>=I; the initial comparison uses

    ||V(initial)|| <= exp(sum u(initial)).

On continuous pieces, differentiating Tr(V rho_z) contributes the negative backward derivative of V. At free coordinates that derivative cancels the M drift. At clamped coordinates the derivative is zero and the explicit selected-site allocation above is used instead. This is the relevant join; one must not also apply a fictitious negative free-coordinate drift at the clamped sites.

Injection contributes at most a sum u V. The paid real-creation activation gives the additional 4c²/lambda sum u V. Selected source-independent control mismatch contributes 2R||Delta_l|| V and integrates to 2R epsilon_ctl per selected location. Real outside couplings, intended system-only controls and other admitted commuting terms remain on. The resulting Gronwall comparison is valid for the non-trace-preserving positive tilted evolution; it uses no normalization or Jensen step.

## 5. Common dilation and all-order extraction

Use one fixed jump-history dilation with the initialized Markov fields and the same jump labels/phases for every complex parameter. On each finite register instance, the source and interaction operators are bounded and the finite-time jump-sector Dyson expansion converges uniformly on compact parameter sets. This gives an operator-norm analytic W(z); the weighted positive-evolution estimate bounds W(z)*W(z), including reference extensions. With an infinite spectator, this statement remains conditional on the previously supplied interaction-picture/domain premise and bounded admitted coefficients; it is not a formal unbounded-GKSL existence claim.

The weight comparison yields

    ||W(z)||² <= exp(k[C0+36R²c²g tau/lambda+2R epsilon_ctl]),

with the source's C0. The common-dilation construction allows the usual inclusive extraction, the product of evaluation-at-one minus evaluation-at-zero operations at the selected location parameters. All other locations retain their real actual interactions. Applying multivariate Cauchy on each radius-R contour gives the factor (R-1)^(-k), and hence the exact stated eta(R).

This is an initialized-isometry fault-amplitude statement for every finite selected set. Arbitrary initial finite source/system/reference correlations are allowed. Arbitrary unknown incoming field states are not. No classical jump-trajectory representation of the coherent source, product of marginal errors, Pauli randomization, source reset, or exposed noise record is assumed. A subsequent code/threshold receiver must still supply its usual ideal operations, support, initialization and gadget premises.

## 6. Radius, limits and interpretation

For the proposed radius at least two, the three caps imply respectively the QQ allocation condition, an R² exponent at most 1/4, and a control exponent at most 1/2. Also (R-1)^(-1)<=2/R. This gives exactly the displayed maximum bound and the 3/4 exponent, reduced to 1/4 when epsilon_ctl=0. The c=0 and zero-exposure cases require the separate direct reasoning stated in the source rather than division by zero.

In the fixed-diffusion convention c=sqrt(lambda)b, the leading term is proportional to b sqrt(g tau), multiplied by the stated conservative C0 factor. It does not tend to zero merely because lambda grows. In particular, the R² term remains 18R²b²g tau, and a_eff includes 4b². The proof therefore does not make the induced O(b² tau) dissipative disturbance disappear. Warm-source transients and uncontrolled source creation are paid by the initial-weight and activation terms.

The assumptions rule out the earlier unbounded-fanout counterexamples through actual location/guard incidence and system support bounds. They also exclude arbitrary unprotected PP couplings. This does not establish a useful operating point for every member of the model, nor physical feasibility of holding the injection/control premises fixed while increasing loss.

No numerical diagnostic was used as theorem evidence in this review. Gaussian-correlation and established microscopic Hamiltonian-noise admission methods remain ordinary primary comparators; this receipt makes no historical priority determination or practical advantage claim. Its conclusion is the precise new local receiving bound for the declared source-creating model.
