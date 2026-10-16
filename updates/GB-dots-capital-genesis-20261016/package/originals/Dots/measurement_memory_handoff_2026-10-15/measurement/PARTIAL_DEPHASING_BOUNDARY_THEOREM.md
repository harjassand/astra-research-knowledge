# Qualified partial unread dephasing at scheduled boundaries

Date: 2026-10-15. Verdict: **PASS for the stated compositional channel model**, independently audited. Exact extra pinching can be relaxed to finite-strength unread dephasing, including finite-strength endpoints if their latent failures are explicitly charged. This does not qualify generic noisy measurement hardware or concurrent Hamiltonian noise during a presumed isolated boundary channel.

## 1. Channel interface and actual experiment

Retain the exact correction-first, fixed full-reservation, arbitrary finite persistent-bath model of REPORT.md. A clean parent's weak perturbation V_i is supported in its entire A_i, with ||V_i(t)||<=J_i, and obeys the same full-footprint detection/no-local-logical condition. Retain fresh isolated boundary reservoirs and a fixed common dilation under all perturbation deletions/interpolations. All extra boundary outcomes are unread and unused by later controls.

Split the total weak exposure tau_i into M_i prescribed cells. Initially suppose complete pinching D_G is actually implemented at the entering and final boundaries. At each INTERNAL boundary implement exactly

    T_(i,b) = r_(i,b) Id + (1-r_(i,b)) D_Gi,             (1)
    0 <= r_(i,b) <= 1,
    D_Gi(X)=sum_s P_(i,s) X P_(i,s).

These are full joint-memory/bath channels with identity action on the persistent bath. Independent fresh boundary channels are required: the scalar convex weights are input-independent, and the latent mixture choices are independent across parents. The simple formula below additionally assumes independent internal choices within each parent.

For one Hermitian involution S, an isolated ideal Markov dephaser realizes precisely

    exp[s gamma(Ad S-I)] = r Id+(1-r)D_S,
    r=exp(-2gamma s).                                 (2)

For a full group G of rank greater than one, (1) is a specifically qualified channel, not a generic identity for generator-wise dephasing. Section 5 gives the valid generator-wise extension.

A canonical dilation of (1) has Kraus operators sqrt(r) I and sqrt(1-r) P_s. Its latent label says either 'skip' or 'complete pinching with sector s'. These labels need not be physically available. They define a complete Kraus representation of the actual unread channel, exactly as in UNREAD_MEASUREMENT_REFINEMENT.md.

## 2. Fixed-pattern theorem

Condition only on the state-independent mixture pattern eta, not on generated syndrome outcomes. Merge consecutive weak cells across skipped boundaries. Successful complete pinchings delimit blocks. With exact entering and final pinchings every weak cell belongs to a block with both required sector endpoints.

Let a_(i,c) be the integrated norm of the weak perturbation in original cell c. For a merged block B define

    a_(i,B) = sum_(c in B) a_(i,c).

All actual skipped-boundary operations remain in the physical circuit. In (1) they are identity; in the generalization of Section 5 they need not be identity. They are fixed interventions with norm-one dilations and preserve the full G_i sectors.

For each block, define the latent bad predicate by inequality of its entering and exiting complete-pinch labels. Deleting that block's entire weak perturbation preserves its entering sector under all other interpolations, including arbitrary remote shared-bath dynamics. Hence its bad output projector annihilates the complete noise-deleted dilation as a full operator identity. The deletion-null theorem gives product a_(i,B)^2 for any selected block set.

A parent is bad when ANY of its blocks is bad. Union over one witness block per selected parent gives the conditional full-input effect bound

    F_R(eta) <= product_(i in R) p_i(eta_i) I,
    p_i(eta_i)=min{1, sum_(blocks B of i) a_(i,B)^2}.    (3)

This is uniform in arbitrary initial memory-bath-reference correlations. It neither normalizes syndrome outcomes nor serializes crossing shared-bath pulses.

Under the same full-footprint support condition, each good block has a net patch Pauli commuting with G_i, hence is a code stabilizer on the encoded Pauli orbit. A good parent adds no support. A bad parent is conservatively charged on its whole bounded reservation, and all bath coefficients remain in chronological order. The original common-decoder good-CP construction therefore applies to these latent labels.

## 3. Exact average and cross-parent composition

The actual channel is the average of the conditional-pattern channels. Because (3) is a uniform operator inequality and the parent pattern families are independent,

    F_R <= product_(i in R) bar_p_i I,
    bar_p_i = E_(eta_i) p_i(eta_i).

In particular,

    bar_p_i <= min{1, E sum_B a_(i,B)^2}.               (4)

For cell actions a_1,...,a_M and independent internal skip probabilities r_1,...,r_(M-1), two cells c<d are in the same merged block exactly when every boundary c,...,d-1 is skipped. Expanding squared block actions therefore gives the exact identity

    E sum_B (sum_(c in B) a_c)^2
       = sum_c a_c^2
          +2 sum_(c<d) a_c a_d product_(b=c)^(d-1) r_b. (5)

For equal weak durations delta=tau/M, common bound J, and common skip probability r=1-q,

    bar_p <= min{1, J^2 tau^2/M^2 * F_M(r)},
    F_M(r)=M+2 sum_(k=1)^(M-1) (M-k) r^k.             (6)

Thus the requested expected squared BLOCK-DURATION sum is exactly tau^2 F_M(r)/M^2. The bound is on pulse action; no factor equal to the number of stabilizer generators appears when the complete-G channel (1) is given.

For 0<=r<1,

    F_M(r)=M(1+r)/(1-r)-2r(1-r^M)/(1-r)^2.

At r=0 the budget is J^2 tau^2/M; at r=1 it is J^2 tau^2. A convenient looser bound is

    bar_p <= min{1, J^2 tau^2 * min[1,(1+r)/(M(1-r))]}.

For fixed q>0 and large M the leading factor is (2-q)/(Mq). The exact expectation of the capped quantity in (3) can improve (6).

Shared bath correlations do not obstruct this average, because the conditional inequality holds on the full input space before averaging. Independent PARENT pattern families are what factorizes its scalar right side. If channel implementations have correlated mixture choices across parents, the valid generic expression is E_eta product_i p_i(eta_i), not necessarily product_i E p_i. Matching individual boundary-channel marginals is insufficient to infer process-level independence.

## 4. Endpoint requirements and a fully partial version

Formula (6) assumes an actual complete entering pinching and an actual complete final pinching. They cannot be inserted mathematically for free. A proved known entering sector can substitute for the initial pinching on that stated input domain. A terminal decoder measurement only substitutes for the final boundary if it actually supplies that boundary at the needed time; final-decoder equivalence does not suffice before later interactions or reuse.

Suppose the two endpoints instead implement independently qualified mixtures with complete-pinching weights q_in and q_out. Include their latent success/failure flags in the full instrument. Charge the ENTIRE parent as bad whenever either endpoint lacks the complete-pinching component. Conditional on both endpoint successes, use the internal block theorem. Independence from the internal pattern yields

    p_parent = 1-q_in q_out + q_in q_out bar_p_internal. (7)

Here bar_p_internal<=1 and may use (4) or (6). The same per-parent averaging gives product bounds across independent parent families, including parents whose endpoints fail. On such branches one drops the quantum mismatch constraint and uses the trivial effect bound I; their arbitrary local memory action is charged on the full reserved patch.

Equation (7) permits EVERY extra boundary to have finite strength and no readout. The term 1-q_in q_out is a conservative floor in THIS CERTIFICATE, not a proved physical logical-error floor. Some failed-endpoint branches can be harmless, but this proof does not use that fact.

For one involution and equal endpoint exposures s_e, q_in=q_out=1-exp(-2gamma s_e). Small certified endpoint failure therefore requires nonzero exposure, asymptotically s_e approximately (1/(2gamma)) log(2/epsilon) for endpoint budget epsilon. Initial exact correction-controller requirements and the final recovery remain unchanged.

## 5. Independent generator dephasing: safe remainder and its limits

Let S_1,...,S_m be commuting stabilizer generators, and D_a=(Id+Ad S_a)/2. Isolated generator dephasing with exposure s_a gives

    T = product_a [r_a Id+(1-r_a)D_a],
    r_a=exp(-2gamma_a s_a).

Because the D_a commute, their product is D_G. Expand the product over subsets A of generators:

    T = q D_G + (1-q) R,
    q=product_a(1-r_a),                               (8)
    (1-q)R = sum_(A proper subset of {1,...,m})
                  [product_(a in A)(1-r_a)
                   product_(a notin A)r_a] D_A,
    D_A=product_(a in A)D_a, D_empty=Id.

For q<1, R is CPTP as a normalized convex combination of partial stabilizer pinchings. For q=1 there is no remainder; for q=0 all boundaries are conservatively skipped as complete-G boundaries.

This extension is valid with the effective skip probability r_eff=1-q in (5)-(6). R is skipped ONLY as a complete-syndrome cut; it remains in the physical block evolution and the common dilation. Its projectors are in the stabilizer algebra, preserve every full G sector, and act scalar or zero on each encoded Pauli orbit. Consequently it neither spoils block deletion nullness nor adds support. The Duhamel proof permits these fixed norm-one interventions between perturbation insertions.

It is not valid to replace R by identity as a channel. It is also not enough for a generic remainder merely to commute with G: a logical unitary within a syndrome sector commutes with every stabilizer yet can change the logical state while every mismatch is zero. Sector preservation suffices for deletion nullness, but support requires the additional stabilizer-algebra property (or another separately proved harmlessness property). The specific R in (8) has that property.

### Why generator-wise dephasing is not usually a scalar full-group mixture

For independent Z generators on two qubits, the coherences |00><01|, |00><10|, |00><11| are multiplied by r_2, r_1, r_1 r_2. A channel r Id+(1-r)D_G would multiply all three by the same r. Generic finite generator-wise rates do not satisfy this.

### Maximality of the extracted complete component

For independent Pauli generators, their products are distinct orthogonal Pauli operators on the full memory Hilbert space. The random-unitary coefficients of T are

    w_g=product_a [1+(-1)^(g_a) r_a]/2,

whereas D_G has uniform coefficient 1/2^m. Their Choi vectors are orthogonal. Thus T-q' D_G is CP exactly when w_g-q'/2^m>=0 for every g, and the largest possible complete-pinch weight is

    q'_max=2^m min_g w_g=product_a(1-r_a)=q.            (9)

This is a statement about extracting that particular D_G subchannel on the full memory space. It is not an optimality theorem for all weak-measurement protection analyses. Dependent redundant generators can give a larger combined minimum after coinciding group products are aggregated; (8) remains a safe lower bound.

## 6. Measurement time, noise during boundaries, and resource tradeoff

The weak exposure tau in (6) and the total reserved duration theta are different. With M weak cells, M-1 internal boundaries, initial/final boundary times s_in,s_out, and correction/reset overhead theta_0,

    theta = theta_0 + tau + (M-1)s + s_in+s_out.       (10)

Equivalently, if one counts M equally costly boundaries after the weak cells and charges the entering operation in theta_0, theta=theta_0+tau+Ms. Recompute all reservation, conflict, latency, guard, and pending constants using theta and the full dephaser supports.

At fixed tau and fixed boundary exposure s>0, increasing M improves (6) but increases theta linearly. This can worsen the scheduled memory's kappa*theta conflict/latency terms. There is no cost-free M→infinity limit.

At fixed TOTAL internal dephasing exposure S=(M-1)s and fixed finite gamma for ONE generator, r_M=exp[-2gamma S/(M-1)]. With a=2gamma S,

    lim_(M→infinity) F_M(r_M)/M^2
       = 2 integral_0^1 (1-x)exp(-a x) dx
       = 2(a-1+exp(-a))/a^2,                         (11)

with value 1 at a=0. Refining a fixed total exposure does not drive the certified error to zero. At large a the factor is approximately 2/a. If all endpoint exposures were also shrunk as 1/M, their success probabilities would vanish and the conservative endpoint certificate would approach 1; endpoints need their own budget.

For m>1 independent generator dephasers at the same short boundary, q(s)=product_a(1-exp(-2gamma_a s)) behaves as (product_a 2gamma_a) s^m. At fixed S and M→infinity, Mq(s) tends to zero for m>1. This coarse 'all generators complete at the same boundary' certificate then tends to the unsuppressed action-squared budget. This is a limitation of this block extraction, not a physical no-go for generator-wise continuous dephasing. Equation (9) shows it cannot be repaired merely by extracting a larger identical complete-pinching component at each boundary; a different analysis could exploit partial information.

There is also a structural limit to simply enlarging the noisy footprint to include detector data. The independent rank proof in [FULL_DETECTOR_FOOTPRINT_CLOSURE_OBSTRUCTION.md](FULL_DETECTOR_FOOTPRINT_CLOSURE_OBSTRUCTION.md) shows that if all measured checks are supported wholly on D and the unchanged zero-good-support certificate is demanded against every Pauli on D, then D must be a fixed pure stabilizer-state tensor factor of the code. Thus blindly setting A equal to the entire detector data support cannot qualify a nontrivially coupled code patch. This does not invalidate the present conditional theorem, which keeps its justified smaller weak-error footprint and qualified boundary channels; it identifies why arbitrary detector noise needs a different certificate or separately charged faults.

Most importantly, (2) or (8) requires the QUALIFIED boundary channel on the retained system. Simultaneous noncommuting Hamiltonian noise during a finite dephasing operation does not in general equal an ideal boundary channel followed or preceded by an independent weak cell. For example, starting from |0>, pure Z dephasing leaves the state unchanged; a simultaneous hX Hamiltonian changes its Z population at order h^2 s^2. The ideal dephasing formula alone cannot represent that process. Safe implementations here either isolate the weak coupling during boundary operations, have commuting dynamics that factor exactly, or separately qualify the full noisy-boundary channel and its support. The report does not assume that a laboratory calibration establishes any of these.

## 7. Exact algebraic tests and full-input shared-bath checks

Original script: check_partial_dephasing.py. Results: partial_dephasing_results.json.

Exact rational tests use r_1=1/3 and r_2=2/5. They verify q=2/5 and

    R=(2/9)Id+(4/9)D_1+(1/3)D_2
     =(11/18)Id+(2/9)Ad S_1+(1/6)Ad S_2.

All weights are nonnegative and sum to one. The script verifies exact matrix identities, trace preservation, full-sector preservation, the three distinct coherence factors 2/5,1/3,2/15, and maximal CP pinching weight q=2/5. The nonzero unnormalized Choi eigenvalues of R are 22/9,8/9,2/3. It also verifies the endpoint-failure effect (1-q_in q_out)I exactly in a zero-noise example and checks the block-square identity for 28 rational (M,r) cases by exhaustive pattern enumeration.

A separate floating-point check uses two crossing three-cell parents on disjoint memory qubits sharing a noncommuting bath. It expands all 1,296 actual latent Kraus branches, representing 16 independent success patterns, and verifies 48 conditional subset-effect inequalities plus the averaged marginal/joint bounds. The branch sum agrees with direct composition of the partial channels within 8.17e-16; normalization error is 9.03e-16. The averaged two-parent bad effect has maximum eigenvalue 6.17654e-5, below the predicted product budget 3.68687e-4. No bath initialization is fixed: effects are tested on the whole joint input space.

These tests corroborate the proof; they do not certify physical devices or replace the imported support/contour machinery. PARTIAL_DEPHASING_INDEPENDENT_AUDIT.md records an independent proof audit.

## 8. Closest prior art and claim boundary

The central weak-measurement decomposition is established explicitly in Dominy, Paz-Silva, Rezakhani and Lidar, *Analysis of the quantum Zeno effect for quantum control and computation*, J. Phys. A 46, 075306 (2013), Section II.1, Eq. (4): their nonselective weak measurement has an equivalent three-Kraus description consisting of identity with weight zeta=sech(epsilon) and projective pinching with weight 1-zeta. Section II.2 treats products over stabilizer generators. They derive protection bounds and parameter tradeoffs; their introduction explicitly assumes instantaneous measurements. Primary source: https://arxiv.org/html/1207.5880v2#S2.SS1 and https://arxiv.org/abs/1207.5880. Their earlier PRL is https://arxiv.org/abs/1104.5507.

Thus neither the mixture interpretation, unread weak stabilizer measurement, nor weak-Zeno suppression is claimed as new. The result established here is a conditional local joint-subset-effect and completion-support interface for the specified scheduled memory architecture, including its scalar pattern average, partial-pinch remainder qualification, and explicit endpoint/resource accounting. No priority claim is made for that interface without a broader literature audit.

The relaxation is real but narrow: exact COMPLETE pinching can be replaced everywhere in the extra protection layer by a specified finite-strength dephasing channel, with (7) charging endpoint failures. The channel's exact structural form, bath isolation, independent freshness, fixed timing, locality, original exact corrections, and perfect final recovery remain assumptions. Arbitrary imperfect measurements, coherent implementation errors, and uncontrolled continuous memory noise remain outside this result.
