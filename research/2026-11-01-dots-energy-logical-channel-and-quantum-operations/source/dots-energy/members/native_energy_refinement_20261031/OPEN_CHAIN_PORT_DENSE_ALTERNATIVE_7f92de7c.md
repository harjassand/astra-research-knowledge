# Acquired variance-normalized P/Q port for an open zero-field chain

31 October2026. Local construction candidate, separate from the frozen native compiler and resource audit. It supplies an actual operator circuit; it is not a free optimal-norm oracle or a general state-vector erasure result.

Let the source be the open zero-field Ising chain of the geometric native binding. Write independent coordinates as one global spin and n-1 bond signs. For bond j let

    |phi_j>=sqrt(p_j)|0>+sqrt(1-p_j)|1>,
    p_j=q_j/(1+q_j), t_j=2p_j-1=tanh J_j,
    |phi_j_perp>=sqrt(1-p_j)|0>-sqrt(p_j)|1>.

Then Z|phi_j>=t_j|phi_j>+sqrt(1-t_j²)|phi_j_perp>. A reversible prefix-XOR map C takes global/bond bits to physical spins. With U_phi,j the real orthogonal matrix having columns phi_j,phi_j_perp, define

    U_psi=C (Hadamard_global tensor product_j U_phi,j).

It prepares the exact positive Gibbs vector psi from all zero. In these coordinates the physical Z_i equals Z_global times the product of bond Z's preceding spin i. Number spins1..n and bonds1..n-1.

## 1. Explicit orthonormal frame

Set v_i=Z_i psi. Define w_0 by global |-> and every bond phi_j, followed by C. For j>=1 define w_j by global |->, bonds k<j in Z phi_k, bond j in phi_j_perp, and all bonds k>j in phi_k, followed by C.

These n vectors are orthonormal. For j<ell, at bond ell the vector w_j has phi_ell while w_ell has phi_ell_perp, so their overlap vanishes; each vector is normalized. Also

    v_1=w_0,
    v_(i+1)=t_i v_i+sqrt(1-t_i²)w_i.

This identity follows by expanding only bond i; all earlier factors are identical. Hence F:|i> ->v_i factors F=W R, where W|j>=w_j and the explicit n-by-n upper-triangular matrix R has entries

    R_(0,i)=product_(e=1)^(i-1) t_e,
    R_(j,i)=sqrt(1-t_j²) product_(e=j+1)^(i-1) t_e, 1<=j<i,
    R_(j,i)=0, j>=i,

with the indexing convention column i∈1..n and row j∈0..n-1. Empty products are1. In particular R_(0,1)=1.

The Gram matrix is Ccorr=F†F=R†R, with Ccorr_ij equal to the product of t's along the path from i to j. If |t_j|<=tmax<1, row sums of absolute entries are at most (1+tmax)/(1-tmax). Thus

    ||R||² <= gamma²=(1+tmax)/(1-tmax).

For |J_j|<=1/40 one can use the certified gamma²=41/39. No partition-function estimate or spectral-norm computation is needed.

## 2. The frame isometry is acquired, including index erasure

Work first in the phi basis, before U_psi. Given binary index j∈{0,...,n-1} and a zero n-bit source register:

1. Set the global input bit to1, so U_psi will map it to |->.
2. If j>0, set bond j to1. For each k<j rotate bond k from0 to t_k|0>+sqrt(1-t_k²)|1>. Leave every k>j at0. For j=0 leave all bonds0.
3. Reversibly compute the HIGHEST occupied bond, with the no-occupied-bond outcome encoded as0. It equals j exactly on every basis component of this superposition: bond j is definitely1 and all later bonds are0. XOR that answer into the index register, clearing it. Uncompute the answer/work register from the source.
4. Apply U_psi to the source.

The result is |0_index> w_j with clean work. This is an isometry on the valid n-dimensional index subspace and extends to a reversible circuit; invalid binary indices are flagged separately and select zero in the eventual operator block. It uses at most polynomial(n) routing, comparisons, controlled rotations and prefix-XOR gates. A simple scan implementation suffices; no QRAM or inverse-image oracle is assumed. The index is erased because the prepared states carry an acquired last-excitation marker, not because arbitrary labels can be erased for free.

All t_j are rational for rational q_j. Rotation amplitudes are algebraic and can be synthesized to any requested absolute tolerance. An O(number_of_rotations) telescoping bound controls the unitary error. Negative t_j are retained as signed amplitudes. Exactly zero t_j causes no division and is handled directly.

## 3. Finite small-matrix operation

R has only n² explicitly computable entries. Finite dense contraction synthesis can acquire a block encoding of R/gamma; the actual implementation chosen here instead acquires R/(2gamma) with uniform slack. Its norm is at most1 by the proved bound. A standard Halmos unitary dilation uses square roots of I-R†R/gamma² and I-RR†/gamma². These positive square roots are computed to squared tolerance to account for their Holder continuity at zero; no eigenvalue-gap assumption or matrix inversion is required. Alternatively first attenuate R/(2gamma), whose norm is at most1/2, and use the resulting uniform spectral slack. All n-dimensional matrix arithmetic, state/gate synthesis, controlled access and requested precision are paid polynomial(n,log(1/delta)); this is not unit-cost access to a general exponentially large matrix.

For the chosen attenuated version the square-root matrices have eigenvalues at least3/4 before taking square roots, so their ordinary analytic matrix arithmetic is uniformly conditioned. A near-unitary numerical dilation can be polar repaired with its Gram matrix near I; no small singular value is inverted. The final normalization is2gamma, exactly matching the native offdiagonal slack convention.

## 4. Actual noncommuting system-operator port

Supply individual Hermitian system blocks A_i/alpha_i, with alpha_i>=0 and q_A=sqrt(sum_i alpha_i²)>0. Prepare index amplitudes alpha_i/q_A and SELECT A_i/alpha_i, retaining the index on success. This gives the rectangular system-operator stack

    B_A: v ->sum_i |i>A_i v, normalization q_A.

Terms with alpha_i=0 must be certified zero and omitted. The coefficients and SELECT routing have their actual polynomial-size costs. This is not the normalization sum_i alpha_i used for a generic coherent LCU sum.

For input system plus SOURCE, apply U_psi† to the source and use its all-zero projection as a block-encoding success condition. On this branch the old source is a clean zero register. Apply B_A into an index register, R/(2gamma) to that index, then the acquired W map which transfers the index into the source and erases it. The resulting successful operator is

    (1/(2gamma q_A)) sum_i A_i tensor |v_i><psi|
       = Q K P/(2gamma q_A),
    K=sum_i A_i tensor Z_i.

Every v_i is orthogonal to psi by the global odd spin, so the Q output is exact. The argument is valid on arbitrary source/system inputs as an operator BLOCK; it is not a normalized postselection protocol. Reverse the full unitary to acquire the adjoint port PKQ with the same normalization and error.

Thus 2rho_cert=2gamma q_A is the actually acquired offdiagonal normalization, with rho_cert=gamma q_A also a certified norm bound. This is not merely an unimplemented variance bound: the block is already QKP/(2rho_cert). If rho_cert exceeds the already acquired b=sum_i alpha_i, use the original projected K/b block instead and set rho=min(b,rho_cert); otherwise use this construction. Either branch acquires QKP/(2rho) without the generic singular-value-amplification overhead b/rho. There is still polynomial-n matrix/frame work and actual individual-A_i SELECT cost. Those cannot be hidden in a unit-cost query to an unrelated black-box K.

## 5. Limits

The construction uses the exact open zero-field chain coordinate factorization and individually accessible A_i. It does not grant the same frame for periodic, field-bearing, generic Gibbs or learned sources. A generic K/b encoding plus a small certified ||QKP|| still requires the paid slack-SVA route. Known state preparation alone does not acquire arbitrary coherent inverse fibres.

This local operation may sharpen a separately re-proved high-rate activity-based compiler. It does not alter the frozen baseline's billions-of-slots audit, prove practical advantage, or remove source-kernel conditioning, jump-stack normalization, arbitrary-input energy costs and control costs. No whole refined compiler is accepted by this note alone.
