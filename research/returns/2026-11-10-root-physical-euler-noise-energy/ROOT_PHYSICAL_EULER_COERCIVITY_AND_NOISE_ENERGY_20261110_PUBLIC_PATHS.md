ROOT P2 MATHEMATICAL CHECK: PHYSICAL GENERATOR COERCIVITY DOES NOT IMPLY NOISE-ENERGY DECAY
10 November 2026 Brisbane. One exact analytical mode computation; no proposed physical experiment, full squeezing no-go or new historical-priority claim.

Let kappa=2*pi and L_F v=P[(F dot grad)v+(v dot grad)F] for the twelve fields e_i cos(kappa*x_j), e_i sin(kappa*x_j), i!=j. These are physical Euler generators, not passive skew transports. E155's coercivity sum||L_F v||2^2 between||grad v||2^2 and3||grad v||2^2 does not itself establish a contracting time-ordered or stochastic evolution.

Take v=e2*cos(kappa*x1). Put k=(1,0,0), Pk=diag(0,1,1). For i!=j and sig=+1,-1 set p=k+sig*ej and
 T=Pp*(k_i I+sig*ei*ej^T)*Pk,
 Tback=Pk*(p_i I-sig*ei*ej^T)*Pp,
where Pp=I-p*p^T/|p|^2 and P0=0. Exact rational matrix multiplication gives
 sum_(i!=j,sig)T^T*T=diag(0,4,4),
 sum_(i!=j,sig)Tback*T=diag(0,2,2).
These identities can also be checked term by term from the displayed twelve rational matrices; the zero output mode vanishes by incompressibility. ROOT evaluated the sums with exact fractions, not floating-point fixtures or a finite-frequency extrapolation.

Combining sine/cosine contributes kappa^2/2 to the first identity and -kappa^2/2 to the return-loop identity. Orthogonality of Fourier modes gives exactly
 sum_F ||L_F v||2^2=2*kappa^2*||v||2^2,
 sum_F <v,L_F^2 v>=-kappa^2*||v||2^2.
For any Fourier Galerkin projection P_R containing all k+/-ej intermediates (R>=2 suffices), define A_F=P_R L_F P_R and consider the finite linear Stratonovich SDE
 dV=-sum_F A_F V circle dB_F, V(0)=v,
with independent standard Brownian coordinates. Finite-dimensional linear SDE existence is sufficient; no infinite-dimensional stochastic PDE assertion is needed. Ito's formula gives
 d/dt E||V_t||2^2 at t=0
 =sum_F[<v,A_F^2 v>+||A_F v||2^2]
 =kappa^2*||v||2^2>0.
All needed intermediate modes lie inside the projection, so the selected-mode derivative is the exact physical-generator calculation.

Thus replacing the deterministic control problem by equally weighted rapid random shear switching and invoking only sum||L_F v||2^2 coercivity does not automatically yield mean-square contraction. The pressure/stretching correction has a real second-order energy cost. This is an obstruction to that inference, not to every random construction, deterministic zero-return word, compact H1-to-L2 squeezing condition or the full viscous additive-force compiler. It does not replace the separate geometric-optics essential-L2-norm obstruction.

The completed E155 H1/allweak fast-return transference, weighted SJ finite certificate and their true WE existence condition remain accepted at their stated scopes. ROOT uses this calculation to distinguish coercivity, averaged amplitudes, mean-square energy and a single uniform deterministic propagator. No method is imposed. Source: P2_XI_E155_RECOVERED_RETURN.md41838UTF8/SHA7fdbfe01a28749a0ce6727e684f07b949a853378aedd2a70b0803a47554e6a17; earlier interrupted material is not independently labelled completed science. All inherited source/access/transfer/resource holds remain.
