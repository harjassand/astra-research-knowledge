# Independent whole receiving review: energy-resolved native compiler

31 October 2026. Verdict: PASS at the mathematical finite-circuit/existence level, with the access-dependent high-rate resource scope stated in the source. This is a new receiving theorem, not a revision of the frozen baseline resource ledger, an implemented simulator, or a practical advantage claim.

## 1. Full source and dependency binding

I read all eight sections of the 14,528-byte `ENERGY_RESOLVED_NATIVE_RECEIVING.md` and verified SHA-256 `b87596c5553e5b06f37d03bb894f9bb75a4c4dfcbd0ccaab89f0813c69d07262`.

Its complete native receiver remains `f503c80089c85006856e6ca1ea8b536bb36e0aa4931db071320a33a056a07192`, independently reviewed in `0fa56f50ca5160cbbbe9dc51c360f2b34b9e9e301894dc49c9ce6288d8cafeed`. Its new energy-count input is `ac06ea4451f653db3824792b259a553057ca053639e59a784c87b6a2cbb320f3`, with mathematical receipt `4bb1b450ae3ba82b527655eabbbc97c5bc3034b92f173a70e35d10d9b5a68a48`. Only that receipt's mathematical portion is used; its historical resource-file versions do not become new algorithm premises.

The optional structural open-chain port binds to corrected source `92a63305a6ec512039c784d213bae63a97233002e00f3da8ece10518d35170a6`, local receipt `e32303f8f9dea00b383cac324413024fbba7b7fc8a19d38c8bcf14fc17dc62fa`, and tail correction binding `3958d005a7dd92a7b2ee593c6877d7165ad8b327815afab01b7e106e3dd98ff1`. That operation is optional: the generic paid slack-amplification branch is independently a valid input realization.

## 2. Distinct physical, crossing and QQ parameters

The theorem correctly keeps three quantities distinct. The energy-form certificate e bounds PKHKP and prices the physical count. The acquired offdiagonal normalization rho prices QKP and PKQ. The full normalization b still prices QKQ, the actual generator norm, and high-rate admission. Replacing b by rho everywhere would be false; the present source does not do that.

The proposed certificate tightenings are valid: H <= hQ gives e^2 <= h rho^2 as an available upper certificate, and ||[K,H]|| <= 2hb together with H_Q >= g gives the fallback a_E <= 2hb/g. These are bounds on certificates, not algorithms for optimal norms or inverse-H access.

From an acquired K/b, projected blocks plus slack singular-value amplification acquire QKP/(2rho) and its adjoint at real cost proportional to max(1,b/rho), up to precision factors. The target norm is at most one half. Robust raw precision and controlled inverses must be included, as the source explicitly requires. An individually acquired structural port can avoid this ratio cost, but a mere variance estimate or unrelated opaque K oracle cannot.

Gap normalization is consistent. With H' = H/g, K' = K/sqrt(g), lambda' = lambda g, the normalized injection square is e^2/g^2 and normalized kappa is kappa/g. Therefore the count exponent is the claimed original-parameter C_E = e^2 T/kappa^2. The other dimensionless parameters mu = lambda g T, B_diag = b^2 T/g and R = rho^2 T/g are likewise correct.

## 3. Actual count and changed positive word sum

The two high-rate conditions separately earn scalar separation and the energy-count absorption. The inherited tilted bound gives 2^(p+1) exp(32u C_E), including arbitrary initial source energy and arbitrary prescribed joint instruments. Its Chernoff cap has the stated leading C_E term and the remaining h/kappa-dependent initial/control/tail term. No expected-count replacement is used for the coherent circuit's cap.

A slack offdiagonal block has normalization 2rho, so c_off = 2sqrt(mu R) is necessary. The QQ coefficient remains c_diag = sqrt(mu B_diag). Each Q dwell still contributes its factor two. Thus the displayed nonsymmetric Metzler matrix and its symmetric similarity form exactly majorize the actual ordered operator words. Both crossings and QQ insertions carry the Hamiltonian phase -i; the physical damping jump does not.

From mu >= 4096 B_diag and rho <= b, one obtains c_diag <= mu/64, c_off <= mu/32, delta >= 15mu/32, c_off/delta <= 1/15 and 2c_diag/d <= 1/15. These are stronger than the old bridge/self-insertion bounds needed by the received proof. In particular s = 2c_off^2/d <= 16B_off/3 with B_off = 4R. The fast propagator F remains exactly the old g-normalized source kernel; its contraction, factor two, derivative and acquired LCHS cost do not change.

The old endpoint formulas apply with crossing coefficient c_off and the newly defined delta. The event-row estimate leads to the same no-event and jump envelopes with B_off in the positive floor. The physical event still appends sqrt(mu)L/sqrt(g), retaining its true source state and output label. The source stack normalization has not been absorbed into rho or e. Integrating the envelope on tau <= 1/(128B_off) gives the inherited bounded proposal mass and the same padded complete-isometry normalizer.

As a nonproof diagnostic I also checked 200 randomly scaled high-branch scalar instances, including widely separated R and B_diag. The admission ratios and event-row envelope were consistent with the derived inequalities to ordinary floating-point tolerance. The operator argument, not these numerical tests, is load-bearing.

## 4. Deterministic schedule and paid Hamiltonian duration

With D = 128B_off + M + p + log(100/epsilon) + 4 and 1/(2D) <= tau <= 1/D, the stated counts obey S = O(D) and

 S tau <= 1 + (M+p+4)tau <= 2.

This follows using ceil(1/tau) <= 1/tau + 1; fixed extra ceiling margins only change the absolute constant. Splitting at controls is included. Incorporating M into D does not create an M-squared number of first-event calls.

For a binary duration in one padded interval slot, the sum of all controlled fixed-time Hamiltonian evolutions is at most T*tau. Charging this worst bound for every slot and amplification call gives alpha_0 T times dA(Kcap+1) up to a constant, because S*tau is bounded. The separate per-piece synthesis/query overhead still scales with S, the bit precision and the padded word length. This is a genuine deterministic schedule argument; it does not assume that realized coherent paths can be charged by their actual total duration without a circuit construction.

## 5. Finite source and numerical re-binding

The Doob crossing bridge uses the new s,d, while the independent QQ insertion process uses rate 2c_diag. The latter-to-down ratio is at most 1/15. Thus the earlier full-visit domination and E[2^V] <= 4 exp(7s tau) bound still apply. Conditional tail estimates divide by the actual original endpoint floor p0 once. The same raw-uniform atom/full-CDF convention, capped inverse bisection, finite Poisson scan, sorting and unconditional overflow treatment remain actual operations, not a newly assumed conditional-sampling oracle.

The explicit numerical substitutions are essential and correct:

- e_step, beta, sigma and eta use the new global S and the actual amplification degree.
- Lphys keeps c_diag and the actual alpha_LN, since it bounds the true joint generator and its frozen count augmentation.
- The outer event floor depends on sqrt(B_off), while its derivative numerator uses Hs + c_diag + mu hN. Consequently Lout has exactly the stated form; no false replacement of the full coupling by rho is made there.
- qrate and duration-TV estimates use nu + 2c_diag and the true QQ Poisson rate. Global near-boundary/tie cuts and remaining-time floors are retained.
- Word timing still pays Hs + mu(alpha_HN+1), since the source contraction kernel has not changed.
- All real offdiagonal SVA or frame-circuit operation counts and tighter raw errors must be added to the per-operation subdivision. The symbolic count of crossings does not make those operations unit cost.

The same common-uniform L2 outer comparison and complete-isometry amplification then apply. Private timestamp errors are compared through the actual remaining joint channel, using its count-augmented generator bound, not through total variation between grid and continuous timestamp laws. The exact process's jump-count tail supplies the discarded CP mass; there is no inference of an approximate-process MGF. Every finite circuit branch still has an unconditional CPTP continuation.

Positive-parameter inverse factors may increase bit precision logarithmically, while generic b/rho amplification increases actual operation cost. The source distinguishes these two effects. Certified b = 0, lambda = 0 and T = 0 receive their frozen branches. A zero crossing certificate with nonzero QQ coupling is not misclassified as zero K; choosing a positive crossing upper bound avoids an undefined bridge.

## 6. Resource and process conclusion

Z = 1 + C_E + R + max(1,h/kappa)[p+log(1/epsilon)] bounds M+B_off+p+log(1/epsilon), hence S = O(Z). The per-call virtual count, finite source precision and source-only contraction implementation have the claimed logarithmic dependence on global S, rapid rate and requested error, multiplied by the explicitly retained source-conditioning and acquired-access factors. The integer complete-isometry amplification cost and actual stack normalization remain in those products.

Accordingly the high-branch near-linear extensive-activity and H0-action statement is justified only in the qualified sense displayed by the source: actual source and operator costs, including generic b/rho when used, are multiplied rather than omitted. It is not a near-linear total-n gate theorem, a variance-only all-rate bound, or a gate bound for opaque query oracles with unspecified implementation. Consumer instruments are external or their true implementation costs are added.

Below either admission condition the frozen finite-action Taylor/complete-first-event construction remains valid. Using the fallback a_E bound makes that regime polynomial in the original acquired parameters, but not automatically near-linear in Z. The source states this limitation correctly.

The received process guarantee retains arbitrary source/system/reference inputs, prescribed joint instruments and the actual final source; private compiler records remain private. The refinement does not expand classical-source equivalence beyond its separate adjoint-algebra and dephased-output interface.

No load-bearing correction is required. This mathematical whole PASS does not recompute the baseline billions-of-slots ledger, establish an executable gate backend, demonstrate practical advantage, claim novelty or rule out stronger model-specific ordinary methods. Those questions remain separate from the valid receiving construction.
