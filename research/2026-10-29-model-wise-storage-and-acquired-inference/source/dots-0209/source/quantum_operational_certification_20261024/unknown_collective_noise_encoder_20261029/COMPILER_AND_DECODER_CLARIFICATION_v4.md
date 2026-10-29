# Physical compiler and diagnostic decoder clarification
2026-10-29. Responds to independent review. Supplements v1/v2; originals unchanged.

## CPTP decoder and simulation label
The programs calculate EH† times the physical output, then the Bell overlap in the returned code block. There are two honest interpretations:
1. Decode code-block outcomes to logical L and send all orthogonal outcomes to an orthogonal erasure flag |err>. This is a CPTP decoder with output L direct-sum span{|err>}. The displayed fidelity is EXACT entanglement fidelity against the ideal embedded logical Bell state. The channel diamond comparison uses the same enlarged output and ideal embedding.
2. Reset all orthogonal outcomes to any fixed logical state on L. The displayed value is a LOWER BOUND on the actual completed CPTP decoder entanglement fidelity, not in general its exact value. The additional leakage-replacement contribution is nonnegative.
The phrase 'entanglement fidelity with leakage' in data is therefore governed by interpretation 1, and must not be called the exact fidelity of an arbitrary fixed logical replacement decoder. The deterministic acquisition and storage bounds hold with either completion. No heralded conditioning or acceptance division is performed.

## Arbitrary logical input into valid Schur labels
Efficient Schur transform alone is not the whole encoder. For n=2r, the spin-zero multiplicity basis can be indexed by nonnegative walks h_0=0,h_n=0 with h_{t+1}=h_t±1. These are Dyck paths; h_t=2j_t is the angular-momentum coupling label after t spins. There are C_r paths. Let k=floor(log2 C_r); reserve the first 2^k lexicographically ordered paths.

Precompute integer counts F(m,h) of length-m nonnegative continuations from height h ending at zero:
F(0,h)=1 if h=0 else 0;
F(m,h)=F(m−1,h+1)+1_{h>0}F(m−1,h−1),
with impossible heights/parities assigned zero. There are O(n²) entries of ≤n bits, computed by O(n²) n-bit additions. This classical table is part of the calibrated compiler, independent of noise or logical input.

Unranking: start x∈[0,2^k), h=0. At each position, let D=1_{h>0}F(m−1,h−1) for the down-first lexicographic branch. If x<D, output down and set h←h−1. Otherwise output up, set x←x−D and h←h+1. For the valid rank range, this ends at x=0,h=0 and produces exactly its rank's Dyck path. Ranking reverses this by summing D at every selected up branch. Both algorithms use polynomial-size exact comparisons, additions, and classical-table access.

Reversibilize unranking to coherently write |x>|path(x)> with workspace, uncompute workspace, then use reversible ranking(path) to XOR away the input rank. This maps an arbitrary k-qubit superposition to its chosen valid path-label superposition with all unused registers reset. A deliberately loose implementation using equality-controlled table lookup, schoolbook arithmetic, and stored histories has O(n^4) elementary reversible gates and O(n^3) ancillary bits; tighter synthesis is not needed for the polynomial existence statement. No QRAM oracle or data-dependent postselection is assumed. Exact integer gates can be implemented in a fixed universal reversible basis, then fault-tolerantly synthesized as needed.

The chosen path labels together with fixed final j=0,m=0 labels initialize the conventional sequential Clebsch–Gordan Schur register. Apply the inverse qubit Schur transform, then the learned local SU(2) rotations. The decoder reverses these operations and checks whether the path belongs to the reserved rank interval; leakage is completed as above. Schur compilation approximation and all control errors are separately charged in diamond distance. Required clean registers and physical routing/connectivity are actual costs; local two-qubit compilation on a line adds at most polynomial SWAP overhead. Arbitrarily faulty preparation or gates are not protected by the passive storage theorem.

The dense J² eigenspace construction in the n=4 program is only a small-instance diagnostic, not the claimed scalable encoder implementation. The reversible rank/unrank procedure supplies the missing scalable logical-input injection interface.
