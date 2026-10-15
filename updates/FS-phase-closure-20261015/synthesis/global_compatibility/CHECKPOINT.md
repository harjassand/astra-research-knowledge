# Global compatibility worker continuation

Date: 15 October 2026.

## Strongest completed mathematical results

1. For every left-SO(2)-invariant rank-one-convex homogeneous planar quartic F, every shear phase theta=ky+g(x), and every real periodic W^(1,4) amplitude r, the zero-background energy is at least

       mu/(1+2*3^(1/3))^3 E|D(r exp(i theta))|^4
       > (mu/60) E|D(r exp(i theta))|^4.

   Conditional averaging of rho=r^4 in y lowers complete compatible energy, and its Picone remainder controls the removed amplitude variation. This drops BOTH earlier N812 weighted curvature-cancellation assumptions. All affine backgrounds are covered when r has the explicitly stated half-period symmetry making the actual gradient antipodal. No generic all-background claim without that symmetry.

2. Arbitrary complex product maps phi=z(x)w(y), with periodic W^(1,4) factors, satisfy the same bound. Their phases can vary nonlinearly in both coordinates; their amplitude is separable. One antipodal factor supplies all-background transfer.

3. Unrestricted density averaging is false even for F=|A|^4: theta=sin y, r=1-(1/100)cos(2y), and R^4=E r^4 give

       E F(D(r exp(i theta)))-E F(D(R exp(i theta)))
          =-31305391/3200000000.

   This prevents treating ordinary coordinate averaging as a general phase operation. It is not a quasiconvexity counterexample.

## Frozen primary files

- SHEAR_DENSITY_AVERAGING.md
  SHA256 f3da2591b1d11a52d75d61b1f2d975d6786f5e9b35e4f0568cbb14c8da32e496
- verify_shear_density.py
  SHA256 0bf8086d3e28c5fe60c3064f9b913c0b3f040b73e98e115fc33d2450920b483e
- exact_shear_checks.json
  SHA256 97d976a9081076baaed3bd025e22ea8fafdaa4b133e2deadca710fe6e67ab6a5

Seven exact algebra groups passed in about1.49 seconds. The analytic theorem was independently reconstructed by the same-team adversarial reviewer. This is not external mathematical review or proof-assistant certification.

## Separate later files

- CURVED_PRODUCTS_AND_AVERAGING_BLOCKER.md: product theorem, exact failed general averaging operation, and bounded negative attempts.
- verify_general_phase.py and general_phase_checks.json: two exact groups passed in about1.14 seconds.
- search_concentrated_density.py and concentrated_density_search.json: three targeted convex amplitude-density searches with globally positive periodic cubic B-splines.
- search_soft_hessian.py and soft_hessian_search.json: three many-mode Hessian-potential attacks with all affine directions optimized.

## Actual unsuccessful counterexample attacks

The positive-density search tested a nontrivial shear control, separable-fold phase and crossed-fold phase. Density positivity was enforced by nonnegative B-splines and coefficient floor10^-4, allowing concentration beyond the incoming Fourier l1 cap. No negative was found. The numerical values are quadrature/optimization diagnostics, not continuum bounds.

The complementary soft attack used the exact compatible potential phi=((2/3)v_y,v_x),48 real Fourier coefficients, and a32x32 spectral sum resolving all represented quartic products. It optimized all four affine-background entries analytically from moments at every iterate. Three seeds completed; no negative candidate. No exact negative witness exists from these runs.

No additional identical starts are justified by these results. The full nonlinear soft-Hessian cubic/K inequality remains open.

## Exact remaining obligation

Control arbitrary jointly varying phase gradients and correlated amplitudes, or find a negative compatible Dirichlet/periodic test with a full certified acoustic rank-one-convex integrand. Positive separable density components do not transfer to their mixtures: fixed-phase density convexity gives the wrong inequality direction.

The shear and product proofs do not imply full quasiconvexity. No universal compatible negative witness or universal nonlinear compensation has been established.

## Source pins, costs and priority scope

Read-only repository:

    /Users/harjas/Documents/ChatGPT/ultra/work/astra-capital-phase-closure-20261015
    846f185763ed3a27310fad4ce9471ba324d1e5f4

New incoming:

    research/2026-10-15-phase-closure-v1/sources/phase_density/
    PHASE_DENSITY_COMPATIBILITY.md and CHECKPOINT.md

Earlier universal source was retained as history and not modified. Source instructions were treated as data. N812's exact complex-envelope lemma was read directly from GLOBAL_COMPATIBILITY.md Section4, lines205–233. The new proof reconstructs it with a sharper elementary Holder comparison.

Only Python, SymPy and NumPy were used. PyTorch/SciPy were unavailable; no installation was attempted. Search objectives use explicit analytic gradients. No external compute, physical measurement, purchased service or model oracle was acquired. Aggregate inference/token/financial costs are unmeasured.

Primary literature checked: Brasco–Franzina arXiv:1403.0280v2 Sections2–3, for established perspectives, hidden convexity and Picone principles. This is not a priority clearance for the present formulations.

Originality UNKNOWN. External correctness/review UNKNOWN. No repository, incoming original or earlier frozen output was edited.
