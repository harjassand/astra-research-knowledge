# Capability audit: the70 primitive is not needed for the local inverse

The sol11 theorem and its independent reviews remain valid and frozen.
This audit challenges its downstream leverage, not its correctness.

For the same calibrated supports ell_A, define the ordinary construction

    S(z)=sup_A ell_A(z)+kappa|z|^2.

The graph supports bound this supremum above using two actual graph
atoms, and a fixed support bounds it below. Thus S is finite, globally
2kappa-strongly convex and graph-exact. The70 value always lies above S.
On the certified graph neighborhood, the PD69 certificate proves that
one actual support attains the70 value. Therefore S=G70 throughout that
neighborhood. All local values, gradients, analytic inverse charts,
characteristic segments and Fenchel pairs already computed there belong
to S as well, with the same conditioning and the same local Newton step.

This equally informed comparator uses the same acquired jet and support
certificates. The70 construction adds a finite convex global SDP closure;
it has not been shown to add a local entropy/inverse capability or a
physical response advantage. Generic strong-convexity inverse and conjugate
bounds apply equally to either function. A physical entropy augmentation
is also established machinery, with additional PDE hypotheses; it should
not be counted as a new theorem merely by inserting this energy.

Accordingly the70 branch is DEPRIORITIZED as an operational inverse/PDE
advantage. Its finite graph-exact analytic-near-graph representation is
retained as the actual mathematical result. No global equality S=G70 or
global algorithmic advantage is inferred.

A shorter independently developed receiver is in COMPATIBLE_INVERSE.md.
It uses the ORIGINAL no-C2-lift energy and candidate contact coercivity,
without an epsilon energy modification, an off-graph extension, or a
1/(2kappa) penalty. It is explicitly qualified to compatible five-coordinate
data. The script supplies an executable noisy-data test and same-data
coarse comparator, together with an exact stress-only ambiguity control.

## Global inverse and off-graph gauge comparison

The old compensated15-moment value also has a finite global conjugate
operation. Let f=F-kappa q^2+(epsilon-kappa)T, m=(A,q), and K15 be its
moment value plus kappa|z|^2. Directly eliminating z gives

    K15*(w)=max_y {w:L_y m-kappa|L_y m|^2-L_y f},
    y0=1, M2(y)>=0.

This is an ordinary concave-quadratic maximization over the SAME15 PSD
moment matrix, with70 moments. The maximizing state L_y m is unique
because K15 is strongly convex, even if its moment witness is not.
Thus global finite inverse/conjugate optimization is not exclusive to70.
K15 is a different representative and lacks the new analytic graph chart;
we do not combine properties of different functions into a false claim
that the original15 representative is itself analytic.

An exact discriminating comparison exposes the constitutive ambiguity.
Take kappa=1/20000000 and force w=(0,0,0,0,1/10^11). The frozen normal
strip gives for the new calibrated representative

    grad G70*(w)=(0,0,0,0,1/10000), G70*(w)=5e-16.

For K15, f(A)-w_s q(A) is SOS: F-kappa q^2 has a PD10 Gram, and
(epsilon-kappa)T-w_s q is PSD since |w_s|<=2(epsilon-kappa).
Hence K15(z)>=w:z+kappa|z|^2, with equality at z=0, so

    grad K15*(w)=0, K15*(w)=0.

Both representatives have EXACTLY the same physical graph energy
F+epsilon T. Their incompatible inverse outputs concern the auxiliary
off-graph state, so this difference cannot identify a more accurate
physical constitutive prediction. In general the on-graph entropy jet
is (DW-lambda cofA,lambda), whose contraction with Dm is always DW.
The normal multiplier and its off-graph response are not fixed by W.

The experiment records this exact comparison alongside the original
energy's stress ambiguity. A mathematical entropy chart can be useful
once its auxiliary-variable contract is chosen. No independently
acquired physical five-coordinate measurement or model requiring this
particular gauge is supplied here. The new compatible inverse is
therefore retained as a qualified mathematical receiver, while broader
physical/algorithmic superiority claims remain NOT_ESTABLISHED.
