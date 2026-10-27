# A relative-to-marginal entropy region with an arbitrarily ill-conditioned reference

27 October 2026. Exact BKM path theorem and source-specific contraction coefficient. Independent receiving requested. This does not whiten entropy and does not assume a well-conditioned reference spectrum.

## Statement

Let X≥0 on C3⊗C^d, finite d, let E(X)=I3/3⊗Tr_A X=:τ, and let N=W3⊗id. Work on the actual product support C3⊗supp(Tr_A X); τ is faithful there. Suppose

mτ≤X≤Mτ, 0<m≤1≤M.

Define, continuously at z=1,

I(z)=(z logz−z+1)/(z−1)², I(1)=1/2,
Hτ(D)=Tr[D Dlog_τ(D)], D=X−τ.

Then the actual entropy deficit satisfies

Δ(X)≥[I(M)−I(m)/2] Hτ(D).                       (1)

Thus I(M)≥I(m)/2 is a sufficient dimension-free relative spectral region for the full VALUE inequality. When the coefficient is positive, equality forces X=τ.

More specifically, the SAME original source obeys the relative-entropy contraction bound

D(NX||τ)≤[I(m)/(4I(M))] D(X||τ).                (2)

Here both relative entropies use the actual τ=EX, which N fixes. This is a source-specific one-reference-state statement; it is not an arbitrary two-source relative-entropy comparison or an unrestricted mutual-information contraction theorem.

For the clean relative band τ/2≤X≤2τ, (1) becomes

Δ(X)≥(3log2−2)Hτ(X−τ)>0  if X≠τ,

and (2) has coefficient

(1−log2)/[2(2log2−1)]<1/2.

The reference eigenvalues may have arbitrary positive ratios. These conclusions are not obtained by applying the condition-number24 theorem to a whitened matrix.

## 1. Exact entropy path about the SAME marginal

Since E(D)=0, TrD=0 and TrD logτ=0. The latter follows because logτ belongs to E's fixed algebra. For X_s=τ+sD,

D(X||τ)=∫_0^1(1−s)H_(τ+sD)(D) ds.             (3)

This is the exact second-order Taylor integral for TrXlogX; its first derivative at τ is zero. TrX=Trτ, so the homogeneous relative-entropy convention's affine trace terms cancel as well.

The output path is N(X_s)=τ+sN(D), because Nτ=τ. It has the same marginal and trace, so

D(NX||τ)=∫_0^1(1−s)H_(τ+sN(D))(N(D)) ds.       (4)

The identity Δ=D(X||τ)−2D(NX||τ) is exact: logτ is fixed by E and both sources have marginal τ. No discarded reference, normalized-success branch, or changed baseline appears.

## 2. BKM base order and scaling are valid without commutation

For a faithful A,

H_A(K)=∫_0^∞ Tr[K(A+tI)^(-1)K(A+tI)^(-1)]dt.

It is inverse-homogeneous in its base: H_(cA)(K)=H_A(K)/c. It is also antitone in its base. If A≥B>0, then P=(A+tI)^(-1)≤Q=(B+tI)^(-1), and

Q^T⊗Q−P^T⊗P=(Q^T−P^T)⊗Q+P^T⊗(Q−P)≥0.

Vectorizing K gives the desired quadratic-form comparison and integrating proves H_A(K)≤H_B(K). This avoids the invalid inference that noncommuting squared resolvents can simply be ordered.

The source bounds imply

[1+s(m−1)]τ≤X_s≤[1+s(M−1)]τ.

Complete positivity of N and Nτ=τ give the same order bounds for N(X_s). Therefore

H_(X_s)(D)≥Hτ(D)/[1+s(M−1)],
H_(N X_s)(N D)≤Hτ(ND)/[1+s(m−1)].              (5)

## 3. Exact quarter factor at the actual product marginal

Because E(D)=0,

N(D)=−D^(T_A)/2.

At τ=I3/3⊗R, physical partial transpose is a Hilbert–Schmidt isometry and commutes with left and right multiplication by every resolvent of τ, whose physical factor is identity. Thus the resolvent metric gives the EXACT identity

Hτ(ND)=Hτ(D)/4.                                 (6)

This factor was already received in earlier product-baseline asymptotic work; here it is used in a finite path with the changing bases controlled by(5). It is not extrapolated to an arbitrary non-product base.

## 4. Integrate with all changing-base costs retained

The elementary scalar integral is

∫_0^1(1−s)/[1+s(z−1)]ds=I(z).

Combining(3)–(6) gives

D(X||τ)≥I(M)Hτ(D),
D(NX||τ)≤I(m)Hτ(D)/4.

Subtracting twice the second inequality proves(1). Since I(M)>0, eliminating Hτ(D) in the correct direction proves(2). As m,M→1 the coefficient in(2) tends to the exact local value1/4; no global-quarter contraction is inferred.

For m=1/2,M=2, I(1/2)=2−2log2 and I(2)=2log2−1, yielding the stated formulas. Positivity is exact: the first three positive terms of the atanh series give log2>842/1215, hence3log2−2>32/405>0.

## 5. Support, trace and scope

If the reference marginal is singular, positivity of X implies that X and NX vanish outside C3⊗supp(Tr_A X). Removing that unused zero direct-sum block is exact and is not a change of the reference information. On the retained finite product support, τ is faithful and m>0 makes every path head faithful, so all derivatives and integrals above are ordinary finite-dimensional ones.

The proof imposes no lower bound on the smallest retained eigenvalue of τ beyond positivity. For example, choose an arbitrarily ill-conditioned R>0 and any Hermitian K with E(K)=0 and ||K||≤1/2; then

X=(I3⊗R^(1/2))(I+K)(I3⊗R^(1/2)),
τ=I3⊗R

has τ/2≤X≤3τ/2. K may include several physical off-diagonal blocks with noncommuting reference coefficients. The congruence here constructs an actual source and proves its order bounds; it is NOT used to transform an entropy inequality. The entropy proof remains the original-source path above.

No external novelty priority is asserted. The new receiving step relative to the local quarter-factor asset is the finite relative-order path and its explicit source-specific coefficient.

Files: relative_marginal_bkm_entropy_region_certificate.py/.json. Existing quarter-factor sources include large_graph_attachment_entropy_asymptotic_theorem.md and anchored_reference_filter_high_noise_independent_audit.md.
