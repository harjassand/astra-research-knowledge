# Independent analytic audit of the quadratic-debt global Foster proof

**Verdict: PASS for the stated exact rate-2 chain, with a finite but unevaluated head.** This is a new whole mathematical review, not inherited acceptance of a local clip or a different architecture. Independent finite checks are separately reported; they supplement the proof below rather than supply its uniformity.

## Binding and scope

Controlling source: `GLOBAL_FOSTER_FINITE_HEAD_AUTHOR.md`, SHA256
`069fcf0b3b861937c8bfcd04252ef0d1693855789915b907d4ce2795644502ec`.
Auxiliary bare-AE source: `AE_EXPONENTIAL_PAID_BY_SIX_RECIPROCALS.md`, SHA256
`86b7b478c65f0b1f238ecdf83501fdfd583867a2cededa521168ea421bafe612`.
Preserved failed linear/angular proposal: `ANGULAR_BASELINE_FAILURE.md`, SHA256
`270c10dfab02ca91022a4b5213aa6f6c8c861c041e84ca4544ea013ee4c433bd`.
The original full charging proof and cutoff-two strengthening, together with their earlier independent audit, are explicitly copied and bound in this audit's input manifest. Their admitted local inequalities are used only where licensed. All new claims, including R, quadratic clipping, the low-debt budget and the all-escape argument, were independently reviewed. Frozen author sources and previous audit files were not modified.

For the exact twelve-channel falling-factorial model and r=1000001/1000000, define
 F=e^tau[1+20 A^2 min(tau^2/4,1)/(B+1)]+10P+R/1000,
 P=1/(c+1)+1/(d+1), R=-A/[(c+1)(d+1)], W=r^N F.
The accepted conclusion is existence of a finite integer Nstar with LW<=-W/60000 on N>=Nstar. Neither Nstar nor a numeric head constant is acquired. No executable all-state admission algorithm, polynomial complexity claim, or evaluated stationary-moment bound is admitted.

## 1. Positivity and the actual charging interface

At positive debt, 2A^2 t<=H<=B/100. For t<2 this bounds p2 by t/800<=1/400; for t>=2 it bounds p2 by1/(200t)<=1/400. At zero debt p2=0. Thus 1<=h2<=21/20. Also A/[(c+1)(d+1)]<=A/(A+1)^2<=1/4, while 0<P<=2. Hence F>=3999/4000>0. In the low-debt region F<30; globally F<=1.05e^t+20.

At a current t>=2, the quadratic-clip debt term equals the accepted uncut charging potential. At EVERY actual successor its value is no larger than that potential. The full generator therefore transfers all charging reserves by successor domination, including successors below the clip. There is no derivative argument at t=2 and no hidden restriction of outgoing transitions.

## 2. Full reciprocal and hub generators

The reciprocal identity follows from the exact c,d changes of all twelve channels. Birth raises both; death lowers both; forward2A channels lower each coordinate twice in total; reverse AC raises d, reverse AD raises c, reverse AE raises both. AB<->CD and both CD/AE directions otherwise preserve c,d. Thus
 LP=(2A^2-A)(B_c+B_d)-(1+AE)(D_c+D_d)-AC D_d-AD D_c.
The first term is below4 when A>=1; at A=0 the whole term is defined as zero without evaluating 1/0. Immigration's extra tilt is <=2delta and death's is favorable. The source retains the additional favorable -(D_c+D_d), correctly.

The R identity is also checked channel by channel. CD exits total -3CD/[(c+1)(d+1)]; AB contributes the opposite-sign AB fraction. The two reverse-arm differences in the source are exact and nonpositive. Each forward channel's positive rate-weighted R increment is <=1: for example its increase is bounded by1/[(c+1)(d+1)], and A(A-1)<(A+1)^2. The single-coordinate version has increment (D+1)/[(c+1)d(d+1)] or its symmetric counterpart and satisfies the same bound. Ordinary birth and death positive costs are each <=1/4. Death tilt costs at most Delta*A(A-1)/(cd)<=Delta<delta; birth tilt on R is nonpositive.

For the AE pair, its AE->CD cost is 1/[(c+1)(d+1)]<=(3/4)(D_c+D_d). For AE->2A, write the positive coordinate-shift effect as at most A D_c/(d+1)+A D_d/(c+2)<=D_c+D_d, discarding the additional negative new-A term. Thus the pair costs <=(7/4)AE(D_c+D_d).

The exact H identity gives B<=A+99E+200Q, with equality at H>0 and Q=0 at H<=0. Using c,d>=A for A>=1 gives the stated AB bound, and 99*(3/4)+7/4=76. All ordinary positive costs plus its A^2 term total9/2+delta. This proves (3) without an omitted channel. At A=0 its sharper formula (4) is exact. In particular CD>0 gives CD/[(C+1)(D+1)]>=1/4.

## 3. Independent check of the bare AE allowance

The auxiliary proof covers the actual positive root and zero-root kink. For t>=4/5, the AE reverse decrease s is positive and below1. The finite polynomial shift, also when 4/5<=t<1, justifies that bound. Its decrease/increase ratio is at least10287/4900, while the adverse increase is <=25/162. The rational inequality (5/8)(10287/4900)>162/137 proves the grouped bare exponential nonpositive.

Below4/5, the two positive root increments are bounded by1/(2cd) and1/[2(c+1)(d+1)], including H<=0 by the successor right-hand sides rather than differentiating through the kink. Exponential chord bounds and the two reciprocal comparisons give coefficient153/28<6. The elementary exponential constants follow from power-series upper/lower bounds. Therefore the entire positive bare AE exponential is paid by six of the ten reciprocals. This allowance concerns the bare exponential only, not its phase.

## 4. Low-debt phase, death retention and quadratic damping

The source's complete bound (6) is valid. Important points checked independently:

* Death always has t'>=t and h2'>=1, so its tilt contribution is at most -Delta*A*e^t. It may be retained in addition to the un-tilted upper remainder. For A>=2, exact shifted-cubic comparison gives z<=6t/A+.02/A^2, z<1, and the phase increment <=7z/800. The resulting normalized full increment is <=(21/8)z. Multiplying by A bounds the un-tilted death remainder by32. For A=1 the crude finite-jump/h2 bounds are smaller. At H<=0, a positive death or forward entrance can occur only at integer H=0; B=A+99E>=A makes the same estimates valid directly.
* For each forward2A channel, the shifted-cubic numerator is t(c+d-1+t)+a/q and its derivative denominator is at least(c-1+t)(d-1+t). This gives the displayed z bound. The prior A^2 z/(B+1)<=1/(20A) estimate and A^2t/(B+1)<=1/200 yield
 (p2'-p2)_+ <=[1/400+1/(80A)]z<=7z/800.
The same upper estimate remains valid across the clip because min(t'^2/4,1)<=t'^2/4. Three rates A(A-1) therefore cost <=(189/4)At+63/400. The two possible H=0 entrances obey the still smaller direct bound; no continuous-root derivative is used at zero.
* Reverse AC/AD positive phase cost is <=At/10+1/10; their negative bare exponential remains available. Both CD positive phases cost <=3At/20+3/20; the negative bare CD->AE exponential is retained. AB is exactly root-neutral and its phase is <=-(5/2)(At)^2. For A>=2 use A(A-1)>=A^2/2, and for A=1 use integer B+1>=3. At t=0 both sides vanish.
* Inequality (7), the sensitive AE-phase estimate, is correct as a grouped finite difference. Put z=1/(2cd)<=1/2. After division by20AE/(B+1), the phase is at most
 (1/2)[e^z(A^2+1)(t+z)^2-A^2t^2].
Using e^z<=2, e^z-1<=2z, A^2z<=1/2 and (A^2+1)z<=1 bounds this by(3/2)t^2+2t+z, precisely (7). For H>0, E/(B+1)<=1/99 gives <=(100/99)At+10/99. If H<=-1, actual phase is zero. Otherwise t=0 and integer H>-1 with A>=1 gives E/(B+1)<=1; the cost is <=10A/(cd)<=10/A<=10. Both AE successors, including ones crossing zero or2, are paid.

The constants sum to17363/400<44 and the At coefficients to9605/198<49. The R polynomial costs at most(13/15)At in low debt after multiplying by kappa; it fits the increase from49 to50 inside e^t. The remaining AE credit is exactly10-6-.076=3.924. Maximizing 50v-(5/2)v^2 gives250, and9*(44+250)+41=2687<2700. Retaining all the stated negative P/R credits therefore proves (8) with the true -Delta*A term. There is no hidden positive A^2 term.

## 5. Charging bound for this same F

For A>=1, kappa's R polynomial is bounded by e^t A^2 using the positive exponential series; the charging reserve loses at most one of its ten quadratic units. The remaining upper bound is
 -e^t(.15+9A^2)+40+20delta+kappa(4.5+delta).
For A=0 the reciprocal budget sharpens to2delta and R is nonpositive, giving -.15e^t+20delta. Since e^2>7 and F<4e^t in this region, both imply D_rF<=-F/100. The source's constants have ample strict margin. The charging and low-debt expressions are the same global function, with actual outgoing successors already included.

## 6. Uniform escape classification, not selected rays

Assume for contradiction an escaping low-debt sequence with D_rF>-1/2000. Bound (8) forces A<=(2700+1/2000)/Delta. Because A is integer, pass to a subsequence with A fixed. Each integer c,d then has a subsequence on which it is fixed or diverges, and compactness gives t->t* in[0,2]. These operations exhaust escapes and do not assume a bulk ratio. All limiting uses of the quadratic expression remain UPPER bounds at t*=2, even when successors cross the clip.

1. **A>=1, a coordinate bounded.** If c is fixed and d diverges, the retained -10AD D_c tends to minus infinity. If both c,d are fixed, bounded debt and the B identity force E to infinity, and the retained AE credit tends to minus infinity. The symmetric case is identical.
2. **Both c,d diverge, t*=0.** Ordinary positive reciprocal and hub costs vanish. The E-dependent R terms are paid by the still-positive reciprocal credit. The remaining R AB polynomial is200kappa*A*Q/[(c+1)(d+1)]->0. Every positive phase term vanishes; for AE, (7) gives convergence to zero either through E/(B+1)<=1/99 at H>0 or through10A/(cd) at H<=0. Forward rates are fixed and their root increments tend to zero. The actual port limit is delta-Delta*A. Bare AE is paid by its six-reciprocal bound. The retained CD hub fraction tends to1, leaving limsup<=delta-Delta*A-.003<=-.002999.
3. **Both c,d diverge, t*>0, A>=1.** H tends to infinity. The actual CD->AE root decrease is asymptotic to1/(2cd); since CD/cd->1 its bare loss tends to-e^t*. Reverse-arm MVT bounds and 1-e^-s>=s/2 give a combined limsup <=-e^t* A t*/2, because the product of C/(d+t+1) and D/(c+t+1) tends to1, regardless of imbalance. If their sum diverges the negative reserve is stronger. Positive reverse phase vanishes; positive CD phase is at most e^t*.075t*(2A+1).
   Pass further so E/B converges in[0,1/99]. If its limit is positive, E is at least a positive multiple of cd, while the reverse-AE debt decrease is bounded below by a positive multiple of t*(1/c+1/d). The opposite increase is O(1/(cd)); hence the actual bare AE drift tends to minus infinity. IMPORTANT: in this branch retain that actual negative drift, do NOT replace it by the six-reciprocal positive upper allowance. The ten reciprocals still pay the .076 E-dependent R price, and the phase AE cost is bounded for fixed A.
   If E/B->0, the exact identity gives E/(cd)->0. The AE phase vanishes and the bare AE pair is eventually nonpositive. Remaining R AB price tends to .2A t*. Combining with the port limit yields
   limsup<=e^t*[delta-Delta*A-1-.5At*+.075t*(2A+1)]+.2At*
   <=e^t*[delta-1-.15At*+.075t*]<=e^t*(delta-1).
4. **A=0, both coordinates diverge, t*>0.** There are no AE/reverse-arm sources. The bare CD loss is-e^t*, positive CD phase <=.075t*e^t*<=.15e^t*, and port tilt <=delta e^t*. Thus limsup<=e^t*(delta-.85).
5. **A=0, exactly one coordinate bounded.** If its value C is0, P's immigration decrement tends to1/2 and coefficient10 gives-5; all positive phases vanish. If C>=1 and t*=0, phases vanish and R's hub loss tends to at most-.003*C/(C+1)<=-.0015. If C>=1 and t*>0, bare CD loss tends to-e^t*C/(C+t*) and its positive phase is at most e^t*(3/40)C t*/(C+t*/2)<=.3e^t*C/(C+t*). Their sum is <=-(.7/3)e^t*. In every case the total positive tilt allowance is <=29delta, safely below the retained reserve. Symmetry covers the other coordinate.
6. **A=0, both coordinates bounded.** E must diverge. Any positive current or successor root forces B to diverge as well, so all quadratic phase terms vanish; otherwise those terms are exactly zero. Bare CD is nonpositive. If CD>0, R's hub reserve is at least3kappa/4=.00075, with total positive port/reciprocal tilt <=29delta. Thus limsup<=-.000721. If CD=0, P immigration instead supplies at least-5.

Every case has a strict bound below -1/2000; the weakest displayed margin is-.000721. This contradicts the presumed escaping sequence. It proves one finite LOW-DEBT head, uniformly over all states, not merely eventual negativity on each ray. In particular the finite bound on A is essential for fixing A before using these limits.

Since F<30 at low debt, the eventual -1/2000 absolute drift implies -F/60000. The charging region has the stronger -F/100 drift. Their union proves the full claimed finite-head Foster inequality.

## 7. Preserved failure, limits and probabilistic receiving

The linear-clip failure is also correct. At A=B=n,C=D=E=0, two forward kink entrances each contribute .05n+O(1) to the linear-phase drift. The fixed negative angular term contributes2beta*n+O(1); true-death tilt contributes-Delta*(1-beta/2)n+O(1); P,R contribute only O(1). The coefficient .1+2beta-Delta*(1-beta/2) is positive for beta>=0 and1<r<=1.01. This refutes that candidate, including beta=0, but not the earlier local charging theorem. Quadratic clipping changes those two phase costs to O(1/n); it is not an unacknowledged reuse of the failed phase.

The actual chain is nonexplosive by N_s<=N_0+I_s and bounded rates on finite N sublevels. The potential has Poisson-integrable finite-horizon supremum since tau<=(3N/200)^(1/3), and multiplying by polynomial rates preserves that integrability. Thus localized Dynkin applies with actual finite jumps. The explicit model is irreducible: immigration supplies A; reverse AC/AD/AE convert each satellite to A; AB->CD followed by reverse arms removes B; deaths clear A. Conversely births and the forward arms create C,D,E, and CD->AB creates B, with excess A removable. Every finite prescribed legal path has positive probability.

A separately included probabilistic consequence explains how the accepted finite-head inequality yields positive recurrence and one stationary exponential moment at this explicit r. Its head constant remains finite but unevaluated. No numeric stationary bound, executable Nstar, algorithmic admission or arbitrary-rate/network extension is inferred. No defect or source repair was required for the admitted mathematical proof.
