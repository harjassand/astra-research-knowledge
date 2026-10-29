# Independent receiving review: gap-free online encoder learning
2026-10-29. Reviewer derive_matching_survival_bound. Final scoped acceptance and resolution of initially pending obligations appear below.

## Independently checked mathematics
The one-shot estimator correctly includes the nonunital identity contribution. For arbitrary pair CPTP maps its conditional mean is delta, and its exact second moment is747/16+(3/2)delta. Eight independent arbitrary nonunital fixtures exhaustively summed input settings/signs and output settings/outcomes; both identities pass.

For any Hermitian unitary candidate swap and trace-preserving source Kraus family,
 delta=(1/(2D))sum_a||[S,K_a]||F².
This proves positivity and, under an exactly commuting true swap, the sharper realizable comparator bound delta(C)≤(9/2)||C−Ctrue||F². Twenty collective-source fixtures pass this bound. Quadratic approximation, not the v1 Lipschitz bound, supports epsilon=T^−1/4 and M=O(T^3/4).

Caputo–Liggett–Richthammer arXiv0906.1238v4 was actually read: section1.2 defines the unnormalized edge-rate generator; Theorem1.1 in section1.3 equates its interchange and graph random-walk gaps. An unweighted star has gap1 for n≥3. Decomposing a finite unitary representation into irreducibles transfers this lower bound from the regular representation to swap conjugation; the kernel is precisely its commutant. The n4 physical operator-conjugation generator was independently diagonalized and has gap1. No source excitation gap is inserted by this group inequality.
Primary: https://arxiv.org/html/0906.1238v4 .

The resulting full-P scalar-residual estimate is correct. If Ecomm is the group average, it acts on the full spin-zero irreducible space as a scalar. The scalar trace of each Kraus operator minimizes its P-restricted Frobenius residual. CPTP normalization gives sum||(K_a−a_a I)P||F²/d=1−sum|a_a|², and Poincare bounds it by(D/d)sum delta_i.

## Explicit full-memory lift, not an analogy
For arbitrary joint Kraus K_a on physical data X and memory M, define
 E_i(C)=(1/(2D))Tr_X sum_a [S_C tensor I,K_a]†[S_C tensor I,K_a].
It is a positive memory operator; for every memory state sigma its expectation equals the reduced-channel loss delta_i(C;sigma). The scalar proof applied to every sigma establishes
 Hbad(C) ≤ (D/d) sum_i E_i(C).
Here Hbad is the already proved actual orbit bad-branch effect I_logical tensor Hbad(C). Thus the bad-slot probability on an ARBITRARY correlated logical-memory input is bounded by the same expression evaluated on its actual memory marginal. Fresh known-probe inputs sample precisely that marginal, whereas the role and candidate draws must be independent of the pre-call source map and current memory. This supplies the missing operational interpretation without assuming an independent payload.

Twenty arbitrary joint CPTP source-memory fixtures independently verify the operator inequality, not just independent-state samples. The complete quantum online proof must apply it to the actual observed-history filtration, summing over unobserved prior virtual branches rather than pretending those labels were measured.

## Finite v2 learner
The stereographic chart covers rotations through quaternion sign equivalence; inverse-chart Lipschitz factor2 and quaternion-to-rotation factor2sqrt2 give the stated2sqrt6/m net radius. Grid points outside the unit ball are harmless additional rotations. Rational matrix entries and common factorial denominator are valid, though expensive.

Shifted loss is in[0,1]. For update1−eta ell with ell=1_probe fhat/p and eta≤p/2, log potential gives regret≤logM/eta+eta sum comparator ell². Its expectation is bounded bylogM/eta+eta T/p. The constant shift cancels in regret, restoring the stated45 factor. A fixed nearest true comparator is valid even for causally changing loss sequences. Exact integer weights and capped rejection sampling have polynomial bit complexity in the declared horizon, not practical complexity. Aborting on sampler-cap failure costs at most(n−1)T2^−r. Rational descriptions do not by themselves compile accurate physical gates.

## Three-role closure to be supplied by author
Use PROBE p, MATCH a, SERVICE s, with p+a+s=1. Draw the same hidden candidate law before the role coin. Probe observations update all star experts; no other role is used as fictitious loss feedback. Matching failure satisfies q(C)≤praw(C)≤(D/d)sum delta_i(C), so the same regret yields
 E total matching failures ≤a(D/d)(n−1)L_T,
 E virtual bad services ≤s(D/d)(n−1)L_T.
The service-to-test hazard ratio s C_n/a=R retains the model-free guard under arbitrary source noise. Under the common-algebra promise, Markov bounds failure-budget abort by the first expectation/(b+1); a private-role Chernoff bound handles insufficient service count at the finite horizon; sampler/control budgets remain separate. This does not require a high-probability per-round loss theorem. Changing candidate frames do not change the outer logical register because each good branch is identity in its own actual encoder/decoder coordinates.

The operational theorem, concrete finite parameter choice, strongest equally informed comparator and physical control budget remain to be frozen and reviewed before accepting a complete protocol. Existing small numerical trajectories must not be described as full outer-code execution or proof of finite-precision physical operation.

## Additional executed evidence and comparator
Replayed the author's actual20,000-round product-probe/retained-bath fixture:9940 probes,10060 services; maximal star-transfer residual1.28e-15. This is a floating small-net diagnostic with exact average private-orbit memory evolution, not complete outer-code execution or the exact integer learner. The separately supplied200,000-round results were inspected, not replayed in this review.

`HIGH_RATE_FULLPATH_COMPARATOR.md` supplies a strong alternative using K'>d/2 singlet coding and full-path tests, same online learner and at most factor2 transfer loss. It retains the actual higher-complexity encoder/decoder costs. Thus the online bridge can be meaningful while a generic exclusivity or practical-control advantage claim remains unsupported.

# Final receiving determination for v1+v2+v3
The earlier pending items above are resolved as follows; the working narrative is retained to expose what was actually challenged.

The author's THREE_ROLE_GUARDED_READINESS_v3.md supplies the exact conditional role boundary, finite cap and complete outer-code composition, using actual accepted-memory closure from the governing orbit theorem. LEARN calls are neutral for the competing service/test hazard and can alter source memory arbitrarily. The common current candidate law on validation and service is explicit. Completion on the last cap call precedes cap abort. Dummy zero-loss rounds after stopping are a mathematical device, not execution or a future-source oracle. Their shifted feedback can be identical across candidates, leaving weights unchanged. The cap/sampler abort probability is separately budgeted.

At n=4h,B=2^h,T=9B, p=1/3,s=2/[3(C+1)],a=Cs, all role constants and outer tail bounds check. The acceptance lower bound follows from the EXPECTED cumulative loss through Markov, plus the independent private-role Chernoff bound; no high-probability regret theorem is smuggled in. Correlated payload/source inputs are handled by the explicit operator effect above and the received orbit branch closure, not by replacing actual memory after service with an independent bath. This proof yields a full accepted-map statement with its original retired-record scope, not uniform normalized rare-success fidelity or future-channel identification.

`check_three_role_parameters.py/.json` supplies an entirely integer/rational concrete learning-rate/net instantiation and checks the constants. It gives vacuous readiness at h5..40; at h80 the failure-abort upper bound is about0.04503, and at h120 about1.401e−7, before role and sampler allowances. These astronomically large examples establish finite/asymptotic existence, NOT practicability. The native source-qubit exposure ratio is exactly1/72; all classical learner time, enormous exact integer widths, trusted control synthesis, buffers, endpoint calibration and private randomness are outside that ratio and remain paid.

The exact sampler off-by-one found during inspection was corrected. Replayed final exact-kernel script:27 exact proper rotations,6912 exact update checks,256 steps, forced32-rejection boundary returns failure after exactly32 draws. The floating20k/200k physical-memory trajectories use a different signed exponential-weights kernel and are correctly labelled; only20k was independently replayed here. They do not execute the large outer code or compiled exact learner.

The high-rate full-path comparator is now included in v3, and separately derived in HIGH_RATE_FULLPATH_COMPARATOR.md. It can obtain the same polynomial gap-free learning-transfer order with at most factor2 coefficient while paying the high-rate singlet encoder/decoder rather than simple blocks/permutation routing. This review establishes no generic control or sample-complexity advantage.

Subject to the explicitly inherited mathematical guard/compiler dependencies and exact common joint algebra for readiness, the v1/v2/v3 construction is ACCEPTED AT ITS STATED MATHEMATICAL SCOPE. Historical novelty, practical complexity, physical controller noise certification, experimental performance and universal unknown-noise yield are not accepted claims. The small-code transfer obstruction is reviewed separately.
