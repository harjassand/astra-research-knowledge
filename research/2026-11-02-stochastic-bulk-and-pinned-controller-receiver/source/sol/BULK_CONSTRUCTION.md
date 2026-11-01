# A stochastic bulk receiver for finite affine trapping families

Author-derived work, 2026-11-02. No independent whole audit, historical novelty claim, or complete positive-recurrence theorem is asserted. This is intended as a substantial intermediate operation toward the arbitrary-dimensional recurrence problem, rather than a new recognized chemical architecture.

## Statement being developed

Let a finite weakly reversible mass-action network have positive rates, integer complexes, finite maximal source degree D, and stoichiometric space S. Fix a positive affine compatibility class P=(c+S) intersected with the positive orthant. Suppose P contains a point c with c_i>=1; otherwise the eventual logarithmic bulk considered below is empty. The claim is that the finite affine-family construction described below yields a nonnegative normlike function V on the whole count orthant and finite constants C,N0 such that

    L V(x) <= -1

for every count state x in c+S with N=max_i x_i>=N0 and min_i x_i>=C log(2+N).

The generator is the ACTUAL falling-factorial generator. No stationarity, spectral gap, fast equilibration, normalized frozen fiber, volume limit, or mixing-time hypothesis is used. V is not claimed to dissipate on the complementary low-count faces. Those faces include the catalytic bottleneck and are the remaining central obstacle; this statement alone does not prove recurrence.

The argument uses the finite affine approximation lemma from OpenAI, *Uniform Permanence in Weakly Reversible Mass-Action Systems*, October 5, 2026, sections affine.tex and trapping.tex. That source proves a deterministic theorem and does not itself provide the stochastic receiver here. Its repository identifies the collection as research data of mixed verification status. The source lemma is a governing mathematical input, not an independently audited Astra theorem or an uncharged software oracle.

## 1. Exact smooth-minimum jump estimate

Let L_i(x)=r_i.x+b_i, i in a finite set I, theta>0, and

    Ftheta(x)=-theta log(sum_i exp(-L_i(x)/theta)).
    p_i(x)=exp(-L_i(x)/theta)/sum_j exp(-L_j(x)/theta).

Let the finitely many actual jumps be nu_e, with rates q_e(x)>=0, and set

    R=max_(i,e) |r_i.nu_e|,
    Gamma_i(x)=sum_e q_e(x)|r_i.nu_e|,
    d_i(x)=sum_e q_e(x) r_i.nu_e,
    delta=R exp(R/theta)/(2 theta).

The exact, finite-jump inequality is

    L(-Ftheta)(x) <= sum_i p_i(x)[-d_i(x)+delta Gamma_i(x)].       (1)

Indeed, for z_i=r_i.nu_e,

    Ftheta(x+nu_e)-Ftheta(x)=-theta log E_p exp(-z/theta).

Taylor's inequality exp(u)<=1+u+exp(R/theta)u^2/2, followed by log(v)<=v-1, gives

    Ftheta(x+nu_e)-Ftheta(x)
      >= E_p z - exp(R/theta) E_p z^2/(2 theta)
      >= E_p z - delta E_p |z|.

Multiplication by the actual rates and summation proves (1). This avoids applying a generator rule for a nonsmooth minimum and does not discard fast jumps tangent to a proposed slow face. Choose theta>=4 max(R,1). Then delta<=exp(1/4)/8<1/6.

If a collection G of slopes obeys d_i>=Gamma_i/2, then (1), |d_i|<=Gamma_i, and Gamma_i<=R Q, Q=sum_e q_e, imply

    L(-Ftheta) <= -(1/3) sum_(i in G) p_i Gamma_i
                 +(7/6) R Q sum_(i notin G) p_i.              (2)

If every bad slope has affine gap L_i-min_j L_j>=g, its total soft weight is at most |I|exp(-g/theta). An active good slope has weight at least 1/|I|. These constants are uniform over the offsets and the actual count state.

## 2. A source-cut inequality strong enough to pay curvature

For a slope r, order the distinct complex levels r.y. For every consecutive cut, write U_j and D_j for total actual upward and downward flux. Weak reversibility supplies an upward edge whenever a downward edge crosses a cut. If every downward source v and every upward source u below that same cut satisfy

    q_(v->v')(x) <= eta q_(u->u')(x)/m_E,

where m_E is the number of edges, then D_j<=eta U_j. The telescoping level decomposition gives, EXACTLY,

    d_r=sum_j gap_j (U_j-D_j),
    Gamma_r=sum_j gap_j (U_j+D_j).

Thus d_r>=(1-eta)/(1+eta) Gamma_r. Taking eta<=1/3 gives the hypothesis d_r>=Gamma_r/2 in (2). Rates of edges with r.nu=0 contribute to neither quantity and are not charged as if they changed the potential.

For actual mass action, if every x_i>=2D, then 2^(-D)x^y<=x_(y)<=x^y for source complexes of degree <=D. Consequently, a monomial ratio x^v/x^u<=a gives the required propensity ratio with only the paid constant 2^D kmax/kmin. No continuum approximation is made here.

## 3. What the primary affine construction supplies

The cited construction fixes one finite family of slopes r_i in [-1,1]^d, offsets b_i(h), and constants h0,H>0, independent of h, such that for all 0<h<=h0:

* F_h=min_i(r_i.x+b_i(h)) on B_h=[h,h^(-1)]^d.
* If r_i is active at x=h^p in B_h and r_i.v!=0, then r_i.v and p.v have the same sign and |p.v|>=H. This applies to coordinate vectors and ALL differences of complexes.
* There is a zero-slope label of value M_h=F_h(c), and K_h={F_h=M_h} is compact with K_h contained in the interior of [sqrt(h),h^(-1/2)]^d.
* A slope in S-perp cannot be active at a point of (c+S) outside K_h.

The first property also gives [h^H,h^(-H)]^d contained in K_h, after reducing H if needed: otherwise an active nonzero coordinate r_(i,j) would imply |p_j|>=H. The strict interior version suffices at endpoints by continuity. Reduce H further so H<1/2 and every nonzero scalar product r_i.v in the finite comparison list has absolute value at least 2H.

Only this finite-family conclusion is needed below. Its acquisition and potentially enormous constants are inherited from the governing mathematical construction; no polynomial-bit or practical implementation promise is made.

## 4. Removing irrelevant labels and acquiring a uniform near-active guarantee

For R=h^(-1), retain only labels active somewhere in the compact box [1,R]^d. The minimum on that box is unchanged. Every retained slope is coordinatewise nonpositive: a positive coordinate would force the corresponding exponent p_j to be positive at an active point, whereas x_j>=1 gives p_j<=0. Retain all tied zero labels at the least constant M_h and discard higher constant labels. There are between 1 and m labels, where m is the original finite family size.

For each retained label, its active region in [1,R]^d is a nonempty polyhedron. Hoffman's bound for its linear inequalities gives

    dist_infinity(x,T_i) <= B [L_i(x)-F_h(x)]                 (3)

for x in [1,R]^d. The coefficient matrices use only the fixed slope differences and coordinate normals. There are finitely many possible retained subfamilies, so a single finite B works for every R; the varying offsets and box bounds affect right sides, not this constant. This is a standard finite-dimensional linear-inequality error bound; it does not require an asymptotic phase or stochastic oracle. Equivalently, B can be acquired from the finitely many nonsingular row minors, with the usual feasible-polyhedron conventions.

Let n=min_i x_i, N=max_i x_i, R>=2N, and call a label near-active if its gap is <=n/(2B). By (3), it has an actual active point z in [1,R]^d with |z-x|_infinity<=n/2. Hence every coordinate ratio x_j/z_j lies between 1/2 and 2. The source construction gives, whenever r_i.u<r_i.v,

    z^v/z^u <= R^(-H),
    x^v/x^u <= 2^(|v-u|_1) R^(-H).

With n>=2D, Section 2 therefore makes every near-active label good once R exceeds one fixed finite threshold. The finite complex set and kmax/kmin pay the prefactor and number of cuts. Every remaining label has soft weight <=exp[-n/(2B theta)].

If x is in c+S and outside K_h, an active label lies outside S-perp, so some actual reaction has |r_i.nu_e|>=2H. All sources are enabled and each falling-factorial product is at least one. Thus Gamma_i>=2H kmin. Equations (1)--(3) yield

    L U_R(x) <= C1 Q(x) exp(-c1 n),                        (4)
    L U_R(x) <= -c0+C1 Q(x)exp(-c1 n) if x outside K_h,    (5)

where c0=2H kmin/(3m)>0 and c1=1/(2B theta)>0. Here the nonnegative normalized function is

    U_R(x)=theta log[(1/z_R) sum_(retained i)
                            exp((M_h-L_i(x))/theta)],      (6)

and z_R is the number of retained zero labels. They each contribute one, so U_R>=0 everywhere. Normalization changes only an additive constant. The active region and source inequalities are evaluated at actual x and actual z, not at a stationary surrogate.

## 5. A convergent scale sum and the pointwise bulk drift

Take R_k=2^k, starting at a fixed k0 large enough for all the preceding finite thresholds, and put

    p=2D+2,
    V(x)=sum_(k>=k0) R_k^p U_(R_k)(x).                    (7)

This is a well-defined, nonnegative function on the whole nonnegative count orthant. To see convergence, every retained nonzero slope has -sum_j r_(i,j)>=2H. Its affine value is at least M_h throughout [1,R^H]^d. Evaluating at R^H times the all-ones vector shows, for every x>=0 with max x_j=N<R^H,

    L_i(x)-M_h >= 2H(R^H-N).

Therefore

    0<=U_R(x)<=theta m exp[-2H(R^H-N)/theta].              (8)

The geometric-scale series with the polynomial weight R^p converges locally uniformly, including at all finitely many one-jump neighbors of x. Consequently L and the series can be interchanged at each count state.

For a large state with N=max x_i, split (7) into three ranges.

1. R<2N. Each U_R is Lipschitz in every jump by at most the fixed number Rjump=max_(i,e)|r_i.nu_e|. Its generator is bounded above by Rjump Q(x). The sum of the weights in this range is O(N^p), so its entire adverse contribution is O(N^(p+D)).
2. 2N<=R<=(2N)^(1/H). Equations (4)--(5) apply whenever n>=2D. Their total positive error is O(N^(p/H+D)exp(-c1 n)). Choosing n>=C log(2+N) with a sufficiently large FINITE C bounds this error, for example by 1.
3. R>(2N)^(1/H). Bound (8), applied also to all one-jump neighbors, bounds the whole generator tail by a geometric-scale exponential tail, O(Q(x) sum R^p exp(-c R^H)). It tends to zero as N tends to infinity, even after the fixed maximal jump is included.

There is a dyadic R in [N^(3/2),2N^(3/2)]. For large N this lies in range 2 and satisfies sqrt(R)<N. Hence x is outside K_h by the outer plateau bound. Its contribution has the negative term

    -c0 R^p <= -c0 N^(3p/2).

Since 3p/2=3D+3 and p+D=3D+2, this dominates the entire O(N^(p+D)) first range. The total positive errors in the other ranges were already bounded. Thus L V(x)<=-1 for all sufficiently large N in the logarithmic bulk, establishing the proposed receiving inequality.

V is normlike on the whole count orthant. For the same matching R, restrict F_h on the axis with one coordinate increasing and all others equal to one. It equals M_h initially, and past sqrt(R) every active branch on that axis has that coordinate's slope <=-2H: a branch with zero slope there could never become smaller than M_h. Hence M_h-F_h(x)>=2H(N-sqrt(R))-d after allowing the other coordinates to be below one. Equation (6) loses at most theta log m. Its matching term in (7) therefore tends to infinity at least as a positive multiple of N^(3p/2+1). The actual finite head and C depend on the class, finite affine family and rates.

## Remaining operation

No bulk-to-boundary join has been proved. In particular, freezing all coordinates below C log N and importing a finite-phase stationary law would be invalid: those coordinates evolve, the face can change, and the catalytic family has no uniform L2 gap. A complete theorem must acquire a compatible actual-time face receiver or replace this entire framework. The construction above is useful only if that operation can be earned; it is not a disguised claim that full arbitrary weak reversibility has been solved.

The primary planar bulk theorem of Agazzi and Laurence (arXiv:2610.31550v1, October 22, 2026) covers a different, broader-than-weak-reversible family of planar vector fields, including stabilization by noise, and explicitly requires compatible boundary estimates for its recurrence corollary. It must not be described as failing to handle the same raw assumptions without reading its hypotheses. Historical priority for the all-dimensional weakly reversible bulk receiver here remains UNKNOWN.
