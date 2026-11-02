# Actual gate outcome: no consequential communication witness

**Decision:** do not promote finite-flag symmetric coding as an earned replacement scientific programme. The indispensable positive-coherent-information step was implemented and attempted, but no witness at v=0.38 or 0.4 was acquired. There is now a sharp all-length obstruction for its standard repetition fallback, while a separate certificate prevents incorrectly extending that obstruction to every code.

## What was implemented, rather than assumed

`schur_channel.py` evaluates the full logical-plus-reference channel, with every finite-flag histogram and every product-Schur multiplicity retained. It accepts arbitrary real or complex rank-two symmetric-subspace purifications and supplies analytic amplitude gradients. It uses the exact root-of-unity symmetric-power reduction from the earlier note; no branch is postselected and no flag is available to the sender.

Independent checks:

* Direct full tensor/reference channel entropy for n=1..4 and flags B=2 or4 agrees within 1e-15. One check explicitly constructs the entire flag-block-diagonal output and reference-output matrices before evaluating entropies, not merely a conditional-entropy formula.
* Real and imaginary gradient components agree with independent finite differences to better than 6e-10.
* The actual publicly supplied complex Dicke seeds from Agarwal et al. at n=3,6,9,12 reproduce their independent-XZ positive coherent-information control points (about 1e-5). This shows that the implementation can detect the known non-repetition degeneracy mechanism.
* At n12 and tiny repetition rates, root-of-unity coefficient cancellation is visible: Schur gives about -8.3e-12 where the stable exact repetition expression gives -2.76e-12. Values on this scale are not evidence of a sign. Any putative positive witness would require independent high-precision/certified evaluation; none arose.

## Stronger baseline correction

The earlier target “anything above v=1/e” was too weak. For a rectangular GKP qubit with aspect r, the already-published analog formula gives

    Ic = 1-H(v/r)-H(v*r).

At v=1/e+1e-5,r=3, independent 60-digit integration gives Ic=0.0001110361211613039568580. The rectangular reduction is already explicit in Subramanian–Zheng–Jiang, PRX Quantum6,040342 (2025), AppendixD2, EqD56 in the published paper. Whether the tiny positive window was previously emphasized is not relevant to the construction comparator. There is no historical novelty claim here. Simple finite bins can preserve this tiny margin (e.g. 32 optimized bins per quadrature, 1024 joint flags, about7.5e-5); such a decimal-scale result is not the selected consequential goal.

At v=.38 and r=3 the unquantized one-use maximally mixed rectangular benchmark is already negative, about-.0103041. Three optimized total flags add approximately .0114 entropy loss. The actual certified64×64 lookup with three output flags has Ic1=-.02169287080148. A fresh six-start complex n6 search on this exact lookup channel (not the earlier quadrature surrogate) also remained negative; the best retained normalized endpoint was -2.63250831456412e-07 bits. The n-mode comparisons use the identical lattice, flag channel and logical-subsystem encoder: the common finite-energy syndrome packet can be shared between conventional and symmetric encodings, so no logical-state-dependent input-energy advantage is assumed. This does not assert that a generic common-packet encoder or modular receiver is efficient, nor that this is a globally optimal finite-energy bosonic comparator.

## Searches and charged resources

The high-noise searches optimize complex rank-two symmetric purifications, with normalization and a lower reference-eigenvalue target .05 to prevent interpreting collapse to a pure input as a communication improvement. Raw unconverged endpoints are preserved; normalized coherent information is separately reported. Many searches end near repetition or the reference-purity constraint. No global optimization or general no-go conclusion follows from them.

Diagnostic high-noise completed searches include n6 at (v,r,B)=(.38,1,3),(.38,2,3),(.38,3,2),(.38,3,3),(.4,3,3), with 4--6 starts including published primary seeds and random complex states, plus n9 at(.38,3,3). All retained endpoints are negative. n12 primary-seed baselines at(.38,3,3) are -.0438342 (original) and -.0511239 (Hadamard transformed). The largest full n12,B3 engine stored1.828GB of transfer tensors,1218 Schur blocks,maximal output block dimension125, and took about11--12 seconds per full value/gradient evaluation on this workspace. This is not an efficiently scalable promise to n30 or fine analog alphabets.

Earlier near-hashing real-family runs are also preserved: n6/B4, n8/B4, n4/B16, and a biased n6/B4 run. The n8 and n4 runs were intentionally interrupted after four completed starts once the stronger rectangular comparator invalidated their scientific target; no completion is implied for those interrupted runs.

## Exact obstruction and exact limitation of that obstruction

For equal-mixture repetition in any fixed Clifford axis, let b=H(bit error|flag) and rho=E[conditional phase bias squared]. Every block length satisfies

    Ic(n) <= rho^n-b^n.

The phase-information bound follows from the positive series for1-h2((1+t)/2). The BMS repetition entropy obeys H_n>=b^n by the elementary polar entropy identity and the same positive-series/Chebyshev inequality. Thus rho<b excludes every length, not just those enumerated.

The actual64×64 lookup partition atv=.38,r3,B3 has certified lower bounds on b-rho of .00492438,.00526134,.00773758 for the X,Y,Z axes. v=.4 also passes. The Gaussian probabilities are independently enclosed by interval arithmetic with a composite-Simpson remainder and bounded omitted image tails, not just trusted because a high-precision CDF agreed. See `../FINAL_REPETITION_CERTIFICATE.md`, `../REPETITION_ALL_N_OBSTRUCTION.md`, and `certified_repetition_quantizers.json`.

Conversely, `NON_ANTIDEGRADABILITY_CERTIFICATE.md` proves this same explicit v=.38 channel is NOT antidegradable, using an exact rational self-compatibility dual and the same probability intervals. The all-length result therefore excludes the conventional repetition mechanism, not the entire channel or the entire symmetric-state family. A genuinely non-repetition degeneracy improvement remains necessary and was not found.

## Resource correction, not a capability claim

`SECOND_ORDER_PACKET_BOUND.md` improves the finite-energy comparison: for a centered common syndrome packet h, the first Taylor term vanishes and half-diamond error is at most φ_standard(1) E|s|²/v. For the cosine packet this is O(1/N) at fixed mode count/shape, improving the earlier conservative O(N^(-1/2)) estimate. This does not construct an efficient encoder, remove finite receiver costs, or turn a missing ideal positive witness into a communication capability.

## Stopping decision

The implemented mechanism survived mathematical cross-checks but did not earn its indispensable positive witness. Its simple fallback is now rigorously blocked for the chosen high-noise finite flags. Enlarging the alphabet/block length without a new degeneracy seed would spend rapidly increasing resources on an unestablished prospect. Preserve this as a tested negative result and a corrected comparator, not a breakthrough or an already viable route toward the antidegradability boundary v=.5.
