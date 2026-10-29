# Heralded unknown-frame gate programs from correlated commutator records

2026-10-29. New author construction; independent receiving review requested. This is an exact conditional capability with potentially zero or extremely small success probability, not a practical recovery architecture or gap-free yield theorem.

## Starting instrument and explicit promise
Use the accepted one-call instrument in `coherent_commutator_acquisition_20261029/GOVERNING.md`: the unnormalized minus label record is H(sigma)^T/18 on nine labels, with full retained source memory and no controlled unknown channel/inverse. Assume one fixed unknown physical relative frame R in SO(3), c=vec(R)/sqrt(3), such that the corresponding twisted swap commutes with EVERY full-joint source Kraus operator throughout these acquisition calls. Protected label registers, flags and trusted controls remain outside source access.

The full-joint condition implies every minus record is supported on c-perp, including in its joint state with all earlier records, source memory and references. This follows directly from the zero linear combination of commutator Kraus amplitudes; it is stronger than merely estimating a scalar kernel on one occupied memory marginal. Later operations on memory cannot alter an isolated earlier label's support. Records need NOT be iid, and their bath correlations are NOT discarded in the argument.

## 1. Exterior-power kernel extraction
Let d=9 and r=8. Define a known linear map A_w:(C^9)^tensor8 -> C^9 by
 (A_w)_(a,i1...i8)=epsilon_(a,i1...i8)/sqrt(8!).
Its rows are orthonormal, A_w A_w^dagger=I9; A_w^dagger A_w is the orthogonal projector onto the totally antisymmetric subspace. Thus it is a valid heralded Kraus operator.

For ANY joint positive input omega supported on (c-perp)^tensor8 tensor B,
 (A_w tensor I_B) omega (A_w^dagger tensor I_B)
   = |conj(c)><conj(c)| tensor tau_B
for some positive subnormalized tau_B. Reason: wedge^8(c-perp) has dimension one, and the Levi-Civita/Hodge map sends its unit ray to conj(c). Equivalently A_w P^tensor8 A_w^dagger=adj(P)^T=|conj(c)><conj(c)| for P=I−cc^dagger. A positive operator supported on a one-dimensional program factor must factorize, so success DEC0UPLES the pure program from all retained memory and references. Here c is real up to irrelevant global phase, hence the program is precisely |vec(R)>/sqrt(3).

This is a kernel PREPARATION mechanism, not the incorrect assertion that the original range record itself lies in the kernel. If the joint occupied label support has dimension<8, this event has probability zero. An additional common dark direction also forces zero success. Identity and permanently one-axis sources can therefore defeat it completely despite having useful codes. There is no occupation/yield guarantee hidden in the postselection.

## 2. Concrete known-control realization of the exterior map
The antisymmetric projection can be realized by a finite linear-combination-of-permutations circuit, without calling the source again. Prepare independent uniform selector registers of radices8,7,...,2 (17 qubits suffice in binary encodings). A Fisher-Yates network maps these8! equally weighted selector strings bijectively to permutations of the eight label registers. Apply the sign of each permutation as a known selector phase and coherently perform that permutation. Unprepare the selectors and postselect their initial state. The resulting successful operator is (1/8!)sum_pi sign(pi) U_pi=P_antisym, exactly a projector, not a further uncharged amplification oracle.

There are28 addressed register transpositions across the seven Fisher-Yates stages; for four-qubit encodings of the nine labels this is112 selector-controlled bit swaps, with at most three selector bits in each address, plus state preparation/unpreparation and sign gates. All are known controls; no unknown source unitary or bath operation occurs. Uniform finite-radix preparation requires paid known rotations. A physical exact Clifford+T implementation is NOT assumed.

After projection, coherently compute the missing label (XOR of labels0..8 is8), then reversibly Fisher-Yates-sort the eight distinct labels while recording the selector choices. For each stage find the position of the largest remaining canonical label; swap it to the final position and store the index. Erase the now-canonical complement list using the known missing label. The remaining selector state is the known signed uniform product state, independent of the missing label; undo its sign and preparation. Correct the known phase(−1)^a on missing label a. This leaves the Hodge-dual program and clean work registers. Exact classical tests enumerate120960 permutations for missing labels0,4,8, checking reconstruction and parity. Linearity gives the coherent decoder; no dense9^8 circuit simulation is claimed. Comparators, reversible search, routing, protected storage, reset/readout and all gate errors remain paid operations.

## 3. Two rotation programs produce two quaternion programs
Write q=(w,x,y,z), ||q||=1, with V(q)=wI−i(xX+yY+zZ), and let R(q) be its adjoint SO(3) rotation. The usual linear quaternion projector identity is
 qq^T=[I4+B(R)]/4,
where B has diagonal(traceR, R00−R11−R22, −R00+R11−R22, −R00−R11+R22), and off-diagonal entries R21−R12, R02−R20, R10−R01, R01+R10, R02+R20, R12+R21 in positions01,02,03,12,13,23.

A single unknown program cannot simply be given a coherent constant reference amplitude. Instead exploit the SO(3) identities cof(R)=R and sum_ab R_ab^2=3. Define the homogeneous QUADRATIC map
 Q2(R)=[(sum_ab R_ab^2)/3 * I4+B(cof(R))]/4.
There is an explicit rational16×81 linear operator A such that A(vecR tensor vecR)=vec Q2(R). The complete matrix is in `transducer_matrix.json`.

The exact symbolic check proves, for arbitrary real quaternion coordinates,
 A vec(R(q))^tensor2=(q.q) vec(qq^T).
The exact rational LDL factorization of I16−AA^T has strictly positive diagonal, proving ||A||<1 and therefore that A is a valid successful Kraus operator. Its unused complement can be realized by a known finite-dimensional Stinespring dilation; it is not an unknown-channel oracle. The fixed rational matrix defines all coefficients, and a spectral square root of the known PSD complement gives an algebraic dilation. Gate compilation/finite precision is a separate paid trusted-control obligation, not a claim of a native experiment.

On TWO independently stored successful programs |vecR>/sqrt(3), A outputs (1/3)|q> tensor |q>. Thus the success probability is exactly1/9 and the two normalized output programs are pure and decoupled from the source. The earlier coarse Frobenius proposal used a larger normalization and is not needed after the exact LDL check. Both signs q and−q give the same output, so the SU(2) double-cover gauge causes no physical ambiguity.

## 4. Actual one-use unknown unitary operation
A known basis unitary maps |q> to the normalized Choi vector of V(q), using orthonormal Bell basis vectors |I>>/sqrt(2), −i|X>>/sqrt(2), −i|Y>>/sqrt(2), −i|Z>>/sqrt(2). Standard gate teleportation postselecting the identity Bell outcome then implements the all-input subchannel rho -> V rho V^dagger/4. Changing signs of the three vector components before this conversion instead programs V^dagger. This uses no classical reconstruction of R or the environment.

Consequently, conditional on TWO extracted rotation programs, the transducer plus one gate attempt has success1/36. Its two quaternion outputs may instead be used for one V and one V^dagger attempt; both heralded gate outcomes succeed with probability1/16 conditional on transduction, hence1/144 overall. Arbitrary input/reference entanglement is preserved on the accepted branch. Other Bell outcomes are FAILURES, not freely correctable unknown-frame gates. An unknown payload may be damaged on failure; any recovery/outer-erasure architecture must explicitly account for that. No deterministic reusable programmable gate is claimed.

## 5. Success, cost and exactness limitations
A fixed attempt uses sixteen ordinary coherent-acquisition source calls in two eight-call batches, paid minus flags, two exterior projections/decoders, the two-program transducer and a gate attempt. Each batch's probability may vanish. With adaptive batching/retries, source memory changes and cannot be reset or assumed iid. The exact conditional correctness remains valid under the full-joint promise, but waiting time need not be finite. Use a finite acquisition cap and report failure honestly.

For an IID normalized label state sigma of rank8, the exterior success probability is the product of its eight nonzero eigenvalues, at most8^(−8). This iid formula is an EXAMPLE, not an assumption about general source records. For unnormalized iid H^T/18 records the all-eight-minus plus exterior probability is product_nonzero(H)/18^8.

An exact memoryless example mixes the collective rotations exp(−i pi X/4)^tensor2 and exp(−i pi Y/4)^tensor2 equally. The Gram spectrum is{0, 1/2 (three times),1 (twice),3/2 (three times)}. Its minus probability is4/9, and eight-call joint kernel-program probability is1/26121388032 (~3.83e−11). Arbitrary unknown local twisting preserves this spectrum while changing the prepared program. This proves nonzero acquisition is attainable, but the unoptimized numbers are extremely impractical. No beneficial yield relative to conventional adaptive tomography/control is established.

Approximate symmetry, label decoherence, gate error or false heralding can contaminate the extracted program, and conditioning can magnify errors by inverse success probability. No robust/noisy version or gap-free practical rate is proved. The result closes an exact conditional quantum-program bridge only; it does not replace the accepted gap-free classical acquisition and guarded recovery schemes.

## Evidence and provenance
`check_exact_transducer.py` verifies all16 symbolic polynomial identities and exact rational PSD certificate; `check_program_transducer.py` checks100 numerical quaternion instances; `check_correlated_wedge.py` tests the general proof in dimensions3,4,5 including entangled bath, complex conjugation and rank-deficient failure; `check_permutation_decoder.py` checks the explicit reversible permutation mechanism; `check_collective_example.py` computes the exact physical Gram spectrum and success fraction. These are derivations and reproducible simulations, not acquired laboratory observations. Historical novelty of exterior-algebra state processing, probabilistic unitary programming or their composition here has not been established; equally informed conventional quantum processing may use the same method.
