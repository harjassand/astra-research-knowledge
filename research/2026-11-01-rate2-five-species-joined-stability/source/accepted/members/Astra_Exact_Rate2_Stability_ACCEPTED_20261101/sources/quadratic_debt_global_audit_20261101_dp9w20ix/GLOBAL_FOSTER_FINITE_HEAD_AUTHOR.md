# Explicit quadratic-debt potential: finite-head global Foster author proof

**Status: author proof, frozen for independent audit.** This is a mathematical finite-head existence claim for the specified five-species rate-2 chain. The head is proved finite but is not evaluated. It is not an executable all-state admission algorithm or an evaluated stationary-moment bound. Prior local freezes are not changed.

## 1. Model, parameters, and explicit potential

The exact chain has port 0<->A, rates 1 and A, and reversible internal pairs
2A<->AC, 2A<->AD, 2A<->AE, AE<->CD, CD<->AB. Every rate constant is1 except CD->AE, whose constant is2. Falling-factorial 2A propensity is A(A-1). All twelve source channels are included below.

Set

  a=1/100, q=2, r=1+10^-6, delta=r-1, Delta=1-1/r, kappa=1/1000,
  c=A+C, d=A+D, H=(B-A-99E)/100, N=A+B+C+D+E.

Let t=tau=0 when H<=0; otherwise let t be the positive root of

  2 Q(c,d,t)=H,
  Q(c,d,t)=cdt+(c+d)t²/2+t³/3.

Put

  m2(t)=min(t²/4,1), p2=A² m2(t)/(B+1), h2=1+20p2,
  P=1/(c+1)+1/(d+1), R=-A/[(c+1)(d+1)],
  F=exp(t)h2+10P+kappa R, W=r^N F.

Write D_r f=r^-N L(r^N f). The claimed conclusion is:

> There exists a finite integer Nstar such that
> L W <= -(1/60000) W on every state N>=Nstar.

A finite-head additive constant then gives a global Foster inequality. The proof below establishes the entire outgoing generator at each state and a common strict margin along every escaping low-debt sequence; it does not restart episodes or assume interface continuity.

## 2. Global bounds and charging receipt

Since 2A²t<=H<=aB whenever t>0,

  0<=p2<=1/400, 1<=h2<=21/20, -1/4<=R<=0, 0<P<=2.

Consequently F>=1-kappa/4>0, and F<=1.05 exp(t)+20. For t<2, F<30.

Let U=r^N exp(t)[1+20A²/(B+1)] be the already audited charging potential.
At a current state t>=2, r^N exp(t)h2=U; at EVERY actual successor its value
is at most U. Thus exact successor domination transfers the frozen theorem:

  D_r(exp(t)h2)
   <=-exp(t)h2[3/20+10A²+(t/4){AC/(d+t+1)+AD/(c+t+1)}].       (1)

This includes jumps crossing t=2; it is not a differential cutoff argument.
The source proof is `activation_debt_stopped_certificate_20261101/STRENGTHENED_CUTOFF_TWO.md`, SHA256 6aae3e98af55eda8500d34b5add9cb3e9c9ff5df938a32c566d9d44184d8e5b7, together with its original full-generator proof. Their independent audit has already passed.

## 3. Exact reciprocal and hub corrections

Set

  B_c=1/[c(c+1)], D_c=1/[(c+1)(c+2)],

and similarly for d. Terms containing B_c or B_d below occur only when A>=1,
so their denominators are positive. Direct finite jumps give

  LP=(2A²-A)(B_c+B_d)-(1+AE)(D_c+D_d)-AC D_d-AD D_c.

The port tilt has upper cost 2 delta; its death contribution is favorable.
The positive first term is <4. Therefore

  D_r P <=4+2delta-(1+AE)(D_c+D_d)-AC D_d-AD D_c.              (2)

For R, the two CD exits give exactly -3CD/[(c+1)(d+1)]. AB gives
+AB/[(c+1)(d+1)]. Reverse AC and AD are favorable, exactly

  Delta_AC R=-(D+1)/[(c+1)(d+1)(d+2)],
  Delta_AD R=-(C+1)/[(d+1)(c+1)(c+2)].

Each forward 2A channel has positive rate-weighted R cost at most1. For the
AE pair, AE->CD has change1/[(c+1)(d+1)] <=(3/4)(D_c+D_d), while the positive
part of AE->2A is <=D_c+D_d. Its aggregate cost is therefore at most
(7/4) AE(D_c+D_d).

The positive birth and ordinary death R costs are at most1/4 each; the
adverse death tilt is at most delta. Thus all these ordinary positive costs
sum to at most7/2+delta.

The exact identity when H>0, and corresponding inequality when H<=0, are

  B<=A+99E+200Q(c,d,t).

For A>=1 this gives

  AB/[(c+1)(d+1)]
   <=1+(297/4) AE(D_c+D_d)
      +200 A t[1+t/A+t²/(3A²)].

Combining, and defining the last polynomial term to be0 at A=0,

  D_r R <=9/2+delta+76 AE(D_c+D_d)
      +200 A t[1+t/A+t²/(3A²)]-3CD/[(c+1)(d+1)].             (3)

All discarded reverse-arm terms are nonpositive. At A=0 the sharper exact
formula is

  D_r R=-r/[(C+2)(D+2)]-3CD/[(C+1)(D+1)].                  (4)

In particular CD>0 supplies at least3/4 of hub reserve at A=0. If CD=0,
P's immigration decrease includes at least1/2. No inactive-state indicator
is needed in this representation.

## 4. The complete bare AE exponential is paid by six reciprocals

Let t1,t2 be the actual successor roots for AE->2A and AE->CD. The separate
finite-jump proof `activation_debt_global_repair_20261101/AE_EXPONENTIAL_PAID_BY_SIX_RECIPROCALS.md`, SHA256 86b7b478c65f0b1f238ecdf83501fdfd583867a2cededa521168ea421bafe612, proves

  exp(t1)+exp(t2)-2exp(t) <=6(D_c+D_d).                      (5)

Its proof explicitly covers H<=0. It also proves this grouped exponential
is nonpositive already for t>=4/5. For reference, positive increments below
that threshold are at most1/(2cd) and1/[2(c+1)(d+1)]; reciprocal comparisons
and exp(4/5)<9/4 give the coefficient6. Thus (5) uses actual finite roots,
not a derivative across the kink.

## 5. Full low-debt budget, retaining true death and fast quadratic damping

Here 0<=t<2. Write v=A t. Separate the bare AE contribution from exp(t),
so it can be paid by (5). Every other positive cost, plus the phase AE cost,
satisfies

  D_r(exp(t)h2) - [bare AE exponential contribution]
    <=exp(t)[44+49v-(5/2)v²-Delta A].                       (6)

The following channel-by-channel receipt supplies (6).

* Immigration costs at most1 after division by exp(t), using h2<=21/20.
* Death retains -Delta A after division by exp(t), because death cannot lower
  t and its successor h2>=1. Its un-tilted positive remainder is at most32.
* For a forward 2A jump, A>=2. Let z=(t'-t)_+. Direct cubic comparison gives

      z<=6t/A+.02/A², z<1,
      (p2'-p2)_+ <= (7/800) z.

  To check the phase estimate, first use the previously established bound
  A²z/(B+1)<=1/(20A), together with A²t/(B+1)<=a/q. Then

      (p2'-p2)_+ <= A²[t z/2+z²/4]/(B+1)
                   <=[1/400+1/(80A)]z <=7z/800.

  The normalized multiplier increment is at most(21/8)z. The three rates
  A(A-1) therefore cost at most(189/4)v+63/400. If H<=0, positive successor
  debt is possible only at H=0 for the AC/AD forward arms (100H is integer);
  B=A+99E>=A and z<=a/[q(A-1)²], giving the same bound with v=0.
* The death estimate uses the same bound for A>=2, multiplied by A rather
  than A(A-1): it is less than32. For A=1, the crude finite-jump increase
  t'-t<1 and h2<=21/20 suffice. This also treats H<=0 directly.
* Reverse AC/AD exponential terms are favorable. Their combined positive
  phase cost is at most v/10+1/10, using AC t/(B+1)<=a/q and its symmetric
  counterpart. They can be retained when needed rather than discarded.
* The combined CD positive phase cost is at most3v/20+3/20. The CD->AE bare
  exponential term is favorable and is retained in the escape argument.
* AB preserves t. If t>0, integer B>A. Its exact phase term is

      20 m2(t)[-A(2A-1)+A³/(B+1)] <=-(5/2)v².

  For A>=2, use A(A-1)>=A²/2. For A=1 use B+1>=3 directly. At t=0 both sides
  vanish.
* For the AE **phase**, put z=1/(2cd)<=1/2. Each successor root is at most
  t+z, even at H<=0. Since m2(t')<=t'²/4, grouping the squares (A+1)² and
  (A-1)² bounds its normalized contribution by

      20 AE/(B+1) [ (3/2)t²+2t+1/(2cd) ].                  (7)

  If H>0, E/(B+1)<=1/99, so (7) is at most(100/99)v+10/99.
  If H<=-1 it is zero. Otherwise t=0 and E/(B+1)<=1, so it is at most10/A<=10.
  Thus (100/99)v+10 is a uniform bound. This explicitly receives both AE
  successors becoming positive-debt states at the root kink.

The constants sum to17363/400<44, and the v coefficients sum to
9605/198<49. This proves (6), with no angular baseline or uncharged channel.

Combine (2)--(6), with10P and kappa R. At t<2, (3)'s polynomial is at most
(2600/3)A t; multiplying by kappa and absorbing it into exp(t) increases49v
to less than50v. After paying (5), the remaining AE coefficient is
10-6-76kappa=3.924. The constant positive cost outside exp(t) is less than41.
Since exp(t)<9 and max_v>=0(50v-(5/2)v²)=250, the full explicit inequality is

  D_r F <=2700-Delta A-3.924 AE(D_c+D_d)
       -10(D_c+D_d)-10AC D_d-10AD D_c
       -.003 CD/[(c+1)(d+1)],        t<2.                   (8)

This is a global low-debt bound, not yet by itself a uniform negative drift.
It guarantees negative drift for all sufficiently large A, and retains the
credits needed for every remaining escape case.

## 6. Charging region is received by the same global function

For t>=2, use (1), (2), and (3). The 76kappa AE price is paid by10P. If A>=1,

  .2 A t[1+t/A+t²/(3A²)] <=.2 A²[t+t²+t³/3] <=exp(t)A².

The last inequality follows from the positive exponential power series.
Consequently

  D_r F <=-exp(t)(.15+9A²)+40+20delta+kappa(4.5+delta).

For A=0, (2) is sharpened to the exact immigration expression, whose upper
bound is2delta; (4) is nonpositive. Hence

  D_r F <=-.15 exp(t)+20delta.

Using exp(2)>7 and F<=1.05 exp(t)+20<4exp(t), both cases imply

  D_r F <=-F/100,                         t>=2.              (9)

The actual outgoing interface has already been included; (9) and (8) concern
the very same globally defined F.

## 7. Exhaustive escape-sequence proof of a finite low-debt head

Let eta=1/2000. Suppose no finite low-debt head had D_r F<=-eta. Then there
would be states x_n with N_n->infinity, t_n<2, and D_r F(x_n)>-eta.
By (8), A_n is bounded by(2700+eta)/Delta. Passing to a subsequence fixes its
integer value A. Each of c_n,d_n can then be passed to a subsequence on which
it is either a fixed integer or tends to infinity. Also pass to t_n->t* in[0,2].
These choices exhaust all escapes; no presumed fixed bulk ratio is imposed.

### 7.1 A>=1 and at least one rare coordinate stays bounded

If, say, c is fixed and d->infinity, the term -10AD D_c in (8) tends to minus
infinity. If both c,d are fixed, bounded t and the identity/inequality for B
force E->infinity whenever N->infinity. The AE term in (8) then tends to minus
infinity. Both contradict D_r F>-eta. The symmetric case is identical.

### 7.2 c,d both tend to infinity and t*=0 (any fixed A)

All ordinary positive reciprocal and hub terms tend to zero, except the
E-dependent AB/AE terms of R, which are paid by the spare reciprocal AE credit
as in (3),(5). The remaining AB price is200kappa A Q/[(c+1)(d+1)]->0.
All positive quadratic phase terms tend to zero: the CD and reverse-arm bounds
are O(t(2A+1)); forward 2A rates are bounded and their actual root changes tend
to zero; for AE use (7), which tends to zero when H>0, and is either zero or
at most10A/(cd) when H<=0. The birth phase also vanishes. The non-AE bare debt
terms are nonpositive except the port; their positive port limit is
(delta-Delta A). Bare AE is paid by (5).

Meanwhile CD/[(c+1)(d+1)]->1, giving the retained hub limit -3kappa. Thus

  limsup D_r F <=delta-Delta A-3kappa <=-.002999<-eta.         (10)

In particular the root-kink case does not borrow a nonexistent full unit CD
exponential loss.

### 7.3 c,d both tend to infinity and t*>0, A>=1

Here H->infinity. The bare CD->AE contribution tends to -exp(t*): its rate
is2CD~2cd and its root decrease is asymptotic to1/(2cd). Reverse-arm debt
terms have the exact lower reserves s_C>=t/[2(d+t+1)] and
s_D>=t/[2(c+t+1)], with decreases below1. Thus their combined bare contribution
has limsup at most

  -exp(t*) A t*/2,

using 1-exp(-s)>=s/2 and the arithmetic-geometric mean bound on
C/(d+t+1)+D/(c+t+1), whose product tends to1. If the sum diverges, the conclusion
is stronger. Their positive phase parts tend to zero, since B>=200cdt and
A is fixed. The CD positive phase has limsup at most
exp(t*) .075t*(2A+1). The AB phase is nonpositive and may be discarded.

Pass further so E/B has a limit. If this limit is positive, the bare AE
contribution tends to minus infinity: its AE->2A decrease is asymptotic to
at least a positive multiple of t*(1/c+1/d), while the opposite increase is
O(1/(cd)); E>=const B>=const cd, so AE times their negative difference diverges.
All phase AE costs remain bounded by (7), and the E-dependent R cost is paid
by P. This case contradicts the presumed drift lower bound.

If E/B->0, the exact B identity gives E/(cd)->0, because Q/(cd)->t*.
The AE phase (7) then tends to zero; the bare AE pair is eventually nonpositive
since its decrease/increase ratio tends to infinity. E-dependent R costs remain
paid by P. All other positive P,R costs vanish; R's remaining AB price tends
to .2A t*. Together with the port limit, this gives

  limsup D_r F
   <=exp(t*)[delta-Delta A-1-.5A t*+.075t*(2A+1)]+.2A t*
   <=exp(t*)[delta-1-.15A t*+.075t*]
   <=exp(t*)[delta-1]<-eta.                                 (11)

The estimate is uniform over imbalance; no limit of C/D was required.

### 7.4 A=0 and c,d both tend to infinity, t*>0

There is no AE or reverse-arm source. The bare CD loss again tends to-exp(t*),
and the phase cost is at most .075t* exp(t*)<=.15 exp(t*). Port tilt contributes
at most delta exp(t*); all positive P,R terms vanish. Hence limsup D_r F is
at most exp(t*)[delta-.85], again strictly below-eta.

### 7.5 A=0 and exactly one coordinate stays bounded

Take c=C fixed, d->infinity. If C=0, P's immigration decrease tends to1/2;
its coefficient10 supplies -5. All positive U2 phase terms vanish, because
CD=0 and the birth phase tends to zero. Bare birth costs at most9delta.
The reciprocal birth tilt is at most20delta; R is nonpositive. Thus the
limsup is at most-5+29delta.

If C>=1 and t*=0, phase costs vanish and R's hub credit tends to
-3kappa C/(C+1)<=-3kappa/2. Bare CD is nonpositive, and all port tilt costs
are at most29delta. The limsup is therefore below-eta.

If C>=1 and t*>0, H->infinity and the bare CD contribution tends to
-exp(t*) C/(C+t*). The positive CD phase has limsup at most

  exp(t*) (3/40) C t*/(C+t*/2)
  <=exp(t*) .3 C/(C+t*),

using t*<=2. Thus their sum is at most
-.7 exp(t*) C/(C+t*)<=-(.7/3)exp(t*). Birth contributes at most9delta,
reciprocal tilt at most20delta, and the other corrections help. Again the
limsup is below-eta. The symmetric case is identical.

### 7.6 A=0 and both coordinates stay bounded

N->infinity forces E->infinity. If any current or successor root is positive,
B must then tend to infinity, and all quadratic phase terms tend to zero;
otherwise they are exactly zero. Bare immigration is at most9delta, bare CD
is nonpositive, and reciprocal birth tilt is at most20delta. If CD>0, R's
hub credit is at most-3kappa/4=-.00075, leaving

  limsup D_r F <=-.00075+29delta=-.000721<-eta.

If CD=0, P immigration instead supplies at least-5, with the same small
positive tilt allowance. This is the last case.

Every escaping sequence has a subsequence in one of7.1--7.6, each with a
common strict limsup below-eta. This contradicts the assumed sequence and
proves existence of a finite integer Nstar for which

  D_r F<=-1/2000,                     t<2, N>=Nstar.          (12)

The proof is a uniform escape-sequence argument, not an assertion that selected
rays look negative. It establishes existence of a head, not its executable value.

## 8. Global Foster statement and legitimate consequences

For t<2, F<30, so (12) yields L W<=-W/60000. For t>=2, (9) is stronger.
Thus the stated finite-head global inequality follows. There are finitely many
states N<Nstar; the maximum of LW+W/60000 over that head gives a finite
additive constant K. The function is norm-like since F>=1-kappa/4 and r>1.

Nonexplosion follows from N(s)<=N(0)+I(s), with unit-rate Poisson immigration.
Also tau<=(3aN/2)^(1/3), so W is bounded above by a constant times
r^N exp[(3aN/2)^(1/3)], which supplies finite-horizon localization integrability.
No unstated reset, frozen fiber, hitting-time definition, or external control
enters the potential. Standard irreducible countable-chain Foster receiving may
be applied after this author theorem survives independent audit. This file does
not claim an evaluated stationary moment constant or a computationally acquired
finite head.
