# Selected governing proofs, completed reviews and acquisition contract

Only the ten coordinator-named text members of the newly supplied archive are included. The original ZIP remains unchanged; no producer program is executed and no other member content is read.

## fluid_energy_basin_v1/README.md

# One fixed actuator: a certified three-dimensional energy-space performance basin

## Result in one paragraph

For the native controlled Navier–Stokes model on the unit three-torus at viscosity 0.001, one prescribed shear pulse of duration 4.2 and nominal peak 128 reduces the L2 velocity norm by a factor below 1/3 for **every Leray–Hopf solution** from a specified full three-dimensional L2 ball. Every no-control solution from the same initial ball retains more than half its initial norm at the same time. The ball has relative radius 20 percent around 0.01 e3 cos(2 pi x2), admits arbitrary three-dimensional perturbations, and is independent of the unknown allowed static calibration.

This is a complete, narrow quantitative performance certificate, not a proof of general three-dimensional regularity. It is packaged because the exact infinite-mode linear witness, nonlinear energy argument, same-input baseline, and independent source review form one auditable result. No novelty or laboratory feasibility is claimed.

## Read first: what is NOT claimed

- No uniqueness, absence of singularities, or global strong-solution theorem for arbitrary data in the ball.
- No solution of a full H3-ball stabilization problem.
- No nonlinear simulation, PDE trajectory computation, hardware run, or acquired laboratory calibration.
- No empirical validation of the prescribed transport model, periodic geometry, viscosity, preparation error, or readout contract.
- No new general Reynolds–Orr energy-stability principle. The contribution is the explicit composition and finite-parameter certificate.

The theorem bounds every energy-admissible realization despite possible nonuniqueness. If a claim requires a uniquely selected smooth physical trajectory throughout the intervention, that stronger requirement remains open here.

## The model and scope

The equation is

    u_t = 0.001 Delta u - P div(u tensor u) + P[(b dot grad)u].

The controller is prescribed TRANSPORT. A model also containing (u dot grad)b is different and is not covered. The initial field is real, mean-zero, divergence free, and within L2 distance 1/(500 sqrt(2)) of the fixed center. Control gain and transverse-direction errors are static and bounded by 1/1024; phase is arbitrary and static. The full exact contract is in PROOF.md.

The same theorem gives a low Fourier-score contrast greater than 27/80. ACQUISITION.md describes a prospective finite-bit, finite-variance volume-average readout. Its 43,200 observations are conditional on explicit unacquired preparation and sensor contracts; they are not completed experiment counts. Grid point samples alone are insufficient for arbitrary L2 fields.

## Reading order

1. PROOF.md: governing nonlinear theorem and all weak-solution quantifiers.
2. FREE_FIBER_CERTIFICATE.md: direct scalar Fourier reduction and exact infinite-tail certificate actually used.
3. reviews/NONLINEAR_REVIEW.md: coordinated independent analytical challenge, with limitations.
4. ACQUISITION.md: observable, error budgets, statistics, and physical costs.
5. reviews/LINEAR_REVIEW.md: source challenge of the inherited exact linear certificate.
6. reviews/ACQUISITION_REVIEW.md: narrow analytical check of the prospective instrument and statistical contract.
7. negative_wrapper/: a preserved failed generic nonlinear route, with all 650 diagonal values and its exact receipt.

The older complete linear packet is under linear_certificate/. It contains exact integer metrics and congruences, original source and execution receipts, and the failed higher-sector floating bounds. The broader historical three-actuator theorem is not being relabeled as a one-actuator full-space contraction. Only one free scalar channel is required for the new result.

## Verification

The new read-only entry point is:

    python3 verify_one_channel.py

It requires only the Python standard library. It reconstructs the six saved rational matrices needed by the new theorem, checks their integer congruence certificates, and recounts scalar reserves. It does not solve an optimization problem, fit parameters, perform a PDE calculation, or modify files. Exact operations and the separately recorded replay status are described in REPLAY_STATUS.md.

To check the delivered file integrity:

    python3 verify_manifest.py

The historical script linear_certificate/qualify_saved_exact.py is a PRODUCING script. It uses NumPy/SciPy to propose congruence coordinates and writes output files. It is included for provenance but is not required to verify this packet. If exploring that historical process, work on a copy; do not confuse regenerated witnesses with the frozen delivered ones.

## Honest resource summary

One actuator block: duration 4.2, nominal scalar peak 128, calibrated vector peak below 129, nominal slew at most 2400, scalar action 524.8, integrated squared command at most 68812.8. All are nondimensional quantities of the model. The actuator peak is about 12,800 times the initial center amplitude. The packet does not convert these values to seconds, power, cost, or feasible hardware tolerances.

Historical producing operations: one floating screen, including failures, and one exact saved-witness pass. Their receipts are preserved. The new analytic nonlinear theorem required no nonlinear propagation. The standalone read-only replay is separately labeled and is not an independent mathematical audit.

## Primary context

Energy-space stability of symmetric viscous flows and Reynolds–Orr energy estimates are established prior. The packet derives the extra prescribed-skew-drift cancellation and amplitude-only bound explicitly rather than importing an unforced theorem outside its scope.

- Bardos et al., “Stability of two-dimensional viscous incompressible flows under three-dimensional perturbations and inviscid symmetry breaking,” arXiv:1201.2742v2: https://arxiv.org/html/1201.2742v2
- Waleffe, GFD 2011 lecture on nonlinear shear-flow stability: https://people.math.wisc.edu/~fwaleffe/GFD2011lectures/GFD3.pdf

The reviews are coordinated analytical checks, not blind discovery, external expert certification, proof-assistant verification, or independent PDE experiments. Source hashes and delivery-copy editorial changes are recorded in SOURCE_MAP.json. All scientific witness bytes are retained unchanged.

## fluid_energy_basin_v1/PROOF.md

# A finite-parameter three-dimensional energy-space performance basin

2026-11-09. Author analytic construction. No new PDE propagation, spectral solve, parameter search, or saved-matrix rerun. This result concerns every Leray–Hopf solution. It does not prove regularity or uniqueness of general three-dimensional solutions during the intervention.

## 1. Governing equation, fixed command, and exact claim

Use normalized Lebesgue measure on the unit torus T^3, and the native equation

    partial_t u = nu Delta u - P div(u tensor u) + P[(b dot grad)u],
    div u = 0, mean u = 0, nu = 1/1000.

Here P is the orthogonal Leray projection. The prescribed drift is the FIRST block of the already certified linear command, not the whole three-block word:

    b(t,x) = f(t) theta (e2 + e) sin(2 pi x1 + phi),
    e dot e1 = 0, |e| <= 1/1024,
    theta in [1-1/1024, 1+1/1024].

The phase phi, gain theta, and transverse error e are arbitrary but static during this block. The scalar command rises from zero to 128 by the original quintic smoothstep in time 1/10, is constant for 4 units, and falls to zero by the reverse smoothstep in time 1/10. After T=21/5=4.2 it is zero. No feedback, identification, or intermediate pinching/reset is used.

Set

    a = 1/100,
    U0(x) = a e3 cos(2 pi x2),
    M = ||U0||2 = a/sqrt(2),
    B = {u0: real, mean-zero, divergence-free L2;
               ||u0-U0||2 <= M/5}.

For every u0 in B and every admitted calibration:

1. Every controlled Leray–Hopf solution satisfies

       ||u(T)||2 <= (21/64)||u0||2 < (1/3)||u0||2.

2. Every uncontrolled Leray–Hopf solution from the SAME u0 satisfies

       ||u_free(T)||2 > (1/2)||u0||2.

Thus a full three-dimensional L2 ball, with relative radius 20 percent and absolute radius 1/(500 sqrt(2)), has a strict matched on/off performance separation. The open interior is included; the estimates also cover its closed boundary. There is no restriction on perturbation Fourier support, H3 norm, or dependence on x3. Smooth perturbations are allowed but are not presumed to remain smooth.

The basin is not an exponentially small H3 neighborhood. It is also not a strong-solution basin or a proof of the earlier arbitrary-H3-ball stabilization target.

## 2. The exact scalar center and inherited linear certificate

Under the prescribed drift, U(t)=e3 w(t,x1,x2) is an exact globally smooth solution of the FULL native equation. Indeed U dot grad U is zero, the scalar is independent of x3, the calibrated vertical drift multiplies partial_3=0, and the scalar evolution is

    partial_t w = nu Delta_h w + b_h dot grad_h w.

This field remains divergence free, so Leray is the identity on its right-hand side. The scalar maximum principle yields

    ||w(t)||infinity <= a = 1/100                  (1)

for all time, independently of the drift amplitude, direction error, and static phase.

The initial scalar belongs to the two conjugate transverse fibers k2=+/-1, k3=0, hence m=|xi|^2=1 and dominant coordinate |k2|=1. The saved free-polarization certificate in CERTIFIED_LINEAR_THEOREM.md covers the full longitudinal fiber, not just its initial n=0 mode. It gives plateau operator norm at most 1/16 after four units. Both ramps preserve these fibers and are L2 contractions. Therefore

    ||U(T)||2 <= M/16.                            (2)

This uses only the two real conjugate copies of the already checked (m,k)=(1,1) free channel. It does not claim a full-space contraction for one actuator. Its untouched-axis linear operator norm still equals the no-driver norm.

For b=0 the corresponding exact center is

    U_free(t)=exp(-4 pi^2 nu t) U0.

Since 4 pi^2 nu < 1/25 and T=21/5, exp(-x)>1-x gives

    exp(-4 pi^2 nu T) > 1-21/125 = 104/125 > 4/5.  (3)

## 3. A drift-independent nonlinear relative-energy inequality

Let U=e3 w be the smooth scalar center under either the controlled or zero drift. Let u be any Leray–Hopf solution with the SAME prescribed drift and let z=u-U.

The standard weak–strong relative-energy identity, obtained by testing the weak equation against the smooth U and using the two energy relations, gives

 ||z(t)||2^2 + 2 nu integral_0^t ||grad z||2^2
 <= ||z(0)||2^2 - 2 integral_0^t integral z3 z_h dot grad_h w.   (4)

The prescribed transport cancels exactly in the cross energy because div b=0. No derivative of b occurs. Its Leray projection is harmless against divergence-free test fields. The perturbation self-advection also cancels. This argument works for the native transport form; it would not automatically apply to a different control containing (u dot grad)b.

Using div_h z_h = -partial_3 z3 and partial_3 w=0,

 -integral z3 z_h dot grad_h w
 = integral w z_h dot grad_h z3 - integral w z3 partial_3 z3
 = integral w z_h dot grad_h z3.                 (5)

The last term vanishes by periodic integration in x3. Mean-zero Poincare applies to the horizontal components on the full T^3:

    ||z_h||2 <= ||grad z_h||2/(2 pi).

Consequently, writing D=||grad z||2,

 |integral w z_h dot grad_h z3|
 <= [||w||infinity/(2 pi)] ||grad z_h||2 ||grad_h z3||2
 <= [||w||infinity/(4 pi)] D^2.                  (6)

This component structure is stronger than bounding the base by its large H3 norm or gradient. It uses the actual scalar maximum principle, not a maximum principle for a general Leray velocity.

In general, if ||w(0)||infinity <= 4 pi nu, (4)-(6) show that every perturbation has nonincreasing L2 distance from this center, regardless of perturbation amplitude. In our numerical normalization, pi>25/8 implies

    a/(4 pi nu) < 4/5.

Thus

 ||z(t)||2^2 + (2 nu/5) integral_0^t ||grad z||2^2
 <= ||z(0)||2^2.                                (7)

In particular ||z(t)||2 <= ||z(0)||2. The small relative radius of B is needed for a useful endpoint comparison, not to derive (7).

For completeness, the prescribed drift is smooth in space and bounded with sufficient time regularity. The usual divergence-free Galerkin construction gives global Leray–Hopf solutions with the unforced energy inequality, because prescribed transport is skew in L2. Smooth U is an admissible relative-energy test after time approximation. Inequality (7) initially holds at the standard energy times; weak continuity and lower semicontinuity extend its norm bound to every t. No uniqueness of u is inferred. The same reasoning applies independently to all uncontrolled Leray–Hopf solutions.

## 4. Endpoint and same-input no-control separation

For u0 in B, put r=||u0-U0||2 <= M/5. By (2) and (7),

    ||u(T)||2 <= M/16+r <= (21/80)M,
    ||u0||2 >= M-r >= (4/5)M.

Dividing gives 21/64 < 1/3.

For the SAME initial datum in the no-control experiment, (3) and (7) give

    ||u_free(T)||2 >= ||U_free(T)||2-r > (3/5)M,
    ||u0||2 <= M+r <= (6/5)M.

The ratio is therefore strictly greater than 1/2. This is a statement for every datum and every pair of admitted Leray–Hopf realizations, not merely a slow center or a worst-case datum somewhere in the ball.

An explicit genuinely three-dimensional smooth member is

 u0 = a e3 cos(2 pi x2)
      +(1/2000)[e1 cos(2 pi x3)+e2 sin(2 pi x1)+e3 sin(2 pi x2)].

It is divergence free, mean zero, depends on all three coordinates, and has relative perturbation norm sqrt(3)/20 < 1/10. Its nonlinear self-advection is not identically zero. An additional mean-zero, divergence-free manufacturing error of L2 norm at most M/10 keeps it in B. This is a conditional preparation specification, not a certified experimental input.

## 5. A directly measurable low-mode prediction

Define the normalized vertical Fourier score

    F(u)=(2/a) integral_T3 u3(x) cos(2 pi x2) dx.

The center initially has F(U0)=1. Its dual L2 norm gives |F(z)|<=||z||2/M. Therefore

    F(u_control(T)) <= 21/80,
    F(u_free(T)) > 3/5,
    F(u_free(T))-F(u_control(T)) > 27/80.          (8)

The controlled score can have either sign; the upper bound is enough. Unlike total terminal kinetic energy, (8) can be acquired by a single Fourier-weighted velocity measurement. A separate acquisition note pays finite-variance spatial sampling and makes its calibration assumptions explicit.

## 6. Physical cost, prior, and limitations

The command is one 4.2-unit block: nominal scalar peak 128, calibrated vector peak below 129, nominal slew at most 2400, scalar area 524.8, and integrated squared command at most 68812.8. It uses one fixed spatial frequency p=e1. These are nondimensional mathematical quantities, not watts, seconds, monetary cost, or demonstrated hardware performance. The actuator is much stronger than the initial fluid amplitude 0.01.

The underlying nonlinear energy method is established Reynolds–Orr methodology. Global energy-space stability of symmetric Navier–Stokes flows under general three-dimensional Leray–Hopf perturbations is established prior; see Bardos, Lopes Filho, Niu, Nussenzveig Lopes, and Titi, arXiv:1201.2742v2, Theorem 3.1 and its relative-energy argument (3.7). Their stated theorem is unforced and in its declared geometry; our prescribed skew drift and component bound are derived above, not imported as an unexamined corollary. The inherited spectral operation is independently certified but is not a nonlinear regularity theorem.

Primary sources checked:
- https://arxiv.org/html/1201.2742v2
- https://people.math.wisc.edu/~fwaleffe/GFD2011lectures/GFD3.pdf

This is a finite-time performance law for all energy-admissible solutions of the stated model. It does not select a unique physical solution, exclude singularities, prove a global strong basin, or make a generic turbulence claim. The exact initial mean, divergence constraint, full L2 preparation error, controller calibration, viscosity, spatial periodicity, and readout error contract must be supplied or separately qualified. No experimental calibration is acquired here.

## fluid_energy_basin_v1/FREE_FIBER_CERTIFICATE.md

# Self-contained dependency map for the one scalar fiber

The new nonlinear theorem needs only the free scalar channel (m,k)=(1,1). It does not need the in-plane Leray–Jacobi reduction, Jost scattering, an enhanced-dissipation asymptotic, a nonlinear short-pulse theorem, or a general three-actuator composition. The complete historical linear packet is included to preserve provenance and failed bounds; this note isolates the actual dependency.

## Physical Fourier equation

On the exact vertical center U=e3 w(x1,x2), Leray projection is the identity and self-advection vanishes. In either transverse Fourier fiber k2=+/-1, write w as a sum of exp(2 pi i(n x1+k2 x2)). During the plateau the scalar generator, after fixed diagonal unitary phase/sign gauges, is

    A=-d diag(1+n^2)+c K,  n in Z,
    K_(n,n+1)=-1/2, K_(n+1,n)=1/2,
    d=4 pi^2/1000,
    |c|=256 pi theta |1+e2|.

The sine convention in PROOF.md and cosine convention in the historical source differ only by a static phase. The two conjugate real fibers have the same norm. Direct rational bounds 157/50<pi<22/7 and the stated calibration interval give

    197/5000 <= d <= 198/5000,
    801 <= |c| <= 807.

A fixed sign gauge makes c positive. The ramps have the same transverse fibers and physical L2 contraction, independent of the phase.

## Exact finite metric and infinite exterior

Let D be the integer matrix in linear_certificate/exact_saved/m1_k1_free_metric.json. Set S=D/2^40 on -32<=n<=32 and extend S by the identity outside this interval. The six saved congruences prove

    I<S<8I

and strict positivity, at each rectangle corner c in {801,807}, d in {197/5000,198/5000}, of

    H= -A_32^T S-S A_32-2S
       - alpha[(S-I)e_left e_left^T(S-I)
                +(S-I)e_right e_right^T(S-I)],
    alpha=807^2 / [8((197/5000)*1090-1)].

The interior formula is affine in c,d, so one fixed S covers the full physical rectangle. In the exterior, the residual -A^*S-SA-2S equals the positive diagonal 2[d(1+n^2)-1]. All exterior-to-exterior transport cancels. There are exactly two cut bonds. Their cross terms are c(S-I) times the boundary coefficient 1/2. Bounding the two exterior inverse diagonal entries by 1/[2((197/5000)*1090-1)] gives precisely the subtracted alpha term. Thus the full infinite operator satisfies

    A^*S+SA <= -2S.

This calculation is first valid on finitely supported sequences. Diagonal heat plus bounded skew K generates a strongly continuous semigroup. The finite-rank modification S-I preserves the diagonal generator domain, so the form estimate extends by the usual core/energy argument. It follows that

    ||exp(tA)|| <= sqrt(8) exp(-t).

The positive Taylor sum sum_{j=0}^32 8^j/j! exceeds 2048. Therefore sqrt(8) exp(-4)<1/16. No floating eigenvalue is needed for that implication.

## Why the saved positivity witnesses are decisive

For each of the six rational matrices H, a saved dyadic matrix B satisfies exact positive strict row diagonal dominance of B H B^T. It is therefore positive definite. This also forces B to be nonsingular, hence H is positive definite. The auxiliary floating eigensolver only proposed B; its eigenvalues are not premises of the proof.

The read-only script verify_one_channel.py reconstructs all six H matrices from the saved metric and rational constants, multiplies the saved integer congruences, and checks both strict dominance and agreement with the recorded exact margins. It uses Python's arbitrary-precision integers and fractions, with no numerical linear-algebra library, fit, solve, or PDE. Its scalar checks also recount the new theorem's basic rational margins.

The historical qualification checked 60 matrix gates across ten channels. The new theorem uses six of those gates. Historical failed high-sector storage attempts remain in linear_certificate/FLOAT_RESULT.json; they are not needed for this one-fiber argument, and are not silently promoted to successes.

## fluid_energy_basin_v1/linear_certificate/CERTIFIED_LINEAR_THEOREM.md

# Finite-parameter, calibrated, infinite-mode linear viscous-shear certificate

2026-11-09. Author-constructed analytic/computer-assisted certificate. The exact arithmetic run is not a proof-assistant validation, independent end-to-end audit, nonlinear Navier–Stokes controller, PDE simulation, or device experiment. The inherited native Leray-to-Jacobi reduction remains an analytic dependency.

## The quantified statement

On the unit three-torus, consider the mean-zero divergence-free LINEAR equation

    u_t = (1/1000) Delta u + P[(b(t,x) dot grad)u].

Use three consecutive prescribed blocks with nominal spatial pairs

    (p1,a1)=(e1,e2), (p2,a2)=(e1,e3), (p3,a3)=(e2,e1).

In block j, the implemented spatial field is theta_j(a_j+e_j) cos(2pi p_j dot x+phi_j), where the independent errors are static over that block,

    |theta_j-1|<=1/1024, e_j dot p_j=0, |e_j|<=1/1024,

and phi_j is arbitrary. Multiply it by the scalar command consisting of a0.1-unit quintic ramp from0 to128, a4-unit constant plateau, then a0.1-unit reverse ramp. All spatial frequencies and plateau/ramp durations in this theorem are exact. No spatial leakage, time-dependent direction error or nonlinear self-advection is silently included.

For every mean-zero divergence-free initial datum in L2, the time12.6 solution satisfies

    ||u(12.6)||2 <= sqrt(2)/16 ||u(0)||2.                    (T)

The actual mean-zero no-driver linear semigroup at the same viscosity and time has norm exp[-4pi^2*.001*12.6]>1/2. Thus (T) is a full-space finite-parameter improvement over a paid baseline, not a claim based on a few initial vectors or finite-cutoff eigenvalues.

## Exact low-sector certificate

The native Fourier reduction and calibration bounds are detailed in the unchanged INFINITE_TAIL_INTERFACE.md. The five retained pairs are

    (m,k)=(1,1),(2,1),(4,2),(5,2),(8,2),

and both free and native in-plane polarizations are included. The speed/damping rectangle is c in[801k,807k], d in[197/5000,99/2500]. It contains every physical value admitted above using157/50<pi<22/7 and the static calibration bounds. Signs and phases are unitary gauges.

At longitudinal cutoff N=32, the exact pass rounded the ALREADY SAVED floating matrices to rational metrics S with denominator2^40. This is merely the definition of the new rational witness; no rounding-error premise is needed. Free-polarization energy weight is G=I. Native in-plane energy weight is G_n=m+n^2 and the rational skew generator has adjacent coefficients

    K_(n,n+1)=-(m+n(n+1))/(2G_n),
    K_(n+1,n)=+(m+n(n+1))/(2G_(n+1)).

The pass verified G<S<8G and, at all four rectangle corners, strict positivity of

    -A_N^T S-S A_N-2S
    -c_max^2/[2(d_min q_out-1)G_out]
          (S-G) K_LH K_LH^T (S-G),                          (1)

where q_out=m+33^2, the two boundary columns K_LH use the INTERIOR row denominators, and G_out=q_out for the native polarization or1 for the free polarization.

There are60 exact matrix gates:2 metric comparisons plus4 corners for each of10 cases. Every one passed. For each target symmetric rational matrix H, an auxiliary floating diagonalization proposed a dyadic matrix B with denominator2^48. The decisive computation then formed B H B^T in exact integer arithmetic and checked all65 strict row diagonal-dominance inequalities. Positive diagonal dominance proves positive definiteness of the congruence. It also implies B is nonsingular, so H is positive definite. No floating eigenvalue, condition number or factorization is trusted as evidence of positivity.

The exact witness metrics and all60 congruence matrices are saved under exact_saved/. The input/source freeze is EXACT_FREEZE.json, SHA a11c18dacdc10b96b6473c0c19480a1fb7c8f23edd1160909478a0f7ef3d8ee6. The executed checker is qualify_saved_exact.py, SHA50c83962c4312bedcd53632c2876024703cb739c096a6b97b39a25b868a41895. A verifier may reconstruct every rational H from the saved metric and declared integers; no future floating solve or physical oracle is required.

## Why this controls the infinite Fourier tail

Extend S by the natural diagonal energy metric G outside |n|<=32. The exact exterior dissipation residual is2(dq_n-1)G_n, positive beyond the cutoff. Internal exterior skew transport cancels. The only interior/exterior couplings are the two boundary bonds. Taking their exact Schur complement gives (1). Bounding the exterior inverse by the displayed d_min value and c^2 by c_max^2 is conservative. The finite part is affine in c,d, so four corners cover the entire rectangle with the SAME metric. The weighted inequality therefore holds on the full infinite line, not merely the truncated matrix.

Standard closure of the diagonal dissipative generator plus bounded skew Jacobi perturbation then gives

    ||exp(tA)||2 <= sqrt(8) exp(-t)

in the physical orthonormal energy representation. The exact positive Taylor sum confirms exp(8)>2048; hence each retained active plateau contracts by1/16 after time4. The ramps preserve the same transverse sector and contract L2, so they cannot undo this bound.

## Why the failed high-sector screen is not hidden

The original frozen floating screen sought a separate storage bound for every m<18. It FAILED in all ten m>=9 cases. Those failures, including negative infinite-tail margins, are unchanged in FLOAT_RESULT.json and the original report/manifest.

The separate TWO_STAGE_HEAT_REPAIR.md proves that these cases are unnecessary for the whole-word theorem. The first TWO blocks preserve the same transverse sector and together dissipate every m>=9 by ordinary heat:

    exp[-8*(197/5000)*9]=exp(-1773/625)<1/16.

That final inequality was also checked by an exact positive Taylor sum. For m<=8, one nominally dominant-coordinate block has the certified active speed; the other is contractive. Thus the off-axis input is reduced by1/16 before block3.

On the original k1 axis the first two blocks are exactly heat, so |k1|>=3 is already reduced by1/16. The third block needs the low-sector storage only for k1=+/-1,+/-2. It preserves (k1,k3), making these low-axis and high-axis outputs orthogonal. Its full axis norm is therefore at most1/16. The final axis and original off-axis images may overlap, so their contributions are combined by triangle/Cauchy, producing sqrt(2)/16 rather than an unearned1/16.

## Resources and limits

The single exact child completed in3.727289329 seconds, peak50,288 KiB, return code0. The preceding single floating feasibility child cost0.829608051 seconds, peak49,104 KiB. These are selected operation costs, not total research time. No physical trajectory, full nonlinear synthesis or PDE propagation was run.

Nominal scalar peak is128; each ramp's scalar slew is at most2400. Total time is12.6, total scalar absolute area1574.4, and integrated squared scalar command at most206438.4. The calibrated spatial-vector peak is at most129, not exactly128. These are dimensionless mathematical values, not verified hardware specifications.

The present native nonlinear shortness interface does not admit these multi-unit plateaus at nu=.001,K>=1. L2 contraction is not a3D strong-continuation theorem. The remaining operation is a paid nonlinear/critical-norm bridge at these actual parameter values. Neither the earlier giant-resource nonlinear controller nor this concrete linear certificate supplies that bridge automatically.

The method is compared with standard quadratic hypocoercivity, exact Schur tails, robust-corner positivity, and Goulart–Chernyshenko's finite-mode/uncertain-tail nonlinear Lyapunov framework. See PRIOR_AND_NONLINEAR_BOUNDARY.md. No general enhanced-dissipation or external novelty claim is made.

## fluid_energy_basin_v1/SOURCE_MAP.json

{
  "scope": "Scientific proof and exact witness bytes are unchanged. The delivered nonlinear review uses a descriptive reviewer label and package-relative proof location; no mathematical change.",
  "nonlinear_proof_sha256": "4b30a4d09efabeb35f7b8bc6391818fff179340c4b0a8748158303cfb99a7d8a",
  "acquisition_sha256": "7f3c1cd42ca361625dafd22e2daabdcc6c7d5dfd666f6fbed819684b44f9e4d8",
  "original_nonlinear_review_sha256": "6001f1470562bcbf540c309744003562cd997de3c12613f739a75a023e1dad0d",
  "delivered_nonlinear_review_sha256": "e149bd6fc316442cf128b4eabb4ca9115d41504aa5c0062a89741c2943257e03",
  "acquisition_qualification": "The final acquisition text expressly requires fixed fields or a common i.i.d. paired law for a two-sided confidence interval. The earlier text is preserved in the author record; no numerical constants changed.",
  "original_acquisition_review_sha256": "437497db52b7f0b9fe1fe43d7559803259fc3c2b8a2f1e3f58a9b8bdd45dea45",
  "delivered_acquisition_review_sha256": "859f8a0a735bf11bdd064b1d11e7bf16539162314dbe9d70e09560c1d4017b92"
}

## fluid_energy_basin_v1/reviews/NONLINEAR_REVIEW.md

# Targeted challenge of the one-block 3D energy-space performance basin

2026-11-09. Reviewer: coordinated analytical source review. Governing source: PROOF.md, SHA 4b30a4d09efabeb35f7b8bc6391818fff179340c4b0a8748158303cfb99a7d8a. The source was read in full. The reviewer separately checked the component cancellation and constants, then sent the author feedback before this source was bound. This is not blind discovery or an independent replay of the old matrix certificate.

## Disposition

No concrete mathematical blocker was found in the stated finite-time performance theorem for every Leray--Hopf solution. The same fixed L2 ball and same time have a strict controlled-versus-zero-control separation. The result is materially stronger than a small structured-input family for this PERFORMANCE question, but it does not prove strong regularity, uniqueness, or the original arbitrary-H3-ball stabilization target.

No new PDE, floating solve, exact matrix qualification or experimental acquisition was run by this review.

## 1. Native center and allowed calibration

The center is U = e3*w(x1,x2). Its native quadratic self-advection is identically zero, not approximately small. The first calibrated shear has frequency e1 and direction perpendicular to e1. Its vertical component acts through partial3 and therefore vanishes on the center. The remaining scalar drift is divergence free. Leray acts as the identity on the vertical right-hand side at k3=0. Consequently the scalar maximum principle really gives ||w||infinity <= .01 for every admitted static phase, gain and transverse error.

The initial center is fixed as .01*e3*cos(2*pi*x2), independent of the unknown calibration. No feedback or calibration-dependent initial preparation is used. The generic perturbation is not assumed to share the center's symmetry; it may depend on all three coordinates and have unbounded H3 norm within the L2 ball.

## 2. Exact cross term and its factor

The same prescribed transport is skew in the relative L2 energy, including its Leray projection. It would not cancel for a control with a different stretching term (u.grad)b. The nonlinear relative term is exactly minus the integral of z3*z_h.grad_h w. Integration by parts gives

    integral w*z_h.grad_h z3 - integral w*z3*partial3 z3.

The second term is zero because w is independent of x3 and the domain is periodic. The horizontal components of z have zero GLOBAL mean, which is preserved by the native equation. Thus full-torus Poincare gives ||z_h||2 <= ||grad z_h||2/(2*pi). Cauchy and twice-product absorption then give precisely

    |cross term| <= ||w||infinity/(4*pi) * ||grad z||2^2.

There is no missing factor of two: the relative-energy inequality contains twice this cross term and twice the viscous dissipation. Since .01/(4*pi*.001) < 4/5, at least 2*nu/5 times the integrated perturbation dissipation remains. In particular the L2 distance is nonincreasing for perturbations of any amplitude. The radius restriction is used only in converting this distance into a useful output ratio.

## 3. Weak solution and endpoint quantifiers

A smooth divergence-free prescribed drift gives the usual global Leray--Hopf construction with the native energy inequality, because it is L2-skew. The center is globally smooth, so it is an admissible relative-energy test after standard time approximation. No assumption of perturbation smoothness or uniqueness enters the inequality. Both controlled and uncontrolled comparisons apply to every Leray--Hopf solution separately.

Weak L2 continuity and lower semicontinuity extend the uniform distance upper bound from energy times to every declared endpoint. The low-mode observable is also weakly continuous. Consequently the theorem is not merely an almost-every-time statement at an unspecified nearby time. It makes no claim about arbitrary weak solutions lacking the Leray--Hopf energy condition.

## 4. Correct inherited spectral sector

The center lies in k2=+/-1, k3=0. These are the two real conjugate copies of the saved free channel (m,k)=(1,1), not the native in-plane channel and not an untested transverse sector. The exact prior certificate covers the whole longitudinal fiber, including all modes generated by the ramp. Its common metric gives sqrt(8)*exp(-4)<1/16 on the plateau. Both ramps preserve that fiber and are L2 contractions. Static phase is a unitary gauge and the admitted gain/direction interval lies in the previously certified rectangle.

The old infinite-tail theorem was read as a dependency, not rerun. The source correctly refrains from claiming that one actuator contracts the entire linear space by 1/16: its untouched axis would contradict that claim.

## 5. Matched initial ball and arithmetic

For M=.01/sqrt(2) and r<=M/5, the controlled output is at most (1/16+1/5)M = 21M/80. The input is at least 4M/5, giving 21/64 < 1/3.

For the SAME datum without control, the center's heat factor exceeds 1-.04*4.2 = 104/125 > 4/5. Its perturbation distance is still at most M/5. The output therefore exceeds 3M/5 while the input is at most 6M/5, giving a strictly greater than 1/2 ratio. This is uniform over every datum in the closed ball, every allowed controlled calibration, and every pair of controlled/uncontrolled Leray--Hopf realizations. It is stronger than merely finding a slow no-control center.

For the Fourier score (2/a)<u3,cos(2*pi*x2)>, the exact dual norm is 1/M. Hence the controlled absolute score is at most 21/80, the uncontrolled score exceeds 3/5, and the difference exceeds 27/80. The weaker written controlled upper bound remains valid even if its score is negative.

The explicit 3D example is divergence free and has relative perturbation norm sqrt(3)/20 < 1/10. Its quadratic self-advection is nonzero. Adding a further divergence-free mean-zero error of norm M/10 stays inside the prescribed ball. No preparation procedure or measurement guarantee follows merely from writing this specification.

## 6. Prior, practical comparison and remaining gap

The Reynolds--Orr energy method and energy-space stability of symmetric viscous flows are established. The reviewer directly read Bardos et al., arXiv:1201.2742v2, including its symmetry/stability framework and weak--strong relative-energy context. The prescribed skew drift and special vertical-component bound are checked here rather than silently imported from an unforced theorem. No novelty of nonlinear energy stability is certified.

The useful specific composition is a paid one-fiber viscous mixing certificate plus an amplitude-only nonlinear relative-energy estimate, producing a finite L2 preparation-error allowance and an observable matched on/off gap. The actuator peak is still about 12,800 times the center amplitude in nondimensional velocity units. Exact mean/divergence, viscosity, periodic geometry, allowed static calibration, preparation error and readout noise remain assumptions requiring separate physical qualification.

The theorem does not exclude singularities or select a unique 3D realization. Its all-Leray performance statement is intentionally compatible with that unresolved issue. It should not be relabeled a strong-solution basin or a solution of the original full-ball control problem.

## fluid_energy_basin_v1/ACQUISITION.md

# Prospective finite-bit Fourier readout and honest implementation costs

2026-11-09. This is an analytic acquisition contract for PROOF.md, not an experiment or a completed device calibration. It measures a low Fourier coefficient rather than assuming access to the entire terminal velocity field.

## 1. Ideal observable and finite partition

For a=1/100, the ideal score is F(u)=(2/a) integral u3 cos(2 pi x2). The proved contrast is

    Delta = F(u_free(T))-F(u_control(T)) > 27/80,
    T=21/5.

Each state has ||u||2 <= ||u0||2 <= (6/5)M. A formally uniform point sample would have finite second moment, but replacing it by a finite grid of point values is NOT valid for arbitrary L2 fields. The following instrument avoids that aliasing gap.

Partition T^3 into 64 by 1024 by 64 equal rectangular cells. Choose one cell uniformly with 22 random bits. The instrument returns the VOLUME AVERAGE of u3 over that cell, not an unqualified point value. Let y be its x2 center. Multiply the average by (2/a) c_y, where c_y is a rational approximation to cos(2 pi y) with error at most 2^-16.

The expectation is the integral against a piecewise-constant approximation of the cosine. Since the cosine varies by at most pi/1024 inside a cell,

 |E Y - F(u)| <= (2/a)||u||2 (pi/1024 + 2^-16)
              < 6/1024 + 2/65536.                         (1)

This bias is volume- and high-frequency-uniform. It requires the specified cell averaging; 43,200 arbitrary point readings cannot certify the same result without further smoothness or distribution assumptions.

Jensen's inequality gives the ideal finite-cell score's second moment at most

    (1+2^-16)^2 * 2*(6/5)^2
    = (1+2^-16)^2 * 72/25.                               (2)

No output L-infinity or derivative bound is used. A finite range is nevertheless available for cell averages: cell volume is 2^-22, so their magnitude is at most 2^11 ||u||2 < 32. Thus clipping readout to [-32,32] does not increase error relative to the true cell average. Quantizing the clipped velocity with step 2^-20 needs at most 27 signed bits and adds error at most 2^-21.

The 1024 cosine coefficients can be prepared once by rational Taylor arithmetic, with pi bracketed to sufficient precision, and rounded to a 16-bit dyadic grid. This is a fixed finite preprocessing problem. No transcendental oracle, output-dependent fitting, or giant controller synthesis is required. A direct certified cosine polynomial on [-pi,pi] suffices; coefficient preparation has not been executed in this packet.

## 2. Explicit, unacquired instrument and timing contract

Assume:

- The preparation belongs to the proved ball, including mean zero and divergence freedom. The input can be a declared finite Fourier profile plus a separately certified total L2 manufacturing error. Finite low-mode calibration alone does not bound an unknown unresolved tail.
- Each measured cell average has root-mean-square raw velocity error at most 1/100000 before the clipping/rounding above. This includes systematic offset and random sensor error. It must be qualified in the actual spatial averaging geometry and velocity range; it is not inferred here.
- Cells are sampled independently and uniformly. For the two-sided confidence interval below, use either a fixed pair of controlled/uncontrolled fields with independent readouts, or a common independent and identically distributed paired preparation/realization law. Independence alone with an arbitrarily changing law is insufficient to define one common contrast. A noninvasive fixed-field imaging protocol may supply conditional independence.
- Readout occurs at a common time in [T,T+1/100], or at an independently sampled delay in that interval. The delay must be independent of the cell index and the field. The command is already off. Early readout or uncertain actuator completion is not covered.
- Actual viscosity, command, and static calibration satisfy the governing proof. No arbitrary time-dependent phase, spatial leakage, or boundary error is silently admitted.

After T, testing the weak equation against the smooth Fourier mode shows that F is absolutely continuous and

 |F'(t)| <= 4 pi^2 nu |F(t)| + (2 pi/a)||u(t)||2^2
          < 1/10.

Thus the allowed post-completion delay costs at most 1/1000 in mean score. Combining this with (1), sensor error multiplied by 2/a, and dyadic rounding gives a total systematic mean bias below 1/100 per arm. Conservatively the observed score has second moment below 3: its L2 sampling norm is at most the square root of (2), plus the normalized sensor and rounding errors, which is less than 171/100.

These are paid mathematical implications of an explicit instrument contract. The actual instrument qualification, initial-profile manufacture, cell geometry, coordinate registration, and independent snapshot or reset capability are NOT acquired or costed as free. Without them, the physical acquisition is pending rather than validated.

## 3. A simple variance-only confidence ledger

Use independent paired observations D=Y_free-Y_control. The variance is below 6. For each of nine groups, take 2400 such pairs and form its arithmetic mean. Chebyshev gives probability at most 1/4 that a group mean differs from its expectation by more than 1/10. Take the median of the nine group means.

With independent groups, its failure probability is at most

    sum_{k=5}^9 binom(9,k)(1/4)^k(3/4)^(9-k)
    = 12826/262144 < 1/20.                                (3)

The statistical half-width is 1/10. The two instrument-bias allowances add 1/50, so an interval for the IDEAL contrast must have half-width 3/25, not merely 1/10. Under the proved alternative, the worst-case lower confidence endpoint is strictly greater than

    27/80 - 2*(1/50) - 2*(1/10) = 39/400.                 (4)

Both the shift of the implemented mean and its inclusion in the ideal confidence interval are charged. This is standard median-of-means statistics, not a new estimation principle. A valid null interpretation still requires the stated preparation, energy, and instrument variance contracts. If the preparation or realization law changes between runs but every run stays within the theorem, the uniform per-group positive-gap bound still supports a one-sided benefit test; it must not be reported as a two-sided confidence interval for one fixed ideal contrast.

Counts:
- 21,600 paired observations;
- 43,200 cell-averaged velocity readouts;
- 950,400 independent random bits for cell selection;
- fixed-width coefficient/velocity products and rational group means; no fitted root or trajectory reconstruction.

If each readout needs a fresh physical run, the maximum total evolution wait is 43,200*(4.2+0.01)=181,872 native time units, plus all preparation/reset/readout overhead. Only half the runs use the actuator. Their aggregate nominal scalar action is 11,335,680 and aggregate integrated squared command is at most 1,486,356,480 in the model's units.

A truly noninvasive simultaneous spatial snapshot could reduce the number of repeated evolutions, but that hardware is not assumed. The finite-variance result does not establish seconds of wall time, energy consumption, sensor resolution feasibility, or a ready laboratory protocol.

## fluid_energy_basin_v1/reviews/ACQUISITION_REVIEW.md

# Narrow review of the prospective finite-cell Fourier acquisition

2026-11-09. Bound source: ACQUISITION.md, SHA 7f3c1cd42ca361625dafd22e2daabdcc6c7d5dfd666f6fbed819684b44f9e4d8. This is an analytic contract check, not instrument qualification, a statistical experiment or a numerical replay. The reviewer identified the common-law qualification, and the author explicitly added it while preserving the older text.

No concrete blocker was found at the narrowed stated scope.

The cell-average construction is essential. Jensen bounds the sampled average's second moment using the global L2 energy. Its expectation is exactly an integral against a piecewise-constant cosine approximation. The displayed pi/1024 spatial-weight error and 2^-16 coefficient error therefore remain valid for arbitrary L2 fields, without an unearned point-grid or derivative bound. Cauchy gives the stated cell range, and clipping followed by quantization has the stated deterministic error. These conclusions do not establish that a physical sensor can supply the required volume average or RMS accuracy.

After switch-off, the smooth cosine test has viscous derivative 4*pi^2*nu times the score. The quadratic contribution is bounded by (2*pi/a)||u||2^2, using the product of the second and third velocity components. Under the proved energy cap their sum is below .1. Thus the independent post-completion delay at most .01 costs at most .001. Early measurements and cell-correlated timing are correctly excluded.

The combined spatial, coefficient, sensor, rounding and timing bias is below .01 per arm. The Minkowski second-moment bound is below 3. Independent paired differences consequently have variance below 6. A group of 2400 pairs has Chebyshev failure probability below 1/4 at half-width .1. The nine-group median tail is exactly 12826/262144 < 1/20. The ideal interval's half-width is .12, not .1: the two-arm bias allowance is paid. The worst-case positive lower endpoint correctly charges both displacement of the implemented mean and the interval enlargement, leaving 39/400.

The revised source now requires a fixed field pair with independent readouts, or one common i.i.d. paired preparation/realization law, for a two-sided confidence interval about one ideal contrast. This resolves the earlier ambiguity: independence alone does not define such a contrast under changing laws. The separate one-sided uniform-benefit interpretation for independent observations with varying admissible laws is properly distinguished.

The counts of 21,600 pairs, 43,200 readouts, 950,400 selection bits, worst-case repeated evolution time, aggregate actuation and squared actuation are consistent. Preparation, reset, actual averaging hardware, calibration, unresolved input-tail control and independent sampling remain explicitly unacquired. No laboratory practicality or end-to-end execution is certified by this review.

## fluid_energy_basin_v1/reviews/LINEAR_REVIEW.md

# Independent analytic and source challenge of the finite-parameter linear certificate

2026-11-09. Scope: independently inspect the native polarization reduction, uncertainty coverage, infinite-tail Schur condition, exact checker construction, whole-word heat repair and no-driver comparison. This review did not rerun the60 integer congruence gates, perform a new floating solve, propagate a PDE, or test a nonlinear controller. It verified the110 file hashes in the existing exact manifest and inspected saved integer-witness structure. The existing execution receipt supplies the reported gate outcomes.

## Verdict

No concrete analytic obstruction or source/statement mismatch was found. The stated all-calibration, infinite-mode LINEAR bound `sqrt(2)/16` at time12.6 follows from the archived positive exact gates through the displayed argument. The high-sector screen failures are genuinely bypassed by a valid two-block heat estimate, not silently deleted or relabeled as successes. The bound is meaningfully smaller than the actual full-space no-driver linear norm at the same viscosity and time.

This is not an independent replay of all saved numerical certificates, a proof-assistant check, a nonlinear Navier–Stokes admission, or an apparatus claim. A source review plus the producing run's receipt should not be described as a second execution.

## Bound source state

- Governing theorem `CERTIFIED_LINEAR_THEOREM.md`: SHA256 `9a6ea7ee366e19e9b9e744d5628d5748acc426d023453ab23df4c6e5060dcd2a`.
- `INFINITE_TAIL_INTERFACE.md`: `9e659d090830f438511bfa06066e97c12cbba17c3615ed390b3716d9399ac30c`.
- `TWO_STAGE_HEAT_REPAIR.md`: `892ff8cab3a0f7aa208ea8ad2ff4f18550dcd2a96f6cd1d735c78ff1e2f30692`.
- Exact checker `qualify_saved_exact.py`: `50c83962c4312bedcd53632c2876024703cb739c096a6b97b39a25b868a41895`.
- `EXACT_FREEZE.json`: `a11c18dacdc10b96b6473c0c19480a1fb7c8f23edd1160909478a0f7ef3d8ee6`.
- `exact_saved/RESULT.json`: `6c97d89819e6e090bb7d3dc380f4b78cc975d5031ca3db2ebcbdb1fa72570eca`.
- `EXACT_MANIFEST.json`: `bb71748584e5c4d4f5ad2fb652790942790ef8821bb6a79f8fa9a1a331b512aa`. All110 listed file digests matched during this review.

No governing file was changed by this review.

## 1. Actual native polarizations and calibration

For one coordinate shear, fixing the transverse integer frequency xi gives `(v.grad)=2pi i(v.xi)`. The direction v therefore enters the longitudinal generator only through the scalar speed. Leray projection between neighboring frequencies has a fixed free polarization perpendicular to the plane spanned by p and xi, and an in-plane polarization. The latter has neighboring unit-vector overlap

    [m+n(n+1)] / sqrt[(m+n^2)(m+(n+1)^2)],  m=|xi|^2.

The cosine supplies the factor1/2. Thus the two displayed Jacobi channels are the actual native velocity reduction, not a replacement by a passive scalar. The polarizations depend on p,xi,n, not on the calibrated transverse v. The zero-transverse-frequency fiber is handled separately as ordinary heat.

With rho=1/1024, `v=theta(a+e)` satisfies

    |v-a| <= rho+(1+rho)rho = 2rho+rho^2 < 1/500.

For a nominally dominant coordinate k, `sqrt(m)<=sqrt(2)k<3k/2`; hence `.997k<|v.xi|<1.003k`. The elementary pi enclosure gives

    256*(157/50)*(997/1000) > 801,
    256*(22/7)*(1003/1000) < 807.

The speed rectangle therefore contains every admitted active physical speed. Similarly `197/5000 < 4pi^2/1000 < 99/2500`. Signs are removable by a fixed alternating diagonal gauge; static phases by a fixed diagonal phase gauge. Both commute with viscosity and preserve the physical norm. Independent phase and calibration choices in different blocks cause no problem because the intermediate composition uses physical L2 bounds, not a common metric across different blocks.

The frozen theorem assumes fixed phase and direction within each block, exact spatial frequencies and exact times. It does not cover phase drift, off-frequency leakage or nonlinear self-advection.

## 2. Weighted rational coordinates and the infinite tail

Writing physical orthonormal in-plane coordinates as `z_n=sqrt(G_n) psi_n`, with `G_n=m+n^2`, converts the skew coupling to

    K_(n,n+1) = -[m+n(n+1)]/(2G_n),
    K_(n+1,n) = +[m+n(n+1)]/(2G_(n+1)).

Thus `K^T G+G K=0`. The checker correctly uses the INTERIOR weight in the boundary coefficient from outside to inside. At either cut bond its absolute coefficient is

    kb=[m+N(N+1)]/[2(m+N^2)]

for the native in-plane channel, or1/2 for the free channel. The two cut bonds have the same absolute coefficient by reflection.

Extend the finite metric S by G outside. In the residual `-A^T S-SA-2S`, the exterior block is exactly the positive diagonal `2(dq_n-1)G_n`. All internal exterior skew terms cancel. The cross-block term is `-c(S-G)K_LH`; there are precisely two boundary columns. Eliminating the exterior therefore gives the finite subtraction

    c^2 kb^2/[2(dq_out-1)G_out]
       *[(S-G)e_left e_left^T(S-G)
          +(S-G)e_right e_right^T(S-G)].

There is no truncated-tail approximation in this expression. Replacing its scalar by the c_max,d_min value is conservative. The remaining finite residual is affine in c,d, and the same S is used at all four corners. Hence corner positivity covers the full rectangle without any assumption that nonnormal semigroup decay is monotone in c.

In physical orthonormal coordinates, the metric is identity plus a finite-rank bounded perturbation, and the generator is the closed diagonal dissipative operator plus bounded skew Jacobi coupling in each retained sector. The energy inequality extends from its core. Thus the infinite-line implication is justified at the stated linear scope.

## 3. Exact source construction and certificate meaning

I checked the integer scaling in the source. With `L=2^40`, `S=D/L`, `A=AI/AD`, `V=D-LG`, and the positive rational tail coefficient `tailnum/tailden`, the desired matrix is

    RN/(AD L) - tailnum*outer/(tailden L^2),
    RN=-(AI^T D+D AI)-2AD D,
    outer=V_left V_left^T+V_right V_right^T.

The saved checker constructs exactly the numerator

    H=RN*tailden*L-outer*tailnum*AD

over the positive denominator `AD*tailden*L^2`. Its `dn=197,198` over5000 gives the declared damping endpoints. Its rational K coefficients satisfy the exact G-skew check. Lower and upper metric gates are exactly `D-LG>0` and `8LG-D>0`.

The decisive array products have object-integer entries. Floating diagonalization is used only to propose the saved integer matrix B; rounding a candidate does not itself certify anything, but the subsequent exact multiplication does. The check `C_ii>sum_(j!=i)|C_ij|` for symmetric `C=BHB^T` gives positive definiteness by Gershgorin. It also forces B to have full rank, so an additional determinant test is unnecessary. Therefore H is positive definite.

The saved metric defines a rational witness in its own right. Its validity does not depend on the accuracy of the earlier floating Lyapunov solve, square roots or rounding. Saved metric and congruence matrices inspected here had the declared65-by65 integer structure. The manifest binds all remaining witnesses and the source. This review did not independently recompute all60 products; the archived producing run reports60 successes and two exact scalar successes.

## 4. Whole-word composition and failed-sector repair

The first two blocks preserve the same transverse frequency xi relative to p=e1. In every fiber their physical energy supplies a norm factor at most `exp(-4dm)` per plateau, regardless of whether the actual transport speed is active, weak or resonant. Therefore for m>=9 the pair contributes

    exp[-8*(197/5000)*9] = exp(-1773/625) < 1/16.

The exact positive Taylor lower-sum check in the saved source is a valid way to prove the last inequality. It uses no floating exponential.

The only nonzero sums of two squares below9 are1,2,4,5,8. A nominally dominant-coordinate block is certified for each, and its partner remains contractive in that same invariant fiber. No commutation between the two different calibrated generators is required. Hence the original off-axis input Q is reduced by1/16 after the first two blocks.

On the original p=e1 axis E, those two blocks are exactly heat. Modes with |n|>=3 already satisfy the same1/16 bound. The third block preserves its own transverse coordinates `(k1,k3)`, so its outputs from original axis modes |n|<=2 are orthogonal to those from |n|>=3. The low-axis modes have third-block parameters m=1 or4 and are certified. Thus the full original axis contribution is at most1/16.

The third block is contractive on the off-axis image. Final axis and off-axis images need not be orthogonal. The proof correctly uses

    ||T3 T2 T1 f|| <= (||Ef||+||Qf||)/16
                      <= sqrt(2)||f||/16.

The failing individual-storage cases with m>=9 remain failures. The two-block heat estimate makes those individual conditions unnecessary for this particular whole-word theorem. This is a valid analytic repair, not an unreported physical parameter change.

## 5. Scalar exponential gates, legal command and baseline

Metric comparison `G<S<8G` gives norm at most `sqrt(8)exp(-4)` over the plateau. Its being below1/16 is equivalent to `exp(8)>2048`, exactly the first scalar gate. The source computes positive finite Taylor lower sums for both exponential gates with rational arithmetic. Positive omitted terms justify the direction of each comparison.

The quintic ramp has `r'=30s^2(1-s)^2`, maximum15/8, and r,r',r'' match the neighboring zero/constant segments. Consequently the three-block command is globally C2, nominal scalar peak128, slew at most `1280*(15/8)=2400`, and total time `3*(4+1/10+1/10)=63/5`. The ramp symmetry gives total scalar area `3*128*(4+1/10)=1574.4`. Bounding the full command by128 yields the stated squared-area upper bound `128^2*(63/5)=206438.4`. Finally `128|v|<=128(1+1/1024)^2<129`. These are dimensionless command values, not spatial W3 norms or hardware measurements.

The exact unforced mean-zero linear norm is `exp(-d*63/5)`, attained on a divergence-free |k|=1 Fourier mode. A simple exact proof of the claimed lower baseline is

    d*(63/5) < (99/2500)*(63/5) = 6237/12500 < 1/2,
    exp(1/2) < sum_(j>=0)(1/2)^j = 2.

Thus the no-driver norm is strictly greater than1/2, whereas the certified controlled upper bound is `sqrt(2)/16`. The comparison is full-space linear operator norm against full-space linear operator norm, not selected test vectors against an unmatched baseline.

## 6. Remaining boundary

The proof does not establish a nonlinear strong-solution interval, pay the nonlinear storage defect, or enter a critical continuation basin. The previous short-pulse theorem does not admit these multi-unit plateaus at the stated viscosity and incoming K>=1. That is a substantive remaining operation, not a minor implementation detail.

The method uses established Lyapunov/storage and exact Schur-complement ideas, with the inherited native Leray reduction. The useful supported increment is the saved finite-parameter all-mode LINEAR certificate under the stated static calibration and explicit baseline. Broad novelty, practical control and nonlinear stabilization should not be inferred.

An optional pointwise-storage extension was discussed separately with the author: with fixed p and phase, a common S would allow scalar speed/damping varying measurably within the same rectangle, since polarizations do not depend on v. This observation is not included in the frozen theorem or its certification scope, and supplies no actuator-slew or phase-drift allowance.

## fluid_energy_basin_v1/REPLAY_STATUS.md

# Exact read-only package replay

One pre-frozen standard-library replay completed successfully on 2026-11-09:

- Six pre-existing free-channel matrix gates passed.
- Each saved exact diagonal-dominance margin was reproduced.
- Ten rational scalar reserves passed, including the plateau exponential, nonlinear ratios, readout bias/variance and confidence margin.
- Whole-child elapsed time: 0.568801124998572 seconds.
- Peak resident memory: 12,288 KiB. Return code: 0.
- The declared cap was 20 seconds, with one computational thread.

The source and all scientific inputs were frozen beforehand. No metric or congruence was generated, changed or fitted. No nonlinear or linear PDE was propagated. No parameter was retuned. The replay's stdout, stderr, receipt and input freeze are included.

This run verifies the read-only packaging aid against the existing exact witnesses. It is not an independent mathematical audit, a new scientific dataset, or an experiment. The historical floating screen and exact 60-gate producing pass have separate receipts and scopes in linear_certificate/.
