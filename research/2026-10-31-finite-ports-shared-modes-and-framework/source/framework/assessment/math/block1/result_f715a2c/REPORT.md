# A compatible QC construction beyond translations

The full exceptional-face question remains open, including the sharp boundary member P₀ from the first tranche. This continuation obtains **global quasiconvexity certificates for nontranslation cubics**, and combines two such certificates into an explicit positive class covering every real 2×2 nontranslation matrix M.

Keep the earned normal form

    P=F+zᵀMν(w)+Q,
    F=|w|⁴+2|z|²|w|², ν(w)=(u²-v²,2uv).

The following two polynomials are now proved QC for all means and all compatible test fields:

    P₊=F+x(u²-v²)+2yuv+(99/500)(r+t),
    P₋=F+x(u²-v²)-2yuv+(27/100)(r+t).

Each has a literal global polynomial one-form primitive and an exact positive definite rational 18×18 Gram for its corrected compatible heat density. `receive.py` reconstructs the entire polynomial identity and all positive rational pivots independently of the discovery algorithm. Thus this is an actual compatible QC construction, not sampled admission or a correction-selection oracle.

For P₊, the exact ROC threshold is 3/16. Consequently the global QC threshold for this isotropic slice is now rigorously bracketed by

    3/16 ≤ λ_QC ≤ 99/500.

The upper quadratic coefficient is 1.056 times the sharp ROC coefficient. This ratio measures the acquired sufficient coefficient, not a demonstrated separation or an optimal QC constant. In the original task normalization, divide by three: the acquired upper quadratic is (33/250)|A|², versus the ROC boundary (1/8)|A|².

There is an explicit extension to arbitrary M. Use a proper singular-value decomposition with signed singular values m≥|n|, where m=σ₁ and n=sign(det M)σ₂. Set

    a=(m+n)/2, b=(m-n)/2,
    ρ(M)=(sqrt(99/500)*a+sqrt(27/100)*b)².

Then

    Q-ρ(M)(r+t) rank-one convex  =>  F+zᵀMν(w)+Q is QC.

The residual quadratic may lie on its weak ROC boundary and may contain all cross terms and determinant lineality. Proper rotations, amplitude rescaling, an optimized convex combination of P₊ and P₋, and addition of the actual QC quadratic provide the construction. It is a sufficient subclass of the sharp full ROC admission from the first tranche, not equality with that full class.

A further exact partial result holds at conformal means: for M=σO with O orthogonal, **every Q admitted by the sharp ROC criterion satisfies QC at every mean (z₀,0)**. This uses a nonnegative remainder plus a ROC quadratic, not finite-field testing. The proof is in `PROOF.md`.

The successful step was to build all twelve bilinear syzygies of the actual leading acoustic null variety. Appending the six Hessian coordinates produces eighteen features. A coefficientwise Gram lift then becomes finite linear algebra and a PSD feasibility problem; rational projection and exact positive pivots turn the acquired points into proofs. This supplies a constructive route beyond the first tranche's sharp-boundary polynomial-heat obstruction, while respecting that obstruction.

The alternative rational-primitive attack was not completed. It produced an exact thirteen-parameter affine family satisfying all leading and sharp-boundary null columns for denominator 1+16(r+t) and numerator degree at most five. A finite sample fit looked nearly positive, but fresh tests found a normalized negative eigenvalue about -0.00929. That candidate is rejected; neither global feasibility nor impossibility of the rational class is claimed. A compatible resonant-three-wave heat search also found no violation and approached the one-wave ROC threshold from below; finite searches establish no universal inequality.

Run `python3 receive.py`. The two selected exact replays pass. `sos_certificate_99_500.txt` and `sos_minus_certificate_27_100.txt` contain the literal primitives, features and rational Gram matrices. The acquisition scripts and failed search logs remain preserved. Governing source credit remains the frozen Bruno–Pasqualotto compatible heat mechanism and the inherited exceptional normal form/admission. Historical priority and external independent review are unestablished.

The remaining gap is the interval [3/16,99/500) even for M=I with isotropic Q, and the much larger problem of every general Q admitted by the sharp ROC criterion. No ROC/non-QC polynomial or actual gradient energy violation has been constructed.
