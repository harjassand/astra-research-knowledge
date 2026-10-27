# A sharp obstruction for the independent-time version

The authorized helper proved this result, and the main worker independently reconstructed it during integration. The algorithm is (A) in THEOREM.md, with k independent covariance actions, each using T uniform[0,1]. Positive integers n,k may depend deterministically on d. Fix tau,eta>0. This is an architecture result, not a lower bound for N687. It excludes the stratified-time alternative in STRATIFIED.md.

**Theorem.** For the smooth conservative 1-Lipschitz field

    g_d(x)_i=sin(x_i), F_d(x)=-sum_i cos(x_i),

if n+4k=o(d^(1/3)), then TV(Law(Y),N(0,sigma^2 I_d))->1.

The upper theorem's dimension exponent is sharp at fixed accuracy for this independent-time architecture. The field's mean is analytically easy; the result rejects this mechanism and supplies no information-theoretic hardness claim.

## Legal action versus a diagonal surrogate

With u=v/||v|| and fresh standard Gaussian xi, the heat action is exactly

    J_s(c;v)_i=v_i cos(c_i+s xi_i-s(xi.u)u_i) sinc(Ru_i),
    R=s chi_3.

Here sinc(z)=sin(z)/z and sinc(0)=1. Both |J_i|<=|v_i| and

    E||J_s(c;v)-diag(cos(c+s xi))v||^2
        <= (17/6) max_i |v_i|^2                                  (1)

hold uniformly in c,s<=1. Use |cos(a-b)-cos a|<=|b|, |sinc z-1|<=z^2/6 and |a+b|^2<=2a^2+2b^2. Summing the two errors and using E(xi.u)^2=1, E R^4<=15, sum_i v_i^2 u_i^2<=||v||infinity^2, and sum_i v_i^2 u_i^4<=||v||infinity^2 gives 2+15/18=17/6.

Apply (1) twice, using |J_1(v)_i|<=|v_i|. The squared L2 error from each four-query action J(Z) to

    Jtilde_j(Z)_i=Z_i B_ji,
    B_ji=cos(sqrt(T_j)C_ji+sqrt(1-T_j)xi_ji)
          cos(sqrt(T_j)C_ji+sqrt(1-T_j)xi'_ji)

is O(log(2d)), since E max_i Z_i^2=O(log(2d)). The k-action average has the same bound by Jensen; no independence of approximation errors is required.

Conditional on T_1,...,T_k, surrogate coordinates are iid. Put

    v0=(1-exp(-2))/2,
    q(t)=exp(-1)cosh t,
    r(t)=[1+2exp(-2)+exp(-4)cosh(4t)]/4,
    qbar=(1/k)sum_j q(T_j),
    Rbar=qbar^2+(1/k^2)sum_j [r(T_j)-q(T_j)^2].

Gaussian integration gives E B_ji=q(T_j), E B_ji^2=r(T_j). The conditional variance is

    sigma^2+delta,
    delta=(v0-qbar)/n+Rbar/(4 tau^2 n^2).                      (2)

Conditional fourth moments are uniformly bounded, since the sine average is bounded by one and B_ji is bounded by one. The squared radius per coordinate concentrates around (2) at rate d^(-1/2).

For the actual output, (1) and Cauchy-Schwarz bound the error in n sqrt(k)(||Y||^2/d-sigma^2) by O(sqrt(k log(2d)/d)) in L1, plus O(sqrt(k)log(2d)/(nd)). Both vanish under the stated query budget.

## Independent-time shell fluctuation

For uniform T,

    E q(T)=v0,
    Var q(T)=exp(-2)-1/8-3exp(-4)/8 > 0.

Suppose k->infinity. Set S_k=sqrt(k)(qbar-v0), a_d=n sqrt(k), b_d=v0^2 sqrt(k)/(4 tau^2 n). The bounded-variable CLT and (2) give

    a_d delta=-[1-v0/(2 tau^2 n)]S_k+b_d+o_P(1/n).            (3)

The conditional sampling fluctuation is O(a_d/sqrt(d)) in L2. Since n+4k=o(d^(1/3)), a_d<= (n+4k)^(3/2)=o(sqrt(d)). The target Gaussian's same scaled shell tends to zero. Pass to a subsequence on which b_d has a limit in [0,infinity]. If finite, n->infinity and (3) converges to a nondegenerate shifted normal, which has no atom at zero. If infinite, (3) diverges positively in probability. A shrinking shell event separates either case from the target with probability tending to one.

If k stays bounded, pass to fixed k. For n->infinity, normalize the shell by n; its candidate limit v0-qbar has no atom at zero. If n also stays bounded, pass to fixed n,k. Defect (2) is analytic in T_1,...,T_k and not identically zero: at all T_j=0, exp(-1)<v0 and both terms are positive. Its zero set has Lebesgue measure zero. Shell concentration again gives separation. These cases cover further subsequences of every subsequence and prove TV->1.

## Executed discrimination and stronger alternative

The helper's check_shell.py executes actual secants. At d=262144,n=8,k=1, with 256 runs, the event outside a target two-standard-deviation radial band occurred in 0.64453125 of candidate runs and 0.0390625 of target runs. The empirical event difference was 0.60546875; conditional shell prediction correlation was 0.92990095. These frequencies support the mechanism. They do not prove the asymptotic theorem or certify numerical TV for the ideal exact law. Seed, dimensions and all data are retained in helper/.

Stratifying T_j is a stronger ordinary alternative with the same query count. Its average action remains unbiased and shared-time shell fluctuation is smaller. The theorem above must not be generalized to that alternative. Its current universal upper bound remains (B); the polylogarithmic target remains open.
