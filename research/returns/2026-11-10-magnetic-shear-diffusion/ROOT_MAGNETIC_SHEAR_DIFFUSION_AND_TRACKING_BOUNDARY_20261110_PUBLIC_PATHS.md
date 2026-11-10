ROOT mathematical preparation,10 November2026
Magnetic shear conjugations, actual coupled interfaces and an endpoint/tracking distinction

1. EXACT PHYSICAL MAGNETIC REPRESENTATION.
Use the unit three-torus, kappa=2pi, i!=j, F(x)=e_i s(x_j), with s=sin(kappa x_j) or cos(kappa x_j). Let
 Phi_a(x)=x+a s(x_j)e_i,
 T_a q(x)=q(x-a s(x_j)e_i),
 c=s', E=e_i tensor e_j.
The ideal induction equation B_t+(w.grad)B-(B.grad)w=0 under w=b(t)F has exact propagator
 M_a=(I+a c E)T_a, a=integral b(t)dt.
It is the volume-preserving pushforward by Phi_a, not the physical linearized Euler propagator. T_a and multiplication by c commute, E^2=0, and M_a^-1=M_-a. The Piola identity preserves divergence. For a solenoidal B, integral c B_j=-integral s partial_j B_j=0 by periodic integration in the other coordinates, so the mean is also preserved.

The explicit shear map, inverse Jacobian and finite chain rule give, for each FIXED nonnegative integer m,
 ||M_a^+/-1||_(H^m->H^m)<=C_m(1+|a|)^(m+1).
The constants include the fixed powers of kappa and are effectively bounded. This holds on all fields for the norm estimate and on the solenoidal mean-zero space for the physical interpretation. It is polynomial for long impulses. No stability of a generic magnetic velocity field is inferred.

2. EXACT CONJUGATED DIFFUSION.
Set A_a^s=M_a^-1 Delta M_a. On smooth vector fields,
 T_a^-1 partial_j T_a=partial_j-a c partial_i,
 T_a^-1 Delta T_a
 =Delta-2a c partial_ij-a c' partial_i+a^2 c^2 partial_ii.
Since M_a=T_a(I+a c E) and E^2=0, direct differentiation gives the FULL vector operator
 A_a^s=Delta-2a c partial_ij-a c' partial_i+a^2 c^2 partial_ii
       +2a c' E partial_j+a c'' E-2a^2 c c' E partial_i.
The final three terms are the stretching correction. Treating magnetic induction as scalar advection would miss them.

Average the two impulse signs. Odd terms cancel:
 (A_a^s+A_-a^s)/2=Delta+a^2[c^2 partial_ii-2c c' E partial_i].
For the sine/cosine pair, c_sin^2+c_cos^2=kappa^2 and
 c_sin c_sin'+c_cos c_cos'=0. Hence the FOUR physically compatible conjugates obey
 (1/4)sum_(s in{sin,cos},sigma in{+1,-1}) A_(sigma a)^s
 =Delta+(a^2 kappa^2/2)partial_ii.
Use the three cyclic orientations (i,j)=(1,2),(2,3),(3,1), then average their twelve conjugates:
 (1/12)sum A=(1+a^2 kappa^2/6)Delta.

This is an EXACT identity of differential operators, including the stretching terms. Its averaged linear magnetic heat equation damps all mean-zero modes at rate at least rho kappa^2(1+a^2 kappa^2/6), for magnetic diffusivity rho>0. A rational a of polynomial numerical size can make that FORMAL averaged rate arbitrarily large on a specified finite horizon. Every shear used belongs to the admitted fundamental family.

This does NOT yet construct a finite-duration common magnetic controller. Replacing an arithmetic generator average by actual shear-transit/diffusion intervals requires a uniform finite product approximation, paid commutator/high-frequency errors and Sobolev/viscous stability. M_a and the physical Euler propagator have different representations. A magnetic good average is not automatically a simultaneous stable average for velocity, and repeated nonunitary bounds cannot simply be multiplied once per sample. Those are actual mathematical interfaces, not assumed lemmas.

3. WHAT COMPOSES WITH THE COMPLETED FLUID CONSTRUCTION.
Around a known zero-magnetic carrier (w,0), write velocity u=w+v. With the carrier force w_t-nu Delta w+B(w,w)+g, the linearized pair consists of
 v_t=-L_w v+nu Delta v+g,
 B_t=-(w.grad)B+(B.grad)w+rho Delta B.
Thus a fundamental-shear word and its exact inverse reset BOTH inviscid propagators to identity: the Euler block uses the completed long-shear polynomial estimates and the magnetic block uses M_a above. The Lorentz term P[(B.grad)B] and the v/B induction terms are genuinely quadratic. No magnetic actuator is needed to define this carrier, and no initial field is known to the controller.

For the fully coupled equations set mu=min(nu,rho). The usual H1 pairing, H1/H2 interpolation and Young inequality give a conservative local estimate
 Y'+mu Z^2<=C mu^-3 Y^3+C mu^-1||f+h||_2^2,
 Y=||u||H1^2+||B||H1^2,
 Z^2=||u||H2^2+||B||H2^2,
with harmless lower-order mean-zero torus constants absorbed. This is a local continuation tool, not global control at large forcing. After subtracting a carrier and using separate moving coordinates, the required norms involve both blocks; a bound for Euler alone cannot pay the coupled bootstrap.

If an actual controlled pair has finite L-infinity H1 and L2 H2 norms on the whole interval, the standard relative-energy calculation compares it with EVERY energy-admissible weak solution with the same initial data/force/disturbance. For the pair difference E, absorb its H1 dissipation to obtain
 E'<=C mu^-3 (||grad u_strong||2+||grad B_strong||2)^4 E.
The coefficient is integrable under that strong bound. Initial E=0 therefore gives weak-strong uniqueness. A potentially large uniqueness factor multiplies zero; it is not a quantitative disturbance tolerance. This is the same distinction needed in the completed fluid all-weak transfer.

4. AN ESSENTIAL IDEAL-LIMIT OBSTRUCTION.
The zero magnetic mean is required for steering to zero on a closed torus. For smooth mean-zero solenoidal B, let A=curl^-1 B in the periodic Coulomb gauge and H_mag=integral A.B. The ideal mechanically forced system (rho=0, no magnetic disturbance/control) conserves H_mag, independently of the momentum force. Since
 |H_mag|<=kappa^-1||B||2^2,
data with nonzero helicity cannot be steered arbitrarily close to zero in L2 in that ideal model. With rho>0,
 dH_mag/dt=-2rho integral B.curl B
without magnetic disturbance, so the obstruction no longer proves a negative. Resistive cost and generated currents remain payable. Boundary-control theorems can change helicity through the boundary and do not transfer to this closed periodic model by terminology alone.

5. WHY A CONTINUOUS TRACKING SUCCESSOR IS NOT FREE.
The completed Navier--Stokes result is a fixed-time endpoint operation; its large carriers do not remain close to the target during writing. There is an elementary obstruction to replacing that contract by arbitrarily accurate strong L2 tracking of an arbitrary prescribed curve on a nonzero time interval with the same finite spatial forcing space.

Let psi be smooth solenoidal and L2-orthogonal to all twelve forcing fields. For a disturbance-free solution and a smooth prescribed V(t), suppose
 sup_(0<=t<=T)||U(t)-V(t)||2<=epsilon.
The weak equation tested against psi gives
 |integral_0^T <V_t-nu Delta V+B(V,V),psi>dt|
 <=2epsilon||psi||2
   +T nu epsilon||Delta psi||2
   +T epsilon(2sup_t||V(t)||2+epsilon)||grad psi||infinity.
This uses U tensor U-V tensor V=(U-V)tensor V+V tensor(U-V)+(U-V)tensor(U-V), so no gradient of the unknown error is required. The finite-dimensional force cancels in this test regardless of its amplitude.

For example take a fixed nonfundamental shear V=e_1 cos(2kappa x_2) with any fixed positive scale, and psi=V/||V||2. Then B(V,V)=0 and the left side is T nu(2kappa)^2||V||2>0, while the right side tends to zero with epsilon. This supplies a positive tracking-error floor. It is not a negative to the completed endpoint compiler. It prevents treating endpoint programming as full path tracking or assigning that additional consequence without an actual different control contract.

6. GOVERNING PRIMARY CONTRACTS READ.
van Veen--Goto, https://arxiv.org/html/1512.02570v1, Section2.2 equations11--19, uses the fundamental cubic-torus Kolmogorov profile, Squire/Orr--Sommerfeld energy and enstrophy to exclude linear eigenvalue instability. It does not prove arbitrary-shear stability, nonlinear global regularity or the new compiler. The completed fluid answer supplies its own polynomial propagator/commutator/Garding construction.

DLMF https://dlmf.nist.gov/10.17 equations10.17.2--3 is a FIXED-order large-argument Bessel asymptotic; the completed answer's Volterra equation supplies its additional order-uniform bound at X_n=pi[8(n+1)^2+n/2+1/4]. DLMF https://dlmf.nist.gov/10.12 equation10.12.1 gives the generating series and https://dlmf.nist.gov/10.9 equation10.9.2 gives the integer-order integral. These classical identities are not new discoveries, nor do they by themselves implement a physical fluid forcing direction.

Liao--Sueur--Zhang, https://arxiv.org/pdf/2505.07366v1, assumptions1.2a--b/Theorem1.1/Section2.2 return construction, concerns a bounded simply connected domain, a controlled boundary portion for BOTH u and B, Navier slip on the remainder, NON-RESISTIVE dynamics and H24/H8 extended initial data. Its return/flushing and well-prepared dissipation mechanisms are informative but provide neither twelve mechanical-only periodic controls nor one common H1-ball force with polynomial resources. The requested positive rho and closed-domain conditions are different, not an unmentioned specialization. No full-proof transfer is assumed from that theorem.

All constructions in this note are explicit algebra/energy arguments. No numerical run, optimizer, scientific verification job, physical experiment or new worker was used. The simultaneous nonlinear MHD common-erasure/write operation remains unconstructed.
