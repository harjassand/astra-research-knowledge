# All-orders joint spacetime emission upper bound

## Statement

For the guarded-drive, amplitude-damped qubit clock, started all ready, let epsilon=g/kappa and a=4 epsilon^2. No smallness assumption is needed for correctness (the estimate is useful when a<<1). For any ordered distinct times 0<t_1<...<t_m and any sites x_1,...,x_m, including repeated sites, the marked emission process has factorial correlation density

 r_m((x_1,t_1),...,(x_m,t_m)) <= (kappa a)^m = (4g^2/kappa)^m.   (1)

This is uniform in graph size, graph degree, times, and m. It is a genuine all-orders spacetime upper bound, not merely pairwise clustering or mixing. It bounds excess activity; it does NOT upper-bound joint missing-emission faults.

## Positive moment cone

For S a set of sites let n_S=product_{x in S}n_x, n_empty=I. Fix a>=4(g/kappa)^2. A positive, possibly unnormalized state rho belongs to C(M,a) when

 p_S=Tr(rho n_S)<=M a^|S| for EVERY S, including empty.

Claim 1: the full trace-preserving clock semigroup preserves C(M,a).

Only Hamiltonian terms centered at x in S fail to commute with n_S; guard projectors are diagonal. Damping contributes exactly -kappa |S|p_S. Positivity/Cauchy-Schwarz bounds the Hamiltonian contribution at x by 2g sqrt(p_S p_{S\{x}}). Therefore

 p_S' <= -kappa |S|p_S +2g sum_{x in S}sqrt(p_S p_{S\{x}}).       (2)

At a first boundary crossing p_S=M a^|S| while all lower moments satisfy their bounds, the right side is at most

 M a^|S| |S|[-kappa+2g/sqrt(a)]<=0.

The finite triangular differential comparison proves invariance; equivalently induct on |S| and compare sqrt(p_S) with sqrt(M)a^(|S|/2). One can first take a strictly larger than 4 epsilon^2 and then use continuity for equality. The empty moment is constant and at most M. This proof applies on the full qubit space, hence also to the invariant independent-set subspace.

Claim 2: an emission at x maps C(M,a) into C(kappa a M,a).

For the unnormalized jump map J_x(rho)=kappa sigma-_x rho sigma+_x,

 Tr[J_x(rho)n_S] = 0,                          if x in S,
                  kappa Tr[rho n_{S union{x}}], if x notin S.

The cone inequalities give the claimed multiplier kappa a. This includes S=empty, so it controls the probability density/trace as well as all remaining occupation moments.

## Arbitrary ordered jump insertions

The all-ready product state belongs to C(1,a). The factorial density is precisely

 Tr[J_{x_m} exp((t_m-t_{m-1})L) ... J_{x_1} exp(t_1 L)(rho_ready)].

Evolution preserves M; each inserted jump multiplies its permissible value by kappa a. The final empty-set inequality proves (1). Other jumps between the selected insertions are unobserved and already included in the full semigroup. Thus (1) is a factorial-correlation statement, not a probability of an exclusive jump record.

More generally (1) holds with prefactor M if the initial state lies in C(M,a).

## Product bound for disjoint spacetime cells

For a measurable marked spacetime cell C, let |C|=sum_x Lebesgue_measure{t:(x,t) in C}. For pairwise disjoint cells C_1,...,C_m,

 P[N(C_j)>=1 for every j]
 <=E product_j N(C_j)
 <=product_j [ (4g^2/kappa)|C_j| ].                         (3)

The first inequality is pointwise and the second integrates (1), summing the possible time orderings. Disjointness prevents one emission from satisfying two factors. Each factor may of course be capped only through alternative valid bounds; (3) is directly useful when its factors are small.

For any finite-volume cell C, factorial moments also obey

 E[(N(C))_m] <= [(4g^2/kappa)|C|]^m.

Consequently, for theta>=0,

 E exp(theta N(C)) <= exp[(4g^2/kappa)|C|(exp(theta)-1)].       (4)

This is Poisson-type upper-tail control, obtained by the nonnegative factorial-moment expansion. It does not imply stochastic domination in every order and cannot be applied at negative theta by alternating-series substitution.

## Non-ready initial states

For an arbitrary normalized initial state and epsilon<=1/2, comparison in (2) gives the simultaneous hierarchy

 p_S(t)<=b(t)^(2|S|),
 b(t)=exp(-kappa t/2)+2epsilon[1-exp(-kappa t/2)].

Indeed b'=-kappa b/2+g and b(0)=1. Thus after burn-in t_0 the state belongs to C(1,b(t_0)^2), with b(t_0)^2>=4epsilon^2, and the same future factorial-density bound holds with rate kappa b(t_0)^2. This is unconditional burn-in; arbitrary postselection on the earlier record need not preserve M=1, though the unnormalized cone multiplier remains valid.

## Boundary relevant to fault-path claims

These bounds control simultaneous occupation, fast/excess emissions, and all-orders marked emission moments. Desired progress failures are events N(C)=0. Upper factorial-moment bounds do NOT directly upper-bound intersections of such absence events: the generating-function expansion has alternating signs. A missing-emission product law still requires a separate lower-activity/extensive-survival argument.
