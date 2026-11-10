ROOT original mathematical preparation, 10 November 2026,12:06UTC review
Polynomial nominal decoding accuracy on infinite classes

SCOPE. This strengthens the qualitative nominal infinite-class boundary in ROOT_FINITE_CLASS_BIMOLECULAR_LIFT_AND_INFINITE_BOUNDARY_20261110.txt,11122ASCII/SHAa1a9b3a7b42f8a72b8850036f0692552f65e6ea38ffc36766650ce2af255000a. That earlier file and the actually posted scientific question remain unchanged. The result below gives a polynomial numerical small-activity choice, nominal recurrence and nominal stationary law/ABSOLUTE moment accuracy on ALL actual classes. It does NOT give the full independently perturbed positive recurrence/mixing/physical-cost compiler.

1. A GENERAL CONDITIONED PRODUCT LAW.
Let Gamma be ANY subset of N^d containing x0. Let e_1,...,e_s be a fixed finite list of nonzero nonnegative integer vectors, and let D_0>=1 bound their orders. Put E a=sum_l a_l e_l and decoder D(x,a)=x+E a. The fine conditioning set is
 Gamma_hat={(x,a):x+E a in Gamma}.
For positive rational lambda and0<theta<=1 give original coordinates activities lambda_i and auxiliary coordinates activities theta lambda^{e_l}. Its conditional product law is
 pi_hat_theta(x,a)=Z_theta^-1 lambda^x/x! * product_l[(theta lambda^{e_l})^{a_l}/a_l!],
 on Gamma_hat.
The target law is pi(x)=Z_0^-1 lambda^x/x! on Gamma. All sums converge because the unrestricted product-Poisson partition converges. The canonical anchor (x0,0) has weight w0=lambda^{x0}/x0! INDEPENDENT OF theta.

Nothing in Sections1--4 requires a chemical process, a finite class, a lattice description or a lower bound on the probability of Gamma.

2. UNIFORM MOMENTS WITHOUT AN AUXILIARY RECIPROCAL.
Write N=|x|_1+|a|_1, n0=|x0|_1,
 A=sum_i lambda_i+sum_l lambda^{e_l},
 G=2+3A+n0^2+n0 sum_i lambda_i^-1.
This G is a directly computable positive rational. For every theta in(0,1],
 Z_theta>=w0,
 sum_(all x,a) exp(N) lambda^x/x! product_l[(theta lambda^{e_l})^{a_l}/a_l!]
 =exp(e[sum lambda_i+theta sum lambda^{e_l}])<=exp(3A).
Also -log w0 <=n0^2+n0 sum_i lambda_i^-1: use log(x0!)<=n0 log(max(1,n0))<=n0^2 and log^+(lambda_i^-1)<=lambda_i^-1.
Consequently
 Pr_pi_hat_theta(N>r)<=min(1,exp(G-r)).
In particular N is stochastically bounded by G plus a unit exponential random variable, uniformly in theta. For every FIXED integer j>=1 one may take
 M_j=2^j j! (1+G)^j,
 E_pi_hat_theta(1+N)^j<=M_j.
Set M_0=1. The same bounds apply to the original pi, by the same anchor calculation with no auxiliary coordinates.

The key point is retaining the ACTUAL zero-auxiliary anchor. Replacing its log weight by n0 times the largest log reciprocal of ALL activities would introduce a spurious log(theta^-1). Replacing logarithms by reciprocal activities would further introduce a spurious polynomial theta^-1. Neither is necessary. For fixed e_l,D_0 and
 W=2+n0+sum_i(lambda_i+lambda_i^-1)+epsilon^-1,
G<=C_R W^{max(D_0,2)} and every displayed fixed-order moment bound is polynomial numerical in W, UNIFORMLY as theta decreases.

3. EXACT AUXILIARY/FALLING-FACTORIAL IDENTITY.
For every l and every nonnegative function h of the decoded population,
 E_pi_hat_theta[a_l h(D(x,a))]
 =theta E_pi_hat_theta[(x)_(e_l) h(D(x,a))].
Proof: on the left shift a_l down by one; its weight contributes theta lambda^{e_l}. On the right shift x down by e_l; its falling factorial contributes lambda^{e_l}. In BOTH sums the remaining point (z,b) must satisfy z+E b+e_l in Gamma and the observable is h(z+E b+e_l). Thus the sums agree term by term. Tonelli applies to nonnegative terms. The moment estimates justify signed observables of fixed polynomial growth as well.

This identity uses the decoder conditioning set exactly, so it remains valid at all boundaries and on rare classes. It does not assume that Gamma is invariant under adding e_l or that auxiliary counts are independent after conditioning.

Let N_aux=sum_l a_l. Then
 p_theta:=Pr(N_aux>0)<=E N_aux<=theta s M_(D_0).
Furthermore, since |D(x,a)|_1<=D_0 N, for every fixed j>=0,
 E[(1+|D(x,a)|_1)^j; N_aux>0]
 <=E[N_aux(1+|D(x,a)|_1)^j]
 <=theta s D_0^j M_(D_0+j).

4. WEIGHTED LAW ACCURACY WITH AN EXPLICIT POLYNOMIAL THETA.
Conditioned on N_aux=0, the decoded law is EXACTLY pi. Hence its unconditional decoded law nu_theta decomposes as
 nu_theta=(1-p_theta)pi+rho_theta,
where rho_theta is a nonnegative measure of mass p_theta. Therefore
 TV(nu_theta,pi)<=p_theta<=theta s M_(D_0).
For every fixed integer j>=0 its weighted absolute variation satisfies
 sum_x (1+|x|_1)^j |nu_theta(x)-pi(x)|
 <=theta K_j,
 K_j=s[D_0^j M_(D_0+j)+M_(D_0)M_j].
The two terms respectively bound the auxiliary-occupied part and its removed mass times the target moment. In particular EVERY original coordinate's ABSOLUTE first-moment error is <=theta K_1. No inference from TV alone is made.

For example choose the ordinary positive rational
 theta=epsilon/[8(1+s M_(D_0)+K_1)].
It lies below one, pays both TV and ABSOLUTE first-moment errors by epsilon/8, and theta^-1<=C_R W^p_R for explicit fixed constants/exponents obtained from the displayed factorials and powers. Its rational bit length and the bit work to compute it are polynomial in COMPLETE binary input length; there is no class-normalizer or real-number oracle. The case s=0 is exact with no error.

Equivalently, the normalizer also obeys a polynomial logarithmic derivative:
 (d/dtheta)log Z_theta=E N_aux/theta<=s M_(D_0),
so log(Z_theta/Z_0)<=theta s M_(D_0). This follows by the same positive-series identity; it is not the exponentially bad crude ratio Z_1/Z_0. The direct event/Palm argument above already proves the required law/moment bounds without this derivative.

5. CONSEQUENCES FOR THE ACTUAL NOMINAL ELEMENTARY LIFT.
Use the previous exact prefix construction from a supplied fixed complex-balanced catalytic table with rates k_r in(0,1]. Every prefix is an auxiliary vector e_l, its actual fine class is exactly Gamma_hat, and all central balanced fluxes are retained. Set the raw binding scale K=1. First binding/release constants are theta,1; later ones are1,1; central constants are k_r/theta for source order>=2 and k_r for source order<=1. Multiply ALL constants by theta. The physical constants are then respectively theta^2,theta; theta,theta; and k_r or theta k_r. Every physical constant is<=1 and >=theta^2 k_min. Thus polynomial numerical rate reciprocals and polynomial binary compilation follow from the accepted original table and the explicit theta above.

Complex balance and its conditional product law are established primary machinery, not new theorems here. The new uniform moment estimate pays the actual fine stationary intensity: with J fixed elementary channel labels,
 a_all(u)<=J(1+|u|_1)^2,
 E_pi_hat_theta a_all<=J M_2.
This includes null and parallel firings as separate labels. The condition sum pi_hat a_all<infinity implies nonexplosion from every state in the actual fine class and positive recurrence/uniqueness of pi_hat_theta there. For a singleton/no-jump class the conclusion is immediate; bounded-intensity labelled self firings are counted separately. Thus the ACTUAL nominal process, with finite normalized rates, realizes the whole target law to the stated TV/ABS-moment accuracy on ALL finite or infinite classes, and has polynomial stationary auxiliary populations and stationary expected firings per unit time. This is stronger than a qualitative theta->0 statement.

It still supplies NO polynomial mixing time or polynomial total firing cost from the prescribed initial state. An elementary global bound from invariance, P_t(u0,u)<=pi_hat(u)/pi_hat(u0), can cost exp(poly(W)); a logarithmic point-weight bound by itself cannot replace a missing physical gap.

6. NONEXPLOSION IS STRUCTURAL FOR EVERY ELEMENTARY DESIGN IN THIS MODEL.
There is a further independent simplification. For ANY finite mass-action network with at most TWO molecules on EACH side and channel constants bounded by3/2, positive changes of the total fine population N can only come from reactions with zero or one reactant molecule. Quadratic propensities cannot accompany a positive total-population increment. Thus for V_j=(1+N)^j,
 Q V_j<=C_j V_j, C_j=6j3^j J,
is a conservative uniform bound; negative population changes have been discarded. Stop at N reaching n, apply finite-state Dynkin/Gronwall, and use j=1 to send n to infinity. The exit probability on a finite time interval is O(n^-1). On every bounded-population set the total labelled intensity is bounded, so infinitely many null/internal firings cannot accumulate there. This proves nonexplosion for every admitted independently perturbed coefficient choice, without a stationary-law premise or weak reversibility.

For each finite T it also gives
 E_(u0,tildek)(1+N(T))^j<=(1+|u0|_1)^j exp(C_j T).
Expected ALL firings to T are at most
 (3J/2)(1+|u0|_1)^2 integral_0^T exp(C_2 t)dt.
This is finite but exponential in T. It is NOT the polynomial numerical full-cycle cost required when T itself may grow polynomially in W. Positive recurrence, stationary perturbation accuracy and a polynomial physical mixing/firing bound remain genuinely unresolved. Neither the drift inequality nor nominal product balance supplies those conclusions for independently perturbed rates.

7. PRIMARY CONTRACTS READ FOR THIS NOTE.
Anderson--Craciun--Kurtz, https://arxiv.org/pdf/0803.3042v1, Theorem4.1 and its complex-flux proof: complex balance supplies a conditional product form on each closed irreducible class; deficiency zero is sufficient, not required. Anderson--Cappelletti--Koyama--Kurtz, https://arxiv.org/pdf/1708.09356v1, Theorem2, its invariant jump-chain argument and Corollaries1--2: a formal invariant law plus finite stationary exit intensity pays nonexplosion. Its introductory counterexamples warn that a formal stationary solution alone is insufficient. These original sources are distinct from all held Anderson--Kim, Plesa, unidentified or other sources; no held-file recovery was attempted.

The prefix graph/balance construction and finite-capacity comparison retain their original scopes. The zero-auxiliary anchor/Palm/weighted-variation calculation is the present addition, not a claim that conditional product form, classical nonexplosion criteria or factorial shifting were invented here. No scientific code, simulation, optimizer, physical experiment or additional worker was used.
