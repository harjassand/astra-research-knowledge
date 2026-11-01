# Independent stopped charging-domain audit: PASS

## Exact admitted scope

The immutable sources are `FULL_GENERATOR_STOPPED_DRIFT.md` SHA256
`3c8dcd58970fa40589bb1f9b45e254ddd01ad1d6a0117249e3f2420285e9fd27`,
`STRENGTHENED_CUTOFF_TWO.md` SHA256
`6aae3e98af55eda8500d34b5add9cb3e9c9ff5df938a32c566d9d44184d8e5b7`, and
`UNIFORM_PAID_CHARGING_COROLLARY_PENDING.md` SHA256
`58ced3a6c4d0248140bde1a2a3a7a24547ef80ba228cca01289b779db0d05f95`.
All three were read in full and their original bytes were not edited.

The original cutoff-100 result and the stronger cutoff-2 result are accepted for the exact twelve-channel falling-factorial rate-2 model in the first source. In particular, for EVERY real 1 <= r <= 101/100 and EVERY integer state with t=tau >= 2,

 LV/V <= -[3/20 + 10 A^2 + t/4 {AC/(d+t+1)+AD/(c+t+1)}].

The r=1 endpoint is explicitly admitted, not inferred from a claimed positive-tilt conclusion. The paid charging-time and population corollary is accepted. These are stopped charging-domain statements, not a global Lyapunov theorem, not a population-reduction block, and not a stationary-moment theorem. No new runtime admission/certificate interface is claimed.

## Independent analytic review

1. The twelve raw stoichiometric jumps give the stated changes in c=A+C, d=A+D, H=(B-A-99E)/100 and total N. All non-port jumps conserve N. With t>=2, H>=2t^3/3>=16/3, so every actual one-jump neighbor still has H>0. All generator ratios use its actual positive root, not an artificially reset or killed value.

2. The structural bounds follow directly from B=A+Z-E>(1-a)Z and H=qP<=aZ: cd/(B+1)<=1/(198t), A^2/(B+1)<=1/(198t), 1/(B+1)<=3/(198t^3), E/(B+1)<=1/99. Hence h<=104/99 on t>=2, and h<=991/990 on t>=100. There is no balanced-arm assumption.

3. The polynomial shift identity is exact. It bounds every death/forward debt increase by one. A legal death has c,d>=1, so qP(c-1,d-1,1)>=2/3>a. Immigration and reverse AC/AD strictly decrease debt, and AB<->CD is exactly debt-neutral. The reverse-arm decrease is less than one by the shifted-polynomial comparison.

4. The two AE exits must be grouped. Their actual debt changes are -s and +delta, with 0<s<1, delta<=1/(2t^2)<=1/8, and s/delta>=44/9>4. Consequently 1-exp(-s)>4delta/3 and exp(delta)-1<=8delta/7, so their base sum is nonpositive. Their weighted phase sum is also correctly bounded: for A>=1,
 (2A+1)exp(-s)+(1-2A)exp(delta)<=2.
This follows by maximizing the expression over A>=1 at A=1, then using 3exp(-s)-exp(delta)<=2. No derivative-only cancellation is used.

5. The exact product identity separates h times the base drift from exp(z) times the phase differences. The AB->CD phase term is exactly -20A(2A-1)+20A^3/(B+1); its denominator after the jump really is B, and a legal AB jump has B>=1. Port death and all forward 2A phase terms are nonpositive. The remaining positive costs in the source pay all three reverse arms, CD exits, immigration, and the AB remainder. The total phase bound is
 -20A(2A-1)+20 theta(t,r) A,
 theta=16/(198t)+2/99+9r/(198t^3).
At t=2,r=101/100, theta=3503/52800<1/15. Relaxing the first term to -20A^2 yields at most -56A^2/3. The base positive budget is less than 7A^2. Thus -35A^2/3 remains before division by h, separately retaining the negative AC/AD base terms; their positive phase costs were already paid. Since (35/3)(99/104)=1155/104>10+3/20, the asserted A>=1 reserve follows.

6. For reverse AC, the MVT lower bound is s_C>=t/[2(d+t+1)], and analogously s_D>=t/[2(c+t+1)]. Because both are below one, concavity gives 1-exp(-s)>=s/2. This earns exactly the quantitative AC/AD reserve, including arbitrarily unbalanced arms. No reserve has been spent twice.

7. At A=0 only immigration and the two CD exits are active. With beta=1-cd/[(c+t)(d+t)], rho=(t/(t+1))^2, eta=1-1/(4t^2), the base bound is r exp(-rho beta)-1-eta(1-beta). This is convex in beta, so its endpoint maximum suffices. One logical detail is made explicit here: for charging decrease s_c>=v=1/[q(c+t)(d+t)], first use monotonicity exp(-s_c)-1<=exp(-v)-1, THEN apply the quadratic Taylor upper bound at v; do not substitute s_c into a nonmonotone quadratic. At t>=2, the endpoints are <=-4319/12500 and the phase cost <=501/2640. Their sum is below -3/20 by the exact margin 3161/550000. At t>=100 the source's rational endpoint estimates give base<-3/5 and phase<1/100. The original -1/2 bound therefore also holds.

## Actual process, localization, and stopped cost

The only N-increasing reaction is unit-rate immigration. Pathwise N_s<=N_0+I_s for a unit Poisson count. A fixed N sublevel has finitely many states and bounded rates, which together with this domination proves nonexplosion. Globally tau<=(3aN/q)^(1/3) and V<=r^N exp((3aN/q)^(1/3))(1+20N^2). Finite-horizon suprema therefore have finite expectation by Poisson exponential moments. Localization on finite population sublevels and dominated convergence justify stopped Dynkin with actual exit values. The root kink at H=0 does not require differentiability; the generator uses finite differences, and no positive-root interior estimate is asserted there.

For sigma_2=inf{s>=0:tau(X_s)<2}, gamma=3/20,
 E_x[exp(gamma(T wedge sigma_2)) V(X_(T wedge sigma_2))] <= V(x).
Since V>=1, Fatou implies sigma_2<infinity almost surely and E exp(gamma sigma_2)<=V(x). The cutoff100 analogue has gamma=1/2. The same reasoning retains the integrated reserve R=10A^2+t/4[AC/(d+t+1)+AD/(c+t+1)]:
 E[exp(gamma stop)V(X_stop) + integral_0^stop exp(gamma s) R(X_s)V(X_s) ds] <= V(x).
R is polynomially bounded in N on the stopped domain, so the same finite-horizon localization applies. This is an additional direct consequence, not a claim of globally paid service.

## Uniform paid charging corollary

At r=1, for initial N>=1, tau< N^(1/3)/4 and h<=21N^2. Using log N<=3(N^(1/3)-1) and log21<6 gives log V<=25N^(1/3)/4<=7N^(1/3). Markov at time 100N^(1/3) yields failure <=exp(-8N^(1/3)), uniformly over every initial state (sigma=0 is harmless below cutoff).

For N>=3000, 100N^(1/3)<=N/2 since 3000^2>200^3. The event {N(X_sigma)>2N, sigma<=100N^(1/3)} is contained in {I_(100N^(1/3))>N}. Chernoff at log2 gives <=exp[-(log2-1/2)N]<exp(-N/6), since log2>2/3. This is event inclusion, not independence at a stopping time. The exit relation aZ<E+4cd+4(c+d)+16/3 follows by monotonicity of the cubic; H<=0 is also covered. It does not supply A-occupation, actual removal, a prepared exit, or repeat-crossing payment.

## Independent executable supplements and reproduction

`independent_finite_jump_checks.py` imports no author program. It builds the raw twelve-channel stoichiometric ledger itself, computes each actual post-jump state, brackets cubic roots by rational bisection (128 steps), and bounds exponential ratios by exact rational Taylor sums with a geometric remainder (degree40). It evaluates LV/V, not a truncated or selected-channel drift. There are 216 states and 648 exact interval checks at r=1, 1000001/1000000,101/100, covering t near2,3,100, A=0/1/2/20, E=0/10^12, and arms as unbalanced as 10^9 versus0. All strengthened-reserve inequalities passed, including 54 A=0 states, 162 positive-A states, 12 ledger rows, 64 shift-identity instances, and five corollary constant checks. Finite tests supplement rather than establish the uniform proof above.

To reproduce, copy the script and three admitted source files into a fresh directory, then run `PYTHONDONTWRITEBYTECODE=1 python independent_finite_jump_checks.py`. It writes `INDEPENDENT_CHECKS.json` next to itself. A clean replay produced byte-identical JSON, SHA256 `5181e85c224798114f66aeedf68b92e9caf3a207a0276261641edde80ba28317`. Initial time 6.88426084799903 seconds and replay time 6.195831799999723 seconds differ honestly; no deterministic timing claim is made. No giant power is expanded. Input hashes are rechecked by the final audit binding.

## Remaining obligations / exclusions

No defect was found in these admitted mathematical statements. The region tau<2 is not received, repeated crossings are not paid, and no uniform population-reduction block (H) is established. Thus global positive recurrence and an actual stationary exponential moment for this rate-2 network remain UNKNOWN from this component. The separate N-denominator repair is not covered by this receipt. Original sources and prior audit receipts remain unchanged.
