# Compliance-constrained ballistic transport: exact optimum or stiff-mode escape

27 October 2026. Original construction/integration in this owned trajectory. Frozen governing sources: F (complete attainable-spectrum inverse and unconstrained full-Bose theorem), C and A (exact static CM compliance moment). The all-frequency three-moment root lemma was independently derived by the authorised helper; its complete self-contained proof is in `helper/PROOF.md`. Numerical signs stated below are exact enclosures from `certify.py`, not frequency sampling. No historical-priority, specimen, material or practical-device claim is made.

## 1. The fixed physical model and a useful spectral variable

Fix a backbone mass m, total cell mass M>m, intercell spring K>0, temperature theta>0, and a finite positive CM compliance cap Cmax. Put

S=4K, A0=S/m, B=S/M, ms=M-m,
dmax=S ms² Cmax/M².

Every admitted finite connected positive scalar spring/mass network has a full band indicator chi with disjoint acoustic/optical bands and 0<=chi<=1. After dark-band cancellation its exact resources are

T(chi)=integral 2w chi(w)dw=A0,
L(chi)=integral [chi-1_[0,sqrt(B)]]/w dw=0,
W(chi)=integral [chi-1_[0,sqrt(B)]]/w³ dw
      =-ms² C_CM/(2M)>=-dmax/(2B).

These are full-spectrum identities. The objective is J(chi)=integral g_theta(w)chi(w)dw with g_theta=[w/(2theta)/sinh(w/(2theta))]². Physical conductance is k_B J/(2pi).

For A>B and r>0 define p,s by

p²+s²-r²=A, p²s²/r²=B, 0<p<r<s,

or, explicitly,

s²=[r²+A+sqrt((r²+A)²-4Br²)]/2, p²=Br²/s².

Let chi_(A,r)=1_[0,p]+1_[r,s] and j(A,r)=J(chi_(A,r)). This is an actual one-pendant spectrum with backbone S/A and total mass M. Its regularized cubic moment is

W(chi_(A,r))=-(A-B)/(2B r²).

When A<A0 this is an effective heavier-backbone object. Its W is compared with the original fixed-m physical cap; it is not assigned the effective cell's own unrescaled CM compliance.

## 2. General exact infimum theorem

**Theorem.** The infimum of J over all admitted finite networks with the original fixed m,M,K,theta and C_CM<=Cmax equals

j*=min { j(A,r): B<A<=A0, r>0, (A-B)/r²<=dmax }.

The right side has a unique minimizing active spectrum and a unique pair (A*,r*). There are two possibilities:

1. If A*=A0, the infimum is attained by the actual one-pendant cell of mass m, side mass ms and spring k=r*² m ms/M. No extra passive mode can improve it.
2. If A*<A0, no admitted finite network attains the infimum. A sequence of actual positive two-branch stars, all with the exact original masses and cap, converges to it. In this regime a finite two-branch star eventually beats the best legal one-pendant cell. The sequence spends unbounded internal stiffness and does not describe a free physical resource.

This theorem is about the scalar ideal-contact harmonic ballistic model and this precise compliance charge. Its alternative is an optimum versus an infimum, not a claimed finite optimum with an ignored high-frequency band.

### 2.1 Existence inside the two-band family

There are feasible members with j<J_rigid: keep A=A0 and take a sufficiently large finite r. Frozen F proves the missing acoustic tail is a positive multiple of r^-2, whereas the compensating optical contribution is exponentially small. Such a member also has (A0-B)/r²<=dmax.

Every degenerating boundary of the feasible two-band family has limit J_rigid. As r tends to zero, feasibility gives A-B<=dmax r², so A tends to B and the small gap closes. As r tends to infinity, uniformly for B<=A<=A0, p tends to sqrt(B) and s-r<=A0/(2r). As A tends to B with r in a positive compact interval the two bands merge/cancel to the rigid interval, including at the double-root point r=sqrt(B). These statements follow directly from the endpoint formulas and boundedness/continuity of g_theta. Consequently a sublevel set strictly below J_rigid stays in a compact subset with A>B and 0<r<infinity. Its continuous objective attains a minimum there.

### 2.2 Finite-dimensional stationarity creates an all-frequency dual

At any such minimizer fit the unique triple (lambda,a,nu) satisfying

R(w)=g_theta(w)+lambda/w+a w+nu/w³=0 at w=p,r,s.

This is a nonsingular Vandermonde interpolation in w² after multiplying by w³. Differentiating endpoint integrals gives, for arbitrary variations of (A,r),

dj+(a/2)dA+nu dW=0,

because dL=0 and R vanishes at all three endpoints. Since W=-(A-B)/(2Br²), its gradient is independent of the gradient of A. The two active constraint gradients A<=A0 and (A-B)/r²<=dmax are likewise independent. Ordinary finite-dimensional KKT conditions therefore identify

a>=0, nu<=0,
a(A*-A0)=0,
nu[(A*-B)/r*²-dmax]=0.

If nu<0 and a=0, lambda must be positive. Otherwise the positive-root-equivalent entire series has only negative even coefficients and one positive cubic coefficient; Descartes gives at most two positive roots, contradicting p<r<s. Thus nu<0 gives exactly the proper quadrant required by the helper's all-frequency theorem: a>=0, and either a>0 or lambda>0.

If nu=0, frozen F's three-root proof forces lambda<0<a and supplies the same sign conclusion. In particular A*=A0 in this case. The case a=nu=0 cannot have the three prescribed positive roots.

In every case R is strictly negative precisely on the candidate's two occupied bands and strictly positive on their complement. For clarity, the new root argument for nu<0 multiplies w³R by sinh²(w/(2theta))/(w/(2theta))². The resulting entire series has a negative constant, a positive cubic term, and an even coefficient tail with at most one negative-to-positive change. Its full coefficient sequence has at most three sign changes. The self-contained power-series Descartes argument proves at most three positive roots, counting multiplicity. The prescribed endpoints exhaust them. There is no untested high-frequency region.

### 2.3 The dual solves the entire spectral relaxation

Let chi be any finite-band indicator with the same B, T(chi)<=A0 and W(chi)>=-dmax/(2B). Pointwise sign minimization gives

I=integral R(chi-chi*)dw>=0.

All difference integrals converge: each finite connected spectrum equals one near zero and has bounded support. The log moment cancels and

J(chi)-j*=I-(a/2)[T(chi)-A*]-nu[W(chi)-W*]>=0.

Complementary slackness and the constraint signs justify both inequalities. Equality forces chi=chi* almost everywhere because R has only three isolated zeros. Thus the active spectrum is unique. Two strict two-band spectra with the same active indicator have the same optical start and endpoints, so (A*,r*) is unique. This also proves global correctness of the finite-dimensional minimizer without assuming that a general indicator relaxation is positively realizable.

The original physical class has T=A0 and is included in this relaxation. If A*=A0, frozen F positively realizes chi* by the displayed pendant and the lower bound is attained. If A*<A0, equality in the lower bound would force T=A*, contradicting T=A0. Thus no original finite network can attain j*.

### 2.4 Positive two-branch sequence with every moment exact

For the nonattained case put delta=A0-A*>0, d*=(A*-B)/r*²>0. For a large squared frequency H define

B_H=B H/(H+delta),
Q=(1+d*)/B,
t_H=(A*-B_H)/{B_H[Q-1/B_H+delta/(H(H+delta))]}.

For all sufficiently large H the denominator is positive, t_H tends to r*² and A*>B_H. Take a low two-band spectrum with parameters (A*,B_H,r_H=sqrt(t_H)), and append the high band [sqrt(H),sqrt(H+delta)]. For sufficiently large H the three bands strictly interlace. They satisfy exactly

trace = A*+delta=A0,
log product = B_H(H+delta)/H=B,
inverse endpoint sum
 =1/B_H+(A*-B_H)/(B_H t_H)-delta/[H(H+delta)]
 =Q.

The last equality gives W=-d*/(2B), hence exactly the candidate's legal CM compliance. Frozen F's full finite-spectrum inverse now supplies a genuine positive star with two side masses and two springs, backbone m=S/A0, total mass M=S/B and every pass band shown. No difficult realization is left to an oracle.

Endpoint continuity gives convergence of the low-band conductance to j*, and the high-band conductance is bounded by its width times g_theta(sqrt(H)), which tends to zero. This proves the claimed infimum with actual finite networks and retains the whole optical spectrum.

The backbone-incident internal spring sum has the exact full-spectrum formula S(E-A0²)/(2A0²), with E=sum(beta²-alpha²). In this sequence E=2H delta+O(1), so total star stiffness is

k_total=S delta H/A0²+O(1).

Thus stiffness diverges linearly in the squared high frequency. The compliance cap alone does not make the physical design space compact.

### 2.5 A scalar design formulation when the cap binds

Let (A0,r_un) be frozen F's unconstrained optimum and d_un=(A0-B)/r_un². If dmax>=d_un it remains legal and is globally optimal. If dmax<d_un, the new minimizer must have nu<0 (otherwise it would be that illegal unconstrained optimum), so the cap binds. Then

A=B+dmax r²,
0<r<=sqrt((A0-B)/dmax).

The entire constrained infimum reduces to the unique minimizing member of this scalar family. The endpoint interpolation and signs provide a verifiable global certificate for a found minimizer; they do not rely on trusting a local optimiser. The ordinary comparator has the same synthesis information and can use this construction.

## 3. Requested resource point: no extra-mode improvement

For m=1,M=2,K=1,theta=1/2,Cmax=1/4, take k=4 and

p=sqrt(5)-1, r=sqrt(8), s=sqrt(5)+1.

These are exact endpoints of the actual two-unit-mass cell. Its full CM compliance is 1/4. The exact dyadic interval certificate proves

-0.591137020902620 < lambda < -0.591137020902619,
0.039578900151494 < a < 0.039578900151495,
-0.351276884506193 < nu < -0.351276884506192.

The all-frequency dual therefore proves this is the unique optimal active spectrum over every finite admitted passive network under the cap, including arbitrary topology and every band. It automatically is the optimized legal one-pendant comparator k>=4. Its full objective is

J=1.094388522317695923972117822366...,
J_rigid=1.161335871206520783747355441437...,
J/J_rigid=0.942353155061616461360470298716....

The unconstrained smaller k optimum is illegal here. The optimal cap value is not inferred from a parameter sweep.

## 4. A certified severe-cap consequence with an actual extra mode

Keep the same m,M,K,theta and use Cmax=1/20. The strongest legal one-pendant has k>=20. Frozen F's unique stationary point is below k=20, so the optimized pendant is exactly k=20, r²=40. Its full objective is enclosed by

1.142045387542071761716599 < J_pendant < 1.142045387542071761716600.

### 4.1 Exact sharp infimum

Set A(r)=2+r²/20. The exact interpolation coefficient a(r) is positive at r=5.28796811028488 and negative at r=5.28796811028490. The interval certificate also proves lambda>0 and nu<0 throughout that bracket, with A(r)<4. The intermediate value theorem gives an exact root rhat there; at that root a=0 exactly. The all-frequency proof establishes the global lower bound and uniqueness. It is the actual infimum by the preceding positive-star sequence, with

3.398130336769492 < Ahat < 3.398130336769503,
1.1419160253172285 < J_infimum < 1.1419160253172461.

No legal finite network attains this value, since its required trace Ahat is strictly less than 4. This is a proved nonattainment result, not numerical optimizer failure.

### 4.2 An explicit finite positive three-band cell

Choose rational low trace A_l=17/5, delta=3/5 and H=400. The moment-exact formulas give

B_l=4000/2003,
t=r_l²=28144153/971605.

Let p_l²,s_l² be the two positive roots of z²-(t+A_l)z+B_l t=0. The exact squared endpoint data are

alpha=(0,t,400),
beta=(p_l²,s_l²,2003/5).

They strictly interlace. Their full spectrum is

[0,1.37789557131200971012...]
union [5.38206850095806536889...,5.51978850532914415305...]
union [20,20.01499437921479907004...].

For an explicit physical realization write the Stieltjes response as

q(z)=(z²+c z+d)/[z(z+t)(z+400)],
c=698227683/1943210,
d=1125766120/194321.

The leading coefficient fixes backbone mass 1. Let

sigma_1,2=(c -/+ sqrt(c²-4d))/2,
kappa=t+400-c=135344623/1943210,
rho_1=[400t-d-kappa sigma_1]/(sigma_2-sigma_1),
rho_2=kappa-rho_1.

The star's side springs are k_j=rho_j and side masses are m_j=rho_j/sigma_j. Certified positive values are

m_1=0.837991250411562127370665...,
m_2=0.162008749588437872629334...,
k_1=14.178763462407268475012397...,
k_2=55.471260467070245535310727....

The total cell mass is exactly 2; intercell spring is 1; backbone mass is exactly 1; C_CM is exactly 1/20. The full internal spring sum is about 69.6500 (the exact fraction above governs). Thus the extra mode spends additional stiffness and an additional degree of freedom within the declared budget. It is not a fabrication claim or an improvement at equal spring-sum budget.

The certified all-band result is

1.141944111902213589820156 < J_three_band < 1.141944111902213589820157,
0.000101275639858171896442 < J_pendant-J_three_band
                                < 0.000101275639858171896443.

This is about 0.0088679 percent below the optimized pendant, and is a small mathematical improvement. Two side modes suffice for strict improvement in this severe-cap example; one cannot do so. The exact lower bound shows the finite design remains about 0.000028086585 above the infimum.

## 5. Verification, overlap and physical scope

`certify.py` uses only Python's standard library. Its 256-bit dyadic intervals round every arithmetic operation outward. Square roots are enclosed by integer square roots. Positive exponential Taylor sums have an explicit geometric remainder. Bose-band integrals use the convergent full exponential series with a positive tail bound; pi is enclosed by Machin's formula with alternating atan remainders. Exact rational resource equalities and positive masses/springs are separately asserted. `CERTIFICATE.md` is generated by running that file. `network_check.py` supplies independent floating matrix reconstruction; such residuals check implementation rather than replace the analytic result.

The source inverse is classical Foster/Stieltjes synthesis. It is used equally by the conventional comparator. The contribution here is the charged-compliance optimum/infimum theorem, the all-frequency sufficient certificate, the exact solution at the supplied resource point, and an explicit severe-cap positive construction plus nonattainment mechanism. No historical novelty clearance was attempted. Frozen C/A explicitly left this three-moment extremal problem open.

All conclusions remain inside the exact fixed-m scalar rank-one harmonic ideal-contact model. CM compliance is one static aggregate response; it does not bound every internal displacement, material strain or connector mass. The extra-mode gain is small and spends substantial additional stiffness. Multichannel/vector elasticity, finite contacts, anharmonicity, finite specific modulus, full fabrication costs and measured device advantage remain outside the result. The next physically decisive mathematical interface is the jointly charged compliance and internal-stiffness frontier: the escape sequence is then excluded, and the required optimal network order is not established here.
