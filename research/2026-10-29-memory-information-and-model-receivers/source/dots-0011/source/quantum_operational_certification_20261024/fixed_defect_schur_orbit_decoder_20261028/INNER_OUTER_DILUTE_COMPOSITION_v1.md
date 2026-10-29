# Conditional inner-to-outer dilute-source composition

28 October 2026. Candidate synthesis. The inner dilute corollary is under independent review; the explicit outer GRS/CSS construction and its operational audit are being developed separately. This document does **not** receive that outer premise in advance. Conventional concatenation, Pauli twirling and Reed–Solomon decoding are not claimed as new.

## Precise conditional theorem

Fix local dimensions, c>=0, R>0, Delta>0, a scaling exponent 0<z<1, and constants 0<epsilon_0<gamma<1/4. For each total copy count n, suppose the actual input is rho_n^tensor n, with

    rho_n=(1−delta_n)|psi_n><psi_n|+delta_n tau_n,
    delta_n<=c/n^z, tau_n orthogonal to psi_n,
    H((psi_n)_B)>=R+Delta.

The state and its spectrum/eigenvectors are unknown. This is a promise on a changing family of iid sources, not an inferred temporal independence claim.

Let k=floor(n^z), B=floor(n/k), ell=floor(kR), q=2^ell, and f=ceil(gamma B). Discard fewer than k unused input copies. Run the fixed-accuracy inner universal distillation map independently on each group of k copies, with fresh independent randomness and freshly initialized/isolated working registers. Since delta_n<=c/k, the inner theorem applies uniformly for sufficiently large n. Include all failure branches by local fixed-dimensional fallback, so each block produces an ell-qubit pair with Bell overlap at least 1−epsilon_0. Average and retire private random seeds; retaining them as accessible controls would define a different interface.

Apply independent bilateral q-ary Pauli twirling to the B output pairs and retire its keys. The reduced resource is then a product of Bell-diagonal q-ary pairs. The probability of a nonidentity Bell label in each block is at most epsilon_0. Independence here follows from the product input and tensor-product maps with independent initialized apparatus. It does not follow from small one-block infidelity alone.

**Outer premise to be independently established:** a polynomial-time one-way bilateral implementation of a q-ary CSS code [[B,B−4f,2f+1]]_q for even q and B<=q, with an explicit syndrome decoder correcting every error on at most f qdits and a total fallback on uncorrectable syndromes. For sufficiently large n, B<=q and B−4f>0. Applying this outer distillation yields (B−4f)ell ebits with Bell infidelity bounded by

    Pr[Bin(B,epsilon_0)>f]
        <= exp[−B D(gamma||epsilon_0)],

where D uses natural logarithms. With unequal but independently bounded error probabilities the same Chernoff upper bound holds. A separate total outer-circuit operational discrepancy xi_n adds at most xi_n to the bound. Taking xi_n no larger than exp[−B D(gamma||epsilon_0)] gives overall error at most twice the displayed exponential.

Consequently the asymptotic rate per supplied bipartite copy is at least (1−4gamma)R, while error is exp[−Omega(n^(1−z))]. Floors/ceilings only contribute vanishing rate corrections. For each chosen target rate strictly below R, choose fixed gamma sufficiently small and then fixed epsilon_0<gamma. The corresponding inner cutoff j is fixed independently of n.

## Physical and computational bills

The inner theorem's polynomial exponent depends on fixed c,epsilon_0,Delta and local dimensions. Running B copies costs B times the single-block cost, hence remains polynomial in n for fixed z. Its enormous normalization and classical-table factors are not erased by concatenation. A constant-accuracy inner compiled channel is adequate provided it is the same independently realized map per block, including local resets and isolated stored halves. Coherent or correlated apparatus faults across blocks are outside this assertion.

Outer syndrome extraction, finite-field arithmetic, encoding/decoding and classical syndrome messages must be actual circuits, not an existence/capacity bound. Their required cost must be polynomial in B and log q=ell. If these circuits have polynomial length, synthesizing their total operator/operational error xi_n=exp[−Omega(B)] uses polynomial log(1/xi_n)=O(B) accuracy overhead in a conventional universal ideal-gate model. This does not tolerate a fixed physical gate-error rate. Charge storage of O(B ell)=O(n) distilled qubits on each side during outer processing, all consumed test/syndrome systems, trusted local operations, and the forward classical link. Corrected Schur front-end costs and independent approximate-design access remain part of the inner cost.

Only after the resource is prepared should an unknown external payload be admitted. Standard teleportation consumes the distilled ebits, actual Bell measurements, Pauli corrections and two classical bits per payload qubit. This keeps the unknown payload out of the long preparation period. A reduced teleportation-channel bound does not itself guarantee decoupling from every retained implementation/environment record without its separate interface proof.

## What the regime does and does not establish

For exact orthogonal contamination delta_n=c/n^z with c>0, the distance of the full input from the dominant pure tensor power is 1−(1−c/n^z)^n, which tends to one. Expected contaminants grow like c n^(1−z). Thus the conditional theorem is not a global pure-state approximation with vanishing error; fixed-defect correction is reused locally and conventional outer coding removes the remaining fixed block-error floor.

The source impurity still vanishes with n. This gives no efficient universal decoder for a fixed positive mixed-state impurity, no generic correlated-noise theorem, and no experimental or practical advantage. It is not a way to make fixed-j access solve the extensive-defect reference channel. A strong equally informed conventional purification protocol may match or outperform this changing-source regime; priority and practical comparison remain open. The distinctive bridge, if the inner review is received, is executable complete-multiplicity reference-frame access within the universal Schur code, not the standard outer amplification argument.
