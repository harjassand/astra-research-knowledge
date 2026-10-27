# Qubit reference: a state-inversion representation and a finite bias region

24 October 2026, root derivation; independent check requested. This is an actual same-state spectral identity, not a replacement of a general reference by a qubit.

Let rho be a state on A=C3 and R=C2, with marginals rho_A and tau=rho_R. The two-dimensional reduction identity is

 X^T=(Tr X)I−J X J*,

where J is the real antisymmetric qubit unitary. Taking the full transpose of (W3 tensor id)rho and then conjugating its R factor by J* shows that the channel output has exactly the same spectrum as

 Xi(rho)=[rho+I_AR−rho_A tensor I_R−I_A tensor tau]/2.

The expression is positive for every such rho because of its channel/transposition construction, not because the individual difference terms are positive. Its reference marginal is I_R−tau, which has the same entropy as tau.

## Uniform physical input and bounded reference bias

Suppose rho_A=I3/3 and the two eigenvalues of tau lie in [1/3,2/3]. Then tau_tilde=2I_R−3tau is a density operator, and

 Xi(rho)=rho/2+(I3/3 tensor tau_tilde)/2.

Concavity of conditional entropy gives

 S(A|R)_Xi >=[S(A|R)_rho+ln3]/2.

Since S(Xi_R)=S(tau) and S(Xi)=S((W3 tensor id)rho), this is precisely

 2S((W3 tensor id)rho)−S(rho)−S(tau)>=ln3.

Therefore every extension represented by a qubit reference with this bias cap obeys the antisymmetric-qutrit target. The state may be entangled; no separability assumption is used. At tau=I2/2, Xi(rho)=rho/2+I6/12, giving the familiar depolarizing spectral relation as a special case.

## Scope and failed automatic extensions

The bias threshold is imposed by positivity of tau_tilde; its failure does not imply a violation. General qubit reference states with an eigenvalue above2/3 remain outside this construction. Reference twirling while retaining the twirl flag increases the reference dimension, so it cannot silently be used to satisfy the qubit premise.

For nonuniform rho_A, the remainder I−rho_A tensor I−I tensor tau is not the required uniform-product state. Its conditional entropy need not be ln3. The universal Weyl-flag reduction establishes equivalence of the unrestricted entropy question with uniform physical input, but does not preserve the two-dimensional reference restriction. These are distinct statements.

Universal state inversion is established prior machinery; this is a direct receiving derivation for the current conditional-entropy target. No universal entropy inequality follows merely from positivity of the inverted state.
