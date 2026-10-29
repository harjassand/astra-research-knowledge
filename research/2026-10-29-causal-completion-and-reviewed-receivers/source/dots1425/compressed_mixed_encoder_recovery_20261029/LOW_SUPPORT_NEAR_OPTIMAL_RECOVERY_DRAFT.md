# Forward-query physical near-optimal recovery for arbitrary low-support channels

2026-10-29. Root extension prompted by the mixed-encoder construction; independent review pending. This removes the perfect-correctability premise, not the low-support/memoryless/trusted-control premises.

## Factorization without an accessible purification
Let N:L(C^k)->L(C^D) be any memoryless CPTP map and suppose rank N(I_k/k)<=d, with d<=D a supplied upper bound. Let V:C^d->C^D be any isometry extending the support of N(I/k). Every output of N lies in this support: for positive rho, rho<=k(I/k) implies N(rho)<=kN(I/k), and linearity extends the support statement to every operator. Thus F(X)=V†N(X)V is a CPTP channel k->d and N=V F. Neither V nor F is supplied to the controller.

If N has Kraus rank s, then the output support is contained in the span of the s Kraus images, so d<=ks suffices (or d=D when smaller). This is an upper-bound promise, not a learned Kraus decomposition. The channel may lose logical information irreversibly. No exact error-correcting code or perfectly recoverable subsystem is assumed.

## Reuse of the physical construction
Jointly compress N training Choi outputs and the later payload using the established reference-safe compression channel. The resulting state is the single-common-U ensemble of training and payload from A_U=U F, U Haar in U(d). This is again a channel identity with all logical references retained, so conditional on U the training experiments are IID and independent of the unknown payload. Apply the same finite tomography, rational TP/positive repair and actual synthesized Petz map from the received base theorem.

Write
 F_opt(N)=sup_R F_e(I_k/k,R N),
where R ranges over all CPTP physical decoders D->k. This optimum is unchanged by replacing N with F or U F: a decoder can be restricted through V, and a small-space decoder can be extended to all of D by a support measurement plus fixed output on its orthogonal complement. This is an existence comparison, not access to the unknown support projection.

On the good tomography event let halfdiamond(Ahat,A_U)<=delta. The unknown optimal recovery for A_U has fidelity on Ahat at least max(0,F_opt-delta). Barnum--Knill gives the learned physical Petz map fidelity on Ahat at least max(0,F_opt-delta)^2. Returning to the actual A_U loses at mostdelta. For0<=delta<=1,
 F_e(R_Ahat A_U)>=F_opt(N)^2-3delta.
Ifdelta>F_opt the right side is nonpositive and the bound is trivial; otherwise expand the square and useF_opt<=1. Averaging estimation failures and including the actual joint implementation error gives
 F_e(implemented N)>=F_opt(N)^2-3delta-beta-gamma.
Equivalently, the achieved entanglement infidelity is at most twice the optimal infidelity plus3delta+beta+gamma.

This is a PHYSICAL near-optimal recovery guarantee in entanglement fidelity, not merely a virtual estimate, a diamond-near-optimality claim, or a guarantee that an irreversibly damaged channel can be corrected to identity. IfF_opt is close to1, the standard normalized-Choi bound gives an identity-error consequence; otherwise no such claim follows. Source-independent fallback remains CPTP on every statistical record.

## Resources and significance at actual scope
The base theorem's finite source-query budget depends polynomially on k,d,1/delta and log1/beta, not on D or unknown nonzero spectral gaps. It uses coherent retention and joint processing of all training outputs with the later payload. The established finite compiler is polynomial in batch size and logD for FIXED d, with an explicit d-dependent exponent; a jointly polynomial-in-d design upgrade remains separate until received.

The construction does not require a source/Stinespring inverse, controlled unknown source, an environment purification, or a classical reconstruction of the original D-dimensional channel. It DOES reconstruct a small randomized compressed channel and compile its known Petz matrices. A new payload normally needs a fresh training/compression batch; the separate multi-payload note applies only to one common joint batch.

Small Kraus rank does not imply local/easy hardware noise, and protected quantum training storage can dominate costs. The result does not establish historical novelty, universal quantum advantage, capacity, fault-tolerant controls or practical superiority. Its potential opening is an intrinsic-output-support rather than ambient-output-dimension physical recovery compiler. Existing pure-isometry inversion and generic Petz recovery are serious predecessors; their actual access models must remain attached when comparing them.
