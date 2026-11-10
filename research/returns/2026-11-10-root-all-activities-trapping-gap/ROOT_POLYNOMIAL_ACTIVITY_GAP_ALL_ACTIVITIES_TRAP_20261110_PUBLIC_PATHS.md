ROOT MATHEMATICAL CONSTRUCTION: A GRADED ACTIVITY GAP UNIFORM OVER ALL POSITIVE ACTIVITIES
10 November 2026 Brisbane. Original reaction structure 0<->A+B, B<->2B only. This extends the fixed-lambda nominal certificate to arbitrary positive rational(a,b) with polynomial numerical-activity bounds. The structure's full robust physical realization was already accepted by another method; that physical consequence is counted once.

THE NOMINAL CLOCK. Put lambdaA=a>0,lambdaB=b>0, V=2+a+a^-1+b+b^-1. Let K0 be the accepted fixed sufficient degree for this structure's nominal physical-time Poincare construction, and choose fixed K>=max(2,K0). Write F_j(n)=sum_(l=0)^j binom(n,l), N=A+B, and
 Gamma=1/[4*(K+1)*(1+a)*(1+b)].
Use total rates
 q_pair+=Gamma*a*b*F_K(N), q_pair-=Gamma*A*B*F_K(N-2),
 q_B+=Gamma*b*(K+1)*B*F_(K+1)(N-1),
 q_B-=Gamma*(K+1)*B*(B-1)*F_(K+1)(N-2).
Disabled channels are0. These use only the original channels with every catalyst |w|<=K on the pair linkage, |w|<=K+1 on the B linkage, and coefficients Gamma*ab/w!,Gamma/w!,Gamma*b*(K+1)/w!,Gamma*(K+1)/w!, respectively. They are ordinary positive rational constants<=1/4, with inverses bounded by a fixed polynomial in V. No species/vector/edge changes. Each reversed pair is exactly detailed balanced for pi=Pois(a) tensor Pois(b); the class is N^2. Polynomial activity gives finite pi-activity and nominal nonexplosion.

CLAIM. This fixed design satisfies the pi-centred ACTIVITY-weighted Poincare inequality
 sum pi(x)*activity(x)*(f(x)-pi f)^2 <=G_K(V)*E_pi,Q(f,f)
with an explicit computable fixed-degree polynomial majorant G_K. In addition activity(x)>=c_K*V^-p*(1+N)^2 and pi(activity)<=C_K*V^p, with computable fixed constants. Therefore136C's accepted nominal-only sufficient theorem applies for EVERY a,b,x0,epsilon at the complete bit/physical-firing contract. No new robust physical result for this previously completed structure is counted; the added operation is a parameter-uniform nominal firing-activity certificate.

1. A POLYNOMIAL LYAPUNOV-TO-WEIGHTED-GAP COMPOSITION. Let ANY reversible nominal generator Q have invariant pi, total activity a_Q>0 and an ordinary physical Poincare bound Var_pi(f)<=g E_pi(f,f). Suppose a positive proof function H satisfies
 QH/H<=-ell*a_Q outside a finite set C,
 QH/H<=a_Q everywhere,
and A_C is an explicit bound on a_Q inside C. The reversible ground-state identity gives sum pi*f^2*(-QH/H)<=E_pi(f,f). Apply it to f-pi f. Then
 ell*sum_(outsideC)pi*a_Q*(f-pi f)^2<=E_pi+A_C Var_pi(f),
and the inside contribution is <=A_C Var_pi(f). Consequently
 sum pi*a_Q*(f-pi f)^2
 <=[ell^-1+A_C*(1+ell^-1)*g]*E_pi.
This replaces a finite-atom path/rare-probability bound by the ALREADY accepted physical gap. It is stated for reversible Q; no automatic nonreversible transfer is claimed. Clipping and Fatou justify the domain extension. Thus polynomial g,A_C,ell^-1 suffice, even when C's cardinality and its smallest pi atom are inconvenient.

2. REFERENCE EMBEDDED DRIFT AT ARBITRARY(a,b). Ignore the common time scale and first consider rates
 r_pair+=ab, r_pair-=AB, r_B+=b*B*N, r_B-=B(B-1)(N-1).
Let P0 be this reference embedded chain. Set
 u=1/[10*(1+b)], e=b*u, d=b/[40*(1+b)^2],
 h(0)=1+4u+e, h(1)=4u, h(B)=u*B forB>=2,
 L(A,B)=A+h(B).
L is positive/coercive, L>=u*N, and every original reaction changes L by at most11/10. Write r_tot for the reference total. Exact calculations are:
 B=0: r_tot=ab, Q0 L=-e*ab;
 B=1: r_tot=ab+b+(1+b)A,
 Q0 L=ab*(1-2u)-2ub-A*b*u;
 B=2: r_tot=ab+4b+2+(4+2b)A,
 Q0 L=ab*(1+u)+4u*(1+b)+A*(-2+(8+2b)u);
 B>=3: r_tot=ab+A*B*(B+b)+B*((B-1)^2+bB),
 Q0 L=ab*(1+u)+AB*(-1+u*(b-B))+uB*(-B^2+(b+2)B-1).
Let R0=ceil(1000*(1+a)*(1+b)^2). These formulas imply
 P0 L-L<=-2d whenever N>R0.
Here is explicit all-state accounting. For B=1, Q0 L+2d*r_tot has A coefficient<=-e/2 and constant<=2ab+b; it is nonpositive for A>=20*(1+b)*(2a+1). For B=2 its A coefficient<=-1 and constant<=2ab+1. Both thresholds follow from N>R0.
For B>=3, since 2d<=u/2 and ub<1/10,
 Q0 L+2d*r_tot
 <=2ab-(4/5)AB+uB[-B^2/2+(3b/2+1)B-1/2].
If B<=9*(1+b), the last term is <=13*(1+b)^2, and N>R0 forces A>=ab+7*(1+b)^2. If B>9*(1+b), that last term is <=-u*B^3/4. A>=ab then suffices; otherwise A<ab and N>R0 force B>999*(1+a)*(1+b)^2, whose cubic term pays2ab. B=0 has drift-e<=-2d directly. All bounds are elementary rational comparisons; no finite frequency/state scan or stationary-density estimate is used. Notice d^-1=40*(b+2+b^-1), so the inward margin has polynomial numerical-activity cost.

3. FIXED DEGREE GRADING RETAINS THAT DRIFT. The stated degreeK/(K+1) clock equals Gamma*F_K(N) times the reference rates, with channel-group multipliers
 1, F_K(N-2)/F_K(N),
 (K+1)*F_(K+1)(N-1)/(N*F_K(N)),
 (K+1)*F_(K+1)(N-2)/((N-1)*F_K(N)).
They converge to1 with rational fixed-degree polynomial coefficients, independently of a,b. A computable fixed integer C_K gives |multiplier-1|<=C_K/N for N>=C_K. For completeness, write any ratio as P(N)/Q(N) with equal positive leading coefficient q_D. For N>=1+2*sum_(j<D)|q_j|/q_D, Q>=q_D*N^D/2. Then |P/Q-1|<=2*sum_(j<D)|p_j-q_j|/(q_D*N). Take C_K larger than these finitely many coefficient bounds and K+2. This computes C_K using only the fixed degree, not a spectral search.
Choose
 R=ceil(R0+100*C_K/d+2*C_K+10).
For N>R, row normalisation changes the expected value of a jump bounded by11/10 by <=4*(11/10)*C_K/N<d. Therefore the actual embedded chain P obeys
 PL-L<=-d outside C={N<=R}.
R is a fixed-degree polynomial majorant in a,b,b^-1; it is not enumerated by the compiler. The common time multiplier cancels only for this EMBEDDED row comparison; the exact nominal pi is preserved by the explicitly shifted catalytic reactions, not by an illicit common physical clock change.

4. EXPONENTIAL DRIFT AND CONTROLLED INTERIOR ACTIVITY. Put theta=d/10, H=exp(theta*L), ell=d^2/20. Since d<=1/160 and |DeltaL|<=11/10, Taylor's inequality with exp(theta*11/10)<2 gives
 PH/H<=1-theta*d+theta^2*(11/10)^2<=1-ell outside C,
and PH/H<2 everywhere. H is pi-integrable: it is at most an exponential of population, against Poisson factorial tails. Thus QH/H=activity*(PH/H-1) satisfies Section1. Exponentials appear only in the proof, not in any compiler output/oracle call.
If J_K is the fixed number of labelled channels, every coefficient<=1 and every augmented reactant has degree<=K+3. Hence the explicit rational bound
 A_C=J_K*(1+R)^(K+3)
pays activity inside C. Neither class enumeration nor a smallest pi atom is charged or assumed. A_C and ell^-1 are bounded by fixed polynomials in V; their evaluation uses fixed-exponent rational arithmetic with polynomial binary work.

5. THE ORDINARY PHYSICAL GAP IS ALREADY AVAILABLE. Take the accepted nominal full-catalyst degreeK0 clock atlambda=(a,b), with unit reversible-linkage circulations and its computable polynomial gap majorant g0(V). Its coefficients are c0/w!, c0/(ab*w!),c0/(b*w!),c0/(b^2*w!), respectively, where c0 and c0^-1 obey the accepted polynomial activity bounds. All of its channels are present because K>=K0. The new pair-linkage coefficients are Gamma*ab/c0 times the baseline ones, and the new B-linkage coefficients are Gamma*(K+1)*b^2/c0 times the baseline ones. Therefore
 E_new>=t*E_baseline,
 t=min(Gamma*ab/c0, Gamma*(K+1)*b^2/c0)>0,
so Var_pi(f)<=[g0(V)/t]*E_new.
The inverse t is bounded by a fixed polynomial in V. If the accepted circulation constants are written differently, use the minimum of the finitely many exact coefficient ratios; the same fixed-power bound holds. No physical gap is inferred merely from matching stationary laws. This is a direct compatible-premise comparison, not a request to reprove the accepted baseline.

6. CONCLUSION AND PAID CONTRACTS. Section1 now proves the activity inequality with
 G=ell^-1+A_C*(1+ell^-1)*g0(V)/t.
Every displayed quantity has an explicit computable fixed-degree polynomial bound in V and polynomial complete-binary evaluation cost. The total nominal activity is exactly
 Z=2*Gamma*ab*sum_(j=0)^K(a+b)^j/j!
   +2*Gamma*(K+1)*b^2*sum_(j=0)^(K+1)(a+b)^j/j!,
by Poisson falling-factorial expectations, hence has the required polynomial bound. Finally F_K(N)>=c_K*(1+N)^K for a computable fixed c_K>0, and Gamma*ab has reciprocal polynomial activity size. Thus activity>=c'_K V^-p*(1+N)^2 since K>=2. All136C nominal criteria are satisfied for this structure at EVERY positive rational(a,b). Fixed K/channel tables/preprocessing and all rational rates/constants are charged, ordinary positive coefficients stay<=1, and the state graph is exactly original.

The full independent-error/four-accuracy/time/tolerance/actual-firing conclusion follows by the accepted136C criterion. The robust physical consequence for this particular structure was ALREADY proved with another clock by D123; preserve that antecedent and do not count a second full physical breakthrough. The new construction is a parameter-uniform graded nominal activity certificate, replacing the former fixed-lambda finite-path proof whose rare-atom constants did not give polynomial(a,b) control.

LIMITS AND COMPOSITION. The Lyapunov-to-weighted-gap composition above requires reversibility as written. General weakly reversible networks need not supply reverse physical edges or the same two-variable boundary corrector, and no all-R grading, generic face hierarchy or universal robust compiler follows here. The reference and graded clocks retain exactly this reaction structure. This proof changes the operation available on its trapping prototype, not the full allocation endpoint. No historical priority, practical-rate, new resource or model-policy-effect claim is made.

SOURCES. ROOT_GRADED_TRAPPING_NETWORK_ACTIVITY_GAP_20261110.txt8064/SHA7750f03463f6531bc4ece891d0165c15f0b781c99405f670edfee64958c82f55 supplied the earlier fixed-lambda all-state certificate. ROOT_NOMINAL_CATALYTIC_CLOCK_GAP_20261110.txt10257/SHAdc6469dc52912375e4775bb03eb12325ff5ea850b9fee2ad8856f1b117f32ac9 supplies the accepted ordinary nominal physical gap. Complete136C21802/SHA57aceb232d13713bd83a3362aca11ca8a1dbc1c28912e3a35b4a5213ec26bc7b supplies the nominal-only robustness criterion. All new rate ratios, boundary corrections, drift estimates and polynomial-cost composition are given above; no held primary paper, stationarity oracle or unavailable transfer is substituted. Current scientists retain autonomy and their issued full questions; all known/unknown access/transfer/resource holds, threeXi/Capital/dispatcher, Sol/Dots and existing cadences remain.
