# Independent receipt: arbitrary-weight three-block pure-success value

Status: PASS, 2026-10-26. Governing proof: `arbitrary_weight_three_block_pure_success_value_theorem.md`; boundary dependency: `three_block_pure_success_boundary_stationarity_reduction.md`. This is a new whole-value/equality receipt for the specified actual source class, not an extension to mixed logical blocks or physical reset coherences.

## Actual source acquisition and scalar formula

For success pure logical state s and reset vectors vi, only ri=|<s,vi>|² affect the complementary Choi spectra. The Stinespring complement has three mutually orthogonal maximally entangled vectors Omega_i and three orthogonal flag vectors fi. Its input blocks are exactly [[d,ci],[ci,3bi]], ci²=3d bi ri. Its physical marginal is (d+sum bi)I3, so normalization 3d+3sum bi=1 makes it an actual TP complementary source. Independent physical/logical phases are absorbed in those Gram vectors; no extra mutual-overlap constraint is imposed on the ri. Any triple in [0,1]^3 is realizable using a success vector and a common orthogonal logical direction (dimension one gives the fully saturated boundary).

The reference has the stated center3d/leaves bi arrow with couplings ci/sqrt3, plus two spectator copies of each bi. The normalized WH output has three center-d, leaves-bi,bj arrows with couplings ci/sqrt6,cj/sqrt6, plus one spectator bi per label. Their traces and input/reference/output multiplicities are correct. Purification duality follows from the symmetric complementary outputs of the antisymmetric WH Stinespring dilation, so the dual and original deficits coincide.

Factoring each determinant against its zero-coherence counterpart yields the scalar integral exactly. The zero-coherence source has zero HOMOGENEOUS deficit for every d,b, not merely on the normalized hyperplane. In input terms the change of resolvent variable s=3t supplies the factor -3 and produces ui=d-ci²/[3(bi+t)]. Reference and normalized output factors remain at t. No affine trace or normalization term is missing.

## Frozen scalar zero geometry

Independently verified the quadratic numerator and its mean/deviation factorization. For positive a,b,c its leading coefficient is positive and constant term negative, so there is exactly one positive root. Assuming b<=c, evaluating at b,c brackets it; the factorization gives root<=(b+c)/2. At a root rescaled to t=1 these facts yield B<=A<=D<=C, hence v>=x>=y>=u>0 in the manuscript's reciprocal notation.

The zero equation and A+D=B+C give the stated sum/product identities. The derivative in a is (3/4)(x-y)²-(v-u)²<=0 because v-u>=x-y. For the companion derivatives, the only nontrivial term is y²-2u². With T=x/y>=1, the quadratic for u/y,v/y is strictly positive at3/4 and has vertex >=1. Since its two roots are real, 3/4 is strictly below the smaller root. Its numerator 6T²-7T+3 is positive by negative discriminant. Thus u/y>3/4>1/sqrt2, proving both companion derivatives strictly negative. This is valid also when b=c (the a derivative may vanish, but the other derivatives remain strict).

## Actual crossing and joint stationarity

Each ui(t)/t=d(1-ri)/t+d ri/(bi+t) is positive and strictly decreasing in the interior. At every zero of Gi(t), the frozen partial derivative signs therefore force a strictly positive derivative along the actual resolvent path. Every zero is a strict upward crossing. The finite lower-end value is negative, while the upper tail is 4d/(3t²)+O(t^-3)>0. Continuity and the strict upward-crossing property give exactly one zero, with the stated negative/positive sides; no free pointwise choice of ui is used.

Differentiation gives precisely the ci and bi formulas (5). At ci-stationarity the weighted Gi integral vanishes. Subtracting its value at the unique crossing gives both strict signs in (6); the identity for the unweighted integral uses (t-theta)/(bi+t)=1-(bi+theta)/(bi+t). All these integrals converge.

At fixed b,c, every ui has d derivative one. The explicit baseline derivative integrates to zero: an antiderivative of the full displayed baseline is 3ln(d+3t)+3ln(3d+t)-6ln(d+t), with equal endpoint limits. Thus partial_d Delta=sum integral Gi>0, while every partial_bi Delta<0 at overlap stationarity. The actual affine normalization has equal coefficients3 on d and all bi, so constrained interior stationarity requires these derivatives equal. This is impossible. The coordinates are locally independent because all inequalities ci>0 and ci²<3d bi are strict. No fixed-p-only conclusion is incorrectly promoted: the d variation is essential.

## Every boundary stratum received

The finite d,b,c domain is compact and every feasible point is an actual source, so a negative value has a global minimizer without any arbitrary-dimensional attainment assumption. At d=0 or sum b=0, coherence vanishes and the value is zero. A zero physical weight is already the received two-block class.

If ri=0, the original reference vector |i>vi is orthogonal to the whole success reference code and every other reset physical label. Its isolated reset summand has homogeneous deficit zero. Removing it and normalizing the remaining mass gives an actual TP source with at most two reset blocks, not an arbitrary compressed state. This receives intersections of zero-weight/zero-overlap boundaries and their equality cases.

With all remaining weights positive, a proper saturated-overlap face is excluded by an actual inward path. Each saturated input block opens with hi=d xi/(d+xi). The reference stays faithful unless all three overlaps are one. Exactly one output pair opens when exactly two overlaps are saturated; its normalized-output opening is hij=d/[1+(3d/2)(1/xi+1/xj)]. The vector and perturbation coefficient in the boundary note are correct. Thus the deficit's t ln t coefficient is hi, or hi+hj-2hij, respectively. Since hij is strictly below the harmonic mean of hi,hj, both coefficients are positive and give a strict descent. The all-three-saturated corner is correctly excluded from this expansion because its reference also opens a kernel.

That fully saturated corner is the already received identity-or-arbitrary-qutrit-reset theorem, which is strictly positive for p,q>0. Therefore every negative minimum would be interior, where the stationary contradiction excludes it. Once positivity is established, an interior zero would also be a global minimum and is excluded; the proper saturated faces cannot minimize either. The two-block boundary equality theorem then leaves exactly pq=0 or sum wi ri=0. No other boundary zero is inferred from a limiting strict inequality.

## Independent replay and scope

Replayed `three_star_single_crossing_symbolic_check.py` and `three_star_resolvent_stationarity_check.py`: exact numerator/root identities and homogeneous value/gradient comparisons PASS. Added `three_star_whole_value_independent_source_check.py`:12 complex original sources, actual complementary duals, all three full spectra and scalar integrals PASS, maximum discrepancy1.32e-15. These support the exact derivation, not a sampled sign premise. The fully saturated strictness dependency is documented in `arbitrary_qutrit_mixed_reset_value_theorem.md` and its independent audit.

This pays arbitrary physical weights with pure logical success and at most three pure logical reset blocks. It neither assumes nor proves generic affine convexity, permutation balancing, arbitrary mixed logical reset blocks, arbitrary physical coherences, or unrestricted WH3 positivity. The earlier affine-balancing failures remain compatible. No correction required.
