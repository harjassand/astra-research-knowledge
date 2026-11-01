# Full rate-2 dynamics: corrected dyadic amplification stage

**Author candidate lemma, pending independent source-level review.** Every actual
channel is retained. This is a conditional stage estimate, not yet a global
recurrence or stationary-moment theorem. The fixed-level mesoscopic input and
post-entry occupation consumer have separate burdens.

## 1. Model and exact correction

The five-species model has unit 0<->A, 2A<->AC, 2A<->AD, 2A<->AE,
AE<->CD, CD<->AB except CD->AE has rate 2. Falling-factorial propensities are
used. Fix a constant reference integer N; N is NOT changed when the actual total
count changes. Put

  L=A+(C+D)/2, Z=C-D, F=L-3E^2/(4N)+AE/N.

The following are exact identities of the FULL generator:

  LA=1-A-3A(A-1)+A(C+D)+3CD-AB,
  LL=1+A+AL+AE-3A^2,
  LE=A(A-1)-2AE+2CD,
  LZ=-AZ,
  q_Z=2A(A-1)+A(C+D),

where q_Z is the predictable quadratic-variation intensity of the Z martingale.
Most importantly,

  L(AE)=E+3ECD+2ACD+A(A-1)^2+2CD
         -AE[B-C-D-2+5A].                                  (1)

Consequently

 LF=1+A+AL-3A^2+E/N+CD/(2N)+2ACD/N
       +A(A-1)^2/N-3A(A-1)/(4N)
       +AE[1+(C+D+2+3E-13A/2-B)/N].                        (2)

The jumps of F are:

| channel | change of F |
|---|---|
| AB->CD | -E/N |
| CD->AB | E/N |
| CD->AE | (A-E/2+1/4)/N |
| AE->CD | (E/2-A+1/4)/N |
| AE->2A | 1+(5E/2-A-7/4)/N |
| 2A->AE | -1+(A-5E/2-7/4)/N |
| AC or AD ->2A | 1/2+E/N |
| 2A->AC or AD | -1/2-E/N |
| 0->A | 1+E/N |
| A->0 | -1-E/N |

Thus the very frequent AB/CD clocks have SMALL F jumps. Treating their jump size
as order one would lose the needed concentration estimate.

## 2. Explicit stage statement

Use deliberately conservative constants

  delta=10^-100, K=10^40, Cstar=3*10^12.

Let N>=10^200 and let K N^(1/5)<=m<=delta N. Write e=sqrt(Nm) and
Tstage=16e/m^2. At the stage start assume

  m<=L<=m+1,
  A<=m/32+1, |Z|<=m/32+1,
  |F|<=m/8, e<=E<=13e/10,
  (1-delta)N<=Ntot<=(1+delta)N.                              (3)

Stop when any of the following occurs: L reaches 2m; the actual total count
leaves the band in (3); the stage deadline Tstage; or an auxiliary tube/clock
boundary listed below. Then the probability that neither L reaches 2m nor the
actual total count exits its band by Tstage is at most

  16 exp[-m/Cstar].                                        (4)

Outside the exceptional event, at an L-success exit the same entrance conditions
hold for the next scale 2m (allowing its displayed +1 overshoot). In particular,
this is a continuing actual-state construction, not a reset of a seed or a frozen
B reservoir. A total-count lower-band exit is a possible service success; an
upper-band exit must separately be charged by the actual immigration process.

## 3. Tube and occupation clocks

Stop additionally at L=m/2, E=e/2 or 2e, A=m/16, |Z|=m/16, or |F|=m/4.
All threshold exits mean first crossing; jump overshoots are at most the respective
bounded jump size. Before these stops,

  C+D<=4m, CD<=4m^2, A<=m/16, E<=2e, N/2<=B<=2N.

Introduce two continuous occupation clocks, stopped at

  H=int A dt <= Hbar=10^4 e/N,
  J2=int A^2 dt <= Jbar=10^7 m e/N.                         (5)

Directly from the full A generator and its A^2 generator, on this tube,

  LA<=13m^2-(N/4)A,
  L(A^2)<=-(N/2)A^2+(3N+24m^2)A+13m^2.                    (6)

The total A-jump intensity is at most 13m^2+5NA. Therefore the stopped A martingale
has bracket at most 10^5 e when H<=Hbar. The A^2 martingale has jumps at most m
and bracket at most 10^5 m^2 e. If H reaches Hbar first, (6), nonnegativity of
terminal A, and A(0)<=m/32+1 force the A martingale to exceed e. If J2 reaches
Jbar before H exits, the second inequality in (6) forces the A^2 martingale to
exceed me. The margins in both implications exceed a factor 100.

For a stopped martingale with positive jumps at most b and bracket at most v,

  P(sup M>=x)<=exp[-x^2/(2(v+bx/3))].                       (7)

For completeness, (7) follows from the exponential compensator inequality
e^(theta z)-1-theta z <= theta^2 z^2/[2(1-theta b/3)] for |z|<=b and theta b<3,
optional stopping of the resulting nonnegative supermartingale, and optimization
in theta. Negative deviations use -M. No occupation law or equilibrium premise
is needed. Applying (7) shows that the two clock exits together cost at most

  2 exp[-e/200002].                                        (8)

## 4. Small drift and bracket of the corrected variable

On the clock budgets (5), integration of (2) gives

  int |LF|dt <=10^9 sqrt(delta) m+4 Tstage <m/64.            (9)

Here |1-B/N|<=delta+4m/N+2e/N. The remaining AE coefficient in (2) has absolute
value at most 32sqrt(delta). Use int AE<=2eHbar=2*10^4m,
int A^2<=Jbar, A<=m/16, CD<=4m^2, and E<=2e. The individual residual classes are
bounded by a constant times m e/N, except the immigration term Tstage and the
integrated E/N term, bounded by 2Tstage. Their sum is less than the displayed
10^9sqrt(delta)m+4Tstage. Finally Tstage/m<=16/K^(5/2), making the last inequality
in (9) literal for the stated constants.

Using the exact jump table, the predictable bracket of the F martingale is at
most 2*10^8 m, and every F jump has absolute value at most 2:

* AB, CD->AB, CD->AE, AE->CD: total compensator <=5*10^4e and jump size <=2e/N,
  so bracket <=2*10^5 m e/N;
* AE->2A: compensator <=2*10^4m and jump size <=2;
* AC/AD->2A: compensator <=4mHbar and jump size <=1;
* all 2A-source channels: compensator <=3Jbar and jump size <=2;
* the two port channels: compensator <=Tstage+Hbar and jump size <=2.

Their displayed upper bounds sum to less than 2*10^8m. Thus (7) gives

  P(sup |M_F|>m/64)<=2exp[-m/(3*10^12)].                   (10)

Together (9), (10), and |F(0)|<=m/8 ensure |F|<=5m/32<m/4. This is the crucial
O(m), rather than O(sqrt(Nm)), concentration calculation.

## 5. E, imbalance, and fast-A boundaries

The E martingale has unit jumps and bracket <=5*10^4e on (5). Hence its absolute
maximum exceeds e/100 with probability at most 2exp[-e/(2*10^9)]. Also

  E(t)-E(0)>=2int CD dt-2int AE dt+M_E(t),
  2int AE dt<=4*10^4m<e/100.

So E cannot fall by as much as e/50 on the good martingale event.

The Z martingale has unit jumps and bracket <=3*10^7m e/N<=3*10^7m. Its damping
is -AZ. The pathwise solution of dZ=-AZdt+dM_Z satisfies
sup|Z|<=|Z(0)|+2sup|M_Z| (integration by parts against the decreasing damping
factor proves this). A bound sup|M_Z|<=m/128 therefore keeps |Z|<m/16. Its failure
probability is at most 2exp[-m/(2*10^12)] by (7).

For the fast-A boundary, upward intensity is at most 13m^2+6eA and downward
intensity at least NA/2. Since e/N<=sqrt(delta),

  L exp(A)/exp(A)<=26m^2-NA/8.

It is nonpositive for A>=a0=ceil(208m^2/N), and a0<=m/64. The exponential barrier
bounds each excursion from a0+1 to m/16 by exp[-m/32] (a weaker bound would suffice).
The initial A<=m/32+1 excursion costs at most exp[-m/64]. The expected number of
subsequent upward excursions is at most the expected upward event count, bounded
by 10^5e. Because e<=N<=m^5 and m>=10^6,

  P(A reaches m/16 before another stop)<=2exp[-m/128].       (11)

This counts failed attempts, rather than assigning a favorable next-jump path.

## 6. No other tube exit; the deadline forces amplification

The entry relation F(0)<=m/8 implies E(0)^2>=7Nm/6. On the good E event,
E>=sqrt(7/6)e-e/50>1.06e. Together with |F|<m/4 and AE/N<m/100,

  L=F+3E^2/(4N)-AE/N>m/2.

Thus the lower-L exit is impossible. The upper E exit is impossible while L<2m:
E=2e would give 3E^2/(4N)=3m, whereas L+AE/N-F<2m+m/100+m/4. The lower E exit
was already excluded by its small possible decrease.

If no successful exit occurs before the deadline, the tube gives

  CD=(L-A)^2-Z^2/4>=m^2/8.

Consequently at the deadline,

  E(Tstage)-E(0)>= (m^2/4)Tstage-4*10^4m-e/100>3.98e,

contradicting E<=2e. Thus an L-success or actual total-count band exit must occur.
At an L-success, L is in [2m,2m+1], A and |Z| are at most m/16+1,
|F|<=5m/32<(2m)/8, and the same identity yields E in
[sqrt(2Nm), (13/10)sqrt(2Nm)]. These are (3) for the next scale.

Adding (8), (10), the E and Z bounds, and (11), and using e>=m, gives a bound
less than 16exp[-m/Cstar], proving (4).

## 7. What composition of the lemma does and does not earn

Starting from a received entrance at m0=K N^(1/5), a dyadic sequence reaches a
fixed positive-fraction L level (between delta N and 2delta N) unless a total-count
band exit occurs. The sum of stage deadlines is at most

  16 sqrt(N)/m0^(3/2) / (1-2^(-3/2))=O(N^(1/5)/K^(3/2)),

and the sum of stage failure probabilities is at most

  32 exp[-m0/Cstar]

for all sufficiently large N. There are O(log N) actual stages; no state resets
are performed. A lower total-count band exit earns a fixed fractional loss. An
upper exit must be charged by the actual Poisson immigration process over the
whole paid deadline, not declared harmless.

The earlier fixed-level mesoscopic law receives the entrance with probability
tending to one, but its proof killed the first rare omitted channel. That proof
ALONE does not provide an exponential entrance-failure estimate. An exponential
moment consumer must upgrade that initial phase by retaining every channel and
using the same clock/exponential-martingale method, and must also receive the
post-entry long-time interior occupation block. This lemma does not silently
import either result or claim recurrence/stationary moments.

## 8. Constants and actual cost

All stage constants are explicit rationals/integers except the algebraic length
e=sqrt(Nm) and the exponential probability expression. They can be represented
exactly as finite arithmetic/root expressions; numerical evaluation requires a
stated precision budget. The proof has no simulation, frozen equilibrium oracle,
or face-enumeration cost. A pathwise stage implementation still observes the
actual CTMC and its occupation clocks; this mathematical certificate is not an
operational controller. The astronomical delta and K are conservative existence
costs, not practical rates or sharp constants.
