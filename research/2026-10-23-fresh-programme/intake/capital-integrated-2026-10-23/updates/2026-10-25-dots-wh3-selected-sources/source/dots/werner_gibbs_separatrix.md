# An exact correlated stationary point and two basins at a=2

24 October 2026, root derivation. This corrects any temptation to classify ALL faithful stationary points as products. It does not contradict the previously proved local product uniqueness or the open global upper bound.

Let F be Swap on C3 tensor C3 and consider normalized Werner states

 X_x=exp[−(log x)F]/[3x+6/x], x>0.

Their antisymmetric eigenvalue is x²/[3(x²+2)] (multiplicity3), and symmetric eigenvalue1/[3(x²+2)] (multiplicity6). The reference marginal is I3/3. At a=2 the exact dual objective is

 Phi(X_x)=(x^4+8x)/[3(x²+2)²].

The Gibbs input is isotropic: its maximally entangled eigenvalue is x³/(x³+8), and its other eight eigenvalues are1/(x³+8). Applying W3 gives the exact one-variable update

 x_next=sqrt[(x³+2)/3].

Its positive fixed points are x=1 and x_star=1+sqrt3. At x_star, both X and the Gibbs input are faithful and genuinely correlated. By direct substitution X=W3(Y), this is a FULL stationary point, not merely stationarity within a constrained numerical family. Equivalently covariance forces the full gradient into span{I,F}, and the single normalized Werner derivative sets its traceless component to zero.

The objective at x_star is sqrt3/6<1/3. Its derivative along the Werner curve vanishes there and its second derivative is positive. Therefore this point is NOT a local maximum in the full state space; it cannot threaten the conjectured bound. It does disprove the stronger claim that all faithful stationary points are products.

## Exact dynamics and limitation of local searches

The update derivative at x_star is x_star/2=(1+sqrt3)/2>1, while the derivative at1 is1/2. Since

 x³−3x²+2=(x−1)(x²−2x−2),

all0<x<x_star except the exact unstable point converge to1. Every x>x_star increases without bound and approaches the normalized antisymmetric boundary state. The two endpoints have equal objective1/3 at a=2, separated by a finite correlated stationary barrier below them.

This explains two different outcomes of the executed search: product convergence and a singular-conditioning stop can belong to different legitimate basins, without establishing that no other basin exists. The barrier is exact, not inferred from repeated random trials. The full phase-bearing or higher-rank state geometry remains unresolved.

No general algorithmic novelty or global optimum is claimed. The all-state target remains Phi(X)<=1/3.
