# Independent receipt: rare spectral-subspace programmed filter

27 October 2026. PASS for rare_spectral_subspace_programmed_filter_theorem.md. The fixed unknown density pair, supplied positive gap and supplied target-weight bound are promises, not verified by the protocol. The instrument is freshly programmed with consumed independent copies; “reusable principle” does not mean a reusable learned quantum device.

## Arbitrary-rank population calculation

The earlier signed-pair proof extends to any orthogonal projector P. Indeed sigma P sigma<=Tr(Psigma)sigma follows by bounding the positive operator sigma^(1/2) P sigma^(1/2) by its trace, so <=WI. Similarly rho P rho<=WI. The cross product square gives ±(sigma rho P+P rho sigma)<=P+sigma rho P rho sigma<=P+WI; the remaining double-commutator terms cost2WI. The scalar trace difference is bounded by2sqrt(Tr P sigma² Tr P rho²)<=2W. None of these requires rank one. Cancellation uses only [P,H]=0. The signed-pair800 bound is therefore unchanged for arbitrary rank, negative times, coherent inputs and arbitrary ancillary/reference correlations.

## Coherent compute/classify/uncompute

The phase map sends [-6,4] into[0,5/8], and the positive/nonpositive threshold margin is g0/32 with the stated circular acceptance window. For a fixed eigenvalue, let A be the ideal QPE work-state unitary and Pi its reversible majority acceptance projector. Copying classification to a flag and then applying A inverse to the WORK registers (not uncomputing the copied flag) produces an isometry within sqrt(2 eta)<=2sqrt(eta) of a clean ideal membership flag. The incorrect component's probability is unchanged by that inverse, since it is a unitary independent of the copied flag. Data eigenvectors remain orthogonal and unchanged by all exact spectral evolutions, so the isometry norm bound is uniform over coherent superpositions of distinct eigenvalues, including within a higher-rank positive subspace.

Measuring the flag and discarding work thus has complete diamond error <=4sqrt(eta) against the full binary Lueders instrument. This specifically repairs the dephasing problem that would occur if phase labels were left measured or retained without uncomputation. L repetitions telescope to <=4Lsqrt(eta)=.04xi; the final accept-all and erased-reject postprocessing is CPTP. The ideal acceptance effect before and after uncomputation is the same function of H and is <=P+eta I.

## Simulation, recurrence, and budgets

Forward times are pi2^a/8; summing forward AND reverse over all Lr classifiers gives S=Lr pi(M-1)/4. Negative-time reverse gates are simulated with fresh ordinary mixed samples and negative angles, not by physically inverting noisy previous collisions. Per-gate absolute-time allocation gives the same total generic simulation bound xi/256 and per-classifier xi/(256L). All work/flag operations preserve the data observable P. The shared delta² allocation gives v<=xi/(80L), so the population recurrence is exactly the previously independently received recurrence with p replaced by W, now for any0<xi<=1. Its constants remain valid at xi=1: a^L<=80/79, bL<=1/40, beta<1/16, and its feedback coefficient is below1/16.

Consequently accepted mass <=3r0+5b+beta^L<=3r0+3Wxi/16, uniformly for arbitrary positive subnormalized/coherent accepted states; there is no presumed absent import, virtual sector measurement, or hidden normalization. Total instrument error .04xi+xi/256<xi. There are2Lrm controlled evolutions including reversals, each using two samples per round, yielding131072S²/xi+4Lrm. The sample count has no raw dimension factor, while gate width/memory do. For P=0 the same construction and estimates remain valid (the positive-gap promise is vacuous); the claim is not a general relative-error guarantee on coherent P/complement superpositions.

This result is a filtering primitive only, not a source decoder or entropy theorem without additional task-specific analysis.

## Addendum: arbitrary known positive coefficients (section4)

Independently received the appended two-program H=A sigma-B rho extension. The phase interval [0,1/2], gap margin g0/(4ell), and upper boundary3/4 are valid for ell=A+B and g0<=ell (including vacuous positive-spectrum promises). Forward/reverse time sum2Lr pi(M-1)/ell and two-copy round count are correct. The coefficient residual is(2/3)(A³+B³)+ABell=(2/3)ell³-ABell<=ell³. Under ell|delta|<=1, it contributes at mostell²delta² to both P and WI; identity and double-commutator terms and2A²B|delta|³ fit the conservative8ell² bound. The simulation coefficient4(A²+B²)+2AB<=4ell² is valid. Allocated rounds ensure ell|delta|<=1 since ell S>=2pi, and the per-classifier population/simulation budgets xi/(8192L),xi/(16384L) are smaller than those already received. Both complete-instrument and rare-acceptance guarantees therefore remain valid, with131072ell²S²/xi+4Lrm samples. Simultaneously scaling A,B,g0 leaves this count invariant. No many-term extension is inferred.
