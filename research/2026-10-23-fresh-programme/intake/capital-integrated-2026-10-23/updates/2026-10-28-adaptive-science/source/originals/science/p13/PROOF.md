# A compliance-constrained phonon frontier with a topology change

The subsequent `JOINT_CAP_PROOF.md` strengthens Section 3 to a globally
optimal finite two-pendant cell under C_CM<=1/20 and total spring sum<=24.
It removes the open optimization gap for that particular joint-budget
point; the general resource phase diagram remains open.

All statements below concern the exact scalar, rank-one, harmonic,
ideal-contact ballistic model of frozen sources F and C. Throughout,
the actual backbone mass is **m=1**, total cell mass **M=2**, intercell
spring **K=1**, and temperature **theta=1/2**. The objective, before the
common factor k_B/(2 pi), is

    J(chi) = integral_0^infinity g(w) chi(w) dw,
    g(w) = (w/sinh w)^2.

No actual elastic material, connector mass, three-dimensional polarization,
disorder, anharmonicity, finite contact or measurement is claimed.

## 1. The exact resources and an all-frequency certificate

Let chi be the complete passband indicator of any connected finite positive
internal mass/spring network in the stated model. Source F proves
0 <= chi <= 1, the rank-one trace identity, the regularized logarithmic
identity, and full positive-star inverse realization. Source C, with the
consistent sign convention audited in A, proves the additional compliance
identity. At our resources these read

    T(chi) = integral 2 w chi(w) dw = 4,
    integral [chi-1_[0,sqrt2]]/w dw = 0,
    D(chi) = integral [1_[0,sqrt2]-chi]/w^3 dw = C_CM/4.

Every difference integral used below is finite: two connected finite
spectra agree with one on some interval next to zero and have bounded
frequency support. Dark bands cancel and do not invalidate these identities.

Suppose a strict two-band indicator chi_* has positive edges p<r<s and
define its exact interpolated multipliers by

    F(w) = w^3 g(w) + lambda w^2 + 2 mu w^4 - eta,
    F(p)=F(r)=F(s)=0.

Interpolation at the three distinct squared edges determines the multipliers
uniquely. If mu>0 and eta>0, then F has exactly these three positive roots,
all simple, and

    F<0 on (0,p) union (r,s),
    F>0 on (p,r) union (s,infinity).

The same conclusion holds when mu=0, lambda>0, eta>0. This criterion requires
no assumed sign for lambda when mu>0.

Here is a self-contained proof of the all-frequency root assertion. Multiply
F by the positive factor sinh^2(w)/w^2 to obtain the entire function

    Q(w)=w^3 + lambda sinh^2(w) + 2 mu w^2 sinh^2(w)
              - eta sinh^2(w)/w^2.

Writing a_n=2^(2n-1)/(2n)! gives its constant coefficient -eta, its sole
odd coefficient +1 at degree three, and even coefficients a_n B_n, where

    B_1=lambda-eta/3,
    B_n=lambda+mu*n*(2n-1)-4*eta/[(2n+2)(2n+1)]  (n>=2).

B_2-B_1=6 mu+eta/5>0, and all subsequent differences are positive. Their
limit is positive infinity if mu>0, and lambda>0 if mu=0. Thus the even
coefficients have at most one negative-to-positive change. Together with
the constant and the lone positive odd coefficient, Q has at most three
coefficient sign variations.

For completeness, a convergent Laurent/power series with integer exponents
bounded below, compact-uniform termwise differentiation on (0,infinity),
and V finite coefficient sign variations has at most V positive zeros
counted with multiplicity. Induct on V. If there is no variation, the sum
has one strict sign. Otherwise let k be the exponent at the first sign
change. Differentiating x^(-k) times the series flips all earlier signs,
removes the coefficient at k, and preserves every later sign. This removes
the first variation. The resulting series has at most V-1 positive zeros
by induction. Rolle's theorem, including multiplicities, rules out V+1
zeros of the original series. The same argument excludes infinitely many
zeros by selecting any finite collection of them.

Applying this lemma to Q gives at most three positive roots, with
multiplicity. The three known distinct edges exhaust the count. Since
F(0)=-eta<0 and F is positive at sufficiently large w, the claimed signs
follow on the whole frequency axis, without a sampled-frequency argument.

Put R=F/w^3. Whenever chi_* equals one exactly where R<0, pointwise

    R(w) [chi(w)-chi_*(w)] >= 0.

If chi and chi_* have the same log and trace moments, then

    J(chi)-J(chi_*)
      = integral R(chi-chi_*) dw - eta [D(chi)-D(chi_*)].       (1)

Hence eta>=0 and D(chi)<=D(chi_*) prove the global lower bound. If mu=0,
the trace moments need not agree, because the trace term is absent. This
last observation is what makes the tighter-cap limiting frontier possible.

## 2. The supplied C_CM <= 1/4 point is globally solved

Take the actual positive one-pendant cell with masses (1,1), internal
spring 4, and intercell spring 1. Its endpoint matrices are

    D0  = [[4,-4],[-4,4]],
    Dpi = [[8,-4],[-4,4]].

The complete bands are

    [0,sqrt5-1] union [2 sqrt2,sqrt5+1].

Their trace is 4, log moment is the required sqrt2 anchor, and

    p^(-2)+s^(-2)-r^(-2)=5/8,
    D=1/16, C_CM=1/4.

The helper's exact rational interval certificate proves

    -0.591137020902620 < lambda < -0.591137020902619,
     0.0197894500757470 < mu < 0.0197894500757471,
     0.351276884506192 < eta < 0.351276884506193.

It also encloses B_1,...,B_4 below zero and B_5 above zero. Therefore the
all-frequency certificate of Section 1 applies. Equation (1) proves that
**no legal finite internal network improves on this cell at C_CM<=1/4**.
Equality requires the same complete active spectrum and cap saturation;
equivalent realizations and additional dark modes are not excluded.

The parent reran `helper/certify_dual.py`, and independently integrated the
entire spectrum with exact rational bounds:

    J_* in [1.094388522317695923972117,
            1.094388522317695923972118],
    J_*/J_rigid in [0.942353155061616461360470,
                    0.942353155061616461360471].

This closes the case's initial discriminator with a genuine all-network
bound. It is not a reprise of the unconstrained one-resonator theorem: the
new negative moment and its correctly signed multiplier are load-bearing.

## 3. Extra internal modes really can help under a tighter cap

For an actual star with total side mass one, side masses m_i, and springs
k_i, the CM readout is Y=sum_i m_i y_i. A unit static force on Y applies
force m_i to coordinate y_i. The spring energy is sum_i k_i y_i^2/2, so

    C_CM = sum_i m_i^2/k_i.                                  (2)

This is an exact compliance calculation, not a stiffness surrogate.

Now impose the tighter **C_CM<=1/20** and, additionally, the matched finite
budget **sum_i k_i<=24**. Take

    backbone mass 1,
    side masses (1/20,19/20),
    side springs (5,1805/99),
    intercell spring 1.

Every component is finite and positive. Exactly,

    C_CM = (1/20)^2/5 + (19/20)^2/(1805/99) = 1/20,
    sum_i k_i = 2300/99 = 23.232323... < 24.

The nonzero squared q=0 edges are the two roots of

    99 t^2 - 14100 t + 380000 = 0;

the three squared q=pi edges are the roots of

    99 t^3 - 14496 t^2 + 427200 t - 760000 = 0.

These follow from the exact star trace, pair coefficient, and determinant.
For example, trace(D0)=H(1+1/h)+k(1+1/b), the positive pair product is
2Hk/(hb), and adding 4 to the backbone diagonal increments the pair
coefficient by 4(H/h+k/b) and gives determinant 4Hk/(hb). The certificate
checks all these rational equalities before isolating the roots.

All three passbands are included:

    [0,1.378377191477788...],
    [6.008420801383301...,6.155712233661423...],
    [10.311310387033593...,10.326254192039208...].

The strongest legal one-pendant comparator has spring k in [20,24]. Source
F proves its objective increases beyond the unique unconstrained optimum
k*=2.729088..., so its optimized spring is **20**. We do not compare
against a mistuned pendant. Exact rational integral enclosures give

    J_two in [1.142020891633280879557087,
              1.142020891633280879557088],
    J_one in [1.142045387542071761716599,
              1.142045387542071761716600],
    J_one-J_two in [0.000024495908790882159512,
                    0.000024495908790882159513] > 0.

This is a strict finite-network benefit of an additional active mode at a
binding compliance cap, even after a finite total-spring cap is matched.
It does not establish that this two-pendant cell is optimal under the joint
cap 24. An equally informed ordinary Foster/Stieltjes designer has the same
network operations and can reproduce it.

## 4. A complete tighter-cap infimum, with explicit nonattainment

Drop the optional sum-spring cap 24, retaining the original case's fixed
masses and C_CM<=C=1/20. For an effective trace A in (2,4), define

    r^2=(A-2)/C,
    Delta=sqrt[(r^2+A)^2-8r^2],
    s^2=(r^2+A+Delta)/2,
    p^2=2r^2/s^2.

These are the actual one-pendant endpoints with effective backbone mass
4/A, total mass 2, and side mass 2-4/A. They satisfy the required log
moment and

    p^(-2)+s^(-2)-r^(-2)=1/2+C/2,
    D=C/4,
    T=A.

This effective cell is used to construct a lower bound; its backbone mass
exceeds the actual fixed backbone mass 1, so it is **not** called a legal
attaining network.

For each A fit the exact three-edge multipliers of Section 1. The rational
interval sign bracket in `certify_envelope.py` proves that a root mu(A)=0
exists in

    3.39813033676949568 < A_* < 3.39813033676949570.

At that exact root, lambda>0 and eta>0 are enclosed, so the mu=0
all-frequency certificate applies. The trace term has vanished. Thus its
two-band objective is a global lower bound on **every** actual fixed-m=1
finite network with C_CM<=1/20:

    J_inf in [1.141916025317237306946979,
              1.141916025317237340078980].                    (3)

No such finite network attains (3). Equality in the pointwise comparison
would force exactly the same active bands, hence T=A_*<4, contrary to the
fixed-m=1 trace identity. Extra dark modes cannot repair an active trace
identity.

The bound is nevertheless the exact infimum. Put

    h=4/A_*-1, b=1-h, H>h^2/C,
    k_H=b^2/(C-h^2/H).

Build an actual m=1 star with side masses (h,b) and springs (H,k_H).
Equation (2) gives C_CM=C exactly for every finite H. Its total mass is
exactly 2. As H tends to infinity, its low-frequency behavior converges to
the effective cell with backbone 1+h=4/A_* and soft spring b^2/C.
For instance its exact driving-point response at t>0 is

    q_H(t)=1 / {t [1+h H/(H+h t)+b k_H/(k_H+b t)]},

which converges to that effective two-mass response. After clearing the
denominators, continuity of the simple finite roots gives convergence of
the two low bands; the third band escapes to infinite frequency. Its Bose
contribution is bounded by the tail integral from its lower edge and
therefore tends to zero. Consequently J_H tends to (3). This is a positive
finite approximation sequence with every compliance contribution charged,
not an uncharged rigid mass or an attained infinite-stiffness component.

For orientation, h=0.17711788648... and limiting k=13.5426994550....
The executed numerical continuation with H=1000 gives J=1.14191778927...;
that floating value is supplementary, while (3) and the rational cell in
Section 3 have interval certificates. The limiting sequence's total
stiffness diverges, so it does not solve any common finite material budget.

## 5. The sharp all-network small-compliance law

There is a sharper general consequence than a single tighter-cap example.
Let a=sqrt2. Define r0 as an exact root in the certified bracket

    5.2916003633454644313334084015605480943466
      < r0 <
    5.2916003633454644313334084015605480943467,

of E(r)=a^3 g(a)+2 lambda(r)-eta(r), where

    lambda(r)=r g(r)[r coth(r)-5/2],
    eta(r)=r^3 g(r)+lambda(r)r^2.

The interval certificate proves opposite strict endpoint signs of E and
therefore exact existence by continuity. It also proves lambda0>0 and
eta0>0. By construction

    F0(w)=w^3 g(w)+lambda0 w^2-eta0

vanishes at a and has a double root at r0. Section 1's coefficient argument
bounds its positive zeros with multiplicity by three. Hence the root at a
is simple, the root at r0 is exactly double, and there are no other positive
roots. Since F0(0)<0 and F0 is positive at infinity, F0 is negative on
(0,a), positive on (a,infinity) apart from that isolated double zero.

The rigid indicator is therefore the pointwise minimizer of R0=F0/w^3.
For every finite legal network, the log moment cancels and

    0 <= integral R0(chi-chi_rigid)
       = J-J_rigid + eta0 D.

Thus the **uniform, all-network, all-cap bound** is

    J_rigid-J <= (eta0/4) C_CM,
    eta0/4 in [0.398643595583964859020343,
               0.398643595583964859020344].                  (4)

Its coefficient is sharp as the cap tends to zero. To exhibit legality,
for every sufficiently small positive C choose

    b_C=2 C r0^2/(2+C r0^2), h_C=1-b_C,
    H_C=C^(-2),
    k_C=b_C^2/(C-h_C^2/H_C).

All masses and springs are positive and finite, m=1 and M=2, and the full
CM compliance is exactly C. The very stiff branch dynamically binds h_C
to the backbone. Its departure from the bound mass is O(C^2) at finite
frequencies. The low optical frequency is r_C=r0+O(C), and ordinary
simple-root perturbation of the exact star characteristic polynomial gives

    p_C=a-C*a*r0^2/[2(r0^2-a^2)]+O(C^2),
    s_C-r_C=C*r0^3/[2(r0^2-a^2)]+O(C^2).

The high band has lower edge of order 1/C, so its full Bose integral is
o(C). Integrating the two finite bands gives

    J_rigid-J_C
      = C*r0^2 [a g(a)-r0 g(r0)]/[2(r0^2-a^2)] + O(C^2)
      = C*eta0/4 + O(C^2).

The final equality follows by eliminating lambda0 between F0(a)=F0(r0)=0.
Combining this legal sequence with (4), for the infimum over **all** finite
legal internal networks,

    lim_(C down 0) [J_rigid-inf_(C_CM<=C) J]/C = eta0/4.       (5)

In contrast the optimized one-pendant cell has k=1/C when C is small,
r^2=2/C, and

    J_rigid-J_one(C)
      = C*g(sqrt2)/sqrt2 + O(C^2),
    g(sqrt2)/sqrt2 = 0.377679197206601085462980... .

The ratio of sharp leading savings is therefore

    1.055508480563454653872697... .

This is 5.55% more of a saving that itself vanishes linearly with C; it is
not a 5.55% reduction of total conductance. The displayed sharp sequence
spends H_C=C^(-2), so its stiffness expenditure is explicitly unbounded.
Equation (5) makes no finite-stiffness or finite-material claim.

## 6. What was and was not established

Established within the model: the specified C=1/4 global finite optimum;
a positive finite additional-mode improvement at C=1/20 under the extra
matched stiffness cap 24; the exact unrestricted-stiffness infimum and its
nonattainment at C=1/20; and the sharp all-network small-compliance slope.

A numerical continuation places the fixed-one-pendant zero-mu point near
k=13.9753027391, C=0.0715548005414. That is useful frontier guidance, not
a proof of a global phase diagram. The conditional multiplier criterion
and the separately certified examples and asymptotic theorem are the actual
proved scope. Optimizer failures are not used as exclusions.

The full finite-stiffness/compliance tradeoff over all resource values is
still open here; `JOINT_CAP_PROOF.md` solves the point C<=1/20, sum<=24.
The scalar ideal ballistic setting also omits enough
physical resources that neither the small absolute improvement nor the
infinite-stiffness frontier establishes a practical thermal insulator.

The construction uses the supplied exact third moment, full-spectrum
inverse and classical Foster/Stieltjes operations. Finite-sign-variation
root counting is classical mathematical machinery. Historical priority for
these specialized constrained Bose results has not been researched or
cleared. No algorithmic advantage over an equally informed conventional
designer is claimed.
