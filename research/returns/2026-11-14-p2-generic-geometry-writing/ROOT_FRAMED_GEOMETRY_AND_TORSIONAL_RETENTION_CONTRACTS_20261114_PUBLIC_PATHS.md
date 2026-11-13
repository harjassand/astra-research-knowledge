FRAMED GEOMETRY, CURVED LOAD PATHS AND TORSIONAL RETENTION
ROOT independent mechanics/source contracts --14 November2026Brisbane/13NovemberUTC.
All material values and numerical design points below are INTRODUCED. No apparatus, prepared structural material, sensor, physical experiment, manufacturing result or cost advantage is supplied. This extends a physical geometry-writing contract; the rod framework itself is established prior work.

OWN executable artifact:
ROOT_FRAMED_GEOMETRY_AND_CURVED_LOAD_PATH_SCREEN_20261114.py
12094 ASCII bytes; SHA256 601f8e5889b2bbf90a349bc90b0b42221845e0b37e9ab1ecdf71af338d4620b2.
OWN generated output:
ROOT_FRAMED_GEOMETRY_AND_CURVED_LOAD_PATH_SCREEN_20261114.json
93161 ASCII bytes; SHA256 c42150d9bb8d66aebf2d28158db6e709ce312c11e25dfa65e8ecc422295c8706.
Both are under research/returns/2026-11-14-p2-generic-geometry-writing/.
Execution uses existing NumPy only, serially with numerical-library thread counts one. No installation, producer-code execution, external compute or physical experiment.

1. Actual distinct governing source and its limits.

Gazzola, Dudte, McCormick and Mahadevan2018, Forward and inverse problems in the mechanics of soft filaments, DOI10.1098/rsos.171628:
https://www.cosseratrods.org/publications/pubs/2018_RSOS.pdf
Dependent local identity/alias/hold checks across README, COORDINATION_EXPERIMENTS, ALLOCATION and the working note completed before first navigation. Actual main lines0--363/pp0--5 were read, including Sections2.1--2.2, Table1 and equations2.1--2.14's opening. This is a successful source exposure, not recovery of any earlier held identity. No follow-up failed or hold released.
The source supplies material frames, intrinsic curvature/twist and shear/stretch, force/moment balance and local linear constitutive laws. Its main formulation assumes slender rods and diagonal rigidities, with circular sections for the displayed material/geometric specialization. Its stretch-dependent rescaling assumes incompressibility and circular cross sections; later text sets intrinsic strains zero to simplify the notation, after explicitly allowing them.
This is established rod mechanics, not a physical state writer, a qualified rectangular dynamic network, a claim of long-term constitutive accuracy, or a whole-class stability theorem for an introduced structure. Later main, benchmarks, appendix, figures, linked software, SI and cited originals were not read/followed/executed. The independent construction below states its own hypotheses and does not import unread validation.

2. The physical geometric state is a framed curve, not two additive angles.

Let s be reference arclength, r(s) the centerline and R(s) in SO(3) map material vectors into the world. This R is the transpose of Q in the source. Under exact inextensibility and unshearability,
r'=R e3, R'=R hat(kappa), kappa=(kappa1,kappa2,kappa3).
The zero commanded local twist condition kappa3=0 does not imply zero final rotation about a fixed world axis. Nor does integral kappa1=integral kappa2=0 imply the final frame is the root frame. Sequential rotations about transported material axes do not commute.

For a constant curvature vector on a zone of length h, put K=hat(kappa), q=|kappa| and theta=q h. The exact update is
R_new=R[Id+sin(theta)K/q+(1-cos(theta))K^2/q^2],
r_new=r+R[h Id+(1-cos(theta))K/q^2+(theta-sin(theta))K^2/q^3] e3.
At q=0 use R_new=R and r_new=r+h R e3. These are known rigid-motion exponential identities, used here for a concrete physical programming diagnostic; no new integration algorithm is claimed.

Use ten50mm zones. The explicit program is:
(2,0),(2,0),(0,2),(0,2),(-2,0),(-2,0),(0,-2),(0,-2),(0,0),(0,0), all in per metre.
Both integrated material bending components are exactly zero and local intrinsic twist is zero everywhere. Its final frame differs from the root by2.28423974degrees. Reversing the order preserves both component integrals but changes the endpoint by111.109441mm and the final frame by4.52316551degrees.
These are distinct requested shapes. They are not errors of an implemented controller or evidence that the shape class fails. They show that total differential feed or two cumulative angle registers alone do not identify this3D state. The finite global rotation is geometric frame holonomy, not a hidden imposed local twist. Material-frame definition, physical phase/orientation registration and ordered local operations remain part of a real writer.

3. A full ideal centerline geometry bound, with exact limited scope.

For the ten-zone class with each bending component in {-2,0,+2}/m and kappa3=0, there are9^10=3486784401 ideal programs. The unit tangent's spherical path length from its root direction is at most integral|kappa_perp|ds <=sqrt(8)*0.5=1.414213562rad, strictly below pi/2.
Consequently r'(s).t_root >=cos(sqrt(8)*0.5)=0.155943695>0. Root-axis projection is strictly increasing, so every such IDEAL centerline is injective and cannot cross itself. The same tangent-cone argument applies to a physical smoothing of transitions IF its actual curvature magnitude remains within sqrt(8)/m and the stated arclength remains valid.
This removes one ideal centerline self-intersection concern for this exact class; it does not construct the shapes. It does not certify finite-thickness solid nonintersection, local transitions, cross-section warping, supports, root attachment, moving writer/tool/cables or load-deformed geometry. A positive graph projection is not a swept-volume or access certificate.

4. Curvature writing and structural load retention require distinct tensor properties.

For a stress-free assigned reference curve, take positive local bending/twist matrix B=diag(B1,B2,C), and shear/stretch matrix S. The first variations use spatial infinitesimal rotation phi and material curvature increment delta_kappa:
phi(s)=integral_0^s R(u) delta_kappa(u)du,
delta_r(L)=integral_0^L -hat(r(L)-r(s)) R(s) delta_kappa(s)ds.
Define H(s) as the6x3 vertical stack [-hat(r(L)-r(s))R(s);R(s)]. For a small dead tip wrench w=(F,M), the incremental tip compliance is
C_tip=integral H B^-1 H^T ds,
with an additional translational block integral R S^-1 R^T ds for shear/stretch.
This follows directly from virtual work and the stated local quadratic energy. It is a first-order compliance about the assigned stress-free framed curve, not a nonlinear stability, fracture, contact or viscoelastic lifetime certificate.

For a uniform world body-force density f, q(s)=integral_s^L[r(u)-r(s)]du and the reference bending moment is q(s) cross f. The load contribution is integral H B^-1 R^T(q cross f)ds plus the direct shear/stretch response to f(L-s).
A transverse tip force on a curved body can generate local torsional moment, even when its intrinsic twist is zero and its centerline is planar. A straight transverse-bending test does not identify C, and a large bending-stiffness ratio does not supply torsional retention.

INTRODUCED point: length0.5m,40x35mm section, density1200kg/m^3, mass0.84kg, E500MPa. B1=71.4583333Nm^2 and B2=93.3333333Nm^2 are the elementary rectangle bending values for that hypothetical E. Effective torsional C=40Nm^2 and S=(200000,200000,700000)N are separately introduced; they are not established by that E or by the source's circular specialization. Gravity is uniform(0,-16.4808,0)N/m, root tangent initially world z. Tip force has magnitude<=10N; no tip moment.

The serial finite collection has75 programs: straight, the ordered and reversed program above, eight nonzero uniform choices and64 fixed pseudo-random ten-zone programs. It is not a probability sample, an exhaustive class verification or a manufacturing campaign.
At each curve, the translational upper bound used is10*lambda_max(C_tip,rr)+|delta_r_gravity|. The rotation upper bound is10*sigma_max(C_tip,thetaF)+|phi_gravity|. The reported particular force is one admissible direction chosen from the leading translational eigenvector with its sign aligned to gravity; it need not maximize the full six-coordinate response.
The largest finite nominal translation upper bound is8.03887350mm, at uniform material curvature(0,-2)/m, with rotation upper1.38469467degrees. Those finite results do not establish the full3.486billion-program service endpoint or any physical operation.
A simple uniform-in-geometry sufficient translational estimate using min(B1,B2,C)=40Nm^2, |r(L)-r(s)|<=L-s, and min(S)=200000N is
[10 L^3/3+|f| L^4/8]/40 +[10 L+|f| L^2/2]/200000
=13.6708734mm.
This bound exceeding10mm removes that particular sufficient certificate; it does NOT prove actual failure or impossibility. More geometry-specific analysis or different physical rigidities may improve it.

5. Independent finite nonlinear equilibrium checks.

For four introduced settings, a separate inextensible/unshearable static shooting calculation integrates
r'=R e3,
R'=R hat(kappa0+B^-1 R^T m),
n(s)=F+f(L-s),
m'=-(R e3) cross n,
with the fixed root frame and terminal m(L)=0.
Quaternion RK4 integration uses10 and20 substeps per50mm zone; finite Newton solves the three initial moment components. This is an independently implemented finite equilibrium diagnostic, not source code, a stability solver, proof of uniqueness, a continuum error bound or an installed measurement. Nonlinear checks OMIT the introduced shear/stretch compliance included in the linear calculations, so the small difference between the two outputs is not a pure nonlinear correction.

With C=40Nm^2:
straight gives7.63134584mm/1.277332degrees;
the noncommuting program gives7.56664355mm/1.274648degrees;
uniform(0,-2)/m gives8.00168629mm/1.379758degrees.
Terminal moment residual norms are at most5.9e-10Nm in these checks. Refining the integration changes the shown displacements by at most8.1e-10mm; that agreement alone is not a physical or rigorous continuum error bound.

Now change ONLY introduced torsional C from40 to4Nm^2, keeping both bending rigidities and all loads unchanged. The straight transverse test remains identical. The same uniform(0,-2)/m curved setting has linear particular23.4343386mm/6.929326degrees and nonlinear equilibrium23.2868569mm/6.891268degrees, with terminal moment residual about1.5e-14Nm. Refinement changes its displacement7.55e-9mm.
This is a scoped example of the missing torsional property changing the modeled useful function while a straight bend test stays unchanged. It is not a claim that any actual material has those properties, that this is the only equilibrium, that it is stable, or that an actual device fails.
The C0.4Nm^2 first-variation outputs enter large rotations and are explicitly flagged outside the introduced0.1rad small-rotation screen; do not treat their large linear numbers as actual finite-deformation measurements.

6. Checks, physical operations still needed and compatibility limits.

The output retains every finite program, force direction and computed limit. Compliance matrices are numerically symmetric positive definite. The straight analytic bending-plus-shear prediction7.66804102mm agrees with the finer quadrature7.66804840mm within7.4e-6mm. The difference from the earlier7.63274mm straight bending screen is the now explicit introduced transverse-shear term, plus the stated quadrature resolution; there is no revised qualified material claim.
All4shooting settings converge at the recorded finite scope and were compared across two resolutions. Only the OWN bounded model was executed. No accepted proof or producer result was re-executed.

The new useful contract is an ORDERED FRAMED intrinsic geometry with both bending and torsional response, not just scalar programmed curvature or a high bending ratio. Actual local write/relock operations need to retain the material register and cross-sectional phase, support loads during changes, and leave compatible bending/torsional/creep properties after temporary supports withdraw. Real observations must distinguish geometric shape from local constitutive state; the simulation knows both by construction, which is not a sensor.

No installed force/orientation accuracy, same-body repeated writing, reaction or thermal map, load-bearing lock, actuator-free holding, nonlinear stability, permanent stock renewal, useful cycle count, manufacturing yield or whole-cost advantage follows. Full finite-thickness access, material transitions and mechanics after wear remain open physical operations.
The source and independent kinematic/compliance identities are reusable analysis tools. They do not establish a new rod theory, a qualified invention, a general impossibility, or permission for an experiment.

