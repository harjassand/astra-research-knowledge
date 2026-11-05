BOUNDED CONVEX RELAXATION: CONSTRUCTION, PROOFS AND FAILED CLAIMS
Research record, 5 November 2026

STATUS

This record contains completed mathematics for a declared classical planar
linear diffusion model. It is not an experimental demonstration, a new
microscopic law, or a completed civilisation-changing capability. The initial
energy-order and holonomy primitive novelty claims were defeated by direct
primary literature. The surviving results are exact constructive deductions
within established geometry and Langevin dynamics. Priority of the combined
deductions has not been established by an exhaustive literature review.

MAIN OPERATION

dX=-A(t)X dt+sqrt(2D)dW, symmetric 0<=A(t)<=Lambda I, D,Lambda>0.
The control is chosen independently of the unknown input and bath trajectory.
The target is the full input-independent response X_T=F X_0+eta, with a fixed
real 2-by-2 F, not only the final marginal for one chosen input distribution.

For det F>0, set s=-log(det F)/2, N=exp(s)F and d equal to the established
SL2 symmetric-traceless horizontal distance to N. The record evaluates d by
explicit monotone scalar roots. Reachability is exactly s>=d; minimum time
is (s+d)/Lambda. Singular and negative-determinant targets are unreachable
at finite bounded-control time.

Among every minimum-time realization, traverse a shortest shape at maximal
rank-one damping first, then put all surplus isotropic damping last. The
result simultaneously minimizes every radial thermal-error tail. Multiple
shortest shapes have orthogonally conjugate optimal covariances. Independent
preselected randomization cannot improve the radial law. At initial and final
trap A=Lambda I, counted net expected potential work is exactly 2kBT*d.
This is not a minimum-work theorem or a wall-plug energy price.

For F=exp(-s)R_theta, d=L_theta=sqrt(theta^2+2*pi*abs(theta)), with principal
abs(theta)<=pi. At s=L, the fastest operation is radial-error optimal even
when longer durations are allowed. For every nonzero theta and s>L, a smooth
admissible loop perturbation lowers mean-square noise to first order while
time and net work increase only to second order. Thus no finite linear time
and net-work penalties make the fastest point minimize a positive weighted
noise objective. It remains Pareto efficient; the slower-time optimum is not
solved and not every radial tail is proved to improve.

FINITE-STAGE COMPANION

For at most N constant symmetric positive-control stages implementing
exp(-s)R_theta, 0<abs(theta)<=pi, define

  s_N=N*acosh(cos(pi/N)/cos((pi+abs(theta))/N)).

Reachability is exactly N>2+2*abs(theta)/pi and s>=s_N. Minimum time is
(s+s_N)/Lambda; optimal worst positive-factor condition number is
exp(2*s_N/N). The construction and global proof include winding and
self-intersections. For theta=pi and N=5, the sharp condition number is
25.37700210714847. The known 2026 factorization paper already supplies
the organizing holonomy framework and minimum factor counts.

WHERE THE COMPLETE PROOFS ARE

invention_variation/proof_and_claim_boundary.txt
  General target distance computation, explicit controls, thermal ordering,
  endpoint error law, work accounting, and scope.
invention_geometry/finite_stage_rotation.txt
  Finite-stage global bound, convexification lemma, exact factor construction.
invention_variation/slower_loop_derivation.txt
  Explicit admissible deformation and all-angle first-variation proof.
invention_holonomy_audit/audit.txt
  Independent proof audit, corrections, randomization, cut locus, work,
  first-variation audit, and additional scoped noise-law construction.
invention_root/resource_deductions.txt
  Input stored-energy, reset, and dimension-independent necessary bounds.
invention_root/source_audit.txt
  Primary-literature comparisons and actual measured constraints.
invention_root/primitive_log.txt
  Original candidates before literature, failed novelty, and revisions.

REPRODUCE

Requires Python with numpy, scipy, matplotlib and mpmath. No accelerator,
atomistic simulator, fitted endpoint, paid service or new experiment is used.
From the unpacked record directory:

  python invention_variation/gradient_rotation.py
  python invention_holonomy_audit/check.py
  python invention_holonomy_audit/variation_check.py
  python invention_geometry/verify_finite_stage.py
  python invention_variation/slower_loop_counterexample.py
  python invention_root/compile_planar_response.py

The compiler accepts --input request.json and optional --output result.json.
Example request:
  {"target":[[0,-0.029825028198888534],[0.029825028198888534,0]],
   "cap":1.0,"diffusion":1.0,"confidence":0.95}
The output gives actual ideal control-stage durations, rotation rates,
covariance, a radial error quantile, work, and floating residuals. It is not
a laboratory control program. Numerical residuals are not interval enclosures.

BOUNDARIES THAT MATTER

The theorem permits ideal parameter switches and PSD stiffness with a zero
eigenvalue. It does not price finite slew, actuator bandwidth, power, input
preparation, readout, signal amplification, or complete hardware reset.
There is no adaptive feedback, anisotropic bath, hydrodynamic memory, inertia,
unknown force calibration or nonlinear-noise claim. Generic orientation
randomization does not preserve a generic target F; the isotropic-covariance
coin construction is confined to rotation targets and gives a Gaussian mixture.

The severe rotation attenuation is a planar whole-map bound. It must not be
assumed to survive extra initialized coordinates or changing access resources.
The separate dimension-independent necessary bounds are stated at their own
scope. All plotted curves are exact-model evaluations, not empirical evidence.

PRESERVATION

Earlier materials, selection and reflection records were not edited. Hashes
and comparison results appear in invention_root/preserved_records.json.
The failed frozen-law materials specimen was not refitted. Full earlier
archives remain separate; they are not duplicated in this record.

Copyrighted primary papers and full extracted texts are omitted. Acquisition
URLs and hashes are retained. All included explanatory text and code are the
current research construction, with old mathematics explicitly attributed.
