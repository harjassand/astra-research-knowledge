# An exact nonfaithful qutrit boundary example

9 October 2026. This illustrates the scope and non-robustness of the general-map finite criterion. It is not a practical tomography classifier or a priority claim.

Write C^3=C|0> direct_sum C^2 and let N=[[0,1],[0,0]]. Fix epsilon=1/8, r=1/2, and a real parameter |t|<=1/4. Put

 C_t=N+t I_2,  R_t=r I_2-epsilon C_t* C_t.

Since ||C_t||_op<=1+|t|<=5/4, R_t>=39 I_2/128>0. Define

 Phi_t([[x,u],[v,X]])
 =[[x+(1-r)trX, epsilon u C_t*],
   [epsilon C_t v, epsilon C_t X C_t*+tr(R_t X)I_2/2]].

This is CPTP. One Kraus operator is sqrt(epsilon) diag(1,C_t). The remaining terms are positive measure-and-prepare maps: an extra (1-epsilon)x on |0>, the Q-to-|0> leakage of effect (1-r)I_2, and the Q reset of effect R_t and output I_2/2. Their input effects sum to I_3. For algebraic t the map has algebraic entries; for rational t its superoperator and Choi entries are rational.

The state |0><0| is the unique invariant density matrix. The Q population contracts by the fixed factor r at each step, so there is no faithful invariant state. Thus the published faithful-channel characterization does not directly cover this family.

For P=|0><0|, cross transfer is the row operator

 T_t(u)=epsilon u C_t*.

At t=0 it is nonzero but satisfies T_0^2=0. The Q corner theta_0 is EB already: Ad_N has a rank-one Kraus operator, and the other term is a reset. Therefore

 Phi_0^2([[x,u],[v,X]])
 =[[x+(1-r^2)trX,0],[0,theta_0^2(X)]]

is EB. Phi_0 itself is NPT because its invariant-corner cross transfer is nonzero. Its exact EB index is two.

For t!=0, the cross operator has nonzero eigenvalue epsilon t. Thus T_t^n is nonzero for every n, and every Phi_t^n is NPT. The family is continuous and Phi_t approaches the index-two channel Phi_0 as t approaches zero.

Consequently exact eventual-EB classification is discontinuous even inside an explicit algebraic CPTP family with a fixed absorbing pure state. Arbitrarily accurate unconstrained tomography cannot decide which side holds. A trusted exact structural model or a separate promise gap is necessary for an experimental decision claim.
