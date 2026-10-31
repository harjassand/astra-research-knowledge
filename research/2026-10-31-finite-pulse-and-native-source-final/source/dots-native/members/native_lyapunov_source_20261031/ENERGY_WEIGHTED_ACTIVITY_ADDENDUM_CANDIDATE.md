# Energy-weighted injection rather than the global interaction norm

31 October2026. Root candidate, pending independent review. This sharpens the native physical-count lemma only. The complete compiler must be re-bound separately before its improved overall complexity is claimed.

Retain G=sum D[L_a], H=sum L_a†L_a/2, gQ<=H<=hQ and G†H<=-kappa H. Let K be the actual Hermitian source-system coupling. Assume acquired upper certificates

r_E^2 >= ||P K H K P||,
a_E >= ||H_Q^(-1/2) Q i[K,H] Q H_Q^(-1/2)||.

Here the inverse is only on Q. Neither an optimal norm nor an inverse-energy oracle is supplied for free; concrete structural bounds may instead certify these numbers.

For any normalized joint state rho and E=Tr(H rho), splitting into P/Q blocks and applying Cauchy-Schwarz in the H energy form gives

|Tr(i[K,H]rho)| <= a_E E + 2 r_E sqrt(E).

Indeed the QQ part is bounded by a_E H as a quadratic form. For the cross part, write the two factors H^(1/2)K P and H^(1/2)Q; their expectation is bounded by r_E sqrt(E). This is a statement on arbitrary joint states and reference extensions, not Jensen applied to an unnormalized tilted state.

Use exactly the previous tilted weight W=I+aH, a=4u/kappa, u=e^theta-1<=min(1,kappa/(16h)). Its source drift is <=-a kappa H/4. If

sqrt(lambda)>=8 a_E/kappa,

the QQ Hamiltonian drift is absorbed by half that negative term. Optimizing the remaining energy expression gives

-(a kappa lambda/8) E+2a r_E sqrt(lambda E)
 <=8a r_E^2/kappa.

Therefore

L_theta†W <= (32u r_E^2/kappa^2) W,
E exp(theta N(T)) <= 2^(p+1) exp(32u r_E^2 T/kappa^2).

The same prescribed-instrument, arbitrary-input, reference and actual-unraveling restrictions apply. A sufficient count cap is the ceiling of

[(p+1)ln2+ln(1/delta)+32u r_E^2T/kappa^2]/theta.

The leading driven activity is r_E^2T, not h^2 b^2T/g. The allowed tilt still depends on h/kappa, so initial energy, control insertions and tail terms are not made dimension-free. This does not by itself alter the previously reviewed first-event window, bridge or gate counts.

## Explicit acquired certificates for the direction-merged Gibbs family

Use H=sum_j Pi_j and K=sum_i A_i tensor Z_i from the native Gibbs binding, with ||A_i||<=alpha_i. Each Pi_j flips only spin j and is diagonal on its neighbors. Consequently Pi_j commutes with Z_i when i!=j. Since Pi_j psi=0,

Pi_j Z_i psi=0 for i!=j.

All cross terms in P K H K P vanish except i=j=l. Hence

P K H K P = sum_j <psi|Z_j Pi_j Z_j|psi> A_j^2 tensor P,
||P K H K P|| <= sum_j alpha_j^2.

This bound is exact structural arithmetic; no expectation estimation is needed. It does not require the A_i to commute. It also survives nonzero fields, although exact mean centering for the full compiler must then be acquired separately.

Furthermore [K,H]=sum_i A_i tensor[Z_i,Pi_i]. A controlled two-dimensional rank-one projector obeys ||[Z_i,Pi_i]||=2sqrt(r0 r1)<=1. Thus an acquired bound is

a_E <= (sum_i alpha_i)/g.

Using these certificates removes the artificial global factor h^2 from the physical driven-count estimate. Spectator source size can still affect preparation, encoding, return, initial energy and output costs.

## A separate offdiagonal coupling certificate, not yet a new compiler

For the zero-field open chain, <Z_i Z_j> is the product of tanh J along their unique path. If t=max_i |tanh J_i|<1, the correlation matrix C has

||C|| <= (1+t)/(1-t).

Write the system operator stack B v=sum_i |i>A_i v. Exact centering gives

P K Q K P = P K^2 P,
<psi|K^2|psi> = B†(C tensor I)B
 <= [(1+t)/(1-t)] sum_i A_i^2.

Thus ||Q K P||^2 <= [(1+t)/(1-t)] sum_i alpha_i^2, at most (41/39)sum_i alpha_i^2 under |J_i|<=1/40. This could price P/Q interaction blocks separately from the QQ block norm b=sum alpha_i in a refined positive-sector construction. Amplifying a supplied K/b block to a smaller certified offdiagonal normalization is a real operation with a normalization-ratio cost; it is not supplied for free here. No improved complete simulator or practical crossover is asserted by this certificate alone.
