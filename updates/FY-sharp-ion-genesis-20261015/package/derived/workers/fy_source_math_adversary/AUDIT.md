# FY source mathematical audit

The incoming report does not advance the fixed-coefficient QC frontier
beyond pinned PR #99. Its explicit full-cone nonspectrahedral statement
is a valid immediate corollary of the already integrated nonexposed-ray
proof and the classical spectrahedral exposed-face theorem. It concerns
direct LMIs in the nine coefficients. A finite semidefinite lift with six
auxiliary variables is already available and remains valid.

Pin: `b32943eeb62d0d79929a9e572a344219a785ebf9`, including PR #99
at `ab5118e70a7e6a0dd39e75dd563d3a3f50b06b25` and PR #100 at the
pin itself. The source input is `R/sources/mathematical_report.txt`.
W was read only. No other new worker result was read. The incoming ZIP
was absent, so no absent producer verifier or ten-group replay is claimed.

## Exact overlap with the pinned mathematical capital

Paths below are relative to W. Full hashes and selected line ranges are
saved in `INPUT_RECEIPT.json`.

| Incoming statement | Already present at the pin | Audit conclusion |
| --- | --- | --- |
| ROC iff QC iff two PSD 2-by-2 matrices for every delta<=0 | PR #99, `updates/FW-moving-heat-observable-20261015/package/derived/workers/moving_kernel_genesis/REPORT.v0002.txt`, lines 16-95 | Same coefficient theorem, including affine backgrounds, W0^(1,4), delta=0 and the one-generator decomposition. |
| Every sharp J_r with r<-2 is QC at the acoustic floor, diffusion diag(h,1), 12-dimensional support and 4+4+2+2 blocks | PR #99, `.../workers/sharp_boundary_qc/UNIVERSAL_REPORT.txt`, lines 1-239 | Same theorem and described certificate architecture. Missing incoming arrays prevent byte or coefficient identity comparison. |
| Sharp G subtraction 9/8 and lower Jensen constant 3/1250 | PR #99, `.../workers/moving_kernel_genesis/REPORT.v0002.txt`, lines 150-204 | Same values and same 6000-fold improvement already integrated. No new optimal Jensen-constant claim. |
| Full nine-dimensional ambient extremality, nonexposure, minimal exposed face cone{J_r,j²}, both branches | PR #99, `.../workers/contact_face_priority_audit/STRUCTURAL_PROOF.txt`, lines 97-222 | Same result and dual-closure/contact proof. Independently reconstructed here. |
| Every finite alpha non-PC for r(r+2)>0 | PR #99 structural proof, lines 136-176; PR #100 `updates/FX-global-completion-axis-20261015/package/derived/root/SCIENTIFIC_SYNTHESIS.md`, lines 129-145 | PR #100 already gives the stronger r(r+2)!=0 statement and unrestricted nonsmooth/nonpolynomial minor-lift scope. |
| Positive sharp J_r, r>0, is ROC/non-PC but QC unresolved | PR #99 N867 and structural proof; retained explicitly by PR #100 | No positive sharp QC advance is supplied. |
| Full nine-coefficient K is not spectrahedral | No explicit instance of this target-cone conclusion was acquired in the inspected FW/FX proof paths | Valid newly articulated corollary of the PR #99 nonexposure theorem plus a classical theorem; not a new certificate or QC theorem. |
| Full nine-coefficient acoustic finite PSD lift | `updates/FV-positive-consequences-20261015/package/derived/workers/heat_cone_adversary_sol/ROC_CLASSIFIER.md`, lines 1-90; PR #100 original report, lines 499-515 | Existing 8-by-8 PSD block and six skew auxiliary variables. No-lift wording would contradict established capital. |

The four-dimensional shear-contact ROC cone itself has a direct two-LMI
description. Its rays can be exposed inside that face while nonexposed
in K. Confusing these two ambient spaces would invalidate the new direct-LMI
conclusion; the reconstructed proof keeps them separate.

There is a concrete certificate-level difference in the available prose:
the incoming report illustrates positivity with quadratics
`31r²+44r+21` and `31r²+54r+17`, whereas the pinned universal report's
displayed LDL pivots involve `17r²+22r+9` and `17r²+23r+8`.
The source may therefore use different certificate coefficients or a
different reduced basis. The summary does not supply those arrays,
so this audit neither validates them nor calls them byte-identical to
the earlier certificate. The exact QC theorem they would establish is
already present regardless of that representation difference.

## Independent findings

`PROOFS.md` gives universal arguments for complete contact classification,
two-contact exposed-face geometry, extremality, acoustic dual-cone
closure, nonexposure, and direct finite affine-LMI impossibility. It also
reconstructs the classical finite lift and the polyconvex cubic obstruction.
The standalone checker passes 43 exact algebra/sign checks. It reads no
producer certificate, other worker module, or discovery state.

No missing contact was found. For r<-2 both nonzero acoustic backgrounds
have positive determinant. For r>0 their determinants have opposite signs.
All mixed spatial directions have positive-definite acoustic matrices.
On the axes, the kernels are precisely span(I) and span(A_r), and A_r is
invertible on both allowed branches. Thus no nonzero singular background
can support an extra functional capable of exposing J_r.

The determinant in the incoming report uses the full acoustic matrix.
The half-acoustic matrix used in older structural proofs has determinant
`9r⁴n⁴m⁴/16`; multiplying it by two gives the incoming `9r⁴n⁴m⁴`.
This is a checked normalization difference.

An additional immediate consequence is available: K is not a closed
hyperbolicity cone in its nine coefficient variables. Renegar's classical
exposed-face theorem implies it from the same nonexposed ray. This audit
deduction does not obstruct auxiliary-variable hyperbolic or PSD lifts.

## External priority and proof boundaries

The targeted primary comparison in `PRIORITY.md` confirms that the general
heat/exact-form strategy, acoustic SOS lifting and spectrahedral-face
obstruction are established methods. Bruno-Pasqualotto's quartic theorem
has both left and right SO(2) invariance; it does not directly receive
these merely left-invariant sharp polynomials. The pinned public
`openai/math` catalogue has no acquired theorem for this exact K or its
QC boundary. Its unrelated hyperbolicity entries supply no such transfer.
These are receiving-hypothesis and acquisition findings. Historical
priority for the exact family or target-cone corollary remains UNKNOWN.

The report's negative-branch QC theorem is inherited capital in this
audit. The full heat identity and analytic endpoint argument were not
rerun here. The universal dual and LMI arguments in `PROOFS.md` and the
finite exact algebra receipt have their stated scopes; neither is
independent external correctness certification, historical-first
evidence, a planar Morrey resolution, or a physical capability result.
