# Independent audit, 5 November 2026

## Conclusions

The exact LP certificates rigorously exclude every n=9,...,17 under the stated unrestricted fully symmetric, rank-two, distance-five definition. Together with quantum Singleton (n>=9), this proves n_min>=18. The n=18 dual bound is exactly 1, not an exclusion. The known n=19 construction therefore leaves {18,19}. This is an evaluated consequence of an existing intrinsic MacWilliams LP, not a new LP framework. A targeted literature search located no earlier explicit distance-five n>=18 statement; that is not an exhaustive novelty certification.

No correctness error was found in the three-copy/PPT conventions. Independent full-matrix numerical tests support the partial-time-reversal map. Nevertheless, numerical feasibility/infeasibility or solver failure alone is not a rigorous bound. At inspection, ppt18.log ended in CLARABEL SolverError; this says nothing about code existence. The n=19 job was not rerun or modified.

## Exact certificate audit

check_certificates.py regenerates each Wigner-6j matrix independently, compares it exactly with the saved transform, checks M^2=I, verifies every dual multiplier is nonnegative, and verifies the rational identity

beta*1 - H^T*y - E^T*z = e_0,

where H=[I;2M-I] and E=(2M-I)[1:5,:]. Thus a_0<=beta*(n+1)/2 for every feasible enumerator. All exact checks passed. The upper bounds for n=9,...,18 are respectively:

359/734; 12/23; 19783/35392; 949/1546; 1495163/2189896; 3762283/4902390; 43874103385/51228355564; 507/550; 5455505247039/5544970533778; 1.

Define a_k=D/K^2 sum_q |Tr(P T_kq)|^2 using Hilbert-Schmidt orthonormal tensor operators. Then a_0=1 and sum a=D/K because Tr(P^2)=K. The twirl enumerator b_k=D/K sum_q Tr(P T_kq^dag P T_kq) obeys b=KMa and b>=a by Cauchy-Schwarz, with equality precisely on detected sectors. These facts require neither real coefficients nor a parity ansatz. Intrinsic ranks <5 correspond to compressed physical errors of weight <5.

check_enumerators.py directly builds tensor operators and pair Clebsch-Gordan projectors for random complex rank-two projectors at n=1,...,6. It checks b=2Ma and w=(4/D)M diag((-1)^k)a, with errors below 1.5e-14. This also confirms the marginal normalization used in the SDP: sum_J(2J+1)R_J[l,l]=K w_l.

## Three-copy audit

For X=twirl(P tensor P tensor P), Schur blocks R_J are PSD, commute with S3, and have no alternating S3 component because wedge^3(range P)=0. The code's symmetric/standard block construction respects this structure. Restricting the relaxation to real symmetric blocks does not exclude complex codes: average any feasible Hermitian blocks with their complex conjugates, since all constraints and recoupling coefficients are real. This averaged object need not itself be a code, which is harmless for a necessary-condition relaxation.

The lifted KL identities follow before twirling from partial tracing X(S_23-I/K) against a rank-r operator on copy 3: the result contains P tensor (P T P - Tr(P T)P/K), which vanishes for r<d. Rotating and averaging preserves this property. The supplied n=7 code audit checks the particular recoupled formula to 2.7e-16. This benchmark is useful but not a substitute for an exact symbolic derivation of the coefficient convention.

Partial time reversal is unitary-conjugate to partial transpose. Twirled P^tensor3 is separable among copies, so its partial time reversal is PSD. check_ppt.py constructs arbitrary real SU(2)-invariant three-copy matrices in the full product basis, transposes copy 3, conjugates by the spin time-reversal matrix, and compares the resulting Schur blocks with the implemented weighted 6j transform. It passes n=1,2,3,4 with maximum error 2.4e-14. It does not assume S3 symmetry or positivity, making it a direct linear-map test rather than a code-only check.

For publication-level SDP exclusion, retain an exact or rigorously interval-certified dual separator, prove the recoupled identities, and verify all PSD inequalities with certified margins. A solver status alone is insufficient. The original audit_lift.py's fallback sparse code is the 21-qubit example, not a 19-qubit witness; use audit(21), not audit(19), for that branch.

## Prior art and cautions

- Kubischta and Teixeira, MacWilliams Identities for Intrinsic Quantum Codes, arXiv:2604.16023v2 (26 August 2026), Appendix A normalized enumerators and SU(2) 6j transform; Proposition B2 identifies intrinsic depth with physical distance. https://arxiv.org/html/2604.16023v2
- Teixeira, Orthogonal Polynomials and the MacWilliams Transform for Permutation-Invariant Qudit Codes, arXiv:2605.15372v1, provides the explicit Racah transform for general n. https://arxiv.org/html/2605.15372v1
- KT itself attributes the SU(2) transform case to Bumgardner. Avoid claiming the enumerator or transform is newly derived.
- KT Appendix B-B has an apparent normalization typo saying sum tilde A=K; its own definition implies D/K. The audited code correctly uses D/K.
- The QIQCOP two-error record, last edited 15 September 2026, says neither preprint states a distance-five bound. This supports, but does not prove, novelty of the explicit evaluation. https://qiqc-op.com/problem/op_a72722e455d85d55/

Only files within audit_independent were created by this audit. Original scripts/results were not changed and heavy jobs were not rerun.

## Added sparse/complement formulation

The additional inequalities in three_copy_sparse.py are necessary. If Q=I-P, then twirl(P tensor P tensor Q)=X2_12 tensor I-X3>=0. This operator is separable, so partial time reversal on copy 3 remains PSD. In coupled blocks X2_12 tensor I is B12=diag(w_l/(2l+1)), agreeing with the script. Thus B12-R>=0 and B12-PPT3(R)>=0 are correctly normalized. The sparse row-major KL/PPT assembly agrees structurally with the dense formula. Dropping coefficients below 1e-15 makes the numerical model slightly approximate, so certification must restore exact coefficients or rigorously bound their errors.

Minimizing a common nonnegative PSD slack epsilon gives a useful numerical margin diagnostic, but a positive numerical optimum alone is not a rigorous separator. A certified strictly positive dual lower bound would establish exclusion. An epsilon numerically close to zero establishes only approximate feasibility of the relaxation, not a code.

Optional stronger constraints with no new variables come from all Boolean complement patterns. Let B13=U B12 U and B23=V U B12 U V. Then require (K/D)I-B12-B13+R>=0 and (1-3K/D)I+B12+B13+B23-R>=0, corresponding to twirls of P tensor Q tensor Q and Q tensor Q tensor Q. Their partial-time-reversal images are also PSD. Include permutation images of the first pattern before applying copy-3 time reversal, because fixed-leg PPT images may be inequivalent. All are necessary for arbitrary complex rank-two projectors.
