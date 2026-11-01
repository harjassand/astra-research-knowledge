# Independent mathematical review: retained full rate-2 dyadic stage

## Verdict and controlling interpretation

**PASS for the conditional full-chain stage probability estimate with the stated constants, and for its carefully stopped dyadic composition.** No numerical-constant correction is needed. Two stopping conventions must be explicit:

1. **A total-count band exit takes priority over a simultaneous L hit.** “L-success supplies the next entrance” means an L hit while the actual total remains in the band. An immigration can change both quantities on the same jump; it is not legitimate to continue from an out-of-band state merely because that jump also hit L=2m. The saved exact witness demonstrates the possible tie. Auxiliary-boundary events in the exceptional-event accounting include the terminal jump, so simultaneous auxiliary hits are not omitted.
2. A terminal dyadic-stage endpoint can overshoot its target by at most one. One may report the conservative bound L<=2 delta N+1. Alternatively, to obtain literally a level between delta N and 2 delta N, stop at the first actual L>=delta N; then L lies in [delta N,delta N+1], a subset of that interval since delta N>=1. This early final stopping does not increase the paid time or failure probability.

These conventions do not change (4), its exponent, or its deadline. The unprioritized interpretation that *every* L hit, even a simultaneous band exit, supplies the next in-band entrance is **not accepted**.

Exact source: `EXACT_CORRECTOR_AND_STAGE_LEMMA.md`, 10,053 bytes, SHA256 `0ddcfb78c068ae58c2e5ddae1da015ba70d76acae67a2b0e9104f7358775e0a2`. Author-stage manifest SHA256 `53686515708c0a407cb76b2d748f44efc5b7b7e2e845cd859b35f934ff8f6b9b`. All four manifest payload hashes match and are preserved. The earlier mesoscopic source is read as history, not inherited as an entrance/consumer theorem. The deterministic primary-source receipt is bound as an unchanged companion only; no step here relies on the cited external paper, and no external retrieval was made.

This is a mathematical component review, not executable/numerical receiving. The independent script imports no author code. It passed **1,393 exact assertions**, including global polynomial coefficient identities and uniform normalized constant envelopes. The 1,200 finite polynomial-evaluation checks are supplementary implementation checks, not a substitute for the continuum argument below.

## 1. Actual chain, fixed reference and exact algebra

The full model has all twelve directed channels from the pairs

    0 <-> A,
    2A <-> AC, 2A <-> AD, 2A <-> AE,
    AE <-> CD, CD <-> AB,

with coefficient two only on CD->AE and coefficient one elsewhere. The falling-factorial intensity of a 2A source is A(A-1), not A(A-1)/2. Every A jump is +/-1. Internal channels conserve total count; the port changes total by +/-1. Consequently Ntot(t)<=Ntot(0)+I(t), where I is the actual unit immigration Poisson count. This also proves nonexplosion on every finite horizon: total is bounded by a finite random count and all finitely many binary intensities are then bounded.

The reference N in F is a fixed parameter. It is not replaced by Ntot(t); doing that would introduce different port increments and a different generator calculation.

An independent exact polynomial engine uses variables A,B,C,D,E and w=1/N. It expands each literal increment and the complete generator. Equality is checked coefficient by coefficient, not at one selected N or state. It verifies all claimed LA, LL, LE, LZ, L(AE), LF identities and all twelve corrected-F increments. It additionally obtains

    qA = 1+A+3A(A-1)+A(C+D)+2AE+3CD+AB,
    qE = A(A-1)+2AE+2CD,
    qZ = 2A(A-1)+A(C+D),
    L(A^2)=2A LA+qA.

The exact A^2 drift expanded in a useful form is

    1+7A^2-6A^3+2A^2(C+D)+6ACD-2A^2B
      +A(C+D)+2AE+3CD+AB.

These are identities of the actual full chain. In particular the two fast AB/CD directions have corrected-F increments +/-E/N. CD->AE and AE->CD have increments `(A-E/2+1/4)/N` and `(E/2-A+1/4)/N`; they are also small. The frequent fast channels have not been deleted, replaced by an equilibrium law, or assigned order-one F jumps.

## 2. Uniform parameters and stopping framework

Write rho=e/N=sqrt(m/N), and denote the deadline by T. The hypotheses imply uniformly

    m>=10^80,  1/N<=10^-200,
    rho<=10^-50,  m/N=rho^2<=10^-100,
    T/m=16sqrt(N)/m^(5/2)<=16*10^-100.

The last bound follows from m^5>=K^5 N and K=10^40. These uniform extrema, not one huge fixture, control the numeric margins below. Algebraic m and e are allowed; the underlying counts are integers and L is half-integral. All thresholds are first crossings, with the terminal jump included.

Let sigma be the first of the upper L target, either total-band exit, deadline, auxiliary L/E/A/Z/F exits and the two continuous occupation-clock exits. Every martingale below is stopped at this *same* sigma. At pre-jump times before sigma,

    m/2<L<2m, A<m/16, |Z|<m/16, e/2<E<2e,
    C+D=2(L-A)<=4m,
    A+C+D=2L-A<=4m,
    CD<=4m^2.

The actual total-count band then gives

    B/N >= 1-delta-4m/N-2e/N >1/2,
    B/N <=1+delta<2.

Initial A and Z are strictly inside their auxiliary tubes since m>=10^80. At sigma, each count-coordinate overshoot is at most one, A^2 has the corresponding bounded increment, and F's exact jump table applies to the pre-jump state. Drift and bracket integrals use pre-stop states, so terminal overshoot does not invalidate their bounds. When excluding an auxiliary exit on the good event, post-jump bounds A<=m/16+1 and E<=2e+1 are sufficient.

For each fixed N,m, all pre-stop counts and rates are bounded and T is finite. Stopped counting-process compensators therefore give square-integrable Dynkin martingales and valid optional stopping. No equilibrium, occupation law, reset or unexplained uniform-integrability limit is required. At later actual stage-entry stopping times the same conditional calculation applies to the continuing full chain, with the same fixed N and newly reset *analysis clocks*, not a reset state.

## 3. The two occupation clocks are not circular assumptions

Using the exact A drift, the positive terms satisfy 1+3CD<=13m^2, while B-2-(C+D)>=N/4. Thus

    LA<=13m^2-(N/4)A.

In the expanded A^2 drift, combine -2A^2B<=-NA^2 with `7A^2+2A^2(C+D)<= (7+8m)A^2`; the latter costs less than N A^2/2. Also

    6ACD<=24m^2 A,
    A(C+D)+2AE+AB <= (4m+4e+2N)A <=3NA,
    1+3CD<=13m^2.

This proves exactly the second inequality (6), not merely the weaker result obtained by combining a loose qA bound with LA. Separately the full qA obeys `qA<=13m^2+5NA` on the tube.

At the common stop, H<=Hbar=10^4e/N and J2<=Jbar=10^7me/N pathwise; these are stopping budgets, not asserted occupation laws. Therefore

    <MA> <=13m^2 T+5N Hbar =50208e <10^5e.

The absolute A^2 increment is `|2A+/-1|<=m/8+1<m`, including the exit mark, so `<M_A2><=10^5m^2e`.

If H reaches Hbar at sigma, nonnegative terminal A yields

    MA >= (N/4)Hbar-13m^2T-A(0)
        >=[2500-208-rho(1/32+1/m)]e >100e.

If J2 reaches Jbar before another exit, the A^2 inequality and H<=Hbar give

    M_A2/(me) >=5*10^6-30208/m-240000rho^2
                         -rho(1/32+1/m)^2 >100.

Thus the claimed weaker thresholds e and me are safely forced. These statements use the deterministic clock ceilings of the common stopping time. The subsequent probability estimate is not assuming in advance that the clocks fail to exit.

For bounded martingale jumps, the exponential compensator bound follows directly from

    exp(theta z)-1-theta z
      <=theta^2 z^2/[2(1-theta b/3)]  (|z|<=b, theta b<3).

The power-series inequality follows from n!>=2*3^(n-2) for n>=2. The associated stopped nonnegative exponential supermartingale and the choice `theta=x/(v+bx/3)` give

    P{sup M>=x}<=exp[-x^2/(2(v+bx/3))].

Apply also to -M when needed. The A and A^2 clock denominators, after cancellation, are `200000+2/3<200002`. Their joint exit probability is therefore at most `2 exp(-e/200002)`.

## 4. Corrected-F drift and its O(m) bracket

The actual total band supplies

    |1-B/N|<=delta+4m/N+2e/N.

The remaining AE coefficient in LF is bounded by

    delta+(269/32)(m/N)+8e/N+2/N <32*10^-50.

Since `int AE<=2e Hbar=2*10^4m`, this term costs at most `640000*10^-50*m`. The remaining absolute drift terms, divided by m, are bounded by positive combinations of rho, rho^3, rho/m and rho/N. Explicitly, apart from the time terms they are at most

    10000rho/m +20000rho+30000000rho+32rho/m
      +80000rho^3+625000rho^3+7500000rho/N
      +640000*10^-50.

For the cubic term, A(A-1)^2<=A^3 for nonnegative integer A; A=0 and A=1 cause no exception. Immigration and E/N contribute at most `(1+2rho)T<4T`. The displayed monotone envelope is below `10^9*10^-50*m+4T<m/64` for every admitted N,m.

The complete bracket decomposition is:

- AB->CD, CD->AB, CD->AE and AE->CD have total compensator at most `2NHbar+12m^2T+2eHbar<50000e`. Their absolute F marks are <=2e/N, giving <=`200000me/N`.
- AE->2A has compensator <=20000m and marks <=2, giving <=80000m.
- AC/AD->2A have compensator <=4mHbar and marks <=1.
- All three 2A-source channels have total compensator <=3Jbar and marks <=2.
- Port channels have compensator <=T+Hbar and marks <=2.

The sum divided by m is at most

    80000 +200000rho+40000rho+120000000rho
       +4T/m+40000rho/m <2*10^8.

Every full F mark is <=2: the slow marks are bounded by `1+5rho+rho^2/16+7/(4N)<2`, AC/AD marks by `1/2+2rho<1`, and the small CD/AE marks satisfy their stated bound including the 1/(4N) term. Thus no rare omitted channel or oversized mark is hidden in the concentration step.

For x=m/64, the Bernstein denominator after cancellation is

    8192*(2*10^8+1/96)<3*10^12.

Hence `P{sup |MF|>m/64}<=2exp[-m/(3*10^12)]`. Together with initial |F|<=m/8 and the drift bound, the entire stopped path has `|F|<=5m/32<m/4` on this event. This excludes its F boundary, including terminal jumps. The O(m) bracket is genuine; replacing the frequent small marks by order-one marks would indeed destroy it.

## 5. E, imbalance and the fast-A excursion calculation

The E marks have absolute size one and

    <ME> <=Jbar+4eHbar+8m^2T
          <=[10^7rho^2+40000rho+128]e <50000e.

Bernstein at e/100 gives the stated `2exp[-e/(2*10^9)]` bound. The exact LE identity has nonnegative A(A-1), hence

    E(t)-E(0)>=2int CD-2int AE+ME(t),
    2int AE<=40000m<e/100.

Thus on its good martingale event E decreases by less than e/50 at any stopped time.

For Z, `<MZ><=(2*10^7+40000)me/N<3*10^7me/N<=3*10^7m`, with unit marks. Variation of constants for `dZ=-AZdt+dMZ`, followed by integration by parts against its damping kernel, gives pathwise

    sup |Z| <= |Z(0)|+2sup |MZ|.

The kernel has nonnegative total mass at most one because A>=0. With sup |MZ|<=m/128, this is `<m/16`; the +1 in the entry bound is included. Bernstein's canceled denominator `32768*(3*10^7+1/384)` is less than `2*10^12`, proving the quoted Z probability.

For A, it is necessary to count unsuccessful excursions; a single favorable next-jump path would not suffice. The actual upward intensity is `1+A(C+D)+AE+3CD`, bounded by `13m^2+6eA`. Downward intensity is at least AB>=NA/2. Elementary `exp(1)-1<2` and `1-exp(-1)>1/2` give

    L exp(A)/exp(A)
       <=26m^2+12eA-NA/4 <=26m^2-NA/8.

Thus exp(A), stopped while A>=a0=ceil(208m^2/N) and inside the remaining tube, is a supermartingale. The uniform inequality `208m/N+1/m<1/64` gives a0<=m/64.

An excursion starting at a0+1 and stopped upon return to a0, reaching m/16 or any other common stop therefore has upper-hit probability at most

    exp(a0+1-m/16)<=exp(-m/32).

The possible initial excursion costs at most `exp(A(0)-m/16)<=exp(-m/64)`. All A jumps are +/-1, so every later excursion has a distinct upward crossing into a0+1. Its expected number is bounded by the expected total upward event count before sigma:

    13m^2T+6eHbar <=[208+60000rho]e<10^5e.

Conditional optional stopping at each excursion start and summing these conditional probabilities is legitimate; independence of excursions is not used. The total A-hit probability is bounded by

    exp(-m/64)+10^5e exp(-m/32).

Since e<=N<=m^5, this is <=`2exp(-m/128)` for m>=10^6. A uniform elementary check is `log(10^5)<15`, `log m<=sqrt(m)` and, for u=sqrt(m)>=1000,

    15+5u <=3u^2/128.

The latter quadratic is positive and increasing beyond 1000. This proves absorption of the polynomial excursion count, rather than just evaluating the inequality at one giant fixture. The actual hypothesis m>=10^80 is substantially stronger.

## 6. No missing tube event and correct transfer

Let the good event exclude the two clock events and the F/E/Z/A martingale or barrier events just bounded, all defined through the common stopped path and including terminal marks. The F, Z, A and clock boundaries are excluded by their bounds. For E and L the exact corrected-variable identity closes the remaining possibilities.

At entry, F(0)<=m/8 and L(0)>=m imply

    E(0)^2 >=7Nm/6.

Therefore on the good E event

    E>=sqrt(7/6)e-e/50>1.06e.

The strict inequality is exact: `(27/25)^2<7/6`. Even allowing post-jump A<=m/16+1 and E<=2e+1, `AE/N<m/100`. Thus

    L=F+3E^2/(4N)-AE/N
      >[-1/4+(3/4)(1.06)^2-1/100]m >m/2.

No lower-L crossing is missed by an overshoot. The E lower exit is excluded by the same lower bound. At E>=2e, the identity would require `3E^2/(4N)>=3m`, whereas before an L success the right side `L+AE/N-F` is at most `(2+1/m+1/100+1/4)m<3m`, including a possible terminal L overshoot. Thus the upper E exit cannot occur on the good event either.

If no upper-L or total-band outcome occurs by T, the whole tube persists and

    CD=(L-A)^2-Z^2/4
       >=[(7/16)^2-1/1024]m^2 >m^2/8.

The exact E equation then implies

    E(T)-E(0) >=(m^2/4)T-40000m-e/100 >3.98e,

contradicting its tube. Consequently the good event forces the disjunction in (4).

At an L-success **with no total-band exit**, L is in [2m,2m+1], the post-jump A/Z bounds are at most m/16+1, and |F|<=5m/32<(2m)/8. The exact identity yields

    E^2/(Nm) >=(4/3)(2-5/32)>2,
    E^2/(Nm) <=(4/3)(2+1/m+1/100+5/32)<169/50.

These are precisely `sqrt(2Nm)<=E<=(13/10)sqrt(2Nm)`, and all next-stage entrance conditions follow. This transfer is to the same actual state with fixed reference N; B is never frozen.

The probability sum contains at most ten exponential terms:

    2 exp(-e/200002)
    +2 exp(-m/(3*10^12))
    +2 exp(-e/(2*10^9))
    +2 exp(-m/(2*10^12))
    +2 exp(-m/128).

Since e>=m and all other denominators are below 3*10^12, this is at most `10 exp(-m/(3*10^12))`, strictly below the claimed 16-term envelope. No additional unpriced boundary event was found after adopting the explicit stopping conventions above.

The tie convention is not cosmetic. The saved exact example has N=10^250, m=10^100, pre-jump A=0, C=D=2m-1, E=floor(sqrt(4N(2m-1)/3)), and B chosen so the actual total is exactly (1+delta)N. F is small and all relevant state coordinates are nonnegative. One immigration then hits L=2m and puts total above the band simultaneously. This is a kinematic counterexample to unconditional next-entrance transfer, not a counterexample to (4): its band outcome is already included in that disjunction. No probability lower bound or entire entrance-to-witness path is asserted by this diagnostic.

## 7. Composition and the limits of the received component

Apply the same conditional stage estimate at successive genuine in-band L-success times, using scales m_j=2^j m0. Stop composition at either band exit, at its desired final actual level, or at the first exceptional stage. There are finitely many stages and no resets. Conditional bounds and a union bound give

    sum_j 16 exp(-2^j m0/Cstar)
      <=32 exp(-m0/Cstar),

because m0/Cstar>=1 and `2^j>=j+1`. The deadline sum is exactly bounded by the displayed geometric series with ratio `2^(-3/2)`, yielding the stated O(N^(1/5)/K^(3/2)) paid time. No separate O(log N) factor is lost in the exponentially decreasing failure sum.

For a literal final level between delta N and 2 delta N, stopping at the first actual L>=delta N gives [delta N,delta N+1]. Reporting the final dyadic-stage endpoint instead requires retaining its +1 overshoot. Neither choice changes the upper deadline or the failure bound.

**Both mass-band exits count in (4).** An upper-band exit is not amplification or removal service. Moreover (3) permits the entrance total to be already at the upper edge, so this stage does not by itself give a uniformly exponentially small upper-exit probability. A future immigration estimate must receive the actual starting headroom and charge the actual unit Poisson immigration count over the paid horizon. A lower-band exit puts total below the fixed reference level (1-delta)N; it is not necessarily a delta-fraction reduction from every permitted stage-entry total, which might already be at the lower edge. These distinctions prevent a conditional disjunction from silently becoming a return-time consumer.

The review does **not** receive an initial-phase entrance from x_N, arbitrary-state entry, an exponential entrance-failure estimate, long interior occupation, a renewal/recurrence theorem or any stationary moment bound. The companion fixed-level mesoscopic result uses a killed omitted-channel coupling and a convergence-in-probability statement. Its role cannot be upgraded merely by this stage. The sentence saying it receives the full entrance “with probability tending to one” is not independently granted here as a separate initial-phase theorem; in particular fast-A control at a hitting time and any desired quantitative entrance rate must be supplied at that boundary. The task explicitly concerns only the already received entrance (3).

This audit does not use the deterministic complex-balanced realization or its cited primary theorem to fill any stochastic step. Those remain separate material. No physical implementation, observation/clock acquisition or numerical evaluation budget for the algebraic/exponential constants is established. The stage constants are extraordinarily conservative mathematical existence costs, not practical rates.

## Evidence and preservation

`POLYNOMIAL_IDENTITIES.json` contains the global coefficient identities; `CHECK_RESULTS.json` records 1,393 independent exact assertions. Normalized-envelope tests are consequences of the entire admissible parameter range, while random small-state evaluations only check the polynomial engine. `SIMULTANEOUS_EXIT_WITNESS.json` records the stopping-convention witness. All source bytes, author manifest and read companion are preserved in `inputs/`; no author executable was imported and no source was edited. The author finite-test results are bound as supplied evidence, not claimed as this audit's fresh replay.

The final manifest binds this derivation, a source-bound acceptance with the controlling stopping interpretations, exact check code/results and all inputs. Final source/audit readback is performed before releasing hashes. No helper, external retrieval, denied-source retry, operational action, publication or equipment was used. The only required qualifications are the explicit stopping/endpoint interpretations and the narrow conditional scope stated above; no nonuniform numerical constant or missing martingale/clock cost remains in the received stage estimate.
