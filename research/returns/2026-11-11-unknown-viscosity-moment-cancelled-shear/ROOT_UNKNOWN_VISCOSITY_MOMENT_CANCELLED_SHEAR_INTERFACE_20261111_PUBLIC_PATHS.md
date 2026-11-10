Unknown-viscosity shear excursions with two cancelled moments
11 November 2026 Brisbane

1. The exact physical scalar operation.

On the unit three-torus let F=e_i sin(2pi x_j) or e_i cos(2pi x_j), i!=j, and kappa=2pi. Thus div F=0, Delta F=-kappa^2 F and P[(F.grad)F]=0. Let viscosity be ANY unknown constant nu in a supplied interval 0<nu_-<=nu<=nu_+<=1. Write lambda=nu kappa^2 and choose the rational upper bound Lambda=49, so 0<lambda<Lambda. This lambda is used only in the proof, never as input to the force.

Set
 r(z)=z^2(1-z)^2(14z^2-14z+3), 0<=z<=1.
It has degree6 and r(0)=r(1)=r'(0)=r'(1)=0. Direct beta-integral arithmetic gives
 integral r=0, integral z r=0, integral r^2=3/10010.       (1)
For example, the first identity is 14 B(5,3)-14 B(4,3)+3 B(3,3)=0; symmetry r(1-z)=r(z) then gives the second. For the third, expanding the square gives
 196 B(9,5)-392 B(8,5)+280 B(7,5)-84 B(6,5)+9 B(5,5)
 =196/6435-392/3960+280/2310-84/1260+9/630=3/10010.
Also ||r||infinity<=3/16<1.

For rational amplitude A and rational duration h>0 apply the ORDINARY force
 f(t,x)=A h^-2 r''(t/h) F(x), 0<=t<=h.                 (2)
Its time degree is4. It contains no nu or rho and no transcendental time coefficient. For initial velocity zero and magnetic field zero, the EXACT physical Navier--Stokes/MHD solution with zero disturbances is u(t)=x_lambda(t)F, B(t)=0, where
 x_lambda'+lambda x_lambda=A h^-2 r''(t/h), x_lambda(0)=0.
Define the integrated shear alpha_lambda(t)=integral_0^t x_lambda(s)ds. Integration by parts gives
 alpha_lambda(t)=A r(t/h)-lambda A integral_0^t exp[-lambda(t-s)]r(s/h)ds,
 x_lambda(t)=A h^-1 r'(t/h)-lambda alpha_lambda(t).     (3)
Consequently, uniformly over ALL real nu in the interval,
 sup_(0<=t<=h)|alpha_lambda(t)-A r(t/h)|<=|A|Lambda h.   (4)

At the final time, subtract the first two Taylor terms of exp[-lambda(h-s)] inside the integral. Both vanish by (1). Since |exp(-y)-1+y|<=y^2/2 for y>=0,
 |alpha_lambda(h)|<=|A|Lambda^3 h^3/2,
 |x_lambda(h)|<=|A|Lambda^4 h^3/2.                    (5)
This is an approximate, quantified return, NOT an exact inverse. With only the first cancelled moment the corresponding residual is of order h^2. The second moment materially improves accumulation across a variable number of pulses. No unknown coefficient is estimated or measured.

2. The magnetic average remains uniformly favorable at the isolated-pulse level.

Put z=t/h and R_lambda(z)=alpha_lambda(hz)/A for A!=0. From (4), ||R_lambda-r||infinity<=Lambda h. If Lambda h<=1, then
 |integral R_lambda^2-3/10010|<=3 Lambda h.              (6)
For instance Lambda h<=10^-6 implies integral R_lambda^2>=3/20020.

The exact ideal induction propagator for x_lambda(t)F is M_(alpha_lambda(t)), with the inherited polynomial fixed-order bounds. For the four choices of impulse sign and sine/cosine, followed by the three cyclic shear orientations, the generator identity is algebraic at EACH common profile value. Its time-averaged conjugated magnetic diffusion is exactly
 rho [1+(kappa^2 A^2/6) integral_0^1 R_lambda(z)^2 dz] Delta.  (7)
All twelve fundamental fields have the same Laplacian eigenvalue; hence the unknown lambda and scalar profile are the same across these isolated pulses. The stretching corrections cancel in the sine/cosine/sign average, rather than being discarded. For every rho>=rho_->0, (6) supplies a uniform enhanced mean-zero diffusion coefficient. It is important that (7) is the arithmetic average of ISOLATED pulled-back generators. Equation (5) does not reset an actual concatenated train exactly, and neither (6) nor (7) asserts a finite-time coupled contraction theorem.

3. What can be paid for a train of pulses before nonlinear stability.

Consider N nonoverlapping pulses (2) of a common width h, from the fixed twelve-field catalogue, with |A_j|<=A_*, and total train duration T=N h<=1. Let w_lin be the EXACT linear Stokes response to this prescribed force, starting from zero. On pulse j, split w_lin into its isolated response x_lambda F_j and the decaying tails of previous pulses. All active fields are Laplacian eigenfields with the same lambda. Equation (5) gives, for every fixed spatial order s,
 ||tail||Hs<=C_s N A_* Lambda^4 h^3
             =C_s A_* Lambda^4 T h^2.                (8)
The isolated active response is bounded by C A_*/h when Lambda h<=1. Its self-quadratic convection vanishes. Thus the known Stokes reference has momentum residual bounded by
 ||P[(w_lin.grad)w_lin]||Hs
 <=C_s[A_*^2 Lambda^4 T h + A_*^2 Lambda^8 T^2 h^4].   (9)
The derivative orders are fixed and all spatial frequencies here are fundamental. At the end of the train, ||w_lin(T)||Hs has the bound in (8). This is a bound for the prescribed reference's residual, NOT already a bound for the error of the nonlinear physical solution. A direct Gronwall estimate in the large carrier norm would be exponentially bad; an actual moving-coordinate stability argument is still required.

The force peak is at most C A_* h^-2 and its integrated W1,infinity norm at most C T A_* h^-2. Expanding (2) into ordinary rational time polynomials costs a fixed number of rational operations per pulse; its coefficient heights are bounded polynomially in the bit lengths of A_j, h and the rational pulse origins. The interval count N and every pulse are charged. If A_*, T and h^-1 have polynomial numerical bounds, these quantities do too. Exponentials in (3) are proof formulas for all real lambda, not values queried by the compiler.

4. The interface still missing for a full unknown-parameter compiler.

The accepted known-(nu,rho) common MHD construction controls an arbitrary unknown mean-zero H1 pair, erases both fields, and writes an arbitrary input velocity Fourier target with the same twelve mechanical actuators, no chosen magnetic force, all disturbances/all energy-admissible weak realizations and paid uniform polynomial resources. Its physical carriers include viscosity-dependent terms such as -nu Delta w. Merely selecting one representative nu, using a parameter-dependent force for each pair, or taking the union of the output schedules does NOT give one force for an entire parameter rectangle.

The pulse (2) supplies a new exact viscosity-independent PHYSICAL operation, not just a desired velocity. Equations (4)--(9) retain uniform ideal-phase, endpoint-tail and reference-residual budgets without knowing nu. For a full compiler they must be composed with uniform joint velocity/magnetic stability, a velocity-reset mechanism, generator averaging, the variable-target writer and all-weak transfer. In particular the enlarged erasing word may require nonzero intermediate impulses and different modes; the isolated-loop lemma is not silently substituted for that word. Unknown rho also remains in physical evolution although (7) has a uniform lower bound. This note does not construct those operations, prove the full ensemble result or obstruct all controls.

5. Other representations and boundaries.

Nonzero conserved magnetic mean is a different natural extension. On the closed torus, integral B is invariant when the magnetic disturbance has zero mean. For a known harmonic mean H and b=B-H the equations have additional opposite first-order couplings +(H.grad)b in momentum and +(H.grad)u in induction. Their TOTAL L2 energy contributions cancel by integration by parts. The full ideal shear acts on H affinely: M_a H=H+a s'(x_j)H_j e_i. Thus one cannot simply replace B by b and quote the zero-mean theorem without retaining the known magnetic carrier and its Lorentz force. At most this supplies an affine representation and a plausible separate flux-sector operation. Unknown coefficients pose a different shared-force quantifier that the known-parameter theorem has not constructed.

An arbitrary nonzero magnetic target under mechanical control for EVERY input field is impossible as stated: zero magnetic data and zero magnetic disturbance stay identically zero. At rho=0, mean-zero magnetic helicity is a separate obstruction to erasure. These do not negate the strictly positive, zero-magnetic-target parameter-rectangle problem.

Continuous strong tracking of an arbitrary prescribed velocity curve is already obstructed by testing the equation against an unforced Fourier direction, even in the fluid subsystem. Likewise the known H1-ball theorem is not automatically an L2-ball theorem: the nonlinear short-time smoothing kernel needed for that replacement loses integrability in3D. Those are distinct objectives, not consequences obtained by relabeling endpoint control.

6. Primary contracts used for comparison.

Nersesyan1403.5369v2, https://arxiv.org/pdf/1403.5369v2, introductory controllability definition and Main Theorem: for each nu>0 and smooth initial/terminal velocity and desired volume-preserving flow, a finite-dimensional force exists. The definition quantifies nu BEFORE the existential control, not one control uniformly for an unknown continuum, and provides no common-H1-ball binary/numerical compiler contract. The twelve fundamental space is included in its generator example. These qualitative foundations are inherited, not new here.

Liao--Sueur--Zhang2505.07366v1, https://arxiv.org/pdf/2505.07366v1, assumptions1.2a--b/Theorem1.1, has non-resistive dynamics, bounded-domain boundary action on BOTH fields and H24/H8 extended initial data. It does not supply the parameter-blind periodic mechanical compiler. Kukavica--Novack--Vicol2108.12089v1, https://arxiv.org/pdf/2108.12089, Theorem1.1 and equation1.5, has ideal2D duct boundary control and an explicit conserved-mean obstruction; its additional magnetic forcing is an actual change of control contract. These governing passages were read at those scopes. No theorem for the present coupled uncertainty problem is inferred from an abstract or from common terminology.
