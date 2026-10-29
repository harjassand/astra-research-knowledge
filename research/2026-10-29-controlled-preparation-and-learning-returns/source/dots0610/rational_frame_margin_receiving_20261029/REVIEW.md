# Independent receiving review of exact-rational confidence margins
2026-10-29. ACCEPTED at stated mathematical/statistical scope.

I authored the preceding matrix-confidence theorem, but not this rational arithmetic construction. I inspected the new proof and checker separately and reran an unchanged copy with single-threaded BLAS. All exact rational assertions passed. Original files were not overwritten. Floating SVD proposal residual diagnostics can differ across BLAS settings; the exact verified margins and confidence conclusions agree. This is not a byte-identical floating-output claim.

## Load-bearing checks
1. Exact e=23/200 and ell=3657/500 satisfy the tail exponent inequality. A finite positive Taylor sum certifies exp(ell)>1500; the three-edge union factor75 therefore gives failure probability<1/20.
2. The checker reads only integer `sums` and zero/one `Jembed` for the certificate. True frames, source coefficients, bath moments and bath state are not used. Source arrays are allowed to contain diagnostics, but those keys are not accessed.
3. B=A^T A is rational from the acquired sums. Q and proposed squared singular values are exact binary-float rationals in the verifier. Symmetric row norms bound Gram and diagonalization spectral defects. Because the proposed smallest eigenvalue exceeds the residual, generalized Courant-Fischer gives the stated positive ordered eigenvalue bounds; the denominator signs are correct.
4. The residual bound and gap>0.1 put the proposed minimum eigenvector within the conservatively declared1e-8 distance of a signed exact unit minimum eigenvector. Normalization error is covered. No exactness of floating SVD is assumed.
5. Exact positive determinant plus Gram defect<1e-12 places the rational candidate within1e-10 of its exact proper polar factor. The sqrt3 bracket and sign-dependent cross-term bound give the advertised0.0600 distance bound.
6. The singular cone uses only s1>=0 and e/s2_lower. Exact squaring proves h<0.35. The wrong SO3 branch is excluded using the exact distance2 between -R and SO3 for any R in SO3. Triangle inequalities then yield frame error<0.667.

## Accepted result
On the same simultaneous95% concentration event, conditional on the original common-kernel promise and ideal trusted acquisition boundary, the observed occupation gaps exceed0.2222,0.2358,0.2291; the proper rotation chosen by the verified polar construction is within Frobenius distance0.667 of each true relative frame. The exact rational result is a conservative replacement for floating numerical margins, not a new physical acquisition or an exact estimate of unknown parameters.

The proper target rotation is the exact polar factor of the rational candidate produced and checked by this run. It is not a hardware pulse certificate. The current output summary does not serialize every rational candidate entry; the checker reproduces and verifies a candidate. Persisting those entries would help future control compilation but is not required for this algorithmic existence/certification statement. Different numerical proposal software must pass the same exact verifier, not merely reuse this receipt.

No generic noise-model certification, future stationarity, small uniform-horizon recovery error, independent laboratory validation, or hardware advantage is accepted. Imperfect-SPAM use must follow the larger increment and bias allowances in the governing matrix-confidence theorem; this arithmetic instance verifies its ideal-boundary e=.115 case only.
