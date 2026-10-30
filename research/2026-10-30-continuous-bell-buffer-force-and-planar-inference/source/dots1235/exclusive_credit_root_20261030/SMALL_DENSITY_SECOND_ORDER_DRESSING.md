# A small stationary-density budget can replace exact second-order corner cancellation
2026-10-30. Root candidate simplification, not an accepted actual-generator theorem.

Suppose a local credited raw tilt has conservative local GKLS generator L_c and total killing Delta>=0. Assume both have bounded-size cones and a sum of O(N) uniformly bounded local terms. Individual Delta terms need not be positive. Let Xi be bounded self-adjoint local proof observables with bounded overlap, arranged in a fixed number of colors, and set Y=ordered product exp(epsilon_i Xi/2), G=Y†Y. All |epsilon_i|<=epsilon.

The relative dressed expression is

 B=Y^(-†)[L_c(G)-{Delta,G}/2]Y^(-1).

At epsilon=0, B=-Delta. Its first derivative is sum_i epsilon_i L_c(Xi). There is NO first-order killing commutator: Y=I+H/2+O(epsilon²), H=sum_i epsilon_i Xi self-adjoint, and

 Y Delta Y^(-1)=Delta+[H,Delta]/2+O(epsilon²);

its adjoint cancels the anti-Hermitian first-order commutator. The equivalent two-sided relative formula has the same cancellation.

For a genuinely finite-depth local circuit, each generator term cancels all disjoint factors in this relative expression. A bounded enlarged cone therefore controls its Taylor remainder. Summing O(N) terms gives a generic operator bound

 B <= -Delta+sum_i epsilon_i L_c(Xi)+C epsilon² N I.

This is a candidate standard local-circuit Taylor estimate; exact cone cancellation and derivative conventions must be checked for the actual chosen ordering. It does NOT follow merely from a global norm estimate, which could incorrectly cost N². It also requires a bounded local decomposition of the conservative tilt and killing, not just a total operator bound.

## Why a generic second-order identity remainder may be affordable
Suppose actual useful energy service is kappa=c lambda t, an exposure/activity correction has strength zeta=O(lambda t), and debt service has strength delta=O(sqrt(lambda)*t). Then

 delta²/kappa=O(t),
 zeta²/(delta*kappa)=O(sqrt(lambda)),
 lambda*zeta/kappa=O(lambda).

Thus a generic C delta² N remainder yields only an O(t) stationary energy density. A Young estimate for a zeta-sized clean/debt cross term costs zeta²/delta on the clean side, below kappa for sufficiently small lambda. Weak LOAD activity birth contributes O(lambda²t)N, also a small density. Fixed t can be chosen small before lambda; physical perturbation strength then satisfies eta<<lambda t. No zero stationary-density limit is needed to retain a fixed positive extensive energy barrier.

This does not justify ANY first-order C delta N source, a missing actual useful-coverage inequality, or a hidden condition-number cost growing with N. Such an error would overwhelm the target service. It merely shows why further exact second-order corner cancellation need not be the automatic research destination when a small macroscopic density already proves the desired barrier.

Actual debt/activity/exposure witnesses, coefficient hierarchy, and the subsequent energy-to-logical-error confinement argument remain to be composed and independently reviewed.

## Exact noncommuting two-dimensional check
Take L_c(O)=Z O Z−O, Delta=I+aZ with |a|<1, X=Pauli X, and Y=exp(epsilon X/2). Direct matrix algebra gives

 B=exp(−2epsilon X)−2I−a cosh(epsilon) Z
  =−Delta−2epsilon X+2epsilon² I−(a/2)epsilon² Z+O(epsilon³).

The first derivative is L_c(X)=−2X. Although [X,Delta] is nonzero, there is no linear killing error. This verifies the cancellation in a genuinely noncommuting fixture, not the finite-depth many-body estimate by itself.
