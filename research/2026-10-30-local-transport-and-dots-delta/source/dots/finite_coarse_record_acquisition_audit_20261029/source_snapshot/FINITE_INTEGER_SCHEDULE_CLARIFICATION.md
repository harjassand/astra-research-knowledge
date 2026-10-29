# Integer schedule clarification and diagnostic scope
2026-10-29. Additive to FINITE_COARSE_RECORD_ACQUISITION.md; no governing source edits.

For fully rational public collision counts, let m=log2 M and U=4sM. For each QPE power ell=0,...,m-1 in each of s repetitions and its uncomputation, use u_ell=2^(ell+1), which bounds its true absolute time pi 2^ell/2. Set
 n_ell=ceil(16 u_ell)+ceil(64 u_ell U/tau), tau=nu/4.
There are exactly2sm such evolutions and their u_ell sum is4s(M-1)<U. The actual simulation error therefore remains at mosttau and total collisions are at most16U+64U^2/tau+4sm. These are bounded integer/rational computations; no exact comparison of a pi-dependent quantity to an integer is required. Signed time is still supplied through the known rotation coefficient.

check_coherent_bins.py/json executes36 small single-QPE instrument cases, with exact FFT unitary arithmetic up to floating-point error, and compares the retained-bin channel to the ideal coarse instrument. It also records a useful failure: for two eigenvalues in the SAME bin, copying the bin and uncomputing preserves coherence0.98946, whereas measuring the full phase and forgetting all but the bin leaves only0.04735. This distinguishes the required instrument from a full eigenvalue measurement. The diagnostic does NOT execute the enormous conservative s/M schedule, native DME or a decoder.
