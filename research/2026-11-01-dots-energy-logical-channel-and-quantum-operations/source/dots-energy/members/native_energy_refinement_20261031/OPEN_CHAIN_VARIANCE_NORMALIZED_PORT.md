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

## 3. Acquired Neumann factor, without dense matrix synthesis

Use zero-based index labels0..n-1 for the frame. Let D_index be diagonal with D_00=1 and D_jj=sqrt(1-t_j²) for j>=1. Let S be the weighted left shift S|i>=t_i|i-1> for i>=1, and S|0>=0. Then

    R=D_index (I-S)^(-1)=D_index sum_(ell=0)^(n-1) S^ell.

Indeed the (j,i) entry of S^(i-j) is product_(e=j+1)^i t_e, exactly the frame coefficient above. This factorization also directly proves an acquired norm bound. Use tstar=1/40, ||S||<=tstar, and chi=1/(1-tstar)=40/39.

The contraction S/tstar is acquired by reading the known local t_i, a signed acceptance amplitude t_i/tstar, and an index decrement on its successful branch. Index0 and invalid padded indices select zero exactly. The input-dependent failure flag is retained; this is a contraction block, not an irreversible shift on the full register. A direct reversible scan through the n coefficient records prices lookup without QRAM. D_index is another normalization-one diagonal contraction with known nonnegative acceptance amplitude.

Prepare a finite LCU over ell with weights tstar^ell/chi, and a zero arm carrying the remaining weight. SELECT the product of ell copies of S/tstar, then apply D_index. Use fresh success ancillas for each product and unprepare the LCU index. This gives

    (1/chi) D_index sum_(ell=0)^L S^ell

as its good block. Here L=min(n-1, ceiling(log[1/(eta(1-tstar))]/log(1/tstar))) suffices. If L=n-1, the actual discarded tail is ZERO because S^n=0, irrespective of the numerical geometric bound. If the accuracy cutoff is selected before n-1, the discarded operator tail is at most tstar^(L+1)/(1-tstar)<=eta. All signs of t_i remain inside SELECT, not in sampling probabilities. The weight sum is <=chi, so the zero-arm padding is nonnegative. No singular-value amplification, stationary-weight oracle or optimal norm computation is used.

Compute the rational t_i and finite geometric weights reversibly, and synthesize their rotations to per-operation error eta divided by the explicit capped operation count. Products use at most L weighted shifts. A straightforward lookup/routing implementation costs O(n) record scans per shift, times their actual bit arithmetic and rotation costs; L=O(log(1/eta)) unless n is smaller. The frame W itself uses O(n) index-controlled rotations/comparisons and a highest-occupied-bond scan. Thus the construction has near-linear n overhead up to polynomial logarithmic and coefficient-bit factors, instead of requiring a dense n-dimensional unitary synthesis. This is a circuit-access bound, not a final native-simulator gate count.

The earlier correct dense-contraction alternative is preserved separately as OPEN_CHAIN_PORT_DENSE_ALTERNATIVE_7f92de7c.md; it is not load-bearing here.

## 4. Actual noncommuting system-operator port

Supply individual Hermitian system blocks A_i/alpha_i, with alpha_i>=0 and q_A=sqrt(sum_i alpha_i²)>0. Prepare index amplitudes alpha_i/q_A and SELECT A_i/alpha_i, retaining the index on success. This gives the rectangular system-operator stack

    B_A: v ->sum_i |i>A_i v, normalization q_A.

Terms with alpha_i=0 must be certified zero and omitted. The coefficients and SELECT routing have their actual polynomial-size costs. This is not the normalization sum_i alpha_i used for a generic coherent LCU sum.

For input system plus SOURCE, apply U_psi† to the source and use its all-zero projection as a block-encoding success condition. On this branch the old source is a clean zero register. Apply B_A into an index register, R/chi to that index, then the acquired W map which transfers the index into the source and erases it. The resulting successful operator is

    (1/(chi q_A)) sum_i A_i tensor |v_i><psi|
       = Q K P/(chi q_A),
    K=sum_i A_i tensor Z_i.

Every v_i is orthogonal to psi by the global odd spin, so the Q output is exact. The argument is valid on arbitrary source/system inputs as an operator BLOCK; it is not a normalized postselection protocol. Reverse the full unitary to acquire the adjoint port PKQ with the same normalization and error.

Thus rho_cert=chi q_A is an actually acquired offdiagonal normalization, with a proven norm bound; it is not merely an unimplemented variance estimate. Attenuate by one half to acquire QKP/(2rho_cert), as required by the native offdiagonal slack convention. If rho_cert exceeds the already acquired b=sum_i alpha_i, use the original projected K/b block instead and set rho=min(b,rho_cert); otherwise use this construction. Either branch acquires QKP/(2rho) without the generic singular-value-amplification overhead b/rho. There is still the priced finite Neumann/frame work and actual individual-A_i SELECT cost. Those cannot be hidden in a unit-cost query to an unrelated black-box K.

## 5. Limits

The construction uses the exact open zero-field chain coordinate factorization and individually accessible A_i. It does not grant the same frame for periodic, field-bearing, generic Gibbs or learned sources. A generic K/b encoding plus a small certified ||QKP|| still requires the paid slack-SVA route. Known state preparation alone does not acquire arbitrary coherent inverse fibres.

This local operation may sharpen a separately re-proved high-rate activity-based compiler. It does not alter the frozen baseline's billions-of-slots audit, prove practical advantage, or remove source-kernel conditioning, jump-stack normalization, arbitrary-input energy costs and control costs. No whole refined compiler is accepted by this note alone.
