ROOT MATHEMATICAL CONSTRUCTION: A POSITIVE ACTIVITY-WEIGHTED GAP FOR A GRADED TRAPPING NETWORK
10 November 2026 Brisbane. A complete nominal certificate at lambdaA=lambdaB=1, not an all-R or all-activity-vector theorem. The same reaction structure already has an accepted robust physical compiler; this constructs a different sufficient operation previously unavailable for its uniform clock.

THEOREM AND EXACT CLOCK. On the ORIGINAL network 0<->A+B, B<->2B, put F_j(n)=sum_(l=0)^j binom(n,l). Use pair-linkage catalyst degree2 with circulation c=1/6, and B-linkage catalyst degree3 with circulation3c=1/2. The four total rates at N=A+B are
 q_pair+=c F2(N), q_pair-=c A B F2(N-2),
 q_B+=3c B F3(N-1), q_B-=3c B(B-1)F3(N-2).
Disabled rates are0. These are exactly the allowed fixed catalytic channels, coefficients c/w! or3c/w!, including every original w=0 channel. There are32 labelled channels; every coefficient lies between1/12 and1/2. Each reversible translated pair balances atlambda=(1,1), so pi=Pois(1) tensor Pois(1) is exact, the entire original directed graph is retained, and the actual class is N^2. Polynomial intensity and finite Poisson activity give nominal nonexplosion.
Let a be TOTAL labelled intensity. Then
 pi a=8, a(x)>=F2(N)/6>=(1+N)^2/24.
There is an explicitly computable fixed constant G such that
 sum_x pi(x)a(x)(f(x)-pi f)^2<=G E_pi(f,f).
One valid value is G=49*500001*(1+C0), where
 C0=12003*432*(6001!)^2.
The constants are deliberately large and fixed; no spectral or stationary-law oracle is used. This is the activity-weighted inequality required by136C, not merely a physical-time gap or removal of two selected cut tests.

1. A SIMPLE REFERENCE FIRING CHAIN. First take degree0 on the pair linkage, degree1 on the B linkage and circulation1. Its rates are
 q0_pair+=1, q0_pair-=A B,
 q0_B+=B N, q0_B-=B(B-1)(N-1).
The invariant law is again pi, and its total a0 has pi a0=8. Its embedded chain P0 is reversible for rho0=pi*a0/8.
Define the coercive function V(A,B)=A+h(B), where
 h(0)=8/5, h(1)=1/2, h(B)=B/10 for B>=2.
Then V>0, V>=N/10 and every actual jump changes V by at most11/10. Exact generator calculations give:
 B=0: a0=1, L0 V=-1/10;
 B=1: a0=2A+2, L0 V=2/5-A/5;
 B=2: a0=6A+7, L0 V=21/10-3A/5;
 B>=3: a0=(B^2+B)A+B^3-B^2+B+1,
 L0 V=-(B(B+9)/10)A+11/10-B^3/10+3B^2/10-B/10.
It follows that (P0 V-V)<=-1/100 outside the NINE-point set
 F={(A,1):0<=A<=2} union {(A,2):0<=A<=4} union {(0,3)}.
For B>=4 the inequality follows directly from
 L0 V+a0/100=-(9B^2+89B)A/100+111/100-9B^3/100+29B^2/100-9B/100<0;
the constant polynomial is negative atB=4 and strictly decreasing thereafter. B=3,A>=1 and the displayed B=0,1,2 formulas handle the other infinite regions. This is an exact all-state proof, not a finite fixture scan.

2. TRANSFER THIS DRIFT TO THE DEGREE2/3 CLOCK. Let P be its embedded chain. For N>=6000, each new channel-group rate equals c F2(N) times its q0 rate times a multiplier in[999/1000,1]. The multipliers are exactly
 r_pair+=1,
 r_pair-=(N^2-3N+4)/(N^2+N+2),
 r_B+=(N^2-3N+8)/(N^2+N+2),
 r_B-=(N^2-5N+12)/(N^2+N+2).
These follow from F2(n)=(n^2+n+2)/2 and F3(n)=(n^3+5n+6)/6. Every deficit is <=6/N. Therefore normalising the rows changes the conditional mean of ANY jump bounded by11/10 by at most
 (11/10)*(2/999)<1/200.
All states outside C={N<=6000} are outsideF. Hence
 PV-V<=-1/200 outsideC.
The exact common state multiplier cancels in the row; this argument does NOT time-rescale the invariant law or assume the old physical gap transfers without proof.

3. EXPONENTIAL DRIFT WITH RATIONAL CONSTANTS. Put H=exp(V/1000). For a jump DeltaV with |DeltaV|<=11/10,
 exp(DeltaV/1000)<=1+DeltaV/1000+(DeltaV)^2*exp(11/10000)/(2*10^6).
The uniform remainder is <121/(100*10^6), since exp(11/10000)<2. Consequently
 PH/H<=1-1/500000 outsideC,
and PH/H<2 everywhere. H is integrable against rho=pi*a/8, since a has fixed polynomial growth and pi has factorial tails. Exponentials are proof functions; no transcendental oracle is part of the rate/compiler construction.

4. FINITE PATH BOUND AND THE GLOBAL GAP. The embedded chain is reversible for rho. For ANY positive H and bounded f the ground-state identity gives
 E_rho,P(f,f)-sum_x rho(x)f(x)^2*(1-PH(x)/H(x))
 =(1/2)sum_xy rho(x)P(x,y)H(x)H(y)*(f(x)/H(x)-f(y)/H(y))^2>=0.
This identity is a direct expansion plus reversibility, not an imported gap theorem. Take g=f-f(0,0). Every x in C connects to(0,0) by an original reaction path of length<=12003 entirely inside 0<=A,B<=6001. For A,B>=1 create A pairs then adjust B by its existing birth/death reactions; for B=0 create(A+1,1) then remove a pair; for A=0 first use(0,0)->(1,1)->(1,2)->(0,1), then adjustB. These paths add no physical edge.
Every enabled path edge has q>=c=1/6 and pi>=exp(-2)/(6001!)^2>1/[9*(6001!)^2]. Since pi a=8,
 rho(x)P(x,y)=pi(x)q(x,y)/8>=1/[432*(6001!)^2].
Path Cauchy-Schwarz therefore gives max_(x in C)g(x)^2<=C0 E_rho,P(f,f), with C0 as stated. In particular sum_C rho*g^2<=C0 E. The ground-state inequality and the two drift bounds imply
 (1/500000)sum_(outsideC)rho*g^2<=E+sum_C rho*g^2.
Combining them yields
 Var_rho(f)<=[C0+500000*(1+C0)]E_rho,P(f,f)
 <=500001*(1+C0)E_rho,P(f,f).
This is a global embedded Poincare inequality. Periodicity is irrelevant to I-P coercivity; no assertion of absolute discrete-time convergence through a possible eigenvalue -1 is used.

5. CORRECT CENTRE FOR THE PHYSICAL ACTIVITY INEQUALITY. Here d pi/d rho=8/a<=48 and E_rho(8/a)=1. Hence
 (pi f-rho f)^2 <=E_rho[(8/a)^2]*Var_rho(f)<=48*Var_rho(f).
Thus E_rho[(f-pi f)^2]<=49 Var_rho(f). Since E_pi,Q=8 E_rho,P, multiplying by8 proves exactly
 sum pi*a*(f-pi f)^2 <=49*500001*(1+C0)*E_pi,Q(f,f).
Bounded functions suffice first. Value clipping and Fatou extend it to every function in the physical Dirichlet-form domain with finite pi mean. This deals with the pi-centred weight, not just a rho-centred variant.

6. CONSEQUENCE THROUGH THE ACCEPTED NOMINAL CRITERION. The displayed G, lower a>=(1+N)^2/24, exact pi a=8, fixed positive rational channels and their graph/bit contracts satisfy136C's sufficient conditions at THIS activity vector. That theorem therefore supplies the full four-accuracy, independent-error/nonexplosion/recurrence/actual-firing construction for every initial x0 and epsilon with lambda FIXED to(1,1), with computable fixed constants and polynomial numerical x0/epsilon cost. This restricted physical conclusion was already available by the accepted nonradial Foster proof; it is not counted as a second discovery of that same compiler. What has changed is the constructed all-state activity-weighted nominal certificate for a finite graded clock where the uniform menu's firing chain failed.

The rate scales and proof constants are fixed, all precomputation is finite and chargeable; the enormous finite C0 is not a practical-rate or efficiency claim. Extending this certificate uniformly over arbitrary lambda, other networks, all face hierarchies, arbitrary catalyst schedules or the universal allR endpoint is NOT done. No other clock is proved impossible. This result strengthens the preceding two-cut diagnostic ROOT_GRADED_CATALYST_CONDUCTANCE_TRADEOFF_20261110.txt4707/c6db26a9, which did not yet prove an all-state gap. It is optional capital for P3's full question, not a request to reprove a known physical subcase or a replacement assignment.

SOURCE CONTRACT. The use of136C's nominal activity criterion is at its accepted scope: complete21802UTF8/SHA57aceb232d13713bd83a3362aca11ca8a1dbc1c28912e3a35b4a5213ec26bc7b. The shared Poisson/catalytic construction and earlier robust-positive example are accepted D123/8FE1 capital. All drift identities, row comparison, finite path bounds and weighted-centre conversion are given above directly. No unread original, numeric sample, audit requirement, oracle or source substitution is used. All known/unknown access/transfer/resource holds and existing three-seat/Sol/Dots/cadence protections remain; no scientist interruption, new worker/model or additional resource is requested.
