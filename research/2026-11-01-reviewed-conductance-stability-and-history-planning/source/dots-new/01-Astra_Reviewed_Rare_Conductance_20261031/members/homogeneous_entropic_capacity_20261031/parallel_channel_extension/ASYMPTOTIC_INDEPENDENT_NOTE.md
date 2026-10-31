# Separate review: asymptotic exactness of the parallel certificate

PASS for `ASYMPTOTIC_CONSEQUENCE_CANDIDATE.md`, SHA-256 `bcc41ca0e6c6027b289cfd26f5ba6624280393e5af7adda242b7eef711a98cec`, read in full. This is separate from executable receiving and from any claim of Markovian trajectory convergence.

The reviewed parallel theorem gives

    I_minus(alpha)/I_plus(alpha) <=k_full/k_free<=1.

Fix kappa>0 and p while alpha=m/p tends to infinity. Put x(y)=Delta(y)/a. Then x(y)=c y^2+O(y^4), c=2kappa/(1+kappa)>0. The two logarithmic exponents log(1-x(y)) and -log(1+x(y)) both equal -c y^2+O(y^4).

On the whole slab, x(y)>=7kappa y^2/[4(1+kappa)], while x(y)<=d<1. The inequalities -log(1-x)>=x and log(1+x)>=x/(1+d) bound both exponentials by exp(-alpha c0 y^2) for a fixed positive c0. After y=u/sqrt(alpha), extend the integrands by zero outside their expanding intervals. Dominated convergence with exp(-c0 u^2) gives

    sqrt(alpha) I_minus ->sqrt(pi/c),
    sqrt(alpha) I_plus  ->sqrt(pi/c).

Thus their ratio tends to one. Since these bounding functions contain no U_m, the squeeze is uniform over all admitted angular models in each dimension. Their global process/finite-partition hypotheses must still hold. No bounded coercivity sequence, convexity, angular relaxation estimate or partition computation is inserted into the proof.

The stated result is fixed-profile asymptotics. It does not establish uniformity for arbitrary kappa_m, p_m or changed basins, and does not turn a fixed numerical quadrature width into vanishing numerical error. It also does not assert arbitrary-start equilibration, mean passage times or full-path reduced dynamics.
