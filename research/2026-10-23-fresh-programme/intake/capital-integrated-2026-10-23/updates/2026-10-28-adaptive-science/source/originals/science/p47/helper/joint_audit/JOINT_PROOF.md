# A finite global optimum with compliance and total spring sum both charged

This closes one concrete jointly charged point left open in the general-frontier discussion. The full joint-budget family for arbitrary resources is not solved. The exact object below is a positive finite three-band star, and its all-frequency dual proves global optimality over arbitrary positive finite internal topology at the stated masses, temperature and both budgets. It is not only a better two-branch numerical local optimum.

## 1. Model, exact budgets and scalar construction

Fix m=1,M=2,K=1,theta=1/2 and require

C_CM<=1/20,
kappa_total:=sum(all positive internal spring constants)<=1001/50=20.02.

For any admitted network frozen F/C/A gives

L=0,
T=integral 2w chi=4,
W=integral (chi-1_[0,sqrt2])/w³ >=-1/80,
E=integral 4w³ chi=sum(beta²-alpha²).

Frozen F's incident-spring identity gives kappa_inc=(E-16)/8. Since every positive internal edge costs spring sum, kappa_inc<=kappa_total and therefore

E<=16+8*(1001/50)=4404/25=176.16.

Let delta>0 and H>0. Define

A=4-delta,
B=2H/(H+delta),
t=(A-B)/{B[21/40-1/B+delta/(H(H+delta))]},
c=[B t+(t+A)(H+delta)-tH]/4,
kappa(delta,H)=t+H-c.

Let p²,s² be the roots of z²-(t+A)z+B t=0 and set r=sqrt(t), u=sqrt(H), v=sqrt(H+delta). The proposed squared endpoints are

alpha=(0,t,H), beta=(p²,s²,H+delta).

These automatically have exact original trace 4, exact log product 2 and exact inverse endpoint sum 21/40, hence exact C_CM=1/20. The positive-star inverse has q(z)=(z²+c z+d)/[z(z+t)(z+H)], with d=B t(H+delta)/4. Its total internal spring sum is precisely the rational function kappa above.

## 2. Exact nested root existence, including the stationarity equation

For each H near 73.33846366923165, define delta(H) as the root of

kappa(delta,H)=1001/50.

The exact interval script encloses both partial derivatives kappa_delta>0 and kappa_H>0 throughout delta in [0.00577,0.00578] and the displayed H bracket. At the lower delta edge kappa<1001/50, and at the upper edge kappa>1001/50, uniformly in H. Thus there is one continuous differentiable delta(H) on the whole bracket. It decreases in H. Rational bisection with 220 steps encloses its values at each H endpoint; those endpoint enclosures bound the full branch.

At four edges p,r,s,u fit the unique cubic polynomial in w² through -w³g(w). Equivalently fit (nu,lambda,a,b) to

F(w)=w³g(w)+nu+lambda w²+a w⁴+b w⁶=0

at those four edges. Define F5(H)=F(v) on the continuous kappa-exact branch. The computed signs are exact outward bounds:

F5(73.33846366923165)<-3.686e-21<0,
F5(73.33846366923166)>+6.359e-21>0.

The intermediate value theorem therefore supplies an exact root Hhat in this bracket, and deltahat=delta(Hhat). At this exact object all five edges are distinct and F vanishes at all five. The root is specified by these equations and brackets, not by treating floating coordinates as exact physical parts.

The entire parameter box has nu<0 and b>0. Its candidate star has two strictly positive side masses and two strictly positive springs. It obeys both budgets exactly at the root.

## 3. Complete five-root certificate over the entire frequency axis

Define

R(w)=g(w)+lambda/w+a w+nu/w³+b w³,
Q(w)=F(w) sinh²(w)/w².

Because theta=1/2, g(w)=(w/sinh(w))² and

Q(w)=w³+nu sinh²(w)/w²+lambda sinh²(w)
      +a w² sinh²(w)+b w⁴ sinh²(w).

The apparent singularity at zero is removable. Write d_j=2^(2j-1)/(2j)! for j>=1 and d_j=0 for j<=0. The even coefficient at w^(2n) is

q_n=nu d_(n+1)+lambda d_n+a d_(n-1)+b d_(n-2).

Every q_n for n=0,...,17 has a rigorous sign enclosure from the complete root box. The signs are

n=0,...,5: negative;
n=6,...,8: positive;
n=9,...,12: negative;
n=13,...,17: positive.

There is also the positive cubic coefficient between n=1 and n=2. Hence this finite initial segment has exactly five sign changes.

No infinite tail is left unchecked. For n>=18 normalize by d_(n-2)>0. With

U_n=(2n-2)(2n-3),
V_n=U_n(2n)(2n-1),
Z_n=V_n(2n+2)(2n+1),

one has

q_n/d_(n-2)=b+4a/U_n+16lambda/V_n+64nu/Z_n.

The interval certificate proves lambda>0, a<0, nu<0 and

b+4a/U_18+64nu/Z_18>0.00000118549115940998.

For n>=18 the omitted lambda term is positive and both negative terms increase toward zero as their denominators increase. Thus every remaining coefficient is strictly positive. The full entire coefficient series has exactly five sign changes.

The self-contained Descartes lemma in helper/PROOF.md therefore bounds positive roots of Q, counting multiplicities, by five. The five distinct prescribed edges exhaust that bound, hence are simple and no further root exists. Since R is negative near zero (nu<0) and positive at infinity (b>0), its negative set is exactly

(0,p) union (r,s) union (u,v).

This proves the correct sign at all frequencies without a sampled grid. Exact interval coefficient signs support this one joint resource point; no unproved universal five-root theorem is being invoked.

## 4. Global comparison against every admitted finite graph

Let chi* be this actual three-band star's full indicator and chi any finite positive network satisfying the same fixed m,M,K and both caps. Pointwise sign minimization gives

I=integral R(chi-chi*)>=0.

The exact trace and log moments cancel. The compliance and stiffness moment differences obey DeltaW>=0 and DeltaE<=0. Consequently

J(chi)-J(chi*)=I-nu DeltaW-(b/4)DeltaE>=0,

because nu<0<b. Thus the displayed finite network is a global optimum over every finite internal graph and mode count under both charged budgets. Equality forces chi=chi* almost everywhere because R has only five isolated zeros. Its active spectrum/response is unique; dark or isospectral physical representations are not ruled out.

This also proves uniqueness of the nested root in its isolating box: any other such root has the same proper dual sign certificate and budgets, hence the same unique active spectrum and therefore the same high-band start H and width delta.

## 5. Actual positive parts and objective

The exact root is enclosed by

73.33846366923165 < Hhat < 73.33846366923166,
0.00577347758826857272 < deltahat < 0.00577347758826857554.

Use the explicit star inverse

sigma_(1,2)=(c -/+ sqrt(c²-4d))/2,
k_1=[Ht-d-kappa sigma_1]/(sigma_2-sigma_1),
k_2=kappa-k_1,
m_j=k_j/sigma_j,

with backbone mass 1 and intercell spring 1. Certified enclosures are printed by joint_certify.py; representative values are

m_1 approximately 0.9994837657673,
m_2 approximately 0.0005162342327,
k_1 approximately 19.9821713988125,
k_2 approximately 0.0378286011875.

They sum to total side mass 1 and exact total internal stiffness 20.02. All are finite and positive. The full bands are approximately

[0,1.37849414733326]
union [6.32076003234950,6.48428776310294]
union [8.56378792761893,8.56412500765956].

The exact all-band objective is enclosed by

1.142045199292380356594718 < J_opt < 1.142045199292393889573449.

The strongest legal one-pendant with both caps has 20<=k<=20.02 and chooses k=20. Its objective is 1.142045387542071761716599.... Therefore

1.88249677872143150e-7 < J_pendant-J_opt
                           <1.88249691405121882e-7.

The improvement is approximately 1.65e-7 relative conductance. Two side modes are necessary to improve the one-pendant comparator and sufficient to attain this joint-budget optimum. The gain is mathematically strict and practically unestablished.

## 6. Verification and remaining interface

joint_certify.py uses the exact dyadic arithmetic and Bose-tail bounds in certify.py. Rational bisection encloses the nested compliance/stiffness construction; interval derivative signs provide branch existence and monotonicity; the fifth-edge sign change provides an exact interior stationary object; the entire-series sign count proves the global result. The certificate checks positive star parts and includes the highest optical band.

The general fixed-compliance frontier in PROOF.md is independently audited; this joint point has its own certificate and requires its own scoped audit. The full arbitrary-resource joint-stiffness/compliance family, finite manufacturing tolerance, connector mass, individual displacement/strain, vector elasticity, contacts, anharmonicity and measured device benefit remain open. This result removes the unbounded-stiffness loophole at one exact finite-budget point; it does not make the scalar model a fabricated insulator or clear historical novelty.
