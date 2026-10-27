# A uniform, nonexplicit relative-output spectral collar at peak 3/2

27 October 2026. A compactness consequence of exact rigidity plus the independently received explicit entropy tube. No numerical value for the spectral threshold is asserted.

There exists a universal η>0 with the following property. Let X≥0 be a nonzero source on C3⊗C3 with faithful τ=EX and X≤(3/2)τ. If

λ_min[τ^(−1/2)N(X)τ^(−1/2)]≤η,

then

Δ(X)≥(157/180000)TrX>0.                         (1)

The constant η does not depend on the condition number of τ. The theorem only concerns three-dimensional retained reference support; it does not assert a dimension-uniform collar for arbitrary references.

## Compact source geometry

Let C={Y:0≤Y≤(3/2)I9, EY=I9}. This is a compact finite-dimensional set. Let Z be the compact family of all locally rotated (3/2)P_sym. The exact deficient-kernel exclusion plus full-Schmidt rigidity show

{Y∈C : λ_min(NY)=0}=Z.

Indeed every kernel vector must have Schmidt rank three; the full-Schmidt theorem with marginal I forces its Schmidt coefficients to be equal and forces Y to have the stated symmetric-projector form. Conversely every member of Z has a zero output eigenvalue.

Set δ=1/10000. The subset

C_δ={Y∈C : dist_operator_norm(Y,Z)≥δ}

is compact and contains no zero-output source. It is nonempty, for example Y=I has distance at least1 from Z because every member of Z has a zero eigenvalue. Consequently

η=(1/2)min_{Y∈C_δ} λ_min(NY)>0                   (2)

is a well-defined universal positive number. Equation (2) is a rigorous variational definition, not a computed certificate of its magnitude. If λ_min(NY)≤η, then dist(Y,Z)<δ.

## Return to the actual source, without whitening entropy

Write τ=I3⊗T, T>0, F=I3⊗sqrt T and Y=F^(−1)XF^(−1). Then Y∈C, and N commutes with this reference-only congruence, so its output is exactly the relative output in the hypothesis. Choose Y0∈Z with ||Y−Y0||<δ and define X0=FY0F. Both X and X0 have the same actual marginal τ and hence the same trace t=Trτ=TrF². The ordinary Schatten inequality gives

||X−X0||_1≤||Y−Y0|| TrF²<δt.

Therefore their normalized trace distance is less than δ/2=1/20000. The source X0 is a locally rotated reference-filtered symmetric projector; rotations preserve the low-Schmidt spectral receiver and its normalized margin1/288. The independently received explicit entropy tube in low_schmidt_spectral_quantitative_gap_and_boundary_tube.md now gives (1).

At no point is Δ(X) replaced by Δ(Y). Reference whitening is used only for compact source classification and a trace-distance estimate. The entropy comparison occurs between the original normalized X and X0, with the same actual marginal. This distinction makes the conclusion uniform even when T becomes arbitrarily ill-conditioned.

## What this does and does not close

This supplies a source-native spectral neighborhood of the entire singular-output boundary. Any negative source in the peak3/2 region with faithful 3-dimensional marginal must have its relative output bounded below by ηI. No explicit η, all-peak3/2 VALUE theorem, or quantitative approximate-rigidity rate is claimed. Producing a useful explicit value of η remains a separate task.
