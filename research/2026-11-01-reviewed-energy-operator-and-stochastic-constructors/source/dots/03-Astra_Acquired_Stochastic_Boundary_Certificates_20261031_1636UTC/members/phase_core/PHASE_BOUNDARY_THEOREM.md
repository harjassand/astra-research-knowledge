# Acquiring a finite boundary patch compatible with an unbounded rational tail

## Result and scope

The previous one-pivot construction is preserved unchanged. This continuation removes the premise that the reactive core contains only one species or that one good pivot can be supplied. A finite raw-list search acquires a service subset, several possible active hubs, and a shared satellite family. A first-hitting calculation supplies exponential weights and a rational tail recurrence. A second, genuinely finite killed-chain calculation supplies the entire inactive low-count boundary patch. Its leakage is not ignored: a structural guard ensures that every leaking layer has a negative satellite-leading coefficient, which is then verified and paid explicitly.

**Theorem (phase-core/shared-hub closure).** Under the raw-list conditions below, every reachable class is nonexplosive and positive recurrent, and its invariant law has every finite exponential total-count moment. For trusted exact rational input and any rational T>1, the construction produces a positive normlike V and explicit rational epsilon,C with

    LV <= -epsilon V+C.

The algorithm returns UNKNOWN rather than an instability claim when no qualifying partition is acquired or an explicit work budget is exceeded. Completeness is only for checking the stated finite structural architecture and completing its finite linear algebra when permitted; it is not completeness for stable reaction networks. Historical novelty and practical advantage are unestablished. All work is abstract count-process mathematics, not an operational chemistry procedure.

## 1. Exact input class, acquired rather than supplied

The input is a finite list of nonnegative integer source/product vectors and positive rational mass-action rates. Null channels can be discarded. The program verifies full weak reversibility and enumerates proper nonempty candidate service subsets S of the species. Its complement consists of satellites Z_1,...,Z_k, k>=1. Write service counts y=(y_1,...,y_m), satellite counts z, and r=sum y_i.

Every non-null reaction must be classified as one of:

1. **Monomolecular core:** source and target are in {0,Y_1,...,Y_m}, and its graph is strongly connected on that entire vertex set. Let lambda_i be the immigration rate 0->Y_i, k_ij the conversion rate Y_i->Y_j, and d_i the death rate Y_i->0; absent edges have rate zero.
2. **Shared-hub star:** for a nonempty acquired hub set H subset S, every h in H and every satellite j has both exact positive-rate edges

       2Y_h -> Y_h+Z_j       rate alpha_hj>0,
       Y_h+Z_j -> 2Y_h       rate beta_hj>0.

   There are no unclassified satellite-changing channels. The hub set is detected from the raw star edges; it is not an externally supplied partition. Every hub must have a complete positive row across all satellites.
3. **Neutral remainder:** the reaction preserves every individual service count y_i and preserves the total count N=sum y+sum z. Its degree and finite rates are unrestricted. It therefore preserves total satellite count as well.

The **boundary compatibility guard** is

    d_h>0 for every h in H;      d_i=0 for every inactive i in I=S\H.     (G)

A direct inactive-species death is not silently allowed. This guard is what prevents the finite correction from leaking back into an inactive unbounded layer. It is sufficient, not a necessary condition for recurrence.

The class has arbitrary dimension and permits several unbounded inactive phases and several active hubs. It is not the previous one-species-core/pivot class. Generic multi-hub instances need not be complex balanced.

## 2. First finite acquisition: hitting weights with equal hub values

Let t_h=0 for h in H. For inactive i, solve the finite linear equations

    sum_j k_ij(t_j-t_i)=-1.                                      (1)

These are the mean first-hitting-time equations for one service particle's conversion chain killed when it reaches H. They are used as finite linear algebra, not as a stationary fiber law. Every inactive phase has a conversion path to H: a path to 0 in the strongly connected core must reach a hub before its first death, by (G). The killed matrix is therefore transient, its inverse exists, and the solution has t_i>0.

Acquire

    L=max_(h in H) [1+sum_(i in I) k_hi t_i]/d_h,
    v_i=L+t_i,        v_h=L.

Let Q be the full single-particle conversion/death matrix. For inactive rows, Qv=-1 because those rows have no death and (1) holds. For a hub,

    (Qv)_h=sum_(i in I) k_hi t_i-d_h L <=-1.                     (2)

Thus v is positive, all hub values coincide, and Qv<=-1. This construction is the ordinary finite Poisson/M-matrix method, with its full acquisition cost charged.

Fix rational T>1 and set

    eta=(T-1)/L,       q_i=1+eta v_i.

Then q_h=T for all hubs, and q_i>=T>1 for every service species. Assign every satellite weight T. Since Q1+d=0,

    [sum_j k_ij(q_j-q_i)+d_i(1-q_i)]/q_i
       =eta(Qv)_i/q_i <=-eta/q_i.                               (3)

Define delta=min_i eta/q_i>0, alpha=max_h sum_j alpha_hj, D=max_i d_i/q_i, and B=sum_i lambda_i(q_i-1).

## 3. Acquired rational tail recurrence

Choose rational c>0 with c alpha<=delta/2; the code uses min(1,delta/(4alpha)). For integer r>=1 let

    g(1)=1,       g(r+1)/g(r)=r/(r+c).

All finite values and finite-jump ratios are exact rational products. As before,

    exp(-c)r^(-c)<=g(r)<=1.

The base tail is

    V_0(y,z)=q^y T^(sum z) g(r),       r>=1.                     (4)

For r>=2, core conversions leave r fixed. The core's weighted-linear quotient from (3) is at most -delta r. Immigration contributes at most B because g(r+1)/g(r)<=1. The additional correction from deaths is

    [c/(r-1)]sum_i (d_i/q_i)y_i <=2cD.

Therefore

    L_core V_0/V_0 <= B+2cD-delta r.                            (5)

Hub/satellite weights agree, so the exponential factor in (4) is unchanged by a star exchange. The forward-star quotient is

    [c/(r-1)]sum_(h,j) alpha_hj y_h(y_h-1) <=c alpha r,          (6)

using sum_h y_h(y_h-1)<=r(r-1). The reverse quotient is exactly

    -[c/(r+c)]sum_(h,j) beta_hj y_h z_j.                        (7)

Neutral channels contribute zero. Hence

    LV_0/V_0 <= B+2cD-(delta-c alpha)r
                   -[c/(r+c)]sum_(h,j) beta_hj y_h z_j.         (8)

Pick epsilon_tail>0 and an integer R>=2 with

    B+2cD-(delta-c alpha)R <=-epsilon_tail.                     (9)

The code uses epsilon_tail=delta/4 and an exact ceiling. Equations (1)–(9) acquire the tail uniformly over every service composition, not merely a chosen ray, a stationary phase mixture, or finitely many populations.

## 4. Second finite acquisition: the actual inactive boundary head

Define the service-head set

    F={y: y_h=0 for every h in H, sum y_i<R}.                    (10)

It is finite, despite all species being unbounded in the original process. Its size is binomial(R+|I|-1,|I|), with the convention size1 when I is empty. The satellite vector is NOT truncated; it remains arbitrary throughout this construction.

On F no star reaction is enabled. The core projection on y is autonomous and has a genuine finite killed generator Q_F when stopped on leaving F. Every head state has an executable path to exit: positive service populations have conversion paths into H, and the empty population has an immigration path followed by such a conversion path. Thus Q_F is transient.

For each possible exit y' from F, set h_0(y')=q^(y')g(sum y'). All exits have positive service total and are either active or at level R. Let Q_FB denote actual core exit rates. Acquire u by exact rational inversion:

    (-Q_F)u = 1+Q_FB h_0.                                     (11)

The inverse is nonnegative, the right-hand side is positive, and u(y)>0. Equation (11), including the actual boundary values, is checked exactly. It is NOT the homogeneous first-hitting equation or an assumed stationary distribution.

Define the complete function

    V(y,z)=T^(sum z) u(y),                       y in F;
    V(y,z)=V_0(y,z),                             y outside F.    (12)

On F, the exact full generator is

    LV(y,z)=-T^(sum z),        LV/V=-1/u(y).                    (13)

Neutral satellite motion cannot change the value, and all star propensities are zero. This is the explicit extinction/multiphase-boundary correction, including states with many satellites and no service particles.

There is an available more economical implementation: because inactive species have no deaths, Q_F is block upper triangular by r; one can solve the finite Dirichlet equations downward by population level. The current reference code uses an exact dense solve and reports its actual matrix size. No efficient complexity bound is claimed.

## 5. Compatibility: where patch leakage can and cannot occur

This is the principal obstruction, and it is not assumed away by (11).

**Inactive states outside F.** They have r>=R. By (G) they have no enabled death, conversions preserve r, and immigration increases r. They therefore cannot jump into F. Their generator is unchanged from V_0, so (8)–(9) apply.

**Active states at r>=R+1.** A core jump changes r by at most one, so any destination has r>=R. They cannot jump into F either. Stars preserve the existence of at least one active hub: a forward star consumes two hub particles and returns one; a reverse adds one. Thus (8)–(9) apply here as well.

**Potentially leaking states.** Only active configurations with 1<=r<=R remain. There are finitely many such service configurations, although z remains arbitrary. For any such y, core leakage into F changes only a finite constant quotient. Every enabled star maps active states to active states, so its g-ratio is UNCHANGED by the patch.

Let H_y be the exact core quotient at z=0 plus the positive forward-star quotient, using the true patched values at all destinations. Then for every satellite vector,

    LV/V = H_y-sum_j a_yj z_j,
    a_yj=[c/(r+c)]sum_h beta_hj y_h >0.                         (14)

Strict positivity uses both an active hub count and the full positive reverse row for every satellite. It is not inferred from global weak reversibility alone.

Set epsilon=min(epsilon_tail,min_(y in F)1/u(y)). For each leaking service configuration, acquire an integer K_y so that H_y-min_j(a_yj) Z<=-epsilon for Z>K_y. Then the exceptional states satisfy finite y and sum z<=K_y, hence form a finite set. An explicit safe C is

    max_y q^y g(r) T^(K_y) max(0,H_y+epsilon),                  (15)

omitting negative K_y. Equations (13)–(15), together with the unchanged tail, prove LV<=-epsilon V+C globally. The code computes the actual H_y, every a_yj, K_y, epsilon and C as rational values.

Without (G), a low-count inactive death can carry a tail state into the patched head while all satellite-leading slopes vanish. The present theorem does not silently extend through that interface. Such a network is rejected as UNKNOWN by this finder, even when it is stable. A general compatible finite-head search with inactive deaths remains a real open extension.

## 6. Nonexplosion, recurrence, and moments

V is positive and normlike. In the tail, every q_i and T is >=T>1 and the loss g(r) is only polynomial. On the finite service-head set, every u(y)>0 and T^(sum z) grows exponentially in the unbounded satellite total. Its finite service values therefore admit a common positive lower bound relative to any smaller exponential of N.

Stopped Dynkin applied to LV<=C rules out escape through arbitrarily large finite V-sublevels in finite time. Every such sublevel is a finite set of integer states with bounded total rate, even when neutral reactions have high degree. Hence there is no hidden explosion in a level set. Outside a finite set, LV<=-1 gives finite expected hitting time. Full weak reversibility provides enabled return paths for every population edge, so reachable sets are closed communicating classes. Finite-set regeneration proves positive recurrence.

To obtain stationary moments without assuming integrability, stopped exponential Dynkin gives P_t V<=aV+b, with a=exp(-epsilon t)<1 and b=C(1-a)/epsilon. Invariance and concavity of phi_n(v)=min(v,n) give pi(phi_n(V))<=pi(phi_n(aV+b)). The difference is bounded below by -b and tends to (1-a)V-b; Fatou gives pi(V)<=C/epsilon.

For any finite theta>0, choose rational T>exp(theta) and perform the finite construction again. The lower bound on g and the positive finite head values imply V>=K exp(theta N) for some K>0. Thus the same classwise invariant law has every exponential N moment. Constants, matrix sizes, arithmetic bit lengths and thresholds are not uniform over theta, rates, species count, or instances.

## 7. Executed five-species non-complex-balanced example

The raw input, in abstract count symbols A,E,B,D,C, is

    0 -> A             rate1/10
    A -> E             rate1
    E -> A             rate1
    E -> B, E -> D     rate2 each
    B ->0, D ->0       rate1 each
    2B <-> B+C         rates1,1
    2D <-> D+C         rates2,1.

The finder tries26 service subsets before acquiring S={A,E,B,D}, inactive I={A,E}, hubs H={B,D}, and satellite C. No grouping or good pivot is supplied. The previous one-pivot architecture cannot accept this list: 0->A forces A as that pivot, but A->E is neither its one-species core, an exact2A star edge, nor A-neutral.

The acquired values include

    t=(3/2,1/2,0,0),    L=1,
    q=(7/2,5/2,2,2),   T=2,
    c=1/28,            R=2.

The head contains the empty service state, one E, and one A. Its exact values are

    u(0)=194523/13369,
    u(E)=37735/13369,
    u(A)=60833/13369.

There are9 active leaking service configurations. The executed epsilon is13369/194523. The Foster constant is explicit but large; no useful constant-size or practical mixing-rate claim is made. There are1260 additional exact rational state challenges, separate from the all-state proof. The executed T=2 certificate alone controls moments below log2. The all-exponent theorem follows from repeating the mathematically finite construction for arbitrary T, not from extrapolating this one run. The implementation defaults to a2000-state finite-head budget and explicitly declines larger heads; raising that budget and paying the associated arithmetic would be needed for such runs. The largest finite satellite head bound in this example is191, so a three-state inactive solve does not imply small global constants.

The network is not complex balanced. Core balance forces e=1/40 and b=d=1/20. The B-star then forces satellite concentration c=b, whereas the D-star forces c=2d, a contradiction. The proof neither assumes nor computes a full stationary fiber law.

## 8. Strong conventional comparators and what remains open

Finite Poisson equations, M-matrix positivity, monomolecular/affine-process drift weights, killed-chain Dirichlet problems, and Foster-Lyapunov theory are standard machinery and receive credit. The constructive contribution under investigation is their compatible boundary-to-tail assembly, including acquired raw partition, actual exit data, and proof that all leakage has a controlled satellite-leading term. A result being non-complex-balanced is not by itself evidence of novelty: autocatalytic product-form and compatible network-decomposition theorems remain strong comparators.

A positive weighted-linear Lyapunov function cannot supply a global one-step negative drift for this class. Choose a satellite of minimum linear weight. At a fixed single hub particle and arbitrarily many particles of that satellite, reverse-star drift would be positive and linear if the hub weight exceeded the minimum satellite weight. Any enabled neutral redistribution there has nonnegative reward, since it preserves satellite total and cannot replace minimum-weight particles by lower-weight ones. Thus every hub weight is <=the minimum satellite weight. At a large isolated hub with zero satellites, the forward quadratic coefficient is sum_j alpha_hj(w_Zj-w_h); every summand is now nonnegative, so nonpositive drift requires every one to vanish. Complete positive hub rows therefore force all hub and satellite weights to coincide. The star contribution then vanishes, and the service-empty face has positive immigration drift at arbitrarily large satellite populations. An increasing function of total count likewise has positive drift there. This is a method obstruction, not instability or a novelty claim.

The general weak-reversibility conjecture remains outside this theorem. Inactive deaths, incomplete hub-to-satellite rows, several independently missing hub sets, nonlinear service cores, or arbitrary fast conservative geometry are not discharged. Their acquisition/compatibility problem is not replaced by an oracle. The present exact finder is sufficient and may reject stable networks.
