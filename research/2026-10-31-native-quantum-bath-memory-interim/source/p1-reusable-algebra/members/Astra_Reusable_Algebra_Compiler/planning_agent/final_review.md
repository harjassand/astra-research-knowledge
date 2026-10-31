# Final focused review of MAIN_PROOF.txt

Reviewed the combined source and cumulative_exact.py / cumulative_exact_results.json. Scope: theorem constants, centre separation, confidence inversion, costs, and the separate cumulative construction. This is a focused internal mathematical review, not historical novelty certification.

## Accepted items

* The moment-curve centre search is valid: at most binom(b,2)(b-1) integer choices can collide, so the stated number of trials suffices. Minimal-polynomial degree b certifies separation.
* The corrected complex-Gaussian bound uses epsilon^2/4; the stated q and the separately stated real-Gaussian constants are sound.
* The centre-only dimensions and one-copy trace formulas are correct, using the full compressed algebra basis.
* The Gamma deviance tail bound is correct. Its interval inversion needs the boundary convention below.
* Source actions, full-vector handling, algebra/centre work, exact bit costs, and downstream evaluation remain distinguished. The result does not claim free word execution or unrestricted optimization.
* Same-seed central-projector dependence and finite-grid rank/concentration union bounds are appropriately qualified.
* The cumulative relation construction maintains injective witnesses and charges residual-word execution. Its fixture reports 24 product candidates, 188 acquisition source actions, and 48 separate truth-check actions. These counts match the code and the stated restricted purpose.

## Three scoped corrections — incorporated and checked

Final consistency check confirmed all three patches below are incorporated in MAIN_PROOF.txt. Section 2 also explicitly distinguishes ideal exact-root operations for general complex sources from the finite-bit rational-source algorithm. The review is therefore accepted within its stated scope, rather than awaiting these corrections.

1. **Confidence inversion at zero.** For fixed observed w, D(w,nu) tends to w as nu decreases to zero. When t>=w the sublevel interval has lower endpoint zero, not a second positive boundary root. Invert positive boundaries where they exist, use zero otherwise, and then impose the unresolved-rank lower bound. This is a boundary convention, not a failure of the confidence theorem.
2. **General-source root terminology.** In the main arbitrary-complex exact-coefficient model, say "real root", not "real algebraic root" over Q. Algebraicity over Q and the fields Q(i,lambda) belong to the rational-source corollary. Exact root operations over the source coefficient field remain part of the charged exact algebraic model.
3. **Cumulative adjoint closure.** Explicitly require admitted generators to be Hermitian, or include each generator's adjoint as a separately available and charged action. Left-product closure of arbitrary non-Hermitian generators alone does not establish a *-algebra. The supplied cumulative fixture already uses real symmetric generators.

With those wording/boundary fixes incorporated, this review found no remaining material mathematical error in its stated scope. No practical numerical robustness or novelty conclusion is inferred.

## Optional regular recompression — accepted

For a basis B_i of the full learned algebra, let H_ij=Tr_K(B_i^dagger B_j), where dagger is the G-adjoint in nonorthonormal coordinates. This H is positive definite. Left multiplication matrices L_j satisfy H L_j=L_j*H for Hermitian source generators and form a faithful unital *-representation. Inverses, spectra, operator norm and PSD order therefore transfer using the H metric.

If e is the coordinate vector of the identity and f_i=That(B_i), the trace estimate is f^T L_X e. The transpose is intentional: That is complex-linear, so no conjugation of f is applied. Centre-normalized linear functionals transfer in the same manner.

The construction uses no new original source actions. The stated conservative preparation cost O(d R^3+d^2 R^2) accounts for G-adjoints plus Gram formation, with the first term unnecessary in orthonormal coordinates. Structure-constant solving remains charged. Retaining the smaller of the R-dimensional cyclic and d-dimensional regular representations yields the stated conservative future evaluation bound O(L min(R,d)^3), with scalar/bit costs still separate. This is established regular-representation machinery, not a separate novelty claim.
