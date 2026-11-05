# Weak-parent boundary-mode stress test and an explicit repair

Date: 2026-11-05. Internal mathematical extension and independent stress test. This is not an external proof review, novelty claim, new physical gap discovery, or general weak-parent theorem. The proper-parent candidate in `../lti_gap_completeness_20261105/` is left unchanged.

## Result and scope

The persistent open zero modes of one-species Product Vacua with Boundary States (PVBS) do **not** furnish a counterexample to convergence of the unrestricted nearest-neighbor Rai LTI gap hierarchy. There is an explicit, reference-safe boundary channel that handles them. The same argument covers every positive two-site interaction with the same local kernel, including number-nonconserving interactions, and finite tensor products with other repaired layers.

The naïve channel that resets both buffers to the bulk vacuum fails the needed exponentially small operator estimate. Its failure is real but is a counterexample to that channel, not to the SDP hierarchy.

For the class proved below, for valid hierarchy levels n>=3,

    gamma_n >= Delta_n - O(sqrt(log(n)/n)),

and gamma_n converges to the periodic finite-size gap limit. No assertion is made here that this includes every weak parent, every native multispecies PVBS model, every unique-MPS bulk Hamiltonian, or every restricted numerical hierarchy. GNS identification is outside this note.

## 1. A genuine weak parent

Fix 0<lambda<1 and define

    p = (|01> - lambda |10>)/sqrt(1+lambda^2),
    h0 = |p><p| + |11><11|.

Its L-site open ground space, for every L>=2, is

    S_L = span{|vac_L>, |psi_L>},
    |psi_L> = sum_(j=1)^L lambda^(j-1) |j>,
    n_L = ||psi_L|| = sqrt((1-lambda^(2L))/(1-lambda^2)).

Here |j> has one particle at site j. Thus the open kernel remains two-dimensional at all lengths, although the bulk and periodic ground state is the product vacuum. It is not a proper parent of the D=1 bulk tensor.

For completeness, write n_j=|1><1|_j and a=lambda/(1+lambda^2). Then

    h0_(j,j+1) = [lambda^2 n_j+n_(j+1)]/(1+lambda^2)
                 - a (sigma_j^+ sigma_(j+1)^- + h.c.).

The open Jordan-Wigner transform is quadratic. Its one-particle spectrum consists of one exact zero mode psi_L and

    1 - 2a cos(k*pi/L),   k=1,...,L-1.

Many-body energies are sums of those one-particle energies. Consequently the full open gap is

    g_L = 1 - 2a cos(pi/L) >= g0 := (1-lambda)^2/(1+lambda^2)>0.

The periodic gap of h0 is exactly g0: the operator inequality H_per>=g0 N_particle follows by bounding each hopping term by n_j+n_(j+1), and the uniform one-particle vector attains g0. This does not need a boundary-condition convention for Jordan-Wigner fermions.

More generally, let h be any positive two-qubit interaction with

    ker h = span{|00>, |10>+lambda|01>}.

If a0 is its smallest positive eigenvalue and M=||h||, then

    a0 h0 <= h <= M h0.

Every open kernel remains S_L, the uniform open gap is at least g=a0 g0, and the periodic ground is uniquely the vacuum. The complementary two-dimensional positive block of h can be arbitrary; it need not commute with particle number. These are genuine weak-parent deformations, not proper parents obtained by changing the bulk MPS bond dimension.

For lambda>1, spatially reflect the construction and use 1/lambda. The local projectors transform accordingly. The special lambda=1 model is periodically gapless and is treated by the elementary gapless observation below, not the exponentially localized repair.

## 2. Why resetting both ends is wrong

Use two ell-site end buffers L and R and their untouched inner neighbors s and t, respectively. Input physical order is L,s,...,t,R. The right extended ground vector is

    |psi_(ell+1)>_(t,R)
      = |1>_t |vac_ell>_R + lambda |0>_t |psi_ell>_R.

Take the normalized product of left-window vacuum and this right-window vector. It is exactly in S_(ell+1)^L tensor S_(ell+1)^R. Resetting both buffers to vacuum leaves probability 1/n_(ell+1)^2 of a particle at untouched site t. For h0, its repaired boundary-square expectation is

    lambda^2 / [(1+lambda^2) n_(ell+1)^2]
       -> lambda^2(1-lambda^2)/(1+lambda^2) > 0.

The mode sits at an artificial inner cut, so it must be retained rather than erased. A separate simpler obstruction says that no boundary-only channel can turn every finite open zero mode exactly into the periodic vacuum: its nonzero interior particle marginal cannot change. Neither observation prevents exponentially accurate repair.

## 3. A CPTP channel that retains the correct mode

Let V_L be the exact two-column isometry

    V_L|0> = |vac_L>,   V_L|1> = |psi_L>/n_L.

The channel acts jointly on the two end buffers only:

1. Discard the entire old left buffer into an environment.
2. Decode the right buffer with the CPTP map

       D_ell(X)=V_ell^* X V_ell
                 + Tr[(I-V_ell V_ell^*)X] |0><0|.

   With a reference, the second branch uses the partial trace of the projected input and preserves that reference; it is not a scalar replacement of its state.
3. Encode the retained qubit with V_(2ell), placing its physical output in cyclic order R followed by L, without reversing either block.

Call the channel Phi_ell. It preserves the entire untouched core marginal. Every output is exactly in S_(2ell) on the joined R,L buffers, so all internal buffer terms and the periodic seam annihilate the output. Only the two seams to the unchanged core can act.

An explicit complete Kraus family appears in `check_pvbs_repair.py`. For each old-left computational bra <p|, it contains

    V_(2ell) V_ell^* (<p|_L tensor I_R)

and, for an orthonormal basis {|z>} of S_ell^perp on R,

    |vac_(2ell)> (<p|_L tensor <z|_R).

The sum of K^*K is exactly identity. In the success term the displayed product means composition with the right-buffer decoder, with output in the joined order. The usual reference extension is automatic for this Kraus channel.

## 4. Full-code operator estimate, including arbitrary references

Let P project onto S_(ell+1)^(L,s) tensor S_(ell+1)^(t,R). It is a four-dimensional code; any reference is arbitrary. Keep the entire discarded left buffer as a Stinespring environment. On P the right decoder's reset branch vanishes, so the actual map K is an isometry.

Set

    alpha = n_ell/n_(ell+1),
    beta = lambda^ell/n_(ell+1),
    delta^2 = [lambda^2(n_ell-n_(2ell))^2
                + lambda^(4ell+2)] / n_(ell+1)^2.

Use normalized ground labels a,b in {0,1} for the left and right extended windows. Define an ideal comparison map K0 on all four code basis vectors:

    K0 |a,b> = e_a tensor f_b,

where the environment and output vectors are

    e_0=|vac_ell>,        e_1=alpha |psi_ell>/n_ell,
    f_0=|vac_(2ell+2)>,   f_1=|psi_(2ell+2)>/n_(ell+1).

The physical output order is t,R,L,s. K0 need not preserve norm; its norms are uniformly bounded for fixed lambda. Its physical image is exactly S_(2ell+2), so both core seams, all joined internal terms, and their sum annihilate it.

The actual input decompositions are

    |1>_(L,s) = alpha (|psi_ell>/n_ell)|0>_s
                  + beta |vac_ell>|1>_s,

    |1>_(t,R) = [|1>_t|vac_ell>_R
                    + lambda n_ell |0>_t(|psi_ell>/n_ell)_R]
                   / n_(ell+1).

These identities give the four squared column errors of K-K0, in order 00,10,01,11:

    0, beta^2, delta^2, alpha^2 delta^2+beta^2.

In the last column the two terms have orthogonal environment vectors, the old-left vacuum and normalized one-particle vector. Hence the exact Frobenius error is

    ||(K-K0)P||_F^2
       = epsilon_ell^2 := 2 beta^2+(1+alpha^2)delta^2
       = O(lambda^(2ell)).

Thus the operator norm is at most epsilon_ell. The estimate is on the full code and remains valid after tensoring with an arbitrary reference. It is not a calculation on one selected ground vector.

Let H_b contain all periodic terms outside the unchanged contiguous core. On both K and K0 images, H_b reduces to the two seams and has norm at most 2M. Since H_b K0 P=0,

    P Phi_ell^*(H_b^2) P <= 4M^2 epsilon_ell^2 P.

For all inputs, including reset branches,

    ||Phi_ell^*(H_b^2)|| <= 4M^2.

The positive-block inequality F<=2||F||(I-P)+2||PFP||P now gives

    Phi_ell^*(H_b^2)
       <= 8M^2(I-P)+8M^2 epsilon_ell^2 I
       <= (8M^2/g)(H_left_extended+H_right_extended)
                     +8M^2 epsilon_ell^2 I.

This is exactly the energetic repair guarantee needed by the hierarchy argument, now for a non-proper parent.

## 5. Consequence for the unrestricted LTI hierarchy

This section records the necessary argument so the extension is not merely an unverified reference to boundary intuition. Use the unrestricted nearest-neighbor hierarchy of Rai et al., Eq. (17), n>=3. Its dual rho>=0 has equal left/right (n-1)-site marginals, Tr(rho h1)=1, and objective

    v = Tr rho [h1^2 + sum_(j=2)^(n-1) {h1,hj}].

Write m=n-1. Local translation invariance gives every Tr rho hi=1, a=Tr rho hi^2<=M, and translated anticommutator moments b_r. Positivity gives b_1>=-2M and b_r>=0 for r>=2. Therefore

    Tr rho H_open^2 <= m v+2M.

The maximally mixed normalized dual is strictly feasible; the primal is feasible at delta=-M by the standard three-site coboundary (h1+h2)^2+(M h1-h1^2). Slater duality applies and nearly optimal dual witnesses suffice. A one-site excitation above the unique periodic vacuum bounds gamma_n<=2M.

Let Q project off the full two-dimensional open kernel, not just off the vacuum, and put mu=Q rho Q. Every hi and every hi hj annihilates that full kernel on both sides, so all used moments are unchanged. The open gap gives Tr mu<=m/g.

With buffers of length ell, the untouched contiguous core has m_c=m-2ell bonds and obeys the exact moment bounds

    Tr mu H_c=m_c,
    Tr mu H_c^2<=m_c v+2M.

Apply nu=Phi_ell(mu). It is unnormalized; the channel preserves its trace and core moments. From the preceding repair inequality,

    K_(n,ell):=Tr nu H_b^2
       <=16M^2 ell/g+8M^2 epsilon_ell^2 m/g.

The periodic gap inequality H_per^2>=Delta_n H_per and the weighted Hilbert-Schmidt triangle inequality yield

    Delta_n <= [sqrt(m_c v+2M)+sqrt(K_(n,ell))]^2/m_c.

No normalization of mu or nu is silently performed, and no orthogonality of nu to the periodic ground is required. Take v down to gamma_n. Choosing ell proportional to log n makes K_(n,ell)=O(log n) and gives

    gamma_n >= Delta_n - O(sqrt(log(n)/n)).

The usual certified upper comparison gamma_n<=Delta_N for N>=2n implies

    Delta_n <= inf_(N>=2n) Delta_N + o(1).

It forces limsup Delta_n<=liminf Delta_n. Thus the periodic limit exists and gamma_n converges to it. No separate monotonicity assumption is needed.

The locality and subspace proof work for any h with the stated local kernel; the reference h0 is used only to supply the exact kernels and a uniform open gap.

## 6. A larger class, without claiming all weak parents

Take finitely many independent on-site layers, each either a noncritical one-species PVBS chain (possibly with opposite localization direction) or one of the proper injective-MPS parent chains from the separately audited candidate. Let

    h_ref = sum_j c_j h_j,  c_j>0,

on the tensor-product site. The local and open ground spaces factor across layers. The open gap is bounded below by the smallest weighted layer gap. The periodic ground is unique for sufficiently large lengths.

Apply each layer's boundary channel to its own tensor factors. Their tensor product is CPTP and leaves the core marginal unchanged. Joined-buffer outputs lie in the tensor-product open ground space. The tensor product of the ideal comparison maps is exactly seam-ground. A telescoping norm bound, using finitely many uniformly bounded maps, gives exponential actual-ideal error with the slowest layer rate. Thus the same repair estimate and hierarchy convergence follow.

One can then replace h_ref by **any positive nearest-neighbor interaction h with exactly the same local kernel**. Finite-dimensional comparison gives constants a,b>0 with a h_ref<=h<=b h_ref. It preserves every open ground space, the uniform open gap, and the unique periodic ground. The very same repair channels remain ground-subspace preserving and their bounds transfer with M=||h||. Such a deformation can couple layers and need not retain particle-number conservation or a sum-of-layers form.

This is a meaningful class of weak parents with injective-MPS bulk ground states and persistent finite-dimensional boundary modes. It is not asserted to contain the native exclusion-coupled multispecies PVBS family in full: tensor-product layers and that family have different on-site spaces and constraints.

## 7. What this does and does not settle

- The known PVBS zero modes invalidate automatic use of the proper-parent kernel hypothesis. They do not invalidate the hierarchy's convergence once the appropriate asymmetric channel is constructed.
- A vacuum reset fails, even on an exact local ground subspace. The retained inner-cut mode is essential.
- No counterexample to full unrestricted hierarchy convergence was found. The general gapped weak-parent case without a demonstrated uniform open gap and controlled boundary channel remains open in this work.
- For any frustration-free chain with liminf_N Delta_N=0, the generic dual estimate gamma_n>=-2M/(n-1) and gamma_n<=inf_(N>=2n)Delta_N already squeeze gamma_n to zero. Therefore a periodically gapless uncle model is not by itself an adversarial counterexample to hierarchy convergence. This observation does not assert a periodic limit exists for every general chain.
- The PVBS spectra, boundary modes, and gap existence are established prior art. The present operation is an explicit repair used for this particular SDP convergence extension. Its novelty has not been established.
- The proof depends on the correctly scoped proper-parent result only for the optional tensor factors of that type. The single-species PVBS proof is self-contained apart from standard SDP duality and the hierarchy's published finite-periodic lower-bound property.

## 8. Reproducible checks and references

`check_pvbs_repair.py` independently constructs all physical matrices; it imports no earlier MPS repair code. `pvbs_repair_results.json` records:

- 24 full-code operator tests: lambda in {0.25,0.7,0.95}, ell=1,2,3,4, for h0 and a complex positive kernel-equivalent interaction;
- 20 finite open spectra/kernel checks, including lambda=1.4;
- three full-input Kraus completeness and joined-ground checks, each with a nonzero reset branch.

The maximum full-code isometry defect was 8.89e-16 and maximum ideal seam residual 1.72e-16. The exact Frobenius expression matched in every case. These are floating sanity checks, not validated numerical gap certificates and not a substitute for the algebra above.

Primary sources:

- S. Bachmann and B. Nachtergaele, *Product Vacua with Boundary States and the Classification of Gapped Phases*, arXiv:1212.3718, https://arxiv.org/abs/1212.3718. The PVBS family, open boundary degeneracy, bulk product vacuum, and gap properties predate this work.
- Rai et al., *A Hierarchy of Spectral Gap Certificates for Frustration-Free Spin Systems*, arXiv:2411.03680v3, https://arxiv.org/html/2411.03680v3. The hierarchy and its certified lower-bound property are theirs.
- Rozman, Molnar, and Schuch, *Lower Bounds on Spectral Gaps of Parent Hamiltonians via Tensor Networks*, arXiv:2607.19078, https://arxiv.org/html/2607.19078v1. Relevant proper/weak-parent distinction and established parent-gap methods.

The accompanying second review records its own primary-source checks and the exact limitations of native multispecies gap formulas.
