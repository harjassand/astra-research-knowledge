# Computable global W1 nearest-paid-law optimization

## Result and scope

Let Sigma be the boundary of the 3 by 3 correlation elliptope E, let

    Z(x,y)=(cos x, cos y, cos(x+y)),   mu=Z_# Haar(T^2),
    q(d)=d1*d2+d1*d3+d2*d3,

and let C be the weak closure of complete finite zero-root null-tree laws, including finite mixtures. Distances below are Euclidean in coefficient coordinates. The audited positive-accuracy GLOBAL reward oracle implies the following effective, end-to-end conclusion:

For every rational epsilon>0 an algorithm terminates with an explicitly specified complete paid law nu, rational numbers 0<=L<=delta<=U, and

    delta=min_{eta in C} W1(mu,eta),
    W1(mu,nu)<=U,       U-L<epsilon.

Thus nu is an epsilon-nearest paid law. The output contains a rational finite-mixture primal witness and a verified global polynomial dual witness, with every quantization, integration, oracle, and LP error paid. There is no useful runtime claim. This is a positive-accuracy computation, NOT an exact-membership decision. Delta=0 is not finitely decidable by this procedure. If delta>0, sufficiently fine calls eventually return L>0 and a genuine global separating reward.

The numerical execution recorded here is the warm-start interval [0,39/100] at epsilon=2/5, using the already certified actual AC law. It is not a newly improved .39 bound, and it is not an executed small-epsilon unrestricted optimization. The executable receiver below can consume certified global oracle responses; the previously audited arbitrary-reward oracle is a terminating mathematical algorithm, not an existing fast library. A new algebraic lower-search simplification is proved in Section 1.

## 0. Global Kantorovich minimax identity

Normalize 1-Lipschitz functions by fixing their value at one boundary point. This is a compact convex family in the uniform norm, by the uniform diameter bound and Arzela-Ascoli. The paid set C is compact and convex in the weak topology. The bilinear payoff (f,nu) -> mu(f)-nu(f) is continuous. Compact convex minimax and Kantorovich duality therefore give

    delta = min_{nu in C} max_{Lip(f)<=1} [mu(f)-nu(f)]
          = max_{Lip(f)<=1} [mu(f)-sup_{nu in C}nu(f)].

The following finite receiver is an effective realization with explicit error costs. It does not rely on evaluating an exact infinite-dimensional maximizer or deciding whether delta vanishes.

## 1. Brownian integration is unnecessary for the W1 lower oracle

For y=(u,v,w) in the INTERIOR of E, set

    a_minus=vw-sqrt((1-v^2)(1-w^2)),
    a_plus =vw+sqrt((1-v^2)(1-w^2)).

The complete u-axis chord has endpoints (a_minus,v,w),(a_plus,v,w) and probabilities

    p_minus=(a_plus-u)/(a_plus-a_minus),
    p_plus =(u-a_minus)/(a_plus-a_minus).

It is an actual binary null split, stays in E, ends on Sigma, and preserves its parent exactly. Its conditional variance is the exact identity

    E|Y-y|^2=(a_plus-u)(u-a_minus)
             =(1-v^2)(1-w^2)-(u-vw)^2
             =F(y)=1-u^2-v^2-w^2+2uvw.

For z in Sigma with |y-z|<=h<=1, |grad F|<=4 sqrt(3)<7 on the cube. Consequently

    E|Y-z|^2=F(y)+|y-z|^2<=7h+h^2<=8h,
    W1(Law(Y),delta_z)<=sqrt(8h).                         (1)

This is uniform even at edges and vertices. It does not claim boundary-root refinement: the split starts at the interior point y, and its whole law approaches a point mass as y approaches the boundary.

Dilate a finite target null tree about zero and approximate its split directions and the two positive branch lengths recursively by dyadics, exactly as in the audited nested-helper proof. All internal parents and children are strictly interior dyadic points, every new split is exactly null and barycentric, and the finite approximating tree converges to the target tree. Append the above chord at every leaf. Formula (1) pays the final receiving error. Hence these FINITE trees, with finitely many quadratic-algebraic boundary atoms, are weakly dense in C.

This gives a simpler effective lower oracle: enumerate dyadic finite interior null trees, append algebraic axis chords, and evaluate the finitely many atom rewards using certified square-root and reward intervals. No Brownian quadrature, nonabsorbing policy, or occupation inverse is needed. The physical law is the exact algebraic law, never its rounded atomization. Fair enumeration is complete by density. An efficient optional finite-horizon dynamic program on each dyadic helper mesh produces the same increasing lower search.

This simplification is for weak/W1 and Lipschitz rewards. Brownian smoothing remains useful for AC/affinity, and no finite atomic output is asserted AC.

## 2. Rational finite quantization

Fix h=2/n, where n is a positive integer. Let c_i be ALL grid nodes of [-1,1]^3 with this spacing. Let lambda_i be the tensor products of the usual one-dimensional piecewise-linear hat functions. On the cube,

    lambda_i>=0, sum_i lambda_i=1,
    lambda_i(z)>0 => |c_i-z|<=sqrt(3)h<2h.

The Markov quantizer Q sends z to c_i with probability lambda_i(z). Thus

    W1(rho,Qrho)<=2h                                      (2)

for every cube-supported probability law. Grid nodes outside E are ONLY transport intermediaries; they are never called paid physical states.

Choose rational gamma in (0,1/2]. Round each Euclidean grid distance UP to a multiple of gamma and take the all-pairs shortest-path metric d. Then all entries are rational and

    |c_i-c_j|<=d_ij<=|c_i-c_j|+gamma,   diameter(d)<4.       (3)

The left inequality follows on every path from the Euclidean triangle inequality; the right inequality follows from the direct edge. Set d_ii=0.

A normalized d-Lipschitz potential v has |v_i-v_j|<=d_ij and osc(v)<4. Its lift

    f_v(z)=sum_i v_i lambda_i(z)

is a computable Lipschitz reward, so it is a legal GLOBAL oracle input. Along a coordinate segment its slope is a convex combination of adjacent differences divided by h. Therefore a valid global Euclidean Lipschitz bound is

    Lip(f_v)<=2(1+gamma/h).                              (4)

A rational bound on its absolute value is max_i |v_i|. Exact tensor-hat evaluation is rational at rational inputs.

## 3. Actual source evaluation and paid columns

Use an M by M uniform torus grid. Certified cosine intervals supply rational cube points x_ab satisfying |x_ab-Z(2pi*a/M,2pi*b/M)|<=e. Put

    p_hat=(1/M^2) sum_ab Q(delta_x_ab).

Every entry is rational, nonnegative, and their sum is EXACTLY one. Coupling each torus cell to its node, then to x_ab and the randomized grid quantizer, gives

    W1(mu,p_hat)<=beta:=10/M+e+2h.                       (5)

Here the phase-map covering constant is the already audited sqrt(6)pi/M<10/M. The same nearest-node torus cells are exactly equal mass. The cosines in (5) are certified intervals, not rounded nodes silently substituted for the source.

For each returned actual paid law nu_s, compute a rational probability vector q_hat_s with

    ||q_hat_s-Qnu_s||_1<=b.                              (6)

This is effective because each lambda_i is Lipschitz. For the new finite algebraic lower laws, it is just a finite radical interval sum. For the original nested Brownian policy, use its audited deterministic integrator. To turn component intervals into a probability vector, take nonnegative rational lower endpoints l_i and allocate the residual 1-sum l_i to any one node. If sum of interval widths<=b/2, (6) follows from the total missing mass. This pays positivity and normalization, not only individual scalar errors.

For every d-Lipschitz v and two probability vectors differing by L1<=b,

    |v dot(q_hat_s-Qnu_s)|<2b.                           (7)

It is osc(v), not its possibly arbitrary additive normalization, that enters this estimate.

## 4. Exact restricted transport LP and global pricing

Maintain finitely many actual paid laws nu_s and their certified columns q_hat_s. Solve the rational restricted problem

    W_hat=min_{alpha in simplex} T_d(p_hat,sum_s alpha_s q_hat_s).

Return a rational feasible primal mixture/coupling of cost W_pr and a rational feasible dual potential v. Let

    H=max_s v dot q_hat_s,
    W_du=v dot p_hat-H,
    0<=W_pr-W_du<=ell.                                  (8)

An exact rational LP is one option (ell=0); a rigorously repaired numerical primal/dual pair is equally acceptable. Finite rational LP algorithms suffice. Uncertified floating solver output is not used.

Call the GLOBAL positive-accuracy oracle on f_v. It returns an actual paid law nu_new, a certified lower A, and a verified rational polynomial P such that

    A<=nu_new(f_v)<=sup_C nu(f_v)<=B=P(0),
    B-A<a.                                               (9)

Define the global pricing gap g=B-H. The following numbers are certified:

    U=W_pr+beta+2h+2b,
    L=max(0, v dot p_hat-B-beta-2h-gamma).                (10)

The actual returned primal is nu=sum_s alpha_s nu_s, not its quantized vector. Equations (2),(3),(5),(6) and the rational primal coupling give W1(mu,nu)<=U.

For the lower receiving, define the genuine Euclidean 1-Lipschitz reward

    g_v(z)=min_i (v_i+|z-c_i|).

Equation (3) gives v_i-gamma<=g_v(c_i)<=v_i. At every boundary point, averaging g_v(z)<=v_i+|z-c_i| over the quantizer gives

    g_v(z)<=f_v(z)+2h.

Hence the VERIFIED polynomial P+2h is a global null-concave majorant of g_v on Sigma, and

    mu(g_v)>=v dot p_hat-gamma-beta,
    sup_C nu(g_v)<=B+2h.

Their difference gives exactly the untruncated lower bound in (10). Thus L>0 carries an actual global source-separating reward and polynomial majorant, not a finite-family LP dual mislabelled as global.

The primal/dual interval width satisfies

    U-L <= ell+g+2beta+4h+gamma+2b.                       (11)

If g is negative, this inequality remains valid; accepted certificates cannot make a true lower exceed the true primal upper.

## 5. Finite termination, with no hidden compactness oracle

Fix a positive rational stopping threshold t. Stop if g<=t; otherwise compute q_hat_new satisfying (6), append its actual law, and repeat. Require

    s:=t-a-2b>0.                                        (12)

When g>t, (7),(9) imply

    v dot q_hat_new > H+s.

For every previous column q_hat_j, osc(v)<4 implies

    ||q_hat_new-q_hat_j||_1>s/2.                         (13)

All columns lie in the finite-dimensional probability simplex. There are only finitely many mutually separated points at this fixed positive scale. Explicitly, partition each of the N coordinates into intervals of width s/(4N); two vectors in one box have L1<=s/4, so at most

    (ceil(4N/s)+1)^N

columns can be added. This supplies a finite bound on the NUMBER of pricing calls. Individual oracle calls have no claimed practical runtime, but terminate by the audited theorem. Numerical stagnation is not the stopping test.

One concrete choice for 0<epsilon<=1 is

    h<=epsilon/64,  M>=320/epsilon, e<=epsilon/64,
    gamma<=epsilon/32, b<=epsilon/64,
    a=epsilon/32, ell<=epsilon/32, t=epsilon/4.

Then s>=3epsilon/16>0 and (11) is at most 9epsilon/16<epsilon. (Use a slightly finer integer grid when necessary.) For larger requested errors one can use epsilon'=min(epsilon,1); all costs remain finite. The actual complete mixture is an epsilon-nearest law. Compactness of C gives existence of a nearest law, but the algorithm does not require choosing an exact minimizer.

Finite atomic nu can optionally be globally dilated and Brownian-completed to an actual AC paid law. Reserve a separate positive budget and pay the already audited sqrt(24 eta) W1 smoothing cost. This is whole-law zero-root smoothing, not illegal boundary-root refinement.

## 6. Implementation and obtained execution

`certified_w1_receiver.py` implements rational metric rounding, tensor-hat features, interval-to-simplex receiving, exact rational restricted primal/dual LPs with independent feasibility/value checks, the global pricing-gap receiver, and a column-generation loop parameterized by the audited global reward oracle. The oracle interface explicitly carries the actual law and accepted global polynomial certificate; a restricted optimizer cannot satisfy this interface merely by returning its finite value.

`run_receiving_checks.py` checks the exact chord variance, its source-specific boundary receiving, radical-law feature evaluation, rational source moments at a coarse quantizer, nontrivial exact finite transport/mixture pricing, adverse column-rounding cases, and the original-source warm start. No claim is made that tests of a finite synthetic pricing backend execute the unrestricted Morrey oracle.

The original-source execution reads the already certified refined AC-law receipt and obtains

    0<=delta<39/100<2/5,
    W1(mu,nu_AC)<39/100.

The lower certificate is the exactly verified reward/majorant pair f=P=0. Thus this is an executed epsilon-nearest-law certificate at epsilon=2/5. It does not improve the existing numerical upper bound. Arbitrarily small positive-accuracy computation is established by the complete receiver plus the audited oracle theorem, not falsely reported as already run.

## 7. Executed nontrivial GLOBAL support-oracle bracket

The separate `OBTAINED_GLOBAL_CUBIC_ORACLE_BRACKET.md` records a nontrivial executed support-oracle query for f=uvw, combining the actual complete algebraic paid tree with an exactly verified rational quartic null-concave majorant. This is a genuine unrestricted lower/upper reward bracket beyond the [0,.39] nearest-law regression. It is not an executed fine-accuracy nearest-source optimization. The latter still requires sufficiently fine source features and many global pricing calls; the full tensor grid and dense transport matrix are the principal implementation-scale bottleneck, not a missing mathematical receiving inequality.
