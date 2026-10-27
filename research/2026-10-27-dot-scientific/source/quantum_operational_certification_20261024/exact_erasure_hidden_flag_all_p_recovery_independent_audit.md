# Independent audit: all-p and complete noisy recovery corollaries

27 October 2026, 02:31 UTC. PASS for exact_erasure_hidden_flag_all_p_and_recovery_corollaries.md.

The all-p construction is a positive normalized isometry-plus-replacer source with reset orthogonal to its code. D=floor(1/p) and an independent coin of probability pD exactly simulate each new-channel query with at most one canonical-channel query. The new fixed erasure sector is orthogonal to the entire original received space. This works on entangled probes as a complete channel identity and respects any ordinary adaptive strategy. Its use is worst-case capped query count, not an inferred expected-query inequality. Since floor(1/p)>=1/(2p) for p<=1/2, the received inverse bound is n>=1/(160p^2) at error<=1/4.

The complete-recovery to code-inverse implication was checked independently. For the normalized qutrit Choi state, a replacement branch of accepted mass b has accepted-entangled overlap b/9 and accepted orthogonal mass8b/9. The ideal target has zero probability under that orthogonal projector. The complete UNHALVED diamond error delta therefore gives q(8b/9)<=delta/2, with nonnegative code-branch contribution. After the fixed known output-flag dephasing, ||sigma-e||_1=2b, so q||R_sigma-R_e||_diamond<=9delta/8. Subtracting this replacement branch yields code-channel error<=17delta/(8p), exactly as stated.

This subtraction remains valid for a decoder that calls the same fixed source adaptively: at each fixed source the entire decoder is still a CPTP map of its independent data input, hence a replacement input produces a replacement channel. No external reference is supplied to the decoder. Private training randomness can be averaged first. Neither learning the unknown source flag nor discarding failed trials is assumed.

For the hidden-flag hard pair, the two desired partial-erasure inverse outputs have HALF trace distance alpha. The actual output half-distance is at least s=alpha-17delta/(8p). Applying the already received adaptive Haar argument gives n>=(D^2/8)[1-1/sqrt(1+s^2)] when s>0. Constants at delta<=2p/17 for alpha1 and delta<=4alpha p/17 for general fixed alpha are correct.

The proof charges the decoder's bounded source queries. If the original noisy-data preparation itself is counted as a channel use, it is an additional call; dropping that extra one only weakens the stated lower bound on total operational cost. No free data-generation advantage is inferred.

The result is a meaningful lower bound for complete noisy recovery at a fixed positive fraction of p and small error RELATIVE to p, not merely deterministic code inversion. It does not prohibit zero-query always-erasing recovery at fixed absolute error as p tends to zero, accepted-only fidelity with uncharged failures, vanishing unspecified throughput, known-code shortcuts, or a dimension-fixed advantage. The accuracy exponent remains open.
