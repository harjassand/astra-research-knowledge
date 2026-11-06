# Exact failed substitutions in an ordinary-capacity upper certificate

Transferred after both r2 and r4 preserved their natural initial full
attempts. Source: r4/REPORT.txt, section5.2, read in full. This supplies
a mathematical counterexample object to r2's actual divergence/upper-
certificate direction, not a preferred replacement method or a new target.

For a channel N:A->B and R isomorphic to A, ordinary coherent information
can be written

    max_{omega in image(id_R tensor N)}
       min_{sigma_B in image(N)} D(omega_RB || I_R tensor sigma_B).

For a fixed omega the inner minimum is attained at omega_B and equals
-H(R|B)_omega. The outer operation is a MAXIMUM. Replacing it by an
infimum to fit a convex-set divergence theorem changes the quantity.
For N=id_A, the wanted value is log d_A. The allowed product state
|0><0|_R tensor sigma_B makes the substituted objective zero, so an
infimum cannot return the desired positive maximum. With generalized
relative entropy and an unnormalized second argument it can be even
smaller; no equality to Q follows.

The second failure is full stabilization of

    (id_R tensor N || R_R^I tensor N),
    R_R^I(X)=Tr(X) I_R.

Allow an additional untouched system Z and choose a maximally entangled
state on RZ, independently of the physical A input. The output comparison
is then

    D(Phi_RZ tensor N(rho_A) ||
      I_R tensor (I_Z/d_R) tensor N(rho_A))=log d_R.

The conditional-entropy bound -H(R|ZB)<=log d_R makes this the stabilized
value for EVERY N. For a pure replacer N the true ordinary Q is zero;
the fully stabilized expression still equals log d_A. For the normalized
replacer convention, the divergence has an extra log d_A and the usual
subtracted normalization leaves the same erroneous constant.

These are exact finite counterexamples. They exclude those two operations,
not all possible regularized-divergence representations or algorithms.
The primary convex-set divergence/AEP sources used by r4 are identified
in its full report with their actual infimum and tensor-polar conditions.
Read a governing theorem before using it in a different optimization.

No result from r1, r2's own construction, or the lead's rate construction
is included. r4's ongoing own-depth continuation receives no peer input.
