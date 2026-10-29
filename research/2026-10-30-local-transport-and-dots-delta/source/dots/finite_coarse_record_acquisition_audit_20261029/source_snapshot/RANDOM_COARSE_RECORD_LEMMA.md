# Random coarse records: a proved disturbance lemma, not yet a decoder
2026-10-29. Author derivation pending independent review. This is additive to the normalized-defect note.

Let B=B* preserve a known-in-analysis response support P of dimension d, and let X=X*=PXP. For width w>0 and offset u uniform on [0,w), partition the real spectral axis into intervals [u+jw,u+(j+1)w), and let E_u be the corresponding nonselective spectral pinching of B. No spectral gap is assumed.

## Exact bound
In a B eigenbasis, a matrix entry X_ij is erased exactly when the two eigenvalues lie in different bins. Their separation probability over u is min(1,|b_i-b_j|/w). Therefore
 E_u ||X-E_u(X)||_F^2
 = sum_ij |X_ij|^2 min(1,|b_i-b_j|/w)
 <= ||[B,X]||_F ||X||_F / w.
The last step is ordinary Cauchy-Schwarz on the ordered entries. Since all matrices remain supported on P, trace/Frobenius comparison and Jensen give
 E_u ||X-E_u(X)||_1 <= sqrt(d ||[B,X]||_F ||X||_F / w).
The bound is valid with degeneracies and arbitrary background outside P. It is a rank-paid statement; it is not replication-invariant at fixed absolute bin width.

For a discrete uniform offset grid with L equally spaced points, the probability of separation is at most min(1,|b_i-b_j|/w+1/L). The rigorous finite-randomness version adds ||X||_F^2/L inside the squared Frobenius bound, giving
 E ||X-E_u(X)||_1 <= sqrt(d[||[B,X]||_F ||X||_F/w+||X||_F^2/L]).
The grid only uses ceil(log2 L) fair bits when L is a power of two.

## Several noncommuting record operators
For B_1,...,B_q all preserving P, use independent offsets and successively measure their bins, retaining the classical records. Their pinching maps need NOT commute. The telescoping identity and trace-norm contractivity imply
 E ||X-E_q ... E_1(X)||_1 <= sum_j E||X-E_j(X)||_1.
Here every right-hand term uses the ORIGINAL X, not a fictitious assumption that later measurements see an unchanged operator. This is why no joint diagonalization is silently supplied.

For a qubit-input channel N, taking X=Delta_a and B_j among its six Gram operators yields a lower bound on the optimal fidelity available AFTER the record extraction:
 Fopt(record-instrument composed N)
 >= Fopt(N) - (1/8) sum_(a,j) sqrt(d[||[B_j,Delta_a]||_F ||Delta_a||_F/w_j+||Delta_a||_F^2/L_j]).
Proof: a decoder can ignore all records and apply the original optimal decoder to the unrecorded output. The Pauli response formula and ||R*(sigma_a)||op<=1 bound its fidelity change by one eighth the summed trace response disturbance. No claim that this decoder is known or executable is used.

## Unclosed operation
This lemma prices the disturbance of acquiring coarse records. It does NOT prove that these records supply consistent approximate Clifford axes, that the post-record blocks are two-dimensional, or that a decoder can attain the retained optimum without the original unknown optimal recovery. Those remain the hard bridge. Likewise the exact spectral pinching here is a mathematical instrument, not an unpriced native primitive. A finite controlled-program QPE with random boundary guard bands must be analyzed before assigning a physical source-call cost. The existing exact-central QPE theorem cannot simply be reused to claim these approximate records are scalar.
