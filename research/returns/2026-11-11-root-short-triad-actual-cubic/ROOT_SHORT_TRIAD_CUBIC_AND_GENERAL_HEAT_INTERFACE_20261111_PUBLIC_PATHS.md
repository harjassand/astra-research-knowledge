A short coupled triad makes a material-independent cubic response
ROOT, 11 November 2026 Brisbane

This note proves a finite-amplitude short-pulse estimate directly from the
coupled equations. Combining it with a general memory-preserving heat service
and an actual H1 packet-preparation service yields a conditional cubic gate.
The two interfaces are stated as hypotheses. This was derived while the new
P2 capture was incomplete; Section7 now binds their actual instantiation to
the complete human-supplied final. No missing helper proof is imported.
This is not the arbitrary polynomial-response compiler.

1. WHY THE PREVIOUS DIFFUSIVE JET IS NOT THE ONLY SCALING

The earlier exact diffusive triad coefficient contains the unknown factor
1/[rho(nu+rho)]. That coefficient is correct for its scaling, not a universal
obstruction to coefficient-blind nonlinear response. A much shorter nonlinear
pulse can create the cubic BEFORE appreciable diffusion. A separate general
heat service, if available, can then erase the large carrier signals while
preventing further uncontrolled Lorentz evolution.

Let kappa=2pi, q>=2 integer, Q=q^4, A=q^6, T=q^-11, m=e3. Put
 k1=Qe1, k2=Qe2, k3=-Q(e1+e2)+e3,
 b1=e2, b2=e3, b3=e1-e2.
Use the real solenoidal smooth reference
 u(0)=0,
 B(0)=H+A sum_(j=1)^3[H_j b_j exp(i kappa k_j.x)+conjugate].       (1)
Its mean is H, |H|<=M. On[0,T] set the applied force to zero. The actual
nu(t),rho(t) may be ANY measurable functions in[mu,1], mu>0. No freezing,
coefficient measurement or material normalization is needed for this pulse.

Denote by P_s the Fourier projection onto modes with k1=k2=0. Then the
nominal actual solution satisfies, for q above a computable polynomial in M,
 ||P_s B(T)-[H+kappa^2 H1 H2 H3(e1-e2)e_m+conjugate]||H1
       <=P(M)q^-2,                                               (2)
and through every fixed spatial order r,
 sup_(0<=t<=T)||(u,B-H)(t)||X^r <=P_r(M) A Q^r.                    (3)
Here X^r is the l1 Fourier norm with weight (1+|k|)^r. Fixed-order envelopes
in (3) are actual polynomial bounds, not unknown PDE norms.

2. A CONVERGENT FOURIER MAJORANT, NOT AN UNPAID FORMAL TAYLOR SERIES

Include the constant-H Alfven coupling and scalar diffusion in the linear
Fourier propagator E_k(t,s). Its pair matrix has Hermitian part
 -kappa^2 |k|^2 diag(nu,rho),
and skew-Hermitian off-diagonal H coupling. Thus ||E_k(t,s)||<=1 for every
unknown coefficient history. No commutation of its time matrices is used.

Expand the mean-zero solution into homogeneous terms Z_n in the nonconstant
initial packet; equivalently introduce a scalar theta multiplying that packet.
The degree-one term is its exact linear evolution. Degree n is supported in
the signed sums of n members of {k1,k2,k3}, and therefore |k|<=C n Q.
Let R0=C0 M A bound the initial l1 norm. Quadratic divergence nonlinearities
and the Leray multiplier give an output derivative bound C n Q. In the
degree-n Duhamel recurrence, the time integral of t^(n-2) contributes
1/(n-1). The quotient n/(n-1)<=2 leaves a Catalan-type recurrence. Hence
 ||Z_n(t)||X0 <=C^n R0^n Q^(n-1)t^(n-1),
 ||Z_n(t)||Xr <=C_r^n n^r R0^n Q^(n-1)t^(n-1).                    (4)
Increase the fixed constants to include all two-equation polarizations.
The series and its fixed spatial derivatives converge whenever C Q R0 t<1.
At our actual T this parameter is bounded by C M/q. Choose q>=C'(1+M).
The convergent series constructs the actual smooth solution on the entire
window and proves (3). Positive diffusion only improves the contraction.

Every slow output of degree n has the form r e3 with |r|<=n. The derivative
at its ROOT interaction is therefore <=C n rather than C n Q; its H1 weight
is also <=C n. Repeating the same recurrence only at this root gives
 ||P_s Z_n(T)||H1
   <=C^n n^2 R0^n Q^(n-2)T^(n-1) for n>=2.                      (5)
No estimate of a whole high-frequency field by a low-frequency derivative
is used. The improvement is specifically at the projected root.

For slow output, the three signed carrier counts must be equal to the same
integer r. Their total count n has parity r and n>=3|r|. For n=2 or4, only
r=0 is possible. The nonlinear mean is exactly zero by the two divergence
identities, so P_s Z_2=P_s Z_4=0. There is no slow degree-one initial mode.
At degree three, r=+/-1 and the only choices use each high carrier once with
the same sign. Summing (5) over n>=5 gives
 sum_(n>=5)||P_s Z_n(T)||H1
   <=C (R0/Q)(C Q R0 T)^4 <=P(M)q^-2.                           (6)
This is the uniform finite-amplitude low remainder missing from the older
diffusive-jet calculation. It does not assert that the entire high remainder
is small; its fixed-order norms are instead bounded by (3).

3. THE CUBIC COEFFICIENT IS KNOWN AND MATERIAL-INDEPENDENT

For degree three, first replace each linear propagator on the finite triad
by the identity. On frequencies <=3CQ, its error is bounded by
 C T(Q^2+M Q) <=P(M)q^-3,                                      (7)
uniformly for every actual nu,rho in[mu,1]. Duhamel's integral identity gives
this estimate directly even for time-dependent coefficients; the time matrix
norm is bounded by C(Q^2+M Q). In the projected degree-three coefficient the
corresponding absolute error is <=P(M)q^-3 by (5).

With identity propagators the first velocity coefficient is zero. For each
unordered pair a,b, c its remaining index, define
 F_ab=P_(k_a+k_b)[(b_a.k_b)b_b+(b_b.k_a)b_a],
 D_ab,c=(b_c.m)F_ab-(F_ab.m)b_c.
The exact cubic magnetic coefficient at m is
 -kappa^2 A^3 T^2 H1 H2 H3 sum_(pairs ab)D_ab,c/2.                (8)
The two time integrals give T^2/2. Solenoidality moves the outer derivative
from a high carrier onto m: b_c.(k_a+k_b)=b_c.m and F_ab.k_c=F_ab.m.
After division by Q the three D values tend respectively to
 -(e1-e2), -e1, +e2.
Their sum tends to -2(e1-e2). The finite-Q rational Leray projections have
denominators >=Q^2, so the normalized error is <=C/Q. Since
 A^3 T^2 Q=q^18 q^-22 q^4=1,
(8), (7) and (6) prove (2). The sign is positive. This is the coefficient of
exp(i kappa x3); the real cosine coefficient is twice that value.

Replacing H_j in the three initial packet signals by arbitrary prescribed
rational linear forms L_j(H) replaces the product in (2) by their product,
with the corresponding polynomial envelope. No unknown H_j is divided out.
Known constant kappa^2 can be adjusted using a rational approximation to its
reciprocal in one signal; that is ordinary finite precision, not calibration.
General output directions/frequencies and memory-safe composition still need
their own constructions. One triad does not prove arbitrary cubic outputs.

4. ROUGH ERRORS, DISTURBANCES AND ALL-WEAK REALIZATIONS

The reference bounds (3) imply
 L=sup||grad(u_ref,B_ref)||infinity <=P(M)q^10,
 D2=sup||grad^2(u_ref,B_ref)||infinity <=P(M)q^14.
Consequently L T<=P(M)/q, so the coupled L2 relative-energy exponential is
bounded after increasing q polynomially. Let incoming joint errors be e0
in L2 and e1 in H1, and disturbances have joint L2 bound eta. Relative energy
gives sup error_L2<=P(e0+eta T). The H1 inequality retains the term
 C D2 sqrt(E0 E1),
rather than putting D2 in the exponent. Young's inequality on scale T and
the ordinary cubic H1 remainder close a small-error bootstrap and give
 sup error_H1 <=P(M,mu^-1)[e1+q^3 e0+eta sqrt(T)].                (9)
Here T D2=P q^3 and mu^-3 T is polynomially small. All required incoming
errors and eta can therefore be inverse-polynomial in q and the data.
This is an actual strong perturbation on the whole interval. Same-data
weak--strong uniqueness transfers it to every corresponding energy weak
realization and its endpoint trace. No global regularity claim is needed.

5. THE TWO PRECISE PHYSICAL INTERFACES FOR A CONDITIONAL CUBIC GATE

HYPOTHESIS A: a coefficient-blind preparation service actually produces (1)
with the inverse-polynomial JOINT H1 discrepancy required in (9), from all
admitted initial data, using the same twelve actuators and polynomial costs.
An L2 headline alone is insufficient; its proof or a separate smoothing
argument must provide this real H1 interface and a paid state envelope.

HYPOTHESIS B: for ANY unknown smooth reference beta0 with supplied fixed-order
Sobolev envelope P0 and a small H1 discrepancy, a mechanical reset/hold service
occupies an exact prescribed rational interval S and gives
 ||B_out-exp(D_rho Delta)beta0||H1<=zeta,
 ||u_out||H1<=zeta,
 D_rho in[rho_- S/2,S],
with polynomial physical/binary costs in P0,zeta^-1,S^-1,mu^-1,Lambda and the
paid incoming joint H1 envelope. It uses only these envelopes, not beta0 or
the coefficient history. Near-contracting memory resets must be paid over the
whole interval; a fixed polynomial loss at each of many calls does not suffice.
This hypothesis is the general heat service. Its actual current instantiation
is bound to the complete supplied proof in Section7, not an unseen helper.

Assuming A and B, set S=q^-7 after the nonlinear pulse. Take beta0 to be the
ACTUAL smooth B(T), which may depend on H and the unknown material history.
Its envelope P0 is the explicit polynomial from (3); it is not measured.
Every non-slow Fourier mode has |(k1,k2)|>=Q, independently of its third
coordinate, even at arbitrarily large homogeneous degree. Therefore
 ||exp(D_rho Delta)(I-P_s)beta0||H1
    <=P(M)q^10 exp(-c mu q).                                  (10)
The retained cubic has fixed frequency e3 and changes by at most P(M)S.
Heat contracts the slow remainder in (2). Choose zeta<=epsilon/8 and then q
above a computable polynomial in M,mu^-1,epsilon^-1 and the time budgets.
Equations (2), (9), (10) give a conditional endpoint gate
 u_out approximately0,
 B_out approximately H+kappa^2 H1 H2 H3(e1-e2)e_m+conjugate,
uniformly in all unknown admitted profiles, without the nuisance factor
1/[rho(nu+rho)] and without observing H. Initial packet amplitude is q^6,
not the q^2 amplitude of the older packet-specific heat premise; this is why
the GENERAL service is indispensable. All envelopes and inverse tolerances
are fixed powers of q. If A and B have universal polynomial costs, so does
this fixed finite composition. It is a single physical experiment.

6. THE REMAINING WHOLE QUESTION

The pulse proves a useful finite-amplitude nonlinear operation, conditional
only on the two stated preparation/filter services. It does not construct
general spatial output polarizations, arbitrary even velocity functions,
selective preservation/reuse of nonlinear intermediate registers, or a
variable-degree polynomial compiler with universal polynomial costs. It
does not prove that repeated field-dependent operations have a common global
geometry/error budget. Those are central new operations rather than free
corollaries of a nonzero cubic coefficient.

The earlier diffusive jet and tracking obstruction remain valid at their
scopes. The new separation of a nearly ideal nonlinear pulse from a reset-
controlled heat interval changes the material-normalization interface; it
does not negate the earlier coefficient calculation. The two physical
interfaces are instantiated below from the complete available final.
No unavailable helper/component proof or held source is imported.

7. INSTANTIATION AFTER THE COMPLETE HUMAN-SUPPLIED RETURN

Harjas subsequently supplied the entire P2 final. The exact body is preserved
as P2_814186_HUMAN_SUPPLIED_EXACT_BODY_20261111.txt35723UTF8/SHA533ea905,
with the original handed-off one-terminal-LF file35724/e70d44e0 unchanged.
Its first20000characters match the earlier native prefix exactly. ROOT read
the ENTIRE supplied final; the full current activity/helper capture remains
unavailable, and its missing proof content is not assumed.

The final's Section5 equations30--36 construct HypothesisB, including an
arbitrary polynomial reference envelope, EXACT prescribed total time,
unknown effective heat amount in[rho0 S/2,S], and a single global magnetic
inequality rather than a local error summed over all cells. The endpoint
velocity U<=zeta. Reference beta0 may be unknown; only its envelope is used.

For HypothesisA use the actual construction for the finite Fourier matrix
Pi_pkt in (1), not merely its L2 headline. Section7 explicitly budgets the
magnetic writing error in H1. Section3 then resets velocity to any prescribed
inverse-polynomial H1 accuracy while preserving that smooth magnetic memory.
All intermediate reference and joint-state envelopes are polynomial, and
the total duration can be assigned before compilation. This supplies the
real joint H1 interface required by (9), with no observation of H.

Thus, under the SAME accepted baseline control constructions as that full
answer, the conditional theorem above now yields an ACTUAL coefficient-blind
nonlinear cubic endpoint operation in a single fluid, for all admitted data,
disturbances and energy weak realizations with polynomial costs. It is not
conditional on an unavailable new service. The unknown diffusion factor of
the older critical-diffusion jet has been made unnecessary by the different
time ordering. The full variable-degree response, general output operations
and a shared memory/composition ledger remain open as stated in Section6.
