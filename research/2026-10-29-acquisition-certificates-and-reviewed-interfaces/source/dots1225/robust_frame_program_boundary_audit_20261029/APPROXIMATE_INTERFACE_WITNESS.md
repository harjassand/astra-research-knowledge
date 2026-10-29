# A constructive approximate interface, with its costs and limits
2026-10-29. Independent derivation; not historical novelty.

For a MEMORYLESS noisy unitary query N_U^eta=(1-eta)Ad_U+eta D, prepare a protected maximally entangled pair |Phi_d>_AB and send B through one source use before the unknown payload arrives. Store the normalized Choi resource omega=(id tensor N_U^eta)(Phi_d). Later project the unknown payload X and A onto |Phi_d>. On this one accepted Bell outcome the exact output map is

 E_accept(X)=N_U^eta(X)/d^2.

The success probability is exactly1/d^2, independent of X,U,eta, and the resource is consumed. No complete environment or classical estimate of U is required. Failure generally destroys the unknown payload; it cannot be blindly retried on that same payload. Trusted pair preparation, memory, Bell measurement and the complete channel interface are paid.

The accepted normalized channel has half-diamond error

 (1/2)||N_U^eta-Ad_U||diamond=eta(1-1/d^2).

Proof: the maximally entangled input gives the lower bound, because its output is (1-eta)P_U+eta I/d^2. For the upper bound, expand the depolarizer as the uniform average over d^2 generalized Pauli conjugations, conjugated by U. One term is exactly Ad_U and all other channels differ from it in half-diamond norm at most1. The upper and lower bounds coincide.

This is a constructive noise-continuous alternative to exact heralding, not an error-suppression architecture. If the source can be used directly when the payload arrives, direct application of N_U^eta has the same approximation error deterministically and dominates this postselected resource in success. Its distinct feature is delayed execution from a stored quantum program. A source family of arbitrary collective noise is NOT thereby converted into the target frame unitary; that acquisition obligation remains.

For an existing finite-query exact frame-acquisition protocol with a uniform ideal success lower bound p0 and an actual FULL-interface per-query deviation epsilon, hybrid continuity instead gives a conservative operational route: use a finite N cap, pay Delta=N epsilon, and retain only a quantitative approximate target with actual success at least p0-Delta. This is useful only if a genuine small interface error and nonrare ideal herald are acquired or assumed. It is not inferred from reduced marginal agreement.

Prior art actually read: Nielsen and Chuang, Programmable quantum gate arrays, quant-ph/9703032, equations11–17 and subsequent discussion explicitly give Choi-program postselected teleportation, success2^{-2m}, and extension to mixed programs/nonunitary operations. Our noisy-mixture calculation is an elementary specialization, not a new processor proposal.
