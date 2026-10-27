# Relative peak 3/2: exclusion of deficient-Schmidt output kernels

27 October 2026. Exact structural extension of the full-Schmidt rigidity theorem.

Let X≥0 on C3⊗C^d, τ=EX faithful on the actual product support, and X≤(3/2)τ. Every nonzero vector in ker(NX) has Schmidt rank three. In particular, when the retained reference dimension is three, every source with singular NX is the reference-filtered symmetric-projector family characterized and VALUE-paid in relative_peak_three_halves_singular_output_rigidity.md.

## Proof without assuming the reference has dimension three

Normalize a hypothetical kernel vector ψ and let S be its reference Schmidt support of dimension r≤2. Set A=(3/2)τ−X. Then A≥0, EA=τ/2 and (3E−N)A=NX. Thus A is orthogonal to the positive operator (3E−N)^*(Pψ).

Compress to C3⊗S and denote A_S that positive compression. Its reference marginal is faithful because Tr_A A_S=(3/2) times the compression of τ's reference factor. In Schmidt coordinates, Rψ is faithful on S. Conjugate A_S by K=I3⊗sqrt(Rψ), obtaining B. The support orthogonality says B lies in the kernel of

(I3⊗I_S+F_r)/2,

where F_r swaps the physical Schmidt support with S and is zero on the complementary physical subspace. On that complementary subspace the displayed operator equals I/2. On the r×r Schmidt block its kernel is exactly wedge²C^r.

Meanwhile A≤3EA, and compression and the reference-only congruence give

B≤I3⊗Tr_A B.                                    (1)

For r=1 the kernel is zero, so B=0. For r=2 the kernel is the one-dimensional normalized antisymmetric line, so B=cP_singlet with c≥0. Its partial trace is cI_S/2; evaluating (1) on the singlet gives c≤c/2 and forces c=0. Both cases contradict the faithful compressed marginal. Hence r cannot be 1 or 2.

The case of a smaller retained reference support is included: if its dimension is at most two, NX is necessarily faithful under this relative peak assumption. No unsupported inverse of a singular Rψ is used; all inverses and congruences are restricted to S.

## Exact canonical boundary block for arbitrary finite reference

A useful algebraic normal form does NOT imply entropy whitening. Write τ=I3⊗T with T>0 and define Y=(I⊗T^(−1/2))X(I⊗T^(−1/2)). Then EY=I and 0≤Y≤3I/2. A kernel vector of NY has Schmidt rank three, as just proved. Let S be its three-dimensional reference Schmidt support. The compressed source Y_S still has marginal identity and relative peak 3/2, and the full-Schmidt rigidity theorem applies. Since its marginal is identity, the theorem forces the kernel vector to be maximally entangled on S and

Y_S=(3/2)P_sym,S

in suitable physical and reference Schmidt bases.

Set Z=2Y/3. Its S-corner is the projector P_sym,S. Because both Z and I−Z are positive, the cross block between C3⊗S and C3⊗S^perp must vanish: positivity of Z kills the cross block on ker P_sym,S, and positivity of I−Z kills it on ran P_sym,S. Thus

Y=(3/2)P_sym,S direct-sum Y_rest,
EY_rest=I on the remaining reference factor, 0≤Y_rest≤3I/2.

This is an exact source classification after a reference congruence. For d=3 it leaves no remainder and gives the already-paid family. For d>3, undoing the congruence need not preserve an orthogonal reference direct sum: T may couple S and S^perp. Therefore no entropy additivity, mixture closure, or unrestricted VALUE proof follows from this normal form. The remaining source-linked interface is precisely that nonorthogonal reference recombination.
