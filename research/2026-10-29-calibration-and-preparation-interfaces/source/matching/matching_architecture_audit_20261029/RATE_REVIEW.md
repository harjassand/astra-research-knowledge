# Independent partial-swap and conditional-rate review
2026-10-29. Source: matching_guard_rate_20261029/RATE_BRIDGE_DRAFT.md, hash in REVIEW_RECEIPT.json.

The exact partial-swap saturation is accepted. A uniform perfect matching pairs sites1,2 with probability1/(n-1); otherwise their joint marginal is I/4. Thus mean swap is a=(n-4)/(2(n-1)), paired states survive with certainty, and unpaired states have survival cos²t+sin²t/4. The full singlet trace of exp(itS) is cos t+i a sin t. These yield q=3(n-2)sin²t/[4(n-1)] and e=3(n²-4)sin²t/[4(n-1)²]; e/q=(n+2)/(n-1) exactly whenever sin t≠0. No subcode sharpness is inferred.

The guard substitution is correct under the already proved full-memory private-pad hypotheses: s=1/(1+C) gives hazard ratio Cs/(1-s)=1, hence b=0 accepted >t-fault bound2^(-t-1). Arbitrary-current-source soundness and zero-failure good-source yield remain separate.

Qualification required for the phrase 'With no failures': the negative-binomial role count and Binomial(L,s) cap-completion expression require the GOOD-SOURCE premise q_h=0 at every visited history, not conditioning a noisy source on an observed all-pass record. Such conditioning can bias role counts. Under that premise the uncapped expected calls are indeed (C+1)J; with a finite cap, accepted throughput additionally includes the cap success probability. Root was told this before review completion.

The rate formula R_out k/[n(C+1)] is correct uncapped good-source exposure accounting, CONDITIONAL on the supplied actual fixed-rate outer code, block/alphabet compatibility and trusted control/holding assumptions. It is not a new standalone outer-code family, total-runtime rate, hardware threshold or arbitrary-noise capacity. Choosing a cap overhead factor strictly larger than one gives exponentially small noncompletion for large J. The ordinary logical-two-design comparator already has constant exposure overhead; the new matching operation changes test controls, not that general fact.

Update 04:10 UTC: Re-read the current root note. The good-source q_h=0 premise and uncapped-versus-capped throughput qualifications are now explicit in its governing text. The corrected rate note is accepted at the conditional scope above.
