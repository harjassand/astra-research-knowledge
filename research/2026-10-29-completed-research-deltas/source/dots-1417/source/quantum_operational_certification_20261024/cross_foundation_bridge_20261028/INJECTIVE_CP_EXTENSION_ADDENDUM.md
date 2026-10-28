# Optional extension: observable rank need not be a square

28 October 2026. Separate derivation prompted by the root's injective-embedding proposal. Not incorporated into or substituted for the frozen full-`d²` certificate; not independently reviewed. It does not solve a general quotient-operator-system lifting problem.

## Sufficient certificate

Retain the exact `r`-dimensional preparation-coordinate model `C_z=H^(-1)H_z`, trace row `m=1^T`, initial state `e_1`, count confidence event, and rank/reset assumptions. Choose an orthonormal Hermitian coordinate basis for `Herm(d)`, of real dimension `D=d²`, with trace row `tau`.

A candidate supplies a real injection `L:R^r -> R^D` and an explicitly checked left inverse `K:R^D -> R^r`, with

    K L=I_r,       tau L=m,
    sigma_0=X(L e_1)>=0,       Tr sigma_0=1.             (A1)

Fit predictive matrices `Ctilde_z` and full Hermitian-space maps `Wtilde_z` satisfying

    Wtilde_z L=L Ctilde_z,
    m sum_o Ctilde_(a,o)=m,
    tau sum_o Wtilde_(a,o)=tau,
    J(Wtilde_z)>=0.                                    (A2)

At fixed `L,K`, these are linear equalities and Choi LMIs in the fitted maps; minimizing a convex count-residual objective is an SDP. Embedding search remains nonconvex and paid.

The usual interval inversion, now without a square gauge, provides an entrywise error matrix:

    U=Hhat^(-1), A=|U|D_H, ||A||_infinity<1,
    M=(I-A)^(-1)|U|,
    E_z=M[D_z+D_H|Ctilde_z|+|Hhat Ctilde_z-Hhat_z|],
    |C_z-Ctilde_z|<=E_z.                               (A3)

Define the **existential exact extension** by

    W_z = Wtilde_z + L(C_z-Ctilde_z)K.                  (A4)

It is not an oracle supplied to the learner: its existence and properties are proved from the count interval. The actual implemented model is `Wtilde`.

Because `KL=I`, equation (A4) yields `W_z L=L C_z` exactly. Its error is entrywise bounded by

    F_z=|L| E_z |K|,      kappa_z >= ||F_z||_F.          (A5)

Require a rationally verified Choi margin `J(Wtilde_z)>=m_z I` with `m_z>=kappa_z`. The Choi/Frobenius isometry proves every `W_z` CP. Both full and predictive trace constraints in (A2) are essential:

    tau sum_o (W_z-Wtilde_z)
       =m sum_o(C_z-Ctilde_z)K=0.

Thus the exact extensions are instruments on **all** `Herm(d)`, not merely positive maps on the image of `L`. Starting from `sigma_0`, their products remain in `image(L)` and give

    tau W_(z_H)...W_(z_1)L e_1
       =m C_(z_H)...C_(z_1)e_1,

the actual word probability. The same hybrid half-diamond, common-CP-mixture, clocked and retained-memory bounds from the main note apply, with (A5)'s radii and physical quantum dimension `d`.

## Terminal effects without post-terminal calls

For a terminal outcome row `g_b` on `R^r`, fit a full-space effect row `btilde_b` and predictive row `gtilde_b` with `btilde_b L=gtilde_b`, positive Hermitian effects, and exact sums `sum_b btilde_b=tau`, `sum_b gtilde_b=m`. Define

    b_b=btilde_b+(g_b-gtilde_b)K.

Then `b_b L=g_b`. A count/repair radius for `g_b-gtilde_b`, multiplied entrywise by `|K|`, bounds the full effect's Frobenius/operator perturbation. Subtracting this radius before accepting each fitted effect certifies the actual full virtual POVM. Its measurement-channel error is charged separately. All terminal rows must still factor through the supplied observable quotient; this requires the enlarged test/rank promise, not merely a fitted extension.

## What this does and does not remove

This genuinely removes the arithmetic restriction `r=d²`; only `r<=d²` is required. It also avoids treating a positive or CP map on a quotient as automatically extendible: the fitted full CP extension and its exact intertwining equations are explicit witnesses, and uncertainty is lifted through a charged `K`.

It does **not** establish that every finite quantum process has an injective invariant copy of its minimal quotient inside a finite matrix algebra. A nontrivial quotient of a physical reachable space need not split as an invariant subspace. Nor does it give a dimension bound, efficient embedding search, zero-cost norm conversion, a guarantee on rank-deficient Choi boundaries, or a physical memory/reference interface.

An open sufficient regime exists whenever an embedding has a strictly CP full extension: small trace-preserving perturbations of `C` lift by `L(delta C)K` and remain CP. In contrast, positivity restricted to `image(L)` alone would not suffice.

## Elementary non-square fixture at the algebraic level

Take a qubit, initially `I/2`, retaining only the real-symmetric operator span `{I,X,Z}`. Use full-rank resets toward X and Z, unsharp X/Z test-and-reset instruments, and a depolarizing rotation about Y with `r=4/5`, `cos(theta)=3/5`, `sin(theta)=4/5`. These operations preserve that three-dimensional span, while their full qubit Choi matrices are strictly positive. The `Y` coefficient supplies the extra full-algebra direction; `L` embeds the three predictive coordinates and `K` projects back. The reachable and test spans both have dimension three, hence observable rank `r=3<d²=4`.

Its deterministic rotation has observable spectrum `1,(4/5)(3/5 +/-4i/5)`. Therefore `Tr C=49/25`, `Tr(C²)=401/625`, and

    (Tr C)² -3 Tr(C²)=1198/625>0.

Every nonnegative `3×3` matrix instead satisfies `(Tr Q)²<=3 Tr(Q²)`, excluding a three-state HMM realization at the same minimal rank. This is an **algebraic example only**, not a new count acquisition fixture; the main note's executed rank-four replay is unchanged. Larger HMMs are not excluded.
