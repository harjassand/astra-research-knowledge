# Acquiring a projective Foster correction from leading support accessibility

## Result, scope and what is acquired

Consider a finite mass-action count process on n>=2 species. A distinguished species A has the only nonconservative channels, 0->A and A->0, with positive rates lambda and mu. All other channels conserve total count N and have order at most p, where p=max(2, maximum internal source order). Assume the full reaction graph is weakly reversible.

Use only the internal channels of order exactly p. Starting from a singleton species support, repeatedly add the product species of any channel whose source species are all already present. This is **leading support closure**, not a claim that one actual particle can fire a p-particle channel.

**Structural theorem.** If this closure reaches A from every singleton, then every communicating class of the count process is nonexplosive and positive recurrent, and its invariant probability has every finite exponential total-count moment. This holds for every choice of positive real rates on this fixed raw list.

**Constructive rational theorem.** For positive rational rates, the finite support test followed by unbudgeted exact rational polynomial-cone search acquires, for each rational t>1, a function

    W(x)=t^N [1-epsilon H_d(x)/(N+1)^(d+p-2)]             (1)

and rational constants C0,kappa>0 such that

    LW/W <= C0-kappa N                                   (2)

at every integer state. No stationary fiber law, good weight, smooth Lyapunov function or decomposition is supplied. The polynomial H_d and its degree are acquired. A finite computation budget may return UNKNOWN for explicit quantitative certificate acquisition; a successful support test separately satisfies the qualitative structural theorem.

**Exact acquisition boundary, not general stability completeness.** Leading support accessibility is equivalent to existence of some degree in the strict polynomial cone defined below. If the support test fails, its closed-face witness rules out that cone at *every* degree. This still leaves network stability UNKNOWN; a stable unary network provides an explicit counterexample to stability completeness.

The proof combines ordinary Foster, Euler, simplex and Pólya ideas. The explicit bridge from raw support closure to an acquired count-normalized certificate is the construction here. No general weak-reversibility theorem, historical priority or practical worst-case efficiency is claimed. The formal termination witness has enormous disclosed degree and is not silently materialized.

## 1. Raw recognition and the finite degree cone

The receiver enumerates the open coordinate from the raw list. It checks positive 0->A and A->0 rates, total conservation of every remaining non-null channel, and full weak reversibility. Null channels may be discarded and duplicate positive rates aggregate. Inputs to the exact prototype are trusted nonnegative integer stoichiometries and positive int/Fraction rates; this is not a hardened hostile-input interface.

Write m=n-1 and let B_1,...,B_m be the other species. For each d>=1, put

    H_d(x)=sum_(|alpha|=d) binom(d,alpha) c_alpha x^alpha,
    0<=c_alpha<=1.                                      (3)

No useful coefficient is fixed or supplied. In particular c_(d e_A) need not be one. The coefficient box gives

    0<=H_d(x)<=N^d,
    0<=partial_A H_d(x)<=d N^(d-1)                       (4)

on the nonnegative orthant. These follow by comparison with N^d and its derivative.

Expand the **exact discrete** internal generator L_int H_d as a polynomial, using falling-factorial propensities and finite shifts. Let

    q=d+p-1,
    G_q = homogeneous degree-q part of L_int H_d,
    R = L_int H_d-G_q,       degree R<=q-1.               (5)

The leading polynomial also equals v dot grad H_d, where

    v(y)=sum_(order-p channels u->u') kappa y^u (u'-u).   (6)

All coefficients are linear in c_alpha. On the face A=0 impose:

- the coefficient of each pure B_j^q is at least beta;
- every other degree-q boundary coefficient is nonnegative;
- 0<=beta<=M_beta, where M_beta is an explicit finite coefficient bound.

One valid M_beta is max(1, maximum over pure boundary coefficients of the sum of absolute coefficients of its affine form on the c-box). It does not exclude any positive feasible beta. The all-ones c, beta=0 is feasible since H=N^d is internally conserved.

This is a compact rational polytope. Enumerating all full-size constraint bases, solving each nonsingular system exactly, and checking all inequalities decides whether beta>0 is feasible. A positive feasible point implies a positive-beta extreme point; active normals at a vertex span the ambient space even when the polytope lies in a proper affine subspace. Therefore exhaustive basis enumeration is complete for this degree cone. It does not require a floating proposer or an external coefficient oracle.

The degree cones are nested in the appropriate sense: H_d -> N H_d preserves the Bernstein box by degree elevation, L_int(NH)=N L_int H by total conservation, and all boundary coefficients remain nonnegative with positive pure ones. Thus a successful degree has successful higher-degree lifts.

## 2. One exact cone gives a global stochastic inequality

For an accepted polynomial define, by exact coefficient extraction,

    K = sum of absolute values of negative coefficients of G_q
        whose monomials contain A,
    C_R = sum of absolute values of all coefficients of R.

Writing a=x_A and b=sum_j x_(B_j), every A-containing degree-q monomial is bounded by a N^(q-1). Every remainder monomial is at most (N+1)^(q-1). Hence

    L_int H_d >= beta sum_j B_j^q-K a N^(q-1)
                                      -C_R(N+1)^(q-1).  (7)

The elementary power-mean inequality gives sum_j B_j^q>=b^q/m^(q-1).

For any t>1 let

    D=mu(1-1/t),
    epsilon=min(1/2,D/(4K)) if K>0, else epsilon=1/2,
    h=1-epsilon H_d/(N+1)^(q-1),       W=t^N h.

Since p>=2, (4) gives 1-epsilon<=h<=1. W is therefore positive, normlike and uniformly comparable to t^N.

Internal channels preserve N, so their contribution is **exactly**

    (L_int W)/W = -epsilon L_int H_d/[(N+1)^(q-1) h].    (8)

Using the appropriate denominator bound for each sign gives

    internal quotient <= epsilon K a/(1-epsilon)
             +epsilon C_R/(1-epsilon)
             -epsilon beta b^q/[m^(q-1)(N+1)^(q-1)].     (9)

Immigration contributes at most lambda[t/(1-epsilon)-1], using only the bounds on h. For an A death, set H'=H_d(x-e_A). Monotonicity of H and (4) imply

    H_d(x)/(N+1)^(q-1)-H'/N^(q-1)
       <= [H_d(x)-H']/(N+1)^(q-1)
       <= d N^(d-1)/(N+1)^(d+p-2).

After multiplication by mu a/t, its correction to the usual negative term -D a is at most mu epsilon d/[t(1-epsilon)], since p>=2 and a<=N. Death is absent at N=0. This is why no regularity at a fictitious negative count is needed.

Our epsilon ensures epsilon K/(1-epsilon)<=D/2. Thus

    LW/W <= C0-(D/2)a
             -epsilon beta b^q/[m^(q-1)(N+1)^(q-1)],
    C0=lambda[t/(1-epsilon)-1]
             +mu epsilon d/[t(1-epsilon)]
             +epsilon C_R/(1-epsilon).                 (10)

For N>=1 either a>=N/2, or b>N/2 and N+1<=2N. Consequently (2) holds with

    kappa=min(D/4,epsilon beta/[2^(2q-1) m^(q-1)]).      (11)

At N=0 the same immigration bound applies. There are no unverified boundary limits or finite layers hidden in this all-state calculation.

### Why the molecularity attenuation matters

For p>2 the denominator in (1) includes the additional factor (N+1)^(p-2). It turns the leading internal drift into order N, while its adverse A-containing part is only order A and can be paid by linear A death. The next-degree discrete/falling-factorial terms become bounded. Omitting that factor can leave a positive order N^(p-1) term that linear death cannot absorb; a cubic lifted fixture tests this failure separately.

## 3. Foster, closed classes and all exponential moments

Set zeta=kappa and

    R0=max(1,ceil((C0+zeta)/kappa)),
    C_F=(C0+zeta)t^R0.

Then LW<=-zeta W+C_F globally. The exception region N<R0 is bounded analytically; its possible count states need not be enumerated. C_F may be stored as an exact rational-power expression with explicit bit bounds rather than expanded beyond a declared budget.

Nonexplosion already follows by ordinary Poisson domination: only constant-rate immigration increases N, while all other channels preserve or decrease it. On a finite time interval, initial N plus the immigration count bounds the chain inside a finite set with bounded rates.

Full weak reversibility gives a feasible return path for every enabled transition by translating a reverse complex path by the nonnegative residual population. Hence communicating classes are closed. Foster's criterion gives positive recurrence classwise; no global irreducibility is assumed. Without WR, the support property alone would not make transient communicating classes recurrent.

For stationary moments, stopped exponential Dynkin yields P_s W<=a_0 W+b_0 with a_0=exp(-zeta s)<1 and b_0=C_F(1-a_0)/zeta. For phi_k(w)=min(w,k), invariance and concavity give

    integral [phi_k(W)-phi_k(a_0 W+b_0)] d pi <=0.

The integrand is bounded below by -b_0. Fatou after adding b_0 gives (1-a_0)pi(W)<=b_0, without assuming integrability. Thus pi(t^N)<infinity, including exponent log t. Repeating for arbitrary t proves every finite exponential count moment. These tails come from the exact count-specific inequality, **not** from a generic fluid-stability assertion.

## 4. Acquiring uniform activation using only finite support chains

The remainder of the proof earns a successful degree from the raw support property.

Use the infinity vector norm, the induced row-sum Jacobian norm, and the bilinear infinity Hessian norm bounded by the maximum row sum of absolute second derivatives. Let S be the sum of the positive order-p rates and k_min their minimum. Define

    C=max(1,p^3 S),       T=1/(4C).

On the simplex Delta={y>=0:sum y_i=1}, direct differentiation of (6) gives

    v_i(y)>=-C y_i,
    ||v(y)||_infinity<=C,
    ||Dv(y)||_infinity<=C,
    ||D^2v(y)||_infinity<=C.                             (12)

Indeed |u'_i-u_i|<=p, the total first derivative degree is p, and the total second derivative degree is p(p-1); negative terms in coordinate i contain y_i. These bounds use only raw finite coefficients.

For an integer M divisible by n, set h_E=T/M and

    E(y)=y+h_E v(y).

Then E preserves the simplex: total mass is conserved and y_i+h_E v_i>= (1-h_E C)y_i>=0. Also

    (1-h_E C)^M >=1-M h_E C=3/4.                        (13)

At least one initial coordinate is >=1/n. Starting from its singleton, the support algorithm supplies at most n-1 additions before reaching A. Divide the M steps into n equal blocks. Define rational levels

    ell_0=3/(4n),
    ell_(j+1)=min(ell_j, T k_min ell_j^p/(4n)),
    delta=ell_n>0.                                      (14)

The initial positive species stays above ell_0 throughout. If all source species of the next support channel remain above ell_j, that channel produces each newly added species at rate at least k_min ell_j^p. During a block, the scalar Euler recurrence adds at least

    (T/n) k_min ell_j^p (3/4).

Subsequent decay retains at least another factor 3/4, so the lower bound in (14), with factor 1/4, is conservative. Previously established bounds remain valid because ell decreases. Padding unused stages only decreases the displayed bound. Therefore

    (E^M(y))_A >= delta                 for every y in Delta,  (15)

uniformly in every admissible M. This is an explicit finite support-propagation calculation, not a stationary law or an unproved compactness claim.

## 5. An exact rational Euler polynomial earns the directional drift

Define the polynomial

    F_M(y)=h_E sum_(k=0)^(M-1) (E^k(y))_A.              (16)

It satisfies 0<=F_M<=T on Delta. Its exact discrete coboundary is

    [F_M(E(y))-F_M(y)]/h_E=(E^M(y))_A-y_A.              (17)

The comparison with a directional derivative has a uniform, acquired error. Let J_k and B_k bound the Jacobian and Hessian norms of E^k on Delta. Since k h_E C<=1/4,

    J_k<=(1+h_E C)^k <=1/(1-k h_E C)<=4/3.

The middle inequality follows by bounding the binomial expansion by a geometric series. The Hessian chain rule gives

    B_(k+1)<=(1+h_E C)B_k+h_E C J_k^2,
    B_0=0,
    B_k<=(4/3)^3 C k h_E <3 C T.

Hence ||D^2 F_M||<=3 C T^2. The line segment from y to E(y) stays in the simplex. Taylor's formula along it, (12), (15) and (17) give

    v(y) dot grad F_M(y)
       >=delta-y_A-(3/2)h_E C^3 T^2.

Choose the explicit integer

    M=n max(1,ceil(3 C^3 T^3/(n delta))).                (18)

It is divisible by n and makes the final error at most delta/2. Thus

    v dot grad F_M >=delta/2-y_A.                       (19)

All operations in (14), (18) and (16) are finite rational operations for rational raw rates. No continuous ODE solver or supplied F is a premise. Ordinary finite-time Lyapunov/resolvent constructions motivate (16); the discrete coboundary and error estimate make this instance explicit.

## 6. Homogenization stays inside the coefficient box

The derivative estimates in Section 5 concern the inhomogeneous extension E(y)=y+h_E v(y), not its homogeneous extension. The latter is used only for coefficient positivity; agreement on the simplex and tangency transfer the directional derivative afterward.

The homogeneous degree-p version of the Euler map is

    E_i^hom(x)=x_i N^(p-1)+h_E v_i(x).                  (20)

Every monomial coefficient is nonnegative. A negative coefficient from v_i can occur only in a source monomial containing x_i, whose baseline coefficient in x_i N^(p-1) is an integer at least one. Its total negative contribution is at most h_E p S<=h_E C<=1/4. A source not containing x_i has nonnegative i-increment. Also sum_i E_i^hom=N^p.

Consequently every homogeneous Euler iterate Phi^(k) has nonnegative coefficients and sum_i Phi_i^(k)=N^(p^k). Homogenize all terms of F_M/T to common degree

    d0=p^(M-1),
    H_(d0)(x)=(1/M) sum_(k=0)^(M-1)
                       N^(d0-p^k) Phi_A^(k)(x).         (21)

Its Bernstein coefficients lie in [0,1]: each summand is coefficientwise bounded by N^d0 and the average preserves that bound. On the simplex H=F_M/T. Because v dot grad N=0, differentiation in direction v commutes with homogenization. On A=0,

    (v dot grad H)(y)>=delta/(2T)=:delta_g>0.            (22)

This strict positivity is not yet coefficientwise positivity. The next ordinary Pólya step earns that missing operation.

## 7. Explicit coefficient elevation, with an elementary proof

Let g be the homogeneous boundary restriction of v dot grad H, of degree q=d0+p-1, and let S_g=sum_(|alpha|=q)|g_alpha|. A raw upper bound avoiding coefficient cancellation is

    S_g <= 2 p S d0 n^(d0-1).                           (23)

It follows from coefficientwise H<=N^d0 and sum_i ||v_i||_(coefficient l1)<=2pS.

For r>=q, the normalized coefficient at gamma, |gamma|=r, of

    (sum B_j)^(r-q) g(B)

is exactly

    b_gamma=sum_alpha g_alpha (gamma)_alpha/(r)_q.      (24)

This is direct factorial cancellation in the multinomial coefficients. Compare it with g(gamma/r). For each alpha, use the products of factors max(gamma_i-j,0)/r. They agree with the nonnegative integer falling-factorial product, and differ from the corresponding powers by at most q(q-1)/(2r). Also (r)_q/r^q>=1-q(q-1)/(2r). Thus, whenever r>=q(q-1),

    |b_gamma-g(gamma/r)| <=2 S_g q(q-1)/r.               (25)

For q=1 the identity is already exact; here q>=2. Choosing

    r>=max(q,q(q-1),ceil(4 S_g q(q-1)/delta_g))           (26)

makes every normalized boundary coefficient at least delta_g/2. The raw bound (23) may replace S_g. This is a deliberately conservative constructive form of classical Pólya positivity, not a new positivity theorem.

Lift H to H*=N^(r-q) H. It remains in the Bernstein box, its degree is r-p+1, and L_int H*=N^(r-q)L_int H exactly. Therefore all leading boundary coefficients of H* are positive and every pure coefficient is at least delta_g/2. A positive rational point of the finite cone has been constructed.

Equations (14), (18), (21), (23) and (26) give an explicit finite upper-degree construction. They prove that sequential unbudgeted exact degree search must terminate successfully. They do not make that worst-case search efficient.

## 8. Failure of support accessibility rules out every strict degree cone

Suppose closure from a singleton does not reach A. The terminal support S0 is nonempty, excludes A, and is closed under the order-p channels: a source supported in S0 has its entire product support in S0. The simplex face Delta_(S0) is therefore invariant under every sufficiently small Euler map E.

Any candidate homogeneous polynomial H attains a maximum at some y* in this compact face. Since E_h(y*) stays in the face,

    H(y*+h v(y*))<=H(y*)       for all sufficiently small h>0.

Taking the directional derivative gives v(y*) dot grad H(y*)<=0. But a strict degree cone requires

    v(y*) dot grad H(y*)>=beta sum_j (y*_j)^q>0,

because y* lies on A=0 and has total mass one. Contradiction. This argument does not rely on the coefficient box and does not require solving the ODE.

Thus the finite support test gives either a termination guarantee or a valid obstruction to **all degrees of this strict leading cone at the raw maximum order p**. It does not exclude all polynomial Foster corrections. For example, the earlier accepted mediated triangle plus the individually weight-neutral cubic pair A+2C<->3B has p=3 and failed pure-C top-order closure, yet its accepted linear correction still works because the cubic generator vanishes and binary restoration controls the tail. Earlier routes must be retained in parallel. It is not a recurrence decision. Even with genuine quadratic dynamics, the all-rate-one network `0<->A, A<->B, A<->C, 2B<->2C` has top-order closed support {B,C}, missing A. Nevertheless V=4^A 5^(B+C) has exact quotient 3-A/4-(B+C)/5. Lower-order restoration makes it stable. The simpler unary `0<->A, A<->B` also fails the quadratic-leading test while V=3^A4^B gives 2-A/3-B/4.

## 9. A genuine linear-weight obstruction and its ordinary comparator

A small test family is

    0 <-> A,
    2B <-> B+C <-> 2C,
    B+C <-> A+B.                                        (27)

Every singleton reaches A in the leading support closure. For a linear H=c_A A+c_B B+c_C C, positivity at pure B requires c_C>c_B, while positivity at pure C requires c_B>c_C. Hence degree one cannot succeed, at any positive rate values.

A degree-two witness is H=A N+eta BC. Writing rates p0:2B->BC, q0:BC->2B, r0:BC->2C, s0:2C->BC, u0:BC->AB, v0:AB->BC, the boundary cubic coefficients are

    B^3: eta p0,       C^3: eta s0,
    B^2 C: u0+eta(-p0-q0+r0-u0),
    B C^2: u0+eta(q0-r0-s0).

The rational choice

    eta=min(1,u0/[2(p0+q0+u0)],u0/[2(r0+s0)])

makes both mixed coefficients at least u0/2 and both pure ones positive. The exact program does not receive this witness.

For all rates one except BC->2C at rate two, the acquired polynomial is instead

    H=2A(B+C)+BC.

Degree one exhausts 330 candidate bases. Degree two succeeds after 10,298 further attempts (685 nonsingular), among 31,824 candidate degree-two bases. It gives beta=1, K=5, C_R=11. At t=2,

    epsilon=1/40, C0=53/39, kappa=1/5120, R0=6959.

The implicit finite exception region has 56,192,254,840 states, bounded analytically rather than enumerated. The raw demo checks 5,456 small states and 30 targeted states exactly. The full internal polynomial expansion, constraints, residuals and formal multiplication counts are recorded.

This parameter instance is not complex balanced: balance at the pure-2B and pure-2C leaf complexes would require b=c and c=2b at a strictly positive point. It has two linkage classes and fails strong endotacticity in the all-ones direction.

A stronger ordinary comparator must be retained: `P=A+eta min(B,C)` also has a direct piecewise regenerative drift for this family, with eta acquired from its raw rates. Thus a polynomial correction is not uniquely necessary here. The point of the general theorem is systematic acquisition and an exact structural termination boundary, not claiming that a handpicked quadratic beats every conventional nonsmooth Lyapunov construction. The independent comparator proof is kept separately.

## 10. Costs, conventional sources and limits

The implementation actually expands and checks only the finite degrees it searches. At degree d it has binom(n+d-1,d) coefficient variables plus beta; all constraint bases are explicitly charged, including singular ones. Polynomial expansion term-pair counts and coefficient bit sizes are recorded. Finite degree or basis caps yield UNKNOWN for the explicit polynomial certificate; both caps must be removed to invoke its acquisition termination guarantee. The independently checked successful support condition already satisfies the structural recurrence theorem; these two statuses are not conflated. A support-negative result still leaves actual network stability UNKNOWN. The trusted API and separate audit status must not be confused with hostile-input verification.

The formal Euler witness (21) has degree p^(M-1); (26) can increase it drastically again. The support receiver stores exact M and the degree as a factored expression, without pretending to write an astronomical coefficient list. Its worst-case construction is a proof of finite acquisition, not a practical resource estimate. Actual low-degree search can be far smaller, as (27) demonstrates.

The architecture still requires one directly immigrating/dying coordinate and conservative internals. Accessibility uses only the highest-order channels. A stable system may fail it, including because restoration is lower order. No arbitrary weak-reversibility result follows.

Ordinary forward-support/Petri-net face geometry, converse/fluid Lyapunov principles and Pólya coefficient elevation are credited in `SOURCE_SCOPE.md`. Generic fluid stability does not imply exponential tails; the all-exponent conclusion here uses (8)–(11), bounded jumps, count conservation and linear A death. No historical-priority search or external refereeing is claimed. This package is purely mathematical and non-operational; earlier accepted artifacts are unchanged.


## 11. Separate qualitative and quantitative receiving interfaces

The theorem is reusable mathematical capital. For a new rational-rate raw list, the qualitative interface needs only finite raw recognition, weak-reversibility checks and explicit leading-support chains. It returns classwise positive recurrence and every finite exponential stationary count moment when those witnesses pass. It does **not** return an explicit H, a numerical Foster radius, a tail prefactor, a mixing estimate or an efficient sampler. It does not evaluate the astronomical Euler witness just to issue this qualitative conclusion.

A separate quantitative request pays exact polynomial extraction and finite LP-basis search. A degree or work cap can leave that output UNKNOWN even when qualitative recurrence is already certified by the support theorem. Conversely, support failure certifies an obstruction to every strict degree cone at the raw maximum order but leaves actual stability UNKNOWN.

`structural_receiver.py` provides these finite qualitative output semantics and validates the raw list and support witness directly. Its theorem-source hash is explicit. The receiver is ordinary research validation code, not a hardened malicious-input service or external proof assistant. The independent audit must bind its exact source before it is promoted. Structural search has at most n seeds, n-1 support enlargements per seed and a finite scan of top-order channels at each enlargement; every source/product test uses at most n coordinates. No polynomial degree, real-valued flow or stationary law is an instance-input oracle.
