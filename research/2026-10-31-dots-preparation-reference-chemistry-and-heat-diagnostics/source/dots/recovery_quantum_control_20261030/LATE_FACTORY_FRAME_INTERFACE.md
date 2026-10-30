# Late factory frame interface: concrete failure and stronger comparator
2026-10-30. Research note, not an independently reviewed native construction.

## Result
A raw bilateral Bell buffer plus one destructive physical-Z readout does **not** automatically supply a zero-syndrome encoded |0> factory. The missing property is robust acquisition of an arbitrary absolute syndrome, not the weight of a Pauli mask. A separate published constant-depth factory already removes that ordinary circuit premise, but its explicitly instantaneous classical feedforward does not remove the autonomous late-loading interface.

## Exact signed-Bell calculation
For real CSS projector Pi_s and |Omega_s>=vec(Pi_s)/sqrt(K), Alice Z measurement a leaves Bob proportional to Pi_s|a>. Applying raw X^a leaves a state proportional to Pi_(s_X,0)|0^n>: the Z-check signs are removed because any nonzero outcome obeys H_Z a=s_Z; the X-check signs s_X survive. All logical Z operators have the known |0> eigenvalues. A Z correction z with H_X z=s_X prepares encoded |0>. Any two such corrections differ by Z stabilizers and logical Z operators and therefore give the SAME known state up to phase. Dense corrections alone are not a failure.

But if a noisy acquired sign string s_X+D is a valid syndrome and the correction solves that reported string, the residual syndrome is D. With redundant checks an invalid report must first be sanitized, and the corresponding effective discrepancy replaces D. One must prove that this residual has a low-weight representative (modulo all Z operators fixing the known |0>), with the desired joint fault norm bound. Small-data-error single-shot correction does not alone prove this arbitrary-syndrome acquisition property.

## Exact one-round obstruction (limited comparator)
Let H_X be the (n-1)-by-n path incidence matrix with row i equal to e_i+e_(i+1); H_Z is empty. This is a bounded-weight/bounded-incidence CSS code, not a good-distance Tanner code. Every syndrome is valid. For the central unit syndrome D=e_m, all Z preimages are the prefix 1_[1,m] and its complement. Modulo the logical Z=Z_all (which fixes known logical |0>), their minimum weight is min(m,n-m).

Suppose a one-round sign-based Z-Pauli correction rule, with no additional quantum syndrome acquisition, is exact in every noiseless sector (not an arbitrary fresh-state replacement channel). On actual sector s and reported s+D it must use the same operation as in the noiseless sector s+D. The residual on the actual state has syndrome D and hence weight at least min(m,n-m), despite one flipped measurement bit. This is an indistinguishability proof; the failure is not a bad choice of linear right inverse. It disproves a generic implication from CSS-LDPC plus ideal arbitrary-sign correction to robust one-shot acquisition. It does NOT disprove the desired property for the specific Tanner family; that requires an actual syndrome-filling theorem or additional spacetime redundancy.

## Stronger ordinary comparator: alternating Tanner graph factory
Bergamaschi and Liu, ITCS 2025, Theorem 1, supply |0>^k and |+>^k preparation for any [[n,k,d]] CSS LDPC code using O(nT) ancillas, a constant-depth bounded-degree CZ graph-state preparation, bulk X measurements, and classical Pauli feedforward. Under their local stochastic circuit noise assumptions, failure is at most nT*2^{-Omega(min(d,T))}. The graph contains 2T+1 code layers and alternating X/Z check layers. Their text explicitly assumes instantaneous classical computation, avoiding output noise during that step. The information-theoretic decoder can be implemented in T*exp(n) time; polynomial decoding needs an additional hypothesis (Theorem 2).

Source: https://drops.dagstuhl.de/storage/00lipics/lipics-vol325-itcs2025/html/LIPIcs.ITCS.2025.16/LIPIcs.ITCS.2025.16.html
Full version: https://arxiv.org/abs/2411.04405
This is an ordinary noisy-circuit comparator, not a theorem for retained quantum baths or autonomous controllers.

Taking n,T=Theta(log(L/epsilon)), when the chosen code family has linear distance, makes graph space O(log^2(L/epsilon)) and even exp(O(n)) classical work polynomial in L/epsilon. Consequently computational inefficiency alone need not block polynomial-overhead autonomy. It does not make the physical feedforward interval noiseless. Moreover exp(c*n) classical time need not fit an exp(b*n) native memory lifetime when c exceeds b; polynomial total overhead alone does not settle that exponent comparison. Parallel exhaustive decoding is a possible different paid resource, not an implemented reliable controller here.

## Specific failed native interface
Proposed interface: run factory, retain bulk readout, let a reliable classical source compute its correction, hold the boundary in the existing zero-sector native memory, then apply correction when available.

Failure: before feedforward the boundary lies in a generally extensive outcome-dependent Pauli frame. The existing native small-radius basin is around the fixed zero-sector code, not this random frame. Its energy/barrier and stopped-window estimates cannot be invoked on this state. In addition, corrections made during the delay change the frame, so applying the originally computed mask later is not automatically the factory instrument. Conjugating the WHOLE memory by the final Pauli mask would repair the ideal algebra, but that mask is precisely unavailable during the delay. Assuming its bits or a trusted fresh completion gate simply reinstates the missing controller interface.

Possible real repairs must prove one of: (a) storage that preserves a relative frame tied to a protected evolving classical record; (b) a native factory whose boundary remains in the memory basin throughout actual bounded-rate correction computation; (c) spacetime factory redundancy which includes the entire physical computation/wait interval and yields a common full-output error bound. No such repair is supplied here. In particular, this is a failure to meet the hypotheses of the existing native-memory theorem, not a proof that the native memory cannot globally prepare known |0>; all-state convergence with the needed output semantics is unestablished. Static rail freshness and preset source firewalls remain accepted at their existing scopes, not solutions of this seam.

## Existing source paths
- producer-workspace/BILATERAL_BELL_BUFFER.md
- producer-workspace/SIGNED_BELL_ENCODED_TELEPORTATION.md
- producer-workspace/ACTUAL_NATIVE_LOCC_CONTINUOUS_MEMORY_V1.md
- Local ABSORBING_RECEIVER_RAIL_V2.md and its review preserve the late-arrival freshness counterexample.
