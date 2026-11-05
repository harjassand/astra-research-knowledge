# Completed independent endpoint

## Result

Completed exact finite-experiment trajectory certification for one globally Lipschitz stationary law, with finite interpolation proof, Gram SDP and physical-rank condition, trace-bounded dual certificates, exact all-L two-step envelopes, exact contraction equilibrium balls, and positive-margin infinite-horizon completion.

## Sharp completed statement

One measured transition f(0)=-e, ||e||=1; start -e; objective <e,f(f(-e))>.

- d>=2: -1+L(1+L)/(1+2L) for 0<=L<=1/2; L^2-7/8 for L>=1/2.
- d=1: the first expression until phi=(1+sqrt(5))/2; L^2-L-1 thereafter.
- At L=1: stepwise outer relaxation gives 1, exact vector result 1/8, exact scalar result -1/3.
- Explicit maps attain every regime. Two exact sum-of-squares identities prove vector upper bounds; scalar interval optimization proves the scalar bound.

## Unlimited horizon

For 0<=L<1 and exact autonomous data, possible fixed points are exactly Apollonius-ball intersections. Linear equilibrium support is an actual-dimension SOCP. With uniform contraction radius R, robust all-time supremum lies between max(M_H,M*) and max(M_H,M*+kappa R L^(H+1)). Strict-margin safety and finite violation are decidable by increasing H and effective exact finite optimization. SDP completeness still requires rank-valid exactness; low-dimensional rank-constrained problems remain nonconvex. Weak contraction has explicit divergent horizon cost.

## Verification

All checks passed in verification_results.json. SymPy verified both SOS identities, exact L=1 rank-two Gram certificate, and completing-square equilibrium identity. Ten SDP vector cases and nine scalar attainer/grid checks agree. Positive-L vector numerical errors <=1.1e-9. L=0 numerical degeneracy yields 2.32e-7 error and optimal_inaccurate, with an independent exact constant-map proof. Controlled bounded-noise and squared-reference cases also exercised. Numerical candidates are not mislabelled formal certificates.

## Sources and overlap

Kirszbraun extension and Ryu/Taylor/Bergeling/Giselsson OSPEP are the exact existing interpolation machinery; PEPit implements the same Gram framework. This general method is NOT new. Alanwar et al. data-driven reachability and Huang et al. 2026 ForeReach are close related work. ForeReach abstract only was available; no universal dominance claim. Historical novelty of the particular sharp envelope and synthesis is unestablished. The result is a completed mathematical construction, not an evidenced civilization-scale advance.

## Files

- FIXED_LAW_CERTIFICATION.md — full theorem statements, elementary proofs, costs, comparisons, references.
- certify_fixed_law.py — generic numerical Gram builder, dual diagnostics, realization/rank check, equilibrium SOCP, tail helper, attaining maps.
- verify_results.py — independent symbolic and numerical audit.
- verification_results.json — completed evidence.

Own full question resolved. Root is selecting its separate first-event sampler as main direction. No external writes or original-file modifications performed.
