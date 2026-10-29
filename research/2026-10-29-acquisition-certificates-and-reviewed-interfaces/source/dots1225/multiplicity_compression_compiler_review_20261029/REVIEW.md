# Independent receiving review: joint mixed-encoder compression and control interface

2026-10-29. Reviewer: review_finite_quantum_sampler. Status: PASS AT THE SCOPED INTERFACE BELOW, not acceptance of the separate tomography/Petz theorem.

## Received scope
The sections on joint compression and large-D control in `compressed_mixed_encoder_recovery_20261029/GOVERNING_DRAFT.md` are justified for known D>=d=kr, fixed k,r, coherent access to all n=N+1 output carriers, trusted known quantum controls, and one fixed memoryless encoder N(x)=V(x tensor sigma)V†. The procedure consumes/stores all training outputs jointly with the payload. No classical-training-only interpretation, generic memoryful source, unknown-environment oracle, uniform polynomial-in-r gate claim, hardware demonstration, or practical advantage is accepted.

## Governing primary dependencies, actually inspected
* Yoshida–Soeda–Murao, arXiv:2110.00258v4 (13 March 2023), https://arxiv.org/pdf/2110.00258v4, Lemma 4, equations 21–23, Figure 4 and Appendix H. The source supplies the CPTP compression identity, including the off-promise completion. Appendix H's prose after Eq242 says U(D); the governing lemma and domains require U(d).
* Burchardt et al., arXiv:2509.22640v1 (26 September 2025), https://arxiv.org/pdf/2509.22640, Sections 4–5, Theorem 1/Table 1 and Eq49. This corrects Krovi's nonclassical final basis-isometry step. Its corrected full transform has gate count/depth soft-O(n^4), space soft-O(n^2), with polylogarithmic local-dimension and precision factors. Its symmetric-group Fourier conventions and matched GT bases support the implementation route below.
These are explicit primary-theorem dependencies, not an independent reproduction of an entire Schur/QFT compiler. Krovi 2018 alone is not a valid receiving foundation.

## Exact reference-joint transfer
Write Schur–Weyl space as a direct sum of W_(lambda,d) tensor H_lambda, where H_lambda carries the S_n representation. Permutations intertwine with V^tensor n; its blocks are V_lambda tensor I_H. The channel measures lambda, traces W_(lambda,D), inserts I_W/dim W_(lambda,d), and applies inverse small-d Schur. Consequently its composition with V^tensor n is precisely the collective U(d) twirl. On partitions with more than d rows use a fixed d^n-dimensional density operator; the promise never reaches those branches.

This is equality of linear completely positive maps, not merely equality on identical product states. Tensoring with id_R therefore gives, for every Omega on (C^d)^tensor n tensor R,

 (C tensor id_R)[(V^tensor n tensor I_R) Omega (V†tensor n tensor I_R)]
 = integral (U^tensor n tensor I_R) Omega (U†tensor n tensor I_R) dU.

Take Omega to be the reordered tensor product of the logical training/payload state (possibly entangled with R) and sigma^tensor n. The output ensemble contains ONE common latent U across all slots. The isometry V on arbitrary chosen junk states is not queried: actual calls to N supply the stipulated unknown sigma. Zero eigenvalues cause no interface problem. The latent U is not an available seed or oracle, and separate per-slot compression does not implement this identity. Training references are untouched. Padding a rank-deficient junk space and extending V is mathematical only, permitted by D>=kr.

## Independent multiplicity-only construction
The necessary compression is weaker than full high-D Schur basis output. Let f_lambda=dim H_lambda. Prepare the uniform group register n!^(-1/2) sum_pi |pi>, apply controlled physical-carrier permutation P(pi), then the S_n Fourier transform with coefficient sqrt(f_lambda/n!) D_lambda(pi)^*_(ab). The physical-register Kraus amplitude accompanying |lambda,a,b> is

 A_(lambda,a,b) = sqrt(f_lambda)/n! sum_pi D_lambda(pi)^*_(ab) P(pi)
                 = f_lambda^(-1/2) |lambda,a><lambda,b| tensor I_W.

The second equality is matrix-coefficient orthogonality; it holds separately on each irrep and vanishes on the others. Trace out the original physical registers and row index a, and dephase/measure lambda. The surviving column-index density matrix is exactly Tr_W(Pi_lambda rho Pi_lambda), including all its correlations with an arbitrary external reference. Indeed an input |b,w><b',w'| contributes |b><b'| delta_(w,w') after summing the f_lambda equal row contributions. KEEP COLUMN b. Keeping row a instead destroys the desired quantum irrep state. Equivalent Fourier conventions require the corresponding index change.

This explicitly implements the retained component without a high-D unknown basis operation. QFT and inverse small-d Schur must use matching Young/GT H_lambda bases; an unspecified basis identification would be a real gap. The corrected primary compiler provides such compatible conventions.

## Finite controls, storage and precision
Let B=ceil(log2 D). The physical interface is n known B-qubit carriers, computationally padded when necessary. A register permutation is implemented by known swaps, preserving the valid D-level subspaces. Coherent Fisher–Yates digits prepare the uniform permutation register with n! elements using radix sizes n,n-1,...,2, followed by reversible conversion to the QFT encoding. Addressed swaps cost at most O(n^2 B polylog n) elementary gates conservatively; permutation encoding conversion costs a polynomial in n. Add the efficient S_n QFT with its explicitly paid precision/workspace. There is no D-entry matrix lookup or uncharged D-dimensional unitary oracle.

At fixed d, prepare the discarded/replacement W_(lambda,d) factor by enumerating all interlacing GT arrays with top row lambda. There are h=d(d-1)/2 lower entries, each in {0,...,n}; at most (n+1)^h arrays need checking. A two-pass count and indexed selection does not require storing the entire list. Uniform selection among valid arrays yields the maximally mixed GT factor when the selection record is discarded. A finite binary interval sampler uses O(log C) known biased rotations for C valid arrays; alternatively finite capped rejection adds a separately charged error. Do not assume exact bounded-work unbiased-bit sampling for arbitrary C. Algebraic rotation synthesis to finite precision is paid. Then apply the known inverse small-d Schur transform. The off-promise fixed maximally mixed output has an equally finite sampler.

Thus a conservative fixed-d time bound has the form
 poly(n, log D, log(1/gamma)) + (n+1)^[d(d-1)/2] poly(n,d,log(1/gamma)),
with the first term including Fourier/permutation controls and small-d Schur circuits. This establishes polynomial n and log D for FIXED d, not uniform polynomial d. The nB input qubits, retained training references, QFT work, classical counters and compressed payload storage are paid. Neither quantum storage nor gates are independent of log D.

To achieve total half-diamond implementation error gamma, allocate error across the uniform-permutation state, Fourier circuit, mixed-irrep sampler, inverse Schur and subsequent recovery synthesis. A telescoping channel bound charges the sum, without conditioning on a successful branch. If L gates are synthesized, individual channel errors at most gamma/L suffice. This costs logarithmic precision in L/gamma for standard finite universal gate synthesis; no exact finite Clifford+T assertion is made.

## Independent diagnostic and limitations
`check_s3_extraction.py` constructs all six S3 elements, explicit trivial/sign/standard irreps and the actual Fourier Kraus maps. Ten random complex isometries C^2 -> C^4 were tested on states entangled with a two-dimensional reference. The retained-column outputs agreed to 7.56e-16; the wrong-row implementation differed by as much as 0.368. The QFT unitarity residual was 6.21e-16. This is a small floating arithmetic diagnostic of the exact orthogonality argument, not proof of the general compiler's numerical stability or native execution.

The source identity, arbitrary-reference mixed-junk substitution, and finite fixed-d control interface pass. Tomography confidence events, Petz fidelity, accepted-estimate conditioning, total recovery error and source-query count are outside this receipt and are being reviewed separately. Optional Haar-twirl irrep preparation is unnecessary here and not received by this note.
