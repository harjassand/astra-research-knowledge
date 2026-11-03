# Independent audit: both Wilson faces massed, normal thickness two

2026-11-03. Audited `TWO_MASSED_FACE_WILSON_BRIDGE.md` at the request of its constructor, and reported to root.

**Verdict:** the static endpoint gap and additive index proof pass. This is a distinct two-covariant-texture model, not a permission to put a symmetry-breaking constant mass on the original far face.

1. For the actual two-layer SSH matrix bI-S, the singular values are (sqrt(1+4b^2) +/- 1)/2. The smaller is <=b^2 and the larger >=1. With theta=arctan(2b)/2, |sin theta|<=b and 1-cos theta<=b^2/2. The two low chirality sectors have the stated opposite tangential Dirac operators and tunneling <=b^2/a.

2. A mass at either physical layer acts as identity on the Wilson spin/normal factor and therefore preserves X chirality. Direct matrix elements between the two low opposite-chirality sectors vanish, even for nonconstant textures. Their diagonal mass compressions are C U0 C+S U1 S and S U0 S+C U1 C (a harmless sign convention for S cancels consistently). Each differs from its intended texture by <=3 b_*^2 in norm. No momentum-count factor is needed.

3. The physical layer projectors are orthogonal, so the total boundary perturbation has norm M, not 2M. The previous full-Brillouin-zone gap bound remains valid at L=2; indeed the excluded second normal singular value is >=1. The high block can be homotoped to the balanced doubled free block without closing its gap. Its Schur correction on the full low space has norm <=M/399.

4. The two finite localizers are one for D=+sigma.p and U0, one for -D and U1. Each already includes spin and the two-dimensional flavor; no extra multiplicity is to be inserted. Both have gap M/2 under the primary localizer theorem. The total error is block-norm maximum for the face-diagonal errors plus normal tunneling and the single high-sector correction, not a mandatory sum of both localizer errors.

5. With Lambda=1000M and aM<=10^-6, b_*<=5e-7 and b_*^2/a<=2.5e-7 M. The displayed E2/M<.024 follows. Exact Schur congruence then gives gap(H)>.476M/(1+1/399)^2>M/3. The argument does not use M>=pmin and does not retain an untreated small-gap far sector. AP makes the continuum D invertible; it is not the origin of the final gap.

6. Exact inertia gives Q=-Index(D+,U0)-Index(D-,U1)=-W0+W1. Using the separately calibrated winding convention Wj=-sj yields Q=s0-s1. The compensation signs in the note follow. There is no ultraviolet integer left undetermined.

7. Both U0 and U1 must transform by the same physical left D(alpha) action. A fixed U1=I would break this covariance. Independent covariant fields with appropriate opposite decorations are genuine additional physical input relative to the one-face model; static results for this doubled boundary system should not be relabeled as a single-boundary interface theorem.

The two-layer model has finite-range coefficients, local norm O(1/a), and a volume-uniform static gap. Its projector locality and finite-patch endpoint transport can therefore be obtained with constants depending only on the fixed ratio W/M, without the earlier pmin-dependent low-far suppression or logarithmic thickness. This is a useful simplification for the actual two-texture problem. It still proves no consistency of charged-move signs, rotor collective gap, or efficient simulation. The earlier >=10^21-site-per-coarse-cell UV scale remains.

## Addendum: all normal thicknesses and the static half-space

The constructor's subsequent extension to every L>=2 also passes. The geometric singular-vector estimate gives distance <=sqrt(2)b^L/(1-b)<2b^L for b<=1/8. Own-face amplitude error is <=b^2+2b^L<=3b^2. Remote amplitude is <=[1+sqrt(2)b/(1-b)]b^(L-1)<=1.25b^(L-1). Thus the two compressed mass errors are bounded by [6+25/16]Mb_*^2<8Mb_*^2, while hybridization is <=b_*^L/a<=b_*^2/a. Replacing 3Mb_*^2 by 8Mb_*^2 leaves E2/M<.024 and gap>M/3 unchanged, uniformly in L and lateral volume. The high-gap argument uses the previously audited nu_2>=1-b, rather than the sharper L=2 identity.

A static half-space with the near covariant mass inherits the same gap. For every finitely supported vector, sufficiently long two-massed-face slabs agree exactly with the half-space operator on the vector and its one-hop neighborhood. Their uniform bound ||H_L psi||>=(M/3)||psi|| therefore passes to the half-space. Extend by density; the operator is bounded and self-adjoint at fixed a, so this is a genuine spectral gap. This limit is not an inference from low-energy spectral convergence and does not silently discard a finite-slab small eigenvalue: all L already have the same lower bound.

Absolute filled counts are no longer finite in the half-space. Any use of relative charge or Fock sectors there requires the corresponding trace-class difference/relative-index formulation. The half-space gap alone does not prove the interacting rotor interface gap or a finite Hilbert-space replacement of the bulk.
