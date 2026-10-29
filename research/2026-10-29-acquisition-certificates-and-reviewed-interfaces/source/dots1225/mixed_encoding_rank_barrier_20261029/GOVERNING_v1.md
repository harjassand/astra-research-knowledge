# A tight hidden-key coverage barrier for universal mixed-encoding recovery
2026-10-29. Author theorem; independent receiving review requested. The mechanism is elementary coupon coverage and quantum one-time-pad decoupling, not a claim to invent either tool.

## A physically reversible family
Fix logical dimension k>=2 and junk probabilities p_1,...,p_r>0. Let W_a, a=1,...,k², be a known orthogonal Weyl-unitary basis. Each flag i has an independent unknown key a_i. Define
 N_a(rho)=sum_i p_i |i><i| tensor W_(a_i) rho W_(a_i)†.
This is exactly the mixed encoding V(rho tensor sigma)V† with sigma=diag(p), D=kr and V(|psi> tensor |i>)=|i> tensor W_(a_i)|psi>. V is unitary after reordering factors. A decoder knowing the keys simply reads i and applies W_(a_i)†. Thus no logical information is intrinsically lost. The flag basis, probabilities and Weyl basis may all be given to the learner; only the keys are unknown. A lower bound in this easier subclass applies to arbitrary unknown mixed encodings.

## Query model and missing mass
A decoder receives one later encoded payload and at most n ordinary forward CPTP calls of N_a. Queries may be entangled, adaptive, before or after receipt of the payload, and coupled to all retained quantum workspace. No inverse, coherent access to the channel's random-flag environment, or ability to select the output flag is supplied. The payload's original reference is inaccessible. Known protected memory/control are allowed.

Every channel call draws its flag independently according to p, regardless of its input and of previous operations. The payload flag J has the same law and is independent of training flags. Pad any early-stopping protocol to n unused calls for the lower-bound argument. The event that no training call has flag J has probability
 u_n=sum_i p_i(1-p_i)^n.
This remains true with adaptivity or post-payload queries because the flag distribution is input-independent.

## Information-theoretic lower bound
Use a maximally entangled logical payload/reference and place the uniform independent prior on the unknown keys. On the no-hit event, no training output depends on key a_J. Averaging that key applies the complete Weyl twirl to the payload half, making the reference maximally mixed and independent of EVERYTHING available to the decoder. All subsequent no-hit query branches act only on that other system. They cannot restore reference entanglement. This argument conditions on the complete classical flag history (which can be copied without disturbing this block-diagonal channel), and therefore also covers quantum-adaptive strategies that do not explicitly read flags.

Any deterministic decoder consequently has averaged entanglement fidelity at most
 F_e <= (1-u_n)+u_n/k² =1-(1-1/k²)u_n.
Hence some fixed key tuple has at least this entanglement infidelity, and its half-diamond decoding error is at least (1-1/k²)u_n. This is a minimax lower bound, not a statement about an estimator with weaker resources.

For a universal EXACT heralded decoder, each successful Choi output for each fixed key tuple must be a nonnegative multiple of the pure maximally entangled projector. After averaging keys, the no-hit success contribution is separable from the reference. A positive separable operator cannot be a nonzero contribution to a rank-one entangled projector. Thus no-hit success has zero weight and the uniformly guaranteed exact-herald probability is at most1-u_n.

## Matching physical strategy
Train with n Bell/Choi inputs. For each output, read its public flag and measure the corresponding reference/output pair in the known Weyl-Bell basis. This identifies that flag's key EXACTLY from a single hit. Store observed keys classically. On the encoded payload, correct if its flag was seen. If unseen, choose a uniformly random Weyl inverse; the resulting averaged channel is completely depolarizing. For every fixed key tuple the total decoded channel is exactly
 (1-u_n) identity +u_n depolarizing_k.
Its entanglement fidelity and half-diamond error saturate the preceding bounds. Alternatively, report failure on unseen flags and obtain exact heralded success1-u_n. No pre-shared entanglement with the unknown payload is used; training Bell pairs are ordinary probes prepared before encoding.

For uniform p, u_n=(1-1/r)^n. To obtain deterministic half-diamond error at most epsilon<1-1/k², one necessarily needs
 n >= log[(1-1/k²)/epsilon]/[-log(1-1/r)]
for r>1, and this family admits the matching strategy above. Thus rank-independent query complexity is impossible: the requirement is asymptotically r log(1/epsilon). Exact-herald success>=1-delta similarly requires n>=log(1/delta)/[-log(1-1/r)]. The r=1 case is separately trivial: one flagged Bell query identifies its Weyl key exactly.

## Scientific scope
This does not rule out output-D-independent recovery for fixed junk rank r, nor the separate exterior decoder with2r-1 queries and tiny success. It identifies a necessary rank/spectral-coverage cost even when junk labels are publicly exposed. For general p the missing mass u_n is a more informative obstruction than rank alone. It is not a complete characterization for arbitrary unknown V, where the junk flags themselves are hidden and further costs may arise. The matching strategy is classical-key learning, so this family does not establish a quantum advantage; its role is to prevent an impossible rank-free promise.
