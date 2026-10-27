# A globally optimal finite two-resonance cell under two real static costs

This proof extends `PROOF.md` to a finite, binding total-spring budget. It
keeps the same fixed actual resources m=1, M=2, K=1, theta=1/2, while
requiring **C_CM<=1/20** and **total positive internal spring sum<=24**.
All acoustic and optical passbands count in J. The topology class is every
finite connected positive scalar internal spring graph attached to the
single backbone coordinate. This is still an ideal harmonic ballistic
model, not a material or measured-device result.

## The fourth resource moment is physically necessary

Let alpha and beta be the squared endpoint eigenvalues of D0 and
Dpi=D0+4 e_b e_b^T. At fixed actual backbone mass one,

    E(chi):=integral 4 w^3 chi(w) dw
           =sum_j(beta_j^2-alpha_j^2)
           =trace(Dpi^2-D0^2)
           =16+8(D0)_bb
           =16+8 k_incident.

Here k_incident is the sum of positive internal springs directly incident
to the backbone. Every other internal spring also consumes the total
budget, so the stipulated total sum<=24 implies **E<=208** for every graph.
For a star the incident and total sums coincide. This is also the
high-frequency cost formula in frozen source F, here derived directly.

The other necessary moments from `PROOF.md` remain

    T=integral 2w chi=4,
    integral(chi-chi_rigid)/w=0,
    D=integral(chi_rigid-chi)/w^3=C_CM/4<=1/80.

No spring, mass or disconnected component supplying the hard part is free.

## Exact finite positive candidate

Let h be an exact root specified below in the rational bracket

    0.06552741459340005487388219669883060107690
      < h <
    0.06552741459340005487388219669883060107692.

Put b=1-h and define

    H(h) = {24C-1+2h
              +sqrt[(1-2h-24C)^2-96 C h^2]}/(2C),
    C=1/20,
    k(h)=24-H(h).

Use the actual star with backbone 1, side masses (h,b), springs (H,k),
and intercell spring 1. All are finite and strictly positive throughout
the displayed bracket. Its total mass is exactly two and total spring sum
exactly 24. The quadratic defining H is

    C H^2 + (1-2h-24C)H + 24h^2=0,

equivalent to the exact star compliance equation

    h^2/H + b^2/(24-H)=C.

Thus **D=1/80 and E=208 exactly**. The resource caps both bind.

The executed certificate encloses the component values as

    h=0.065527414593400054873882...,
    b=0.934472585406599945126117...,
    H=6.293614801754828497043887...,
    k=17.706385198245171502956112... .

This candidate uses no infinite-frequency limit.

## Exact definition of h and of the five-edge dual

For every h in the bracket, build the mass-normalized star endpoint
matrices. Their spectra are obtained from the exact formulas

    tr0=H(1+1/h)+k(1+1/b),
    pair0=2Hk/(hb),
    det(t I-D0)=t*(t^2-tr0*t+pair0),
    det(t I-Dpi)=t^3-(tr0+4)t^2
                   +[pair0+4(H/h+k/b)]t-4Hk/(hb).

Let x1<...<x5 be the five positive frequency edges, with full passbands
[0,x1] union [x2,x3] union [x4,x5]. Strict interlacing is enclosed by the
certificate throughout the h bracket.

Fit lambda, mu, nu, eta uniquely at the first four edges by

    F(w)=w^3 g(w)+lambda w^2+2mu w^4+4nu w^6-eta,
    F(x1)=F(x2)=F(x3)=F(x4)=0.

This is ordinary degree-three interpolation at the four distinct squared
nodes. Define the continuous scalar residual f(h)=F(x5). The exact-rational
interval calculation `certify_joint_cap.py` proves

    f(h_lo)>2.1893963685*10^(-42)>0,
    f(h_hi)<-1.9800554203*10^(-42)<0.

The intermediate value theorem therefore supplies an exact h in the
bracket with **all five edges roots of F**. This exact root equation, not
a rounded optimizer output, defines the claimed cell. No uniqueness of
the scalar parameter is assumed as a premise.

The certificate encloses the resulting multipliers:

    lambda= 0.060581186496038450863066...,
    mu=    -0.000367112442249563895644...,
    nu=     0.000000709781539446768645... >0,
    eta=    1.553310193562645321512763... >0.

Mu is the multiplier of an equality resource and may be negative. Nu and
eta have the required signs for the stiffness and compliance inequalities.

## An all-frequency five-root certificate

Multiply F by sinh^2(w)/w^2. The resulting entire function is

    Q(w)=w^3+lambda*sinh^2(w)+2mu*w^2*sinh^2(w)
           +4nu*w^4*sinh^2(w)-eta*sinh^2(w)/w^2.

As before its constant coefficient is -eta, its sole odd coefficient is
the positive coefficient of w^3, and its even coefficient at w^(2n) is
a_n B_n, with a_n=2^(2n-1)/(2n)!>0 and

    B1=lambda-eta/3,
    B2=lambda+6mu-2eta/15,
    Bn=lambda+mu*n(2n-1)+nu*n(n-1)(2n-1)(2n-3)
          -4eta/[(2n+2)(2n+1)]                   (n>=3).

The exceptions at n=1,2 matter: the shifted sinh series has no constant
term. The exact interval computation proves

    B1,...,B5 < 0,
    B6,...,B9 > 0,
    B10,...,B13 < 0,
    B14 > 0.

This finite check also owns the whole infinite tail. Set

    P(n)=lambda+mu*n(2n-1)+nu*n(n-1)(2n-1)(2n-3).

The certificate proves

    P'(14)>0.00617932921133978,
    P''(14)>0.00450933035622242.

Furthermore P'''(n)=nu(96n-72)>0 for n>=14. Consequently P increases
thereafter. The remaining term -4eta/[(2n+2)(2n+1)] also strictly increases,
so **every Bn for n>=14 is positive**. No numerical frequency grid or
unchecked coefficient tail is being used.

After the constant and the lone +w^3 are inserted, the coefficient signs
have exactly five variations:

    negative, positive, negative, positive, negative, positive.

The convergent-series sign-variation lemma proved in `PROOF.md` therefore
bounds the number of positive roots of Q, and F, by five including
multiplicity. The five known distinct edges exhaust the bound and are
simple. Since F(0)=-eta<0 and its leading polynomial term is 4nu*w^6>0,
its negative set is exactly

    (0,x1) union (x2,x3) union (x4,x5).

The candidate is the pointwise minimizer on the entire positive axis of

    R(w)=F(w)/w^3
        =g(w)+lambda/w+2mu*w+4nu*w^3-eta/w^3.

## Global result over every legal finite topology

For every legal finite competing indicator chi,

    integral R(chi-chi_*) >=0.

The exact log and trace equalities cancel. Expanding the remaining moments
with Delta denoting competitor minus candidate gives

    integral R(chi-chi_*)
      = J-J_* + nu*Delta E + eta*Delta D.

Since E<=E_*=208, D<=D_*=1/80, and nu,eta>0,

    J-J_*
      =integral R(chi-chi_*)-nu*Delta E-eta*Delta D >=0.

Thus the displayed **finite two-pendant cell globally minimizes full
Bose-weighted conductance over every finite connected positive internal
network at both charged resource caps**. Equality forces the same active
spectrum and saturation of both resource inequalities. Equivalent active
realizations and possible cancelled dark modes need not be unique.

Its three nonempty active bands require at least three active degrees of
freedom, so one pendant cannot attain this optimum. The candidate uses
exactly two pendants: the minimal active order is therefore two internal
resonances for this joint-budget point.

The certificate includes every band and rigorously bounds the conductance:

    J_joint in [1.142016098461582733349079,
                1.142016098461582733349080].

The optimized one-pendant comparator under these same budgets has k=20
and J_one=1.142045387542071761716599... . The global two-pendant saving
over it is 0.000029289080489028367520... . It is about 0.00256% of its
total conductance: a real but small model effect, not a practical-device
breakthrough.

The same exact construction, interpolation and coefficient-tail method
supplies a local design opening around this nondegenerate resource point;
no global all-resource phase diagram or uniform conditioning theorem is
claimed. A conventional equally informed passive-network designer can
realize the same optimum. Novelty and physical realization remain separate.
