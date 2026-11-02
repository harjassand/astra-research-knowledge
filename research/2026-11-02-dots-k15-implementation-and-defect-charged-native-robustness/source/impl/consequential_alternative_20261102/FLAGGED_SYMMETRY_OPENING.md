# Selected sharper opening: degenerate symmetric codes with analog noise flags

This is an exact construction/evaluation reduction, not a positive-capacity witness. It is the same scientific target as the N585 lattice attempt: unassisted bosonic communication in a noise region not supplied by the established hashing bound. The fresh enabling primary is Agarwal et al., *Enhanced quantum capacity thresholds from symmetry*, arxiv:2605.09138v1 (May 2026). It shows that low-rank states in the n-qubit symmetric subspace yield better Pauli thresholds via environment degeneracy. Hard-decoded square GKP cannot transfer those numbers beyond v=1/e: p(1/e)=.143965 exceeds their .118371 independent-XZ point. Therefore retaining analog reliability is indispensable.

## Physical receiving channel

For square qubit GKP, one quadrature syndrome s lies in C=[−sqrt(pi)/2,sqrt(pi)/2). Write

    g_v(s)=sum_m f_v(s+m sqrt(pi)),
    p_v(s)=sum_(m odd) f_v(s+m sqrt(pi))/g_v(s).

The q and p records are independent under isotropic displacement noise, and condition independent logical X and Z errors. Quantize the pair of records into a fixed alphabet A with B cells. Let w_a be the probability of cell a, and let Phi_a be the Pauli channel whose probabilities are the exact conditional integrals over that cell. The receiver's complete channel is

    F(rho)=sum_a w_a |a><a| tensor Phi_a(rho).

The flags are independent of the logical input; they are retained at the receiver, not heralded to the sender. No failed branch is removed. A common compact syndrome wavepacket gives the finite-energy version by replacing f_v by its convolution as detailed in FINITE_ENERGY_ZAK_BRIDGE_DRAFT.md. Actual decoder costs remain separate.

## The symmetry operation survives finite flags

Take orthonormal codewords psi_0,psi_1 in Sym^n(C²), and any fixed prior p. The input is rho_n=sum_r p_r |psi_r><psi_r| with reference dimension two. For a flag sequence, channel probabilities factor. All flag sequences with the same histogram n_vec=(n_1,...,n_B) give unitarily equivalent output/reference states because the input is fully permutation symmetric. Their conditional channel is

    Phi_1^tensor n_1 tensor ... tensor Phi_B^tensor n_B,

and the histogram probability is

    W(n_vec)=n!/(prod_a n_a!) prod_a w_a^n_a.

Hence the COMPLETE coherent information, including all flags, is exactly

    Ic(F^tensor n,rho_n)
     =sum_nvec W(nvec) [S(sigma_B(nvec))−S(sigma_RB(nvec))].

For each histogram the conditional states commute with H=prod_a S_(n_a), not with the full S_n. Decompose each flag group with qubit Schur–Weyl duality. Its spin block j_a=0,...,floor(n_a/2) has small dimension l_a+1=n_a−2j_a+1 and multiplicity

    mu(n_a,j_a)=binom(n_a,j_a)−binom(n_a,j_a−1).

The output has blocks X_j tensor I_mu and reference-output has Y_j tensor I_mu, with X_j=Tr_R Y_j. The largest matrix requiring diagonalization is

    2 prod_a (n_a−2j_a+1),

rather than 2^(n+1). Multiplicity entropy terms cancel in the coherent-information difference. All branches and multiplicities remain counted.

## Explicit block generator, no hidden exponential tensor

Use n+1 roots z_i of unity and unnormalized qubit vectors v_i=|0>+z_i|1>. Fourier inversion gives

    |D_k^n> = 1/[(n+1)sqrt(binom(n,k))] sum_i z_i^(−k) |v_i>^tensor n.

Thus any code density/reference block is a finite sum of M_ij^tensor n, M_ij=|v_i><v_j|, with known coefficients. For histogram nvec its small block is obtained by replacing each power with

    tensor_a q_(n_a−j_a,j_a)(Phi_a(M_ij)),
    q_(n−j,j)(M)=det(M)^j Sym^(n−2j)(M).

The normalized symmetric-power matrix is a finite binomial polynomial in the four entries of M (Agarwal et al. Eq4). This yields all output and reference blocks by finite algebraic operations and one-dimensional/two-dimensional Gaussian integrals for the flags. Root-of-unity interpolation can be enclosed to arbitrary precision; cancellation/bit precision must be charged.

## Real resource restriction and decisive gate

For FIXED B the count of histograms is binom(n+B−1,B−1); Schur blocks and dimensions are polynomial in n. A crude dense-eigensolver bound is O(n^(5B−1)) arithmetic. This is not practically small merely because it is polynomial. With two bins per quadrature B=4, n=12 has maximum reference-block dimension 2*4^4=512 (balanced groups), but many blocks and histograms; n=30 can already have blocks above ten thousand. Fine analog bins explode this cost. B=2 total joint flags is cheaper but may lose too much useful reliability.

The hard target is now specific: find one finite n, rank-two symmetric state and small flag partition with a rigorously positive Ic at v>1/e, with finite-energy perturbation smaller than its strict margin. Use the corresponding symmetric-state, unrestricted-receiver and unquantized analog baselines at identical noise and resource constraints. A positive Pauli threshold without the flag integrals is not a bosonic result. A finite numerical optimization without outward entropy certification is not a capacity proof. No such witness was acquired in this pass.

This is a better-motivated continuation than Euclidean lattice packing alone because the 2026 primary provides an actual environment-entropy suppression mechanism that beats hashing in another channel, while the exact flag-histogram reduction identifies how to preserve the decisive analog information without giving up all finite symmetry. It is still a scientific opening, not a demonstrated enabling capability or a civilization-changing result.
